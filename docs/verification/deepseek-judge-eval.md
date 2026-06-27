# DeepSeek Judge Evaluation Verification

Phase: 4C - DeepSeek Judge for live answer outputs
Recorded: 2026-06-27T20:52:59Z

## Scope

This phase adds the auxiliary DeepSeek Judge described in `RAG.md` section 5.4. It does not replace rule-based metrics. Instead, it consumes Phase 4B live answer outputs and adds a second evaluation layer for:

- answer correctness
- context support
- faithfulness
- answer relevance
- unsupported factual claims

The Judge uses the 0 to 5 scoring scale from `RAG.md`.

## Implementation

New module:

```text
benchmark/domainrag/deepseek_judge_runner.py
```

New CLI commands:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset <dataset_dir> \
  --input <answer_results.jsonl> \
  --output <output_dir> \
  --split fresh_hard

PYTHONPATH=benchmark python -m domainrag.cli judge-report \
  --input <judge_results.jsonl> \
  --output <report_dir>
```

Security behavior:

- `DEEPSEEK_API_KEY` is required and is read only from the environment.
- Tests do not call DeepSeek.
- API keys are not written to outputs, configs, docs, git config, or logs.

Judge output rows include:

```text
id
method
split
prediction
golden_answers
gold_context_ids
retrieved_context_ids
judge
judge_scores
latency_ms
input_tokens
output_tokens
api_calls
error
```

Judge result schema:

```json
{
  "correctness": 4,
  "context_support": 4,
  "faithfulness": 5,
  "relevance": 5,
  "unsupported_claims": [],
  "reason": "..."
}
```

`judge_scores.hallucination_risk` is derived as `5 - faithfulness` for reporting convenience.

## Live Judge Run

Input answer results:

```text
outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl
```

Command:

```bash
DEEPSEEK_API_KEY=<set in environment> PYTHONPATH=benchmark \
python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --input outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --output outputs/phase4c/deepseek_judge_fresh_hard \
  --split fresh_hard \
  --max-retries 1 \
  --timeout-seconds 120
```

Report command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-report \
  --input outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/phase4c/deepseek_judge_fresh_hard/report_fresh_hard
```

Output:

```text
outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl
outputs/phase4c/deepseek_judge_fresh_hard/report_fresh_hard/summary.json
outputs/phase4c/deepseek_judge_fresh_hard/report_fresh_hard/summary.md
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
  "no_rag": {
    "questions": 4,
    "api_calls": 4,
    "errors": 0,
    "unsupported_claims": 5,
    "total_tokens": 5392,
    "metrics": {
      "correctness": 1.75,
      "context_support": 0.0,
      "faithfulness": 1.25,
      "hallucination_risk": 3.75,
      "relevance": 4.5
    }
  },
  "oracle_context": {
    "questions": 4,
    "api_calls": 4,
    "errors": 0,
    "unsupported_claims": 1,
    "total_tokens": 4362,
    "metrics": {
      "correctness": 5.0,
      "context_support": 5.0,
      "faithfulness": 4.75,
      "hallucination_risk": 0.25,
      "relevance": 5.0
    }
  },
  "lexical_rag": {
    "questions": 4,
    "api_calls": 4,
    "errors": 0,
    "unsupported_claims": 0,
    "total_tokens": 5263,
    "metrics": {
      "correctness": 5.0,
      "context_support": 5.0,
      "faithfulness": 5.0,
      "hallucination_risk": 0.0,
      "relevance": 5.0
    }
  }
}
```

Interpretation:

- Judge separates a model's unsupported No-RAG answer from a context-supported RAG answer even when both look fluent.
- `no_rag` has high relevance but low correctness, zero context support, and high hallucination risk on the live `fresh_hard` split.
- `oracle_context` and `lexical_rag` are high-scoring because the current pilot corpus is very small and lexical retrieval finds all gold contexts.
- `oracle_context` has one unsupported claim on `ns_ht_q012`, showing the Judge pass catches semantic overreach that token F1 alone cannot fully describe.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest \
  tests/test_deepseek_judge_runner.py \
  tests/test_phase4c_outputs.py \
  tests/test_cli.py::test_judge_deepseek_answers_requires_api_key \
  tests/test_cli.py::test_judge_deepseek_answers_rejects_invalid_runtime_options \
  tests/test_cli.py::test_judge_report_command_writes_summary \
  -q

pytest

grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" \
  outputs benchmark scripts tests README.md docs data fixtures || true
```

## Limitations

- Judge is still an LLM-based auxiliary evaluator; it should not replace rule-based metrics or human review.
- The current live Judge run covers only the curated pilot `fresh_hard` split.
- The pilot corpus is still small, so `lexical_rag` is artificially strong.
- Judge calibration has not yet been compared across multiple judge models or repeated runs.

## Next Step

The next phase should move from the local lexical bridge to actual FlashRAG multi-method runs. In parallel, the corpus should be expanded beyond the 9-chunk pilot so retrieval differences become meaningful.
