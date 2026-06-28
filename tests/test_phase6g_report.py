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
    assert "Phase 7B Medium-Plus Update" in report
    assert "Phase 7C Medium-Plus Live Subset" in report
    assert "Phase 7D Demo-Scale Source Acquisition" in report
    assert "Phase 7E Source Screening Queue" in report
    assert "Phase 7F Source Decisions" in report
    assert "Phase 7G Source Verification And Full-Text Intake" in report
    assert "Phase 7H Full-Text Intake Combined115" in report
    assert "Phase 7I Manual Finalization Packet" in report
    assert "Phase 7J Human Sign-Off Workflow" in report
    assert "outputs/phase6e/medium_fresh_hard_comparison/summary.json" in report
    assert "outputs/phase6f/medium_human_calibration_audit/summary.json" in report
    assert "outputs/phase7b/medium_plus_bm25s/" in report
    assert "outputs/phase7c/medium_plus_live_subset/comparison/summary.json" in report
    assert "outputs/phase7d/demo_scale_source_acquisition/coverage.json" in report
    assert "outputs/phase7e/source_screening_queue/screening_summary.json" in report
    assert "outputs/phase7f/source_decisions/decision_summary.json" in report

    assert audit["phase"] == "Phase 7J"
    assert audit["dataset"]["name"] == "real_pilot_nickel_superalloy_medium_plus"
    assert audit["dataset"]["corpus_chunks"] == 100
    assert audit["dataset"]["questions"] == 150
    assert audit["dataset"]["fresh_hard_questions"] == 50
    assert audit["rag_md_targets"]["demo"]["corpus_chunks"] == [1000, 3000]
    assert audit["rag_md_targets"]["demo"]["questions"] == [300, 500]
    assert audit["completion_estimate"]["excluding_final_scale"] == "about 99%"
    assert audit["completion_estimate"]["including_rag_md_demo_scale"] == "94%-95%"


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
    assert requirements["dense_rerank_methods"]["status"] == "partial"
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


def test_phase6g_audit_tracks_phase7c_medium_plus_live_subset():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    subset = audit["phase7c_medium_plus_live_subset"]
    leaderboard = {row["method"]: row for row in subset["leaderboard"]}

    assert subset["questions"] == 12
    assert subset["answer_rows"] == 36
    assert subset["judge_rows"] == 36
    assert subset["answer_errors"] == 0
    assert subset["judge_errors"] == 0
    assert subset["total_api_calls"] == 75
    assert set(leaderboard) == {
        "no_rag",
        "lexical_rag",
        "flashrag_bm25_live_deepseek",
    }
    assert leaderboard["flashrag_bm25_live_deepseek"]["retrieval_hit"] == 0.9167
    assert leaderboard["lexical_rag"]["retrieval_hit"] == 0.9167
    assert leaderboard["no_rag"]["hallucination_risk"] == 3.75
    assert leaderboard["no_rag"]["unsupported_claims"] == 18


def test_phase6g_audit_tracks_phase7d_candidate_pool_without_closing_scale_gap():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    acquisition = audit["phase7d_demo_scale_source_acquisition"]

    assert acquisition["candidate_count"] == 124
    assert acquisition["research_article_candidates"] == 113
    assert acquisition["review_candidates"] == 11
    assert acquisition["open_access_candidates"] == 115
    assert acquisition["subtopic_count"] == 8
    assert acquisition["final_included_sources"] == 0
    assert acquisition["verification_status"] == "candidate_pool_only"
    assert acquisition["inclusion_status"] == "candidate_for_manual_verification"
    assert requirements["literature_source_policy"]["status"] == "partial"
    assert requirements["demo_scale"]["status"] == "partial"


def test_phase6g_audit_tracks_phase7e_screening_queue_without_finalizing_sources():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    screening = audit["phase7e_source_screening_queue"]

    assert screening["candidate_count"] == 124
    assert screening["final_included_sources"] == 0
    assert screening["verification_status"] == "machine_prescreen_only"
    assert screening["full_text_ready_candidates"] == 115
    assert screening["review_gap_subtopics"] == [
        "coatings",
        "life_prediction",
        "microstructure_characterization",
    ]
    assert screening["priority_counts"] == {"high": 3, "low": 42, "medium": 79}
    assert requirements["literature_source_policy"]["status"] == "partial"
    assert requirements["demo_scale"]["status"] == "partial"


def test_phase6g_audit_tracks_phase7f_source_decisions_as_stop_point():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    decisions = audit["phase7f_source_decisions"]

    assert decisions["candidate_count"] == 124
    assert decisions["decision_counts"] == {
        "accepted_provisional": 82,
        "pending_manual_review": 33,
        "rejected_prescreen": 9,
    }
    assert decisions["provisional_whitelist_count"] == 115
    assert decisions["verification_status"] == "provisional_not_final"
    assert decisions["stop_point_recommendation"] == "pause_after_phase7f"
    assert requirements["literature_source_policy"]["status"] == "partial"
    assert requirements["demo_scale"]["status"] == "partial"
    assert "outputs/phase7f/source_decisions/decision_summary.json" in requirements[
        "literature_source_policy"
    ]["evidence"]
