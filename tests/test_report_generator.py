import json
from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.io_utils import write_jsonl
from domainrag.report_generator import generate_report


def test_generate_report_writes_markdown_and_json(tmp_path: Path):
    input_path = tmp_path / "results.jsonl"
    output_dir = tmp_path / "reports"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            }
        ],
    )

    markdown_path, json_path = generate_report(input_path, output_dir)

    assert markdown_path.exists()
    assert json_path.exists()
    assert "mock_rag" in markdown_path.read_text(encoding="utf-8")


def test_generate_report_marks_fresh_hard_candidates(tmp_path: Path):
    input_path = tmp_path / "results.jsonl"
    output_dir = tmp_path / "reports"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "no_rag",
                "split": "fresh_hard",
                "scores": {"single_choice_accuracy": 0.0},
                "latency_ms": 0.0,
                "input_tokens": 5,
                "output_tokens": 0,
                "api_calls": 0,
                "error": None,
            },
            {
                "id": "q1",
                "method": "oracle_context",
                "split": "fresh_hard",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 0.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
            {
                "id": "q2",
                "method": "no_rag",
                "split": "fresh_hard",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 0.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
            {
                "id": "q2",
                "method": "oracle_context",
                "split": "fresh_hard",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 0.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
        ],
    )

    _, json_path = generate_report(input_path, output_dir)
    summary = json.loads(json_path.read_text(encoding="utf-8"))

    assert summary["_diagnostics"]["fresh_hard_candidates"] == 1
    assert summary["_diagnostics"]["fresh_hard_candidate_ids"] == ["q1"]


def test_generate_report_summarizes_token_usage(tmp_path: Path):
    input_path = tmp_path / "results.jsonl"
    output_dir = tmp_path / "reports"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "deepseek_oracle",
                "split": "dev",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 10.0,
                "input_tokens": 11,
                "output_tokens": 2,
                "api_calls": 1,
                "error": None,
            },
            {
                "id": "q2",
                "method": "deepseek_oracle",
                "split": "dev",
                "scores": {"single_choice_accuracy": 0.0},
                "latency_ms": 20.0,
                "input_tokens": 13,
                "output_tokens": 4,
                "api_calls": 1,
                "error": None,
            },
        ],
    )

    markdown_path, json_path = generate_report(input_path, output_dir)
    summary = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert summary["deepseek_oracle"]["total_input_tokens"] == 24
    assert summary["deepseek_oracle"]["total_output_tokens"] == 6
    assert summary["deepseek_oracle"]["total_tokens"] == 30
    assert summary["deepseek_oracle"]["mean_input_tokens"] == 12
    assert summary["deepseek_oracle"]["mean_output_tokens"] == 3
    assert "Total tokens: 30" in markdown


@pytest.mark.parametrize(
    "row, message",
    [
        (
            {
                "id": "q1",
                "method": 123,
                "split": "dev",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
            "record 1: method must be a string",
        ),
        (
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": [],
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
            "record 1: scores must be an object",
        ),
        (
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": {"single_choice_accuracy": "bad"},
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
            "record 1: scores.single_choice_accuracy must be numeric",
        ),
        (
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": "fast",
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            },
            "record 1: latency_ms must be numeric",
        ),
        (
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": "two",
                "error": None,
            },
            "record 1: api_calls must be an integer-compatible number",
        ),
    ],
)
def test_generate_report_rejects_invalid_rows(
    tmp_path: Path,
    row: dict,
    message: str,
):
    input_path = tmp_path / "results.jsonl"
    output_dir = tmp_path / "reports"
    write_jsonl(input_path, [row])

    with pytest.raises(ValidationError) as exc:
        generate_report(input_path, output_dir)

    assert message in str(exc.value)
