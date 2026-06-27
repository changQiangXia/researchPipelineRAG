from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from domainrag.io_utils import read_jsonl


def generate_comparison_report(
    *,
    answer_inputs: list[Path],
    judge_inputs: list[Path],
    output_dir: Path,
) -> tuple[Path, Path]:
    answer_rows = [row for path in answer_inputs for row in read_jsonl(path)]
    judge_rows = [row for path in judge_inputs for row in read_jsonl(path)]

    method_names = sorted(
        {
            row["method"]
            for row in answer_rows + judge_rows
            if isinstance(row.get("method"), str)
        }
    )
    methods = {
        method: _summarize_method(
            method,
            [row for row in answer_rows if row.get("method") == method],
            [row for row in judge_rows if row.get("method") == method],
        )
        for method in method_names
    }
    leaderboard = sorted(
        [_leaderboard_row(method, values) for method, values in methods.items()],
        key=_leaderboard_sort_key,
    )
    summary = {
        "_metadata": {
            "answer_input_files": [str(path) for path in answer_inputs],
            "judge_input_files": [str(path) for path in judge_inputs],
        },
        "leaderboard": leaderboard,
        "methods": methods,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "summary.json"
    markdown_path = output_dir / "summary.md"
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(summary), encoding="utf-8")
    return markdown_path, json_path


def _summarize_method(
    method: str,
    answer_rows: list[dict[str, Any]],
    judge_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    answer_metrics = _mean_nested_metrics(answer_rows, "scores")
    judge_metrics = _mean_nested_metrics(judge_rows, "judge_scores")
    answer_tokens = _token_totals(answer_rows)
    judge_tokens = _token_totals(judge_rows)
    return {
        "questions": max(len(answer_rows), len(judge_rows)),
        "answer_rows": len(answer_rows),
        "judge_rows": len(judge_rows),
        "answer_metrics": answer_metrics,
        "judge_metrics": judge_metrics,
        "answer_api_calls": _sum_int(answer_rows, "api_calls"),
        "judge_api_calls": _sum_int(judge_rows, "api_calls"),
        "total_api_calls": _sum_int(answer_rows + judge_rows, "api_calls"),
        "answer_errors": sum(1 for row in answer_rows if row.get("error")),
        "judge_errors": sum(1 for row in judge_rows if row.get("error")),
        "unsupported_claims": sum(
            len(row.get("judge", {}).get("unsupported_claims", []))
            for row in judge_rows
            if isinstance(row.get("judge"), dict)
        ),
        "answer_tokens": answer_tokens,
        "judge_tokens": judge_tokens,
        "total_tokens": answer_tokens["total_tokens"] + judge_tokens["total_tokens"],
        "mean_answer_latency_ms": _mean_numeric(answer_rows, "latency_ms"),
        "mean_judge_latency_ms": _mean_numeric(judge_rows, "latency_ms"),
    }


def _mean_nested_metrics(rows: list[dict[str, Any]], field: str) -> dict[str, float]:
    values_by_metric: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        metrics = row.get(field)
        if not isinstance(metrics, dict):
            continue
        for metric, value in metrics.items():
            if _is_number(value):
                values_by_metric[metric].append(float(value))
    return {
        metric: mean(values)
        for metric, values in sorted(values_by_metric.items())
        if values
    }


def _token_totals(rows: list[dict[str, Any]]) -> dict[str, int]:
    input_tokens = _sum_int(rows, "input_tokens")
    output_tokens = _sum_int(rows, "output_tokens")
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def _sum_int(rows: list[dict[str, Any]], field: str) -> int:
    total = 0
    for row in rows:
        value = row.get(field)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            total += value
        elif isinstance(value, float) and value.is_integer():
            total += int(value)
    return total


def _mean_numeric(rows: list[dict[str, Any]], field: str) -> float | None:
    values = [float(row[field]) for row in rows if _is_number(row.get(field))]
    return mean(values) if values else None


def _leaderboard_row(method: str, values: dict[str, Any]) -> dict[str, Any]:
    answer_metrics = values["answer_metrics"]
    judge_metrics = values["judge_metrics"]
    return {
        "method": method,
        "questions": values["questions"],
        "answer_score": _answer_score(answer_metrics),
        "retrieval_hit": answer_metrics.get("retrieval_hit"),
        "retrieval_mrr": answer_metrics.get("retrieval_mrr"),
        "correctness": judge_metrics.get("correctness"),
        "context_support": judge_metrics.get("context_support"),
        "faithfulness": judge_metrics.get("faithfulness"),
        "hallucination_risk": judge_metrics.get("hallucination_risk"),
        "total_api_calls": values["total_api_calls"],
        "total_tokens": values["total_tokens"],
        "errors": values["answer_errors"] + values["judge_errors"],
        "unsupported_claims": values["unsupported_claims"],
    }


def _answer_score(metrics: dict[str, float]) -> float | None:
    values = [
        value
        for metric, value in metrics.items()
        if not metric.startswith("retrieval_")
    ]
    return mean(values) if values else None


def _leaderboard_sort_key(row: dict[str, Any]) -> tuple[float, float, float, float, int, str]:
    return (
        -_none_to_negative(row.get("faithfulness")),
        -_none_to_negative(row.get("correctness")),
        -_none_to_negative(row.get("answer_score")),
        -_none_to_negative(row.get("retrieval_hit")),
        int(row.get("total_api_calls", 0)),
        str(row["method"]),
    )


def _none_to_negative(value: Any) -> float:
    return float(value) if _is_number(value) else -1.0


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# DomainRAG-Bench Comparison",
        "",
        "## Leaderboard",
        "",
        (
            "| method | questions | answer_score | retrieval_hit | correctness | "
            "faithfulness | hallucination_risk | api_calls | errors | unsupported_claims |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["leaderboard"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["method"],
                    str(row["questions"]),
                    _fmt(row["answer_score"]),
                    _fmt(row["retrieval_hit"]),
                    _fmt(row["correctness"]),
                    _fmt(row["faithfulness"]),
                    _fmt(row["hallucination_risk"]),
                    str(row["total_api_calls"]),
                    str(row["errors"]),
                    str(row["unsupported_claims"]),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Method Details")
    lines.append("")
    for method, values in sorted(summary["methods"].items()):
        lines.append(f"### {method}")
        lines.append("")
        lines.append(f"- Questions: {values['questions']}")
        lines.append(f"- Answer API calls: {values['answer_api_calls']}")
        lines.append(f"- Judge API calls: {values['judge_api_calls']}")
        lines.append(f"- Total tokens: {values['total_tokens']}")
        lines.append(f"- Answer errors: {values['answer_errors']}")
        lines.append(f"- Judge errors: {values['judge_errors']}")
        lines.append(f"- Unsupported claims: {values['unsupported_claims']}")
        for metric, value in sorted(values["answer_metrics"].items()):
            lines.append(f"- answer.{metric}: {value:.4f}")
        for metric, value in sorted(values["judge_metrics"].items()):
            lines.append(f"- judge.{metric}: {value:.4f}")
        lines.append("")
    return "\n".join(lines)


def _fmt(value: Any) -> str:
    return "" if value is None else f"{float(value):.4f}"
