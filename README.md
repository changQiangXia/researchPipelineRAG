# DomainRAG-Bench

DomainRAG-Bench 是一个面向专业领域 RAG 测评的数据契约和基准流水线项目。当前版本已经完成第一阶段最小闭环、Phase 2A FlashRAG 兼容输出，以及 Phase 2B Easy Dataset 风格导出适配。项目现在可以从增强版 Easy Dataset 导出包生成 DomainRAG 标准数据集，再继续准备为 FlashRAG 消费。

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

后续阶段同样遵守两个约束：测试不调用真实模型 API，仓库不保存 API key。

## 目录结构

```text
benchmark/domainrag/        核心 Python 包和 CLI
configs/domainrag/          第一阶段本地配置
configs/easy_dataset/       Easy Dataset / DeepSeek 示例配置，不包含密钥
data/example_domain/        示例领域公开数据
data/invalid_fixtures/      校验失败用例
docs/data-contract.md       数据契约说明
docs/verification/          验证记录
fixtures/easy_dataset/      Easy Dataset 风格导出输入样例
outputs/example_domain/     示例 benchmark 输出
outputs/domainrag/          Easy Dataset adapter 生成的 DomainRAG 数据
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

## Phase 2A: FlashRAG 兼容输出

第二阶段 A 当前提供的是 FlashRAG 输入准备，不要求安装 FlashRAG 依赖，也不会调用真实模型或在线 API。在项目根目录执行：

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag --dataset data/example_domain --output outputs/flashrag --dataset-name example_domain
```

预期结果：

- `outputs/flashrag/example_domain/` 被生成，包含 `dev.jsonl`、`test.jsonl`、`fresh_hard.jsonl`、`corpus.jsonl` 和 `qrels/*.tsv`
- `outputs/flashrag/example_domain_flashrag.yaml` 被生成，可作为后续 FlashRAG 数据集绑定示例
- 该阶段只验证本地 bundle 准备，不验证 FlashRAG 真实运行

## Phase 2B: Easy Dataset 风格导出

第二阶段 B 当前提供的是 Easy Dataset intake 和 DomainRAG exporter。Easy Dataset 上游源码只 clone 到本地 ignored 路径 `dataset-factory/easy-dataset-fork/` 用于架构检查，不提交进本仓库。

当前 exporter 消费一个增强版 Easy Dataset 导出包：

```text
fixtures/easy_dataset/example_export/chunks.jsonl
fixtures/easy_dataset/example_export/items.jsonl
```

在项目根目录执行：

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input fixtures/easy_dataset/example_export --output outputs/domainrag --dataset-name example_easy_dataset
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/example_easy_dataset
```

预期结果：

- `outputs/domainrag/example_easy_dataset/` 被生成
- 输出包含 `corpus.jsonl`、`canonical_dataset.jsonl`、`dev.jsonl`、`test.jsonl`、`fresh_hard_test.jsonl`、`qrels/*.tsv`、`dataset_card.md` 和 `statistics.json`
- 生成的数据集能通过现有 `validate-data`
- Easy Dataset 原始来源元数据不会进入公开输出

也可以运行脚本：

```bash
python scripts/export_easy_dataset_example.py
```

DeepSeek 示例配置在 `configs/easy_dataset/deepseek.example.json`。它只记录 `DEEPSEEK_API_KEY` 这个环境变量名，不包含任何真实密钥。测试不会调用 DeepSeek。

## 数据安全约束

公开数据中只保留数据集内部需要的 ID 和证据关系，不导出论文身份元数据。校验器会拒绝 DOI、作者、venue、页码、原始 PDF 路径、原始论文标题等字段。

`answer` 在所有题型中都统一使用数组，包括填空题。选择题答案必须对应合法选项，多选题必须至少包含两个不同的正确选项。

## 下一阶段建议

建议下一阶段做 Phase 2C：把当前 `fixtures/easy_dataset/example_export` 这份文件契约落回 Easy Dataset fork，增加一个实际导出入口，让 Easy Dataset 能导出 `chunks.jsonl` 和 `items.jsonl`。确认真实导出能被本仓库 `export-domainrag` 消费后，再进入小规模真实论文 pilot。
