from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.easy_dataset_adapter import export_domainrag_bundle


def main() -> int:
    os.chdir(ROOT)
    bundle = export_domainrag_bundle(
        Path("fixtures") / "easy_dataset" / "example_export",
        Path("outputs") / "domainrag",
        "example_easy_dataset",
    )
    print(f"DomainRAG dataset written to {bundle.dataset_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
