from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.io_utils import read_jsonl, read_qrels
from domainrag.validator import validate_dataset


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


def _write_minimal_dataset(root: Path) -> None:
    (root / "qrels").mkdir(parents=True)
    (root / "corpus.jsonl").write_text(
        '{"id":"d000001","contents":"Topic\\nSupported fact one."}\n'
        '{"id":"d000002","contents":"Topic\\nSupported fact two."}\n'
        '{"id":"d000003","contents":"Topic\\nSupported fact three."}\n',
        encoding="utf-8",
    )
    import json

    def canonical_item(question_id: str, chunk_id: str, answer: str) -> dict:
        return {
            "id": question_id,
            "question_type": "single_choice",
            "question": f"Which option is {answer}?",
            "options": {"A": "Unsupported", "B": answer, "C": "Other", "D": "None"},
            "answer": ["B"],
            "answer_aliases": [],
            "reference_answer": answer,
            "required_points": [],
            "source_chunk_ids": [chunk_id],
            "subdomain": "demo",
            "knowledge_type": "fact",
            "difficulty": "easy",
            "quality_score": 1.0,
        }

    canonical = [
        canonical_item("q000001", "d000001", "Supported fact one"),
        canonical_item("q000002", "d000002", "Supported fact two"),
        canonical_item("q000003", "d000003", "Supported fact three"),
    ]

    def flashrag_item(item: dict) -> dict:
        metadata = {
            "question_type": item["question_type"],
            "source_chunk_ids": item["source_chunk_ids"],
            "knowledge_type": item["knowledge_type"],
            "difficulty": item["difficulty"],
            "answer_aliases": item["answer_aliases"],
            "required_points": item["required_points"],
        }
        if item["question_type"] in {"single_choice", "multiple_choice"}:
            metadata["correct_options"] = item["answer"]
        return {
            "id": item["id"],
            "question": f"{item['question']}\nA. Unsupported\nB. {item['reference_answer']}\nC. Other\nD. None",
            "golden_answers": item["answer"],
            "metadata": metadata,
        }

    (root / "canonical_dataset.jsonl").write_text(
        "".join(json.dumps(item) + "\n" for item in canonical),
        encoding="utf-8",
    )
    split_map = {
        "dev": canonical[0],
        "test": canonical[1],
        "fresh_hard_test": canonical[2],
    }
    qrels_map = {
        "dev": ("q000001", "d000001"),
        "test": ("q000002", "d000002"),
        "fresh_hard": ("q000003", "d000003"),
    }
    for split, item in split_map.items():
        (root / f"{split}.jsonl").write_text(
            json.dumps(flashrag_item(item)) + "\n",
            encoding="utf-8",
        )
    for name, (query_id, corpus_id) in qrels_map.items():
        (root / "qrels" / f"{name}.tsv").write_text(
            f"{query_id}\t{corpus_id}\t1\n",
            encoding="utf-8",
        )


def test_validate_dataset_accepts_minimal_dataset(tmp_path: Path):
    _write_minimal_dataset(tmp_path)

    validate_dataset(tmp_path)


def test_validate_dataset_rejects_missing_qrels(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    (tmp_path / "qrels" / "test.tsv").unlink()

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    assert "test.tsv" in str(exc.value)


def test_validate_dataset_rejects_non_string_split_id(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    (tmp_path / "dev.jsonl").write_text(
        '{"id":[],"question":"Which option is Supported fact one?\\nA. Unsupported\\nB. Supported fact one\\nC. Other\\nD. None","golden_answers":["B"],"metadata":{"question_type":"single_choice","correct_options":["B"],"source_chunk_ids":["d000001"],"knowledge_type":"fact","difficulty":"easy","answer_aliases":[],"required_points":[]}}\n',
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    assert "record 1: id must be a string" in str(exc.value)


def test_validate_dataset_rejects_forbidden_public_metadata_fields(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    corpus_path = tmp_path / "corpus.jsonl"
    corpus = read_jsonl(corpus_path)
    corpus[0]["metadata"] = {"authors": ["Hidden"], "nested": {"doi": "10.1/demo"}}
    import json

    corpus_path.write_text(
        "".join(json.dumps(record) + "\n" for record in corpus),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    message = str(exc.value)
    assert "forbidden field" in message
    assert "authors" in message
    assert "doi" in message


def test_validate_dataset_rejects_split_records_that_drift_from_canonical(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    dev_path = tmp_path / "dev.jsonl"
    dev_records = read_jsonl(dev_path)
    dev_records[0]["golden_answers"] = ["A"]
    dev_records[0]["metadata"]["difficulty"] = "hard"
    dev_records[0]["metadata"]["source_chunk_ids"] = ["d000999"]
    dev_records[0]["metadata"]["correct_options"] = ["A"]
    import json

    dev_path.write_text(
        "".join(json.dumps(record) + "\n" for record in dev_records),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    message = str(exc.value)
    assert "golden_answers must match canonical answer" in message
    assert "metadata.difficulty must match canonical difficulty" in message
    assert "metadata.source_chunk_ids must match canonical source_chunk_ids" in message
    assert "metadata.correct_options must match canonical answer" in message


def test_validate_dataset_rejects_split_metadata_shape_mismatches(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    dev_path = tmp_path / "dev.jsonl"
    dev_records = read_jsonl(dev_path)
    del dev_records[0]["metadata"]["required_points"]
    dev_records[0]["metadata"]["unexpected"] = "value"
    import json

    dev_path.write_text(
        "".join(json.dumps(record) + "\n" for record in dev_records),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    message = str(exc.value)
    assert "metadata: missing fields ['required_points']" in message
    assert "metadata: unexpected fields ['unexpected']" in message


def test_validate_dataset_rejects_multiple_choice_with_wrong_option_keys(tmp_path: Path):
    _write_minimal_dataset(tmp_path)
    canonical_path = tmp_path / "canonical_dataset.jsonl"
    canonical = read_jsonl(canonical_path)
    canonical[0]["question_type"] = "multiple_choice"
    canonical[0]["options"] = {
        "A": "Supported fact one",
        "B": "Distractor one",
        "C": "Distractor two",
        "D": "Distractor three",
        "G": "Distractor four",
    }
    canonical[0]["answer"] = ["A", "G"]
    import json

    canonical_path.write_text(
        "".join(json.dumps(record) + "\n" for record in canonical),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    assert "multiple_choice requires A-E or A-F options" in str(exc.value)


def test_validate_dataset_rejects_choice_options_with_blank_or_non_string_values(
    tmp_path: Path,
):
    _write_minimal_dataset(tmp_path)
    canonical_path = tmp_path / "canonical_dataset.jsonl"
    canonical = read_jsonl(canonical_path)
    canonical[0]["options"]["B"] = ""
    canonical[0]["options"]["C"] = 3
    import json

    canonical_path.write_text(
        "".join(json.dumps(record) + "\n" for record in canonical),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        validate_dataset(tmp_path)

    message = str(exc.value)
    assert "option B must be a non-empty string" in message
    assert "option C must be a non-empty string" in message
