from __future__ import annotations

from collections import Counter, defaultdict
import json
import re
from pathlib import Path
from typing import Any

from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.source_acquisition import DEMO_SOURCE_TARGET


VERIFICATION_CHECKS = (
    "venue_metric",
    "doi_title_year",
    "article_type",
    "retraction",
    "full_text_processability",
    "domain_relevance",
)
FINAL_ACCEPTED_STATUS = "accepted_final_verification"
READY_FOR_MANUAL_STATUS = "ready_for_manual_finalization"
REJECTED_STATUS = "rejected_verification"
VERIFIED_STATUS = "verified_source_candidate"
STATUS_ORDER = {
    READY_FOR_MANUAL_STATUS: 0,
    REJECTED_STATUS: 1,
    VERIFIED_STATUS: 2,
    "needs_evidence": 3,
}
ACCEPTABLE_RESEARCH_TYPES = {"article", "preprint"}
ACCEPTABLE_REVIEW_TYPES = {"article", "review"}
MIN_FULL_TEXT_CHARS = 1000


def verify_source(
    row: dict[str, Any],
    *,
    metadata: dict[str, Any] | None = None,
    access: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checks = {
        "venue_metric": _verify_venue(row),
        "doi_title_year": _verify_doi_title_year(row, metadata),
        "article_type": _verify_article_type(row, metadata),
        "retraction": _verify_retraction(metadata),
        "full_text_processability": _verify_full_text(access),
        "domain_relevance": _verify_domain_relevance(row),
    }
    reasons = _verification_reasons(checks)
    status, final_inclusion_status = _source_status(checks)

    verified = dict(row)
    verified.update(
        {
            "source_verification_status": status,
            "final_inclusion_status": final_inclusion_status,
            "verification_checks": checks,
            "verification_reasons": reasons,
            "metadata_evidence_status": "provided" if metadata else "missing",
            "full_text_evidence_status": "provided" if access else "missing",
        }
    )
    return verified


def summarize_verifications(rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = _ordered_status_counts(row["source_verification_status"] for row in rows)
    accepted_count = sum(
        1 for row in rows if row["final_inclusion_status"] == FINAL_ACCEPTED_STATUS
    )
    ready_count = status_counts.get(READY_FOR_MANUAL_STATUS, 0)
    rejected_count = status_counts.get(REJECTED_STATUS, 0)
    subtopics: dict[str, dict[str, int]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("subtopic", "unknown"))].append(row)
    for subtopic, subtopic_rows in sorted(grouped.items()):
        subtopics[subtopic] = {
            "source_count": len(subtopic_rows),
            "accepted_final_verification": sum(
                1
                for row in subtopic_rows
                if row["final_inclusion_status"] == FINAL_ACCEPTED_STATUS
            ),
            "ready_for_manual_finalization": sum(
                1
                for row in subtopic_rows
                if row["source_verification_status"] == READY_FOR_MANUAL_STATUS
            ),
            "rejected_verification": sum(
                1
                for row in subtopic_rows
                if row["source_verification_status"] == REJECTED_STATUS
            ),
        }

    target_min, target_max = DEMO_SOURCE_TARGET
    final_whitelist_claim = (
        "complete" if target_min <= accepted_count <= target_max else "not_complete"
    )
    return {
        "source_count": len(rows),
        "status_counts": status_counts,
        "accepted_final_verification_count": accepted_count,
        "ready_for_manual_finalization_count": ready_count,
        "rejected_verification_count": rejected_count,
        "final_whitelist_claim": final_whitelist_claim,
        "target_final_source_whitelist": DEMO_SOURCE_TARGET,
        "verification_status": "machine_assisted_not_human_final",
        "subtopic_count": len(subtopics),
        "subtopics": subtopics,
        "remaining_gaps": [
            "manual JCR/CiteScore or flagship venue confirmation for pending rows",
            "human final inclusion sign-off",
            "full 1,000-3,000 chunk and 300-500 question demo-scale production",
        ],
    }


def build_verification_outputs(
    whitelist_path: Path,
    *,
    output_dir: Path,
    metadata_path: Path | None = None,
    access_path: Path | None = None,
) -> tuple[Path, Path, Path, Path]:
    whitelist_rows = read_jsonl(whitelist_path)
    metadata_by_source = _records_by_source_id(metadata_path)
    access_by_source = _records_by_source_id(access_path)
    matrix = [
        verify_source(
            row,
            metadata=metadata_by_source.get(str(row["source_id"])),
            access=access_by_source.get(str(row["source_id"])),
        )
        for row in whitelist_rows
    ]
    final_queue = [
        row for row in matrix if row["final_inclusion_status"] == FINAL_ACCEPTED_STATUS
    ]
    summary = summarize_verifications(matrix)

    output_dir.mkdir(parents=True, exist_ok=True)
    matrix_path = output_dir / "source_verification_matrix.jsonl"
    final_queue_path = output_dir / "final_verification_queue.jsonl"
    summary_path = output_dir / "verification_summary.json"
    markdown_path = output_dir / "summary.md"
    write_jsonl(matrix_path, matrix)
    write_jsonl(final_queue_path, final_queue)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return matrix_path, final_queue_path, summary_path, markdown_path


def _verify_venue(row: dict[str, Any]) -> str:
    if row.get("venue_whitelist_status") == "candidate_top_venue_or_domain_flagship":
        return "verified"
    return "pending_manual"


def _verify_doi_title_year(row: dict[str, Any], metadata: dict[str, Any] | None) -> str:
    if metadata is None:
        return "pending_evidence"
    row_doi = _normalize_doi(row.get("doi"))
    meta_doi = _normalize_doi(metadata.get("doi"))
    row_title = _normalize_title(row.get("title"))
    meta_title = _normalize_title(metadata.get("title") or metadata.get("display_name"))
    row_year = _int_or_none(row.get("year"))
    meta_year = _int_or_none(metadata.get("publication_year") or metadata.get("year"))
    if row_doi and meta_doi and row_doi == meta_doi and row_title == meta_title and row_year == meta_year:
        return "verified"
    return "failed"


def _verify_article_type(row: dict[str, Any], metadata: dict[str, Any] | None) -> str:
    raw_type = str((metadata or {}).get("type") or row.get("work_type") or "").lower()
    work_kind = str(row.get("work_kind") or "").lower()
    if work_kind == "review_candidate":
        return "verified" if raw_type in ACCEPTABLE_REVIEW_TYPES else "failed"
    if work_kind == "research_article_candidate":
        return "verified" if raw_type in ACCEPTABLE_RESEARCH_TYPES else "failed"
    return "pending_manual"


def _verify_retraction(metadata: dict[str, Any] | None) -> str:
    if metadata is None or "is_retracted" not in metadata:
        return "pending_evidence"
    return "failed" if bool(metadata["is_retracted"]) else "verified"


def _verify_full_text(access: dict[str, Any] | None) -> str:
    if access is None:
        return "pending_evidence"
    if (
        access.get("parse_status") == "parseable"
        and int(access.get("extracted_chars") or 0) >= MIN_FULL_TEXT_CHARS
    ):
        return "verified"
    return "pending_manual"


def _verify_domain_relevance(row: dict[str, Any]) -> str:
    terms = [
        term
        for term in row.get("domain_relevance_terms", [])
        if isinstance(term, str) and term.strip()
    ]
    return "verified" if len(terms) >= 2 else "pending_manual"


def _source_status(checks: dict[str, str]) -> tuple[str, str]:
    if any(value == "failed" for value in checks.values()):
        return REJECTED_STATUS, "rejected_after_verification"
    if all(value == "verified" for value in checks.values()):
        return VERIFIED_STATUS, "not_finalized"
    if all(value in {"verified", "pending_manual"} for value in checks.values()):
        return READY_FOR_MANUAL_STATUS, "not_finalized"
    return "needs_evidence", "not_finalized"


def _verification_reasons(checks: dict[str, str]) -> list[str]:
    if any(value == "failed" for value in checks.values()):
        return [
            f"{name}:{value}"
            for name, value in checks.items()
            if value == "failed"
        ]
    if all(value == "verified" for value in checks.values()):
        return ["all_machine_checks_verified_requires_human_final_signoff"]
    reasons = [
        f"{name}_requires_manual_or_external_metric_check"
        for name, value in checks.items()
        if value == "pending_manual"
    ]
    reasons.extend(
        f"{name}_requires_external_evidence"
        for name, value in checks.items()
        if value == "pending_evidence"
    )
    return reasons


def _records_by_source_id(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    return {str(row["source_id"]): row for row in read_jsonl(path)}


def _ordered_status_counts(values: Any) -> dict[str, int]:
    return dict(
        sorted(
            Counter(str(value) for value in values).items(),
            key=lambda item: (STATUS_ORDER.get(item[0], 99), item[0]),
        )
    )


def _normalize_doi(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:", "", text)
    return text.strip()


def _normalize_title(value: Any) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7G Source Verification",
        "",
        f"- Verification status: {summary['verification_status']}",
        f"- Final whitelist claim: {summary['final_whitelist_claim']}",
        f"- Source rows checked: {summary['source_count']}",
        f"- Accepted final verification rows: {summary['accepted_final_verification_count']}",
        f"- Ready for manual finalization rows: {summary['ready_for_manual_finalization_count']}",
        f"- Rejected after verification rows: {summary['rejected_verification_count']}",
        "",
        "## Status Counts",
        "",
        "| status | count |",
        "| --- | ---: |",
    ]
    for status, count in summary["status_counts"].items():
        lines.append(f"| {status} | {count} |")
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "This is a machine-assisted verification matrix. It does not replace "
            "human final source sign-off or subscription venue metric checks.",
            "",
        ]
    )
    return "\n".join(lines)
