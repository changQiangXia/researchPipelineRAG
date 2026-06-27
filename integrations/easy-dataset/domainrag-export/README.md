# Easy Dataset DomainRAG Export Route

This directory contains DomainRAG-owned files that can be copied into an Easy Dataset fork to export the enriched DomainRAG intake bundle:

```text
chunks.jsonl
items.jsonl
```

The Easy Dataset upstream source is not vendored in DomainRAG-Bench. Copy these files into a fork that you control:

```text
files/lib/domainrag/exporter.js
files/app/api/projects/[projectId]/domainrag-export/route.js
```

After copying, the Easy Dataset fork should contain:

```text
lib/domainrag/exporter.js
app/api/projects/[projectId]/domainrag-export/route.js
```

## Route

The route adds:

```text
GET  /api/projects/:projectId/domainrag-export
POST /api/projects/:projectId/domainrag-export
```

`GET` returns a small preview with the number of evaluation rows that have a linked chunk.

`POST` returns a JSON envelope with two named file payloads:

```json
{
  "files": [
    {"path": "chunks.jsonl", "content": "..."},
    {"path": "items.jsonl", "content": "..."}
  ],
  "statistics": {
    "chunk_count": 3,
    "item_count": 3,
    "split_counts": {"dev": 1, "fresh_hard": 1, "test": 1}
  },
  "skipped": [],
  "errors": []
}
```

The envelope avoids adding a zip dependency to Easy Dataset. Save each `files[].content` value as its matching `files[].path`.

## Request Body

Example:

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

If `splits` does not mention an item, the helper checks tags such as `split:dev`, `split:test`, or `split:fresh_hard`. If no split is found, compatible rows are assigned deterministically while preserving required `dev`, `test`, and `fresh_hard` coverage when possible.

Metadata precedence is:

1. `itemOverrides[item.id]`
2. Tags such as `subdomain:oxidation`, `knowledge:mechanism`, `difficulty:hard`, `quality:0.96`
3. `defaults`

## Materialize Files

Save the route response to `domainrag-export.json`, then write the files:

```bash
python - <<'PY'
from pathlib import Path
import json

payload = json.loads(Path("domainrag-export.json").read_text(encoding="utf-8"))
out = Path("domainrag-export")
out.mkdir(exist_ok=True)
for file in payload["files"]:
    (out / file["path"]).write_text(file["content"], encoding="utf-8")
PY
```

Then run the DomainRAG-Bench exporter:

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input domainrag-export \
  --output outputs/domainrag \
  --dataset-name my_easy_dataset
```

## Mapping Notes

- Easy Dataset `single_choice` maps to DomainRAG `single_choice`.
- Easy Dataset `multiple_choice` maps to DomainRAG `multiple_choice` when it has five or six options.
- Easy Dataset `short_answer` maps to DomainRAG `short_answer`.
- Easy Dataset `open_ended` maps to DomainRAG `short_answer`.
- `fill_blank` is supported when present in a fork or imported eval data.
- `true_false` is skipped because the current DomainRAG contract has no two-option true/false type.

Only chunks referenced by exported items are included in `chunks.jsonl`. The route does not export DOI, authors, venue, page number, original PDF path, or original paper title.

## Boundary

These files are intended for an Easy Dataset fork. DomainRAG-Bench does not commit modified Easy Dataset source and does not call live model providers while testing this integration.
