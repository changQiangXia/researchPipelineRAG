from __future__ import annotations

from pathlib import Path
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl, read_qrels
from domainrag.schema import (
    DIFFICULTIES,
    FORBIDDEN_PUBLIC_FIELD_FAMILIES,
    KNOWLEDGE_TYPES,
    QUESTION_TYPES,
    REQUIRED_CANONICAL_FIELDS,
    REQUIRED_CORPUS_FIELDS,
    REQUIRED_FLASHRAG_FIELDS,
    SPLIT_METADATA_BASE_FIELDS,
    SPLIT_METADATA_CHOICE_FIELDS,
)


SPLIT_FILES = {
    "dev": ("dev.jsonl", "dev.tsv"),
    "test": ("test.jsonl", "test.tsv"),
    "fresh_hard": ("fresh_hard_test.jsonl", "fresh_hard.tsv"),
}

NORMALIZED_FORBIDDEN_PUBLIC_FIELDS = {
    "".join(ch for ch in field.lower() if ch.isalnum())
    for field in FORBIDDEN_PUBLIC_FIELD_FAMILIES
}
MULTIPLE_CHOICE_OPTION_KEY_SETS = (
    {"A", "B", "C", "D", "E"},
    {"A", "B", "C", "D", "E", "F"},
)


def validate_dataset(dataset_dir: Path) -> None:
    issues: list[ValidationIssue] = []
    corpus_path = dataset_dir / "corpus.jsonl"
    canonical_path = dataset_dir / "canonical_dataset.jsonl"

    try:
        corpus = read_jsonl(corpus_path)
        canonical = read_jsonl(canonical_path)
    except ValidationError as exc:
        raise exc

    corpus_ids = _validate_corpus(corpus_path, corpus, issues)
    canonical_ids, chunk_groups, canonical_by_id = _validate_canonical(
        canonical_path,
        canonical,
        corpus_ids,
        issues,
    )

    split_to_source_groups: dict[str, set[tuple[str, ...]]] = {}
    for split_name, (json_name, qrels_name) in SPLIT_FILES.items():
        split_path = dataset_dir / json_name
        qrels_path = dataset_dir / "qrels" / qrels_name
        try:
            split_records = read_jsonl(split_path)
            qrels_rows = read_qrels(qrels_path)
        except ValidationError as exc:
            issues.extend(exc.issues)
            continue
        query_ids = _validate_split(
            split_path,
            split_records,
            canonical_ids,
            canonical_by_id,
            issues,
        )
        _validate_qrels(qrels_path, qrels_rows, query_ids, corpus_ids, issues)
        split_to_source_groups[split_name] = {
            tuple(chunk_groups[query_id])
            for query_id in query_ids
            if query_id in chunk_groups
        }

    if split_to_source_groups.get("dev", set()) & split_to_source_groups.get(
        "test",
        set(),
    ):
        issues.append(
            ValidationIssue(
                str(dataset_dir),
                "dev and test contain questions from the same source_chunk_ids group",
            )
        )

    if issues:
        raise ValidationError(issues)


def _validate_corpus(
    path: Path,
    records: list[dict[str, Any]],
    issues: list[ValidationIssue],
) -> set[str]:
    ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        _validate_exact_fields(path, f"record {index}", record, REQUIRED_CORPUS_FIELDS, issues)
        _reject_forbidden_public_fields(path, f"record {index}", record, issues)
        if REQUIRED_CORPUS_FIELDS - set(record):
            continue
        record_id = record.get("id")
        if isinstance(record_id, str):
            ids.add(record_id)
        else:
            issues.append(
                ValidationIssue(str(path), f"record {index}: id must be a string")
            )
    return ids


