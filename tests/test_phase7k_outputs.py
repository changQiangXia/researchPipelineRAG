from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_medium_plus"
OUTPUT = ROOT / "outputs" / "phase7k" / "hashed_dense_benchmark"
RESULTS = OUTPUT / DATASET_NAME / "fresh_hard_hashed_dense_results.jsonl"
REPORT = OUTPUT / "report_fresh_hard" / "summary.json"
DOC = ROOT / "docs" / "verification" / "hashed-dense-formal-benchmark.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7k_hashed_dense_outputs_run_on_medium_plus_fresh_hard():
    rows = _read_jsonl(RESULTS)
    summary = json.loads(REPORT.read_text(encoding="utf-8"))

    assert len(rows) == 100
    assert {row["method"] for row in rows} == {
        "hashed_dense_oracle_reader",
        "hashed_dense_lexical_rerank_oracle_reader",
    }
    assert {
        method: sum(1 for row in rows if row["method"] == method)
        for method in {row["method"] for row in rows}
    } == {
        "hashed_dense_oracle_reader": 50,
        "hashed_dense_lexical_rerank_oracle_reader": 50,
    }
    assert len({row["id"] for row in rows}) == 50
    assert all(row["split"] == "fresh_hard" for row in rows)
    assert all(row["api_calls"] == 0 for row in rows)
    assert all(row["error"] is None for row in rows)
    assert all(len(row["retrieved_context_ids"]) == 5 for row in rows)
    assert all(row["metadata"]["benchmark_family"] == "local_hashed_dense" for row in rows)
    assert all(row["metadata"]["neural_model"] is False for row in rows)

    for method in {
        "hashed_dense_oracle_reader",
        "hashed_dense_lexical_rerank_oracle_reader",
    }:
        assert summary[method]["questions"] == 50
        assert "retrieval_hit" in summary[method]["metrics"]
        assert summary[method]["api_calls"] == 0


def test_phase7k_updates_docs_and_audit_without_claiming_neural_dense_done():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    dense = requirements["dense_rerank_methods"]

    assert "Phase 7K" in doc
    assert "non-neural" in doc
    assert "hashed_dense_oracle_reader" in doc
    assert "hashed_dense_lexical_rerank_oracle_reader" in doc
    assert audit["phase"] == "Phase 7K"
    assert audit["phase7k_hashed_dense_benchmark"] == {
        "dataset": DATASET_NAME,
        "split": "fresh_hard",
        "questions": 50,
        "rows": 100,
        "methods": [
            "hashed_dense_oracle_reader",
            "hashed_dense_lexical_rerank_oracle_reader",
        ],
        "benchmark_family": "local_hashed_dense",
        "neural_dense_or_reranker_claim": "not_claimed",
        "outputs": [
            "outputs/phase7k/hashed_dense_benchmark/real_pilot_nickel_superalloy_medium_plus/fresh_hard_hashed_dense_results.jsonl",
            "outputs/phase7k/hashed_dense_benchmark/report_fresh_hard/summary.json",
            "docs/verification/hashed-dense-formal-benchmark.md",
        ],
    }
    assert dense["status"] == "partial"
    assert "local hashed dense benchmark" in dense["summary"]
    assert (
        "outputs/phase7k/hashed_dense_benchmark/real_pilot_nickel_superalloy_medium_plus/fresh_hard_hashed_dense_results.jsonl"
        in dense["evidence"]
    )
