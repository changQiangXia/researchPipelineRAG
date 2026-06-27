# DomainRAG-Bench Phase 2A FlashRAG Intake Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested FlashRAG intake and DomainRAG adapter path that prepares `data/example_domain` as a FlashRAG-consumable dataset bundle without vendoring FlashRAG or calling live model APIs.

**Architecture:** Keep FlashRAG as an ignored local upstream checkout used for inspection only. Commit DomainRAG-owned adapter code under `benchmark/domainrag`, a `prepare-flashrag` CLI subcommand, a script wrapper, example config, baseline/architecture docs, and verification docs. The adapter validates the existing data contract, maps DomainRAG split names to FlashRAG split names, copies corpus/qrels for future retrieval metrics, and writes deterministic YAML config text.

**Tech Stack:** Python 3.10+, pytest, standard-library pathlib/shutil/dataclasses/argparse/subprocess. No live APIs, no FlashRAG dependency installation requirement, no Easy Dataset work, no PyYAML dependency.

## Global Constraints

- Work in `/root/autodl-tmp/RAG/DomainRAG-Bench/.worktrees/phase-2a-flashrag-adapter`.
- Keep `benchmark/flashrag-fork/` ignored; do not commit FlashRAG upstream source.
- Do not call live DeepSeek APIs.
- Do not call live OpenAI-compatible model APIs.
- Do not install heavyweight FlashRAG dependencies as a required verification step.
- Tests must pass with the existing lightweight Python environment.
- Preserve first-milestone CLI behavior and outputs.
- Public data artifacts must not expose DOI, author, venue, page number, original PDF path, or original paper title fields.
- Every behavior change must be test-first.
- Every task ends with verification and a commit.

---

## File Structure

Create or modify:

```text
.gitignore
benchmark/domainrag/cli.py
benchmark/domainrag/flashrag_adapter.py
configs/flashrag/example_domain.yaml
docs/architecture-flashrag.md
docs/baseline/flashrag-baseline.md
docs/superpowers/specs/2026-06-27-domainrag-phase-2a-flashrag-intake-design.md
docs/superpowers/plans/2026-06-27-domainrag-phase-2a-flashrag-intake-implementation.md
docs/verification/flashrag-intake.md
scripts/prepare_flashrag_example.py
tests/test_cli.py
tests/test_flashrag_adapter.py
```

Local ignored checkout:

```text
benchmark/flashrag-fork/
```

---

### Task 1: FlashRAG Intake Baseline And Design Artifacts

**Files:**
- Modify: `.gitignore`
- Create: `docs/baseline/flashrag-baseline.md`
- Create: `docs/architecture-flashrag.md`
- Create: `docs/superpowers/specs/2026-06-27-domainrag-phase-2a-flashrag-intake-design.md`
- Create: `docs/superpowers/plans/2026-06-27-domainrag-phase-2a-flashrag-intake-implementation.md`

**Interfaces:**
- Produces: documented upstream URL, commit SHA, license, dependency status, and architecture map.
- Consumes: local ignored checkout `benchmark/flashrag-fork/`.

- [ ] **Step 1: Confirm FlashRAG checkout metadata**

Run:

```bash
cd /root/autodl-tmp/RAG/DomainRAG-Bench/.worktrees/phase-2a-flashrag-adapter
git -C benchmark/flashrag-fork rev-parse HEAD
git -C benchmark/flashrag-fork remote get-url origin
```

Expected:

```text
e0e73399ce8d4563397b5fb4980de72a9c5e15a6
https://github.com/RUC-NLPIR/FlashRAG.git
```

- [ ] **Step 2: Record dependency import baseline**

Run:

```bash
PYTHONPATH=benchmark/flashrag-fork python - <<'PY'
from flashrag.dataset import Dataset
print("dataset import ok")
from flashrag.utils import get_dataset
print("utils import ok")
PY
```

Expected in the current environment:

```text
ModuleNotFoundError: No module named 'transformers'
```

Document that FlashRAG's `Dataset` shape is compatible but full `get_dataset` requires dependencies not installed in this phase.

- [ ] **Step 3: Write baseline and architecture docs**

`docs/baseline/flashrag-baseline.md` must include:

- upstream URL
- commit SHA
- license
- clone path
- dependency import result
- files inspected
- decision not to vendor upstream code

`docs/architecture-flashrag.md` must include:

- `flashrag.dataset.dataset.Item`
- `flashrag.dataset.dataset.Dataset`
- `flashrag.utils.get_dataset`
- `flashrag.config.Config`
- `flashrag.evaluator.Evaluator`
- the `data_dir/<dataset_name>/<split>.jsonl` convention
- the DomainRAG `fresh_hard_test.jsonl` to FlashRAG `fresh_hard.jsonl` mapping

- [ ] **Step 4: Verify and commit**

Run:

```bash
pytest
git status --short
git add .gitignore docs/baseline/flashrag-baseline.md docs/architecture-flashrag.md docs/superpowers/specs/2026-06-27-domainrag-phase-2a-flashrag-intake-design.md docs/superpowers/plans/2026-06-27-domainrag-phase-2a-flashrag-intake-implementation.md
git commit -m "docs: record flashrag intake design"
```

Expected: `40 passed`, then a commit.

---

### Task 2: FlashRAG Adapter Core

**Files:**
- Create: `benchmark/domainrag/flashrag_adapter.py`
- Create: `tests/test_flashrag_adapter.py`

