#!/usr/bin/env python3
"""Validate the framework-neutral AI project template using Python stdlib only."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "AGENTS.md", "VERSION", "CHANGELOG.md", "justfile",
    "doc/ai/PROJECT.md", "doc/ai/CONTEXT.md", "doc/ai/ARCHITECTURE.md",
    "doc/ai/CONVENTIONS.md", "doc/ai/STATUS.md", "doc/ai/ROADMAP.md",
    "doc/ai/CHATGPT_PROJECT.md", "doc/ai/TOOLS.md",
    "doc/ai/decisions/0000-template.md",
    "examples/mcp/codex.config.toml", "examples/mcp/vscode.mcp.json",
    ".agents/skills/implement-feature/SKILL.md",
    ".agents/skills/code-review/SKILL.md",
    ".agents/skills/release/SKILL.md",
    ".agents/skills/documentation/SKILL.md",
    ".agents/skills/knowledge-ingest/SKILL.md",
    ".agents/skills/knowledge-query/SKILL.md",
    ".agents/skills/knowledge-lint/SKILL.md",
    "scripts/validate_knowledge.py", "tests/test_validate_knowledge.py",
    ".github/workflows/ci.yml",
)
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


for name in REQUIRED:
    path = ROOT / name
    check(path.is_file(), f"Missing: {name}")
    if path.is_file():
        check(bool(path.read_text(encoding="utf-8").strip()), f"Empty: {name}")

version_file = ROOT / "VERSION"
if version_file.is_file():
    version = version_file.read_text(encoding="utf-8").strip()
    semver = r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"
    check(bool(re.fullmatch(semver, version)), f"Invalid SemVer: {version}")

for skill in sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md")):
    content = skill.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    check(len(parts) == 3 and not parts[0].strip(), f"Missing YAML frontmatter: {skill}")
    if len(parts) == 3:
        metadata = parts[1]
        match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", metadata)
        check(bool(match), f"Missing skill name: {skill}")
        check(bool(re.search(r"(?m)^description:\s*\S", metadata)), f"Missing description: {skill}")
        if match:
            check(match.group(1) == skill.parent.name, f"Skill name mismatch: {skill}")

chatgpt = ROOT / "doc/ai/CHATGPT_PROJECT.md"
if chatgpt.is_file():
    instructions = chatgpt.read_text(encoding="utf-8")
    for heading in (
        "## 1. Rolle", "## 2. Ziel", "## 3. Kontext",
        "## 4. Einschränkungen", "## 5. Erfolgskriterien", "## 6. Arbeitsweise",
    ):
        check(heading in instructions, f"ChatGPT project instructions missing: {heading}")

project = ROOT / "doc/ai/PROJECT.md"
if project.is_file():
    spec = project.read_text(encoding="utf-8")
    for heading in ("## KI-Rolle", "## Ziel (Goal)", "## Projektbezogene Constraints", "## Erfolgskriterien (Done when)"):
        check(heading in spec, f"PROJECT.md missing: {heading}")

vscode = ROOT / "examples/mcp/vscode.mcp.json"
if vscode.is_file():
    try:
        check(isinstance(json.loads(vscode.read_text(encoding="utf-8")).get("servers"), dict), "Missing MCP server mapping")
    except (json.JSONDecodeError, AttributeError) as exc:
        ERRORS.append(f"Invalid MCP JSON: {exc}")

codex = ROOT / "examples/mcp/codex.config.toml"
if codex.is_file():
    try:
        with codex.open("rb") as stream:
            check(isinstance(tomllib.load(stream).get("mcp_servers"), dict), "Missing Codex MCP server mapping")
    except (tomllib.TOMLDecodeError, OSError) as exc:
        ERRORS.append(f"Invalid MCP TOML: {exc}")

# The entire knowledge/ directory may be removed from smaller projects.
wiki_validator = ROOT / "scripts/validate_knowledge.py"
if wiki_validator.is_file():
    result = subprocess.run(
        [sys.executable, str(wiki_validator), "--root", str(ROOT)],
        capture_output=True, text=True, check=False
    )
    if result.returncode:
        ERRORS.append(f"Knowledge validation failed:\n{result.stdout}{result.stderr}")

if ERRORS:
    print("Template validation FAILED")
    for error in ERRORS:
        print(f"  - {error}")
    sys.exit(1)

print(f"Template validation OK: {len(REQUIRED)} required files checked")
