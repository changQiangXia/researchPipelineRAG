# Phase 7H Full-Text Intake Combined115

Recorded: 2026-06-28

This checkpoint extends Phase 7G from a 25-row full-text probe to all 115 rows
in the Phase 7F provisional source whitelist. It is not final manual
verification; in status terms, this checkpoint is not final manual verification.
It records machine access, parseability, and combined source
verification evidence so the next step can focus on human finalization and
chunk extraction.

## Scope

Phase 7H covers:

- full-text access and parse probing for all 115 provisional whitelist rows;
- a combined 115-row full-text access manifest;
- a combined 115-row source verification matrix using Phase 7G OpenAlex
  metadata and Phase 7H full-text access evidence;
- a corrected source-verification policy where 403, timeout, and truncated
  downloads remain `pending_manual` rather than hard source rejections.

It does not claim:

- final manually verified 100-180 source whitelist;
- completed JCR/CiteScore or flagship venue manual verification;
- completed 1,000-3,000 chunk demo dataset;
- completed 300-500 question demo benchmark.

## Commands

The remaining full-text batches were probed with the same function used in
Phase 7G, using 5-row batches from offset 25 through offset 110:

```bash
PYTHONPATH=benchmark python - <<'PY'
from pathlib import Path
from domainrag.full_text_intake import build_full_text_access_outputs, fetch_full_text

def fetcher(url: str):
    return fetch_full_text(url, timeout_seconds=10, max_bytes=8_000_000)

for offset in range(25, 115, 5):
    build_full_text_access_outputs(
        Path('outputs/archive/provenance/source-workflow/source-decisions/source_decisions/provisional_source_whitelist.jsonl'),
        output_dir=Path(f'outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_offset{offset}_limit5'),
        fetcher=fetcher,
        offset=offset,
        limit=5,
    )
PY
```

The full 115-row access manifest was combined with:

```bash
PYTHONPATH=benchmark python - <<'PY'
from pathlib import Path
from domainrag.full_text_intake import combine_full_text_access_outputs

access_paths = [Path('outputs/archive/provenance/source-workflow/source-verification-first-batches/full_text_access_combined25/full_text_access.jsonl')]
for offset in range(25, 115, 5):
    access_paths.append(Path(f'outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_offset{offset}_limit5/full_text_access.jsonl'))

combine_full_text_access_outputs(
    access_paths,
    output_dir=Path('outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_combined115'),
)
PY
```

The combined verification matrix was built with:

```bash
PYTHONPATH=benchmark python scripts/build_phase7g_source_verification.py \
  --whitelist outputs/archive/provenance/source-workflow/source-decisions/source_decisions/provisional_source_whitelist.jsonl \
  --metadata outputs/archive/provenance/source-workflow/source-verification-first-batches/source_metadata/openalex_metadata.jsonl \
  --access outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_combined115/full_text_access.jsonl \
  --output outputs/archive/provenance/source-workflow/source-verification-combined/source_verification_combined115
```

## Results

Full-text access:

| metric | value |
| --- | ---: |
| source rows checked | 115 |
| downloaded | 71 |
| not accessible | 37 |
| download failed | 6 |
| download truncated | 1 |
| parseable | 71 |
| not attempted | 44 |
| total extracted characters | 4366176 |

The access manifest records access and parse status only. It does not store
paper text samples or extracted full text.

Source verification:

| metric | value |
| --- | ---: |
| source rows in matrix | 115 |
| accepted final verification | 0 |
| verified source candidate | 2 |
| ready for manual finalization | 106 |
| rejected after verification | 7 |
| final whitelist claim | not_complete |

## Interpretation

The 115-row source-side queue is now much more concrete:

- 71 provisional sources have parseable machine-extracted text evidence.
- 44 rows need alternate access, manual handling, or a larger/full download
  path before chunk extraction.
- 108 rows are now machine-ready for human finalization: 2 have all machine
  checks verified, and 106 need manual venue/source-quality or access review.
- 7 rows are rejected by machine verification due metadata, type, or other hard
  evidence failures; these should still be manually spot-checked before final
  removal.
- Final accepted source count remains 0 because human sign-off is intentionally
  not simulated.

The next efficient step is to manually finalize the 2 verified source
candidates and the 106 ready rows, then extract chunks only from the human
accepted subset. If the accepted subset falls below 100 sources after manual
review, targeted replacement source acquisition is needed before demo-scale
chunk/question generation.
