#!/usr/bin/env python3
"""Validate the optional Markdown knowledge base without third-party packages.

The manifest and page frontmatter intentionally use a documented YAML subset.
This is a structural/provenance check, NOT semantic fact verification.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

TYPES = {"concept": "concepts", "entity": "entities", "topic": "topics", "synthesis": "syntheses"}
STATUSES = {"draft", "reviewed", "disputed", "stale"}
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
FIELD = re.compile(r"^([a-z_]+):[ \t]*(.*)$")
LIST_ITEM = re.compile(r"^  -[ \t]+(.+)$")
DOC_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKI_FIELDS = {"id", "title", "type", "status", "updated", "sources", "related"}


def parse_page_frontmatter(path: Path, errors: list[str]) -> dict[str, object]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.S)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        return {}
    fields: dict[str, object] = {}
    active_list: str | None = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        head = FIELD.fullmatch(line)
        if head:
            key, value = head.groups()
            if key in fields:
                errors.append(f"{path}: duplicate field '{key}'")
            fields[key] = [] if value == "[]" or not value else value.strip().strip('"')
            active_list = key if not value else None
        elif (item := LIST_ITEM.fullmatch(line)) and active_list in {"sources", "related"}:
            value = item.group(1).strip().strip('"')
            assert isinstance(fields[active_list], list)
            fields[active_list].append(value)
        else:
            errors.append(f"{path}: unsupported frontmatter line: {line}")
    for key in WIKI_FIELDS - fields.keys():
        errors.append(f"{path}: missing frontmatter field '{key}'")
    for key in ("sources", "related"):
        if key in fields and not isinstance(fields[key], list):
            errors.append(f"{path}: '{key}' must be a YAML sequence or []")
    return fields


def parse_manifest(path: Path, errors: list[str]) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    body = path.read_text(encoding="utf-8").splitlines()
    first = next((line.strip() for line in body if line.strip() and not line.lstrip().startswith("#")), "")
    if first not in {"sources:", "sources: []"}:
        errors.append(f"{path}: expected 'sources:' or 'sources: []'")
        return entries
    current: dict[str, str] | None = None
    def finalize(item: dict[str, str] | None) -> None:
        if item is None:
            return
        ident = item.get("id", "")
        for key in ("id", "title", "uri"):
            if not item.get(key):
                errors.append(f"{path}: missing source field '{key}' for {ident or 'unnamed entry'}")
        if not IDENTIFIER.fullmatch(ident):
            errors.append(f"{path}: invalid source id '{ident}'")
        elif ident in entries:
            errors.append(f"{path}: duplicate source id '{ident}'")
        else:
            entries[ident] = item
        if item.get("retrieved"):
            try:
                date.fromisoformat(item["retrieved"])
            except ValueError:
                errors.append(f"{path}: invalid retrieved date for '{ident}'")
        digest = item.get("sha256", "")
        if digest and not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
            errors.append(f"{path}: sha256 must have 64 hexadecimal characters for '{ident}'")
    for lineno, line in enumerate(body[1:], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if (item := re.fullmatch(r"  - id:[ \t]*(.+)", line)):
            finalize(current)
            current = {"id": item.group(1).strip().strip('"')}
        elif (field := re.fullmatch(r"    ([a-z_]+):[ \t]*(.*)", line)) and current is not None:
            key, value = field.groups()
            if key in current:
                errors.append(f"{path}:{lineno}: repeated source attribute '{key}'")
            current[key] = value.strip().strip('"')
        else:
            errors.append(f"{path}:{lineno}: unsupported manifest syntax")
    finalize(current)
    return entries


def within(path: Path, directory: Path) -> bool:
    return path.is_relative_to(directory)


def link_target(path: Path, target: str, root: Path, errors: list[str]) -> Path | None:
    if target.startswith("#") or urlsplit(target).scheme in {"http", "https", "mailto", "doi"}:
        return None
    if target.startswith("/") or urlsplit(target).scheme:
        errors.append(f"{path}: unsupported local link: {target}")
        return None
    dest = (path.parent / unquote(target.split("#", 1)[0].split("?", 1)[0])).resolve()
    if not within(dest, root.resolve()):
        errors.append(f"{path}: link escapes knowledge directory: {target}")
        return None
    if not dest.is_file():
        errors.append(f"{path}: broken local link: {target}")
    return dest


def validate(root: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    metrics = {"pages": 0, "sources": 0, "indexed_pages": 0}
    base = root / "knowledge"
    if not base.exists():
        return errors, metrics
    required = ["README.md", "SCHEMA.md", "raw/manifest.yaml", "wiki/index.md", "wiki/log.md"]
    for rel in required:
        if not (base / rel).is_file():
            errors.append(f"knowledge/{rel}: missing required file")
    if errors:
        return errors, metrics
    manifest = base / "raw" / "manifest.yaml"
    sources = parse_manifest(manifest, errors)
    metrics["sources"] = len(sources)
    for sid, src in sources.items():
        uri = src.get("uri", "")
        if uri.startswith(("https://", "http://")):
            continue
        if "://" in uri or not uri or uri.startswith("/"):
            errors.append(f"{manifest}: unsupported uri for '{sid}': {uri}")
            continue
        file = (base / "raw" / uri).resolve()
        if not within(file, (base / "raw").resolve()) or not file.is_file():
            errors.append(f"{manifest}: local source not found for '{sid}': {uri}")
            continue
        digest = src.get("sha256", "")
        if digest and hashlib.sha256(file.read_bytes()).hexdigest().lower() != digest.lower():
            errors.append(f"{manifest}: source sha256 mismatch for '{sid}'")
    wiki = base / "wiki"
    pages = [p for p in sorted(wiki.rglob("*.md")) if p not in {wiki / "index.md", wiki / "log.md"}]
    metrics["pages"] = len(pages)
    seen: set[str] = set()
    index = (wiki / "index.md").read_text(encoding="utf-8")
    indexed = set()
    for target in DOC_LINK.findall(index):
        resolved = link_target(wiki / "index.md", target, base, errors)
        if resolved is not None:
            indexed.add(resolved)
    metrics["indexed_pages"] = len(set(p.resolve() for p in pages) & indexed)
    for page in pages:
        fields = parse_page_frontmatter(page, errors)
        ident = str(fields.get("id", ""))
        if not IDENTIFIER.fullmatch(ident):
            errors.append(f"{page}: invalid page id '{ident}'")
        elif ident in seen:
            errors.append(f"{page}: duplicate wiki id '{ident}'")
        seen.add(ident)
        typ = str(fields.get("type", ""))
        if typ not in TYPES or page.parent.name != TYPES.get(typ):
            errors.append(f"{page}: invalid page type or directory '{typ}'")
        if fields.get("status") not in STATUSES:
            errors.append(f"{page}: invalid status '{fields.get('status')}'")
        try:
            date.fromisoformat(str(fields.get("updated", "")))
        except ValueError:
            errors.append(f"{page}: invalid updated date")
        for sid in fields.get("sources", []) if isinstance(fields.get("sources"), list) else []:
            if sid not in sources:
                errors.append(f"{page}: unknown source id '{sid}'")
        for related in fields.get("related", []) if isinstance(fields.get("related"), list) else []:
            link_target(page, str(related), base, errors)
        if page.resolve() not in indexed:
            errors.append(f"{page}: missing entry in wiki/index.md")
    for md in sorted(base.rglob("*.md")):
        for target in DOC_LINK.findall(md.read_text(encoding="utf-8")):
            link_target(md, target, base, errors)
    return sorted(set(errors)), metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--stats", action="store_true", help="Print number of sources and indexed pages")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args()
    errors, metrics = validate(args.root)
    present = (args.root / "knowledge").exists()
    if args.json:
        print(json.dumps({"enabled": present, "ok": not errors, "metrics": metrics, "errors": errors}, ensure_ascii=False))
    elif args.stats:
        print(f"Knowledge: {'enabled' if present else 'disabled'}; sources={metrics['sources']}, pages={metrics['pages']}, indexed_pages={metrics['indexed_pages']}; errors={len(errors)}")
        for error in errors:
            print(f"ERROR: {error}")
    elif errors:
        print("Knowledge validation FAILED")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"Knowledge validation {'OK' if present else 'SKIPPED (optional directory absent)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
