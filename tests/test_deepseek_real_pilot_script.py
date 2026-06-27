from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_deepseek_real_pilot.py"
CHUNKS = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy" / "chunks.jsonl"


spec = importlib.util.spec_from_file_location("run_deepseek_real_pilot", SCRIPT)
run_deepseek_real_pilot = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run_deepseek_real_pilot)


def test_deepseek_real_pilot_script_dry_run_writes_planned_requests_without_secret(
    tmp_path: Path,
):
    env = os.environ.copy()
    env.pop("DEEPSEEK_API_KEY", None)
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--chunks",
            str(CHUNKS),
            "--output",
            str(tmp_path),
            "--dry-run",
            "--max-items",
            "1",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads((tmp_path / "run_manifest.json").read_text(encoding="utf-8"))
    planned = (tmp_path / "planned_requests.jsonl").read_text(encoding="utf-8")

    assert manifest["dry_run"] is True
    assert manifest["planned_items"] == 1
    assert "api_key" not in planned.lower()
    assert "sk-" not in planned
    assert "planned requests written" in result.stdout


def test_deepseek_real_pilot_script_all_chunks_dry_run_plans_each_chunk(
    tmp_path: Path,
):
    env = os.environ.copy()
    env.pop("DEEPSEEK_API_KEY", None)
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--chunks",
            str(CHUNKS),
            "--output",
            str(tmp_path),
            "--dry-run",
            "--plan",
            "all-chunks",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    planned_rows = [
        json.loads(line)
        for line in (tmp_path / "planned_requests.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    manifest = json.loads((tmp_path / "run_manifest.json").read_text(encoding="utf-8"))

    assert manifest["plan"] == "all-chunks"
    assert manifest["planned_items"] == 9
    assert len(planned_rows) == 9
    assert {row["chunk_id"] for row in planned_rows} == {
        json.loads(line)["id"] for line in CHUNKS.read_text(encoding="utf-8").splitlines()
    }
    assert {row["split"] for row in planned_rows} == {"dev", "test", "fresh_hard"}
    assert {"single_choice", "multiple_choice", "fill_blank", "short_answer"} <= {
        row["question_type"] for row in planned_rows
    }


def test_candidate_audit_row_classifies_accepted_rejected_and_human_review():
    item = {
        "id": "candidate_1",
        "split": "dev",
        "question_type": "single_choice",
    }
    accepted = run_deepseek_real_pilot.build_candidate_audit_row(
        chunk_id="chunk_1",
        item=item,
        review_result={
            "accepted": True,
            "quality_score": 0.92,
            "problems": [],
            "corrected_item": {},
        },
    )
    needs_review = run_deepseek_real_pilot.build_candidate_audit_row(
        chunk_id="chunk_1",
        item=item,
        review_result={
            "accepted": True,
            "quality_score": 0.86,
            "problems": ["borderline distractor quality"],
            "corrected_item": {},
        },
    )
    rejected = run_deepseek_real_pilot.build_candidate_audit_row(
        chunk_id="chunk_1",
        item=item,
        review_result={
            "accepted": False,
            "quality_score": 0.6,
            "problems": ["unsupported answer"],
            "corrected_item": {},
        },
    )

    assert accepted["decision"] == "accepted"
    assert accepted["needs_human_review_reason"] == ""
    assert needs_review["decision"] == "needs_human_review"
    assert "quality score below automatic acceptance threshold" in needs_review[
        "needs_human_review_reason"
    ]
    assert rejected["decision"] == "rejected"
    assert rejected["needs_human_review_reason"] == "review rejected candidate"
