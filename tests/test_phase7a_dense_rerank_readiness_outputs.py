from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "outputs" / "phase7a" / "dense_rerank_readiness" / "readiness.json"
SUMMARY = ROOT / "outputs" / "phase7a" / "dense_rerank_readiness" / "summary.md"
DOC = ROOT / "docs" / "verification" / "dense-rerank-isolated-readiness.md"
AUDIT = ROOT / "docs" / "reports" / "rag-md-implementation-audit.json"


def test_phase7a_dense_rerank_readiness_outputs_exist_and_capture_isolation_decision():
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    summary = SUMMARY.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    assert readiness["phase"] == "Phase 7A"
    assert readiness["current_environment"]["decision"] == "use_isolated_environment"
    assert readiness["current_environment"]["safe_to_mutate"] is False
    assert readiness["target_methods"] == [
        "flashrag_dense",
        "flashrag_reranker",
        "flashrag_bm25_plus_reranker",
    ]
    assert readiness["isolated_environment"]["python"] == "3.10"
    assert "torch>=2.4" in readiness["isolated_environment"]["pip_requirements"]
    assert len(readiness["acceptance_gates"]) >= 5
    assert "medium_dense_retrieval_smoke" in {
        gate["name"] for gate in readiness["acceptance_gates"]
    }
    assert "Do not install these dependencies into the current AutoDL environment" in summary
    assert "Phase 7A" in doc
    assert "dense-rerank-readiness" in doc


def test_phase7a_updates_rag_md_audit_dense_rerank_evidence():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in audit["requirements"]}
    dense = requirements["dense_rerank_methods"]

    assert dense["status"] == "partial"
    assert "outputs/phase7a/dense_rerank_readiness/readiness.json" in dense["evidence"]
    assert "docs/verification/dense-rerank-isolated-readiness.md" in dense["evidence"]
    assert "isolated readiness" in dense["summary"]
