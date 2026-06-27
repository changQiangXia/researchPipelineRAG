from __future__ import annotations

import json
from pathlib import Path

from domainrag.comparison_report import generate_comparison_report
from domainrag.io_utils import write_jsonl


def test_generate_comparison_report_merges_answer_and_judge_metrics(tmp_path: Path):
    answer_path = tmp_path / "answers.jsonl"
    judge_path = tmp_path / "judge.jsonl"
    output = tmp_path / "comparison"
    write_jsonl(
        answer_path,
        [
            {
                "id": "q1",
                "method": "method_a",
                "split": "fresh_hard",
                "prediction": "A",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": ["d1"],
                "scores": {
                    "single_choice_accuracy": 1.0,
                    "retrieval_hit": 1.0,
                    "retrieval_mrr": 1.0,
                    "retrieval_recall": 1.0,
                },
                "latency_ms": 10.0,
                "input_tokens": 11,
                "output_tokens": 3,
                "api_calls": 1,
                "error": None,
            },
            {
                "id": "q1",
                "method": "method_b",
                "split": "fresh_hard",
                "prediction": "",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": [],
                "scores": {
                    "single_choice_accuracy": 0.0,
                    "retrieval_hit": 0.0,
                    "retrieval_mrr": 0.0,
                    "retrieval_recall": 0.0,
                },
                "latency_ms": 5.0,
                "input_tokens": 7,
                "output_tokens": 0,
                "api_calls": 1,
                "error": "failed",
            },
        ],
    )
    write_jsonl(
        judge_path,
        [
            {
                "id": "q1",
                "method": "method_a",
                "split": "fresh_hard",
                "prediction": "A",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": ["d1"],
                "judge": {
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 5.0,
                    "relevance": 5.0,
                    "unsupported_claims": [],
                    "reason": "ok",
                },
                "judge_scores": {
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 5.0,
                    "relevance": 5.0,
                    "hallucination_risk": 0.0,
                },
                "latency_ms": 20.0,
                "input_tokens": 13,
                "output_tokens": 4,
                "api_calls": 1,
                "error": None,
            },
            {
                "id": "q1",
                "method": "method_b",
                "split": "fresh_hard",
                "prediction": "",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": [],
                "judge": {
                    "correctness": 0.0,
                    "context_support": 0.0,
                    "faithfulness": 0.0,
                    "relevance": 0.0,
                    "unsupported_claims": ["unsupported"],
                    "reason": "bad",
                },
                "judge_scores": {
                    "correctness": 0.0,
                    "context_support": 0.0,
                    "faithfulness": 0.0,
                    "relevance": 0.0,
                    "hallucination_risk": 5.0,
                },
                "latency_ms": 15.0,
                "input_tokens": 9,
                "output_tokens": 2,
                "api_calls": 1,
                "error": "answer row error",
            },
        ],
    )

    markdown_path, json_path = generate_comparison_report(
        answer_inputs=[answer_path],
        judge_inputs=[judge_path],
        output_dir=output,
    )

    summary = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert markdown_path == output / "summary.md"
    assert json_path == output / "summary.json"
    assert summary["methods"]["method_a"]["questions"] == 1
    assert summary["methods"]["method_a"]["answer_metrics"]["single_choice_accuracy"] == 1.0
    assert summary["methods"]["method_a"]["answer_metrics"]["retrieval_hit"] == 1.0
    assert summary["methods"]["method_a"]["judge_metrics"]["faithfulness"] == 5.0
    assert summary["methods"]["method_a"]["total_api_calls"] == 2
    assert summary["methods"]["method_a"]["total_tokens"] == 31
    assert summary["methods"]["method_b"]["answer_errors"] == 1
    assert summary["methods"]["method_b"]["judge_errors"] == 1
    assert summary["methods"]["method_b"]["unsupported_claims"] == 1
    assert [row["method"] for row in summary["leaderboard"]] == ["method_a", "method_b"]
    assert "| method_a |" in markdown
    assert "faithfulness" in markdown


def test_generate_comparison_report_keeps_answer_only_methods(tmp_path: Path):
    answer_path = tmp_path / "answers.jsonl"
    output = tmp_path / "comparison"
    write_jsonl(
        answer_path,
        [
            {
                "id": "q1",
                "method": "retrieval_only",
                "split": "fresh_hard",
                "prediction": "A",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": ["d1"],
                "scores": {
                    "single_choice_accuracy": 1.0,
                    "retrieval_hit": 1.0,
                },
                "latency_ms": 0.0,
                "input_tokens": 0,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            }
        ],
    )

    _, json_path = generate_comparison_report(
        answer_inputs=[answer_path],
        judge_inputs=[],
        output_dir=output,
    )

    summary = json.loads(json_path.read_text(encoding="utf-8"))

    assert summary["methods"]["retrieval_only"]["judge_metrics"] == {}
    assert summary["leaderboard"][0]["method"] == "retrieval_only"
