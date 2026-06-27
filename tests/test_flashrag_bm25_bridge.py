from __future__ import annotations

import json
from pathlib import Path

import pytest

from domainrag.errors import ValidationError
from domainrag.flashrag_bm25_bridge import run_flashrag_bm25_bridge


def _write_fake_flashrag(root: Path) -> None:
    package = root / "flashrag"
    dataset = package / "dataset"
    retriever = package / "retriever"
    dataset.mkdir(parents=True)
    retriever.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (dataset / "__init__.py").write_text("", encoding="utf-8")
    (retriever / "__init__.py").write_text("", encoding="utf-8")
    (dataset / "dataset.py").write_text(
        "\n".join(
            [
                "import json",
                "",
                "class Item:",
                "    def __init__(self, data):",
                "        self.id = data['id']",
                "        self.question = data['question']",
                "        self.golden_answers = data['golden_answers']",
                "        self.metadata = data['metadata']",
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
                "    def __getitem__(self, index):",
                "        return self.data[index]",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (retriever / "index_builder.py").write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "",
                "class Index_Builder:",
                "    def __init__(self, **kwargs):",
                "        self.kwargs = kwargs",
                "    def build_index(self):",
                "        index_dir = Path(self.kwargs['save_dir']) / 'bm25'",
                "        index_dir.mkdir(parents=True, exist_ok=True)",
                "        (index_dir / 'built.txt').write_text(self.kwargs['corpus_path'], encoding='utf-8')",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (retriever / "retriever.py").write_text(
        "\n".join(
            [
                "import json",
                "",
                "class BM25Retriever:",
                "    def __init__(self, config):",
                "        self.config = config",
                "        self.corpus = []",
                "        with open(config['corpus_path'], encoding='utf-8') as handle:",
                "            for line in handle:",
                "                if line.strip():",
                "                    self.corpus.append(json.loads(line))",
                "    def batch_search(self, query, num=None, return_score=False):",
                "        results = []",
                "        scores = []",
                "        for item in query:",
                "            ranked = []",
                "            query_terms = {term.lower() for term in item.split()}",
                "            for doc in self.corpus:",
                "                doc_terms = {term.lower().strip('.,') for term in doc['contents'].split()}",
                "                ranked.append((len(query_terms & doc_terms), doc['id'], doc))",
                "            ranked.sort(key=lambda row: (-row[0], row[1]))",
                "            top = ranked[:num]",
                "            results.append([doc for _, _, doc in top])",
                "            scores.append([float(score) for score, _, _ in top])",
                "        if return_score:",
                "            return results, scores",
                "        return results",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_bundle(root: Path) -> None:
    (root / "qrels").mkdir(parents=True)
    (root / "dev.jsonl").write_text(
        json.dumps(
            {
                "id": "q001",
                "question": "Which alloy mentions gamma prime strengthening?",
                "golden_answers": ["B"],
                "metadata": {
                    "question_type": "single_choice",
                    "source_chunk_ids": ["d_gold"],
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "qrels" / "dev.tsv").write_text("q001\td_gold\t1\n", encoding="utf-8")
    (root / "corpus.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "d_gold",
                        "contents": "Gamma prime strengthening is documented for the alloy answer B.",
                    }
                ),
                json.dumps(
                    {
                        "id": "d_other",
                        "contents": "Oxidation scale adhesion is a different mechanism.",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_run_flashrag_bm25_bridge_writes_domainrag_rows(tmp_path: Path):
    flashrag = tmp_path / "flashrag-fork"
    bundle = tmp_path / "bundle"
    output = tmp_path / "outputs"
    index_dir = tmp_path / "index"
    _write_fake_flashrag(flashrag)
    _write_bundle(bundle)

    result_path = run_flashrag_bm25_bridge(
        flashrag,
        bundle,
        output,
        dataset_name="unit_domain",
        split="dev",
        top_k=2,
        index_dir=index_dir,
    )

    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]
    assert result_path == output / "bundle" / "dev_flashrag_bm25_results.jsonl"
    assert (index_dir / "bm25" / "built.txt").exists()
    assert rows == [
        {
            "api_calls": 0,
            "error": None,
            "gold_context_ids": ["d_gold"],
            "golden_answers": ["B"],
            "id": "q001",
            "input_tokens": 16,
            "latency_ms": 0.0,
            "method": "flashrag_bm25_oracle_reader",
            "output_tokens": 1,
            "prediction": "B",
            "prompt": (
                "Which alloy mentions gamma prime strengthening?\n\n"
                "Return exactly one uppercase option letter. Do not include explanation."
            ),
            "retrieval_scores": [3.0, 0.0],
            "retrieved_context_ids": ["d_gold", "d_other"],
            "scores": {
                "retrieval_hit": 1.0,
                "retrieval_mrr": 1.0,
                "retrieval_recall": 1.0,
                "single_choice_accuracy": 1.0,
            },
            "split": "dev",
        }
    ]


def test_run_flashrag_bm25_bridge_rejects_non_positive_top_k(tmp_path: Path):
    flashrag = tmp_path / "flashrag-fork"
    bundle = tmp_path / "bundle"
    _write_fake_flashrag(flashrag)
    _write_bundle(bundle)

    with pytest.raises(ValidationError) as exc:
        run_flashrag_bm25_bridge(
            flashrag,
            bundle,
            tmp_path / "outputs",
            dataset_name="unit_domain",
            split="dev",
            top_k=0,
        )

    assert "top_k must be positive" in str(exc.value)
