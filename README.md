# DomainRAG-Bench

DomainRAG-Bench 是一个面向专业领域 RAG 测评的数据契约和基准流水线项目。当前版本已经完成第一阶段最小闭环、Easy Dataset intake、FlashRAG 兼容输出、真实数据 pilot、DeepSeek 生成/复核候选题，以及 No-RAG / Oracle-Context / lexical RAG 的诊断评测。项目现在已经可以在真实 pilot 数据上调用 DeepSeek API 生成 live answer，并保留检索、答题、延迟和 token 指标。

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

## Phase 3A: 小规模真实论文数据 pilot

第三阶段 A 已开始从 synthetic fixture 转向真实文献数据。当前 pilot 选择“镍基高温合金高温失效”方向，人工抽取并转述 7 篇开放访问文章页面中的领域事实，形成可追溯的小规模数据闭环：

- 内部来源 manifest：`data/real_pilot_sources/nickel_superalloy_high_temp_failure/sources.jsonl`
- Easy Dataset 风格输入：`fixtures/easy_dataset/real_pilot_nickel_superalloy/chunks.jsonl` 和 `items.jsonl`
- 公开 DomainRAG 数据集：`data/real_pilot_nickel_superalloy/`
- 当前规模：9 个 chunk，12 道题，`dev` / `test` / `fresh_hard` 各 4 道
- 题型覆盖：单选、多选、填空、简答各 3 道
- 已通过 `validate-data`
- 已能生成 FlashRAG bundle
- 已跑通 `no_rag` 最小 baseline 和 summary report

这一步仍未调用 DeepSeek。source manifest 用于内部溯源；公开 DomainRAG 数据集不包含论文标题、URL、DOI、作者、venue、页码或原始 PDF 路径。详细记录见 `docs/verification/real-data-pilot.md`。

## Phase 3B: DeepSeek 生成和独立复核 pilot

第三阶段 B 已在 Phase 3A 的真实 chunk 上接入受控 DeepSeek 生成和独立复核：

- 新增本地流水线模块：`benchmark/domainrag/deepseek_pipeline.py`
- 新增运行脚本：`scripts/run_deepseek_real_pilot.py`
- 测试和 dry-run 不调用 DeepSeek
- 真实调用只从 `DEEPSEEK_API_KEY` 环境变量读取密钥
- 生成调用和复核调用是两个独立请求
- 输出保存在 `outputs/deepseek/real_pilot_nickel_superalloy/`
- 当前真实运行生成 3 个候选题，并全部通过独立复核
- DeepSeek accepted items 已能通过 `export-domainrag` 转成合法 DomainRAG candidate dataset

这一步发现并修复了一个真实契约风险：DeepSeek 可能把选择题 `options` 输出成数组，而 DomainRAG 需要 `A/B/C/D` keyed object。现在本地校验会拒绝这种输出，prompt 也加入了明确 JSON 形状示例。详细记录见 `docs/verification/deepseek-generation-review.md`。

## Phase 3C: DeepSeek 全 chunk 候选题和审计表

第三阶段 C 已把 DeepSeek 生成/复核从 3 条小样本扩展到 Phase 3A 的全部真实 chunk：

- `scripts/run_deepseek_real_pilot.py --plan all-chunks` 会为输入 `chunks.jsonl` 的每个 chunk 规划 1 道候选题
- 新增 `candidate_audit.jsonl`，把每条候选标为 `accepted`、`rejected` 或 `needs_human_review`
- 当前真实运行覆盖 9 个 chunk，生成 9 道候选题
- 9 道候选题都通过独立复核并达到自动接受阈值
- 生成完整候选 DomainRAG 数据集：`outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates/`
- 候选数据集已通过 `validate-data`
- 候选数据集已能生成 FlashRAG bundle
- 候选数据集已跑通 `no_rag` 最小 baseline 和 summary report

