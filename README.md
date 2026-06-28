# DomainRAG-Bench

DomainRAG-Bench 是一个面向专业领域 RAG 测评的数据契约、数据生产适配和基准评测流水线项目。它把上游的 Easy Dataset 风格数据生产、DomainRAG 标准数据契约、FlashRAG 检索/数据接口、DeepSeek 真实回答与 Judge、人工校准和文献来源筛选连接成一条可复现的研究流程。

当前实现领域是“镍基高温合金高温失效”。最新仓库里程碑是 **Phase 7I manual finalization packet checkpoint**：

- 当前最佳验证数据集：`data/real_pilot_nickel_superalloy_medium_plus/`
- 当前公开 benchmark 规模：100 个 corpus chunks / 150 道问题
- split：50 dev / 50 test / 50 fresh_hard
- 题型：38 single_choice / 38 multiple_choice / 37 fill_blank / 37 short_answer
- Phase 7D 文献候选池：124 篇候选文献，覆盖 8 个子方向
- Phase 7F provisional whitelist：115 条候选来源，其中 104 条研究型候选、11 条综述型候选
- Phase 7G OpenAlex 元数据：115/115 找到记录，0 条 OpenAlex retracted
- Phase 7H 全文探测：115 条 provisional whitelist 全覆盖，其中 71 条 parseable，37 条 not accessible，6 条 download failed，1 条 download truncated
- Phase 7H 机器辅助验证矩阵：2 条 verified source candidate，106 条 ready for manual finalization，7 条 rejected verification，0 条 final accepted
- Phase 7I 人工终审包：115 条 manual finalization packet，108 条 candidate final whitelist queue，候选队列落在 RAG.md 100-180 来源目标范围内
- 当前停点：`phase7i_human_review_packet_not_final`

需要明确的是：Phase 7I 是人工终审 handoff packet，不是最终人工签核结果。项目还没有宣称完成最终人工验证的 100-180 篇文献白名单、1,000-3,000 chunks、300-500 questions、chunk extraction 流水线或 dense/rerank 正式 benchmark。

## 项目流水线

端到端流程如下：

```text
目标领域和文献策略
  -> 文献来源收集和人工/机器预筛
  -> Easy Dataset 风格数据生产
  -> chunks.jsonl + items.jsonl
  -> DomainRAG export-domainrag 转换
  -> validate-data 数据契约校验
  -> FlashRAG bundle 准备
  -> no_rag / oracle_context / lexical_rag / BM25 检索评测
  -> DeepSeek live answer
  -> DeepSeek Judge
  -> comparison report
  -> human calibration audit
  -> RAG.md completion audit 和阶段报告
```

其中 source-side 扩展流程单独记录：

```text
OpenAlex source acquisition
  -> 124-paper candidate pool
  -> machine screening queue
  -> provisional source decisions
  -> 115-row provisional whitelist
  -> OpenAlex metadata refresh
  -> 25-row full-text access probe
  -> 115-row full-text access probe
  -> machine-assisted verification matrix
  -> manual finalization packet
  -> phase7i_human_review_packet_not_final
```

这条线的目的不是直接生成最终数据，而是先把“来源是否足够、是否可访问、是否覆盖子方向、是否需要人工核验”做成可审查资产。

## 输入是什么

项目接受几类输入。

**1. Easy Dataset 风格导出**

最核心的上游输入是：

```text
chunks.jsonl
items.jsonl
```

当前样例和真实 pilot 输入在：

```text
fixtures/easy_dataset/
```

`chunks.jsonl` 提供语料块：

```json
{"id": "chunk_id", "content": "chunk text"}
```

`items.jsonl` 提供题目和证据关联，必须包含问题、题型、答案、split、`source_chunk_ids`、子领域、知识类型、难度和质量分。`source_chunk_ids` 是 qrels 的来源，也是判断 RAG 是否真的检索到证据的关键字段。

**2. DomainRAG 标准数据集**

转换后的标准输入位于：

```text
data/<dataset_name>/
```

每个数据集包含：

```text
corpus.jsonl
canonical_dataset.jsonl
dev.jsonl
test.jsonl
fresh_hard_test.jsonl
qrels/dev.tsv
qrels/test.tsv
qrels/fresh_hard.tsv
dataset_card.md
statistics.json
```

**3. 文献来源和候选池**

内部 source manifest 和候选池用于溯源、扩展和人工核验：

```text
data/real_pilot_sources/
outputs/phase7d/demo_scale_source_acquisition/
outputs/phase7e/source_screening_queue/
outputs/phase7f/source_decisions/
outputs/phase7g/
outputs/phase7h/
outputs/phase7i/
```

公开 benchmark 数据不携带 DOI、作者、venue、页码、原始 PDF 路径或论文题目等来源元数据；这些只留在内部 source-side 文件中。

