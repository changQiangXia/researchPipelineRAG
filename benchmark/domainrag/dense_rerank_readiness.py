from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from domainrag.errors import ValidationError, ValidationIssue


PIP_REQUIREMENTS = [
    "torch>=2.4",
    "transformers>=4.40,<5",
    "sentence-transformers>=3.0",
    "FlagEmbedding>=1.3",
    "scikit-learn>=1.4",
    "faiss-cpu>=1.8",
    "numpy>=1.26,<2",
    "termcolor>=2.4",
    "openai>=1.40",
]

TARGET_METHODS = [
    "flashrag_dense",
    "flashrag_reranker",
    "flashrag_bm25_plus_reranker",
]


def generate_dense_rerank_readiness(
    feasibility_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    feasibility = _read_json_object(feasibility_path)
    methods = feasibility.get("methods")
    if not isinstance(methods, dict):
        raise ValidationError(
            [ValidationIssue(str(feasibility_path), "methods must be an object")]
        )

    blockers = feasibility.get("blockers", [])
    if not isinstance(blockers, list):
        raise ValidationError(
            [ValidationIssue(str(feasibility_path), "blockers must be an array")]
        )
    packages = feasibility.get("packages", {})
    if not isinstance(packages, dict):
        raise ValidationError(
            [ValidationIssue(str(feasibility_path), "packages must be an object")]
        )

    manifest = _build_manifest(feasibility_path, feasibility, methods, blockers, packages)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "readiness.json"
    markdown_path = output_dir / "summary.md"
    json_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(manifest), encoding="utf-8")
    return markdown_path, json_path


def _read_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValidationError([ValidationIssue(str(path), "file does not exist")])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(
            [ValidationIssue(str(path), f"invalid JSON: {exc.msg}")]
        ) from exc
    if not isinstance(data, dict):
        raise ValidationError([ValidationIssue(str(path), "JSON root must be an object")])
    return data


