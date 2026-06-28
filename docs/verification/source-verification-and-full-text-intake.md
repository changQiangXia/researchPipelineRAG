# Phase 7G Source Verification And Full-Text Intake

Recorded: 2026-06-28

This checkpoint starts the post-7F path toward a final source whitelist and
demo-scale corpus expansion. It is not final manual verification. It adds
machine-assisted evidence for metadata consistency, retraction status,
article type, and first 25-row full-text processability.

## Scope

Phase 7G currently covers:

- OpenAlex metadata refresh for all 115 Phase 7F provisional whitelist rows.
- Full-text access and parse probing for the first 25 rows, in 5-row batches.
- A source verification matrix that combines provisional source decisions,
  OpenAlex metadata evidence, and available full-text access evidence.

It does not claim:

- final manually verified 100-180 source whitelist;
- completed JCR/CiteScore or flagship venue manual verification;
- completed full-text parsing for all 115 rows;
- completed 1,000-3,000 chunk demo dataset;
- completed 300-500 question demo benchmark.

## Commands

OpenAlex metadata was collected with:

```bash
PYTHONPATH=benchmark python - <<'PY'
from pathlib import Path
from domainrag.source_metadata import build_openalex_metadata_outputs, fetch_openalex_work_by_doi

def fetcher(doi: str):
    return fetch_openalex_work_by_doi(doi, timeout_seconds=30, mailto='2454212515@qq.com')

build_openalex_metadata_outputs(
    Path('outputs/phase7f/source_decisions/provisional_source_whitelist.jsonl'),
    output_dir=Path('outputs/phase7g/source_metadata'),
    fetcher=fetcher,
)
PY
```

The first full-text batch was probed with:

```bash
PYTHONPATH=benchmark python - <<'PY'
from pathlib import Path
from domainrag.full_text_intake import build_full_text_access_outputs, fetch_full_text

def fetcher(url: str):
    return fetch_full_text(url, timeout_seconds=10, max_bytes=8_000_000)

build_full_text_access_outputs(
    Path('outputs/phase7f/source_decisions/provisional_source_whitelist.jsonl'),
    output_dir=Path('outputs/phase7g/full_text_access_batch5'),
    fetcher=fetcher,
    limit=5,
)
PY
```

Additional 5-row batches were probed with the same command using `offset=5`,
`offset=10`, `offset=15`, and `offset=20`, each with `limit=5`. The batches
were combined with:

```bash
PYTHONPATH=benchmark python - <<'PY'
from pathlib import Path
from domainrag.full_text_intake import combine_full_text_access_outputs

combine_full_text_access_outputs(
    [
        Path('outputs/phase7g/full_text_access_batch5/full_text_access.jsonl'),
        Path('outputs/phase7g/full_text_access_offset5_limit5/full_text_access.jsonl'),
        Path('outputs/phase7g/full_text_access_offset10_limit5/full_text_access.jsonl'),
        Path('outputs/phase7g/full_text_access_offset15_limit5/full_text_access.jsonl'),
        Path('outputs/phase7g/full_text_access_offset20_limit5/full_text_access.jsonl'),
    ],
    output_dir=Path('outputs/phase7g/full_text_access_combined25'),
)
PY
```

The combined verification matrix was built with:

```bash
PYTHONPATH=benchmark python scripts/build_phase7g_source_verification.py \
  --whitelist outputs/phase7f/source_decisions/provisional_source_whitelist.jsonl \
  --metadata outputs/phase7g/source_metadata/openalex_metadata.jsonl \
  --access outputs/phase7g/full_text_access_combined25/full_text_access.jsonl \
  --output outputs/phase7g/source_verification_combined25
```

## Output Files

- `outputs/phase7g/source_metadata/openalex_metadata.jsonl`
- `outputs/phase7g/source_metadata/openalex_metadata_summary.json`
- `outputs/phase7g/source_metadata/openalex_metadata_summary.md`
- `outputs/phase7g/full_text_access_batch5/full_text_access.jsonl`
- `outputs/phase7g/full_text_access_batch5/full_text_access_summary.json`
- `outputs/phase7g/full_text_access_batch5/full_text_access_summary.md`
- `outputs/phase7g/full_text_access_offset5_limit5/full_text_access.jsonl`
- `outputs/phase7g/full_text_access_offset10_limit5/full_text_access.jsonl`
- `outputs/phase7g/full_text_access_offset15_limit5/full_text_access.jsonl`
- `outputs/phase7g/full_text_access_offset20_limit5/full_text_access.jsonl`
- `outputs/phase7g/full_text_access_combined25/full_text_access.jsonl`
- `outputs/phase7g/full_text_access_combined25/full_text_access_summary.json`
- `outputs/phase7g/full_text_access_combined25/full_text_access_summary.md`
- `outputs/phase7g/source_verification_combined25/source_verification_matrix.jsonl`
- `outputs/phase7g/source_verification_combined25/final_verification_queue.jsonl`
- `outputs/phase7g/source_verification_combined25/verification_summary.json`
- `outputs/phase7g/source_verification_combined25/summary.md`

## Results

OpenAlex metadata:

| metric | value |
| --- | ---: |
| source rows checked | 115 |
| metadata found | 115 |
| retracted rows | 0 |
| article type rows | 103 |
| preprint rows | 6 |
| dissertation rows | 2 |
| report rows | 2 |
| review rows | 1 |
| other rows | 1 |

Full-text combined 25-row batch:

| metric | value |
| --- | ---: |
| source rows checked | 25 |
| downloaded | 17 |
| not accessible | 6 |
| download failed | 2 |
| parseable | 17 |
| not attempted | 8 |
| total extracted characters | 1120613 |

The full-text manifest records access and parse status only. It does not store
paper text samples or extracted full text.

Verification matrix:

| metric | value |
| --- | ---: |
| source rows in matrix | 115 |
| accepted final verification | 0 |
| verified source candidate | 1 |
| ready for manual finalization | 23 |
| rejected after verification | 7 |
| needs evidence | 84 |
| final whitelist claim | not_complete |

## Interpretation

This checkpoint makes the next work more concrete:

- Metadata verification is no longer the main blocker for the 115 provisional
  rows: all 115 were found in OpenAlex and none are marked retracted there.
- Some Phase 7F provisional whitelist rows are not normal research/review
  article candidates by OpenAlex type and should be rejected or manually
  reviewed before any final whitelist claim.
- Full-text processing is real but still incomplete: 17 of the first 25 rows are
  parseable, while 403 rows and timeout rows need alternate access or manual
  handling rather than automatic source rejection.
- One row has all machine checks verified, but it is still only a verified
  source candidate until human final sign-off.
- Rows with `ready_for_manual_finalization` still need human venue/JCR/CiteScore
  or flagship-source confirmation before they can become final accepted sources.

The next efficient step is to run the full-text probe in additional batches and
add a parser fallback for the failing PDFs only if failures remain common.
