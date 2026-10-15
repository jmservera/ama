"""Design system foundations: tokens defined and used, state components present, doc inventory matches CSS."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSS = (ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web" / "style.css").read_text()
APP = (ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web" / "app.js").read_text()
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
        for name in re.findall(r"(--[\w-]+):", root):
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
        self.assertIn("## Decision: adopt Fluent UI (Fluent 2)", DOC)
        self.assertNotIn("Status: proposed by the delivery agent", DOC)
        for field in ("Why it is blocked", "Owner", "Next action"):
            self.assertIn(field, DOC)

    def test_fluent_foundation_mapping_and_consumption(self):
        expected = {
            "--colorNeutralForeground1": "#242424",
            "--colorNeutralForeground2": "#424242",
            "--fontSizeBase500": "1.25rem",
            "--fontSizeBase600": "1.5rem",
            "--spacingHorizontalM": ".75rem",
            "--borderRadiusMedium": ".25rem",
            "--borderRadiusXLarge": ".5rem",
            "--durationFast": "150ms",
        }
        for name, value in expected.items():
            self.assertIn(f"{name}:{value};", CSS)
            self.assertIn(f"var({name})", CSS)
        for selector in ("button,.btn", "input,select,textarea", ".card"):
            rule = re.search(re.escape(selector) + r"\{([^}]+)\}", CSS).group(1)
            self.assertIn("var(--radius", rule)
            self.assertIn("var(--sp-", rule)
        self.assertIn("84abdb5fd25a10c627a08465ae82a96e17927270", DOC)

    def test_map_and_filter_signals_have_visible_non_colour_cues(self):
        self.assertNotIn("L.circleMarker", APP)
        self.assertIn('svg("circle"', APP)
        self.assertIn('svg("rect"', APP)
        self.assertIn('svg("path"', APP)
        for code in ("O", "W", "!"):
            self.assertIn(f'code: "{code}"', APP)
        self.assertIn("Safety: ${p.hazards}", APP)
        self.assertIn('"Selected" : "Select filter"', APP)
        self.assertIn('keyboard: true', APP)
        self.assertIn("forced-colors:active", CSS)
        self.assertNotIn('html: `<', APP)


if __name__ == "__main__":
    unittest.main()
