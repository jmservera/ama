"""#215: end-to-end alert-to-chat provenance, grounding, safety stop and non-mutation matrix.

Local engineering verification only: synthetic fixtures, a stand-in model, no network, and static
source checks of the Workbench scripts. It is NOT evidence of live Azure OpenAI behaviour, of a
rendered browser, or of manual WCAG / screen-reader sign-off; those stay separate human and
live-environment steps (Refs #215).
"""

import json
import os
import re
import sys
import unittest
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.chat_panel import SOURCE_LABELS

sys.path.append(str(Path(__file__).resolve().parent))
import test_role_matrix as roles  # noqa: E402

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT_JS = (WEB / "chat.js").read_text()
WIDGET_JS = (WEB / "chat-widget.js").read_text()
APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
CASE = "ZF-4"
UNBLOCK = "what can I do to unblock this case?"
BLOCKING = "review what is blocking it"
VISIT = "how can we fix this safety? Should we schedule a visit?"
CLAIMS = re.compile(r"\b(approved|cleared|signed off|consented|booked|scheduled for)\b", re.I)
UNAVAILABLE = ("disabled", "timeout", "input-refused", "model-mismatch")


def envelope(text: str | None, outcome: str = "returned") -> dict[str, Any]:
    return dict(outcome=outcome, text=text, usage=None, source="ai", model="synthetic")


def unavailable(outcome: str, _prompt: str) -> dict[str, Any]:
    return envelope(None, outcome)


class AlertToChatMatrix(roles.Matrix):
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
        self.prompts: list[str] = []
        self.model: Callable[[str], dict[str, Any]] = self.cite_first
        self.original = self.store.ai.evidence
        self.store.ai.evidence = lambda _s, prompt, *_a: self.record_prompt(prompt)
        self.store.data.pop("chat_threads", None)
        email = next(s["email"] for s in self.store.data["staff"] if s["role"] == ROLE)
        self.cookie = self.session(email)

    def tearDown(self) -> None:
        self.store.ai.evidence = self.original

    def record_prompt(self, prompt: str) -> dict[str, Any]:
        self.prompts.append(prompt)
        return self.model(prompt)

    @staticmethod
    def first_source(prompt: str) -> str:
        first = re.search(rf'"({CASE}/[^"]+)"', prompt)
        assert first
        return first.group(1)

    def cite_first(self, prompt: str) -> dict[str, Any]:
        text = json.dumps(dict(answer="From the case card.", citations=[self.first_source(prompt)]))
        return envelope(text)

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


class ContextAndProvenanceTests(AlertToChatMatrix):
    def test_case_context_is_injected_and_cited_ids_belong_to_that_case(self) -> None:
        reply = self.ask(BLOCKING)
        self.assertEqual(len(self.prompts), 1)
        self.assertIn(f'"{CASE}/', self.prompts[0])
        self.assertTrue(reply["citations"], reply)
        self.assertTrue(all(c["id"].startswith(f"{CASE}/") for c in reply["citations"]))
        rules_reply = self.ask(UNBLOCK)
        self.assertEqual(len(self.prompts), 1)
        self.assertTrue(rules_reply["citations"], rules_reply)
        self.assertTrue(
            all(c["id"].startswith((f"{CASE}/", "workflow/")) for c in rules_reply["citations"])
        )
        self.assertTrue(any(c["id"].startswith(f"{CASE}/") for c in rules_reply["citations"]))

    def test_generative_and_decision_model_turns_carry_distinct_provenance(self) -> None:
        generative = self.ask(BLOCKING)
        rules_first = self.ask(VISIT)
        self.model = lambda _p: envelope("not json at all")
        rules = self.ask(BLOCKING)
        self.assertEqual(generative["answer_source"], "generative-grounded")
        self.assertEqual(rules_first["answer_source"], "decision-rules")
        self.assertEqual(rules["answer_source"], "decision-rules-fallback")
        self.assertEqual(rules["model"], "workflow-only")
        self.assertEqual(
            len(
                {
                    generative["answer_source_label"],
                    rules_first["answer_source_label"],
                    rules["answer_source_label"],
                }
            ),
            3,
        )
        self.assertIn("Generative model suggestion", generative["answer_source_label"])
        self.assertNotIn("generative model suggestion", rules["answer_source_label"].casefold())
        self.assertEqual(rules["answer_source_label"], SOURCE_LABELS["decision-rules-fallback"])
        self.assertTrue(rules["citations"])

    def test_unblock_and_visit_get_grounded_guidance_not_a_withheld_reply(self) -> None:
        self.model = lambda _p: envelope("not json at all")
        for question in (UNBLOCK, BLOCKING, VISIT):
            with self.subTest(question=question):
                reply = self.ask(question)
                self.assertEqual(reply["kind"], "answer", reply)
                self.assertNotIn(reply["kind"], ("withheld", "abstain", "refused"))
                self.assertIn("A person decides next steps", reply["reply"])
                self.assertNotRegex(reply["reply"], CLAIMS)


