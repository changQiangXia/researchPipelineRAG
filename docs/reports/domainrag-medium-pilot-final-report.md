# DomainRAG-Bench Medium Pilot Final Report

Recorded: 2026-06-28

Blueprint: `/root/autodl-tmp/RAG/RAG.md`

Repository milestone: Phase 7B, after `a53c18c Merge Phase 7A dense rerank readiness`

## Executive Summary

DomainRAG-Bench now has a validated medium-plus pilot for a nickel-superalloy
high-temperature-failure domain. The project implements the core engineering
chain requested by `RAG.md`: a DomainRAG data contract, Easy Dataset-style
intake, FlashRAG bundle preparation, real FlashRAG BM25 retrieval, typed
scoring, live DeepSeek answer generation, live DeepSeek Judge evaluation,
Fresh-Hard comparison, and a small human calibration audit.

The current project is not yet a full `RAG.md` demo-scale dataset. The best
dataset has 100 corpus chunks and 150 questions; `RAG.md` calls for 1,000-3,000
chunks and 300-500 questions for the demo tier. Treat this repository as a
medium-plus pilot whose non-scale engineering path is close to complete.

Completion estimate:

- Excluding final scale: 98%-99%
- Including `RAG.md` demo scale: 82%-84%

The structured audit behind this report is committed at:

```text
docs/reports/rag-md-implementation-audit.json
```

## What Is Implemented

### Data Contract

The public DomainRAG dataset contract is implemented and validated:

- `corpus.jsonl`
- `canonical_dataset.jsonl`
- `dev.jsonl`
- `test.jsonl`
- `fresh_hard_test.jsonl`
- `qrels/dev.tsv`
- `qrels/test.tsv`
- `qrels/fresh_hard.tsv`

The contract preserves `source_chunk_ids` for retrieval evaluation while
forbidding public DOI, author, venue, page, original PDF path, and paper-title
metadata.

Main evidence:

- `docs/data-contract.md`
- `benchmark/domainrag/schema.py`
- `benchmark/domainrag/validator.py`
- `tests/test_validator.py`
- `data/real_pilot_nickel_superalloy_medium_plus/`

### Easy Dataset Intake

The repository does not commit the full Easy Dataset application fork. Instead,
it implements the DomainRAG-owned boundary that consumes an Easy Dataset-style
export and provides copyable Easy Dataset integration assets.

Main evidence:

- `benchmark/domainrag/easy_dataset_adapter.py`
- `integrations/easy-dataset/domainrag-export/`
- `docs/verification/easy-dataset-domainrag-export-route.md`
- `tests/test_easy_dataset_adapter.py`
- `tests/test_easy_dataset_integration_assets.py`

This is enough for the current medium pilot because the exported
`chunks.jsonl` and `items.jsonl` fixtures can be transformed into validated
DomainRAG datasets and FlashRAG bundles.

### FlashRAG Path

FlashRAG is the single downstream benchmark framework surface. The project
prepares FlashRAG-compatible bundles and runs real FlashRAG BM25 retrieval
through the bridge. The BM25 bridge is deliberately named
`flashrag_bm25_oracle_reader` when it uses deterministic oracle reading after
retrieval, and `flashrag_bm25_live_deepseek` when the retrieved context feeds a
live DeepSeek answer run.

Main evidence:

- `benchmark/domainrag/flashrag_adapter.py`
- `benchmark/domainrag/flashrag_runtime_intake.py`
- `benchmark/domainrag/flashrag_bm25_bridge.py`
- `outputs/flashrag/real_pilot_nickel_superalloy_medium/`
- `docs/verification/flashrag-runtime-intake.md`
- `docs/verification/flashrag-bm25-bridge.md`
- `docs/verification/medium-scale-real-pilot-expansion.md`

### DeepSeek Answer And Judge

Live DeepSeek evaluation exists for the medium Fresh-Hard split. API keys are
read from environment variables and are not committed.

