from __future__ import annotations

import importlib
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from domainrag.benchmark_runner import _gold_prediction, _retrieval_scores
from domainrag.domain_evaluator import evaluate_record
from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_qrels, write_jsonl
from domainrag.prompt_renderer import render_prompt


METHOD_NAME = "flashrag_bm25_oracle_reader"


def run_flashrag_bm25_bridge(
    flashrag_path: Path,
    dataset_bundle: Path,
    output_dir: Path,
    *,
    dataset_name: str,
    split: str = "dev",
    top_k: int = 5,
    index_dir: Path | None = None,
    rebuild_index: bool = False,
) -> Path:
    issues = _validate_inputs(flashrag_path, dataset_bundle, split, top_k)
    if issues:
        raise ValidationError(issues)

    if index_dir is None:
        index_dir = output_dir / dataset_bundle.name / "flashrag_bm25_index"

    split_path = dataset_bundle / f"{split}.jsonl"
    corpus_path = dataset_bundle / "corpus.jsonl"
    qrels_path = dataset_bundle / "qrels" / f"{split}.tsv"

    with _flashrag_on_path(flashrag_path):
        _build_index_if_needed(
            corpus_path=corpus_path,
            index_dir=index_dir,
            rebuild_index=rebuild_index,
        )
        records = _load_flashrag_records(split_path, dataset_name)
        retrieval_results, retrieval_scores = _retrieve_with_flashrag_bm25(
            corpus_path=corpus_path,
            index_path=index_dir / "bm25",
            records=records,
            top_k=top_k,
            save_dir=output_dir / dataset_bundle.name,
        )

    qrels = _load_positive_qrels(qrels_path)
    output_records = [
        _build_output_row(
            record=record,
            split=split,
            gold_context_ids=qrels.get(record["id"], []),
            retrieved_docs=retrieved_docs,
            retrieval_scores=scores,
        )
        for record, retrieved_docs, scores in zip(records, retrieval_results, retrieval_scores)
    ]
    result_path = output_dir / dataset_bundle.name / f"{split}_flashrag_bm25_results.jsonl"
    write_jsonl(result_path, output_records)
    return result_path


