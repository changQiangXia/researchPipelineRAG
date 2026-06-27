# First Milestone Verification

## Scope

Verified scaffold, data contract, example dataset, validator, prompt renderer, answer normalizer, evaluator, minimal benchmark runner, and report generator.

## Commands

```bash
pytest
python scripts/create_example_domain.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain
PYTHONPATH=benchmark python -m domainrag.cli run --dataset data/example_domain --output outputs --methods no_rag,mock_rag --split dev
PYTHONPATH=benchmark python -m domainrag.cli report --input outputs/example_domain/dev_results.jsonl --output reports/example_domain
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/invalid_fixtures/missing_qrels
```

## Expected Results

- `pytest` passes.
- Valid dataset validation exits `0`.
- Invalid fixture validation exits `1`.
- Benchmark run writes `outputs/example_domain/dev_results.jsonl`.
- Report generation writes `reports/example_domain/summary.md` and `reports/example_domain/summary.json`.

## Out Of Scope

- Live DeepSeek calls.
- Easy Dataset modification.
- FlashRAG upstream modification.
- Real literature processing.
- Real Fresh-Hard construction.
