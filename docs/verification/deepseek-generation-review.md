# DeepSeek Generation and Review Verification

Phase: 3B - controlled DeepSeek generation and independent review
Recorded: 2026-06-27T19:35:00Z

## Scope

This phase adds a controlled DeepSeek generation/review loop for the Phase 3A real-data pilot. It proves that real source-derived chunks can be sent through an OpenAI-compatible DeepSeek API call, parsed as strict DomainRAG candidate items, independently reviewed by a second DeepSeek call, and converted into a valid DomainRAG candidate dataset.

This phase does not replace the curated Phase 3A public dataset. DeepSeek output is kept under `outputs/deepseek/` as candidate artifacts for inspection.

## Safety Boundary

- API keys are read only from `DEEPSEEK_API_KEY`.
- API keys are not written to config files, output files, git remotes, git config, or logs.
- Unit tests and dry-run tests do not call DeepSeek.
- Real API calls are explicit script runs, not part of `pytest`.
- Generation and review are separate requests.
- Outputs are accepted only after local schema validation and review quality checks.

## Implementation

Core module:

```text
benchmark/domainrag/deepseek_pipeline.py
```

Runner:

```text
scripts/run_deepseek_real_pilot.py
```

The module provides:

- generation prompt construction
- independent review prompt construction
- fenced/plain JSON response parsing
- generated item contract validation
- review result validation
- OpenAI-compatible `/chat/completions` calls with Python standard library

The script provides:

- `--dry-run` planning without requiring an API key
- default 3-item plan over the real pilot chunks
- generation model and review model selection
- bounded retries for empty or invalid responses
- `generated_items.jsonl`
- `review_results.jsonl`
- `accepted_items.jsonl`
- `raw_responses.jsonl`
- `run_manifest.json`

## Real API Run

Model availability was checked against:

```text
GET https://api.deepseek.com/models
```

Available models:

```text
deepseek-v4-flash
deepseek-v4-pro
```

The real run used:

```bash
DEEPSEEK_API_KEY=<env only> PYTHONPATH=benchmark python scripts/run_deepseek_real_pilot.py \
  --chunks fixtures/easy_dataset/real_pilot_nickel_superalloy/chunks.jsonl \
  --output outputs/deepseek/real_pilot_nickel_superalloy \
  --generation-model deepseek-v4-pro \
  --review-model deepseek-v4-pro \
  --max-items 3 \
  --max-retries 2
```

Output:

```text
generated items written to outputs/deepseek/real_pilot_nickel_superalloy/generated_items.jsonl
review results written to outputs/deepseek/real_pilot_nickel_superalloy/review_results.jsonl
accepted items written to outputs/deepseek/real_pilot_nickel_superalloy/accepted_items.jsonl
```

Current output size:

```text
3 accepted_items.jsonl
3 generated_items.jsonl
3 planned_requests.jsonl
6 raw_responses.jsonl
3 review_results.jsonl
```

Token usage from `raw_responses.jsonl`:

```json
{
  "generation_prompt": 1780,
  "generation_completion": 4548,
  "review_prompt": 1392,
  "review_completion": 3226
}
```

The real run produced 3 accepted candidate items:

- 1 `single_choice` item for `dev`
- 1 `fill_blank` item for `test`
- 1 `short_answer` item for `fresh_hard`

## Validation

Focused tests:

```bash
PYTHONPATH=benchmark pytest tests/test_deepseek_pipeline.py tests/test_deepseek_real_pilot_script.py -q
```

Result:

```text
9 passed
```

Candidate DomainRAG round trip:

```bash
mkdir -p /tmp/domainrag-deepseek-candidate-source
cp fixtures/easy_dataset/real_pilot_nickel_superalloy/chunks.jsonl \
  /tmp/domainrag-deepseek-candidate-source/chunks.jsonl
cp outputs/deepseek/real_pilot_nickel_superalloy/accepted_items.jsonl \
  /tmp/domainrag-deepseek-candidate-source/items.jsonl
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input /tmp/domainrag-deepseek-candidate-source \
  --output /tmp/domainrag-deepseek-candidate-output \
  --dataset-name deepseek_real_pilot_candidates
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset /tmp/domainrag-deepseek-candidate-output/deepseek_real_pilot_candidates
```

Result:

```text
DomainRAG dataset written to /tmp/domainrag-deepseek-candidate-output/deepseek_real_pilot_candidates
/tmp/domainrag-deepseek-candidate-output/deepseek_real_pilot_candidates is valid
```

## Issue Found and Fixed

The first live DeepSeek run exposed a useful contract bug: the model could return choice `options` as an array, while DomainRAG requires an object keyed by `A`, `B`, `C`, and `D` for single-choice questions. The local validator originally checked field presence but did not reject this shape.

Phase 3B added regression coverage and fixed the root cause:

- choice options must be keyed objects, not arrays
- single-choice answers must be one option key
- multiple-choice answers must include at least two option keys
- fill-blank and short-answer options must be empty objects
- source-context phrases such as `provided information` are rejected
- generation prompts now include explicit JSON shape examples

## Limitations

- Only 3 candidate items were generated and reviewed in this phase.
- DeepSeek outputs are candidate artifacts, not final gold data.
- The review is model-based and still needs human audit before replacing or expanding curated data.
- No Oracle-Context, Actual-RAG, or full Fresh-Hard filtering was run in this phase.

## Next Step

Phase 3C should use this same pipeline to generate a full candidate set for all Phase 3A chunks, then add an audit step that compares DeepSeek candidates against the curated items and marks accepted/rejected/needs-human-review records.
