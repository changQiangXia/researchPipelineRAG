# DomainRAG-Bench Medium Pilot Status Report

Recorded: 2026-06-28

Blueprint: `/root/autodl-tmp/RAG/RAG.md`

Repository milestone: Phase 7M provisional demo-question generation checkpoint

## Executive Summary

DomainRAG-Bench now has a validated medium-plus pilot for a nickel-superalloy
high-temperature-failure domain. The project implements the core engineering
chain requested by `RAG.md`: a DomainRAG data contract, Easy Dataset-style
intake, FlashRAG bundle preparation, real FlashRAG BM25 retrieval, typed
scoring, live DeepSeek answer generation, live DeepSeek Judge evaluation,
Fresh-Hard comparison, a small human calibration audit, and a bounded
medium-plus live subset.

This is a status report for a provisional engineering milestone, not a human-final benchmark（不是 human-final benchmark）. The final-source and final-question claims remain blocked until real human source sign-off and accepted-source regeneration or verification are complete.

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

Phase 7G resumes from that pause point and starts machine-assisted source
verification plus real full-text intake. OpenAlex metadata was refreshed for all
115 provisional whitelist rows; all 115 were found and none are marked
retracted there. Full-text access was probed for the first 25 rows in 5-row
batches; 17 rows are parseable, 6 were not accessible, and 2 download attempts
failed. The combined source verification matrix now marks 1 row as a verified
source candidate, 23 rows as ready for manual finalization, and 7 as rejected
after verification, while 84 still need evidence.

Phase 7H extends the full-text probe to all 115 provisional whitelist rows.
Seventy-one rows are parseable, 37 are not accessible in the current runtime, 6
download attempts failed, and 1 download hit the 8MB truncation guard. The
combined source verification matrix now marks 2 rows as verified source
candidates, 106 rows as ready for manual finalization, and 7 rows as rejected
after verification. It still has 0 final accepted sources because
manual venue/JCR/CiteScore or flagship-source confirmation and human sign-off
remain open.

Phase 7I turns the 115-row verification matrix into a human-review packet and a
108-row candidate final whitelist queue. That queue is inside the RAG.md
100-180 source-paper target range, but it remains a handoff for real human
sign-off rather than a final accepted whitelist.

Phase 7J adds the sign-off workflow for that 108-row queue. It generates a
pending `human_signoff_template.jsonl` and an empty `final_source_whitelist.jsonl`
until real human labels are supplied. This is the correct stopping boundary for
machine-only source verification.

Phase 7K adds a formal local dense-style retrieval benchmark on the real
medium-plus Fresh-Hard split. It runs `hashed_dense_oracle_reader` and
`hashed_dense_lexical_rerank_oracle_reader` over 50 Fresh-Hard questions and
writes 100 DomainRAG result rows. This is a non-neural signed-hashing TF-IDF
benchmark with a lexical-overlap rerank variant; it does not claim FlashRAG
neural dense retriever or neural reranker execution.

Phase 7L turns the Phase 7H full-text access probe into a real full-text
chunk-extraction workflow. It re-fetches the 71 machine-parseable full-text rows,
successfully chunks 60 sources, and writes 2,196 chunk manifests, which is inside
the RAG.md demo chunk-count target of 1,000-3,000 chunks. The committed output
does not store raw chunk text; it stores chunk ids, token boundaries, counts,
hashes, and `machine_parseable_not_human_final` provenance.

Phase 7M adds a deterministic provisional 300-question dataset over the
validated 100-chunk medium-plus corpus. It writes a DomainRAG dataset, prepares
a FlashRAG bundle, runs `no_rag`, `oracle_context`, and `lexical_rag` on the
100-question Fresh-Hard split, and runs the local hashed dense diagnostics over
the same split. This closes the immediate question-count engineering gap
provisionally, with 0 live API calls.

