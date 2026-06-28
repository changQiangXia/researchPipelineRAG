from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "outputs" / "archive" / "provenance" / "source-workflow" / "source-verification-first-batches" / "source_metadata"
FULL_TEXT = ROOT / "outputs" / "archive" / "provenance" / "source-workflow" / "source-verification-first-batches" / "full_text_access_combined25"
VERIFICATION = ROOT / "outputs" / "archive" / "provenance" / "source-workflow" / "source-verification-first-batches" / "source_verification_combined25"
DOC = ROOT / "docs" / "verification" / "source-verification-and-full-text-intake.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7g_openalex_metadata_covers_provisional_whitelist():
    records = _read_jsonl(METADATA / "openalex_metadata.jsonl")
    summary = json.loads((METADATA / "openalex_metadata_summary.json").read_text())

    assert len(records) == 115
    assert summary["source_count"] == 115
    assert summary["metadata_status_counts"] == {"found": 115}
    assert summary["retracted_count"] == 0
    assert summary["type_counts"]["article"] == 103
    assert summary["type_counts"]["preprint"] == 6


def test_phase7g_full_text_batch_records_parseability_without_text_leakage():
    records = _read_jsonl(FULL_TEXT / "full_text_access.jsonl")
    summary = json.loads((FULL_TEXT / "full_text_access_summary.json").read_text())

    assert len(records) == 25
    assert summary["source_count"] == 25
    assert summary["access_status_counts"] == {
        "download_failed": 2,
        "downloaded": 17,
        "not_accessible": 6,
    }
    assert summary["parse_status_counts"] == {
        "not_attempted": 8,
        "parseable": 17,
    }
    assert summary["parseable_count"] == 17
    assert all("text_sample" not in row for row in records)


def test_phase7g_source_verification_matrix_tracks_not_final_status():
    matrix = _read_jsonl(VERIFICATION / "source_verification_matrix.jsonl")
    final_queue = _read_jsonl(VERIFICATION / "final_verification_queue.jsonl")
    summary = json.loads((VERIFICATION / "verification_summary.json").read_text())
    doc = DOC.read_text(encoding="utf-8")

    assert len(matrix) == 115
    assert len(final_queue) == 0
    assert summary["source_count"] == 115
    assert summary["accepted_final_verification_count"] == 0
    assert summary["ready_for_manual_finalization_count"] == 23
    assert summary["rejected_verification_count"] == 7
    assert summary["status_counts"] == {
        "needs_evidence": 84,
        "ready_for_manual_finalization": 23,
        "rejected_verification": 7,
        "verified_source_candidate": 1,
    }
    assert summary["final_whitelist_claim"] == "not_complete"
    assert summary["verification_status"] == "machine_assisted_not_human_final"
    assert "Phase 7G" in doc
    assert "not final manual verification" in doc
    assert "outputs/archive/provenance/source-workflow/source-verification-first-batches/source_metadata/openalex_metadata.jsonl" in doc
    assert "outputs/archive/provenance/source-workflow/source-verification-first-batches/full_text_access_combined25/full_text_access.jsonl" in doc
