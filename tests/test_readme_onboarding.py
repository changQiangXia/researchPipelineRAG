from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_introduces_easy_dataset_domainrag_and_flashrag():
    readme = README.read_text(encoding="utf-8")

    assert "Easy Dataset" in readme
    assert "上游数据生产" in readme
    assert "chunks.jsonl" in readme
    assert "items.jsonl" in readme
    assert "DomainRAG" in readme
    assert "标准 benchmark 数据契约" in readme
    assert "FlashRAG" in readme
    assert "下游 RAG benchmark 框架" in readme


def test_readme_is_chinese_first_showcase_document():
    readme = README.read_text(encoding="utf-8")

    assert readme.startswith("# DomainRAG-Bench：面向专业领域的可追溯 RAG 测评流水线")
    assert "## 项目亮点" in readme
    assert "## 当前示例领域：镍基高温合金高温失效" in readme
    assert "## 整体技术路线" in readme
    assert "## 当前已形成的产物" in readme
    assert "## 当前评测快照" in readme
    assert "## 严谨性与当前边界" in readme
    assert "## Codex 与 DeepSeek 的分工" in readme
    assert "## 当前完成状态" in readme


def test_readme_front_loads_value_artifacts_and_results():
    readme = README.read_text(encoding="utf-8")
    before_quickstart = readme.split("## 快速运行", 1)[0]

    assert "gold evidence" in before_quickstart
    assert "qrels" in before_quickstart
    assert "Fresh-Hard" in before_quickstart
    assert "100 chunks / 300 questions" in before_quickstart
    assert "2,196" in before_quickstart
    assert "108" in before_quickstart
    assert "retrieval_hit" in before_quickstart
    assert "0.7200" in before_quickstart
    assert "human-final" in before_quickstart


def test_readme_status_table_keeps_human_final_boundary_clear():
    readme = README.read_text(encoding="utf-8")

    assert "| 工程流水线 | 基本完成 |" in readme
    assert "| 300 题 provisional 数据集 | 已完成 provisional 版本 |" in readme
    assert "| 人工最终文献白名单 | 待完成 |" in readme
    assert "| human-final benchmark 声明 | 目前不能声明 |" in readme
    assert "不能描述为最终人工验证 benchmark" in readme


def test_readme_describes_current_domain_without_phase_changelog_bullets():
    readme = README.read_text(encoding="utf-8")
    opening = readme.split("## 项目流水线", 1)[0]

    assert "当前实现领域是“镍基高温合金高温失效”" in opening
    assert "数据集" in opening
    assert "候选文献筛选" in opening
    assert "全文解析" in opening
    assert "provisional" in opening
    assert opening.count("Phase 7") <= 4


def test_readme_explains_pipeline_terms_and_baselines():
    readme = README.read_text(encoding="utf-8")

    for term in [
        "Easy Dataset 风格",
        "DomainRAG 标准数据集",
        "gold evidence",
        "gold context",
        "no_rag",
        "oracle_context",
        "lexical_rag",
    ]:
        assert term in readme

    assert "不给检索上下文" in readme
    assert "直接提供 gold context" in readme
    assert "词面检索" in readme


def test_readme_uses_real_input_examples():
    readme = README.read_text(encoding="utf-8")

    assert "data/real_pilot_nickel_superalloy_demo_questions/corpus.jsonl" in readme
    assert "data/real_pilot_nickel_superalloy_demo_questions/canonical_dataset.jsonl" in readme
    assert "data/real_pilot_nickel_superalloy_demo_questions/qrels/fresh_hard.tsv" in readme
    assert "ns_ht_oxidation_gb_energy_001" in readme
    assert "real_pilot_nickel_superalloy_demo_questions_q0001" in readme