The current project is still not a final `RAG.md` demo-scale dataset. It now has
2,196 machine-parseable full-text chunk manifests and 300 provisional questions,
but the chunks and questions are not filtered or regenerated from real
human-accepted final sources. Phase 7D/7E/7F/7G/7H/7I materially advance the
paper acquisition, screening, and provisional decision prerequisites; Phase 7J
keeps the final source gate open for real human labels; Phase 7K closes a local
dense-style benchmark gap; Phase 7L reaches the chunk-count range as manifests;
Phase 7M reaches the question-count range provisionally. Neural dense/rerank
remains an isolated environment task.

Completion status: the engineering pipeline is largely implemented, while strict `RAG.md` demo completion remains partial because final human source labels, accepted-source filtering/regeneration, and neural dense/rerank execution are still open. The previous percentage-style estimate should not be read as a human-final completion claim.

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

- `outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_fresh_hard_comparison/summary.json`
- `outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_fresh_hard_comparison/summary.md`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/comparison/summary.json`
- `docs/verification/medium-live-deepseek-eval.md`
- `docs/verification/medium-plus-live-subset.md`
- `tests/test_phase6e_outputs.py`

## Phase 7B Medium-Plus Update

Phase 7B adds a larger source-backed pipeline checkpoint:

- `data/real_pilot_nickel_superalloy_medium_plus/`
- `fixtures/easy_dataset/real_pilot_nickel_superalloy_medium_plus/`
- `data/real_pilot_sources/nickel_superalloy_high_temp_failure_medium_plus/sources.jsonl`
- `outputs/flashrag/real_pilot_nickel_superalloy_medium_plus/`
- `outputs/archive/provenance/expanded-pilots/medium-plus-baseline-and-bm25/medium_plus_baseline/`
- `outputs/archive/provenance/expanded-pilots/medium-plus-baseline-and-bm25/medium_plus_bm25s/`
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

- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/answers/real_pilot_nickel_superalloy_medium_plus/fresh_hard_deepseek_results.jsonl`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/judge/real_pilot_nickel_superalloy_medium_plus/fresh_hard_judge_results.jsonl`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/judge_report/summary.json`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/comparison/summary.json`
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

- `outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/candidates.jsonl`
- `outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/coverage.json`
- `outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/summary.md`
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

- `outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl`
- `outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_summary.json`
- `outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/summary.md`
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

- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/source_decisions.jsonl`
- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/provisional_source_whitelist.jsonl`
- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/decision_summary.json`
- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/summary.md`
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

## Phase 7G Source Verification And Full-Text Intake

Phase 7G starts the post-provisional verification path. It adds OpenAlex
metadata evidence, real full-text access probing, and a combined source
verification matrix. It still does not claim final manual verification.

Output evidence:

- `outputs/archive/provenance/source-workflow/source-verification-first-batches/source_metadata/openalex_metadata.jsonl`
- `outputs/archive/provenance/source-workflow/source-verification-first-batches/full_text_access_combined25/full_text_access.jsonl`
- `outputs/archive/provenance/source-workflow/source-verification-first-batches/source_verification_combined25/source_verification_matrix.jsonl`
- `outputs/archive/provenance/source-workflow/source-verification-first-batches/source_verification_combined25/verification_summary.json`
- `docs/verification/source-verification-and-full-text-intake.md`

OpenAlex metadata:

| metric | value |
| --- | ---: |
| provisional whitelist rows checked | 115 |
| OpenAlex records found | 115 |
| retracted rows | 0 |
| article rows | 103 |
| preprint rows | 6 |
| review rows | 1 |
| dissertation/report/other rows | 5 |

Full-text intake, first 25 rows:

| metric | value |
| --- | ---: |
| rows probed | 25 |
| downloaded | 17 |
| not accessible | 6 |
| download failed | 2 |
| parseable | 17 |
| not attempted | 8 |
| extracted characters counted | 1120613 |

Combined verification matrix:

| metric | value |
| --- | ---: |
| source rows in matrix | 115 |
| accepted final verification | 0 |
| verified source candidate | 1 |
| ready for manual finalization | 23 |
| rejected after verification | 7 |
| needs evidence | 84 |
| final whitelist claim | not_complete |

Interpretation: Phase 7G converts part of the source-side uncertainty into an
auditable queue. The main bottleneck is now less about finding metadata and more
about finishing full-text processability checks plus human venue/source-quality
sign-off. Rows marked `ready_for_manual_finalization` can be reviewed first;
rows marked `rejected_verification` should be manually spot-checked before
removal from the final source candidate set.

## Phase 7H Full-Text Intake Combined115

Phase 7H expands the real full-text access probe from the first 25 provisional
whitelist rows to all 115 rows. It also updates the verification policy so
current-runtime access failures remain manual-review items rather than hard
source rejections.

Output evidence:

- `outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_combined115/full_text_access.jsonl`
- `outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_combined115/full_text_access_summary.json`
- `outputs/archive/provenance/source-workflow/source-verification-combined/source_verification_combined115/source_verification_matrix.jsonl`
- `outputs/archive/provenance/source-workflow/source-verification-combined/source_verification_combined115/verification_summary.json`
- `docs/verification/full-text-intake-combined115.md`

Full-text intake, all 115 rows:

| metric | value |
| --- | ---: |
| rows probed | 115 |
| downloaded | 71 |
| not accessible | 37 |
| download failed | 6 |
| download truncated | 1 |
| parseable | 71 |
| not attempted | 44 |
| extracted characters counted | 4366176 |

Combined verification matrix:

| metric | value |
| --- | ---: |
| source rows in matrix | 115 |
| accepted final verification | 0 |
| verified source candidate | 2 |
| ready for manual finalization | 106 |
| rejected after verification | 7 |
| final whitelist claim | not_complete |

Interpretation: Phase 7H completes the machine access/processability pass over
the 115-row provisional whitelist. It produces a practical human-finalization
queue: 108 rows are machine-ready for human decision, and 7 rows need manual
spot-checking before removal. This is enough to enter source finalization and
chunk extraction work, but it is still not a final manually verified source
whitelist.

## Phase 7I Manual Finalization Packet

Phase 7I converts the 115-row verification matrix into a review-ready packet for
human finalization. It does not simulate human sign-off and does not claim a
final accepted whitelist.

Output evidence:

- `outputs/archive/provenance/source-workflow/manual-finalization-packet/manual_finalization_packet/manual_finalization_packet.jsonl`
- `outputs/archive/provenance/source-workflow/manual-finalization-packet/manual_finalization_packet/candidate_final_whitelist_queue.jsonl`
- `outputs/archive/provenance/source-workflow/manual-finalization-packet/manual_finalization_packet/manual_finalization_summary.json`
- `docs/verification/manual-finalization-packet.md`

Manual finalization packet:

| metric | value |
| --- | ---: |
| source rows in packet | 115 |
| candidate final whitelist queue | 108 |
| verified source candidates | 2 |
| ready for manual finalization | 106 |
| spot-check rejected sources | 7 |
| accepted final sources | 0 |
| final whitelist claim | not_complete |

Candidate queue by subtopic:

| subtopic | queue | verified | ready | reviews | research |
| --- | ---: | ---: | ---: | ---: | ---: |
| additive_manufacturing | 5 | 0 | 5 | 3 | 2 |
| coatings | 9 | 1 | 8 | 0 | 9 |
| creep | 26 | 0 | 26 | 2 | 24 |
| fatigue | 8 | 0 | 8 | 1 | 7 |
| hot_corrosion | 13 | 1 | 12 | 2 | 11 |
| life_prediction | 11 | 0 | 11 | 0 | 11 |
| microstructure_characterization | 14 | 0 | 14 | 0 | 14 |
| oxidation | 22 | 0 | 22 | 3 | 19 |

Interpretation: the candidate final whitelist queue now matches the source-count
range requested by RAG.md, but only with an 8-source buffer above the lower
bound. If human review rejects more than 8 queued rows, targeted replacement
source acquisition is needed before chunk extraction should be treated as
demo-scale. The next high-value work is human sign-off followed by chunk
extraction from accepted sources only.

## Phase 7J Human Sign-Off Workflow

Phase 7J creates the workflow boundary for real human labels. It writes the
108-row sign-off template and keeps the final whitelist empty until labels are
supplied.

Output evidence:

- `outputs/archive/provenance/source-workflow/human-signoff/human_signoff/human_signoff_template.jsonl`
- `outputs/archive/provenance/source-workflow/human-signoff/human_signoff/final_source_whitelist.jsonl`
- `outputs/archive/provenance/source-workflow/human-signoff/human_signoff/human_signoff_summary.json`
- `docs/verification/human-signoff-workflow.md`

Human sign-off status:

| metric | value |
| --- | ---: |
| candidate queue rows | 108 |
| human sign-off template rows | 108 |
| pending human review | 108 |
| accepted final sources | 0 |
| final whitelist claim | not_complete |

Interpretation: the automated source-side work has reached a clear boundary.
The next step requires human labels. Once labels exist, the same workflow can
produce `final_source_whitelist.jsonl`; chunk extraction should not treat the
current pending template as final accepted literature.

## Phase 7K Hashed Dense Formal Benchmark

Phase 7K adds a current-environment dense-vector retrieval benchmark without
mutating the fragile neural retrieval dependency stack. The implementation is
deterministic and non-neural.

Output evidence:

- `benchmark/domainrag/hashed_dense_benchmark.py`
- `outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/real_pilot_nickel_superalloy_medium_plus/fresh_hard_hashed_dense_results.jsonl`
- `outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/report_fresh_hard/summary.json`
- `docs/verification/hashed-dense-formal-benchmark.md`

Fresh-Hard result:

| method | questions | retrieval_hit | retrieval_recall | retrieval_mrr | api_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hashed_dense_oracle_reader` | 50 | 0.8800 | 0.7083 | 0.6240 | 0 |
| `hashed_dense_lexical_rerank_oracle_reader` | 50 | 0.9000 | 0.7183 | 0.6260 | 0 |

