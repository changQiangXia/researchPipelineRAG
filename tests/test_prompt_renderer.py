from domainrag.prompt_renderer import render_prompt


def test_single_choice_prompt_requires_one_letter():
    record = {
        "id": "q1",
        "question": "Question?\nA. One\nB. Two\nC. Three\nD. Four",
        "metadata": {"question_type": "single_choice"},
    }

    prompt = render_prompt(record)

    assert "Question?" in prompt
    assert "Return exactly one uppercase option letter" in prompt


def test_multiple_choice_prompt_requires_sorted_letters():
    record = {
        "id": "q2",
        "question": "Question?\nA. One\nB. Two\nC. Three\nD. Four\nE. Five",
        "metadata": {"question_type": "multiple_choice"},
    }

    prompt = render_prompt(record)

    assert "Return sorted uppercase option letters separated by commas" in prompt


def test_fill_blank_prompt_requires_missing_text_only():
    record = {
        "id": "q3",
        "question": "The answer is ____.",
        "metadata": {"question_type": "fill_blank"},
    }

    prompt = render_prompt(record)

    assert "Return only the missing text" in prompt


def test_short_answer_prompt_requires_concise_answer():
    record = {
        "id": "q4",
        "question": "Why?",
        "metadata": {"question_type": "short_answer"},
    }

    prompt = render_prompt(record)

    assert "Return 1 to 4 concise sentences" in prompt
