from __future__ import annotations

import json
from pathlib import Path

from domainrag import full_text_intake
from domainrag.full_text_intake import (
    FullTextResponse,
    build_full_text_access_outputs,
    parse_full_text,
    probe_full_text_access,
)
from domainrag.io_utils import write_jsonl


def _source_row(source_id: str = "openalex_W1", oa_url: str = "https://example.org/paper") -> dict:
    return {
        "source_id": source_id,
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
        "subtopic": "oxidation",
        "oa_url": oa_url,
        "official_url": "https://doi.org/10.1234/example",
    }


def test_parse_full_text_extracts_html_text():
    parsed = parse_full_text(
        b"<html><body><h1>Title</h1><p>Nickel superalloy oxidation evidence.</p></body></html>",
        content_type="text/html; charset=utf-8",
    )

    assert parsed["parse_status"] == "parseable"
    assert parsed["extracted_chars"] >= 35
    assert "Nickel superalloy oxidation evidence" in parsed["text_sample"]


def test_probe_full_text_access_records_downloaded_and_parseable():
    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="text/html",
            content=b"<p>Nickel superalloy creep and oxidation full text.</p>",
        )

    rows = [_source_row()]

    records = probe_full_text_access(rows, fetcher=fetcher)

    assert records[0]["access_status"] == "downloaded"
    assert records[0]["parse_status"] == "parseable"
    assert records[0]["bytes_downloaded"] > 0
    assert records[0]["extracted_chars"] > 0


def test_probe_full_text_access_records_failed_http_status():
    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=403,
            content_type="text/html",
            content=b"Forbidden",
        )

    records = probe_full_text_access([_source_row()], fetcher=fetcher)

    assert records[0]["access_status"] == "not_accessible"
    assert records[0]["parse_status"] == "not_attempted"
    assert records[0]["http_status"] == 403
    assert "text_sample" not in records[0]


def test_probe_full_text_access_marks_truncated_download_without_parsing():
    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="application/pdf",
            content=b"%PDF-1.7 incomplete",
            truncated=True,
        )

    records = probe_full_text_access([_source_row()], fetcher=fetcher)

    assert records[0]["access_status"] == "download_truncated"
    assert records[0]["parse_status"] == "not_attempted"
    assert records[0]["download_truncated"] is True
    assert records[0]["extracted_chars"] == 0
    assert "text_sample" not in records[0]


def test_build_full_text_access_outputs_writes_records_summary_and_markdown(
    tmp_path: Path,
):
    whitelist = tmp_path / "provisional_source_whitelist.jsonl"
    output = tmp_path / "full_text"
    write_jsonl(
        whitelist,
        [
            _source_row(source_id="openalex_W1"),
            _source_row(source_id="openalex_W2"),
        ],
    )

    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="text/html",
            content=b"<p>Nickel superalloy oxidation parseable full text.</p>",
        )

    records_path, summary_path, markdown_path = build_full_text_access_outputs(
        whitelist,
        output_dir=output,
        fetcher=fetcher,
    )

    records = [
        json.loads(line)
        for line in records_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(records) == 2
    assert summary["source_count"] == 2
    assert summary["parse_status_counts"] == {"parseable": 2}
    assert summary["parseable_count"] == 2
    assert "Phase 7G Full-Text Access" in markdown


def test_build_full_text_access_outputs_can_limit_probe_batch(tmp_path: Path):
    whitelist = tmp_path / "provisional_source_whitelist.jsonl"
    output = tmp_path / "full_text"
    write_jsonl(
        whitelist,
        [
            _source_row(source_id="openalex_W1"),
            _source_row(source_id="openalex_W2"),
        ],
    )

    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="text/html",
            content=b"<p>Nickel superalloy oxidation parseable full text.</p>",
        )

    records_path, summary_path, _ = build_full_text_access_outputs(
        whitelist,
        output_dir=output,
        fetcher=fetcher,
        limit=1,
    )

    assert len(records_path.read_text(encoding="utf-8").splitlines()) == 1
    assert json.loads(summary_path.read_text(encoding="utf-8"))["source_count"] == 1


def test_build_full_text_access_outputs_can_offset_probe_batch(tmp_path: Path):
    whitelist = tmp_path / "provisional_source_whitelist.jsonl"
    output = tmp_path / "full_text"
    write_jsonl(
        whitelist,
        [
            _source_row(source_id="openalex_W1"),
            _source_row(source_id="openalex_W2"),
            _source_row(source_id="openalex_W3"),
        ],
    )

    def fetcher(url: str) -> FullTextResponse:
        return FullTextResponse(
            final_url=url,
            status_code=200,
            content_type="text/html",
            content=b"<p>Nickel superalloy oxidation parseable full text.</p>",
        )

    records_path, summary_path, _ = build_full_text_access_outputs(
        whitelist,
        output_dir=output,
        fetcher=fetcher,
        offset=1,
        limit=1,
    )

    records = [
        json.loads(line)
        for line in records_path.read_text(encoding="utf-8").splitlines()
    ]

    assert [row["source_id"] for row in records] == ["openalex_W2"]
    assert json.loads(summary_path.read_text(encoding="utf-8"))["source_count"] == 1


def test_combine_full_text_access_outputs_writes_merged_records_and_summary(
    tmp_path: Path,
):
    first_batch = tmp_path / "batch1.jsonl"
    second_batch = tmp_path / "batch2.jsonl"
    output = tmp_path / "combined"
    write_jsonl(
        first_batch,
        [
            {
                "source_id": "openalex_W1",
                "access_status": "downloaded",
                "parse_status": "parseable",
                "content_type": "text/html",
                "extracted_chars": 1200,
            }
        ],
    )
    write_jsonl(
        second_batch,
        [
            {
                "source_id": "openalex_W2",
                "access_status": "download_failed",
                "parse_status": "not_attempted",
                "content_type": None,
                "extracted_chars": 0,
            }
        ],
    )

    records_path, summary_path, markdown_path = full_text_intake.combine_full_text_access_outputs(
        [first_batch, second_batch],
        output_dir=output,
    )

    records = [
        json.loads(line)
        for line in records_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert [row["source_id"] for row in records] == ["openalex_W1", "openalex_W2"]
    assert summary["source_count"] == 2
    assert summary["parseable_count"] == 1
    assert summary["access_status_counts"] == {"download_failed": 1, "downloaded": 1}
    assert "Phase 7G Full-Text Access" in markdown
