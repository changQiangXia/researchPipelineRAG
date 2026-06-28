# DomainRAG-Bench Medium Pilot Final Report

Recorded: 2026-06-28

Blueprint: `/root/autodl-tmp/RAG/RAG.md`

Repository milestone: Phase 7F provisional source decisions and stop point

## Executive Summary

DomainRAG-Bench now has a validated medium-plus pilot for a nickel-superalloy
high-temperature-failure domain. The project implements the core engineering
chain requested by `RAG.md`: a DomainRAG data contract, Easy Dataset-style
intake, FlashRAG bundle preparation, real FlashRAG BM25 retrieval, typed
scoring, live DeepSeek answer generation, live DeepSeek Judge evaluation,
Fresh-Hard comparison, a small human calibration audit, and a bounded
medium-plus live subset.

Phase 7D adds a real OpenAlex-backed source-acquisition checkpoint for the
remaining demo-scale gap: 124 candidate papers across 8 subtopics, including
113 research-article candidates, 11 review candidates, and 115 open-access
candidates. These rows are explicitly `candidate_for_manual_verification`; they
are not a final inclusion list.

Phase 7E converts that candidate pool into a machine pre-screening and
full-text processing queue. It queues all 124 candidates, identifies 115
open-access/full-text-ready candidates, and flags review-paper gaps in
`coatings`, `life_prediction`, and `microstructure_characterization`. It still
does not finalize any source.

Phase 7F converts the screening queue into a provisional source-decision
package: 82 `accepted_provisional`, 33 `pending_manual_review`, 9
`rejected_prescreen`, and a 115-row provisional source whitelist. This is the
recommended pause point for the current engineering/source-screening effort.

The current project is not yet a full `RAG.md` demo-scale dataset. The best
dataset has 100 corpus chunks and 150 questions; `RAG.md` calls for 1,000-3,000
chunks and 300-500 questions for the demo tier. Phase 7D/7E/7F materially
advance the paper acquisition, screening, and provisional decision
prerequisites, but final manual source verification, full-text parsing, chunk
extraction, and question generation are still open.

Completion estimate:

- Excluding final scale: about 99%
- Including `RAG.md` demo scale: 89%-90%

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

Phase 7C adds a bounded medium-plus live subset:

- Dataset: `real_pilot_nickel_superalloy_medium_plus`
- Split: Fresh-Hard
- Questions: 12
- Methods: `no_rag`, `lexical_rag`, `flashrag_bm25_live_deepseek`
- Answer rows: 36
- Judge rows: 36
- Total live API calls: 75
- Answer/Judge errors: 0

Main evidence:

- `outputs/phase6e/medium_fresh_hard_comparison/summary.json`
- `outputs/phase6e/medium_fresh_hard_comparison/summary.md`
- `outputs/phase7c/medium_plus_live_subset/comparison/summary.json`
- `docs/verification/medium-live-deepseek-eval.md`
- `docs/verification/medium-plus-live-subset.md`
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

## Phase 7C Medium-Plus Live Subset

Phase 7C runs live DeepSeek answer generation and live DeepSeek Judge scoring
on a bounded, diagnostic subset of the medium-plus Fresh-Hard split.

The committed run uses the first 12 Fresh-Hard questions. That subset includes
partial-recall rows and one BM25s retrieval miss, so it is more useful than an
8-question sample that happened to have saturated retrieval hits.

Output evidence:

- `outputs/phase7c/medium_plus_live_subset/answers/real_pilot_nickel_superalloy_medium_plus/fresh_hard_deepseek_results.jsonl`
- `outputs/phase7c/medium_plus_live_subset/judge/real_pilot_nickel_superalloy_medium_plus/fresh_hard_judge_results.jsonl`
- `outputs/phase7c/medium_plus_live_subset/judge_report/summary.json`
- `outputs/phase7c/medium_plus_live_subset/comparison/summary.json`
- `docs/verification/medium-plus-live-subset.md`

Comparison summary:

