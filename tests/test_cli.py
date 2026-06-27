from domainrag.cli import main


def test_version_command(capsys):
    exit_code = main(["version"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "domainrag-bench 0.1.0" in captured.out
