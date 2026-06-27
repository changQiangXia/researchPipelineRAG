# DeepSeek Full Candidate Audit Verification

Phase: 3C - full real-pilot DeepSeek candidate generation and audit
Recorded: 2026-06-27T19:50:00Z

## Scope

This phase expands the controlled DeepSeek generation/review loop from the Phase 3B three-item sample to every real chunk in the Phase 3A nickel-based superalloy pilot. It also adds a candidate audit table so generated items are explicitly classified as `accepted`, `rejected`, or `needs_human_review`.

The output is still treated as a candidate dataset, not a final gold benchmark. It is suitable for inspection, comparison, and downstream pipeline validation.

## Implementation Changes

Runner:

```text
scripts/run_deepseek_real_pilot.py
```

New behavior:

- `--plan default`: existing curated 3-item pilot plan.
- `--plan all-chunks`: one generated item for every chunk in the input `chunks.jsonl`.
- `candidate_audit.jsonl`: per-candidate audit rows with decision, review score, review status, problems, and human-review reason.
- `accepted_items.jsonl`: only candidates accepted by review and meeting the automatic acceptance threshold.

Automatic acceptance threshold:

```text
review accepted == true
review quality_score >= 0.90
```

## Real API Run

Command:

```bash
DEEPSEEK_API_KEY=<env only> PYTHONPATH=benchmark python scripts/run_deepseek_real_pilot.py \
  --chunks fixtures/easy_dataset/real_pilot_nickel_superalloy/chunks.jsonl \
  --output outputs/deepseek/real_pilot_nickel_superalloy_full \
  --generation-model deepseek-v4-pro \
  --review-model deepseek-v4-pro \
  --plan all-chunks \
  --max-retries 2
```

Output:

```text
generated items written to outputs/deepseek/real_pilot_nickel_superalloy_full/generated_items.jsonl
review results written to outputs/deepseek/real_pilot_nickel_superalloy_full/review_results.jsonl
candidate audit written to outputs/deepseek/real_pilot_nickel_superalloy_full/candidate_audit.jsonl
accepted items written to outputs/deepseek/real_pilot_nickel_superalloy_full/accepted_items.jsonl
```

Run manifest:

```json
{
  "dry_run": false,
  "generation_model": "deepseek-v4-pro",
  "plan": "all-chunks",
  "planned_items": 9,
  "review_model": "deepseek-v4-pro"
}
```

Candidate counts:

```text
9 generated_items.jsonl
9 review_results.jsonl
9 candidate_audit.jsonl
9 accepted_items.jsonl
18 raw_responses.jsonl
```

Audit summary:

```json
{
  "decision_counts": {
    "accepted": 9
  },
  "question_type_counts": {
    "fill_blank": 2,
    "multiple_choice": 2,
    "short_answer": 2,
    "single_choice": 3
  },
  "split_counts": {
    "dev": 3,
    "fresh_hard": 3,
    "test": 3
  }
}
```

Token usage:

```json
{
  "generation_completion": 13404,
  "generation_prompt": 5359,
  "review_completion": 8493,
  "review_prompt": 4251
}
```

## Candidate Dataset

The accepted candidates were converted into a DomainRAG candidate dataset:

```text
outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates/
```

Conversion and validation:

```bash
mkdir -p /tmp/domainrag-deepseek-full-candidate-source
cp fixtures/easy_dataset/real_pilot_nickel_superalloy/chunks.jsonl \
  /tmp/domainrag-deepseek-full-candidate-source/chunks.jsonl
cp outputs/deepseek/real_pilot_nickel_superalloy_full/accepted_items.jsonl \
  /tmp/domainrag-deepseek-full-candidate-source/items.jsonl
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input /tmp/domainrag-deepseek-full-candidate-source \
  --output outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate \
  --dataset-name deepseek_real_pilot_full_candidates
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates
```

Result:

```text
DomainRAG dataset written to outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates
outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates is valid
```

Candidate dataset statistics:

```json
{
  "corpus_count": 9,
  "dataset_name": "deepseek_real_pilot_full_candidates",
  "difficulty_counts": {
    "easy": 7,
    "medium": 2
  },
  "question_count": 9,
  "question_type_counts": {
    "fill_blank": 2,
    "multiple_choice": 2,
    "short_answer": 2,
    "single_choice": 3
  },
  "split_counts": {
    "dev": 3,
    "fresh_hard": 3,
    "test": 3
  }
}
```

## Downstream Checks

FlashRAG candidate bundle:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates \
  --output outputs/deepseek/real_pilot_nickel_superalloy_full/flashrag_candidate \
  --dataset-name deepseek_real_pilot_full_candidates
```

Minimal candidate baseline:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates \
  --output outputs/deepseek/real_pilot_nickel_superalloy_full/benchmark \
  --methods no_rag \
  --split dev
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/deepseek/real_pilot_nickel_superalloy_full/benchmark/deepseek_real_pilot_full_candidates/dev_results.jsonl \
  --output outputs/deepseek/real_pilot_nickel_superalloy_full/report
```

Baseline report result:

```json
{
  "no_rag": {
    "api_calls": 0,
    "errors": 0,
    "questions": 3
  }
}
```

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_deepseek_real_pilot_script.py tests/test_deepseek_full_candidate_outputs.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy
```

Secret scan:

```bash
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs/deepseek benchmark scripts tests README.md docs data fixtures || true
```

Result: no secret-like values were found in committed files.

## Limitations

- The candidate dataset has one DeepSeek-generated question per chunk, not the final RAG.md target density.
- All 9 candidates were accepted by model review, but they still need human audit before replacing curated data.
- `fresh_hard` is structurally present, but it has not yet passed the full Fresh-Hard protocol of No-RAG low score plus Oracle-Context high score.
- Actual-RAG and multi-method FlashRAG comparison are still not run.

## Next Step

Phase 4 should implement Oracle-Context and a simple lexical Actual-RAG baseline over the real pilot and DeepSeek candidate dataset. That will start measuring whether the questions are answerable from the right evidence and whether retrieval can find it.
