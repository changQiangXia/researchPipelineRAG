from pathlib import Path
import json

import pytest

from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.errors import ValidationError
from domainrag.io_utils import read_jsonl
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "easy_dataset" / "example_export"


def test_export_domainrag_bundle_writes_valid_dataset(tmp_path: Path):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    assert bundle.dataset_name == "example_easy_dataset"
    assert bundle.dataset_dir == tmp_path / "example_easy_dataset"
    assert (bundle.dataset_dir / "corpus.jsonl").exists()
    assert (bundle.dataset_dir / "canonical_dataset.jsonl").exists()
    assert (bundle.dataset_dir / "dev.jsonl").exists()
    assert (bundle.dataset_dir / "test.jsonl").exists()
    assert (bundle.dataset_dir / "fresh_hard_test.jsonl").exists()
    assert (bundle.dataset_dir / "qrels" / "dev.tsv").exists()
    assert (bundle.dataset_dir / "dataset_card.md").exists()
    assert (bundle.dataset_dir / "statistics.json").exists()
    validate_dataset(bundle.dataset_dir)


def test_export_domainrag_bundle_strips_internal_source_metadata(tmp_path: Path):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    public_text = "".join(
        path.read_text(encoding="utf-8")
        for path in [
            bundle.dataset_dir / "corpus.jsonl",
            bundle.dataset_dir / "canonical_dataset.jsonl",
            bundle.dataset_dir / "dev.jsonl",
            bundle.dataset_dir / "test.jsonl",
            bundle.dataset_dir / "fresh_hard_test.jsonl",
        ]
    )
    assert "original_paper_title" not in public_text
    assert "doi" not in public_text
    assert "authors" not in public_text
    assert "venue" not in public_text
    assert "page_number" not in public_text


def test_export_domainrag_bundle_renders_choice_options_in_split_question(
    tmp_path: Path,
):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    dev = read_jsonl(bundle.dataset_dir / "dev.jsonl")

    assert "A. Chromium-rich oxide scales" in dev[0]["question"]
    assert dev[0]["metadata"]["correct_options"] == ["A"]


def test_export_domainrag_bundle_rejects_missing_source_chunk(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "chunks.jsonl").write_text(
        '{"id":"chunk-1","content":"content"}\n',
        encoding="utf-8",
    )
    (source / "items.jsonl").write_text(
        '{"id":"q1","split":"dev","question_type":"single_choice","question":"Q?","options":{"A":"a","B":"b","C":"c","D":"d"},"answer":["A"],"answer_aliases":[],"reference_answer":"a","required_points":[],"source_chunk_ids":["missing"],"subdomain":"demo","knowledge_type":"fact","difficulty":"easy","quality_score":1.0}\n',
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        export_domainrag_bundle(source, tmp_path / "out", "bad")

    assert "source chunk missing not in chunks.jsonl" in str(exc.value)
    assert not (tmp_path / "out" / "bad").exists()


def test_export_domainrag_bundle_writes_split_statistics(tmp_path: Path):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    statistics = json.loads(bundle.statistics_path.read_text(encoding="utf-8"))

    assert statistics["split_counts"] == {
        "dev": 1,
        "fresh_hard": 1,
        "test": 1,
    }
    assert statistics["question_type_counts"] == {
        "fill_blank": 1,
        "short_answer": 1,
        "single_choice": 1,
    }


def test_export_domainrag_bundle_rejects_output_inside_input(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()

    with pytest.raises(ValidationError) as exc:
        export_domainrag_bundle(source, source / "nested-output", "bad")

    assert "overlaps the Easy Dataset input directory" in str(exc.value)
