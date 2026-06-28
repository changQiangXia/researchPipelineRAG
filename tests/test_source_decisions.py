from __future__ import annotations

import json
from pathlib import Path

from domainrag.io_utils import write_jsonl
from domainrag.source_decisions import (
    build_decision_outputs,
    decide_source,
    summarize_decisions,
)


def _screening_row(
    *,
    source_id: str = "openalex_W1",
    subtopic: str = "oxidation",
    work_kind: str = "research_article_candidate",
    screening_priority: str = "high",
    full_text_queue_status: str = "ready_for_full_text_download_attempt",
) -> dict:
    return {
        "source_id": source_id,
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
        "subtopic": subtopic,
        "work_kind": work_kind,
        "screening_priority": screening_priority,
        "full_text_queue_status": full_text_queue_status,
        "full_text_status": "open_access_full_text_candidate",
        "screening_status": "needs_manual_verification",
        "verification_status": "machine_prescreen_only",
        "venue_whitelist_status": "candidate_top_venue_or_domain_flagship",
        "domain_relevance_terms": ["nickel", "superalloy"],
        "oa_url": "https://publisher.example/paper.pdf",
        "official_url": "https://doi.org/10.1234/example",
    }


def test_decide_source_assigns_provisional_accept_pending_and_reject():
    accepted = decide_source(_screening_row(screening_priority="high"))
    pending = decide_source(_screening_row(screening_priority="low"))
    rejected = decide_source(
        _screening_row(
            screening_priority="low",
            full_text_queue_status="needs_access_check",
        )
    )

    assert accepted["source_decision"] == "accepted_provisional"
    assert pending["source_decision"] == "pending_manual_review"
    assert rejected["source_decision"] == "rejected_prescreen"
    assert accepted["decision_status"] == "provisional_not_final"
    assert pending["decision_status"] == "provisional_not_final"
    assert rejected["decision_status"] == "provisional_not_final"
    assert accepted["manual_verification_status"] == {
        "venue_metric": "pending",
        "doi_title_year": "pending",
        "article_type": "pending",
        "retraction": "pending",
        "full_text_processability": "pending",
        "domain_relevance": "pending",
    }


def test_summarize_decisions_tracks_whitelist_count_stop_point_and_review_gaps():
    rows = [
        decide_source(_screening_row(source_id="openalex_W1", subtopic="oxidation")),
        decide_source(
            _screening_row(
                source_id="openalex_W2",
                subtopic="coatings",
                screening_priority="low",
            )
        ),
        decide_source(
            _screening_row(
                source_id="openalex_W3",
                subtopic="coatings",
                screening_priority="low",
                full_text_queue_status="needs_access_check",
            )
        ),
        decide_source(
            _screening_row(
                source_id="openalex_W4",
                subtopic="creep",
                work_kind="review_candidate",
                screening_priority="medium",
            )
        ),
    ]

    summary = summarize_decisions(rows)

    assert summary["candidate_count"] == 4
    assert summary["decision_counts"] == {
        "accepted_provisional": 2,
        "pending_manual_review": 1,
        "rejected_prescreen": 1,
    }
    assert summary["provisional_whitelist_count"] == 3
    assert summary["verification_status"] == "provisional_not_final"
    assert summary["stop_point_recommendation"] == "pause_after_phase7f"
    assert summary["review_gap_subtopics"] == ["coatings", "oxidation"]
    assert summary["subtopics"]["creep"]["review_candidates"] == 1


def test_build_decision_outputs_writes_decisions_whitelist_summary_and_markdown(
    tmp_path: Path,
):
    queue_path = tmp_path / "screening_queue.jsonl"
    output = tmp_path / "decisions"
    write_jsonl(
        queue_path,
        [
            _screening_row(source_id="openalex_W1", subtopic="oxidation"),
            _screening_row(
                source_id="openalex_W2",
                subtopic="coatings",
                screening_priority="low",
            ),
            _screening_row(
                source_id="openalex_W3",
                subtopic="coatings",
                screening_priority="low",
                full_text_queue_status="needs_access_check",
            ),
        ],
    )

    decisions_path, whitelist_path, summary_path, markdown_path = build_decision_outputs(
        queue_path,
        output_dir=output,
    )

    decisions = [
        json.loads(line)
        for line in decisions_path.read_text(encoding="utf-8").splitlines()
    ]
    whitelist = [
        json.loads(line)
        for line in whitelist_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(decisions) == 3
    assert len(whitelist) == 2
    assert summary["provisional_whitelist_count"] == 2
    assert "Phase 7F Source Decisions" in markdown
    assert "pause_after_phase7f" in markdown
