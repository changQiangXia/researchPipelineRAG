# Phase 7L: Full-Text Chunk Extraction

Recorded: 2026-06-28

## Purpose

Phase 7L turns the Phase 7H full-text access probe into an actual chunk
extraction workflow. It uses the 115-row full-text access table, re-fetches the
71 machine-parseable rows, parses the full text again, and emits chunk-level
manifests.

This is a machine full-text parsing and chunking checkpoint. It is not a final
demo dataset because the source rows still do not have human final sign-off,
and no 300-500 question set has been generated from these chunks.

## Command

```bash
PYTHONPATH=benchmark python -m domainrag.cli extract-fulltext-chunks \
  --access outputs/archive/provenance/source-workflow/source-verification-combined/full_text_access_combined115/full_text_access.jsonl \
  --output outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction \
  --chunk-tokens 350 \
  --overlap-tokens 50 \
  --min-chunk-tokens 80
```

## Outputs

```text
outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/full_text_chunks.jsonl
outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_source_manifest.jsonl
outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.json
outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.md
```

Default output policy:

```text
chunk text omitted; text_sha256 retained
```

The committed `full_text_chunks.jsonl` is a chunk manifest, not a raw text
corpus dump. It stores chunk ids, source ids, token boundaries, token counts,
character counts, content type, provenance status, and SHA-256 hashes of each
chunk. It intentionally does not store `text` or `text_sample` fields.

The extraction module supports explicit text inclusion for private local runs,
but Phase 7L committed outputs keep `include_text = false`.

## Result

Summary:

| metric | value |
| --- | ---: |
| access rows | 115 |
| parseable access rows | 71 |
| sources attempted | 71 |
| sources chunked | 60 |
| chunk count | 2,196 |
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

The 2,196 chunk manifests fall inside the RAG.md demo chunk-count target of
1,000-3,000 chunks.

## Interpretation

Phase 7L materially advances the full-text parsing pipeline:

- it moves beyond access probing into re-fetching, parsing, token-window
  chunking, source-level manifests, and chunk-level manifests;
- it reaches the demo-scale chunk-count range with real parseable full-text
  sources;
- it preserves the source-signoff boundary by labeling chunks as
  `machine_parseable_not_human_final`;
- it avoids committing raw full-text chunks by default.

The current status is therefore:

```text
full_text_chunk_manifest_target_met
final_demo_dataset_claim_not_complete
```

Remaining gaps:

- no final manually signed-off 100-180 source whitelist;
- chunk manifests are not yet filtered to human-accepted sources;
- no 300-500 question set has been generated from these chunks;
- no DeepSeek answer/Judge or human calibration has been run on a 300-500
  question demo benchmark.

## Verification

Focused verification:

```bash
PYTHONPATH=benchmark pytest tests/test_full_text_chunk_extraction.py tests/test_cli.py::test_extract_fulltext_chunks_command_writes_empty_outputs
PYTHONPATH=benchmark pytest tests/test_phase7l_outputs.py
```

Full verification before commit:

```bash
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
python -m json.tool docs/reports/rag-md-implementation-audit.json >/tmp/phase7l-audit.json
python -m json.tool outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/chunk_extraction_summary.json >/tmp/phase7l-summary.json
git diff --check
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs/archive/provenance/source-workflow outputs/archive/provenance/retrieval-diagnostics benchmark scripts tests docs pyproject.toml README.md || true
```
