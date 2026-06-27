from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.schema import (
    REQUIRED_CANONICAL_FIELDS,
    SPLIT_METADATA_BASE_FIELDS,
    SPLIT_METADATA_CHOICE_FIELDS,
)
from domainrag.validator import validate_dataset


EASY_DATASET_CHUNKS_FILE = "chunks.jsonl"
EASY_DATASET_ITEMS_FILE = "items.jsonl"
REQUIRED_CHUNK_FIELDS = {"id", "content"}
REQUIRED_ITEM_FIELDS = REQUIRED_CANONICAL_FIELDS | {"split"}
SPLIT_OUTPUT_FILES = {
    "dev": "dev.jsonl",
    "test": "test.jsonl",
    "fresh_hard": "fresh_hard_test.jsonl",
}
SAFE_DATASET_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


@dataclass(frozen=True)
class DomainRAGExportBundle:
    dataset_name: str
    output_dir: Path
    dataset_dir: Path
    corpus_path: Path
    canonical_path: Path
    qrels_dir: Path
    dataset_card_path: Path
    statistics_path: Path


def export_domainrag_bundle(
    input_dir: Path,
    output_dir: Path,
    dataset_name: str,
) -> DomainRAGExportBundle:
    resolved_dataset_name = _validate_dataset_name(dataset_name)
    target_dataset_dir = output_dir / resolved_dataset_name
    _validate_target_does_not_overlap_source(input_dir, target_dataset_dir)

    chunks = read_jsonl(input_dir / EASY_DATASET_CHUNKS_FILE)
    items = read_jsonl(input_dir / EASY_DATASET_ITEMS_FILE)
    corpus_records, chunk_ids = _prepare_corpus_records(
        input_dir / EASY_DATASET_CHUNKS_FILE,
        chunks,
    )
    canonical_records, split_records, qrels_rows = _prepare_item_records(
        input_dir / EASY_DATASET_ITEMS_FILE,
        items,
        chunk_ids,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    staging_dataset_dir = output_dir / f".{resolved_dataset_name}.tmp"
    if staging_dataset_dir.exists():
        shutil.rmtree(staging_dataset_dir)
    staging_dataset_dir.mkdir(parents=True, exist_ok=True)

    try:
        _write_domainrag_dataset(
            staging_dataset_dir,
            resolved_dataset_name,
            corpus_records,
            canonical_records,
            split_records,
            qrels_rows,
        )
        validate_dataset(staging_dataset_dir)
        if target_dataset_dir.exists():
            shutil.rmtree(target_dataset_dir)
        staging_dataset_dir.rename(target_dataset_dir)
    except Exception:
        if staging_dataset_dir.exists():
            shutil.rmtree(staging_dataset_dir)
        raise

    corpus_path = target_dataset_dir / "corpus.jsonl"
    canonical_path = target_dataset_dir / "canonical_dataset.jsonl"
    qrels_dir = target_dataset_dir / "qrels"
    dataset_card_path = target_dataset_dir / "dataset_card.md"
    statistics_path = target_dataset_dir / "statistics.json"

    return DomainRAGExportBundle(
        dataset_name=resolved_dataset_name,
        output_dir=output_dir,
        dataset_dir=target_dataset_dir,
        corpus_path=corpus_path,
        canonical_path=canonical_path,
        qrels_dir=qrels_dir,
        dataset_card_path=dataset_card_path,
        statistics_path=statistics_path,
    )


def _write_domainrag_dataset(
    dataset_dir: Path,
    dataset_name: str,
    corpus_records: list[dict[str, str]],
    canonical_records: list[dict[str, Any]],
    split_records: dict[str, list[dict[str, Any]]],
    qrels_rows: dict[str, list[tuple[str, str, int]]],
) -> None:
    corpus_path = dataset_dir / "corpus.jsonl"
    canonical_path = dataset_dir / "canonical_dataset.jsonl"
    qrels_dir = dataset_dir / "qrels"
    dataset_card_path = dataset_dir / "dataset_card.md"
    statistics_path = dataset_dir / "statistics.json"

    write_jsonl(corpus_path, corpus_records)
    write_jsonl(canonical_path, canonical_records)

    for split_name, output_name in SPLIT_OUTPUT_FILES.items():
        write_jsonl(dataset_dir / output_name, split_records[split_name])

    qrels_dir.mkdir(parents=True, exist_ok=True)
    for split_name in SPLIT_OUTPUT_FILES:
        _write_qrels(qrels_dir / f"{split_name}.tsv", qrels_rows[split_name])

    dataset_card_path.write_text(
        _render_dataset_card(dataset_name, corpus_records, canonical_records),
        encoding="utf-8",
    )
    statistics_path.write_text(
        json.dumps(
            _build_statistics(
                dataset_name,
                corpus_records,
                canonical_records,
                split_records,
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _prepare_corpus_records(
    path: Path,
    chunks: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], set[str]]:
    issues: list[ValidationIssue] = []
    if not chunks:
        issues.append(ValidationIssue(str(path), "chunks.jsonl must not be empty"))

    seen_ids: set[str] = set()
    corpus_records: list[dict[str, str]] = []
    for index, chunk in enumerate(chunks, start=1):
        missing = REQUIRED_CHUNK_FIELDS - set(chunk)
        if missing:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"record {index}: missing fields {sorted(missing)}",
                )
            )
            continue
        chunk_id = chunk["id"]
        content = chunk["content"]
        if not isinstance(chunk_id, str) or not chunk_id:
            issues.append(ValidationIssue(str(path), f"record {index}: id must be a string"))
            continue
        if chunk_id in seen_ids:
            issues.append(ValidationIssue(str(path), f"{chunk_id}: duplicate chunk id"))
            continue
        if not isinstance(content, str) or not content.strip():
            issues.append(
                ValidationIssue(str(path), f"{chunk_id}: content must be a non-empty string")
            )
            continue
        seen_ids.add(chunk_id)
        corpus_records.append({"id": chunk_id, "contents": content})

    if issues:
        raise ValidationError(issues)
    return corpus_records, seen_ids


def _prepare_item_records(
    path: Path,
    items: list[dict[str, Any]],
    chunk_ids: set[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[tuple[str, str, int]]],
]:
    issues: list[ValidationIssue] = []
    if not items:
        issues.append(ValidationIssue(str(path), "items.jsonl must not be empty"))

    seen_ids: set[str] = set()
    canonical_records: list[dict[str, Any]] = []
    split_records: dict[str, list[dict[str, Any]]] = {
        split_name: [] for split_name in SPLIT_OUTPUT_FILES
    }
    qrels_rows: dict[str, list[tuple[str, str, int]]] = {
        split_name: [] for split_name in SPLIT_OUTPUT_FILES
    }

    for index, item in enumerate(items, start=1):
        missing = REQUIRED_ITEM_FIELDS - set(item)
        if missing:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"record {index}: missing fields {sorted(missing)}",
                )
            )
            continue
        question_id = item["id"]
        split_name = item["split"]
        if not isinstance(question_id, str) or not question_id:
            issues.append(ValidationIssue(str(path), f"record {index}: id must be a string"))
            continue
        if question_id in seen_ids:
            issues.append(ValidationIssue(str(path), f"{question_id}: duplicate item id"))
            continue
        if split_name not in SPLIT_OUTPUT_FILES:
            issues.append(
                ValidationIssue(str(path), f"{question_id}: unsupported split {split_name}")
            )
            continue

        source_chunk_ids = item["source_chunk_ids"]
        if not isinstance(source_chunk_ids, list) or not source_chunk_ids:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"{question_id}: source_chunk_ids must be a non-empty array",
                )
            )
            continue
        for chunk_id in source_chunk_ids:
            if chunk_id not in chunk_ids:
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"{question_id}: source chunk {chunk_id} not in chunks.jsonl",
                    )
                )

        canonical_record = {
            field: item[field]
            for field in REQUIRED_CANONICAL_FIELDS
        }
        canonical_records.append(canonical_record)
        split_records[split_name].append(_render_split_record(canonical_record))
        qrels_rows[split_name].extend(
            (question_id, chunk_id, 1) for chunk_id in source_chunk_ids
        )
        seen_ids.add(question_id)

    missing_splits = [
        split_name
        for split_name, records in split_records.items()
        if not records
    ]
    for split_name in missing_splits:
        issues.append(ValidationIssue(str(path), f"missing required split {split_name}"))

    if issues:
        raise ValidationError(issues)
    return canonical_records, split_records, qrels_rows


