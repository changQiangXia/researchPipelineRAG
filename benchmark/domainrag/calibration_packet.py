from __future__ import annotations

from pathlib import Path
from typing import Any

from domainrag.dataset_adapter import load_split
from domainrag.errors import ValidationError, ValidationIssue
from domainrag.io_utils import read_jsonl, write_jsonl
from domainrag.validator import validate_dataset


def generate_calibration_packet(
    dataset_dir: Path,
    answers_path: Path,
    judge_path: Path,
    output_dir: Path,
    *,
    split: str,
) -> tuple[Path, Path]:
    validate_dataset(dataset_dir)
    records = {record["id"]: record for record in load_split(dataset_dir, split)}
    corpus = _load_corpus(dataset_dir)
    answer_rows = read_jsonl(answers_path)
    judge_rows = read_jsonl(judge_path)
    judge_by_key = _index_judges(judge_rows, split=split, path=judge_path)

    review_rows: list[dict[str, Any]] = []
    issues: list[ValidationIssue] = []
    for index, answer_row in enumerate(answer_rows, start=1):
        row_split = answer_row.get("split")
        question_id = answer_row.get("id")
        method = answer_row.get("method")
        if row_split != split:
            issues.append(
                ValidationIssue(
                    str(answers_path),
                    f"record {index}: answer row split must be {split}",
                )
            )
            continue
        if not isinstance(question_id, str):
            issues.append(ValidationIssue(str(answers_path), f"record {index}: id must be a string"))
            continue
        if not isinstance(method, str):
            issues.append(
                ValidationIssue(str(answers_path), f"record {index}: method must be a string")
            )
            continue
        if question_id not in records:
            issues.append(
                ValidationIssue(str(answers_path), f"record {index}: unknown question id {question_id}")
            )
            continue
        review_rows.append(
            _build_review_row(
                records[question_id],
                answer_row,
                judge_by_key.get((question_id, method)),
                corpus,
                split=split,
            )
        )

    if issues:
        raise ValidationError(issues)

    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "review_packet.jsonl"
    markdown_path = output_dir / "review_packet.md"
    write_jsonl(jsonl_path, review_rows)
    markdown_path.write_text(_render_markdown(review_rows), encoding="utf-8")
    return jsonl_path, markdown_path


def _load_corpus(dataset_dir: Path) -> dict[str, str]:
    corpus: dict[str, str] = {}
    for record in read_jsonl(dataset_dir / "corpus.jsonl"):
        corpus_id = record.get("id")
        contents = record.get("contents")
        if isinstance(corpus_id, str) and isinstance(contents, str):
            corpus[corpus_id] = contents
    return corpus


def _index_judges(
    judge_rows: list[dict[str, Any]],
    *,
    split: str,
    path: Path,
) -> dict[tuple[str, str], dict[str, Any]]:
    issues: list[ValidationIssue] = []
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for index, row in enumerate(judge_rows, start=1):
        question_id = row.get("id")
        method = row.get("method")
        row_split = row.get("split")
        if row_split != split:
            issues.append(
                ValidationIssue(str(path), f"record {index}: judge row split must be {split}")
            )
            continue
        if not isinstance(question_id, str):
            issues.append(ValidationIssue(str(path), f"record {index}: id must be a string"))
            continue
        if not isinstance(method, str):
            issues.append(ValidationIssue(str(path), f"record {index}: method must be a string"))
            continue
        key = (question_id, method)
        if key in indexed:
            issues.append(
                ValidationIssue(
                    str(path),
                    f"record {index}: duplicate judge row for {method}/{question_id}",
                )
            )
            continue
        indexed[key] = row
    if issues:
        raise ValidationError(issues)
    return indexed


