from __future__ import annotations

from collections import Counter, defaultdict
import html
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from domainrag.io_utils import write_jsonl


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
FROM_YEAR = 2017
TO_YEAR = 2026
DEMO_SOURCE_TARGET = [100, 180]
DEMO_CHUNK_TARGET = [1000, 3000]
DEMO_QUESTION_TARGET = [300, 500]

DOMAIN_FLAGSHIP_VENUES = {
    "acta materialia",
    "additive manufacturing",
    "corrosion science",
    "international journal of fatigue",
    "journal of alloys and compounds",
    "materials & design",
    "materials science and engineering a",
    "npj materials degradation",
    "progress in materials science",
    "scripta materialia",
    "surface and coatings technology",
}
DOMAIN_RELEVANCE_TERMS = (
    "nickel",
    "superalloy",
    "superalloys",
    "ni-base",
    "ni-based",
    "inconel",
    "nimonic",
    "hastelloy",
    "rene",
    "gh4169",
    "gh3536",
    "in625",
    "in718",
    "cm247",
    "dd5",
)
DEFAULT_SUBTOPIC_QUERIES = {
    "oxidation": [
        "nickel superalloy high temperature oxidation",
        "Inconel nickel superalloy oxidation grain boundary",
    ],
    "creep": [
        "nickel based superalloy creep microstructure",
        "gamma prime rafting nickel superalloy creep",
    ],
    "fatigue": [
        "nickel superalloy high temperature fatigue",
        "nickel superalloy low cycle fatigue oxidation",
        "Inconel 718 low cycle fatigue high temperature",
        "nickel based superalloy creep fatigue interaction",
        "nickel superalloy fatigue crack propagation",
    ],
    "hot_corrosion": [
        "nickel superalloy hot corrosion molten salt",
        "nickel based superalloy sulfate hot corrosion",
    ],
    "additive_manufacturing": [
        "additive manufactured nickel superalloy creep fatigue oxidation",
        "laser powder bed fusion nickel superalloy high temperature",
    ],
    "coatings": [
        "nickel superalloy coating interdiffusion oxidation",
        "thermal barrier coating nickel superalloy oxidation corrosion",
    ],
    "life_prediction": [
        "nickel superalloy creep life prediction machine learning",
        "nickel superalloy fatigue life prediction microstructure",
        "Inconel 718 fatigue life prediction nickel superalloy",
        "nickel superalloy creep rupture life prediction",
    ],
    "microstructure_characterization": [
        "nickel superalloy gamma prime microstructure characterization",
        "nickel superalloy precipitate evolution high temperature",
    ],
}


def build_openalex_url(
    query: str,
    *,
    from_year: int = FROM_YEAR,
    to_year: int = TO_YEAR,
    per_page: int = 15,
    mailto: str | None = None,
) -> str:
    filters = ",".join(
        [
            f"from_publication_date:{from_year}-01-01",
            f"to_publication_date:{to_year}-12-31",
            "has_doi:true",
        ]
    )
    params = {
        "search": query,
        "filter": filters,
        "per-page": str(per_page),
        "sort": "publication_date:desc",
    }
    if mailto:
        params["mailto"] = mailto
    return f"{OPENALEX_WORKS_URL}?{urlencode(params)}"


def build_query_plan(
    *,
    per_query: int = 15,
    mailto: str | None = None,
) -> list[dict[str, str]]:
    return [
        {
            "subtopic": subtopic,
            "query": query,
            "url": build_openalex_url(query, per_page=per_query, mailto=mailto),
        }
        for subtopic, queries in DEFAULT_SUBTOPIC_QUERIES.items()
        for query in queries
    ]


def fetch_openalex_records(
    *,
    per_query: int = 15,
    mailto: str | None = None,
    timeout_seconds: int = 60,
) -> list[dict[str, Any]]:
    raw_records: list[dict[str, Any]] = []
    for planned in build_query_plan(per_query=per_query, mailto=mailto):
        payload = _fetch_json(planned["url"], timeout_seconds=timeout_seconds)
        results = payload.get("results", [])
        if not isinstance(results, list):
            continue
        for work in results:
            if isinstance(work, dict):
                raw_records.append(
                    {
                        "subtopic": planned["subtopic"],
                        "query": planned["query"],
                        "work": work,
                    }
                )
    return raw_records