| method | questions | retrieval hit | retrieval recall | answer score | correctness | faithfulness | hallucination risk | unsupported claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flashrag_bm25_live_deepseek` | 12 | 0.9167 | 0.7569 | 0.8554 | 5.0000 | 5.0000 | 0.0000 | 0 |
| `lexical_rag` | 12 | 0.9167 | 0.7361 | 0.8540 | 5.0000 | 5.0000 | 0.0000 | 0 |
| `no_rag` | 12 | 0.0000 | 0.0000 | 0.3074 | 2.5833 | 1.2500 | 3.7500 | 18 |

Interpretation: the medium-plus data now has real model-backed evidence in
addition to deterministic retrieval diagnostics. Retrieval-grounded methods
remain faithful on this subset, while No-RAG produces unsupported claims and
higher hallucination risk even when it answers some choice questions correctly.

## Phase 7D Demo-Scale Source Acquisition

Phase 7D starts the source-acquisition path needed for strict `RAG.md`
demo-scale work. It does not expand the public benchmark dataset yet; it
creates a reproducible candidate pool that must be manually screened before
chunk extraction.

Output evidence:

- `outputs/phase7d/demo_scale_source_acquisition/candidates.jsonl`
- `outputs/phase7d/demo_scale_source_acquisition/coverage.json`
- `outputs/phase7d/demo_scale_source_acquisition/summary.md`
- `docs/verification/demo-scale-source-acquisition.md`

Coverage:

| metric | value |
| --- | ---: |
| candidate papers | 124 |
| research article candidates | 113 |
| review candidates | 11 |
| open-access candidates | 115 |
| subtopics covered | 8 |
| final included sources | 0 |

Subtopic coverage:

| subtopic | candidates | research | reviews | open access |
| --- | ---: | ---: | ---: | ---: |
| additive_manufacturing | 8 | 5 | 3 | 6 |
| coatings | 9 | 9 | 0 | 9 |
| creep | 28 | 26 | 2 | 27 |
| fatigue | 10 | 9 | 1 | 9 |
| hot_corrosion | 17 | 15 | 2 | 14 |
| life_prediction | 12 | 12 | 0 | 11 |
| microstructure_characterization | 15 | 15 | 0 | 15 |
| oxidation | 25 | 22 | 3 | 24 |

Interpretation: the candidate pool now crosses the RAG.md 100-paper lower
bound and spans the required nickel-superalloy high-temperature-failure
subtopics. It remains a candidate-only acquisition artifact. The next gate is
manual venue, DOI, article-type, retraction, full-text, and domain-relevance
verification, followed by a final 100-180 source whitelist.

## Phase 7E Source Screening Queue

Phase 7E turns the Phase 7D candidate pool into a deterministic queue for
manual source verification and full-text processing. It does not claim that any
source is accepted; every row remains `not_finalized` and
`needs_manual_verification`.

Output evidence:

- `outputs/phase7e/source_screening_queue/screening_queue.jsonl`
- `outputs/phase7e/source_screening_queue/screening_summary.json`
- `outputs/phase7e/source_screening_queue/summary.md`
- `docs/verification/source-screening-queue.md`

Queue summary:

| metric | value |
| --- | ---: |
| candidate papers queued | 124 |
| high priority candidates | 3 |
| medium priority candidates | 79 |
| low priority candidates | 42 |
| open-access/full-text ready candidates | 115 |
| access-check-needed candidates | 9 |
| final included sources | 0 |

Subtopic queue:

| subtopic | candidates | high | medium | low | full-text ready | reviews |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| additive_manufacturing | 8 | 0 | 4 | 4 | 6 | 3 |
| coatings | 9 | 1 | 6 | 2 | 9 | 0 |
| creep | 28 | 0 | 24 | 4 | 27 | 2 |
| fatigue | 10 | 0 | 8 | 2 | 9 | 1 |
| hot_corrosion | 17 | 2 | 7 | 8 | 14 | 2 |
| life_prediction | 12 | 0 | 5 | 7 | 11 | 0 |
| microstructure_characterization | 15 | 0 | 10 | 5 | 15 | 0 |
| oxidation | 25 | 0 | 15 | 10 | 24 | 3 |

Interpretation: the project now has a practical queue for the next manual
screening pass. The best immediate value is to review the 3 high-priority and
79 medium-priority rows first, while running targeted review-paper search for
`coatings`, `life_prediction`, and `microstructure_characterization`.

## Phase 7F Source Decisions

Phase 7F turns the Phase 7E screening queue into provisional source decisions.
It is explicitly not final manual verification. Its purpose is to create a
clean pause point with a usable source-side handoff.

Output evidence:

- `outputs/phase7f/source_decisions/source_decisions.jsonl`
- `outputs/phase7f/source_decisions/provisional_source_whitelist.jsonl`
- `outputs/phase7f/source_decisions/decision_summary.json`
- `outputs/phase7f/source_decisions/summary.md`
- `docs/verification/source-decisions-and-stop-point.md`

Decision summary:

| metric | value |
| --- | ---: |
| candidate decisions | 124 |
| accepted provisional | 82 |
| pending manual review | 33 |
| rejected prescreen | 9 |
| provisional source whitelist | 115 |
| stop recommendation | pause_after_phase7f |

Subtopic decisions:

| subtopic | candidates | accepted | pending | rejected | whitelist | reviews |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| additive_manufacturing | 8 | 4 | 2 | 2 | 6 | 3 |
| coatings | 9 | 7 | 2 | 0 | 9 | 0 |
| creep | 28 | 24 | 3 | 1 | 27 | 2 |
| fatigue | 10 | 8 | 1 | 1 | 9 | 1 |
| hot_corrosion | 17 | 9 | 5 | 3 | 14 | 2 |
| life_prediction | 12 | 5 | 6 | 1 | 11 | 0 |
| microstructure_characterization | 15 | 10 | 5 | 0 | 15 | 0 |
| oxidation | 25 | 15 | 9 | 1 | 24 | 3 |

Interpretation: the provisional whitelist count is now within the RAG.md
100-180 source-paper range, but it remains provisional. If work resumes, the
first source-side tasks are manual verification and targeted review search for
`coatings`, `life_prediction`, and `microstructure_characterization`.

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
| Literature source policy | partial | Source manifests, a 124-paper OpenAlex candidate pool, Phase 7E screening queue, and Phase 7F provisional decisions exist, but no final manually verified 100-180-paper top-venue whitelist is committed. |
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
| Demo scale | partial | 100 chunks / 150 questions plus a 115-row provisional source whitelist versus RAG.md target of 1,000-3,000 chunks / 300-500 questions. |
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
- 124 OpenAlex source candidates for the next expansion
- 115 open-access/full-text-ready queue candidates
- 115 provisional source-whitelist rows
- 0 final manually verified source inclusions

The implementation path is ready for more scale, but the dataset itself is
still far below the requested demo scale. A true demo-scale build should not be
claimed until the same validation, FlashRAG preparation, retrieval comparison,
live answer/Judge evaluation, calibration packet, and at least sampled human
audit are repeated on a dataset at or near 1,000 chunks. The Phase 7D candidate
pool, Phase 7E queue, and Phase 7F provisional decisions are the source-side
handoff for that route, not the completed scale expansion.

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
- A bounded medium-plus live DeepSeek answer/Judge subset.
- A 124-paper OpenAlex candidate pool for demo-scale source screening.
- A Phase 7E machine pre-screening and full-text processing queue.
- A Phase 7F provisional source-decision package and 115-row provisional whitelist.
- Deterministic diagnostic baselines.
- Live DeepSeek answer generation and Judge evaluation.
- A five-method Fresh-Hard comparison.
- A human calibration audit.
- A structured `RAG.md` implementation audit.

The project is strong enough to support a report or demo focused on method
diagnostics, benchmark engineering, and source-screening readiness. It is not
yet strong enough to claim the full `RAG.md` dataset scale.

## Next Phase Recommendation

Recommended next phase if work resumes: Phase 7G manual verification and
demo-scale extraction.

This is the recommended pause point. If work resumes, the high-value path is:

1. Verify venue quality, DOI/title/year, article type, retraction status,
   full-text processability, and domain relevance.
2. Fill subtopic review gaps for coatings, life prediction, and
   microstructure characterization.
3. Promote the 115-row provisional whitelist into a final 100-180 source
   whitelist.
4. Extract chunks only from verified sources and expand toward at least 1,000
   chunks / 300 questions.
5. Keep the same validation, FlashRAG bundle preparation, retrieval comparison,
   live answer/Judge, and sampled human calibration gates.
6. Run dense/rerank only in the isolated environment described by Phase 7A, not
   by mutating the current AutoDL runtime.

If the goal is a defensible near-term project deliverable, finish with this
medium-plus report and append a scale roadmap. If the goal is strict `RAG.md`
completion, the next work must be dataset scale, not another evaluator feature.

## Verification Commands

Run from repository root:

```bash
PYTHONPATH=benchmark pytest tests/test_phase6g_report.py
PYTHONPATH=benchmark pytest tests/test_phase7c_live_subset.py
PYTHONPATH=benchmark pytest tests/test_phase7d_outputs.py tests/test_source_acquisition.py tests/test_cli.py -k 'phase7d or source_acquisition or acquire_sources'
PYTHONPATH=benchmark pytest tests/test_phase7e_outputs.py tests/test_source_screening.py tests/test_cli.py -k 'phase7e or source_screening or screen_sources'
PYTHONPATH=benchmark pytest tests/test_phase7f_outputs.py tests/test_source_decisions.py tests/test_cli.py -k 'phase7f or source_decisions or decide_sources'
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
PYTHONPATH=benchmark pytest tests/test_real_pilot_medium_plus_assets.py tests/test_phase7b_outputs.py
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures pyproject.toml || true
git diff --check
```
