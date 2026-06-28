from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import re
from typing import Any

import numpy as np

from domainrag.benchmark_runner import _gold_prediction, _retrieval_scores
from domainrag.dataset_adapter import load_split
from domainrag.domain_evaluator import evaluate_record
from domainrag.io_utils import read_jsonl, read_qrels, write_jsonl
from domainrag.prompt_renderer import render_prompt
from domainrag.validator import validate_dataset


HASHED_DENSE_METHOD = "hashed_dense_oracle_reader"
HASHED_DENSE_RERANK_METHOD = "hashed_dense_lexical_rerank_oracle_reader"
QRELS_FILE_BY_SPLIT = {
    "dev": "dev.tsv",
    "test": "test.tsv",
    "fresh_hard": "fresh_hard.tsv",
}
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


def retrieve_hashed_dense(
    query: str,
    corpus: dict[str, str],
    *,
    top_k: int,
    dimensions: int = 512,
) -> list[tuple[str, float]]:
    index = HashedDenseIndex.build(corpus, dimensions=dimensions)
    return index.retrieve(query, top_k=top_k)


def run_hashed_dense_benchmark(
    dataset_dir: Path,
    output_dir: Path,
    *,
    split: str = "dev",
    top_k: int = 5,
    dimensions: int = 512,
) -> Path:
    _validate_retrieval_parameters(top_k=top_k, dimensions=dimensions)
    validate_dataset(dataset_dir)
    records = load_split(dataset_dir, split)
    corpus = _load_corpus(dataset_dir)
    qrels = _load_positive_qrels(dataset_dir / "qrels" / QRELS_FILE_BY_SPLIT[split])
    index = HashedDenseIndex.build(corpus, dimensions=dimensions)

    output_records: list[dict[str, Any]] = []
    for record in records:
        output_records.append(
            _build_output_row(
                record=record,
                split=split,
                gold_context_ids=qrels.get(record["id"], []),
                retrieved=index.retrieve(record["question"], top_k=top_k),
                method=HASHED_DENSE_METHOD,
                metadata={
                    "benchmark_family": "local_hashed_dense",
                    "neural_model": False,
                    "vectorizer": "signed_hashing_tfidf",
                    "dimensions": dimensions,
                    "top_k": top_k,
                    "reranker": None,
                },
            )
        )
        output_records.append(
            _build_output_row(
                record=record,
                split=split,
                gold_context_ids=qrels.get(record["id"], []),
                retrieved=index.retrieve_with_lexical_rerank(record["question"], top_k=top_k),
                method=HASHED_DENSE_RERANK_METHOD,
                metadata={
                    "benchmark_family": "local_hashed_dense",
                    "neural_model": False,
                    "vectorizer": "signed_hashing_tfidf",
                    "dimensions": dimensions,
                    "top_k": top_k,
                    "reranker": "lexical_overlap",
                },
            )
        )

    result_path = output_dir / dataset_dir.name / f"{split}_hashed_dense_results.jsonl"
    write_jsonl(result_path, output_records)
    return result_path


@dataclass(frozen=True)
class HashedDenseIndex:
    corpus: dict[str, str]
    dimensions: int
    document_frequencies: dict[str, int]
    vectors: dict[str, np.ndarray]

    @classmethod
    def build(cls, corpus: dict[str, str], *, dimensions: int = 512) -> "HashedDenseIndex":
        _validate_retrieval_parameters(top_k=1, dimensions=dimensions)
        document_frequencies = _document_frequencies(corpus)
        vectors = {
            context_id: _normalized_hashed_vector(
                _tokens(contents),
                document_frequencies=document_frequencies,
                corpus_count=len(corpus),
                dimensions=dimensions,
            )
            for context_id, contents in corpus.items()
        }
        return cls(
            corpus=corpus,
            dimensions=dimensions,
            document_frequencies=document_frequencies,
            vectors=vectors,
        )

    def retrieve(self, query: str, *, top_k: int) -> list[tuple[str, float]]:
        _validate_retrieval_parameters(top_k=top_k, dimensions=self.dimensions)
        query_vector = _normalized_hashed_vector(
            _tokens(query),
            document_frequencies=self.document_frequencies,
            corpus_count=len(self.corpus),
            dimensions=self.dimensions,
            skip_oov=True,
        )
        scored = [
            (context_id, float(np.dot(query_vector, vector)))
            for context_id, vector in self.vectors.items()
        ]
        scored.sort(key=lambda item: (-item[1], item[0]))
        return scored[:top_k]

    def retrieve_with_lexical_rerank(
        self,
        query: str,
        *,
        top_k: int,
        rerank_candidates: int | None = None,
        lexical_weight: float = 0.2,
    ) -> list[tuple[str, float]]:
        _validate_retrieval_parameters(top_k=top_k, dimensions=self.dimensions)
        candidate_count = rerank_candidates or min(len(self.corpus), max(top_k * 4, top_k))
        dense_candidates = self.retrieve(query, top_k=candidate_count)
        query_tokens = _tokens(query)
        reranked: list[tuple[str, float]] = []
        for context_id, dense_score in dense_candidates:
            lexical_score = _weighted_overlap_score(
                query_tokens,
                _tokens(self.corpus[context_id]),
                document_frequencies=self.document_frequencies,
                corpus_count=len(self.corpus),
            )
            reranked.append((context_id, dense_score + lexical_weight * lexical_score))
        reranked.sort(key=lambda item: (-item[1], item[0]))
        return reranked[:top_k]


