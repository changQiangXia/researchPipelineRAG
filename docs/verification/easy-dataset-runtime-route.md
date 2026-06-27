# Easy Dataset Runtime Route Verification

Phase: 2E - Easy Dataset runtime route verification
Recorded: 2026-06-27T18:36:00Z

## Scope

This verification runs the copied DomainRAG export route inside a real Easy Dataset Next.js dev server. It uses Easy Dataset's Prisma-backed SQLite database, calls the route over HTTP, materializes the route response into `chunks.jsonl` and `items.jsonl`, then converts and validates the result with DomainRAG-Bench.

It does not call DeepSeek or any other live model provider. It does not commit Easy Dataset source, dependency folders, generated SQLite files, route outputs, or API keys into this repository.

## Upstream

- Repository: `https://github.com/ConardLi/easy-dataset.git`
- Local ignored checkout: `dataset-factory/easy-dataset-fork/`
- Commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Version: `easy-dataset 1.7.3`
- Next.js: `14.2.29`
- Prisma: `6.9.0`
- Package manager used for this run: `pnpm 11.9.0`

The checkout is ignored by:

```text
.gitignore:7:dataset-factory/easy-dataset-fork/
```

## Runtime Boundary

The active container cgroup still limits memory to 2GiB:

```text
/sys/fs/cgroup/memory.max=2147483648
/sys/fs/cgroup/memory.swap.max=0
```

Earlier `npm install` attempts were killed with Signal 9 under this limit. For this runtime verification, dependency installation succeeded by using `pnpm` with low concurrency:

```bash
corepack enable
corepack prepare pnpm@latest --activate
pnpm install --frozen-lockfile --ignore-scripts --child-concurrency=1 --network-concurrency=1
```

Result:

```text
Done in 8m 52.3s using pnpm v11.9.0
```

The generated `node_modules` directory was about 1.7GiB. The cgroup limit is therefore important for reproducibility and deployment sizing, but it is no longer a blocker for local route verification in this environment.

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

Syntax checks:

```bash
node --check dataset-factory/easy-dataset-fork/lib/domainrag/exporter.js
node --check 'dataset-factory/easy-dataset-fork/app/api/projects/[projectId]/domainrag-export/route.js'
```

Result: both files parsed successfully.

## Database Setup

The Easy Dataset Prisma schema was pushed into the local SQLite database:

```bash
pnpm exec prisma db push
```

Result:

```text
SQLite database "db.sqlite" at "file:./db.sqlite"
Generated Prisma Client (v6.9.0)
```

The database was seeded through Prisma Client with actual Easy Dataset rows:

```json
{
  "projectId": "domainrag_smoke",
  "projects": 1,
  "chunks": 3,
  "evalDatasets": 3
}
```

Seeded question coverage:

- `ed_runtime_q_001`: `single_choice`, split `dev`
- `ed_runtime_q_002`: `fill_blank`, split `test`
- `ed_runtime_q_003`: `open_ended`, mapped to DomainRAG `short_answer`, split `fresh_hard`

## HTTP Route Verification

Easy Dataset was started with:

```bash
pnpm run dev
```

Server log:

```text
Next.js 14.2.29
Local: http://localhost:1717
Ready in 7.5s
Compiled /api/projects/[projectId]/domainrag-export in 8s
GET /api/projects/domainrag_smoke/domainrag-export 200 in 16696ms
POST /api/projects/domainrag_smoke/domainrag-export 200 in 603ms
```

The route availability check used:

```bash
curl -fsS http://127.0.0.1:1717/api/projects/domainrag_smoke/domainrag-export
```

Result:

```json
{
  "route": "domainrag-export",
  "contract": [
    "chunks.jsonl",
    "items.jsonl"
  ],
  "compatible_rows_with_chunk": 3
}
```

The real export used:

```bash
curl -fsS -X POST http://127.0.0.1:1717/api/projects/domainrag_smoke/domainrag-export \
  -H 'Content-Type: application/json' \
  -d '{"defaults":{"subdomain":"general","knowledge_type":"fact","difficulty":"easy","quality_score":0.95},"itemOverrides":{"ed_runtime_q_002":{"answer_aliases":["applied stress"]},"ed_runtime_q_003":{"required_points":["fine precipitates","impede dislocation motion","improve high-temperature strength"]}}}'
```

Route response summary:

```json
{
  "statistics": {
    "chunk_count": 3,
    "item_count": 3,
    "split_counts": {
      "dev": 1,
      "fresh_hard": 1,
      "test": 1
    }
  },
  "skipped": [],
  "errors": []
}
```

The response contained two file payloads:

```text
chunks.jsonl
items.jsonl
```

Those payloads were materialized to:

```text
/tmp/easy-dataset-route-export/chunks.jsonl
/tmp/easy-dataset-route-export/items.jsonl
```

Both files contained three JSONL rows.

## DomainRAG Round Trip

The runtime route output was converted with:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input /tmp/easy-dataset-route-export \
  --output /tmp/easy-dataset-route-domainrag \
  --dataset-name easy_dataset_route_runtime
```

Result:

```text
DomainRAG dataset written to /tmp/easy-dataset-route-domainrag/easy_dataset_route_runtime
```

Validation:

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset /tmp/easy-dataset-route-domainrag/easy_dataset_route_runtime
```

Result:

```text
/tmp/easy-dataset-route-domainrag/easy_dataset_route_runtime is valid
```

Generated statistics:

```json
{
  "corpus_count": 3,
  "dataset_name": "easy_dataset_route_runtime",
  "difficulty_counts": {
    "easy": 1,
    "hard": 1,
    "medium": 1
  },
  "question_count": 3,
  "question_type_counts": {
    "fill_blank": 1,
    "short_answer": 1,
    "single_choice": 1
  },
  "required_splits": [
    "dev",
    "fresh_hard",
    "test"
  ],
  "split_counts": {
    "dev": 1,
    "fresh_hard": 1,
    "test": 1
  }
}
```

## Conclusion

The Phase 2C/2D copyable Easy Dataset assets now pass a real runtime route check inside Easy Dataset 1.7.3:

1. Dependencies installed under the 2GiB cgroup by using `pnpm` low concurrency.
2. Prisma created the real local SQLite schema and generated Prisma Client.
3. Actual Easy Dataset database rows were seeded.
4. The Next.js route responded over HTTP with 200 for both `GET` and `POST`.
5. The exported files were accepted by DomainRAG-Bench and passed `validate-data`.

The next milestone should use a small real-paper pilot instead of adding more synthetic smoke fixtures.
