from __future__ import annotations

import importlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_qrels


def verify_flashrag_runtime_intake(
    flashrag_path: Path,
    dataset_bundle: Path,
    *,
    dataset_name: str,
    splits: tuple[str, ...],
    output_path: Path | None = None,
) -> dict[str, Any]:
    issues = _validate_inputs(flashrag_path, dataset_bundle, splits)
    if issues:
        raise ValidationError(issues)

    with _temporary_sys_path(flashrag_path):
        module_imports = {
            module_name: _import_status(module_name)
            for module_name in [
                "flashrag.dataset.dataset",
                "flashrag.config.config",
                "flashrag.utils.utils",
            ]
        }
        dataset_module = importlib.import_module("flashrag.dataset.dataset")
        dataset_class = getattr(dataset_module, "Dataset")

        split_summaries: dict[str, dict[str, Any]] = {}
        qrels_summaries: dict[str, dict[str, Any]] = {}
        for split in splits:
            split_path = dataset_bundle / f"{split}.jsonl"
            dataset = dataset_class(
                config={"dataset_name": dataset_name},
                dataset_path=str(split_path),
            )
            ids = list(getattr(dataset, "id"))
            golden_answers = list(getattr(dataset, "golden_answers"))
            first_item = dataset[0] if len(dataset) else None
            split_summaries[split] = {
                "file": str(split_path),
                "records": len(dataset),
                "first_id": ids[0] if ids else None,
                "first_question_preview": (
                    getattr(first_item, "question", "")[:160] if first_item else ""
                ),
                "first_golden_answers": golden_answers[0] if golden_answers else [],
            }
            qrels_rows = read_qrels(dataset_bundle / "qrels" / f"{split}.tsv")
            qrels_summaries[split] = {
                "file": str(dataset_bundle / "qrels" / f"{split}.tsv"),
                "rows": len(qrels_rows),
            }

    manifest = {
        "dataset_bundle": str(dataset_bundle),
        "dataset_name": dataset_name,
        "flashrag_path": str(flashrag_path),
        "flashrag_commit": _git_commit(flashrag_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "module_imports": module_imports,
        "qrels": qrels_summaries,
        "splits": split_summaries,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return manifest


def _validate_inputs(
    flashrag_path: Path,
    dataset_bundle: Path,
    splits: tuple[str, ...],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not (flashrag_path / "flashrag").is_dir():
        issues.append(ValidationIssue(str(flashrag_path), "FlashRAG package directory missing"))
    if not dataset_bundle.is_dir():
        issues.append(ValidationIssue(str(dataset_bundle), "dataset bundle directory missing"))
    if not splits:
        issues.append(ValidationIssue("splits", "at least one split must be requested"))
    for split in splits:
        split_path = dataset_bundle / f"{split}.jsonl"
        qrels_path = dataset_bundle / "qrels" / f"{split}.tsv"
        if not split_path.exists():
            issues.append(ValidationIssue(str(split_path), "file does not exist"))
        if not qrels_path.exists():
            issues.append(ValidationIssue(str(qrels_path), "file does not exist"))
    if not (dataset_bundle / "corpus.jsonl").exists():
        issues.append(ValidationIssue(str(dataset_bundle / "corpus.jsonl"), "file does not exist"))
    return issues


class _temporary_sys_path:
    def __init__(self, path: Path) -> None:
        self.path = str(path)
        self._removed_modules: dict[str, Any] = {}

    def __enter__(self) -> None:
        sys.path.insert(0, self.path)
        for module_name in list(sys.modules):
            if module_name == "flashrag" or module_name.startswith("flashrag."):
                self._removed_modules[module_name] = sys.modules.pop(module_name)

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass
        for module_name in list(sys.modules):
            if module_name == "flashrag" or module_name.startswith("flashrag."):
                sys.modules.pop(module_name, None)
        sys.modules.update(self._removed_modules)


def _import_status(module_name: str) -> dict[str, Any]:
    try:
        importlib.import_module(module_name)
    except Exception as exc:
        return {
            "ok": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    return {"ok": True, "error_type": None, "error": None}


def _git_commit(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    return result.stdout.strip()
