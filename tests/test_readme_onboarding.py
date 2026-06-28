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
