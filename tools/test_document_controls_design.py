"""Drift guard for docs/design/document-scan-retention-legal-hold.md (Refs #117).

Offline. Checks that the design exists, keeps its required sections and quotes
the constants that doc_controls.py actually uses, so the design cannot drift
silently from the built behaviour.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/design/document-scan-retention-legal-hold.md"
SOURCE = ROOT / "src/core/src/zava_forward/core/doc_controls.py"
SECTIONS = ("## Scan before availability", "## Retention", "## Legal hold", "## Evidence boundary")


class DocumentControlsDesignTest(unittest.TestCase):
    def setUp(self):
        self.doc = DESIGN.read_text(encoding="utf-8")
        self.src = SOURCE.read_text(encoding="utf-8")

    def test_required_sections_present(self):
        for heading in SECTIONS:
            self.assertIn(heading, self.doc)

    def test_defender_tag_values_match_source(self):
        for name in ("DEFENDER_TAG", "DEFENDER_CLEAN", "DEFENDER_BAD"):
            value = re.search(rf'^{name} = "([^"]+)"', self.src, re.MULTILINE).group(1)
            self.assertIn(f"`{value}`", self.doc, name)

    def test_retention_periods_match_source(self):
        body = re.search(r"^RETENTION_YEARS = \{([^}]+)\}", self.src, re.MULTILINE).group(1)
        pairs = re.findall(r'"([^"]+)": (\d+)', body)
        self.assertTrue(pairs)
        for kind, years in pairs:
            self.assertIn(f"{kind} {years}", self.doc)

    def test_relative_links_resolve(self):
        for target in re.findall(r"\]\((\.\./[^)#\s]+)", self.doc):
            self.assertTrue((DESIGN.parent / target).exists(), target)


if __name__ == "__main__":
    unittest.main()
