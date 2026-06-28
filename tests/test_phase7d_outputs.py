from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "phase7d" / "demo_scale_source_acquisition"
CANDIDATES = OUTPUT / "candidates.jsonl"
COVERAGE = OUTPUT / "coverage.json"
SUMMARY = OUTPUT / "summary.md"
DOC = ROOT / "docs" / "verification" / "demo-scale-source-acquisition.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7d_source_acquisition_outputs_candidate_pool_not_final_list():
    candidates = _read_jsonl(CANDIDATES)
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    summary = SUMMARY.read_text(encoding="utf-8")

    assert len(candidates) >= 100
    assert coverage["candidate_count"] == len(candidates)
    assert coverage["subtopic_count"] == 8
    assert coverage["research_article_candidates"] >= 70
    assert coverage["review_candidates"] >= 5
    assert coverage["demo_scale_targets"]["source_papers"] == [100, 180]
    assert coverage["demo_scale_targets"]["corpus_chunks"] == [1000, 3000]
    assert "candidate_for_manual_verification" in summary
    assert "Phase 7D Demo-Scale Source Acquisition" in summary
    assert all(candidate["source_id"].startswith("openalex_") for candidate in candidates)
    assert all(candidate["doi"] for candidate in candidates)
    assert all(candidate["official_url"].startswith("http") for candidate in candidates)
    assert {candidate["verification_status"] for candidate in candidates} == {
        "candidate_openalex_verified"
    }
    assert {candidate["inclusion_status"] for candidate in candidates} == {
        "candidate_for_manual_verification"
    }


def test_phase7d_source_acquisition_covers_required_domain_subtopics():
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))

    assert set(coverage["subtopics"]) == {
        "additive_manufacturing",
        "coatings",
        "creep",
        "fatigue",
        "hot_corrosion",
        "life_prediction",
        "microstructure_characterization",
        "oxidation",
    }
    assert all(
        values["candidate_count"] >= 5
        for values in coverage["subtopics"].values()
    )


def test_phase7d_updates_verification_doc_and_audit_without_closing_scale_gap():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    acquisition = audit["phase7d_demo_scale_source_acquisition"]

    assert "Phase 7D" in doc
    assert "candidate_for_manual_verification" in doc
    assert "not a final inclusion list" in doc
    assert "outputs/phase7d/demo_scale_source_acquisition/candidates.jsonl" in doc
    assert audit["phase"] == "Phase 7G"
    assert acquisition["candidate_count"] >= 100
    assert acquisition["subtopic_count"] == 8
    assert acquisition["final_included_sources"] == 0
    assert acquisition["verification_status"] == "candidate_pool_only"
    assert audit["phase7e_source_screening_queue"]["verification_status"] == (
        "machine_prescreen_only"
    )
    assert audit["phase7f_source_decisions"]["verification_status"] == (
        "provisional_not_final"
    )
    assert requirements["literature_source_policy"]["status"] == "partial"
    assert "outputs/phase7d/demo_scale_source_acquisition/coverage.json" in requirements[
        "literature_source_policy"
    ]["evidence"]
    assert requirements["demo_scale"]["status"] == "partial"
