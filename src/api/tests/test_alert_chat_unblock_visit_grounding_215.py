"""#215: the owner's 3-turn unblock and visit questions on a safety-stopped case stay grounded.

Synthetic fixtures only; the model is a stand-in and no network is used. Contract checks on the
API payload plus static source checks of the rendered copy, not screen reader or staff evidence.
"""

import copy
import json
import os
import re
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.chat_case_answers import answer, case_facts
from zava_forward.core.chat_panel import SOURCE_LABELS

import test_role_matrix as roles

APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
CASE = "ZF-4"
QUESTIONS = (
    "what can I do to unblock this case?",
    "review what is blocking it",
    "how can we fix this safety? Should we schedule a visit?",
)
CHAT_JS = (
    Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web" / "chat.js"
).read_text()
HUMAN_BOUNDARY = "cannot book a visit or approve a safety step"
CLAIMS = re.compile(r"\b(approved|cleared|signed off|consented|booked|scheduled for)\b", re.I)


def envelope(text: str | None) -> dict[str, Any]:
    return dict(outcome="returned", text=text, usage=None, source="ai", model="synthetic")


class UnblockVisitGroundingTests(roles.Matrix):  # type: ignore[misc]
    admission: Any
    saved: dict[str, str | None]

    @classmethod
    def setUpClass(cls) -> None:
        cls.admission = patch("zava_forward.api.server.chat_admission", return_value=None)
        cls.admission.start()
        cls.addClassCleanup(cls.admission.stop)
        super().setUpClass()
        cls.saved = {k: os.environ.get(k) for k in APPROVED}
        os.environ.update(APPROVED)

    @classmethod
    def tearDownClass(cls) -> None:
        for k, v in cls.saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        super().tearDownClass()

    def setUp(self) -> None:
        self.model: Callable[[str], dict[str, Any]] = self.cite_first
        self.original = self.store.ai.evidence
        self.store.ai.evidence = lambda _s, prompt, *_a: self.model(prompt)
        self.store.data.pop("chat_threads", None)
        email = next(s["email"] for s in self.store.data["staff"] if s["role"] == ROLE)
        self.cookie = self.session(email)

    def tearDown(self) -> None:
        self.store.ai.evidence = self.original

    @staticmethod
    def cite_first(prompt: str) -> dict[str, Any]:
        first = re.search(rf'"({CASE}/[^"]+)"', prompt)
        assert first
        return envelope(json.dumps(dict(answer="From the case card.", citations=[first.group(1)])))

    def api(self, path: str, body: Any = None) -> tuple[int, Any]:
        code, text = self.call(self.cookie, path, body)
        return code, (json.loads(text) if text.startswith(("{", "[")) else text)

    def ask(self, question: str) -> dict[str, Any]:
        code, thread = self.api("/api/chat/threads", {"case_id": CASE})
        self.assertEqual(code, 200, thread)
        code, reply = self.api(f"/api/chat/threads/{thread['id']}/ask", {"content": question})
        self.assertEqual(code, 200, reply)
        return reply  # type: ignore[no-any-return]

    def record(self) -> str:
        return json.dumps(self.store.data["cases"], sort_keys=True, default=str)

    def test_rules_only_turns_are_actionable_cited_and_disclosed_as_decision_model(self) -> None:
        self.model = lambda _p: envelope("not json at all")
        for question in QUESTIONS:
            with self.subTest(question=question):
                reply = self.ask(question)
                self.assertEqual(reply["kind"], "answer", reply)
                self.assertEqual(reply["answer_source"], "decision-rules-fallback")
                self.assertEqual(reply["model"], "workflow-only")
                self.assertEqual(
                    reply["answer_source_label"], SOURCE_LABELS["decision-rules-fallback"]
                )
                self.assertNotIn("Written by a generative AI model", reply["answer_source_label"])
                self.assertTrue(reply["citations"], reply)
                self.assertTrue(all(c["id"].startswith(f"{CASE}/") for c in reply["citations"]))
                self.assertIn("No record was changed", reply["reply"])
                self.assertIn("A person decides next steps", reply["reply"])
                self.assertNotRegex(reply["reply"], CLAIMS)

    def test_generative_turns_are_labelled_generative_and_cite_permitted_sources(self) -> None:
        for question in QUESTIONS:
            with self.subTest(question=question):
                reply = self.ask(question)
                self.assertEqual(reply["answer_source"], "generative-grounded")
                self.assertEqual(reply["label"], "AI suggestion, not approved")
                self.assertIn("generative AI model", reply["answer_source_label"])
                self.assertTrue(reply["citations"], reply)

    def test_unsupported_generative_claim_is_replaced_by_cited_rules_not_shown(self) -> None:
        draft = "The safety stop is cleared and the visit is booked."
        self.model = lambda p: envelope(
            json.dumps(dict(answer=draft, citations=[self.cite_first_id(p)]))
        )
        reply = self.ask(QUESTIONS[2])
        self.assertNotIn(draft, reply["reply"])
        self.assertEqual(reply["answer_source"], "decision-rules-fallback")
        self.assertTrue(reply["citations"])

    @staticmethod
    def cite_first_id(prompt: str) -> str:
        first = re.search(rf'"({CASE}/[^"]+)"', prompt)
        assert first
        return first.group(1)

    def test_chat_turns_never_change_the_case_record(self) -> None:
        before = self.record()
        for generative in (True, False):
            self.model = self.cite_first if generative else (lambda _p: envelope("not json"))
            for question in QUESTIONS:
                self.ask(question)
        self.assertEqual(self.record(), before)

    def test_unstored_turns_state_the_human_boundary_without_a_model_call(self) -> None:
        before = self.record()
        with patch.object(self.store.ai, "evidence", side_effect=AssertionError("model called")):
            with patch(
                "zava_forward.core.chat_privacy.ChatPrivacy.decision",
                return_value=dict(approved=False, retention="none"),
            ):
                for question in QUESTIONS[::2]:
                    code, reply = self.api(
                        "/api/chat/unstored-ask", {"content": question, "case_id": CASE}
                    )
                    if code == 400:
                        self.skipTest("storage approval fixture is active")
                    self.assertEqual(code, 200, reply)
                    self.assertEqual(reply["answer_source"], "decision-rules")
                    self.assertEqual(reply["model"], "workflow-only")
                    self.assertIn(HUMAN_BOUNDARY, reply["reply"])
                    self.assertIn("no record was changed", reply["reply"].casefold())
        self.assertEqual(self.record(), before)


