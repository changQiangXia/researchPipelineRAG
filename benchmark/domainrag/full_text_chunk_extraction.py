from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from domainrag.full_text_intake import (
    FullTextFetcher,
    FullTextResponse,
    _parse_html,
    _parse_pdf,
    fetch_full_text,
)
from domainrag.io_utils import read_jsonl, write_jsonl


TOKEN_PATTERN = re.compile(r"\S+")
DEFAULT_CHUNK_TOKENS = 350
DEFAULT_OVERLAP_TOKENS = 50
DEFAULT_MIN_CHUNK_TOKENS = 80
PROVENANCE_STATUS = "machine_parseable_not_human_final"


def split_text_into_chunks(
    text: str,
    *,
    chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
    min_chunk_tokens: int = DEFAULT_MIN_CHUNK_TOKENS,
) -> list[dict[str, Any]]:
    _validate_chunk_parameters(
        chunk_tokens=chunk_tokens,
        overlap_tokens=overlap_tokens,
        min_chunk_tokens=min_chunk_tokens,
    )
    tokens = _tokens(text)
    if len(tokens) < min_chunk_tokens:
        return []
    chunks: list[dict[str, Any]] = []
    step = chunk_tokens - overlap_tokens
    start = 0
    while start < len(tokens):
        end = min(start + chunk_tokens, len(tokens))
        window = tokens[start:end]
        if len(window) < min_chunk_tokens:
            break
        chunks.append(
            {
                "chunk_index": len(chunks) + 1,
                "text": " ".join(window),
                "token_count": len(window),
                "token_start": start,
                "token_end": end,
            }
        )
        if end == len(tokens):
            break
        start += step
    return chunks


