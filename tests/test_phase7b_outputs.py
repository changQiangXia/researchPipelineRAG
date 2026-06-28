from __future__ import annotations

import json
from pathlib import Path

from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_medium_plus"
DATASET = ROOT / "data" / DATASET_NAME
FLASHRAG = ROOT / "outputs" / "flashrag" / DATASET_NAME
BASELINE = ROOT / "outputs" / "phase7b" / "medium_plus_baseline"
BM25 = ROOT / "outputs" / "phase7b" / "medium_plus_bm25s"
DOC = ROOT / "docs" / "verification" / "medium-plus-scale-expansion.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7b_medium_plus_dataset_and_flashrag_bundle_are_valid():
    validate_dataset(DATASET)
    statistics = json.loads((DATASET / "statistics.json").read_text(encoding="utf-8"))

    assert statistics["corpus_count"] == 100
    assert statistics["question_count"] == 150
    assert statistics["split_counts"] == {
        "dev": 50,
        "fresh_hard": 50,
        "test": 50,
    }
    assert len(_read_jsonl(FLASHRAG / "fresh_hard.jsonl")) == 50
    assert len(_read_jsonl(FLASHRAG / "corpus.jsonl")) == 100
    assert (FLASHRAG / "qrels" / "fresh_hard.tsv").exists()


def test_phase7b_medium_plus_baseline_and_bm25_outputs_have_real_retrieval_signal():
    baseline_rows = _read_jsonl(BASELINE / DATASET_NAME / "fresh_hard_results.jsonl")
    bm25_rows = _read_jsonl(BM25 / DATASET_NAME / "fresh_hard_bm25s_results.jsonl")

    assert len(baseline_rows) == 150
    assert {row["method"] for row in baseline_rows} == {
        "no_rag",
        "oracle_context",
        "lexical_rag",
    }
    assert len({row["id"] for row in baseline_rows}) == 50
    assert len(bm25_rows) == 50
    assert {row["method"] for row in bm25_rows} == {"bm25s_oracle_reader"}
    assert all(len(row["retrieved_context_ids"]) == 5 for row in bm25_rows)
    assert sum(row["scores"]["retrieval_hit"] for row in bm25_rows) >= 40.0
    assert any(row["scores"]["retrieval_recall"] < 1.0 for row in bm25_rows)


def test_phase7b_updates_audit_and_verification_doc_for_medium_plus_scale():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    demo_scale = requirements["demo_scale"]

    assert "Phase 7B" in doc
    assert "100 chunks / 150 questions" in doc
    assert audit["dataset"]["name"] == DATASET_NAME
    assert audit["dataset"]["corpus_chunks"] == 100
    assert audit["dataset"]["questions"] == 150
    assert demo_scale["status"] == "partial"
    assert "100 chunks and 150 questions" in demo_scale["summary"]
    assert "data/real_pilot_nickel_superalloy_medium_plus/statistics.json" in demo_scale["evidence"]
