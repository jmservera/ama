"""#215: source-origin attribution, citation disclosure and warning banner for alerts and chat.

Static source checks only, not screen reader, assistive technology or staff comprehension evidence.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()


def _attribution() -> str:
    start = CHAT.index('const ORIGIN = "Answer origin: ";')
    return CHAT[start : CHAT.index("function statusFor(", start)]


class SourceOriginAttributionTests(unittest.TestCase):
    def test_each_origin_has_its_own_visible_label_and_source_sentence(self) -> None:
        body = _attribution()
        self.assertIn(
            'const RULE_LABEL = ORIGIN + "Deterministic decision or workflow rule '
            '(not generative AI; no record changed)";',
            body,
        )
        self.assertIn(
            'const MODEL_LABEL = ORIGIN + "Generative model suggestion '
            '(unapproved; check cited sources; no record changed)";',
            body,
        )
        expected = {
            "decision-rules": (
                "label: RULE_LABEL",
                "Origin: decision_rule. Source: deterministic decision rules "
                "from recorded case facts (0 generative calls).",
            ),
            "decision-rules-fallback": (
                "label: RULE_LABEL",
                "The generative draft did not pass the source check and was not shown.",
            ),
            "generative-grounded": (
                "label: MODEL_LABEL",
                "Origin: generative_model. Source: generative AI model",
            ),
        }
        for origin, (label_ref, phrase) in expected.items():
            with self.subTest(origin=origin):
                branch = body[body.index(f'source === "{origin}"') :]
                branch = branch[: branch.index("};") + 2]
                self.assertIn(label_ref, branch)
                self.assertIn(phrase, branch)
        self.assertEqual(len({phrase for _, phrase in expected.values()}), 3)

    def test_generative_origin_warns_it_may_be_wrong_and_asks_for_a_source_check(self) -> None:
        body = _attribution()
        self.assertIn("AI-generated content may be incorrect.", body)
        self.assertEqual(body.count('const check = " Check the sources.";'), 1)
        self.assertEqual(body.count("${check}") + body.count("+ check"), 3)

    def test_deterministic_origin_is_never_labelled_as_model_output(self) -> None:
        body = _attribution()
        rule = body[body.index('source === "decision-rules")') :]
        rule = rule[: rule.index('source === "generative-grounded"')]
        self.assertIn("(0 generative calls)", rule)
        self.assertNotIn("Model-generated", rule)
        self.assertNotIn("generative AI model", rule)

    def test_withheld_and_unverified_guidance_is_separate_from_both_answer_origins(self) -> None:
        body = _attribution()
        self.assertIn(
            'if (source === "withheld" || source === "abstain" || (calls && !isAnswer)) return {',
            body,
        )
        self.assertIn(
            "Withheld. Cited sources did not support a stated status or figure (no record changed)",
            body,
        )
        self.assertIn("The reply checks stopped the draft. No record changed.", body)
        tail = body[body.index('if (source === "withheld"') :]
        self.assertIn("Workflow-only help, no record changed", tail)
        self.assertIn("Workflow-only or unverified help. No record changed.", tail)
        # Only a real answer can claim a generative or rule origin.
        self.assertIn('const isAnswer = answer.kind === "answer";', body)
        self.assertIn('isAnswer && answer.model === "workflow-only" ? "decision-rules"', body)
        self.assertIn('isAnswer && answer.model ? "generative-grounded" : ""', body)

    def test_outcome_and_attribution_are_rendered_as_text_not_colour(self) -> None:
        self.assertIn(
            'outcomeNames = { answer: "answer", withheld: "withheld", abstain: "withheld", '
            'refused: "refused", fallback: "workflow-only help" }',
            CHAT,
        )
        self.assertIn("label: view.label,", CHAT)
        self.assertIn("outcome: outcomeNames[answer.kind]", CHAT)
        self.assertIn(
            "detail: `Skill: ${answer.skill}. ${usageNote(answer.consumption)}${view.detail}`", CHAT
        )
        message = WIDGET[WIDGET.index("function message(") : WIDGET.index("let observer")]
        self.assertIn("`Outcome: ${outcome}`", message)
        self.assertIn(
            'if (label) item.append(node("small", label, { class: "chat-widget-meta" }))', message
        )

    def test_alert_surface_states_it_uses_no_model_and_lists_sources_by_status(self) -> None:
        start = CHAT.index("async function showAlerts")
        alert = CHAT[start : start + 4200]
        self.assertIn("Model calls per check and alert: 0.", alert)
        self.assertIn("No AI model is used for any role.", alert)
        self.assertIn('h("h4", {}, "Source and status"), regulatorySources(alert.citations)', alert)


class SourceKindTagTests(unittest.TestCase):
    def test_chat_citations_are_tagged_by_kind_in_text(self) -> None:
        start = CHAT.index("function sourceLine(")
        body = CHAT[start : CHAT.index("function attribution(", start)]
        for tag in ("[Workflow rule]", "[Decision rule]", "[Case record]"):
            self.assertIn(tag, body)
        self.assertIn("return `${tag} ${id}: ${source.text}`;", body)

    def test_lookup_citations_state_status_dates_and_the_no_source_case(self) -> None:
        start = CHAT.index("function regulatorySources(")
        body = CHAT[start : start + 1800]
        self.assertIn('"aria-label": "Provision and fact citations"', body)
        for fragment in ("Status:", "Effective:", "Retrieved/observed:"):
            self.assertIn(fragment, body)
        self.assertIn("No source held for this answer. Do not infer a duty or terms", body)


class CitationDisclosureTests(unittest.TestCase):
    def test_source_list_is_a_native_disclosure_with_its_count_in_the_summary(self) -> None:
        self.assertIn('node("summary", `Sources (${sources.length})`)', WIDGET)
        message = WIDGET[WIDGET.index("function message(") : WIDGET.index("let observer")]
        self.assertIn('const details = node("details");', message)
        self.assertIn('if (role !== "user") {', message)
        # Native details exposes expanded state; the list sits inside the disclosure.
        self.assertLess(
            message.index("details.append(list)"), message.index("item.append(details)")
        )

    def test_empty_source_list_still_reports_zero_and_says_to_check_with_a_person(self) -> None:
        self.assertIn("Sources (${sources.length})", WIDGET)
        self.assertIn(
            "No supporting source was provided. Check with a person before relying on this reply.",
            WIDGET,
        )
        self.assertIn("sources: (answer.citations || []).map(sourceLine)", CHAT)

    def test_explicit_expanded_and_controls_state_is_declared_on_the_panel_disclosure(
        self,
    ) -> None:
        # aria-expanded/aria-controls exist only on the launcher; per-message source lists
        # rely on native details semantics, so adding them there would duplicate state.
        self.assertEqual(len(re.findall(r'setAttribute\("aria-controls"', WIDGET)), 1)
        self.assertIn('launcher.setAttribute("aria-controls", id)', WIDGET)
        self.assertIn('launcher.setAttribute("aria-expanded", "true")', WIDGET)
        self.assertIn('launcher.setAttribute("aria-expanded", "false")', WIDGET)
        message = WIDGET[WIDGET.index("function message(") : WIDGET.index("let observer")]
        self.assertNotIn("aria-expanded", message)
        self.assertNotIn("aria-controls", message)

    def test_citation_links_are_real_anchors_that_name_the_new_tab(self) -> None:
        self.assertEqual(len(re.findall(r'h\("a", \{ href: [^}]*rel: "noopener"', CHAT)), 2)
        self.assertIn("(source record, opens new tab)", CHAT)


class WarningBannerTests(unittest.TestCase):
    NOTICE = (
        "Do not enter personal or sensitive resident information. "
        "Chat cannot approve or change records."
    )

    def test_entry_warning_is_set_once_outside_the_message_log(self) -> None:
        self.assertEqual(CHAT.count(self.NOTICE), 1)
        self.assertIn('{ id: "employee-chat-entry-warning", class: "chat-widget-meta" }', CHAT)
        self.assertIn("ui.beforeInput.append(", CHAT)
        # The banner lives in the form; answers and withheld replies only append to the log.
        self.assertIn("form.append(beforeInput, input, tools, reason);", WIDGET)
        self.assertNotIn(
            "beforeInput", WIDGET[WIDGET.index("function message(") : WIDGET.index("let observer")]
        )

    def test_no_reply_path_clears_or_replaces_the_banner_or_the_log(self) -> None:
        for source in (CHAT, WIDGET):
            self.assertNotRegex(
                source, r"beforeInput\.(?:replaceChildren|remove|hidden|textContent|innerHTML)"
            )
            self.assertNotRegex(source, r"beforeInput\.hidden\s*=")
        self.assertNotRegex(WIDGET, r"log\.(?:replaceChildren|innerHTML\s*=|textContent\s*=)")

    def test_input_stays_described_by_the_banner_for_every_outcome(self) -> None:
        self.assertIn(
            'input.setAttribute("aria-describedby", '
            '"employee-chat-entry-warning employee-chat-error")',
            CHAT,
        )
        # Answer, withheld, abstain, refused and fallback all use the same message call.
        self.assertEqual(CHAT.count('ui.message("assistant", '), 1)
        self.assertIn("ui.setStatus(statusFor(answer.kind));", CHAT)

    def test_non_mutation_statement_is_repeated_in_privacy_intro_and_attribution(self) -> None:
        self.assertIn("Chat cannot approve, send, book or change records.", CHAT)
        self.assertIn(
            "Do not enter resident names, contact details or sensitive personal information.", CHAT
        )
        body = _attribution()
        self.assertGreaterEqual(len(re.findall("no record changed", body, re.I)), 5)
        self.assertEqual(body.count("Workflow-only or unverified help. No record changed."), 1)

    def test_regulatory_lookup_keeps_synthetic_and_privacy_notice_with_its_results(self) -> None:
        self.assertIn(
            "Synthetic data only. Do not enter resident personal or special-category details.", CHAT
        )
        self.assertIn('h("p", { id: "regulatory-privacy", class: "muted" }', CHAT)
        self.assertIn("synthetic-demo only. Exact source excerpts and recorded facts", CHAT)
        self.assertIn("not legal interpretation", CHAT)

    def test_withheld_reply_status_points_to_recorded_facts_not_an_invented_answer(self) -> None:
        start = CHAT.index("function statusFor(")
        body = CHAT[start : CHAT.index("const outcomeNames", start)]
        self.assertIn("Reply withheld. Check the case card for recorded facts.", body)
        self.assertIn("A person must take that action in the workflow.", body)
        self.assertIn("Answer added. Check the sources before relying on it.", body)


if __name__ == "__main__":
    unittest.main()
