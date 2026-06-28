from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl, write_jsonl


METRICS = ("correctness", "context_support", "faithfulness")


def generate_calibration_audit(
    packet_path: Path,
    labels_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    packet_rows = read_jsonl(packet_path)
    label_rows = read_jsonl(labels_path)
    indexed_packet = _index_packet_rows(packet_rows, packet_path)
    reviewed_rows = _merge_reviewed_rows(label_rows, indexed_packet, labels_path)
    summary = _summarize_audit(
        reviewed_rows,
        packet_path=packet_path,
        labels_path=labels_path,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    reviewed_path = output_dir / "reviewed_rows.jsonl"
    json_path = output_dir / "summary.json"
    markdown_path = output_dir / "summary.md"
    write_jsonl(reviewed_path, reviewed_rows)
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return markdown_path, json_path


def _index_packet_rows(rows: list[dict[str, Any]], path: Path) -> dict[str, dict[str, Any]]:
    issues: list[ValidationIssue] = []
    indexed: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows, start=1):
        review_id = row.get("review_id")
        if not isinstance(review_id, str) or not review_id:
            issues.append(ValidationIssue(str(path), f"record {index}: review_id must be a string"))
            continue
        if review_id in indexed:
            issues.append(
                ValidationIssue(str(path), f"record {index}: duplicate review_id {review_id}")
            )
            continue
        indexed[review_id] = row
    if issues:
        raise ValidationError(issues)
    return indexed


def _merge_reviewed_rows(
    label_rows: list[dict[str, Any]],
    indexed_packet: dict[str, dict[str, Any]],
    labels_path: Path,
) -> list[dict[str, Any]]:
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    reviewed_rows: list[dict[str, Any]] = []
    for index, label_row in enumerate(label_rows, start=1):
        review_id = label_row.get("review_id")
        if not isinstance(review_id, str) or not review_id:
            issues.append(
                ValidationIssue(str(labels_path), f"record {index}: review_id must be a string")
            )
            continue
        if review_id in seen:
            issues.append(
                ValidationIssue(str(labels_path), f"record {index}: duplicate review_id {review_id}")
            )
            continue
        seen.add(review_id)
        packet_row = indexed_packet.get(review_id)
        if packet_row is None:
            issues.append(
                ValidationIssue(str(labels_path), f"record {index}: unknown review_id {review_id}")
            )
            continue
        human_review = _validate_human_review(label_row, labels_path, index, issues)
        judge_scores = packet_row.get("judge_scores")
        if not isinstance(judge_scores, dict):
            issues.append(
                ValidationIssue(str(labels_path), f"record {index}: packet judge_scores must be an object")
            )
            continue
        deltas = _metric_deltas(human_review, judge_scores, labels_path, index, issues)
        if human_review is None or deltas is None:
            continue
        reviewed_rows.append(
            {
                **packet_row,
                "human_review": human_review,
                "judge_human_abs_delta": deltas,
            }
        )
    if not label_rows:
        issues.append(ValidationIssue(str(labels_path), "at least one human label is required"))
    if issues:
        raise ValidationError(issues)
    return reviewed_rows


def _validate_human_review(
    label_row: dict[str, Any],
    labels_path: Path,
    index: int,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    review = label_row.get("human_review")
    if not isinstance(review, dict):
        issues.append(
            ValidationIssue(str(labels_path), f"record {index}: human_review must be an object")
        )
        return None
    normalized: dict[str, Any] = {}
    for metric in METRICS:
        value = review.get(metric)
        if not _is_number(value) or not 0.0 <= float(value) <= 5.0:
            issues.append(
                ValidationIssue(
                    str(labels_path),
                    f"record {index}: human_review.{metric} must be 0..5",
                )
            )
            continue
        normalized[metric] = float(value)
    decision = review.get("decision")
    if not isinstance(decision, str) or not decision:
        issues.append(
            ValidationIssue(
                str(labels_path),
                f"record {index}: human_review.decision must be a non-empty string",
            )
        )
    else:
        normalized["decision"] = decision
    notes = review.get("notes")
    if notes is None:
        normalized["notes"] = ""
    elif isinstance(notes, str):
        normalized["notes"] = notes
    else:
        issues.append(
            ValidationIssue(str(labels_path), f"record {index}: human_review.notes must be a string")
        )
    if any(metric not in normalized for metric in METRICS) or "decision" not in normalized:
        return None
    return normalized


def _metric_deltas(
    human_review: dict[str, Any] | None,
    judge_scores: dict[str, Any],
    labels_path: Path,
    index: int,
    issues: list[ValidationIssue],
) -> dict[str, float] | None:
    if human_review is None:
        return None
    deltas: dict[str, float] = {}
    for metric in METRICS:
        judge_value = judge_scores.get(metric)
        if not _is_number(judge_value):
            issues.append(
                ValidationIssue(
                    str(labels_path),
                    f"record {index}: packet judge_scores.{metric} must be numeric",
                )
            )
            continue
        deltas[metric] = abs(float(human_review[metric]) - float(judge_value))
    if len(deltas) != len(METRICS):
        return None
    return deltas


def _summarize_audit(
    rows: list[dict[str, Any]],
    *,
    packet_path: Path,
    labels_path: Path,
) -> dict[str, Any]:
    methods = sorted({str(row.get("method")) for row in rows if isinstance(row.get("method"), str)})
    summary = {
        "_metadata": {
            "packet_file": str(packet_path),
            "labels_file": str(labels_path),
        },
        "reviewed_rows": len(rows),
        "priority_rows": sum(1 for row in rows if row.get("priority") == "high"),
        "unsupported_claim_rows": sum(1 for row in rows if _has_unsupported_claims(row)),
        "decisions": dict(sorted(Counter(_decision(row) for row in rows).items())),
        "overall": _summarize_rows(rows),
        "methods": {
            method: _summarize_rows([row for row in rows if row.get("method") == method])
            for method in methods
        },
        "disagreements": _disagreements(rows),
    }
    return summary


def _summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    agreement_within_1 = {
        metric: sum(1 for row in rows if row["judge_human_abs_delta"][metric] <= 1.0)
        for metric in METRICS
    }
    return {
        "reviewed_rows": len(rows),
        "human_metrics": {
            metric: _mean_metric(rows, "human_review", metric)
            for metric in METRICS
        },
        "judge_metrics": {
            metric: _mean_metric(rows, "judge_scores", metric)
            for metric in METRICS
        },
        "mean_abs_delta": {
            metric: mean(row["judge_human_abs_delta"][metric] for row in rows) if rows else None
            for metric in METRICS
        },
        "agreement_within_1": agreement_within_1,
        "agreement_rate_within_1": {
            metric: (agreement_within_1[metric] / len(rows)) if rows else None
            for metric in METRICS
        },
    }


def _mean_metric(rows: list[dict[str, Any]], field: str, metric: str) -> float | None:
    values = [
        float(row[field][metric])
        for row in rows
        if isinstance(row.get(field), dict) and _is_number(row[field].get(metric))
    ]
    return mean(values) if values else None


def _disagreements(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    disagreements: list[dict[str, Any]] = []
    for row in rows:
        for metric in METRICS:
            delta = row["judge_human_abs_delta"][metric]
            if delta <= 1.0:
                continue
            disagreements.append(
                {
                    "review_id": row["review_id"],
                    "method": row["method"],
                    "metric": metric,
                    "human": float(row["human_review"][metric]),
                    "judge": float(row["judge_scores"][metric]),
                    "abs_delta": delta,
                    "question": row.get("question", ""),
                }
            )
    return sorted(
        disagreements,
        key=lambda item: (str(item["review_id"]), str(item["metric"])),
    )


def _has_unsupported_claims(row: dict[str, Any]) -> bool:
    judge = row.get("judge")
    if not isinstance(judge, dict):
        return False
    unsupported_claims = judge.get("unsupported_claims")
    return isinstance(unsupported_claims, list) and bool(unsupported_claims)


def _decision(row: dict[str, Any]) -> str:
    review = row.get("human_review")
    if isinstance(review, dict) and isinstance(review.get("decision"), str):
        return review["decision"]
    return "unknown"


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# DomainRAG Human Calibration Audit",
        "",
        f"Reviewed rows: {summary['reviewed_rows']}",
        f"Priority rows: {summary['priority_rows']}",
        f"Rows with judge unsupported claims: {summary['unsupported_claim_rows']}",
        "",
        "## Overall",
        "",
        _metric_line("Human", summary["overall"]["human_metrics"]),
        _metric_line("Judge", summary["overall"]["judge_metrics"]),
        _metric_line("Mean absolute delta", summary["overall"]["mean_abs_delta"]),
        "",
        "## Methods",
        "",
        (
            "| method | reviewed_rows | human_correctness | human_context_support | "
            "human_faithfulness | judge_correctness | judge_context_support | judge_faithfulness |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for method, values in sorted(summary["methods"].items()):
        lines.append(
            "| "
            + " | ".join(
                [
                    method,
                    str(values["reviewed_rows"]),
                    _fmt(values["human_metrics"]["correctness"]),
                    _fmt(values["human_metrics"]["context_support"]),
                    _fmt(values["human_metrics"]["faithfulness"]),
                    _fmt(values["judge_metrics"]["correctness"]),
                    _fmt(values["judge_metrics"]["context_support"]),
                    _fmt(values["judge_metrics"]["faithfulness"]),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Decisions", ""])
    for decision, count in summary["decisions"].items():
        lines.append(f"- {decision}: {count}")
    lines.extend(["", "## Disagreements", ""])
    if not summary["disagreements"]:
        lines.append("No metric deltas exceeded 1 point.")
    for item in summary["disagreements"]:
        lines.append(
            "- "
            f"{item['review_id']} {item['metric']}: "
            f"human={_fmt(item['human'])}, judge={_fmt(item['judge'])}, "
            f"abs_delta={_fmt(item['abs_delta'])}"
        )
    lines.append("")
    return "\n".join(lines)


def _metric_line(label: str, metrics: dict[str, Any]) -> str:
    return (
        f"- {label}: "
        f"correctness={_fmt(metrics['correctness'])}, "
        f"context_support={_fmt(metrics['context_support'])}, "
        f"faithfulness={_fmt(metrics['faithfulness'])}"
    )


def _fmt(value: Any) -> str:
    return "" if value is None else f"{float(value):.4f}"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
