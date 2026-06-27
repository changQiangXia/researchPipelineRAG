from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import textwrap

from domainrag.easy_dataset_adapter import export_domainrag_bundle
from domainrag.validator import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_ROOT = ROOT / "integrations" / "easy-dataset" / "domainrag-export"
README = INTEGRATION_ROOT / "README.md"
HELPER = INTEGRATION_ROOT / "files" / "lib" / "domainrag" / "exporter.js"
ROUTE = (
    INTEGRATION_ROOT
    / "files"
    / "app"
    / "api"
    / "projects"
    / "[projectId]"
    / "domainrag-export"
    / "route.js"
)


def test_easy_dataset_domainrag_integration_assets_exist():
    assert README.exists()
    assert HELPER.exists()
    assert ROUTE.exists()
    readme_text = README.read_text(encoding="utf-8")
    assert "files/lib/domainrag/exporter.js" in readme_text
    assert "files/app/api/projects/[projectId]/domainrag-export/route.js" in readme_text
    assert "chunks.jsonl" in readme_text
    assert "items.jsonl" in readme_text


def test_easy_dataset_domainrag_route_references_helper_and_upstream_patterns():
    route_text = ROUTE.read_text(encoding="utf-8")
    helper_text = HELPER.read_text(encoding="utf-8")

    assert "@/lib/db/index" in route_text
    assert "@/lib/db/evalDatasets" in route_text
    assert "@/lib/domainrag/exporter" in route_text
    assert "export async function POST" in route_text
    assert "export async function GET" in route_text
    assert "buildDomainRAGBundle" in route_text
    assert "export function buildDomainRAGBundle" in helper_text
    assert "chunks.jsonl" in helper_text
    assert "items.jsonl" in helper_text
    assert "source_chunk_ids" in helper_text


def test_easy_dataset_domainrag_assets_parse_as_javascript():
    node = shutil.which("node")
    assert node is not None, "node is required for JavaScript asset syntax checks"

    for path in [HELPER, ROUTE]:
        result = subprocess.run(
            [node, "--check", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr


def test_easy_dataset_domainrag_helper_payload_feeds_python_exporter(
    tmp_path: Path,
):
    node = shutil.which("node")
    assert node is not None, "node is required for JavaScript helper smoke test"

    helper_copy = tmp_path / "exporter.mjs"
    helper_copy.write_text(HELPER.read_text(encoding="utf-8"), encoding="utf-8")
    runner = tmp_path / "run-helper.mjs"
    runner.write_text(
        textwrap.dedent(
            f"""
            import {{ buildDomainRAGBundle }} from {json.dumps(helper_copy.as_uri())};

            const rows = [
              {{
                id: "ed_q_001",
                question: "Which feature slows oxygen ingress at high temperature?",
                questionType: "single_choice",
                options: JSON.stringify([
                  "Chromium-rich oxide scales",
                  "Cooling fins",
                  "Vacuum seals",
                  "Random sampling"
                ]),
                correctAnswer: "A",
                tags: "domainrag,subdomain:oxidation,knowledge:mechanism",
                chunkId: "ed_chunk_001",
                chunks: {{
                  id: "ed_chunk_001",
                  name: "oxidation-part-1",
                  fileName: "hidden-source.md",
                  content: "Oxidation\\nChromium-rich oxide scales can slow oxygen ingress at high temperature."
                }}
              }},
              {{
                id: "ed_q_002",
                question: "Creep rate increases when temperature and applied ____ increase together.",
                questionType: "fill_blank",
                options: "",
                correctAnswer: "stress",
                tags: "domainrag,subdomain:creep,knowledge:condition,difficulty:medium",
                chunkId: "ed_chunk_002",
                chunks: {{
                  id: "ed_chunk_002",
                  name: "creep-part-1",
                  fileName: "hidden-source.md",
                  content: "Creep\\nCreep rate increases when temperature and applied stress increase together."
                }}
              }},
              {{
                id: "ed_q_003",
                question: "Why can fine precipitates improve high-temperature strength?",
                questionType: "open_ended",
                options: "",
                correctAnswer: "Fine precipitates impede dislocation motion.",
                tags: "domainrag,subdomain:microstructure,knowledge:mechanism,difficulty:hard",
                chunkId: "ed_chunk_003",
                chunks: {{
                  id: "ed_chunk_003",
                  name: "microstructure-part-1",
                  fileName: "hidden-source.md",
                  content: "Microstructure\\nFine precipitates impede dislocation motion and improve high-temperature strength."
                }}
              }}
            ];

            const bundle = buildDomainRAGBundle(rows, {{
              splits: {{
                dev: ["ed_q_001"],
                test: ["ed_q_002"],
                fresh_hard: ["ed_q_003"]
              }},
              defaults: {{
                subdomain: "general",
                knowledge_type: "fact",
                difficulty: "easy",
                quality_score: 0.95
              }},
              itemOverrides: {{
                ed_q_002: {{
                  answer_aliases: ["applied stress"]
                }},
                ed_q_003: {{
                  required_points: [
                    "fine precipitates",
                    "impede dislocation motion",
                    "improve high-temperature strength"
                  ]
                }}
              }}
            }});

            console.log(JSON.stringify(bundle));
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [node, str(runner)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    bundle = json.loads(result.stdout)
    assert bundle["errors"] == []
    files = {file["path"]: file["content"] for file in bundle["files"]}
    assert set(files) == {"chunks.jsonl", "items.jsonl"}
    exported_items = [
        json.loads(line)
        for line in files["items.jsonl"].splitlines()
        if line.strip()
    ]
    assert [item["quality_score"] for item in exported_items] == [0.95, 0.95, 0.95]

    source = tmp_path / "easy-dataset-export"
    source.mkdir()
    for file_name, content in files.items():
        (source / file_name).write_text(content, encoding="utf-8")

    domainrag_bundle = export_domainrag_bundle(source, tmp_path / "outputs", "from_easy_dataset_route")
    validate_dataset(domainrag_bundle.dataset_dir)
    assert bundle["statistics"]["split_counts"] == {
        "dev": 1,
        "fresh_hard": 1,
        "test": 1,
    }


def test_easy_dataset_domainrag_integration_assets_do_not_contain_secrets():
    secret_patterns = [
        re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(
            r"(api[_-]?key|authorization)\s*[:=]\s*['\"][^'\"\n]+",
            re.IGNORECASE,
        ),
    ]
    checked_files = [README, HELPER, ROUTE]
    for path in checked_files:
        text = path.read_text(encoding="utf-8")
        for pattern in secret_patterns:
            assert not pattern.search(text), f"secret-like value found in {path}"
