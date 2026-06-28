from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "phase7f" / "source_decisions"
DECISIONS = OUTPUT / "source_decisions.jsonl"
WHITELIST = OUTPUT / "provisional_source_whitelist.jsonl"
SUMMARY = OUTPUT / "decision_summary.json"
MARKDOWN = OUTPUT / "summary.md"
DOC = ROOT / "docs" / "verification" / "source-decisions-and-stop-point.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"
REPORT = ROOT / "docs" / "reports" / "domainrag-medium-pilot-final-report.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7f_decision_outputs_cover_all_candidates_and_stop_point():
    decisions = _read_jsonl(DECISIONS)
    whitelist = _read_jsonl(WHITELIST)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    markdown = MARKDOWN.read_text(encoding="utf-8")

    assert len(decisions) == 124
    assert len(whitelist) == 115
    assert summary["candidate_count"] == 124
    assert summary["decision_counts"] == {
        "accepted_provisional": 82,
        "pending_manual_review": 33,
        "rejected_prescreen": 9,
    }
    assert summary["provisional_whitelist_count"] == 115
    assert summary["verification_status"] == "provisional_not_final"
    assert summary["stop_point_recommendation"] == "pause_after_phase7f"
    assert all(row["decision_status"] == "provisional_not_final" for row in decisions)
    assert all(
        row["source_decision"] != "rejected_prescreen"
        for row in whitelist
    )
    assert "Phase 7F Source Decisions" in markdown
    assert "pause_after_phase7f" in markdown


def test_phase7f_decisions_keep_manual_verification_pending_and_track_gaps():
    decisions = _read_jsonl(DECISIONS)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert summary["review_gap_subtopics"] == [
        "coatings",
        "life_prediction",
        "microstructure_characterization",
    ]
    assert summary["subtopics"]["coatings"]["review_candidates"] == 0
    assert summary["subtopics"]["life_prediction"]["review_candidates"] == 0
    assert summary["subtopics"]["microstructure_characterization"]["review_candidates"] == 0
    assert all(
        set(row["manual_verification_status"].values()) == {"pending"}
        for row in decisions
    )
    assert "full 1,000-3,000 chunk and 300-500 question demo-scale production" in summary[
        "remaining_gaps"
    ]


def test_phase7f_updates_report_audit_and_stop_point_documentation():
    doc = DOC.read_text(encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    decisions = audit["phase7f_source_decisions"]

    assert "Phase 7F" in doc
    assert "pause_after_phase7f" in doc
    assert "not final manual verification" in doc
    assert "outputs/phase7f/source_decisions/source_decisions.jsonl" in doc
    assert "Phase 7F Source Decisions" in report
    assert audit["phase"] == "Phase 7J"
    assert audit["completion_estimate"]["including_rag_md_demo_scale"] == "94%-95%"
    assert decisions["candidate_count"] == 124
    assert decisions["provisional_whitelist_count"] == 115
    assert decisions["verification_status"] == "provisional_not_final"
    assert decisions["stop_point_recommendation"] == "pause_after_phase7f"
    assert requirements["literature_source_policy"]["status"] == "partial"
    assert requirements["demo_scale"]["status"] == "partial"
    assert "outputs/phase7f/source_decisions/decision_summary.json" in requirements[
        "literature_source_policy"
    ]["evidence"]
    assert audit["phase7g_source_verification"]["accepted_final_verification"] == 0
