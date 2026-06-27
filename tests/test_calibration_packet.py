from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.calibration_packet import generate_calibration_packet
from domainrag.errors import ValidationError
from domainrag.io_utils import write_jsonl
from tests.test_validator import _write_minimal_dataset


def _answer_row(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "id": "q000003",
        "method": "flashrag_bm25_live_deepseek",
        "split": "fresh_hard",
        "prediction": "B",
        "golden_answers": ["B"],
        "gold_context_ids": ["d000003"],
        "retrieved_context_ids": ["d000003", "d000001"],
        "scores": {
            "single_choice_accuracy": 1.0,
            "retrieval_hit": 1.0,
            "retrieval_mrr": 1.0,
            "retrieval_recall": 1.0,
        },
        "api_calls": 1,
        "error": None,
    }
    row.update(overrides)
    return row


def _judge_row(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "id": "q000003",
        "method": "flashrag_bm25_live_deepseek",
        "split": "fresh_hard",
        "prediction": "B",
        "golden_answers": ["B"],
        "gold_context_ids": ["d000003"],
        "retrieved_context_ids": ["d000003", "d000001"],
        "judge": {
            "correctness": 5.0,
            "context_support": 4.0,
            "faithfulness": 4.0,
            "relevance": 5.0,
            "unsupported_claims": ["extra causal mechanism"],
            "reason": "One claim needs human inspection.",
        },
        "judge_scores": {
            "correctness": 5.0,
            "context_support": 4.0,
            "faithfulness": 4.0,
            "relevance": 5.0,
            "hallucination_risk": 1.0,
        },
        "api_calls": 1,
        "error": None,
    }
    row.update(overrides)
    return row


def test_generate_calibration_packet_merges_answers_judges_and_context(tmp_path: Path):
    dataset = tmp_path / "dataset"
    answers = tmp_path / "answers.jsonl"
    judge = tmp_path / "judge.jsonl"
    output = tmp_path / "packet"
    _write_minimal_dataset(dataset)
    write_jsonl(answers, [_answer_row()])
    write_jsonl(judge, [_judge_row()])

    jsonl_path, markdown_path = generate_calibration_packet(
        dataset,
        answers,
        judge,
        output,
        split="fresh_hard",
    )

    rows = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines()]
    markdown = markdown_path.read_text(encoding="utf-8")

    assert jsonl_path == output / "review_packet.jsonl"
    assert markdown_path == output / "review_packet.md"
    assert len(rows) == 1
    row = rows[0]
    assert row["review_id"] == "fresh_hard::flashrag_bm25_live_deepseek::q000003"
    assert row["question_type"] == "single_choice"
    assert row["question"].startswith("Which option is Supported fact three?")
    assert row["prediction"] == "B"
    assert row["golden_answers"] == ["B"]
    assert row["retrieved_context_ids"] == ["d000003", "d000001"]
    assert row["context_chunks"] == [
        {"id": "d000003", "contents": "Topic\nSupported fact three."},
        {"id": "d000001", "contents": "Topic\nSupported fact one."},
    ]
    assert row["judge"]["unsupported_claims"] == ["extra causal mechanism"]
    assert row["priority"] == "high"
    assert row["priority_reasons"] == [
        "unsupported_claims",
        "context_support_below_5",
        "faithfulness_below_5",
        "hallucination_risk_above_0",
    ]
    assert row["human_review"] == {
        "correctness": None,
        "context_support": None,
        "faithfulness": None,
        "decision": None,
        "notes": None,
    }
    assert "flashrag_bm25_live_deepseek" in markdown
    assert "extra causal mechanism" in markdown


def test_generate_calibration_packet_rejects_wrong_answer_split(tmp_path: Path):
    dataset = tmp_path / "dataset"
    answers = tmp_path / "answers.jsonl"
    judge = tmp_path / "judge.jsonl"
    _write_minimal_dataset(dataset)
    write_jsonl(answers, [_answer_row(split="dev")])
    write_jsonl(judge, [_judge_row()])

    with pytest.raises(ValidationError) as exc:
        generate_calibration_packet(
            dataset,
            answers,
            judge,
            tmp_path / "packet",
            split="fresh_hard",
        )

    assert "answer row split must be fresh_hard" in str(exc.value)
