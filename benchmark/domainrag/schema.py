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

SPLIT_METADATA_BASE_FIELDS = {
    "question_type",
    "source_chunk_ids",
    "knowledge_type",
    "difficulty",
    "answer_aliases",
    "required_points",
}
SPLIT_METADATA_CHOICE_FIELDS = {"correct_options"}

FORBIDDEN_PUBLIC_FIELD_FAMILIES = {
    "doi",
    "author",
    "authors",
    "venue",
    "page",
    "pagenumber",
    "page_number",
    "originalpdfpath",
    "original_pdf_path",
    "originalpapertitle",
    "original_paper_title",
}
