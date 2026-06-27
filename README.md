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

## Phase 2C: Easy Dataset DomainRAG 导出入口资产

第二阶段 C 提供 Easy Dataset fork 可复制的导出入口资产，位置在：

```text
integrations/easy-dataset/domainrag-export/
```

把其中 `files/` 下的两个文件复制到 Easy Dataset fork 根目录后，可得到：

- `lib/domainrag/exporter.js`
- `app/api/projects/[projectId]/domainrag-export/route.js`

该路由返回 `chunks.jsonl` 和 `items.jsonl` 的文件内容。将这两个文件写入同一目录后，可继续使用 Phase 2B 的命令转换为 DomainRAG 标准数据集：

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag --input <easy_dataset_export_dir> --output outputs/domainrag --dataset-name <dataset_name>
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset outputs/domainrag/<dataset_name>
```

本仓库不会提交修改后的 Easy Dataset 上游源码；`dataset-factory/easy-dataset-fork/` 仍然只作为本地 ignored 对照 checkout。

## Phase 2D: Easy Dataset fork smoke test

第二阶段 D 已在 ignored 的 Easy Dataset fork 中验证 Phase 2C 资产复制路径：

- Easy Dataset fork 版本：`4002b09d9c5726cafb9f61a8d12765cb96a2d94b`，`easy-dataset 1.7.3`
- 复制后目标路径：
  - `lib/domainrag/exporter.js`
  - `app/api/projects/[projectId]/domainrag-export/route.js`
- fork 内 helper 可以生成 `chunks.jsonl` 和 `items.jsonl`
- 生成的文件可以被本仓库 `export-domainrag` 消费，并通过 `validate-data`

当前环境的 cgroup 内存上限是 2GiB，完整 Easy Dataset `npm install` 会被 Signal 9 杀掉，因此本阶段没有把 Next.js dev server 作为通过门槛。详细记录见 `docs/verification/easy-dataset-fork-smoke-test.md`。

## Phase 2E: Easy Dataset 真实路由运行验证

第二阶段 E 已在 ignored 的 Easy Dataset fork 中启动真实 Next.js dev server，并通过 HTTP 调用复制进去的 DomainRAG 导出路由：

- Easy Dataset fork 版本：`4002b09d9c5726cafb9f61a8d12765cb96a2d94b`，`easy-dataset 1.7.3`
- 当前容器 cgroup 内存上限仍为 2GiB，但使用 `pnpm install --frozen-lockfile --ignore-scripts --child-concurrency=1 --network-concurrency=1` 可以完成依赖安装
- `pnpm exec prisma db push` 创建本地 SQLite schema 并生成 Prisma Client
- 通过 Prisma Client 写入真实 Easy Dataset 项目、chunk 和 eval dataset 行
- `GET /api/projects/domainrag_smoke/domainrag-export` 返回 200
- `POST /api/projects/domainrag_smoke/domainrag-export` 返回 200，并导出 `chunks.jsonl` 与 `items.jsonl`
- 路由导出结果可以被本仓库 `export-domainrag` 消费，并通过 `validate-data`

这一步没有调用 DeepSeek，也没有提交 Easy Dataset 上游源码、依赖目录、SQLite 文件或临时导出结果。详细记录见 `docs/verification/easy-dataset-runtime-route.md`。

## 数据安全约束

公开数据中只保留数据集内部需要的 ID 和证据关系，不导出论文身份元数据。校验器会拒绝 DOI、作者、venue、页码、原始 PDF 路径、原始论文标题等字段。

`answer` 在所有题型中都统一使用数组，包括填空题。选择题答案必须对应合法选项，多选题必须至少包含两个不同的正确选项。

## 下一阶段建议

建议下一阶段进入 Phase 3A：小规模真实论文数据 pilot。不要继续扩大 mock/smoke fixture，先选择 3 到 5 篇真实论文，完成“论文文本进入 Easy Dataset 或等价本地入口 -> 生成/整理 chunk 和题目 -> 导出 DomainRAG -> 校验 -> 跑最小 baseline”的端到端闭环。确认数据质量、人工复核点和 DeepSeek 调用边界后，再扩大到 RAG.md 中的 100 到 180 篇标准规模。
