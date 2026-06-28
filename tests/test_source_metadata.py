from __future__ import annotations

import json
from pathlib import Path

from domainrag.io_utils import write_jsonl
from domainrag.source_metadata import (
    build_openalex_metadata_outputs,
    collect_openalex_metadata,
    normalize_openalex_metadata,
)


def _source_row(source_id: str = "openalex_W1") -> dict:
    return {
        "source_id": source_id,
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
    }


def _payload(*, is_retracted: bool = False, work_type: str = "article") -> dict:
    return {
        "id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1234/example",
        "display_name": "High-temperature oxidation of nickel superalloy",
        "publication_year": 2026,
        "publication_date": "2026-01-02",
        "type": work_type,
        "is_retracted": is_retracted,
        "primary_location": {
            "source": {
                "display_name": "Corrosion Science",
                "type": "journal",
            }
        },
    }


def test_normalize_openalex_metadata_keeps_verification_fields():
    record = normalize_openalex_metadata(_source_row(), _payload())

    assert record == {
        "source_id": "openalex_W1",
        "metadata_status": "found",
        "openalex_id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "publication_year": 2026,
        "publication_date": "2026-01-02",
        "type": "article",
        "is_retracted": False,
        "venue": "Corrosion Science",
        "venue_type": "journal",
    }


def test_collect_openalex_metadata_uses_injected_fetcher_and_records_errors():
    def fetcher(doi: str) -> dict:
        if doi == "10.1234/missing":
            raise OSError("network unavailable")
        return _payload()

    rows = [
        _source_row(source_id="openalex_W1"),
        {**_source_row(source_id="openalex_W2"), "doi": "10.1234/missing"},
    ]

    records = collect_openalex_metadata(rows, fetcher=fetcher)

    assert records[0]["metadata_status"] == "found"
    assert records[1]["metadata_status"] == "error"
    assert records[1]["metadata_error"] == "network unavailable"


def test_build_openalex_metadata_outputs_writes_records_summary_and_markdown(
    tmp_path: Path,
):
    whitelist = tmp_path / "provisional_source_whitelist.jsonl"
    output = tmp_path / "metadata"
    write_jsonl(
        whitelist,
        [
            _source_row(source_id="openalex_W1"),
            _source_row(source_id="openalex_W2"),
        ],
    )

    def fetcher(doi: str) -> dict:
        return _payload(is_retracted=doi.endswith("example"))

    records_path, summary_path, markdown_path = build_openalex_metadata_outputs(
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
    assert summary["metadata_status_counts"] == {"found": 2}
    assert summary["retracted_count"] == 2
    assert "Phase 7G OpenAlex Metadata" in markdown
