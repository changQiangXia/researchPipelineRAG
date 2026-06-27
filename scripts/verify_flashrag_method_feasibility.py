from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.errors import ValidationError  # noqa: E402
from domainrag.flashrag_method_feasibility import (  # noqa: E402
    probe_flashrag_method_feasibility,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Probe which FlashRAG method families are feasible in this Python runtime.",
    )
    parser.add_argument("--flashrag-path", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = probe_flashrag_method_feasibility(
            Path(args.flashrag_path),
            output_path=Path(args.output),
        )
    except ValidationError as exc:
        print(str(exc))
        return 1

    print(f"FlashRAG method feasibility manifest written to {args.output}")
    for method, summary in manifest["methods"].items():
        print(f"{method}: feasible={summary['feasible']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