**Interfaces:**
- Consumes: `domainrag.validator.validate_dataset(dataset_dir: Path) -> None`
- Produces: `FlashRAGBundle`
- Produces: `prepare_flashrag_bundle(dataset_dir: Path, output_dir: Path, dataset_name: str | None = None, splits: tuple[str, ...] = ("dev", "test", "fresh_hard")) -> FlashRAGBundle`

- [ ] **Step 1: Write failing adapter tests**

Create `tests/test_flashrag_adapter.py` with tests that assert:

- `prepare_flashrag_bundle(Path("data/example_domain"), tmp_path / "flashrag")` creates `tmp_path/flashrag/example_domain/dev.jsonl`.
- It creates `test.jsonl`.
- It creates `fresh_hard.jsonl` from `fresh_hard_test.jsonl`.
- It copies `corpus.jsonl`.
- It copies `qrels/dev.tsv`, `qrels/test.tsv`, and `qrels/fresh_hard.tsv`.
- It writes `example_domain_flashrag.yaml`.
- The YAML text contains `data_dir:`, `dataset_name: example_domain`, and `split:` entries for `dev`, `test`, and `fresh_hard`.
- Invalid fixture `data/invalid_fixtures/missing_qrels` raises `ValidationError`.

Run:

```bash
pytest tests/test_flashrag_adapter.py -q
```

Expected: fail because `domainrag.flashrag_adapter` does not exist.

- [ ] **Step 2: Implement adapter**

Implement deterministic copy and YAML writing in `benchmark/domainrag/flashrag_adapter.py`.

Use this split mapping:

```python
DOMAINRAG_TO_FLASHRAG_SPLIT_FILES = {
    "dev": ("dev.jsonl", "dev.jsonl"),
    "test": ("test.jsonl", "test.jsonl"),
    "fresh_hard": ("fresh_hard_test.jsonl", "fresh_hard.jsonl"),
}
```

Use `shutil.copy2` for files and remove any existing target dataset directory before writing it.

- [ ] **Step 3: Verify and commit**

Run:

```bash
pytest tests/test_flashrag_adapter.py -q
pytest
git add benchmark/domainrag/flashrag_adapter.py tests/test_flashrag_adapter.py
git commit -m "feat: add flashrag dataset adapter"
```

Expected: adapter tests pass and full suite passes.

---

### Task 3: CLI, Script, And Example Config

**Files:**
- Modify: `benchmark/domainrag/cli.py`
- Modify: `tests/test_cli.py`
- Create: `scripts/prepare_flashrag_example.py`
- Create: `configs/flashrag/example_domain.yaml`

**Interfaces:**
- Consumes: `prepare_flashrag_bundle`
- Produces CLI command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/example_domain --output outputs/flashrag --dataset-name example_domain
```

- [ ] **Step 1: Write failing CLI tests**

Add tests that run the CLI in a subprocess and assert:

- success command exits `0`
- stdout contains `FlashRAG bundle written to`
- generated `fresh_hard.jsonl` exists
- invalid fixture exits non-zero

Run:

```bash
pytest tests/test_cli.py -q
```

Expected: fail because `prepare-flashrag` is not implemented.

- [ ] **Step 2: Implement CLI subcommand**

Add `prepare-flashrag` parser with:

- `--dataset`
- `--output`
- `--dataset-name`
- optional `--splits` defaulting to `dev,test,fresh_hard`

On success, print:

```text
FlashRAG bundle written to <dataset_dir>
FlashRAG config written to <config_path>
```

- [ ] **Step 3: Add script wrapper**

Create `scripts/prepare_flashrag_example.py` that imports `prepare_flashrag_bundle`, prepares `data/example_domain` into `outputs/flashrag`, and prints the same two paths.

- [ ] **Step 4: Add stable config**

Create `configs/flashrag/example_domain.yaml` with:

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

- [ ] **Step 5: Verify and commit**

Run:

```bash
pytest tests/test_cli.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/example_domain --output outputs/flashrag --dataset-name example_domain
python scripts/prepare_flashrag_example.py
git add benchmark/domainrag/cli.py tests/test_cli.py scripts/prepare_flashrag_example.py configs/flashrag/example_domain.yaml
git commit -m "feat: add flashrag preparation CLI"
```

Expected: tests pass and commands produce the bundle/config paths.

---

### Task 4: Verification Docs And Final Smoke

**Files:**
- Create: `docs/verification/flashrag-intake.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Phase 2A commands.
- Produces: final verification record and user-facing README update.

- [ ] **Step 1: Run full verification**

Run:

```bash
pytest
python scripts/create_example_domain.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/example_domain --output outputs/flashrag --dataset-name example_domain
python scripts/prepare_flashrag_example.py
git status --short
```

Expected:

- `40+ passed`
- example data is valid
- FlashRAG bundle and config paths are printed
- no unexpected tracked changes except generated outputs selected for commit if intentionally included

- [ ] **Step 2: Write verification docs**

`docs/verification/flashrag-intake.md` must record:

- FlashRAG URL and commit
- dependency import baseline
- commands run
- output paths
- known limitation that full FlashRAG dependencies and live generation are deferred

- [ ] **Step 3: Update README**

Add a short Phase 2A section with the `prepare-flashrag` command and output location.

- [ ] **Step 4: Verify and commit**

Run:

```bash
pytest
git add docs/verification/flashrag-intake.md README.md outputs/flashrag
git commit -m "docs: record flashrag intake verification"
```

Expected: tests pass and verification artifacts are committed.
