# Phase 7E Source Screening Queue

Recorded: 2026-06-28

This checkpoint converts the Phase 7D OpenAlex candidate pool into a
deterministic source-screening and full-text processing queue. It is not a
final source whitelist, and no candidate is treated as finally included in the
benchmark source set.

In operational terms, this is not a final source whitelist.

## Command

Run from repository root:

```bash
PYTHONPATH=benchmark python scripts/screen_phase7d_sources.py \
  --candidates outputs/phase7d/demo_scale_source_acquisition/candidates.jsonl \
  --output outputs/phase7e/source_screening_queue
```

Equivalent CLI entrypoint:

```bash
PYTHONPATH=benchmark python -m domainrag.cli screen-sources \
  --candidates outputs/phase7d/demo_scale_source_acquisition/candidates.jsonl \
  --output outputs/phase7e/source_screening_queue
```

## Output Files

- `outputs/phase7e/source_screening_queue/screening_queue.jsonl`
- `outputs/phase7e/source_screening_queue/screening_summary.json`
- `outputs/phase7e/source_screening_queue/summary.md`

## Queue Summary

| metric | value |
| --- | ---: |
| candidate papers queued | 124 |
| research article candidates | 113 |
| review candidates | 11 |
| high priority candidates | 3 |
| medium priority candidates | 79 |
| low priority candidates | 42 |
| open-access/full-text ready candidates | 115 |
| access-check-needed candidates | 9 |
| final included sources | 0 |

Every row is marked with:

- `verification_status`: `machine_prescreen_only`
- `screening_status`: `needs_manual_verification`
- `final_inclusion_status`: `not_finalized`

## Review Gaps

These subtopics still have zero review-paper candidates and need targeted
search before a final source whitelist can satisfy the RAG.md review coverage
intent:

- `coatings`
- `life_prediction`
- `microstructure_characterization`

## Subtopic Queue

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

## Manual Verification Tasks

Each queue row carries the same manual verification checklist:

- verify venue metric or flagship status
- verify full-text processability
- verify article type
- verify retraction status
- verify domain relevance

## Verification Limits

This queue is a machine pre-screen only:

- Venue metrics are not manually verified here.
- Full-text URLs are not downloaded or parsed here.
- Retraction status is not checked here.
- Article type still needs publisher/database confirmation.
- Domain relevance still needs manual title, abstract, and full-text screening.
- The queue does not create benchmark chunks or questions.

The source-policy and demo-scale requirements therefore remain partial in
`docs/reports/rag-md-implementation-audit.json`.

## Next Gate

Phase 7F should run manual screening over this queue, reject weak/off-topic
rows, add targeted review-paper candidates for the three review-gap subtopics,
and then produce a final 100-180 source whitelist before chunk extraction.
