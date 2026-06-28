from __future__ import annotations

from collections import Counter
import json
import subprocess
import sys
from pathlib import Path

from domainrag.io_utils import read_jsonl
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_medium_plus"
SOURCES = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure_medium_plus"
    / "sources.jsonl"
)


def test_medium_plus_fixture_has_scaled_shape_and_source_coverage():
    chunks = read_jsonl(FIXTURE / "chunks.jsonl")
    items = read_jsonl(FIXTURE / "items.jsonl")
    sources = read_jsonl(SOURCES)
    chunk_ids = {chunk["id"] for chunk in chunks}
    covered_chunk_ids = {
        chunk_id
        for source in sources
        for chunk_id in source.get("used_for_chunk_ids", [])
    }
    split_counts = Counter(item["split"] for item in items)
    type_counts = Counter(item["question_type"] for item in items)

    assert len(chunks) == 100
    assert len(items) == 150
    assert len(sources) >= 32
    assert chunk_ids <= covered_chunk_ids
    assert split_counts == {
        "dev": 50,
        "test": 50,
        "fresh_hard": 50,
    }
    assert type_counts == {
        "single_choice": 38,
        "multiple_choice": 38,
        "fill_blank": 37,
        "short_answer": 37,
    }
    assert sum(1 for item in items if len(item["source_chunk_ids"]) >= 2) >= 45
    assert sum(
        1
        for item in items
        if item["split"] == "fresh_hard" and len(item["source_chunk_ids"]) >= 2
    ) >= 30
    assert len(
        {
            (
                item["split"],
                item["question"],
                tuple(item["source_chunk_ids"]),
            )
            for item in items
        }
    ) == len(items)


def test_build_real_pilot_medium_plus_script_writes_valid_dataset(tmp_path: Path):
    dataset_name = "unit_real_pilot_medium_plus"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_real_pilot_medium_plus.py",
            "--fixture-output",
            str(tmp_path / "fixture"),
            "--source-output",
            str(tmp_path / "sources"),
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
    assert statistics["corpus_count"] == 100
    assert statistics["question_count"] == 150
    assert statistics["split_counts"] == {
        "dev": 50,
        "fresh_hard": 50,
        "test": 50,
    }
    assert statistics["question_type_counts"] == {
        "fill_blank": 37,
        "multiple_choice": 38,
        "short_answer": 37,
        "single_choice": 38,
    }
