# Easy Dataset Fork Smoke Test

Phase: 2D - Easy Dataset fork smoke test
Recorded: 2026-06-27T18:05:18Z

## Scope

This verification checks whether the Phase 2C copyable assets can be placed into a real Easy Dataset fork checkout and whether the fork-side helper can emit files that the DomainRAG-Bench exporter accepts.

It does not call DeepSeek or any other live model provider. It does not commit Easy Dataset source into this repository.

## Upstream

- Repository: `https://github.com/ConardLi/easy-dataset.git`
- Local ignored checkout: `dataset-factory/easy-dataset-fork/`
- Commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Version: `easy-dataset 1.7.3`
- Package manager available in this environment: `npm 11.16.0`
- Node: `v24.18.0`

The checkout is ignored by:

```text
.gitignore:7:dataset-factory/easy-dataset-fork/
```

## Copied Assets

Copied from DomainRAG-Bench:

```text
integrations/easy-dataset/domainrag-export/files/lib/domainrag/exporter.js
integrations/easy-dataset/domainrag-export/files/app/api/projects/[projectId]/domainrag-export/route.js
```

Copied into the Easy Dataset fork:

```text
dataset-factory/easy-dataset-fork/lib/domainrag/exporter.js
dataset-factory/easy-dataset-fork/app/api/projects/[projectId]/domainrag-export/route.js
```

Verification:

```bash
node --check dataset-factory/easy-dataset-fork/lib/domainrag/exporter.js
node --check 'dataset-factory/easy-dataset-fork/app/api/projects/[projectId]/domainrag-export/route.js'
cmp -s integrations/easy-dataset/domainrag-export/files/lib/domainrag/exporter.js dataset-factory/easy-dataset-fork/lib/domainrag/exporter.js
cmp -s 'integrations/easy-dataset/domainrag-export/files/app/api/projects/[projectId]/domainrag-export/route.js' 'dataset-factory/easy-dataset-fork/app/api/projects/[projectId]/domainrag-export/route.js'
```

Result: both copied files parse as JavaScript and match the committed copyable assets.

## Runtime Boundary

The environment reports high host memory, but the active cgroup limit is 2GiB:

```text
/sys/fs/cgroup/memory.max=2147483648
/sys/fs/cgroup/memory.swap.max=0
```

`npm install --ignore-scripts --no-audit --no-fund` was killed with Signal 9. A second attempt with lower heap/socket settings was also killed:

```bash
NODE_OPTIONS=--max-old-space-size=512 npm install --ignore-scripts --no-audit --no-fund --prefer-offline --maxsockets=1
```

Because dependencies were not installed, `npm run dev` failed before Next.js startup:

```text
> easy-dataset@1.7.3 dev
> prisma db push && next dev -p 1717

sh: 1: prisma: not found
```

Conclusion: full Easy Dataset dev server verification is blocked by the current container memory limit, not by the DomainRAG route/helper syntax.

## Fork Helper Smoke

The copied fork helper was imported from:

```text
dataset-factory/easy-dataset-fork/lib/domainrag/exporter.js
```

It was run against three Easy Dataset-like eval rows with included chunks:

- one `single_choice` item for `dev`
- one `fill_blank` item for `test`
- one `open_ended` item mapped to DomainRAG `short_answer` for `fresh_hard`

The helper emitted:

```text
/tmp/domainrag-phase2d-smoke/source/chunks.jsonl
/tmp/domainrag-phase2d-smoke/source/items.jsonl
```

Statistics:

```json
{
  "chunk_count": 3,
  "item_count": 3,
  "split_counts": {
    "dev": 1,
    "fresh_hard": 1,
    "test": 1
  }
}
```

The smoke test exposed a bug where an empty quality tag value was converted with `Number("")`, producing `quality_score: 0`. Phase 2D fixed the helper so blank values are skipped and the request default is preserved. A regression assertion now verifies exported quality scores remain `[0.95, 0.95, 0.95]`.

Direct Node import of `exporter.js` produces a `MODULE_TYPELESS_PACKAGE_JSON` warning because Easy Dataset's package does not declare `"type": "module"`. This is a raw Node warning; the intended route usage is through Next.js bundling.

## DomainRAG Round Trip

The helper output was consumed by DomainRAG-Bench:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input /tmp/domainrag-phase2d-smoke/source \
  --output /tmp/domainrag-phase2d-smoke/domainrag \
  --dataset-name easy_dataset_fork_smoke
```

Result:

```text
DomainRAG dataset written to /tmp/domainrag-phase2d-smoke/domainrag/easy_dataset_fork_smoke
```

Validation:

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset /tmp/domainrag-phase2d-smoke/domainrag/easy_dataset_fork_smoke
```

Result:

```text
/tmp/domainrag-phase2d-smoke/domainrag/easy_dataset_fork_smoke is valid
```

## Final Verification Commands

DomainRAG-Bench verification for the committed changes:

```bash
PYTHONPATH=benchmark pytest tests/test_easy_dataset_integration_assets.py -q
pytest
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
```

## Next Step

Run the same copied route inside an environment with more than 2GiB cgroup memory so Easy Dataset can install dependencies and start its Next.js dev server. Then call the real route:

```text
POST /api/projects/:projectId/domainrag-export
```

The expected route payload is still the two-file envelope documented in `integrations/easy-dataset/domainrag-export/README.md`.
