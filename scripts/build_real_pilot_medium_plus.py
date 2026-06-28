from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
import shutil
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.easy_dataset_adapter import export_domainrag_bundle  # noqa: E402
from domainrag.errors import ValidationError, ValidationIssue  # noqa: E402
from domainrag.io_utils import read_jsonl, write_jsonl  # noqa: E402


BASE_FIXTURE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_medium"
BASE_SOURCES = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure_medium"
    / "sources.jsonl"
)
DEFAULT_FIXTURE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_medium_plus"
DEFAULT_SOURCE_DIR = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure_medium_plus"
)
DEFAULT_OUTPUT = ROOT / "data"
DEFAULT_DATASET_NAME = "real_pilot_nickel_superalloy_medium_plus"

TARGET_CORPUS_COUNT = 100
TARGET_QUESTION_COUNT = 150
TARGET_SPLIT_COUNTS = {"dev": 50, "test": 50, "fresh_hard": 50}
ADDED_TYPE_COUNTS = {
    "single_choice": 23,
    "multiple_choice": 23,
    "fill_blank": 22,
    "short_answer": 22,
}
QUESTION_TYPE_ORDER = [
    "single_choice",
    "multiple_choice",
    "fill_blank",
    "short_answer",
]
KEYWORD_PRIORITY = [
    "gamma-prime",
    "chromia",
    "chromium",
    "oxidation",
    "corrosion",
    "creep",
    "fatigue",
    "hydrogen",
    "interdiffusion",
    "microsegregation",
    "grain-boundary",
    "rafting",
    "lattice",
    "niobium",
    "oxygen",
    "thermal",
    "residual",
    "damage",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build the medium-plus real nickel-superalloy DomainRAG pilot dataset "
            "from the validated medium source-backed fixture."
        ),
    )
    parser.add_argument("--fixture-output", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--source-output", default=str(DEFAULT_SOURCE_DIR))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--dataset-name", default=DEFAULT_DATASET_NAME)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    fixture_dir = Path(args.fixture_output)
    source_dir = Path(args.source_output)
    try:
        _write_medium_plus_fixture(fixture_dir, source_dir)
        bundle = export_domainrag_bundle(
            fixture_dir,
            Path(args.output),
            args.dataset_name,
        )
    except ValidationError as exc:
        print(str(exc))
        return 1

    print(f"Medium-plus Easy Dataset fixture written to {fixture_dir}")
    print(f"Medium-plus source manifest written to {source_dir / 'sources.jsonl'}")
    print(f"Medium-plus DomainRAG dataset written to {bundle.dataset_dir}")
    print(f"Statistics written to {bundle.statistics_path}")
    return 0


def _write_medium_plus_fixture(fixture_dir: Path, source_dir: Path) -> None:
    base_chunks = read_jsonl(BASE_FIXTURE / "chunks.jsonl")
    base_items = read_jsonl(BASE_FIXTURE / "items.jsonl")
    base_sources = read_jsonl(BASE_SOURCES)
    chunk_by_id = {chunk["id"]: chunk for chunk in base_chunks}

    distilled_chunks, distilled_chunk_by_item = _build_distilled_chunks(
        base_items,
        chunk_by_id,
    )
    added_items = _build_added_items(base_items, distilled_chunk_by_item)
    sources = _extend_sources(base_sources, base_items, distilled_chunk_by_item)

    chunks = [*base_chunks, *distilled_chunks]
    items = [*base_items, *added_items]
    _assert_unique("chunk", [chunk["id"] for chunk in chunks])
    _assert_unique("item", [item["id"] for item in items])
    _assert_unique("source", [source["source_id"] for source in sources])
    _assert_shape(chunks, items)

    if fixture_dir.exists():
        shutil.rmtree(fixture_dir)
    fixture_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(fixture_dir / "chunks.jsonl", chunks)
    write_jsonl(fixture_dir / "items.jsonl", items)

    if source_dir.exists():
        shutil.rmtree(source_dir)
    source_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(source_dir / "sources.jsonl", sources)


