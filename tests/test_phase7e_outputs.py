from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "phase7e" / "source_screening_queue"
QUEUE = OUTPUT / "screening_queue.jsonl"
SUMMARY = OUTPUT / "screening_summary.json"
MARKDOWN = OUTPUT / "summary.md"
DOC = ROOT / "docs" / "verification" / "source-screening-queue.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"
REPORT = ROOT / "docs" / "reports" / "domainrag-medium-pilot-final-report.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7e_screening_queue_covers_all_phase7d_candidates_without_finalizing():
    queue = _read_jsonl(QUEUE)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    markdown = MARKDOWN.read_text(encoding="utf-8")

    assert len(queue) == 124
    assert summary["candidate_count"] == 124
    assert summary["final_included_sources"] == 0
    assert summary["verification_status"] == "machine_prescreen_only"
    assert summary["full_text_ready_candidates"] >= 100
    assert set(summary["priority_counts"]) <= {"high", "medium", "low"}
    assert set(summary["screening_status_counts"]) == {"needs_manual_verification"}
    assert set(summary["full_text_queue_status_counts"]) == {
        "needs_access_check",
        "ready_for_full_text_download_attempt",
    }
    assert all(row["final_inclusion_status"] == "not_finalized" for row in queue)
    assert all(row["screening_status"] == "needs_manual_verification" for row in queue)
    assert all(row["verification_status"] == "machine_prescreen_only" for row in queue)
    assert "Phase 7E Source Screening Queue" in markdown
    assert "machine_prescreen_only" in markdown


def test_phase7e_screening_summary_tracks_review_gaps_and_subtopic_queue():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert summary["review_gap_subtopics"] == [
        "coatings",
        "life_prediction",
        "microstructure_characterization",
    ]
    assert summary["subtopic_count"] == 8
    assert summary["subtopics"]["coatings"]["review_candidates"] == 0
    assert summary["subtopics"]["life_prediction"]["review_candidates"] == 0
    assert summary["subtopics"]["microstructure_characterization"]["review_candidates"] == 0
    assert summary["subtopics"]["additive_manufacturing"]["review_candidates"] == 3
    assert summary["demo_scale_targets"]["source_papers"] == [100, 180]
    assert summary["demo_scale_targets"]["corpus_chunks"] == [1000, 3000]
    assert summary["demo_scale_targets"]["questions"] == [300, 500]


def test_phase7e_updates_verification_doc_report_and_audit_without_closing_scale_gap():
    doc = DOC.read_text(encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    screening = audit["phase7e_source_screening_queue"]

    assert "Phase 7E" in doc
    assert "machine_prescreen_only" in doc
    assert "not a final source whitelist" in doc
    assert "outputs/phase7e/source_screening_queue/screening_queue.jsonl" in doc
    assert "Phase 7E Source Screening Queue" in report
    assert "Phase 7F Source Decisions" in report
    assert audit["phase"] == "Phase 7M"
    assert screening["candidate_count"] == 124
    assert screening["final_included_sources"] == 0
    assert screening["verification_status"] == "machine_prescreen_only"
    assert screening["full_text_ready_candidates"] >= 100
    assert screening["review_gap_subtopics"] == [
        "coatings",
        "life_prediction",
        "microstructure_characterization",
    ]
    assert audit["phase7f_source_decisions"]["verification_status"] == (
        "provisional_not_final"
    )
    assert requirements["literature_source_policy"]["status"] == "partial"
    assert requirements["demo_scale"]["status"] == "partial"
    assert "outputs/phase7e/source_screening_queue/screening_summary.json" in requirements[
        "literature_source_policy"
    ]["evidence"]
