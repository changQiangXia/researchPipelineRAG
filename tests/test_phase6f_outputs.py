from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-human-calibration-audit" / "medium_human_calibration_audit"
LABELS = AUDIT / "human_labels.jsonl"
SUMMARY = AUDIT / "summary.json"
SUMMARY_MD = AUDIT / "summary.md"
REVIEWED = AUDIT / "reviewed_rows.jsonl"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase6f_human_calibration_audit_outputs_cover_representative_subset():
    labels = _read_jsonl(LABELS)
    reviewed = _read_jsonl(REVIEWED)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    markdown = SUMMARY_MD.read_text(encoding="utf-8")

    methods = Counter(row["review_id"].split("::")[1] for row in labels)

    assert len(labels) == 15
    assert len(reviewed) == 15
    assert methods == {
        "no_rag": 3,
        "oracle_context": 3,
        "lexical_rag": 3,
        "flashrag_bm25_oracle_reader": 3,
        "flashrag_bm25_live_deepseek": 3,
    }
    assert summary["reviewed_rows"] == 15
    assert summary["priority_rows"] >= 12
    assert summary["unsupported_claim_rows"] >= 5
    assert set(summary["methods"]) == set(methods)
    assert summary["overall"]["agreement_rate_within_1"]["correctness"] >= 0.8
    assert summary["overall"]["agreement_rate_within_1"]["context_support"] >= 0.7
    assert summary["disagreements"]
    assert "DomainRAG Human Calibration Audit" in markdown
    assert "| flashrag_bm25_live_deepseek | 3 |" in markdown
