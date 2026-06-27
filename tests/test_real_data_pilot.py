from __future__ import annotations

import json
from pathlib import Path

from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.io_utils import read_jsonl
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure"
    / "sources.jsonl"
)
EASY_DATASET_SOURCE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy"
PUBLIC_DATASET = ROOT / "data" / "real_pilot_nickel_superalloy"


def test_real_pilot_manifest_tracks_real_sources():
    sources = read_jsonl(SOURCE_MANIFEST)

    assert len(sources) >= 5
    source_ids = {source["source_id"] for source in sources}
    assert len(source_ids) == len(sources)
    for source in sources:
        assert set(source) == {
            "source_id",
            "title",
            "year",
            "url",
            "access",
            "used_for_chunk_ids",
            "evidence_note",
        }
        assert source["source_id"].startswith("nsht_")
        assert source["year"] in {2022, 2025}
        assert source["url"].startswith("https://")
        assert source["access"] == "open_access"
        assert source["used_for_chunk_ids"]
        assert "mock" not in source["evidence_note"].lower()


def test_real_pilot_easy_dataset_source_has_real_chunks_and_all_splits():
    chunks = read_jsonl(EASY_DATASET_SOURCE / "chunks.jsonl")
    items = read_jsonl(EASY_DATASET_SOURCE / "items.jsonl")

    chunk_ids = {chunk["id"] for chunk in chunks}
    assert len(chunks) >= 8
    assert len(items) >= 12
    assert {item["split"] for item in items} == {"dev", "test", "fresh_hard"}
    assert {item["question_type"] for item in items} == {
        "fill_blank",
        "multiple_choice",
        "short_answer",
        "single_choice",
    }
    for chunk in chunks:
        assert chunk["id"].startswith("ns_ht_")
        assert chunk["content"].strip()
        lowered = chunk["content"].lower()
        assert "mock" not in lowered
        assert "smoke" not in lowered
        assert "doi" not in lowered
        assert "author" not in lowered
    for item in items:
        assert set(item["source_chunk_ids"]) <= chunk_ids
        assert not any(phrase in item["question"].lower() for phrase in ["this paper", "the paper"])


def test_export_domainrag_bundle_recreates_real_pilot_dataset(tmp_path: Path):
    bundle = export_domainrag_bundle(
        EASY_DATASET_SOURCE,
        tmp_path,
        "real_pilot_nickel_superalloy",
    )

    validate_dataset(bundle.dataset_dir)
    statistics = json.loads(bundle.statistics_path.read_text(encoding="utf-8"))
    assert statistics["corpus_count"] >= 8
    assert statistics["question_count"] >= 12
    assert statistics["split_counts"] == {
        "dev": 4,
        "fresh_hard": 4,
        "test": 4,
    }


def test_committed_real_pilot_public_dataset_is_valid():
    validate_dataset(PUBLIC_DATASET)

    statistics = json.loads((PUBLIC_DATASET / "statistics.json").read_text(encoding="utf-8"))
    assert statistics["dataset_name"] == "real_pilot_nickel_superalloy"
    assert statistics["corpus_count"] >= 8
    assert statistics["question_count"] >= 12
