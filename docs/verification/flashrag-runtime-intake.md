# FlashRAG Runtime Intake Verification

Phase: 5A - actual FlashRAG Dataset runtime intake
Recorded: 2026-06-27T21:05:00Z

## Scope

Earlier FlashRAG work only prepared compatible files without importing FlashRAG. This phase verifies that a real FlashRAG upstream checkout can load the DomainRAG-produced FlashRAG bundle with FlashRAG's own `Dataset` class.

This is still not a full retriever/generator experiment. It is the runtime intake gate before multi-method FlashRAG execution.

## Upstream Checkout

Path:

```text
benchmark/flashrag-fork/
```

This path is ignored by git and not committed.

Commit:

```text
e0e73399ce8d4563397b5fb4980de72a9c5e15a6
```

Clone command:

```bash
source /etc/network_turbo
git clone --depth 1 https://github.com/RUC-NLPIR/FlashRAG.git benchmark/flashrag-fork
```

## Environment Finding

Current Python environment:

```text
torch: available, 2.1.2+cu121
transformers: missing
datasets: missing
faiss: missing
sentence_transformers: missing
```

Observed FlashRAG import status:

```json
{
  "flashrag.dataset.dataset": {
    "ok": true
  },
  "flashrag.config.config": {
    "ok": true
  },
  "flashrag.utils.utils": {
    "ok": false,
    "error_type": "ModuleNotFoundError",
    "error": "No module named 'transformers'"
  }
}
```

Interpretation:

- FlashRAG's `Dataset` and `Config` paths can be imported in the current environment.
- Full FlashRAG utility/pipeline imports are still blocked by missing runtime dependencies.
- This phase proves the dataset intake layer, not the full RAG method stack.

## Implementation

New verifier module:

```text
benchmark/domainrag/flashrag_runtime_intake.py
```

New script:

```text
scripts/verify_flashrag_runtime_intake.py
```

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy

python scripts/verify_flashrag_runtime_intake.py \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy \
  --dataset-name real_pilot_nickel_superalloy \
  --output outputs/archive/provenance/flashrag-integration/runtime-intake/flashrag_runtime_intake/real_pilot_nickel_superalloy_manifest.json \
  --splits dev,test,fresh_hard
```

Output manifest:

```text
outputs/archive/provenance/flashrag-integration/runtime-intake/flashrag_runtime_intake/real_pilot_nickel_superalloy_manifest.json
```

Runtime result:

```text
dev: 4 records
test: 4 records
fresh_hard: 4 records
```

First loaded item ids:

```json
{
  "dev": "ns_ht_q001",
  "test": "ns_ht_q005",
  "fresh_hard": "ns_ht_q009"
}
```

Qrels row counts:

```json
{
  "dev": 4,
  "test": 4,
  "fresh_hard": 6
}
```

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_flashrag_runtime_intake.py tests/test_phase5a_outputs.py -q
pytest
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
```

## Limitations

- Full FlashRAG pipeline execution still requires installing missing dependencies such as `transformers`, `datasets`, FAISS-related packages, and retriever/generator dependencies.
- This phase does not run BM25, dense retrieval, reranking, or generation inside FlashRAG.
- The local FlashRAG checkout remains ignored and uncommitted.

## Next Step

The next phase should install or isolate a dependency-complete FlashRAG runtime and run at least one real FlashRAG method over the prepared `real_pilot_nickel_superalloy` bundle. If full dense retriever dependencies are too heavy, the next best target is a BM25-style method first, then dense/rerank methods.
