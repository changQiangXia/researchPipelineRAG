from pathlib import Path

from domainrag.cli import main
from tests.test_validator import _write_minimal_dataset


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
