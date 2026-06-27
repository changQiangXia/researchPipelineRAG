from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.flashrag_runtime_intake import verify_flashrag_runtime_intake


def _write_fake_flashrag(root: Path) -> None:
    package = root / "flashrag"
    dataset = package / "dataset"
    config = package / "config"
    dataset.mkdir(parents=True)
    config.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (dataset / "__init__.py").write_text("", encoding="utf-8")
    (config / "__init__.py").write_text("", encoding="utf-8")
    (dataset / "dataset.py").write_text(
        "\n".join(
            [
                "import json",
                "",
                "class Item:",
                "    def __init__(self, data):",
                "        self.id = data.get('id')",
                "        self.question = data.get('question')",
                "        self.golden_answers = data.get('golden_answers', [])",
                "        self.metadata = data.get('metadata', {})",
                "",
                "class Dataset:",
                "    def __init__(self, config=None, dataset_path=None):",
                "        self.config = config or {}",
                "        self.data = []",
                "        with open(dataset_path, encoding='utf-8') as handle:",
                "            for line in handle:",
                "                if line.strip():",
                "                    self.data.append(Item(json.loads(line)))",
                "    def __len__(self):",
                "        return len(self.data)",
                "    @property",
                "    def id(self):",
                "        return [item.id for item in self.data]",
                "    @property",
                "    def golden_answers(self):",
                "        return [item.golden_answers for item in self.data]",
                "    def __getitem__(self, index):",
                "        return self.data[index]",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (config / "config.py").write_text("class Config: pass\n", encoding="utf-8")


def _write_bundle(root: Path) -> None:
    (root / "qrels").mkdir(parents=True)
    for split in ["dev", "fresh_hard"]:
        (root / f"{split}.jsonl").write_text(
            json.dumps(
                {
                    "id": f"q_{split}",
                    "question": f"{split} question",
                    "golden_answers": ["A"],
                    "metadata": {"question_type": "single_choice"},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "qrels" / f"{split}.tsv").write_text(
            f"q_{split}\td_{split}\t1\n",
            encoding="utf-8",
        )
    (root / "corpus.jsonl").write_text(
        '{"id":"d_dev","contents":"dev context"}\n',
        encoding="utf-8",
    )


def test_verify_flashrag_runtime_intake_loads_dataset_splits(tmp_path: Path):
    flashrag = tmp_path / "flashrag-fork"
    bundle = tmp_path / "bundle"
    output = tmp_path / "manifest.json"
    _write_fake_flashrag(flashrag)
    _write_bundle(bundle)

    manifest = verify_flashrag_runtime_intake(
        flashrag,
        bundle,
        dataset_name="unit_domain",
        splits=("dev", "fresh_hard"),
        output_path=output,
    )

    assert output.exists()
    assert manifest["dataset_name"] == "unit_domain"
    assert manifest["module_imports"]["flashrag.dataset.dataset"]["ok"] is True
    assert manifest["module_imports"]["flashrag.config.config"]["ok"] is True
    assert manifest["module_imports"]["flashrag.utils.utils"]["ok"] is False
    assert manifest["splits"]["dev"]["records"] == 1
    assert manifest["splits"]["fresh_hard"]["first_id"] == "q_fresh_hard"
    assert manifest["qrels"]["dev"]["rows"] == 1


def test_verify_flashrag_runtime_intake_rejects_missing_split_file(tmp_path: Path):
    flashrag = tmp_path / "flashrag-fork"
    bundle = tmp_path / "bundle"
    _write_fake_flashrag(flashrag)
    _write_bundle(bundle)

    with pytest.raises(ValidationError) as exc:
        verify_flashrag_runtime_intake(
            flashrag,
            bundle,
            dataset_name="unit_domain",
            splits=("dev", "test"),
        )

    assert "test.jsonl" in str(exc.value)
