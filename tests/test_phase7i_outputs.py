from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "outputs" / "phase7i" / "manual_finalization_packet"
DOC = ROOT / "docs" / "verification" / "manual-finalization-packet.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7i_manual_finalization_packet_matches_source_target_queue():
    packet = _read_jsonl(PACKET / "manual_finalization_packet.jsonl")
    queue = _read_jsonl(PACKET / "candidate_final_whitelist_queue.jsonl")
    summary = json.loads((PACKET / "manual_finalization_summary.json").read_text())

    assert len(packet) == 115
    assert len(queue) == 108
    assert summary["source_count"] == 115
    assert summary["candidate_final_whitelist_queue_count"] == 108
    assert summary["candidate_queue_target_status"] == (
        "candidate_queue_meets_source_count_target"
    )
    assert summary["accepted_final_source_count"] == 0
    assert summary["final_whitelist_claim"] == "not_complete"
    assert summary["action_counts"] == {
        "human_finalize_verified_candidate": 2,
        "human_review_ready_source": 106,
        "spot_check_rejected_source": 7,
    }
    assert all(row["final_inclusion_status"] == "not_finalized" for row in queue)


def test_phase7i_updates_docs_and_audit_without_claiming_human_finalization():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    assert "Phase 7I" in doc
    assert "not final manual verification" in doc
    assert "candidate final whitelist queue" in doc
    assert audit["phase"] == "Phase 7M"
    assert audit["phase7i_manual_finalization_packet"] == {
        "source_count": 115,
        "candidate_final_whitelist_queue_count": 108,
        "verified_source_candidates": 2,
        "ready_for_manual_finalization": 106,
        "spot_check_rejected_sources": 7,
        "accepted_final_source_count": 0,
        "candidate_queue_target_status": "candidate_queue_meets_source_count_target",
        "final_whitelist_claim": "not_complete",
        "verification_status": "human_review_packet_not_final",
        "outputs": [
            "outputs/phase7i/manual_finalization_packet/manual_finalization_packet.jsonl",
            "outputs/phase7i/manual_finalization_packet/candidate_final_whitelist_queue.jsonl",
            "outputs/phase7i/manual_finalization_packet/manual_finalization_summary.json",
            "docs/verification/manual-finalization-packet.md",
        ],
    }
