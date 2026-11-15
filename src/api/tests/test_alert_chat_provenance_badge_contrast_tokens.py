"""#215 criterion 3: contrast of alert severity chips and chat provenance badges.

Computes WCAG 2.2 relative-luminance contrast (SC 1.4.3, AA >= 4.5:1) from the shipped CSS
tokens (light) and from Fluent 2 web dark reference values (dark). The app ships no dark
theme today, so the dark values are an explicit reference table, not shipped CSS. Static
source and arithmetic only; not rendered-colour, assistive technology or conformance evidence.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET_JS = (WEB / "chat-widget.js").read_text()
WIDGET_CSS = (WEB / "chat-widget.css").read_text()
CSS = (WEB / "style.css").read_text()

AA = 4.5

# Fluent 2 webDarkTheme neutral values used by the aliases below (reference, not shipped).
DARK_TOKENS = {
    "colorNeutralForeground1": "#ffffff",
    "colorNeutralForeground2": "#d6d6d6",
    "colorNeutralBackground1": "#292929",
    "colorNeutralBackground2": "#1f1f1f",
}
ALIASES = {
    "--ink": "colorNeutralForeground1",
    "--muted": "colorNeutralForeground2",
    "--surface": "colorNeutralBackground1",
    "--bg": "colorNeutralBackground2",
}
STATES = (
    "breach-risk",
    "attention",
    "unknown",
    "clear",
    "not-applicable",
    "answer",
    "refused",
    "conflict",
    "no-source",
    "sent",
)
# Provenance variants of attribution() in chat.js: visible label text per answer source.
PROVENANCE = {
    "decision-model": (
        "Deterministic decision or workflow rule (not generative AI; no record changed)"
    ),
    "generative-model": (
        "Generative model suggestion (unapproved; check cited sources; no record changed)"
    ),
    "withheld": (
        "Withheld. Cited sources did not support a stated status or figure (no record changed)"
    ),
    "abstain": ("Withheld. The permitted sources do not cover the question (no record changed)"),
    "workflow-only": "Workflow-only help, no record changed",
}


def root_tokens() -> dict[str, str]:
    block = CSS[CSS.index(":root{") : CSS.index("}", CSS.index(":root{"))]
    return dict(re.findall(r"(--[\w-]+):([^;]+);", block))


def resolve(name: str, tokens: dict[str, str]) -> str:
    value = tokens[name].strip()
    while value.startswith("var("):
        inner = value[4:-1].strip()
        value = tokens[inner].strip() if inner in tokens else inner
    return value


def channel(value: int) -> float:
    s = value / 255
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def luminance(colour: str) -> float:
    digits = colour.lstrip("#")
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    r, g, b = (int(digits[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(fg: str, bg: str) -> float:
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def themes() -> dict[str, dict[str, str]]:
    light = root_tokens()
    dark = {alias: DARK_TOKENS[source] for alias, source in ALIASES.items()}
    return {
        "light": {alias: resolve(alias, light) for alias in ALIASES},
        "dark": dark,
    }


# (text token, surface token) for each component, from the cascade in the CSS above.
# Alert chips inherit --ink and sit on the card --surface or the page --bg.
CHIP_PAIRS = (("--ink", "--surface"), ("--ink", "--bg"))
# Provenance badges use .chat-widget-meta (--muted) inside .chat-widget-message (--bg),
# and the user bubble (--soft) is not a provenance surface.
BADGE_PAIRS = (("--muted", "--bg"), ("--muted", "--surface"))


class TokenResolutionTests(unittest.TestCase):
    def test_light_tokens_resolve_to_fluent_neutral_values_from_the_css(self) -> None:
        light = themes()["light"]
        self.assertEqual(light["--ink"], "#242424")
        self.assertEqual(light["--muted"], "#424242")
        self.assertEqual(light["--surface"], "#fff")
        self.assertEqual(light["--bg"], "#f5f7f8")

    def test_dark_reference_covers_every_alias_the_components_use(self) -> None:
        self.assertEqual(set(themes()["dark"]), set(ALIASES))

    def test_contrast_helper_matches_known_wcag_values(self) -> None:
        self.assertAlmostEqual(contrast("#000", "#fff"), 21.0, places=1)
        self.assertAlmostEqual(contrast("#777", "#fff"), 4.48, places=1)


class SeverityChipContrastTests(unittest.TestCase):
    def test_alert_chip_text_has_no_override_colour_so_it_inherits_ink(self) -> None:
        for state in STATES:
            with self.subTest(state=state):
                rules = re.findall(rf"\.state-{state}(?::before)?\{{([^}}]*)\}}", CSS)
                self.assertTrue(rules)
                self.assertFalse(any(re.search(r"(?<!-)color:", rule) for rule in rules))
        base = re.search(r"\.regulatory-state\{([^}]*)\}", CSS)
        self.assertIsNotNone(base)
        assert base is not None
        self.assertNotRegex(base.group(1), r"(?<!-)color:")

    def test_alert_chip_text_meets_aa_on_light_and_dark_surfaces(self) -> None:
        for theme, tokens in themes().items():
            for fg, bg in CHIP_PAIRS:
                with self.subTest(theme=theme, fg=fg, bg=bg):
                    self.assertGreaterEqual(contrast(tokens[fg], tokens[bg]), AA)

    def test_every_severity_chip_has_a_text_glyph_and_border_cue_besides_colour(self) -> None:
        glyphs = dict(re.findall(r"\.state-([\w-]+):before\{content:\"([^\"]+)\" / \"\"\}", CSS))
        self.assertEqual(set(STATES) - set(glyphs), set())
        self.assertRegex(CSS, r"\.regulatory-state\{border-left:4px solid currentColor")
        self.assertIn("`Status: ${regulatoryStateLabel(alert.result)}`", CHAT)
        self.assertIn("`Lookup status: ${answer.kind}`", CHAT)


class ProvenanceBadgeContrastTests(unittest.TestCase):
    def test_badge_rule_sets_only_token_colours(self) -> None:
        meta = re.search(r"\.chat-widget-meta\{([^}]*)\}", WIDGET_CSS)
        self.assertIsNotNone(meta)
        assert meta is not None
        self.assertIn("color:var(--muted)", meta.group(1))
        message = re.search(r"\.chat-widget-message\{([^}]*)\}", WIDGET_CSS)
        self.assertIsNotNone(message)
        assert message is not None
        self.assertIn("background:var(--bg)", message.group(1))

    def test_provenance_badge_text_meets_aa_on_light_and_dark_surfaces(self) -> None:
        for theme, tokens in themes().items():
            for fg, bg in BADGE_PAIRS:
                with self.subTest(theme=theme, fg=fg, bg=bg):
                    self.assertGreaterEqual(contrast(tokens[fg], tokens[bg]), AA)

    def test_each_provenance_variant_has_distinct_visible_text_not_colour_alone(self) -> None:
        self.assertEqual(len(set(PROVENANCE.values())), len(PROVENANCE))
        for variant, label in PROVENANCE.items():
            with self.subTest(variant=variant):
                self.assertIn(label, CHAT)
        # Decision-model, generative-model and withheld/workflow-only never share a label,
        # and fallback keeps explicit withheld-draft detail text.
        self.assertTrue(PROVENANCE["decision-model"].startswith("Deterministic decision"))
        self.assertTrue(PROVENANCE["generative-model"].startswith("Generative model suggestion"))
        self.assertTrue(PROVENANCE["withheld"].startswith("Withheld."))
        self.assertIn("Workflow-only", PROVENANCE["workflow-only"])
        self.assertIn("The generative draft did not pass the source check and was not shown.", CHAT)

    def test_badge_is_rendered_as_text_with_an_outcome_cue(self) -> None:
        self.assertIn('node("small", label, { class: "chat-widget-meta" })', WIDGET_JS)
        self.assertIn("`Outcome: ${outcome}`", WIDGET_JS)
        self.assertIn("outcome: outcomeNames[answer.kind]", CHAT)


if __name__ == "__main__":
    unittest.main()
