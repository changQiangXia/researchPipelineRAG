# FlashRAG Architecture Notes For DomainRAG

Date: 2026-06-27
Upstream commit inspected: `e0e73399ce8d4563397b5fb4980de72a9c5e15a6`

## Relevant Entry Points

### Dataset Item

`flashrag/dataset/dataset.py` defines `Item`.

Relevant fields:

- `id`
- `question`
- `golden_answers`
- `choices`
- `metadata`
- `output`

DomainRAG split rows already provide `id`, `question`, `golden_answers`, and `metadata`. `choices` is optional for Phase 2A because DomainRAG renders choice options into the `question` text and stores correct options in `metadata.correct_options`.

### Dataset Loader

`flashrag/dataset/dataset.py` defines `Dataset`.

It loads `.jsonl`, `.json`, and `.parquet` files. For JSONL files, each line is parsed into an `Item`.

### Split Resolution

`flashrag/utils/utils.py` defines `get_dataset(config)`.

The loader reads:

```text
config["dataset_path"]/<split>.jsonl
```

`flashrag/config/config.py` sets:

```python
config["dataset_path"] = os.path.join(config["data_dir"], config["dataset_name"])
```

Therefore a DomainRAG dataset must be prepared as:

```text
<data_dir>/<dataset_name>/
├── dev.jsonl
├── test.jsonl
└── fresh_hard.jsonl
```

### Config

`flashrag/config/config.py` merges `flashrag/config/basic_config.yaml`, an optional config file, and an optional config dict.

For Phase 2A, the committed example config focuses on dataset binding only:

- `data_dir`
- `dataset_name`
- `split`
- `framework`
- `generator_model`
- `metrics`
- `disable_save`

It intentionally avoids live API credentials and model paths.

### Evaluator

`flashrag/evaluator/evaluator.py` dynamically collects metric classes from `flashrag/evaluator/metrics.py`.

The default metrics include `em`, `f1`, and `acc`. DomainRAG keeps its own type-specific evaluator from the first milestone. Phase 2A does not replace either evaluator; it prepares data so FlashRAG can load the examples in a later dependency-complete environment.

## DomainRAG Mapping

| DomainRAG source | FlashRAG prepared target |
| --- | --- |
| `dev.jsonl` | `dev.jsonl` |
| `test.jsonl` | `test.jsonl` |
| `fresh_hard_test.jsonl` | `fresh_hard.jsonl` |
| `corpus.jsonl` | `corpus.jsonl` |
| `qrels/dev.tsv` | `qrels/dev.tsv` |
| `qrels/test.tsv` | `qrels/test.tsv` |
| `qrels/fresh_hard.tsv` | `qrels/fresh_hard.tsv` |

FlashRAG's core JSONL dataset loader does not consume qrels directly. DomainRAG still copies qrels into the prepared bundle because retrieval metrics and index-building phases will need the query-to-corpus relation.

## Phase 2A Boundary

The adapter must not depend on FlashRAG imports. This keeps tests fast and avoids installing `transformers`, `torch`, `datasets`, and generator/retriever dependencies during the intake phase.

The prepared bundle is a compatibility artifact, not a full FlashRAG experiment. Full retriever/generator execution remains a later phase after dependency installation and model/API decisions.
