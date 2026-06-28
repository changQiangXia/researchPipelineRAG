# Expanded FlashRAG BM25 Live Comparison Verification

Phase: 6C - expanded Fresh-Hard FlashRAG BM25 bridge, live answer, Judge, comparison, and calibration
Recorded: 2026-06-27T23:29:31Z

## Scope

Phase 6C adds FlashRAG BM25 to the expanded `real_pilot_nickel_superalloy_expanded` Fresh-Hard comparison from Phase 6B.

This phase uses:

- Real FlashRAG `Dataset`, `Index_Builder`, and `BM25Retriever` runtime calls for retrieval.
- Real DeepSeek API calls for the BM25 live answer run and both BM25 Judge runs.
- A five-method comparison over the same 8 expanded Fresh-Hard questions.
- A combined human calibration packet covering all five methods.

API keys are read only from `DEEPSEEK_API_KEY` and are not written to repository files.

## Dataset

Dataset:

```text
data/real_pilot_nickel_superalloy_expanded
```

FlashRAG bundle:

```text
outputs/flashrag/real_pilot_nickel_superalloy_expanded
```

Split:

```text
fresh_hard
```

Question count:

```text
8
```

Methods in the final comparison:

```text
no_rag
oracle_context
lexical_rag
flashrag_bm25_oracle_reader
flashrag_bm25_live_deepseek
```

## FlashRAG BM25 Bridge

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-flashrag-bm25 \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy_expanded \
  --output outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge \
  --dataset-name real_pilot_nickel_superalloy_expanded \
  --split fresh_hard \
  --top-k 5 \
  --index-dir outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge/index \
  --rebuild-index
```

Output:

```text
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge/real_pilot_nickel_superalloy_expanded/fresh_hard_flashrag_bm25_results.jsonl
```

Observed result:

```text
rows: 8
api_calls: 0
errors: 0
retrieval_hit: 1.0000
retrieval_recall: 0.9375
```

FlashRAG BM25 hits every question, but it does not fully cover every multi-source question. In particular, `ns_ht_q024` retrieves the PM-HIP review source but misses the entropy-fatigue source required by the gold answer.

## BM25 Oracle-Reader Judge

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --input outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge/real_pilot_nickel_superalloy_expanded/fresh_hard_flashrag_bm25_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

Outputs:

```text
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_fresh_hard/report_fresh_hard/summary.md
```

Observed result:

```text
rows: 8
judge API calls: 8
errors: 0
correctness: 5.0000
faithfulness: 4.3750
hallucination_risk: 0.6250
unsupported_claims: 1
```

The oracle-reader answer text is exactly the gold answer when BM25 hits at least one gold context. This exposes a useful edge case: correctness can be perfect while context support is not, because partial retrieval can leave part of a synthesized gold answer unsupported.

## BM25 Live DeepSeek Answer And Judge

Answer command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_live_deepseek_flashrag_bm25_fresh_hard \
  --methods flashrag_bm25_live_deepseek \
  --split fresh_hard \
  --retrieval-results outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge/real_pilot_nickel_superalloy_expanded/fresh_hard_flashrag_bm25_results.jsonl \
  --max-retries 2
```

Judge command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --input outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_live_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

Outputs:

```text
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_live_fresh_hard/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_live_fresh_hard/report_fresh_hard/summary.md
```

Observed result:

```text
answer rows: 8
answer API calls: 10
answer errors: 1
judge rows: 8
judge API calls: 7
judge errors: 1
```

`ns_ht_q010` returned empty DeepSeek message content after three answer attempts and is preserved as a real answer error. The Judge runner records the corresponding Judge row as an answer-row error without making a Judge API call for that row.

## Comparison And Calibration

Comparison command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli compare \
  --answer-inputs \
    outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge/real_pilot_nickel_superalloy_expanded/fresh_hard_flashrag_bm25_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --judge-inputs \
    outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_fresh_hard_comparison
```

Calibration command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli calibration-packet \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --answers \
    outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_flashrag_bm25_bridge/real_pilot_nickel_superalloy_expanded/fresh_hard_flashrag_bm25_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --judge \
    outputs/archive/provenance/expanded-pilots/expanded-deepseek-evaluation/expanded_deepseek_judge_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
    outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_judge_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_human_calibration_fresh_hard \
  --split fresh_hard
```

Outputs:

```text
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_fresh_hard_comparison/summary.json
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_fresh_hard_comparison/summary.md
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_human_calibration_fresh_hard/review_packet.jsonl
outputs/archive/provenance/expanded-pilots/expanded-flashrag-evaluation/expanded_human_calibration_fresh_hard/review_packet.md
```

Calibration packet rows:

```text
40
```

## Leaderboard Snapshot

```text
lexical_rag:
  retrieval_hit: 1.0000
  retrieval_recall: 1.0000
  correctness: 5.0000
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 17
  unsupported_claims: 0

oracle_context:
  retrieval_hit: 1.0000
  retrieval_recall: 1.0000
  correctness: 4.8750
  faithfulness: 5.0000
  hallucination_risk: 0.0000
  api_calls: 16
  unsupported_claims: 0

flashrag_bm25_oracle_reader:
  retrieval_hit: 1.0000
  retrieval_recall: 0.9375
  correctness: 5.0000
  faithfulness: 4.3750
  hallucination_risk: 0.6250
  api_calls: 8
  unsupported_claims: 1

flashrag_bm25_live_deepseek:
  retrieval_hit: 1.0000
  retrieval_recall: 0.9375
  correctness: 3.7500
  faithfulness: 4.3750
  hallucination_risk: 0.6250
  api_calls: 17
  unsupported_claims: 0

no_rag:
  retrieval_hit: 0.0000
  retrieval_recall: 0.0000
  correctness: 1.8750
  faithfulness: 0.7500
  hallucination_risk: 4.2500
  api_calls: 18
  unsupported_claims: 10
```

## Interpretation

Phase 6C closes the expanded FlashRAG BM25 gap from Phase 6B:

- FlashRAG BM25 is now exercised on the expanded real pilot bundle through actual FlashRAG runtime objects.
- The final expanded Fresh-Hard comparison covers five methods instead of three.
- The combined calibration packet now covers all five methods and all 8 Fresh-Hard questions.
- BM25 and lexical both hit every question, but BM25 has lower recall on multi-source questions. This created a useful context-support failure on `ns_ht_q024`.
- No-RAG remains clearly separated by context support and hallucination risk.

The most important technical finding is that hit rate alone is insufficient. On synthesized questions with multiple required sources, a method can hit one relevant chunk and still leave part of the answer unsupported. The framework now captures that through retrieval recall, Judge faithfulness, unsupported claims, and high-priority calibration rows.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_calibration_packet.py -q
PYTHONPATH=benchmark pytest tests/test_phase6c_outputs.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_expanded
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- The expanded corpus still has only 17 chunks, so retrieval separation is not yet representative of the full RAG.md target scale.
- `flashrag_bm25_live_deepseek` has one preserved real answer error on `ns_ht_q010`.
- Dense retrieval and reranking remain deferred because Phase 5E found runtime dependency conflicts in the current AutoDL environment.
- Human review fields are present in the calibration packet, but the packet has not been manually filled.

## Next Step

The next highest-value step is another real-data scale expansion. The current stack is already capable of ingesting the expanded data, running FlashRAG BM25, calling live DeepSeek, judging, comparing, and producing calibration packets. More chunks and more Fresh-Hard questions are now the main blocker to stronger retrieval-method differentiation.
