import json
import os
import subprocess
import sys
from pathlib import Path

from domainrag.cli import main
from domainrag.io_utils import write_jsonl
from tests.test_calibration_packet import _answer_row as _calibration_answer_row
from tests.test_calibration_packet import _judge_row as _calibration_judge_row
from tests.test_flashrag_bm25_bridge import (
    _write_bundle as _write_flashrag_bm25_bundle,
)
from tests.test_flashrag_bm25_bridge import (
    _write_fake_flashrag as _write_fake_flashrag_bm25_package,
)
from tests.test_flashrag_method_feasibility import (
    _write_fake_flashrag as _write_fake_flashrag_feasibility_package,
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


def test_compare_command_writes_comparison_report(tmp_path: Path, capsys):
    answer_path = tmp_path / "answers.jsonl"
    judge_path = tmp_path / "judge.jsonl"
    output = tmp_path / "comparison"
    write_jsonl(
        answer_path,
        [
            {
                "id": "q1",
                "method": "method_a",
                "split": "fresh_hard",
                "prediction": "A",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": ["d1"],
                "scores": {
                    "single_choice_accuracy": 1.0,
                    "retrieval_hit": 1.0,
                },
                "latency_ms": 0.0,
                "input_tokens": 1,
                "output_tokens": 1,
                "api_calls": 0,
                "error": None,
            }
        ],
    )
    write_jsonl(
        judge_path,
        [
            {
                "id": "q1",
                "method": "method_a",
                "split": "fresh_hard",
                "prediction": "A",
                "golden_answers": ["A"],
                "gold_context_ids": ["d1"],
                "retrieved_context_ids": ["d1"],
                "judge": {
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 5.0,
                    "relevance": 5.0,
                    "unsupported_claims": [],
                    "reason": "ok",
                },
                "judge_scores": {
                    "correctness": 5.0,
                    "context_support": 5.0,
                    "faithfulness": 5.0,
                    "relevance": 5.0,
                    "hallucination_risk": 0.0,
                },
                "latency_ms": 0.0,
                "input_tokens": 2,
                "output_tokens": 1,
                "api_calls": 1,
                "error": None,
            }
        ],
    )

    exit_code = main(
        [
            "compare",
            "--answer-inputs",
            str(answer_path),
            "--judge-inputs",
            str(judge_path),
            "--output",
            str(output),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "comparison report written" in captured.out
    assert (output / "summary.md").exists()
    assert (output / "summary.json").exists()


def test_calibration_packet_command_writes_review_files(tmp_path: Path, capsys):
    dataset = tmp_path / "dataset"
    answers = tmp_path / "answers.jsonl"
    judge = tmp_path / "judge.jsonl"
    output = tmp_path / "packet"
    _write_minimal_dataset(dataset)
    write_jsonl(answers, [_calibration_answer_row()])
    write_jsonl(judge, [_calibration_judge_row()])

    exit_code = main(
        [
            "calibration-packet",
            "--dataset",
            str(dataset),
            "--answers",
            str(answers),
            "--judge",
            str(judge),
            "--output",
            str(output),
            "--split",
            "fresh_hard",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "calibration packet written" in captured.out
    assert (output / "review_packet.jsonl").exists()
    assert (output / "review_packet.md").exists()


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


def test_probe_flashrag_methods_command_writes_manifest(tmp_path: Path, capsys):
    flashrag = tmp_path / "flashrag-fork"
    output = tmp_path / "manifest.json"
    _write_fake_flashrag_feasibility_package(flashrag)

    exit_code = main(
        [
            "probe-flashrag-methods",
            "--flashrag-path",
            str(flashrag),
            "--output",
            str(output),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "FlashRAG method feasibility manifest written" in captured.out
    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["methods"]["flashrag_bm25"]["feasible"] is True


def test_verify_flashrag_method_feasibility_script_writes_manifest(tmp_path: Path):
    flashrag = tmp_path / "flashrag-fork"
    output = tmp_path / "manifest.json"
    _write_fake_flashrag_feasibility_package(flashrag)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/verify_flashrag_method_feasibility.py",
            "--flashrag-path",
            str(flashrag),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "FlashRAG method feasibility manifest written" in result.stdout
    assert json.loads(output.read_text(encoding="utf-8"))["methods"]["flashrag_bm25"][
        "feasible"
    ]


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


def test_run_deepseek_answers_accepts_flashrag_bm25_retrieval_results(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    retrieval_results = tmp_path / "flashrag_bm25_results.jsonl"
    _write_minimal_dataset(dataset)
    write_jsonl(
        retrieval_results,
        [
            {
                "id": "q000001",
                "method": "flashrag_bm25_oracle_reader",
                "split": "dev",
                "retrieved_context_ids": ["d000001"],
            }
        ],
    )

    captured = {}

    def fake_run_deepseek_answer_benchmark(
        dataset_dir,
        output_dir,
        methods,
        split,
        config,
        *,
        limit=None,
        retrieval_results_path=None,
    ):
        captured["dataset_dir"] = dataset_dir
        captured["output_dir"] = output_dir
        captured["methods"] = methods
        captured["split"] = split
        captured["limit"] = limit
        captured["retrieval_results_path"] = retrieval_results_path
        return output / "dataset" / "dev_deepseek_results.jsonl"

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(
        "domainrag.cli.run_deepseek_answer_benchmark",
        fake_run_deepseek_answer_benchmark,
    )

    exit_code = main(
        [
            "run-deepseek-answers",
            "--dataset",
            str(dataset),
            "--output",
            str(output),
            "--methods",
            "flashrag_bm25_live_deepseek",
            "--split",
            "dev",
            "--retrieval-results",
            str(retrieval_results),
            "--limit",
            "1",
        ]
    )
    stdout = capsys.readouterr().out

    assert exit_code == 0
    assert "DeepSeek answer results written" in stdout
    assert captured["methods"] == ["flashrag_bm25_live_deepseek"]
    assert captured["split"] == "dev"
    assert captured["limit"] == 1
    assert captured["retrieval_results_path"] == retrieval_results


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