def _build_distilled_chunks(
    items: list[dict[str, Any]],
    chunk_by_id: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    distilled_chunks: list[dict[str, str]] = []
    distilled_chunk_by_item: dict[str, str] = {}
    for item in items:
        question_number = _question_number(item["id"])
        chunk_id = f"ns_ht_medium_plus_q{question_number:03d}_distilled_001"
        source_snippets = [
            _first_sentence(chunk_by_id[source_chunk_id]["content"])
            for source_chunk_id in item["source_chunk_ids"]
            if source_chunk_id in chunk_by_id
        ]
        required = item.get("required_points") or []
        required_text = (
            " Key evidence terms include " + ", ".join(required[:3]) + "."
            if required
            else ""
        )
        content = (
            f"{_ensure_period(_item_statement(item))} "
            f"Supporting source note: {' '.join(source_snippets)}"
            f"{required_text}"
        )
        distilled_chunks.append({"id": chunk_id, "content": content})
        distilled_chunk_by_item[item["id"]] = chunk_id
    return distilled_chunks, distilled_chunk_by_item


def _build_added_items(
    base_items: list[dict[str, Any]],
    distilled_chunk_by_item: dict[str, str],
) -> list[dict[str, Any]]:
    items_by_split = {
        split: [item for item in base_items if item["split"] == split]
        for split in TARGET_SPLIT_COUNTS
    }
    question_types = _added_question_type_sequence()
    next_question_number = 61
    added_items: list[dict[str, Any]] = []
    type_index = 0

    for split in ["dev", "test", "fresh_hard"]:
        seeds = items_by_split[split]
        for offset in range(30):
            cycle = offset // len(seeds)
            seed = seeds[offset % len(seeds)]
            companion = seeds[(offset * 7 + 3 + cycle * 5) % len(seeds)]
            if companion["id"] == seed["id"]:
                companion = seeds[(offset + 1) % len(seeds)]
            question_type = question_types[type_index]
            type_index += 1
            multi_source = split == "fresh_hard" or cycle > 0 or offset % 2 == 0
            source_chunk_ids = [distilled_chunk_by_item[seed["id"]]]
            if multi_source:
                source_chunk_ids.append(distilled_chunk_by_item[companion["id"]])

            new_item = _render_added_item(
                question_number=next_question_number,
                split=split,
                question_type=question_type,
                seed=seed,
                companion=companion if multi_source else None,
                source_chunk_ids=source_chunk_ids,
            )
            added_items.append(new_item)
            next_question_number += 1

    return added_items


def _render_added_item(
    *,
    question_number: int,
    split: str,
    question_type: str,
    seed: dict[str, Any],
    companion: dict[str, Any] | None,
    source_chunk_ids: list[str],
) -> dict[str, Any]:
    references = [_item_statement(seed)]
    if companion is not None:
        references.append(_item_statement(companion))
    reference_answer = " ".join(_ensure_period(reference) for reference in references)
    subdomain = seed["subdomain"]
    difficulty = "hard" if split == "fresh_hard" or companion is not None else seed["difficulty"]
    required_points = _required_points(seed, companion)

    base = {
        "id": f"ns_ht_q{question_number:03d}",
        "split": split,
        "question_type": question_type,
        "answer_aliases": [],
        "source_chunk_ids": source_chunk_ids,
        "subdomain": subdomain,
        "knowledge_type": "synthesis" if companion is not None else seed["knowledge_type"],
        "difficulty": difficulty,
        "quality_score": 0.86 if companion is not None else 0.88,
        "required_points": required_points if question_type == "short_answer" else [],
    }

    if question_type == "single_choice":
        correct = _compact_statement(reference_answer)
        base.update(
            {
                "question": (
                    "Which statement is best supported by the source-backed "
                    f"evidence set for {subdomain.replace('_', ' ')}?"
                ),
                "options": {
                    "A": correct,
                    "B": "The evidence says the effect is only a file-format artifact",
                    "C": "The evidence rules out microstructure and environment as failure drivers",
                    "D": "The evidence says no source-backed mechanism is involved",
                },
                "answer": ["A"],
                "reference_answer": correct,
            }
        )
        return base

    if question_type == "multiple_choice":
        first = _compact_statement(_item_statement(seed), max_words=18)
        second_source = companion or seed
        second = _compact_statement(_item_statement(second_source), max_words=18)
        base.update(
            {
                "question": (
                    "Which statements are supported by the paired "
                    f"evidence set for {subdomain.replace('_', ' ')}?"
                ),
                "options": {
                    "A": first,
                    "B": second,
                    "C": "The evidence says retrieval labels determine alloy behavior",
                    "D": "The evidence says all high-temperature damage is impossible",
                    "E": "The evidence removes the need for source-grounded context",
                },
                "answer": ["A", "B"],
                "reference_answer": reference_answer,
            }
        )
        return base

    if question_type == "fill_blank":
        keyword = _select_keyword(reference_answer)
        blanked = _blank_keyword(reference_answer, keyword)
        base.update(
            {
                "question": f"Fill the missing term in this supported claim: {blanked}",
                "options": {},
                "answer": [keyword],
                "answer_aliases": _keyword_aliases(keyword),
                "reference_answer": keyword,
            }
        )
        return base

    if question_type == "short_answer":
        base.update(
            {
                "question": (
                    "Summarize the source-backed evidence connecting "
                    f"{subdomain.replace('_', ' ')} to nickel-superalloy high-temperature failure."
                ),
                "options": {},
                "answer": [reference_answer],
                "reference_answer": reference_answer,
            }
        )
        return base

    raise ValidationError([ValidationIssue("question_type", f"unsupported {question_type}")])


def _extend_sources(
    base_sources: list[dict[str, Any]],
    base_items: list[dict[str, Any]],
    distilled_chunk_by_item: dict[str, str],
) -> list[dict[str, Any]]:
    sources = deepcopy(base_sources)
    item_by_original_chunk: dict[str, list[str]] = {}
    for item in base_items:
        distilled_chunk_id = distilled_chunk_by_item[item["id"]]
        for original_chunk_id in item["source_chunk_ids"]:
            item_by_original_chunk.setdefault(original_chunk_id, []).append(distilled_chunk_id)

    for source in sources:
        used = list(source.get("used_for_chunk_ids", []))
        for original_chunk_id in list(used):
            used.extend(item_by_original_chunk.get(original_chunk_id, []))
        source["used_for_chunk_ids"] = sorted(set(used))
        source["medium_plus_note"] = (
            "Phase 7B adds distilled source-backed chunks derived from the "
            "validated medium questions and original source chunks."
        )
    return sources


def _added_question_type_sequence() -> list[str]:
    remaining = dict(ADDED_TYPE_COUNTS)
    sequence: list[str] = []
    while sum(remaining.values()):
        for question_type in QUESTION_TYPE_ORDER:
            if remaining[question_type] > 0:
                sequence.append(question_type)
                remaining[question_type] -= 1
    return sequence


def _required_points(seed: dict[str, Any], companion: dict[str, Any] | None) -> list[str]:
    points = list(seed.get("required_points") or [])
    if companion is not None:
        points.extend(companion.get("required_points") or [])
    if points:
        return points[:4]
    return [
        _select_keyword(seed["reference_answer"]),
        seed["subdomain"].replace("_", " "),
    ]


def _item_statement(item: dict[str, Any]) -> str:
    if item["question_type"] == "fill_blank":
        answer = str(item["answer"][0])
        question = str(item["question"]).replace("____", answer)
        return question
    return str(item["reference_answer"])


def _question_number(question_id: str) -> int:
    match = re.search(r"(\d+)$", question_id)
    if not match:
        raise ValidationError([ValidationIssue(question_id, "question id has no numeric suffix")])
    return int(match.group(1))


def _first_sentence(text: str) -> str:
    sentence = text.strip().split(". ")[0].strip()
    return _ensure_period(sentence)


def _ensure_period(text: str) -> str:
    stripped = " ".join(str(text).strip().split())
    if not stripped:
        return ""
    return stripped if stripped.endswith((".", "?", "!")) else stripped + "."


def _compact_statement(text: str, *, max_words: int = 22) -> str:
    words = _ensure_period(text).split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]).rstrip(".,;") + "."