这一步仍不把 DeepSeek candidate 直接替换为最终 gold 数据；它是可审计的候选生产结果。详细记录见 `docs/verification/deepseek-full-candidate-audit.md`。

## Phase 4: Oracle-Context 和 lexical RAG 评测闭环

第四阶段开始进入真实评测链路。当前 runner 已支持：

- `no_rag`：不提供上下文，作为低分诊断基线
- `oracle_context`：直接使用 qrels gold context，验证题目能被正确证据回答
- `lexical_rag`：使用无外部依赖的词面检索 top-k，并记录 `retrieval_hit`、`retrieval_recall` 和 `retrieval_mrr`

Phase 4 已在两个数据集上跑通 `dev` / `test` / `fresh_hard` 三个 split：

- curated real pilot：`data/real_pilot_nickel_superalloy`
- DeepSeek full candidate dataset：`outputs/deepseek/real_pilot_nickel_superalloy_full/domainrag_candidate/deepseek_real_pilot_full_candidates`

输出位置：

- curated reports：`outputs/phase4/curated/report_*/summary.json`
- DeepSeek candidate reports：`outputs/phase4/deepseek_candidate/report_*/summary.json`

报告中新增 `_diagnostics.fresh_hard_candidates`，用于初筛 No-RAG 低、Oracle-Context 高的问题。当前 curated `fresh_hard` 中识别 3 个候选，DeepSeek candidate `fresh_hard` 中识别 3 个候选。详细记录见 `docs/verification/oracle-lexical-rag-eval.md`。

## Phase 4B: DeepSeek live answer 评测

第四阶段 B 把 Phase 4 的完美 reader 模拟推进到真实 DeepSeek 回答生成。离线 `domainrag run` 仍保持 deterministic；真实 API 调用单独放在：

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs/phase4b/live_deepseek_fresh_hard \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard
```

该命令只从环境变量读取 `DEEPSEEK_API_KEY`，测试不会调用真实 API。输出行保留 Phase 4 的字段，并记录真实模型的：

- `prediction`
- `latency_ms`
- `input_tokens`
- `output_tokens`
- `api_calls`
- `error`

报告器现在会汇总 `mean_input_tokens`、`mean_output_tokens`、`total_input_tokens`、`total_output_tokens` 和 `total_tokens`，用于效率榜的下一步扩展。

当前已在 curated real pilot 的 `fresh_hard` split 上完成真实运行：

- 输出：`outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl`
- 报告：`outputs/phase4b/live_deepseek_fresh_hard/report_fresh_hard/summary.json`
- 结果：12 行，12 次 API 调用，0 个错误
- live Fresh-Hard 候选：`ns_ht_q010`、`ns_ht_q011`
- `lexical_rag` 在当前小 corpus 上检索召回为 1.0；这仍然只是 pilot 规模结果，不代表大规模语料难度

这一步还修复了真实调用中暴露的两个 runner 风险：reasoning 响应耗尽 token 导致 `message.content` 为空，以及空 `answer` 被误当作成功预测。详细记录见 `docs/verification/deepseek-live-answer-eval.md`。

## Phase 4C: DeepSeek Judge 辅助评测

第四阶段 C 增加 RAG.md 中要求的 DeepSeek 辅助 Judge。它不替代规则指标，而是消费 Phase 4B 的 live answer 输出，额外评分：

- `correctness`
- `context_support`
- `faithfulness`
- `relevance`
- `unsupported_claims`

Judge 使用 0 到 5 分制，并派生 `hallucination_risk = 5 - faithfulness` 方便报告。真实 API 调用入口：

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --input outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --output outputs/phase4c/deepseek_judge_fresh_hard \
  --split fresh_hard
```

生成 Judge summary：

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-report \
  --input outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/phase4c/deepseek_judge_fresh_hard/report_fresh_hard