def _render_split_record(item: dict[str, Any]) -> dict[str, Any]:
    metadata = {
        field: item[field]
        for field in sorted(SPLIT_METADATA_BASE_FIELDS)
    }
    if item["question_type"] in {"single_choice", "multiple_choice"}:
        metadata.update(
            {
                field: item["answer"]
                for field in sorted(SPLIT_METADATA_CHOICE_FIELDS)
            }
        )
    return {
        "id": item["id"],
        "question": _render_question(item),
        "golden_answers": item["answer"],
        "metadata": metadata,
    }


def _render_question(item: dict[str, Any]) -> str:
    options = item.get("options")
    if item["question_type"] not in {"single_choice", "multiple_choice"}:
        return item["question"]
    if not isinstance(options, dict) or not options:
        return item["question"]
    option_lines = [
        f"{option_key}. {options[option_key]}"
        for option_key in sorted(options)
    ]
    return "\n".join([item["question"], *option_lines])


def _write_qrels(path: Path, rows: list[tuple[str, str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for query_id, corpus_id, score in rows:
            handle.write(f"{query_id}\t{corpus_id}\t{score}\n")


def _render_dataset_card(
    dataset_name: str,
    corpus_records: list[dict[str, str]],
    canonical_records: list[dict[str, Any]],
) -> str:
    return "\n".join(
        [
            f"# {dataset_name}",
            "",
            "Generated from an Easy Dataset-style enriched export bundle.",
            "",
            f"- Corpus rows: {len(corpus_records)}",
            f"- Question rows: {len(canonical_records)}",
            "- Public metadata follows the DomainRAG data contract.",
            "- Source paper identity metadata is not included in public artifacts.",
            "",
        ]
    )


def _build_statistics(
    dataset_name: str,
    corpus_records: list[dict[str, str]],
    canonical_records: list[dict[str, Any]],
    split_records: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    type_counts = Counter()
    difficulty_counts = Counter()
    for item in canonical_records:
        type_counts[item["question_type"]] += 1
        difficulty_counts[item["difficulty"]] += 1

    return {
        "dataset_name": dataset_name,
        "corpus_count": len(corpus_records),
        "question_count": len(canonical_records),
        "question_type_counts": dict(sorted(type_counts.items())),
        "difficulty_counts": dict(sorted(difficulty_counts.items())),
        "required_splits": sorted(SPLIT_OUTPUT_FILES),
        "split_counts": {
            split_name: len(split_records[split_name])
            for split_name in sorted(SPLIT_OUTPUT_FILES)
        },
    }


def _validate_dataset_name(dataset_name: str) -> str:
    if (
        not dataset_name
        or dataset_name in {".", ".."}
        or "/" in dataset_name
        or "\\" in dataset_name
        or not SAFE_DATASET_NAME_PATTERN.fullmatch(dataset_name)
    ):
        raise ValidationError(
            [
                ValidationIssue(
                    path="dataset_name",
                    message=(
                        "dataset_name must be a simple dataset basename "
                        "containing only letters, numbers, '.', '_' or '-'"
                    ),
                )
            ]
        )
    return dataset_name


def _validate_target_does_not_overlap_source(
    input_dir: Path,
    target_dataset_dir: Path,
) -> None:
    resolved_source = input_dir.resolve()
    resolved_target = target_dataset_dir.resolve()
    if (
        resolved_target == resolved_source
        or resolved_source in resolved_target.parents
        or resolved_target in resolved_source.parents
    ):
        raise ValidationError(
            [
                ValidationIssue(
                    path=str(target_dataset_dir),
                    message=(
                        "output dataset directory overlaps the Easy Dataset input directory; "
                        "choose an output path outside the source export"
                    ),
                )
            ]
        )
