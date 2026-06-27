from domainrag.answer_normalizer import alias_match, normalize_choice_answer, normalize_text_answer


def test_normalize_single_choice_variants():
    assert normalize_choice_answer("答案是B") == ["B"]
    assert normalize_choice_answer("选 b") == ["B"]


def test_normalize_multiple_choice_variants():
    assert normalize_choice_answer("A、C、D") == ["A", "C", "D"]
    assert normalize_choice_answer("DCA") == ["A", "C", "D"]


def test_normalize_text_answer():
    assert normalize_text_answer("  Oxygen，Ingress。 ") == "oxygen ingress"


def test_alias_match_accepts_aliases():
    assert alias_match("oxygen ingress", ["ingress"], ["oxygen ingress"])