def _validate_inputs(
    flashrag_path: Path,
    dataset_bundle: Path,
    split: str,
    top_k: int,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if top_k <= 0:
        issues.append(ValidationIssue("top_k", "top_k must be positive"))
    if not (flashrag_path / "flashrag").is_dir():
        issues.append(ValidationIssue(str(flashrag_path), "FlashRAG package directory missing"))
    if not dataset_bundle.is_dir():
        issues.append(ValidationIssue(str(dataset_bundle), "dataset bundle directory missing"))
        return issues
    for path in [
        dataset_bundle / f"{split}.jsonl",
        dataset_bundle / "corpus.jsonl",
        dataset_bundle / "qrels" / f"{split}.tsv",
    ]:
        if not path.exists():
            issues.append(ValidationIssue(str(path), "file does not exist"))
    return issues


@contextmanager
def _flashrag_on_path(flashrag_path: Path) -> Iterator[None]:
    path = str(flashrag_path)
    removed_modules: dict[str, Any] = {}
    sys.path.insert(0, path)
    for module_name in list(sys.modules):
        if module_name == "flashrag" or module_name.startswith("flashrag."):
            removed_modules[module_name] = sys.modules.pop(module_name)
    try:
        yield
    finally:
        try:
            sys.path.remove(path)
        except ValueError:
            pass
        for module_name in list(sys.modules):
            if module_name == "flashrag" or module_name.startswith("flashrag."):
                sys.modules.pop(module_name, None)
        sys.modules.update(removed_modules)


def _build_index_if_needed(
    *,
    corpus_path: Path,
    index_dir: Path,
    rebuild_index: bool,
) -> None:
    bm25_index_dir = index_dir / "bm25"
    if rebuild_index and bm25_index_dir.exists():
        shutil.rmtree(bm25_index_dir)
    if bm25_index_dir.exists() and any(bm25_index_dir.iterdir()):
        return

    module = importlib.import_module("flashrag.retriever.index_builder")
    index_builder_class = getattr(module, "Index_Builder")
    index_builder = index_builder_class(
        retrieval_method="bm25",
        model_path=None,
        corpus_path=str(corpus_path),
        save_dir=str(index_dir),
        max_length=180,
        batch_size=512,
        use_fp16=False,
        bm25_backend="bm25s",
    )
    index_builder.build_index()


def _load_flashrag_records(split_path: Path, dataset_name: str) -> list[dict[str, Any]]:
    module = importlib.import_module("flashrag.dataset.dataset")
    dataset_class = getattr(module, "Dataset")
    dataset = dataset_class(
        config={"dataset_name": dataset_name},
        dataset_path=str(split_path),
    )
    return [_record_from_flashrag_item(dataset[index]) for index in range(len(dataset))]


def _record_from_flashrag_item(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return {
            "id": item["id"],
            "question": item["question"],
            "golden_answers": item["golden_answers"],
            "metadata": item["metadata"],
        }
    return {
        "id": getattr(item, "id"),
        "question": getattr(item, "question"),
        "golden_answers": getattr(item, "golden_answers"),
        "metadata": getattr(item, "metadata"),
    }


def _retrieve_with_flashrag_bm25(
    *,
    corpus_path: Path,
    index_path: Path,
    records: list[dict[str, Any]],
    top_k: int,
    save_dir: Path,
) -> tuple[list[list[dict[str, Any]]], list[list[float]]]:
    module = importlib.import_module("flashrag.retriever.retriever")
    retriever_class = getattr(module, "BM25Retriever")
    retriever = retriever_class(
        {
            "retrieval_method": "bm25",
            "retrieval_topk": top_k,
            "index_path": str(index_path),
            "corpus_path": str(corpus_path),
            "save_retrieval_cache": False,
            "use_retrieval_cache": False,
            "retrieval_cache_path": None,
            "use_reranker": False,
            "silent_retrieval": True,
            "bm25_backend": "bm25s",
            "save_dir": str(save_dir),
        }
    )
    queries = [record["question"] for record in records]
    results, scores = retriever.batch_search(queries, num=top_k, return_score=True)
    return _to_nested_doc_lists(results), _to_nested_float_lists(scores)


def _to_nested_doc_lists(value: Any) -> list[list[dict[str, Any]]]:
    if hasattr(value, "tolist"):
        value = value.tolist()
    return [
        [dict(doc) for doc in docs]
        for docs in value
    ]


def _to_nested_float_lists(value: Any) -> list[list[float]]:
    if hasattr(value, "tolist"):
        value = value.tolist()
    return [[float(score) for score in scores] for scores in value]


def _load_positive_qrels(path: Path) -> dict[str, list[str]]:
    qrels: dict[str, list[str]] = {}
    for query_id, corpus_id, score in read_qrels(path):
        if score > 0:
            qrels.setdefault(query_id, []).append(corpus_id)
    return qrels


def _build_output_row(
    *,
    record: dict[str, Any],
    split: str,
    gold_context_ids: list[str],
    retrieved_docs: list[dict[str, Any]],
    retrieval_scores: list[float],
) -> dict[str, Any]:
    prompt = render_prompt(record)
    retrieved_context_ids = [str(doc["id"]) for doc in retrieved_docs]
    prediction = (
        _gold_prediction(record)
        if set(retrieved_context_ids) & set(gold_context_ids)
        else ""
    )
    scores = evaluate_record(record, prediction)
    scores.update(_retrieval_scores(gold_context_ids, retrieved_context_ids))
    return {
        "id": record["id"],
        "method": METHOD_NAME,
        "split": split,
        "prompt": prompt,
        "prediction": prediction,
        "golden_answers": record["golden_answers"],
        "gold_context_ids": gold_context_ids,
        "retrieved_context_ids": retrieved_context_ids,
        "retrieval_scores": retrieval_scores,
        "scores": scores,
        "latency_ms": 0.0,
        "input_tokens": len(prompt.split()),
        "output_tokens": len(prediction.split()),
        "api_calls": 0,
        "error": None,
    }
