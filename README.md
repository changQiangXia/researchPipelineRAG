# DomainRAG-Bench

DomainRAG-Bench 是一个面向专业领域 RAG 测评的数据契约和基准流水线项目。当前版本完成的是第一阶段最小闭环：先冻结数据格式、构造 `example_domain` 示例数据，并用本地 mock/no-RAG 方法跑通验证、评测和报告生成流程。

## 当前阶段范围

第一阶段已经完成：

- 定义公开数据契约：`canonical_dataset.jsonl`、`corpus.jsonl`、FlashRAG 风格 split、`qrels/*.tsv`
- 构造示例领域数据：`data/example_domain`
- 构造负例数据：`data/invalid_fixtures/missing_qrels`
- 实现数据校验 CLI：`validate-data`
- 实现最小 benchmark runner：`run`
- 实现类型化答案归一化和评测指标
- 实现 summary 报告生成：`report`
- 加入回归测试，覆盖 schema、validator、prompt、normalizer、evaluator、runner、reporter 和 CLI

第一阶段不会调用真实模型 API，不会克隆或修改 Easy Dataset / FlashRAG，也不会处理真实论文。所有运行都在本地完成，benchmark 方法只包含 `no_rag` 和 `mock_rag`。

## 目录结构

```text
benchmark/domainrag/        核心 Python 包和 CLI
configs/domainrag/          第一阶段本地配置
data/example_domain/        示例领域公开数据
data/invalid_fixtures/      校验失败用例
docs/data-contract.md       数据契约说明
docs/verification/          验证记录
outputs/example_domain/     示例 benchmark 输出
reports/example_domain/     示例报告
scripts/                    数据生成脚本
tests/                      自动化测试
```

## 快速复现

在项目根目录执行：

```bash
python scripts/create_example_domain.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/example_domain
PYTHONPATH=benchmark python -m domainrag.cli run --dataset data/example_domain --output outputs --methods no_rag,mock_rag --split dev
PYTHONPATH=benchmark python -m domainrag.cli report --input outputs/example_domain/dev_results.jsonl --output reports/example_domain
pytest
```

预期结果：

- `data/example_domain is valid`
- `outputs/example_domain/dev_results.jsonl` 被生成
- `reports/example_domain/summary.md` 和 `summary.json` 被生成
- 全量测试通过

## 数据安全约束

公开数据中只保留数据集内部需要的 ID 和证据关系，不导出论文身份元数据。校验器会拒绝 DOI、作者、venue、页码、原始 PDF 路径、原始论文标题等字段。

`answer` 在所有题型中都统一使用数组，包括填空题。选择题答案必须对应合法选项，多选题必须至少包含两个不同的正确选项。

## 下一阶段建议

建议下一阶段先做 FlashRAG 接入：克隆并记录 FlashRAG 上游版本，跑 baseline，审计 Dataset / Corpus / Retriever / Generator / Evaluator / Pipeline，再把当前 `example_domain` 数据契约接入真实 FlashRAG benchmark 流程。确认下游 benchmark 能稳定消费 DomainRAG 数据后，再改造 Easy Dataset 作为上游数据生产工具。
