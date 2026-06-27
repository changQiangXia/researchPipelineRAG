from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

from domainrag.io_utils import read_jsonl


def generate_report(input_path: Path, output_dir: Path) -> tuple[Path, Path]:
    rows = read_jsonl(input_path)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)

    summary: dict[str, dict] = {}
    for method, method_rows in grouped.items():
        metric_values: dict[str, list[float]] = defaultdict(list)
        for row in method_rows:
            for metric, value in row["scores"].items():
                metric_values[metric].append(float(value))
        summary[method] = {
            "questions": len(method_rows),
            "metrics": {metric: mean(values) for metric, values in sorted(metric_values.items())},
            "mean_latency_ms": mean(float(row["latency_ms"]) for row in method_rows),
            "api_calls": sum(int(row["api_calls"]) for row in method_rows),
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
