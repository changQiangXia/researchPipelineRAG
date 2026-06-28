# Benchmark Results

当前主要看 Fresh-Hard split。

本表的 `api_calls` 只统计外部模型/API 调用。这里展示的是本地检索诊断 baseline，不包含 DeepSeek live answer/Judge；因此下面这些不调用外部模型的方法都是 0。

Baseline 输出：

```text
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/baseline/report_fresh_hard/summary.json
```

结果摘要：

| method | questions | retrieval_hit | retrieval_recall | api_calls |
| --- | ---: | ---: | ---: | ---: |
| `no_rag` | 100 | 0.0000 | 0.0000 | 0 |
| `oracle_context` | 100 | 1.0000 | 1.0000 | 0 |
| `lexical_rag` | 100 | 0.7200 | 0.7200 | 0 |

本地 hashed dense 诊断：

```text
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/hashed_dense/report_fresh_hard/summary.json
```

| method | questions | retrieval_hit | retrieval_recall | api_calls |
| --- | ---: | ---: | ---: | ---: |
| `hashed_dense_oracle_reader` | 100 | 0.7000 | 0.7000 | 0 |
| `hashed_dense_lexical_rerank_oracle_reader` | 100 | 0.7200 | 0.7200 | 0 |

边界：hashed dense 是本地 non-neural baseline，不是 FlashRAG neural dense/reranker。

如果需要查看真实模型回答与 Judge 的 API 调用、token 和错误统计，应看 DeepSeek live comparison 相关归档，而不是把本页的 `api_calls=0` 理解为项目没有 live 模型评测。

