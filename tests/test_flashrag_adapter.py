from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.flashrag_adapter import prepare_flashrag_bundle
from tests.test_validator import _write_minimal_dataset


ROOT = Path(__file__).resolve().parents[1]


def test_prepare_flashrag_bundle_creates_expected_files(tmp_path: Path):
    dataset_dir = ROOT / "data" / "example_domain"
    output_dir = tmp_path / "flashrag"

    bundle = prepare_flashrag_bundle(dataset_dir, output_dir)

    dataset_output_dir = output_dir / "example_domain"
    assert bundle.dataset_name == "example_domain"
    assert bundle.dataset_dir == dataset_output_dir
    assert (dataset_output_dir / "dev.jsonl").exists()
    assert (dataset_output_dir / "test.jsonl").exists()
    assert (dataset_output_dir / "fresh_hard.jsonl").exists()
    assert (dataset_output_dir / "corpus.jsonl").exists()
    assert not (dataset_output_dir / "fresh_hard_test.jsonl").exists()
    assert (dataset_output_dir / "qrels" / "dev.tsv").exists()
    assert (dataset_output_dir / "qrels" / "test.tsv").exists()
    assert (dataset_output_dir / "qrels" / "fresh_hard.tsv").exists()
    assert bundle.config_path == output_dir / "example_domain_flashrag.yaml"
    assert bundle.config_path.exists()


def test_prepare_flashrag_bundle_writes_expected_yaml(tmp_path: Path):
    dataset_dir = ROOT / "data" / "example_domain"
    output_dir = tmp_path / "flashrag"

    prepare_flashrag_bundle(dataset_dir, output_dir)

    yaml_text = (output_dir / "example_domain_flashrag.yaml").read_text(encoding="utf-8")

    expected_yaml = (
        f"data_dir: {output_dir}\n"
        "dataset_name: example_domain\n"
        "split:\n"
        "  - dev\n"
        "  - test\n"
        "  - fresh_hard\n"
    )

    assert yaml_text == expected_yaml


def test_prepare_flashrag_bundle_rejects_invalid_dataset(tmp_path: Path):
    dataset_dir = ROOT / "data" / "invalid_fixtures" / "missing_qrels"
    output_dir = tmp_path / "flashrag"

    with pytest.raises(ValidationError):
        prepare_flashrag_bundle(dataset_dir, output_dir)


@pytest.mark.parametrize("dataset_name", ["", ".", "..", "nested/name", "nested\\name"])
def test_prepare_flashrag_bundle_rejects_unsafe_dataset_name(
    tmp_path: Path, dataset_name: str
):
    dataset_dir = ROOT / "data" / "example_domain"
    output_dir = tmp_path / "flashrag"

    with pytest.raises(ValidationError) as excinfo:
        prepare_flashrag_bundle(dataset_dir, output_dir, dataset_name=dataset_name)

    assert "dataset_name must be a simple dataset basename" in str(excinfo.value)


def test_prepare_flashrag_bundle_replaces_existing_target_dataset_dir(tmp_path: Path):
    dataset_dir = ROOT / "data" / "example_domain"
    output_dir = tmp_path / "flashrag"
    stale_dir = output_dir / "example_domain"
    stale_dir.mkdir(parents=True)
    stale_file = stale_dir / "stale.txt"
    stale_file.write_text("obsolete", encoding="utf-8")

    prepare_flashrag_bundle(dataset_dir, output_dir)

    assert not stale_file.exists()
    assert (stale_dir / "dev.jsonl").exists()


def test_prepare_flashrag_bundle_rejects_output_target_equal_to_source(tmp_path: Path):
    dataset_dir = tmp_path / "example_domain"
    _write_minimal_dataset(dataset_dir)

    with pytest.raises(ValidationError) as excinfo:
        prepare_flashrag_bundle(
            dataset_dir,
            dataset_dir.parent,
            dataset_name=dataset_dir.name,
        )

    assert "output dataset directory overlaps the source dataset directory" in str(
        excinfo.value
    )


def test_prepare_flashrag_bundle_rejects_output_target_nested_in_source(tmp_path: Path):
    dataset_dir = tmp_path / "dataset"
    _write_minimal_dataset(dataset_dir)

    with pytest.raises(ValidationError) as excinfo:
        prepare_flashrag_bundle(
            dataset_dir,
            dataset_dir / "outputs",
            dataset_name="nested_bundle",
        )

    assert "output dataset directory overlaps the source dataset directory" in str(
        excinfo.value
    )


def test_prepare_flashrag_bundle_rejects_output_target_parent_of_source(tmp_path: Path):
    dataset_dir = tmp_path / "data" / "example_domain"
    _write_minimal_dataset(dataset_dir)

    with pytest.raises(ValidationError) as excinfo:
        prepare_flashrag_bundle(
            dataset_dir,
            tmp_path,
            dataset_name="data",
        )

    assert "output dataset directory overlaps the source dataset directory" in str(
        excinfo.value
    )


def test_prepare_flashrag_bundle_rejects_empty_splits(tmp_path: Path):
    dataset_dir = tmp_path / "example_domain"
    _write_minimal_dataset(dataset_dir)
    output_dir = tmp_path / "flashrag"

    with pytest.raises(ValidationError) as excinfo:
        prepare_flashrag_bundle(
            dataset_dir,
            output_dir,
            splits=(),
        )

    assert "at least one split must be requested" in str(excinfo.value)
