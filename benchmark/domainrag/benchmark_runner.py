from __future__ import annotations

from pathlib import Path
from time import perf_counter

from domainrag.dataset_adapter import load_split
from domainrag.domain_evaluator import evaluate_record
from domainrag.io_utils import write_jsonl
from domainrag.prompt_renderer import render_prompt
from domainrag.validator import validate_dataset


def run_benchmark(
    dataset_dir: Path,
    output_dir: Path,
    methods: list[str],
    split: str = "dev",
) -> Path:
    validate_dataset(dataset_dir)
    records = load_split(dataset_dir, split)
    output_records: list[dict] = []
    for method in methods:
        for record in records:
            started = perf_counter()
            prompt = render_prompt(record)
            prediction = _predict(method, record)
            latency_ms = (perf_counter() - started) * 1000
            output_records.append(
                {
                    "id": record["id"],
                    "method": method,
                    "split": split,
                    "prompt": prompt,
                    "prediction": prediction,
                    "golden_answers": record["golden_answers"],
                    "scores": evaluate_record(record, prediction),
                    "latency_ms": latency_ms,
                    "input_tokens": len(prompt.split()),
                    "output_tokens": len(prediction.split()),
                    "api_calls": 0,
                    "error": None,
                }
            )
    result_path = output_dir / dataset_dir.name / f"{split}_results.jsonl"
    write_jsonl(result_path, output_records)
    return result_path


def _predict(method: str, record: dict) -> str:
    if method == "no_rag":
        return ""
    if method == "mock_rag":
        return ",".join(record["golden_answers"])
    raise ValueError(f"unsupported method: {method}")
