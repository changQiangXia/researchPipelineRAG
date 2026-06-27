# DomainRAG-Bench Phase 2C Easy Dataset Export Route Design

Created: 2026-06-27T17:33:12Z

## Goal

Add DomainRAG-owned integration assets that an Easy Dataset fork can copy into its Next.js app to emit the enriched Phase 2B export contract:

```text
chunks.jsonl
items.jsonl
```

The emitted files must be consumable by:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input <export_dir> \
  --output outputs/domainrag \
  --dataset-name <name>
```

## Scope

Phase 2C includes:

1. A documented integration package under `integrations/easy-dataset/domainrag-export/`.
2. A copyable Easy Dataset helper module at `files/lib/domainrag/exporter.js`.
3. A copyable Easy Dataset API route at `files/app/api/projects/[projectId]/domainrag-export/route.js`.
4. Tests that verify the integration assets exist, are syntactically valid JavaScript, do not contain secrets, and emit the expected file payload shape.
5. README updates documenting how to copy the assets into an Easy Dataset fork and how to materialize `chunks.jsonl` / `items.jsonl`.

Phase 2C does not include:

1. Vendoring Easy Dataset into this repository.
2. Committing modified upstream Easy Dataset source.
3. Adding a full Easy Dataset UI button.
4. Adding schema migrations to Easy Dataset.
5. Calling DeepSeek or any other live model API.
6. Running Easy Dataset's full production build as a required gate in this environment.

## Context

The inspected Easy Dataset upstream checkout is:

- Repository: `https://github.com/ConardLi/easy-dataset.git`
- Commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Version: `1.7.3`
- License: AGPL-3.0 with additional terms

Relevant upstream paths:

- Existing eval export route: `app/api/projects/[projectId]/eval-datasets/export/route.js`
- Eval dataset DB helpers: `lib/db/evalDatasets.js`
- Chunk DB helpers: `lib/db/chunks.js`
- Prisma models: `Chunks` and `EvalDatasets` in `prisma/schema.prisma`

`EvalDatasets` stores one optional `chunkId`. DomainRAG qrels therefore use that chunk as the source evidence for each exported question. Domain-specific fields that Easy Dataset does not store natively are supplied through request defaults, per-item overrides, or lightweight tags.

## Approaches Considered

### Recommended: Copyable Route And Pure Helper

Commit a pure helper plus a Next.js route as DomainRAG-owned integration assets. The helper converts Easy Dataset eval rows with included chunk records into two JSONL payloads. The route queries Easy Dataset's Prisma client and returns a JSON response containing named file contents.

Pros:

- No vendored upstream source.
- No Easy Dataset schema migration.
- Testable from this Python repository with static checks and a Node helper smoke test.
- Directly matches Phase 2B's enriched file contract.

Cons:

- User must copy two files into an Easy Dataset fork.
- The initial response is a JSON envelope containing two file contents, not a zip download.

### Alternative: Patch File Against Easy Dataset

Commit a git patch that adds the route directly to Easy Dataset.

Pros:

- Easier for a fork maintainer to apply with `git apply`.

Cons:

- More brittle when upstream shifts.
- Harder to review the actual route/helper files in this repository.

### Alternative: DomainRAG Python Directly Reads Easy Dataset SQLite

Add a Python intake that opens Easy Dataset's SQLite database.

Pros:

- No Easy Dataset app changes.

Cons:

- Couples DomainRAG-Bench to Easy Dataset internal schema and local storage paths.
- Harder to use against remote deployments.
- Less aligned with the explicit Phase 2C goal of adding an Easy Dataset export entry point.

## Approved Design

Use the recommended copyable route and pure helper.

The repository will contain:

```text
integrations/easy-dataset/domainrag-export/
  README.md
  files/
    app/api/projects/[projectId]/domainrag-export/route.js
    lib/domainrag/exporter.js
```

Consumers copy `files/` into an Easy Dataset fork root. The new route is:

```text
POST /api/projects/:projectId/domainrag-export
GET  /api/projects/:projectId/domainrag-export
```

`GET` returns a small preview: total compatible rows and route metadata.

`POST` returns:

```json
{
  "files": [
    {"path": "chunks.jsonl", "content": "..."},
    {"path": "items.jsonl", "content": "..."}
  ],
  "statistics": {
    "chunk_count": 3,
    "item_count": 3,
    "split_counts": {"dev": 1, "test": 1, "fresh_hard": 1}
  }
}
```

This envelope avoids adding a zip dependency to Easy Dataset. The README shows how to write each file from the response.

## Request Contract

