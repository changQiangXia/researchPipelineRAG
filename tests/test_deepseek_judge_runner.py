from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from domainrag.deepseek_judge_runner import (
    DeepSeekJudgeConfig,
    build_judge_messages,
    generate_judge_report,
    normalize_judge_result,
    run_deepseek_judge,
)
from domainrag.errors import ValidationError
from domainrag.io_utils import write_jsonl
from tests.test_validator import _write_minimal_dataset


def _write_answer_results(path: Path) -> None:
    write_jsonl(
        path,
        [
            {
                "id": "q000001",
                "method": "oracle_context",
                "split": "dev",
                "prompt": "prompt text",
                "prediction": "B",
                "golden_answers": ["B"],
                "gold_context_ids": ["d000001"],
                "retrieved_context_ids": ["d000001"],
                "scores": {
                    "single_choice_accuracy": 1.0,
                    "retrieval_hit": 1.0,
                    "retrieval_recall": 1.0,
                    "retrieval_mrr": 1.0,
                },
                "latency_ms": 12.0,
                "input_tokens": 40,
                "output_tokens": 4,
                "api_calls": 1,
                "error": None,
            }
        ],
    )


def test_deepseek_judge_config_defaults_and_validation():
    config = DeepSeekJudgeConfig(api_key="test-key")

    assert config.max_tokens == 4096
    assert config.temperature == 0.0

    with pytest.raises(ValueError) as exc:
        DeepSeekJudgeConfig(api_key="test-key", max_retries=-1)

    assert "max_retries must be non-negative" in str(exc.value)


def test_build_judge_messages_contains_rag_md_scoring_contract():
    record = {
        "id": "q000001",
        "question": "Which option is supported?\nA. Bad\nB. Good",
        "golden_answers": ["B"],
        "metadata": {
            "question_type": "single_choice",
            "required_points": [],
            "answer_aliases": [],
        },
    }
    answer_row = {
        "id": "q000001",
        "method": "oracle_context",
        "prediction": "B",
        "scores": {"single_choice_accuracy": 1.0},
        "retrieved_context_ids": ["d000001"],
    }

    messages = build_judge_messages(
        record,
        answer_row,
        context_chunks=[{"id": "d000001", "contents": "Good is supported."}],
    )

    combined = "\n".join(message["content"] for message in messages)

    assert "Return exactly one JSON object" in combined
    assert "correctness" in combined
    assert "context_support" in combined
    assert "faithfulness" in combined
    assert "relevance" in combined
    assert "unsupported_claims" in combined
    assert "0 to 5" in combined
    assert "Good is supported" in combined
    assert "prediction" in combined


def test_normalize_judge_result_accepts_valid_schema():
    raw = {
        "correctness": 4,
        "context_support": 5,
        "faithfulness": 5,
        "relevance": 4,
        "unsupported_claims": [],
        "reason": "The answer matches the gold option and is supported.",
    }

    assert normalize_judge_result(raw) == {
        **raw,
        "correctness": 4.0,
        "context_support": 5.0,
        "faithfulness": 5.0,
        "relevance": 4.0,
    }


def test_normalize_judge_result_rejects_invalid_scores_and_fields():
    with pytest.raises(ValidationError) as exc:
        normalize_judge_result(
            {
                "correctness": 6,
                "context_support": 5,
                "faithfulness": 5,
                "relevance": 4,
                "unsupported_claims": [],
                "reason": "bad",
                "extra": "field",
            }
        )

    message = str(exc.value)
    assert "unexpected fields" in message
    assert "correctness must be 0..5" in message


