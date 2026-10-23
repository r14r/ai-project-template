"""Regression tests for the optional knowledge validator (stdlib unittest)."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_knowledge.py"


class KnowledgeValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / "knowledge"
        (self.base / "raw" / "sources").mkdir(parents=True)
        (self.base / "wiki" / "concepts").mkdir(parents=True)
        (self.base / "README.md").write_text("# Knowledge\n", encoding="utf-8")
        (self.base / "SCHEMA.md").write_text("# Schema\n", encoding="utf-8")
        (self.base / "raw" / "manifest.yaml").write_text("sources: []\n", encoding="utf-8")
        (self.base / "wiki" / "index.md").write_text("# Index\n", encoding="utf-8")
        (self.base / "wiki" / "log.md").write_text("# Log\n", encoding="utf-8")

    def run_validation(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "--json"],
            capture_output=True, text=True, check=False
        )

    def add_page(self, sources="[]", index=True):
        page = self.base / "wiki" / "concepts" / "one.md"
        page.write_text(
            "---\nid: one\ntitle: One\ntype: concept\nstatus: draft\n"
            f"updated: 2026-10-23\nsources: {sources}\nrelated: []\n---\n# One\n",
            encoding="utf-8"
        )
        if index:
            (self.base / "wiki" / "index.md").write_text("# Index\n- [One](concepts/one.md)\n", encoding="utf-8")
        return page

    def test_empty_optional_wiki(self):
        self.assertEqual(self.run_validation().returncode, 0)

    def test_missing_knowledge_directory_is_allowed(self):
        import shutil
        shutil.rmtree(self.base)
        self.assertEqual(self.run_validation().returncode, 0)

    def test_valid_source_reference(self):
        (self.base / "raw" / "manifest.yaml").write_text(
            "sources:\n  - id: s1\n    title: Source\n    uri: https://example.org\n", encoding="utf-8"
        )
        page = self.add_page()
        page.write_text(page.read_text(encoding="utf-8").replace("sources: []", "sources:\n  - s1"), encoding="utf-8")
        self.assertEqual(self.run_validation().returncode, 0)

    def test_unknown_source_fails(self):
        self.add_page(sources="unknown")
        result = self.run_validation()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be a YAML sequence", result.stdout)

    def test_orphaned_page_fails(self):
        self.add_page(index=False)
        self.assertIn("missing entry in wiki/index.md", self.run_validation().stdout)

    def test_broken_link_fails(self):
        self.add_page()
        (self.base / "wiki" / "index.md").write_text(
            "# Index\n- [One](concepts/one.md)\n- [Missing](concepts/missing.md)\n", encoding="utf-8"
        )
        self.assertIn("broken local link", self.run_validation().stdout)

    def test_duplicate_source_fails(self):
        (self.base / "raw" / "manifest.yaml").write_text(
            "sources:\n  - id: duplicate\n    title: A\n    uri: https://one.invalid\n"
            "  - id: duplicate\n    title: B\n    uri: https://two.invalid\n",
            encoding="utf-8"
        )
        self.assertIn("duplicate source id", self.run_validation().stdout)

    def test_broken_local_source_fails(self):
        (self.base / "raw" / "manifest.yaml").write_text(
            "sources:\n  - id: local\n    title: Reference\n    uri: sources/absent.txt\n",
            encoding="utf-8"
        )
        self.assertIn("local source not found", self.run_validation().stdout)


if __name__ == "__main__":
    unittest.main()
