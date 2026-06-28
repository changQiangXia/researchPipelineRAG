# Outputs Guide

这个目录分成两类内容：当前成果入口和历史运行记录。

先看 current：

```text
outputs/current/
```

`outputs/current/` 用成果类别组织当前项目状态，适合第一次阅读本项目的人。

历史运行记录在：

```text
outputs/archive/provenance/
```

这些归档目录是 provenance，用于复现、审计和回查，不是推荐的第一阅读入口。

## 当前建议阅读顺序

1. `outputs/current/README.md`
2. `outputs/current/demo_question_dataset.md`
3. `outputs/current/benchmark_results.md`
4. `outputs/current/full_text_chunks.md`
5. `outputs/current/source_review.md`

## 仍需注意的边界

- 300 题数据集是 provisional，不是 human-final benchmark。
- 全文 chunk manifest 是 machine-parseable 结果，不是 human-final accepted-source corpus。
- human sign-off workflow 不是最终人工签核白名单。
- 本地 hashed dense benchmark 是 non-neural baseline，不是 FlashRAG neural dense/reranker。

## 目录说明

| 目录 | 用途 |
| --- | --- |
| `current/` | 当前成果导航，适合读者快速理解项目 |
| `archive/provenance/` | 按成果主题收束的历史运行产物，适合审计和复现 |
| `flashrag/` | FlashRAG 兼容数据包 |
| `deepseek/` | 早期 DeepSeek 生成/复核输出 |
| `domainrag/` | Easy Dataset adapter 生成的示例 DomainRAG 输出 |
| `example_domain/` | 最小示例输出 |