```

当前已在 curated real pilot 的 `fresh_hard` split 上完成真实 Judge：

- 输出：`outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl`
- 报告：`outputs/phase4c/deepseek_judge_fresh_hard/report_fresh_hard/summary.json`
- 结果：12 行，12 次 API 调用，0 个错误
- `no_rag` 平均 correctness：1.75，context_support：0.0，hallucination_risk：3.75
- `oracle_context` 平均 correctness：5.0，context_support：5.0，faithfulness：4.75
- `lexical_rag` 平均 correctness：5.0，context_support：5.0，faithfulness：5.0

这一步把“模型答得像不像”推进到“回答是否被上下文支持、是否忠实”的辅助评测。详细记录见 `docs/verification/deepseek-judge-eval.md`。

## Phase 5A: FlashRAG 真实 Dataset runtime intake

第五阶段 A 从“只生成 FlashRAG 兼容文件”推进到“真实 FlashRAG 上游代码能读取 DomainRAG bundle”。当前在 ignored 的本地 checkout 中重新 clone 了 FlashRAG：

```text
benchmark/flashrag-fork/
```

该路径不提交进仓库。当前 upstream commit：

```text
e0e73399ce8d4563397b5fb4980de72a9c5e15a6
```

新增校验模块和脚本：

```text
benchmark/domainrag/flashrag_runtime_intake.py
scripts/verify_flashrag_runtime_intake.py
```

真实运行命令：

```bash
python scripts/verify_flashrag_runtime_intake.py \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy \
  --dataset-name real_pilot_nickel_superalloy \
  --output outputs/phase5a/flashrag_runtime_intake/real_pilot_nickel_superalloy_manifest.json \
  --splits dev,test,fresh_hard
```

当前结果：

- FlashRAG `flashrag.dataset.dataset.Dataset` 可导入并能读取 real pilot bundle
- FlashRAG `flashrag.config.config` 可导入
- `flashrag.utils.utils` 仍因缺少 `transformers` 无法导入
- `dev` / `test` / `fresh_hard` 三个 split 均由真实 FlashRAG `Dataset` 读取成功，各 4 条记录
- manifest：`outputs/phase5a/flashrag_runtime_intake/real_pilot_nickel_superalloy_manifest.json`

这一步不是完整 FlashRAG 多方法实验，但已经把数据层从“格式兼容”推进到“真实上游 Dataset runtime 可读”。详细记录见 `docs/verification/flashrag-runtime-intake.md`。

## Phase 5B: FlashRAG BM25 检索桥接

第五阶段 B 从 Dataset runtime intake 继续推进到真实 FlashRAG 检索组件。当前新增：

- `benchmark/domainrag/flashrag_bm25_bridge.py`
- CLI：`run-flashrag-bm25`
- 输出回归测试：`tests/test_flashrag_bm25_bridge.py`、`tests/test_phase5b_outputs.py`
- 验证记录：`docs/verification/flashrag-bm25-bridge.md`

该阶段使用真实 FlashRAG 上游 checkout 中的：

- `flashrag.dataset.dataset.Dataset`
- `flashrag.retriever.index_builder.Index_Builder`
- `flashrag.retriever.retriever.BM25Retriever`

真实运行命令示例：

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-flashrag-bm25 \
  --flashrag-path benchmark/flashrag-fork \
  --dataset-bundle outputs/flashrag/real_pilot_nickel_superalloy \
  --output outputs/phase5b/flashrag_bm25_bridge \
  --dataset-name real_pilot_nickel_superalloy \
  --split fresh_hard \
  --top-k 5 \
  --index-dir outputs/phase5b/flashrag_bm25_bridge/index \
  --rebuild-index
```

方法名是：

```text
flashrag_bm25_oracle_reader
```

这个名字是有意为之：该阶段已经用真实 FlashRAG Dataset 和 BM25Retriever 做检索，但答案仍是检索命中后的 deterministic oracle reader，不是完整 FlashRAG generator pipeline。

当前在 curated real pilot 上完成 `dev` / `test` / `fresh_hard` 三个 split：

