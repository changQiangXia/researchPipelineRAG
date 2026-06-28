# Phase 7F Source Decisions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a provisional source-decision package from the Phase 7E screening queue and use it as the planned stopping point before full demo-scale chunk/question production.

**Architecture:** Add a focused `domainrag.source_decisions` module that reads the Phase 7E screening queue, assigns conservative provisional decisions, writes a provisional whitelist, and records a review-gap fill plan. The output remains explicitly non-final: it is suitable as a handoff and pause point, not as a claim of full manual publisher-level verification.

**Tech Stack:** Python 3.10 standard library, existing `domainrag.io_utils`, existing CLI/test patterns, committed Phase 7E screening queue.

## Global Constraints

- Do not call live DeepSeek APIs in tests.
- Do not store API keys in code, configs, logs, or generated outputs.
- Treat Phase 7F outputs as provisional source decisions, not final manual source verification.
- Public benchmark datasets must not export paper title, author, DOI, venue, page, or original PDF path metadata.
- Do not start full 1,000+ chunk / 300+ question production in Phase 7F.

---

### Task 1: Source Decisions Core

**Files:**
- Create: `benchmark/domainrag/source_decisions.py`
- Test: `tests/test_source_decisions.py`

**Interfaces:**
- Consumes: Phase 7E screening rows with `screening_priority`, `full_text_queue_status`, `subtopic`, `work_kind`, and candidate metadata.
- Produces: `decide_source(row: dict) -> dict`
- Produces: `summarize_decisions(rows: list[dict]) -> dict`
- Produces: `build_decision_outputs(screening_queue_path: Path, output_dir: Path) -> tuple[Path, Path, Path, Path]`

- [x] **Step 1: Write failing tests**

Require:

```python
accepted = decide_source({"screening_priority": "high", "full_text_queue_status": "ready_for_full_text_download_attempt", ...})
assert accepted["source_decision"] == "accepted_provisional"
assert accepted["decision_status"] == "provisional_not_final"

pending = decide_source({"screening_priority": "low", "full_text_queue_status": "ready_for_full_text_download_attempt", ...})
assert pending["source_decision"] == "pending_manual_review"

rejected = decide_source({"screening_priority": "low", "full_text_queue_status": "needs_access_check", ...})
assert rejected["source_decision"] == "rejected_prescreen"
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_source_decisions.py -q`

Expected: FAIL because `domainrag.source_decisions` does not exist.

- [x] **Step 3: Implement minimal core**

Decision rules:

```python
accepted_provisional = high or medium priority and ready_for_full_text_download_attempt
pending_manual_review = low priority and ready_for_full_text_download_attempt
rejected_prescreen = needs_access_check or missing_access_url rows
```

Every row must keep:

```python
decision_status = "provisional_not_final"
manual_verification_status = {
  "venue_metric": "pending",
  "doi_title_year": "pending",
  "article_type": "pending",
  "retraction": "pending",
  "full_text_processability": "pending",
  "domain_relevance": "pending",
}
```

- [x] **Step 4: Verify GREEN**

Run: `PYTHONPATH=benchmark pytest tests/test_source_decisions.py -q`

Expected: PASS.

### Task 2: CLI And Script Wrapper

**Files:**
- Modify: `benchmark/domainrag/cli.py`
- Create: `scripts/build_phase7f_source_decisions.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `build_decision_outputs(screening_queue_path: Path, output_dir: Path)`
- Produces CLI command: `domainrag decide-sources --screening-queue ... --output ...`

- [x] **Step 1: Write failing CLI tests**

Require:

```python
result = _run_cli(
    "decide-sources",
    "--screening-queue",
    str(queue),
    "--output",
    str(output),
)
assert (output / "source_decisions.jsonl").exists()
assert (output / "provisional_source_whitelist.jsonl").exists()
assert (output / "decision_summary.json").exists()
assert (output / "summary.md").exists()
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_cli.py -k decide_sources -q`

Expected: FAIL because command/script does not exist.

- [x] **Step 3: Implement CLI and wrapper**

Add command:

```bash
PYTHONPATH=benchmark python -m domainrag.cli decide-sources \
  --screening-queue outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl \
  --output outputs/archive/provenance/source-workflow/source-decisions/source_decisions
```

- [x] **Step 4: Verify GREEN**

Run: `PYTHONPATH=benchmark pytest tests/test_cli.py -k decide_sources -q`

Expected: PASS.

### Task 3: Phase 7F Outputs, Audit, And Stopping Point

**Files:**
- Create: `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/source_decisions.jsonl`
- Create: `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/provisional_source_whitelist.jsonl`
- Create: `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/decision_summary.json`
- Create: `outputs/archive/provenance/source-workflow/source-decisions/source_decisions/summary.md`
- Create: `docs/verification/source-decisions-and-stop-point.md`
- Modify: `docs/reports/rag-md-implementation-audit.json`
- Modify: `docs/reports/domainrag-medium-pilot-final-report.md`
- Test: `tests/test_phase7f_outputs.py`
- Test: `tests/test_phase6g_report.py`

**Interfaces:**
- Consumes: committed Phase 7E screening queue
- Produces: committed Phase 7F provisional decisions and stop-point documentation

- [x] **Step 1: Write failing output tests**

Assert:

```python
assert len(decisions) == 124
assert summary["decision_counts"]["accepted_provisional"] == 82
assert summary["decision_counts"]["pending_manual_review"] == 33
assert summary["decision_counts"]["rejected_prescreen"] == 9
assert summary["provisional_whitelist_count"] == 115
assert summary["stop_point_recommendation"] == "pause_after_phase7f"
assert audit["phase"] == "Phase 7F"
assert audit["phase7f_source_decisions"]["verification_status"] == "provisional_not_final"
```

- [x] **Step 2: Verify RED**

Run: `PYTHONPATH=benchmark pytest tests/test_phase7f_outputs.py -q`

Expected: FAIL because outputs/docs do not exist.

- [x] **Step 3: Generate real Phase 7F outputs**

Run:

```bash
PYTHONPATH=benchmark python scripts/build_phase7f_source_decisions.py \
  --screening-queue outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl \
  --output outputs/archive/provenance/source-workflow/source-decisions/source_decisions
```

- [x] **Step 4: Update docs and audit**

Record the stop point and explicitly state that full demo-scale generation is deferred.

- [x] **Step 5: Verify GREEN and full suite**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_source_decisions.py tests/test_phase7f_outputs.py tests/test_cli.py -k 'source_decisions or phase7f or decide_sources' -q
PYTHONPATH=benchmark pytest
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_medium_plus
python -m json.tool docs/reports/rag-md-implementation-audit.json >/tmp/phase7f-audit.json
git diff --check
grep -REn "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9_]+" outputs benchmark scripts tests README.md docs data fixtures pyproject.toml || true
```

Expected: PASS / valid / no secret matches / clean diff.

## Self-Review

- Spec coverage: defines provisional decisions, provisional whitelist, explicit stop point, and preserves the demo-scale gap.
- Placeholder scan: no TODO/TBD placeholders.
- Type consistency: status names, output filenames, command names, and report fields are fixed and reused across all tasks.
