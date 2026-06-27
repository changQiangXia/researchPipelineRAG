from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "outputs"
    / "phase5a"
    / "flashrag_runtime_intake"
    / "real_pilot_nickel_superalloy_manifest.json"
)


def test_phase5a_flashrag_runtime_manifest_records_real_dataset_load():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["flashrag_commit"] == "e0e73399ce8d4563397b5fb4980de72a9c5e15a6"
    assert manifest["module_imports"]["flashrag.dataset.dataset"]["ok"] is True
    assert manifest["module_imports"]["flashrag.config.config"]["ok"] is True
    assert manifest["module_imports"]["flashrag.utils.utils"]["ok"] is False
    assert "transformers" in manifest["module_imports"]["flashrag.utils.utils"]["error"]
    assert {split: summary["records"] for split, summary in manifest["splits"].items()} == {
        "dev": 4,
        "fresh_hard": 4,
        "test": 4,
    }
    assert manifest["splits"]["dev"]["first_id"] == "ns_ht_q001"
    assert manifest["splits"]["test"]["first_id"] == "ns_ht_q005"
    assert manifest["splits"]["fresh_hard"]["first_id"] == "ns_ht_q009"
    assert manifest["qrels"]["fresh_hard"]["rows"] == 6
