from __future__ import annotations

import argparse
from pathlib import Path

from domainrag.benchmark_runner import run_benchmark
from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.errors import ValidationError
from domainrag.flashrag_adapter import prepare_flashrag_bundle
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
    report = subparsers.add_parser("report")
    report.add_argument("--input", required=True)
    report.add_argument("--output", required=True)
    prepare_flashrag = subparsers.add_parser("prepare-flashrag")
    prepare_flashrag.add_argument("--dataset", required=True)
    prepare_flashrag.add_argument("--output", required=True)
    prepare_flashrag.add_argument("--dataset-name", required=True)
    prepare_flashrag.add_argument("--splits", default="dev,test,fresh_hard")
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
    if args.command == "report":
        try:
            markdown_path, json_path = generate_report(Path(args.input), Path(args.output))
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"report written to {markdown_path} and {json_path}")
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
