# DomainRAG-Bench Phase 2C Easy Dataset Export Route Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add tested DomainRAG-owned integration assets that an Easy Dataset fork can copy in order to export `chunks.jsonl` and `items.jsonl` for the existing DomainRAG exporter.

**Architecture:** Keep Easy Dataset upstream as an ignored local checkout for reference only. Commit copyable files under `integrations/easy-dataset/domainrag-export/files/`: a pure JavaScript mapper helper and a Next.js API route. Tests validate static file placement, JavaScript syntax, secret hygiene, and a Node helper smoke path that materializes the exported file payload and feeds it into the Python `export_domainrag_bundle()` adapter.

**Tech Stack:** Python 3.10+, pytest, Node.js syntax/runtime smoke test, standard-library JavaScript for Easy Dataset assets, Next.js route conventions, Prisma query through Easy Dataset's existing `db` client.

## Global Constraints

- Do not vendor Easy Dataset upstream source into this repository.
- Keep `dataset-factory/easy-dataset-fork/` ignored and untracked.
- Do not modify or commit files under `dataset-factory/easy-dataset-fork/`.
- Do not call live DeepSeek APIs in tests.
- Do not store API keys in code, configs, logs, generated outputs, or Git remotes.
- Preserve the existing Phase 2B input contract: `chunks.jsonl` and `items.jsonl`.
- Preserve the existing DomainRAG data contract documented in `docs/data-contract.md`.
- Exported public artifacts must not contain DOI, author/authors, venue, page/page_number, original PDF path, or original paper title fields.
- Full Easy Dataset app build is not a required completion gate in this environment.
- Run `pytest` before claiming completion.

---

## File Structure

- Create `tests/test_easy_dataset_integration_assets.py`: verifies the integration package paths, JavaScript syntax, helper behavior, Python exporter compatibility, and secret hygiene.
- Create `integrations/easy-dataset/domainrag-export/files/lib/domainrag/exporter.js`: pure JavaScript mapper from Easy Dataset eval rows with included chunks into the Phase 2B `chunks.jsonl` / `items.jsonl` file payload.
- Create `integrations/easy-dataset/domainrag-export/files/app/api/projects/[projectId]/domainrag-export/route.js`: copyable Next.js route that queries Easy Dataset's Prisma client and returns the helper payload.
- Create `integrations/easy-dataset/domainrag-export/README.md`: copy/install/use instructions for an Easy Dataset fork.
- Modify `README.md`: add Phase 2C usage summary and the no-vendoring boundary.
- Create `docs/verification/easy-dataset-domainrag-export-route.md`: record verification commands and known Easy Dataset build boundary.

---

### Task 1: Red Tests For Integration Assets

**Files:**
- Create: `tests/test_easy_dataset_integration_assets.py`

**Interfaces:**
- Consumes: no Phase 2C production assets yet.
- Produces: failing tests that define the required integration asset behavior.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_easy_dataset_integration_assets.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import textwrap

from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_ROOT = ROOT / "integrations" / "easy-dataset" / "domainrag-export"
README = INTEGRATION_ROOT / "README.md"
HELPER = INTEGRATION_ROOT / "files" / "lib" / "domainrag" / "exporter.js"
ROUTE = (
    INTEGRATION_ROOT
    / "files"
    / "app"
    / "api"
    / "projects"
    / "[projectId]"
    / "domainrag-export"
    / "route.js"
)


def test_easy_dataset_domainrag_integration_assets_exist():
    assert README.exists()
    assert HELPER.exists()
    assert ROUTE.exists()
    readme_text = README.read_text(encoding="utf-8")
    assert "files/lib/domainrag/exporter.js" in readme_text
    assert "files/app/api/projects/[projectId]/domainrag-export/route.js" in readme_text
    assert "chunks.jsonl" in readme_text
    assert "items.jsonl" in readme_text


def test_easy_dataset_domainrag_route_references_helper_and_upstream_patterns():
    route_text = ROUTE.read_text(encoding="utf-8")
    helper_text = HELPER.read_text(encoding="utf-8")

    assert "@/lib/db/index" in route_text
    assert "@/lib/db/evalDatasets" in route_text
    assert "@/lib/domainrag/exporter" in route_text
    assert "export async function POST" in route_text
    assert "export async function GET" in route_text
    assert "buildDomainRAGBundle" in route_text
    assert "export function buildDomainRAGBundle" in helper_text
    assert "chunks.jsonl" in helper_text
    assert "items.jsonl" in helper_text
    assert "source_chunk_ids" in helper_text


