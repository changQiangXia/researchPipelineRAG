from __future__ import annotations

QUESTION_TYPES = {"single_choice", "multiple_choice", "fill_blank", "short_answer"}
KNOWLEDGE_TYPES = {
    "fact",
    "parameter",
    "condition",
    "method",
    "mechanism",
    "comparison",
    "synthesis",
}
DIFFICULTIES = {"easy", "medium", "hard"}

REQUIRED_CANONICAL_FIELDS = {
    "id",
    "question_type",
    "question",
    "options",
    "answer",
    "answer_aliases",
    "reference_answer",
    "required_points",
    "source_chunk_ids",
    "subdomain",
    "knowledge_type",
    "difficulty",
    "quality_score",
}

REQUIRED_FLASHRAG_FIELDS = {"id", "question", "golden_answers", "metadata"}
REQUIRED_CORPUS_FIELDS = {"id", "contents"}
