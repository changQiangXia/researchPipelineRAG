# Phase 6F: Medium Human Calibration Audit

This phase adds a small manual audit over the Phase 6E medium Fresh-Hard
calibration packet. The goal is not to replace the DeepSeek Judge, but to
check whether its scores are directionally reliable on representative rows
before using the Judge metrics in the final medium-pilot report.

## Inputs

- Dataset packet:
  `outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_human_calibration_fresh_hard/review_packet.jsonl`
- Manual labels:
  `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/human_labels.jsonl`
- Output directory:
  `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit`

The manual subset contains 15 rows, evenly distributed across the five
evaluated methods:

- `no_rag`: 3 rows
- `oracle_context`: 3 rows
- `lexical_rag`: 3 rows
- `flashrag_bm25_oracle_reader`: 3 rows
- `flashrag_bm25_live_deepseek`: 3 rows

The sample intentionally favors risky rows: 14 of the 15 rows are
high-priority rows from the calibration packet, and 7 rows contain Judge
unsupported-claim flags.

## Command

```bash
PYTHONPATH=benchmark python -m domainrag.cli calibration-audit \
  --packet outputs/archive/provenance/expanded-pilots/medium-live-and-judge/medium_human_calibration_fresh_hard/review_packet.jsonl \
  --labels outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/human_labels.jsonl \
  --output outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit
```

This writes:

- `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/reviewed_rows.jsonl`
- `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/summary.json`
- `outputs/archive/provenance/expanded-pilots/medium-human-calibration-audit/medium_human_calibration_audit/summary.md`

## Results

Overall human scores across the 15 reviewed rows:

- correctness: 3.5333
- context_support: 2.9000
- faithfulness: 2.9000

Overall Judge scores on the same rows:

- correctness: 3.4000
- context_support: 2.6000
- faithfulness: 2.6000

Mean absolute human-vs-Judge delta:

- correctness: 0.1333
- context_support: 0.3667
- faithfulness: 0.3667

Agreement within 1 point:

- correctness: 15 / 15, rate 1.0000
- context_support: 13 / 15, rate 0.8667
- faithfulness: 13 / 15, rate 0.8667

Human decisions:

- agree_with_judge: 10
- mostly_agree_with_judge: 3
- disagree_with_judge: 2

## Method-Level Summary

| method | rows | human correctness | human support | human faithfulness | judge correctness | judge support | judge faithfulness |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_rag` | 3 | 2.0000 | 0.0000 | 0.0000 | 1.6667 | 0.0000 | 0.0000 |
| `oracle_context` | 3 | 4.0000 | 5.0000 | 5.0000 | 4.0000 | 5.0000 | 5.0000 |
| `lexical_rag` | 3 | 3.3333 | 3.1667 | 3.1667 | 3.0000 | 3.3333 | 3.3333 |
| `flashrag_bm25_oracle_reader` | 3 | 5.0000 | 3.0000 | 3.0000 | 5.0000 | 1.3333 | 1.3333 |
| `flashrag_bm25_live_deepseek` | 3 | 3.3333 | 3.3333 | 3.3333 | 3.3333 | 3.3333 | 3.3333 |

## Interpretation

The audit supports using the DeepSeek Judge as a directional evaluator for the
medium pilot. Correctness agreement is especially strong in this subset, and
support/faithfulness agreement remains high enough to preserve the Phase 6E
ranking conclusions.

The main observed bias is in partial-evidence rows for
`flashrag_bm25_oracle_reader`. For `ns_ht_q024` and `ns_ht_q060`, BM25 retrieved
some but not all required evidence. The Judge assigned 0.0 to context support
and faithfulness, while the human audit assigned 2.5 because half of the answer
was grounded. This means the Judge is conservative on partial support: useful
for flagging risk, but potentially too harsh when summarizing graded support.

This reinforces the earlier Phase 6C-6E conclusion: retrieval hit rate is not
enough. The benchmark should continue reporting retrieval recall, Judge support,
faithfulness, and unsupported-claim counts together, especially for multi-source
questions.

## Verification

```bash
PYTHONPATH=benchmark pytest tests/test_calibration_audit.py
PYTHONPATH=benchmark pytest tests/test_cli.py -k calibration_audit_module_entrypoint_writes_summary
PYTHONPATH=benchmark pytest tests/test_phase6f_outputs.py
```

Observed results during implementation:

- `tests/test_calibration_audit.py`: 3 passed
- `tests/test_cli.py -k calibration_audit_module_entrypoint_writes_summary`: 1 passed
- `tests/test_phase6f_outputs.py`: 1 passed
