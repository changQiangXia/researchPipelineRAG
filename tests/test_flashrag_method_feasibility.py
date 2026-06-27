from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.flashrag_method_feasibility import probe_flashrag_method_feasibility


def _write_fake_flashrag(root: Path) -> None:
    package = root / "flashrag"
    dataset = package / "dataset"
    retriever = package / "retriever"
    pipeline = package / "pipeline"
    generator = package / "generator"
    for path in [package, dataset, retriever, pipeline, generator]:
        path.mkdir(parents=True, exist_ok=True)
        (path / "__init__.py").write_text("", encoding="utf-8")
    (dataset / "dataset.py").write_text("class Dataset: pass\n", encoding="utf-8")
    (retriever / "retriever.py").write_text("class BM25Retriever: pass\n", encoding="utf-8")
    (retriever / "index_builder.py").write_text("class Index_Builder: pass\n", encoding="utf-8")
    (pipeline / "pipeline.py").write_text(
        "import missing_pipeline_dependency\n",
        encoding="utf-8",
    )
    (generator / "generator.py").write_text(
        "import missing_generator_dependency\n",
        encoding="utf-8",
    )


def test_probe_flashrag_method_feasibility_records_imports_and_blockers(tmp_path: Path):
    flashrag = tmp_path / "flashrag-fork"
    output = tmp_path / "manifest.json"
    _write_fake_flashrag(flashrag)

    manifest = probe_flashrag_method_feasibility(
        flashrag,
        output_path=output,
        package_names=("json", "definitely_missing_dense_dep"),
    )

    assert output.exists()
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written == manifest
    assert manifest["flashrag_path"] == str(flashrag)
    assert manifest["module_imports"]["flashrag.dataset.dataset"]["ok"] is True
    assert manifest["module_imports"]["flashrag.retriever.retriever"]["ok"] is True
    assert manifest["module_imports"]["flashrag.retriever.index_builder"]["ok"] is True
    assert manifest["module_imports"]["flashrag.pipeline.pipeline"]["ok"] is False
    assert (
        manifest["module_imports"]["flashrag.pipeline.pipeline"]["error_type"]
        == "ModuleNotFoundError"
    )
    assert manifest["packages"]["json"]["ok"] is True
    assert manifest["packages"]["definitely_missing_dense_dep"]["ok"] is False
    assert manifest["methods"]["flashrag_bm25"]["feasible"] is True
    assert manifest["methods"]["flashrag_dense"]["feasible"] is False
    assert manifest["methods"]["flashrag_reranker"]["feasible"] is False
    assert any(
        blocker["kind"] == "missing_package"
        and blocker["name"] == "definitely_missing_dense_dep"
        for blocker in manifest["blockers"]
    )
    assert manifest["recommendation"]["next_step"] == "keep_bm25_and_calibration_first"


def test_probe_flashrag_method_feasibility_rejects_missing_flashrag_checkout(tmp_path: Path):
    with pytest.raises(ValidationError) as exc:
        probe_flashrag_method_feasibility(tmp_path / "missing")

    assert "FlashRAG package directory missing" in str(exc.value)
