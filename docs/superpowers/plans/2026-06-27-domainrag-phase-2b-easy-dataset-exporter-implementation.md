# DomainRAG-Bench Phase 2B Easy Dataset Exporter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested Easy Dataset intake and DomainRAG exporter path that converts an Easy Dataset-style export fixture into the existing DomainRAG canonical dataset contract.

**Architecture:** Keep Easy Dataset as an ignored local upstream checkout used only for intake. Commit DomainRAG-owned Python adapter code under `benchmark/domainrag`, source fixtures under `fixtures/easy_dataset`, example config under `configs/easy_dataset`, script wrappers, docs, and tests. The exporter validates an enriched Easy Dataset file bundle, writes the existing DomainRAG public data contract, and runs the existing validator before returning success.

**Tech Stack:** Python 3.10+, pytest, standard-library pathlib/shutil/dataclasses/json/collections/argparse. Easy Dataset intake is Next.js/Prisma/npm documentation only. No live APIs and no API keys.

## Global Constraints

- Do not vendor Easy Dataset upstream source into this repository.
- Keep `dataset-factory/easy-dataset-fork/` ignored.
- Do not call live DeepSeek APIs in tests.
- Do not store API keys in code, configs, logs, generated outputs, or Git remotes.
- Preserve the existing DomainRAG data contract documented in `docs/data-contract.md`.
- Use `DEEPSEEK_API_KEY` only as an environment-variable name.
- Exported public artifacts must not contain DOI, author/authors, venue, page/page_number, original PDF path, or original paper title fields.
- Run `pytest` before claiming completion.

---

### Task 1: Intake Docs And Config Example

**Files:**
- Create: `docs/baseline/easy-dataset-baseline.md`
- Create: `docs/architecture-easy-dataset.md`
- Create: `configs/easy_dataset/deepseek.example.json`
- Modify: `.gitignore`

**Interfaces:**
- Produces baseline evidence used by later reviews.
- Produces a DeepSeek config example with `api_key_env`, not a key.

- [ ] **Step 1: Confirm ignored checkout**

Run:

```bash
git check-ignore -v dataset-factory/easy-dataset-fork/README.md
```

Expected: `.gitignore` rule for `dataset-factory/easy-dataset-fork/`.

- [ ] **Step 2: Record upstream metadata**

Run:

```bash
git -C dataset-factory/easy-dataset-fork rev-parse HEAD
git -C dataset-factory/easy-dataset-fork remote -v
node -e "const p=require('./dataset-factory/easy-dataset-fork/package.json'); console.log(p.name, p.version)"
```

Expected:

```text
4002b09d9c5726cafb9f61a8d12765cb96a2d94b
easy-dataset 1.7.3
```

- [ ] **Step 3: Write baseline docs**

Create `docs/baseline/easy-dataset-baseline.md` with:

```markdown
# Easy Dataset Baseline Intake

Phase: 2B - Easy Dataset Intake + DomainRAG Exporter
Recorded: 2026-06-27T11:38:08Z

## Upstream

- Repository: `https://github.com/ConardLi/easy-dataset.git`
- Local checkout: `dataset-factory/easy-dataset-fork/`
- Commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Version: `1.7.3`
- License: AGPL-3.0 with additional Easy Dataset terms.

## Baseline Commands

| Command | Result |
| --- | --- |
| `npm install` | Failed: process killed with Signal 9 in this environment after creating partial `node_modules/`. |
| `npm test` | Failed: package has no `test` script. |
| `npm run lint` | Failed/non-interactive: `next lint` prompted to configure ESLint. |
| `CI=1 npm run build` | Timed out after 180 seconds during `next build`; `prisma db push` completed first. |

## Environment

- Node: `v24.18.0`
- npm: `11.16.0`
- Available memory at diagnosis: 472 GiB available, no swap.
- Disk at diagnosis: 249 GiB available under `/root/autodl-tmp`.

## Notes

The baseline failures are upstream/environment facts, not DomainRAG exporter failures. Phase 2B does not modify Easy Dataset source.
```

- [ ] **Step 4: Write architecture notes**

Create `docs/architecture-easy-dataset.md` documenting:

```markdown
# Easy Dataset Architecture Notes For DomainRAG

