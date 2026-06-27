from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

from domainrag.benchmark_runner import (
    _load_corpus,
    _load_qrels,
    _retrieval_scores,
    _retrieve_lexical,
)
from domainrag.dataset_adapter import load_split
from domainrag.deepseek_pipeline import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    call_chat_completions,
    extract_message_content,
    parse_json_object,
)
from domainrag.domain_evaluator import evaluate_record
from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.prompt_renderer import render_prompt
from domainrag.validator import validate_dataset


FLASHRAG_BM25_LIVE_METHOD = "flashrag_bm25_live_deepseek"
SUPPORTED_LIVE_METHODS = {
    "no_rag",
    "oracle_context",
    "lexical_rag",
    FLASHRAG_BM25_LIVE_METHOD,
}


@dataclass(frozen=True)
class DeepSeekAnswerConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout_seconds: int = 120
    max_tokens: int = 4096
    temperature: float = 0.0
    top_k: int = 5
    max_retries: int = 0

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ValueError("api_key is required")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")

    def endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


ChatClient = Callable[[DeepSeekAnswerConfig, list[dict[str, str]]], dict[str, Any]]


def run_deepseek_answer_benchmark(
    dataset_dir: Path,
    output_dir: Path,
    methods: list[str],
    split: str,
    config: DeepSeekAnswerConfig,
    *,
    chat_client: ChatClient = call_chat_completions,
    limit: int | None = None,
    retrieval_results_path: Path | None = None,
) -> Path:
    validate_dataset(dataset_dir)
    records = load_split(dataset_dir, split)
    if limit is not None:
        records = records[:limit]
    corpus = _load_corpus(dataset_dir)
    qrels = _load_qrels(dataset_dir, split)
    external_retrievals = _load_external_retrievals(
        retrieval_results_path,
        methods=methods,
        split=split,
    )
    output_records: list[dict[str, Any]] = []

    for method in methods:
        _validate_method(method)
        for record in records:
            gold_context_ids = qrels.get(record["id"], [])
            retrieved_context_ids = _select_context_ids(
                method,
                record=record,
                corpus=corpus,
                qrels=qrels,
                top_k=config.top_k,
                external_retrievals=external_retrievals,
            )
            context_chunks = [
                {"id": context_id, "contents": corpus[context_id]}
                for context_id in retrieved_context_ids
                if context_id in corpus
            ]
            messages = build_answer_messages(
                record,
                method=method,
                context_chunks=context_chunks,
            )
            prediction, usage, latency_ms, api_calls, error = _call_answer_model(
                config,
                messages,
                chat_client=chat_client,
            )
            scores = evaluate_record(record, prediction)
            scores.update(_retrieval_scores(gold_context_ids, retrieved_context_ids))
            output_records.append(
                {
                    "id": record["id"],
                    "method": method,
                    "split": split,
                    "prompt": _serialize_messages(messages),
                    "prediction": prediction,
                    "golden_answers": record["golden_answers"],
                    "gold_context_ids": gold_context_ids,
                    "retrieved_context_ids": retrieved_context_ids,
                    "scores": scores,
                    "latency_ms": latency_ms,
                    "input_tokens": usage["input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "api_calls": api_calls,
                    "error": error,
                }
            )

    result_path = output_dir / dataset_dir.name / f"{split}_deepseek_results.jsonl"
    write_jsonl(result_path, output_records)
    return result_path


def build_answer_messages(
    record: dict[str, Any],
    *,
    method: str,
    context_chunks: list[dict[str, str]],
) -> list[dict[str, str]]:
    question_type = record["metadata"]["question_type"]
    system = (
        "You are a DomainRAG benchmark answerer. Return exactly one JSON object "
        'and no markdown. The JSON object must use the shape {"answer": "..."}'
    )
    user_parts = [
        f"Method: {method}",
        f"Question type: {question_type}",
        "",
        "Answer-format constraints:",
        _answer_format_constraint(question_type),
        "",
        "Question:",
        record["question"],
    ]
    if method != "no_rag" and context_chunks:
        user_parts.extend(
            [
                "",
                "Context chunks:",
                json.dumps(context_chunks, ensure_ascii=False, sort_keys=True),
                "",
                "Use only facts stated in the supplied context chunks. "
                "Do not add mechanisms, causal links, or comparisons unless they are "
                "explicitly supported by those chunks. Do not cite chunk ids.",
            ]
        )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n".join(user_parts)},
    ]


def _call_answer_model(
    config: DeepSeekAnswerConfig,
    messages: list[dict[str, str]],
    *,
    chat_client: ChatClient,
) -> tuple[str, dict[str, int], float, int, str | None]:
    start = perf_counter()
    last_error: Exception | None = None
    api_calls = 0
    total_usage = {"input_tokens": 0, "output_tokens": 0}
    for _ in range(config.max_retries + 1):
        api_calls += 1
        try:
            response = chat_client(config, messages)
            total_usage = _add_usage(
                total_usage,
                _usage_from_response(response, messages, _response_content_for_usage(response)),
            )
            latency_ms = (perf_counter() - start) * 1000.0
            content = extract_message_content(response)
            parsed = parse_json_object(content)
            return (
                _normalize_answer(parsed.get("answer")),
                total_usage,
                latency_ms,
                api_calls,
                None,
            )
        except Exception as exc:
            last_error = exc
    latency_ms = (perf_counter() - start) * 1000.0
    return "", total_usage, latency_ms, api_calls, str(last_error)


