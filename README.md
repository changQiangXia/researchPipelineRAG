# DomainRAG-Bench：面向专业领域的可追溯 RAG 测评流水线

DomainRAG-Bench 是一个面向专业领域 RAG 测评的数据生产、标准化、检索评测和审计流水线。它的核心目标是：从领域文献和证据材料出发，构建带有 `gold evidence`（每道题绑定的标准证据块）与 `qrels`（question relevance labels，即问题与相关证据 chunk 的标准关联表）的标准化数据资产，并在同一评测协议下比较不同 RAG 方法的检索、答题、忠实度和效率表现。

当前示例领域是 **镍基高温合金高温失效**。换句话说，当前实现领域是“镍基高温合金高温失效”。这个领域足够专业、知识更新快，适合构造 `Fresh-Hard`（专门测试证据依赖的新近/专业问题 split）问题：基础模型不能完全依赖常识回答，但可以通过领域知识库回答。

当前仓库已经形成一条流水线：从 Easy Dataset 风格输入，到 DomainRAG 标准数据集，再到 FlashRAG bundle、本地检索 baseline、DeepSeek answer/Judge、人工审核 workflow 和结构化审计。当前数据集仍是 `provisional`（工程验证阶段的临时版本），不是 `human-final benchmark`（经过真实人工来源签核、题库复核后才能声明的最终人工验证 benchmark）。

## 项目亮点

- 从领域材料构建 literature-grounded RAG benchmark。
- 使用 Easy Dataset 风格输入：`chunks.jsonl` + `items.jsonl`。
- 定义 DomainRAG 标准数据契约：`corpus.jsonl`、`canonical_dataset.jsonl`、splits 和 `qrels`。
- 每道题绑定 `source_chunk_ids`，保留 `gold evidence` 和 `gold context`。
- 支持 `no_rag`、`oracle_context`、`lexical_rag`、BM25、hashed dense 等诊断基线。
- 支持 `Fresh-Hard` split，用于测试模型在新近、专业证据上的依赖程度。
- 可导出 FlashRAG-compatible bundle，让同一批数据进入下游 RAG benchmark 生态。
- 集成 DeepSeek answer/Judge 路径，但明确不替代人工最终签核。
- 保留候选文献筛选、来源审核、全文解析、人工 sign-off workflow 和结构化审计记录。

## 当前示例领域：镍基高温合金高温失效

当前实现领域是：

```text
镍基高温合金高温失效
```

该领域覆盖氧化、蠕变、疲劳、热腐蚀、涂层、增材制造、组织表征和寿命预测等子方向。项目使用这个领域作为示例，是因为它符合专业 RAG benchmark 的典型条件：

- 领域知识高度专业，普通通用模型容易依赖模糊常识。
- 近年研究持续更新，适合构造 `Fresh-Hard` 问题。
- 问题需要可追溯证据，而不是开放式泛泛回答。
- 研究型文献可以提供机制、参数、实验结果和失败案例。
- 综述型文献可以提供概念体系、技术路线、争议和趋势。

当前公开数据集中不导出 DOI、作者、venue、页码、原始 PDF 路径或论文题目。公开 benchmark 只保留证据 chunk 和内部 `source_chunk_ids`，用于检索评测和 `qrels` 构建。

## 整体技术路线

```text
领域文献 / 证据材料
        |
        v
Easy Dataset 风格输入
chunks.jsonl + items.jsonl
        |
        v
DomainRAG 标准数据集
corpus.jsonl + canonical_dataset.jsonl + splits + qrels
        |
        v
FlashRAG bundle / DomainRAG runner
        |
        v
RAG 方法对比
no_rag / oracle_context / lexical_rag / BM25 / dense diagnostics
        |
        v
Answer、Judge、reports、audit、human sign-off workflow
```

这条流水线的核心设计是把“生成题库”和“评测 RAG”之间的接口固定下来。只要一个新领域能提供 Easy Dataset 风格输入，就可以转换成 DomainRAG 标准数据集，再进入统一的评测和报告流程。

## 当前已形成的产物

