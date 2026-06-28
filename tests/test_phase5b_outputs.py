from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE5B = ROOT / "outputs" / "archive" / "provenance" / "flashrag-integration" / "bm25-bridge-and-judge"
BM25 = PHASE5B / "flashrag_bm25_bridge"
JUDGE = PHASE5B / "deepseek_judge_flashrag_bm25_fresh_hard"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase5b_flashrag_bm25_outputs_cover_all_real_pilot_splits():
    for split in ["dev", "test", "fresh_hard"]:
        result_path = (
            BM25
            / "real_pilot_nickel_superalloy"
            / f"{split}_flashrag_bm25_results.jsonl"
        )
        rows = _read_jsonl(result_path)

        assert len(rows) == 4
        assert {row["method"] for row in rows} == {"flashrag_bm25_oracle_reader"}
        assert all(row["error"] is None for row in rows)
        assert all(row["api_calls"] == 0 for row in rows)
        assert all(row["retrieved_context_ids"] for row in rows)
        assert all(row["scores"]["retrieval_hit"] == 1.0 for row in rows)
        assert all(row["scores"]["retrieval_mrr"] == 1.0 for row in rows)
        assert all(row["scores"]["retrieval_recall"] == 1.0 for row in rows)


def test_phase5b_flashrag_bm25_summary_records_retrieval_metrics():
    summary = json.loads((BM25 / "report_fresh_hard" / "summary.json").read_text(encoding="utf-8"))
    metrics = summary["flashrag_bm25_oracle_reader"]["metrics"]

    assert summary["flashrag_bm25_oracle_reader"]["questions"] == 4
    assert summary["flashrag_bm25_oracle_reader"]["api_calls"] == 0
    assert summary["flashrag_bm25_oracle_reader"]["errors"] == 0
    assert metrics["retrieval_hit"] == 1.0
    assert metrics["retrieval_mrr"] == 1.0
    assert metrics["retrieval_recall"] == 1.0
    assert metrics["single_choice_accuracy"] == 1.0
    assert metrics["multiple_choice_exact_match"] == 1.0
    assert metrics["fill_blank_normalized_em"] == 1.0
    assert metrics["short_answer_token_f1"] == 1.0


def test_phase5b_deepseek_judge_outputs_are_complete_for_fresh_hard():
    result_path = (
        JUDGE
        / "real_pilot_nickel_superalloy"
        / "fresh_hard_judge_results.jsonl"
    )
    rows = _read_jsonl(result_path)

    assert len(rows) == 4
    assert {row["method"] for row in rows} == {"flashrag_bm25_oracle_reader"}
    assert all(row["error"] is None for row in rows)
    assert all(row["api_calls"] == 1 for row in rows)
    assert all(row["judge_scores"]["hallucination_risk"] == 0.0 for row in rows)
    assert all(not row["judge"]["unsupported_claims"] for row in rows)


def test_phase5b_deepseek_judge_summary_scores_oracle_reader_at_ceiling():
    summary = json.loads((JUDGE / "report_fresh_hard" / "summary.json").read_text(encoding="utf-8"))
    method = summary["flashrag_bm25_oracle_reader"]

    assert method["questions"] == 4
    assert method["api_calls"] == 4
    assert method["errors"] == 0
    assert method["unsupported_claims"] == 0
    assert method["metrics"]["correctness"] == 5.0
    assert method["metrics"]["context_support"] == 5.0
    assert method["metrics"]["faithfulness"] == 5.0
    assert method["metrics"]["hallucination_risk"] == 0.0
