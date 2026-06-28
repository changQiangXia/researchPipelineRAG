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


MANUAL_VERIFICATION_TASKS = [
    "verify_venue_metric_or_flagship_status",
    "verify_full_text_processability",
    "verify_article_type",
    "verify_retraction_status",
    "verify_domain_relevance",
]
REVIEW_TARGET_PER_SUBTOPIC = 1
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def screen_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    domain_terms = [
        str(term)
        for term in candidate.get("domain_relevance_terms", [])
        if isinstance(term, str) and term.strip()
    ]
    venue_status = _string_or_default(
        candidate.get("venue_whitelist_status"),
        "needs_venue_metric_verification",
    )
    full_text_status = _full_text_status(candidate)
    full_text_queue_status = (
        "ready_for_full_text_download_attempt"
        if full_text_status == "open_access_full_text_candidate"
        else "needs_access_check"
    )
    priority = _screening_priority(
        venue_status=venue_status,
        full_text_status=full_text_status,
        domain_term_count=len(domain_terms),
    )

    row = dict(candidate)
    row.update(
        {
            "screening_status": "needs_manual_verification",
            "screening_priority": priority,
            "screening_reasons": _screening_reasons(
                venue_status=venue_status,
                full_text_status=full_text_status,
                domain_term_count=len(domain_terms),
            ),
            "manual_verification_tasks": MANUAL_VERIFICATION_TASKS,
            "full_text_status": full_text_status,
            "full_text_queue_status": full_text_queue_status,
            "final_inclusion_status": "not_finalized",
            "verification_status": "machine_prescreen_only",
        }
    )
    return row


def summarize_screening(rows: list[dict[str, Any]]) -> dict[str, Any]:
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

    return {
        "candidate_count": len(rows),
        "final_included_sources": 0,
        "verification_status": "machine_prescreen_only",
        "priority_counts": _ordered_counter(
            row["screening_priority"] for row in rows
        ),
        "screening_status_counts": _ordered_counter(
            row["screening_status"] for row in rows
        ),
        "full_text_status_counts": _ordered_counter(
            row["full_text_status"] for row in rows
        ),
        "full_text_queue_status_counts": _ordered_counter(
            row["full_text_queue_status"] for row in rows
        ),
        "full_text_ready_candidates": sum(
            1
            for row in rows
            if row["full_text_queue_status"] == "ready_for_full_text_download_attempt"
        ),
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
        "limitations": [
            "machine pre-screening only",
            "venue metrics still require manual verification",
            "full-text processability still requires download and parsing verification",
            "article type and retraction status still require publisher/database checks",
            "domain relevance still requires manual title/abstract/full-text screening",
        ],
    }


def build_screening_outputs(
    candidates_path: Path,
    *,
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    candidates = read_jsonl(candidates_path)
    rows = sorted(
        (screen_candidate(candidate) for candidate in candidates),
        key=lambda row: (
            PRIORITY_ORDER[row["screening_priority"]],
            row["subtopic"],
            -int(row.get("year") or 0),
            row["source_id"],
        ),
    )
    summary = summarize_screening(rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    queue_path = output_dir / "screening_queue.jsonl"
    summary_path = output_dir / "screening_summary.json"
    markdown_path = output_dir / "summary.md"

    write_jsonl(queue_path, rows)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return queue_path, summary_path, markdown_path


def _full_text_status(candidate: dict[str, Any]) -> str:
    if bool(candidate.get("open_access")) and _string_or_none(candidate.get("oa_url")):
        return "open_access_full_text_candidate"
    if _string_or_none(candidate.get("official_url")):
        return "landing_page_only"
    return "missing_access_url"


def _screening_priority(
    *,
    venue_status: str,
    full_text_status: str,
    domain_term_count: int,
) -> str:
    has_full_text_candidate = full_text_status == "open_access_full_text_candidate"
    has_strong_domain_match = domain_term_count >= 2
    has_top_venue_signal = venue_status == "candidate_top_venue_or_domain_flagship"
    if has_top_venue_signal and has_full_text_candidate and has_strong_domain_match:
        return "high"
    if has_full_text_candidate and has_strong_domain_match:
        return "medium"
    return "low"


def _screening_reasons(
    *,
    venue_status: str,
    full_text_status: str,
    domain_term_count: int,
) -> list[str]:
    return [
        venue_status,
        full_text_status,
        (
            "strong_domain_term_match"
            if domain_term_count >= 2
            else "weak_domain_term_match"
        ),
    ]


def _subtopic_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_count": len(rows),
        "high_priority_candidates": sum(
            1 for row in rows if row["screening_priority"] == "high"
        ),
        "medium_priority_candidates": sum(
            1 for row in rows if row["screening_priority"] == "medium"
        ),
        "low_priority_candidates": sum(
            1 for row in rows if row["screening_priority"] == "low"
        ),
        "full_text_ready_candidates": sum(
            1
            for row in rows
            if row["full_text_queue_status"] == "ready_for_full_text_download_attempt"
        ),
        "research_article_candidates": sum(
            1 for row in rows if row.get("work_kind") == "research_article_candidate"
        ),
        "review_candidates": sum(
            1 for row in rows if row.get("work_kind") == "review_candidate"
        ),
    }


def _ordered_counter(values: Any) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7E Source Screening Queue",
        "",
        "- Verification status: machine_prescreen_only",
        f"- Candidate papers queued: {summary['candidate_count']}",
        f"- Final included sources: {summary['final_included_sources']}",
        f"- Full-text ready candidates: {summary['full_text_ready_candidates']}",
        f"- Review-gap subtopics: {', '.join(summary['review_gap_subtopics']) or 'none'}",
        "",
        "## Priority Counts",
        "",
        "| priority | count |",
        "| --- | ---: |",
    ]
    for priority, count in summary["priority_counts"].items():
        lines.append(f"| {priority} | {count} |")

    lines.extend(
        [
            "",
            "## Subtopic Queue",
            "",
            "| subtopic | candidates | high | medium | low | full-text ready | reviews |",
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
                    str(values["high_priority_candidates"]),
                    str(values["medium_priority_candidates"]),
                    str(values["low_priority_candidates"]),
                    str(values["full_text_ready_candidates"]),
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
            "This queue is a deterministic machine pre-screen. It is not a final "
            "source whitelist and does not replace manual venue, full-text, article-type, "
            "retraction, or domain-relevance verification.",
            "",
        ]
    )
    return "\n".join(lines)


def _string_or_default(value: Any, default: str) -> str:
    return _string_or_none(value) or default


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