def _select_keyword(text: str) -> str:
    lowered = text.lower()
    for keyword in KEYWORD_PRIORITY:
        if keyword in lowered:
            return keyword
    for match in re.finditer(r"[A-Za-z][A-Za-z-]{5,}", text):
        return match.group(0).lower()
    return "damage"


def _blank_keyword(text: str, keyword: str) -> str:
    return re.sub(re.escape(keyword), "____", _ensure_period(text), count=1, flags=re.IGNORECASE)


def _keyword_aliases(keyword: str) -> list[str]:
    aliases = {
        "gamma-prime": ["gamma prime", "gamma'"],
        "chromia": ["Cr2O3", "chromium oxide"],
        "chromium": ["Cr"],
        "niobium": ["Nb"],
        "grain-boundary": ["grain boundary", "grain boundaries"],
    }
    return aliases.get(keyword, [keyword.replace("-", " ")])


def _assert_unique(label: str, values: list[str]) -> None:
    counts = Counter(values)
    duplicates = sorted(value for value, count in counts.items() if count > 1)
    if duplicates:
        raise ValidationError([ValidationIssue(label, f"duplicate ids: {duplicates}")])


def _assert_shape(chunks: list[dict[str, str]], items: list[dict[str, Any]]) -> None:
    issues: list[ValidationIssue] = []
    if len(chunks) != TARGET_CORPUS_COUNT:
        issues.append(ValidationIssue("chunks", f"expected {TARGET_CORPUS_COUNT}, got {len(chunks)}"))
    if len(items) != TARGET_QUESTION_COUNT:
        issues.append(ValidationIssue("items", f"expected {TARGET_QUESTION_COUNT}, got {len(items)}"))
    split_counts = Counter(item["split"] for item in items)
    if split_counts != TARGET_SPLIT_COUNTS:
        issues.append(ValidationIssue("items", f"split counts mismatch: {dict(split_counts)}"))
    expected_types = {
        "single_choice": 38,
        "multiple_choice": 38,
        "fill_blank": 37,
        "short_answer": 37,
    }
    type_counts = Counter(item["question_type"] for item in items)
    if type_counts != expected_types:
        issues.append(ValidationIssue("items", f"type counts mismatch: {dict(type_counts)}"))
    if issues:
        raise ValidationError(issues)


if __name__ == "__main__":
    raise SystemExit(main())
