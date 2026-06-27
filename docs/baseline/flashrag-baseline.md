# FlashRAG Baseline Intake

Date: 2026-06-27
Phase: 2A - FlashRAG Intake + DomainRAG Adapter

## Upstream

- Repository: `https://github.com/RUC-NLPIR/FlashRAG.git`
- Local checkout: `benchmark/flashrag-fork/`
- Commit: `e0e73399ce8d4563397b5fb4980de72a9c5e15a6`
- License: MIT, based on upstream `LICENSE` and README badge.

`benchmark/flashrag-fork/` is intentionally ignored by this repository. The DomainRAG-Bench repository commits adapter code, configs, tests, and docs, not the upstream FlashRAG source tree.

## Files Inspected

- `README.md`
- `requirements.txt`
- `flashrag/config/basic_config.yaml`
- `flashrag/config/config.py`
- `flashrag/dataset/dataset.py`
- `flashrag/utils/utils.py`
- `flashrag/evaluator/evaluator.py`
- `flashrag/evaluator/metrics.py`
- `examples/quick_start/simple_pipeline.py`
- `examples/methods/run_exp.py`
- `docs/zh-cn/data_preparation/evaluation-datasets.md`

## Dependency Baseline

Command:

```bash
PYTHONPATH=benchmark/flashrag-fork python - <<'PY'
from flashrag.dataset import Dataset
print("dataset import ok")
from flashrag.utils import get_dataset
print("utils import ok")
PY
```

Observed result in the current lightweight environment:

```text
ModuleNotFoundError: No module named 'transformers'
```

Interpretation:

- Full FlashRAG utility imports require dependencies such as `transformers`, `torch`, `datasets`, and related packages.
- Phase 2A does not install the full FlashRAG dependency set.
- Adapter tests must remain independent of FlashRAG imports.
- The local checkout is still useful for source inspection and for documenting the exact dataset/config conventions.

## Data Format Compatibility

FlashRAG documents each dataset split as JSONL records shaped like:

```python
{
    "id": str,
    "question": str,
    "golden_answers": list[str],
    "metadata": dict,
}
```

This matches DomainRAG split records produced by `data/example_domain`.

## Dataset Path Convention

FlashRAG's `get_dataset(config)` resolves split files as:

```text
data_dir/<dataset_name>/<split>.jsonl
```

DomainRAG already has `dev.jsonl` and `test.jsonl`. The only required split filename mapping for Phase 2A is:

```text
data/example_domain/fresh_hard_test.jsonl
outputs/flashrag/example_domain/fresh_hard.jsonl
```

## Baseline Decision

Phase 2A prepares a FlashRAG-compatible bundle from the DomainRAG contract without importing FlashRAG at runtime. Once the heavier FlashRAG environment is installed in a later phase, the generated bundle and config can be used with FlashRAG's `Config` and `get_dataset` path conventions.