**4. DeepSeek API key**

真实 DeepSeek answer/Judge 运行只从环境变量读取：

```text
DEEPSEEK_API_KEY
```

测试不会调用真实 DeepSeek API，仓库也不保存任何 API key。

## 输出是什么

主要输出分为六类。

| 输出类别 | 位置 | 用途 |
| --- | --- | --- |
| DomainRAG 数据集 | `data/real_pilot_nickel_superalloy_medium_plus/` | 标准 benchmark 输入 |
| Easy Dataset fixtures | `fixtures/easy_dataset/` | 上游导出样例和真实 pilot 输入 |
| FlashRAG bundle | `outputs/flashrag/` | FlashRAG 兼容数据包 |
| benchmark 结果 | `outputs/phase*/` | 检索、回答、Judge、comparison、calibration 输出 |
| 报告和审计 | `docs/reports/`、`docs/verification/` | 项目状态、验证记录、RAG.md 对照 |
| source-side 包 | `outputs/phase7d/`、`outputs/phase7e/`、`outputs/phase7f/`、`outputs/phase7g/`、`outputs/phase7h/`、`outputs/phase7i/` | 文献候选、筛选队列、provisional decisions、机器辅助来源验证、全文探测和人工终审包 |

最新核心报告是：

```text
docs/reports/domainrag-medium-pilot-final-report.md
docs/reports/rag-md-implementation-audit.json
docs/verification/source-decisions-and-stop-point.md
docs/verification/source-verification-and-full-text-intake.md
docs/verification/full-text-intake-combined115.md
docs/verification/manual-finalization-packet.md
```

## 研究这个项目应重点看哪里

建议按下面顺序阅读。

| 目的 | 重点文件或目录 |
| --- | --- |
| 快速理解项目状态 | `README.md`、`docs/reports/domainrag-medium-pilot-final-report.md` |
| 对照原始需求 | `/root/autodl-tmp/RAG/RAG.md`、`docs/reports/rag-md-implementation-audit.json` |
| 理解数据格式 | `docs/data-contract.md`、`benchmark/domainrag/schema.py`、`benchmark/domainrag/validator.py` |
| 理解 Easy Dataset 如何接入 | `benchmark/domainrag/easy_dataset_adapter.py`、`integrations/easy-dataset/domainrag-export/`、`fixtures/easy_dataset/` |
| 理解 FlashRAG 路径 | `benchmark/domainrag/flashrag_adapter.py`、`benchmark/domainrag/flashrag_runtime_intake.py`、`benchmark/domainrag/flashrag_bm25_bridge.py` |
| 理解检索和评测 | `benchmark/domainrag/benchmark_runner.py`、`benchmark/domainrag/bm25s_retrieval.py`、`benchmark/domainrag/domain_evaluator.py`、`benchmark/domainrag/comparison_report.py` |
| 理解 DeepSeek answer/Judge | `benchmark/domainrag/deepseek_answer_runner.py`、`benchmark/domainrag/deepseek_judge_runner.py`、`benchmark/domainrag/deepseek_pipeline.py` |
| 理解人工校准 | `benchmark/domainrag/calibration_packet.py`、`benchmark/domainrag/calibration_audit.py`、`outputs/phase6f/` |
| 理解文献来源路线 | `benchmark/domainrag/source_acquisition.py`、`benchmark/domainrag/source_screening.py`、`benchmark/domainrag/source_decisions.py`、`outputs/phase7f/source_decisions/` |
| 看可复现命令 | `docs/verification/*.md`、`scripts/` |
| 看测试保障 | `tests/` |

## 如何复现当前核心状态

在仓库根目录执行：

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_medium_plus

PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output outputs/local_readme_check \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard

PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_medium_plus \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_medium_plus

PYTHONPATH=benchmark python -m domainrag.cli decide-sources \
  --screening-queue outputs/phase7e/source_screening_queue/screening_queue.jsonl \
  --output outputs/phase7f/source_decisions

PYTHONPATH=benchmark python -m domainrag.cli verify-sources \
  --whitelist outputs/phase7f/source_decisions/provisional_source_whitelist.jsonl \
  --metadata outputs/phase7g/source_metadata/openalex_metadata.jsonl \
  --access outputs/phase7h/full_text_access_combined115/full_text_access.jsonl \
  --output outputs/phase7h/source_verification_combined115

PYTHONPATH=benchmark python -m domainrag.cli build-finalization-packet \
  --verification-matrix outputs/phase7h/source_verification_combined115/source_verification_matrix.jsonl \
  --output outputs/phase7i/manual_finalization_packet

