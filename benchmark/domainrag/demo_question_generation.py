from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from domainrag.easy_dataset_adapter import DomainRAGExportBundle, export_domainrag_bundle
from domainrag.io_utils import read_jsonl, write_jsonl


QUESTION_TYPES = ("single_choice", "multiple_choice", "fill_blank", "short_answer")
SPLITS = ("dev", "test", "fresh_hard")
STOPWORDS = {
    "about",
    "across",
    "after",
    "all",
    "also",
    "and",
    "because",
    "between",
    "from",
    "into",
    "that",
    "their",
    "these",
    "this",
    "through",
    "under",
    "with",
}
WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9+-]*")


def build_demo_question_dataset(
    source_dataset_dir: Path,
    output_dir: Path,
    *,
    dataset_name: str = "real_pilot_nickel_superalloy_demo_questions",
    target_questions: int = 300,
    fixture_output_dir: Path | None = None,
) -> DomainRAGExportBundle:
    if target_questions < 300 or target_questions > 500:
        raise ValueError("target_questions must be between 300 and 500")
    if target_questions % len(SPLITS) != 0:
        raise ValueError("target_questions must be divisible by 3")

    corpus = read_jsonl(source_dataset_dir / "corpus.jsonl")
    if len(corpus) < len(SPLITS):
        raise ValueError("source dataset must contain at least three corpus chunks")

    fixture_dir = fixture_output_dir or output_dir.parent / "fixtures" / dataset_name
    chunks = [{"id": row["id"], "content": row["contents"]} for row in corpus]
    items = _generate_items(
        dataset_name=dataset_name,
        corpus=corpus,
        target_questions=target_questions,
    )
    write_jsonl(fixture_dir / "chunks.jsonl", chunks)
    write_jsonl(fixture_dir / "items.jsonl", items)
    bundle = export_domainrag_bundle(fixture_dir, output_dir, dataset_name)
    _write_provisional_dataset_card(
        bundle.dataset_card_path,
        dataset_name,
        len(corpus),
        len(items),
    )
    return bundle


def _generate_items(
    *,
    dataset_name: str,
    corpus: list[dict[str, Any]],
    target_questions: int,
) -> list[dict[str, Any]]:
    per_split = target_questions // len(SPLITS)
    split_chunks = _partition_corpus(corpus)
    items: list[dict[str, Any]] = []
    for split in SPLITS:
        chunks = split_chunks[split]
        for offset in range(per_split):
            global_index = len(items) + 1
            chunk = chunks[offset % len(chunks)]
            question_type = QUESTION_TYPES[(global_index - 1) % len(QUESTION_TYPES)]
            items.append(
                _build_item(
                    dataset_name=dataset_name,
                    index=global_index,
                    split=split,
                    question_type=question_type,
                    chunk=chunk,
                )
            )
    return items


