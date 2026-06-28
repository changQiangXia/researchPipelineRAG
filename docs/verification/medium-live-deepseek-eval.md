# Medium Fresh-Hard Live DeepSeek Evaluation Verification

Phase: 6E - medium Fresh-Hard live answer, Judge, comparison, and calibration
Recorded: 2026-06-28T00:34:04Z

## Scope

Phase 6E runs live DeepSeek answer and Judge evaluation on the Phase 6D medium-scale real pilot dataset.

Dataset:

```text
data/real_pilot_nickel_superalloy_medium
```

Split:

```text
fresh_hard
```

Question count:

```text
20
```

Final methods:

```text
no_rag
oracle_context
lexical_rag
flashrag_bm25_oracle_reader
flashrag_bm25_live_deepseek
```

API keys are read only from `DEEPSEEK_API_KEY` and are not written to repository files.

## Live Answer And Judge Runs

Base answer command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --output outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_live_deepseek_fresh_hard \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard \
  --max-retries 2
```

Base Judge command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --input outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_deepseek_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

BM25 oracle-reader Judge command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --input outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_flashrag_bm25_bridge/real_pilot_nickel_superalloy_medium/fresh_hard_flashrag_bm25_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

BM25 live answer command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --output outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_live_deepseek_flashrag_bm25_fresh_hard \
  --methods flashrag_bm25_live_deepseek \
  --split fresh_hard \
  --retrieval-results outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_flashrag_bm25_bridge/real_pilot_nickel_superalloy_medium/fresh_hard_flashrag_bm25_results.jsonl \
  --max-retries 2
```

BM25 live Judge command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --input outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_deepseek_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_live_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

Observed API result:

```text
base answers: 60 rows, 60 API calls, 0 errors
base Judge: 60 rows, 60 API calls, 0 errors
BM25 oracle-reader Judge: 20 rows, 20 API calls, 0 errors
BM25 live answers: 20 rows, 20 API calls, 0 errors
BM25 live Judge: 20 rows, 20 API calls, 0 errors
total live API calls recorded in outputs: 180
```

## Outputs

```text
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_deepseek_results.jsonl
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_judge_results.jsonl
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_judge_results.jsonl
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_deepseek_results.jsonl
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy_medium/fresh_hard_judge_results.jsonl
```

Judge reports:

```text
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_fresh_hard/report_fresh_hard/summary.md
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_fresh_hard/report_fresh_hard/summary.md
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_live_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_deepseek_judge_flashrag_bm25_live_fresh_hard/report_fresh_hard/summary.md
```

Comparison and calibration:

```text
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_fresh_hard_comparison/summary.json
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_fresh_hard_comparison/summary.md
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_human_calibration_fresh_hard/review_packet.jsonl
outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_human_calibration_fresh_hard/review_packet.md
```

Calibration packet rows:

```text
100
```

## Leaderboard Snapshot

```text
oracle_context:
  answer_score: 0.8358
  retrieval_hit: 1.0000
  retrieval_recall: 1.0000
  correctness: 4.8500
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  unsupported_claims: 0
  api_calls: 40

lexical_rag:
  answer_score: 0.8251
  retrieval_hit: 0.9500
  retrieval_recall: 0.9250
  correctness: 4.7000
  faithfulness: 4.7500
  hallucination_risk: 0.2500
  unsupported_claims: 1
  api_calls: 40

flashrag_bm25_live_deepseek:
  answer_score: 0.6573
  retrieval_hit: 0.9500
  retrieval_recall: 0.8542
  correctness: 4.3500
  faithfulness: 4.7500
  hallucination_risk: 0.2500
  unsupported_claims: 0
  api_calls: 40

flashrag_bm25_oracle_reader:
  answer_score: 0.8583
  retrieval_hit: 0.9500
  retrieval_recall: 0.8542
  correctness: 4.7500
  faithfulness: 4.4500
  hallucination_risk: 0.5500
  unsupported_claims: 4
  api_calls: 20

no_rag:
  answer_score: 0.5153
  retrieval_hit: 0.0000
  retrieval_recall: 0.0000
  correctness: 3.4500
  faithfulness: 2.5000
  hallucination_risk: 2.5000
  unsupported_claims: 17
  api_calls: 40
```

## Interpretation

Phase 6E is the strongest live evaluation so far:

- The medium Fresh-Hard split has 20 questions instead of 8.
- All live answer and Judge calls completed without recorded errors.
- No-RAG still looks superficially better on some direct answer metrics than it should, but the Judge exposes the problem: 17 unsupported claims, 0 context support, and hallucination risk 2.5.
- Oracle context remains the upper-bound method: full retrieval recall, zero hallucination risk, and zero unsupported claims.
- Lexical retrieval is no longer saturated. It misses or partially retrieves evidence enough to produce one unsupported claim and non-zero hallucination risk.
- FlashRAG BM25 live is meaningfully below lexical because BM25 has weaker full-evidence recall on multi-source questions.
- BM25 oracle-reader is intentionally diagnostic: it can be correct as an answer string while still receiving lower faithfulness when retrieved context does not fully support all parts of the gold answer.

The central conclusion from Phase 6C is now better supported at medium scale: retrieval hit rate alone is insufficient. Fresh-Hard evaluation needs recall/full-evidence metrics plus answer faithfulness judging.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_phase6e_outputs.py -q
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- The medium corpus still has only 40 chunks, below the RAG.md target scale.
- Dense retrieval and reranking remain deferred to an isolated environment because the current AutoDL Python stack has dependency conflicts from Phase 5E.
- Human calibration fields are present but not manually filled.
- No-RAG can still guess some choice/fill-blank answers. The Judge and unsupported-claim counts are therefore more important than raw exact-match metrics for interpreting RAG value.

## Next Step

At this point, the next highest-value work is not another small runner change. The next step should be one of:

1. Scale again toward hundreds or thousands of chunks, using the same medium-builder pattern.
2. Fill a small human calibration subset from the 100-row packet to check DeepSeek Judge alignment.
3. Build an isolated dense/rerank environment only after deciding whether BM25/lexical separation at medium scale is enough for the report.
