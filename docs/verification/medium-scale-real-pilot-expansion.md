# Medium-Scale Real Pilot Expansion Verification

Phase: 6D - medium-scale real pilot data expansion and retrieval diagnostics
Recorded: 2026-06-28T00:01:16Z

## Scope

Phase 6D expands the real nickel-superalloy pilot from the Phase 6A/6C shape to a larger medium pilot dataset. The goal is to reduce the retrieval saturation observed with 17 chunks and 8 Fresh-Hard questions.

This phase does not call DeepSeek live APIs. It focuses on:

- Expanding source-backed chunks and questions.
- Exporting a valid DomainRAG dataset.
- Preparing a FlashRAG bundle.
- Running diagnostic `no_rag`, `oracle_context`, and `lexical_rag`.
- Running real FlashRAG BM25 retrieval through FlashRAG runtime objects.
- Comparing lexical retrieval and FlashRAG BM25 retrieval on the larger Fresh-Hard split.

## Dataset

Dataset:

```text
data/real_pilot_nickel_superalloy_medium
```

Easy Dataset-style fixture:

```text
fixtures/easy_dataset/real_pilot_nickel_superalloy_medium
```

Source manifest:

```text
data/real_pilot_sources/nickel_superalloy_high_temp_failure_medium/sources.jsonl
```

Builder:

```text
scripts/build_real_pilot_medium.py
```

Shape:

```text
corpus chunks: 40
questions: 60
dev: 20
test: 20
fresh_hard: 20
single_choice: 15
multiple_choice: 15
fill_blank: 15
short_answer: 15
source records: 32
```

The medium fixture appends 23 new source-backed chunks and 36 new questions to the Phase 6A expanded fixture. The added material covers:

- Rene 77 steam oxidation and cast heat-treatment microstructure.
- DD5 over-temperature phase stability and creep rupture degradation.
- K452 SO2 corrosion.
- Hastelloy N stress-assisted FLiNaK corrosion.
- AM Hastelloy X fatigue modelling.
- AM nickel-superalloy feedstock and defect review evidence.
- Phase-field-informed ML creep descriptors.
- Single-crystal high-temperature LCF damage competition.
- Film-cooling-hole hot corrosion.
- Coating interdiffusion, steam/fireside corrosion, hydrogen-assisted LCF, LPBF cracking, Laves/delta heat-treatment control, creep-fatigue dwell damage, chloride molten-salt corrosion, and rejuvenation risk.

## Build Commands

Build the medium fixture, source manifest, and DomainRAG export:

```bash
PYTHONPATH=benchmark python scripts/build_real_pilot_medium.py
```

Validate the dataset:

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_medium
```

Prepare FlashRAG:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_medium
```

## Diagnostic Baseline

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_medium \
  --output outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_baseline \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard
```

Report:

```bash
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_baseline/real_pilot_nickel_superalloy_medium/fresh_hard_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_baseline/report_fresh_hard
```

Outputs:

```text
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_baseline/real_pilot_nickel_superalloy_medium/fresh_hard_results.jsonl
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_baseline/report_fresh_hard/summary.json
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_baseline/report_fresh_hard/summary.md
```

Observed Fresh-Hard result:

```text
fresh_hard questions: 20
fresh_hard diagnostic candidates: 15

no_rag:
  retrieval_hit: 0.0000
  retrieval_recall: 0.0000

oracle_context:
  retrieval_hit: 1.0000
  retrieval_recall: 1.0000

lexical_rag:
  retrieval_hit: 0.9500
  retrieval_recall: 0.9250
  retrieval_mrr: 0.9250
```

Compared with Phase 6C, lexical retrieval is no longer saturated.

## FlashRAG BM25

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-flashrag-bm25 \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy_medium \
  --output outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_flashrag_bm25_bridge \
  --dataset-name real_pilot_nickel_superalloy_medium \
  --split fresh_hard \
  --top-k 5 \
  --index-dir outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_flashrag_bm25_bridge/index \
  --rebuild-index
```

Output:

```text
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_flashrag_bm25_bridge/real_pilot_nickel_superalloy_medium/fresh_hard_flashrag_bm25_results.jsonl
```

Observed Fresh-Hard result:

```text
questions: 20
retrieval_hit: 0.9500
retrieval_recall: 0.8542
retrieval_mrr: 0.9000
misses: ns_ht_q049
partial-recall questions: ns_ht_q023, ns_ht_q024, ns_ht_q056, ns_ht_q057, ns_ht_q060
```

BM25 and lexical both hit 19 of 20 questions, but BM25 has weaker full-evidence recall on multi-source questions.

## Retrieval Comparison

A lexical-only comparison input was produced from the diagnostic baseline:

```text
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_retrieval_comparison_inputs/lexical_fresh_hard_results.jsonl
```

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli compare \
  --answer-inputs \
    outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_retrieval_comparison_inputs/lexical_fresh_hard_results.jsonl \
    outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_flashrag_bm25_bridge/real_pilot_nickel_superalloy_medium/fresh_hard_flashrag_bm25_results.jsonl \
  --output outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_retrieval_comparison
```

Outputs:

```text
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_retrieval_comparison/summary.json
outputs/archive/provenance/expanded-pilots/medium-baseline-and-bm25/medium_retrieval_comparison/summary.md
```

Snapshot:

```text
lexical_rag:
  questions: 20
  retrieval_hit: 0.9500
  retrieval_recall: 0.9250
  retrieval_mrr: 0.9250

flashrag_bm25_oracle_reader:
  questions: 20
  retrieval_hit: 0.9500
  retrieval_recall: 0.8542
  retrieval_mrr: 0.9000
```

## Interpretation

Phase 6D improves the evidence quality of the project in two ways:

- Dataset scale increased from 17 chunks / 24 questions to 40 chunks / 60 questions.
- Retrieval diagnostics now show misses and partial evidence recall, rather than universal saturation.

The most useful new finding is that the medium Fresh-Hard split separates hit rate from full evidence recall. Both lexical and BM25 retrieve at least one gold context for 19 of 20 questions, but BM25 misses more required evidence on multi-source synthesis questions. This supports the Phase 6C conclusion that `retrieval_hit` alone is not enough for Fresh-Hard evaluation.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_real_pilot_medium_assets.py -q
PYTHONPATH=benchmark pytest tests/test_phase6d_outputs.py -q
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- The medium corpus is still far below the RAG.md target of thousands of chunks.
- Phase 6D does not run live DeepSeek answer/Judge on the new 20-question Fresh-Hard split.
- Dense retrieval and reranking are still deferred because Phase 5E found dependency conflicts in the current environment.
- Source records are traceability metadata for the pilot; the public DomainRAG export still excludes paper identity metadata as intended.

## Next Step

Run live DeepSeek answer and Judge on the medium Fresh-Hard split for the main comparison methods. Recommended next comparison:

```text
no_rag
oracle_context
lexical_rag
flashrag_bm25_oracle_reader
flashrag_bm25_live_deepseek
```

The medium dataset should make this live/Judge run more meaningful than the previous 17-chunk expanded dataset.
