from __future__ import annotations

import argparse
import os
from pathlib import Path

from domainrag.benchmark_runner import run_benchmark
from domainrag.calibration_packet import generate_calibration_packet
from domainrag.comparison_report import generate_comparison_report
from domainrag.deepseek_answer_runner import (
    DeepSeekAnswerConfig,
    run_deepseek_answer_benchmark,
)
from domainrag.deepseek_judge_runner import (
    DeepSeekJudgeConfig,
    generate_judge_report,
    run_deepseek_judge,
)
from domainrag.deepseek_pipeline import DEFAULT_BASE_URL, DEFAULT_MODEL
from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.errors import ValidationError
from domainrag.flashrag_adapter import prepare_flashrag_bundle
from domainrag.flashrag_bm25_bridge import run_flashrag_bm25_bridge
from domainrag.flashrag_method_feasibility import probe_flashrag_method_feasibility
from domainrag.report_generator import generate_report
from domainrag.validator import validate_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="domainrag")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version")
    validate = subparsers.add_parser("validate-data")
    validate.add_argument("--dataset", required=True)
    run = subparsers.add_parser("run")
    run.add_argument("--dataset", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--methods", required=True)
    run.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_deepseek = subparsers.add_parser("run-deepseek-answers")
    run_deepseek.add_argument("--dataset", required=True)
    run_deepseek.add_argument("--output", required=True)
    run_deepseek.add_argument("--methods", required=True)
    run_deepseek.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_deepseek.add_argument("--base-url", default=DEFAULT_BASE_URL)
    run_deepseek.add_argument("--model", default=DEFAULT_MODEL)
    run_deepseek.add_argument("--timeout-seconds", type=int, default=120)
    run_deepseek.add_argument("--max-tokens", type=int, default=4096)
    run_deepseek.add_argument("--temperature", type=float, default=0.0)
    run_deepseek.add_argument("--top-k", type=int, default=5)
    run_deepseek.add_argument("--max-retries", type=int, default=1)
    run_deepseek.add_argument("--limit", type=int, default=None)
    run_deepseek.add_argument("--retrieval-results", default=None)
    judge_deepseek = subparsers.add_parser("judge-deepseek-answers")
    judge_deepseek.add_argument("--dataset", required=True)
    judge_deepseek.add_argument("--input", required=True)
    judge_deepseek.add_argument("--output", required=True)
    judge_deepseek.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    judge_deepseek.add_argument("--base-url", default=DEFAULT_BASE_URL)
    judge_deepseek.add_argument("--model", default=DEFAULT_MODEL)
    judge_deepseek.add_argument("--timeout-seconds", type=int, default=120)
    judge_deepseek.add_argument("--max-tokens", type=int, default=4096)
    judge_deepseek.add_argument("--temperature", type=float, default=0.0)
    judge_deepseek.add_argument("--max-retries", type=int, default=1)
    judge_deepseek.add_argument("--limit", type=int, default=None)
    report = subparsers.add_parser("report")
    report.add_argument("--input", required=True)
    report.add_argument("--output", required=True)
    compare = subparsers.add_parser("compare")
    compare.add_argument("--answer-inputs", nargs="+", required=True)
    compare.add_argument("--judge-inputs", nargs="+", default=[])
    compare.add_argument("--output", required=True)
    calibration_packet = subparsers.add_parser("calibration-packet")
    calibration_packet.add_argument("--dataset", required=True)
    calibration_packet.add_argument("--answers", required=True)
    calibration_packet.add_argument("--judge", required=True)
    calibration_packet.add_argument(
        "--split",
        default="fresh_hard",
        choices=["dev", "test", "fresh_hard"],
    )
    calibration_packet.add_argument("--output", required=True)
    judge_report = subparsers.add_parser("judge-report")
    judge_report.add_argument("--input", required=True)
    judge_report.add_argument("--output", required=True)
    prepare_flashrag = subparsers.add_parser("prepare-flashrag")
    prepare_flashrag.add_argument("--dataset", required=True)
    prepare_flashrag.add_argument("--output", required=True)
    prepare_flashrag.add_argument("--dataset-name", required=True)
    prepare_flashrag.add_argument("--splits", default="dev,test,fresh_hard")
    run_flashrag_bm25 = subparsers.add_parser("run-flashrag-bm25")
    run_flashrag_bm25.add_argument("--flashrag-path", required=True)
    run_flashrag_bm25.add_argument("--dataset-bundle", required=True)
    run_flashrag_bm25.add_argument("--output", required=True)
    run_flashrag_bm25.add_argument("--dataset-name", required=True)
    run_flashrag_bm25.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_flashrag_bm25.add_argument("--top-k", type=int, default=5)
    run_flashrag_bm25.add_argument("--index-dir", default=None)
    run_flashrag_bm25.add_argument("--rebuild-index", action="store_true", default=False)
    probe_flashrag_methods = subparsers.add_parser("probe-flashrag-methods")
    probe_flashrag_methods.add_argument("--flashrag-path", required=True)
    probe_flashrag_methods.add_argument("--output", required=True)
    export_domainrag = subparsers.add_parser("export-domainrag")
    export_domainrag.add_argument("--input", required=True)
    export_domainrag.add_argument("--output", required=True)
    export_domainrag.add_argument("--dataset-name", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        print("domainrag-bench 0.1.0")
        return 0
    if args.command == "validate-data":
        try:
            validate_dataset(Path(args.dataset))
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"{args.dataset} is valid")
        return 0
    if args.command == "run":
        methods = [method.strip() for method in args.methods.split(",") if method.strip()]
        try:
            result_path = run_benchmark(Path(args.dataset), Path(args.output), methods, args.split)
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"results written to {result_path}")
        return 0
    if args.command == "run-deepseek-answers":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("DEEPSEEK_API_KEY is required")
            return 1
        methods = [method.strip() for method in args.methods.split(",") if method.strip()]
        try:
            config = DeepSeekAnswerConfig(
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                top_k=args.top_k,
                max_retries=args.max_retries,
            )
            result_path = run_deepseek_answer_benchmark(
                Path(args.dataset),
                Path(args.output),
                methods,
                args.split,
                config,
                limit=args.limit,
                retrieval_results_path=(
                    Path(args.retrieval_results) if args.retrieval_results else None
                ),
            )
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"DeepSeek answer results written to {result_path}")
        return 0
    if args.command == "judge-deepseek-answers":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("DEEPSEEK_API_KEY is required")
            return 1
        try:
            config = DeepSeekJudgeConfig(
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                max_retries=args.max_retries,
            )
            result_path = run_deepseek_judge(
                Path(args.dataset),
                Path(args.input),
                Path(args.output),
                split=args.split,
                config=config,
                limit=args.limit,
            )
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"DeepSeek judge results written to {result_path}")
        return 0
    if args.command == "report":
        try:
            markdown_path, json_path = generate_report(Path(args.input), Path(args.output))
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"report written to {markdown_path} and {json_path}")
        return 0
    if args.command == "compare":
        try:
            markdown_path, json_path = generate_comparison_report(
                answer_inputs=[Path(path) for path in args.answer_inputs],
                judge_inputs=[Path(path) for path in args.judge_inputs],
                output_dir=Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"comparison report written to {markdown_path} and {json_path}")
        return 0
    if args.command == "calibration-packet":
        try:
            jsonl_path, markdown_path = generate_calibration_packet(
                Path(args.dataset),
                Path(args.answers),
                Path(args.judge),
                Path(args.output),
                split=args.split,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"calibration packet written to {jsonl_path} and {markdown_path}")
        return 0
    if args.command == "judge-report":
        try:
            markdown_path, json_path = generate_judge_report(
                Path(args.input),
                Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"judge report written to {markdown_path} and {json_path}")
        return 0
    if args.command == "prepare-flashrag":
        splits = tuple(split.strip() for split in args.splits.split(",") if split.strip())
        try:
            bundle = prepare_flashrag_bundle(
                Path(args.dataset),
                Path(args.output),
                dataset_name=args.dataset_name,
                splits=splits,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"FlashRAG bundle written to {bundle.dataset_dir}")
        print(f"FlashRAG config written to {bundle.config_path}")
        return 0
    if args.command == "run-flashrag-bm25":
        try:
            result_path = run_flashrag_bm25_bridge(
                Path(args.flashrag_path),
                Path(args.dataset_bundle),
                Path(args.output),
                dataset_name=args.dataset_name,
                split=args.split,
                top_k=args.top_k,
                index_dir=Path(args.index_dir) if args.index_dir else None,
                rebuild_index=args.rebuild_index,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"FlashRAG BM25 results written to {result_path}")
        return 0
    if args.command == "probe-flashrag-methods":
        try:
            probe_flashrag_method_feasibility(
                Path(args.flashrag_path),
                output_path=Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"FlashRAG method feasibility manifest written to {args.output}")
        return 0
    if args.command == "export-domainrag":
        try:
            bundle = export_domainrag_bundle(
                Path(args.input),
                Path(args.output),
                args.dataset_name,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"DomainRAG dataset written to {bundle.dataset_dir}")
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
