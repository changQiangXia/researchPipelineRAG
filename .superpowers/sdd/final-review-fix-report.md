# Final Review Fix Report

## Status

DONE

## Files Changed

- `.gitignore`
- `benchmark/domainrag/schema.py`
- `benchmark/domainrag/validator.py`
- `data/example_domain/canonical_dataset.jsonl`
- `data/example_domain/dev.jsonl`
- `data/example_domain/test.jsonl`
- `data/invalid_fixtures/missing_qrels/canonical_dataset.jsonl`
- `data/invalid_fixtures/missing_qrels/dev.jsonl`
- `data/invalid_fixtures/missing_qrels/test.jsonl`
- `docs/data-contract.md`
- `outputs/example_domain/dev_results.jsonl`
- `scripts/create_example_domain.py`
- `tests/test_validator.py`

## Issue-By-Issue Fix Summary

1. Validator allows extra public fields, including forbidden metadata fields.
   - Added exact-field validation for `corpus.jsonl`, `canonical_dataset.jsonl`, and split JSONL rows.
   - Added recursive forbidden-field rejection for public rows and nested objects/arrays.
   - Added explicit forbidden-field families for DOI, author/authors, venue, page/page_number, original PDF path, and original paper title.
   - Tightened contract wording in `docs/data-contract.md`.

2. Split records are not checked for metadata consistency with `canonical_dataset.jsonl`.
   - Built canonical record lookup during validation.
   - Compared split `golden_answers` to canonical `answer`.
   - Compared split metadata `question_type`, `source_chunk_ids`, `knowledge_type`, `difficulty`, `answer_aliases`, and `required_points` against canonical values.
   - Compared split metadata `correct_options` against canonical answers for choice questions.
   - Enforced exact split metadata field sets, including missing and unexpected keys.

3. Choice option validation is too weak.
   - Enforced exact single-choice option keys `A-D`.
   - Enforced exact multiple-choice option keys `A-E` or `A-F`.
   - Rejected blank and non-string option values.
   - Rejected choice answers that are not present in the option key set.
   - Added focused regression coverage for malformed multiple-choice keys and invalid option values.

4. Public example distractor text contains forbidden metadata terms.
   - Replaced metadata-themed distractors in the example generator with neutral domain distractors.
   - Regenerated example and invalid-fixture data from the generator.

5. Python cache hygiene.
   - Added root `.gitignore` entries for `__pycache__/`, `.pytest_cache/`, and `*.py[cod]`.
   - Removed untracked cache directories before final status and commit.

## Commands Run And Output Summaries

1. `pytest tests/test_validator.py -q`
   - Exit: `1`
   - Summary: 5 new regression tests failed before implementation, covering forbidden fields, split drift, split metadata shape, malformed multiple-choice keys, and invalid option values.

2. `pytest tests/test_validator.py -q`
   - Exit: `0`
   - Summary: `12` validator tests passed after implementation.

3. `python scripts/create_example_domain.py`
   - Exit: `0`
   - Summary: regenerated `data/example_domain` and `data/invalid_fixtures/missing_qrels`.

4. `pytest -q`
   - Exit: `0`
   - Summary: full test suite passed.

5. `PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain`
   - Exit: `0`
   - Output: `data/example_domain is valid`

6. `PYTHONPATH=benchmark python -m domainrag.cli run --dataset data/example_domain --output outputs --methods no_rag,mock_rag --split dev`
   - Exit: `0`
   - Output: `results written to outputs/example_domain/dev_results.jsonl`

7. `PYTHONPATH=benchmark python -m domainrag.cli report --input outputs/example_domain/dev_results.jsonl --output reports/example_domain`
   - Exit: `0`
   - Output: `report written to reports/example_domain/summary.md and reports/example_domain/summary.json`

8. `PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/invalid_fixtures/missing_qrels`
   - Exit: `1`
   - Output: `data/invalid_fixtures/missing_qrels/qrels/test.tsv: file does not exist`

9. `git status --short`
   - Exit: `0`
   - Summary before commit:
     - modified validator/schema/tests/docs/generator/generated data/output files
     - new `.gitignore`

10. `git status --short`
    - Exit: `0`
    - Summary after commit: clean working tree with no staged, modified, or untracked files.

## Commit SHA(s)

- `94842679f58d5ee8a1335b13ce1b37fed2451b95` `fix: tighten dataset validation`

## Concerns

- None.
