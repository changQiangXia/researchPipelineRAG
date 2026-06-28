# Phase 7D Demo-Scale Source Acquisition

Recorded: 2026-06-28

This checkpoint creates a reproducible OpenAlex-backed candidate pool for the
larger RAG.md demo-scale build. It is not a final inclusion list, and no paper
from this output is treated as finally accepted for benchmark expansion yet.

## Command

Run from repository root:

```bash
PYTHONPATH=benchmark python scripts/acquire_demo_scale_sources.py \
  --output outputs/phase7d/demo_scale_source_acquisition \
  --per-query 25 \
  --timeout-seconds 60
```

Equivalent CLI entrypoint:

```bash
PYTHONPATH=benchmark python -m domainrag.cli acquire-sources \
  --output outputs/phase7d/demo_scale_source_acquisition \
  --per-query 25 \
  --timeout-seconds 60
```

Dry-run query-plan check:

```bash
PYTHONPATH=benchmark python scripts/acquire_demo_scale_sources.py --dry-run --per-query 25
```

## Output Files

- `outputs/phase7d/demo_scale_source_acquisition/candidates.jsonl`
- `outputs/phase7d/demo_scale_source_acquisition/coverage.json`
- `outputs/phase7d/demo_scale_source_acquisition/summary.md`

## Coverage

| metric | value |
| --- | ---: |
| candidate papers | 124 |
| research article candidates | 113 |
| review candidates | 11 |
| open-access candidates | 115 |
| subtopics covered | 8 |
| final included sources | 0 |

Every row is marked with:

- `verification_status`: `candidate_openalex_verified`
- `inclusion_status`: `candidate_for_manual_verification`

The OpenAlex metadata gives a useful acquisition checkpoint, but it does not
replace manual inclusion checks.

## Subtopic Coverage

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

## Verification Limits

The output is intentionally conservative:

- OpenAlex confirms DOI-linked bibliographic metadata candidates.
- Venue metrics and top-venue status are not manually verified here.
- Full text availability and processability are not verified here.
- Retraction status is not checked here.
- Article-type labels still need publisher/database confirmation.
- Domain relevance still needs manual screening against title, abstract, and
  full text.
- Review coverage is uneven: `coatings`, `life_prediction`, and
  `microstructure_characterization` still need targeted review-paper search.

Because of these limits, this checkpoint advances the source-acquisition gap
but leaves `literature_source_policy` and `demo_scale` partial in
`docs/reports/rag-md-implementation-audit.json`.

## Next Gate

Phase 7E should convert this candidate pool into a manually verified source
whitelist before any demo-scale dataset expansion:

1. Verify venue quality through publisher pages, journal databases, JCR,
   CiteScore, or an agreed domain-flagship list.
2. Verify DOI, title, year, article type, and retraction status.
3. Confirm full text can be legally and technically processed.
4. Remove off-topic and duplicate candidates after manual screening.
5. Build a final 100-180 source whitelist and only then extract chunks toward
   the 1,000-3,000 chunk / 300-500 question demo target.
