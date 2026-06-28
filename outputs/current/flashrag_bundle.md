# FlashRAG Bundle

当前 300 题 provisional 数据集的 FlashRAG bundle：

```text
outputs/flashrag/real_pilot_nickel_superalloy_demo_questions/
outputs/flashrag/real_pilot_nickel_superalloy_demo_questions_flashrag.yaml
```

包含：

```text
corpus.jsonl
dev.jsonl
test.jsonl
fresh_hard.jsonl
qrels/dev.tsv
qrels/test.tsv
qrels/fresh_hard.tsv
```

重新生成命令：

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_demo_questions
```