## Intake Summary

Easy Dataset is a Next.js 14 and Prisma application. It stores chunks, questions, generated QA datasets, evaluation datasets, model provider config, and task metadata in SQLite through Prisma.

## Relevant Components

| Concern | Files |
| --- | --- |
| Provider registry | `lib/db/llm-providers.js` |
| OpenAI-compatible client | `lib/llm/core/providers/openai.js` |
| Provider dispatch | `lib/llm/core/index.js` |
| Text splitting API | `app/api/projects/[projectId]/split/route.js` |
| Text splitting implementation | `lib/file/text-splitter.js` |
| Question generation API | `app/api/projects/[projectId]/generate-questions/route.js` |
| Question generation service | `lib/services/questions/index.js` |
| Dataset export API | `app/api/projects/[projectId]/datasets/export/route.js` |
| Eval dataset export API | `app/api/projects/[projectId]/eval-datasets/export/route.js` |
| Prisma schema | `prisma/schema.prisma` |

## DomainRAG Gap

Existing exports do not include all retrieval provenance required by DomainRAG qrels. The Phase 2B adapter therefore consumes an enriched export contract with `chunks.jsonl` and `items.jsonl`.
```

- [ ] **Step 5: Add DeepSeek config example**

Create `configs/easy_dataset/deepseek.example.json`:

```json
{
  "provider_id": "deepseek",
  "provider_name": "DeepSeek",
  "base_url": "https://api.deepseek.com",
  "api_key_env": "DEEPSEEK_API_KEY",
  "generation_model": "deepseek-v4-pro",
  "review_model": "deepseek-v4-pro",
  "fast_model": "deepseek-v4-flash",
  "timeout_seconds": 120,
  "max_retries": 3
}
```

- [ ] **Step 6: Commit**

Run:

```bash
git add .gitignore docs/baseline/easy-dataset-baseline.md docs/architecture-easy-dataset.md configs/easy_dataset/deepseek.example.json
git commit -m "docs: record easy dataset intake"
```

### Task 2: Easy Dataset Fixture And Exporter Tests

**Files:**
- Create: `fixtures/easy_dataset/example_export/chunks.jsonl`
- Create: `fixtures/easy_dataset/example_export/items.jsonl`
- Create: `tests/test_easy_dataset_adapter.py`

**Interfaces:**
- Produces test input consumed by `export_domainrag_bundle(input_dir: Path, output_dir: Path, dataset_name: str) -> DomainRAGExportBundle`.

- [ ] **Step 1: Create fixture**

Create `fixtures/easy_dataset/example_export/chunks.jsonl` with three chunks:

```jsonl
{"id":"ed_chunk_001","name":"oxidation-part-1","content":"Oxidation\nChromium-rich oxide scales can slow oxygen ingress at high temperature.","metadata":{"original_paper_title":"Hidden source title","doi":"10.0000/hidden"}}
{"id":"ed_chunk_002","name":"creep-part-1","content":"Creep\nCreep rate increases when temperature and applied stress increase together.","metadata":{"authors":["Hidden Author"]}}
{"id":"ed_chunk_003","name":"microstructure-part-1","content":"Microstructure\nFine precipitates impede dislocation motion and improve high-temperature strength.","metadata":{"venue":"Hidden venue"}}
```

Create `fixtures/easy_dataset/example_export/items.jsonl` with one item per split:

```jsonl
{"id":"ed_q_001","split":"dev","question_type":"single_choice","question":"Which feature slows oxygen ingress at high temperature?","options":{"A":"Chromium-rich oxide scales","B":"Cooling fins","C":"Vacuum seals","D":"Random sampling"},"answer":["A"],"answer_aliases":[],"reference_answer":"Chromium-rich oxide scales slow oxygen ingress at high temperature.","required_points":[],"source_chunk_ids":["ed_chunk_001"],"subdomain":"oxidation","knowledge_type":"mechanism","difficulty":"easy","quality_score":0.96,"metadata":{"page_number":12}}
{"id":"ed_q_002","split":"test","question_type":"fill_blank","question":"Creep rate increases when temperature and applied ____ increase together.","options":{},"answer":["stress"],"answer_aliases":["applied stress"],"reference_answer":"stress","required_points":[],"source_chunk_ids":["ed_chunk_002"],"subdomain":"creep","knowledge_type":"condition","difficulty":"medium","quality_score":0.94}
{"id":"ed_q_003","split":"fresh_hard","question_type":"short_answer","question":"Why can fine precipitates improve high-temperature strength?","options":{},"answer":["They impede dislocation motion."],"answer_aliases":[],"reference_answer":"Fine precipitates impede dislocation motion, which improves high-temperature strength.","required_points":["fine precipitates","impede dislocation motion","improve high-temperature strength"],"source_chunk_ids":["ed_chunk_003"],"subdomain":"microstructure","knowledge_type":"mechanism","difficulty":"hard","quality_score":0.97}
```

- [ ] **Step 2: Write failing tests**

Create `tests/test_easy_dataset_adapter.py` with:

```python
from pathlib import Path

