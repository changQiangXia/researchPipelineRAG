from __future__ import annotations

import argparse
import os
from pathlib import Path

from domainrag.bm25s_retrieval import run_bm25s_retrieval
from domainrag.benchmark_runner import run_benchmark
from domainrag.calibration_audit import generate_calibration_audit
from domainrag.calibration_packet import generate_calibration_packet
from domainrag.comparison_report import generate_comparison_report
from domainrag.deepseek_answer_runner import (
    DeepSeekAnswerConfig,
    run_deepseek_answer_benchmark,
)
from domainrag.deepseek_judge_runner import (
    DeepSeekJudgeConfig,
    generate_judge_report,
    run_deepseek_judge,
)
from domainrag.deepseek_pipeline import DEFAULT_BASE_URL, DEFAULT_MODEL
from domainrag.demo_question_generation import build_demo_question_dataset
from domainrag.dense_rerank_readiness import generate_dense_rerank_readiness
from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.errors import ValidationError
from domainrag.flashrag_adapter import prepare_flashrag_bundle
from domainrag.flashrag_bm25_bridge import run_flashrag_bm25_bridge
from domainrag.flashrag_method_feasibility import probe_flashrag_method_feasibility
from domainrag.full_text_chunk_extraction import build_full_text_chunk_outputs
from domainrag.hashed_dense_benchmark import run_hashed_dense_benchmark
from domainrag.report_generator import generate_report
from domainrag.source_acquisition import acquire_demo_scale_sources, build_query_plan
from domainrag.source_decisions import build_decision_outputs
from domainrag.source_finalization_packet import build_manual_finalization_outputs
from domainrag.source_human_signoff import build_human_signoff_outputs
from domainrag.source_screening import build_screening_outputs
from domainrag.source_verification import build_verification_outputs
from domainrag.validator import validate_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="domainrag")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version")
    validate = subparsers.add_parser("validate-data")
    validate.add_argument("--dataset", required=True)
    run = subparsers.add_parser("run")
    run.add_argument("--dataset", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--methods", required=True)
    run.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_deepseek = subparsers.add_parser("run-deepseek-answers")
    run_deepseek.add_argument("--dataset", required=True)
    run_deepseek.add_argument("--output", required=True)
    run_deepseek.add_argument("--methods", required=True)
    run_deepseek.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_deepseek.add_argument("--base-url", default=DEFAULT_BASE_URL)
    run_deepseek.add_argument("--model", default=DEFAULT_MODEL)
    run_deepseek.add_argument("--timeout-seconds", type=int, default=120)
    run_deepseek.add_argument("--max-tokens", type=int, default=4096)
    run_deepseek.add_argument("--temperature", type=float, default=0.0)
    run_deepseek.add_argument("--top-k", type=int, default=5)
    run_deepseek.add_argument("--max-retries", type=int, default=1)
    run_deepseek.add_argument("--limit", type=int, default=None)
    run_deepseek.add_argument("--retrieval-results", default=None)
    judge_deepseek = subparsers.add_parser("judge-deepseek-answers")
    judge_deepseek.add_argument("--dataset", required=True)
    judge_deepseek.add_argument("--input", required=True)
    judge_deepseek.add_argument("--output", required=True)
    judge_deepseek.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    judge_deepseek.add_argument("--base-url", default=DEFAULT_BASE_URL)
    judge_deepseek.add_argument("--model", default=DEFAULT_MODEL)
    judge_deepseek.add_argument("--timeout-seconds", type=int, default=120)
    judge_deepseek.add_argument("--max-tokens", type=int, default=4096)
    judge_deepseek.add_argument("--temperature", type=float, default=0.0)
    judge_deepseek.add_argument("--max-retries", type=int, default=1)
    judge_deepseek.add_argument("--limit", type=int, default=None)
    report = subparsers.add_parser("report")
    report.add_argument("--input", required=True)
    report.add_argument("--output", required=True)
    compare = subparsers.add_parser("compare")
    compare.add_argument("--answer-inputs", nargs="+", required=True)
    compare.add_argument("--judge-inputs", nargs="+", default=[])
    compare.add_argument("--output", required=True)
    calibration_packet = subparsers.add_parser("calibration-packet")
    calibration_packet.add_argument("--dataset", required=True)
    calibration_packet.add_argument("--answers", nargs="+", required=True)
    calibration_packet.add_argument("--judge", nargs="+", required=True)
    calibration_packet.add_argument(
        "--split",
        default="fresh_hard",
        choices=["dev", "test", "fresh_hard"],
    )
    calibration_packet.add_argument("--output", required=True)
    calibration_audit = subparsers.add_parser("calibration-audit")
    calibration_audit.add_argument("--packet", required=True)
    calibration_audit.add_argument("--labels", required=True)
    calibration_audit.add_argument("--output", required=True)
    judge_report = subparsers.add_parser("judge-report")
    judge_report.add_argument("--input", required=True)
    judge_report.add_argument("--output", required=True)
    prepare_flashrag = subparsers.add_parser("prepare-flashrag")
    prepare_flashrag.add_argument("--dataset", required=True)
    prepare_flashrag.add_argument("--output", required=True)
    prepare_flashrag.add_argument("--dataset-name", required=True)
    prepare_flashrag.add_argument("--splits", default="dev,test,fresh_hard")
    run_flashrag_bm25 = subparsers.add_parser("run-flashrag-bm25")
    run_flashrag_bm25.add_argument("--flashrag-path", required=True)
    run_flashrag_bm25.add_argument("--dataset-bundle", required=True)
    run_flashrag_bm25.add_argument("--output", required=True)
    run_flashrag_bm25.add_argument("--dataset-name", required=True)
    run_flashrag_bm25.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_flashrag_bm25.add_argument("--top-k", type=int, default=5)
    run_flashrag_bm25.add_argument("--index-dir", default=None)
    run_flashrag_bm25.add_argument("--rebuild-index", action="store_true", default=False)
    run_bm25s = subparsers.add_parser("run-bm25s")
    run_bm25s.add_argument("--dataset", required=True)
    run_bm25s.add_argument("--output", required=True)
    run_bm25s.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_bm25s.add_argument("--top-k", type=int, default=5)
    run_hashed_dense = subparsers.add_parser("run-hashed-dense")
    run_hashed_dense.add_argument("--dataset", required=True)
    run_hashed_dense.add_argument("--output", required=True)
    run_hashed_dense.add_argument("--split", default="dev", choices=["dev", "test", "fresh_hard"])
    run_hashed_dense.add_argument("--top-k", type=int, default=5)
    run_hashed_dense.add_argument("--dimensions", type=int, default=512)
    build_demo_questions = subparsers.add_parser("build-demo-questions")
    build_demo_questions.add_argument("--source-dataset", required=True)
    build_demo_questions.add_argument("--output", required=True)
    build_demo_questions.add_argument(
        "--dataset-name",
        default="real_pilot_nickel_superalloy_demo_questions",
    )
    build_demo_questions.add_argument("--target-questions", type=int, default=300)
    build_demo_questions.add_argument("--fixture-output", default=None)
    probe_flashrag_methods = subparsers.add_parser("probe-flashrag-methods")
    probe_flashrag_methods.add_argument("--flashrag-path", required=True)
    probe_flashrag_methods.add_argument("--output", required=True)
    dense_rerank_readiness = subparsers.add_parser("dense-rerank-readiness")
    dense_rerank_readiness.add_argument("--feasibility", required=True)
    dense_rerank_readiness.add_argument("--output", required=True)
    extract_fulltext_chunks = subparsers.add_parser("extract-fulltext-chunks")
    extract_fulltext_chunks.add_argument("--access", required=True)
    extract_fulltext_chunks.add_argument("--output", required=True)
    extract_fulltext_chunks.add_argument("--chunk-tokens", type=int, default=350)
    extract_fulltext_chunks.add_argument("--overlap-tokens", type=int, default=50)
    extract_fulltext_chunks.add_argument("--min-chunk-tokens", type=int, default=80)
    extract_fulltext_chunks.add_argument("--max-sources", type=int, default=None)
    extract_fulltext_chunks.add_argument("--include-text", action="store_true", default=False)
    export_domainrag = subparsers.add_parser("export-domainrag")
    export_domainrag.add_argument("--input", required=True)
    export_domainrag.add_argument("--output", required=True)
    export_domainrag.add_argument("--dataset-name", required=True)
    acquire_sources = subparsers.add_parser("acquire-sources")
    acquire_sources.add_argument(
        "--output",
        default="outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition",
    )
    acquire_sources.add_argument("--per-query", type=int, default=15)
    acquire_sources.add_argument("--mailto", default=None)
    acquire_sources.add_argument("--timeout-seconds", type=int, default=60)
    acquire_sources.add_argument("--dry-run", action="store_true", default=False)
    screen_sources = subparsers.add_parser("screen-sources")
    screen_sources.add_argument(
        "--candidates",
        default="outputs/archive/provenance/source-workflow/demo-scale-source-acquisition/demo_scale_source_acquisition/candidates.jsonl",
    )
    screen_sources.add_argument(
        "--output",
        default="outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue",
    )
    decide_sources = subparsers.add_parser("decide-sources")
    decide_sources.add_argument(
        "--screening-queue",
        default="outputs/archive/provenance/source-workflow/source-screening-queue/source_screening_queue/screening_queue.jsonl",
    )
    decide_sources.add_argument(
        "--output",
        default="outputs/archive/provenance/source-workflow/source-decisions/source_decisions",
    )
    verify_sources = subparsers.add_parser("verify-sources")
    verify_sources.add_argument(
        "--whitelist",
        default="outputs/archive/provenance/source-workflow/source-decisions/source_decisions/provisional_source_whitelist.jsonl",
    )
    verify_sources.add_argument("--metadata", default=None)
    verify_sources.add_argument("--access", default=None)
    verify_sources.add_argument(
        "--output",
        default="outputs/archive/provenance/source-workflow/source-verification-first-batches/source_verification",
    )
    finalization_packet = subparsers.add_parser("build-finalization-packet")
    finalization_packet.add_argument(
        "--verification-matrix",
        default="outputs/archive/provenance/source-workflow/source-verification-combined/source_verification_combined115/source_verification_matrix.jsonl",
    )
    finalization_packet.add_argument(
        "--output",
        default="outputs/archive/provenance/source-workflow/manual-finalization-packet/manual_finalization_packet",
    )
    human_signoff = subparsers.add_parser("build-human-signoff")
    human_signoff.add_argument(
        "--candidate-queue",
        default="outputs/archive/provenance/source-workflow/manual-finalization-packet/manual_finalization_packet/candidate_final_whitelist_queue.jsonl",
    )
    human_signoff.add_argument("--labels", default=None)
    human_signoff.add_argument(
        "--output",
        default="outputs/archive/provenance/source-workflow/human-signoff/human_signoff",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        print("domainrag-bench 0.1.0")
        return 0
    if args.command == "validate-data":
        try:
            validate_dataset(Path(args.dataset))
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"{args.dataset} is valid")
        return 0
    if args.command == "run":
        methods = [method.strip() for method in args.methods.split(",") if method.strip()]
        try:
            result_path = run_benchmark(Path(args.dataset), Path(args.output), methods, args.split)
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"results written to {result_path}")
        return 0
    if args.command == "run-deepseek-answers":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("DEEPSEEK_API_KEY is required")
            return 1
        methods = [method.strip() for method in args.methods.split(",") if method.strip()]
        try:
            config = DeepSeekAnswerConfig(
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                top_k=args.top_k,
                max_retries=args.max_retries,
            )
            result_path = run_deepseek_answer_benchmark(
                Path(args.dataset),
                Path(args.output),
                methods,
                args.split,
                config,
                limit=args.limit,
                retrieval_results_path=(
                    Path(args.retrieval_results) if args.retrieval_results else None
                ),
            )
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"DeepSeek answer results written to {result_path}")
        return 0
    if args.command == "judge-deepseek-answers":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("DEEPSEEK_API_KEY is required")
            return 1
        try:
            config = DeepSeekJudgeConfig(
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                max_retries=args.max_retries,
            )
            result_path = run_deepseek_judge(
                Path(args.dataset),
                Path(args.input),
                Path(args.output),
                split=args.split,
                config=config,
                limit=args.limit,
            )
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"DeepSeek judge results written to {result_path}")
        return 0
    if args.command == "report":
        try:
            markdown_path, json_path = generate_report(Path(args.input), Path(args.output))
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"report written to {markdown_path} and {json_path}")
        return 0
    if args.command == "compare":
        try:
            markdown_path, json_path = generate_comparison_report(
                answer_inputs=[Path(path) for path in args.answer_inputs],
                judge_inputs=[Path(path) for path in args.judge_inputs],
                output_dir=Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"comparison report written to {markdown_path} and {json_path}")
        return 0
    if args.command == "calibration-packet":
        try:
            jsonl_path, markdown_path = generate_calibration_packet(
                Path(args.dataset),
                [Path(path) for path in args.answers],
                [Path(path) for path in args.judge],
                Path(args.output),
                split=args.split,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"calibration packet written to {jsonl_path} and {markdown_path}")
        return 0
    if args.command == "calibration-audit":
        try:
            markdown_path, json_path = generate_calibration_audit(
                Path(args.packet),
                Path(args.labels),
                Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"calibration audit written to {markdown_path} and {json_path}")
        return 0
    if args.command == "judge-report":
        try:
            markdown_path, json_path = generate_judge_report(
                Path(args.input),
                Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"judge report written to {markdown_path} and {json_path}")
        return 0
    if args.command == "prepare-flashrag":
        splits = tuple(split.strip() for split in args.splits.split(",") if split.strip())
        try:
            bundle = prepare_flashrag_bundle(
                Path(args.dataset),
                Path(args.output),
                dataset_name=args.dataset_name,
                splits=splits,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"FlashRAG bundle written to {bundle.dataset_dir}")
        print(f"FlashRAG config written to {bundle.config_path}")
        return 0
    if args.command == "run-flashrag-bm25":
        try:
            result_path = run_flashrag_bm25_bridge(
                Path(args.flashrag_path),
                Path(args.dataset_bundle),
                Path(args.output),
                dataset_name=args.dataset_name,
                split=args.split,
                top_k=args.top_k,
                index_dir=Path(args.index_dir) if args.index_dir else None,
                rebuild_index=args.rebuild_index,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"FlashRAG BM25 results written to {result_path}")
        return 0
    if args.command == "run-bm25s":
        try:
            result_path = run_bm25s_retrieval(
                Path(args.dataset),
                Path(args.output),
                split=args.split,
                top_k=args.top_k,
            )
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"BM25s results written to {result_path}")
        return 0
    if args.command == "run-hashed-dense":
        try:
            result_path = run_hashed_dense_benchmark(
                Path(args.dataset),
                Path(args.output),
                split=args.split,
                top_k=args.top_k,
                dimensions=args.dimensions,
            )
        except (ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"hashed dense results written to {result_path}")
        return 0
    if args.command == "build-demo-questions":
        try:
            bundle = build_demo_question_dataset(
                Path(args.source_dataset),
                Path(args.output),
                dataset_name=args.dataset_name,
                target_questions=args.target_questions,
                fixture_output_dir=Path(args.fixture_output) if args.fixture_output else None,
            )
        except (OSError, ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"demo question dataset written to {bundle.dataset_dir}")
        return 0
    if args.command == "probe-flashrag-methods":
        try:
            probe_flashrag_method_feasibility(
                Path(args.flashrag_path),
                output_path=Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"FlashRAG method feasibility manifest written to {args.output}")
        return 0
    if args.command == "dense-rerank-readiness":
        try:
            markdown_path, json_path = generate_dense_rerank_readiness(
                Path(args.feasibility),
                Path(args.output),
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"dense/rerank readiness written to {markdown_path} and {json_path}")
        return 0
    if args.command == "extract-fulltext-chunks":
        try:
            chunks_path, manifest_path, summary_path, markdown_path = (
                build_full_text_chunk_outputs(
                    Path(args.access),
                    output_dir=Path(args.output),
                    chunk_tokens=args.chunk_tokens,
                    overlap_tokens=args.overlap_tokens,
                    min_chunk_tokens=args.min_chunk_tokens,
                    max_sources=args.max_sources,
                    include_text=args.include_text,
                )
            )
        except (OSError, ValidationError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"full-text chunks written to {chunks_path}")
        print(f"chunk source manifest written to {manifest_path}")
        print(f"chunk extraction summary written to {summary_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    if args.command == "export-domainrag":
        try:
            bundle = export_domainrag_bundle(
                Path(args.input),
                Path(args.output),
                args.dataset_name,
            )
        except ValidationError as exc:
            print(str(exc))
            return 1
        print(f"DomainRAG dataset written to {bundle.dataset_dir}")
        return 0
    if args.command == "acquire-sources":
        if args.per_query <= 0:
            print("per-query must be positive")
            return 1
        if args.timeout_seconds <= 0:
            print("timeout-seconds must be positive")
            return 1
        if args.dry_run:
            print("OpenAlex query plan")
            for planned in build_query_plan(per_query=args.per_query, mailto=args.mailto):
                print(f"{planned['subtopic']}\t{planned['query']}\t{planned['url']}")
            return 0
        try:
            candidates_path, coverage_path, markdown_path = acquire_demo_scale_sources(
                output_dir=Path(args.output),
                per_query=args.per_query,
                mailto=args.mailto,
                timeout_seconds=args.timeout_seconds,
            )
        except OSError as exc:
            print(str(exc))
            return 1
        print(f"source candidates written to {candidates_path}")
        print(f"coverage summary written to {coverage_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    if args.command == "screen-sources":
        try:
            queue_path, summary_path, markdown_path = build_screening_outputs(
                Path(args.candidates),
                output_dir=Path(args.output),
            )
        except (OSError, ValidationError) as exc:
            print(str(exc))
            return 1
        print(f"source screening queue written to {queue_path}")
        print(f"screening summary written to {summary_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    if args.command == "decide-sources":
        try:
            decisions_path, whitelist_path, summary_path, markdown_path = (
                build_decision_outputs(
                    Path(args.screening_queue),
                    output_dir=Path(args.output),
                )
            )
        except (OSError, ValidationError) as exc:
            print(str(exc))
            return 1
        print(f"source decisions written to {decisions_path}")
        print(f"provisional source whitelist written to {whitelist_path}")
        print(f"decision summary written to {summary_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    if args.command == "verify-sources":
        try:
            matrix_path, final_queue_path, summary_path, markdown_path = (
                build_verification_outputs(
                    Path(args.whitelist),
                    output_dir=Path(args.output),
                    metadata_path=Path(args.metadata) if args.metadata else None,
                    access_path=Path(args.access) if args.access else None,
                )
            )
        except (OSError, ValidationError) as exc:
            print(str(exc))
            return 1
        print(f"source verification matrix written to {matrix_path}")
        print(f"final verification queue written to {final_queue_path}")
        print(f"verification summary written to {summary_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    if args.command == "build-finalization-packet":
        try:
            packet_path, queue_path, summary_path, markdown_path = (
                build_manual_finalization_outputs(
                    Path(args.verification_matrix),
                    output_dir=Path(args.output),
                )
            )
        except (OSError, ValidationError) as exc:
            print(str(exc))
            return 1
        print(f"manual finalization packet written to {packet_path}")
        print(f"candidate final whitelist queue written to {queue_path}")
        print(f"manual finalization summary written to {summary_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    if args.command == "build-human-signoff":
        try:
            template_path, final_path, summary_path, markdown_path = (
                build_human_signoff_outputs(
                    Path(args.candidate_queue),
                    output_dir=Path(args.output),
                    labels_path=Path(args.labels) if args.labels else None,
                )
            )
        except (OSError, ValidationError) as exc:
            print(str(exc))
            return 1
        print(f"human sign-off template written to {template_path}")
        print(f"final source whitelist written to {final_path}")
        print(f"human sign-off summary written to {summary_path}")
        print(f"markdown summary written to {markdown_path}")
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
