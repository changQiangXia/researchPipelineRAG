# Phase 7K: Hashed Dense Formal Benchmark

Recorded: 2026-06-28

Dataset:

```text
data/real_pilot_nickel_superalloy_medium_plus
```

Split:

```text
fresh_hard
```

## Purpose

Phase 7K adds a formal local dense-style retrieval benchmark while the
FlashRAG neural dense/reranker dependency stack remains isolated by Phase 7A.
This is a non-neural benchmark. It does not claim that FlashRAG dense retrieval,
sentence-transformers, FlagEmbedding, or a neural reranker has run successfully
in the current environment.

The purpose is narrower and explicit:

- add a deterministic dense-vector baseline using signed hashing plus TF-IDF;
- add a second variant with lightweight lexical-overlap reranking;
- run both methods on the real medium-plus Fresh-Hard split;
- write normal DomainRAG result rows and a normal summary report;
- preserve the existing live-API boundary by making 0 DeepSeek calls.

## Methods

The benchmark writes two methods:

```text
hashed_dense_oracle_reader
hashed_dense_lexical_rerank_oracle_reader
```

Both methods use `benchmark/domainrag/hashed_dense_benchmark.py`.

`hashed_dense_oracle_reader` builds fixed-width vectors from corpus and query
tokens using deterministic signed hashing and corpus-level IDF weights. It ranks
contexts by cosine similarity.

`hashed_dense_lexical_rerank_oracle_reader` first retrieves candidates with the
same hashed dense index, then reranks candidates with a weighted lexical-overlap
bonus. This is a local rerank baseline, not a neural cross-encoder reranker.

Both methods use the same oracle-reader convention as the existing local
retrieval baselines: the row prediction is the gold answer only when the
retrieved context set hits at least one qrels context. This isolates retrieval
quality from LLM generation quality.

## Commands

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-hashed-dense \
  --dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark \
  --split fresh_hard \
  --top-k 5 \
  --dimensions 512

PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/real_pilot_nickel_superalloy_medium_plus/fresh_hard_hashed_dense_results.jsonl \
  --output outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/report_fresh_hard
```

## Outputs

```text
outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/real_pilot_nickel_superalloy_medium_plus/fresh_hard_hashed_dense_results.jsonl
outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/report_fresh_hard/summary.json
outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/report_fresh_hard/summary.md
```

The result file contains 100 rows:

- 50 rows for `hashed_dense_oracle_reader`;
- 50 rows for `hashed_dense_lexical_rerank_oracle_reader`.

Each row records:

- `retrieved_context_ids`;
- `retrieval_scores`;
- normal typed answer metrics;
- qrels-derived retrieval metrics;
- `api_calls = 0`;
- `metadata.benchmark_family = local_hashed_dense`;
- `metadata.neural_model = false`.

## Results

Fresh-Hard summary:

| method | questions | retrieval_hit | retrieval_recall | retrieval_mrr | api_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hashed_dense_oracle_reader` | 50 | 0.8800 | 0.7083 | 0.6240 | 0 |
| `hashed_dense_lexical_rerank_oracle_reader` | 50 | 0.9000 | 0.7183 | 0.6260 | 0 |

The lexical-overlap rerank variant improves retrieval hit from 0.88 to 0.90
and retrieval recall from 0.7083 to 0.7183 on this Fresh-Hard split.

For reference, Phase 7B recorded these medium-plus Fresh-Hard retrieval metrics:

| method | retrieval_hit | retrieval_recall | retrieval_mrr |
| --- | ---: | ---: | ---: |
| `lexical_rag` | 0.8800 | 0.7033 | 0.6047 |
| `bm25s_oracle_reader` | 0.8600 | 0.7117 | 0.6073 |

This places the local hashed dense baseline in the same evidence regime as the
existing lexical/BM25 local retrieval checks, while still leaving neural
dense/rerank execution open.

## Interpretation

Phase 7K is useful because it gives the project a formal dense-vector retrieval
benchmark on real data without changing the fragile current ML dependency stack.
It is also intentionally conservative:

- it is non-neural;
- it does not use sentence-transformers or FlagEmbedding;
- it does not claim FlashRAG dense retriever readiness;
- it does not replace the Phase 7A isolated dense/rerank dependency plan;
- it does not close the final human source-signoff, chunk-scale, or question-scale gaps.

The correct current status is:

```text
formal_local_dense_style_benchmark_complete
neural_dense_or_reranker_claim_not_made
```

## Verification

Fresh verification commands:

```bash
PYTHONPATH=benchmark pytest tests/test_hashed_dense_benchmark.py tests/test_cli.py::test_run_hashed_dense_command_writes_retrieval_rows
PYTHONPATH=benchmark pytest tests/test_phase7k_outputs.py
```

Broader completion checks before commit should still include:

```bash
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
python -m json.tool docs/reports/rag-md-implementation-audit.json >/tmp/phase7k-audit.json
git diff --check
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs/archive/provenance/source-workflow outputs/archive/provenance/retrieval-diagnostics benchmark scripts tests docs pyproject.toml README.md || true
```
