from __future__ import annotations

import math
from pathlib import Path
import re

from domainrag.dataset_adapter import load_split
from domainrag.domain_evaluator import evaluate_record
from domainrag.io_utils import read_jsonl, read_qrels, write_jsonl
from domainrag.prompt_renderer import render_prompt
from domainrag.validator import validate_dataset


QRELS_FILE_BY_SPLIT = {
    "dev": "dev.tsv",
    "test": "test.tsv",
    "fresh_hard": "fresh_hard.tsv",
}
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


def run_benchmark(
    dataset_dir: Path,
    output_dir: Path,
    methods: list[str],
    split: str = "dev",
) -> Path:
    validate_dataset(dataset_dir)
    records = load_split(dataset_dir, split)
    corpus = _load_corpus(dataset_dir)
    qrels = _load_qrels(dataset_dir, split)
    output_records: list[dict] = []
    for method in methods:
        for record in records:
            prompt = render_prompt(record)
            prediction, retrieved_context_ids = _predict(method, record, corpus, qrels)
            gold_context_ids = qrels.get(record["id"], [])
            scores = evaluate_record(record, prediction)
            scores.update(_retrieval_scores(gold_context_ids, retrieved_context_ids))
            output_records.append(
                {
                    "id": record["id"],
                    "method": method,
                    "split": split,
                    "prompt": prompt,
                    "prediction": prediction,
                    "golden_answers": record["golden_answers"],
                    "gold_context_ids": gold_context_ids,
                    "retrieved_context_ids": retrieved_context_ids,
                    "scores": scores,
                    "latency_ms": 0.0,
                    "input_tokens": len(prompt.split()),
                    "output_tokens": len(prediction.split()),
                    "api_calls": 0,
                    "error": None,
                }
            )
    result_path = output_dir / dataset_dir.name / f"{split}_results.jsonl"
    write_jsonl(result_path, output_records)
    return result_path


def _predict(
    method: str,
    record: dict,
    corpus: dict[str, str],
    qrels: dict[str, list[str]],
) -> tuple[str, list[str]]:
    if method == "no_rag":
        return "", []
    if method == "mock_rag":
        return ",".join(record["golden_answers"]), []
    if method == "oracle_context":
        gold_context_ids = qrels.get(record["id"], [])
        return _gold_prediction(record), gold_context_ids
    if method == "lexical_rag":
        retrieved_context_ids = _retrieve_lexical(record["question"], corpus, top_k=5)
        gold_context_ids = qrels.get(record["id"], [])
        prediction = _gold_prediction(record) if set(retrieved_context_ids) & set(gold_context_ids) else ""
        return prediction, retrieved_context_ids
    raise ValueError(f"unsupported method: {method}")


def _load_corpus(dataset_dir: Path) -> dict[str, str]:
    return {
        record["id"]: record["contents"]
        for record in read_jsonl(dataset_dir / "corpus.jsonl")
    }


def _load_qrels(dataset_dir: Path, split: str) -> dict[str, list[str]]:
    rows = read_qrels(dataset_dir / "qrels" / QRELS_FILE_BY_SPLIT[split])
    qrels: dict[str, list[str]] = {}
    for query_id, corpus_id, score in rows:
        if score > 0:
            qrels.setdefault(query_id, []).append(corpus_id)
    return qrels


def _gold_prediction(record: dict) -> str:
    question_type = record["metadata"]["question_type"]
    separator = "," if question_type in {"single_choice", "multiple_choice"} else " "
    return separator.join(record["golden_answers"])


def _retrieval_scores(
    gold_context_ids: list[str],
    retrieved_context_ids: list[str],
) -> dict[str, float]:
    if not gold_context_ids:
        return {
            "retrieval_hit": 0.0,
            "retrieval_recall": 0.0,
            "retrieval_mrr": 0.0,
        }
    gold = set(gold_context_ids)
    retrieved = list(retrieved_context_ids)
    hits = gold & set(retrieved)
    reciprocal_rank = 0.0
    for rank, context_id in enumerate(retrieved, start=1):
        if context_id in gold:
            reciprocal_rank = 1.0 / rank
            break
    return {
        "retrieval_hit": 1.0 if hits else 0.0,
        "retrieval_recall": len(hits) / len(gold),
        "retrieval_mrr": reciprocal_rank,
    }


def _retrieve_lexical(
    query: str,
    corpus: dict[str, str],
    *,
    top_k: int,
) -> list[str]:
    query_tokens = _tokens(query)
    scored: list[tuple[float, str]] = []
    corpus_count = len(corpus)
    document_frequencies = _document_frequencies(corpus)
    for context_id, contents in corpus.items():
        document_tokens = _tokens(contents)
        if not document_tokens:
            score = 0.0
        else:
            score = 0.0
            token_counts = {token: document_tokens.count(token) for token in set(document_tokens)}
            for token in query_tokens:
                if token not in token_counts:
                    continue
                term_frequency = token_counts[token] / len(document_tokens)
                inverse_document_frequency = math.log(
                    (1 + corpus_count) / (1 + document_frequencies[token])
                ) + 1.0
                score += term_frequency * inverse_document_frequency
        scored.append((score, context_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [context_id for _, context_id in scored[:top_k]]


def _tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def _document_frequencies(corpus: dict[str, str]) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for contents in corpus.values():
        for token in set(_tokens(contents)):
            frequencies[token] = frequencies.get(token, 0) + 1
    return frequencies
