# Easy Dataset Architecture Notes For DomainRAG

## Intake Summary

Easy Dataset is a Next.js 14 and Prisma application. It stores projects, uploaded files, chunks, generated questions, QA datasets, evaluation datasets, model provider config, and task metadata in SQLite through Prisma.

DomainRAG-Bench does not import this application. Phase 2B records the upstream architecture and adds a small file-based adapter that can consume an enriched Easy Dataset export.

## Relevant Components

| Concern | Files | Notes |
| --- | --- | --- |
| Provider registry | `lib/db/llm-providers.js` | Includes a `deepseek` provider entry and default API URL. |
| OpenAI-compatible client | `lib/llm/core/providers/openai.js` | Uses `@ai-sdk/openai-compatible` for non-OpenAI endpoints. |
| Provider dispatch | `lib/llm/core/index.js` | Maps `deepseek` to `OpenAIClient`. |
| Model list fetch | `app/api/llm/fetch-models/route.js` | Calls `<endpoint>/models` for OpenAI-compatible providers. |
| Text splitting API | `app/api/projects/[projectId]/split/route.js` | Calls `splitProjectFile()` and stores chunks. |
| Text splitting implementation | `lib/file/text-splitter.js` | Supports markdown, character, token, recursive, code, and custom splitting. |
| Question generation API | `app/api/projects/[projectId]/generate-questions/route.js` | Generates questions per chunk with optional GA expansion. |
| Question generation service | `lib/services/questions/index.js` | Uses `LLMClient`, prompt builders, JSON extraction, labels, and DB persistence. |
| Dataset export API | `app/api/projects/[projectId]/datasets/export/route.js` | Exports QA dataset rows, but not enough retrieval provenance for DomainRAG qrels. |
| Eval dataset export API | `app/api/projects/[projectId]/eval-datasets/export/route.js` | Supports JSON, JSONL, CSV and question type filters. |
| Prisma schema | `prisma/schema.prisma` | Defines `Chunks`, `Datasets`, `EvalDatasets`, `ModelConfig`, and related tables. |

## Data Model Mapping

| Easy Dataset concept | DomainRAG concept | Phase 2B handling |
| --- | --- | --- |
| `Chunks.id` | `corpus.jsonl.id` and qrels corpus id | Source `chunks.jsonl` row `id`. |
| `Chunks.content` | `corpus.jsonl.contents` | Source `chunks.jsonl` row `content`. |
| Eval question id | Canonical question id and split row id | Source `items.jsonl` row `id`. |
| `questionType` | `question_type` | Source export normalizes to DomainRAG names. |
| `options` | `options` and rendered split question text | Source export uses option-key object. |
| `correctAnswer` | `answer` / `golden_answers` | Source export uses answer arrays. |
| `chunkId` / source chunks | `source_chunk_ids` and qrels | Source export must provide `source_chunk_ids`. |
| Tags/labels | `subdomain`, optional filtering | Source export must provide `subdomain`. |
| Quality score | `quality_score` | Source export must provide numeric score. |

## DomainRAG Gap

Easy Dataset's current public export routes are useful but insufficient for DomainRAG retrieval benchmarks because they do not consistently include chunk ids, chunk contents, source chunk ids, split assignment, and all canonical metadata needed by `docs/data-contract.md`.

Phase 2B therefore defines an enriched export bundle:

```text
chunks.jsonl
items.jsonl
```

A later Easy Dataset fork can add an export route or UI action that emits this same bundle. The DomainRAG-Bench side remains independent and testable.

## DeepSeek Integration Surface

Easy Dataset already maps `deepseek` to the OpenAI-compatible client path. The minimal future upstream change is likely a preset/config addition rather than a new model client:

- Provider id: `deepseek`
- Base URL: `https://api.deepseek.com`
- API key source: `DEEPSEEK_API_KEY`
- Generation/review model: `deepseek-v4-pro`
- Fast/batch model: `deepseek-v4-flash`

Phase 2B commits only config examples and documentation. It does not call live APIs.

## AGPL Boundary

Easy Dataset is AGPL-3.0 with additional terms. The local checkout is ignored and must not be committed. Any future modified Easy Dataset fork or hosted service needs a separate license compliance review.
