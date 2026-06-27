# DomainRAG-Bench Phase 2A FlashRAG Intake Design

Date: 2026-06-27
Status: Pre-approved by user for continuous execution
Source blueprint: `/root/autodl-tmp/RAG/RAG.md`
Previous milestone: `docs/verification/first-milestone.md`

## Goal

Connect the first-milestone DomainRAG data contract to FlashRAG's real dataset/config conventions without vendoring FlashRAG source code or calling live model APIs.

This phase proves that `data/example_domain` can be prepared as a FlashRAG-consumable dataset bundle, that the upstream FlashRAG repository has been inspected and recorded, and that the adapter can be tested locally without requiring heavyweight FlashRAG dependencies.

## Scope

Phase 2A includes:

1. Local FlashRAG upstream checkout for intake only at `benchmark/flashrag-fork/`.
2. Baseline documentation for FlashRAG URL, commit SHA, license, dependency status, and key architecture entry points.
3. A committed DomainRAG-to-FlashRAG adapter in the existing `benchmark/domainrag` package.
4. A CLI/script path that prepares `data/example_domain` into FlashRAG's `data_dir/<dataset_name>/<split>.jsonl` convention.
5. A committed example FlashRAG config for the prepared example dataset.
6. Tests for split filename mapping, copied artifacts, config generation, and CLI behavior.
7. Verification documentation for the Phase 2A smoke flow.

## Out Of Scope

Phase 2A does not include:

1. Installing the full FlashRAG dependency set.
2. Running a live generator, retriever model, reranker, or DeepSeek API.
3. Building dense or sparse indexes.
4. Modifying FlashRAG upstream source files.
5. Vendoring the FlashRAG repository into this project's Git history.
6. Cloning or modifying Easy Dataset.
7. Processing real papers.

## Upstream Intake Decision

FlashRAG is cloned locally under `benchmark/flashrag-fork/` for inspection and smoke checks, but this directory is ignored by the DomainRAG-Bench repository.

Rationale:

- FlashRAG is a separate upstream project with its own Git history and large dependency surface.
- The DomainRAG-Bench repository should commit our adapter, configs, tests, and documentation, not a snapshot of upstream code.
- The baseline document records enough information to recreate the local checkout.

The observed upstream checkout for this phase is:

- URL: `https://github.com/RUC-NLPIR/FlashRAG.git`
- Commit: `e0e73399ce8d4563397b5fb4980de72a9c5e15a6`
- License shown in upstream README/badge and `LICENSE`: MIT

## FlashRAG Compatibility Surface

FlashRAG's dataset loader accepts split files with one JSON object per line:

```python
{
    "id": str,
    "question": str,
    "golden_answers": list[str],
    "metadata": dict,
}
```

This matches the DomainRAG split records from the first milestone.

FlashRAG resolves dataset files as:

```text
data_dir/<dataset_name>/<split>.jsonl
```

The DomainRAG split naming differs for Fresh-Hard:

```text
DomainRAG: fresh_hard_test.jsonl
FlashRAG: fresh_hard.jsonl
```

The adapter must copy or materialize the DomainRAG splits into a FlashRAG bundle and rename `fresh_hard_test.jsonl` to `fresh_hard.jsonl`.

## Adapter Design

Add `benchmark/domainrag/flashrag_adapter.py`.

Public interface:

```python
@dataclass(frozen=True)
class FlashRAGBundle:
    dataset_name: str
    data_dir: Path
    dataset_dir: Path
    corpus_path: Path
    qrels_dir: Path
    config_path: Path
    splits: tuple[str, ...]

def prepare_flashrag_bundle(
    dataset_dir: Path,
    output_dir: Path,
    dataset_name: str | None = None,
    splits: tuple[str, ...] = ("dev", "test", "fresh_hard"),
) -> FlashRAGBundle:
    ...
```

Behavior:

1. Validate the DomainRAG dataset before preparing files.
2. Create `output_dir/<dataset_name>/`.
3. Copy `dev.jsonl` and `test.jsonl` unchanged.
4. Copy `fresh_hard_test.jsonl` to `fresh_hard.jsonl`.
5. Copy `corpus.jsonl`.
6. Copy `qrels/` into the bundle for future retrieval metrics, even though FlashRAG's core dataset loader does not consume qrels directly.
7. Write a minimal YAML config that FlashRAG can use with `Config` once dependencies are installed.
8. Avoid adding a PyYAML runtime dependency by writing deterministic YAML text manually.

## CLI And Script Surface

Add a CLI subcommand:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/example_domain \
  --output outputs/flashrag \
  --dataset-name example_domain
```

Add a script wrapper:

```bash
python scripts/prepare_flashrag_example.py
```

The script uses the CLI-compatible adapter defaults and prints the prepared dataset path and config path.

## Config Surface

Commit `configs/flashrag/example_domain.yaml` as the stable example config for the prepared bundle:

```yaml
data_dir: outputs/flashrag
dataset_name: example_domain
split:
  - dev
  - test
  - fresh_hard
framework: openai
generator_model: local-noop
disable_save: true
metrics:
  - em
  - f1
  - acc
```

This config is intentionally not enough to run live generation. It is enough to document FlashRAG's dataset/config binding for the prepared bundle.

## Error Handling

The adapter fails with `ValidationError` when the source dataset fails the existing validator.

The adapter fails with `ValidationError` when a requested split is unsupported or its source file is missing.

The CLI returns non-zero on validation or preparation failure and prints the existing validation issue text.

## Testing

Tests must cover:

1. Preparing a bundle from `data/example_domain`.
2. Fresh-Hard filename mapping from `fresh_hard_test.jsonl` to `fresh_hard.jsonl`.
3. Corpus and qrels copy behavior.
4. Deterministic config generation.
5. CLI `prepare-flashrag` success.
6. CLI failure on `data/invalid_fixtures/missing_qrels`.

## Verification

Phase 2A verification commands:

```bash
pytest
python scripts/create_example_domain.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/example_domain --output outputs/flashrag --dataset-name example_domain
python scripts/prepare_flashrag_example.py
```

The expected result is a clean test suite and a prepared FlashRAG bundle under:

```text
outputs/flashrag/example_domain/
├── corpus.jsonl
├── dev.jsonl
├── fresh_hard.jsonl
├── qrels/
└── test.jsonl
```
