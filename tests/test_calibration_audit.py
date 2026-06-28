from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.io_utils import write_jsonl


def _load_audit_generator():
    try:
        from domainrag.calibration_audit import generate_calibration_audit
    except ModuleNotFoundError:
        pytest.fail("domainrag.calibration_audit.generate_calibration_audit should be importable")
    return generate_calibration_audit


def _packet_row(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "review_id": "fresh_hard::no_rag::q1",
        "id": "q1",
        "method": "no_rag",
        "split": "fresh_hard",
        "question": "Which mechanism is supported?",
        "prediction": "Gamma prime rafting is always beneficial.",
        "golden_answers": ["Rafting can be beneficial or harmful depending on stress state."],
        "retrieved_context_ids": [],
        "context_chunks": [],
        "judge_scores": {
            "correctness": 2.0,
            "context_support": 0.0,
            "faithfulness": 1.0,
            "hallucination_risk": 4.0,
        },
        "judge": {
            "unsupported_claims": ["always beneficial"],
            "reason": "The answer overgeneralizes the mechanism.",
        },
        "priority": "high",
        "priority_reasons": ["unsupported_claims", "context_support_below_5"],
    }
    row.update(overrides)
    return row


def _label_row(review_id: str, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "review_id": review_id,
        "human_review": {
            "correctness": 3.0,
            "context_support": 0.0,
            "faithfulness": 2.0,
            "decision": "mostly_agree_with_judge",
            "notes": "The answer is partly correct but unsupported without retrieved context.",
        },
    }
    row.update(overrides)
    return row


def test_generate_calibration_audit_summarizes_human_judge_agreement(tmp_path: Path):
    generate_calibration_audit = _load_audit_generator()
    packet = tmp_path / "review_packet.jsonl"
    labels = tmp_path / "human_labels.jsonl"
    output = tmp_path / "audit"
    write_jsonl(
        packet,
        [
            _packet_row(),
            _packet_row(
                review_id="fresh_hard::oracle_context::q2",
                id="q2",
                method="oracle_context",
                judge_scores={"correctness": 5.0, "context_support": 5.0, "faithfulness": 5.0},
                judge={"unsupported_claims": [], "reason": "Fully supported."},
                priority="normal",
                priority_reasons=[],
            ),
            _packet_row(
                review_id="fresh_hard::lexical_rag::q3",
                id="q3",
                method="lexical_rag",
                judge_scores={"correctness": 5.0, "context_support": 5.0, "faithfulness": 5.0},
                judge={"unsupported_claims": [], "reason": "Judge missed the gap."},
                priority="high",
                priority_reasons=["faithfulness_below_5"],
            ),
        ],
    )
    write_jsonl(
        labels,
        [
            _label_row("fresh_hard::no_rag::q1"),
            _label_row(
                "fresh_hard::oracle_context::q2",
                human_review={
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 5.0,
                    "decision": "agree_with_judge",
                    "notes": "Control row is fully supported.",
                },
            ),
            _label_row(
                "fresh_hard::lexical_rag::q3",
                human_review={
                    "correctness": 3.0,
                    "context_support": 2.0,
                    "faithfulness": 3.0,
                    "decision": "disagree_with_judge",
                    "notes": "Retrieved context misses one required support point.",
                },
            ),
        ],
    )

    markdown_path, json_path = generate_calibration_audit(packet, labels, output)

    summary = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert markdown_path == output / "summary.md"
    assert json_path == output / "summary.json"
    assert summary["reviewed_rows"] == 3
    assert summary["priority_rows"] == 2
    assert summary["unsupported_claim_rows"] == 1
    assert summary["overall"]["human_metrics"]["correctness"] == pytest.approx(3.6667, abs=1e-4)
    assert summary["overall"]["judge_metrics"]["correctness"] == pytest.approx(4.0)
    assert summary["overall"]["mean_abs_delta"]["correctness"] == pytest.approx(1.0)
    assert summary["overall"]["agreement_within_1"]["correctness"] == 2
    assert summary["overall"]["agreement_rate_within_1"]["faithfulness"] == pytest.approx(2 / 3)
    assert summary["methods"]["no_rag"]["reviewed_rows"] == 1
    assert summary["methods"]["oracle_context"]["human_metrics"]["faithfulness"] == 5.0
    assert summary["decisions"]["disagree_with_judge"] == 1
    assert summary["disagreements"] == [
        {
            "review_id": "fresh_hard::lexical_rag::q3",
            "method": "lexical_rag",
            "metric": "context_support",
            "human": 2.0,
            "judge": 5.0,
            "abs_delta": 3.0,
            "question": "Which mechanism is supported?",
        },
        {
            "review_id": "fresh_hard::lexical_rag::q3",
            "method": "lexical_rag",
            "metric": "correctness",
            "human": 3.0,
            "judge": 5.0,
            "abs_delta": 2.0,
            "question": "Which mechanism is supported?",
        },
        {
            "review_id": "fresh_hard::lexical_rag::q3",
            "method": "lexical_rag",
            "metric": "faithfulness",
            "human": 3.0,
            "judge": 5.0,
            "abs_delta": 2.0,
            "question": "Which mechanism is supported?",
        },
    ]
    assert "| lexical_rag | 1 |" in markdown
    assert "fresh_hard::lexical_rag::q3" in markdown


def test_generate_calibration_audit_rejects_unknown_review_id(tmp_path: Path):
    generate_calibration_audit = _load_audit_generator()
    packet = tmp_path / "review_packet.jsonl"
    labels = tmp_path / "human_labels.jsonl"
    write_jsonl(packet, [_packet_row()])
    write_jsonl(labels, [_label_row("fresh_hard::no_rag::missing")])

    with pytest.raises(ValidationError) as exc:
        generate_calibration_audit(packet, labels, tmp_path / "audit")

    assert "unknown review_id fresh_hard::no_rag::missing" in str(exc.value)


def test_generate_calibration_audit_rejects_invalid_human_score(tmp_path: Path):
    generate_calibration_audit = _load_audit_generator()
    packet = tmp_path / "review_packet.jsonl"
    labels = tmp_path / "human_labels.jsonl"
    write_jsonl(packet, [_packet_row()])
    write_jsonl(
        labels,
        [
            _label_row(
                "fresh_hard::no_rag::q1",
                human_review={
                    "correctness": 6.0,
                    "context_support": 0.0,
                    "faithfulness": 2.0,
                    "decision": "mostly_agree_with_judge",
                    "notes": "Out of range.",
                },
            )
        ],
    )

    with pytest.raises(ValidationError) as exc:
        generate_calibration_audit(packet, labels, tmp_path / "audit")

    assert "human_review.correctness must be 0..5" in str(exc.value)
