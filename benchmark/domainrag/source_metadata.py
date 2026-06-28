from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from domainrag.io_utils import read_jsonl, write_jsonl


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
MetadataFetcher = Callable[[str], dict[str, Any]]


def normalize_openalex_metadata(source_row: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    primary_location = payload.get("primary_location")
    if not isinstance(primary_location, dict):
        primary_location = {}
    source = primary_location.get("source")
    if not isinstance(source, dict):
        source = {}
    return {
        "source_id": str(source_row["source_id"]),
        "metadata_status": "found",
        "openalex_id": _string_or_none(payload.get("id")),
        "doi": _string_or_none(payload.get("doi")),
        "title": _string_or_none(payload.get("display_name") or payload.get("title")),
        "publication_year": _int_or_none(payload.get("publication_year")),
        "publication_date": _string_or_none(payload.get("publication_date")),
        "type": _string_or_none(payload.get("type")),
        "is_retracted": bool(payload.get("is_retracted")),
        "venue": _string_or_none(source.get("display_name")),
        "venue_type": _string_or_none(source.get("type")),
    }


def collect_openalex_metadata(
    source_rows: list[dict[str, Any]],
    *,
    fetcher: MetadataFetcher | None = None,
) -> list[dict[str, Any]]:
    active_fetcher = fetcher or fetch_openalex_work_by_doi
    records: list[dict[str, Any]] = []
    for row in source_rows:
        doi = str(row.get("doi") or "").strip()
        source_id = str(row["source_id"])
        if not doi:
            records.append(
                {
                    "source_id": source_id,
                    "metadata_status": "missing_doi",
                    "metadata_error": "source row has no DOI",
                }
            )
            continue
        try:
            payload = active_fetcher(doi)
        except OSError as exc:
            records.append(
                {
                    "source_id": source_id,
                    "metadata_status": "error",
                    "metadata_error": str(exc),
                }
            )
            continue
        if not payload:
            records.append(
                {
                    "source_id": source_id,
                    "metadata_status": "not_found",
                    "metadata_error": "OpenAlex returned no work",
                }
            )
            continue
        records.append(normalize_openalex_metadata(row, payload))
    return records


def build_openalex_metadata_outputs(
    whitelist_path: Path,
    *,
    output_dir: Path,
    fetcher: MetadataFetcher | None = None,
) -> tuple[Path, Path, Path]:
    source_rows = read_jsonl(whitelist_path)
    records = collect_openalex_metadata(source_rows, fetcher=fetcher)
    summary = summarize_openalex_metadata(records)

    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "openalex_metadata.jsonl"
    summary_path = output_dir / "openalex_metadata_summary.json"
    markdown_path = output_dir / "openalex_metadata_summary.md"
    write_jsonl(records_path, records)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return records_path, summary_path, markdown_path


def summarize_openalex_metadata(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "source_count": len(records),
        "metadata_status_counts": dict(
            sorted(Counter(str(row["metadata_status"]) for row in records).items())
        ),
        "retracted_count": sum(1 for row in records if row.get("is_retracted") is True),
        "type_counts": dict(
            sorted(
                Counter(str(row.get("type") or "unknown") for row in records).items()
            )
        ),
        "venue_type_counts": dict(
            sorted(
                Counter(str(row.get("venue_type") or "unknown") for row in records).items()
            )
        ),
    }


def fetch_openalex_work_by_doi(
    doi: str,
    *,
    timeout_seconds: int = 30,
    mailto: str | None = None,
) -> dict[str, Any]:
    params = {}
    if mailto:
        params["mailto"] = mailto
    suffix = f"/doi:{quote(doi, safe='')}"
    query = f"?{urlencode(params)}" if params else ""
    request = Request(
        f"{OPENALEX_WORKS_URL}{suffix}{query}",
        headers={"User-Agent": "DomainRAG-Bench/0.1"},
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7G OpenAlex Metadata",
        "",
        f"- Source rows checked: {summary['source_count']}",
        f"- Retracted rows: {summary['retracted_count']}",
        "",
        "## Metadata Status Counts",
        "",
        "| status | count |",
        "| --- | ---: |",
    ]
    for status, count in summary["metadata_status_counts"].items():
        lines.append(f"| {status} | {count} |")
    lines.append("")
    return "\n".join(lines)
