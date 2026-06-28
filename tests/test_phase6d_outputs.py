from __future__ import annotations

import json
from pathlib import Path

from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_medium"
DATASET = ROOT / "data" / DATASET_NAME
FLASHRAG = ROOT / "outputs" / "flashrag" / DATASET_NAME
BASELINE = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-baseline-and-bm25" / "medium_baseline"
BM25 = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-baseline-and-bm25" / "medium_flashrag_bm25_bridge"
COMPARISON = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-baseline-and-bm25" / "medium_retrieval_comparison" / "summary.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase6d_medium_dataset_and_flashrag_bundle_are_valid():
    validate_dataset(DATASET)
    statistics = json.loads((DATASET / "statistics.json").read_text(encoding="utf-8"))

    assert statistics["corpus_count"] == 40
    assert statistics["question_count"] == 60
    assert statistics["split_counts"] == {
        "dev": 20,
        "fresh_hard": 20,
        "test": 20,
    }
    assert len(_read_jsonl(FLASHRAG / "fresh_hard.jsonl")) == 20
    assert len(_read_jsonl(FLASHRAG / "corpus.jsonl")) == 40
    assert (FLASHRAG / "qrels" / "fresh_hard.tsv").exists()


def test_phase6d_medium_baseline_covers_three_methods_and_twenty_questions():
    result_path = BASELINE / DATASET_NAME / "fresh_hard_results.jsonl"
    rows = _read_jsonl(result_path)

    assert len(rows) == 60
    assert {row["method"] for row in rows} == {
        "no_rag",
        "oracle_context",
        "lexical_rag",
    }
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert len({row["id"] for row in rows}) == 20
    assert all(row["scores"]["retrieval_hit"] == 0.0 for row in rows if row["method"] == "no_rag")
    assert all(
        row["scores"]["retrieval_hit"] == 1.0
        for row in rows
        if row["method"] == "oracle_context"
    )


def test_phase6d_medium_flashrag_bm25_bridge_has_real_retrieval_signal():
    rows = _read_jsonl(BM25 / DATASET_NAME / "fresh_hard_flashrag_bm25_results.jsonl")

    assert len(rows) == 20
    assert {row["method"] for row in rows} == {"flashrag_bm25_oracle_reader"}
    assert all(len(row["retrieved_context_ids"]) == 5 for row in rows)
    assert sum(row["scores"]["retrieval_hit"] for row in rows) >= 17.0
    assert any(row["scores"]["retrieval_recall"] < 1.0 for row in rows)


def test_phase6d_medium_retrieval_comparison_summarizes_lexical_and_bm25():
    summary = json.loads(COMPARISON.read_text(encoding="utf-8"))

    assert set(summary["methods"]) == {"lexical_rag", "flashrag_bm25_oracle_reader"}
    assert summary["methods"]["lexical_rag"]["questions"] == 20
    assert summary["methods"]["flashrag_bm25_oracle_reader"]["questions"] == 20
    assert "retrieval_hit" in summary["methods"]["lexical_rag"]["answer_metrics"]
    assert "retrieval_recall" in summary["methods"]["flashrag_bm25_oracle_reader"]["answer_metrics"]
