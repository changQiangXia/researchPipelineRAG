# Benchmark Results

当前主要看 Fresh-Hard split。

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

