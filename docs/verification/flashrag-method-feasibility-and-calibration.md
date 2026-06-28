# FlashRAG Method Feasibility and Human Calibration Verification

Phase: 5E - FlashRAG method feasibility probe + Fresh-Hard human calibration packet
Recorded: 2026-06-27T22:25:58Z

## Scope

Phase 5D produced a unified Fresh-Hard leaderboard, but two gaps remained before claiming a stronger benchmark deliverable:

- whether the current runtime can safely execute FlashRAG dense retrieval or reranking
- whether DeepSeek Judge outputs can be packaged for human calibration

Phase 5E addresses both without installing new dependencies or mutating the CUDA/PyTorch environment. It adds a runtime feasibility manifest and a deterministic review packet generator over real Phase 5C outputs.

This phase does not call model APIs.

## Implementation

New modules:

```text
benchmark/domainrag/flashrag_method_feasibility.py
benchmark/domainrag/calibration_packet.py
```

New script:

```text
scripts/verify_flashrag_method_feasibility.py
```

New CLI commands:

```bash
PYTHONPATH=benchmark python -m domainrag.cli probe-flashrag-methods \
  --flashrag-path benchmark/flashrag-fork \
  --output outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/flashrag_method_feasibility/real_pilot_nickel_superalloy_manifest.json

PYTHONPATH=benchmark python -m domainrag.cli calibration-packet \
  --dataset data/real_pilot_nickel_superalloy \
  --answers outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --judge outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/human_calibration_fresh_hard \
  --split fresh_hard
```

## FlashRAG Runtime Feasibility

Output:

```text
outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/flashrag_method_feasibility/real_pilot_nickel_superalloy_manifest.json
```

FlashRAG checkout:

```text
benchmark/flashrag-fork/
```

FlashRAG commit:

```text
e0e73399ce8d4563397b5fb4980de72a9c5e15a6
```

Observed module imports:

```text
flashrag.dataset.dataset: ok
flashrag.retriever.retriever: ok
flashrag.retriever.index_builder: ok
flashrag.pipeline.pipeline: blocked by missing termcolor
flashrag.generator.generator: blocked by missing openai
```

Observed package state:

```text
torch: 2.1.2+cu121
transformers: 5.12.1
numpy: 1.26.3
faiss: 1.14.3
bm25s: 0.2.1
Stemmer: 3.1.0
sentence_transformers: missing
FlagEmbedding: missing
sklearn: missing
```

The `transformers` import also reports that this build requires PyTorch >= 2.4, while the current environment has PyTorch 2.1.2+cu121. That mismatch means model-backed dense paths should not be enabled by just adding missing packages in-place.

Method feasibility recorded in the manifest:

```text
flashrag_bm25: feasible=true
flashrag_dense: feasible=false
flashrag_reranker: feasible=false
```

Recommendation recorded in the manifest:

```text
keep_bm25_and_calibration_first
```

Interpretation:

- BM25 remains the current safe FlashRAG-backed method in this environment.
- Dense retriever and reranker work should use an isolated dependency plan, because changing PyTorch/transformers inside the current AutoDL environment is a larger environment-risk decision than this benchmark phase should hide.

## Human Calibration Packet

Outputs:

```text
outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/human_calibration_fresh_hard/review_packet.jsonl
outputs/archive/provenance/flashrag-integration/method-feasibility-calibration/human_calibration_fresh_hard/review_packet.md
```

Inputs:

```text
data/real_pilot_nickel_superalloy
outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl
outputs/archive/provenance/flashrag-integration/live-bm25-answer-judge/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl
```

Packet summary:

```text
rows: 4
split: fresh_hard
method: flashrag_bm25_live_deepseek
questions: ns_ht_q009, ns_ht_q010, ns_ht_q011, ns_ht_q012
priority: all normal
judge faithfulness: all 5.0
hallucination_risk: all 0.0
human_review fields: present and empty
```

Each JSONL row contains:

- question id, method, split, question type, question text
- gold answers and model prediction
- gold context ids and retrieved context ids
- retrieved context chunk text loaded from canonical `corpus.jsonl`
- answer metrics and answer error state
- DeepSeek Judge object, judge scores, and judge error state
- priority and priority reasons
- blank `human_review` fields for human correctness, context support, faithfulness, decision, and notes

Priority is set to `high` when an answer or judge error exists, a judge row is missing, unsupported claims are present, correctness/context support/faithfulness is below 5, or hallucination risk is above 0. The current committed Phase 5C final outputs produce no high-priority rows, but the generator is designed to surface them when they appear.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_flashrag_method_feasibility.py tests/test_calibration_packet.py tests/test_phase5e_outputs.py -q
PYTHONPATH=benchmark pytest tests/test_cli.py::test_probe_flashrag_methods_command_writes_manifest tests/test_cli.py::test_verify_flashrag_method_feasibility_script_writes_manifest tests/test_cli.py::test_calibration_packet_command_writes_review_files -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- Dense retrieval and reranking are not executed in this phase because the current runtime lacks required packages and has a PyTorch/transformers mismatch.
- The human calibration packet is a review artifact; it does not itself provide completed human labels.
- The underlying real pilot remains 9 chunks and 12 questions, so scale remains the largest unresolved RAG.md gap.

## Next Step

The next pragmatic target is scale expansion: add more real corpus chunks and questions, rerun BM25/live/Judge/comparison on the larger dataset, and then decide whether dense/rerank merits a separate isolated environment.
