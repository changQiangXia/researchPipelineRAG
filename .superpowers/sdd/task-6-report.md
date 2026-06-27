# Task 6 Report: Answer Normalizer

## Summary

Implemented `domainrag.answer_normalizer` with the three required helpers:

- `normalize_choice_answer(text: str) -> list[str]`
- `normalize_text_answer(text: str) -> str`
- `alias_match(prediction: str, answers: list[str], aliases: list[str]) -> bool`

Added focused tests covering:

- single-choice normalization
- multiple-choice normalization
- text normalization
- alias matching

## Files Changed

- `benchmark/domainrag/answer_normalizer.py`
- `tests/test_answer_normalizer.py`

## Behavior

`normalize_choice_answer`:

- NFKC-normalizes the input
- uppercases it
- extracts A-Z letters
- returns sorted unique letters

`normalize_text_answer`:

- NFKC-normalizes the input
- trims and lowercases it
- converts common punctuation to spaces
- collapses repeated whitespace

`alias_match`:

- normalizes the prediction and every value in `answers` and `aliases`
- returns `True` when the normalized prediction matches any normalized candidate

## Verification

Ran:

```bash
cd /root/autodl-tmp/RAG/DomainRAG-Bench
pytest tests/test_answer_normalizer.py -q
pytest -q
```

Result:

- `tests/test_answer_normalizer.py`: `4 passed`
- full suite: `19 passed`

## Self-Review

Checked the implementation against the brief and confirmed:

- public function names and signatures match exactly
- only the two owned files were changed
- no unrelated repository files were modified
- no placeholder text or extra behavior was introduced

## Commit

- `0ca7d12` `feat: add answer normalization helpers`

## Fix Update

Adjusted `normalize_choice_answer` to only accept standalone choice tokens in the A-F range, with a compact-string fast path for inputs like `DCA`. This fixes overmatching on words such as `Answer` and `option` while preserving multi-choice normalization for compact and separated forms.

## Verification

Ran:

```bash
cd /root/autodl-tmp/RAG/DomainRAG-Bench
pytest tests/test_answer_normalizer.py -q
pytest -q
```

Result:

- `tests/test_answer_normalizer.py`: `4 passed`
- full suite: `19 passed`
