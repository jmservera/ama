"""#215 criteria 3 and 4: doubt-route and no-source held states for every staff role.

Synthetic fixtures only; no network and no provider calls. Static source checks and API contract
checks, not browser, screen reader, assistive technology, staff comprehension or manual
acceptance evidence, and no WCAG conformance claim.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from regulatory_fixture import ENV, NOW, Fixture
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.projection import STAFF_ROLES
from zava_forward.core.regulatory_chat import RegulatoryChat

from zava_forward.api.server import App

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
CSS = (WEB / "style.css").read_text()
BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)
APPROVAL_CLAIM = re.compile(
    r"\b(approved|signed off|consent (?:is|was) (?:given|recorded))\b", re.I
)
SENT_TEXT = "Sent to exercise owner; awaiting human review"
LAW_TABLES = ("reg_source", "reg_version", "reg_provision", "reg_gap", "rule_card_version")
ANSWERED = "What are the hazard sources?"
NO_SOURCE = "zzz quantum bananas"


def doubt_button() -> str:
    start = CHAT.index("const doubt = h(")
    return CHAT[start : CHAT.index("item.append(citations,", start)]


class StaticHeldStateContractTests(unittest.TestCase):
    def test_no_source_state_has_text_glyph_dotted_border_and_a_plain_next_step(self) -> None:
        self.assertIn(
            "No source held for this answer. Do not infer a duty or terms; "
            "ask the named human owner.",
            CHAT,
        )
        self.assertRegex(CSS, r"\.regulatory-state\{border-left:4px solid currentColor")
        self.assertRegex(CSS, r"\.state-no-source\{border-left-style:dotted\}")
        self.assertRegex(CSS, r'\.state-no-source:before\{content:"\\2205\\00a0" / ""\}')
        self.assertIn("In plain words: the lookup found nothing it can show.", CHAT)

    def test_sent_state_has_text_and_glyph_not_colour_alone(self) -> None:
        self.assertRegex(CSS, r'\.state-sent:before\{content:"\\2713\\00a0" / ""\}')
        self.assertEqual(CHAT.count(f'doubt.textContent = "{SENT_TEXT}"'), 2)
        self.assertEqual(CHAT.count('doubt.classList.add("regulatory-state", "state-sent")'), 2)

    def test_doubt_control_is_a_native_button_that_stays_keyboard_focusable(self) -> None:
        body = doubt_button()
        self.assertIn('h("button", { type: "button", class: "alt", onclick:', body)
        self.assertIn('doubt.getAttribute("aria-disabled") === "true"', body)
        self.assertNotIn("doubt.disabled", CHAT)
        self.assertNotIn('tabindex: "-1"', body)
        self.assertNotRegex(body, r"onkey(?:down|press|up)")
        self.assertIn("In doubt: send this turn to Juan Manuel Servera", body)

    def test_doubt_failure_re_enables_the_control_and_names_a_next_action(self) -> None:
        body = doubt_button()
        self.assertIn('doubt.removeAttribute("aria-disabled")', body)
        self.assertIn("Doubt route failed:", body)
        self.assertIn("Next action: try again, or ask Juan Manuel Servera directly.", body)

    def test_outcome_is_announced_in_a_status_region_and_states_no_approval(self) -> None:
        self.assertIn('const status = h("p", { role: "status" });', CHAT)
        self.assertIn("No legal approval or resident message.", doubt_button())
        self.assertIn("Sending does not approve or decide anything", CHAT)
        self.assertIn("no resident is contacted", CHAT)

    def test_focus_indicator_is_defined_for_every_focusable_control(self) -> None:
        self.assertRegex(CSS, r":focus-visible\{outline:var\(--focus-w\) solid var\(--focus-ink\)")

    def test_mode_copy_is_a_native_labelled_checkbox_on_by_default_in_plain_ascii(self) -> None:
        self.assertIn('h("input", { type: "checkbox", id, checked: true })', CHAT)
        self.assertIn("Plain-language explanations", CHAT)
        self.assertIn(".regulatory.plain-language .plain-explanation{display:block}", CSS)
        copy = re.findall(r'"(In plain words:[^"]*)"', CHAT)
        self.assertGreaterEqual(len(copy), 5)
        for text in copy:
            with self.subTest(text=text[:40]):
                self.assertTrue(text.isascii())
                self.assertIsNone(BANNED.search(text))
                self.assertIsNone(APPROVAL_CLAIM.search(text))


class DoubtRouteRoleParityTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.f = Fixture(temp.name, sql=True)
        self.addCleanup(self.f.close)
        app: Any = App(self.f.store, "synthetic-local", law=self.f.law)  # type: ignore[no-untyped-call]
        chat = ChatIsolation(self.f.store, env=ENV)
        self.reg = RegulatoryChat(
            chat,
            self.f.law,
            app.regulatory.render,
            app.regulatory.classify,
            app.regulatory.refuse,
            env=ENV,
            clock=lambda: NOW,
        )
        app.rule_engine().run(self.f.store, "ZF-1", now=NOW)
        outbound = patch.object(
            self.f.store.ai, "evidence", side_effect=AssertionError("No provider calls")
        )
        outbound.start()
        self.addCleanup(outbound.stop)

    def as_role(self, role: str) -> dict[str, Any]:
        user: dict[str, Any] = self.f.store.staff[self.f.user["email"]]
        user["role"] = role
        return user

    def controlled(self) -> str:
        law = {t: self.f.law.sql.all(f"SELECT * FROM {t}") for t in LAW_TABLES}
        alerts = self.f.law.sql.all("SELECT * FROM reg_alert")
        return json.dumps(
            dict(
                cases=self.f.store.cases,
                law=law,
                alerts=alerts,
                rules=self.f.law.rules.history("synthetic-hazard"),
            ),
            sort_keys=True,
            default=str,
        )

    def check_copy(self, value: Any) -> None:
        text = json.dumps(value)
        self.assertTrue(text.isascii(), text)
        self.assertIsNone(APPROVAL_CLAIM.search(text), text)

    def test_every_staff_role_gets_the_no_source_state_and_a_safe_doubt_route(self) -> None:
        self.assertGreaterEqual(len(STAFF_ROLES), 7)
        for role in STAFF_ROLES:
            with self.subTest(role=role):
                user = self.as_role(role)
                before = self.controlled()
                tid = self.reg.start(user, "ZF-1")
                held = self.reg.ask(user, tid, NO_SOURCE)
                self.assertEqual(held["kind"], "refused")
                # The panel renders the no-source cue exactly when citations are empty.
                self.assertEqual((held["citations"], held["cards"]), ([], []))
                self.assertTrue(held["requires_human"] and held["workflow_only"])
                self.assertEqual(held["owner"], "Juan Manuel Servera")
                sections = held["sections"]
                self.assertTrue(sections["unknown_or_missing"])
                self.assertIn(
                    "independent human emergency or hazard route", sections["safe_next_action"]
                )
                self.assertIn("synthetic-demo", held["label"])
                self.check_copy(held["reply"])
                receipt = self.reg.doubt(user, tid, held["turn"])
                self.assertEqual(receipt["status"], "sent-to-exercise-inbox")
                self.assertEqual(receipt["referred_turn"], held["turn"])
                self.assertEqual(receipt["label"], "synthetic-demo")
                self.assertEqual(receipt["owner"], "Juan Manuel Servera")
                self.assertEqual(self.reg.doubt(user, tid, held["turn"]), receipt)
                self.assertEqual(self.controlled(), before)

    def test_every_staff_role_can_route_a_cited_answer_without_changing_any_record(self) -> None:
        for role in STAFF_ROLES:
            with self.subTest(role=role):
                user = self.as_role(role)
                before = self.controlled()
                tid = self.reg.start(user, "ZF-1")
                reply = self.reg.ask(user, tid, ANSWERED)
                self.assertEqual(reply["kind"], "answer")
                self.assertTrue(reply["citations"])
                self.assertEqual(reply["usage"]["model_calls"], 0)
                receipt = self.reg.doubt(user, tid, reply["turn"])
                self.assertEqual(receipt["status"], "sent-to-exercise-inbox")
                self.check_copy(receipt)
                self.assertEqual(self.controlled(), before)

    def test_doubt_route_rejects_unsafe_input_for_every_role_and_changes_nothing(self) -> None:
        for role in STAFF_ROLES:
            with self.subTest(role=role):
                user = self.as_role(role)
                tid = self.reg.start(user, "ZF-1")
                held = self.reg.ask(user, tid, NO_SOURCE)
                before = self.controlled()
                for turn in ("2", True, 1, 99, None):
                    with self.assertRaises(ValueError, msg=repr(turn)):
                        self.reg.doubt(user, tid, turn)
                self.assertEqual(held["turn"], 2)
                self.assertEqual(self.controlled(), before)


if __name__ == "__main__":
    unittest.main()
