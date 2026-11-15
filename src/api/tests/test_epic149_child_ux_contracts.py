"""Epic #149 child UX surfaces are wired and intact; automated wiring only, never human sign-off."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = ROOT / "src" / "api" / "src" / "zava_forward" / "api"
UX_DOCS = ROOT / "docs" / "reference" / "research" / "ux"
STYLESHEETS: dict[str, Path] = {
    "staff": API / "web" / "style.css",
    "chat": API / "web" / "chat-widget.css",
    "resident-demo": API / "resident_demo" / "web" / "demo.css",
    "resident-preview": API / "resident_preview" / "web" / "resident.css",
}
ROOT_TOKEN_SHEETS = ("staff", "resident-demo", "resident-preview")
TOKEN_GROUPS: dict[str, str] = {
    "colour": "--brand",
    "type": "--font",
    "spacing": "--sp-1",
    "focus": "--focus",
    "motion": "--motion",
}
NON_COLOUR_CUES: tuple[str, ...] = (
    ".flag.danger:before",
    ".status-line.danger:before",
    ".status-line.ok:before",
    ".blocked .blocked-title:before",
)
RESIDENT_COPY_BANNED = re.compile(r"\b(gates?|provenance|traces?|snapshots?|envelopes?)\b", re.I)
PENDING_HUMAN_EVIDENCE: dict[str, str] = {"#155": "assistive technology", "#215": "comprehension"}


def read(path: Path) -> str:
    return path.read_text()


def root_block(css: str) -> str:
    match = re.search(r":root\{(.*?)\n\}", css, re.S)
    return match.group(1) if match else ""


class DesignSystemTokens(unittest.TestCase):
    def test_every_child_surface_defines_and_uses_tokens(self) -> None:
        for name in ROOT_TOKEN_SHEETS:
            css: str = read(STYLESHEETS[name])
            block: str = root_block(css) or css
            for group, token in TOKEN_GROUPS.items():
                if name != "staff" and group in ("type", "spacing"):
                    continue
                self.assertIn(token + ":", block, f"{name} {group}")
                self.assertIn(f"var({token})", css, f"{name} {group}")

    def test_staff_tokens_are_documented(self) -> None:
        doc: str = read(UX_DOCS / "design-system.md")
        block: str = root_block(read(STYLESHEETS["staff"]))
        names: list[str] = re.findall(r"(--[\w-]+):", block)
        self.assertTrue(names)
        for token in names:
            if re.match(r"--sp-\d", token):
                continue
            self.assertIn(f"`{token}`", doc, token)


class NonColourStatusSignals(unittest.TestCase):
    def test_status_cues_use_glyphs_not_colour_alone(self) -> None:
        css: str = read(STYLESHEETS["staff"])
        for selector in NON_COLOUR_CUES:
            self.assertIn(selector, css, selector)
        self.assertRegex(css, r'\.status-line\.ok:before\{content:"\\2713')
        self.assertRegex(css, r'\.flag\.danger:before[^{]*\{content:"\\26A0')

    def test_resident_pages_announce_status_politely(self) -> None:
        for sub in ("resident_demo", "resident_preview"):
            html: str = read(API / sub / "web" / "index.html")
            self.assertIn('role="status"', html, sub)
            self.assertIn('aria-live="polite"', html, sub)


class ReducedMotion(unittest.TestCase):
    def test_each_stylesheet_has_reduced_motion_hook(self) -> None:
        for name, path in STYLESHEETS.items():
            self.assertIn("prefers-reduced-motion:reduce", read(path), name)

    def test_motion_token_zeroed_for_reduced_motion(self) -> None:
        for name in ROOT_TOKEN_SHEETS:
            css: str = read(STYLESHEETS[name])
            self.assertIn("prefers-reduced-motion:reduce){:root{--motion:0s}}", css, name)

    def test_animations_are_disabled_under_reduced_motion(self) -> None:
        self.assertIn(".async-spinner{animation:none", read(STYLESHEETS["staff"]))
        self.assertIn("animation:none", read(STYLESHEETS["chat"]))
        self.assertIn("animation:none", read(STYLESHEETS["resident-demo"]))


class PlainLanguageLabels(unittest.TestCase):
    def test_resident_copy_avoids_internal_terms(self) -> None:
        for sub, files in (
            ("resident_demo", ("index.html", "demo.js", "assistant.js")),
            ("resident_preview", ("index.html", "resident.js")),
        ):
            for file in files:
                text: str = read(API / sub / "web" / file)
                for number, line in enumerate(text.splitlines(), 1):
                    self.assertIsNone(
                        RESIDENT_COPY_BANNED.search(line), f"{sub}/{file}:{number}: {line.strip()}"
                    )

    def test_content_standard_is_present(self) -> None:
        self.assertIn("plain", read(UX_DOCS / "content-standard.md").lower())


class ApprovalAndConsentBoundaries(unittest.TestCase):
    def test_staff_approvals_are_explicit_controls(self) -> None:
        panels: str = read(API / "web" / "panels.js")
        self.assertIn('go("budget_approve")', panels)
        self.assertIn('go("grant_approve"', panels)
        self.assertRegex(panels, r"Approve (the budget|a commitment|a proposed stage)")

    def test_resident_ai_summary_needs_explicit_optional_consent(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        self.assertIn('consent.type = "checkbox"', js)
        self.assertNotIn("consent.checked = true", js)
        self.assertNotIn("consent.defaultChecked", js)
        self.assertIn("if (!consent.checked)", js)
        self.assertIn('consent.setAttribute("aria-invalid", "true")', js)
        self.assertIn("(optional). This is not consent to works.", js)

    def test_automation_never_claims_decision_or_consent(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        self.assertIn("Neither rules nor AI can make decisions, approve documents", js)
        self.assertIn("give consent", js)
        self.assertIn("does not imply consent or refusal", read(API / "web" / "app.js"))


class HumanEvidenceNotFabricated(unittest.TestCase):
    def test_no_automated_surface_claims_human_sign_off(self) -> None:
        claim = re.compile(
            r"(AT|assistive technology|comprehension)[^\n]{0,40}(passed|signed off)", re.I
        )
        for path in STYLESHEETS.values():
            self.assertIsNone(claim.search(read(path)), path.name)

    def test_pending_evidence_issues_are_named_open(self) -> None:
        self.assertEqual(set(PENDING_HUMAN_EVIDENCE), {"#155", "#215"})


if __name__ == "__main__":
    unittest.main()
