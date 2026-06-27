from domainrag.domain_evaluator import evaluate_record


def test_single_choice_accuracy():
    record = {"golden_answers": ["B"], "metadata": {"question_type": "single_choice"}}
    assert evaluate_record(record, "答案是B")["single_choice_accuracy"] == 1.0


def test_multiple_choice_metrics():
    record = {"golden_answers": ["A", "C", "D"], "metadata": {"question_type": "multiple_choice"}}
    scores = evaluate_record(record, "A,D")
    assert scores["multiple_choice_exact_match"] == 0.0
    assert round(scores["multiple_choice_micro_f1"], 3) == 0.8
    assert round(scores["multiple_choice_jaccard"], 3) == 0.667


def test_fill_blank_alias_match():
    record = {
        "golden_answers": ["ingress"],
        "metadata": {"question_type": "fill_blank", "answer_aliases": ["oxygen ingress"]},
    }
    scores = evaluate_record(record, "oxygen ingress")
    assert scores["fill_blank_alias_match"] == 1.0


def test_short_answer_key_point_coverage():
    record = {
        "golden_answers": ["Fine precipitates impede dislocation motion."],
        "metadata": {
            "question_type": "short_answer",
            "required_points": ["fine precipitates", "dislocation motion", "high-temperature strength"],
        },
    }
    scores = evaluate_record(record, "Fine precipitates impede dislocation motion.")
    assert round(scores["key_point_coverage"], 3) == 0.667
