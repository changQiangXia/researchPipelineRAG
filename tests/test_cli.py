import os
import subprocess
import sys
from pathlib import Path

from domainrag.cli import main
from domainrag.io_utils import write_jsonl
from tests.test_flashrag_bm25_bridge import (
    _write_bundle as _write_flashrag_bm25_bundle,
)
from tests.test_flashrag_bm25_bridge import (
    _write_fake_flashrag as _write_fake_flashrag_bm25_package,
)
from tests.test_validator import _write_minimal_dataset


ROOT = Path(__file__).resolve().parents[1]


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = "benchmark"
    return subprocess.run(
        [sys.executable, "-m", "domainrag.cli", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def test_version_command(capsys):
    exit_code = main(["version"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "domainrag-bench 0.1.0" in captured.out


def test_validate_data_command(tmp_path: Path, capsys):
    _write_minimal_dataset(tmp_path)

    exit_code = main(["validate-data", "--dataset", str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "valid" in captured.out


def test_validate_data_module_entrypoint_accepts_valid_dataset(tmp_path: Path):
    _write_minimal_dataset(tmp_path)

    result = _run_cli("validate-data", "--dataset", str(tmp_path))

    assert result.returncode == 0
    assert "is valid" in result.stdout


def test_validate_data_module_entrypoint_rejects_missing_qrels(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    (tmp_path / "qrels" / "test.tsv").unlink()

    result = _run_cli("validate-data", "--dataset", str(tmp_path))

    assert result.returncode == 1
    assert "test.tsv" in result.stdout


def test_prepare_flashrag_module_entrypoint_writes_bundle_and_config(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    result = _run_cli(
        "prepare-flashrag",
        "--dataset",
        str(dataset),
        "--output",
        str(output),
        "--dataset-name",
        "example_domain",
    )

    assert result.returncode == 0
    assert "FlashRAG bundle written to" in result.stdout
    assert "FlashRAG config written to" in result.stdout
    assert (output / "example_domain" / "fresh_hard.jsonl").exists()


def test_prepare_flashrag_module_entrypoint_rejects_invalid_fixture(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    (dataset / "fresh_hard_test.jsonl").unlink()

    result = _run_cli(
        "prepare-flashrag",
        "--dataset",
        str(dataset),
        "--output",
        str(output),
        "--dataset-name",
        "example_domain",
    )

    assert result.returncode != 0


def test_prepare_flashrag_module_entrypoint_rejects_empty_splits(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    result = _run_cli(
        "prepare-flashrag",
        "--dataset",
        str(dataset),
        "--output",
        str(output),
        "--dataset-name",
        "example_domain",
        "--splits",
        ",",
    )

    assert result.returncode == 1
    assert "at least one split must be requested" in result.stdout


def test_export_domainrag_module_entrypoint_writes_valid_dataset(tmp_path: Path):
    fixture = ROOT / "fixtures" / "easy_dataset" / "example_export"
    output = tmp_path / "outputs"

    result = _run_cli(
        "export-domainrag",
        "--input",
        str(fixture),
        "--output",
        str(output),
        "--dataset-name",
        "example_easy_dataset",
    )

    assert result.returncode == 0
    assert "DomainRAG dataset written to" in result.stdout
    assert (output / "example_easy_dataset" / "canonical_dataset.jsonl").exists()


def test_prepare_flashrag_example_script_keeps_relative_config_path():
    result = subprocess.run(
        [sys.executable, "scripts/prepare_flashrag_example.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    config_text = (ROOT / "outputs" / "flashrag" / "example_domain_flashrag.yaml").read_text(
        encoding="utf-8"
    )
    assert config_text.startswith("data_dir: outputs/flashrag\n")


def test_run_command(tmp_path: Path, capsys):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    exit_code = main(
        [
            "run",
            "--dataset",
            str(dataset),
            "--output",
            str(output),
            "--methods",
            "no_rag,mock_rag",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "results written" in captured.out


def test_run_flashrag_bm25_command(tmp_path: Path, capsys):
    flashrag = tmp_path / "flashrag-fork"
    bundle = tmp_path / "bundle"
    output = tmp_path / "outputs"
    _write_fake_flashrag_bm25_package(flashrag)
    _write_flashrag_bm25_bundle(bundle)

    exit_code = main(
        [
            "run-flashrag-bm25",
            "--flashrag-path",
            str(flashrag),
            "--dataset-bundle",
            str(bundle),
            "--output",
            str(output),
            "--dataset-name",
            "unit_domain",
            "--split",
            "dev",
            "--top-k",
            "2",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "FlashRAG BM25 results written" in captured.out
    assert (output / "bundle" / "dev_flashrag_bm25_results.jsonl").exists()


def test_run_deepseek_answers_requires_api_key(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    env = os.environ.copy()
    env["PYTHONPATH"] = "benchmark"
    env.pop("DEEPSEEK_API_KEY", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "run-deepseek-answers",
            "--dataset",
            str(dataset),
            "--output",
            str(output),
            "--methods",
            "no_rag",
            "--split",
            "dev",
            "--limit",
            "1",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "DEEPSEEK_API_KEY is required" in result.stdout
    assert "Traceback" not in result.stdout
    assert "Traceback" not in result.stderr


def test_run_deepseek_answers_rejects_invalid_runtime_options(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    env = os.environ.copy()
    env["PYTHONPATH"] = "benchmark"
    env["DEEPSEEK_API_KEY"] = "test-key"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "run-deepseek-answers",
            "--dataset",
            str(dataset),
            "--output",
            str(output),
            "--methods",
            "no_rag",
            "--split",
            "dev",
            "--max-retries",
            "-1",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "max_retries must be non-negative" in result.stdout
    assert "Traceback" not in result.stdout
    assert "Traceback" not in result.stderr


def test_judge_deepseek_answers_requires_api_key(tmp_path: Path):
    dataset = tmp_path / "dataset"
    input_path = tmp_path / "answers.jsonl"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    write_jsonl(input_path, [])

    env = os.environ.copy()
    env["PYTHONPATH"] = "benchmark"
    env.pop("DEEPSEEK_API_KEY", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "judge-deepseek-answers",
            "--dataset",
            str(dataset),
            "--input",
            str(input_path),
            "--output",
            str(output),
            "--split",
            "dev",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "DEEPSEEK_API_KEY is required" in result.stdout
    assert "Traceback" not in result.stdout
    assert "Traceback" not in result.stderr


def test_judge_deepseek_answers_rejects_invalid_runtime_options(tmp_path: Path):
    dataset = tmp_path / "dataset"
    input_path = tmp_path / "answers.jsonl"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)
    write_jsonl(input_path, [])

    env = os.environ.copy()
    env["PYTHONPATH"] = "benchmark"
    env["DEEPSEEK_API_KEY"] = "test-key"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "domainrag.cli",
            "judge-deepseek-answers",
            "--dataset",
            str(dataset),
            "--input",
            str(input_path),
            "--output",
            str(output),
            "--split",
            "dev",
            "--max-retries",
            "-1",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "max_retries must be non-negative" in result.stdout
    assert "Traceback" not in result.stdout
    assert "Traceback" not in result.stderr


def test_judge_report_command_writes_summary(tmp_path: Path, capsys):
    input_path = tmp_path / "judge_results.jsonl"
    output = tmp_path / "report"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "oracle_context",
                "split": "dev",
                "judge": {
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 4.0,
                    "relevance": 5.0,
                    "unsupported_claims": [],
                    "reason": "good",
                },
                "judge_scores": {
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 4.0,
                    "relevance": 5.0,
                    "hallucination_risk": 1.0,
                },
                "latency_ms": 10.0,
                "input_tokens": 20,
                "output_tokens": 5,
                "api_calls": 1,
                "error": None,
            }
        ],
    )

    exit_code = main(["judge-report", "--input", str(input_path), "--output", str(output)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "judge report written" in captured.out
    assert (output / "summary.json").exists()


def test_report_command(tmp_path: Path, capsys):
    input_path = tmp_path / "results.jsonl"
    output_dir = tmp_path / "reports"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": {"single_choice_accuracy": 1.0},
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            }
        ],
    )

    exit_code = main(["report", "--input", str(input_path), "--output", str(output_dir)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "report written" in captured.out


def test_report_command_rejects_invalid_rows(tmp_path: Path, capsys):
    input_path = tmp_path / "results.jsonl"
    output_dir = tmp_path / "reports"
    write_jsonl(
        input_path,
        [
            {
                "id": "q1",
                "method": "mock_rag",
                "split": "dev",
                "scores": {"single_choice_accuracy": "bad"},
                "latency_ms": 10.0,
                "input_tokens": 5,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            }
        ],
    )

    exit_code = main(["report", "--input", str(input_path), "--output", str(output_dir)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "record 1: scores.single_choice_accuracy must be numeric" in captured.out
    assert "Traceback" not in captured.out
