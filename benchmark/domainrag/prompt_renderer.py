from __future__ import annotations


def render_prompt(record: dict) -> str:
    question_type = record["metadata"]["question_type"]
    question = record["question"]

    if question_type == "single_choice":
        instruction = (
            "Return exactly one uppercase option letter. Do not include explanation."
        )
    elif question_type == "multiple_choice":
        instruction = (
            "Return sorted uppercase option letters separated by commas, such as A,C,D. "
            "Do not include explanation."
        )
    elif question_type == "fill_blank":
        instruction = "Return only the missing text. Do not include explanation."
    elif question_type == "short_answer":
        instruction = "Return 1 to 4 concise sentences that answer the question directly."
    else:
        raise ValueError(f"unknown question_type: {question_type}")

    return f"{question}\n\n{instruction}"
