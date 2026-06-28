from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.full_text_chunk_extraction import (
    build_full_text_chunk_outputs,
    split_text_into_chunks,
)
from domainrag.full_text_intake import FullTextResponse
from domainrag.io_utils import write_jsonl


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_split_text_into_chunks_uses_token_windows_with_overlap():
    chunks = split_text_into_chunks(
        "alpha beta gamma delta epsilon zeta eta theta iota kappa",
        chunk_tokens=4,
        overlap_tokens=1,
        min_chunk_tokens=2,
    )

    assert chunks == [
        {
            "chunk_index": 1,
            "text": "alpha beta gamma delta",
            "token_count": 4,
            "token_start": 0,
            "token_end": 4,
        },
        {
            "chunk_index": 2,
            "text": "delta epsilon zeta eta",
            "token_count": 4,
            "token_start": 3,
            "token_end": 7,
        },
        {
            "chunk_index": 3,
            "text": "eta theta iota kappa",
            "token_count": 4,
            "token_start": 6,
            "token_end": 10,
        },
    ]


def test_build_full_text_chunk_outputs_writes_public_hash_manifest_without_text(
    tmp_path: Path,
):
    access_path = tmp_path / "full_text_access.jsonl"
    output_dir = tmp_path / "chunks"
    write_jsonl(
        access_path,
        [
            {
                "source_id": "openalex_W1",
                "source_url": "https://example.org/parseable",
                "final_url": "https://example.org/parseable",
                "access_status": "downloaded",
                "parse_status": "parseable",
                "content_type": "text/html",
                "extracted_chars": 120,
            },
            {
                "source_id": "openalex_W2",
                "source_url": "https://example.org/not-attempted",
                "access_status": "download_failed",
                "parse_status": "not_attempted",
                "content_type": None,
                "extracted_chars": 0,
            },
        ],
    )

    def fetcher(url: str) -> FullTextResponse:
        assert url == "https://example.org/parseable"
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="text/html",
            content=(
                b"<main>"
                b"Nickel superalloy creep oxidation fatigue coating microstructure "
                b"life prediction rupture rafting corrosion testing evidence."
                b"</main>"
            ),
        )

    chunks_path, manifest_path, summary_path, markdown_path = build_full_text_chunk_outputs(
        access_path,
        output_dir=output_dir,
        fetcher=fetcher,
        chunk_tokens=6,
        overlap_tokens=2,
        min_chunk_tokens=3,
        include_text=False,
    )

    chunks = _read_jsonl(chunks_path)
    manifest = _read_jsonl(manifest_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(chunks) >= 3
    assert all(row["source_id"] == "openalex_W1" for row in chunks)
    assert all("text" not in row for row in chunks)
    assert all("text_sample" not in row for row in chunks)
    assert all(len(row["text_sha256"]) == 64 for row in chunks)
    assert manifest[0]["chunk_status"] == "chunked"
    assert manifest[0]["chunk_count"] == len(chunks)
    assert manifest[1]["chunk_status"] == "skipped_not_parseable"
    assert summary["access_rows"] == 2
    assert summary["sources_attempted"] == 1
    assert summary["sources_chunked"] == 1
    assert summary["chunk_count"] == len(chunks)
    assert summary["include_text"] is False
    assert "Phase 7L Full-Text Chunk Extraction" in markdown


def test_build_full_text_chunk_outputs_can_include_text_when_explicit(tmp_path: Path):
    access_path = tmp_path / "full_text_access.jsonl"
    write_jsonl(
        access_path,
        [
            {
                "source_id": "openalex_W1",
                "source_url": "https://example.org/parseable",
                "access_status": "downloaded",
                "parse_status": "parseable",
                "content_type": "text/plain",
                "extracted_chars": 120,
            }
        ],
    )

    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="text/plain",
            content=b"alpha beta gamma delta epsilon zeta eta theta",
        )

    chunks_path, _manifest_path, _summary_path, _markdown_path = build_full_text_chunk_outputs(
        access_path,
        output_dir=tmp_path / "with_text",
        fetcher=fetcher,
        chunk_tokens=4,
        overlap_tokens=1,
        min_chunk_tokens=2,
        include_text=True,
    )

    chunks = _read_jsonl(chunks_path)

    assert chunks[0]["text"] == "alpha beta gamma delta"
    assert chunks[0]["text_sha256"]


def test_build_full_text_chunk_outputs_rejects_bad_window_parameters(tmp_path: Path):
    access_path = tmp_path / "full_text_access.jsonl"
    write_jsonl(access_path, [])

    with pytest.raises(ValueError, match="chunk_tokens must be positive"):
        build_full_text_chunk_outputs(access_path, output_dir=tmp_path / "bad", chunk_tokens=0)

    with pytest.raises(ValueError, match="overlap_tokens must be smaller than chunk_tokens"):
        build_full_text_chunk_outputs(
            access_path,
            output_dir=tmp_path / "bad",
            chunk_tokens=4,
            overlap_tokens=4,
        )
