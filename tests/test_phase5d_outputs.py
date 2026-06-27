from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "outputs" / "phase5d" / "fresh_hard_comparison" / "summary.json"
MARKDOWN = ROOT / "outputs" / "phase5d" / "fresh_hard_comparison" / "summary.md"


def test_phase5d_fresh_hard_comparison_contains_expected_methods():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert set(summary["methods"]) == {
        "no_rag",
        "oracle_context",
        "lexical_rag",
        "flashrag_bm25_oracle_reader",
        "flashrag_bm25_live_deepseek",
    }
    assert len(summary["leaderboard"]) == 5
    assert summary["methods"]["no_rag"]["questions"] == 4
    assert summary["methods"]["flashrag_bm25_live_deepseek"]["questions"] == 4


def test_phase5d_fresh_hard_comparison_shows_rag_support_advantage():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    methods = summary["methods"]

    assert methods["no_rag"]["answer_metrics"]["retrieval_hit"] == 0.0
    assert methods["no_rag"]["judge_metrics"]["context_support"] == 0.0
    assert methods["no_rag"]["judge_metrics"]["hallucination_risk"] > 3.0
    assert methods["flashrag_bm25_live_deepseek"]["answer_metrics"]["retrieval_hit"] == 1.0
    assert methods["flashrag_bm25_live_deepseek"]["judge_metrics"]["faithfulness"] == 5.0
    assert methods["flashrag_bm25_live_deepseek"]["unsupported_claims"] == 0
    assert methods["flashrag_bm25_live_deepseek"]["total_api_calls"] == 8


def test_phase5d_fresh_hard_comparison_markdown_has_leaderboard_table():
    text = MARKDOWN.read_text(encoding="utf-8")

    assert "# DomainRAG-Bench Comparison" in text
    assert "| method | questions | answer_score | retrieval_hit | correctness |" in text
    assert "| flashrag_bm25_live_deepseek |" in text
    assert "| no_rag |" in text