def acquire_demo_scale_sources(
    *,
    output_dir: Path,
    per_query: int = 15,
    mailto: str | None = None,
    timeout_seconds: int = 60,
) -> tuple[Path, Path, Path]:
    raw_records = fetch_openalex_records(
        per_query=per_query,
        mailto=mailto,
        timeout_seconds=timeout_seconds,
    )
    return build_acquisition_outputs(raw_records, output_dir=output_dir)


def normalize_openalex_work(
    work: dict[str, Any],
    *,
    subtopic: str,
    query: str,
) -> dict[str, Any] | None:
    title = _clean_text(work.get("display_name"))
    year = _int_or_none(work.get("publication_year"))
    doi = _normalize_doi(work.get("doi"))
    openalex_id = _string_or_none(work.get("id"))
    if not title or not year or not doi or not openalex_id:
        return None
    if year < FROM_YEAR or year > TO_YEAR:
        return None
    abstract_text = _abstract_text(work.get("abstract_inverted_index"))
    domain_terms = _domain_relevance_terms(f"{title} {abstract_text}")
    if not domain_terms:
        return None

    primary_location = work.get("primary_location")
    if not isinstance(primary_location, dict):
        primary_location = {}
    source = primary_location.get("source")
    if not isinstance(source, dict):
        source = {}
    open_access = work.get("open_access")
    if not isinstance(open_access, dict):
        open_access = {}

    work_type = _string_or_none(work.get("type")) or "unknown"
    venue = _string_or_none(source.get("display_name")) or "unknown"
    official_url = (
        _string_or_none(primary_location.get("landing_page_url"))
        or _string_or_none(open_access.get("oa_url"))
        or openalex_id
    )
    is_oa = bool(open_access.get("is_oa") or primary_location.get("is_oa"))
    source_id = "openalex_" + openalex_id.rstrip("/").rsplit("/", 1)[-1]
    work_kind = _work_kind(title, work_type)

    return {
        "source_id": source_id,
        "openalex_id": openalex_id,
        "doi": doi,
        "title": title,
        "year": year,
        "publication_date": _string_or_none(work.get("publication_date")),
        "venue": venue,
        "venue_type": _string_or_none(source.get("type")) or "unknown",
        "official_url": official_url,
        "open_access": is_oa,
        "oa_url": _string_or_none(open_access.get("oa_url")),
        "work_type": work_type,
        "work_kind": work_kind,
        "subtopic": subtopic,
        "query": query,
        "cited_by_count": _int_or_none(work.get("cited_by_count")) or 0,
        "has_abstract": isinstance(work.get("abstract_inverted_index"), dict),
        "domain_relevance_terms": domain_terms,
        "venue_whitelist_status": _venue_whitelist_status(venue),
        "verification_status": "candidate_openalex_verified",
        "inclusion_status": "candidate_for_manual_verification",
        "manual_verification_required": [
            "top_venue_metric_or_flagship_status",
            "full_text_processability",
            "article_type_and_retraction_status",
            "domain_relevance",
        ],
    }