| 产物 | 位置 | 当前状态 |
| --- | --- | --- |
| provisional 300 题数据集 | `data/real_pilot_nickel_superalloy_demo_questions/` | 100 chunks / 300 questions |
| medium-plus pilot 数据集 | `data/real_pilot_nickel_superalloy_medium_plus/` | 100 chunks / 150 questions |
| FlashRAG bundle | `outputs/flashrag/real_pilot_nickel_superalloy_demo_questions/` | 可作为 FlashRAG 风格输入 |
| 当前输出导航 | `outputs/current/` | 面向读者的成果摘要 |
| 历史运行证据 | `outputs/archive/provenance/` | 按产物类型收束，不再按 phase 展示 |
| 全文 chunk manifests | `outputs/current/full_text_chunks.md` | 2,196 条 machine-parseable chunk manifests |
| 来源审核 workflow | `outputs/current/source_review.md` | 108 条 pending human sign-off candidates |
| 结构化审计 | `docs/reports/rag-md-implementation-audit.json` | 对照 `RAG.md` 的状态记录 |

当前状态：

```text
工程流水线：基本完成
严格 human-final benchmark：等待真实人工审核
```

## 当前评测快照

当前 provisional 300 题数据集的 `Fresh-Hard` split 结果摘要如下：

| method | questions | retrieval_hit | retrieval_recall | api_calls |
| --- | ---: | ---: | ---: | ---: |
| `no_rag` | 100 | 0.0000 | 0.0000 | 0 |
| `oracle_context` | 100 | 1.0000 | 1.0000 | 0 |
| `lexical_rag` | 100 | 0.7200 | 0.7200 | 0 |
| `hashed_dense_oracle_reader` | 100 | 0.7000 | 0.7000 | 0 |
| `hashed_dense_lexical_rerank_oracle_reader` | 100 | 0.7200 | 0.7200 | 0 |

这张表的读法：

- `no_rag` 测试没有检索上下文时的表现。
- `oracle_context` 直接提供 `gold context`，用于判断题目是否能被证据回答。
- `lexical_rag` 测试普通词面检索能否找到 `gold evidence`。
- hashed dense 是本地 non-neural 诊断基线，不是 FlashRAG neural dense/reranker（使用神经向量检索器或重排器的 FlashRAG 方法）结果。

`oracle_context` 与检索方法之间的差距很关键：它把“题目本身可由证据回答”和“检索器是否真的找到了证据”分开看。

详细结果见：

```text
outputs/current/benchmark_results.md
```

## 核心概念

**Easy Dataset 风格**

在本仓库中，Easy Dataset 风格指一种上游数据生产和导出形状，而不是强制依赖 Easy Dataset 应用本体：

```text
chunks.jsonl
items.jsonl
```

`chunks.jsonl` 存放证据文本块。`items.jsonl` 存放题目、答案、题型、split 和证据引用。

**DomainRAG 标准数据集**

DomainRAG 将 Easy Dataset 风格输入转换为稳定的标准 benchmark 数据契约：

```text
corpus.jsonl
canonical_dataset.jsonl
dev.jsonl
test.jsonl
fresh_hard_test.jsonl
qrels/*.tsv
```

这个契约由 validators、runners、reports 和 FlashRAG adapters 共同遵守。

**FlashRAG**

FlashRAG 是下游 RAG benchmark 框架。本项目会把 DomainRAG 标准数据集导出为 FlashRAG-compatible bundle，让同一批数据进入更通用的 RAG 实验生态。

**gold evidence**

`gold evidence` 是题目绑定的标准证据块，在数据中表现为 `source_chunk_ids`。

**qrels**

`qrels` 将 question id 与相关 corpus chunk id 连接起来，用于计算 retrieval hit、recall 和 MRR。

**gold context**

`gold context` 是由 `qrels` 指向的真实证据文本。`oracle_context` 会直接使用这部分上下文。

**Fresh-Hard**

`Fresh-Hard` 是用于压力测试证据依赖的 split。理想情况下，这类问题不能稳定依赖常识答对，但可以在给定正确证据时被回答。

**三种诊断基线**

