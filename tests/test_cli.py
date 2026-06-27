import os
import subprocess
import sys
from pathlib import Path

from domainrag.cli import main
from domainrag.io_utils import write_jsonl
from tests.test_validator import _write_minimal_dataset


ROOT = Path(__file__).resolve().parents[1]


def _run_cli(*args: str, dataset: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = "benchmark"
    return subprocess.run(
        [sys.executable, "-m", "domainrag.cli", *args, "--dataset", str(dataset)],
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

    result = _run_cli("validate-data", dataset=tmp_path)

    assert result.returncode == 0
    assert "is valid" in result.stdout


def test_validate_data_module_entrypoint_rejects_missing_qrels(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    (tmp_path / "qrels" / "test.tsv").unlink()

    result = _run_cli("validate-data", dataset=tmp_path)

    assert result.returncode == 1
    assert "test.tsv" in result.stdout


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
