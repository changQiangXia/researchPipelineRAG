from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_medium"
QUESTION_COUNT = 20
BASE_METHODS = {"no_rag", "oracle_context", "lexical_rag"}
ALL_METHODS = {
    "no_rag",
    "oracle_context",
    "lexical_rag",
    "flashrag_bm25_oracle_reader",
    "flashrag_bm25_live_deepseek",
}

BASE_ANSWERS = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge"
    / "medium_live_deepseek_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_deepseek_results.jsonl"
)
BASE_JUDGE = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge"
    / "medium_deepseek_judge_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_judge_results.jsonl"
)
BM25_ORACLE_JUDGE = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge"
    / "medium_deepseek_judge_flashrag_bm25_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_judge_results.jsonl"
)
BM25_LIVE_ANSWERS = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge"
    / "medium_live_deepseek_flashrag_bm25_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_deepseek_results.jsonl"
)
BM25_LIVE_JUDGE = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge"
    / "medium_deepseek_judge_flashrag_bm25_live_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_judge_results.jsonl"
)
COMPARISON = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge" / "medium_fresh_hard_comparison" / "summary.json"
COMPARISON_MD = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge" / "medium_fresh_hard_comparison" / "summary.md"
PACKET_JSONL = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge" / "medium_human_calibration_fresh_hard" / "review_packet.jsonl"
PACKET_MD = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "medium-live-and-judge" / "medium_human_calibration_fresh_hard" / "review_packet.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase6e_medium_base_live_answers_cover_three_methods():
    rows = _read_jsonl(BASE_ANSWERS)

    assert len(rows) == QUESTION_COUNT * 3
    assert {row["method"] for row in rows} == BASE_METHODS
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert len({row["id"] for row in rows}) == QUESTION_COUNT
    assert sum(row["api_calls"] for row in rows) >= QUESTION_COUNT * 3
    assert sum(1 for row in rows if row["error"]) <= 3
    assert all("scores" in row for row in rows)


def test_phase6e_medium_base_judge_covers_base_live_answers():
    answer_rows = _read_jsonl(BASE_ANSWERS)
    judge_rows = _read_jsonl(BASE_JUDGE)
    answer_error_keys = {
        (row["id"], row["method"])
        for row in answer_rows
        if row["error"]
    }

    assert len(judge_rows) == QUESTION_COUNT * 3
    assert {row["method"] for row in judge_rows} == BASE_METHODS
    assert sum(1 for row in judge_rows if row["error"]) <= 3
    assert sum(row["api_calls"] for row in judge_rows) >= len(judge_rows) - len(answer_error_keys)
    assert all("judge_scores" in row for row in judge_rows)
    assert any(
        row["method"] == "no_rag"
        and row.get("judge_scores", {}).get("hallucination_risk", 0.0) > 0.0
        for row in judge_rows
    )


def test_phase6e_medium_flashrag_bm25_oracle_and_live_are_judged():
    oracle_judge_rows = _read_jsonl(BM25_ORACLE_JUDGE)
    live_answer_rows = _read_jsonl(BM25_LIVE_ANSWERS)
    live_judge_rows = _read_jsonl(BM25_LIVE_JUDGE)
    live_error_ids = {row["id"] for row in live_answer_rows if row["error"]}

    assert len(oracle_judge_rows) == QUESTION_COUNT
    assert len(live_answer_rows) == QUESTION_COUNT
    assert len(live_judge_rows) == QUESTION_COUNT
    assert {row["method"] for row in oracle_judge_rows} == {"flashrag_bm25_oracle_reader"}
    assert {row["method"] for row in live_answer_rows} == {"flashrag_bm25_live_deepseek"}
    assert {row["method"] for row in live_judge_rows} == {"flashrag_bm25_live_deepseek"}
    assert sum(row["api_calls"] for row in oracle_judge_rows) >= QUESTION_COUNT - 2
    assert sum(row["api_calls"] for row in live_answer_rows) >= QUESTION_COUNT
    assert sum(row["api_calls"] for row in live_judge_rows) >= QUESTION_COUNT - len(live_error_ids) - 2
    assert sum(1 for row in oracle_judge_rows if row["error"]) <= 2
    assert sum(1 for row in live_answer_rows if row["error"]) <= 3
    assert sum(1 for row in live_judge_rows if row["error"]) <= 3
    assert all(row["scores"]["retrieval_hit"] in {0.0, 1.0} for row in live_answer_rows)
    assert all("judge_scores" in row for row in oracle_judge_rows)
    assert all("judge_scores" in row for row in live_judge_rows)


def test_phase6e_medium_comparison_summarizes_all_five_methods():
    summary = json.loads(COMPARISON.read_text(encoding="utf-8"))
    markdown = COMPARISON_MD.read_text(encoding="utf-8")

    assert set(summary["methods"]) == ALL_METHODS
    assert len(summary["leaderboard"]) == 5
    assert all(summary["methods"][method]["questions"] == QUESTION_COUNT for method in ALL_METHODS)
    assert summary["methods"]["no_rag"]["answer_metrics"]["retrieval_hit"] == 0.0
    assert summary["methods"]["oracle_context"]["answer_metrics"]["retrieval_hit"] == 1.0
    assert summary["methods"]["lexical_rag"]["answer_metrics"]["retrieval_hit"] < 1.0
    assert summary["methods"]["flashrag_bm25_oracle_reader"]["answer_metrics"]["retrieval_hit"] < 1.0
    assert "| flashrag_bm25_live_deepseek |" in markdown
    assert "| no_rag |" in markdown


def test_phase6e_medium_calibration_packet_covers_all_methods():
    rows = _read_jsonl(PACKET_JSONL)
    markdown = PACKET_MD.read_text(encoding="utf-8")

    assert len(rows) == QUESTION_COUNT * 5
    assert {row["method"] for row in rows} == ALL_METHODS
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert all("human_review" in row for row in rows)
    assert any(row["method"] == "no_rag" and row["priority"] == "high" for row in rows)
    assert any(row["method"] == "flashrag_bm25_live_deepseek" for row in rows)
    assert "Questions for review: 100" in markdown
