from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.schema import (
    DIFFICULTIES,
    KNOWLEDGE_TYPES,
    QUESTION_TYPES,
    REQUIRED_CANONICAL_FIELDS,
)


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-pro"
REQUIRED_GENERATED_ITEM_FIELDS = REQUIRED_CANONICAL_FIELDS | {"split"}
REVIEW_FIELDS = {"accepted", "quality_score", "problems", "corrected_item"}
FORBIDDEN_SOURCE_IDENTITY_PHRASES = (
    "this paper",
    "the paper",
    "this article",
    "the article",
    "according to the paper",
    "according to this paper",
    "provided information",
    "provided chunk",
)


@dataclass(frozen=True)
class ChatCompletionConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout_seconds: int = 120
    max_tokens: int = 1800
    temperature: float = 0.1

    def endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


def build_generation_messages(
    chunk: dict[str, Any],
    *,
    split: str,
    question_type: str,
) -> list[dict[str, str]]:
    chunk_id = _require_string(chunk, "id", "chunk")
    content = _require_string(chunk, "content", chunk_id)
    if question_type not in QUESTION_TYPES:
        raise ValidationError([ValidationIssue("question_type", "unsupported question_type")])
    if split not in {"dev", "test", "fresh_hard"}:
        raise ValidationError([ValidationIssue("split", "unsupported split")])

    system = (
        "You are a DomainRAG dataset item generator. Return exactly one JSON object "
        "and no markdown. Generate a self-contained professional domain question "
        "from the supplied knowledge chunk only."
    )
    user = "\n".join(
        [
            "Generate one candidate item for the DomainRAG contract.",
            "",
            "Hard constraints:",
            "- Return JSON with top-level key: item.",
            f"- item.split must be {split}.",
            f"- item.question_type must be {question_type}.",
            f"- item.source_chunk_ids must be exactly [\"{chunk_id}\"].",
            "- Do not include DOI, author, venue, page, source title, URL, or original PDF path.",
            "- Do not use phrases like this paper, the paper, this article, or the article.",
            "- The question must be answerable from the chunk without external context.",
            "- Use answer as an array for every question type.",
            "- For single_choice, options must be an object, not an array, with exactly keys A, B, C, D; answer must be one option key.",
            '- Single-choice shape example: {"options": {"A": "correct text", "B": "wrong text", "C": "wrong text", "D": "wrong text"}, "answer": ["A"]}',
            "- For multiple_choice, options must be an object, not an array, with exactly keys A, B, C, D, E or A, B, C, D, E, F; answer must include at least two option keys.",
            '- Multiple-choice shape example: {"options": {"A": "correct text", "B": "correct text", "C": "wrong text", "D": "wrong text", "E": "wrong text"}, "answer": ["A", "B"]}',
            "- For fill_blank and short_answer, options must be an empty object.",
            "- For fill_blank, provide non-empty answer_aliases.",
            "- For short_answer, provide non-empty required_points.",
            "- Do not start the question with According to, Based on, or Given the provided information.",
            "- Use knowledge_type from: fact, parameter, condition, method, mechanism, comparison, synthesis.",
            "- Use difficulty from: easy, medium, hard.",
            "- Use quality_score from 0.0 to 1.0.",
            "",
            "Required item fields:",
            ", ".join(sorted(REQUIRED_GENERATED_ITEM_FIELDS)),
            "",
            f"Chunk id: {chunk_id}",
            "Chunk content:",
            content,
        ]
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_review_messages(
    chunk: dict[str, Any],
    item: dict[str, Any],
) -> list[dict[str, str]]:
    chunk_id = _require_string(chunk, "id", "chunk")
    content = _require_string(chunk, "content", chunk_id)
    system = (
        "You are an independent DomainRAG quality reviewer. Return exactly one JSON "
        "object and no markdown."
    )
    user = "\n".join(
        [
            "Review whether the candidate item is safe to include in a public DomainRAG dataset.",
            "",
            "Reject or correct the item if:",
            "- it cannot be answered from the chunk,",
            "- it leaks DOI, author, venue, page, source title, URL, or original PDF path,",
            "- it says this paper, the paper, this article, or the article,",
            "- answers/options are ambiguous or unsupported,",
            "- fill_blank lacks aliases,",
            "- short_answer lacks required_points,",
            "- quality_score should be below 0.85.",
            "",
            "Return JSON with exactly these fields:",
            '{"accepted": true, "quality_score": 0.0, "problems": [], "corrected_item": {}}',
            "Use accepted=false when quality_score is below 0.85.",
            "",
            f"Chunk id: {chunk_id}",
            "Chunk content:",
            content,
            "",
            "Candidate item:",
            json.dumps(item, ensure_ascii=False, sort_keys=True),
        ]
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def parse_json_object(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise ValidationError(
            [ValidationIssue("deepseek_response", f"invalid JSON: {exc.msg}")]
        ) from exc
    if not isinstance(value, dict):
        raise ValidationError(
            [ValidationIssue("deepseek_response", "response must be a JSON object")]
        )
    return value


def normalize_generated_item(
    raw: dict[str, Any],
    *,
    chunk_id: str,
    split: str,
    question_type: str,
) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    _validate_exact_fields("generated_item", raw, REQUIRED_GENERATED_ITEM_FIELDS, issues)
    if issues:
        raise ValidationError(issues)

    if raw["split"] != split:
        issues.append(ValidationIssue("generated_item", f"split must be {split}"))
    if raw["question_type"] != question_type:
        issues.append(
            ValidationIssue("generated_item", f"question_type must be {question_type}")
        )
    if raw["question_type"] not in QUESTION_TYPES:
        issues.append(ValidationIssue("generated_item", "unknown question_type"))
    if raw["knowledge_type"] not in KNOWLEDGE_TYPES:
        issues.append(ValidationIssue("generated_item", "unknown knowledge_type"))
    if raw["difficulty"] not in DIFFICULTIES:
        issues.append(ValidationIssue("generated_item", "unknown difficulty"))
    if raw["source_chunk_ids"] != [chunk_id]:
        issues.append(
            ValidationIssue(
                "generated_item",
                f"source_chunk_ids must exactly match ['{chunk_id}']",
            )
        )
    _validate_question_type_rules(raw, issues)
    if not isinstance(raw["answer"], list) or not raw["answer"]:
        issues.append(ValidationIssue("generated_item", "answer must be a non-empty array"))
    if raw["question_type"] == "fill_blank" and not raw["answer_aliases"]:
        issues.append(ValidationIssue("generated_item", "fill_blank requires answer_aliases"))
    if raw["question_type"] == "short_answer" and not raw["required_points"]:
        issues.append(ValidationIssue("generated_item", "short_answer requires required_points"))
    if not isinstance(raw["quality_score"], int | float):
        issues.append(ValidationIssue("generated_item", "quality_score must be numeric"))
    else:
        score = float(raw["quality_score"])
        if score < 0.0 or score > 1.0:
            issues.append(ValidationIssue("generated_item", "quality_score must be 0.0..1.0"))

    _reject_source_identity_text(raw, issues)
    if issues:
        raise ValidationError(issues)
    return raw


def _validate_question_type_rules(
    raw: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    question_type = raw["question_type"]
    options = raw["options"]
    answer = raw["answer"]
    if question_type == "single_choice":
        if not isinstance(options, dict) or set(options) != {"A", "B", "C", "D"}:
            issues.append(
                ValidationIssue(
                    "generated_item",
                    "single_choice requires A-D options object",
                )
            )
            return
        if not isinstance(answer, list) or len(answer) != 1 or answer[0] not in options:
            issues.append(
                ValidationIssue(
                    "generated_item",
                    "single_choice answer must be one option key",
                )
            )
    elif question_type == "multiple_choice":
        valid_key_sets = ({"A", "B", "C", "D", "E"}, {"A", "B", "C", "D", "E", "F"})
        if not isinstance(options, dict) or set(options) not in valid_key_sets:
            issues.append(
                ValidationIssue(
                    "generated_item",
                    "multiple_choice requires A-E or A-F options object",
                )
            )
            return
        if (
            not isinstance(answer, list)
            or len(set(answer)) < 2
            or any(option_key not in options for option_key in answer)
        ):
            issues.append(
                ValidationIssue(
                    "generated_item",
                    "multiple_choice answer must contain at least two option keys",
                )
            )
    elif question_type in {"fill_blank", "short_answer"}:
        if options != {}:
            issues.append(
                ValidationIssue(
                    "generated_item",
                    f"{question_type} options must be an empty object",
                )
            )


def normalize_review_result(raw: dict[str, Any]) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    _validate_exact_fields("review_result", raw, REVIEW_FIELDS, issues)
    if issues:
        raise ValidationError(issues)

    if not isinstance(raw["accepted"], bool):
        issues.append(ValidationIssue("review_result", "accepted must be boolean"))
    if not isinstance(raw["quality_score"], int | float):
        issues.append(ValidationIssue("review_result", "quality_score must be numeric"))
    else:
        score = float(raw["quality_score"])
        if score < 0.0 or score > 1.0:
            issues.append(ValidationIssue("review_result", "quality_score must be 0.0..1.0"))
    if not isinstance(raw["problems"], list):
        issues.append(ValidationIssue("review_result", "problems must be an array"))
    if not isinstance(raw["corrected_item"], dict):
        issues.append(ValidationIssue("review_result", "corrected_item must be an object"))
    if issues:
        raise ValidationError(issues)
    return raw


def call_chat_completions(
    config: ChatCompletionConfig,
    messages: list[dict[str, str]],
) -> dict[str, Any]:
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "response_format": {"type": "json_object"},
    }
    body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        config.endpoint(),
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with request.urlopen(http_request, timeout=config.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek request failed with HTTP {exc.code}: {detail}") from exc


def extract_message_content(response: dict[str, Any]) -> str:
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValidationError(
            [ValidationIssue("deepseek_response", "missing choices[0].message.content")]
        ) from exc
    if not isinstance(content, str) or not content.strip():
        raise ValidationError(
            [ValidationIssue("deepseek_response", "message content must be non-empty")]
        )
    return content


def _validate_exact_fields(
    path: str,
    value: dict[str, Any],
    expected_fields: set[str],
    issues: list[ValidationIssue],
) -> None:
    actual_fields = set(value)
    missing = expected_fields - actual_fields
    extra = actual_fields - expected_fields
    if missing:
        issues.append(ValidationIssue(path, f"missing fields {sorted(missing)}"))
    if extra:
        issues.append(ValidationIssue(path, f"unexpected fields {sorted(extra)}"))


def _reject_source_identity_text(value: Any, issues: list[ValidationIssue]) -> None:
    if isinstance(value, dict):
        for nested_value in value.values():
            _reject_source_identity_text(nested_value, issues)
    elif isinstance(value, list):
        for item in value:
            _reject_source_identity_text(item, issues)
    elif isinstance(value, str):
        lowered = value.lower()
        for phrase in FORBIDDEN_SOURCE_IDENTITY_PHRASES:
            if phrase in lowered:
                issues.append(
                    ValidationIssue(
                        "generated_item",
                        f"question contains forbidden source-identity phrase: {phrase}",
                    )
                )


def _require_string(value: dict[str, Any], field: str, path: str) -> str:
    field_value = value.get(field)
    if not isinstance(field_value, str) or not field_value.strip():
        raise ValidationError([ValidationIssue(path, f"{field} must be a non-empty string")])
    return field_value
