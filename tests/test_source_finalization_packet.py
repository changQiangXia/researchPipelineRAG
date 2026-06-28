from __future__ import annotations

import importlib
import json
from pathlib import Path

from domainrag.io_utils import write_jsonl


def _verified_row(
    *,
    source_id: str = "openalex_W1",
    status: str = "verified_source_candidate",
    subtopic: str = "oxidation",
    work_kind: str = "research_article_candidate",
) -> dict:
    return {
        "source_id": source_id,
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
        "subtopic": subtopic,
        "work_kind": work_kind,
        "venue": "Corrosion Science",
        "source_verification_status": status,
        "final_inclusion_status": "not_finalized",
        "verification_checks": {
            "venue_metric": "verified",
            "doi_title_year": "verified",
            "article_type": "verified",
            "retraction": "verified",
            "full_text_processability": "verified",
            "domain_relevance": "verified",
        },
        "verification_reasons": [
            "all_machine_checks_verified_requires_human_final_signoff"
        ],
    }


def _ready_row(source_id: str = "openalex_W2") -> dict:
    row = _verified_row(source_id=source_id, status="ready_for_manual_finalization")
    row["verification_checks"] = {
        **row["verification_checks"],
        "venue_metric": "pending_manual",
    }
    row["verification_reasons"] = [
        "venue_metric_requires_manual_or_external_metric_check"
    ]
    return row


def _rejected_row(source_id: str = "openalex_W3") -> dict:
    row = _verified_row(source_id=source_id, status="rejected_verification")
    row["verification_checks"] = {
        **row["verification_checks"],
        "article_type": "failed",
    }
    row["verification_reasons"] = ["article_type:failed"]
    row["final_inclusion_status"] = "rejected_after_verification"
    return row


def test_build_manual_finalization_packet_classifies_sources_without_final_claim(
    tmp_path: Path,
):
    module = importlib.import_module("domainrag.source_finalization_packet")
    matrix = tmp_path / "source_verification_matrix.jsonl"
    output = tmp_path / "manual_finalization"
    write_jsonl(matrix, [_verified_row(), _ready_row(), _rejected_row()])

    packet_path, queue_path, summary_path, markdown_path = (
        module.build_manual_finalization_outputs(matrix, output_dir=output)
    )

    packet = [
        json.loads(line)
        for line in packet_path.read_text(encoding="utf-8").splitlines()
    ]
    queue = [
        json.loads(line)
        for line in queue_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert [row["manual_finalization_action"] for row in packet] == [
        "human_finalize_verified_candidate",
        "human_review_ready_source",
        "spot_check_rejected_source",
    ]
    assert [row["source_id"] for row in queue] == ["openalex_W1", "openalex_W2"]
    assert all(row["final_inclusion_status"] == "not_finalized" for row in queue)
    assert summary["source_count"] == 3
    assert summary["candidate_final_whitelist_queue_count"] == 2
    assert summary["accepted_final_source_count"] == 0
    assert summary["final_whitelist_claim"] == "not_complete"
    assert summary["action_counts"] == {
        "human_finalize_verified_candidate": 1,
        "human_review_ready_source": 1,
        "spot_check_rejected_source": 1,
    }
    assert "Phase 7I Manual Finalization Packet" in markdown
    assert "not final manual verification" in markdown
