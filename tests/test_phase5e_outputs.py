from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEASIBILITY = (
    ROOT / "outputs" / "archive" / "provenance" / "flashrag-integration" / "method-feasibility-calibration"
    / "flashrag_method_feasibility"
    / "real_pilot_nickel_superalloy_manifest.json"
)
PACKET_JSONL = ROOT / "outputs" / "archive" / "provenance" / "flashrag-integration" / "method-feasibility-calibration" / "human_calibration_fresh_hard" / "review_packet.jsonl"
PACKET_MD = ROOT / "outputs" / "archive" / "provenance" / "flashrag-integration" / "method-feasibility-calibration" / "human_calibration_fresh_hard" / "review_packet.md"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase5e_flashrag_feasibility_records_current_runtime_blockers():
    manifest = json.loads(FEASIBILITY.read_text(encoding="utf-8"))

    assert manifest["flashrag_commit"] == "e0e73399ce8d4563397b5fb4980de72a9c5e15a6"
    assert manifest["module_imports"]["flashrag.dataset.dataset"]["ok"] is True
    assert manifest["module_imports"]["flashrag.retriever.retriever"]["ok"] is True
    assert manifest["module_imports"]["flashrag.retriever.index_builder"]["ok"] is True
    assert manifest["methods"]["flashrag_bm25"]["feasible"] is True
    assert manifest["methods"]["flashrag_dense"]["feasible"] is False
    assert manifest["methods"]["flashrag_reranker"]["feasible"] is False
    assert manifest["packages"]["torch"]["version"] == "2.1.2+cu121"
    assert manifest["packages"]["transformers"]["version"] == "5.12.1"
    assert {blocker["kind"] for blocker in manifest["blockers"]} >= {
        "missing_package",
        "module_import_failure",
        "version_mismatch",
    }
    assert manifest["recommendation"]["next_step"] == "keep_bm25_and_calibration_first"


def test_phase5e_human_calibration_packet_covers_fresh_hard_bm25_live_rows():
    rows = _read_jsonl(PACKET_JSONL)

    assert len(rows) == 4
    assert {row["method"] for row in rows} == {"flashrag_bm25_live_deepseek"}
    assert {row["split"] for row in rows} == {"fresh_hard"}
    assert [row["id"] for row in rows] == [
        "ns_ht_q009",
        "ns_ht_q010",
        "ns_ht_q011",
        "ns_ht_q012",
    ]
    assert all(row["judge_scores"]["faithfulness"] == 5.0 for row in rows)
    assert all(row["judge_scores"]["hallucination_risk"] == 0.0 for row in rows)
    assert all(row["priority"] == "normal" for row in rows)
    assert all(row["human_review"]["decision"] is None for row in rows)
    assert rows[3]["scores"]["short_answer_token_f1"] > 0.78
    assert len(rows[0]["context_chunks"]) == 5


def test_phase5e_human_calibration_markdown_is_readable_review_packet():
    markdown = PACKET_MD.read_text(encoding="utf-8")

    assert "# DomainRAG Human Calibration Packet" in markdown
    assert "Questions for review: 4" in markdown
    assert "fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q009" in markdown
    assert "Human review:" in markdown
    assert "faithfulness:" in markdown
