from __future__ import annotations

import json
from pathlib import Path

from domainrag.io_utils import write_jsonl
from domainrag.source_screening import (
    build_screening_outputs,
    screen_candidate,
    summarize_screening,
)


def _candidate(
    *,
    source_id: str = "openalex_W1",
    subtopic: str = "oxidation",
    work_kind: str = "research_article_candidate",
    venue_whitelist_status: str = "candidate_top_venue_or_domain_flagship",
    open_access: bool = True,
    oa_url: str | None = "https://publisher.example/paper.pdf",
    domain_relevance_terms: list[str] | None = None,
) -> dict:
    return {
        "source_id": source_id,
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
        "subtopic": subtopic,
        "work_kind": work_kind,
        "venue_whitelist_status": venue_whitelist_status,
        "open_access": open_access,
        "oa_url": oa_url,
        "official_url": "https://doi.org/10.1234/example",
        "domain_relevance_terms": (
            ["nickel", "superalloy"]
            if domain_relevance_terms is None
            else domain_relevance_terms
        ),
        "manual_verification_required": [
            "top_venue_metric_or_flagship_status",
            "full_text_processability",
            "article_type_and_retraction_status",
            "domain_relevance",
        ],
    }


def test_screen_candidate_records_priority_full_text_and_manual_tasks():
    row = screen_candidate(_candidate())

    assert row["source_id"] == "openalex_W1"
    assert row["screening_status"] == "needs_manual_verification"
    assert row["screening_priority"] == "high"
    assert row["full_text_status"] == "open_access_full_text_candidate"
    assert row["full_text_queue_status"] == "ready_for_full_text_download_attempt"
    assert row["final_inclusion_status"] == "not_finalized"
    assert row["manual_verification_tasks"] == [
        "verify_venue_metric_or_flagship_status",
        "verify_full_text_processability",
        "verify_article_type",
        "verify_retraction_status",
        "verify_domain_relevance",
    ]
    assert row["screening_reasons"] == [
        "candidate_top_venue_or_domain_flagship",
        "open_access_full_text_candidate",
        "strong_domain_term_match",
    ]


def test_screen_candidate_keeps_candidate_only_rows_for_access_and_venue_review():
    row = screen_candidate(
        _candidate(
            venue_whitelist_status="needs_venue_metric_verification",
            open_access=False,
            oa_url=None,
            domain_relevance_terms=["nickel"],
        )
    )

    assert row["screening_priority"] == "low"
    assert row["full_text_status"] == "landing_page_only"
    assert row["full_text_queue_status"] == "needs_access_check"
    assert row["final_inclusion_status"] == "not_finalized"
    assert "needs_venue_metric_verification" in row["screening_reasons"]
    assert "weak_domain_term_match" in row["screening_reasons"]


def test_summarize_screening_tracks_priorities_review_gaps_and_targets():
    rows = [
        screen_candidate(_candidate(source_id="openalex_W1", subtopic="oxidation")),
        screen_candidate(
            _candidate(
                source_id="openalex_W2",
                subtopic="coatings",
                work_kind="research_article_candidate",
                venue_whitelist_status="needs_venue_metric_verification",
            )
        ),
        screen_candidate(
            _candidate(
                source_id="openalex_W3",
                subtopic="creep",
                work_kind="review_candidate",
                venue_whitelist_status="needs_venue_metric_verification",
            )
        ),
    ]

    summary = summarize_screening(rows)

    assert summary["candidate_count"] == 3
    assert summary["final_included_sources"] == 0
    assert summary["priority_counts"]["high"] == 1
    assert summary["priority_counts"]["medium"] == 2
    assert summary["full_text_ready_candidates"] == 3
    assert summary["review_gap_subtopics"] == ["coatings", "oxidation"]
    assert summary["demo_scale_targets"]["source_papers"] == [100, 180]
    assert summary["subtopics"]["creep"]["review_candidates"] == 1


def test_build_screening_outputs_writes_queue_summary_and_markdown(tmp_path: Path):
    candidates_path = tmp_path / "candidates.jsonl"
    output = tmp_path / "screening"
    write_jsonl(
        candidates_path,
        [
            _candidate(source_id="openalex_W1", subtopic="oxidation"),
            _candidate(
                source_id="openalex_W2",
                subtopic="coatings",
                venue_whitelist_status="needs_venue_metric_verification",
                open_access=False,
                oa_url=None,
            ),
        ],
    )

    queue_path, summary_path, markdown_path = build_screening_outputs(
        candidates_path,
        output_dir=output,
    )

    queue = [
        json.loads(line)
        for line in queue_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(queue) == 2
    assert summary["candidate_count"] == 2
    assert summary["final_included_sources"] == 0
    assert "Phase 7E Source Screening Queue" in markdown
    assert "machine_prescreen_only" in markdown
