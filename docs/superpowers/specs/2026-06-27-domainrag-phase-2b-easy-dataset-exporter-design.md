# DomainRAG-Bench Phase 2B Easy Dataset Exporter Design

Created: 2026-06-27T11:38:08Z

## Goal

Add a tested Easy Dataset intake and DomainRAG exporter path that can convert an Easy Dataset-derived export bundle into the existing DomainRAG canonical dataset contract without vendoring Easy Dataset source code or calling live model APIs.

## Scope

Phase 2B includes:

1. Local Easy Dataset upstream checkout for intake only at `dataset-factory/easy-dataset-fork/`.
2. Baseline documentation for Easy Dataset URL, commit SHA, license, scripts, dependency status, and key architecture entry points.
3. A committed DomainRAG-owned exporter in `benchmark/domainrag`.
4. A CLI/script path that converts an Easy Dataset-style export fixture into a DomainRAG dataset bundle.
5. A committed fixture that simulates the data fields DomainRAG needs from Easy Dataset chunks and evaluation items.
6. DeepSeek configuration notes and config examples that use environment variables only.
7. Verification docs proving the exported bundle passes the existing DomainRAG validator.

Phase 2B does not include:

1. Modifying Easy Dataset upstream source code.
2. Vendoring Easy Dataset into this repository.
3. Calling DeepSeek or any other live model API.
4. Running a full Easy Dataset production build as a required verification gate if upstream baseline commands fail in this environment.
5. Implementing the full Easy Dataset UI export button.
6. Changing the existing DomainRAG public data contract.

## Approved Approach

Use an adapter-first integration. DomainRAG-Bench defines a small, file-based Easy Dataset export bundle that mirrors the upstream concepts discovered during intake:

```text
chunks.jsonl
items.jsonl
```

`chunks.jsonl` represents Easy Dataset chunk rows from the upstream `Chunks` table. `items.jsonl` represents enriched evaluation dataset rows derived from Easy Dataset question/evaluation flows. The exporter maps those rows into:

```text
corpus.jsonl
canonical_dataset.jsonl
dev.jsonl
test.jsonl
fresh_hard_test.jsonl
qrels/dev.tsv
qrels/test.tsv
qrels/fresh_hard.tsv
dataset_card.md
statistics.json
```

This keeps the integration testable without importing a Next.js/Prisma application into the Python benchmark package. A later Easy Dataset fork change can add an export button or API endpoint that emits the same `chunks.jsonl` and `items.jsonl` shape.

## Upstream Intake Findings

Easy Dataset upstream:

- URL: `https://github.com/ConardLi/easy-dataset.git`
- Inspected commit: `4002b09d9c5726cafb9f61a8d12765cb96a2d94b`
- Version: `1.7.3`
- License: AGPL-3.0 with additional Easy Dataset terms in `LICENSE`
- Runtime shape: Next.js 14, Prisma, SQLite, React, MUI, Electron packaging
- Relevant dependencies: `@ai-sdk/openai`, `@ai-sdk/openai-compatible`, `langchain`, `@opendocsg/pdf2md`, `pdf2md-js`, `jsonrepair`, `zod`

Important code paths:

- Provider registry: `lib/db/llm-providers.js`
- OpenAI-compatible client: `lib/llm/core/providers/openai.js`
- Provider dispatch: `lib/llm/core/index.js`
- Model list fetch: `app/api/llm/fetch-models/route.js`
- Text splitting API: `app/api/projects/[projectId]/split/route.js`
- Text splitting implementation: `lib/file/text-splitter.js`
- Question generation API: `app/api/projects/[projectId]/generate-questions/route.js`
- Question generation service: `lib/services/questions/index.js`
- Dataset export API: `app/api/projects/[projectId]/datasets/export/route.js`
- Eval dataset export API: `app/api/projects/[projectId]/eval-datasets/export/route.js`
- Prisma data model: `prisma/schema.prisma`

Key limitation: Easy Dataset's existing public export surfaces do not expose enough retrieval provenance for DomainRAG by default. The DomainRAG exporter therefore requires an enriched export containing chunk ids, chunk contents, source chunk ids, split labels, and DomainRAG-specific question metadata.

## DeepSeek Configuration Boundary

Official DeepSeek API docs were checked on 2026-06-27. The OpenAI-compatible base URL is `https://api.deepseek.com`. Current model names include `deepseek-v4-flash` and `deepseek-v4-pro`; `deepseek-chat` and `deepseek-reasoner` are documented as deprecated on 2026-07-24 15:59 UTC.

Phase 2B may commit config examples such as:

