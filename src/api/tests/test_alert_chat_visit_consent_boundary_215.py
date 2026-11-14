"""#215: visit questions on a safety-stopped, access-pending case keep the consent boundary.

Synthetic fixtures only; the model is a stand-in and no network is used. Contract checks on the
API payload, not live model, browser, screen reader or staff evidence.
"""

import copy
import json
import os
import re
import unittest
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

from zava_forward.core.chat_case_answers import answer, case_facts

import test_role_matrix as roles

APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
CASE = "ZF-4"
QUESTION = "how can we fix this safety? Should we schedule a visit?"
CONSENT_STEP = "confirm the resident's consent and access with the resident"
SIGN_OFF_STEP = "independent safety sign-off"
BOUNDARY = "cannot book a visit or approve a safety step"
UNSUPPORTED_DRAFTS = (
    "The resident has given consent so the visit is booked for Tuesday.",
    "We have signed off the safety step and consent is on file.",
)
REFUSALS = {
    "book the visit for Tuesday morning": "cannot answer that",
    "record the resident's consent to the visit": "recorded by the named officer",
    "sign-off the safety step": "independent review or sign-off step",
}


def envelope(text: str | None) -> dict[str, Any]:
    return dict(outcome="returned", text=text, usage=None, source="ai", model="synthetic")


class VisitConsentBoundaryTests(roles.Matrix):  # type: ignore[misc]
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
        self.model: Callable[[str], dict[str, Any]] = lambda _p: envelope("not json")
        self.original = self.store.ai.evidence
        self.store.ai.evidence = lambda _s, prompt, *_a: self.model(prompt)
        self.store.data.pop("chat_threads", None)
        email = next(s["email"] for s in self.store.data["staff"] if s["role"] == ROLE)
        self.cookie = self.session(email)

    def tearDown(self) -> None:
        self.store.ai.evidence = self.original

    def api(self, path: str, body: Any = None) -> tuple[int, Any]:
        code, text = self.call(self.cookie, path, body)
        return code, (json.loads(text) if text.startswith(("{", "[")) else text)

    def ask(self, question: str) -> dict[str, Any]:
        code, thread = self.api("/api/chat/threads", {"case_id": CASE})
        self.assertEqual(code, 200, thread)
        code, reply = self.api(f"/api/chat/threads/{thread['id']}/ask", {"content": question})
        self.assertEqual(code, 200, reply)
        return reply  # type: ignore[no-any-return]

    def cases(self) -> str:
        return json.dumps(self.store.data["cases"], sort_keys=True, default=str)

    def test_visit_question_names_consent_access_and_independent_sign_off_with_citations(
        self,
    ) -> None:
        reply = self.ask(QUESTION)
        self.assertEqual(reply["kind"], "answer", reply)
        self.assertEqual(reply["answer_source"], "decision-rules-fallback")
        text = reply["reply"]
        self.assertIn(CONSENT_STEP, text)
        self.assertIn(SIGN_OFF_STEP, text)
        self.assertIn(BOUNDARY, text)
        self.assertIn("does not assume either", text)
        self.assertTrue(reply["citations"], reply)
        self.assertTrue(all(c["id"].startswith(f"{CASE}/") for c in reply["citations"]))
        self.assertTrue(any("hazards" in c["id"] for c in reply["citations"]), reply)

    def test_generative_drafts_that_book_assume_consent_or_sign_off_are_withheld(self) -> None:
        for draft in UNSUPPORTED_DRAFTS:
            with self.subTest(draft=draft):
                self.model = self.drafting(draft)
                reply = self.ask(QUESTION)
                self.assertNotIn(draft, reply["reply"])
                self.assertEqual(reply["kind"], "withheld", reply)
                self.assertEqual(reply["answer_source"], "withheld")
                self.assertEqual(reply["citations"], [])
                self.assertIn("Ask a case question instead", reply["reply"])

    def drafting(self, draft: str) -> Callable[[str], dict[str, Any]]:
        return lambda p: envelope(json.dumps(dict(answer=draft, citations=[self.first_id(p)])))

    @staticmethod
    def first_id(prompt: str) -> str:
        first = re.search(rf'"({CASE}/[^"]+)"', prompt)
        assert first
        return first.group(1)

    def test_requests_to_book_record_consent_or_sign_off_are_never_actioned(self) -> None:
        before = self.cases()
        for request, routes in REFUSALS.items():
            with self.subTest(request=request):
                reply = self.ask(request)
                self.assertNotEqual(reply["kind"], "answer", reply)
                self.assertIn(routes, reply["reply"])
                self.assertNotRegex(reply["reply"], r"\b(booked|scheduled for|consented)\b")
        self.assertEqual(self.cases(), before)

    def test_visit_turns_leave_every_record_unchanged_for_each_answer_path(self) -> None:
        before = self.cases()
        paths = dict(
            rules=lambda _p: envelope("not json"),
            generative=lambda p: envelope(
                json.dumps(dict(answer="From the case card.", citations=[self.first_id(p)]))
            ),
            unsupported=lambda p: envelope(
                json.dumps(dict(answer=UNSUPPORTED_DRAFTS[0], citations=[self.first_id(p)]))
            ),
        )
        for name, model in paths.items():
            with self.subTest(path=name):
                self.model = model
                self.ask(QUESTION)
                self.ask("what can I do to unblock this case?")
        self.assertEqual(self.cases(), before)
        case = next(c for c in self.store.data["cases"] if c["id"] == CASE)
        self.assertEqual((case["appointments"], case["contacts"]), ([], []))


def _access_pending_detail() -> dict[str, Any]:
    return dict(
        stage="Contacting resident",
        status="Blocked",
        waiting_on="Resident Liaison Officer",
        reason="Resident access to be confirmed",
        hazards=[dict(category="Damp", owner="Safety lead", state="open")],
        work=dict(
            blockers=[
                dict(
                    step="Resident access",
                    reason="Resident access to be confirmed",
                    owner="Resident Liaison Officer",
                    responsible_role="Resident Liaison Officer",
                    next_action="Officer agrees a visit time with the resident",
                    source="Contact log",
                    current_stop=True,
                ),
                dict(
                    step="Safety check",
                    reason="Open damp hazard",
                    owner="Safety lead",
                    responsible_role="Retrofit Coordinator",
                    next_action="Safety lead reviews the hazard",
                    source="Hazard register",
                    current_stop=False,
                ),
            ]
        ),
    )


class AccessPendingContractTests(unittest.TestCase):
    def test_access_pending_case_gets_cited_steps_and_the_consent_boundary(self) -> None:
        facts = case_facts(copy.deepcopy(_access_pending_detail()), reason_visible=True)
        kind, text, cites = answer("ZF-9", QUESTION, facts)
        self.assertEqual(kind, "answer")
        for expected in ("Resident access", "Safety check", "Damp, open", CONSENT_STEP):
            self.assertIn(expected, text)
        self.assertIn(SIGN_OFF_STEP, text)
        self.assertIn(BOUNDARY, text)
        self.assertTrue(cites and all(c.startswith("ZF-9/") for c in cites))
        self.assertNotRegex(text, r"\b(booked|consented|signed off|approved|cleared)\b")

    def test_unblock_question_carries_the_same_boundary(self) -> None:
        facts = case_facts(copy.deepcopy(_access_pending_detail()), reason_visible=True)
        _, text, _ = answer("ZF-9", "what can I do to unblock this case?", facts)
        self.assertIn(CONSENT_STEP, text)
        self.assertIn(SIGN_OFF_STEP, text)


if __name__ == "__main__":
    unittest.main()
