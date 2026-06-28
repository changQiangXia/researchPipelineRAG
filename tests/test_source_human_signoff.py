from __future__ import annotations

import importlib
import json
from pathlib import Path

from domainrag.io_utils import write_jsonl


def _queue_row(source_id: str = "openalex_W1", subtopic: str = "oxidation") -> dict:
    return {
        "source_id": source_id,
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
        "subtopic": subtopic,
        "work_kind": "research_article_candidate",
        "venue": "Corrosion Science",
        "manual_finalization_action": "human_review_ready_source",
        "candidate_final_whitelist_queue_status": "candidate_for_final_whitelist_review",
        "final_inclusion_status": "not_finalized",
        "manual_review_fields": ["venue_metric"],
    }


def _label(source_id: str, decision: str = "accepted_final") -> dict:
    return {
        "source_id": source_id,
        "human_signoff_decision": decision,
        "human_reviewer": "reviewer_a",
        "human_review_date": "2026-06-28",
        "human_review_notes": "checked source evidence",
    }


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_build_human_signoff_template_keeps_final_whitelist_open(tmp_path: Path):
    module = importlib.import_module("domainrag.source_human_signoff")
    queue = tmp_path / "candidate_final_whitelist_queue.jsonl"
    output = tmp_path / "human_signoff"
    write_jsonl(queue, [_queue_row("openalex_W1"), _queue_row("openalex_W2")])

    template_path, final_path, summary_path, markdown_path = (
        module.build_human_signoff_outputs(queue, output_dir=output)
    )

    template = _read_jsonl(template_path)
    final_rows = _read_jsonl(final_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert [row["human_signoff_decision"] for row in template] == [
        "pending_human_review",
        "pending_human_review",
    ]
    assert final_rows == []
    assert summary["candidate_queue_count"] == 2
    assert summary["accepted_final_source_count"] == 0
    assert summary["pending_human_review_count"] == 2
    assert summary["final_whitelist_claim"] == "not_complete"
    assert "Phase 7J Human Sign-Off Workflow" in markdown
    assert "not final manual verification" in markdown


def test_build_human_signoff_outputs_promotes_only_human_accepted_rows(tmp_path: Path):
    module = importlib.import_module("domainrag.source_human_signoff")
    queue = tmp_path / "candidate_final_whitelist_queue.jsonl"
    labels = tmp_path / "human_signoff_labels.jsonl"
    output = tmp_path / "human_signoff"
    write_jsonl(queue, [_queue_row("openalex_W1"), _queue_row("openalex_W2")])
    write_jsonl(labels, [_label("openalex_W1"), _label("openalex_W2", "rejected_final")])

    _, final_path, summary_path, _ = module.build_human_signoff_outputs(
        queue,
        output_dir=output,
        labels_path=labels,
    )

    final_rows = _read_jsonl(final_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert [row["source_id"] for row in final_rows] == ["openalex_W1"]
    assert final_rows[0]["final_inclusion_status"] == "accepted_final_verification"
    assert summary["accepted_final_source_count"] == 1
    assert summary["rejected_final_source_count"] == 1
    assert summary["pending_human_review_count"] == 0
    assert summary["final_whitelist_claim"] == "not_complete"
