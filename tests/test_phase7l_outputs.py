from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "archive" / "provenance" / "source-workflow" / "full-text-chunk-extraction" / "full_text_chunk_extraction"
CHUNKS = OUTPUT / "full_text_chunks.jsonl"
MANIFEST = OUTPUT / "chunk_source_manifest.jsonl"
SUMMARY = OUTPUT / "chunk_extraction_summary.json"
DOC = ROOT / "docs" / "verification" / "full-text-chunk-extraction.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase7l_full_text_chunk_extraction_reaches_demo_chunk_range_without_text_leakage():
    chunks = _read_jsonl(CHUNKS)
    manifest = _read_jsonl(MANIFEST)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert len(chunks) == 2196
    assert len(manifest) == 115
    assert summary["phase"] == "Phase 7L"
    assert summary["access_rows"] == 115
    assert summary["parseable_access_rows"] == 71
    assert summary["sources_attempted"] == 71
    assert summary["sources_chunked"] == 60
    assert summary["chunk_count"] == 2196
    assert 1000 <= summary["chunk_count"] <= 3000
    assert summary["chunk_status_counts"] == {
        "chunked": 60,
        "skipped_not_parseable": 44,
        "too_short": 11,
    }
    assert summary["include_text"] is False
    assert summary["provenance_status"] == "machine_parseable_not_human_final"
    assert all("text" not in row for row in chunks)
    assert all("text_sample" not in row for row in chunks)
    assert all(len(row["text_sha256"]) == 64 for row in chunks)


def test_phase7l_updates_docs_and_audit_without_claiming_final_demo_dataset():
    doc = DOC.read_text(encoding="utf-8")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}

    assert "Phase 7L" in doc
    assert "2,196" in doc
    assert "machine_parseable_not_human_final" in doc
    assert "chunk text omitted" in doc
    assert audit["phase"] == "Phase 7M"
    assert audit["phase7l_full_text_chunk_extraction"] == {
        "access_rows": 115,
        "parseable_access_rows": 71,
        "sources_attempted": 71,
        "sources_chunked": 60,
        "chunk_count": 2196,
        "chunk_target_status": "meets_demo_chunk_count_target",
        "include_text": False,
        "provenance_status": "machine_parseable_not_human_final",
        "final_demo_dataset_claim": "not_complete",
        "outputs": [
            "outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/full_text_chunks.jsonl",
            "outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_source_manifest.jsonl",
            "outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.json",
            "docs/verification/full-text-chunk-extraction.md",
        ],
    }
    assert requirements["demo_scale"]["status"] == "partial"
    assert "2,196 full-text chunk manifests" in requirements["demo_scale"]["summary"]
    assert "outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.json" in requirements[
        "demo_scale"
    ]["evidence"]
