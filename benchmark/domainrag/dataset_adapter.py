from __future__ import annotations

from pathlib import Path

from domainrag.io_utils import read_jsonl


SPLIT_TO_FILE = {
    "dev": "dev.jsonl",
    "test": "test.jsonl",
    "fresh_hard": "fresh_hard_test.jsonl",
}


def load_split(dataset_dir: Path, split: str) -> list[dict]:
    if split not in SPLIT_TO_FILE:
        raise ValueError(f"unknown split: {split}")
    return read_jsonl(dataset_dir / SPLIT_TO_FILE[split])