Interpretation: Phase 7K is a formal local dense-style benchmark on real data.
It gives the project another retrieval baseline beyond lexical and BM25, and
the rerank variant slightly improves retrieval hit and recall. It is not a
neural dense retriever or neural reranker result and should not be cited as
closing the FlashRAG dense/rerank target.

## Phase 7L Full-Text Chunk Extraction

Phase 7L adds the first full-text-to-chunk extraction workflow. It consumes:

```text
outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_combined115/full_text_access.jsonl
```

Output evidence:

- `benchmark/domainrag/full_text_chunk_extraction.py`
- `outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/full_text_chunks.jsonl`
- `outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_source_manifest.jsonl`
- `outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.json`
- `docs/verification/full-text-chunk-extraction.md`

Result:

| metric | value |
| --- | ---: |
| access rows | 115 |
| parseable access rows | 71 |
| sources attempted | 71 |
| sources chunked | 60 |
| chunk manifests | 2,196 |
| chunk tokens | 350 |
| overlap tokens | 50 |
| min chunk tokens | 80 |
| include text | false |

Chunk status counts:

| status | count |
| --- | ---: |
| chunked | 60 |
| skipped_not_parseable | 44 |
| too_short | 11 |

Interpretation: Phase 7L reaches the RAG.md 1,000-3,000 chunk-count target, but
only as machine-parseable chunk manifests. These chunks are not yet filtered to
human-final accepted sources, do not include raw text in committed outputs, and
do not yet have a generated 300-500 question benchmark.