Phase 6E recorded:

- Base answers: 60 rows, 60 API calls, 0 errors
- Base Judge: 60 rows, 60 API calls, 0 errors
- BM25 oracle-reader Judge: 20 rows, 20 API calls, 0 errors
- BM25 live answers: 20 rows, 20 API calls, 0 errors
- BM25 live Judge: 20 rows, 20 API calls, 0 errors
- Total live API calls recorded in outputs: 180

Main evidence:

- `outputs/phase6e/medium_fresh_hard_comparison/summary.json`
- `outputs/phase6e/medium_fresh_hard_comparison/summary.md`
- `docs/verification/medium-live-deepseek-eval.md`
- `tests/test_phase6e_outputs.py`

## Phase 7B Medium-Plus Update

Phase 7B adds a larger source-backed pipeline checkpoint:

- `data/real_pilot_nickel_superalloy_medium_plus/`
- `fixtures/easy_dataset/real_pilot_nickel_superalloy_medium_plus/`
- `data/real_pilot_sources/nickel_superalloy_high_temp_failure_medium_plus/sources.jsonl`
- `outputs/flashrag/real_pilot_nickel_superalloy_medium_plus/`
- `outputs/phase7b/medium_plus_baseline/`
- `outputs/phase7b/medium_plus_bm25s/`
- `docs/verification/medium-plus-scale-expansion.md`

Shape:

| item | count |
| --- | ---: |
| corpus chunks | 100 |
| total questions | 150 |
| dev questions | 50 |
| test questions | 50 |
| fresh_hard questions | 50 |
| source records | 32 |
| multi-source questions | 86 |
| fresh_hard multi-source questions | 43 |
| single_choice | 38 |
| multiple_choice | 38 |
| fill_blank | 37 |
| short_answer | 37 |

Fresh-Hard retrieval at this scale:

| method | retrieval hit | retrieval recall | retrieval MRR |
| --- | ---: | ---: | ---: |
| oracle_context | 1.0000 | 1.0000 | 1.0000 |
| lexical_rag | 0.8800 | 0.7033 | 0.6047 |
| bm25s_oracle_reader | 0.8600 | 0.7117 | 0.6073 |
| no_rag | 0.0000 | 0.0000 | 0.0000 |

The Phase 7B FlashRAG bundle is generated. Current-environment retrieval uses
direct `bm25s` rather than the FlashRAG retriever import path because the
current AutoDL environment kills the FlashRAG retriever import after the
PyTorch/transformers mismatch documented in Phase 7A. This is recorded as a
real retrieval fallback, not as a completed FlashRAG BM25 run at medium-plus
scale.

Historical medium dataset:

```text
data/real_pilot_nickel_superalloy_medium
```

Shape:

| item | count |
| --- | ---: |
| corpus chunks | 40 |
| total questions | 60 |
| dev questions | 20 |
| test questions | 20 |
| fresh_hard questions | 20 |
| source records | 32 |
| single_choice | 15 |
| multiple_choice | 15 |
| fill_blank | 15 |
| short_answer | 15 |

The historical medium fixture covers creep, oxidation, hot corrosion, fatigue,
additive-manufacturing defects, phase-field-informed descriptors, hydrogen LCF,
film-cooling corrosion, coating interdiffusion, rejuvenation, and related
nickel-superalloy high-temperature failure knowledge.

Main evidence:

- `data/real_pilot_nickel_superalloy_medium/statistics.json`
- `data/real_pilot_sources/nickel_superalloy_high_temp_failure_medium/sources.jsonl`
- `docs/verification/medium-scale-real-pilot-expansion.md`

## Medium Fresh-Hard Results

Fresh-Hard split: 20 questions.

Comparison summary:

```text
outputs/phase6e/medium_fresh_hard_comparison/summary.json
```

