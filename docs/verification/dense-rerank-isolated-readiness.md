# Dense/Rerank Isolated Readiness

Recorded: 2026-06-28

Phase: Phase 7A

Command surface:

```bash
PYTHONPATH=benchmark python -m domainrag.cli dense-rerank-readiness \
  --feasibility outputs/phase5e/flashrag_method_feasibility/real_pilot_nickel_superalloy_manifest.json \
  --output outputs/phase7a/dense_rerank_readiness
```

This phase converts the Phase 5E FlashRAG method feasibility manifest into an
auditable readiness package for dense retrieval and reranking. It does not claim
that dense or rerank methods have been executed. The purpose is to make the next
environment step explicit, repeatable, and safe.

## Decision

Do not install the dense/rerank dependency set into the current AutoDL runtime.

The Phase 5E feasibility manifest shows that BM25 is usable in the current
environment, while dense and rerank paths are blocked by model-backed dependency
conflicts:

- `flashrag.generator.generator` cannot import `openai`.
- `flashrag.pipeline.pipeline` cannot import `termcolor`.
- `FlagEmbedding` is missing.
- `sentence_transformers` is missing.
- `sklearn` is missing.
- The installed PyTorch is `2.1.2+cu121`, while the observed transformers path
  requires `torch>=2.4` for affected model-backed imports.

Because the base environment already supports the validated medium-pilot path,
mutating it late in the project would risk breaking the existing BM25,
DeepSeek, validation, and reporting evidence. Dense/rerank work should happen
in a separate Python 3.10 environment.

## Committed Outputs

The readiness command writes:

- `outputs/phase7a/dense_rerank_readiness/readiness.json`
- `outputs/phase7a/dense_rerank_readiness/summary.md`

The isolated dependency list is committed at:

- `requirements/flashrag-dense-rerank.txt`

The command is also available as:

```bash
PYTHONPATH=benchmark python -m domainrag.cli dense-rerank-readiness --help
```

## Target Methods

Phase 7A prepares the following method surface for a later isolated run:

- `flashrag_dense`
- `flashrag_reranker`
- `flashrag_bm25_plus_reranker`

The expected dependency stack is intentionally held outside the base runtime:

```text
torch>=2.4
transformers>=4.40,<5
sentence-transformers>=3.0
FlagEmbedding>=1.3
scikit-learn>=1.4
faiss-cpu>=1.8
numpy>=1.26,<2
termcolor>=2.4
openai>=1.40
```

## Acceptance Gates

The readiness output records the next gates before dense/rerank results can be
claimed:

1. Regenerate `readiness.json` and `summary.md` without mutating the base
   environment.
2. Create an isolated Python 3.10 environment and install
   `requirements/flashrag-dense-rerank.txt`.
3. Re-run `probe-flashrag-methods` inside that isolated environment.
4. Confirm `flashrag_dense` and `flashrag_reranker` become feasible in the
   isolated feasibility manifest.
5. Validate the medium dataset remains valid.
6. Prepare the medium FlashRAG bundle and run a dense retrieval smoke test.
7. Re-run repository regression tests.

Until those gates are satisfied, the correct status is partial readiness, not a
completed dense/rerank benchmark.

## Current RAG.md Impact

This closes the previous ambiguity around the dense/rerank gap: the project now
has a concrete isolated-readiness artifact and dependency contract. It still
does not satisfy a full dense/rerank comparison requirement because no dense or
reranker outputs have been generated yet.

The remaining high-impact work after Phase 7A is still dataset scale:

- RAG.md demo target: 1,000-3,000 chunks and 300-500 questions.
- Current medium pilot: 40 chunks and 60 questions.
