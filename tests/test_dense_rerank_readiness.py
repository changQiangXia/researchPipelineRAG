from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.errors import ValidationError


def _load_generator():
    try:
        from domainrag.dense_rerank_readiness import generate_dense_rerank_readiness
    except ModuleNotFoundError:
        pytest.fail("domainrag.dense_rerank_readiness.generate_dense_rerank_readiness should be importable")
    return generate_dense_rerank_readiness


def _write_feasibility(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "flashrag_path": "benchmark/flashrag-fork",
                "flashrag_commit": "abc123",
                "generated_at": "2026-06-28T00:00:00+00:00",
                "packages": {
                    "torch": {"ok": True, "version": "2.1.2+cu121"},
                    "transformers": {"ok": True, "version": "5.12.1"},
                    "sentence_transformers": {"ok": False, "version": None},
                    "FlagEmbedding": {"ok": False, "version": None},
                    "sklearn": {"ok": False, "version": None},
                    "faiss": {"ok": True, "version": "1.14.3"},
                    "numpy": {"ok": True, "version": "1.26.3"},
                },
                "blockers": [
                    {
                        "kind": "missing_package",
                        "name": "sentence_transformers",
                    },
                    {
                        "kind": "missing_package",
                        "name": "FlagEmbedding",
                    },
                    {
                        "kind": "version_mismatch",
                        "name": "torch",
                        "requirement": "torch>=2.4 for this transformers build",
                        "installed": "2.1.2+cu121",
                    },
                ],
                "methods": {
                    "flashrag_bm25": {"feasible": True},
                    "flashrag_dense": {"feasible": False},
                    "flashrag_reranker": {"feasible": False},
                },
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def test_generate_dense_rerank_readiness_turns_feasibility_into_isolated_plan(tmp_path: Path):
    generate_dense_rerank_readiness = _load_generator()
    feasibility = tmp_path / "feasibility.json"
    output = tmp_path / "readiness"
    _write_feasibility(feasibility)

    markdown_path, json_path = generate_dense_rerank_readiness(feasibility, output)

    manifest = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert json_path == output / "readiness.json"
    assert markdown_path == output / "summary.md"
    assert manifest["phase"] == "Phase 7A"
    assert manifest["source_feasibility_manifest"] == str(feasibility)
    assert manifest["current_environment"]["safe_to_mutate"] is False
    assert manifest["current_environment"]["decision"] == "use_isolated_environment"
    assert manifest["current_environment"]["blocker_count"] == 3
    assert manifest["isolated_environment"]["python"] == "3.10"
    assert "torch>=2.4" in manifest["isolated_environment"]["pip_requirements"]
    assert any(
        requirement.startswith("sentence-transformers")
        for requirement in manifest["isolated_environment"]["pip_requirements"]
    )
    assert any(
        requirement.startswith("FlagEmbedding")
        for requirement in manifest["isolated_environment"]["pip_requirements"]
    )
    assert manifest["target_methods"] == [
        "flashrag_dense",
        "flashrag_reranker",
        "flashrag_bm25_plus_reranker",
    ]
    assert manifest["acceptance_gates"][0]["command"].startswith("PYTHONPATH=benchmark")
    assert any(gate["name"] == "medium_dense_retrieval_smoke" for gate in manifest["acceptance_gates"])
    assert "Do not install these dependencies into the current AutoDL environment" in markdown
    assert "flashrag_bm25_plus_reranker" in markdown


def test_generate_dense_rerank_readiness_rejects_missing_feasibility_manifest(tmp_path: Path):
    generate_dense_rerank_readiness = _load_generator()

    with pytest.raises(ValidationError) as exc:
        generate_dense_rerank_readiness(tmp_path / "missing.json", tmp_path / "out")

    assert "file does not exist" in str(exc.value)


def test_generate_dense_rerank_readiness_requires_method_section(tmp_path: Path):
    generate_dense_rerank_readiness = _load_generator()
    feasibility = tmp_path / "bad.json"
    feasibility.write_text('{"blockers": []}\n', encoding="utf-8")

    with pytest.raises(ValidationError) as exc:
        generate_dense_rerank_readiness(feasibility, tmp_path / "out")

    assert "methods must be an object" in str(exc.value)
