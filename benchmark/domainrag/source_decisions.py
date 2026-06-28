from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.source_acquisition import (
    DEMO_CHUNK_TARGET,
    DEMO_QUESTION_TARGET,
    DEMO_SOURCE_TARGET,
)


MANUAL_VERIFICATION_PENDING = {
    "venue_metric": "pending",
    "doi_title_year": "pending",
    "article_type": "pending",
    "retraction": "pending",
    "full_text_processability": "pending",
    "domain_relevance": "pending",
}
REVIEW_TARGET_PER_SUBTOPIC = 1
DECISION_ORDER = {
    "accepted_provisional": 0,
    "pending_manual_review": 1,
    "rejected_prescreen": 2,
}


def decide_source(row: dict[str, Any]) -> dict[str, Any]:
    decision = _decision(row)
    decided = dict(row)
    decided.update(
        {
            "source_decision": decision,
            "decision_status": "provisional_not_final",
            "manual_verification_status": dict(MANUAL_VERIFICATION_PENDING),
            "decision_reasons": _decision_reasons(row, decision),
        }
    )
    return decided


def summarize_decisions(rows: list[dict[str, Any]]) -> dict[str, Any]:
    subtopics: dict[str, dict[str, Any]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["subtopic"])].append(row)
    for subtopic, subtopic_rows in sorted(grouped.items()):
        subtopics[subtopic] = _subtopic_counts(subtopic_rows)

    review_gap_subtopics = [
        subtopic
        for subtopic, values in subtopics.items()
        if values["review_candidates"] < REVIEW_TARGET_PER_SUBTOPIC
    ]
    decision_counts = dict(
        sorted(
            Counter(row["source_decision"] for row in rows).items(),
            key=lambda item: DECISION_ORDER[item[0]],
        )
    )
    provisional_whitelist_count = sum(
        1 for row in rows if row["source_decision"] != "rejected_prescreen"
    )
    return {
        "candidate_count": len(rows),
        "decision_counts": decision_counts,
        "accepted_provisional_count": decision_counts.get("accepted_provisional", 0),
        "pending_manual_review_count": decision_counts.get("pending_manual_review", 0),
        "rejected_prescreen_count": decision_counts.get("rejected_prescreen", 0),
        "provisional_whitelist_count": provisional_whitelist_count,
        "verification_status": "provisional_not_final",
        "stop_point_recommendation": "pause_after_phase7f",
        "research_article_candidates": sum(
            1 for row in rows if row.get("work_kind") == "research_article_candidate"
        ),
        "review_candidates": sum(
            1 for row in rows if row.get("work_kind") == "review_candidate"
        ),
        "review_gap_subtopics": review_gap_subtopics,
        "subtopic_count": len(subtopics),
        "subtopics": subtopics,
        "demo_scale_targets": {
            "source_papers": DEMO_SOURCE_TARGET,
            "corpus_chunks": DEMO_CHUNK_TARGET,
            "questions": DEMO_QUESTION_TARGET,
        },
        "remaining_gaps": [
            "manual venue metric or flagship verification",
            "manual DOI/title/year verification",
            "manual article-type verification",
            "manual retraction-status verification",
            "full-text download and parsing verification",
            "manual domain-relevance screening",
            "full 1,000-3,000 chunk and 300-500 question demo-scale production",
        ],
    }


def build_decision_outputs(
    screening_queue_path: Path,
    *,
    output_dir: Path,
) -> tuple[Path, Path, Path, Path]:
    queue_rows = read_jsonl(screening_queue_path)
    rows = sorted(
        (decide_source(row) for row in queue_rows),
        key=lambda row: (
            DECISION_ORDER[row["source_decision"]],
            row["subtopic"],
            row["source_id"],
        ),
    )
    whitelist = [
        row for row in rows if row["source_decision"] != "rejected_prescreen"
    ]
    summary = summarize_decisions(rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    decisions_path = output_dir / "source_decisions.jsonl"
    whitelist_path = output_dir / "provisional_source_whitelist.jsonl"
    summary_path = output_dir / "decision_summary.json"
    markdown_path = output_dir / "summary.md"

    write_jsonl(decisions_path, rows)
    write_jsonl(whitelist_path, whitelist)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return decisions_path, whitelist_path, summary_path, markdown_path


def _decision(row: dict[str, Any]) -> str:
    if row.get("full_text_queue_status") != "ready_for_full_text_download_attempt":
        return "rejected_prescreen"
    if row.get("screening_priority") in {"high", "medium"}:
        return "accepted_provisional"
    return "pending_manual_review"


def _decision_reasons(row: dict[str, Any], decision: str) -> list[str]:
    reasons = [
        f"screening_priority:{row.get('screening_priority')}",
        f"full_text_queue_status:{row.get('full_text_queue_status')}",
    ]
    if decision == "accepted_provisional":
        reasons.append("ready_for_first_manual_verification_pass")
    elif decision == "pending_manual_review":
        reasons.append("low_priority_but_full_text_candidate_available")
    else:
        reasons.append("access_check_required_before_source_whitelist")
    return reasons


def _subtopic_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_count": len(rows),
        "accepted_provisional": sum(
            1 for row in rows if row["source_decision"] == "accepted_provisional"
        ),
        "pending_manual_review": sum(
            1 for row in rows if row["source_decision"] == "pending_manual_review"
        ),
        "rejected_prescreen": sum(
            1 for row in rows if row["source_decision"] == "rejected_prescreen"
        ),
        "provisional_whitelist_count": sum(
            1 for row in rows if row["source_decision"] != "rejected_prescreen"
        ),
        "review_candidates": sum(
            1 for row in rows if row.get("work_kind") == "review_candidate"
        ),
        "research_article_candidates": sum(
            1 for row in rows if row.get("work_kind") == "research_article_candidate"
        ),
    }


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7F Source Decisions",
        "",
        "- Verification status: provisional_not_final",
        f"- Stop point recommendation: {summary['stop_point_recommendation']}",
        f"- Candidate decisions: {summary['candidate_count']}",
        f"- Provisional whitelist count: {summary['provisional_whitelist_count']}",
        f"- Review-gap subtopics: {', '.join(summary['review_gap_subtopics']) or 'none'}",
        "",
        "## Decision Counts",
        "",
        "| decision | count |",
        "| --- | ---: |",
    ]
    for decision, count in summary["decision_counts"].items():
        lines.append(f"| {decision} | {count} |")
    lines.extend(
        [
            "",
            "## Subtopic Decisions",
            "",
            "| subtopic | candidates | accepted | pending | rejected | whitelist | reviews |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for subtopic, values in summary["subtopics"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    subtopic,
                    str(values["candidate_count"]),
                    str(values["accepted_provisional"]),
                    str(values["pending_manual_review"]),
                    str(values["rejected_prescreen"]),
                    str(values["provisional_whitelist_count"]),
                    str(values["review_candidates"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "These decisions are provisional. Phase 7F is a planned stopping point for "
            "the current engineering/source-screening effort, not a claim that the "
            "full RAG.md demo-scale dataset has been produced.",
            "",
        ]
    )
    return "\n".join(lines)