| method | answer score | retrieval recall | correctness | context support | faithfulness | hallucination risk | unsupported claims | API calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle_context | 0.8358 | 1.0000 | 4.8500 | 4.7500 | 5.0000 | 0.0000 | 0 | 40 |
| lexical_rag | 0.8251 | 0.9250 | 4.7000 | 4.7500 | 4.7500 | 0.2500 | 1 | 40 |
| flashrag_bm25_live_deepseek | 0.6573 | 0.8542 | 4.3500 | 4.7000 | 4.7500 | 0.2500 | 0 | 40 |
| flashrag_bm25_oracle_reader | 0.8583 | 0.8542 | 4.7500 | 4.2000 | 4.4500 | 0.5500 | 4 | 20 |
| no_rag | 0.5153 | 0.0000 | 3.4500 | 0.0000 | 2.5000 | 2.5000 | 17 | 40 |

Interpretation:

- Oracle context is the ceiling: full retrieval recall, zero hallucination
  risk, zero unsupported claims.
- Lexical RAG is strong but not saturated: retrieval recall is 0.9250 and one
  unsupported claim remains.
- FlashRAG BM25 live DeepSeek has the same retrieval hit rate as lexical but
  weaker full-evidence recall, 0.8542. This matters most on multi-source
  questions.
- No-RAG can guess some choice/fill-blank answers, so exact-match metrics alone
  overstate its usefulness. The Judge exposes the real issue: 17 unsupported
  claims and context support of 0.0000.

The central result is stable across Phases 6C-6F: retrieval hit rate alone is
not enough. Multi-source Fresh-Hard questions require recall/full-evidence
tracking plus answer faithfulness and unsupported-claim analysis.

## Human Calibration

Phase 6F audited a 15-row subset from the 100-row Phase 6E calibration packet.
The subset evenly covers all five evaluated methods and intentionally favors
risky rows.

Main evidence:

- `outputs/phase6f/medium_human_calibration_audit/human_labels.jsonl`
- `outputs/phase6f/medium_human_calibration_audit/summary.json`
- `docs/verification/medium-human-calibration-audit.md`

Result:

| metric | agreement within 1 point | mean absolute delta |
| --- | ---: | ---: |
| correctness | 1.0000 | 0.1333 |
| context_support | 0.8667 | 0.3667 |
| faithfulness | 0.8667 | 0.3667 |

The audit supports using DeepSeek Judge as a directional evaluator for this
medium pilot. The main observed bias is conservative scoring on partial
evidence: in some BM25 oracle-reader rows, human review assigned partial
support where the Judge assigned 0.0 support/faithfulness.

## RAG.md Completion Audit

| requirement | status | evidence |
| --- | --- | --- |
| Literature source policy | partial | Source manifests exist, but no full 100-180-paper top-venue verification matrix is committed. |
| Easy Dataset intake | complete | Easy Dataset-style export adapter and copyable integration assets are tested. |
| DomainRAG data contract | complete | Contract, schema, validator, real datasets, and tests are present. |
| Public metadata safety | complete | Validator and tests enforce forbidden metadata rules. |
| DeepSeek generation/review | complete | Generation/review records, live answers, live Judge, retries, usage accounting. |
| FlashRAG single-framework path | complete | FlashRAG bundle preparation and real FlashRAG BM25 bridge are implemented. |
| Typed scoring | complete | Four question types plus retrieval, latency, tokens, API calls, and errors. |
| Fresh-Hard evaluation | complete | Fresh-Hard split and medium live comparison are committed. |
| Human calibration | complete | 15-row manual audit over Phase 6E calibration packet. |
| Method comparison | complete | Five methods compared on the same medium Fresh-Hard split. |
| Efficiency metrics | complete | Latency, tokens, API calls, total tokens, and errors are reported. |
| Demo scale | partial | 100 chunks / 150 questions versus RAG.md target of 1,000-3,000 chunks / 300-500 questions. |
| Dense/rerank methods | partial | Phase 7A adds isolated readiness outputs and gates; dense/rerank results are not yet generated. |
| Final report | complete | This report and `rag-md-implementation-audit.json`. |