`POST` accepts optional JSON:

```json
{
  "questionTypes": ["single_choice", "multiple_choice", "short_answer", "open_ended", "fill_blank"],
  "tags": ["domainrag"],
  "keyword": "",
  "splits": {
    "dev": ["eval-id-1"],
    "test": ["eval-id-2"],
    "fresh_hard": ["eval-id-3"]
  },
  "defaults": {
    "subdomain": "general",
    "knowledge_type": "fact",
    "difficulty": "medium",
    "quality_score": 1.0
  },
  "itemOverrides": {
    "eval-id-1": {
      "subdomain": "oxidation",
      "knowledge_type": "mechanism",
      "difficulty": "easy",
      "quality_score": 0.96,
      "answer_aliases": [],
      "required_points": []
    }
  }
}
```

If `splits` does not mention an item, the helper checks tags for `split:dev`, `split:test`, or `split:fresh_hard`. If no split is found, it assigns rows deterministically in item order while ensuring all three required splits are present when at least three compatible items exist.

Metadata precedence:

1. `itemOverrides[item.id]`
2. Tags such as `subdomain:oxidation`, `knowledge:mechanism`, `difficulty:hard`, `quality:0.96`
3. `defaults`

## Mapping

`Chunks` rows map to `chunks.jsonl`:

```json
{
  "id": "chunk-id",
  "name": "chunk name",
  "content": "chunk content",
  "metadata": {
    "fileName": "source.md"
  }
}
```

Only chunks referenced by exported items are included.

`EvalDatasets` rows map to `items.jsonl`:

```json
{
  "id": "eval-id",
  "split": "dev",
  "question_type": "single_choice",
  "question": "Question text?",
  "options": {"A": "first", "B": "second", "C": "third", "D": "fourth"},
  "answer": ["A"],
  "answer_aliases": [],
  "reference_answer": "A",
  "required_points": [],
  "source_chunk_ids": ["chunk-id"],
  "subdomain": "general",
  "knowledge_type": "fact",
  "difficulty": "medium",
  "quality_score": 1.0
}
```

Question type mapping:

- `single_choice` to `single_choice`
- `multiple_choice` to `multiple_choice`
- `short_answer` to `short_answer`
- `open_ended` to `short_answer`
- `fill_blank` to `fill_blank`
- `true_false` is skipped because DomainRAG does not currently support two-option true/false items.

Choice options are parsed from Easy Dataset's JSON string array and converted to letter-keyed objects.

Answers are normalized to arrays. JSON string answers are parsed when possible.

## Error Handling

The helper returns skipped item diagnostics for rows that cannot be exported:

- Missing `chunkId` or missing included chunk content.
- Unsupported question type.
- Invalid choice options.
- Invalid multiple-choice answer count.
- Missing answer aliases for fill-blank items.
- Missing required points for short-answer items.

The route returns HTTP 400 when no compatible exportable items remain or when the final bundle lacks required split coverage.

## Security And Privacy

The integration assets must not contain API keys, GitHub tokens, DeepSeek keys, or hard-coded auth headers.

The route only exports fields needed for the Phase 2B enriched contract. It does not export DOI, authors, venue, page number, original PDF path, or original paper title.

## Testing

Required tests:

1. Integration README and copyable files exist at the documented paths.
2. The route references the expected Easy Dataset target paths and imports the helper.
3. The helper exports `buildDomainRAGBundle`.
4. Node can parse the helper and route assets with `node --check`.
5. A Node smoke test calls the pure helper on representative Easy Dataset-like rows and observes named `chunks.jsonl` / `items.jsonl` payloads.
6. The materialized helper output can be consumed by the existing `export_domainrag_bundle()` adapter and passes `validate_dataset()`.
7. Integration assets do not contain token-like secrets or literal API keys.

## Verification

Phase 2C verification must include:

```bash
pytest
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
git status --short
```

Full Easy Dataset app build is not a completion gate because Phase 2B recorded upstream build limitations in this environment.

## Risks

1. Easy Dataset has no native `split`, `difficulty`, `knowledge_type`, or `quality_score` columns for eval rows. Request overrides and tags are therefore part of the export contract.
2. Returning a JSON envelope is less ergonomic than a zip download. The upside is zero extra app dependency and simple inspectability.
3. `true_false` and some `open_ended` questions may not satisfy DomainRAG's current typed-answer contract. The helper skips unsupported rows and reports diagnostics.
4. Easy Dataset is AGPL-3.0. Copying the assets into a fork modifies that fork and should be handled under the fork owner's license/compliance process.
