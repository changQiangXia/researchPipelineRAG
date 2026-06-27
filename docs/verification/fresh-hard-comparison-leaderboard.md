# Fresh-Hard Comparison Leaderboard Verification

Phase: 5D - unified Fresh-Hard comparison report
Recorded: 2026-06-27T22:04:22Z

## Scope

Previous phases produced valid per-method or per-phase reports, but the evidence was scattered across Phase 4B, Phase 4C, Phase 5B, and Phase 5C output directories. Phase 5D adds a unified comparison report that merges answer metrics, retrieval metrics, DeepSeek Judge metrics, token usage, API calls, and unsupported-claim counts into one Fresh-Hard leaderboard.

This is a reporting layer. It does not call model APIs and does not change answer generation or retrieval behavior.

## Implementation

New module:

```text
benchmark/domainrag/comparison_report.py
```

New CLI:

```bash
PYTHONPATH=benchmark python -m domainrag.cli compare \
  --answer-inputs <answer_jsonl> [<answer_jsonl> ...] \
  --judge-inputs <judge_jsonl> [<judge_jsonl> ...] \
  --output <output_dir>
```

Output files:

```text
outputs/phase5d/fresh_hard_comparison/summary.json
outputs/phase5d/fresh_hard_comparison/summary.md
```

## Inputs

Answer inputs:

```text
outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl
outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl
outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl
```

Judge inputs:

```text
outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl
outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl
outputs/phase5c/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl
```

The report covers these methods:

```text
no_rag
oracle_context
lexical_rag
flashrag_bm25_oracle_reader
flashrag_bm25_live_deepseek
```

## Command

```bash
PYTHONPATH=benchmark python -m domainrag.cli compare \
  --answer-inputs \
    outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
    outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl \
    outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --judge-inputs \
    outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
    outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
    outputs/phase5c/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/phase5d/fresh_hard_comparison
```

## Leaderboard Snapshot

```text
flashrag_bm25_live_deepseek:
  answer_score: 0.9320
  retrieval_hit: 1.0000
  correctness: 5.0000
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 8
  unsupported_claims: 0

flashrag_bm25_oracle_reader:
  answer_score: 0.9167
  retrieval_hit: 1.0000
  correctness: 5.0000
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 4
  unsupported_claims: 0

lexical_rag:
  answer_score: 0.8631
  retrieval_hit: 1.0000
  correctness: 5.0000
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 8
  unsupported_claims: 0

oracle_context:
  answer_score: 0.9088
  retrieval_hit: 1.0000
  correctness: 5.0000
  faithfulness: 4.7500
  hallucination_risk: 0.2500
  api_calls: 8
  unsupported_claims: 1

no_rag:
  answer_score: 0.1504
  retrieval_hit: 0.0000
  correctness: 1.7500
  faithfulness: 1.2500
  hallucination_risk: 3.7500
  api_calls: 8
  unsupported_claims: 5
```

## Interpretation

The unified report makes the core pilot result easier to see:

- No-RAG can occasionally guess the right choice, but has no retrieval support and high hallucination risk.
- Context-backed methods reach perfect retrieval on the tiny pilot corpus.
- `flashrag_bm25_live_deepseek` is the first FlashRAG-derived retrieval path with non-oracle live answers and zero unsupported claims after prompt iteration.
- `flashrag_bm25_oracle_reader` remains a retrieval diagnostic, not a generated-answer method.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_comparison_report.py tests/test_phase5d_outputs.py -q
PYTHONPATH=benchmark pytest tests/test_cli.py::test_compare_command_writes_comparison_report -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- `answer_score` is a compact mean of non-retrieval rule metrics. Because question types use different metric families, it should be read as a rough report convenience, not a single definitive scientific score.
- All results still come from a 9-chunk, 12-question pilot dataset.
- The leaderboard does not yet include dense retrieval or reranking.
- DeepSeek Judge remains auxiliary and should be manually spot-checked before final reporting.
