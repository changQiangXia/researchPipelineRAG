# Expanded Real Pilot Scale Verification

Phase: 6A - medium real-data pilot expansion
Recorded: 2026-06-27T22:46:24Z

## Scope

Phase 5E made FlashRAG method feasibility and human calibration explicit, but the main RAG.md gap remained dataset scale. Phase 6A starts closing that gap by adding a larger real-data pilot for the existing nickel-superalloy high-temperature failure domain.

This phase does not call model APIs. It produces a larger validated dataset, FlashRAG bundle, and deterministic fresh_hard baseline so the next phase can run live DeepSeek answer and Judge on a more meaningful split.

## New Data Assets

New source manifest:

```text
data/real_pilot_sources/nickel_superalloy_high_temp_failure_expanded/sources.jsonl
```

New Easy Dataset-style enriched fixture:

```text
fixtures/easy_dataset/real_pilot_nickel_superalloy_expanded/chunks.jsonl
fixtures/easy_dataset/real_pilot_nickel_superalloy_expanded/items.jsonl
```

New DomainRAG dataset:

```text
data/real_pilot_nickel_superalloy_expanded/
```

New build script:

```text
scripts/build_real_pilot_expanded.py
```

Build command:

```bash
python scripts/build_real_pilot_expanded.py
```

## Dataset Shape

Expanded dataset statistics:

```text
corpus chunks: 17
questions: 24
dev: 8
test: 8
fresh_hard: 8
single_choice: 6
multiple_choice: 6
fill_blank: 6
short_answer: 6
```

Compared with the earlier curated pilot, this doubles the question count and adds eight more real-source chunks while preserving the public data contract.

Newly covered knowledge areas include:

- transfer-learning-guided single-crystal superalloy creep design
- molten-salt hot corrosion and alloying effects
- SLM Inconel 625 heat treatment plus pre-oxidation
- drilled single-crystal superalloy hot-corrosion behavior
- entropy-based GH4169 low-cycle fatigue prediction
- PM-HIP superalloy fatigue-property factors
- TiC-containing Inconel 625 oxidation behavior
- stress-dependent local phase transformation strengthening

Public exported files still omit source paper identity metadata. Source titles and URLs remain only in the internal source manifest.

## FlashRAG Bundle

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_expanded
```

Output:

```text
outputs/flashrag/real_pilot_nickel_superalloy_expanded/
outputs/flashrag/real_pilot_nickel_superalloy_expanded_flashrag.yaml
```

The bundle contains `dev.jsonl`, `test.jsonl`, `fresh_hard.jsonl`, `corpus.jsonl`, and split qrels.

## Fresh-Hard Baseline

Command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/phase6a/expanded_baseline \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard

PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/phase6a/expanded_baseline/real_pilot_nickel_superalloy_expanded/fresh_hard_results.jsonl \
  --output outputs/phase6a/expanded_baseline/report_fresh_hard
```

Output:

```text
outputs/phase6a/expanded_baseline/real_pilot_nickel_superalloy_expanded/fresh_hard_results.jsonl
outputs/phase6a/expanded_baseline/report_fresh_hard/summary.json
outputs/phase6a/expanded_baseline/report_fresh_hard/summary.md
```

Baseline summary:

```text
fresh_hard questions: 8
fresh_hard diagnostic candidates: 6
no_rag retrieval_hit: 0.0
oracle_context retrieval_hit: 1.0
lexical_rag retrieval_hit: 1.0
```

The lexical baseline still saturates retrieval on this intermediate corpus. That is useful evidence that the project needs a larger Phase 6B/6C scale step before dense/rerank comparisons become meaningful.

## Verification Commands

```bash
PYTHONPATH=benchmark pytest tests/test_real_pilot_expanded_assets.py tests/test_phase6a_outputs.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_expanded
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures || true
git diff --check
```

## Limitations

- This is still far below RAG.md's standard scale target.
- New facts are manually curated and should later be superseded by a more systematic literature intake process.
- No expanded live DeepSeek answer or Judge run is included in Phase 6A.
- Lexical retrieval still saturates, so dense/rerank evaluation should wait for more scale or harder distractor chunks.

## Next Step

Run expanded `fresh_hard` live DeepSeek answer and DeepSeek Judge using the existing Phase 4B/4C pipeline, then produce a Phase 6B comparison and calibration packet for the 8-question expanded split.
