from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from time import perf_counter
from typing import Any

from domainrag.benchmark_runner import _load_corpus
from domainrag.dataset_adapter import load_split
from domainrag.deepseek_pipeline import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    call_chat_completions,
    extract_message_content,
    parse_json_object,
)
from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.validator import validate_dataset


JUDGE_FIELDS = {
    "correctness",
    "context_support",
    "faithfulness",
    "relevance",
    "unsupported_claims",
    "reason",
}
JUDGE_SCORE_FIELDS = {
    "correctness",
    "context_support",
    "faithfulness",
    "relevance",
    "hallucination_risk",
}


@dataclass(frozen=True)
class DeepSeekJudgeConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout_seconds: int = 120
    max_tokens: int = 4096
    temperature: float = 0.0
    max_retries: int = 0

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ValueError("api_key is required")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")

    def endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


ChatClient = Callable[[DeepSeekJudgeConfig, list[dict[str, str]]], dict[str, Any]]


def run_deepseek_judge(
    dataset_dir: Path,
    answer_results_path: Path,
    output_dir: Path,
    *,
    split: str,
    config: DeepSeekJudgeConfig,
    chat_client: ChatClient = call_chat_completions,
    limit: int | None = None,
) -> Path:
    validate_dataset(dataset_dir)
    records = {record["id"]: record for record in load_split(dataset_dir, split)}
    corpus = _load_corpus(dataset_dir)
    answer_rows = read_jsonl(answer_results_path)
    if limit is not None:
        answer_rows = answer_rows[:limit]

    output_rows: list[dict[str, Any]] = []
    for answer_row in answer_rows:
        question_id = _require_string(answer_row, "id", "answer_row")
        answer_split = _require_string(answer_row, "split", question_id)
        if answer_split != split:
            raise ValidationError(
                [ValidationIssue(question_id, f"answer row split must be {split}")]
            )
        if question_id not in records:
            raise ValidationError(
                [ValidationIssue("answer_row", f"unknown question id: {question_id}")]
            )
        record = records[question_id]
        context_chunks = _context_chunks(answer_row, corpus)

        if answer_row.get("error"):
            output_rows.append(_failed_answer_row(record, answer_row))
            continue

        messages = build_judge_messages(record, answer_row, context_chunks=context_chunks)
        judge, usage, latency_ms, api_calls, error = _call_judge_model(
            config,
            messages,
            chat_client=chat_client,
        )
        output_rows.append(
            {
                "id": question_id,
                "method": _require_string(answer_row, "method", question_id),
                "split": split,
                "prediction": answer_row.get("prediction", ""),
                "golden_answers": record["golden_answers"],
                "gold_context_ids": answer_row.get("gold_context_ids", []),
                "retrieved_context_ids": answer_row.get("retrieved_context_ids", []),
                "judge": judge,
                "judge_scores": _judge_scores(judge),
                "latency_ms": latency_ms,
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"],
                "api_calls": api_calls,
                "error": error,
            }
        )

    result_path = output_dir / dataset_dir.name / f"{split}_judge_results.jsonl"
    write_jsonl(result_path, output_rows)
    return result_path