## Phase 7M Provisional Demo-Question Generation

Phase 7M adds the first 300-question dataset over the validated medium-plus
corpus. It consumes:

```text
data/real_pilot_nickel_superalloy_medium_plus
```

Output evidence:

- `benchmark/domainrag/demo_question_generation.py`
- `data/real_pilot_nickel_superalloy_demo_questions/`
- `outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/demo_question_summary.json`
- `outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline/report_fresh_hard/summary.json`
- `outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense/report_fresh_hard/summary.json`
- `outputs/flashrag/real_pilot_nickel_superalloy_demo_questions/`
- `docs/verification/demo-question-generation.md`

Dataset shape:

| item | count |
| --- | ---: |
| corpus chunks | 100 |
| total questions | 300 |
| dev questions | 100 |
| test questions | 100 |
| fresh_hard questions | 100 |
| single_choice | 75 |
| multiple_choice | 75 |
| fill_blank | 75 |
| short_answer | 75 |

Fresh-Hard baseline:

| method | questions | retrieval_hit | retrieval_recall | retrieval_mrr | api_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `no_rag` | 100 | 0.0000 | 0.0000 | 0.0000 | 0 |
| `oracle_context` | 100 | 1.0000 | 1.0000 | 1.0000 | 0 |
| `lexical_rag` | 100 | 0.7200 | 0.7200 | 0.5550 | 0 |

