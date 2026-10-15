"""WCAG 2.2 baseline (#151): static checks on the workbench pages, tokens and the audit record."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "mvp" / "web"
CSS = (WEB / "style.css").read_text()
APP = (WEB / "app.js").read_text()
DOC = (ROOT / "docs" / "reference" / "research" / "ux" / "wcag-conformance-baseline.md").read_text()


def token(name):
    value = re.search(r"--%s:(#[0-9a-fA-F]{3,6})[;}]" % name, CSS).group(1)
    return "#" + "".join(c * 2 for c in value[1:]) if len(value) == 4 else value


def lum(hex_colour):
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


class Wcag22Baseline(unittest.TestCase):
    def test_pages_declare_language_and_allow_zoom(self):
        for page in ("index.html", "welcome.html"):
            html = (WEB / page).read_text()
            self.assertIn('lang="en-GB"', html, page)
            self.assertIn("width=device-width", html, page)
            self.assertNotIn("user-scalable=no", html, page)
            self.assertNotIn("maximum-scale", html, page)

    def test_text_contrast_meets_aa(self):
        pairs = [("ink", "bg"), ("ink", "surface"), ("muted", "surface"), ("muted", "bg"), ("surface", "brand"),
                 ("surface", "brand-d"), ("brand", "surface"), ("brand", "soft"), ("warn", "warn-bg"), ("ok", "ok-bg")]
        for fg, bg in pairs:
            self.assertGreaterEqual(ratio(token(fg), token(bg)), 4.5, "%s on %s" % (fg, bg))

    def test_non_text_contrast_meets_aa(self):
        self.assertGreaterEqual(ratio(token("field-line"), token("surface")), 3.0)
        self.assertGreaterEqual(ratio(token("focus-ink"), token("surface")), 3.0)

    def test_focus_indicator_is_two_tone_and_never_removed(self):
        self.assertRegex(CSS, r":focus-visible\{outline:var\(--focus-w\) solid var\(--focus-ink\)")
        self.assertIn("box-shadow:0 0 0 var(--focus-off) var(--focus)", CSS)
        self.assertNotRegex(CSS, r"outline:\s*(none|0)\b")

    def test_charts_and_map_have_accessible_equivalents(self):
        self.assertIn('role: "img"', APP)
        self.assertIn("Show this chart as a table", APP)
        self.assertIn('scope: "col"', APP)
        self.assertIn("Show the map areas as a list", APP)

    def test_status_regions_exist(self):
        self.assertIn('role="status"', (WEB / "index.html").read_text())
        self.assertIn('role="alert"', (WEB / "index.html").read_text())
        self.assertIn("aria-live", APP)

    def test_audit_record_names_target_gaps_and_makes_no_conformance_claim(self):
        self.assertIn("WCAG 2.2", DOC)
        self.assertIn("pending owner confirmation", DOC)
        self.assertIn("we do not claim conformance", DOC)
        for role in ("Retrofit Coordinator", "Quality Inspector", "Contractor view"):
            self.assertIn(role, DOC)
        self.assertNotRegex(DOC, r"(?i)\bfully conforms\b|\bis WCAG 2\.2 (AA )?compliant\b")


if __name__ == "__main__":
    unittest.main()
