from __future__ import annotations

import json
from pathlib import Path

from domainrag.bm25s_retrieval import run_bm25s_retrieval
from tests.test_validator import _write_minimal_dataset


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_run_bm25s_retrieval_writes_domainrag_rows(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    result_path = run_bm25s_retrieval(dataset, output, split="dev", top_k=2)

    rows = _rows(result_path)
    assert result_path == output / "dataset" / "dev_bm25s_results.jsonl"
    assert len(rows) == 1
    row = rows[0]
    assert row["method"] == "bm25s_oracle_reader"
    assert row["split"] == "dev"
    assert row["id"] == "q000001"
    assert row["gold_context_ids"] == ["d000001"]
    assert row["retrieved_context_ids"][0] == "d000001"
    assert row["scores"]["retrieval_hit"] == 1.0
    assert row["scores"]["retrieval_mrr"] == 1.0
    assert row["api_calls"] == 0
    assert row["error"] is None
