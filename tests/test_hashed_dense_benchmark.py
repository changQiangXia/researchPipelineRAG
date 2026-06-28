from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.hashed_dense_benchmark import (
    HASHED_DENSE_METHOD,
    HASHED_DENSE_RERANK_METHOD,
    retrieve_hashed_dense,
    run_hashed_dense_benchmark,
)
from tests.test_validator import _write_minimal_dataset


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_retrieve_hashed_dense_ranks_matching_context_first():
    corpus = {
        "d1": "Nickel superalloy creep rupture involves gamma prime rafting and oxidation.",
        "d2": "Battery thermal runaway involves electrolyte decomposition and gas release.",
        "d3": "Concrete bridge inspection records crack width and corrosion stains.",
    }

    retrieved = retrieve_hashed_dense(
        "Which nickel superalloy context discusses gamma prime creep rupture?",
        corpus,
        top_k=2,
        dimensions=64,
    )

    assert [context_id for context_id, _score in retrieved] == ["d1", "d2"]
    assert retrieved[0][1] > retrieved[1][1]


def test_run_hashed_dense_benchmark_writes_domainrag_rows_for_both_methods(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    result_path = run_hashed_dense_benchmark(
        dataset,
        output,
        split="dev",
        top_k=2,
        dimensions=64,
    )

    rows = _rows(result_path)
    assert result_path == output / "dataset" / "dev_hashed_dense_results.jsonl"
    assert [row["method"] for row in rows] == [
        HASHED_DENSE_METHOD,
        HASHED_DENSE_RERANK_METHOD,
    ]
    for row in rows:
        assert row["split"] == "dev"
        assert row["id"] == "q000001"
        assert row["gold_context_ids"] == ["d000001"]
        assert row["retrieved_context_ids"][0] == "d000001"
        assert row["scores"]["retrieval_hit"] == 1.0
        assert row["scores"]["retrieval_mrr"] == 1.0
        assert row["api_calls"] == 0
        assert row["error"] is None
        assert row["metadata"]["benchmark_family"] == "local_hashed_dense"
        assert row["metadata"]["neural_model"] is False


def test_run_hashed_dense_benchmark_rejects_invalid_parameters(tmp_path: Path):
    dataset = tmp_path / "dataset"
    _write_minimal_dataset(dataset)

    with pytest.raises(ValueError, match="top_k must be positive"):
        run_hashed_dense_benchmark(dataset, tmp_path / "out", top_k=0)

    with pytest.raises(ValueError, match="dimensions must be at least 8"):
        run_hashed_dense_benchmark(dataset, tmp_path / "out", dimensions=4)
