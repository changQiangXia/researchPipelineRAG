from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl


def generate_report(input_path: Path, output_dir: Path) -> tuple[Path, Path]:
    rows = _validate_rows(input_path, read_jsonl(input_path))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)

    summary: dict[str, dict] = {}
    for method, method_rows in grouped.items():
        metric_values: dict[str, list[float]] = defaultdict(list)
        for row in method_rows:
            for metric, value in row["scores"].items():
                metric_values[metric].append(value)
        summary[method] = {
            "questions": len(method_rows),
            "metrics": {metric: mean(values) for metric, values in sorted(metric_values.items())},
            "mean_latency_ms": mean(row["latency_ms"] for row in method_rows),
            "api_calls": sum(row["api_calls"] for row in method_rows),
            "errors": sum(1 for row in method_rows if row.get("error")),
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "summary.json"
    markdown_path = output_dir / "summary.md"
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return markdown_path, json_path


def _validate_rows(input_path: Path, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[ValidationIssue] = []
    validated_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        method = _validate_string_field(input_path, row, index, "method", issues)
        scores = _validate_scores_field(input_path, row, index, issues)
        latency_ms = _validate_numeric_field(input_path, row, index, "latency_ms", issues)
        api_calls = _validate_integer_field(input_path, row, index, "api_calls", issues)
        if method is None or scores is None or latency_ms is None or api_calls is None:
            continue
        validated_rows.append(
            {
                **row,
                "method": method,
                "scores": scores,
                "latency_ms": latency_ms,
                "api_calls": api_calls,
            }
        )
    if issues:
        raise ValidationError(issues)
    return validated_rows


def _validate_string_field(
    input_path: Path,
    row: dict[str, Any],
    index: int,
    field: str,
    issues: list[ValidationIssue],
) -> str | None:
    value = row.get(field)
    if isinstance(value, str):
        return value
    message = "is required" if field not in row else "must be a string"
    issues.append(ValidationIssue(str(input_path), f"record {index}: {field} {message}"))
    return None


def _validate_scores_field(
    input_path: Path,
    row: dict[str, Any],
    index: int,
    issues: list[ValidationIssue],
) -> dict[str, float] | None:
    if "scores" not in row:
        issues.append(ValidationIssue(str(input_path), f"record {index}: scores is required"))
        return None
    scores = row["scores"]
    if not isinstance(scores, dict):
        issues.append(ValidationIssue(str(input_path), f"record {index}: scores must be an object"))
        return None
    validated_scores: dict[str, float] = {}
    for metric, value in scores.items():
        if not _is_numeric(value):
            issues.append(
                ValidationIssue(
                    str(input_path),
                    f"record {index}: scores.{metric} must be numeric",
                )
            )
            continue
        validated_scores[metric] = float(value)
    return validated_scores


def _validate_numeric_field(
    input_path: Path,
    row: dict[str, Any],
    index: int,
    field: str,
    issues: list[ValidationIssue],
) -> float | None:
    value = row.get(field)
    if _is_numeric(value):
        return float(value)
    message = "is required" if field not in row else "must be numeric"
    issues.append(ValidationIssue(str(input_path), f"record {index}: {field} {message}"))
    return None


def _validate_integer_field(
    input_path: Path,
    row: dict[str, Any],
    index: int,
    field: str,
    issues: list[ValidationIssue],
) -> int | None:
    value = row.get(field)
    if _is_integer_compatible(value):
        return int(value)
    message = "is required" if field not in row else "must be an integer-compatible number"
    issues.append(ValidationIssue(str(input_path), f"record {index}: {field} {message}"))
    return None


def _is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_integer_compatible(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value.is_integer()
    return False


def _render_markdown(summary: dict[str, dict]) -> str:
    lines = ["# DomainRAG-Bench Summary", ""]
    for method, values in sorted(summary.items()):
        lines.append(f"## {method}")
        lines.append("")
        lines.append(f"- Questions: {values['questions']}")
        lines.append(f"- Mean latency ms: {values['mean_latency_ms']:.3f}")
        lines.append(f"- API calls: {values['api_calls']}")
        lines.append(f"- Errors: {values['errors']}")
        for metric, score in sorted(values["metrics"].items()):
            lines.append(f"- {metric}: {score:.4f}")
        lines.append("")
    return "\n".join(lines)
