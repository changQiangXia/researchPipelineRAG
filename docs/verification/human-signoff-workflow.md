# Phase 7J Human Sign-Off Workflow

Recorded: 2026-06-28

This checkpoint creates the workflow needed to turn the Phase 7I candidate final
whitelist queue into a real final source whitelist after human labels are
supplied. It is not final manual verification.

## Scope

Phase 7J covers:

- a 108-row `human_signoff_template.jsonl`;
- an empty `final_source_whitelist.jsonl` until real human labels are supplied;
- a CLI/script path that can promote only rows labeled `accepted_final` into the
  final whitelist;
- explicit preservation of `pending_human_review` for all unlabeled rows.

It does not claim:

- final manually verified 100-180 source whitelist;
- completed JCR/CiteScore or flagship venue manual verification;
- completed 1,000-3,000 chunk demo dataset;
- completed 300-500 question demo benchmark.

## Commands

Generate the pending template:

```bash
PYTHONPATH=benchmark python scripts/build_phase7j_human_signoff.py \
  --candidate-queue outputs/phase7i/manual_finalization_packet/candidate_final_whitelist_queue.jsonl \
  --output outputs/phase7j/human_signoff
```

After human labels exist, rebuild with:

```bash
PYTHONPATH=benchmark python scripts/build_phase7j_human_signoff.py \
  --candidate-queue outputs/phase7i/manual_finalization_packet/candidate_final_whitelist_queue.jsonl \
  --labels <human_signoff_labels.jsonl> \
  --output outputs/phase7j/human_signoff
```

Expected label shape:

```json
{
  "source_id": "openalex_W...",
  "human_signoff_decision": "accepted_final",
  "human_reviewer": "reviewer_id",
  "human_review_date": "2026-06-28",
  "human_review_notes": "checked source evidence"
}
```

Allowed decisions are `accepted_final`, `rejected_final`, and
`pending_human_review`.

## Output Files

- `outputs/phase7j/human_signoff/human_signoff_template.jsonl`
- `outputs/phase7j/human_signoff/final_source_whitelist.jsonl`
- `outputs/phase7j/human_signoff/human_signoff_summary.json`
- `outputs/phase7j/human_signoff/summary.md`

## Results

| metric | value |
| --- | ---: |
| candidate queue rows | 108 |
| human sign-off template rows | 108 |
| pending human review | 108 |
| accepted final sources | 0 |
| final whitelist claim | not_complete |

## Interpretation

The source-side pipeline is now waiting on real human labels. This is the point
where automated work should stop short of claiming final verification. Once
labels are supplied, the same workflow can produce a real
`final_source_whitelist.jsonl`, and chunk extraction should use only rows with
`accepted_final_verification`.
