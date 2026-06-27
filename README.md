# DomainRAG-Bench

First milestone implementation for a domain RAG benchmark.

This milestone builds a local data contract, an example dataset, validation, minimal benchmark execution, type-specific scoring, and reports. It does not call live APIs, clone upstream repositories, or process real papers.

## First Milestone Commands

```bash
python scripts/create_example_domain.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain
PYTHONPATH=benchmark python -m domainrag.cli run --dataset data/example_domain --output outputs --methods no_rag,mock_rag --split dev
PYTHONPATH=benchmark python -m domainrag.cli report --input outputs/example_domain/dev_results.jsonl --output reports/example_domain
```

The first milestone uses mocked/no-RAG execution only. It does not call live model APIs.