```json
{
  "provider_id": "deepseek",
  "provider_name": "DeepSeek",
  "base_url": "https://api.deepseek.com",
  "api_key_env": "DEEPSEEK_API_KEY",
  "generation_model": "deepseek-v4-pro",
  "review_model": "deepseek-v4-pro",
  "fast_model": "deepseek-v4-flash"
}
```

No API key may be committed, logged, exported, or embedded in generated datasets. Unit tests must not call DeepSeek.

## Input Contract

`chunks.jsonl` rows:

```json
{
  "id": "chunk-1",
  "name": "paper-part-1",
  "content": "Supported source text.",
  "metadata": {
    "source": "internal"
  }
}
```

Required fields:

- `id`: stable chunk id.
- `content`: chunk text used to answer generated questions.

Optional fields:

- `name`: human-readable chunk name.
- `metadata`: internal provenance. The exporter must not copy this object into public DomainRAG artifacts.

`items.jsonl` rows:

```json
{
  "id": "q1",
  "split": "dev",
  "question_type": "single_choice",
  "question": "Which mechanism is supported?",
  "options": {"A": "Supported", "B": "Unsupported", "C": "Other", "D": "None"},
  "answer": ["A"],
  "answer_aliases": [],
  "reference_answer": "Supported.",
  "required_points": [],
  "source_chunk_ids": ["chunk-1"],
  "subdomain": "demo",
  "knowledge_type": "fact",
  "difficulty": "easy",
  "quality_score": 0.96
}
```

Required fields are the DomainRAG canonical item fields plus `split`. `split` must be one of `dev`, `test`, or `fresh_hard`. Public output must reject forbidden metadata families documented in `docs/data-contract.md`.

## Exporter Behavior

The exporter must:

1. Read `chunks.jsonl` and `items.jsonl`.
2. Validate source shape before writing output.
3. Reject empty chunks or items.
4. Reject duplicate chunk ids and item ids.
5. Reject unsupported split names.
6. Reject source chunk ids missing from `chunks.jsonl`.
7. Reject missing required split coverage for `dev`, `test`, and `fresh_hard`.
8. Render `corpus.jsonl` from chunk `id` and `content` only.
9. Render `canonical_dataset.jsonl` using exactly the existing canonical fields.
10. Render split files with fields `id`, `question`, `golden_answers`, and `metadata`.
11. Add `correct_options` to split metadata only for choice questions.
12. Render qrels rows for every item and source chunk id.
13. Write `dataset_card.md` and `statistics.json`.
14. Run `validate_dataset()` on the generated output before returning success.
15. Reject output paths that overlap the input directory.

## Public Metadata Rule

The exporter must not copy internal Easy Dataset provenance such as author, DOI, venue, page, original PDF path, or paper title into public output. It may use source metadata internally for future audit files, but Phase 2B public exports must only contain the fields allowed by the existing DomainRAG data contract.

## CLI

Add:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input fixtures/easy_dataset/example_export \
  --output outputs/domainrag \
  --dataset-name example_easy_dataset
```

Expected outputs:

```text
DomainRAG dataset written to outputs/domainrag/example_easy_dataset
```

## Testing

Required tests:

1. Exporter writes all DomainRAG files from a minimal Easy Dataset export.
2. Exported bundle passes `validate_dataset()`.
3. Choice questions render option text in split questions.
4. Fill-blank and short-answer records omit `correct_options`.
5. Missing source chunk ids are rejected before writing output.
6. Forbidden public metadata in source rows is rejected or stripped so output remains valid.
7. Unsafe output/input overlap is rejected.
8. CLI returns success for the fixture and non-zero for invalid input.
9. DeepSeek config example contains no literal API key and references `DEEPSEEK_API_KEY`.

## Verification

Phase 2B verification must include:

```bash
pytest
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
python scripts/export_easy_dataset_example.py
git status --short
```

The Easy Dataset upstream baseline commands and their environment-specific failures are documented separately in `docs/baseline/easy-dataset-baseline.md`.

## Risks

1. Easy Dataset's existing export routes do not include enough provenance for DomainRAG retrieval qrels. Phase 2B addresses this with an enriched export contract rather than patching upstream UI immediately.
2. Easy Dataset is AGPL-3.0. This repository must not vendor the upstream checkout; downstream deployment must handle AGPL obligations separately.
3. Full Easy Dataset build may be resource-heavy or interactive in this environment. Baseline failures are recorded rather than hidden.
4. DeepSeek model names are time-sensitive. Config examples must be easy to update and must not hard-code retired names.

