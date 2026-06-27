from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from domainrag.deepseek_answer_runner import (
    DeepSeekAnswerConfig,
    build_answer_messages,
    run_deepseek_answer_benchmark,
)
from domainrag.errors import ValidationError
from domainrag.io_utils import write_jsonl
from tests.test_validator import _write_minimal_dataset


def test_deepseek_answer_config_uses_generation_sized_token_budget():
    config = DeepSeekAnswerConfig(api_key="test-key")

    assert config.max_tokens == 4096


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"api_key": ""}, "api_key is required"),
        ({"api_key": "test-key", "timeout_seconds": 0}, "timeout_seconds must be positive"),
        ({"api_key": "test-key", "max_tokens": 0}, "max_tokens must be positive"),
        ({"api_key": "test-key", "top_k": 0}, "top_k must be positive"),
        ({"api_key": "test-key", "max_retries": -1}, "max_retries must be non-negative"),
    ],
)
def test_deepseek_answer_config_rejects_invalid_runtime_values(
    kwargs: dict[str, Any],
    message: str,
):
    with pytest.raises(ValueError) as exc:
        DeepSeekAnswerConfig(**kwargs)

    assert message in str(exc.value)


def test_build_answer_messages_includes_oracle_context_for_context_method():
    record = {
        "id": "q000001",
        "question": "Which option is Supported fact one?\nA. Unsupported\nB. Supported fact one",
        "metadata": {"question_type": "single_choice"},
    }
    messages = build_answer_messages(
        record,
        method="oracle_context",
        context_chunks=[{"id": "d000001", "contents": "Topic\nSupported fact one."}],
    )

    combined = "\n".join(message["content"] for message in messages)

    assert "Return exactly one JSON object" in combined
    assert '"answer"' in combined
    assert "Context chunks" in combined
    assert "d000001" in combined
    assert "Supported fact one" in combined


def test_build_answer_messages_omits_context_for_no_rag():
    record = {
        "id": "q000001",
        "question": "Which option is Supported fact one?\nA. Unsupported\nB. Supported fact one",
        "metadata": {"question_type": "single_choice"},
    }

    messages = build_answer_messages(
        record,
        method="no_rag",
        context_chunks=[{"id": "d000001", "contents": "Topic\nSupported fact one."}],
    )

    combined = "\n".join(message["content"] for message in messages)
    assert "Context chunks" not in combined
    assert "d000001" not in combined


def test_build_answer_messages_tells_choice_models_not_to_return_blank():
    record = {
        "id": "q000002",
        "question": "Which options are supported?\nA. One\nB. Two",
        "metadata": {"question_type": "multiple_choice"},
    }

    messages = build_answer_messages(
        record,
        method="lexical_rag",
        context_chunks=[{"id": "d000001", "contents": "One and two are supported."}],
    )

    combined = "\n".join(message["content"] for message in messages)

    assert "Never return an empty answer" in combined
    assert "Select every supported option" in combined
    assert "An option is supported when its statement is directly supported by any supplied context chunk" in combined


def test_build_answer_messages_warns_context_methods_against_unsupported_claims():
    record = {
        "id": "q000003",
        "question": "How do the mechanisms relate?",
        "metadata": {"question_type": "short_answer"},
    }

    messages = build_answer_messages(
        record,
        method="flashrag_bm25_live_deepseek",
        context_chunks=[{"id": "d000001", "contents": "Only fact one is stated."}],
    )

    combined = "\n".join(message["content"] for message in messages)

    assert "Use only facts stated in the supplied context chunks" in combined
    assert "Do not add mechanisms, causal links, or comparisons" in combined