def summarize_coverage(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    subtopics: dict[str, dict[str, Any]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        grouped[str(candidate["subtopic"])].append(candidate)

    for subtopic, rows in sorted(grouped.items()):
        subtopics[subtopic] = _coverage_counts(rows)

    return {
        "candidate_count": len(candidates),
        "research_article_candidates": sum(
            1 for row in candidates if row.get("work_kind") == "research_article_candidate"
        ),
        "review_candidates": sum(
            1 for row in candidates if row.get("work_kind") == "review_candidate"
        ),
        "open_access_candidates": sum(1 for row in candidates if row.get("open_access")),
        "subtopic_count": len(subtopics),
        "subtopics": subtopics,
        "year_counts": dict(sorted(Counter(str(row["year"]) for row in candidates).items())),
        "work_kind_counts": dict(sorted(Counter(row["work_kind"] for row in candidates).items())),
        "venue_whitelist_status_counts": dict(
            sorted(Counter(row["venue_whitelist_status"] for row in candidates).items())
        ),
        "demo_scale_targets": {
            "source_papers": DEMO_SOURCE_TARGET,
            "corpus_chunks": DEMO_CHUNK_TARGET,
            "questions": DEMO_QUESTION_TARGET,
        },
        "verification_note": (
            "OpenAlex verifies bibliographic metadata candidates. Final inclusion still "
            "requires manual venue, full-text, article-type, retraction, and domain checks."
        ),
    }


def build_acquisition_outputs(
    raw_records: list[dict[str, Any]],
    *,
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    candidates = _dedupe_candidates(
        candidate
        for record in raw_records
        for candidate in [
            normalize_openalex_work(
                record["work"],
                subtopic=str(record["subtopic"]),
                query=str(record["query"]),
            )
        ]
        if candidate is not None
    )
    coverage = summarize_coverage(candidates)

    output_dir.mkdir(parents=True, exist_ok=True)
    candidates_path = output_dir / "candidates.jsonl"
    coverage_path = output_dir / "coverage.json"
    markdown_path = output_dir / "summary.md"
    write_jsonl(candidates_path, candidates)
    coverage_path.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(coverage), encoding="utf-8")
    return candidates_path, coverage_path, markdown_path


def _coverage_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_count": len(rows),
        "research_article_candidates": sum(
            1 for row in rows if row.get("work_kind") == "research_article_candidate"
        ),
        "review_candidates": sum(1 for row in rows if row.get("work_kind") == "review_candidate"),
        "open_access_candidates": sum(1 for row in rows if row.get("open_access")),
        "year_counts": dict(sorted(Counter(str(row["year"]) for row in rows).items())),
    }


def _fetch_json(url: str, *, timeout_seconds: int) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "DomainRAG-Bench/0.1"})
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


def _dedupe_candidates(candidates: Any) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for candidate in candidates:
        key = str(candidate.get("doi") or candidate.get("openalex_id"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return sorted(deduped, key=lambda row: (row["subtopic"], -int(row["year"]), row["title"]))


def _render_markdown(coverage: dict[str, Any]) -> str:
    lines = [
        "# Phase 7D Demo-Scale Source Acquisition",
        "",
        f"- Candidate papers: {coverage['candidate_count']}",
        f"- Research article candidates: {coverage['research_article_candidates']}",
        f"- Review candidates: {coverage['review_candidates']}",
        f"- Open-access candidates: {coverage['open_access_candidates']}",
        f"- Subtopics covered: {coverage['subtopic_count']}",
        "- Inclusion status: candidate_for_manual_verification",
        "",
        "## Subtopic Coverage",
        "",
        "| subtopic | candidates | research | reviews | open access |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for subtopic, values in sorted(coverage["subtopics"].items()):
        lines.append(
            "| "
            + " | ".join(
                [
                    subtopic,
                    str(values["candidate_count"]),
                    str(values["research_article_candidates"]),
                    str(values["review_candidates"]),
                    str(values["open_access_candidates"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Verification Status",
            "",
            coverage["verification_note"],
            "",
        ]
    )
    return "\n".join(lines)


def _work_kind(title: str, work_type: str) -> str:
    lowered_title = title.lower()
    lowered_type = work_type.lower()
    if lowered_type == "review" or "review" in lowered_title or "meta-analysis" in lowered_title:
        return "review_candidate"
    return "research_article_candidate"


def _domain_relevance_terms(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in DOMAIN_RELEVANCE_TERMS if term in lowered]


def _abstract_text(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    words: list[tuple[int, str]] = []
    for word, positions in value.items():
        if not isinstance(word, str) or not isinstance(positions, list):
            continue
        for position in positions:
            if isinstance(position, int):
                words.append((position, word))
    return " ".join(word for _, word in sorted(words))


def _venue_whitelist_status(venue: str) -> str:
    normalized = " ".join(venue.lower().replace("&", "and").split())
    if normalized in DOMAIN_FLAGSHIP_VENUES:
        return "candidate_top_venue_or_domain_flagship"
    return "needs_venue_metric_verification"


def _normalize_doi(value: Any) -> str | None:
    raw = _string_or_none(value)
    if not raw:
        return None
    lowered = raw.lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if lowered.startswith(prefix):
            return raw[len(prefix) :].strip()
    return raw


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _clean_text(value: Any) -> str | None:
    raw = _string_or_none(value)
    if raw is None:
        return None
    unescaped = html.unescape(raw)
    return re.sub(r"<[^>]+>", "", unescaped).strip()


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None