def _partition_corpus(corpus: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    partitions = {split: [] for split in SPLITS}
    for index, chunk in enumerate(corpus):
        partitions[SPLITS[index % len(SPLITS)]].append(chunk)
    if not partitions["dev"] or not partitions["test"] or not partitions["fresh_hard"]:
        raise ValueError("source dataset must provide chunks for all splits")
    return partitions


def _build_item(
    *,
    dataset_name: str,
    index: int,
    split: str,
    question_type: str,
    chunk: dict[str, Any],
) -> dict[str, Any]:
    chunk_id = str(chunk["id"])
    contents = " ".join(str(chunk["contents"]).split())
    statement = _first_sentence(contents)
    keywords = _keywords(contents)
    keyword_phrase = " ".join(keywords[:2]) if len(keywords) >= 2 else keywords[0]
    base = {
        "id": f"{dataset_name}_q{index:04d}",
        "split": split,
        "question_type": question_type,
        "source_chunk_ids": [chunk_id],
        "subdomain": _infer_subdomain(chunk_id, contents),
        "knowledge_type": _infer_knowledge_type(index),
        "difficulty": _infer_difficulty(split),
        "quality_score": 0.7,
    }
    if question_type == "single_choice":
        return {
            **base,
            "question": "Which statement is directly supported by the evidence chunk?",
            "options": {
                "A": statement,
                "B": "The evidence is about dataset bookkeeping rather than materials behavior.",
                "C": "The evidence says the mechanism is unrelated to high-temperature exposure.",
                "D": "The evidence only describes API retry settings.",
            },
            "answer": ["A"],
            "answer_aliases": [],
            "reference_answer": statement,
            "required_points": [],
        }
    if question_type == "multiple_choice":
        return {
            **base,
            "question": f"Which two statements are supported by the chunk about {keyword_phrase}?",
            "options": {
                "A": statement,
                "B": f"The chunk is relevant to {keyword_phrase}.",
                "C": "The chunk supports replacing experiments with filename sorting.",
                "D": "The chunk states that high-temperature degradation is impossible.",
                "E": "The chunk is only about command-line flags.",
            },
            "answer": ["A", "B"],
            "answer_aliases": [],
            "reference_answer": f"{statement} The chunk is relevant to {keyword_phrase}.",
            "required_points": [],
        }
    if question_type == "fill_blank":
        return {
            **base,
            "question": "The evidence chunk is mainly associated with ____.",
            "options": {},
            "answer": [keyword_phrase],
            "answer_aliases": [keyword_phrase, keywords[0]],
            "reference_answer": keyword_phrase,
            "required_points": [],
        }
    return {
        **base,
        "question": f"Briefly state the evidence connected to {keyword_phrase}.",
        "options": {},
        "answer": [statement],
        "answer_aliases": [],
        "reference_answer": statement,
        "required_points": keywords[:2],
    }


def _first_sentence(text: str) -> str:
    for separator in (". ", "; ", ": "):
        if separator in text:
            candidate = text.split(separator, 1)[0].strip()
            if candidate:
                return candidate.rstrip(".") + "."
    return text[:240].strip().rstrip(".") + "."


def _keywords(text: str) -> list[str]:
    keywords: list[str] = []
    for match in WORD_PATTERN.finditer(text.lower()):
        token = match.group(0)
        if len(token) < 5 or token in STOPWORDS:
            continue
        if token not in keywords:
            keywords.append(token)
        if len(keywords) >= 4:
            break
    return keywords or ["nickel", "superalloy"]


def _infer_subdomain(chunk_id: str, contents: str) -> str:
    text = f"{chunk_id} {contents}".lower()
    for subdomain in (
        "oxidation",
        "creep",
        "fatigue",
        "coatings",
        "hot_corrosion",
        "life_prediction",
        "microstructure_characterization",
        "additive_manufacturing",
    ):
        if subdomain in text:
            return subdomain
    if "corrosion" in text:
        return "hot_corrosion"
    if "microstructure" in text:
        return "microstructure_characterization"
    if "additive" in text:
        return "additive_manufacturing"
    return "nickel_superalloy_high_temperature_failure"


def _infer_knowledge_type(index: int) -> str:
    return ("mechanism", "method", "fact", "comparison")[index % 4]


def _infer_difficulty(split: str) -> str:
    if split == "fresh_hard":
        return "hard"
    if split == "test":
        return "medium"
    return "easy"


def _write_provisional_dataset_card(
    path: Path,
    dataset_name: str,
    corpus_count: int,
    question_count: int,
) -> None:
    path.write_text(
        "\n".join(
            [
                f"# {dataset_name}",
                "",
                "Provisional demo-question dataset.",
                "",
                "This dataset was generated deterministically from the validated "
                "medium-plus DomainRAG corpus for Phase 7M. It is intended for "
                "pipeline verification and provisional benchmark rehearsal.",
                "",
                f"- Corpus rows: {corpus_count}",
                f"- Question rows: {question_count}",
                "- Split rows: 100 dev / 100 test / 100 fresh_hard",
                "- Question types: 75 each for single_choice, multiple_choice, "
                "fill_blank, and short_answer",
                "- Public metadata follows the DomainRAG data contract.",
                "- Source paper identity metadata is not included in public artifacts.",
                "",
                "Boundary: this is not a human-final demo benchmark. Final use "
                "still requires real human source sign-off and, if strict RAG.md "
                "completion is required, regeneration from human-accepted sources.",
                "",
            ]
        ),
        encoding="utf-8",
    )
