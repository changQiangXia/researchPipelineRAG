from __future__ import annotations

import importlib
import importlib.metadata
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue


DEFAULT_FLASHRAG_MODULES = (
    "flashrag.dataset.dataset",
    "flashrag.retriever.retriever",
    "flashrag.retriever.index_builder",
    "flashrag.pipeline.pipeline",
    "flashrag.generator.generator",
)
DEFAULT_PACKAGE_NAMES = (
    "torch",
    "transformers",
    "sentence_transformers",
    "faiss",
    "bm25s",
    "Stemmer",
    "FlagEmbedding",
    "sklearn",
    "numpy",
)


def probe_flashrag_method_feasibility(
    flashrag_path: Path,
    *,
    output_path: Path | None = None,
    module_names: tuple[str, ...] = DEFAULT_FLASHRAG_MODULES,
    package_names: tuple[str, ...] = DEFAULT_PACKAGE_NAMES,
) -> dict[str, Any]:
    if not (flashrag_path / "flashrag").is_dir():
        raise ValidationError(
            [ValidationIssue(str(flashrag_path), "FlashRAG package directory missing")]
        )

    with _temporary_sys_path(flashrag_path):
        module_imports = {
            module_name: _import_status(module_name)
            for module_name in module_names
        }
    packages = {
        package_name: _package_status(package_name)
        for package_name in package_names
    }
    blockers = _blockers(module_imports, packages)
    methods = _method_feasibility(module_imports, packages, blockers)
    manifest = {
        "flashrag_path": str(flashrag_path),
        "flashrag_commit": _git_commit(flashrag_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "module_imports": module_imports,
        "packages": packages,
        "blockers": blockers,
        "methods": methods,
        "recommendation": _recommendation(methods),
    }

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return manifest


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
        module = importlib.import_module(module_name)
    except Exception as exc:
        return {
            "ok": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    return {
        "ok": True,
        "error_type": None,
        "error": None,
        "version": getattr(module, "__version__", None),
    }


def _package_status(package_name: str) -> dict[str, Any]:
    metadata_version = _metadata_package_version(package_name)
    if metadata_version is not None:
        return {
            "ok": True,
            "version": metadata_version,
            "error_type": None,
            "error": None,
        }
    try:
        module = importlib.import_module(package_name)
    except Exception as exc:
        return {
            "ok": False,
            "version": None,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    return {
        "ok": True,
        "version": _package_version(package_name, module),
        "error_type": None,
        "error": None,
    }


def _metadata_package_version(package_name: str) -> str | None:
    for distribution_name in _distribution_names(package_name):
        try:
            return importlib.metadata.version(distribution_name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def _package_version(package_name: str, module: Any) -> str | None:
    version = getattr(module, "__version__", None)
    if isinstance(version, str):
        return version
    return _metadata_package_version(package_name)


def _distribution_names(package_name: str) -> tuple[str, ...]:
    aliases = {
        "Stemmer": ("PyStemmer",),
        "sklearn": ("scikit-learn",),
        "faiss": ("faiss-cpu", "faiss-gpu"),
    }
    return (package_name, *aliases.get(package_name, ()))


def _blockers(
    module_imports: dict[str, dict[str, Any]],
    packages: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for module_name, status in sorted(module_imports.items()):
        if status.get("ok") is False:
            blockers.append(
                {
                    "kind": "module_import_failure",
                    "name": module_name,
                    "error_type": status.get("error_type"),
                    "error": status.get("error"),
                }
            )
    for package_name, status in sorted(packages.items()):
        if status.get("ok") is False:
            blockers.append(
                {
                    "kind": "missing_package",
                    "name": package_name,
                    "error_type": status.get("error_type"),
                    "error": status.get("error"),
                }
            )

    transformers = packages.get("transformers", {})
    torch = packages.get("torch", {})
    if transformers.get("ok") and torch.get("ok") and _torch_version_too_old(torch.get("version")):
        blockers.append(
            {
                "kind": "version_mismatch",
                "name": "torch",
                "requirement": "torch>=2.4 for this transformers build",
                "installed": torch.get("version"),
                "dependent": "transformers",
                "dependent_version": transformers.get("version"),
            }
        )
    return blockers


def _method_feasibility(
    module_imports: dict[str, dict[str, Any]],
    packages: dict[str, dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    bm25_modules = (
        "flashrag.dataset.dataset",
        "flashrag.retriever.retriever",
        "flashrag.retriever.index_builder",
    )
    bm25_feasible = all(module_imports.get(module, {}).get("ok") is True for module in bm25_modules)
    dense_required = ("torch", "transformers", "sentence_transformers", "faiss", "numpy")
    rerank_required = ("torch", "transformers", "FlagEmbedding", "sklearn", "numpy")
    dense_feasible = bm25_feasible and _packages_ok(packages, dense_required) and not _has_blocker(
        blockers,
        "version_mismatch",
        "torch",
    )
    reranker_feasible = _packages_ok(packages, rerank_required) and not _has_blocker(
        blockers,
        "version_mismatch",
        "torch",
    )
    return {
        "flashrag_bm25": {
            "feasible": bm25_feasible,
            "evidence": "Dataset, retriever, and index builder modules import successfully.",
        },
        "flashrag_dense": {
            "feasible": dense_feasible,
            "required_packages": list(dense_required),
            "evidence": _method_evidence(dense_feasible, dense_required, packages, blockers),
        },
        "flashrag_reranker": {
            "feasible": reranker_feasible,
            "required_packages": list(rerank_required),
            "evidence": _method_evidence(reranker_feasible, rerank_required, packages, blockers),
        },
    }


def _packages_ok(packages: dict[str, dict[str, Any]], names: tuple[str, ...]) -> bool:
    return all(packages.get(name, {}).get("ok") is True for name in names)


def _has_blocker(blockers: list[dict[str, Any]], kind: str, name: str) -> bool:
    return any(blocker.get("kind") == kind and blocker.get("name") == name for blocker in blockers)


def _method_evidence(
    feasible: bool,
    required_packages: tuple[str, ...],
    packages: dict[str, dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> str:
    if feasible:
        return "Required runtime packages are importable in the current environment."
    missing = [
        package_name
        for package_name in required_packages
        if packages.get(package_name, {}).get("ok") is not True
    ]
    if missing:
        return "Blocked by missing packages: " + ", ".join(missing)
    mismatch = [
        blocker
        for blocker in blockers
        if blocker.get("kind") == "version_mismatch"
    ]
    if mismatch:
        return "Blocked by runtime version mismatch: " + ", ".join(
            str(blocker.get("requirement")) for blocker in mismatch
        )
    return "Blocked by current FlashRAG module import failures."


def _recommendation(methods: dict[str, dict[str, Any]]) -> dict[str, str]:
    if methods["flashrag_dense"]["feasible"] and methods["flashrag_reranker"]["feasible"]:
        return {
            "next_step": "run_dense_and_reranker",
            "rationale": "The current environment has the required dense/rerank dependencies.",
        }
    return {
        "next_step": "keep_bm25_and_calibration_first",
        "rationale": (
            "BM25 is available enough for current experiments; dense/rerank should wait "
            "for an isolated dependency plan instead of mutating this environment blindly."
        ),
    }


def _torch_version_too_old(version: Any) -> bool:
    if not isinstance(version, str):
        return False
    parts = []
    for raw_part in version.split("+", 1)[0].split("."):
        if raw_part.isdigit():
            parts.append(int(raw_part))
        else:
            digits = "".join(char for char in raw_part if char.isdigit())
            if digits:
                parts.append(int(digits))
    if len(parts) < 2:
        return False
    return (parts[0], parts[1]) < (2, 4)


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