def build_full_text_chunk_outputs(
    access_path: Path,
    *,
    output_dir: Path,
    fetcher: FullTextFetcher | None = None,
    chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
    min_chunk_tokens: int = DEFAULT_MIN_CHUNK_TOKENS,
    include_text: bool = False,
    max_sources: int | None = None,
) -> tuple[Path, Path, Path, Path]:
    _validate_chunk_parameters(
        chunk_tokens=chunk_tokens,
        overlap_tokens=overlap_tokens,
        min_chunk_tokens=min_chunk_tokens,
    )
    if max_sources is not None and max_sources < 0:
        raise ValueError("max_sources must be non-negative")

    access_rows = read_jsonl(access_path)
    active_fetcher = fetcher or fetch_full_text
    chunks: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    attempted_sources = 0

    for row in access_rows:
        source_id = str(row["source_id"])
        if not _is_parseable_access_row(row):
            manifest.append(_manifest_row(row, chunk_status="skipped_not_parseable"))
            continue
        if max_sources is not None and attempted_sources >= max_sources:
            manifest.append(_manifest_row(row, chunk_status="skipped_max_sources"))
            continue
        url = str(row.get("source_url") or row.get("final_url") or "").strip()
        if not url:
            manifest.append(_manifest_row(row, chunk_status="skipped_missing_url"))
            continue

        attempted_sources += 1
        try:
            response = active_fetcher(url)
            status, source_chunks, error = _chunk_response(
                source_id=source_id,
                row=row,
                response=response,
                chunk_tokens=chunk_tokens,
                overlap_tokens=overlap_tokens,
                min_chunk_tokens=min_chunk_tokens,
                include_text=include_text,
            )
        except Exception as exc:
            status = "download_or_parse_failed"
            source_chunks = []
            error = str(exc)

        chunks.extend(source_chunks)
        manifest.append(
            _manifest_row(
                row,
                chunk_status=status,
                chunk_count=len(source_chunks),
                fetched_url=url,
                error=error,
            )
        )

    summary = summarize_chunk_extraction(
        access_rows=access_rows,
        manifest=manifest,
        chunks=chunks,
        include_text=include_text,
        chunk_tokens=chunk_tokens,
        overlap_tokens=overlap_tokens,
        min_chunk_tokens=min_chunk_tokens,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    chunks_path = output_dir / "full_text_chunks.jsonl"
    manifest_path = output_dir / "chunk_source_manifest.jsonl"
    summary_path = output_dir / "chunk_extraction_summary.json"
    markdown_path = output_dir / "chunk_extraction_summary.md"
    write_jsonl(chunks_path, chunks)
    write_jsonl(manifest_path, manifest)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return chunks_path, manifest_path, summary_path, markdown_path


def summarize_chunk_extraction(
    *,
    access_rows: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
    include_text: bool,
    chunk_tokens: int,
    overlap_tokens: int,
    min_chunk_tokens: int,
) -> dict[str, Any]:
    return {
        "phase": "Phase 7L",
        "access_rows": len(access_rows),
        "parseable_access_rows": sum(1 for row in access_rows if _is_parseable_access_row(row)),
        "sources_attempted": sum(
            1
            for row in manifest
            if row["chunk_status"]
            not in {
                "skipped_not_parseable",
                "skipped_missing_url",
                "skipped_max_sources",
            }
        ),
        "sources_chunked": sum(1 for row in manifest if row["chunk_status"] == "chunked"),
        "chunk_count": len(chunks),
        "chunk_status_counts": dict(
            sorted(Counter(row["chunk_status"] for row in manifest).items())
        ),
        "total_chunk_tokens": sum(int(row["token_count"]) for row in chunks),
        "total_chunk_chars": sum(int(row["char_count"]) for row in chunks),
        "chunk_tokens": chunk_tokens,
        "overlap_tokens": overlap_tokens,
        "min_chunk_tokens": min_chunk_tokens,
        "include_text": include_text,
        "provenance_status": PROVENANCE_STATUS,
        "raw_text_storage_policy": (
            "chunk text included by explicit request"
            if include_text
            else "chunk text omitted; text_sha256 retained"
        ),
    }


def _chunk_response(
    *,
    source_id: str,
    row: dict[str, Any],
    response: FullTextResponse,
    chunk_tokens: int,
    overlap_tokens: int,
    min_chunk_tokens: int,
    include_text: bool,
) -> tuple[str, list[dict[str, Any]], str | None]:
    if response.status_code < 200 or response.status_code >= 300:
        return "not_accessible", [], None
    if response.truncated:
        return "download_truncated", [], None
    text = _extract_text(response.content, content_type=response.content_type)
    extracted_chunks = split_text_into_chunks(
        text,
        chunk_tokens=chunk_tokens,
        overlap_tokens=overlap_tokens,
        min_chunk_tokens=min_chunk_tokens,
    )
    if not extracted_chunks:
        return "too_short", [], None
    output_chunks = [
        _chunk_row(
            source_id=source_id,
            row=row,
            extracted=chunk,
            include_text=include_text,
        )
        for chunk in extracted_chunks
    ]
    return "chunked", output_chunks, None


def _chunk_row(
    *,
    source_id: str,
    row: dict[str, Any],
    extracted: dict[str, Any],
    include_text: bool,
) -> dict[str, Any]:
    text = str(extracted["text"])
    chunk_index = int(extracted["chunk_index"])
    chunk = {
        "chunk_id": f"{source_id}_chunk_{chunk_index:04d}",
        "source_id": source_id,
        "chunk_index": chunk_index,
        "token_start": int(extracted["token_start"]),
        "token_end": int(extracted["token_end"]),
        "token_count": int(extracted["token_count"]),
        "char_count": len(text),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "source_parse_status": row.get("parse_status"),
        "source_access_status": row.get("access_status"),
        "content_type": row.get("content_type"),
        "provenance_status": PROVENANCE_STATUS,
    }
    if include_text:
        chunk["text"] = text
    return chunk


def _manifest_row(
    row: dict[str, Any],
    *,
    chunk_status: str,
    chunk_count: int = 0,
    fetched_url: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    record = {
        "source_id": str(row["source_id"]),
        "source_url": row.get("source_url"),
        "final_url": row.get("final_url"),
        "access_status": row.get("access_status"),
        "parse_status": row.get("parse_status"),
        "content_type": row.get("content_type"),
        "source_extracted_chars": int(row.get("extracted_chars") or 0),
        "chunk_status": chunk_status,
        "chunk_count": chunk_count,
    }
    if fetched_url:
        record["fetched_url"] = fetched_url
    if error:
        record["chunk_error"] = error
    return record


def _extract_text(content: bytes, *, content_type: str) -> str:
    normalized_type = content_type.split(";", 1)[0].strip().lower()
    if normalized_type == "application/pdf" or content.startswith(b"%PDF"):
        text = _parse_pdf(content)
    elif normalized_type in {"text/html", "application/xhtml+xml"}:
        text = _parse_html(content)
    elif normalized_type.startswith("text/"):
        text = content.decode("utf-8", errors="ignore")
    else:
        text = ""
    return " ".join(text.split())


def _is_parseable_access_row(row: dict[str, Any]) -> bool:
    return row.get("access_status") == "downloaded" and row.get("parse_status") == "parseable"


def _validate_chunk_parameters(
    *,
    chunk_tokens: int,
    overlap_tokens: int,
    min_chunk_tokens: int,
) -> None:
    if chunk_tokens <= 0:
        raise ValueError("chunk_tokens must be positive")
    if overlap_tokens < 0:
        raise ValueError("overlap_tokens must be non-negative")
    if overlap_tokens >= chunk_tokens:
        raise ValueError("overlap_tokens must be smaller than chunk_tokens")
    if min_chunk_tokens <= 0:
        raise ValueError("min_chunk_tokens must be positive")
    if min_chunk_tokens > chunk_tokens:
        raise ValueError("min_chunk_tokens must be smaller than or equal to chunk_tokens")


def _tokens(text: str) -> list[str]:
    return [match.group(0) for match in TOKEN_PATTERN.finditer(text)]


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 7L Full-Text Chunk Extraction",
        "",
        f"- Access rows: {summary['access_rows']}",
        f"- Parseable access rows: {summary['parseable_access_rows']}",
        f"- Sources attempted: {summary['sources_attempted']}",
        f"- Sources chunked: {summary['sources_chunked']}",
        f"- Chunk count: {summary['chunk_count']}",
        f"- Include text: {str(summary['include_text']).lower()}",
        f"- Raw text storage policy: {summary['raw_text_storage_policy']}",
        "",
        "## Chunk Status Counts",
        "",
        "| status | count |",
        "| --- | ---: |",
    ]
    for status, count in summary["chunk_status_counts"].items():
        lines.append(f"| {status} | {count} |")
    lines.append("")
    return "\n".join(lines)
