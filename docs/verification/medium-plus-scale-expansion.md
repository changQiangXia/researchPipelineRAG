# Medium-Plus Scale Expansion

Recorded: 2026-06-28

Phase: Phase 7B

Blueprint: `/root/autodl-tmp/RAG/RAG.md`

## Scope

Phase 7B expands the validated nickel-superalloy high-temperature-failure pilot
from 40 chunks / 60 questions to 100 chunks / 150 questions.

This is still below the `RAG.md` demo target of 1,000-3,000 chunks and 300-500
questions. It is a medium-plus scale checkpoint designed to verify that the
data contract, Easy Dataset-style export, FlashRAG bundle preparation,
deterministic baselines, and real retrieval scoring continue to work at a
larger scale.

## Generation Route

Command:

```bash
PYTHONPATH=benchmark python scripts/build_real_pilot_medium_plus.py
```

The builder reads the validated medium Easy Dataset fixture and source manifest:

- `fixtures/easy_dataset/real_pilot_nickel_superalloy_medium/`
- `data/real_pilot_sources/nickel_superalloy_high_temp_failure_medium/sources.jsonl`

It writes:

- `fixtures/easy_dataset/real_pilot_nickel_superalloy_medium_plus/`
- `data/real_pilot_sources/nickel_superalloy_high_temp_failure_medium_plus/sources.jsonl`
- `data/real_pilot_nickel_superalloy_medium_plus/`

The extra chunks are deterministic distilled source-backed evidence chunks
derived from the validated medium questions and their original source chunks.
The extra questions are deterministic medium-plus variants and paired synthesis
questions over those distilled chunks. This is not a substitute for the final
100-180 paper top-venue literature matrix; it is a pipeline scale checkpoint.

## Dataset Shape

Current output:

```text
100 chunks / 150 questions
```

Split shape:

| split | questions |
| --- | ---: |
| dev | 50 |
| test | 50 |
| fresh_hard | 50 |

Question type shape:

| question type | count |
| --- | ---: |
| single_choice | 38 |
| multiple_choice | 38 |
| fill_blank | 37 |
| short_answer | 37 |

Additional scale signal:

- Source records: 32
- Multi-source questions: 86
- Fresh-Hard multi-source questions: 43
- Distilled source-backed chunks: 60

## Verification Commands

Dataset validation:

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_medium_plus
```

FlashRAG bundle preparation:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_medium_plus
```

Fresh-Hard deterministic baseline:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output outputs/archive/provenance/expanded-pilots/medium-plus-baseline-and-bm25/medium_plus_baseline \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard
```

Current-environment BM25s retrieval:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-bm25s \
  --dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output outputs/archive/provenance/expanded-pilots/medium-plus-baseline-and-bm25/medium_plus_bm25s \
  --split fresh_hard \
  --top-k 5
```

The FlashRAG bundle is generated for the medium-plus dataset. The FlashRAG
retriever import path is not used for Phase 7B retrieval because the current
AutoDL environment now kills the process while importing FlashRAG retriever
modules after the PyTorch/transformers mismatch noted in Phase 7A. Phase 7B
therefore records direct `bm25s` retrieval as a current-environment fallback,
not as a completed FlashRAG BM25 run.

## Fresh-Hard Retrieval Results

Fresh-Hard questions: 50

| method | retrieval hit | retrieval recall | retrieval MRR |
| --- | ---: | ---: | ---: |
| oracle_context | 1.0000 | 1.0000 | 1.0000 |
| lexical_rag | 0.8800 | 0.7033 | 0.6047 |
| bm25s_oracle_reader | 0.8600 | 0.7117 | 0.6073 |
| no_rag | 0.0000 | 0.0000 | 0.0000 |

The medium-plus split makes retrieval harder than the 40/60 medium pilot:
multi-source Fresh-Hard questions now dominate the split, and both lexical and
BM25s have partial-recall rows. This is useful because it prevents the
retrieval layer from saturating before live answer/Judge evaluation.

## Current Status

Phase 7B improves the scale evidence but does not close the scale gap.

- Current best: 100 chunks and 150 questions.
- RAG.md demo target: 1,000-3,000 chunks and 300-500 questions.
- Remaining scale factor: at least 10x more chunks and 2x more questions.
