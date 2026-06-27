from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.flashrag_adapter import prepare_flashrag_bundle


def main() -> None:
    os.chdir(ROOT)
    bundle = prepare_flashrag_bundle(
        Path("data") / "example_domain",
        Path("outputs") / "flashrag",
        dataset_name="example_domain",
    )
    print(f"FlashRAG bundle written to {bundle.dataset_dir}")
    print(f"FlashRAG config written to {bundle.config_path}")


if __name__ == "__main__":
    main()
