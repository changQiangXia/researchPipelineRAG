# DeepSeek Live Answer Evaluation Verification

Phase: 4B - live DeepSeek answer generation for No-RAG, Oracle-Context, and lexical RAG
Recorded: 2026-06-27T20:33:11Z

## Scope

This phase moves the Phase 4 diagnostic runner from a perfect-reader simulation to real model answering. It keeps deterministic retrieval diagnostics, but the answer text now comes from DeepSeek API calls.

Implemented methods:

- `no_rag`: sends the question without context.
- `oracle_context`: sends the qrels gold context chunks.
- `lexical_rag`: retrieves top-k chunks with the deterministic lexical retriever, then sends those chunks to DeepSeek.

The normal `domainrag run` command remains deterministic and offline. Live model calls are isolated behind the new `run-deepseek-answers` command.

## Implementation

New runner:

```text
benchmark/domainrag/deepseek_answer_runner.py
```

CLI entry:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset <dataset_dir> \
  --output <output_dir> \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard
```

Security behavior:

- `DEEPSEEK_API_KEY` is required and is read only from the environment.
- Tests do not call DeepSeek.
- API keys are not written to outputs, configs, docs, git config, or logs.

Result rows preserve the Phase 4 schema and add live model usage:

```text
prediction
gold_context_ids
retrieved_context_ids
scores.retrieval_hit
scores.retrieval_recall
scores.retrieval_mrr
latency_ms
input_tokens
output_tokens
api_calls
error
```

The report generator now summarizes token usage:

```text
mean_input_tokens
mean_output_tokens
total_input_tokens
total_output_tokens
total_tokens
```

## Debugging Finding

The first live run exposed a DeepSeek response-shape issue on reasoning-heavy questions:

```text
finish_reason=length
message.content=""
message.reasoning_content=<non-empty reasoning>
completion_tokens exhausted
```

Root cause:

- The original answer-runner default `max_tokens=512` was too low for `deepseek-v4-pro` style reasoning responses.
- Some failed responses still consumed prompt and completion tokens, but the runner initially recorded those failed rows as zero-token failures.
- Empty `{"answer": ""}` responses were initially treated as successful blank predictions.

Fixes:

- Increased live answer default `max_tokens` to `4096`.
- Preserved usage from received responses even when parsing fails.
- Rejected empty normalized answers and records them as errors.
- Strengthened choice prompts with "Select every supported option" and "Never return an empty answer."

## Live Dataset Run

Dataset:

```text
data/real_pilot_nickel_superalloy
```

Split:

```text
fresh_hard
```

Methods:

```text
no_rag
oracle_context
lexical_rag
```

Command:

```bash
DEEPSEEK_API_KEY=<set in environment> PYTHONPATH=benchmark \
python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs/archive/provenance/pilot-benchmarks/live-deepseek-fresh-hard/live_deepseek_fresh_hard \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard \
  --max-retries 1 \
  --timeout-seconds 120
```

Report command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/archive/provenance/pilot-benchmarks/live-deepseek-fresh-hard/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --output outputs/archive/provenance/pilot-benchmarks/live-deepseek-fresh-hard/live_deepseek_fresh_hard/report_fresh_hard
```

Output:

```text
outputs/archive/provenance/pilot-benchmarks/live-deepseek-fresh-hard/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl
outputs/archive/provenance/pilot-benchmarks/live-deepseek-fresh-hard/live_deepseek_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/pilot-benchmarks/live-deepseek-fresh-hard/live_deepseek_fresh_hard/report_fresh_hard/summary.md
```

Final live run:

```text
rows: 12
errors: 0
api calls: 12
```

Summary:

```json
{
  "_diagnostics": {
    "fresh_hard_candidate_ids": [
      "ns_ht_q010",
      "ns_ht_q011"
    ],
    "fresh_hard_candidates": 2
  },
  "no_rag": {
    "questions": 4,
    "api_calls": 4,
    "errors": 0,
    "total_tokens": 2238,
    "metrics": {
      "retrieval_recall": 0.0,
      "multiple_choice_exact_match": 0.0,
      "fill_blank_alias_match": 0.0,
      "short_answer_token_f1": 0.2033898305084746,
      "single_choice_accuracy": 1.0
    }
  },
  "oracle_context": {
    "questions": 4,
    "api_calls": 4,
    "errors": 0,
    "total_tokens": 4463,
    "metrics": {
      "retrieval_recall": 1.0,
      "multiple_choice_exact_match": 1.0,
      "fill_blank_alias_match": 1.0,
      "short_answer_token_f1": 0.6037735849056604,
      "single_choice_accuracy": 1.0
    }
  },
  "lexical_rag": {
    "questions": 4,
    "api_calls": 4,
    "errors": 0,
    "total_tokens": 4701,
    "metrics": {
      "retrieval_recall": 1.0,
      "multiple_choice_exact_match": 1.0,
      "fill_blank_alias_match": 1.0,
      "short_answer_token_f1": 0.5714285714285714,
      "single_choice_accuracy": 1.0
    }
  }
}
```

Interpretation:

- `ns_ht_q009` is no longer a strong Fresh-Hard candidate under live DeepSeek because the model answered it correctly without context.
- `ns_ht_q010` and `ns_ht_q011` remain useful Fresh-Hard candidates: No-RAG is low, while Oracle-Context succeeds.
- `lexical_rag` retrieved all gold contexts on this small pilot split, so it currently matches Oracle retrieval recall. This is expected at pilot scale and will become more meaningful on a larger corpus.
- Short-answer scoring is still lexical/required-point based; DeepSeek Judge is still needed for faithfulness and semantic adequacy.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_deepseek_answer_runner.py tests/test_cli.py::test_run_deepseek_answers_requires_api_key tests/test_report_generator.py -q
pytest
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates
```

## Limitations

- Only the curated pilot `fresh_hard` split was run live in this phase.
- The corpus is still tiny, so lexical retrieval is artificially easy.
- DeepSeek Judge is not implemented yet.
- FlashRAG's full multi-method pipelines are not run yet.
- Cost is recorded as token usage, not priced currency; pricing should not be hardcoded into the repo.

## Next Step

The next phase should add a DeepSeek Judge pass over live answer outputs. It should score answer correctness, context support, and faithfulness while preserving the existing rule-based metrics. After that, the project should move from the local lexical bridge into actual FlashRAG multi-method runs.
