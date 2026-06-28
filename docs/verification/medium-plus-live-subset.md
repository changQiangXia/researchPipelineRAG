# Medium-Plus Live DeepSeek Subset

Recorded: 2026-06-28

Phase: Phase 7C

Blueprint: `/root/autodl-tmp/RAG/RAG.md`

## Scope

Phase 7C adds a bounded live DeepSeek answer/Judge run on the Phase 7B
medium-plus dataset.

Run summary: 12 Fresh-Hard questions, three methods, 36 answer rows, and 36 judge rows.

This is not the final RAG.md demo scale. The goal is to verify that the
100-chunk / 150-question medium-plus checkpoint supports real answer
generation, real Judge scoring, comparison reporting, token accounting, and
retrieval-linked diagnosis beyond deterministic oracle-reader outputs.

## Command

The committed run was generated with:

```bash
PYTHONPATH=benchmark python scripts/run_medium_plus_live_subset.py \
  --limit 12 \
  --model deepseek-v4-pro \
  --max-retries 2
```

The script reads `DEEPSEEK_API_KEY` from the shell environment. It does not
store API keys in code, configs, logs, or generated outputs.

Dry-run command inspection:

```bash
PYTHONPATH=benchmark python scripts/run_medium_plus_live_subset.py \
  --dry-run \
  --limit 12
```

## Inputs

Dataset:

- `data/real_pilot_nickel_superalloy_medium_plus/`

Retrieval input for `flashrag_bm25_live_deepseek`:

- `outputs/archive/provenance/expanded-pilots/medium-plus-baseline-and-bm25/medium_plus_bm25s/real_pilot_nickel_superalloy_medium_plus/fresh_hard_bm25s_results.jsonl`

The live subset uses the first 12 medium-plus Fresh-Hard questions. This range
includes partial-recall rows and one BM25s retrieval miss, so it is more
diagnostic than the first 8-question sample.

## Outputs

- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/answers/real_pilot_nickel_superalloy_medium_plus/fresh_hard_deepseek_results.jsonl`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/judge/real_pilot_nickel_superalloy_medium_plus/fresh_hard_judge_results.jsonl`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/judge_report/summary.json`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/judge_report/summary.md`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/comparison/summary.json`
- `outputs/archive/provenance/expanded-pilots/medium-plus-live-subset/medium_plus_live_subset/comparison/summary.md`

## Run Shape

| item | count |
| --- | ---: |
| Fresh-Hard questions | 12 |
| Methods | 3 |
| Answer rows | 36 |
| Judge rows | 36 |
| Answer API calls | 39 |
| Judge API calls | 36 |
| Total API calls | 75 |
| Answer errors | 0 |
| Judge errors | 0 |

Methods:

- `no_rag`
- `lexical_rag`
- `flashrag_bm25_live_deepseek`

## Comparison Results

| method | questions | retrieval hit | retrieval recall | answer score | correctness | faithfulness | hallucination risk | unsupported claims | total tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flashrag_bm25_live_deepseek` | 12 | 0.9167 | 0.7569 | 0.8554 | 5.0000 | 5.0000 | 0.0000 | 0 | 32147 |
| `lexical_rag` | 12 | 0.9167 | 0.7361 | 0.8540 | 5.0000 | 5.0000 | 0.0000 | 0 | 31399 |
| `no_rag` | 12 | 0.0000 | 0.0000 | 0.3074 | 2.5833 | 1.2500 | 3.7500 | 18 | 36107 |

## Interpretation

The bounded medium-plus live run shows the expected separation between
retrieval-grounded methods and No-RAG. `lexical_rag` and
`flashrag_bm25_live_deepseek` both retrieve at least one gold context for 11 of
12 questions, and their live answers receive full Judge faithfulness and
correctness on this subset. No-RAG still answers some choice questions
correctly from prior knowledge, but it has no retrieved evidence, much weaker
Judge correctness, high hallucination risk, and 18 unsupported claims.

The run also confirms that Phase 7B's medium-plus output is suitable for real
model evaluation. It does not close the final scale gap: the current best
dataset remains 100 chunks / 150 questions, while the RAG.md demo target remains
1,000-3,000 chunks / 300-500 questions.

## Verification

Fresh checks used for this phase:

```bash
PYTHONPATH=benchmark pytest tests/test_phase7c_live_subset.py -q
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_medium_plus
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures pyproject.toml || true
git diff --check
```
