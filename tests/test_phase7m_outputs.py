from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_demo_questions"
DATASET = ROOT / "data" / DATASET_NAME
PHASE_OUTPUT = ROOT / "outputs" / "archive" / "provenance" / "demo-dataset" / "demo-question-generation" / "demo_question_generation"
SUMMARY = PHASE_OUTPUT / "demo_question_summary.json"
FLASHRAG = ROOT / "outputs" / "flashrag" / DATASET_NAME
FLASHRAG_CONFIG = ROOT / "outputs" / "flashrag" / f"{DATASET_NAME}_flashrag.yaml"
BASELINE_RESULTS = PHASE_OUTPUT / "baseline" / DATASET_NAME / "fresh_hard_results.jsonl"
BASELINE_REPORT = PHASE_OUTPUT / "baseline" / "report_fresh_hard" / "summary.json"
HASHED_RESULTS = PHASE_OUTPUT / "hashed_dense" / DATASET_NAME / "fresh_hard_hashed_dense_results.jsonl"
HASHED_REPORT = PHASE_OUTPUT / "hashed_dense" / "report_fresh_hard" / "summary.json"
DOC = ROOT / "docs" / "verification" / "demo-question-generation.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7m_demo_question_dataset_reaches_provisional_question_target():
    statistics = json.loads((DATASET / "statistics.json").read_text(encoding="utf-8"))
    canonical = _read_jsonl(DATASET / "canonical_dataset.jsonl")
    dev = _read_jsonl(DATASET / "dev.jsonl")
    test = _read_jsonl(DATASET / "test.jsonl")
    fresh = _read_jsonl(DATASET / "fresh_hard_test.jsonl")
    dataset_card = (DATASET / "dataset_card.md").read_text(encoding="utf-8")
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert statistics["corpus_count"] == 100
    assert statistics["question_count"] == 300
    assert statistics["split_counts"] == {
        "dev": 100,
        "fresh_hard": 100,
        "test": 100,
    }
    assert statistics["question_type_counts"] == {
        "fill_blank": 75,
        "multiple_choice": 75,
        "short_answer": 75,
        "single_choice": 75,
    }
    assert len(canonical) == 300
    assert len(dev) == 100
    assert len(test) == 100
    assert len(fresh) == 100
    assert canonical[0]["id"] == f"{DATASET_NAME}_q0001"
    assert all(row["quality_score"] == 0.7 for row in canonical)
    assert "Provisional demo-question dataset" in dataset_card
    assert summary["phase"] == "Phase 7M"
    assert summary["provenance_status"] == "provisional_machine_generated_not_human_final"
    assert summary["final_demo_dataset_claim"] == "not_complete"


def test_phase7m_flashrag_and_local_result_outputs_are_present():
    fixture_chunks = _read_jsonl(PHASE_OUTPUT / "easy_dataset_export" / "chunks.jsonl")
    fixture_items = _read_jsonl(PHASE_OUTPUT / "easy_dataset_export" / "items.jsonl")
    baseline_rows = _read_jsonl(BASELINE_RESULTS)
    hashed_rows = _read_jsonl(HASHED_RESULTS)
    baseline_summary = json.loads(BASELINE_REPORT.read_text(encoding="utf-8"))
    hashed_summary = json.loads(HASHED_REPORT.read_text(encoding="utf-8"))

    assert len(fixture_chunks) == 100
    assert len(fixture_items) == 300
    assert len(_read_jsonl(FLASHRAG / "dev.jsonl")) == 100
    assert len(_read_jsonl(FLASHRAG / "test.jsonl")) == 100
    assert len(_read_jsonl(FLASHRAG / "fresh_hard.jsonl")) == 100
    assert "dataset_name: real_pilot_nickel_superalloy_demo_questions" in (
        FLASHRAG_CONFIG.read_text(encoding="utf-8")
    )

    assert len(baseline_rows) == 300
    assert Counter(row["method"] for row in baseline_rows) == {
        "no_rag": 100,
        "oracle_context": 100,
        "lexical_rag": 100,
    }
    assert all(row["api_calls"] == 0 for row in baseline_rows)
    assert all(row["error"] is None for row in baseline_rows)
    assert baseline_summary["oracle_context"]["metrics"]["retrieval_hit"] == 1.0
    assert baseline_summary["lexical_rag"]["metrics"]["retrieval_hit"] == 0.72
    assert baseline_summary["no_rag"]["metrics"]["retrieval_hit"] == 0.0

    assert len(hashed_rows) == 200
    assert Counter(row["method"] for row in hashed_rows) == {
        "hashed_dense_oracle_reader": 100,
        "hashed_dense_lexical_rerank_oracle_reader": 100,
    }
    assert all(row["api_calls"] == 0 for row in hashed_rows)
    assert all(row["error"] is None for row in hashed_rows)
    assert all(row["metadata"]["benchmark_family"] == "local_hashed_dense" for row in hashed_rows)
    assert all(row["metadata"]["neural_model"] is False for row in hashed_rows)
    assert hashed_summary["hashed_dense_oracle_reader"]["metrics"]["retrieval_hit"] == 0.7
    assert (
        hashed_summary["hashed_dense_lexical_rerank_oracle_reader"]["metrics"][
            "retrieval_hit"
        ]
        == 0.72
    )


def test_phase7m_updates_docs_and_audit_without_final_source_claim():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}

    assert "Phase 7M" in doc
    assert "Provisional demo-question dataset" in doc
    assert "not a human-final demo benchmark" in doc
    assert audit["phase"] == "Phase 7M"
    assert audit["phase7m_demo_question_generation"] == {
        "dataset": DATASET_NAME,
        "source_dataset": "real_pilot_nickel_superalloy_medium_plus",
        "corpus_chunks": 100,
        "questions": 300,
        "question_target_status": "meets_demo_question_count_target_provisionally",
        "split_counts": {
            "dev": 100,
            "fresh_hard": 100,
            "test": 100,
        },
        "question_type_counts": {
            "fill_blank": 75,
            "multiple_choice": 75,
            "short_answer": 75,
            "single_choice": 75,
        },
        "provenance_status": "provisional_machine_generated_not_human_final",
        "final_demo_dataset_claim": "not_complete",
        "fresh_hard_baseline_rows": 300,
        "fresh_hard_hashed_dense_rows": 200,
        "live_api_calls": 0,
        "outputs": [
            "data/real_pilot_nickel_superalloy_demo_questions",
            "outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/demo_question_summary.json",
            "outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline/report_fresh_hard/summary.json",
            "outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense/report_fresh_hard/summary.json",
            "docs/verification/demo-question-generation.md",
        ],
    }
    assert requirements["demo_scale"]["status"] == "partial"
    assert "300 provisional questions" in requirements["demo_scale"]["summary"]
    assert "docs/verification/demo-question-generation.md" in requirements["demo_scale"][
        "evidence"
    ]
