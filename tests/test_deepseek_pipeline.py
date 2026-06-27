from __future__ import annotations

import pytest

from domainrag.deepseek_pipeline import (
    build_generation_messages,
    build_review_messages,
    normalize_generated_item,
    normalize_review_result,
    parse_json_object,
)
from domainrag.errors import ValidationError


CHUNK = {
    "id": "ns_ht_oxidation_gb_energy_001",
    "content": (
        "Initial oxidation in Inconel 718 can depend on grain-boundary character. "
        "Boundaries with different energy states can change oxygen adsorption, diffusion, "
        "and oxide nucleation."
    ),
}


def test_build_generation_messages_keep_source_identity_out_of_prompt():
    messages = build_generation_messages(CHUNK, split="dev", question_type="single_choice")
    combined = "\n".join(message["content"] for message in messages)

    assert "ns_ht_oxidation_gb_energy_001" in combined
    assert "Inconel 718" in combined
    assert "DOI" in combined
    assert "author" in combined.lower()
    assert "http" not in combined.lower()
    assert "paper title" not in combined.lower()
    assert "options must be an object, not an array" in combined
    assert '"answer": ["A"]' in combined


def test_parse_json_object_accepts_plain_and_fenced_json():
    assert parse_json_object('{"accepted": true}') == {"accepted": True}
    assert parse_json_object('```json\n{"accepted": false}\n```') == {"accepted": False}


def test_normalize_generated_item_accepts_contract_item():
    raw = {
        "id": "ds_ns_ht_q001",
        "split": "dev",
        "question_type": "single_choice",
        "question": "Which factor can affect initial oxidation across grain boundaries?",
        "options": {
            "A": "Grain-boundary energy state",
            "B": "Output directory name",
            "C": "Dataset card order",
            "D": "Command-line shell",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Grain-boundary energy state can affect initial oxidation.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_oxidation_gb_energy_001"],
        "subdomain": "oxidation",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    }

    item = normalize_generated_item(
        raw,
        chunk_id="ns_ht_oxidation_gb_energy_001",
        split="dev",
        question_type="single_choice",
    )

    assert item == raw


def test_normalize_generated_item_rejects_wrong_chunk_and_source_identity_words():
    raw = {
        "id": "ds_ns_ht_q001",
        "split": "dev",
        "question_type": "single_choice",
        "question": "According to this paper, what changes oxidation?",
        "options": {"A": "x", "B": "y", "C": "z", "D": "w"},
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "x",
        "required_points": [],
        "source_chunk_ids": ["other_chunk"],
        "subdomain": "oxidation",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    }

    with pytest.raises(ValidationError) as exc:
        normalize_generated_item(
            raw,
            chunk_id="ns_ht_oxidation_gb_energy_001",
            split="dev",
            question_type="single_choice",
        )

    assert "source_chunk_ids must exactly match" in str(exc.value)
    assert "question contains forbidden source-identity phrase" in str(exc.value)


def test_normalize_generated_item_rejects_choice_option_arrays_and_context_phrasing():
    raw = {
        "id": "ds_ns_ht_q001",
        "split": "dev",
        "question_type": "single_choice",
        "question": "According to the provided information, what changes oxidation?",
        "options": ["Grain-boundary energy", "Temperature", "Prompt length", "File order"],
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Grain-boundary energy",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_oxidation_gb_energy_001"],
        "subdomain": "oxidation",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    }

    with pytest.raises(ValidationError) as exc:
        normalize_generated_item(
            raw,
            chunk_id="ns_ht_oxidation_gb_energy_001",
            split="dev",
            question_type="single_choice",
        )

    assert "single_choice requires A-D options object" in str(exc.value)
    assert "provided information" in str(exc.value)


def test_build_review_messages_include_independent_quality_gate():
    item = {
        "id": "ds_ns_ht_q001",
        "split": "dev",
        "question_type": "fill_blank",
        "question": "Grain-boundary energy can affect oxygen ____.",
        "options": {},
        "answer": ["diffusion"],
        "answer_aliases": ["oxygen diffusion"],
        "reference_answer": "diffusion",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_oxidation_gb_energy_001"],
        "subdomain": "oxidation",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    }

    messages = build_review_messages(CHUNK, item)
    combined = "\n".join(message["content"] for message in messages)

    assert "accepted" in combined
    assert "quality_score" in combined
    assert "corrected_item" in combined
    assert "0.85" in combined


def test_normalize_review_result_accepts_review_schema():
    raw = {
        "accepted": True,
        "quality_score": 0.91,
        "problems": [],
        "corrected_item": {},
    }

    assert normalize_review_result(raw) == raw


def test_normalize_review_result_rejects_bad_quality_score():
    with pytest.raises(ValidationError) as exc:
        normalize_review_result(
            {
                "accepted": True,
                "quality_score": "high",
                "problems": [],
                "corrected_item": {},
            }
        )

    assert "quality_score must be numeric" in str(exc.value)
