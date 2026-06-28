from __future__ import annotations

import json
from pathlib import Path

from domainrag.source_acquisition import (
    build_acquisition_outputs,
    build_openalex_url,
    normalize_openalex_work,
    summarize_coverage,
)


def _openalex_work(
    *,
    openalex_id: str = "https://openalex.org/W123",
    doi: str | None = "https://doi.org/10.1234/example",
    title: str = "High-temperature oxidation of a nickel superalloy",
    year: int = 2025,
    work_type: str = "article",
    venue: str = "npj Materials Degradation",
    is_oa: bool = True,
) -> dict:
    return {
        "id": openalex_id,
        "doi": doi,
        "display_name": title,
        "publication_year": year,
        "publication_date": f"{year}-03-01",
        "type": work_type,
        "cited_by_count": 17,
        "primary_location": {
            "landing_page_url": "https://publisher.example/work",
            "source": {"display_name": venue, "type": "journal"},
            "is_oa": is_oa,
        },
        "open_access": {"is_oa": is_oa, "oa_url": "https://publisher.example/pdf"},
        "abstract_inverted_index": {"Nickel": [0], "superalloy": [1]},
    }


def test_normalize_openalex_work_keeps_verified_candidate_fields():
    row = normalize_openalex_work(
        _openalex_work(),
        subtopic="oxidation",
        query="nickel superalloy high temperature oxidation",
    )

    assert row is not None
    assert row["source_id"] == "openalex_W123"
    assert row["verification_status"] == "candidate_openalex_verified"
    assert row["inclusion_status"] == "candidate_for_manual_verification"
    assert row["subtopic"] == "oxidation"
    assert row["year"] == 2025
    assert row["work_type"] == "article"
    assert row["work_kind"] == "research_article_candidate"
    assert row["title"] == "High-temperature oxidation of a nickel superalloy"
    assert row["doi"] == "10.1234/example"
    assert row["venue"] == "npj Materials Degradation"
    assert row["official_url"] == "https://publisher.example/work"
    assert row["open_access"] is True
    assert row["has_abstract"] is True
    assert row["venue_whitelist_status"] == "candidate_top_venue_or_domain_flagship"


def test_normalize_openalex_work_rejects_unusable_metadata():
    assert (
        normalize_openalex_work(
            _openalex_work(doi=None),
            subtopic="creep",
            query="nickel superalloy creep",
        )
        is None
    )
    assert (
        normalize_openalex_work(
            _openalex_work(year=2016),
            subtopic="creep",
            query="nickel superalloy creep",
        )
        is None
    )
    generic_work = _openalex_work(title="Generic finite element process parameter framework")
    generic_work["abstract_inverted_index"] = {"finite": [0], "element": [1], "model": [2]}
    assert (
        normalize_openalex_work(
            generic_work,
            subtopic="additive_manufacturing",
            query="laser powder bed fusion nickel superalloy high temperature",
        )
        is None
    )


def test_normalize_openalex_work_uses_abstract_domain_terms_for_relevance():
    work = _openalex_work(title="Generic fatigue model")
    work["abstract_inverted_index"] = {
        "Nickel": [0],
        "superalloy": [1],
        "creep": [2],
        "damage": [3],
    }

    row = normalize_openalex_work(
        work,
        subtopic="fatigue",
        query="nickel superalloy fatigue",
    )

    assert row is not None
    assert row["domain_relevance_terms"] == ["nickel", "superalloy"]


def test_build_openalex_url_uses_reproducible_public_filters():
    url = build_openalex_url(
        "nickel superalloy oxidation",
        from_year=2017,
        to_year=2026,
        per_page=25,
        mailto="research@example.com",
    )

    assert url.startswith("https://api.openalex.org/works?")
    assert "search=nickel+superalloy+oxidation" in url
    assert "from_publication_date%3A2017-01-01" in url
    assert "to_publication_date%3A2026-12-31" in url
    assert "has_doi%3Atrue" in url
    assert "per-page=25" in url
    assert "mailto=research%40example.com" in url


def test_summarize_coverage_tracks_subtopics_years_types_and_targets():
    rows = [
        normalize_openalex_work(
            _openalex_work(openalex_id="https://openalex.org/W1", year=2025),
            subtopic="oxidation",
            query="q1",
        ),
        normalize_openalex_work(
            _openalex_work(
                openalex_id="https://openalex.org/W2",
                doi="https://doi.org/10.1234/review",
                title="Nickel superalloy creep review",
                year=2024,
                work_type="review",
                venue="Progress in Materials Science",
            ),
            subtopic="creep",
            query="q2",
        ),
    ]
    summary = summarize_coverage([row for row in rows if row])

    assert summary["candidate_count"] == 2
    assert summary["research_article_candidates"] == 1
    assert summary["review_candidates"] == 1
    assert summary["open_access_candidates"] == 2
    assert summary["subtopics"]["oxidation"]["candidate_count"] == 1
    assert summary["subtopics"]["creep"]["review_candidates"] == 1
    assert summary["year_counts"]["2025"] == 1
    assert summary["demo_scale_targets"]["source_papers"] == [100, 180]
    assert summary["demo_scale_targets"]["corpus_chunks"] == [1000, 3000]


def test_build_acquisition_outputs_writes_jsonl_coverage_and_markdown(tmp_path: Path):
    raw_records = [
        {
            "subtopic": "oxidation",
            "query": "nickel superalloy oxidation",
            "work": _openalex_work(openalex_id="https://openalex.org/W1"),
        },
        {
            "subtopic": "oxidation",
            "query": "duplicate query",
            "work": _openalex_work(openalex_id="https://openalex.org/W1"),
        },
        {
            "subtopic": "creep",
            "query": "nickel superalloy creep review",
            "work": _openalex_work(
                openalex_id="https://openalex.org/W2",
                doi="https://doi.org/10.1234/review",
                title="Nickel superalloy creep review",
                work_type="review",
                venue="Progress in Materials Science",
            ),
        },
    ]

    candidates_path, coverage_path, markdown_path = build_acquisition_outputs(
        raw_records,
        output_dir=tmp_path,
    )

    candidates = [
        json.loads(line)
        for line in candidates_path.read_text(encoding="utf-8").splitlines()
    ]
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(candidates) == 2
    assert coverage["candidate_count"] == 2
    assert "Phase 7D Demo-Scale Source Acquisition" in markdown
    assert "candidate_for_manual_verification" in markdown
