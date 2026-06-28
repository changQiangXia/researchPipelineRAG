from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE4C = ROOT / "outputs" / "archive" / "provenance" / "pilot-benchmarks" / "deepseek-judge-fresh-hard" / "deepseek_judge_fresh_hard"


def test_phase4c_judge_outputs_are_complete():
    result_path = (
        PHASE4C
        / "real_pilot_nickel_superalloy"
        / "fresh_hard_judge_results.jsonl"
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
    assert all(row["api_calls"] == 1 for row in rows)
    assert all(row["input_tokens"] > 0 for row in rows)
    assert all(row["output_tokens"] > 0 for row in rows)
    for row in rows:
        assert set(row["judge"]) == {
            "correctness",
            "context_support",
            "faithfulness",
            "relevance",
            "unsupported_claims",
            "reason",
        }
        assert set(row["judge_scores"]) == {
            "correctness",
            "context_support",
            "faithfulness",
            "relevance",
            "hallucination_risk",
        }


def test_phase4c_judge_summary_shows_rag_improves_support_and_faithfulness():
    summary = json.loads(
        (PHASE4C / "report_fresh_hard" / "summary.json").read_text(encoding="utf-8")
    )

    assert summary["no_rag"]["metrics"]["context_support"] == 0.0
    assert summary["no_rag"]["metrics"]["correctness"] < 3.0
    assert summary["no_rag"]["metrics"]["hallucination_risk"] > 3.0
    assert summary["oracle_context"]["metrics"]["correctness"] == 5.0
    assert summary["oracle_context"]["metrics"]["context_support"] == 5.0
    assert summary["lexical_rag"]["metrics"]["correctness"] == 5.0
    assert summary["lexical_rag"]["metrics"]["faithfulness"] == 5.0
    assert summary["lexical_rag"]["unsupported_claims"] == 0
