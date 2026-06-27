# FlashRAG BM25 Bridge Verification

Phase: 5B - FlashRAG Dataset + BM25 retriever bridge
Recorded: 2026-06-27T21:36:05Z

## Scope

Phase 5A proved that the real upstream FlashRAG `Dataset` class can load the DomainRAG FlashRAG bundle. Phase 5B moves one step further: it builds a BM25s index over the real pilot corpus, runs FlashRAG's `BM25Retriever`, and writes standard DomainRAG result rows that can be consumed by the existing `report` and DeepSeek Judge paths.

The method name is deliberately explicit:

```text
flashrag_bm25_oracle_reader
```

This is a retrieval-focused bridge. It uses real FlashRAG Dataset intake and real FlashRAG BM25 retrieval, then uses a deterministic oracle reader: if retrieved context intersects qrels gold context, the output answer is the gold answer; otherwise it is empty. It must not be interpreted as a full FlashRAG generator pipeline.

## Upstream Checkout

Path:

```text
benchmark/flashrag-fork/
```

This path is ignored by git and not committed.

Commit observed in Phase 5A:

```text
e0e73399ce8d4563397b5fb4980de72a9c5e15a6
```

## Runtime Dependencies

Phase 5B required additional runtime dependencies for real FlashRAG retriever imports:

```bash
source /etc/network_turbo
python -m pip install --index-url https://pypi.org/simple \
  'transformers>=4.40.0' datasets faiss-cpu 'bm25s[core]==0.2.1' \
  PyStemmer rank_bm25 langid tiktoken
```

After installation:

```text
flashrag.utils.utils: OK
flashrag.retriever.retriever: OK
flashrag.retriever.index_builder: OK
flashrag.pipeline.pipeline: still blocked by termcolor
```

The pipeline import is not a Phase 5B blocker because this phase uses `Dataset`, `Index_Builder`, and `BM25Retriever`, not `SequentialPipeline`.

Runtime warnings observed:

- `transformers` reports that local PyTorch is below its preferred version for model execution.
- `numba` reports that the available TBB version disables the TBB threading layer.

These warnings did not block BM25s index build or retrieval.

## Implementation

New module:

```text
benchmark/domainrag/flashrag_bm25_bridge.py
```

New CLI:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-flashrag-bm25 \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy \
  --output outputs/phase5b/flashrag_bm25_bridge \
  --dataset-name real_pilot_nickel_superalloy \
  --split fresh_hard \
  --top-k 5 \
  --index-dir outputs/phase5b/flashrag_bm25_bridge/index \
  --rebuild-index
```

Subsequent splits reuse the same BM25s index:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-flashrag-bm25 \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy \
  --output outputs/phase5b/flashrag_bm25_bridge \
  --dataset-name real_pilot_nickel_superalloy \
  --split dev \
  --top-k 5 \
  --index-dir outputs/phase5b/flashrag_bm25_bridge/index

PYTHONPATH=benchmark python -m domainrag.cli run-flashrag-bm25 \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy \
  --output outputs/phase5b/flashrag_bm25_bridge \
  --dataset-name real_pilot_nickel_superalloy \
  --split test \
  --top-k 5 \
  --index-dir outputs/phase5b/flashrag_bm25_bridge/index
```

Reports:

```bash
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/dev_flashrag_bm25_results.jsonl \
  --output outputs/phase5b/flashrag_bm25_bridge/report_dev

PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/test_flashrag_bm25_results.jsonl \
  --output outputs/phase5b/flashrag_bm25_bridge/report_test

PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl \
  --output outputs/phase5b/flashrag_bm25_bridge/report_fresh_hard
```

## Outputs

Result rows:

```text
outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/dev_flashrag_bm25_results.jsonl
outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/test_flashrag_bm25_results.jsonl
outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl
```

Reports:

```text
outputs/phase5b/flashrag_bm25_bridge/report_dev/summary.json
outputs/phase5b/flashrag_bm25_bridge/report_test/summary.json
outputs/phase5b/flashrag_bm25_bridge/report_fresh_hard/summary.json
```

BM25s index:

```text
outputs/phase5b/flashrag_bm25_bridge/index/bm25/
```

The index is committed because the current pilot index is only about 44 KB and is useful evidence that the real FlashRAG BM25s build path ran successfully.

## Retrieval Results

The real pilot currently has 9 corpus chunks and 12 questions, split into 4 questions per split.

All three splits reached:

```text
retrieval_hit: 1.0000
retrieval_recall: 1.0000
retrieval_mrr: 1.0000
errors: 0
api_calls: 0
```

`fresh_hard` retrieval examples:

```text
ns_ht_q009: top-1 ns_ht_creep_rafting_al_mobility_001
ns_ht_q010: top-2 covers ns_ht_oxidation_ce_coating_001 and ns_ht_oxidation_lpbf_gh3536_001
ns_ht_q011: top-1 ns_ht_oxidation_ce_coating_001
ns_ht_q012: top-2 covers ns_ht_creep_orientation_850c_001 and ns_ht_creep_rafting_al_mobility_001
```

Because the deterministic oracle reader emits the gold answer on retrieval hit, answer metrics also reach the ceiling on this small pilot. This should be read as evidence that the BM25 retrieval bridge and report schema are connected, not as a claim that a generated-answer FlashRAG method is solved.

## DeepSeek Judge

The `fresh_hard` Phase 5B output was also evaluated with live DeepSeek Judge:

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --input outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl \
  --output outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard \
  --split fresh_hard \
  --max-retries 1

PYTHONPATH=benchmark python -m domainrag.cli judge-report \
  --input outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/report_fresh_hard
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

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_flashrag_bm25_bridge.py tests/test_phase5b_outputs.py -q
PYTHONPATH=benchmark pytest tests/test_cli.py::test_run_flashrag_bm25_command -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- The corpus remains very small: 9 chunks. BM25 and lexical retrieval are both expected to look easier than they would at realistic scale.
- Phase 5B does not run FlashRAG `SequentialPipeline`.
- Phase 5B does not run a dense retriever, reranker, or generated-answer FlashRAG method.
- The oracle reader is intentionally deterministic and should be used as a retrieval diagnostic, not as a final method comparison against real generators.

## Next Step

The next phase should add one non-oracle answer path after retrieval. The pragmatic order is:

1. Use the existing DeepSeek answer runner with `flashrag_bm25` retrieved contexts.
2. Add one dense retriever or reranker path once dependency and model-cache constraints are clear.
3. Expand the real pilot corpus so retrieval metrics stop saturating at top-1/top-2.