def _build_manifest(
    feasibility_path: Path,
    feasibility: dict[str, Any],
    methods: dict[str, Any],
    blockers: list[Any],
    packages: dict[str, Any],
) -> dict[str, Any]:
    dense_feasible = _method_feasible(methods, "flashrag_dense")
    reranker_feasible = _method_feasible(methods, "flashrag_reranker")
    safe_to_mutate = False
    decision = "current_environment_ready" if dense_feasible and reranker_feasible else "use_isolated_environment"
    return {
        "phase": "Phase 7A",
        "source_feasibility_manifest": str(feasibility_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "current_environment": {
            "safe_to_mutate": safe_to_mutate,
            "decision": decision,
            "blocker_count": len(blockers),
            "blockers": blockers,
            "observed_packages": _observed_packages(packages),
            "rationale": (
                "Do not mutate the current AutoDL environment because dense/rerank "
                "requires model-backed packages and PyTorch/transformers changes."
            ),
        },
        "isolated_environment": {
            "python": "3.10",
            "manager": "venv or conda",
            "pip_requirements": PIP_REQUIREMENTS,
            "environment_variables": [
                "PYTHONPATH=benchmark",
                "FLASHRAG_HOME=<path-to-flashrag-fork>",
                "DEEPSEEK_API_KEY=<only needed for generated-answer evaluation>",
            ],
            "creation_commands": [
                "python3.10 -m venv .venvs/flashrag-dense",
                ". .venvs/flashrag-dense/bin/activate",
                "python -m pip install --upgrade pip",
                "python -m pip install -r requirements/flashrag-dense-rerank.txt",
            ],
            "requirements_file": "requirements/flashrag-dense-rerank.txt",
        },
        "target_methods": TARGET_METHODS,
        "acceptance_gates": _acceptance_gates(),
        "source_manifest_summary": {
            "flashrag_path": feasibility.get("flashrag_path"),
            "flashrag_commit": feasibility.get("flashrag_commit"),
            "flashrag_bm25_feasible": _method_feasible(methods, "flashrag_bm25"),
            "flashrag_dense_feasible": dense_feasible,
            "flashrag_reranker_feasible": reranker_feasible,
        },
        "recommendation": {
            "next_step": "build_isolated_dense_rerank_environment",
            "rationale": (
                "BM25 and lexical already separate on the medium pilot. Dense/rerank "
                "should be evaluated next only inside a dependency-isolated environment."
            ),
        },
    }


def _method_feasible(methods: dict[str, Any], name: str) -> bool:
    method = methods.get(name)
    return isinstance(method, dict) and method.get("feasible") is True


def _observed_packages(packages: dict[str, Any]) -> dict[str, Any]:
    names = [
        "torch",
        "transformers",
        "sentence_transformers",
        "FlagEmbedding",
        "sklearn",
        "faiss",
        "numpy",
    ]
    return {
        name: packages.get(name, {"ok": False, "version": None})
        for name in names
    }


def _acceptance_gates() -> list[dict[str, str]]:
    return [
        {
            "name": "install_isolated_requirements",
            "command": (
                "PYTHONPATH=benchmark python -m domainrag.cli dense-rerank-readiness "
                "--feasibility outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/flashrag_method_feasibility/"
                "real_pilot_nickel_superalloy_manifest.json "
                "--output outputs/archive/provenance/retrieval-diagnostics/dense-rerank-readiness/dense_rerank_readiness"
            ),
            "expected": "readiness.json and summary.md are regenerated without mutating the base env",
        },
        {
            "name": "flashrag_dense_import_probe",
            "command": (
                "PYTHONPATH=benchmark python -m domainrag.cli probe-flashrag-methods "
                "--flashrag-path benchmark/flashrag-fork "
                "--output outputs/archive/provenance/retrieval-diagnostics/dense-rerank-readiness/dense_rerank_readiness/isolated_feasibility.json"
            ),
            "expected": "flashrag_dense and flashrag_reranker become feasible in the isolated env",
        },
        {
            "name": "medium_dense_retrieval_smoke",
            "command": (
                "PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag "
                "--dataset data/real_pilot_nickel_superalloy_medium "
                "--output outputs/flashrag "
                "--dataset-name real_pilot_nickel_superalloy_medium"
            ),
            "expected": "medium FlashRAG bundle remains valid before dense/rerank runs",
        },
        {
            "name": "medium_dataset_validation",
            "command": (
                "PYTHONPATH=benchmark python -m domainrag.cli validate-data "
                "--dataset data/real_pilot_nickel_superalloy_medium"
            ),
            "expected": "dataset is valid",
        },
        {
            "name": "regression_tests",
            "command": "PYTHONPATH=benchmark pytest",
            "expected": "all tests pass in the base repository and isolated env-specific tests pass separately",
        },
    ]


def _render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Dense/Rerank Isolated Readiness",
        "",
        f"Phase: {manifest['phase']}",
        "",
        "## Decision",
        "",
        "Do not install these dependencies into the current AutoDL environment.",
        "",
        f"- Current decision: `{manifest['current_environment']['decision']}`",
        f"- Safe to mutate current environment: {manifest['current_environment']['safe_to_mutate']}",
        f"- Blocker count: {manifest['current_environment']['blocker_count']}",
        "",
        "## Target Methods",
        "",
    ]
    for method in manifest["target_methods"]:
        lines.append(f"- `{method}`")
    lines.extend(["", "## Isolated Environment", ""])
    lines.append(f"- Python: {manifest['isolated_environment']['python']}")
    lines.append(f"- Requirements file: `{manifest['isolated_environment']['requirements_file']}`")
    lines.append("- Pip requirements:")
    for requirement in manifest["isolated_environment"]["pip_requirements"]:
        lines.append(f"  - `{requirement}`")
    lines.extend(["", "## Acceptance Gates", ""])
    for gate in manifest["acceptance_gates"]:
        lines.extend(
            [
                f"### {gate['name']}",
                "",
                "```bash",
                gate["command"],
                "```",
                "",
                f"Expected: {gate['expected']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Recommendation",
            "",
            manifest["recommendation"]["rationale"],
            "",
        ]
    )
    return "\n".join(lines)
