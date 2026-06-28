from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "reports" / "domainrag-medium-pilot-final-report.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def test_phase6g_final_report_covers_rag_md_completion_audit():
    report = REPORT.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    assert "# DomainRAG-Bench Medium Pilot Final Report" in report
    assert "RAG.md Completion Audit" in report
    assert "Scale Gap" in report
    assert "Dense And Rerank Gap" in report
    assert "Next Phase Recommendation" in report
    assert "outputs/phase6e/medium_fresh_hard_comparison/summary.json" in report
    assert "outputs/phase6f/medium_human_calibration_audit/summary.json" in report

    assert audit["phase"] == "Phase 6G"
    assert audit["dataset"]["name"] == "real_pilot_nickel_superalloy_medium"
    assert audit["dataset"]["corpus_chunks"] == 40
    assert audit["dataset"]["questions"] == 60
    assert audit["dataset"]["fresh_hard_questions"] == 20
    assert audit["rag_md_targets"]["demo"]["corpus_chunks"] == [1000, 3000]
    assert audit["rag_md_targets"]["demo"]["questions"] == [300, 500]
    assert audit["completion_estimate"]["excluding_final_scale"] == "98%-99%"
    assert audit["completion_estimate"]["including_rag_md_demo_scale"] == "78%-80%"


def test_phase6g_audit_tracks_core_requirements_and_gaps():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}

    expected_ids = {
        "literature_source_policy",
        "easy_dataset_intake",
        "domainrag_data_contract",
        "public_metadata_safety",
        "deepseek_generation_review",
        "flashrag_single_framework",
        "typed_scoring",
        "fresh_hard_evaluation",
        "live_deepseek_judge",
        "human_calibration",
        "method_comparison",
        "efficiency_metrics",
        "demo_scale",
        "dense_rerank_methods",
        "final_report",
    }

    assert set(requirements) == expected_ids
    assert requirements["demo_scale"]["status"] == "partial"
    assert requirements["dense_rerank_methods"]["status"] == "deferred"
    assert requirements["final_report"]["status"] == "complete"
    assert all(item["evidence"] for item in requirements.values())
    assert all(item["status"] in {"complete", "partial", "deferred"} for item in requirements.values())


def test_phase6g_audit_preserves_medium_live_and_calibration_results():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    leaderboard = {row["method"]: row for row in audit["phase6e_leaderboard"]}
    calibration = audit["phase6f_human_calibration"]

    assert set(leaderboard) == {
        "no_rag",
        "oracle_context",
        "lexical_rag",
        "flashrag_bm25_oracle_reader",
        "flashrag_bm25_live_deepseek",
    }
    assert leaderboard["oracle_context"]["retrieval_recall"] == 1.0
    assert leaderboard["lexical_rag"]["retrieval_recall"] == 0.925
    assert leaderboard["flashrag_bm25_live_deepseek"]["retrieval_recall"] == 0.8542
    assert leaderboard["no_rag"]["unsupported_claims"] == 17
    assert leaderboard["flashrag_bm25_oracle_reader"]["unsupported_claims"] == 4

    assert calibration["reviewed_rows"] == 15
    assert calibration["agreement_rate_within_1"]["correctness"] == 1.0
    assert calibration["agreement_rate_within_1"]["context_support"] == 0.8667
    assert calibration["agreement_rate_within_1"]["faithfulness"] == 0.8667
