from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.io_utils import read_jsonl, read_qrels


def test_read_jsonl_reads_records(tmp_path: Path):
    path = tmp_path / "items.jsonl"
    path.write_text('{"id":"q1"}\n{"id":"q2"}\n', encoding="utf-8")

    assert read_jsonl(path) == [{"id": "q1"}, {"id": "q2"}]


def test_read_jsonl_reports_invalid_line(tmp_path: Path):
    path = tmp_path / "items.jsonl"
    path.write_text('{"id":"q1"}\nnot-json\n', encoding="utf-8")

    with pytest.raises(ValidationError) as exc:
        read_jsonl(path)

    assert "line 2" in str(exc.value)


def test_read_qrels_reads_rows(tmp_path: Path):
    path = tmp_path / "qrels.tsv"
    path.write_text("q1\td1\t1\nq1\td2\t1\n", encoding="utf-8")

    assert read_qrels(path) == [("q1", "d1", 1), ("q1", "d2", 1)]


def test_read_qrels_rejects_bad_score(tmp_path: Path):
    path = tmp_path / "qrels.tsv"
    path.write_text("q1\td1\tbad\n", encoding="utf-8")

    with pytest.raises(ValidationError) as exc:
        read_qrels(path)

    assert "score must be an integer" in str(exc.value)