- 每个 split 4 道题
- `retrieval_hit`、`retrieval_recall`、`retrieval_mrr` 均为 1.0
- 输出：`outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/*_flashrag_bm25_results.jsonl`
- 报告：`outputs/phase5b/flashrag_bm25_bridge/report_*/summary.json`
- BM25s 索引：`outputs/phase5b/flashrag_bm25_bridge/index/bm25/`

同时对 `fresh_hard` 的 4 条 Phase 5B 输出完成 DeepSeek Judge：

- 输出：`outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl`
- 报告：`outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/report_fresh_hard/summary.json`
- 4 次 API 调用，0 个错误，0 个 unsupported claims
- correctness、context_support、faithfulness、relevance 均为 5.0

这些高分来自小规模 pilot 和 oracle reader，应作为“FlashRAG BM25 检索桥和 DomainRAG 报告/Judge schema 已接通”的证据，而不是最终规模化方法结论。

## Phase 5C: FlashRAG BM25 检索上下文 + DeepSeek 真实回答

第五阶段 C 把 Phase 5B 的 oracle reader 替换为真实 DeepSeek 回答生成。当前新增：

- `run-deepseek-answers --retrieval-results`
- live 方法名：`flashrag_bm25_live_deepseek`
- 输出回归测试：`tests/test_phase5c_outputs.py`
- 验证记录：`docs/verification/flashrag-bm25-live-answer.md`

运行命令示例：

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy \
  --output outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard \
  --methods flashrag_bm25_live_deepseek \
  --split fresh_hard \
  --retrieval-results outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl \
  --max-retries 1
```

`--retrieval-results` 消费 Phase 5B 的 BM25 检索输出，从中读取 `retrieved_context_ids`，再由当前数据集的 `corpus.jsonl` 拼接上下文交给 DeepSeek 生成答案。这样避免继续使用 oracle reader，同时复用 Phase 4B/4C 已验证的 live answer 和 Judge schema。

当前在 curated real pilot 的 `fresh_hard` split 上完成真实运行：

- 输出：`outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl`
- 报告：`outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard/report_fresh_hard/summary.json`
- 4 道题，4 次 answer API 调用，0 个错误
- `retrieval_hit`、`retrieval_recall`、`retrieval_mrr` 均为 1.0
- 单选、多选、填空规则指标为 1.0；简答 token F1 为 0.7895

随后对该输出完成 DeepSeek Judge：

- 输出：`outputs/phase5c/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl`
- 报告：`outputs/phase5c/deepseek_judge_flashrag_bm25_live_fresh_hard/report_fresh_hard/summary.json`
- 4 次 Judge API 调用，0 个错误，0 个 unsupported claims
- correctness、context_support、faithfulness、relevance 均为 5.0
- hallucination_risk 为 0.0

这一步暴露并修复了一个真实 prompt 风险：过宽的上下文回答会加入未直接支持的因果表述，过窄的多选约束又会导致空答案。当前 prompt 明确要求只使用检索上下文中陈述的事实，同时允许多选题的正确选项由不同检索 chunk 分别支持。

## Phase 5D: Fresh-Hard 横向对比榜

第五阶段 D 把分散在 Phase 4B/4C、Phase 5B、Phase 5C 的 fresh_hard 输出合并成统一 comparison report。当前新增：

- `benchmark/domainrag/comparison_report.py`
- CLI：`compare`
- 输出回归测试：`tests/test_comparison_report.py`、`tests/test_phase5d_outputs.py`
- 验证记录：`docs/verification/fresh-hard-comparison-leaderboard.md`

运行命令示例：

```bash
PYTHONPATH=benchmark python -m domainrag.cli compare \
  --answer-inputs \
    outputs/phase4b/live_deepseek_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
    outputs/phase5b/flashrag_bm25_bridge/real_pilot_nickel_superalloy/fresh_hard_flashrag_bm25_results.jsonl \
    outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --judge-inputs \
    outputs/phase4c/deepseek_judge_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
    outputs/phase5b/deepseek_judge_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
    outputs/phase5c/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/phase5d/fresh_hard_comparison
