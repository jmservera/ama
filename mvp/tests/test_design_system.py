"""Design system foundations: tokens defined and used, state components present, doc inventory matches CSS."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = (ROOT / "mvp" / "web" / "style.css").read_text()
DOC = (ROOT / "docs" / "reference" / "research" / "ux" / "design-system.md").read_text()
TOKEN_GROUPS = {"colour": "--brand", "type": "--font", "spacing": "--sp-1", "focus": "--focus", "motion": "--motion"}
COMPONENTS = [".empty", ".blocked", ".ai-suggestion", ".ai-label", ".field-error", ".status-line.ok", ".flag.danger"]


class DesignSystem(unittest.TestCase):
    def test_tokens_defined_and_used(self):
        root = re.search(r":root\{(.*?)\n\}", CSS, re.S).group(1)
        for group, token in TOKEN_GROUPS.items():
            self.assertIn(token + ":", root, group)
            self.assertIn("var(%s)" % token, CSS, group)
        self.assertIn("prefers-reduced-motion", CSS)

    def test_every_defined_token_is_documented(self):
        root = re.search(r":root\{(.*?)\n\}", CSS, re.S).group(1)
        for name in re.findall(r"(--[a-z0-9-]+):", root):
            if re.match(r"--sp-\d", name):
                continue
            self.assertIn("`%s`" % name, DOC, name)

    def test_components_and_states(self):
        for c in COMPONENTS:
            self.assertIn(c, CSS, c)
            self.assertIn(c.split(".")[1] if c.count(".") > 1 else c.lstrip("."), DOC, c)
        self.assertIn(":disabled", CSS)
        self.assertIn("aria-invalid", CSS)
        self.assertIn("aria-busy", CSS)

    def test_status_signals_have_non_colour_cue(self):
        for sel in (".flag.danger:before", ".status-line.danger:before", ".status-line.ok:before", ".blocked .blocked-title:before"):
            self.assertIn(sel, CSS)

    def test_ai_label_and_decision_documented(self):
        self.assertIn("AI suggestion, not approved", DOC)
        self.assertIn("## Decision: extend the current UI", DOC)
        for field in ("Why it is blocked", "Owner", "Next action"):
            self.assertIn(field, DOC)


if __name__ == "__main__":
    unittest.main()
