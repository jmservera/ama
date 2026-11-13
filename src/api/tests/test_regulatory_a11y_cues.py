"""#215 criterion 3: non-colour cues, Escape on the chat disclosure and plain-language copy.

Static source checks only, not screen reader, assistive technology or staff comprehension evidence.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
JS = (WEB / "chat.js").read_text()
CSS = (WEB / "style.css").read_text()
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
BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)


class RegulatoryCueTests(unittest.TestCase):
    def test_every_state_has_a_decorative_glyph_and_a_border_cue(self) -> None:
        for state in STATES:
            with self.subTest(state=state):
                glyph = re.search(rf"\.state-{state}:before\{{content:\"[^\"]+\" / \"\"\}}", CSS)
                self.assertIsNotNone(glyph, "glyph needs an empty alternative")
        # The base rule gives every state a non-colour shape even if a glyph font is missing.
        self.assertRegex(CSS, r"\.regulatory-state\{border-left:4px solid currentColor")
        glyphs = re.findall(r"\.state-([\w-]+):before\{content:\"([^\"]+)\"", CSS)
        by_state = dict(glyphs)
        self.assertNotEqual(by_state["breach-risk"], by_state["attention"])
        self.assertNotEqual(by_state["clear"], by_state["unknown"])
        self.assertNotEqual(by_state["refused"], by_state["answer"])

    def test_state_text_is_still_visible_and_classes_are_applied(self) -> None:
        alert = 'h("h3", { class: regulatoryStateClass(alert.result) }, `Status: ${alert.result}`)'
        lookup = (
            'h("h3", { class: regulatoryStateClass(answer.kind) }, `Lookup status: ${answer.kind}`)'
        )
        self.assertIn(alert, JS)
        self.assertIn(lookup, JS)
        self.assertIn('class: "regulatory-state state-no-source"', JS)
        self.assertEqual(JS.count('classList.add("regulatory-state", "state-sent")'), 2)
        self.assertIn('status.className = "regulatory-state state-unknown"', JS)

    def test_unrecognised_state_falls_back_to_unknown_not_unmarked(self) -> None:
        fallback = 'regulatoryStates.has(value) ? value.replace(" ", "-") : "unknown"'
        self.assertIn(fallback, JS)

    def test_escape_closes_chat_disclosure_and_restores_summary_focus(self) -> None:
        start = JS.index('root.addEventListener("keydown"')
        body = JS[start : JS.index("});", start)]
        self.assertIn('event.key !== "Escape" || !root.open', body)
        self.assertIn("root.open = false", body)
        self.assertIn("summary.focus()", body)

    def test_plain_explanations_cover_each_outcome_route_and_unknown_state(self) -> None:
        meanings = JS[JS.index("const lookupMeanings") : JS.index("function regulatoryChatPanel")]
        for outcome in ("answer", "refused", "conflict"):
            self.assertRegex(meanings, rf"\b{outcome}: \"In plain words:")
        self.assertIn("In plain words: the lookup found nothing it can show", JS)
        self.assertIn("Sending does not approve or decide anything", JS)
        self.assertRegex(
            CSS, r"\.regulatory\.plain-language li\.plain-explanation\{display:list-item\}"
        )

    def test_new_plain_copy_avoids_internal_terms_and_non_ascii(self) -> None:
        copy = re.findall(r'"(In plain words:[^"]*)"', JS)
        self.assertGreaterEqual(len(copy), 5)
        for text in copy:
            with self.subTest(text=text[:40]):
                self.assertIsNone(BANNED.search(text))
                self.assertTrue(text.isascii())
                self.assertNotIn("\u2014", text)

    def test_no_new_invalid_field_site_in_chat_script(self) -> None:
        self.assertNotIn("aria-invalid", JS)


if __name__ == "__main__":
    unittest.main()