```

输出：

- `outputs/phase5d/fresh_hard_comparison/summary.json`
- `outputs/phase5d/fresh_hard_comparison/summary.md`

当前 comparison report 覆盖：

- `no_rag`
- `oracle_context`
- `lexical_rag`
- `flashrag_bm25_oracle_reader`
- `flashrag_bm25_live_deepseek`

Leaderboard 直接汇总 answer metrics、retrieval metrics、DeepSeek Judge metrics、token 数、API 调用、错误数和 unsupported claims。当前核心结论：

- `no_rag` 的 context_support 为 0.0，hallucination_risk 为 3.75，unsupported claims 为 5
- 所有上下文方法的 retrieval_hit 都是 1.0，但这是小规模 pilot 的结果
- `flashrag_bm25_live_deepseek` 是当前第一条“FlashRAG 检索 + 非 oracle live answer + Judge”完整链路，fresh_hard 上 correctness、context_support、faithfulness、relevance 均为 5.0，unsupported claims 为 0

`answer_score` 是非检索规则指标的便捷均值，不应替代分题型指标或 Judge 指标。

## Phase 5E: FlashRAG 方法可行性和人工校准包

第五阶段 E 处理两个 Phase 5D 后仍然缺失的交付点：当前运行环境是否适合继续上 dense/rerank，以及 DeepSeek Judge 结果如何进入人工校准。当前新增：

- `benchmark/domainrag/flashrag_method_feasibility.py`
- `benchmark/domainrag/calibration_packet.py`
- CLI：`probe-flashrag-methods`
- CLI：`calibration-packet`
- 脚本：`scripts/verify_flashrag_method_feasibility.py`
- 输出回归测试：`tests/test_flashrag_method_feasibility.py`、`tests/test_calibration_packet.py`、`tests/test_phase5e_outputs.py`
- 验证记录：`docs/verification/flashrag-method-feasibility-and-calibration.md`

FlashRAG 方法可行性探测命令：

```bash
PYTHONPATH=benchmark python -m domainrag.cli probe-flashrag-methods \
  --flashrag-path benchmark/flashrag-fork \
  --output outputs/phase5e/flashrag_method_feasibility/real_pilot_nickel_superalloy_manifest.json
```

当前 manifest 记录：

- FlashRAG commit：`e0e73399ce8d4563397b5fb4980de72a9c5e15a6`
- `flashrag.dataset.dataset`、`flashrag.retriever.retriever`、`flashrag.retriever.index_builder` 可导入
- `flashrag.pipeline.pipeline` 缺少 `termcolor`
- `flashrag.generator.generator` 缺少 `openai`
- `sentence_transformers`、`FlagEmbedding`、`sklearn` 缺失
- 当前 `torch` 是 `2.1.2+cu121`，当前 `transformers` 是 `5.12.1`；该 transformers 构建要求 PyTorch >= 2.4
- `flashrag_bm25` 当前可行，`flashrag_dense` 和 `flashrag_reranker` 当前不可行

因此本阶段没有盲目升级 PyTorch 或安装 dense/rerank 依赖；建议把 dense/rerank 放到独立依赖计划中处理。

人工校准包生成命令：

```bash
PYTHONPATH=benchmark python -m domainrag.cli calibration-packet \
  --dataset data/real_pilot_nickel_superalloy \
  --answers outputs/phase5c/live_deepseek_flashrag_bm25_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_deepseek_results.jsonl \
  --judge outputs/phase5c/deepseek_judge_flashrag_bm25_live_fresh_hard/real_pilot_nickel_superalloy/fresh_hard_judge_results.jsonl \
  --output outputs/phase5e/human_calibration_fresh_hard \
  --split fresh_hard