def build_judge_messages(
    record: dict[str, Any],
    answer_row: dict[str, Any],
    *,
    context_chunks: list[dict[str, str]],
) -> list[dict[str, str]]:
    system = (
        "You are a DomainRAG evaluation judge. Return exactly one JSON object "
        "and no markdown. Score professional RAG answers against the supplied "
        "question, retrieved context, model prediction, and gold answer."
    )
    context_text = (
        json.dumps(context_chunks, ensure_ascii=False, sort_keys=True)
        if context_chunks
        else "No retrieved context was supplied."
    )
    user = "\n".join(
        [
            "Judge the model prediction using the fixed JSON schema below.",
            "",
            "Scores use a 0 to 5 scale:",
            "- correctness: whether the prediction matches the gold answer.",
            "- context_support: whether the retrieved context supports the prediction.",
            "- faithfulness: whether the prediction avoids unsupported factual claims.",
            "- relevance: whether the prediction directly answers the question.",
            "- unsupported_claims: array of concise unsupported factual claims.",
            "- reason: one concise sentence explaining the score.",
            "",
            "Return JSON with exactly these fields:",
            json.dumps(
                {
                    "correctness": 0,
                    "context_support": 0,
                    "faithfulness": 0,
                    "relevance": 0,
                    "unsupported_claims": [],
                    "reason": "",
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            "",
            f"Question id: {record['id']}",
            f"Method: {answer_row.get('method', '')}",
            f"Question type: {record['metadata']['question_type']}",
            "",
            "Question:",
            record["question"],
            "",
            "Gold answers:",
            json.dumps(record["golden_answers"], ensure_ascii=False),
            "",
            "Reference metadata:",
            json.dumps(
                {
                    "answer_aliases": record["metadata"].get("answer_aliases", []),
                    "required_points": record["metadata"].get("required_points", []),
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            "",
            "Retrieved context:",
            context_text,
            "",
            "Model prediction:",
            str(answer_row.get("prediction", "")),
        ]
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def normalize_judge_result(raw: dict[str, Any]) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    actual_fields = set(raw)
    missing = JUDGE_FIELDS - actual_fields
    extra = actual_fields - JUDGE_FIELDS
    if missing:
        issues.append(ValidationIssue("judge_result", f"missing fields {sorted(missing)}"))
    if extra:
        issues.append(ValidationIssue("judge_result", f"unexpected fields {sorted(extra)}"))

    normalized: dict[str, Any] = dict(raw)
    for field in ["correctness", "context_support", "faithfulness", "relevance"]:
        value = raw.get(field)
        if not _is_number(value):
            issues.append(ValidationIssue("judge_result", f"{field} must be numeric"))
            continue
        score = float(value)
        if score < 0.0 or score > 5.0:
            issues.append(ValidationIssue("judge_result", f"{field} must be 0..5"))
            continue
        normalized[field] = score

    unsupported_claims = raw.get("unsupported_claims")
    if not isinstance(unsupported_claims, list) or not all(
        isinstance(claim, str) for claim in unsupported_claims
    ):
        issues.append(
            ValidationIssue("judge_result", "unsupported_claims must be an array of strings")
        )
    reason = raw.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        issues.append(ValidationIssue("judge_result", "reason must be a non-empty string"))

    if issues:
        raise ValidationError(issues)
    return normalized


def generate_judge_report(input_path: Path, output_dir: Path) -> tuple[Path, Path]:
    rows = _validate_judge_rows(input_path, read_jsonl(input_path))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)

    summary: dict[str, dict[str, Any]] = {}
    for method, method_rows in grouped.items():
        metric_values: dict[str, list[float]] = defaultdict(list)
        unsupported_claims = 0
        for row in method_rows:
            for metric, value in row["judge_scores"].items():
                metric_values[metric].append(value)
            unsupported_claims += len(row["judge"].get("unsupported_claims", []))
        summary[method] = {
            "questions": len(method_rows),
            "metrics": {
                metric: mean(values) for metric, values in sorted(metric_values.items())
            },
            "mean_latency_ms": mean(row["latency_ms"] for row in method_rows),
            "total_input_tokens": sum(row["input_tokens"] for row in method_rows),
            "total_output_tokens": sum(row["output_tokens"] for row in method_rows),
            "total_tokens": sum(row["input_tokens"] + row["output_tokens"] for row in method_rows),
            "api_calls": sum(row["api_calls"] for row in method_rows),
            "errors": sum(1 for row in method_rows if row.get("error")),
            "unsupported_claims": unsupported_claims,
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "summary.json"
    markdown_path = output_dir / "summary.md"
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    markdown_path.write_text(_render_judge_markdown(summary), encoding="utf-8")
    return markdown_path, json_path


def _call_judge_model(
    config: DeepSeekJudgeConfig,
    messages: list[dict[str, str]],
    *,
    chat_client: ChatClient,
) -> tuple[dict[str, Any], dict[str, int], float, int, str | None]:
    start = perf_counter()
    last_error: Exception | None = None
    api_calls = 0
    total_usage = {"input_tokens": 0, "output_tokens": 0}
    for _ in range(config.max_retries + 1):
        api_calls += 1
        try:
            response = chat_client(config, messages)
            content_for_usage = _response_content_for_usage(response)
            total_usage = _add_usage(
                total_usage,
                _usage_from_response(response, messages, content_for_usage),
            )
            latency_ms = (perf_counter() - start) * 1000.0
            content = extract_message_content(response)
            judge = normalize_judge_result(parse_json_object(content))
            return judge, total_usage, latency_ms, api_calls, None
        except Exception as exc:
            last_error = exc
    latency_ms = (perf_counter() - start) * 1000.0
    return _zero_judge(str(last_error)), total_usage, latency_ms, api_calls, str(last_error)


def _context_chunks(
    answer_row: dict[str, Any],
    corpus: dict[str, str],
) -> list[dict[str, str]]:
    context_ids = answer_row.get("retrieved_context_ids", [])
    if not isinstance(context_ids, list):
        return []
    return [
        {"id": context_id, "contents": corpus[context_id]}
        for context_id in context_ids
        if isinstance(context_id, str) and context_id in corpus
    ]


def _failed_answer_row(
    record: dict[str, Any],
    answer_row: dict[str, Any],
) -> dict[str, Any]:
    error = f"answer row error: {answer_row.get('error')}"
    judge = _zero_judge(error)
    return {
        "id": record["id"],
        "method": _require_string(answer_row, "method", record["id"]),
        "split": answer_row.get("split", ""),
        "prediction": answer_row.get("prediction", ""),
        "golden_answers": record["golden_answers"],
        "gold_context_ids": answer_row.get("gold_context_ids", []),
        "retrieved_context_ids": answer_row.get("retrieved_context_ids", []),
        "judge": judge,
        "judge_scores": _judge_scores(judge),
        "latency_ms": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
        "api_calls": 0,
        "error": error,
    }


def _zero_judge(reason: str) -> dict[str, Any]:
    return {
        "correctness": 0.0,
        "context_support": 0.0,
        "faithfulness": 0.0,
        "relevance": 0.0,
        "unsupported_claims": [],
        "reason": reason,
    }


def _judge_scores(judge: dict[str, Any]) -> dict[str, float]:
    faithfulness = float(judge.get("faithfulness", 0.0))
    return {
        "correctness": float(judge.get("correctness", 0.0)),
        "context_support": float(judge.get("context_support", 0.0)),
        "faithfulness": faithfulness,
        "relevance": float(judge.get("relevance", 0.0)),
        "hallucination_risk": max(0.0, 5.0 - faithfulness),
    }


def _validate_judge_rows(
    input_path: Path,
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    issues: list[ValidationIssue] = []
    validated_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        method = row.get("method")
        judge = row.get("judge")
        judge_scores = row.get("judge_scores")
        if not isinstance(method, str):
            issues.append(ValidationIssue(str(input_path), f"record {index}: method must be a string"))
        if not isinstance(judge, dict):
            issues.append(ValidationIssue(str(input_path), f"record {index}: judge must be an object"))
        if not isinstance(judge_scores, dict):
            issues.append(
                ValidationIssue(str(input_path), f"record {index}: judge_scores must be an object")
            )
        latency_ms = _numeric_field(input_path, row, index, "latency_ms", issues)
        input_tokens = _integer_field(input_path, row, index, "input_tokens", issues)
        output_tokens = _integer_field(input_path, row, index, "output_tokens", issues)
        api_calls = _integer_field(input_path, row, index, "api_calls", issues)
        if not isinstance(method, str) or not isinstance(judge, dict) or not isinstance(judge_scores, dict):
            continue
        scores: dict[str, float] = {}
        for field in JUDGE_SCORE_FIELDS:
            value = judge_scores.get(field)
            if not _is_number(value):
                issues.append(
                    ValidationIssue(
                        str(input_path),
                        f"record {index}: judge_scores.{field} must be numeric",
                    )
                )
                continue
            scores[field] = float(value)
        if (
            latency_ms is None
            or input_tokens is None
            or output_tokens is None
            or api_calls is None
        ):
            continue
        validated_rows.append(
            {
                **row,
                "method": method,
                "judge": judge,
                "judge_scores": scores,
                "latency_ms": latency_ms,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "api_calls": api_calls,
            }
        )
    if issues:
        raise ValidationError(issues)
    return validated_rows


def _render_judge_markdown(summary: dict[str, dict[str, Any]]) -> str:
    lines = ["# DomainRAG-Bench DeepSeek Judge Summary", ""]
    for method, values in sorted(summary.items()):
        lines.append(f"## {method}")
        lines.append("")
        lines.append(f"- Questions: {values['questions']}")
        lines.append(f"- Mean latency ms: {values['mean_latency_ms']:.3f}")
        lines.append(f"- Total input tokens: {values['total_input_tokens']}")
        lines.append(f"- Total output tokens: {values['total_output_tokens']}")
        lines.append(f"- Total tokens: {values['total_tokens']}")
        lines.append(f"- API calls: {values['api_calls']}")
        lines.append(f"- Errors: {values['errors']}")
        lines.append(f"- Unsupported claims: {values['unsupported_claims']}")
        for metric, score in sorted(values["metrics"].items()):
            lines.append(f"- {metric}: {score:.4f}")
        lines.append("")
    return "\n".join(lines)


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
    return {"input_tokens": input_tokens, "output_tokens": output_tokens}


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


def _serialize_messages(messages: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{message['role']}:\n{message['content']}" for message in messages)


def _numeric_field(
    input_path: Path,
    row: dict[str, Any],
    index: int,
    field: str,
    issues: list[ValidationIssue],
) -> float | None:
    value = row.get(field)
    if _is_number(value):
        return float(value)
    issues.append(ValidationIssue(str(input_path), f"record {index}: {field} must be numeric"))
    return None


def _integer_field(
    input_path: Path,
    row: dict[str, Any],
    index: int,
    field: str,
    issues: list[ValidationIssue],
) -> int | None:
    value = row.get(field)
    if _is_integer_compatible(value):
        return int(value)
    issues.append(
        ValidationIssue(
            str(input_path),
            f"record {index}: {field} must be an integer-compatible number",
        )
    )
    return None


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _integer_usage(value: Any) -> int | None:
    if _is_integer_compatible(value):
        return int(value)
    return None


def _is_integer_compatible(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value.is_integer()
    return False


def _require_string(value: dict[str, Any], field: str, path: str) -> str:
    field_value = value.get(field)
    if not isinstance(field_value, str) or not field_value.strip():
        raise ValidationError([ValidationIssue(path, f"{field} must be a non-empty string")])
    return field_value
