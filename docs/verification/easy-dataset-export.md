# Easy Dataset Export Verification

Recorded: 2026-06-27T11:38:08Z

Phase: 2B - Easy Dataset Intake + DomainRAG Exporter

## Scope

This verification covers the DomainRAG-owned Easy Dataset export adapter. It does not modify Easy Dataset upstream source and does not call live DeepSeek or other model APIs.

## Upstream Intake

- Easy Dataset URL: `https://github.com/ConardLi/easy-dataset.git`
- Local ignored checkout: `dataset-factory/easy-dataset-fork/`
- Inspected commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Baseline notes: [docs/baseline/easy-dataset-baseline.md](../baseline/easy-dataset-baseline.md)
- Architecture notes: [docs/architecture-easy-dataset.md](../architecture-easy-dataset.md)

## Commands

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_adapter.py -q
PYTHONPATH=benchmark pytest tests/test_cli.py::test_export_domainrag_module_entrypoint_writes_valid_dataset -q
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
python scripts/export_easy_dataset_example.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
pytest
```

## Observed Output

Focused exporter tests:

```text
...... [100%]
```

CLI focused test:

```text
. [100%]
```

CLI export:

```text
DomainRAG dataset written to outputs/domainrag/example_easy_dataset
```

Script export and validation:

```text
DomainRAG dataset written to outputs/domainrag/example_easy_dataset
outputs/domainrag/example_easy_dataset is valid
```

Full test suite:

```text
64 passed in 2.60s
```

## Generated Files

```text
outputs/domainrag/example_easy_dataset/canonical_dataset.jsonl
outputs/domainrag/example_easy_dataset/corpus.jsonl
outputs/domainrag/example_easy_dataset/dataset_card.md
outputs/domainrag/example_easy_dataset/dev.jsonl
outputs/domainrag/example_easy_dataset/fresh_hard_test.jsonl
outputs/domainrag/example_easy_dataset/qrels/dev.tsv
outputs/domainrag/example_easy_dataset/qrels/fresh_hard.tsv
outputs/domainrag/example_easy_dataset/qrels/test.tsv
outputs/domainrag/example_easy_dataset/statistics.json
outputs/domainrag/example_easy_dataset/test.jsonl
```

## Statistics

```json
{
  "corpus_count": 3,
  "dataset_name": "example_easy_dataset",
  "difficulty_counts": {
    "easy": 1,
    "hard": 1,
    "medium": 1
  },
  "question_count": 3,
  "question_type_counts": {
    "fill_blank": 1,
    "short_answer": 1,
    "single_choice": 1
  },
  "required_splits": [
    "dev",
    "fresh_hard",
    "test"
  ],
  "split_counts": {
    "dev": 1,
    "fresh_hard": 1,
    "test": 1
  }
}
```

## Boundaries

- `dataset-factory/easy-dataset-fork/` is ignored and not tracked.
- Phase 2B consumes an enriched Easy Dataset-style fixture under `fixtures/easy_dataset/example_export`.
- Public DomainRAG outputs strip Easy Dataset source metadata such as DOI, authors, venue, page number, original PDF path, and original paper title fields.
- DeepSeek configuration is example-only and references `DEEPSEEK_API_KEY`; no key is stored.
