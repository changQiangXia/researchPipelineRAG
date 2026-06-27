from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.easy_dataset_adapter import export_domainrag_bundle  # noqa: E402
from domainrag.errors import ValidationError  # noqa: E402


DEFAULT_INPUT = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_expanded"
DEFAULT_OUTPUT = ROOT / "data"
DEFAULT_DATASET_NAME = "real_pilot_nickel_superalloy_expanded"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the expanded real nickel-superalloy DomainRAG pilot dataset.",
    )
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--dataset-name", default=DEFAULT_DATASET_NAME)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        bundle = export_domainrag_bundle(
            Path(args.input),
            Path(args.output),
            args.dataset_name,
        )
    except ValidationError as exc:
        print(str(exc))
        return 1
    print(f"Expanded DomainRAG dataset written to {bundle.dataset_dir}")
    print(f"Statistics written to {bundle.statistics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