def _validate_canonical(
    path: Path,
    records: list[dict[str, Any]],
    corpus_ids: set[str],
    issues: list[ValidationIssue],
) -> tuple[set[str], dict[str, list[str]], dict[str, dict[str, Any]]]:
    ids: set[str] = set()
    chunk_groups: dict[str, list[str]] = {}
    canonical_by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records, start=1):
        _validate_exact_fields(
            path,
            f"record {index}",
            record,
            REQUIRED_CANONICAL_FIELDS,
            issues,
        )
        _reject_forbidden_public_fields(path, f"record {index}", record, issues)
        if REQUIRED_CANONICAL_FIELDS - set(record):
            continue
        question_id = record["id"]
        if not isinstance(question_id, str):
            issues.append(ValidationIssue(str(path), f"record {index}: id must be a string"))
            continue
        ids.add(question_id)
        canonical_by_id[question_id] = record
        if record["question_type"] not in QUESTION_TYPES:
            issues.append(ValidationIssue(str(path), f"{question_id}: unknown question_type"))
        if record["knowledge_type"] not in KNOWLEDGE_TYPES:
            issues.append(ValidationIssue(str(path), f"{question_id}: unknown knowledge_type"))
        if record["difficulty"] not in DIFFICULTIES:
            issues.append(ValidationIssue(str(path), f"{question_id}: unknown difficulty"))
        if not isinstance(record["answer"], list):
            issues.append(ValidationIssue(str(path), f"{question_id}: answer must be an array"))
        source_chunk_ids = record["source_chunk_ids"]
        if not isinstance(source_chunk_ids, list) or not source_chunk_ids:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: source_chunk_ids must be a non-empty array",
                )
            )
            source_chunk_ids = []
        for chunk_id in source_chunk_ids:
            if chunk_id not in corpus_ids:
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"{question_id}: source chunk {chunk_id} not in corpus",
                    )
                )
        chunk_groups[question_id] = sorted(str(chunk_id) for chunk_id in source_chunk_ids)
        _validate_type_rules(path, record, issues)
    return ids, chunk_groups, canonical_by_id


def _validate_type_rules(
    path: Path,
    record: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    question_id = record["id"]
    question_type = record["question_type"]
    answer = record["answer"]
    options = record["options"]
    if question_type == "single_choice":
        if not isinstance(options, dict) or set(options) != {"A", "B", "C", "D"}:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: single_choice requires A-D options",
                )
            )
        else:
            _validate_option_values(path, question_id, options, issues)
        if not isinstance(answer, list) or len(answer) != 1:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: single_choice requires one answer",
                )
            )
        elif isinstance(options, dict):
            _validate_choice_answers(path, question_id, answer, set(options), issues)
    if question_type == "multiple_choice":
        if not isinstance(options, dict) or set(options) not in MULTIPLE_CHOICE_OPTION_KEY_SETS:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: multiple_choice requires A-E or A-F options",
                )
            )
        else:
            _validate_option_values(path, question_id, options, issues)
        if not isinstance(answer, list) or len(answer) < 2:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: multiple_choice requires at least two answers",
                )
            )
        else:
            option_keys = set(options) if isinstance(options, dict) else set()
            valid_answer_count = _validate_choice_answers(
                path,
                question_id,
                answer,
                option_keys,
                issues,
            )
            if valid_answer_count < 2:
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"{question_id}: multiple_choice requires at least two distinct answers",
                    )
                )
    if question_type == "fill_blank":
        if not isinstance(record["answer_aliases"], list) or not record["answer_aliases"]:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: fill_blank requires answer_aliases",
                )
            )
    if question_type == "short_answer":
        if not record["reference_answer"]:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: short_answer requires reference_answer",
                )
            )
        if not isinstance(record["required_points"], list) or not record["required_points"]:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: short_answer requires required_points",
                )
            )


def _validate_split(
    path: Path,
    records: list[dict[str, Any]],
    canonical_ids: set[str],
    canonical_by_id: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> set[str]:
    ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        _validate_exact_fields(path, f"record {index}", record, REQUIRED_FLASHRAG_FIELDS, issues)
        _reject_forbidden_public_fields(path, f"record {index}", record, issues)
        if REQUIRED_FLASHRAG_FIELDS - set(record):
            continue
        question_id = record["id"]
        if not isinstance(question_id, str):
            issues.append(
                ValidationIssue(str(path), f"record {index}: id must be a string")
            )
            continue
        ids.add(question_id)
        if question_id not in canonical_ids:
            issues.append(
                ValidationIssue(str(path), f"{question_id}: not in canonical_dataset.jsonl")
            )
            continue
        _validate_split_against_canonical(path, record, canonical_by_id[question_id], issues)
    return ids


def _validate_qrels(
    path: Path,
    rows: list[tuple[str, str, int]],
    query_ids: set[str],
    corpus_ids: set[str],
    issues: list[ValidationIssue],
) -> None:
    seen_queries: set[str] = set()
    for query_id, corpus_id, score in rows:
        seen_queries.add(query_id)
        if query_id not in query_ids:
            issues.append(ValidationIssue(str(path), f"{query_id}: qrels query not in split"))
        if corpus_id not in corpus_ids:
            issues.append(
                ValidationIssue(str(path), f"{corpus_id}: qrels corpus id not in corpus")
            )
        if score < 0:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{query_id}/{corpus_id}: qrels score must be non-negative",
                )
            )
    missing = query_ids - seen_queries
    for query_id in sorted(missing):
        issues.append(ValidationIssue(str(path), f"{query_id}: missing qrels row"))


