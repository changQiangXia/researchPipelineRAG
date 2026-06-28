# DomainRAG-Bench

DomainRAG-Bench 是一个面向专业领域 RAG 评测的数据生产、数据契约、检索评测和审计流水线项目。它的目标不是做一个孤立 demo，而是把“领域材料 -> 可追溯题库 -> 标准 benchmark 数据集 -> RAG 方法评测 -> 模型回答/Judge -> 人工校准和来源审计”串成一条可复现流程。

当前实现领域是“镍基高温合金高温失效”。这个领域只是示例，项目设计上可以迁移到其他专业领域。

## 三个核心概念

**Easy Dataset**

Easy Dataset 在本项目里指上游数据生产工具或数据生产风格。本仓库不要求读者安装 Easy Dataset；它只约定一种容易导出的输入形状：

```text
chunks.jsonl
items.jsonl
```

`chunks.jsonl` 存放可公开的证据文本块，`items.jsonl` 存放题目、答案、题型、split 和证据引用。只要其他工具能导出这两个文件，也可以接入本项目。

**DomainRAG**

DomainRAG 是本项目定义的标准 benchmark 数据契约。它把 Easy Dataset 风格输入转换成 RAG 评测需要的统一结构：

```text
corpus.jsonl
canonical_dataset.jsonl
dev.jsonl
test.jsonl
fresh_hard_test.jsonl
qrels/*.tsv
```

这个契约的关键是每道题都必须绑定 `source_chunk_ids`，也就是 gold evidence。这样检索是否命中证据、模型是否使用证据回答，都可以被追踪和评分。

**FlashRAG**

FlashRAG 是下游 RAG benchmark 框架。本项目能把 DomainRAG 标准数据集转换成 FlashRAG bundle，让同一批数据进入更标准的 RAG 检索/生成评测生态。当前仓库已经生成 FlashRAG 兼容数据包，并保留了 BM25、hashed dense 等本地评测路径。

一句话关系：

```text
Easy Dataset 风格输入 -> DomainRAG 标准数据集 -> FlashRAG bundle / benchmark runner
```

## 当前示例领域

当前领域是镍基高温合金高温失效。围绕这个领域，仓库已经形成一组可运行产物：

| 产物 | 位置 | 状态 |
| --- | --- | --- |
| 人工策划 medium-plus pilot | `data/real_pilot_nickel_superalloy_medium_plus/` | 100 chunks / 150 questions，已通过数据契约校验 |
| provisional 300 题数据集 | `data/real_pilot_nickel_superalloy_demo_questions/` | 100 chunks / 300 questions，已通过数据契约校验 |
| FlashRAG bundle | `outputs/flashrag/real_pilot_nickel_superalloy_demo_questions/` | 可作为 FlashRAG 数据输入 |
| 当前输出入口 | `outputs/current/` | 给读者看的成果导航 |
| 历史运行记录 | `outputs/archive/provenance/` | 运行证据，不作为第一阅读入口 |
| 项目审计 | `docs/reports/rag-md-implementation-audit.json` | 对照 RAG.md 的结构化状态 |

项目还包含候选文献筛选、全文解析、chunk manifest、检索 benchmark、DeepSeek answer/Judge 和人工校准记录。它们现在被组织为“当前成果入口 + 历史证据归档”，而不是在 `outputs/` 根目录展示一排 phase 目录。

当前必须保留的边界：

- 300 题数据集是 `provisional`，不是 human-final demo benchmark。
- 2,196 条全文 chunk manifest 是 machine-parseable 结果，不是 human-final accepted-source corpus。
- 已有 human sign-off workflow，但没有真实人工签核的 100-180 篇最终文献白名单。
- 本地 hashed dense benchmark 不是 FlashRAG neural dense/reranker。

## 项目流水线

### 1. 数据生产线

```text
领域材料
  -> Easy Dataset 风格导出: chunks.jsonl + items.jsonl
  -> export-domainrag
  -> DomainRAG 标准数据集
  -> validate-data
```

**Easy Dataset 风格** 指上游数据以 `chunks.jsonl` 和 `items.jsonl` 表达。这个风格足够简单，可以来自 Easy Dataset，也可以来自自定义脚本或人工整理。

**DomainRAG 标准数据集** 是转换后的正式 benchmark 输入。它包含 corpus、canonical questions、split 文件和 qrels。

**gold evidence** 是题目绑定的标准证据块，也就是 `source_chunk_ids`。

**qrels** 是检索评测使用的标准答案表，把 question id 和 gold evidence chunk id 连接起来。

### 2. 评测线

```text
DomainRAG 标准数据集
  -> no_rag / oracle_context / lexical_rag
  -> report
  -> optional DeepSeek answer / Judge
```

三种基础方法的意义：

| 方法 | 含义 | 用途 |
| --- | --- | --- |
| `no_rag` | 不给检索上下文，只让模型或规则基线回答 | 测试题目是否会被常识或猜测答中 |
| `oracle_context` | 直接提供 gold context，也就是 qrels 指向的标准证据 | 测试题目本身是否能由证据回答，是上限参考 |
| `lexical_rag` | 用词面检索从 corpus 中找上下文 | 测试普通检索是否能命中 gold evidence |

如果 `oracle_context` 高、`no_rag` 低，说明题目确实依赖证据。如果 `lexical_rag` 低于 `oracle_context`，瓶颈通常在检索。如果检索命中但答案仍差，瓶颈通常在生成或上下文使用。

### 3. 来源审计线

