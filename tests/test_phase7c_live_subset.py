from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "real_pilot_nickel_superalloy_medium_plus"
METHODS = {
    "no_rag",
    "lexical_rag",
    "flashrag_bm25_live_deepseek",
}
LIVE_DIR = ROOT / "outputs" / "phase7c" / "medium_plus_live_subset"
ANSWERS = LIVE_DIR / "answers" / DATASET_NAME / "fresh_hard_deepseek_results.jsonl"
JUDGE = LIVE_DIR / "judge" / DATASET_NAME / "fresh_hard_judge_results.jsonl"
JUDGE_SUMMARY = LIVE_DIR / "judge_report" / "summary.json"
COMPARISON = LIVE_DIR / "comparison" / "summary.json"
DOC = ROOT / "docs" / "verification" / "medium-plus-live-subset.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7c_script_dry_run_records_bounded_live_commands():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_medium_plus_live_subset.py",
            "--dry-run",
            "--limit",
            "12",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "run-deepseek-answers" in result.stdout
    assert "judge-deepseek-answers" in result.stdout
    assert "compare" in result.stdout
    assert "--limit 12" in result.stdout
    assert "--methods no_rag,lexical_rag,flashrag_bm25_live_deepseek" in result.stdout
    assert "outputs/phase7b/medium_plus_bm25s" in result.stdout
    assert "DEEPSEEK_API_KEY" not in result.stdout


def test_phase7c_medium_plus_live_outputs_cover_bounded_subset():
    answer_rows = _read_jsonl(ANSWERS)
    judge_rows = _read_jsonl(JUDGE)
    judge_summary = json.loads(JUDGE_SUMMARY.read_text(encoding="utf-8"))
    comparison = json.loads(COMPARISON.read_text(encoding="utf-8"))

    assert len(answer_rows) == 36
    assert len(judge_rows) == 36
    assert {row["method"] for row in answer_rows} == METHODS
    assert {row["method"] for row in judge_rows} == METHODS
    assert {row["split"] for row in answer_rows} == {"fresh_hard"}
    assert {row["split"] for row in judge_rows} == {"fresh_hard"}
    assert len({row["id"] for row in answer_rows}) == 12
    assert len({row["id"] for row in judge_rows}) == 12
    answer_errors = sum(1 for row in answer_rows if row["error"])
    judge_errors = sum(1 for row in judge_rows if row["error"])
    assert sum(row["api_calls"] for row in answer_rows) >= 36
    assert sum(row["api_calls"] for row in judge_rows) >= 36 - answer_errors
    assert answer_errors <= 2
    assert judge_errors <= answer_errors + 1
    assert all("judge_scores" in row for row in judge_rows)
    assert set(judge_summary) == METHODS
    assert set(comparison["methods"]) == METHODS
    assert len(comparison["leaderboard"]) == 3
    assert comparison["methods"]["no_rag"]["answer_metrics"]["retrieval_hit"] == 0.0
    assert (
        comparison["methods"]["flashrag_bm25_live_deepseek"]["answer_metrics"][
            "retrieval_hit"
        ]
        < 1.0
    )


def test_phase7c_updates_docs_and_audit_without_claiming_final_scale():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}

    assert "Phase 7C" in doc
    assert "bounded live DeepSeek" in doc
    assert "12 Fresh-Hard questions" in doc
    assert "36 answer rows" in doc
    assert "36 judge rows" in doc
    assert "outputs/phase7c/medium_plus_live_subset/comparison/summary.json" in doc
    assert audit["phase"] == "Phase 7I"
    assert audit["dataset"]["name"] == DATASET_NAME
    assert audit["dataset"]["corpus_chunks"] == 100
    assert audit["dataset"]["questions"] == 150
    assert audit["phase7c_medium_plus_live_subset"]["questions"] == 12
    assert audit["phase7c_medium_plus_live_subset"]["answer_rows"] == 36
    assert audit["phase7c_medium_plus_live_subset"]["judge_rows"] == 36
    assert audit["phase7d_demo_scale_source_acquisition"]["verification_status"] == (
        "candidate_pool_only"
    )
    assert audit["phase7e_source_screening_queue"]["verification_status"] == (
        "machine_prescreen_only"
    )
    assert audit["phase7f_source_decisions"]["verification_status"] == (
        "provisional_not_final"
    )
    assert requirements["demo_scale"]["status"] == "partial"
    assert requirements["live_deepseek_judge"]["status"] == "complete"
    assert "outputs/phase7c/medium_plus_live_subset/" in requirements[
        "live_deepseek_judge"
    ]["evidence"]
