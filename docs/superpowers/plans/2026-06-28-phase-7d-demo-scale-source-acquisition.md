# Phase 7D Demo-Scale Source Acquisition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reproducible, tested source-acquisition checkpoint that moves the project toward the RAG.md 100-180 paper / 1,000+ chunk demo-scale requirement without claiming final manual verification.

**Architecture:** Add a small `domainrag.source_acquisition` module that normalizes OpenAlex work metadata into a project-owned candidate manifest, scores coverage by subtopic/year/type/access, and writes JSON/Markdown evidence. Add a CLI command and a script wrapper so the same workflow can run in tests with sample payloads and live against OpenAlex for committed Phase 7D outputs.

**Tech Stack:** Python 3.10 standard library (`urllib`, `json`, `dataclasses`, `collections`), existing DomainRAG CLI/test patterns, OpenAlex Works API public metadata.

## Global Constraints

- Do not call live DeepSeek APIs in tests.
- Do not store API keys in code, configs, logs, or generated outputs.
- Treat OpenAlex results as candidate metadata; final inclusion still needs manual source/venue/full-text verification.
- Public benchmark datasets must not export paper title, author, DOI, venue, page, or original PDF path metadata.
- Keep Phase 7D outputs separate from public `corpus.jsonl` and question split files.

---

### Task 1: Source Acquisition Core

**Files:**
- Create: `benchmark/domainrag/source_acquisition.py`
- Test: `tests/test_source_acquisition.py`

**Interfaces:**
- Produces: `normalize_openalex_work(work: dict, *, subtopic: str, query: str) -> dict | None`
- Produces: `build_acquisition_outputs(raw_records: list[dict], *, output_dir: Path) -> tuple[Path, Path, Path]`

- [x] **Step 1: Write failing tests**

```python
def test_normalize_openalex_work_keeps_verified_candidate_fields():
    work = {
        "id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1234/example",
        "display_name": "High-temperature oxidation of a nickel superalloy",
        "publication_year": 2025,
        "type": "article",
        "primary_location": {
            "landing_page_url": "https://publisher.example/work",
            "source": {"display_name": "npj Materials Degradation", "type": "journal"},
            "is_oa": True,
        },
        "open_access": {"is_oa": True, "oa_url": "https://publisher.example/pdf"},
    }

    row = normalize_openalex_work(work, subtopic="oxidation", query="nickel superalloy oxidation")

    assert row["verification_status"] == "candidate_openalex_verified"
    assert row["subtopic"] == "oxidation"
    assert row["year"] == 2025
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_source_acquisition.py -q`

Expected: FAIL because `domainrag.source_acquisition` does not exist.

- [x] **Step 3: Implement minimal core**

Create normalization, dedupe, coverage summary, and JSON/Markdown writers.

- [x] **Step 4: Verify GREEN**

Run: `PYTHONPATH=benchmark pytest tests/test_source_acquisition.py -q`

Expected: PASS.

### Task 2: CLI And Script Wrapper

**Files:**
- Modify: `benchmark/domainrag/cli.py`
- Create: `scripts/acquire_demo_scale_sources.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `build_acquisition_outputs`
- Produces CLI command: `domainrag acquire-sources --output ... --per-query ... --dry-run`

- [x] **Step 1: Write failing CLI tests**

Add a test that `scripts/acquire_demo_scale_sources.py --dry-run --per-query 3` prints OpenAlex query URLs and does not include secrets.

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_cli.py -k acquire_sources -q`

Expected: FAIL because command/script does not exist.

- [x] **Step 3: Implement CLI and script**

Expose dry-run URL generation and live OpenAlex fetch. Use no API keys.

- [x] **Step 4: Verify GREEN**

Run: `PYTHONPATH=benchmark pytest tests/test_cli.py -k acquire_sources -q`

Expected: PASS.

### Task 3: Phase 7D Live Candidate Output

**Files:**
- Create: `outputs/phase7d/demo_scale_source_acquisition/candidates.jsonl`
- Create: `outputs/phase7d/demo_scale_source_acquisition/coverage.json`
- Create: `outputs/phase7d/demo_scale_source_acquisition/summary.md`
- Create: `docs/verification/demo-scale-source-acquisition.md`
- Modify: `docs/reports/rag-md-implementation-audit.json`
- Modify: `docs/reports/domainrag-medium-pilot-final-report.md`
- Test: `tests/test_phase7d_outputs.py`

**Interfaces:**
- Consumes: live OpenAlex Works API response
- Produces: candidate source pool and coverage evidence

- [x] **Step 1: Write failing output tests**

Assert the Phase 7D candidate output has real rows, covers at least five subtopics, records candidate status, and keeps demo scale partial.

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_phase7d_outputs.py -q`

Expected: FAIL because outputs and docs do not exist.

- [x] **Step 3: Run live acquisition**

Run: `PYTHONPATH=benchmark python scripts/acquire_demo_scale_sources.py --output outputs/phase7d/demo_scale_source_acquisition --per-query 15`

- [x] **Step 4: Update docs and audit**

Record candidate counts, coverage, verification limits, and next gate.

- [x] **Step 5: Verify GREEN and full suite**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_source_acquisition.py tests/test_phase7d_outputs.py -q
PYTHONPATH=benchmark pytest
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures pyproject.toml || true
git diff --check
```

Expected: PASS / no secret matches / clean diff.

## Self-Review

- Spec coverage: covers RAG.md source screening, coverage matrix, verification status, and scale-gap honesty.
- Placeholder scan: no TODO/TBD placeholders.
- Type consistency: module and CLI names are fixed above and reused in tests.