```text
候选文献
  -> screening queue
  -> provisional source decisions
  -> full-text access / parsing
  -> manual finalization packet
  -> human sign-off labels
  -> final_source_whitelist.jsonl
```

这条线的目的不是自动宣布文献通过，而是把 candidate、provisional、ready for manual finalization 和 accepted_final 明确分开。只有真实人工标签能生成最终文献白名单。

## 输入示例

下面直接使用当前真实数据集中的记录。

### Corpus chunk

文件：`data/real_pilot_nickel_superalloy_demo_questions/corpus.jsonl`

```json
{"id": "ns_ht_oxidation_gb_energy_001", "contents": "Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries."}
```

这是一个可公开的证据 chunk。公开数据里不放 DOI、作者、venue、页码、原始 PDF 路径或论文题目。

### Canonical question

文件：`data/real_pilot_nickel_superalloy_demo_questions/canonical_dataset.jsonl`

```json
{"id": "real_pilot_nickel_superalloy_demo_questions_q0001", "question_type": "single_choice", "question": "Which statement is directly supported by the evidence chunk?", "options": {"A": "Initial oxidation in Inconel 718 can depend on grain-boundary character.", "B": "The evidence is about dataset bookkeeping rather than materials behavior.", "C": "The evidence says the mechanism is unrelated to high-temperature exposure.", "D": "The evidence only describes API retry settings."}, "answer": ["A"], "source_chunk_ids": ["ns_ht_oxidation_gb_energy_001"], "difficulty": "easy", "quality_score": 0.7}
```

这里的 `source_chunk_ids` 就是 gold evidence。它说明这道题的标准证据来自哪个 corpus chunk。

### Qrels row

文件：`data/real_pilot_nickel_superalloy_demo_questions/qrels/fresh_hard.tsv`

```text
real_pilot_nickel_superalloy_demo_questions_q0201	ns_ht_oxidation_lpbf_gh3536_001	1
```

qrels 用于检索评测。它表示某个 question 与某个 corpus chunk 是标准相关关系，相关分数为 `1`。

### Easy Dataset 风格输入

归档中保留了一份 Easy Dataset 风格中间导出：

```text
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/easy_dataset_export/chunks.jsonl
outputs/archive/provenance/demo-dataset/demo-question-generation/demo_question_generation/easy_dataset_export/items.jsonl
```

如果迁移到新领域，最小输入也应先准备这两个文件，再用 `export-domainrag` 或项目内生成器转换成 DomainRAG 标准数据集。

## 主要输出在哪里

先看：

```text
outputs/README.md
outputs/current/README.md
```

`outputs/current/` 是给读者看的当前成果导航。历史阶段运行记录已经移到：

```text
outputs/archive/provenance/
```

不要从历史执行顺序去理解项目。`outputs/archive/provenance/` 已按成果主题收束为若干归档目录，用于复现和审计。

## 快速运行

从仓库根目录执行。

验证当前 provisional 300 题数据集：

```bash
PYTHONPATH=benchmark python -m domainrag.cli validate-data \
  --dataset data/real_pilot_nickel_superalloy_demo_questions
```

运行 Fresh-Hard 本地 baseline：

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

## 如何迁移到另一个领域

迁移时优先换数据，不要先改评测器。

1. 定义领域和子方向。
2. 准备来源策略，区分研究型来源和综述型来源。
3. 生成 Easy Dataset 风格输入：`chunks.jsonl` 和 `items.jsonl`。
4. 转换为 DomainRAG 标准数据集。
5. 跑 `validate-data`。
6. 跑 `no_rag`、`oracle_context`、`lexical_rag`。
7. 只在小样本稳定后再接入 live DeepSeek answer/Judge。
8. 做人工校准和来源签核。

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

## 严谨性边界

项目的严谨性来自几道约束：

- 每道题必须绑定 gold evidence。
- `validate-data` 校验字段、split、qrels 和公开元数据安全。
- 公开 benchmark 不泄露 DOI、作者、venue、页码、原始 PDF 路径或论文题目。
- `no_rag`、`oracle_context`、`lexical_rag` 分别测试无上下文、理想上下文和实际检索。
- DeepSeek answer 和 DeepSeek Judge 是辅助评测，不替代 qrels、规则指标或人工校准。
- human sign-off 只能由真实人工标签完成，不能由 Codex 或 DeepSeek 自动代替。

当前最重要的未完成项：

- 没有最终人工签核的 100-180 篇文献白名单。
- 300 题数据集仍是 provisional，不是 human-final benchmark。
- 全文 chunk manifest 尚未过滤到 human-accepted final sources。
- neural dense/rerank 仍需隔离环境正式运行。

## 重点文件

| 目的 | 文件或目录 |
| --- | --- |
| 理解当前输出 | `outputs/README.md`、`outputs/current/README.md` |
| 理解数据契约 | `docs/data-contract.md`、`benchmark/domainrag/schema.py`、`benchmark/domainrag/validator.py` |
| 查看当前 300 题数据集 | `data/real_pilot_nickel_superalloy_demo_questions/` |
| 查看 FlashRAG bundle | `outputs/flashrag/real_pilot_nickel_superalloy_demo_questions/` |
| 查看结构化审计 | `docs/reports/rag-md-implementation-audit.json` |
| 查看历史运行记录 | `outputs/archive/provenance/` |
| 查看测试 | `tests/` |

## 密钥安全

真实 DeepSeek API key 只从环境变量读取：

```text
DEEPSEEK_API_KEY
```

测试不会调用真实 DeepSeek API，仓库也不保存 API key。
