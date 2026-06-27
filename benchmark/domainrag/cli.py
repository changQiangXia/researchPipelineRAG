from __future__ import annotations

import argparse
from pathlib import Path

from domainrag.benchmark_runner import run_benchmark
from domainrag.errors import ValidationError
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
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
