# Outputs Archive

`archive/provenance/` 保存按成果主题收束后的历史运行记录。它的用途是 provenance、复现和审计，不是第一次理解项目的入口。

第一次阅读建议从这里开始：

```text
outputs/current/
```

归档目录按成果类别组织，便于把报告、测试和审计记录追溯到具体产物，同时避免把执行阶段编号暴露成主要阅读结构。当前较重要的归档证据包括：

| path | meaning |
| --- | --- |
| `demo-dataset/demo-question-generation/` | provisional 300 题数据集生成记录和 baseline |
| `source-workflow/full-text-chunk-extraction/` | machine-parseable full-text chunk manifests |
| `retrieval-diagnostics/hashed-dense-benchmark/` | 本地 non-neural hashed dense 诊断 |
| `source-workflow/manual-finalization-packet/` | 人工终审候选包 |
| `source-workflow/human-signoff/` | human sign-off workflow 输出 |

边界：归档证据可以证明流水线做过什么，但不能替代最终人工签核。涉及 final source whitelist、human-final benchmark、accepted-source corpus 的结论，应以 `outputs/current/` 和 README 中的边界说明为准。
