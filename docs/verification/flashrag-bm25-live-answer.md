# FlashRAG BM25 Live Answer Verification

Phase: 5C - FlashRAG BM25 retrieved context + DeepSeek live answer
Recorded: 2026-06-27T21:54:29Z

## Scope

Phase 5B connected real FlashRAG Dataset and BM25 retrieval to the DomainRAG result schema, but its answerer was a deterministic oracle reader. Phase 5C keeps the real FlashRAG BM25 retrieved contexts and replaces the oracle reader with live DeepSeek answer generation.

Method name:

```text
flashrag_bm25_live_deepseek
```

This phase is the first FlashRAG-derived retrieval path that produces non-oracle live model answers and then feeds those answers into the existing report and DeepSeek Judge pipeline.

## Implementation

Updated module:

```text
benchmark/domainrag/deepseek_answer_runner.py
```

Updated CLI:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/live_deepseek_flashrag_bm25_fresh_hard \
  --methods flashrag_bm25_live_deepseek \
  --split fresh_hard \
  --retrieval-results outputs/archive/provenance/flashrag-integration/bm25-bridge-and-judge/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl \
  --max-retries 1
```

The `--retrieval-results` file is required when `flashrag_bm25_live_deepseek` is requested. It is the Phase 5B output containing `retrieved_context_ids`. The live answer runner loads those ids, pulls chunk text from the canonical DomainRAG dataset, and sends the retrieved context to DeepSeek.

The answer prompt now explicitly constrains context-grounded methods:

```text
Use only facts stated in the supplied context chunks.
Do not add mechanisms, causal links, or comparisons unless they are explicitly supported by those chunks.
```

For multiple-choice questions, the prompt also states that an option is supported when its statement is directly supported by any supplied context chunk. This prevents the model from returning an empty answer when correct options are distributed across different retrieved chunks.

## Live Answer Output

Output:

```text
outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl
```

Report:

```text
outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/live_deepseek_flashrag_bm25_fresh_hard/report_fresh_hard/summary.json
```

Summary:

```text
questions: 4
api_calls: 4
errors: 0
retrieval_hit: 1.0000
retrieval_recall: 1.0000
retrieval_mrr: 1.0000
single_choice_accuracy: 1.0000
multiple_choice_exact_match: 1.0000
fill_blank_normalized_em: 1.0000
short_answer_token_f1: 0.7895
```

Observed predictions:

```text
ns_ht_q009: A
ns_ht_q010: A,B,D,E
ns_ht_q011: intergranular
ns_ht_q012: Longitudinal orientation activates more slip systems and APB shearing, showing stronger creep resistance. Larger plastic strain flow promotes P-type rafting.
```

## DeepSeek Judge

Judge command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --input outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --output outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/deepseek_judge_flashrag_bm25_live_fresh_hard \
  --split fresh_hard \
  --max-retries 1

PYTHONPATH=benchmark python -m domainrag.cli judge-report \
  --input outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/deepseek_judge_flashrag_bm25_live_fresh_hard/report_fresh_hard
```

Judge summary:

```text
questions: 4
api_calls: 4
errors: 0
unsupported_claims: 0
correctness: 5.0000
context_support: 5.0000
faithfulness: 5.0000
relevance: 5.0000
hallucination_risk: 0.0000
```

## Iteration Note

The first Phase 5C live answer run exposed a real faithfulness issue on `ns_ht_q012`: the model inserted a causal phrasing not directly stated in the retrieved context. The prompt was tightened and rerun.

The second prompt variant fixed `ns_ht_q012` but made `ns_ht_q010` too conservative, producing an empty answer for a multi-choice question whose correct options were distributed across two retrieved chunks. The multiple-choice instruction was then clarified and rerun.

The committed Phase 5C outputs are from the final rerun: 4 answer API calls, 4 Judge API calls, 0 answer errors, 0 Judge errors, and 0 unsupported claims.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_deepseek_answer_runner.py tests/test_phase5c_outputs.py -q
PYTHONPATH=benchmark pytest tests/test_cli.py::test_run_deepseek_answers_accepts_flashrag_bm25_retrieval_results -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- This phase still uses the small 9-chunk pilot corpus, so retrieval remains saturated.
- The retrieval step is reused from Phase 5B output rather than recomputed inside the answer runner.
- This is still not a dense retriever or reranker experiment.
- DeepSeek Judge is an auxiliary evaluator and should be calibrated with human spot checks before final reporting.

## Next Step

The next meaningful implementation target is a second retrieval method under the same answer/Judge path. The pragmatic order is:

1. Add a dense retriever or reranker method if dependencies and model cache allow it.
2. Build a comparison report that places `no_rag`, `oracle_context`, `lexical_rag`, `flashrag_bm25_oracle_reader`, and `flashrag_bm25_live_deepseek` side by side.
3. Expand the real pilot corpus so retrieval methods stop saturating at 1.0.
