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

这个 bundle 是兼容数据包，用于让同一批 DomainRAG 数据进入 FlashRAG 风格的数据目录和配置入口。它不是完整 FlashRAG neural dense/reranker 实验，也不代表已经运行神经向量检索、神经重排或生成式评测。

`qrels` 会随 bundle 一起保留，供 DomainRAG retrieval metrics、后续 index/retrieval 实验和审计使用。FlashRAG 的基础 JSONL loader 本身不直接消费这些 qrels。

重新生成命令：

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_demo_questions
```

重新生成 bundle 不会调用 DeepSeek 或其他外部模型 API。

