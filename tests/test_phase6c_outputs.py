from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_expanded"
QUESTION_IDS = {
    "ns_ht_q009",
    "ns_ht_q010",
    "ns_ht_q011",
    "ns_ht_q012",
    "ns_ht_q021",
    "ns_ht_q022",
    "ns_ht_q023",
    "ns_ht_q024",
}
ALL_METHODS = {
    "no_rag",
    "oracle_context",
    "lexical_rag",
    "flashrag_bm25_oracle_reader",
    "flashrag_bm25_live_deepseek",
}

BM25_RESULTS = (
    ROOT
    / "outputs"
    / "phase6c"
    / "expanded_flashrag_bm25_bridge"
    / DATASET_NAME
    / "fresh_hard_flashrag_bm25_results.jsonl"
)
BM25_ORACLE_JUDGE = (
    ROOT
    / "outputs"
    / "phase6c"
    / "expanded_deepseek_judge_flashrag_bm25_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_judge_results.jsonl"
)
BM25_LIVE_ANSWERS = (
    ROOT
    / "outputs"
    / "phase6c"
    / "expanded_live_deepseek_flashrag_bm25_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_deepseek_results.jsonl"
)
BM25_LIVE_JUDGE = (
    ROOT
    / "outputs"
    / "phase6c"
    / "expanded_deepseek_judge_flashrag_bm25_live_fresh_hard"
    / DATASET_NAME
    / "fresh_hard_judge_results.jsonl"
)
COMPARISON = ROOT / "outputs" / "phase6c" / "expanded_fresh_hard_comparison" / "summary.json"
COMPARISON_MD = ROOT / "outputs" / "phase6c" / "expanded_fresh_hard_comparison" / "summary.md"
PACKET_JSONL = ROOT / "outputs" / "phase6c" / "expanded_human_calibration_fresh_hard" / "review_packet.jsonl"
PACKET_MD = ROOT / "outputs" / "phase6c" / "expanded_human_calibration_fresh_hard" / "review_packet.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase6c_flashrag_bm25_bridge_retrieves_expanded_fresh_hard_contexts():
    rows = _read_jsonl(BM25_RESULTS)

    assert len(rows) == 8
    assert {row["method"] for row in rows} == {"flashrag_bm25_oracle_reader"}
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert {row["id"] for row in rows} == QUESTION_IDS
    assert all(row["api_calls"] == 0 for row in rows)
    assert all(row["error"] is None for row in rows)
    assert all(row["scores"]["retrieval_hit"] == 1.0 for row in rows)
    assert all(row["scores"]["retrieval_recall"] > 0.0 for row in rows)
    assert all(len(row["retrieved_context_ids"]) == 5 for row in rows)


def test_phase6c_flashrag_bm25_oracle_judge_covers_bridge_rows():
    rows = _read_jsonl(BM25_ORACLE_JUDGE)

    assert len(rows) == 8
    assert {row["method"] for row in rows} == {"flashrag_bm25_oracle_reader"}
    assert {row["id"] for row in rows} == QUESTION_IDS
    assert sum(row["api_calls"] for row in rows) >= 8
    assert sum(1 for row in rows if row["error"]) <= 1
    assert all("judge_scores" in row for row in rows)
    assert all(row["judge_scores"]["correctness"] == 5.0 for row in rows if not row["error"])
    assert any(
        row["id"] == "ns_ht_q024"
        and row["judge_scores"]["hallucination_risk"] > 0.0
        and row["judge"]["unsupported_claims"]
        for row in rows
    )


def test_phase6c_flashrag_bm25_live_answers_and_judge_are_real_expanded_runs():
    answer_rows = _read_jsonl(BM25_LIVE_ANSWERS)
    judge_rows = _read_jsonl(BM25_LIVE_JUDGE)

    assert len(answer_rows) == 8
    assert len(judge_rows) == 8
    assert {row["method"] for row in answer_rows} == {"flashrag_bm25_live_deepseek"}
    assert {row["method"] for row in judge_rows} == {"flashrag_bm25_live_deepseek"}
    assert {row["id"] for row in answer_rows} == QUESTION_IDS
    assert {row["id"] for row in judge_rows} == QUESTION_IDS
    assert 8 <= sum(row["api_calls"] for row in answer_rows) <= 16
    answer_error_ids = {row["id"] for row in answer_rows if row["error"]}
    assert sum(row["api_calls"] for row in judge_rows) >= len(judge_rows) - len(answer_error_ids)
    assert sum(1 for row in answer_rows if row["error"]) <= 1
    assert sum(1 for row in judge_rows if row["error"]) <= 1
    assert all(row["scores"]["retrieval_hit"] == 1.0 for row in answer_rows)
    assert all("judge_scores" in row for row in judge_rows)
    assert all(
        row["api_calls"] == 0 and str(row["error"]).startswith("answer row error:")
        for row in judge_rows
        if row["id"] in answer_error_ids
    )


def test_phase6c_expanded_comparison_summarizes_all_five_methods():
    summary = json.loads(COMPARISON.read_text(encoding="utf-8"))
    markdown = COMPARISON_MD.read_text(encoding="utf-8")

    assert set(summary["methods"]) == ALL_METHODS
    assert len(summary["leaderboard"]) == 5
    assert all(summary["methods"][method]["questions"] == 8 for method in ALL_METHODS)
    assert summary["methods"]["no_rag"]["answer_metrics"]["retrieval_hit"] == 0.0
    assert summary["methods"]["flashrag_bm25_oracle_reader"]["answer_metrics"]["retrieval_hit"] == 1.0
    assert summary["methods"]["flashrag_bm25_live_deepseek"]["answer_metrics"]["retrieval_hit"] == 1.0
    assert summary["methods"]["flashrag_bm25_oracle_reader"]["judge_rows"] == 8
    assert summary["methods"]["flashrag_bm25_live_deepseek"]["judge_rows"] == 8
    assert "| flashrag_bm25_live_deepseek |" in markdown


def test_phase6c_expanded_calibration_packet_covers_all_methods():
    rows = _read_jsonl(PACKET_JSONL)
    markdown = PACKET_MD.read_text(encoding="utf-8")

    assert len(rows) == 40
    assert {row["method"] for row in rows} == ALL_METHODS
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert {row["id"] for row in rows} == QUESTION_IDS
    assert all("human_review" in row for row in rows)
    assert any(row["method"] == "no_rag" and row["priority"] == "high" for row in rows)
    assert any(row["method"] == "flashrag_bm25_live_deepseek" for row in rows)
    assert "Questions for review: 40" in markdown
    assert "fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q023" in markdown