def _select_context_ids(
    method: str,
    *,
    record: dict[str, Any],
    corpus: dict[str, str],
    qrels: dict[str, list[str]],
    top_k: int,
    external_retrievals: dict[str, list[str]],
) -> list[str]:
    if method == "no_rag":
        return []
    if method == "oracle_context":
        return qrels.get(record["id"], [])
    if method == "lexical_rag":
        return _retrieve_lexical(record["question"], corpus, top_k=top_k)
    if method == FLASHRAG_BM25_LIVE_METHOD:
        return external_retrievals.get(record["id"], [])
    raise ValueError(f"unsupported method: {method}")


def _load_external_retrievals(
    retrieval_results_path: Path | None,
    *,
    methods: list[str],
    split: str,
) -> dict[str, list[str]]:
    if FLASHRAG_BM25_LIVE_METHOD not in methods:
        return {}
    if retrieval_results_path is None:
        raise ValidationError(
            [
                ValidationIssue(
                    "retrieval_results_path",
                    f"retrieval_results_path is required for {FLASHRAG_BM25_LIVE_METHOD}",
                )
            ]
        )

    issues: list[ValidationIssue] = []
    retrievals: dict[str, list[str]] = {}
    for index, row in enumerate(read_jsonl(retrieval_results_path), start=1):
        question_id = row.get("id")
        row_split = row.get("split")
        context_ids = row.get("retrieved_context_ids")
        if not isinstance(question_id, str):
            issues.append(
                ValidationIssue(str(retrieval_results_path), f"record {index}: id must be a string")
            )
            continue
        if row_split != split:
            issues.append(
                ValidationIssue(
                    str(retrieval_results_path),
                    f"record {index}: split must be {split}",
                )
            )
            continue
        if not isinstance(context_ids, list) or not all(
            isinstance(context_id, str) for context_id in context_ids
        ):
            issues.append(
                ValidationIssue(
                    str(retrieval_results_path),
                    f"record {index}: retrieved_context_ids must be an array of strings",
                )
            )
            continue
        if question_id in retrievals:
            issues.append(
                ValidationIssue(
                    str(retrieval_results_path),
                    f"record {index}: duplicate id {question_id}",
                )
            )
            continue
        retrievals[question_id] = context_ids

    if issues:
        raise ValidationError(issues)
    return retrievals


def _answer_format_constraint(question_type: str) -> str:
    if question_type == "single_choice":
        return (
            "Select the one best supported option. Return exactly one uppercase option "
            "letter in answer, for example B. Never return an empty answer."
        )
    if question_type == "multiple_choice":
        return (
            "Select every supported option and omit unsupported options. Return sorted "
            "uppercase option letters separated by commas in answer, for example A,C,D. "
            "An option is supported when its statement is directly supported by any "
            "supplied context chunk; all correct options do not need to be supported by "
            "the same chunk. Never return an empty answer."
        )
    if question_type == "fill_blank":
        return "Return only the missing text in answer."
    if question_type == "short_answer":
        return "Return 1 to 4 concise answer sentences in answer."
    raise ValueError(f"unknown question_type: {question_type}")


def _normalize_answer(value: Any) -> str:
    if isinstance(value, str):
        answer = value.strip()
        if answer:
            return answer
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        answer = ",".join(item.strip() for item in value if item.strip())
        if answer:
            return answer
    raise ValueError("answer response must contain non-empty answer")


def _usage_from_response(
    response: dict[str, Any],
    messages: list[dict[str, str]],
    content: str,
) -> dict[str, int]:
    usage = response.get("usage", {})
    if not isinstance(usage, dict):
        usage = {}
    input_tokens = _integer_usage(usage.get("prompt_tokens"))
    output_tokens = _integer_usage(usage.get("completion_tokens"))
    if input_tokens is None:
        input_tokens = len(_serialize_messages(messages).split())
    if output_tokens is None:
        output_tokens = len(content.split())
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def _add_usage(
    current: dict[str, int],
    additional: dict[str, int],
) -> dict[str, int]:
    return {
        "input_tokens": current["input_tokens"] + additional["input_tokens"],
        "output_tokens": current["output_tokens"] + additional["output_tokens"],
    }


def _response_content_for_usage(response: dict[str, Any]) -> str:
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return ""
    return content if isinstance(content, str) else ""


def _integer_usage(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _serialize_messages(messages: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{message['role']}:\n{message['content']}" for message in messages)


def _validate_method(method: str) -> None:
    if method not in SUPPORTED_LIVE_METHODS:
        raise ValueError(f"unsupported method: {method}")
