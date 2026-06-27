# Easy Dataset DomainRAG Export Route Verification

Phase: 2C - Easy Dataset export route assets
Recorded: 2026-06-27T17:33:12Z

## Scope

This verification covers DomainRAG-owned copyable assets under:

```text
integrations/easy-dataset/domainrag-export/
```

It does not build the full Easy Dataset app in this environment. Phase 2B already recorded that the upstream build path is not a reliable completion gate here.

## Commands

Required verification for this phase:

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_integration_assets.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
git status --short --branch
```

## Expected Coverage

- The integration README and copyable Easy Dataset route/helper files exist at documented paths.
- Node parses the route/helper assets with `node --check`.
- A Node smoke test calls `buildDomainRAGBundle()` on Easy Dataset-like rows.
- The helper output is materialized into `chunks.jsonl` and `items.jsonl`.
- The existing Python `export_domainrag_bundle()` adapter consumes those files and `validate_dataset()` accepts the generated DomainRAG dataset.
- Secret-like token patterns are absent from the committed integration assets.

## Boundary

The copied Easy Dataset route emits a JSON envelope containing two file payloads rather than a zip archive. This keeps the fork patch dependency-free and makes the result easy to inspect. A UI button or zipped download can be added later inside the Easy Dataset fork if needed.
