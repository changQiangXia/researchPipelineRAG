from __future__ import annotations

from collections.abc import Iterable

from domainrag.answer_normalizer import alias_match, normalize_choice_answer, normalize_text_answer


def _safe_norm_texts(values: Iterable[str]) -> list[str]:
    return [normalize_text_answer(value) for value in values]


def evaluate_record(record: dict, prediction: str) -> dict[str, float]:
    question_type = record["metadata"]["question_type"]

    if question_type == "single_choice":
        pred = normalize_choice_answer(prediction)
        gold = sorted(record["golden_answers"])
        return {"single_choice_accuracy": 1.0 if pred == gold else 0.0}

    if question_type == "multiple_choice":
        pred_set = set(normalize_choice_answer(prediction))
        gold_set = set(record["golden_answers"])
        true_positive = len(pred_set & gold_set)
        precision = true_positive / len(pred_set) if pred_set else 0.0
        recall = true_positive / len(gold_set) if gold_set else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        union = pred_set | gold_set
        jaccard = len(pred_set & gold_set) / len(union) if union else 0.0
        return {
            "multiple_choice_exact_match": 1.0 if pred_set == gold_set else 0.0,
            "multiple_choice_micro_f1": f1,
            "multiple_choice_jaccard": jaccard,
        }

    if question_type == "fill_blank":
        normalized_prediction = normalize_text_answer(prediction)
        normalized_golden_answers = _safe_norm_texts(record["golden_answers"])
        exact = 1.0 if normalized_prediction in normalized_golden_answers else 0.0
        matched = alias_match(
            prediction,
            record["golden_answers"],
            record["metadata"].get("answer_aliases", []),
        )
        return {
            "fill_blank_normalized_em": exact,
            "fill_blank_alias_match": 1.0 if matched else 0.0,
        }

    if question_type == "short_answer":
        prediction_tokens = set(normalize_text_answer(prediction).split())
        gold_tokens = set(normalize_text_answer(" ".join(record["golden_answers"])).split())
        true_positive = len(prediction_tokens & gold_tokens)
        precision = true_positive / len(prediction_tokens) if prediction_tokens else 0.0
        recall = true_positive / len(gold_tokens) if gold_tokens else 0.0
        token_f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

        required_points = record["metadata"].get("required_points", [])
        normalized_prediction = normalize_text_answer(prediction)
        covered = sum(
            1 for point in required_points if normalize_text_answer(point) in normalized_prediction
        )
        coverage = covered / len(required_points) if required_points else 0.0
        return {
            "short_answer_token_f1": token_f1,
            "key_point_coverage": coverage,
        }

    raise ValueError(f"unknown question_type: {question_type}")
