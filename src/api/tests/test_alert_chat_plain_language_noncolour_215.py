"""#215: plain-language labels, non-colour status and keyboard reach for alerts and chat.

Static source checks only. Not screen reader, assistive technology, staff comprehension or
manual acceptance evidence, and no WCAG conformance claim.
"""

import re
import unittest
from pathlib import Path

from zava_forward.core.projection import STAFF_ROLES
from zava_forward.core.regulatory_usage import TASKS

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()
CSS = (WEB / "style.css").read_text()

CHECK_RESULTS = TASKS["regulatory-check"]
BOUNDARY = re.compile(r"(?i)\b(?:not|no|human|person|owner|ask|do not)\b")
# Staff views that #215 names: repairs, housing (building safety) and grants.
ROLE_VIEWS = {
    "repairs": "Resident Liaison Officer",
    "housing": "Building Safety Liaison",
    "grants": "Grants and Evidence Officer",
}


def block(start: str, end: str, source: str = CHAT) -> str:
    first = source.index(start)
    return source[first : source.index(end, first)]


def js_object(body: str) -> dict[str, str]:
    return {
        (a or b): c for a, b, c in re.findall(r'(?:"([^"]+)"|(\w+)): "((?:[^"\\]|\\.)*)"', body)
    }


def glyph_states() -> set[str]:
    return set(re.findall(r"\.state-([\w-]+):before\{content:\"[^\"]+\"", CSS))


class PlainAlertStatusTests(unittest.TestCase):
    def test_every_rule_result_has_a_plain_meaning_that_keeps_the_human_boundary(self) -> None:
        meanings = js_object(block("const meanings = {", "const refresh"))
        for result in CHECK_RESULTS:
            with self.subTest(result=result):
                self.assertIn(result, meanings)
                self.assertTrue(meanings[result].isascii())
                self.assertRegex(meanings[result], BOUNDARY)

    def test_missing_evidence_is_never_explained_as_clear(self) -> None:
        meanings = js_object(block("const meanings = {", "const refresh"))
        self.assertIn("Do not treat this as clear", meanings["unknown"])
        self.assertIn("does not establish compliance", meanings["clear"])
        self.assertIn("not a legal finding", meanings["breach risk"])

    def test_alert_card_keeps_action_owner_citations_and_approval_limit_beside_plain_copy(
        self,
    ) -> None:
        body = block("const alerts = ", "status.className = data.coverage_status")
        for text in (
            '"Safe action"',
            '"Decision owner"',
            '"Clock"',
            "regulatorySources(alert.citations)",
            "Owner acknowledgement:",
            "This panel cannot acknowledge, decide compliance or restart stopped retrofit work.",
        ):
            with self.subTest(text=text):
                self.assertIn(text, body)
        self.assertIn('h("p", { class: "plain-explanation" }, meanings[alert.result]', body)

    def test_plain_copy_is_added_to_the_card_not_swapped_for_the_status_label(self) -> None:
        body = block("const alerts = ", '"Safe action"')
        self.assertIn("`Status: ${alert.result}`", body)
        self.assertLess(body.index("Status: "), body.index("plain-explanation"))


class PlainChatOutcomeTests(unittest.TestCase):
    def test_lookup_outcomes_have_plain_copy_and_conflict_says_do_not_pick(self) -> None:
        meanings = js_object(block("const lookupMeanings = {", "function regulatoryChatPanel"))
        self.assertEqual({"answer", "refused", "conflict"}, set(meanings))
        for kind, text in meanings.items():
            with self.subTest(kind=kind):
                self.assertTrue(text.startswith("In plain words:"))
                self.assertRegex(text, BOUNDARY)
        self.assertIn("Do not pick one", meanings["conflict"])
        self.assertIn("lookupMeanings[answer.kind] || lookupMeanings.refused", CHAT)

    def test_no_citation_answer_states_it_in_words_and_plain_language(self) -> None:
        body = block("function regulatorySources", "function regulatoryAlertsPanel")
        self.assertIn("No source held for this answer. Do not infer a duty or terms", body)
        self.assertIn("In plain words: the lookup found nothing it can show.", body)

    def test_home_chat_outcomes_have_visible_words_and_a_status_sentence(self) -> None:
        names = js_object(block("const outcomeNames = {", "function usageNote"))
        for kind, word in (("answer", "answer"), ("withheld", "withheld"), ("refused", "refused")):
            self.assertEqual(word, names[kind])
        self.assertIn("`Outcome: ${outcome}`", WIDGET)
        status = block("function statusFor(", "const outcomeNames")
        self.assertIn("Reply withheld. Check the case card for recorded facts.", status)
        self.assertIn("Answer added. Check the sources before relying on it.", status)
        self.assertIn("A person must take that action in the workflow.", status)

    def test_home_chat_failure_says_unavailable_with_owner_and_next_action(self) -> None:
        self.assertEqual(
            2, len(re.findall(r"ui\.fail\(`Chat unavailable: .* Owner: .* Next action: ", CHAT))
        )
        self.assertIn('class: "chat-widget-error"', WIDGET)
        self.assertIn('role: "alert"', WIDGET)

    def test_home_chat_keeps_ai_disclosure_and_missing_source_warning(self) -> None:
        self.assertIn("AI-generated content may be incorrect.", CHAT)
        self.assertIn("Model-generated, not approved. Demo only.", CHAT)
        self.assertIn("No supporting source was provided. Check with a person", WIDGET)
        self.assertIn('node("summary", `Sources (${sources.length})`)', WIDGET)

    def test_withheld_draft_is_disclosed_as_withheld_not_as_an_answer(self) -> None:
        body = block("function attribution(", "function statusFor(")
        tail = body[body.index("if (calls && !isAnswer)") :]
        self.assertIn("Generative draft withheld by source check. No record changed.", tail)
        self.assertNotIn("Model-generated", tail.split("return {", 2)[1])


