from __future__ import annotations

import json
from pathlib import Path

from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
FULL_OUTPUT = ROOT / "outputs" / "deepseek" / "real_pilot_nickel_superalloy_full"
FULL_DATASET = (
    FULL_OUTPUT
    / "domainrag_candidate"
    / "deepseek_real_pilot_full_candidates"
)


def test_deepseek_full_candidate_audit_and_dataset_are_valid():
    audit_rows = [
        json.loads(line)
        for line in (FULL_OUTPUT / "candidate_audit.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    accepted_rows = [
        json.loads(line)
        for line in (FULL_OUTPUT / "accepted_items.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert len(audit_rows) == 9
    assert len(accepted_rows) == 9
    assert {row["decision"] for row in audit_rows} == {"accepted"}
    assert {row["split"] for row in audit_rows} == {"dev", "test", "fresh_hard"}
    assert {"single_choice", "multiple_choice", "fill_blank", "short_answer"} <= {
        row["question_type"] for row in audit_rows
    }
    validate_dataset(FULL_DATASET)


def test_deepseek_full_candidate_outputs_do_not_store_secret_like_values():
    output_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FULL_OUTPUT.rglob("*")
        if path.is_file()
    )

    assert "sk-" not in output_text
    assert "ghp_" not in output_text