See the structured form:

```text
docs/reports/rag-md-implementation-audit.json
```

## Scale Gap

This is the largest remaining gap.

`RAG.md` demo target:

- 1,000-3,000 corpus chunks
- 300-500 formal benchmark questions

Current medium-plus pilot:

- 100 corpus chunks
- 150 total questions
- 50 Fresh-Hard questions

The implementation path is ready for more scale, but the dataset itself is
still far below the requested demo scale. A true demo-scale build should not be
claimed until the same validation, FlashRAG preparation, retrieval comparison,
live answer/Judge evaluation, calibration packet, and at least sampled human
audit are repeated on a dataset at or near 1,000 chunks.

## Dense And Rerank Gap

Dense retrieval and reranking are no longer only an open-ended deferral. Phase
5E recorded that the current runtime has:

- PyTorch 2.1.2+cu121 while the installed transformers path expects PyTorch >=
  2.4 for some model-backed paths
- missing packages such as `sentence_transformers`, `FlagEmbedding`, `sklearn`,
  `termcolor`, and `openai`

BM25 produced useful retrieval-recall differences in the validated Phase 6
FlashRAG runs. In the current Phase 7B environment, importing FlashRAG retriever
modules is also affected by the PyTorch/transformers mismatch, so medium-plus
retrieval uses direct `bm25s` as a current-environment fallback. Dense/rerank
work should still be isolated in a fresh environment rather than mutating the
current AutoDL stack late in the project.

Phase 7A commits that isolated-readiness package:

- `benchmark/domainrag/dense_rerank_readiness.py`
- `requirements/flashrag-dense-rerank.txt`
- `outputs/phase7a/dense_rerank_readiness/readiness.json`
- `outputs/phase7a/dense_rerank_readiness/summary.md`
- `docs/verification/dense-rerank-isolated-readiness.md`

This is a partial implementation state. It defines the Python 3.10 isolated
environment, target methods, dependency list, and acceptance gates for
`flashrag_dense`, `flashrag_reranker`, and
`flashrag_bm25_plus_reranker`. It does not claim dense/rerank benchmark
results yet.

## What I Would Hand Over Now

The current handoff package is coherent as a medium pilot:

- A validated domain RAG data contract.
- A real medium-plus dataset with four question types and qrels.
- A FlashRAG-compatible bundle.
- A real FlashRAG BM25 retrieval path.
- A current-environment BM25s retrieval fallback for the 100/150 checkpoint.
- Deterministic diagnostic baselines.
- Live DeepSeek answer generation and Judge evaluation.
- A five-method Fresh-Hard comparison.
- A human calibration audit.
- A structured `RAG.md` implementation audit.

The project is strong enough to support a report or demo focused on method
diagnostics and benchmark engineering. It is not yet strong enough to claim
the full `RAG.md` dataset scale.

## Next Phase Recommendation

Recommended next phase: Phase 7C medium-plus live subset or demo-scale source acquisition.

Two practical options:

1. Medium-plus live subset: run bounded live DeepSeek answer/Judge evaluation
   over a sampled subset of the 50-question medium-plus Fresh-Hard split.
2. True demo-scale build: target at least 1,000 chunks / 300 questions. This
   aligns with `RAG.md`, but it requires a larger source acquisition and
   review workflow before more API evaluation.

If the goal is a defensible near-term project deliverable, finish with this
medium report and append a scale roadmap. If the goal is strict `RAG.md`
completion, the next work must be dataset scale, not another small evaluator
feature.

## Verification Commands

Run from repository root:

```bash
PYTHONPATH=benchmark pytest tests/test_phase6g_report.py
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
PYTHONPATH=benchmark pytest tests/test_real_pilot_medium_plus_assets.py tests/test_phase7b_outputs.py
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```