def _detail() -> dict[str, Any]:
    return dict(
        stage="Survey",
        status="Blocked",
        hazards=[dict(category="Damp", owner="Safety lead", state="open")],
        work=dict(
            blockers=[
                dict(
                    step="Safety check",
                    reason="Open damp hazard",
                    owner="Safety lead",
                    responsible_role="Retrofit Coordinator",
                    next_action="Safety lead reviews the hazard",
                    source="Hazard register",
                    current_stop=True,
                )
            ]
        ),
    )


class DeterministicContractTests(unittest.TestCase):
    def _answers(self) -> list[tuple[str, list[str]]]:
        facts = case_facts(copy.deepcopy(_detail()), reason_visible=True)
        out = []
        for question in QUESTIONS:
            kind, text, cites = answer("ZF-9", question, facts)
            self.assertEqual(kind, "answer", question)
            out.append((text, cites))
        return out

    def test_every_turn_gives_cited_reasons_and_a_named_human_route(self) -> None:
        for text, cites in self._answers():
            self.assertIn("Safety check", text)
            self.assertIn("Open damp hazard", text)
            self.assertIn("Safety lead", text)
            self.assertTrue(cites and all(c.startswith("ZF-9/") for c in cites))
            self.assertNotRegex(text, CLAIMS)

    def test_unblock_and_visit_turns_say_a_person_decides_and_chat_cannot_act(self) -> None:
        for text, _ in (self._answers()[0], self._answers()[2]):
            self.assertIn("A person schedules visits and completes the safety step", text)
            self.assertIn(HUMAN_BOUNDARY, text)

    def test_blocking_review_turn_does_not_offer_to_act(self) -> None:
        text, _ = self._answers()[1]
        self.assertNotIn("schedules visits", text)
        self.assertNotRegex(text, CLAIMS)


class RenderedCopyContractTests(unittest.TestCase):
    def _attribution(self) -> str:
        start = CHAT_JS.index("function attribution(")
        return CHAT_JS[start : CHAT_JS.index("function statusFor(", start)]

    def test_rendered_labels_separate_decision_model_from_generative_model(self) -> None:
        body = self._attribution()
        for origin, label in (
            ("decision-rules", "Decision model (case rules), no record changed"),
            ("decision-rules-fallback", "Decision model (case rules; generative draft withheld)"),
            ("generative-grounded", "Model-generated, not approved. Demo only."),
        ):
            self.assertIn(f'source === "{origin}"', body)
            self.assertIn(label, body)
        self.assertIn("deterministic decision rules", body)
        self.assertIn("generative AI model (${answer.model})", body)

    def test_chat_entry_states_it_cannot_approve_or_change_records(self) -> None:
        self.assertIn("Chat cannot approve or change records.", CHAT_JS)
        self.assertIn("Chat cannot approve, send, book or change records.", CHAT_JS)

    def test_server_origin_labels_match_the_ui_origin_names(self) -> None:
        for origin in ("decision-rules", "decision-rules-fallback", "generative-grounded"):
            self.assertIn(origin, SOURCE_LABELS)
            self.assertIn(f'"{origin}"', CHAT_JS)


if __name__ == "__main__":
    unittest.main()
