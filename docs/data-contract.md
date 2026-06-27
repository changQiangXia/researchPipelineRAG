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

Public exports allow only the documented public fields for each artifact:

- `corpus.jsonl` rows: `id`, `contents`
- `canonical_dataset.jsonl` rows: the required canonical item fields listed above, with no extras
- split rows: `id`, `question`, `golden_answers`, `metadata`
- split `metadata`: `question_type`, `source_chunk_ids`, `knowledge_type`, `difficulty`, `answer_aliases`, `required_points`, and `correct_options` only for choice questions

Public exports must not contain forbidden metadata fields anywhere in the row, including nested metadata objects or arrays. Forbidden field families include DOI, author/authors, venue, page/page_number, original PDF path, and original paper title.

## Qrels

Each qrels row has three tab-separated fields:

```text
query-id<TAB>corpus-id<TAB>score
```

Every question in a split must have at least one qrels row. Every qrels corpus id must exist in `corpus.jsonl`.
