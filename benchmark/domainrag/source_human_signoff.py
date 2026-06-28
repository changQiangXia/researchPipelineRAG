from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.source_acquisition import DEMO_SOURCE_TARGET


ACCEPTED_FINAL = "accepted_final"
REJECTED_FINAL = "rejected_final"
PENDING_HUMAN_REVIEW = "pending_human_review"
VALID_SIGNOFF_DECISIONS = {ACCEPTED_FINAL, REJECTED_FINAL, PENDING_HUMAN_REVIEW}


def build_human_signoff_outputs(
    candidate_queue_path: Path,
    *,
    output_dir: Path,
    labels_path: Path | None = None,
) -> tuple[Path, Path, Path, Path]:
    queue_rows = read_jsonl(candidate_queue_path)
    labels_by_source = _labels_by_source_id(labels_path)
    template = [
        prepare_human_signoff_row(row, labels_by_source.get(str(row["source_id"])))
        for row in queue_rows
    ]
    final_whitelist = [
        row
        for row in template
        if row["human_signoff_decision"] == ACCEPTED_FINAL
    ]
    summary = summarize_human_signoff(template, final_whitelist)

    output_dir.mkdir(parents=True, exist_ok=True)
    template_path = output_dir / "human_signoff_template.jsonl"
    final_path = output_dir / "final_source_whitelist.jsonl"
    summary_path = output_dir / "human_signoff_summary.json"
    markdown_path = output_dir / "summary.md"
    write_jsonl(template_path, template)
    write_jsonl(final_path, final_whitelist)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return template_path, final_path, summary_path, markdown_path


def prepare_human_signoff_row(
    row: dict[str, Any],
    label: dict[str, Any] | None = None,
) -> dict[str, Any]:
    decision = _decision_from_label(label)
    prepared = dict(row)
    prepared.update(
        {
            "human_signoff_decision": decision,
            "human_reviewer": _label_value(label, "human_reviewer"),
            "human_review_date": _label_value(label, "human_review_date"),
            "human_review_notes": _label_value(label, "human_review_notes"),
            "human_signoff_status": (
                "signed_off" if decision in {ACCEPTED_FINAL, REJECTED_FINAL} else "pending"
            ),
            "final_inclusion_status": (
                "accepted_final_verification"
                if decision == ACCEPTED_FINAL
                else "rejected_after_human_signoff"
                if decision == REJECTED_FINAL
                else "not_finalized"
            ),
        }
    )
    return prepared


def summarize_human_signoff(
    template: list[dict[str, Any]],
    final_whitelist: list[dict[str, Any]],
) -> dict[str, Any]:
    target_min, target_max = DEMO_SOURCE_TARGET
    accepted_count = len(final_whitelist)
    subtopics: dict[str, dict[str, int]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in final_whitelist:
        grouped[str(row.get("subtopic", "unknown"))].append(row)
    for subtopic, rows in sorted(grouped.items()):
        subtopics[subtopic] = {
            "accepted_final_sources": len(rows),
            "review_candidates": sum(
                1 for row in rows if row.get("work_kind") == "review_candidate"
            ),
            "research_article_candidates": sum(
                1
                for row in rows
                if row.get("work_kind") == "research_article_candidate"
            ),
        }

    decision_counts = dict(sorted(Counter(row["human_signoff_decision"] for row in template).items()))
    return {
        "candidate_queue_count": len(template),
        "accepted_final_source_count": accepted_count,
        "rejected_final_source_count": decision_counts.get(REJECTED_FINAL, 0),
        "pending_human_review_count": decision_counts.get(PENDING_HUMAN_REVIEW, 0),
        "human_signoff_decision_counts": decision_counts,
        "final_whitelist_claim": (
            "complete" if target_min <= accepted_count <= target_max else "not_complete"
        ),
        "target_final_source_whitelist": DEMO_SOURCE_TARGET,
        "subtopic_count": len(subtopics),
        "subtopics": subtopics,
        "verification_status": "human_signoff_required",
        "remaining_gaps": [
            "human source sign-off",
            "chunk extraction from human-accepted sources",
            "300-500 question generation from accepted chunks",
        ],
    }


def _labels_by_source_id(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    labels = read_jsonl(path)
    return {str(label["source_id"]): label for label in labels}


def _decision_from_label(label: dict[str, Any] | None) -> str:
    if label is None:
        return PENDING_HUMAN_REVIEW
    decision = str(label.get("human_signoff_decision") or "").strip()
    if decision not in VALID_SIGNOFF_DECISIONS:
        return PENDING_HUMAN_REVIEW
    return decision


def _label_value(label: dict[str, Any] | None, key: str) -> str | None:
    if label is None:
        return None
    value = str(label.get(key) or "").strip()
    return value or None


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7J Human Sign-Off Workflow",
        "",
        "- Verification status: human_signoff_required",
        "- This is not final manual verification until labels are supplied.",
        f"- Candidate queue rows: {summary['candidate_queue_count']}",
        f"- Accepted final source count: {summary['accepted_final_source_count']}",
        f"- Pending human review count: {summary['pending_human_review_count']}",
        f"- Final whitelist claim: {summary['final_whitelist_claim']}",
        "",
        "## Decision Counts",
        "",
        "| decision | count |",
        "| --- | ---: |",
    ]
    for decision, count in summary["human_signoff_decision_counts"].items():
        lines.append(f"| {decision} | {count} |")
    lines.append("")
    return "\n".join(lines)
