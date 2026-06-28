from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from io import BytesIO
import json
from pathlib import Path
from typing import Any, Callable

import requests

from domainrag.io_utils import read_jsonl, write_jsonl


MAX_DOWNLOAD_BYTES = 8_000_000
TEXT_SAMPLE_CHARS = 500
FullTextFetcher = Callable[[str], "FullTextResponse"]


@dataclass(frozen=True)
class FullTextResponse:
    final_url: str
    status_code: int
    content_type: str
    content: bytes
    truncated: bool = False


def parse_full_text(content: bytes, *, content_type: str) -> dict[str, Any]:
    normalized_type = content_type.split(";", 1)[0].strip().lower()
    try:
        if normalized_type == "application/pdf" or content.startswith(b"%PDF"):
            text = _parse_pdf(content)
        elif normalized_type in {"text/html", "application/xhtml+xml"}:
            text = _parse_html(content)
        elif normalized_type.startswith("text/"):
            text = content.decode("utf-8", errors="ignore")
        else:
            return {
                "parse_status": "unsupported_content_type",
                "extracted_chars": 0,
                "text_sample": "",
            }
    except Exception as exc:
        return {
            "parse_status": "parse_failed",
            "parse_error": str(exc),
            "extracted_chars": 0,
            "text_sample": "",
        }

    cleaned = " ".join(text.split())
    if not cleaned:
        return {
            "parse_status": "empty_text",
            "extracted_chars": 0,
            "text_sample": "",
        }
    return {
        "parse_status": "parseable",
        "extracted_chars": len(cleaned),
        "text_sample": cleaned[:TEXT_SAMPLE_CHARS],
    }


def probe_full_text_access(
    source_rows: list[dict[str, Any]],
    *,
    fetcher: FullTextFetcher | None = None,
    keep_text_sample: bool = False,
) -> list[dict[str, Any]]:
    active_fetcher = fetcher or fetch_full_text
    records: list[dict[str, Any]] = []
    for row in source_rows:
        source_id = str(row["source_id"])
        url = str(row.get("oa_url") or row.get("official_url") or "").strip()
        if not url:
            records.append(
                {
                    "source_id": source_id,
                    "source_url": None,
                    "access_status": "missing_url",
                    "parse_status": "not_attempted",
                    "http_status": None,
                    "content_type": None,
                    "bytes_downloaded": 0,
                    "extracted_chars": 0,
                }
            )
            continue
        try:
            response = active_fetcher(url)
        except Exception as exc:
            records.append(
                {
                    "source_id": source_id,
                    "source_url": url,
                    "access_status": "download_failed",
                    "parse_status": "not_attempted",
                    "http_status": None,
                    "content_type": None,
                    "bytes_downloaded": 0,
                    "extracted_chars": 0,
                    "access_error": str(exc),
                }
            )
            continue
        base = {
            "source_id": source_id,
            "source_url": url,
            "final_url": response.final_url,
            "http_status": response.status_code,
            "content_type": response.content_type,
            "bytes_downloaded": len(response.content),
        }
        if response.status_code < 200 or response.status_code >= 300:
            record = {
                **base,
                "access_status": "not_accessible",
                "parse_status": "not_attempted",
                "extracted_chars": 0,
            }
            if keep_text_sample:
                record["text_sample"] = ""
            records.append(record)
            continue
        if response.truncated:
            record = {
                **base,
                "access_status": "download_truncated",
                "parse_status": "not_attempted",
                "download_truncated": True,
                "extracted_chars": 0,
            }
            if keep_text_sample:
                record["text_sample"] = ""
            records.append(record)
            continue
        parsed = parse_full_text(response.content, content_type=response.content_type)
        if not keep_text_sample:
            parsed = {key: value for key, value in parsed.items() if key != "text_sample"}
        records.append(
            {
                **base,
                "access_status": "downloaded",
                **parsed,
            }
        )
    return records


def build_full_text_access_outputs(
    whitelist_path: Path,
    *,
    output_dir: Path,
    fetcher: FullTextFetcher | None = None,
    offset: int = 0,
    limit: int | None = None,
) -> tuple[Path, Path, Path]:
    source_rows = read_jsonl(whitelist_path)
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if offset:
        source_rows = source_rows[offset:]
    if limit is not None:
        source_rows = source_rows[:limit]
    records = probe_full_text_access(source_rows, fetcher=fetcher, keep_text_sample=False)
    summary = summarize_full_text_access(records)

    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "full_text_access.jsonl"
    summary_path = output_dir / "full_text_access_summary.json"
    markdown_path = output_dir / "full_text_access_summary.md"
    write_jsonl(records_path, records)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return records_path, summary_path, markdown_path


def combine_full_text_access_outputs(
    access_paths: list[Path],
    *,
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    records: list[dict[str, Any]] = []
    for path in access_paths:
        records.extend(read_jsonl(path))
    summary = summarize_full_text_access(records)

    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "full_text_access.jsonl"
    summary_path = output_dir / "full_text_access_summary.json"
    markdown_path = output_dir / "full_text_access_summary.md"
    write_jsonl(records_path, records)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return records_path, summary_path, markdown_path


def summarize_full_text_access(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "source_count": len(records),
        "access_status_counts": dict(
            sorted(Counter(str(row["access_status"]) for row in records).items())
        ),
        "parse_status_counts": dict(
            sorted(Counter(str(row["parse_status"]) for row in records).items())
        ),
        "parseable_count": sum(1 for row in records if row["parse_status"] == "parseable"),
        "total_extracted_chars": sum(int(row.get("extracted_chars") or 0) for row in records),
        "content_type_counts": dict(
            sorted(Counter(str(row.get("content_type") or "unknown") for row in records).items())
        ),
    }


def fetch_full_text(
    url: str,
    *,
    timeout_seconds: int = 30,
    max_bytes: int = MAX_DOWNLOAD_BYTES,
) -> FullTextResponse:
    response = requests.get(
        url,
        timeout=timeout_seconds,
        headers={"User-Agent": "DomainRAG-Bench/0.1"},
        stream=True,
    )
    chunks: list[bytes] = []
    downloaded = 0
    truncated = False
    for chunk in response.iter_content(chunk_size=65536):
        if not chunk:
            continue
        downloaded += len(chunk)
        if downloaded > max_bytes:
            truncated = True
            break
        chunks.append(chunk)
    return FullTextResponse(
        final_url=response.url,
        status_code=response.status_code,
        content_type=response.headers.get("content-type", ""),
        content=b"".join(chunks),
        truncated=truncated,
    )


def _parse_html(content: bytes) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    return soup.get_text(" ")


def _parse_pdf(content: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise RuntimeError("pypdf is required for PDF parsing") from exc

    reader = PdfReader(BytesIO(content))
    page_text: list[str] = []
    for page in reader.pages:
        page_text.append(page.extract_text() or "")
    return "\n".join(page_text)


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7G Full-Text Access",
        "",
        f"- Source rows checked: {summary['source_count']}",
        f"- Parseable rows: {summary['parseable_count']}",
        f"- Total extracted characters: {summary['total_extracted_chars']}",
        "",
        "## Parse Status Counts",
        "",
        "| status | count |",
        "| --- | ---: |",
    ]
    for status, count in summary["parse_status_counts"].items():
        lines.append(f"| {status} | {count} |")
    lines.append("")
    return "\n".join(lines)
