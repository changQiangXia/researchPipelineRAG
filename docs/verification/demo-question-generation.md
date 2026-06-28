# Phase 7M: Provisional Demo-Question Generation

Recorded: 2026-06-28

Dataset:

```text
data/real_pilot_nickel_superalloy_demo_questions
```

Source dataset:

```text
data/real_pilot_nickel_superalloy_medium_plus
```

## Purpose

Phase 7M closes the immediate 300-question engineering gap without pretending
that the source-signoff gate has been completed. It builds a deterministic,
provisional 300-question dataset from the already validated 100-chunk
medium-plus corpus, validates the DomainRAG data contract, prepares a FlashRAG
bundle, and runs local retrieval diagnostics on the Fresh-Hard split.

This phase intentionally does not generate questions from the Phase 7L chunk
manifests because those committed manifests omit chunk text by design. It also
does not call DeepSeek. The result is a pipeline-verification and provisional
benchmark-rehearsal artifact, not a human-final demo benchmark.

## Commands

```bash
PYTHONPATH=benchmark python -m domainrag.cli build-demo-questions \
  --source-dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output data \
  --dataset-name real_pilot_nickel_superalloy_demo_questions \
  --target-questions 300 \
  --fixture-output outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/easy_dataset_export

PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_demo_questions

PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_demo_questions

PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard

PYTHONPATH=benchmark python -m domainrag.cli run-hashed-dense \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense \
  --split fresh_hard \
  --top-k 5 \
  --dimensions 512
```

Reports:

```bash
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline/real_pilot_nickel_superalloy_demo_questions/fresh_hard_results.jsonl \
  --output outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline/report_fresh_hard

PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense/real_pilot_nickel_superalloy_demo_questions/fresh_hard_hashed_dense_results.jsonl \
  --output outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense/report_fresh_hard
```

## Outputs

```text
data/real_pilot_nickel_superalloy_demo_questions/
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/easy_dataset_export/
outputs/flashrag/real_pilot_nickel_superalloy_demo_questions/
outputs/flashrag/real_pilot_nickel_superalloy_demo_questions_flashrag.yaml
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline/
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense/
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/demo_question_summary.json
```

## Dataset Shape

| item | count |
| --- | ---: |
| corpus chunks | 100 |
| total questions | 300 |
| dev questions | 100 |
| test questions | 100 |
| fresh_hard questions | 100 |
| single_choice | 75 |
| multiple_choice | 75 |
| fill_blank | 75 |
| short_answer | 75 |

Every generated item keeps at least one `source_chunk_ids` value and receives a
fixed `quality_score` of 0.7. The generator partitions source chunks by split so
that dev/test source groups stay disjoint under the DomainRAG validator.

The generated `dataset_card.md` explicitly labels the dataset as:

```text
Provisional demo-question dataset.
```

## Fresh-Hard Baseline Results

| method | questions | retrieval_hit | retrieval_recall | retrieval_mrr | api_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `no_rag` | 100 | 0.0000 | 0.0000 | 0.0000 | 0 |
| `oracle_context` | 100 | 1.0000 | 1.0000 | 1.0000 | 0 |
| `lexical_rag` | 100 | 0.7200 | 0.7200 | 0.5550 | 0 |

The baseline output contains 300 rows: 100 questions for each of the three
methods.

## Fresh-Hard Hashed Dense Results

| method | questions | retrieval_hit | retrieval_recall | retrieval_mrr | api_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hashed_dense_oracle_reader` | 100 | 0.7000 | 0.7000 | 0.5445 | 0 |
| `hashed_dense_lexical_rerank_oracle_reader` | 100 | 0.7200 | 0.7200 | 0.5557 | 0 |

This is still a local non-neural benchmark. It does not claim FlashRAG neural
dense retriever or neural reranker execution.

## Interpretation

Phase 7M materially advances the `RAG.md` question-scale target:

```text
300 provisional questions generated and validated
```

The correct boundary is:

```text
provisional_machine_generated_not_human_final
final_demo_dataset_claim_not_complete
```

What this phase closes:

- a deterministic 300-question generation route;
- a validated DomainRAG dataset at the lower bound of the demo question target;
- a FlashRAG bundle for that dataset;
- local Fresh-Hard baseline and hashed dense diagnostics.

What remains open:

- final manually signed-off 100-180 source whitelist;
- regeneration or filtering from human-accepted sources;
- live DeepSeek answer/Judge and human calibration over the 300-question set,
  if the project needs a final demo benchmark rather than a provisional
  rehearsal;
- neural dense/rerank execution in the isolated environment described by Phase
  7A, if neural retrieval is required.

## Verification

Focused verification:

```bash
PYTHONPATH=benchmark pytest tests/test_demo_question_generation.py tests/test_cli.py::test_build_demo_questions_command_writes_dataset
PYTHONPATH=benchmark pytest tests/test_phase7m_outputs.py
```

Completion checks before commit:

```bash
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_demo_questions
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
python -m json.tool docs/reports/rag-md-implementation-audit.json >/tmp/phase7m-audit.json
python -m json.tool outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/demo_question_summary.json >/tmp/phase7m-summary.json
git diff --check
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs/archive/provenance/source-workflow outputs/archive/provenance/retrieval-diagnostics outputs/archive/provenance/demo-dataset benchmark scripts tests docs pyproject.toml README.md || true
```
