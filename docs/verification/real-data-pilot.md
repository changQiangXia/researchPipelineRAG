# Real Data Pilot Verification

Phase: 3A - small real-paper data pilot
Recorded: 2026-06-27T19:10:00Z

## Scope

This phase starts the transition from synthetic fixtures to actual literature-derived data. It creates a small nickel-based superalloy high-temperature failure pilot from recent open-access article pages, records source traceability in an internal manifest, converts the pilot through the Easy Dataset-style export contract, and validates the resulting public DomainRAG dataset.

It does not call DeepSeek or any other live model provider. The pilot questions and chunks are manually curated and paraphrased from real source pages. This is not yet a final gold benchmark; it is the first real-data pipeline check.

## Source Traceability

Internal traceability file:

```text
data/real_pilot_sources/nickel_superalloy_high_temp_failure/sources.jsonl
```

Source coverage:

- Grain-boundary-sensitive initial oxidation behavior in Inconel 718
- Cerium coating mitigation of intergranular oxidation in additively manufactured IN625
- LPBF GH3536 oxidation behavior at 950 C
- Directionally solidified nickel-based superalloy creep at 850 C
- Additively manufactured ABD-900AM creep deformation and damage
- Rejuvenation heat treatment for directionally solidified nickel-based superalloy creep recovery
- Phase-field-informed machine learning descriptors for creep strain prediction

The source manifest includes article titles and URLs for auditability. It is separate from the public DomainRAG dataset.

## Public Data Boundary

The public dataset is:

```text
data/real_pilot_nickel_superalloy/
```

The public artifacts contain only DomainRAG contract fields:

```text
corpus.jsonl
canonical_dataset.jsonl
dev.jsonl
test.jsonl
fresh_hard_test.jsonl
qrels/dev.tsv
qrels/test.tsv
qrels/fresh_hard.tsv
dataset_card.md
statistics.json
```

The public artifacts do not include source article titles, URLs, DOI fields, author fields, venue fields, page fields, or original PDF paths.

## Easy Dataset-Style Input

The curated real pilot starts as:

```text
fixtures/easy_dataset/real_pilot_nickel_superalloy/chunks.jsonl
fixtures/easy_dataset/real_pilot_nickel_superalloy/items.jsonl
```

Current size:

- 9 real-source-derived chunks
- 12 questions
- 4 `dev` questions
- 4 `test` questions
- 4 `fresh_hard` questions
- 3 `single_choice`
- 3 `multiple_choice`
- 3 `fill_blank`
- 3 `short_answer`

## Conversion

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input fixtures/easy_dataset/real_pilot_nickel_superalloy \
  --output data \
  --dataset-name real_pilot_nickel_superalloy
```

Result:

```text
DomainRAG dataset written to data/real_pilot_nickel_superalloy
```

Generated statistics:

```json
{
  "corpus_count": 9,
  "dataset_name": "real_pilot_nickel_superalloy",
  "difficulty_counts": {
    "easy": 1,
    "hard": 6,
    "medium": 5
  },
  "question_count": 12,
  "question_type_counts": {
    "fill_blank": 3,
    "multiple_choice": 3,
    "short_answer": 3,
    "single_choice": 3
  },
  "split_counts": {
    "dev": 4,
    "fresh_hard": 4,
    "test": 4
  }
}
```

## Verification Commands

Focused real-pilot tests:

```bash
PYTHONPATH=benchmark pytest tests/test_real_data_pilot.py -q
```

Dataset validation:

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy
```

FlashRAG bundle preparation:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy
```

Minimal baseline:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs \
  --methods no_rag \
  --split dev
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/real_pilot_nickel_superalloy/dev_results.jsonl \
  --output reports/real_pilot_nickel_superalloy
```

The minimal baseline intentionally uses only `no_rag` in this phase. It checks that the real pilot can enter the benchmark runner without treating mock retrieval as the main evidence.

## Limitations

- The pilot is small by design: 9 chunks and 12 questions.
- The chunks are manually curated paraphrases, not full PDF extraction output.
- The questions are not yet DeepSeek-generated or DeepSeek-reviewed.
- The `fresh_hard` split is structurally present, but it has not yet passed the full RAG.md Fresh-Hard filter of No-RAG low score plus Oracle-Context high score.
- The source manifest records source article identity for auditability; the public DomainRAG dataset intentionally strips that identity.

## Next Step

Phase 3B should replace manual question creation with a controlled DeepSeek generation and independent-review loop for this same small pilot before scaling to dozens of papers.
