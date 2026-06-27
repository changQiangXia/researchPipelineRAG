from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.deepseek_pipeline import (  # noqa: E402
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    ChatCompletionConfig,
    build_generation_messages,
    build_review_messages,
    call_chat_completions,
    extract_message_content,
    normalize_generated_item,
    normalize_review_result,
    parse_json_object,
)
from domainrag.io_utils import read_jsonl, write_jsonl  # noqa: E402


DEFAULT_PLAN = [
    {
        "chunk_id": "ns_ht_oxidation_gb_energy_001",
        "split": "dev",
        "question_type": "single_choice",
    },
    {
        "chunk_id": "ns_ht_oxidation_ce_coating_001",
        "split": "test",
        "question_type": "fill_blank",
    },
    {
        "chunk_id": "ns_ht_creep_orientation_850c_001",
        "split": "fresh_hard",
        "question_type": "short_answer",
    },
]
AUTO_ACCEPT_QUALITY_THRESHOLD = 0.9


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a controlled DeepSeek generation/review pass for the real pilot.",
    )
    parser.add_argument("--chunks", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--generation-model", default=DEFAULT_MODEL)
    parser.add_argument("--review-model", default=DEFAULT_MODEL)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument(
        "--plan",
        choices=["default", "all-chunks"],
        default="default",
        help="default runs the curated 3-item pilot; all-chunks plans one item for every chunk.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    chunks_path = Path(args.chunks)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    chunk_records = read_jsonl(chunks_path)
    chunks = {chunk["id"]: chunk for chunk in chunk_records}
    plan = build_plan(chunk_records, args.plan, args.max_items)
    missing_chunks = [entry["chunk_id"] for entry in plan if entry["chunk_id"] not in chunks]
    if missing_chunks:
        raise SystemExit(f"planned chunk ids missing from chunks file: {missing_chunks}")

    manifest = {
        "base_url": args.base_url,
        "dry_run": args.dry_run,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generation_model": args.generation_model,
        "plan": args.plan,
        "planned_items": len(plan),
        "review_model": args.review_model,
        "source_chunks": str(chunks_path),
    }
    (output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    planned_requests = []
    for entry in plan:
        chunk = chunks[entry["chunk_id"]]
        planned_requests.append(
            {
                **entry,
                "generation_messages": build_generation_messages(
                    chunk,
                    split=entry["split"],
                    question_type=entry["question_type"],
                ),
            }
        )
    write_jsonl(output_dir / "planned_requests.jsonl", planned_requests)

    if args.dry_run:
        print(f"planned requests written to {output_dir / 'planned_requests.jsonl'}")
        return 0

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is required unless --dry-run is set")

    generated_items: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    accepted_items: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    raw_responses: list[dict[str, Any]] = []

    for entry in plan:
        chunk = chunks[entry["chunk_id"]]
        generated_item, generation_raw = _generate_item(
            api_key=api_key,
            base_url=args.base_url,
            model=args.generation_model,
            timeout_seconds=args.timeout_seconds,
            max_retries=args.max_retries,
            chunk=chunk,
            split=entry["split"],
            question_type=entry["question_type"],
        )
        generated_items.append(generated_item)
        raw_responses.append(
            {
                "chunk_id": entry["chunk_id"],
                "model": args.generation_model,
                "stage": "generation",
                **generation_raw,
            }
        )

        review_result, review_raw = _review_item(
            api_key=api_key,
            base_url=args.base_url,
            model=args.review_model,
            timeout_seconds=args.timeout_seconds,
            max_retries=args.max_retries,
            chunk=chunk,
            item=generated_item,
        )
        review_rows.append(
            {
                "chunk_id": entry["chunk_id"],
                "item_id": generated_item["id"],
                "review": review_result,
            }
        )
        audit_row = build_candidate_audit_row(
            chunk_id=entry["chunk_id"],
            item=generated_item,
            review_result=review_result,
        )
        audit_rows.append(audit_row)
        raw_responses.append(
            {
                "chunk_id": entry["chunk_id"],
                "item_id": generated_item["id"],
                "model": args.review_model,
                "stage": "review",
                **review_raw,
            }
        )

        accepted_item = _accepted_item(
            generated_item,
            review_result,
            chunk_id=entry["chunk_id"],
            split=entry["split"],
            question_type=entry["question_type"],
        )
        if accepted_item is not None:
            accepted_items.append(accepted_item)

    write_jsonl(output_dir / "generated_items.jsonl", generated_items)
    write_jsonl(output_dir / "review_results.jsonl", review_rows)
    write_jsonl(output_dir / "candidate_audit.jsonl", audit_rows)
    write_jsonl(output_dir / "accepted_items.jsonl", accepted_items)
    write_jsonl(output_dir / "raw_responses.jsonl", raw_responses)

    print(f"generated items written to {output_dir / 'generated_items.jsonl'}")
    print(f"review results written to {output_dir / 'review_results.jsonl'}")
    print(f"candidate audit written to {output_dir / 'candidate_audit.jsonl'}")
    print(f"accepted items written to {output_dir / 'accepted_items.jsonl'}")
    return 0


def build_plan(
    chunks: list[dict[str, Any]],
    plan_name: str,
    max_items: int | None,
) -> list[dict[str, str]]:
    if plan_name == "default":
        limit = len(DEFAULT_PLAN) if max_items is None else max_items
        return DEFAULT_PLAN[:limit]
    if plan_name != "all-chunks":
        raise ValueError(f"unsupported plan: {plan_name}")

    splits = ("dev", "test", "fresh_hard")
    question_types = ("single_choice", "fill_blank", "short_answer", "multiple_choice")
    plan: list[dict[str, str]] = []
    selected_chunks = chunks if max_items is None else chunks[:max_items]
    for index, chunk in enumerate(selected_chunks):
        plan.append(
            {
                "chunk_id": chunk["id"],
                "split": splits[index % len(splits)],
                "question_type": question_types[index % len(question_types)],
            }
        )
    return plan


def _generate_item(
    *,
    api_key: str,
    base_url: str,
    model: str,
    timeout_seconds: int,
    max_retries: int,
    chunk: dict[str, Any],
    split: str,
    question_type: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    config = ChatCompletionConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    last_error: Exception | None = None
    messages = build_generation_messages(chunk, split=split, question_type=question_type)
    for attempt in range(1, max_retries + 2):
        try:
            response = call_chat_completions(config, messages)
            content = extract_message_content(response)
            parsed = parse_json_object(content)
            raw_item = parsed.get("item", parsed)
            if not isinstance(raw_item, dict):
                raise ValueError("generation response must contain an object item")
            item = normalize_generated_item(
                raw_item,
                chunk_id=chunk["id"],
                split=split,
                question_type=question_type,
            )
            return item, {
                "attempt": attempt,
                "content": content,
                "usage": response.get("usage", {}),
            }
        except Exception as exc:
            last_error = exc
    raise SystemExit(f"generation failed after retries: {last_error}")


def _review_item(
    *,
    api_key: str,
    base_url: str,
    model: str,
    timeout_seconds: int,
    max_retries: int,
    chunk: dict[str, Any],
    item: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    config = ChatCompletionConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    last_error: Exception | None = None
    messages = build_review_messages(chunk, item)
    for attempt in range(1, max_retries + 2):
        try:
            response = call_chat_completions(config, messages)
            content = extract_message_content(response)
            review_result = normalize_review_result(parse_json_object(content))
            return review_result, {
                "attempt": attempt,
                "content": content,
                "usage": response.get("usage", {}),
            }
        except Exception as exc:
            last_error = exc
    raise SystemExit(f"review failed after retries: {last_error}")


def _accepted_item(
    generated_item: dict[str, Any],
    review_result: dict[str, Any],
    *,
    chunk_id: str,
    split: str,
    question_type: str,
) -> dict[str, Any] | None:
    if (
        not review_result["accepted"]
        or float(review_result["quality_score"]) < AUTO_ACCEPT_QUALITY_THRESHOLD
    ):
        return None
    candidate = review_result["corrected_item"] or generated_item
    return normalize_generated_item(
        candidate,
        chunk_id=chunk_id,
        split=split,
        question_type=question_type,
    )


def build_candidate_audit_row(
    *,
    chunk_id: str,
    item: dict[str, Any],
    review_result: dict[str, Any],
) -> dict[str, Any]:
    score = float(review_result["quality_score"])
    review_accepted = bool(review_result["accepted"])
    if not review_accepted:
        decision = "rejected"
        reason = "review rejected candidate"
    elif score < AUTO_ACCEPT_QUALITY_THRESHOLD:
        decision = "needs_human_review"
        reason = (
            "quality score below automatic acceptance threshold "
            f"{AUTO_ACCEPT_QUALITY_THRESHOLD:.2f}"
        )
    else:
        decision = "accepted"
        reason = ""

    return {
        "candidate_id": item["id"],
        "chunk_id": chunk_id,
        "decision": decision,
        "needs_human_review_reason": reason,
        "problems": review_result["problems"],
        "question_type": item["question_type"],
        "review_accepted": review_accepted,
        "review_quality_score": score,
        "split": item["split"],
    }


if __name__ == "__main__":
    raise SystemExit(main())
