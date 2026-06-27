# DomainRAG-Bench Data Contract

## Files

Each dataset directory contains:

- `corpus.jsonl`
- `canonical_dataset.jsonl`
- `dev.jsonl`
- `test.jsonl`
- `fresh_hard_test.jsonl`
- `qrels/dev.tsv`
- `qrels/test.tsv`
- `qrels/fresh_hard.tsv`

## Canonical Item

Required fields:

- `id`: stable question id.
- `question_type`: one of `single_choice`, `multiple_choice`, `fill_blank`, `short_answer`.
- `question`: self-contained domain question.
- `options`: object for choice questions, empty object for fill-blank and short-answer.
- `answer`: array for every question type.
- `answer_aliases`: accepted aliases, required non-empty for fill-blank.
- `reference_answer`: reference prose answer.
- `required_points`: required scoring points, non-empty for short-answer.
- `source_chunk_ids`: non-empty array of corpus ids.
- `subdomain`: domain slice label.
- `knowledge_type`: one of `fact`, `parameter`, `condition`, `method`, `mechanism`, `comparison`, `synthesis`.
- `difficulty`: one of `easy`, `medium`, `hard`.
- `quality_score`: numeric quality score.

## Public Metadata Rule

Public exports allow dataset ids and source chunk ids. They do not allow DOI, authors, venue, page number, original PDF path, or original paper title fields.

## Qrels

Each qrels row has three tab-separated fields:

```text
query-id<TAB>corpus-id<TAB>score
```

Every question in a split must have at least one qrels row. Every qrels corpus id must exist in `corpus.jsonl`.
