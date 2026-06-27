from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.errors import ValidationError  # noqa: E402
from domainrag.flashrag_runtime_intake import verify_flashrag_runtime_intake  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify that an actual FlashRAG checkout can load a DomainRAG FlashRAG bundle.",
    )
    parser.add_argument("--flashrag-path", required=True)
    parser.add_argument("--dataset-bundle", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--splits", default="dev,test,fresh_hard")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    splits = tuple(split.strip() for split in args.splits.split(",") if split.strip())
    try:
        manifest = verify_flashrag_runtime_intake(
            Path(args.flashrag_path),
            Path(args.dataset_bundle),
            dataset_name=args.dataset_name,
            splits=splits,
            output_path=Path(args.output),
        )
    except ValidationError as exc:
        print(str(exc))
        return 1

    print(f"FlashRAG runtime intake manifest written to {args.output}")
    for split, summary in manifest["splits"].items():
        print(f"{split}: {summary['records']} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