import pytest

from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.errors import ValidationError
from domainrag.io_utils import read_jsonl
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "easy_dataset" / "example_export"


def test_export_domainrag_bundle_writes_valid_dataset(tmp_path: Path):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    assert bundle.dataset_name == "example_easy_dataset"
    assert bundle.dataset_dir == tmp_path / "example_easy_dataset"
    assert (bundle.dataset_dir / "corpus.jsonl").exists()
    assert (bundle.dataset_dir / "canonical_dataset.jsonl").exists()
    assert (bundle.dataset_dir / "dev.jsonl").exists()
    assert (bundle.dataset_dir / "test.jsonl").exists()
    assert (bundle.dataset_dir / "fresh_hard_test.jsonl").exists()
    assert (bundle.dataset_dir / "qrels" / "dev.tsv").exists()
    assert (bundle.dataset_dir / "dataset_card.md").exists()
    assert (bundle.dataset_dir / "statistics.json").exists()
    validate_dataset(bundle.dataset_dir)


def test_export_domainrag_bundle_strips_internal_source_metadata(tmp_path: Path):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    public_text = "".join(
        path.read_text(encoding="utf-8")
        for path in [
            bundle.dataset_dir / "corpus.jsonl",
            bundle.dataset_dir / "canonical_dataset.jsonl",
            bundle.dataset_dir / "dev.jsonl",
            bundle.dataset_dir / "test.jsonl",
            bundle.dataset_dir / "fresh_hard_test.jsonl",
        ]
    )
    assert "original_paper_title" not in public_text
    assert "doi" not in public_text
    assert "authors" not in public_text
    assert "venue" not in public_text
    assert "page_number" not in public_text


def test_export_domainrag_bundle_renders_choice_options_in_split_question(tmp_path: Path):
    bundle = export_domainrag_bundle(FIXTURE, tmp_path, "example_easy_dataset")

    dev = read_jsonl(bundle.dataset_dir / "dev.jsonl")

    assert "A. Chromium-rich oxide scales" in dev[0]["question"]
    assert dev[0]["metadata"]["correct_options"] == ["A"]


def test_export_domainrag_bundle_rejects_missing_source_chunk(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "chunks.jsonl").write_text(
        '{"id":"chunk-1","content":"content"}\n',
        encoding="utf-8",
    )
    (source / "items.jsonl").write_text(
        '{"id":"q1","split":"dev","question_type":"single_choice","question":"Q?","options":{"A":"a","B":"b","C":"c","D":"d"},"answer":["A"],"answer_aliases":[],"reference_answer":"a","required_points":[],"source_chunk_ids":["missing"],"subdomain":"demo","knowledge_type":"fact","difficulty":"easy","quality_score":1.0}\n',
        encoding="utf-8",
    )

    with pytest.raises(ValidationError) as exc:
        export_domainrag_bundle(source, tmp_path / "out", "bad")

    assert "source chunk missing not in chunks.jsonl" in str(exc.value)
    assert not (tmp_path / "out" / "bad").exists()
```

- [ ] **Step 3: Verify tests fail**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_adapter.py -q
```

Expected: fail with `ModuleNotFoundError: No module named 'domainrag.easy_dataset_adapter'`.

### Task 3: Exporter Implementation

