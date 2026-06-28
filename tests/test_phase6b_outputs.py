from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANSWER_RESULTS = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "expanded-deepseek-evaluation"
    / "expanded_live_deepseek_fresh_hard"
    / "real_pilot_nickel_superalloy_expanded"
    / "fresh_hard_deepseek_results.jsonl"
)
JUDGE_RESULTS = (
    ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "expanded-deepseek-evaluation"
    / "expanded_deepseek_judge_fresh_hard"
    / "real_pilot_nickel_superalloy_expanded"
    / "fresh_hard_judge_results.jsonl"
)
COMPARISON = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "expanded-deepseek-evaluation" / "expanded_fresh_hard_comparison" / "summary.json"
PACKET_JSONL = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "expanded-deepseek-evaluation" / "expanded_human_calibration_fresh_hard" / "review_packet.jsonl"
PACKET_MD = ROOT / "outputs" / "archive" / "provenance" / "expanded-pilots" / "expanded-deepseek-evaluation" / "expanded_human_calibration_fresh_hard" / "review_packet.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase6b_expanded_live_answers_cover_three_methods_and_eight_questions():
    rows = _read_jsonl(ANSWER_RESULTS)

    assert len(rows) == 24
    assert {row["method"] for row in rows} == {"no_rag", "oracle_context", "lexical_rag"}
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert {row["id"] for row in rows} == {
        "ns_ht_q009",
        "ns_ht_q010",
        "ns_ht_q011",
        "ns_ht_q012",
        "ns_ht_q021",
        "ns_ht_q022",
        "ns_ht_q023",
        "ns_ht_q024",
    }
    assert 24 <= sum(row["api_calls"] for row in rows) <= 48
    assert sum(1 for row in rows if row["error"]) <= 1
    assert all("scores" in row for row in rows)


def test_phase6b_expanded_judge_covers_live_answers():
    rows = _read_jsonl(JUDGE_RESULTS)

    assert len(rows) == 24
    assert {row["method"] for row in rows} == {"no_rag", "oracle_context", "lexical_rag"}
    assert sum(row["api_calls"] for row in rows) >= 23
    assert sum(1 for row in rows if row["error"]) <= 1
    assert all("judge_scores" in row for row in rows)
    assert any(
        row["method"] == "no_rag"
        and row.get("judge_scores", {}).get("hallucination_risk", 0.0) > 0.0
        for row in rows
    )


def test_phase6b_expanded_comparison_summarizes_answer_and_judge_metrics():
    summary = json.loads(COMPARISON.read_text(encoding="utf-8"))

    assert set(summary["methods"]) == {"no_rag", "oracle_context", "lexical_rag"}
    assert len(summary["leaderboard"]) == 3
    assert summary["methods"]["oracle_context"]["questions"] == 8
    assert summary["methods"]["lexical_rag"]["answer_metrics"]["retrieval_hit"] == 1.0
    assert summary["methods"]["no_rag"]["answer_metrics"]["retrieval_hit"] == 0.0
    assert summary["methods"]["oracle_context"]["judge_rows"] == 8
    assert summary["methods"]["lexical_rag"]["judge_rows"] == 8


def test_phase6b_expanded_calibration_packet_is_reviewable():
    rows = _read_jsonl(PACKET_JSONL)
    markdown = PACKET_MD.read_text(encoding="utf-8")

    assert len(rows) == 24
    assert {row["method"] for row in rows} == {"no_rag", "oracle_context", "lexical_rag"}
    assert all(row["split"] == "fresh_hard" for row in rows)
    assert all("human_review" in row for row in rows)
    assert any(row["priority"] == "high" for row in rows)
    assert "# DomainRAG Human Calibration Packet" in markdown
    assert "fresh_hard::lexical_rag::ns_ht_q023" in markdown