def _load_corpus(dataset_dir: Path) -> dict[str, str]:
    return {
        record["id"]: record["contents"]
        for record in read_jsonl(dataset_dir / "corpus.jsonl")
    }


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
    retrieved: list[tuple[str, float]],
    method: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    prompt = render_prompt(record)
    retrieved_context_ids = [context_id for context_id, _score in retrieved]
    prediction = (
        _gold_prediction(record)
        if set(retrieved_context_ids) & set(gold_context_ids)
        else ""
    )
    scores = evaluate_record(record, prediction)
    scores.update(_retrieval_scores(gold_context_ids, retrieved_context_ids))
    return {
        "id": record["id"],
        "method": method,
        "split": split,
        "prompt": prompt,
        "prediction": prediction,
        "golden_answers": record["golden_answers"],
        "gold_context_ids": gold_context_ids,
        "retrieved_context_ids": retrieved_context_ids,
        "retrieval_scores": [score for _context_id, score in retrieved],
        "scores": scores,
        "latency_ms": 0.0,
        "input_tokens": len(prompt.split()),
        "output_tokens": len(prediction.split()),
        "api_calls": 0,
        "error": None,
        "metadata": metadata,
    }


def _validate_retrieval_parameters(*, top_k: int, dimensions: int) -> None:
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    if dimensions < 8:
        raise ValueError("dimensions must be at least 8")


def _normalized_hashed_vector(
    tokens: list[str],
    *,
    document_frequencies: dict[str, int],
    corpus_count: int,
    dimensions: int,
    skip_oov: bool = False,
) -> np.ndarray:
    vector = np.zeros(dimensions, dtype=np.float64)
    if not tokens:
        return vector
    counts = Counter(tokens)
    token_count = sum(counts.values())
    for token, count in counts.items():
        if skip_oov and token not in document_frequencies:
            continue
        index, sign = _hash_index_and_sign(token, dimensions)
        term_frequency = count / token_count
        inverse_document_frequency = _idf(token, document_frequencies, corpus_count)
        vector[index] += sign * term_frequency * inverse_document_frequency
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def _hash_index_and_sign(token: str, dimensions: int) -> tuple[int, float]:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    value = int.from_bytes(digest, byteorder="big", signed=False)
    index = value % dimensions
    sign = 1.0 if value & (1 << 63) else -1.0
    return index, sign


def _document_frequencies(corpus: dict[str, str]) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for contents in corpus.values():
        for token in set(_tokens(contents)):
            frequencies[token] = frequencies.get(token, 0) + 1
    return frequencies


def _weighted_overlap_score(
    query_tokens: list[str],
    document_tokens: list[str],
    *,
    document_frequencies: dict[str, int],
    corpus_count: int,
) -> float:
    query_set = set(query_tokens)
    document_set = set(document_tokens)
    if not query_set:
        return 0.0
    total_weight = sum(_idf(token, document_frequencies, corpus_count) for token in query_set)
    if total_weight == 0:
        return 0.0
    matched_weight = sum(
        _idf(token, document_frequencies, corpus_count)
        for token in query_set & document_set
    )
    return matched_weight / total_weight


def _idf(token: str, document_frequencies: dict[str, int], corpus_count: int) -> float:
    return math.log((1 + corpus_count) / (1 + document_frequencies.get(token, 0))) + 1.0


def _tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]
