from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    issues: list[ValidationIssue] = []
    if not path.exists():
        raise ValidationError([ValidationIssue(str(path), "file does not exist")])
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"line {line_number}: invalid JSON: {exc.msg}",
                    )
                )
                continue
            if not isinstance(value, dict):
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"line {line_number}: record must be an object",
                    )
                )
                continue
            records.append(value)
    if issues:
        raise ValidationError(issues)
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def read_qrels(path: Path) -> list[tuple[str, str, int]]:
    rows: list[tuple[str, str, int]] = []
    issues: list[ValidationIssue] = []
    if not path.exists():
        raise ValidationError([ValidationIssue(str(path), "file does not exist")])
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            columns = stripped.split("\t")
            if len(columns) != 3:
                issues.append(
                    ValidationIssue(str(path), f"line {line_number}: expected 3 columns")
                )
                continue
            query_id, corpus_id, raw_score = columns
            try:
                score = int(raw_score)
            except ValueError:
                issues.append(
                    ValidationIssue(
                        str(path),
                        f"line {line_number}: score must be an integer",
                    )
                )
                continue
            rows.append((query_id, corpus_id, score))
    if issues:
        raise ValidationError(issues)
    return rows
