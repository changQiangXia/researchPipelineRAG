from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
PROVENANCE = OUTPUTS / "archive" / "provenance"


def _collect_paths(value: object) -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for nested in value.values():
            paths.extend(_collect_paths(nested))
    elif isinstance(value, list):
        for nested in value:
            paths.extend(_collect_paths(nested))
    elif isinstance(value, str) and value.startswith("outputs/"):
        paths.append(value)
    return paths


def test_outputs_hides_historical_phase_directories():
    phase_dirs = sorted(
        path.relative_to(OUTPUTS).as_posix()
        for path in OUTPUTS.rglob("phase*")
        if path.is_dir()
    )

    assert phase_dirs == []
    assert (OUTPUTS / "README.md").exists()
    assert (OUTPUTS / "current" / "README.md").exists()
    assert (OUTPUTS / "archive" / "README.md").exists()
    assert (PROVENANCE / "demo-dataset" / "demo-question-generation").exists()
    assert (PROVENANCE / "source-workflow" / "full-text-chunk-extraction").exists()
    assert (PROVENANCE / "source-workflow" / "human-signoff").exists()


def test_outputs_archive_keeps_key_evidence_paths_resolvable():
    audit = json.loads(
        (ROOT / "docs" / "reports" / "rag-md-implementation-audit.json").read_text(
            encoding="utf-8"
        )
    )
    output_paths = sorted(set(_collect_paths(audit)))
    key_paths = [
        "outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/demo_question_summary.json",
        "outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.json",
        "outputs/archive/provenance/source-workflow/human-signoff/human_signoff/human_signoff_summary.json",
        "outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/report_fresh_hard/summary.json",
    ]

    for path in key_paths:
        assert path in output_paths
        assert (ROOT / path).exists()


def test_outputs_guidance_points_readers_to_current_before_archive():
    outputs_readme = (OUTPUTS / "README.md").read_text(encoding="utf-8")
    current_readme = (OUTPUTS / "current" / "README.md").read_text(encoding="utf-8")

    assert "先看 current" in outputs_readme
    assert "archive/provenance" in outputs_readme
    assert "历史运行记录" in outputs_readme
    assert "provisional" in current_readme
    assert "human-final" in current_readme
