# Oracle and Lexical RAG Evaluation Verification

Phase: 4 - Oracle-Context and lexical RAG evaluation loop
Recorded: 2026-06-27T20:05:00Z

## Scope

This phase starts the actual RAG diagnostic loop described in `RAG.md`. It adds two non-API baselines to the benchmark runner:

- `oracle_context`: uses the gold qrels context and returns the gold answer.
- `lexical_rag`: retrieves top-k chunks with a deterministic lexical TF-IDF style scorer; if a gold context is retrieved, it returns the gold answer as a perfect-reader simulation.

This is not yet a production LLM RAG method. It is the first measurable bridge between dataset production and RAG evaluation:

```text
No-RAG low
Oracle-Context high
Lexical retrieval hit/recall measured against qrels
```

## Implementation

Modified runner:

```text
benchmark/domainrag/benchmark_runner.py
```

New result fields:

```text
gold_context_ids
retrieved_context_ids
scores.retrieval_hit
scores.retrieval_recall
scores.retrieval_mrr
```

Modified report generator:

```text
benchmark/domainrag/report_generator.py
```

New diagnostics:

```json
{
  "_diagnostics": {
    "fresh_hard_candidates": 0,
    "fresh_hard_candidate_ids": []
  }
}
```

A question is counted as a Fresh-Hard candidate when:

```text
no_rag answer score < 0.60
oracle_context answer score >= 0.80
```

Retrieval metrics are excluded from the answer score used for this diagnostic.

## Datasets Evaluated

Curated real pilot:

```text
data/real_pilot_nickel_superalloy
```

DeepSeek full candidate dataset:

```text
outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates
```

Both datasets were evaluated on:

```text
dev
test
fresh_hard
```

Methods:

```text
no_rag
oracle_context
lexical_rag
```

## Commands

```bash
for split in dev test fresh_hard; do
  PYTHONPATH=benchmark python -m domainrag.cli run \
    --dataset data/real_pilot_nickel_superalloy \
    --output outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/curated \
    --methods no_rag,oracle_context,lexical_rag \
    --split "$split"
  PYTHONPATH=benchmark python -m domainrag.cli report \
    --input "outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/curated/real_pilot_nickel_superalloy/${split}_results.jsonl" \
    --output "outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/curated/report_${split}"

  PYTHONPATH=benchmark python -m domainrag.cli run \
    --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates \
    --output outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/deepseek_candidate \
    --methods no_rag,oracle_context,lexical_rag \
    --split "$split"
  PYTHONPATH=benchmark python -m domainrag.cli report \
    --input "outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/deepseek_candidate/deepseek_real_pilot_full_candidates/${split}_results.jsonl" \
    --output "outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/deepseek_candidate/report_${split}"
done
```

## Output

Curated reports:

```text
outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/curated/report_dev/summary.json
outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/curated/report_test/summary.json
outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/curated/report_fresh_hard/summary.json
```

DeepSeek candidate reports:

```text
outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/deepseek_candidate/report_dev/summary.json
outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/deepseek_candidate/report_test/summary.json
outputs/archive/provenance/pilot-benchmarks/curated-and-candidate-baselines/deepseek_candidate/report_fresh_hard/summary.json
```

Curated `fresh_hard` result:

```json
{
  "_diagnostics": {
    "fresh_hard_candidates": 3,
    "fresh_hard_candidate_ids": [
      "ns_ht_q009",
      "ns_ht_q010",
      "ns_ht_q011"
    ]
  },
  "no_rag": {
    "metrics": {
      "retrieval_recall": 0.0
    }
  },
  "oracle_context": {
    "metrics": {
      "retrieval_recall": 1.0
    }
  },
  "lexical_rag": {
    "metrics": {
      "retrieval_hit": 1.0,
      "retrieval_recall": 1.0
    }
  }
}
```

DeepSeek candidate `fresh_hard` result:

```json
{
  "_diagnostics": {
    "fresh_hard_candidates": 3,
    "fresh_hard_candidate_ids": [
      "creep_descriptor_q1",
      "domainrag_fresh_hard_001",
      "ns_ht_am_abd900_heat_treatment_001_fb1"
    ]
  },
  "no_rag": {
    "metrics": {
      "retrieval_recall": 0.0
    }
  },
  "oracle_context": {
    "metrics": {
      "retrieval_recall": 1.0
    }
  },
  "lexical_rag": {
    "metrics": {
      "retrieval_hit": 1.0,
      "retrieval_recall": 1.0
    }
  }
}
```

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_benchmark_runner.py tests/test_report_generator.py tests/test_phase4_outputs.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates
```

## Limitations

- `lexical_rag` is a deterministic retrieval baseline with a perfect-reader answer simulation, not a real LLM RAG pipeline.
- The current pilot corpus is small, so lexical retrieval is easier than the final target setting.
- Fresh-Hard diagnostics use local answer metrics and no live model; the full RAG.md protocol still requires real model No-RAG and Oracle-Context calls.
- Multi-method FlashRAG algorithms are not run yet.

## Next Step

Phase 4B should add a controlled live DeepSeek answer-generation runner for `no_rag`, `oracle_context`, and `lexical_rag`, preserving the same result schema and adding token/cost accounting. That will replace the perfect-reader simulation with real model behavior while keeping the deterministic retrieval diagnostics.
