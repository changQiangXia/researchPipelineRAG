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


def test_current_docs_explain_local_baseline_and_flashrag_boundaries():
    benchmark = (OUTPUTS / "current" / "benchmark_results.md").read_text(
        encoding="utf-8"
    )
    flashrag_bundle = (OUTPUTS / "current" / "flashrag_bundle.md").read_text(
        encoding="utf-8"
    )
    status_report = (
        ROOT / "docs" / "reports" / "domainrag-medium-pilot-final-report.md"
    ).read_text(encoding="utf-8")

    assert "本表的 `api_calls` 只统计外部模型/API 调用" in benchmark
    assert "不包含 DeepSeek live answer/Judge" in benchmark
    assert "兼容数据包" in flashrag_bundle
    assert "不是完整 FlashRAG neural dense/reranker 实验" in flashrag_bundle
    assert status_report.startswith("# DomainRAG-Bench Medium Pilot Status Report")
    assert "不是 human-final benchmark" in status_report[:1200]


def test_real_dataset_cards_keep_human_final_boundary_clear():
    dataset_cards = [
        ROOT / "data" / "real_pilot_nickel_superalloy" / "dataset_card.md",
        ROOT / "data" / "real_pilot_nickel_superalloy_expanded" / "dataset_card.md",
        ROOT / "data" / "real_pilot_nickel_superalloy_medium" / "dataset_card.md",
        ROOT / "data" / "real_pilot_nickel_superalloy_medium_plus" / "dataset_card.md",
        ROOT
        / "data"
        / "real_pilot_nickel_superalloy_demo_questions"
        / "dataset_card.md",
    ]

    for card in dataset_cards:
        text = card.read_text(encoding="utf-8")
        assert "not a human-final benchmark" in text
        assert "Final use requires real human source sign-off" in text
