from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "real_pilot_nickel_superalloy_medium_plus"
DATASET_NAME = DATASET.name
DEFAULT_OUTPUT = (
    ROOT
    / "outputs"
    / "archive"
    / "provenance"
    / "expanded-pilots"
    / "medium-plus-live-subset"
    / "medium_plus_live_subset"
)
DEFAULT_RETRIEVAL_RESULTS = (
    ROOT
    / "outputs"
    / "archive"
    / "provenance"
    / "expanded-pilots"
    / "medium-plus-baseline-and-bm25"
    / "medium_plus_bm25s"
    / DATASET_NAME
    / "fresh_hard_bm25s_results.jsonl"
)
DEFAULT_METHODS = "no_rag,lexical_rag,flashrag_bm25_live_deepseek"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the bounded Phase 7C live DeepSeek answer/Judge subset on the "
            "medium-plus Fresh-Hard split."
        ),
    )
    parser.add_argument("--dataset", default=str(DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--retrieval-results", default=str(DEFAULT_RETRIEVAL_RESULTS))
    parser.add_argument("--methods", default=DEFAULT_METHODS)
    parser.add_argument("--split", default="fresh_hard", choices=["dev", "test", "fresh_hard"])
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--model", default="deepseek-v4-pro")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-retries", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", default=False)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = Path(args.output)
    answer_output = output / "answers"
    judge_output = output / "judge"
    judge_report_output = output / "judge_report"
    comparison_output = output / "comparison"
    answer_path = answer_output / Path(args.dataset).name / f"{args.split}_deepseek_results.jsonl"
    judge_path = judge_output / Path(args.dataset).name / f"{args.split}_judge_results.jsonl"

    commands = [
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "run-deepseek-answers",
            "--dataset",
            args.dataset,
            "--output",
            str(answer_output),
            "--methods",
            args.methods,
            "--split",
            args.split,
            "--model",
            args.model,
            "--top-k",
            str(args.top_k),
            "--max-retries",
            str(args.max_retries),
            "--limit",
            str(args.limit),
            "--retrieval-results",
            args.retrieval_results,
        ],
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "judge-deepseek-answers",
            "--dataset",
            args.dataset,
            "--input",
            str(answer_path),
            "--output",
            str(judge_output),
            "--split",
            args.split,
            "--model",
            args.model,
            "--max-retries",
            str(args.max_retries),
        ],
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "judge-report",
            "--input",
            str(judge_path),
            "--output",
            str(judge_report_output),
        ],
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "compare",
            "--answer-inputs",
            str(answer_path),
            "--judge-inputs",
            str(judge_path),
            "--output",
            str(comparison_output),
        ],
    ]

    if args.dry_run:
        for command in commands:
            print("PYTHONPATH=benchmark " + shlex.join(_display_command(command)))
        return 0

    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("DEEPSEEK_API_KEY is required")
        return 1

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    benchmark_path = str(ROOT / "benchmark")
    env["PYTHONPATH"] = (
        benchmark_path
        if not existing_pythonpath
        else f"{benchmark_path}{os.pathsep}{existing_pythonpath}"
    )
    for command in commands:
        subprocess.run(command, cwd=ROOT, env=env, check=True)
    print(f"Phase 7C live subset written to {output}")
    return 0


def _display_command(command: list[str]) -> list[str]:
    return ["python" if item == sys.executable else item for item in command]


if __name__ == "__main__":
    raise SystemExit(main())