def _build_review_row(
    record: dict[str, Any],
    answer_row: dict[str, Any],
    judge_row: dict[str, Any] | None,
    corpus: dict[str, str],
    *,
    split: str,
) -> dict[str, Any]:
    question_id = str(answer_row["id"])
    method = str(answer_row["method"])
    retrieved_context_ids = _string_list(answer_row.get("retrieved_context_ids"))
    priority_reasons = _priority_reasons(answer_row, judge_row)
    return {
        "review_id": f"{split}::{method}::{question_id}",
        "id": question_id,
        "method": method,
        "split": split,
        "question_type": record["metadata"]["question_type"],
        "question": record["question"],
        "golden_answers": answer_row.get("golden_answers", record["golden_answers"]),
        "prediction": answer_row.get("prediction", ""),
        "gold_context_ids": _string_list(answer_row.get("gold_context_ids")),
        "retrieved_context_ids": retrieved_context_ids,
        "context_chunks": [
            {"id": context_id, "contents": corpus[context_id]}
            for context_id in retrieved_context_ids
            if context_id in corpus
        ],
        "scores": answer_row.get("scores", {}),
        "answer_error": answer_row.get("error"),
        "judge": judge_row.get("judge") if judge_row else None,
        "judge_scores": judge_row.get("judge_scores") if judge_row else {},
        "judge_error": judge_row.get("error") if judge_row else "missing_judge_row",
        "priority": "high" if priority_reasons else "normal",
        "priority_reasons": priority_reasons,
        "human_review": {
            "correctness": None,
            "context_support": None,
            "faithfulness": None,
            "decision": None,
            "notes": None,
        },
        "review_prompt": (
            "Verify whether the prediction is correct, fully supported by retrieved context, "
            "and free of unsupported factual claims. Fill human_review fields only after "
            "manual inspection."
        ),
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _priority_reasons(
    answer_row: dict[str, Any],
    judge_row: dict[str, Any] | None,
) -> list[str]:
    reasons: list[str] = []
    if answer_row.get("error"):
        reasons.append("answer_error")
    if judge_row is None:
        reasons.append("missing_judge_row")
        return reasons
    if judge_row.get("error"):
        reasons.append("judge_error")
    judge = judge_row.get("judge")
    if isinstance(judge, dict) and judge.get("unsupported_claims"):
        reasons.append("unsupported_claims")
    scores = judge_row.get("judge_scores")
    if isinstance(scores, dict):
        for metric in ("correctness", "context_support", "faithfulness"):
            value = scores.get(metric)
            if _is_number(value) and float(value) < 5.0:
                reasons.append(f"{metric}_below_5")
        hallucination_risk = scores.get("hallucination_risk")
        if _is_number(hallucination_risk) and float(hallucination_risk) > 0.0:
            reasons.append("hallucination_risk_above_0")
    return reasons


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# DomainRAG Human Calibration Packet",
        "",
        f"Questions for review: {len(rows)}",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['review_id']}",
                "",
                f"- Priority: {row['priority']}",
                f"- Reasons: {', '.join(row['priority_reasons']) if row['priority_reasons'] else 'none'}",
                f"- Method: {row['method']}",
                f"- Question type: {row['question_type']}",
                "",
                "Question:",
                "",
                str(row["question"]),
                "",
                f"Gold answers: {row['golden_answers']}",
                f"Prediction: {row['prediction']}",
                "",
                "Judge:",
                "",
                _format_judge(row),
                "",
                "Retrieved context:",
                "",
            ]
        )
        for chunk in row["context_chunks"]:
            lines.extend([f"### {chunk['id']}", "", str(chunk["contents"]), ""])
        lines.extend(
            [
                "Human review:",
                "",
                "- correctness:",
                "- context_support:",
                "- faithfulness:",
                "- decision:",
                "- notes:",
                "",
            ]
        )
    return "\n".join(lines)


def _format_judge(row: dict[str, Any]) -> str:
    judge = row.get("judge")
    if not isinstance(judge, dict):
        return "No judge row was available."
    unsupported_claims = judge.get("unsupported_claims", [])
    if unsupported_claims:
        unsupported = "; ".join(str(claim) for claim in unsupported_claims)
    else:
        unsupported = "none"
    return (
        f"correctness={judge.get('correctness')}, "
        f"context_support={judge.get('context_support')}, "
        f"faithfulness={judge.get('faithfulness')}, "
        f"unsupported_claims={unsupported}, "
        f"reason={judge.get('reason')}"
    )