**Files:**
- Create: `benchmark/domainrag/easy_dataset_adapter.py`

**Interfaces:**
- Consumes: `chunks.jsonl`, `items.jsonl`
- Produces: `DomainRAGExportBundle`
- Produces: `export_domainrag_bundle(input_dir: Path, output_dir: Path, dataset_name: str) -> DomainRAGExportBundle`

- [ ] **Step 1: Implement exporter**

Create `benchmark/domainrag/easy_dataset_adapter.py` with dataclass `DomainRAGExportBundle`, constants for split filenames, source validation helpers, option rendering, qrels writing, statistics, and path overlap validation.

- [ ] **Step 2: Run focused tests**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_adapter.py -q
```

Expected: pass.

- [ ] **Step 3: Run full tests**

Run:

```bash
pytest
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

Run:

```bash
git add benchmark/domainrag/easy_dataset_adapter.py fixtures/easy_dataset/example_export tests/test_easy_dataset_adapter.py
git commit -m "feat: export easy dataset bundle to domainrag"
```

### Task 4: CLI, Script, Generated Example, And Verification Docs

**Files:**
- Modify: `benchmark/domainrag/cli.py`
- Modify: `tests/test_cli.py`
- Create: `scripts/export_easy_dataset_example.py`
- Create: `outputs/domainrag/example_easy_dataset/`
- Create: `docs/verification/easy-dataset-export.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `export_domainrag_bundle()`
- Produces CLI command `export-domainrag`

- [ ] **Step 1: Add failing CLI test**

Append to `tests/test_cli.py`:

```python
def test_export_domainrag_module_entrypoint_writes_valid_dataset(tmp_path: Path):
    fixture = ROOT / "fixtures" / "easy_dataset" / "example_export"
    output = tmp_path / "outputs"

    result = _run_cli(
        "export-domainrag",
        "--input",
        str(fixture),
        "--output",
        str(output),
        "--dataset-name",
        "example_easy_dataset",
    )

    assert result.returncode == 0
    assert "DomainRAG dataset written to" in result.stdout
    assert (output / "example_easy_dataset" / "canonical_dataset.jsonl").exists()
```

- [ ] **Step 2: Verify CLI test fails**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_cli.py::test_export_domainrag_module_entrypoint_writes_valid_dataset -q
```

Expected: fail because `export-domainrag` is not registered.

- [ ] **Step 3: Add CLI subcommand**

Modify `benchmark/domainrag/cli.py` to import `export_domainrag_bundle`, add parser `export-domainrag`, and print:

```text
DomainRAG dataset written to <dataset_dir>
```

- [ ] **Step 4: Add script**

Create `scripts/export_easy_dataset_example.py`:

```python
from pathlib import Path

from domainrag.easy_dataset_adapter import export_domainrag_bundle


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    bundle = export_domainrag_bundle(
        ROOT / "fixtures" / "easy_dataset" / "example_export",
        ROOT / "outputs" / "domainrag",
        "example_easy_dataset",
    )
    print(f"DomainRAG dataset written to {bundle.dataset_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Generate example output**

Run:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
python scripts/export_easy_dataset_example.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
```

Expected: command outputs include `DomainRAG dataset written to` and `is valid`.

- [ ] **Step 6: Write verification doc and README section**

Create `docs/verification/easy-dataset-export.md` with commands and actual outputs. Add a short Chinese README section explaining Phase 2B.

- [ ] **Step 7: Final verification and commit**

Run:

```bash
pytest
python scripts/export_easy_dataset_example.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
git status --short
```

Commit:

```bash
git add benchmark/domainrag/cli.py tests/test_cli.py scripts/export_easy_dataset_example.py outputs/domainrag docs/verification/easy-dataset-export.md README.md
git commit -m "feat: add easy dataset export CLI"
```

## Self-Review

- Spec coverage: The plan covers intake docs, ignored upstream checkout, DeepSeek config without keys, enriched Easy Dataset fixture, exporter, CLI, script, generated output, verification, and README.
- Completeness scan: No unresolved draft markers are allowed in committed docs/code.
- Type consistency: The plan uses `DomainRAGExportBundle` and `export_domainrag_bundle(input_dir, output_dir, dataset_name)` consistently.