- `no_rag`：不给检索上下文。
- `oracle_context`：直接提供 gold context，也就是标准证据上下文。
- `lexical_rag`：从 corpus 中做词面检索。

这三种方法组合起来，可以区分问题是出在题目设计、检索命中，还是答案生成。

## 输入与输出示例

### Corpus chunk

文件：

```text
data/real_pilot_nickel_superalloy_demo_questions/corpus.jsonl
```

示例：

```json
{"id": "ns_ht_oxidation_gb_energy_001", "contents": "Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries."}
```

### Canonical question

文件：

```text
data/real_pilot_nickel_superalloy_demo_questions/canonical_dataset.jsonl
```

示例：

```json
{"id": "real_pilot_nickel_superalloy_demo_questions_q0001", "question_type": "single_choice", "question": "Which statement is directly supported by the evidence chunk?", "options": {"A": "Initial oxidation in Inconel 718 can depend on grain-boundary character.", "B": "The evidence is about dataset bookkeeping rather than materials behavior.", "C": "The evidence says the mechanism is unrelated to high-temperature exposure.", "D": "The evidence only describes API retry settings."}, "answer": ["A"], "source_chunk_ids": ["ns_ht_oxidation_gb_energy_001"], "difficulty": "easy", "quality_score": 0.7}
```

这里的 `source_chunk_ids` 就是 `gold evidence`，说明这道题的标准证据来自哪个 corpus chunk。

### Qrels row

文件：

```text
data/real_pilot_nickel_superalloy_demo_questions/qrels/fresh_hard.tsv
```

示例：

```text
real_pilot_nickel_superalloy_demo_questions_q0201	ns_ht_oxidation_lpbf_gh3536_001	1
```

这表示某个 question 与某个 corpus chunk 是标准相关关系，相关分数为 `1`。

### 输出入口

当前成果报告：

```text
outputs/README.md
outputs/current/README.md
```

历史运行（存档备份）：

```text
outputs/archive/provenance/
```


## 仓库导览

| 目的 | 路径 |
| --- | --- |
| DomainRAG 核心代码 | `benchmark/domainrag/` |
| 数据 schema 与校验 | `benchmark/domainrag/schema.py`、`benchmark/domainrag/validator.py` |
| 数据契约说明 | `docs/data-contract.md` |
| 当前 300 题数据集 | `data/real_pilot_nickel_superalloy_demo_questions/` |
| medium-plus pilot 数据集 | `data/real_pilot_nickel_superalloy_medium_plus/` |
| FlashRAG bundles | `outputs/flashrag/` |
| 面向读者的当前输出 | `outputs/current/` |
| 历史运行证据 | `outputs/archive/provenance/` |
| RAG.md 实现审计 | `docs/reports/rag-md-implementation-audit.json` |
| 测试 | `tests/` |

## 快速运行

从仓库根目录执行。

验证当前 provisional 300 题数据集：

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_demo_questions
```

运行 `Fresh-Hard` 本地 baseline：

```bash
PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/local_readme_check \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard
```

生成报告：

```bash
PYTHONPATH=benchmark python -m domainrag.cli report \
  --input outputs/local_readme_check/real_pilot_nickel_superalloy_demo_questions/fresh_hard_results.jsonl \
  --output outputs/local_readme_check/report_fresh_hard
```

准备 FlashRAG bundle：

```bash
PYTHONPATH=benchmark python -m domainrag.cli prepare-flashrag \
  --dataset data/real_pilot_nickel_superalloy_demo_questions \
  --output outputs/flashrag \
  --dataset-name real_pilot_nickel_superalloy_demo_questions
