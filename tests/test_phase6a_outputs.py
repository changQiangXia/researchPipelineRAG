from __future__ import annotations

import json
from pathlib import Path

from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "real_pilot_nickel_superalloy_expanded"
FLASHRAG = ROOT / "outputs" / "flashrag" / "real_pilot_nickel_superalloy_expanded"
BASELINE = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "expanded-baseline" / "expanded_baseline"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase6a_expanded_dataset_is_valid_and_medium_sized():
    validate_dataset(DATASET)
    statistics = json.loads((DATASET / "statistics.json").read_text(encoding="utf-8"))

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


def test_phase6a_expanded_flashrag_bundle_exists_for_all_splits():
    assert len(_read_jsonl(FLASHRAG / "dev.jsonl")) == 8
    assert len(_read_jsonl(FLASHRAG / "test.jsonl")) == 8
    assert len(_read_jsonl(FLASHRAG / "fresh_hard.jsonl")) == 8
    assert len(_read_jsonl(FLASHRAG / "corpus.jsonl")) == 17
    assert (FLASHRAG / "qrels" / "fresh_hard.tsv").exists()


def test_phase6a_expanded_fresh_hard_baseline_contains_real_methods():
    result_path = BASELINE / "real_pilot_nickel_superalloy_expanded" / "fresh_hard_results.jsonl"
    rows = _read_jsonl(result_path)

    assert len(rows) == 24
    assert {row["method"] for row in rows} == {
        "no_rag",
        "oracle_context",
        "lexical_rag",
    }
    assert {row["split"] for row in rows} == {"fresh_hard"}
    lexical = [row for row in rows if row["method"] == "lexical_rag"]
    assert len(lexical) == 8
    assert sum(row["scores"]["retrieval_hit"] for row in lexical) >= 7.0


def test_phase6a_expanded_fresh_hard_report_summarizes_baseline():
    summary = json.loads((BASELINE / "report_fresh_hard" / "summary.json").read_text(encoding="utf-8"))
    markdown = (BASELINE / "report_fresh_hard" / "summary.md").read_text(encoding="utf-8")

    assert summary["_diagnostics"]["fresh_hard_candidates"] == 6
    assert summary["no_rag"]["questions"] == 8
    assert summary["oracle_context"]["metrics"]["retrieval_hit"] == 1.0
    assert summary["lexical_rag"]["metrics"]["retrieval_hit"] == 1.0
    assert "Fresh-Hard candidates: 6" in markdown
