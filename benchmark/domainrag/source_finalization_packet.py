from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.source_acquisition import DEMO_SOURCE_TARGET


VERIFIED_ACTION = "human_finalize_verified_candidate"
READY_ACTION = "human_review_ready_source"
REJECTED_ACTION = "spot_check_rejected_source"
EVIDENCE_ACTION = "collect_missing_evidence"
ACTION_ORDER = {
    VERIFIED_ACTION: 0,
    READY_ACTION: 1,
    REJECTED_ACTION: 2,
    EVIDENCE_ACTION: 3,
}
QUEUE_ACTIONS = {VERIFIED_ACTION, READY_ACTION}


def build_manual_finalization_outputs(
    verification_matrix_path: Path,
    *,
    output_dir: Path,
) -> tuple[Path, Path, Path, Path]:
    rows = read_jsonl(verification_matrix_path)
    packet = sorted(
        (prepare_manual_finalization_row(row) for row in rows),
        key=lambda row: (
            ACTION_ORDER[row["manual_finalization_action"]],
            row.get("subtopic", ""),
            row.get("source_id", ""),
        ),
    )
    candidate_queue = [
        row for row in packet if row["manual_finalization_action"] in QUEUE_ACTIONS
    ]
    summary = summarize_manual_finalization_packet(packet, candidate_queue)

    output_dir.mkdir(parents=True, exist_ok=True)
    packet_path = output_dir / "manual_finalization_packet.jsonl"
    queue_path = output_dir / "candidate_final_whitelist_queue.jsonl"
    summary_path = output_dir / "manual_finalization_summary.json"
    markdown_path = output_dir / "summary.md"
    write_jsonl(packet_path, packet)
    write_jsonl(queue_path, candidate_queue)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return packet_path, queue_path, summary_path, markdown_path


def prepare_manual_finalization_row(row: dict[str, Any]) -> dict[str, Any]:
    action = _manual_action(row)
    prepared = dict(row)
    prepared.update(
        {
            "manual_finalization_action": action,
            "manual_finalization_status": "requires_human_review",
            "human_final_signoff_status": "not_signed_off",
            "manual_review_fields": _manual_review_fields(row, action),
            "candidate_final_whitelist_queue_status": (
                "candidate_for_final_whitelist_review"
                if action in QUEUE_ACTIONS
                else "not_in_candidate_final_whitelist_queue"
            ),
        }
    )
    if action in QUEUE_ACTIONS:
        prepared["final_inclusion_status"] = "not_finalized"
    return prepared


def summarize_manual_finalization_packet(
    packet: list[dict[str, Any]],
    candidate_queue: list[dict[str, Any]],
) -> dict[str, Any]:
    accepted_final_count = sum(
        1
        for row in packet
        if row.get("final_inclusion_status") == "accepted_final_verification"
    )
    subtopics: dict[str, dict[str, int]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidate_queue:
        grouped[str(row.get("subtopic", "unknown"))].append(row)
    for subtopic, rows in sorted(grouped.items()):
        subtopics[subtopic] = {
            "candidate_queue_count": len(rows),
            "verified_source_candidates": sum(
                1 for row in rows if row["manual_finalization_action"] == VERIFIED_ACTION
            ),
            "ready_for_manual_finalization": sum(
                1 for row in rows if row["manual_finalization_action"] == READY_ACTION
            ),
            "review_candidates": sum(
                1 for row in rows if row.get("work_kind") == "review_candidate"
            ),
            "research_article_candidates": sum(
                1
                for row in rows
                if row.get("work_kind") == "research_article_candidate"
            ),
        }

    target_min, target_max = DEMO_SOURCE_TARGET
    queue_count = len(candidate_queue)
    return {
        "source_count": len(packet),
        "candidate_final_whitelist_queue_count": queue_count,
        "accepted_final_source_count": accepted_final_count,
        "final_whitelist_claim": (
            "complete" if target_min <= accepted_final_count <= target_max else "not_complete"
        ),
        "candidate_queue_target_status": (
            "candidate_queue_meets_source_count_target"
            if target_min <= queue_count <= target_max
            else "candidate_queue_outside_source_count_target"
        ),
        "target_final_source_whitelist": DEMO_SOURCE_TARGET,
        "action_counts": _ordered_action_counts(
            row["manual_finalization_action"] for row in packet
        ),
        "subtopic_count": len(subtopics),
        "subtopics": subtopics,
        "verification_status": "human_review_packet_not_final",
        "remaining_gaps": [
            "human source sign-off",
            "manual venue metric or flagship verification",
            "manual handling for access-limited full-text rows",
            "chunk extraction from human-accepted sources",
            "300-500 question generation from accepted chunks",
        ],
    }


def _manual_action(row: dict[str, Any]) -> str:
    status = str(row.get("source_verification_status") or "")
    if status == "verified_source_candidate":
        return VERIFIED_ACTION
    if status == "ready_for_manual_finalization":
        return READY_ACTION
    if status == "rejected_verification":
        return REJECTED_ACTION
    return EVIDENCE_ACTION


def _manual_review_fields(row: dict[str, Any], action: str) -> list[str]:
    checks = row.get("verification_checks")
    if not isinstance(checks, dict):
        return ["collect_missing_verification_checks"]
    fields = [
        name
        for name, status in checks.items()
        if status in {"pending_manual", "pending_evidence", "failed"}
    ]
    if action == VERIFIED_ACTION:
        return ["human_final_signoff"]
    if action == REJECTED_ACTION and not fields:
        return ["spot_check_rejection_reason"]
    return fields or ["human_final_signoff"]


def _ordered_action_counts(values: Any) -> dict[str, int]:
    return dict(
        sorted(
            Counter(str(value) for value in values).items(),
            key=lambda item: (ACTION_ORDER.get(item[0], 99), item[0]),
        )
    )


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7I Manual Finalization Packet",
        "",
        "- Verification status: human_review_packet_not_final",
        "- This is not final manual verification.",
        f"- Source rows in packet: {summary['source_count']}",
        (
            "- Candidate final whitelist queue: "
            f"{summary['candidate_final_whitelist_queue_count']}"
        ),
        f"- Accepted final source count: {summary['accepted_final_source_count']}",
        f"- Final whitelist claim: {summary['final_whitelist_claim']}",
        "",
        "## Action Counts",
        "",
        "| action | count |",
        "| --- | ---: |",
    ]
    for action, count in summary["action_counts"].items():
        lines.append(f"| {action} | {count} |")
    lines.extend(
        [
            "",
            "## Candidate Queue By Subtopic",
            "",
            "| subtopic | queue | verified | ready | reviews | research |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for subtopic, values in summary["subtopics"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    subtopic,
                    str(values["candidate_queue_count"]),
                    str(values["verified_source_candidates"]),
                    str(values["ready_for_manual_finalization"]),
                    str(values["review_candidates"]),
                    str(values["research_article_candidates"]),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)