PYTHONPATH=benchmark pytest
```

真实 DeepSeek answer/Judge 运行需要先设置 `DEEPSEEK_API_KEY`，并且不应放进常规测试。

## 如何迁移到另一个领域

迁移时不要先改评测器，先换数据和来源策略。推荐步骤如下。

1. 定义领域和子方向。

   例如从镍基高温合金换到“锂电池热失控”，需要先确定子方向，如材料体系、热安全、气体析出、老化机制、故障诊断、BMS 策略等。

2. 建立来源策略。

   如果只做小 pilot，可以先创建新的 source manifest：

   ```text
   data/real_pilot_sources/<new_domain>/sources.jsonl
   ```

   如果要走 OpenAlex 扩展，需要复制或修改：

   ```text
   benchmark/domainrag/source_acquisition.py
   ```

   重点替换：

   - `DOMAIN_FLAGSHIP_VENUES`
   - `DOMAIN_RELEVANCE_TERMS`
   - `DEFAULT_SUBTOPIC_QUERIES`

3. 生成 Easy Dataset 风格输入。

   创建：

   ```text
   fixtures/easy_dataset/<new_domain>/chunks.jsonl
   fixtures/easy_dataset/<new_domain>/items.jsonl
   ```

   每道题必须有 `source_chunk_ids`，否则不能形成 qrels，也无法严肃评测检索。

4. 转换为 DomainRAG 数据集。

   ```bash
   PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
     --input fixtures/easy_dataset/<new_domain> \
     --output data \
     --dataset-name <new_domain>
   ```

5. 校验数据契约。

   ```bash
   PYTHONPATH=benchmark python -m domainrag.cli validate-data \
     --dataset data/<new_domain>
   ```

6. 准备 FlashRAG bundle。

   ```bash
   PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
     --dataset data/<new_domain> \
     --output outputs/flashrag \
     --dataset-name <new_domain>
   ```

7. 先跑离线基线。

   ```bash
   PYTHONPATH=benchmark python -m domainrag.cli run \
     --dataset data/<new_domain> \
     --output outputs/<new_domain> \
     --methods no_rag,oracle_context,lexical_rag \
     --split fresh_hard
   ```

   只有当 Fresh-Hard 中出现“no_rag 低、oracle_context 高、RAG 方法受检索影响”的题目时，这个领域数据才开始有 RAG 评测价值。

8. 再跑受控 live DeepSeek 子集。

   live answer 和 Judge 应先跑小样本，确认提示词、上下文拼接、题型评分和错误处理稳定后再扩大。

9. 做人工校准。

   对 Judge 结果抽样人工复核，特别关注 partial evidence、unsupported claims 和模型是否引入上下文外推断。

10. 最后再扩展到 demo-scale。

   先做 source acquisition / screening / decisions，再做全文解析、chunk extraction 和 question generation。不要用未经人工核验的 provisional whitelist 直接宣称最终来源白名单。

## 如何保证严谨性

项目的严谨性不来自单一模型分数，而来自多层约束。

- **数据契约约束**：所有公开数据必须通过 `validate-data`，并满足 `docs/data-contract.md`。
- **qrels 约束**：每道题必须能追溯到一个或多个 `source_chunk_ids`。
- **公开元数据安全**：公开 benchmark 不允许 DOI、作者、venue、页码、原始 PDF 路径或论文题目泄露。
- **题型化评分**：单选、多选、填空、短答分别用不同规则评分，不把所有问题混成一个粗略准确率。
- **Fresh-Hard 诊断**：重点看 No-RAG 低、Oracle-Context 高、RAG 受检索影响的问题。
- **多方法对比**：同时看 no_rag、oracle_context、lexical_rag、BM25、live answer，而不是只看一个模型输出。
- **真实 API 与测试隔离**：测试不调用 DeepSeek，真实运行单独记录输出和错误。
- **DeepSeek answer 与 Judge 分离**：生成答案和评分是不同调用，避免同一过程自我确认。
- **人工校准**：Phase 6F 对 Judge 结果做人工抽样审计，记录 Judge 在 partial evidence 上偏保守的风险。
- **来源状态不夸大**：Phase 7D/7E/7F 明确区分 candidate、screening queue、provisional whitelist 和 final inclusion list。
- **可复现证据**：每个阶段都有 `docs/verification/` 记录、`outputs/` 产物和 `tests/` 回归测试。
- **密钥安全**：API key 只从环境变量读取，提交前使用 secret scan。

当前最新验证门：

```text
PYTHONPATH=benchmark pytest -> 242 passed
validate-data real_pilot_nickel_superalloy_medium_plus -> valid
rag-md-implementation-audit.json -> valid JSON
git diff --check -> clean
secret scan -> no matches
```

## Codex 和 DeepSeek API 的角色

**Codex 的角色**

Codex 是这个项目中的工程执行和研究助理，不是 benchmark 里的被测模型。它承担：

- 阅读 `RAG.md` 并拆解阶段计划；
- 编写 Python adapter、CLI、测试、脚本和报告；
- 运行验证命令；
- 维护 README、audit、verification docs；
- 根据输出判断下一步是否应扩大规模；
- 在 Phase 7F 处停止，避免把 provisional 结果说成 final。

Codex 不应该被记入 RAG 方法成绩，也不替代人工文献核验。

**DeepSeek API 的角色**

DeepSeek 是项目中的模型服务，承担三类运行时任务：

- **候选题生成和独立复核**：早期用于从真实 chunks 生成候选题，并用独立复核过滤。
- **live answer**：在 no_rag、oracle_context、lexical_rag、BM25 检索上下文等条件下生成真实答案。
- **DeepSeek Judge**：对答案做 correctness、context_support、faithfulness、relevance、unsupported_claims 等辅助评分。

DeepSeek Judge 不替代规则指标，也不替代人工校准。它是一个辅助评估器，必须和 qrels、检索指标、unsupported claims、人工抽查一起解释。

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

## 历史最小闭环快速复现

下面命令复现最早的 example_domain 最小闭环，不代表当前 Phase 7F 的完整状态：

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

后续阶段同样遵守两个约束：测试不调用真实模型 API，仓库不保存 API key。

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

## Phase 6B: Expanded Fresh-Hard 真实 DeepSeek Answer + Judge

第六阶段 B 在 Phase 6A 的扩展版 `fresh_hard` 上复跑真实模型链路。当前新增：

- live answer 输出：`outputs/phase6b/expanded_live_deepseek_fresh_hard/`
- DeepSeek Judge 输出：`outputs/phase6b/expanded_deepseek_judge_fresh_hard/`
- comparison report：`outputs/phase6b/expanded_fresh_hard_comparison/`
- human calibration packet：`outputs/phase6b/expanded_human_calibration_fresh_hard/`
- 输出回归测试：`tests/test_phase6b_outputs.py`
- 验证记录：`docs/verification/expanded-live-deepseek-eval.md`

真实 answer 命令：

```bash
PYTHONPATH=benchmark python -m domainrag.cli run-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --output outputs/phase6b/expanded_live_deepseek_fresh_hard \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard \
  --max-retries 1
