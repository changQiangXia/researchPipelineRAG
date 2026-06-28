# Phase 7F Source Decisions And Stop Point

Recorded: 2026-06-28

This checkpoint converts the Phase 7E screening queue into a provisional source
decision package. It is not final manual verification, and it does not claim
that the full RAG.md demo-scale dataset has been produced.

Operational recommendation: `pause_after_phase7f`.

## Command

Run from repository root:

```bash
PYTHONPATH=benchmark python scripts/build_phase7f_source_decisions.py \
  --screening-queue outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl \
  --output outputs/archive/provenance/source-workflow/source-decisions/source_decisions
```

Equivalent CLI entrypoint:

```bash
PYTHONPATH=benchmark python -m domainrag.cli decide-sources \
  --screening-queue outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl \
  --output outputs/archive/provenance/source-workflow/source-decisions/source_decisions
```

## Output Files

- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/source_decisions.jsonl`
- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/provisional_source_whitelist.jsonl`
- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/decision_summary.json`
- `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/summary.md`

## Decision Summary

| metric | value |
| --- | ---: |
| candidate decisions | 124 |
| accepted provisional | 82 |
| pending manual review | 33 |
| rejected prescreen | 9 |
| provisional source whitelist | 115 |

Every row is marked with:

- `decision_status`: `provisional_not_final`
- `manual_verification_status`: all checks remain `pending`

The provisional whitelist count is inside the RAG.md 100-180 source-paper range,
but it is not a final whitelist because venue metrics, DOI/title/year, article
type, retraction status, full-text parsing, and domain relevance have not been
manually finalized.

## Subtopic Decisions

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

## Remaining Review Gaps

The following subtopics still have zero review-paper candidates and remain the
first source-side gap to close if work resumes:

- `coatings`
- `life_prediction`
- `microstructure_characterization`

## Why This Is A Reasonable Stop Point

Phase 7F is a coherent stopping point because the project now has:

- a validated medium-plus dataset and benchmark/evaluation path;
- live DeepSeek answer and Judge evidence;
- human calibration evidence;
- a 124-paper OpenAlex source candidate pool;
- a 124-row source screening queue;
- a 124-row provisional decision table;
- a 115-row provisional source whitelist inside the RAG.md 100-180 source-paper
  range.

The remaining work is mostly scale production and manual source verification,
not core benchmark engineering.

## Must Not Claim Yet

- final manually verified 100-180 source whitelist;
- completed venue/JCR/CiteScore verification;
- completed full-text parsing;
- completed 1,000-3,000 chunk demo dataset;
- completed 300-500 question demo benchmark;
- completed dense/rerank benchmark results.
