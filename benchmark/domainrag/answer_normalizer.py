from __future__ import annotations

import re
import unicodedata


CHOICE_RE = re.compile(r"[A-Z]", re.IGNORECASE)


def normalize_choice_answer(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).upper()
    letters = CHOICE_RE.findall(normalized)
    allowed = [letter for letter in letters if "A" <= letter <= "Z"]
    return sorted(set(allowed))


def normalize_text_answer(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).strip().lower()
    normalized = normalized.replace("，", ",").replace("。", ".")
    normalized = re.sub(r"[,.。；;:：!?！？]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def alias_match(prediction: str, answers: list[str], aliases: list[str]) -> bool:
    normalized_prediction = normalize_text_answer(prediction)
    candidates = [normalize_text_answer(value) for value in answers + aliases]
    return normalized_prediction in candidates