```

DeepSeek Judge 命令：

```bash
PYTHONPATH=benchmark python -m domainrag.cli judge-deepseek-answers \
  --dataset data/real_pilot_nickel_superalloy_expanded \
  --input outputs/phase6b/expanded_live_deepseek_fresh_hard/real_pilot_nickel_superalloy_expanded/fresh_hard_deepseek_results.jsonl \
  --output outputs/phase6b/expanded_deepseek_judge_fresh_hard \
  --split fresh_hard \
  --max-retries 1
```

当前真实运行结果：

- live answer：24 行，27 次 API 调用，0 个错误
- Judge：24 行，24 次 API 调用，0 个错误
- calibration packet：24 行

expanded Fresh-Hard leaderboard：

| method | answer_score | retrieval_hit | correctness | faithfulness | hallucination_risk | api_calls | unsupported_claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lexical_rag | 0.8673 | 1.0000 | 5.0000 | 5.0000 | 0.0000 | 17 | 0 |
| oracle_context | 0.8631 | 1.0000 | 4.8750 | 5.0000 | 0.0000 | 16 | 0 |
| no_rag | 0.1572 | 0.0000 | 1.8750 | 0.7500 | 4.2500 | 18 | 10 |

这一步的主要证据是：扩展版数据上 No-RAG 仍然暴露出明显 hallucination risk 和 unsupported claims，而上下文方法在本轮保持 0 个 unsupported claims。与此同时，lexical retrieval 仍然 saturated，说明下一步若要比较 BM25/dense/rerank，仍需要继续扩大语料或加入更难的干扰 chunk。

## 数据安全约束

公开数据中只保留数据集内部需要的 ID 和证据关系，不导出论文身份元数据。校验器会拒绝 DOI、作者、venue、页码、原始 PDF 路径、原始论文标题等字段。

`answer` 在所有题型中都统一使用数组，包括填空题。选择题答案必须对应合法选项，多选题必须至少包含两个不同的正确选项。

## 下一阶段建议

建议下一阶段优先在扩展版数据集上复跑真实模型链路，并把 dense/rerank 作为独立环境任务处理：

- 在 `data/real_pilot_nickel_superalloy_expanded` 上运行 FlashRAG BM25 bridge，并复用 `flashrag_bm25_live_deepseek` 生成 expanded BM25 live answer
- 继续扩大真实文献 corpus 和问题规模；当前 17 个 chunk 对 lexical/BM25 retrieval 预计仍然过于容易
- 对 expanded `review_packet.md` 做人工抽检，形成少量校准样例，避免单一 LLM Judge 偏差被误当作最终结论
- 如果要推进 dense retriever / reranker，先新建隔离环境或明确依赖升级方案，再接入同一套 live answer + Judge 口径
