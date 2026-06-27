from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.validator import validate_dataset


DOMAINRAG_TO_FLASHRAG_SPLIT_FILES = {
    "dev": ("dev.jsonl", "dev.jsonl"),
    "test": ("test.jsonl", "test.jsonl"),
    "fresh_hard": ("fresh_hard_test.jsonl", "fresh_hard.jsonl"),
}
SAFE_DATASET_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


@dataclass(frozen=True)
class FlashRAGBundle:
    dataset_name: str
    data_dir: Path
    dataset_dir: Path
    corpus_path: Path
    qrels_dir: Path
    config_path: Path
    splits: tuple[str, ...]


def prepare_flashrag_bundle(
    dataset_dir: Path,
    output_dir: Path,
    dataset_name: str | None = None,
    splits: tuple[str, ...] = ("dev", "test", "fresh_hard"),
) -> FlashRAGBundle:
    validate_dataset(dataset_dir)

    resolved_dataset_name = _validate_dataset_name(
        dataset_dir.name if dataset_name is None else dataset_name
    )
    _validate_requested_splits(dataset_dir, splits)

    output_dir.mkdir(parents=True, exist_ok=True)
    target_dataset_dir = output_dir / resolved_dataset_name
    _validate_target_does_not_overlap_source(dataset_dir, target_dataset_dir)
    if target_dataset_dir.exists():
        shutil.rmtree(target_dataset_dir)
    target_dataset_dir.mkdir(parents=True, exist_ok=True)

    for split in splits:
        source_name, target_name = DOMAINRAG_TO_FLASHRAG_SPLIT_FILES[split]
        shutil.copy2(dataset_dir / source_name, target_dataset_dir / target_name)

    corpus_path = target_dataset_dir / "corpus.jsonl"
    shutil.copy2(dataset_dir / "corpus.jsonl", corpus_path)

    qrels_dir = target_dataset_dir / "qrels"
    qrels_dir.mkdir(parents=True, exist_ok=True)
    for split in splits:
        shutil.copy2(dataset_dir / "qrels" / f"{split}.tsv", qrels_dir / f"{split}.tsv")

    config_path = output_dir / f"{resolved_dataset_name}_flashrag.yaml"
    config_path.write_text(
        _render_config(output_dir, resolved_dataset_name, splits),
        encoding="utf-8",
    )

    return FlashRAGBundle(
        dataset_name=resolved_dataset_name,
        data_dir=output_dir,
        dataset_dir=target_dataset_dir,
        corpus_path=corpus_path,
        qrels_dir=qrels_dir,
        config_path=config_path,
        splits=splits,
    )


def _validate_dataset_name(dataset_name: str) -> str:
    if (
        not dataset_name
        or dataset_name in {".", ".."}
        or "/" in dataset_name
        or "\\" in dataset_name
        or not SAFE_DATASET_NAME_PATTERN.fullmatch(dataset_name)
    ):
        raise ValidationError(
            [
                ValidationIssue(
                    path="dataset_name",
                    message=(
                        "dataset_name must be a simple dataset basename "
                        "containing only letters, numbers, '.', '_' or '-'"
                    ),
                )
            ]
        )
    return dataset_name


def _validate_requested_splits(dataset_dir: Path, splits: tuple[str, ...]) -> None:
    issues: list[ValidationIssue] = []
    if not splits:
        issues.append(
            ValidationIssue(
                path="splits",
                message="at least one split must be requested",
            )
        )
    for split in splits:
        if split not in DOMAINRAG_TO_FLASHRAG_SPLIT_FILES:
            issues.append(
                ValidationIssue(str(dataset_dir), f"unsupported split: {split}")
            )
            continue
        source_name, _ = DOMAINRAG_TO_FLASHRAG_SPLIT_FILES[split]
        source_path = dataset_dir / source_name
        if not source_path.exists():
            issues.append(ValidationIssue(str(source_path), "file does not exist"))
    if issues:
        raise ValidationError(issues)


def _validate_target_does_not_overlap_source(
    dataset_dir: Path, target_dataset_dir: Path
) -> None:
    resolved_source = dataset_dir.resolve()
    resolved_target = target_dataset_dir.resolve()
    if resolved_target == resolved_source or resolved_source in resolved_target.parents:
        raise ValidationError(
            [
                ValidationIssue(
                    path=str(target_dataset_dir),
                    message=(
                        "output dataset directory overlaps the source dataset directory; "
                        "choose an output path outside the source dataset"
                    ),
                )
            ]
        )


def _render_config(
    output_dir: Path,
    dataset_name: str,
    splits: tuple[str, ...],
) -> str:
    lines = [
        f"data_dir: {output_dir}",
        f"dataset_name: {dataset_name}",
        "split:",
    ]
    lines.extend(f"  - {split}" for split in splits)
    return "\n".join(lines) + "\n"
