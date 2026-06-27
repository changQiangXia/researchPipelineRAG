from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_deepseek_real_pilot.py"
CHUNKS = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy" / "chunks.jsonl"


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
