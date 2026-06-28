# Expanded Live DeepSeek Evaluation Verification

Phase: 6B - expanded Fresh-Hard live answer, Judge, comparison, and calibration
Recorded: 2026-06-27T23:04:12Z

## Scope

Phase 6A added the expanded real pilot dataset with 17 chunks and 24 questions. Phase 6B runs the existing live answer and DeepSeek Judge pipeline on the expanded `fresh_hard` split.

This phase uses real DeepSeek API calls. API keys are read only from `DEEPSEEK_API_KEY` and are not written to repository files.

## Dataset

Dataset:

```text
data/real_pilot_nickel_superalloy_expanded
```

Split:

```text
fresh_hard
```

Question count:

```text
8
```

Methods:

```text
no_rag
oracle_context
lexical_rag
```

## Live Answer Run

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard \
  --max-retries 1
```

Output:

```text
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl
```

Observed result:

```text
rows: 24
answer API calls: 27
errors: 0
```

Three rows needed one retry, and all eventually produced valid answer JSON.

## DeepSeek Judge Run

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --input outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

Output:

```text
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl
```

Observed result:

```text
rows: 24
judge API calls: 24
errors: 0
```

Judge report:

```text
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/report_fresh_hard/summary.md
```

## Comparison and Calibration

Comparison command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli compare \
  --answer-inputs outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --judge-inputs outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_fresh_hard_comparison
```

Calibration command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli calibration-packet \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --answers outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --judge outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_human_calibration_fresh_hard \
  --split fresh_hard
```

Outputs:

```text
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_fresh_hard_comparison/summary.json
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_fresh_hard_comparison/summary.md
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_human_calibration_fresh_hard/review_packet.jsonl
outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_human_calibration_fresh_hard/review_packet.md
```

Calibration packet rows:

```text
24
```

## Leaderboard Snapshot

```text
lexical_rag:
  answer_score: 0.8673
  retrieval_hit: 1.0000
  correctness: 5.0000
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 17
  unsupported_claims: 0

oracle_context:
  answer_score: 0.8631
  retrieval_hit: 1.0000
  correctness: 4.8750
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 16
  unsupported_claims: 0

no_rag:
  answer_score: 0.1572
  retrieval_hit: 0.0000
  correctness: 1.8750
  faithfulness: 0.7500
  hallucination_risk: 4.2500
  api_calls: 18
  unsupported_claims: 10
```

## Interpretation

Expanded `fresh_hard` preserves the expected RAG advantage:

- No-RAG can guess some option letters, but has no context support and high hallucination risk.
- Context-backed methods have zero unsupported claims in this run.
- `lexical_rag` and `oracle_context` still saturate retrieval at 1.0, so the expanded 17-chunk dataset is still not large enough to separate lexical, BM25, and dense retrieval.

The most useful new evidence is not that lexical retrieval is superior; it is that the expanded live/Judge/calibration chain now works on the larger dataset and exposes No-RAG unsupported claims at a larger scale than Phase 5.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_phase6b_outputs.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_expanded
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- This phase does not run FlashRAG BM25 on the expanded dataset.
- Dense retrieval and reranking remain blocked by Phase 5E runtime feasibility findings.
- The expanded corpus still has only 17 chunks, and lexical retrieval still saturates.
- Human review fields are present in the calibration packet, but the packet has not been manually filled.

## Next Step

Run FlashRAG BM25 on `real_pilot_nickel_superalloy_expanded`, then run the existing `flashrag_bm25_live_deepseek` path against those retrieved contexts. If BM25 and lexical both remain saturated, the next priority should be another scale expansion rather than dense/rerank.
