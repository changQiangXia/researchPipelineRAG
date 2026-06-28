# Dense/Rerank Isolated Readiness

Phase: Phase 7A

## Decision

Do not install these dependencies into the current AutoDL environment.

- Current decision: `use_isolated_environment`
- Safe to mutate current environment: False
- Blocker count: 6

## Target Methods

- `flashrag_dense`
- `flashrag_reranker`
- `flashrag_bm25_plus_reranker`

## Isolated Environment

- Python: 3.10
- Requirements file: `requirements/flashrag-dense-rerank.txt`
- Pip requirements:
  - `torch>=2.4`
  - `transformers>=4.40,<5`
  - `sentence-transformers>=3.0`
  - `FlagEmbedding>=1.3`
  - `scikit-learn>=1.4`
  - `faiss-cpu>=1.8`
  - `numpy>=1.26,<2`
  - `termcolor>=2.4`
  - `openai>=1.40`

## Acceptance Gates

### install_isolated_requirements

```bash
PYTHONPATH=benchmark python -m domainrag.cli dense-rerank-readiness --feasibility outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/flashrag_method_feasibility/real_pilot_nickel_superalloy_manifest.json --output outputs/archive/provenance/retrieval-diagnostics/dense-rerank-readiness/dense_rerank_readiness
```

Expected: readiness.json and summary.md are regenerated without mutating the base env

### flashrag_dense_import_probe

```bash
PYTHONPATH=benchmark python -m domainrag.cli probe-flashrag-methods --flashrag-path benchmark/flashrag-fork --output outputs/archive/provenance/retrieval-diagnostics/dense-rerank-readiness/dense_rerank_readiness/isolated_feasibility.json
```

Expected: flashrag_dense and flashrag_reranker become feasible in the isolated env

### medium_dense_retrieval_smoke

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/real_pilot_nickel_superalloy_medium --output outputs/flashrag --dataset-name real_pilot_nickel_superalloy_medium
```

Expected: medium FlashRAG bundle remains valid before dense/rerank runs

### medium_dataset_validation

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium
```

Expected: dataset is valid

### regression_tests

```bash
PYTHONPATH=benchmark pytest
```

Expected: all tests pass in the base repository and isolated env-specific tests pass separately

## Recommendation

BM25 and lexical already separate on the medium pilot. Dense/rerank should be evaluated next only inside a dependency-isolated environment.
