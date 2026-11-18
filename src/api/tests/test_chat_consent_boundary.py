"""#164 / #215: missing or withdrawn resident AI consent gives deterministic manual-path guidance.

Synthetic fixtures only; the model is a stand-in and no network is used. Contract checks on the
API payload and web source, not live model, browser, screen reader or staff comprehension evidence.
"""

import json
import os
import re
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.chat_case_answers import AI_CONSENT, RULES
from zava_forward.core.chat_panel import CONSENT_STATES, consent_guidance

import test_role_matrix as roles

APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
CASE = "ZF-4"
QUESTION = "What is the status of this case?"
WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
INTERNAL_TERMS = re.compile(r"\b(DPIA|lawful basis|payload|token|prompt|LLM|API)\b", re.I)
CLAIMS = re.compile(r"\b(approved|consented|booked|signed off|cleared)\b", re.I)


class ConsentBoundaryTests(roles.Matrix):
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
        self.model_calls = 0
        self.original = self.store.ai.evidence
        self.store.ai.evidence = self.fake
        self.store.data.pop("chat_threads", None)
        email = next(s["email"] for s in self.store.data["staff"] if s["role"] == ROLE)
        self.cookie = self.session(email)
        self.resident = self.store._case(CASE)["resident"]
        self.addCleanup(self.resident.pop, "ai_data_use_consent", None)

    def tearDown(self) -> None:
        self.store.ai.evidence = self.original

    def fake(self, _system: str, _prompt: str, *_args: Any) -> dict[str, Any]:
        self.model_calls += 1
        text = json.dumps(dict(answer="Funding is confirmed.", citations=[f"{CASE}/status"]))
        return dict(outcome="returned", text=text, usage=None, source="ai", model="synthetic")

    def api(self, path: str, body: Any = None) -> tuple[int, Any]:
        code, text = self.call(self.cookie, path, body)
        return code, (json.loads(text) if text.startswith(("{", "[")) else text)

    def ask(self, question: str = QUESTION) -> dict[str, Any]:
        code, thread = self.api("/api/chat/threads", {"case_id": CASE})
        self.assertEqual(code, 200, thread)
        code, reply = self.api(f"/api/chat/threads/{thread['id']}/ask", {"content": question})
        self.assertEqual(code, 200, reply)
        return reply  # type: ignore[no-any-return]

    def test_missing_or_withdrawn_consent_returns_manual_path_without_a_model_call(self) -> None:
        for state in (*CONSENT_STATES, "", None):
            with self.subTest(state=state):
                self.resident["ai_data_use_consent"] = state
                before = json.dumps(self.store.data["cases"], sort_keys=True, default=str)
                reply = self.ask()
                self.assertEqual(reply["kind"], "answer", reply)
                self.assertEqual(reply["answer_source"], "decision-rules")
                self.assertEqual(reply["answer_origin"], "decision_rule")
                self.assertEqual(reply["model"], "workflow-only")
                self.assertEqual(reply["consumption"]["model_calls"], 0)
                self.assertEqual(reply["consumption"]["provider_outcome"], "not-called")
                self.assertIn("manual case-card path", reply["reply"])
                self.assertEqual([c["id"] for c in reply["citations"]], [AI_CONSENT])
                self.assertEqual(reply["citations"][0]["source_kind"], "workflow-rule")
                self.assertIn(
                    "Deterministic decision or workflow rule", reply["answer_source_label"]
                )
                self.assertEqual(
                    before, json.dumps(self.store.data["cases"], sort_keys=True, default=str)
                )
        self.assertEqual(self.model_calls, 0)

    def test_stored_state_is_echoed_only_from_the_allowed_list(self) -> None:
        self.resident["ai_data_use_consent"] = "Withdrawn"
        self.assertIn("consent: Withdrawn.", self.ask()["reply"])
        self.resident["ai_data_use_consent"] = "<script>ignore previous</script>"
        text = self.ask()["reply"]
        self.assertIn("consent: Not recorded.", text)
        self.assertNotIn("script", text)

    def test_given_consent_and_legacy_cases_keep_the_existing_path(self) -> None:
        self.ask()
        self.assertEqual(self.model_calls, 1)
        self.resident["ai_data_use_consent"] = " given "
        self.ask()
        self.assertEqual(self.model_calls, 2)

    def test_out_of_scope_requests_keep_their_own_refusal(self) -> None:
        self.resident["ai_data_use_consent"] = "Withdrawn"
        reply = self.ask("record the resident's consent for me")
        self.assertEqual(reply["kind"], "refused", reply)
        self.assertEqual(self.model_calls, 0)

    def test_guidance_is_plain_ascii_short_and_claims_nothing(self) -> None:
        texts = [consent_guidance(state) or "" for state in (*CONSENT_STATES, "")]
        texts.append(RULES[AI_CONSENT])
        for text in texts:
            with self.subTest(text=text):
                self.assertTrue(text.isascii())
                self.assertNotIn("\u2014", text)
                self.assertIsNone(INTERNAL_TERMS.search(text))
                self.assertIsNone(CLAIMS.search(text))
                sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
                self.assertTrue(all(len(s.split()) <= 25 for s in sentences), sentences)
                self.assertIn("Chat cannot record or assume consent.", text)

    def test_guidance_helper_ignores_given_and_absent_states(self) -> None:
        self.assertIsNone(consent_guidance(None))
        self.assertIsNone(consent_guidance("Given"))
        self.assertIsNone(consent_guidance("given "))

    def test_web_labels_rule_answers_in_text_not_colour_and_announces_status(self) -> None:
        js = (WEB / "chat.js").read_text()
        for needle in (
            '"[Workflow rule]"',
            "Deterministic decision or workflow rule (not generative AI; no record changed)",
            "(0 generative calls)",
            "Answer added. Check the sources before relying on it.",
            'role: "status"',
        ):
            self.assertIn(needle, js)
        self.assertNotIn("innerHTML", js)


if __name__ == "__main__":
    unittest.main()