class UnavailableAndNonMutationTests(AlertToChatMatrix):
    def test_model_unavailable_keeps_cited_workflow_help_and_no_model_text(self) -> None:
        for outcome in UNAVAILABLE:
            self.model = partial(unavailable, outcome)
            for question in (UNBLOCK, BLOCKING, VISIT):
                with self.subTest(outcome=outcome, question=question):
                    reply = self.ask(question)
                    self.assertNotEqual(reply["answer_source"], "generative-grounded")
                    self.assertEqual(reply["model"], "workflow-only")
                    self.assertTrue(reply["citations"], reply)
                    self.assertIn("No record was changed", reply["reply"])
                    self.assertNotRegex(reply["reply"], CLAIMS)

    def test_ai_exception_is_a_workflow_only_answer_not_a_crash(self) -> None:
        def boom(_p: str) -> dict[str, Any]:
            raise RuntimeError("provider down")

        self.model = boom
        for question in (BLOCKING, UNBLOCK):
            reply = self.ask(question)
            self.assertNotEqual(reply["answer_source"], "generative-grounded")
            self.assertIn("No record was changed", reply["reply"])

    def test_unsupported_claim_is_withheld_for_cited_rules_and_record_is_unchanged(self) -> None:
        draft = "The safety stop is cleared and the visit is booked."
        before = self.record()
        self.model = lambda p: envelope(
            json.dumps(dict(answer=draft, citations=[self.first_source(p)]))
        )
        blocking = self.ask(BLOCKING)
        self.assertNotIn(draft, blocking["reply"])
        self.assertEqual(blocking["answer_source"], "decision-rules-fallback")
        visit = self.ask(VISIT)
        self.assertNotIn(draft, visit["reply"])
        self.assertEqual(visit["answer_source"], "decision-rules")
        self.assertEqual(self.record(), before)

    def test_no_chat_outcome_mutates_the_controlled_record(self) -> None:
        before = self.record()
        models: list[Callable[[str], dict[str, Any]]] = [
            self.cite_first,
            lambda _p: envelope("not json"),
            lambda _p: envelope(None, "timeout"),
        ]
        for model in models:
            self.model = model
            for question in (UNBLOCK, VISIT):
                self.ask(question)
        self.assertEqual(self.record(), before)

    def test_unstored_path_needs_no_model_and_states_the_human_boundary(self) -> None:
        before = self.record()
        with patch.object(self.store.ai, "evidence", side_effect=AssertionError("model called")):
            with patch(
                "zava_forward.core.chat_privacy.ChatPrivacy.decision",
                return_value=dict(approved=False, retention="none"),
            ):
                code, reply = self.api(
                    "/api/chat/unstored-ask", {"content": VISIT, "case_id": CASE}
                )
                if code == 400:
                    self.skipTest("storage approval fixture is active")
                self.assertEqual(code, 200, reply)
                self.assertEqual(reply["answer_source"], "decision-rules")
                self.assertIn("cannot book a visit or approve a safety step", reply["reply"])
        self.assertEqual(self.record(), before)


class WorkbenchSourceTests(unittest.TestCase):
    def test_chat_sends_case_context_from_the_open_record_to_the_thread_api(self) -> None:
        self.assertIn('api("/api/chat/threads", { case_id: caseId }', CHAT_JS)
        self.assertIn("Context: case ${caseId}. Only facts your role may see are used.", CHAT_JS)
        self.assertIn(
            'api("/api/chat/unstored-ask", '
            "{ content: question, skill, case_id: caseId, plain_language: plainMode.checked }",
            CHAT_JS,
        )

    def test_provenance_badges_and_citation_links_are_rendered_as_text(self) -> None:
        for label in (
            "Deterministic decision or workflow rule (not generative AI; no record changed)",
            "The generative draft did not pass the source check and was not shown.",
            "Generative model suggestion (unapproved; check cited sources; no record changed)",
        ):
            self.assertIn(label, CHAT_JS)
        for tag in ("[Workflow rule]", "[Decision rule]", "[Case record]"):
            self.assertIn(tag, CHAT_JS)
        self.assertIn("Check the sources", CHAT_JS)

    def test_unavailable_and_withheld_paths_name_a_manual_escape(self) -> None:
        self.assertIn("continue with the ordinary workflow", CHAT_JS)
        self.assertIn("Continue ordinary case work manually.", CHAT_JS)
        self.assertIn("Reply withheld. Check the case card for recorded facts.", CHAT_JS)
        self.assertIn("Use the existing human emergency or hazard service", CHAT_JS)
        self.assertIn("Chat cannot approve or change records.", CHAT_JS)

    def test_widget_keeps_errors_in_an_alert_region_and_closes_on_escape(self) -> None:
        self.assertIn('role: "alert"', WIDGET_JS)
        self.assertIn("Escape", WIDGET_JS + CHAT_JS)


class EvidenceBoundaryTests(unittest.TestCase):
    def test_suite_states_what_it_does_not_evidence(self) -> None:
        doc = " ".join((__doc__ or "").split())
        for phrase in ("Local engineering verification only", "live Azure OpenAI", "screen-reader"):
            self.assertIn(phrase, doc)


if __name__ == "__main__":
    unittest.main()
