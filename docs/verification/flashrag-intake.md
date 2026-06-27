# FlashRAG Intake Verification

Date: 2026-06-27
Phase: 2A - FlashRAG Intake + DomainRAG Adapter

## Upstream

- FlashRAG URL: `https://github.com/RUC-NLPIR/FlashRAG.git`
- Baseline commit: `e0e73399ce8d4563397b5fb4980de72a9c5e15a6`
- Local checkout for source inspection only: `benchmark/flashrag-fork/`

`benchmark/flashrag-fork/` remains ignored and uncommitted in this repository. Phase 2A only records compatibility notes and generated bundle artifacts.

## Dependency Import Baseline

Source inspection baseline is recorded in [docs/baseline/flashrag-baseline.md](../baseline/flashrag-baseline.md). The lightweight verification environment does not install full FlashRAG runtime dependencies.

Observed baseline result:

```text
ModuleNotFoundError: No module named 'transformers'
```

Interpretation:

- Phase 2A verification must not require importing FlashRAG.
- Full FlashRAG dependencies such as `transformers`, `torch`, and `datasets` are deferred.
- Live retriever/generator execution is deferred to a later phase with a dependency-complete environment.

## Commands Run

```bash
pytest
python scripts/create_example_domain.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/example_domain --output outputs/flashrag --dataset-name example_domain
python scripts/prepare_flashrag_example.py
git status --short
```

## Command Outputs

- `pytest`: `57 passed`
- `python scripts/create_example_domain.py`: exit `0`
- `validate-data`: `data/example_domain is valid`
- `prepare-flashrag`: `FlashRAG bundle written to outputs/flashrag/example_domain`
- `prepare_flashrag_example.py`: `FlashRAG config written to /root/autodl-tmp/RAG/DomainRAG-Bench/.worktrees/phase-2a-flashrag-adapter/outputs/flashrag/example_domain_flashrag.yaml`
- `git status --short` after the smoke sequence: clean

## Output Paths

- Bundle directory: `outputs/flashrag/example_domain/`
- Prepared split files:
  - `outputs/flashrag/example_domain/dev.jsonl`
  - `outputs/flashrag/example_domain/test.jsonl`
  - `outputs/flashrag/example_domain/fresh_hard.jsonl`
- Corpus copy: `outputs/flashrag/example_domain/corpus.jsonl`
- Qrels copies:
  - `outputs/flashrag/example_domain/qrels/dev.tsv`
  - `outputs/flashrag/example_domain/qrels/test.tsv`
  - `outputs/flashrag/example_domain/qrels/fresh_hard.tsv`
- Example config: `outputs/flashrag/example_domain_flashrag.yaml`

## Known Limitations

- Phase 2A does not install or import FlashRAG as part of required verification.
- Phase 2A does not call live APIs or run real generation.
- The prepared bundle is a compatibility artifact for later FlashRAG execution, not a full FlashRAG experiment result.

## Final Review Follow-up

- Added a pre-cleanup overlap guard so `prepare_flashrag_bundle(...)` rejects any output dataset directory that resolves to the source dataset directory, a path nested inside it, or a parent path that would delete it.
- Added validation for empty requested split sets so the adapter and CLI both reject unusable bundles such as `--splits ,`.
- Re-ran the Phase 2A smoke sequence after the fix and confirmed it does not leave committed output artifacts modified.
