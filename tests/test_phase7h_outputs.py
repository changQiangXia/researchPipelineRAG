from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FULL_TEXT = ROOT / "outputs" / "archive" / "provenance" / "source-workflow" / "source-verification-combined" / "full_text_access_combined115"
VERIFICATION = ROOT / "outputs" / "archive" / "provenance" / "source-workflow" / "source-verification-combined" / "source_verification_combined115"
DOC = ROOT / "docs" / "verification" / "full-text-intake-combined115.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7h_full_text_access_covers_all_provisional_whitelist_rows():
    records = _read_jsonl(FULL_TEXT / "full_text_access.jsonl")
    summary = json.loads((FULL_TEXT / "full_text_access_summary.json").read_text())

    assert len(records) == 115
    assert summary["source_count"] == 115
    assert summary["access_status_counts"] == {
        "download_failed": 6,
        "download_truncated": 1,
        "downloaded": 71,
        "not_accessible": 37,
    }
    assert summary["parse_status_counts"] == {
        "not_attempted": 44,
        "parseable": 71,
    }
    assert summary["parseable_count"] == 71
    assert summary["total_extracted_chars"] == 4366176
    assert all("text_sample" not in row for row in records)


def test_phase7h_source_verification_keeps_final_manual_status_open():
    matrix = _read_jsonl(VERIFICATION / "source_verification_matrix.jsonl")
    final_queue = _read_jsonl(VERIFICATION / "final_verification_queue.jsonl")
    summary = json.loads((VERIFICATION / "verification_summary.json").read_text())
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    assert len(matrix) == 115
    assert len(final_queue) == 0
    assert summary["source_count"] == 115
    assert summary["accepted_final_verification_count"] == 0
    assert summary["ready_for_manual_finalization_count"] == 106
    assert summary["rejected_verification_count"] == 7
    assert summary["status_counts"] == {
        "ready_for_manual_finalization": 106,
        "rejected_verification": 7,
        "verified_source_candidate": 2,
    }
    assert summary["final_whitelist_claim"] == "not_complete"
    assert summary["verification_status"] == "machine_assisted_not_human_final"
    assert "Phase 7H" in doc
    assert "not final manual verification" in doc
    assert audit["phase"] == "Phase 7M"
    assert audit["phase7h_full_text_intake"]["accepted_final_verification"] == 0