def test_run_deepseek_judge_writes_judge_rows_with_usage(tmp_path: Path):
    dataset = tmp_path / "dataset"
    answers = tmp_path / "answers.jsonl"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    _write_answer_results(answers)

    def fake_chat_client(
        config: DeepSeekJudgeConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        assert config.model == "unit-test-model"
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "correctness": 5,
                                "context_support": 5,
                                "faithfulness": 5,
                                "relevance": 5,
                                "unsupported_claims": [],
                                "reason": "Fully supported.",
                            }
                        )
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 101,
                "completion_tokens": 23,
            },
        }

    result_path = run_deepseek_judge(
        dataset,
        answers,
        output,
        split="dev",
        config=DeepSeekJudgeConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 1
    assert rows[0]["id"] == "q000001"
    assert rows[0]["method"] == "oracle_context"
    assert rows[0]["judge"]["correctness"] == 5.0
    assert rows[0]["judge"]["unsupported_claims"] == []
    assert rows[0]["judge_scores"]["hallucination_risk"] == 0.0
    assert rows[0]["input_tokens"] == 101
    assert rows[0]["output_tokens"] == 23
    assert rows[0]["api_calls"] == 1
    assert rows[0]["error"] is None


def test_run_deepseek_judge_marks_answer_row_errors_without_api_call(tmp_path: Path):
    dataset = tmp_path / "dataset"
    answers = tmp_path / "answers.jsonl"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    rows = json.loads(
        (
            '{"id":"q000001","method":"no_rag","split":"dev","prediction":"",'
            '"golden_answers":["B"],"gold_context_ids":["d000001"],'
            '"retrieved_context_ids":[],"scores":{"single_choice_accuracy":0.0},'
            '"latency_ms":0.0,"input_tokens":10,"output_tokens":0,'
            '"api_calls":1,"error":"answer failed"}'
        )
    )
    write_jsonl(answers, [rows])

    def fake_chat_client(
        config: DeepSeekJudgeConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        raise AssertionError("judge should not call API for failed answer rows")

    result_path = run_deepseek_judge(
        dataset,
        answers,
        output,
        split="dev",
        config=DeepSeekJudgeConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
    )

    output_rows = [
        json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()
    ]

    assert output_rows[0]["judge"]["correctness"] == 0.0
    assert output_rows[0]["api_calls"] == 0
    assert "answer row error: answer failed" in output_rows[0]["error"]


def test_run_deepseek_judge_rejects_answer_rows_from_other_splits(tmp_path: Path):
    dataset = tmp_path / "dataset"
    answers = tmp_path / "answers.jsonl"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    _write_answer_results(answers)
    rows = [json.loads(line) for line in answers.read_text(encoding="utf-8").splitlines()]
    rows[0]["split"] = "test"
    write_jsonl(answers, rows)

    with pytest.raises(ValidationError) as exc:
        run_deepseek_judge(
            dataset,
            answers,
            output,
            split="dev",
            config=DeepSeekJudgeConfig(api_key="test-key", model="unit-test-model"),
            chat_client=lambda config, messages: {},
        )

    assert "answer row split must be dev" in str(exc.value)


def test_generate_judge_report_summarizes_scores_and_tokens(tmp_path: Path):
    input_path = tmp_path / "judge_results.jsonl"
    output = tmp_path / "report"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "oracle_context",
                "split": "dev",
                "judge": {
                    "correctness": 5.0,
                    "context_support": 4.0,
                    "faithfulness": 4.0,
                    "relevance": 5.0,
                    "unsupported_claims": [],
                    "reason": "good",
                },
                "judge_scores": {
                    "correctness": 5.0,
                    "context_support": 4.0,
                    "faithfulness": 4.0,
                    "relevance": 5.0,
                    "hallucination_risk": 1.0,
                },
                "latency_ms": 10.0,
                "input_tokens": 20,
                "output_tokens": 5,
                "api_calls": 1,
                "error": None,
            },
            {
                "id": "q2",
                "method": "oracle_context",
                "split": "dev",
                "judge": {
                    "correctness": 3.0,
                    "context_support": 2.0,
                    "faithfulness": 1.0,
                    "relevance": 3.0,
                    "unsupported_claims": ["unsupported mechanism"],
                    "reason": "partial",
                },
                "judge_scores": {
                    "correctness": 3.0,
                    "context_support": 2.0,
                    "faithfulness": 1.0,
                    "relevance": 3.0,
                    "hallucination_risk": 4.0,
                },
                "latency_ms": 14.0,
                "input_tokens": 30,
                "output_tokens": 7,
                "api_calls": 1,
                "error": None,
            },
        ],
    )

    markdown_path, json_path = generate_judge_report(input_path, output)
    summary = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert summary["oracle_context"]["questions"] == 2
    assert summary["oracle_context"]["metrics"]["correctness"] == 4.0
    assert summary["oracle_context"]["metrics"]["context_support"] == 3.0
    assert summary["oracle_context"]["metrics"]["hallucination_risk"] == 2.5
    assert summary["oracle_context"]["unsupported_claims"] == 1
    assert summary["oracle_context"]["total_tokens"] == 62
    assert "hallucination_risk: 2.5000" in markdown
