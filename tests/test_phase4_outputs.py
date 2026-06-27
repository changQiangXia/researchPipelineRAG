from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE4 = ROOT / "outputs" / "phase4"


def test_phase4_reports_cover_curated_and_deepseek_candidate_splits():
    expected_reports = [
        PHASE4 / dataset / f"report_{split}" / "summary.json"
        for dataset in ["curated", "deepseek_candidate"]
        for split in ["dev", "test", "fresh_hard"]
    ]

    for report_path in expected_reports:
        assert report_path.exists()
        summary = json.loads(report_path.read_text(encoding="utf-8"))
        assert {"no_rag", "oracle_context", "lexical_rag", "_diagnostics"} <= set(summary)
        assert summary["oracle_context"]["metrics"]["retrieval_recall"] == 1.0
        assert summary["lexical_rag"]["metrics"]["retrieval_hit"] == 1.0


def test_phase4_fresh_hard_reports_identify_candidates():
    curated = json.loads(
        (PHASE4 / "curated" / "report_fresh_hard" / "summary.json").read_text(
            encoding="utf-8"
        )
    )
    deepseek = json.loads(
        (PHASE4 / "deepseek_candidate" / "report_fresh_hard" / "summary.json").read_text(
            encoding="utf-8"
        )
    )

    assert curated["_diagnostics"]["fresh_hard_candidates"] >= 3
    assert deepseek["_diagnostics"]["fresh_hard_candidates"] == 3
    assert curated["no_rag"]["metrics"]["retrieval_recall"] == 0.0
    assert deepseek["no_rag"]["metrics"]["retrieval_recall"] == 0.0