class NonColourStatusTests(unittest.TestCase):
    def test_every_alert_result_and_lookup_kind_has_a_glyph_and_a_shape_cue(self) -> None:
        glyphs = glyph_states()
        for result in CHECK_RESULTS:
            with self.subTest(result=result):
                self.assertIn(result.replace(" ", "-"), glyphs)
        for kind in ("answer", "refused", "conflict", "no-source", "sent", "unknown"):
            with self.subTest(kind=kind):
                self.assertIn(kind, glyphs)
        self.assertRegex(CSS, r"\.regulatory-state\{border-left:4px solid currentColor")

    def test_glyphs_are_decorative_so_the_visible_text_carries_the_meaning(self) -> None:
        for rule in re.findall(r"\.state-[\w-]+:before\{content:\"[^\"]+\"[^}]*\}", CSS):
            with self.subTest(rule=rule):
                self.assertTrue(rule.endswith('/ ""}'))

    def test_glyphs_are_distinct_across_outcomes(self) -> None:
        glyphs = dict(re.findall(r"\.state-([\w-]+):before\{content:\"([^\"]+)\"", CSS))
        pairs = {glyphs[s.replace(" ", "-")] for s in CHECK_RESULTS}
        self.assertEqual(len(CHECK_RESULTS), len(pairs))

    def test_state_class_is_applied_to_text_headings_and_unknown_is_the_fallback(self) -> None:
        self.assertIn("regulatoryStateClass(alert.result)", CHAT)
        self.assertIn("regulatoryStateClass(answer.kind)", CHAT)
        self.assertIn('? value.replace(" ", "-") : "unknown"', CHAT)

    def test_source_freshness_is_stated_in_words_with_a_date_or_unknown(self) -> None:
        body = block("const freshness = card.source_freshness;", "const doubt")
        self.assertIn("Historical source monitoring cadence unknown.", body)
        self.assertIn('as of: ${freshness?.as_of || "unknown"}', body)
        sources = block("function regulatorySources", "function regulatoryAlertsPanel")
        for label in ("Status:", "Effective:", "Retrieved/observed:", "Completeness:"):
            self.assertIn(label, sources)
        self.assertIn("source.currentness", sources)

    def test_status_never_relies_on_a_colour_name_or_colour_only_rule(self) -> None:
        for text in (block("function regulatoryAlertsPanel", "const lookupMeanings"),):
            self.assertIsNone(re.search(r"(?i)\b(red|amber|green)\b", text))
        for rule in re.findall(r"\.state-[\w-]+\{[^}]*\}", CSS):
            self.assertNotRegex(rule, r"^\.state-[\w-]+\{(?:color|background[\w-]*):[^;}]+\}$")


class KeyboardAndRoleViewTests(unittest.TestCase):
    def test_controls_are_native_elements_without_positive_tabindex(self) -> None:
        self.assertIsNone(re.search(r"tabindex\s*[:=]\s*\"?[1-9]", CHAT + WIDGET))
        self.assertNotIn('h("div", { class: "alt", onclick', CHAT)
        self.assertNotIn('h("span", { onclick', CHAT)
        for label in ("Refresh alerts", "Look up cited sources", "Open chat"):
            self.assertIn(label, CHAT)
        self.assertIn('h("button", { type: "button", class: "alt", onclick: load }', CHAT)
        self.assertIn('h("button", { type: "submit" }, "Look up cited sources")', CHAT)

    def test_disabled_doubt_button_stays_focusable_with_a_visible_sent_label(self) -> None:
        body = block("const doubt = ", "item.append(citations")
        self.assertIn('setAttribute("aria-disabled", "true")', body)
        self.assertNotIn(".disabled = true", body)
        self.assertIn("Sent to exercise owner; awaiting human review", body)

    def test_focus_indicator_is_a_non_colour_ring_for_every_control(self) -> None:
        self.assertRegex(CSS, r":focus-visible\{outline:var\(--focus-w\) solid var\(--focus-ink\)")
        self.assertNotRegex(CSS, r":focus\{outline:\s*(?:none|0)")

    def test_plain_mode_toggle_and_summary_are_keyboard_reachable_natives(self) -> None:
        body = block("function regulatoryPlainMode", "const regulatoryStates")
        self.assertIn('type: "checkbox"', body)
        self.assertIn("for: id", body)
        self.assertIn('h("summary", {}, "Cited regulatory lookup (synthetic-demo)")', CHAT)
        self.assertIn("summary.focus()", CHAT)

    def test_repairs_housing_and_grants_views_share_one_panel_with_their_own_role_line(
        self,
    ) -> None:
        helps = js_object(block("const regulatoryRoleHelp = {", "function regulatoryGuidance"))
        self.assertIn("regulatoryGuidance(me.user.role)", CHAT)
        for view, role in ROLE_VIEWS.items():
            with self.subTest(view=view):
                self.assertIn(role, STAFF_ROLES)
                self.assertRegex(helps[role], BOUNDARY)
                self.assertTrue(helps[role].isascii())
        self.assertEqual(1, CHAT.count("function regulatoryAlertsPanel"))
        self.assertEqual(1, CHAT.count("function regulatoryChatPanel"))
        self.assertIn("synthetic-demo only. Exact source excerpts", CHAT)
        self.assertIn("Synthetic data only. Do not enter resident personal", CHAT)


if __name__ == "__main__":
    unittest.main()
