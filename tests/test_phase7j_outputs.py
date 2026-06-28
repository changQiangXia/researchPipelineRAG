from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGNOFF = ROOT / "outputs" / "phase7j" / "human_signoff"
DOC = ROOT / "docs" / "verification" / "human-signoff-workflow.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7j_human_signoff_template_waits_for_real_labels():
    template = _read_jsonl(SIGNOFF / "human_signoff_template.jsonl")
    final_whitelist = _read_jsonl(SIGNOFF / "final_source_whitelist.jsonl")
    summary = json.loads((SIGNOFF / "human_signoff_summary.json").read_text())

    assert len(template) == 108
    assert final_whitelist == []
    assert summary["candidate_queue_count"] == 108
    assert summary["accepted_final_source_count"] == 0
    assert summary["pending_human_review_count"] == 108
    assert summary["human_signoff_decision_counts"] == {"pending_human_review": 108}
    assert summary["final_whitelist_claim"] == "not_complete"
    assert all(row["human_signoff_decision"] == "pending_human_review" for row in template)


def test_phase7j_updates_docs_and_audit_without_final_whitelist_claim():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    assert "Phase 7J" in doc
    assert "not final manual verification" in doc
    assert "human labels" in doc
    assert audit["phase"] == "Phase 7L"
    assert audit["phase7j_human_signoff_workflow"] == {
        "candidate_queue_count": 108,
        "human_signoff_template_rows": 108,
        "accepted_final_source_count": 0,
        "pending_human_review_count": 108,
        "final_whitelist_claim": "not_complete",
        "verification_status": "human_signoff_required",
        "outputs": [
            "outputs/phase7j/human_signoff/human_signoff_template.jsonl",
            "outputs/phase7j/human_signoff/final_source_whitelist.jsonl",
            "outputs/phase7j/human_signoff/human_signoff_summary.json",
            "docs/verification/human-signoff-workflow.md",
        ],
    }
