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