def test_run_deepseek_answer_benchmark_writes_usage_and_retrieval_metrics(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    captured_messages: list[list[dict[str, str]]] = []

    def fake_chat_client(
        config: DeepSeekAnswerConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        captured_messages.append(messages)
        assert config.model == "unit-test-model"
        return {
            "choices": [{"message": {"content": json.dumps({"answer": "B"})}}],
            "usage": {
                "prompt_tokens": 17,
                "completion_tokens": 3,
                "total_tokens": 20,
            },
        }

    result_path = run_deepseek_answer_benchmark(
        dataset,
        output,
        methods=["oracle_context"],
        split="dev",
        config=DeepSeekAnswerConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 1
    assert rows[0]["method"] == "oracle_context"
    assert rows[0]["prediction"] == "B"
    assert rows[0]["gold_context_ids"] == ["d000001"]
    assert rows[0]["retrieved_context_ids"] == ["d000001"]
    assert rows[0]["scores"]["single_choice_accuracy"] == 1.0
    assert rows[0]["scores"]["retrieval_hit"] == 1.0
    assert rows[0]["scores"]["retrieval_recall"] == 1.0
    assert rows[0]["scores"]["retrieval_mrr"] == 1.0
    assert rows[0]["input_tokens"] == 17
    assert rows[0]["output_tokens"] == 3
    assert rows[0]["api_calls"] == 1
    assert rows[0]["error"] is None
    assert rows[0]["latency_ms"] >= 0.0
    assert "Supported fact one" in "\n".join(
        message["content"] for message in captured_messages[0]
    )


def test_run_deepseek_answer_benchmark_uses_flashrag_bm25_retrieval_file(
    tmp_path: Path,
):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    retrieval_results = tmp_path / "flashrag_bm25_results.jsonl"
    _write_minimal_dataset(dataset)
    write_jsonl(
        retrieval_results,
        [
            {
                "id": "q000001",
                "method": "flashrag_bm25_oracle_reader",
                "split": "dev",
                "retrieved_context_ids": ["d000001", "d000002"],
            }
        ],
    )
    captured_messages: list[list[dict[str, str]]] = []

    def fake_chat_client(
        config: DeepSeekAnswerConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        captured_messages.append(messages)
        return {
            "choices": [{"message": {"content": json.dumps({"answer": "B"})}}],
            "usage": {
                "prompt_tokens": 31,
                "completion_tokens": 2,
            },
        }

    result_path = run_deepseek_answer_benchmark(
        dataset,
        output,
        methods=["flashrag_bm25_live_deepseek"],
        split="dev",
        config=DeepSeekAnswerConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
        retrieval_results_path=retrieval_results,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]
    combined_prompt = "\n".join(message["content"] for message in captured_messages[0])

    assert rows[0]["method"] == "flashrag_bm25_live_deepseek"
    assert rows[0]["prediction"] == "B"
    assert rows[0]["retrieved_context_ids"] == ["d000001", "d000002"]
    assert rows[0]["scores"]["retrieval_hit"] == 1.0
    assert rows[0]["scores"]["retrieval_mrr"] == 1.0
    assert rows[0]["input_tokens"] == 31
    assert "Method: flashrag_bm25_live_deepseek" in combined_prompt
    assert "Supported fact one" in combined_prompt
    assert "Supported fact two" in combined_prompt


def test_run_deepseek_answer_benchmark_requires_retrieval_file_for_flashrag_bm25(
    tmp_path: Path,
):
    dataset = tmp_path / "dataset"
    _write_minimal_dataset(dataset)

    with pytest.raises(ValidationError) as exc:
        run_deepseek_answer_benchmark(
            dataset,
            tmp_path / "outputs",
            methods=["flashrag_bm25_live_deepseek"],
            split="dev",
            config=DeepSeekAnswerConfig(api_key="test-key", model="unit-test-model"),
            chat_client=lambda config, messages: {},
        )

    assert "retrieval_results_path is required" in str(exc.value)


def test_run_deepseek_answer_benchmark_records_errors_without_crashing(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    def fake_chat_client(
        config: DeepSeekAnswerConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        raise RuntimeError("temporary upstream failure")

    result_path = run_deepseek_answer_benchmark(
        dataset,
        output,
        methods=["no_rag"],
        split="dev",
        config=DeepSeekAnswerConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 1
    assert rows[0]["method"] == "no_rag"
    assert rows[0]["prediction"] == ""
    assert rows[0]["scores"]["single_choice_accuracy"] == 0.0
    assert rows[0]["retrieved_context_ids"] == []
    assert rows[0]["api_calls"] == 1
    assert rows[0]["input_tokens"] == 0
    assert rows[0]["output_tokens"] == 0
    assert "temporary upstream failure" in rows[0]["error"]


def test_run_deepseek_answer_benchmark_keeps_usage_when_response_content_is_empty(
    tmp_path: Path,
):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    def fake_chat_client(
        config: DeepSeekAnswerConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        return {
            "choices": [
                {
                    "finish_reason": "length",
                    "message": {
                        "role": "assistant",
                        "content": "",
                        "reasoning_content": "reasoning consumed the budget",
                    },
                }
            ],
            "usage": {
                "prompt_tokens": 23,
                "completion_tokens": 512,
            },
        }

    result_path = run_deepseek_answer_benchmark(
        dataset,
        output,
        methods=["oracle_context"],
        split="dev",
        config=DeepSeekAnswerConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]

    assert rows[0]["prediction"] == ""
    assert rows[0]["input_tokens"] == 23
    assert rows[0]["output_tokens"] == 512
    assert rows[0]["api_calls"] == 1
    assert "message content must be non-empty" in rows[0]["error"]


def test_run_deepseek_answer_benchmark_rejects_empty_answer_value(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    def fake_chat_client(
        config: DeepSeekAnswerConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        return {
            "choices": [{"message": {"content": json.dumps({"answer": ""})}}],
            "usage": {
                "prompt_tokens": 23,
                "completion_tokens": 4,
            },
        }

    result_path = run_deepseek_answer_benchmark(
        dataset,
        output,
        methods=["oracle_context"],
        split="dev",
        config=DeepSeekAnswerConfig(api_key="test-key", model="unit-test-model"),
        chat_client=fake_chat_client,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]

    assert rows[0]["prediction"] == ""
    assert rows[0]["input_tokens"] == 23
    assert rows[0]["output_tokens"] == 4
    assert "answer response must contain non-empty answer" in rows[0]["error"]


def test_run_deepseek_answer_benchmark_counts_retry_api_calls(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    attempts = 0

    def fake_chat_client(
        config: DeepSeekAnswerConfig,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("rate limited")
        return {
            "choices": [{"message": {"content": json.dumps({"answer": "B"})}}],
            "usage": {
                "prompt_tokens": 19,
                "completion_tokens": 2,
            },
        }

    result_path = run_deepseek_answer_benchmark(
        dataset,
        output,
        methods=["oracle_context"],
        split="dev",
        config=DeepSeekAnswerConfig(
            api_key="test-key",
            model="unit-test-model",
            max_retries=1,
        ),
        chat_client=fake_chat_client,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]

    assert attempts == 2
    assert rows[0]["api_calls"] == 2
    assert rows[0]["prediction"] == "B"
    assert rows[0]["input_tokens"] == 19
    assert rows[0]["output_tokens"] == 2
    assert rows[0]["error"] is None