```

输出：

- `outputs/phase5e/human_calibration_fresh_hard/review_packet.jsonl`
- `outputs/phase5e/human_calibration_fresh_hard/review_packet.md`

当前校准包覆盖 `fresh_hard` 的 4 道 `flashrag_bm25_live_deepseek` 题，包含问题、预测、gold answer、gold/retrieved context id、实际检索 chunk 内容、answer metrics、DeepSeek Judge 分数、风险优先级和空的 `human_review` 字段。当前 4 行均为 normal priority，Judge faithfulness 均为 5.0，hallucination_risk 均为 0.0。

## Phase 6A: 真实 pilot 数据规模扩展

第六阶段 A 开始处理 RAG.md 中最大的剩余缺口：真实数据规模。当前没有直接跳到标准版 5,000+ chunk，而是先构造一个可复现的中间规模扩展包，用于后续 live answer / Judge / calibration 复跑。

新增：

- 扩展 source manifest：`data/real_pilot_sources/nickel_superalloy_high_temp_failure_expanded/sources.jsonl`
- 扩展 Easy Dataset 风格输入：`fixtures/easy_dataset/real_pilot_nickel_superalloy_expanded/`
- 构建脚本：`scripts/build_real_pilot_expanded.py`
- 扩展 DomainRAG 数据集：`data/real_pilot_nickel_superalloy_expanded/`
- 扩展 FlashRAG bundle：`outputs/flashrag/real_pilot_nickel_superalloy_expanded/`
- fresh_hard 离线 baseline：`outputs/phase6a/expanded_baseline/`
- 验证记录：`docs/verification/expanded-real-pilot-scale.md`

构建命令：

```bash
python scripts/build_real_pilot_expanded.py
PYTHONPATH=benchmark python -m domainrag.cli validate-data --dataset data/real_pilot_nickel_superalloy_expanded
```

当前扩展数据集规模：

- 17 个 corpus chunk
- 24 道题
- `dev` / `test` / `fresh_hard` 各 8 道
- 单选、多选、填空、简答各 6 道
- 内部 source manifest 覆盖 15 条真实来源记录

生成 FlashRAG bundle：

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_expanded
```

离线 fresh_hard baseline：

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/phase6a/expanded_baseline \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard

PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/phase6a/expanded_baseline/real_pilot_nickel_superalloy_expanded/fresh_hard_results.jsonl \
  --output outputs/phase6a/expanded_baseline/report_fresh_hard
```

当前 expanded fresh_hard 结果：

- 8 道题
- Fresh-Hard diagnostic candidates：6
- `no_rag` retrieval_hit：0.0
- `oracle_context` retrieval_hit：1.0
- `lexical_rag` retrieval_hit：1.0

这说明 17 个 chunk 仍然不足以区分 lexical/BM25/dense 方法，但已经把项目从最小 9 chunk pilot 推进到可复跑的中间规模数据资产。下一步应在该 expanded split 上运行 live DeepSeek answer、DeepSeek Judge、comparison 和 calibration packet。

## 数据安全约束

公开数据中只保留数据集内部需要的 ID 和证据关系，不导出论文身份元数据。校验器会拒绝 DOI、作者、venue、页码、原始 PDF 路径、原始论文标题等字段。

`answer` 在所有题型中都统一使用数组，包括填空题。选择题答案必须对应合法选项，多选题必须至少包含两个不同的正确选项。

## 下一阶段建议

建议下一阶段优先在扩展版数据集上复跑真实模型链路，并把 dense/rerank 作为独立环境任务处理：

- 在 `data/real_pilot_nickel_superalloy_expanded` 上运行 live DeepSeek answer、DeepSeek Judge、comparison 和 calibration packet
- 继续扩大真实文献 corpus 和问题规模；当前 17 个 chunk 对 lexical retrieval 仍然过于容易
- 对 expanded `review_packet.md` 做人工抽检，形成少量校准样例，避免单一 LLM Judge 偏差被误当作最终结论
- 如果要推进 dense retriever / reranker，先新建隔离环境或明确依赖升级方案，再接入同一套 live answer + Judge 口径
