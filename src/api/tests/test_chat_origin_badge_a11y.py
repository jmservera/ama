"""#215 criterion 3: origin badges, live-region announcements and source disclosures.

Static source checks only, not screen reader, assistive technology or staff comprehension evidence.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()
JARGON = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?|llm)\b", re.I)


def const(name: str) -> str:
    match = re.search(rf'const {name} = ORIGIN \+ "([^"]+)"', CHAT)
    assert match, name
    return match.group(1)


def function_body(name: str) -> str:
    start = CHAT.index(f"function {name}(")
    return CHAT[start : CHAT.index("\n  }\n", start)]


class OriginBadgeAnnouncementTests(unittest.TestCase):
    def test_origin_labels_name_the_origin_in_words_and_differ(self) -> None:
        rule, model, withheld = const("RULE_LABEL"), const("MODEL_LABEL"), const("WITHHELD_LABEL")
        self.assertIn("Deterministic decision or workflow rule", rule)
        self.assertIn("not generative AI", rule)
        self.assertTrue(model.startswith("Generative model suggestion"))
        self.assertIn("unapproved", model)
        self.assertTrue(withheld.startswith("Withheld."))
        for text in (rule, model, withheld):
            self.assertIn("no record changed", text)
        self.assertEqual(len({rule, model, withheld}), 3)
        self.assertNotIn("generative", withheld.lower())

    def test_each_origin_detail_says_where_the_reply_came_from(self) -> None:
        body = function_body("attribution")
        self.assertIn("Source: deterministic decision rules from recorded case facts", body)
        self.assertIn("(0 generative calls)", body)
        self.assertIn("Source: generative AI model (${answer.model})", body)
        self.assertIn("AI-generated content may be incorrect.", body)
        self.assertIn("Source: no answer was shown.", body)
        self.assertIn("did not pass the source check and was not shown", body)
        self.assertEqual(body.count('const check = " Check the sources."'), 1)

    def test_rule_tags_distinguish_workflow_decision_and_case_record(self) -> None:
        body = function_body("sourceLine")
        for tag in ("[Workflow rule]", "[Decision rule]", "[Case record]"):
            self.assertIn(tag, body)
        self.assertNotIn("[Generative model]", body)

    def test_live_status_text_differs_for_answer_and_withheld_replies(self) -> None:
        body = function_body("statusFor")
        self.assertIn("Reply withheld. Check the case card for recorded facts.", body)
        self.assertIn("Answer added. Check the sources before relying on it.", body)
        self.assertIn("Request refused.", body)
        self.assertIn("Workflow-only help added. No assistant answer was given.", body)
        self.assertIn("ui.setStatus(statusFor(answer.kind))", CHAT)

    def test_message_passes_label_outcome_detail_and_sources_to_the_widget(self) -> None:
        call = CHAT[CHAT.index('ui.message("assistant"') :]
        call = call[: call.index("});")]
        for field in (
            "label: view.label",
            "outcome: outcomeNames",
            "detail:",
            "sources: (answer.citations",
        ):
            self.assertIn(field, call)
        self.assertIn('withheld: "withheld"', CHAT)
        self.assertIn('abstain: "withheld"', CHAT)


class LiveRegionAndDisclosureTests(unittest.TestCase):
    def test_log_and_status_are_polite_live_regions_and_not_assertive(self) -> None:
        self.assertRegex(
            WIDGET, r'role: "log", "aria-live": "polite", "aria-relevant": "additions"'
        )
        self.assertRegex(WIDGET, r'role: "status", "aria-live": "polite", "aria-atomic": "true"')
        self.assertNotIn('"aria-live": "assertive"', WIDGET)

    def test_message_text_order_puts_outcome_and_origin_before_the_reply(self) -> None:
        start = WIDGET.index("function message(")
        body = WIDGET[start : WIDGET.index("log.append(item)", start)]
        order = [
            body.index(token)
            for token in ("Outcome: ${outcome}", "label, {", 'node("p", text)', "detail, {")
        ]
        self.assertEqual(order, sorted(order))

    def test_origin_is_text_not_colour_only(self) -> None:
        self.assertIn("`Outcome: ${outcome}`", WIDGET)
        self.assertNotRegex(WIDGET, r"chat-widget-outcome[^;\n]*style\.color")

    def test_source_count_is_disclosed_and_empty_sources_are_explained(self) -> None:
        self.assertIn("`Sources (${sources.length})`", WIDGET)
        self.assertIn('node("details")', WIDGET)
        self.assertIn(
            "No supporting source was provided. Check with a person before relying on this reply.",
            WIDGET,
        )
        self.assertIn('if (role !== "user")', WIDGET)

    def test_origin_copy_avoids_internal_jargon(self) -> None:
        copy = " ".join(
            [
                const("RULE_LABEL"),
                const("MODEL_LABEL"),
                const("WITHHELD_LABEL"),
                function_body("attribution"),
                function_body("statusFor"),
            ]
        )
        strings = " ".join(a or b for a, b in re.findall(r'"([^"]+)"|`([^`]+)`', copy))
        self.assertNotRegex(strings.replace("generative-grounded", ""), JARGON)


if __name__ == "__main__":
    unittest.main()
