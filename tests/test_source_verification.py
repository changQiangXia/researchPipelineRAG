from __future__ import annotations

import json
from pathlib import Path

from domainrag.io_utils import write_jsonl
from domainrag.source_verification import (
    build_verification_outputs,
    summarize_verifications,
    verify_source,
)


def _source_row(
    *,
    source_id: str = "openalex_W1",
    doi: str = "10.1234/example",
    title: str = "High-temperature oxidation of nickel superalloy",
    year: int = 2026,
    work_kind: str = "research_article_candidate",
    work_type: str = "article",
    venue_whitelist_status: str = "candidate_top_venue_or_domain_flagship",
    domain_relevance_terms: list[str] | None = None,
) -> dict:
    return {
        "source_id": source_id,
        "doi": doi,
        "title": title,
        "year": year,
        "subtopic": "oxidation",
        "work_kind": work_kind,
        "work_type": work_type,
        "venue": "Corrosion Science",
        "venue_type": "journal",
        "venue_whitelist_status": venue_whitelist_status,
        "domain_relevance_terms": domain_relevance_terms or ["nickel", "superalloy"],
        "oa_url": "https://publisher.example/paper.pdf",
        "official_url": "https://doi.org/10.1234/example",
        "source_decision": "accepted_provisional",
        "decision_status": "provisional_not_final",
    }


def _openalex_record(
    *,
    doi: str = "https://doi.org/10.1234/example",
    title: str = "High-temperature oxidation of nickel superalloy",
    year: int = 2026,
    work_type: str = "article",
    is_retracted: bool = False,
) -> dict:
    return {
        "doi": doi,
        "title": title,
        "display_name": title,
        "publication_year": year,
        "type": work_type,
        "is_retracted": is_retracted,
    }


def _access_record(
    *,
    source_id: str = "openalex_W1",
    access_status: str = "downloaded",
    parse_status: str = "parseable",
    extracted_chars: int = 1500,
) -> dict:
    return {
        "source_id": source_id,
        "access_status": access_status,
        "parse_status": parse_status,
        "content_type": "application/pdf",
        "bytes_downloaded": 128000,
        "extracted_chars": extracted_chars,
    }


def test_verify_source_marks_all_checks_verified_when_evidence_matches():
    verified = verify_source(
        _source_row(),
        metadata=_openalex_record(),
        access=_access_record(),
    )

    assert verified["source_verification_status"] == "verified_source_candidate"
    assert verified["final_inclusion_status"] == "not_finalized"
    assert verified["verification_checks"] == {
        "venue_metric": "verified",
        "doi_title_year": "verified",
        "article_type": "verified",
        "retraction": "verified",
        "full_text_processability": "verified",
        "domain_relevance": "verified",
    }
    assert "all_machine_checks_verified_requires_human_final_signoff" in verified[
        "verification_reasons"
    ]


def test_verify_source_keeps_manual_metric_pending_without_overclaiming_final():
    row = _source_row(
        venue_whitelist_status="needs_venue_metric_verification",
        domain_relevance_terms=["nickel", "superalloy"],
    )

    verified = verify_source(
        row,
        metadata=_openalex_record(),
        access=_access_record(),
    )

    assert verified["source_verification_status"] == "ready_for_manual_finalization"
    assert verified["final_inclusion_status"] == "not_finalized"
    assert verified["verification_checks"]["venue_metric"] == "pending_manual"
    assert verified["verification_checks"]["doi_title_year"] == "verified"
    assert "venue_metric_requires_manual_or_external_metric_check" in verified[
        "verification_reasons"
    ]


def test_verify_source_rejects_metadata_mismatch_or_retraction():
    mismatched = verify_source(
        _source_row(title="Expected title"),
        metadata=_openalex_record(title="Different title"),
        access=_access_record(),
    )
    retracted = verify_source(
        _source_row(source_id="openalex_W2"),
        metadata=_openalex_record(is_retracted=True),
        access=_access_record(source_id="openalex_W2"),
    )

    assert mismatched["source_verification_status"] == "rejected_verification"
    assert mismatched["verification_checks"]["doi_title_year"] == "failed"
    assert retracted["source_verification_status"] == "rejected_verification"
    assert retracted["verification_checks"]["retraction"] == "failed"


def test_verify_source_does_not_accept_tiny_landing_page_as_full_text():
    verified = verify_source(
        _source_row(),
        metadata=_openalex_record(),
        access=_access_record(extracted_chars=11),
    )

    assert verified["verification_checks"]["full_text_processability"] == "pending_manual"
    assert verified["source_verification_status"] == "ready_for_manual_finalization"


def test_summarize_verifications_tracks_final_ready_and_pending_counts():
    rows = [
        verify_source(_source_row(source_id="openalex_W1"), metadata=_openalex_record(), access=_access_record()),
        verify_source(
            _source_row(
                source_id="openalex_W2",
                venue_whitelist_status="needs_venue_metric_verification",
            ),
            metadata=_openalex_record(),
            access=_access_record(source_id="openalex_W2"),
        ),
        verify_source(
            _source_row(source_id="openalex_W3", title="Expected"),
            metadata=_openalex_record(title="Different"),
            access=_access_record(source_id="openalex_W3"),
        ),
    ]

    summary = summarize_verifications(rows)

    assert summary["source_count"] == 3
    assert summary["status_counts"] == {
        "ready_for_manual_finalization": 1,
        "rejected_verification": 1,
        "verified_source_candidate": 1,
    }
    assert summary["accepted_final_verification_count"] == 0
    assert summary["ready_for_manual_finalization_count"] == 1
    assert summary["rejected_verification_count"] == 1
    assert summary["final_whitelist_claim"] == "not_complete"


def test_build_verification_outputs_writes_matrix_queue_summary_and_markdown(
    tmp_path: Path,
):
    whitelist = tmp_path / "provisional_source_whitelist.jsonl"
    metadata = tmp_path / "openalex_metadata.jsonl"
    access = tmp_path / "full_text_access.jsonl"
    output = tmp_path / "verification"
    write_jsonl(
        whitelist,
        [
            _source_row(source_id="openalex_W1"),
            _source_row(
                source_id="openalex_W2",
                venue_whitelist_status="needs_venue_metric_verification",
            ),
        ],
    )
    write_jsonl(
        metadata,
        [
            {"source_id": "openalex_W1", **_openalex_record()},
            {"source_id": "openalex_W2", **_openalex_record()},
        ],
    )
    write_jsonl(
        access,
        [
            _access_record(source_id="openalex_W1"),
            _access_record(source_id="openalex_W2"),
        ],
    )

    matrix_path, final_queue_path, summary_path, markdown_path = (
        build_verification_outputs(
            whitelist,
            output_dir=output,
            metadata_path=metadata,
            access_path=access,
        )
    )

    matrix = [
        json.loads(line)
        for line in matrix_path.read_text(encoding="utf-8").splitlines()
    ]
    final_queue = [
        json.loads(line)
        for line in final_queue_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(matrix) == 2
    assert len(final_queue) == 0
    assert summary["source_count"] == 2
    assert summary["accepted_final_verification_count"] == 0
    assert summary["ready_for_manual_finalization_count"] == 1
    assert "Phase 7G Source Verification" in markdown
    assert "not_complete" in markdown
