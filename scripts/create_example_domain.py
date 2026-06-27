from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.io_utils import write_jsonl

DATA_DIR = ROOT / "data" / "example_domain"
INVALID_DIR = ROOT / "data" / "invalid_fixtures" / "missing_qrels"


def option_text(options: dict[str, str]) -> str:
    return "\n".join(f"{key}. {value}" for key, value in options.items())


def make_flashrag(item: dict) -> dict:
    question = item["question"]
    if item["question_type"] in {"single_choice", "multiple_choice"}:
        question = f"{question}\n{option_text(item['options'])}"
    metadata = {
        "question_type": item["question_type"],
        "source_chunk_ids": item["source_chunk_ids"],
        "knowledge_type": item["knowledge_type"],
        "difficulty": item["difficulty"],
        "required_points": item["required_points"],
        "answer_aliases": item["answer_aliases"],
    }
    if item["question_type"] in {"single_choice", "multiple_choice"}:
        metadata["correct_options"] = item["answer"]
    return {
        "id": item["id"],
        "question": question,
        "golden_answers": item["answer"],
        "metadata": metadata,
    }


def main() -> None:
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True)
    (DATA_DIR / "qrels").mkdir()

    corpus = [
        {"id": "d000001", "contents": "Oxidation\nChromium-rich oxide scales can slow oxygen ingress at high temperature."},
        {"id": "d000002", "contents": "Creep\nCreep rate increases when temperature and applied stress increase together."},
        {"id": "d000003", "contents": "Fatigue\nCrack initiation often begins at surface defects under cyclic loading."},
        {"id": "d000004", "contents": "Heat treatment\nSolution treatment followed by aging can strengthen precipitation-hardened alloys."},
        {"id": "d000005", "contents": "Microstructure\nFine precipitates impede dislocation motion and improve high-temperature strength."},
        {"id": "d000006", "contents": "Life prediction\nRemaining life models combine stress, temperature, exposure time, and damage state."},
        {"id": "d000007", "contents": "Characterization\nElectron microscopy can reveal precipitate morphology and crack paths."},
        {"id": "d000008", "contents": "Comparison\nOxidation resistance and creep strength can trade off when alloying changes phase stability."},
    ]

    canonical = [
        {
            "id": "q000001",
            "question_type": "single_choice",
            "question": "Which feature slows oxygen ingress at high temperature?",
            "options": {"A": "Chromium-rich oxide scales", "B": "File names", "C": "Page numbers", "D": "Random sampling"},
            "answer": ["A"],
            "answer_aliases": [],
            "reference_answer": "Chromium-rich oxide scales slow oxygen ingress at high temperature.",
            "required_points": [],
            "source_chunk_ids": ["d000001"],
            "subdomain": "oxidation",
            "knowledge_type": "mechanism",
            "difficulty": "easy",
            "quality_score": 1.0,
        },
        {
            "id": "q000002",
            "question_type": "single_choice",
            "question": "Which condition pair increases creep rate?",
            "options": {"A": "Lower stress and lower temperature", "B": "Higher temperature and higher applied stress", "C": "Shorter file path", "D": "More citations"},
            "answer": ["B"],
            "answer_aliases": [],
            "reference_answer": "Creep rate increases when temperature and applied stress increase together.",
            "required_points": [],
            "source_chunk_ids": ["d000002"],
            "subdomain": "creep",
            "knowledge_type": "condition",
            "difficulty": "easy",
            "quality_score": 1.0,
        },
        {
            "id": "q000003",
            "question_type": "single_choice",
            "question": "Where does crack initiation often begin under cyclic loading?",
            "options": {"A": "Surface defects", "B": "Bibliography entries", "C": "Dataset cards", "D": "Model names"},
            "answer": ["A"],
            "answer_aliases": [],
            "reference_answer": "Crack initiation often begins at surface defects under cyclic loading.",
            "required_points": [],
            "source_chunk_ids": ["d000003"],
            "subdomain": "fatigue",
            "knowledge_type": "fact",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000004",
            "question_type": "single_choice",
            "question": "Which process can strengthen precipitation-hardened alloys?",
            "options": {"A": "Removing all metadata", "B": "Solution treatment followed by aging", "C": "Changing qrels column order", "D": "Deleting corpus ids"},
            "answer": ["B"],
            "answer_aliases": [],
            "reference_answer": "Solution treatment followed by aging can strengthen precipitation-hardened alloys.",
            "required_points": [],
            "source_chunk_ids": ["d000004"],
            "subdomain": "heat_treatment",
            "knowledge_type": "method",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000005",
            "question_type": "multiple_choice",
            "question": "Which factors are used by remaining life models in the example corpus?",
            "options": {"A": "Stress", "B": "Temperature", "C": "Exposure time", "D": "Damage state", "E": "Paper page number"},
            "answer": ["A", "B", "C", "D"],
            "answer_aliases": [],
            "reference_answer": "Remaining life models combine stress, temperature, exposure time, and damage state.",
            "required_points": [],
            "source_chunk_ids": ["d000006"],
            "subdomain": "life_prediction",
            "knowledge_type": "method",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000006",
            "question_type": "multiple_choice",
            "question": "Which observations can electron microscopy reveal in this example?",
            "options": {"A": "Precipitate morphology", "B": "Crack paths", "C": "API key values", "D": "Original PDF path", "E": "Dataset filename"},
            "answer": ["A", "B"],
            "answer_aliases": [],
            "reference_answer": "Electron microscopy can reveal precipitate morphology and crack paths.",
            "required_points": [],
            "source_chunk_ids": ["d000007"],
            "subdomain": "characterization",
            "knowledge_type": "method",
            "difficulty": "easy",
            "quality_score": 1.0,
        },
        {
            "id": "q000007",
            "question_type": "multiple_choice",
            "question": "Which statements are supported by the example corpus?",
            "options": {"A": "Fine precipitates impede dislocation motion", "B": "Fine precipitates improve high-temperature strength", "C": "Creep rate ignores stress", "D": "Oxide scales can slow oxygen ingress", "E": "Authors must be exported"},
            "answer": ["A", "B", "D"],
            "answer_aliases": [],
            "reference_answer": "Fine precipitates impede dislocation motion, improve high-temperature strength, and chromium-rich oxide scales can slow oxygen ingress.",
            "required_points": [],
            "source_chunk_ids": ["d000001", "d000005"],
            "subdomain": "synthesis",
            "knowledge_type": "synthesis",
            "difficulty": "hard",
            "quality_score": 1.0,
        },
        {
            "id": "q000008",
            "question_type": "multiple_choice",
            "question": "Which properties can trade off when alloying changes phase stability?",
            "options": {"A": "Oxidation resistance", "B": "Creep strength", "C": "Terminal prompt length", "D": "Git branch name", "E": "File extension"},
            "answer": ["A", "B"],
            "answer_aliases": [],
            "reference_answer": "Oxidation resistance and creep strength can trade off when alloying changes phase stability.",
            "required_points": [],
            "source_chunk_ids": ["d000008"],
            "subdomain": "comparison",
            "knowledge_type": "comparison",
            "difficulty": "hard",
            "quality_score": 1.0,
        },
        {
            "id": "q000009",
            "question_type": "fill_blank",
            "question": "Chromium-rich oxide scales can slow oxygen ____ at high temperature.",
            "options": {},
            "answer": ["ingress"],
            "answer_aliases": ["oxygen ingress", "inward oxygen ingress"],
            "reference_answer": "ingress",
            "required_points": [],
            "source_chunk_ids": ["d000001"],
            "subdomain": "oxidation",
            "knowledge_type": "mechanism",
            "difficulty": "easy",
            "quality_score": 1.0,
        },
        {
            "id": "q000010",
            "question_type": "fill_blank",
            "question": "Fine precipitates impede ____ motion.",
            "options": {},
            "answer": ["dislocation"],
            "answer_aliases": ["dislocation motion"],
            "reference_answer": "dislocation",
            "required_points": [],
            "source_chunk_ids": ["d000005"],
            "subdomain": "microstructure",
            "knowledge_type": "mechanism",
            "difficulty": "easy",
            "quality_score": 1.0,
        },
        {
            "id": "q000011",
            "question_type": "fill_blank",
            "question": "Remaining life models combine stress, temperature, exposure time, and damage ____.",
            "options": {},
            "answer": ["state"],
            "answer_aliases": ["damage state"],
            "reference_answer": "state",
            "required_points": [],
            "source_chunk_ids": ["d000006"],
            "subdomain": "life_prediction",
            "knowledge_type": "method",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000012",
            "question_type": "fill_blank",
            "question": "Electron microscopy can reveal precipitate morphology and crack ____.",
            "options": {},
            "answer": ["paths"],
            "answer_aliases": ["crack paths", "path"],
            "reference_answer": "paths",
            "required_points": [],
            "source_chunk_ids": ["d000007"],
            "subdomain": "characterization",
            "knowledge_type": "method",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000013",
            "question_type": "short_answer",
            "question": "Why can fine precipitates improve high-temperature strength?",
            "options": {},
            "answer": ["They impede dislocation motion."],
            "answer_aliases": [],
            "reference_answer": "Fine precipitates impede dislocation motion, which improves high-temperature strength.",
            "required_points": ["fine precipitates", "impede dislocation motion", "improve high-temperature strength"],
            "source_chunk_ids": ["d000005"],
            "subdomain": "microstructure",
            "knowledge_type": "mechanism",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000014",
            "question_type": "short_answer",
            "question": "What conditions are combined in remaining life models?",
            "options": {},
            "answer": ["Stress, temperature, exposure time, and damage state."],
            "answer_aliases": [],
            "reference_answer": "Remaining life models combine stress, temperature, exposure time, and damage state.",
            "required_points": ["stress", "temperature", "exposure time", "damage state"],
            "source_chunk_ids": ["d000006"],
            "subdomain": "life_prediction",
            "knowledge_type": "method",
            "difficulty": "medium",
            "quality_score": 1.0,
        },
        {
            "id": "q000015",
            "question_type": "short_answer",
            "question": "How can alloying changes create a property tradeoff?",
            "options": {},
            "answer": ["They can change phase stability, causing oxidation resistance and creep strength to trade off."],
            "answer_aliases": [],
            "reference_answer": "Alloying changes can alter phase stability, creating a tradeoff between oxidation resistance and creep strength.",
            "required_points": ["alloying changes", "phase stability", "oxidation resistance", "creep strength", "tradeoff"],
            "source_chunk_ids": ["d000008"],
            "subdomain": "comparison",
            "knowledge_type": "comparison",
            "difficulty": "hard",
            "quality_score": 1.0,
        },
        {
            "id": "q000016",
            "question_type": "short_answer",
            "question": "Why is electron microscopy useful in the example corpus?",
            "options": {},
            "answer": ["It reveals precipitate morphology and crack paths."],
            "answer_aliases": [],
            "reference_answer": "Electron microscopy is useful because it can reveal precipitate morphology and crack paths.",
            "required_points": ["electron microscopy", "precipitate morphology", "crack paths"],
            "source_chunk_ids": ["d000007"],
            "subdomain": "characterization",
            "knowledge_type": "method",
            "difficulty": "easy",
            "quality_score": 1.0,
        },
    ]

    write_jsonl(DATA_DIR / "corpus.jsonl", corpus)
    write_jsonl(DATA_DIR / "canonical_dataset.jsonl", canonical)

    by_id = {item["id"]: item for item in canonical}
    dev_ids = ["q000001", "q000002", "q000003", "q000004", "q000007", "q000010"]
    test_ids = ["q000005", "q000006", "q000008", "q000011", "q000012", "q000016"]
    fresh_ids = ["q000009", "q000013", "q000014", "q000015"]

    dev_items = [by_id[question_id] for question_id in dev_ids]
    test_items = [by_id[question_id] for question_id in test_ids]
    fresh_items = [by_id[question_id] for question_id in fresh_ids]

    dev = [make_flashrag(item) for item in dev_items]
    test = [make_flashrag(item) for item in test_items]
    fresh = [make_flashrag(item) for item in fresh_items]
    write_jsonl(DATA_DIR / "dev.jsonl", dev)
    write_jsonl(DATA_DIR / "test.jsonl", test)
    write_jsonl(DATA_DIR / "fresh_hard_test.jsonl", fresh)

    split_items = {"dev": dev_items, "test": test_items, "fresh_hard": fresh_items}
    for split, items in split_items.items():
        rows = []
        for item in items:
            for chunk_id in item["source_chunk_ids"]:
                rows.append(f"{item['id']}\t{chunk_id}\t1\n")
        (DATA_DIR / "qrels" / f"{split}.tsv").write_text("".join(rows), encoding="utf-8")

    if INVALID_DIR.exists():
        shutil.rmtree(INVALID_DIR)
    shutil.copytree(DATA_DIR, INVALID_DIR)
    (INVALID_DIR / "qrels" / "test.tsv").unlink()


if __name__ == "__main__":
    main()
