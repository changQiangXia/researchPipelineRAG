from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from domainrag.io_utils import read_jsonl
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_expanded"
SOURCES = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure_expanded"
    / "sources.jsonl"
)


def test_expanded_fixture_has_medium_pilot_shape_and_source_coverage():
    chunks = read_jsonl(FIXTURE / "chunks.jsonl")
    items = read_jsonl(FIXTURE / "items.jsonl")
    sources = read_jsonl(SOURCES)
    covered_chunk_ids = {
        chunk_id
        for source in sources
        for chunk_id in source.get("used_for_chunk_ids", [])
    }

    assert len(chunks) == 17
    assert len(items) == 24
    assert {item["split"] for item in items} == {"dev", "test", "fresh_hard"}
    assert {split: sum(1 for item in items if item["split"] == split) for split in ["dev", "test", "fresh_hard"]} == {
        "dev": 8,
        "test": 8,
        "fresh_hard": 8,
    }
    assert {chunk["id"] for chunk in chunks} <= covered_chunk_ids
    assert len(sources) >= 15


def test_build_real_pilot_expanded_script_writes_valid_dataset(tmp_path: Path):
    dataset_name = "unit_real_pilot_expanded"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_real_pilot_expanded.py",
            "--output",
            str(tmp_path),
            "--dataset-name",
            dataset_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    dataset_dir = tmp_path / dataset_name
    validate_dataset(dataset_dir)
    statistics = json.loads((dataset_dir / "statistics.json").read_text(encoding="utf-8"))
    assert statistics["corpus_count"] == 17
    assert statistics["question_count"] == 24
    assert statistics["split_counts"] == {
        "dev": 8,
        "fresh_hard": 8,
        "test": 8,
    }
    assert statistics["question_type_counts"] == {
        "fill_blank": 6,
        "multiple_choice": 6,
        "short_answer": 6,
        "single_choice": 6,
    }