def _validate_exact_fields(
    path: Path,
    label: str,
    record: dict[str, Any],
    expected_fields: set[str],
    issues: list[ValidationIssue],
) -> None:
    actual_fields = set(record)
    missing = expected_fields - actual_fields
    extra = actual_fields - expected_fields
    if missing:
        issues.append(
            ValidationIssue(
                str(path),
                f"{label}: missing fields {sorted(missing)}",
            )
        )
    if extra:
        issues.append(
            ValidationIssue(
                str(path),
                f"{label}: unexpected fields {sorted(extra)}",
            )
        )


def _reject_forbidden_public_fields(
    path: Path,
    label: str,
    value: Any,
    issues: list[ValidationIssue],
    location: str | None = None,
) -> None:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            nested_location = key if location is None else f"{location}.{key}"
            if _is_forbidden_public_field(key):
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"{label}: forbidden field '{nested_location}'",
                    )
                )
            _reject_forbidden_public_fields(path, label, nested_value, issues, nested_location)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            nested_location = f"{location}[{index}]" if location is not None else f"[{index}]"
            _reject_forbidden_public_fields(path, label, item, issues, nested_location)


def _is_forbidden_public_field(key: str) -> bool:
    normalized = "".join(ch for ch in key.lower() if ch.isalnum())
    return normalized in NORMALIZED_FORBIDDEN_PUBLIC_FIELDS


def _validate_option_values(
    path: Path,
    question_id: str,
    options: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    for option_key, option_value in options.items():
        if not isinstance(option_value, str) or not option_value.strip():
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: option {option_key} must be a non-empty string",
                )
            )


def _validate_choice_answers(
    path: Path,
    question_id: str,
    answers: list[Any],
    option_keys: set[str],
    issues: list[ValidationIssue],
) -> int:
    valid_answers: list[str] = []
    for answer_value in answers:
        if not isinstance(answer_value, str):
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: choice answers must be strings",
                )
            )
            continue
        if answer_value not in option_keys:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: answer {answer_value} must be present in option keys",
                )
            )
            continue
        valid_answers.append(answer_value)

    if len(valid_answers) != len(set(valid_answers)):
        issues.append(
            ValidationIssue(
                str(path),
                f"{question_id}: choice answers must not contain duplicates",
            )
        )
    return len(set(valid_answers))


def _validate_split_against_canonical(
    path: Path,
    record: dict[str, Any],
    canonical_record: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    question_id = record["id"]
    if record.get("golden_answers") != canonical_record["answer"]:
        issues.append(
            ValidationIssue(
                str(path),
                f"{question_id}: golden_answers must match canonical answer",
            )
        )

    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(str(path), f"{question_id}: metadata must be an object")
        )
        return

    expected_fields = set(SPLIT_METADATA_BASE_FIELDS)
    if canonical_record["question_type"] in {"single_choice", "multiple_choice"}:
        expected_fields |= SPLIT_METADATA_CHOICE_FIELDS
    _validate_exact_fields(path, f"{question_id}: metadata", metadata, expected_fields, issues)

    for field in sorted(SPLIT_METADATA_BASE_FIELDS):
        if field in metadata and metadata[field] != canonical_record[field]:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: metadata.{field} must match canonical {field}",
                )
            )
    if (
        canonical_record["question_type"] in {"single_choice", "multiple_choice"}
        and "correct_options" in metadata
        and metadata["correct_options"] != canonical_record["answer"]
    ):
        issues.append(
            ValidationIssue(
                str(path),
                f"{question_id}: metadata.correct_options must match canonical answer",
            )
        )
