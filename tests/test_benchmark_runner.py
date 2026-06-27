from pathlib import Path

from domainrag.benchmark_runner import run_benchmark
from tests.test_validator import _write_minimal_dataset


def test_run_benchmark_writes_outputs(tmp_path: Path):
    dataset = tmp_path / "dataset"
    output = tmp_path / "outputs"
    _write_minimal_dataset(dataset)

    result_path = run_benchmark(dataset, output, methods=["no_rag", "mock_rag"], split="dev")

    assert result_path.exists()
    text = result_path.read_text(encoding="utf-8")
    assert '"method": "no_rag"' in text
    assert '"method": "mock_rag"' in text
    assert '"scores"' in text
