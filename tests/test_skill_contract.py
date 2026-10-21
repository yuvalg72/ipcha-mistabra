"""Offline tests for the ChatGPT Skill interface and human-facing documentation."""
from __future__ import annotations

import sys
import hashlib
import zipfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skill import validate  # noqa: E402
from package import package  # noqa: E402


class SkillContractTests(unittest.TestCase):
    def test_source_contract_is_valid(self):
        self.assertEqual(validate(ROOT), [])

    def test_reference_files_have_a_reader_facing_home(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        reference_files = {p.name for p in (ROOT / "references").glob("*.md")}
        for reference in reference_files - {"evaluation-cases.md"}:
            self.assertIn(reference, skill)

    def test_declared_tool_is_bundled(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("scripts/argument_graph.py", source)
        self.assertTrue((ROOT / "scripts/argument_graph.py").is_file())

    def test_validator_detects_missing_landing_page(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "ipcha-mistabra"
            root.mkdir()
            self.assertTrue(any("Missing required file" in error for error in validate(root)))

    def test_package_is_reproducible_and_has_single_root(self):
        with tempfile.TemporaryDirectory() as temp:
            first = Path(temp) / "one.zip"
            second = Path(temp) / "two.zip"
            package(first)
            package(second)
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(),
                             hashlib.sha256(second.read_bytes()).digest())
            with zipfile.ZipFile(first) as bundle:
                names = bundle.namelist()
                self.assertTrue(all(name.startswith("ipcha-mistabra/") for name in names))
                self.assertIn("ipcha-mistabra/SKILL.md", names)
                self.assertIn("ipcha-mistabra/LICENSE", names)
                self.assertNotIn("ipcha-mistabra/skill.zip", names)
                self.assertTrue(any(name.endswith("/agents/openai.yaml") for name in names))

    def test_no_unsupported_automated_agent_claims(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("not separate independent models", skill)
        self.assertIn("conditional", skill)
        self.assertIn("do not fabricate", skill)


if __name__ == "__main__":
    unittest.main()