def test_easy_dataset_domainrag_assets_parse_as_javascript():
    node = shutil.which("node")
    assert node is not None, "node is required for JavaScript asset syntax checks"

    for path in [HELPER, ROUTE]:
        result = subprocess.run(
            [node, "--check", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr


def test_easy_dataset_domainrag_helper_payload_feeds_python_exporter(
    tmp_path: Path,
):
    node = shutil.which("node")
    assert node is not None, "node is required for JavaScript helper smoke test"

    helper_copy = tmp_path / "exporter.mjs"
    helper_copy.write_text(HELPER.read_text(encoding="utf-8"), encoding="utf-8")
    runner = tmp_path / "run-helper.mjs"
    runner.write_text(
        textwrap.dedent(
            f"""
            import {{ buildDomainRAGBundle }} from {json.dumps(helper_copy.as_uri())};

            const rows = [
              {{
                id: "ed_q_001",
                question: "Which feature slows oxygen ingress at high temperature?",
                questionType: "single_choice",
                options: JSON.stringify([
                  "Chromium-rich oxide scales",
                  "Cooling fins",
                  "Vacuum seals",
                  "Random sampling"
                ]),
                correctAnswer: "A",
                tags: "domainrag,subdomain:oxidation,knowledge:mechanism",
                chunkId: "ed_chunk_001",
                chunks: {{
                  id: "ed_chunk_001",
                  name: "oxidation-part-1",
                  fileName: "hidden-source.md",
                  content: "Oxidation\\nChromium-rich oxide scales can slow oxygen ingress at high temperature."
                }}
              }},
              {{
                id: "ed_q_002",
                question: "Creep rate increases when temperature and applied ____ increase together.",
                questionType: "fill_blank",
                options: "",
                correctAnswer: "stress",
                tags: "domainrag,subdomain:creep,knowledge:condition,difficulty:medium",
                chunkId: "ed_chunk_002",
                chunks: {{
                  id: "ed_chunk_002",
                  name: "creep-part-1",
                  fileName: "hidden-source.md",
                  content: "Creep\\nCreep rate increases when temperature and applied stress increase together."
                }}
              }},
              {{
                id: "ed_q_003",
                question: "Why can fine precipitates improve high-temperature strength?",
                questionType: "open_ended",
                options: "",
                correctAnswer: "Fine precipitates impede dislocation motion.",
                tags: "domainrag,subdomain:microstructure,knowledge:mechanism,difficulty:hard",
                chunkId: "ed_chunk_003",
                chunks: {{
                  id: "ed_chunk_003",
                  name: "microstructure-part-1",
                  fileName: "hidden-source.md",
                  content: "Microstructure\\nFine precipitates impede dislocation motion and improve high-temperature strength."
                }}
              }}
            ];

            const bundle = buildDomainRAGBundle(rows, {{
              splits: {{
                dev: ["ed_q_001"],
                test: ["ed_q_002"],
                fresh_hard: ["ed_q_003"]
              }},
              defaults: {{
                subdomain: "general",
                knowledge_type: "fact",
                difficulty: "easy",
                quality_score: 0.95
              }},
              itemOverrides: {{
                ed_q_002: {{
                  answer_aliases: ["applied stress"]
                }},
                ed_q_003: {{
                  required_points: [
                    "fine precipitates",
                    "impede dislocation motion",
                    "improve high-temperature strength"
                  ]
                }}
              }}
            }});

            console.log(JSON.stringify(bundle));
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [node, str(runner)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    bundle = json.loads(result.stdout)
    assert bundle["errors"] == []
    files = {file["path"]: file["content"] for file in bundle["files"]}
    assert set(files) == {"chunks.jsonl", "items.jsonl"}

    source = tmp_path / "easy-dataset-export"
    source.mkdir()
    for file_name, content in files.items():
        (source / file_name).write_text(content, encoding="utf-8")

    domainrag_bundle = export_domainrag_bundle(source, tmp_path / "outputs", "from_easy_dataset_route")
    validate_dataset(domainrag_bundle.dataset_dir)
    assert bundle["statistics"]["split_counts"] == {
        "dev": 1,
        "fresh_hard": 1,
        "test": 1,
    }


def test_easy_dataset_domainrag_integration_assets_do_not_contain_secrets():
    secret_patterns = [
        re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"(api[_-]?key|authorization)\\s*[:=]\\s*['\\\"][^'\\\"\\n]+", re.IGNORECASE),
    ]
    checked_files = [README, HELPER, ROUTE]
    for path in checked_files:
        text = path.read_text(encoding="utf-8")
        for pattern in secret_patterns:
            assert not pattern.search(text), f"secret-like value found in {path}"
```

- [ ] **Step 2: Run focused test to verify it fails**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_integration_assets.py -q
```

Expected: fail because `README`, `exporter.js`, and `route.js` do not exist yet.

- [ ] **Step 3: Commit the red tests**

Run:

```bash
git add tests/test_easy_dataset_integration_assets.py
git commit -m "test: specify easy dataset domainrag integration assets"
```

---

### Task 2: Copyable Helper And Route Assets

**Files:**
- Create: `integrations/easy-dataset/domainrag-export/files/lib/domainrag/exporter.js`
- Create: `integrations/easy-dataset/domainrag-export/files/app/api/projects/[projectId]/domainrag-export/route.js`
- Create: `integrations/easy-dataset/domainrag-export/README.md`

**Interfaces:**
- Produces: `buildDomainRAGBundle(evalItems: Array<object>, options?: object) -> {files, statistics, skipped, errors}`
- Produces: `GET` and `POST` Easy Dataset route handlers.

- [ ] **Step 1: Create helper implementation**

Create `integrations/easy-dataset/domainrag-export/files/lib/domainrag/exporter.js` with these exported functions:

```javascript
export function buildDomainRAGBundle(evalItems, options = {}) {
  const rows = Array.isArray(evalItems) ? evalItems : [];
  const prepared = [];
  const skipped = [];

  for (const item of rows) {
    const result = normalizeEvalItem(item, options);
    if (result.error) {
      skipped.push({ id: item && item.id ? item.id : null, reason: result.error });
    } else {
      prepared.push(result.item);
    }
  }

  assignFallbackSplits(prepared);
  const errors = validateBundle(prepared);
  if (errors.length > 0) {
    return { files: [], statistics: buildStatistics(prepared), skipped, errors };
  }

  const chunks = buildChunkRecords(prepared);
  return {
    files: [
      { path: "chunks.jsonl", content: toJsonl(chunks) },
      { path: "items.jsonl", content: toJsonl(prepared.map(entry => entry.domainragItem)) }
    ],
    statistics: buildStatistics(prepared),
    skipped,
    errors: []
  };
}
```

The file must also define the helper functions used by `buildDomainRAGBundle`: `normalizeEvalItem`, `normalizeQuestionType`, `normalizeOptions`, `normalizeAnswer`, `extractTags`, `extractTagValue`, `resolveSplit`, `resolveMetadataValue`, `assignFallbackSplits`, `validateBundle`, `buildChunkRecords`, `buildStatistics`, `parseMaybeJson`, `toArray`, and `toJsonl`.

- [ ] **Step 2: Create Next.js route implementation**

Create `integrations/easy-dataset/domainrag-export/files/app/api/projects/[projectId]/domainrag-export/route.js` with:

```javascript
import { NextResponse } from 'next/server';
import { db } from '@/lib/db/index';
import { buildEvalQuestionWhere } from '@/lib/db/evalDatasets';
import { buildDomainRAGBundle } from '@/lib/domainrag/exporter';

export const dynamic = 'force-dynamic';

export async function GET(request, { params }) {
  const { projectId } = params;
  const total = await db.evalDatasets.count({
    where: { projectId, chunkId: { not: null } }
  });
  return NextResponse.json({
    route: 'domainrag-export',
    contract: ['chunks.jsonl', 'items.jsonl'],
    compatible_rows_with_chunk: total
  });
}

export async function POST(request, { params }) {
  try {
    const { projectId } = params;
    const body = await safeJson(request);
    const where = buildEvalQuestionWhere(projectId, {
      questionTypes: Array.isArray(body.questionTypes) ? body.questionTypes : undefined,
      tags: Array.isArray(body.tags) ? body.tags : undefined,
      keyword: body.keyword || undefined
    });
    where.chunkId = { not: null };

    const rows = await db.evalDatasets.findMany({
      where,
      include: {
        chunks: {
          select: {
            id: true,
            name: true,
            fileName: true,
            content: true
          }
        }
      },
      orderBy: { createAt: 'desc' },
      take: Number.isInteger(body.limit) ? Math.min(body.limit, 5000) : 5000
    });

    const bundle = buildDomainRAGBundle(rows, body);
    if (bundle.errors.length > 0) {
      return NextResponse.json(bundle, { status: 400 });
    }
    return NextResponse.json(bundle);
  } catch (error) {
    console.error('Failed to export DomainRAG bundle:', error);
    return NextResponse.json(
      { error: error.message || 'DomainRAG export failed' },
      { status: 500 }
    );
  }
}

async function safeJson(request) {
  try {
    return await request.json();
  } catch {
    return {};
  }
}
```

- [ ] **Step 3: Create integration README**

Create `integrations/easy-dataset/domainrag-export/README.md` with copy instructions, route URL, request example, response shape, and a Python materialization snippet that writes `chunks.jsonl` and `items.jsonl`.

- [ ] **Step 4: Run focused tests**

Run:

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_integration_assets.py -q
```

Expected: all Phase 2C focused tests pass.

- [ ] **Step 5: Commit helper, route, and README**

Run:

```bash
git add integrations/easy-dataset/domainrag-export
git commit -m "feat: add easy dataset domainrag export route assets"
```

---

### Task 3: Documentation And Verification Record

**Files:**
- Modify: `README.md`
- Create: `docs/verification/easy-dataset-domainrag-export-route.md`

**Interfaces:**
- Consumes: Phase 2C integration asset paths.
- Produces: user-facing instructions and verification evidence.

- [ ] **Step 1: Update root README**

Add a `Phase 2C: Easy Dataset DomainRAG 导出入口资产` section that says:

```markdown
## Phase 2C: Easy Dataset DomainRAG 导出入口资产

第三阶段 C 提供 Easy Dataset fork 可复制的导出入口资产，位置在：

```text
integrations/easy-dataset/domainrag-export/
```

把其中 `files/` 下的两个文件复制到 Easy Dataset fork 根目录后，可得到：

- `lib/domainrag/exporter.js`
- `app/api/projects/[projectId]/domainrag-export/route.js`

该路由返回 `chunks.jsonl` 和 `items.jsonl` 的文件内容。将这两个文件写入同一目录后，可继续使用 Phase 2B 的命令转换为 DomainRAG 标准数据集。
```

- [ ] **Step 2: Add verification record**

Create `docs/verification/easy-dataset-domainrag-export-route.md` documenting:

```markdown
# Easy Dataset DomainRAG Export Route Verification

Phase: 2C - Easy Dataset export route assets
Recorded: 2026-06-27T17:33:12Z

## Scope

This verification covers DomainRAG-owned copyable assets under `integrations/easy-dataset/domainrag-export/`. It does not build the full Easy Dataset app in this environment.

## Commands

- `PYTHONPATH=benchmark pytest tests/test_easy_dataset_integration_assets.py -q`
- `pytest`
- `PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset`
- `PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset`

## Notes

The Node helper smoke test materializes the route payload into `chunks.jsonl` and `items.jsonl`, then feeds those files into the existing Python Easy Dataset adapter.
```

- [ ] **Step 3: Run full tests**

Run:

```bash
pytest
```

Expected: all tests pass.

- [ ] **Step 4: Commit docs**

Run:

```bash
git add README.md docs/verification/easy-dataset-domainrag-export-route.md
git commit -m "docs: document easy dataset domainrag export route"
```

---

### Task 4: Final Verification And Push

**Files:**
- No new files unless verification exposes an issue.

**Interfaces:**
- Consumes: all Phase 2C commits.
- Produces: pushed branch for PR or direct review.

- [ ] **Step 1: Run required verification**

Run:

```bash
pytest
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
git status --short --branch
```

Expected:

```text
66+ passed
DomainRAG dataset written to outputs/domainrag/example_easy_dataset
outputs/domainrag/example_easy_dataset is valid
## phase-2c-easy-dataset-export-route
```

- [ ] **Step 2: Push the branch**

Run:

```bash
source /etc/network_turbo
git push -u origin phase-2c-easy-dataset-export-route
```

Expected: branch is pushed to GitHub.

- [ ] **Step 3: Report next plan**

Report:

- branch name
- commits created
- verification commands and outcomes
- next recommended step: create PR, merge after review, then run a real Easy Dataset fork smoke test with a small project export
