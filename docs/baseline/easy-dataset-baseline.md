# Easy Dataset Baseline Intake

Phase: 2B - Easy Dataset Intake + DomainRAG Exporter
Recorded: 2026-06-27T11:38:08Z

## Upstream

- Repository: `https://github.com/ConardLi/easy-dataset.git`
- Local checkout: `dataset-factory/easy-dataset-fork/`
- Commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Latest inspected commit message: `chore: format resolution entries in pnpm-lock.yaml for consistency`
- Version: `1.7.3`
- License: AGPL-3.0 with additional Easy Dataset terms in `LICENSE`

The upstream checkout is intentionally ignored by this repository. DomainRAG-Bench commits adapter code, fixtures, configs, tests, and documentation, not Easy Dataset source.

## Environment

- Node: `v24.18.0`
- npm: `11.16.0`
- Memory at diagnosis: 503 GiB total, 472 GiB available, no swap
- Disk at diagnosis: 249 GiB available under `/root/autodl-tmp`

## Package Scripts

`package.json` exposes:

- `dev`: `prisma db push && next dev -p 1717`
- `build`: `prisma db push && next build`
- `start`: `next start -p 1717`
- `lint`: `next lint`
- `electron-build`: `pnpm clean-dist && pnpm db:template && prisma db push && next build && electron-builder -mwl`

There is no `test` script.

## Baseline Commands

| Command | Result |
| --- | --- |
| `npm install` | Failed: process was killed with Signal 9 in this environment after creating a partial `node_modules/`. |
| `npm test` | Failed: `npm error Missing script: "test"`. |
| `npm run lint` | Failed/non-interactive: `next lint` prompted to configure ESLint (`Strict`, `Base`, `Cancel`). |
| `CI=1 npm run build` | Timed out after 180 seconds during `next build`; `prisma db push` completed and generated Prisma Client first. |

## Build Output Notes

`CI=1 npm run build` reached:

```text
Datasource "db": SQLite database "db.sqlite" at "file:./db.sqlite"
SQLite database db.sqlite created at file:./db.sqlite
Generated Prisma Client (v6.9.0)
Next.js 14.2.29
Creating an optimized production build ...
```

The command timed out at the optimized production build stage. This is recorded as an upstream baseline/environment limitation, not a DomainRAG exporter failure.

## Architecture Entry Points

| Concern | Files |
| --- | --- |
| Provider registry | `lib/db/llm-providers.js` |
| OpenAI-compatible client | `lib/llm/core/providers/openai.js` |
| Provider dispatch | `lib/llm/core/index.js` |
| Model list fetch | `app/api/llm/fetch-models/route.js` |
| Text splitting API | `app/api/projects/[projectId]/split/route.js` |
| Text splitting implementation | `lib/file/text-splitter.js` |
| Question generation API | `app/api/projects/[projectId]/generate-questions/route.js` |
| Question generation service | `lib/services/questions/index.js` |
| Dataset export API | `app/api/projects/[projectId]/datasets/export/route.js` |
| Eval dataset export API | `app/api/projects/[projectId]/eval-datasets/export/route.js` |
| Prisma schema | `prisma/schema.prisma` |

## DeepSeek Notes

Official DeepSeek API docs were checked on 2026-06-27. The OpenAI-compatible base URL is `https://api.deepseek.com`. Current model names include `deepseek-v4-flash` and `deepseek-v4-pro`; `deepseek-chat` and `deepseek-reasoner` are documented as deprecated on 2026-07-24 15:59 UTC.

Phase 2B does not call DeepSeek. Config examples must reference `DEEPSEEK_API_KEY` but must not contain an API key.
