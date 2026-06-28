from __future__ import annotations

from pathlib import Path
from typing import Any

from domainrag.benchmark_runner import _gold_prediction, _retrieval_scores
from domainrag.dataset_adapter import load_split
from domainrag.domain_evaluator import evaluate_record
from domainrag.io_utils import read_jsonl, read_qrels, write_jsonl
from domainrag.prompt_renderer import render_prompt
from domainrag.validator import validate_dataset


METHOD_NAME = "bm25s_oracle_reader"
QRELS_FILE_BY_SPLIT = {
    "dev": "dev.tsv",
    "test": "test.tsv",
    "fresh_hard": "fresh_hard.tsv",
}


def run_bm25s_retrieval(
    dataset_dir: Path,
    output_dir: Path,
    *,
    split: str = "dev",
    top_k: int = 5,
) -> Path:
    import bm25s

    if top_k <= 0:
        raise ValueError("top_k must be positive")
    validate_dataset(dataset_dir)
    records = load_split(dataset_dir, split)
    corpus = _load_corpus(dataset_dir)
    qrels = _load_positive_qrels(dataset_dir / "qrels" / QRELS_FILE_BY_SPLIT[split])

    corpus_texts = [record["contents"] for record in corpus]
    corpus_tokens = bm25s.tokenize(corpus_texts, show_progress=False)
    retriever = bm25s.BM25(corpus=corpus)
    retriever.index(corpus_tokens, show_progress=False)

    query_tokens = bm25s.tokenize(
        [record["question"] for record in records],
        show_progress=False,
    )
    retrieved_docs, retrieval_scores = retriever.retrieve(
        query_tokens,
        k=top_k,
        show_progress=False,
        n_threads=1,
    )
    output_records = [
        _build_output_row(
            record=record,
            split=split,
            gold_context_ids=qrels.get(record["id"], []),
            retrieved_docs=[dict(doc) for doc in docs],
            retrieval_scores=[float(score) for score in scores],
        )
        for record, docs, scores in zip(records, retrieved_docs, retrieval_scores)
    ]
    result_path = output_dir / dataset_dir.name / f"{split}_bm25s_results.jsonl"
    write_jsonl(result_path, output_records)
    return result_path


def _load_corpus(dataset_dir: Path) -> list[dict[str, str]]:
    return [
        {
            "id": record["id"],
            "contents": record["contents"],
        }
        for record in read_jsonl(dataset_dir / "corpus.jsonl")
    ]


def _load_positive_qrels(path: Path) -> dict[str, list[str]]:
    qrels: dict[str, list[str]] = {}
    for query_id, corpus_id, score in read_qrels(path):
        if score > 0:
            qrels.setdefault(query_id, []).append(corpus_id)
    return qrels


def _build_output_row(
    *,
    record: dict[str, Any],
    split: str,
    gold_context_ids: list[str],
    retrieved_docs: list[dict[str, Any]],
    retrieval_scores: list[float],
) -> dict[str, Any]:
    prompt = render_prompt(record)
    retrieved_context_ids = [str(doc["id"]) for doc in retrieved_docs]
    prediction = (
        _gold_prediction(record)
        if set(retrieved_context_ids) & set(gold_context_ids)
        else ""
    )
    scores = evaluate_record(record, prediction)
    scores.update(_retrieval_scores(gold_context_ids, retrieved_context_ids))
    return {
        "id": record["id"],
        "method": METHOD_NAME,
        "split": split,
        "prompt": prompt,
        "prediction": prediction,
        "golden_answers": record["golden_answers"],
        "gold_context_ids": gold_context_ids,
        "retrieved_context_ids": retrieved_context_ids,
        "retrieval_scores": retrieval_scores,
        "scores": scores,
        "latency_ms": 0.0,
        "input_tokens": len(prompt.split()),
        "output_tokens": len(prediction.split()),
        "api_calls": 0,
        "error": None,
    }