```

运行测试：

```bash
PYTHONPATH=benchmark pytest
```

## 领域迁移

迁移时优先换数据，不要先改评测器。

1. 定义目标领域和 5-8 个子主题。
2. 准备研究型文献和综述型文献的来源策略。
3. 构建或导出 Easy Dataset 风格的 `chunks.jsonl` 和 `items.jsonl`。
4. 转换为 DomainRAG 标准数据集。
5. 运行 `validate-data`。
6. 运行 `no_rag`、`oracle_context`、`lexical_rag`。
7. 增加 FlashRAG/BM25 或 dense retrieval 路径。
8. 小样本本地 baseline 稳定后，再接入 DeepSeek answer/Judge。
9. **做人工校准和来源签核，再声明最终 benchmark**。

研究型文献和综述型文献在工作流中的作用不同（后续将逐步使用全综述型文献）：

| 来源类型 | 主要作用 |
| --- | --- |
| 研究型文献 | 机制、实验条件、参数、结果、失败案例 |
| 综述型文献 | 概念结构、分类体系、技术路线、争议、趋势 |

新领域不需要复制镍基高温合金主题，但必须保留证据契约：每道题都要指向 source chunks，每个相关 chunk 都要能通过 `qrels` 被检索评测使用。

最小迁移闭环：

```bash
PYTHONPATH=benchmark python -m domainrag.cli export-domainrag \
  --input fixtures/easy_dataset/<new_domain> \
  --output data \
  --dataset-name <new_domain>

PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/<new_domain>

PYTHONPATH=benchmark python -m domainrag.cli run \
  --dataset data/<new_domain> \
  --output outputs/<new_domain> \
  --methods no_rag,oracle_context,lexical_rag \
  --split fresh_hard
```

## 严谨性与当前边界

这个项目的严谨性来自显式证据绑定和可审计流程。

已经具备的约束包括：

- 每道题必须有 `source_chunk_ids`。
- 检索结果通过 `qrels` 评测。
- `no_rag`、`oracle_context` 和检索基线分离不同失败模式。
- `Fresh-Hard` split 测试证据依赖。
- 公开数据不泄露 DOI、作者、venue、页码、原始 PDF 路径和论文题目。
- DeepSeek answer/Judge 记录 API 使用和错误状态。
- 人工 sign-off workflow 与机器筛选明确分离。

当前边界：

- 300 题数据集是 `provisional`，不是 `human-final`。
- 2,196 条全文 chunk manifests 是 machine-parseable 结果，不是 human-final accepted-source corpus。
- 项目已有 human sign-off workflow，但还没有真实人工签核的 100-180 篇最终文献白名单。
- hashed dense 是本地 non-neural 诊断基线。
- FlashRAG neural dense/reranker 仍需要隔离依赖环境正式运行。

因此，当前仓库适合作为可复现 prototype 和研究流水线展示，但不能描述为最终人工验证 benchmark。

## Codex 与 DeepSeek 的分工

**Codex** 负责工程侧工作：

- 阅读和修改仓库代码。
- 实现 adapters、validators、runners 和 reports。
- 维护测试。
- 整理 outputs 和 README。
- 保持可复现性和审计路径。

**DeepSeek API** 作为模型服务使用：

- 题目生成。
- 答案生成。
- Judge 评价。
- 辅助复核。

DeepSeek 不替代 `qrels`、确定性校验器或最终人工来源签核。Codex 也不能替代真实人工 sign-off。

真实 DeepSeek API key 只从环境变量读取：

```text
DEEPSEEK_API_KEY
```

测试不会调用真实 DeepSeek API，仓库也不保存 API key。

## 当前完成状态

| 模块 | 状态 |
| --- | --- |
| 工程流水线 | 基本完成 |
| DomainRAG 数据契约 | 已完成 |
| Easy Dataset 风格输入 | 已完成 |
| FlashRAG bundle 准备 | 已完成 |
| BM25 / lexical / oracle / no-rag baseline | 已完成 |
| DeepSeek answer/Judge 路径 | 已在 pilot 和 bounded subset 上实现 |
| 300 题 provisional 数据集 | 已完成 provisional 版本 |
| 全文 chunk manifests | 已完成 machine-parseable manifests |
| 人工最终文献白名单 | 待完成 |
| human-final benchmark 声明 | 目前不能声明 |
| neural dense/rerank | 待隔离环境正式运行 |

相对于 `RAG.md`，当前工程流水线已经基本打通；严格意义上的最终 benchmark 还需要真实人工来源签核、基于 human-accepted sources 的 chunk 过滤或重建，以及最终题库复核。
