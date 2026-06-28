# Phase 7E Source Screening Queue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the Phase 7D OpenAlex candidate pool into a reproducible source-screening and full-text processing queue without claiming final manual source inclusion.

**Architecture:** Add a focused `domainrag.source_screening` module that reads candidate JSONL rows, assigns deterministic pre-screening priority, records manual verification tasks, summarizes subtopic/review/full-text readiness gaps, and writes JSONL/JSON/Markdown evidence. Add a CLI/script wrapper and Phase 7E report/audit outputs that move the source-whitelist work forward while keeping final accepted sources at zero.

**Tech Stack:** Python 3.10 standard library, existing `domainrag.io_utils`, existing CLI/test patterns, committed Phase 7D OpenAlex candidate metadata.

## Global Constraints

- Do not call live DeepSeek APIs in tests.
- Do not store API keys in code, configs, logs, or generated outputs.
- Treat Phase 7E outputs as machine pre-screening and queue evidence, not final manual source verification.
- Public benchmark datasets must not export paper title, author, DOI, venue, page, or original PDF path metadata.
- Keep Phase 7E outputs separate from public `corpus.jsonl` and question split files.

---

### Task 1: Source Screening Core

**Files:**
- Create: `benchmark/domainrag/source_screening.py`
- Test: `tests/test_source_screening.py`

**Interfaces:**
- Consumes: Phase 7D candidate dictionaries with `source_id`, `doi`, `title`, `year`, `subtopic`, `work_kind`, `venue_whitelist_status`, `open_access`, `oa_url`, `official_url`, and `domain_relevance_terms`.
- Produces: `screen_candidate(candidate: dict) -> dict`
- Produces: `summarize_screening(rows: list[dict]) -> dict`
- Produces: `build_screening_outputs(candidates_path: Path, output_dir: Path) -> tuple[Path, Path, Path]`

- [x] **Step 1: Write failing tests**

Add tests that require:

```python
def test_screen_candidate_records_priority_full_text_and_manual_tasks():
    row = screen_candidate({
        "source_id": "openalex_W1",
        "doi": "10.1234/example",
        "title": "High-temperature oxidation of nickel superalloy",
        "year": 2026,
        "subtopic": "oxidation",
        "work_kind": "research_article_candidate",
        "venue_whitelist_status": "candidate_top_venue_or_domain_flagship",
        "open_access": True,
        "oa_url": "https://publisher.example/paper.pdf",
        "official_url": "https://doi.org/10.1234/example",
        "domain_relevance_terms": ["nickel", "superalloy"],
    })

    assert row["screening_status"] == "needs_manual_verification"
    assert row["screening_priority"] == "high"
    assert row["full_text_status"] == "open_access_full_text_candidate"
    assert row["full_text_queue_status"] == "ready_for_full_text_download_attempt"
    assert row["final_inclusion_status"] == "not_finalized"
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_source_screening.py -q`

Expected: FAIL because `domainrag.source_screening` does not exist.

- [x] **Step 3: Implement minimal core**

Create screening classification with these stable values:

```python
screening_status = "needs_manual_verification"
final_inclusion_status = "not_finalized"
full_text_status in {
    "open_access_full_text_candidate",
    "landing_page_only",
    "missing_access_url",
}
full_text_queue_status in {
    "ready_for_full_text_download_attempt",
    "needs_access_check",
}
screening_priority in {"high", "medium", "low"}
```

Priority rules:

```python
high = top venue candidate and OA URL exists and at least two domain terms
medium = OA URL exists and at least two domain terms
low = everything else that remains candidate-only
```

- [x] **Step 4: Verify GREEN**

Run: `PYTHONPATH=benchmark pytest tests/test_source_screening.py -q`

Expected: PASS.

### Task 2: CLI And Script Wrapper

**Files:**
- Modify: `benchmark/domainrag/cli.py`
- Create: `scripts/screen_phase7d_sources.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `build_screening_outputs(candidates_path: Path, output_dir: Path)`
- Produces CLI command: `domainrag screen-sources --candidates ... --output ...`

- [x] **Step 1: Write failing CLI tests**

Add tests that require:

```python
result = _run_cli(
    "screen-sources",
    "--candidates",
    str(candidates),
    "--output",
    str(output),
)
assert result.returncode == 0
assert (output / "screening_queue.jsonl").exists()
assert (output / "screening_summary.json").exists()
assert (output / "summary.md").exists()
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_cli.py -k screen_sources -q`

Expected: FAIL because the command and wrapper do not exist.

- [x] **Step 3: Implement CLI and wrapper**

Add parser command:

```bash
domainrag screen-sources \
  --candidates outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/candidates.jsonl \
  --output outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue
```

Add script wrapper:

```bash
PYTHONPATH=benchmark python scripts/screen_phase7d_sources.py \
  --candidates outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/candidates.jsonl \
  --output outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue
```

- [x] **Step 4: Verify GREEN**

Run: `PYTHONPATH=benchmark pytest tests/test_cli.py -k screen_sources -q`

Expected: PASS.

### Task 3: Phase 7E Real Queue Outputs And Audit

**Files:**
- Create: `outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl`
- Create: `outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_summary.json`
- Create: `outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/summary.md`
- Create: `docs/verification/source-screening-queue.md`
- Modify: `docs/reports/rag-md-implementation-audit.json`
- Modify: `docs/reports/domainrag-medium-pilot-final-report.md`
- Test: `tests/test_phase7e_outputs.py`
- Test: `tests/test_phase6g_report.py`

**Interfaces:**
- Consumes: committed Phase 7D `candidates.jsonl`
- Produces: committed Phase 7E queue evidence and report/audit update

- [x] **Step 1: Write failing output tests**

Assert:

```python
assert len(queue) == 124
assert summary["candidate_count"] == 124
assert summary["final_included_sources"] == 0
assert summary["full_text_ready_candidates"] >= 100
assert summary["review_gap_subtopics"] == [
    "coatings",
    "life_prediction",
    "microstructure_characterization",
]
assert audit["phase"] == "Phase 7E"
assert audit["phase7e_source_screening_queue"]["verification_status"] == "machine_prescreen_only"
assert requirements["literature_source_policy"]["status"] == "partial"
assert requirements["demo_scale"]["status"] == "partial"
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_phase7e_outputs.py -q`

Expected: FAIL because outputs and docs do not exist.

- [x] **Step 3: Generate real queue outputs**

Run:

```bash
PYTHONPATH=benchmark python scripts/screen_phase7d_sources.py \
  --candidates outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/candidates.jsonl \
  --output outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue
```

- [x] **Step 4: Update docs and audit**

Record the queue counts, review gaps, and limitations. Keep final inclusion partial.

- [x] **Step 5: Verify GREEN and full suite**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_source_screening.py tests/test_phase7e_outputs.py tests/test_cli.py -k 'source_screening or phase7e or screen_sources' -q
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
python -m json.tool docs/reports/rag-md-implementation-audit.json >/tmp/phase7e-audit.json
git diff --check
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures pyproject.toml || true
```

Expected: PASS / valid / no secret matches / clean diff.

## Self-Review

- Spec coverage: converts the Phase 7D source candidates into a practical Phase 7E verification and full-text queue while preserving the RAG.md source-policy gap.
- Placeholder scan: no TODO/TBD placeholders.
- Type consistency: module, CLI, output filenames, status values, and report fields are fixed and reused across all tasks.