Fresh-Hard local hashed dense diagnostics:

| method | questions | retrieval_hit | retrieval_recall | retrieval_mrr | api_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hashed_dense_oracle_reader` | 100 | 0.7000 | 0.7000 | 0.5445 | 0 |
| `hashed_dense_lexical_rerank_oracle_reader` | 100 | 0.7200 | 0.7200 | 0.5557 | 0 |

Interpretation: Phase 7M reaches the RAG.md 300-question lower bound
provisionally and verifies the generated data through the same DomainRAG,
FlashRAG bundle, baseline, and local hashed dense paths. It is still marked
`provisional_machine_generated_not_human_final`; it is not a human-final demo
benchmark and should not be used as evidence of final source sign-off.

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
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_fresh_hard_comparison/summary.json
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

- `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/human_labels.jsonl`
- `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/summary.json`
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
| Literature source policy | partial | Source manifests, a 108-row candidate final whitelist queue, and Phase 7J human sign-off template exist, but no final manually signed-off 100-180-paper top-venue whitelist is committed. |
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
| Demo scale | partial | Phase 7L adds 2,196 machine-parseable chunk manifests and Phase 7M adds 300 provisional questions, so the chunk and question counts are reached provisionally. The final human-accepted source filter and human-final demo benchmark remain open. |
| Dense/rerank methods | partial | Phase 7A adds isolated readiness outputs and gates for neural dense/rerank. Phase 7K adds a formal local hashed dense benchmark, but it is non-neural and does not close the neural dense/rerank target. |
| Status reporting | complete | This status report, `rag-md-implementation-audit.json`, and Phase 7G/7H/7I/7J/7K/7L/7M verification documentation. |

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
- 115 source rows with machine full-text access/processability evidence
- 2 verified source candidates and 106 rows ready for manual finalization after machine checks
- 108 source rows in the candidate final whitelist queue
- 108 source rows in the pending human sign-off template
- 2,196 machine-parseable full-text chunk manifests from 60 sources
- 300 provisional demo questions over the validated 100-chunk medium-plus corpus
- 100 provisional Fresh-Hard questions with local baseline and hashed dense diagnostics
- 0 final manually verified source inclusions

The implementation path is ready for more scale, but the dataset itself is
still missing the final human-source side. A true demo-scale benchmark should
not be claimed until the chunk manifests are filtered to human-final accepted
sources, 300-500 questions with qrels are regenerated or verified against those
accepted-source chunks, and the same validation, FlashRAG preparation, retrieval
comparison, live answer/Judge evaluation, calibration packet, and at least
sampled human audit are repeated on that final dataset. The Phase 7D candidate
pool, Phase 7E queue, Phase 7F provisional decisions, Phase 7J sign-off
template, Phase 7L chunk manifests, and Phase 7M provisional questions are the
handoff for that route, not the completed final demo benchmark.

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
- `outputs/archive/provenance/retrieval-diagnostics/dense-rerank-readiness/dense_rerank_readiness/readiness.json`
- `outputs/archive/provenance/retrieval-diagnostics/dense-rerank-readiness/dense_rerank_readiness/summary.md`
- `docs/verification/dense-rerank-isolated-readiness.md`

This is a partial implementation state. It defines the Python 3.10 isolated
environment, target methods, dependency list, and acceptance gates for
`flashrag_dense`, `flashrag_reranker`, and
`flashrag_bm25_plus_reranker`. It does not claim dense/rerank benchmark
results yet.

Phase 7K adds a separate current-environment benchmark:

- `benchmark/domainrag/hashed_dense_benchmark.py`
- `outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/real_pilot_nickel_superalloy_medium_plus/fresh_hard_hashed_dense_results.jsonl`
- `outputs/archive/provenance/retrieval-diagnostics/hashed-dense-benchmark/hashed_dense_benchmark/report_fresh_hard/summary.json`
- `docs/verification/hashed-dense-formal-benchmark.md`

This benchmark is formal and uses the real medium-plus Fresh-Hard split, but it
is explicitly non-neural. The correct status is: local hashed dense benchmark
complete, neural dense/rerank benchmark still open.

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
- A Phase 7G OpenAlex metadata refresh and 25-row full-text/processability checkpoint.
- A Phase 7H 115-row full-text/processability checkpoint and machine finalization queue.
- A Phase 7I 115-row human-review packet and 108-row candidate final whitelist queue.
- A Phase 7J 108-row pending human sign-off template.
- A Phase 7K non-neural local hashed dense benchmark on medium-plus Fresh-Hard.
- A Phase 7L full-text chunk extraction workflow with 2,196 chunk manifests.
- A Phase 7M provisional 300-question dataset with FlashRAG bundle, Fresh-Hard
  baseline, and local hashed dense diagnostics.
- Deterministic diagnostic baselines.
- Live DeepSeek answer generation and Judge evaluation.
- A five-method Fresh-Hard comparison.
- A human calibration audit.
- A structured `RAG.md` implementation audit.

The project is strong enough to support a report or demo focused on method
diagnostics, benchmark engineering, provisional question-scale rehearsal, and
source-screening readiness. It is not yet strong enough to claim final
human-verified `RAG.md` dataset scale.

## Next Phase Recommendation

Recommended next phase if work resumes: final-source labels or stop.

If this is a near-term deliverable, Phase 7M is a reasonable stop point because
it reaches the 300-question lower bound provisionally and keeps all final-source
claims honest. If strict `RAG.md` completion is still required, the high-value
path is:

1. Fill `human_signoff_template.jsonl` with real human labels.
2. Fill subtopic review gaps for coatings, life prediction, and
   microstructure characterization.
3. Promote human-accepted rows into a final 100-180 source whitelist, with
   targeted replacement acquisition if manual review removes more than 8 queue
   rows.
4. Filter Phase 7L chunk manifests to human-accepted sources and regenerate or
   verify 300-500 questions against accepted-source chunks.
5. Keep the same validation, FlashRAG bundle preparation, retrieval comparison,
   live answer/Judge, and sampled human calibration gates.
6. Run neural dense/rerank only in the isolated environment described by Phase
   7A, not by mutating the current AutoDL runtime. Phase 7K already covers the
   non-neural local hashed dense baseline.

If the goal is a defensible near-term project deliverable, finish with this
Phase 7M report and append a scale roadmap. If the goal is strict `RAG.md`
completion, the next work must be human source labels and human-final dataset
production, not another evaluator feature.

## Verification Commands

Run from repository root:

```bash
PYTHONPATH=benchmark pytest tests/test_phase6g_report.py
PYTHONPATH=benchmark pytest tests/test_phase7c_live_subset.py
PYTHONPATH=benchmark pytest tests/test_phase7d_outputs.py tests/test_source_acquisition.py tests/test_cli.py -k 'phase7d or source_acquisition or acquire_sources'
PYTHONPATH=benchmark pytest tests/test_phase7e_outputs.py tests/test_source_screening.py tests/test_cli.py -k 'phase7e or source_screening or screen_sources'
PYTHONPATH=benchmark pytest tests/test_phase7f_outputs.py tests/test_source_decisions.py tests/test_cli.py -k 'phase7f or source_decisions or decide_sources'
PYTHONPATH=benchmark pytest tests/test_phase7g_outputs.py tests/test_source_verification.py tests/test_source_metadata.py tests/test_full_text_intake.py tests/test_cli.py -k 'phase7g or source_verification or source_metadata or full_text_intake or verify_sources'
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
PYTHONPATH=benchmark pytest tests/test_real_pilot_medium_plus_assets.py tests/test_phase7b_outputs.py
PYTHONPATH=benchmark pytest tests/test_demo_question_generation.py tests/test_phase7m_outputs.py
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures pyproject.toml || true
git diff --check
```
