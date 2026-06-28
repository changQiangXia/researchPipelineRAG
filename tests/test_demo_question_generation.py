from __future__ import annotations

import json
from pathlib import Path

from domainrag.demo_question_generation import build_demo_question_dataset
from domainrag.validator import validate_dataset
from tests.test_validator import _write_minimal_dataset


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_build_demo_question_dataset_generates_valid_300_question_dataset(tmp_path: Path):
    source = tmp_path / "source"
    output = tmp_path / "data"
    _write_minimal_dataset(source)

    bundle = build_demo_question_dataset(
        source,
        output,
        dataset_name="demo_questions",
        target_questions=300,
    )

    validate_dataset(bundle.dataset_dir)
    canonical = _read_jsonl(bundle.dataset_dir / "canonical_dataset.jsonl")
    statistics = json.loads((bundle.dataset_dir / "statistics.json").read_text())
    dataset_card = (bundle.dataset_dir / "dataset_card.md").read_text(encoding="utf-8")
    dev = _read_jsonl(bundle.dataset_dir / "dev.jsonl")
    test = _read_jsonl(bundle.dataset_dir / "test.jsonl")
    fresh = _read_jsonl(bundle.dataset_dir / "fresh_hard_test.jsonl")

    assert len(canonical) == 300
    assert statistics["question_count"] == 300
    assert statistics["split_counts"] == {
        "dev": 100,
        "fresh_hard": 100,
        "test": 100,
    }
    assert statistics["question_type_counts"] == {
        "fill_blank": 75,
        "multiple_choice": 75,
        "short_answer": 75,
        "single_choice": 75,
    }
    assert len(dev) == 100
    assert len(test) == 100
    assert len(fresh) == 100
    assert {tuple(row["metadata"]["source_chunk_ids"]) for row in dev}.isdisjoint(
        {tuple(row["metadata"]["source_chunk_ids"]) for row in test}
    )
    assert canonical[0]["id"] == "demo_questions_q0001"
    assert canonical[0]["source_chunk_ids"]
    assert canonical[0]["quality_score"] == 0.7
    assert "Provisional demo-question dataset" in dataset_card


def test_build_demo_question_dataset_rejects_out_of_range_question_count(tmp_path: Path):
    source = tmp_path / "source"
    _write_minimal_dataset(source)

    try:
        build_demo_question_dataset(source, tmp_path / "data", target_questions=299)
    except ValueError as exc:
        assert "target_questions must be between 300 and 500" in str(exc)
    else:
        raise AssertionError("expected ValueError")
