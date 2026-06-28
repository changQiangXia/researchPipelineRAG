from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE4B = ROOT / "outputs" / "archive" / "provenance" / "pilot-benchmarks" / "live-deepseek-fresh-hard" / "live_deepseek_fresh_hard"


def test_phase4b_live_deepseek_fresh_hard_outputs_are_complete():
    result_path = (
        PHASE4B
        / "real_pilot_nickel_superalloy"
        / "fresh_hard_deepseek_results.jsonl"
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]
    method_counts = Counter(row["method"] for row in rows)

    assert len(rows) == 12
    assert method_counts == {
        "no_rag": 4,
        "oracle_context": 4,
        "lexical_rag": 4,
    }
    assert all(row["error"] is None for row in rows)
    assert all(row["api_calls"] >= 1 for row in rows)
    assert all(row["input_tokens"] > 0 for row in rows)
    assert all(row["output_tokens"] > 0 for row in rows)


def test_phase4b_live_deepseek_report_tracks_tokens_and_fresh_hard_candidates():
    summary_path = PHASE4B / "report_fresh_hard" / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["_diagnostics"]["fresh_hard_candidate_ids"] == [
        "ns_ht_q010",
        "ns_ht_q011",
    ]
    assert summary["_diagnostics"]["fresh_hard_candidates"] == 2
    assert summary["no_rag"]["metrics"]["retrieval_recall"] == 0.0
    assert summary["oracle_context"]["metrics"]["retrieval_recall"] == 1.0
    assert summary["lexical_rag"]["metrics"]["retrieval_recall"] == 1.0
    assert summary["no_rag"]["total_tokens"] > 0
    assert summary["oracle_context"]["total_tokens"] > 0
    assert summary["lexical_rag"]["total_tokens"] > 0
    assert summary["no_rag"]["api_calls"] == 4
    assert summary["oracle_context"]["api_calls"] == 4
    assert summary["lexical_rag"]["api_calls"] == 4
