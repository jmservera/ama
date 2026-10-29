"""Issue 159: conversation panel answers are cited, labelled, proposal-only and fall back to the workflow.

Synthetic fixtures only (ADR 0005). The model is a stand-in for `store.ai.evidence`; no network is used.
"""

import copy
import json
import os
import re
import unittest
from unittest.mock import patch
from collections.abc import Callable
from pathlib import Path
from typing import Any

import test_role_matrix as roles
from zava_forward.core.chat_panel import ABSTAIN, FALLBACK, LABEL
from zava_forward.core.assistants import REGISTRY
from zava_forward.core import projection
from zava_forward.core.chat_privacy import redact
from zava_forward.core.chatthreads import MAX_CONTENT

APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"


def envelope(text: str | None, outcome: str = "returned") -> dict[str, Any]:
    return dict(outcome=outcome, text=text, usage=None, source="ai", model="synthetic")


class PanelTests(roles.Matrix):
    @classmethod
    def setUpClass(cls) -> None:
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
        self.systems: list[str] = []
        self.model: Callable[[str], dict[str, Any]] = self.cite_first
        self.original = self.store.ai.evidence
        self.store.ai.evidence = self.fake  # type: ignore[method-assign]
        self.store.data.pop("chat_threads", None)
        self.cks = {r: self.session(self.email(r)) for r in roles.ROLES}

    def tearDown(self) -> None:
        self.store.ai.evidence = self.original  # type: ignore[method-assign]

    def fake(self, system: str, prompt: str, *args: Any) -> dict[str, Any]:
        self.systems.append(system)
        self.prompts.append(prompt)
        return self.model(prompt)

    def cite_first(self, prompt: str) -> dict[str, Any]:
        first = re.search(r'"(ZF-1/[^"]+)"', prompt)
        assert first
        return envelope(json.dumps(dict(answer="From the case card.", citations=[first.group(1)])))

    def email(self, role: str) -> str:
        return next(s["email"] for s in self.store.data["staff"] if s["role"] == role)

    def api(self, role: str, path: str, body: Any = None) -> tuple[int, Any]:
        code, text = self.call(self.cks[role], path, body)
        return code, (json.loads(text) if text.startswith(("{", "[")) else text)

    def thread(self, role: str = ROLE, case: str = "ZF-1") -> str:
        code, d = self.api(role, "/api/chat/threads", {"case_id": case})
        self.assertEqual(code, 200, d)
        return str(d["id"])

    def ask(self, tid: str, text: str = "What stage is it?", role: str = ROLE) -> tuple[int, Any]:
        return self.api(role, f"/api/chat/threads/{tid}/ask", {"content": text})

    def test_answer_is_cited_labelled_and_stored_with_evidence(self) -> None:
        tid = self.thread()
        code, d = self.ask(tid)
        self.assertEqual(code, 200, d)
        self.assertEqual((d["kind"], d["label"], d["workflow_only"]), ("answer", LABEL, False))
        self.assertTrue(d["citations"] and all(c["id"].startswith("ZF-1/") for c in d["citations"]))
        stored = self.api(ROLE, f"/api/chat/threads/{tid}")[1]["messages"]
        self.assertEqual([m["role"] for m in stored], ["user", "assistant"])
        self.assertEqual(stored[1]["evidence"], [c["id"] for c in d["citations"]])

    def test_maximum_question_with_expanding_mask_returns_success(self) -> None:
        question = "x" * (MAX_CONTENT - 8) + " NE1 1AA"
        self.assertEqual(len(question), MAX_CONTENT)
        expected = redact(question)[0][:MAX_CONTENT]
        for skill in (None, "general", *REGISTRY):
            with self.subTest(skill=skill):
                tid = self.thread()
                body = {"content": question}
                if skill is not None:
                    body["skill"] = skill
                code, answer = self.api(ROLE, f"/api/chat/threads/{tid}/ask", body)
                self.assertEqual((code, answer["kind"]), (200, "answer"))
                stored = self.api(ROLE, f"/api/chat/threads/{tid}")[1]["messages"]
                self.assertEqual(stored[0]["content"], expected)
                self.assertNotIn("NE1 1AA", stored[0]["content"])
                events = [
                    json.loads(row["detail"])
                    for row in self.store.audit_entries()
                    if row["action"] == "chat.answer"
                ]
                self.assertEqual(events[-1]["question_seq"], stored[0]["seq"])

    def test_uncited_or_foreign_citation_abstains(self) -> None:
        tid = self.thread()
        for reply in (
            envelope(json.dumps(dict(answer="Probably fine.", citations=[]))),
            envelope(json.dumps(dict(answer="Fine.", citations=["ZF-2/stage"]))),
            envelope("not json at all"),
        ):
            self.model = lambda _p, r=reply: r
            code, d = self.ask(tid)
            self.assertEqual(
                (code, d["kind"], d["reply"], d["citations"]), (200, "abstain", ABSTAIN, [])
            )
            self.assertEqual(d["label"], LABEL)

    def test_no_case_means_no_sources_and_no_model_call(self) -> None:
        tid = str(self.api(ROLE, "/api/chat/threads", {})[1]["id"])
        code, d = self.ask(tid)
        self.assertEqual((code, d["kind"], d["reply"]), (200, "abstain", ABSTAIN))
        self.assertEqual(self.prompts, [])

    def test_out_of_scope_asks_are_refused_with_a_route_and_no_model_call(self) -> None:
        tid = self.thread()
        for text in (
            "Approve the quality check.",
            "Record the resident's consent.",
            "Email the resident.",
            "I need you to approve the case.",
            "I want to approve the work.",
            "Mark ZF-1 as consented.",
            "Call Mrs Smith.",
            "I want you to \u0430\u0440\u0440r\u043eve the case.",
            "a\u200bp\u200cp\u200drove the case.",
        ):
            code, d = self.ask(tid, text)
            self.assertEqual(
                (code, d["kind"], d["label"], d["citations"]), (200, "refused", LABEL, [])
            )
            self.assertTrue(d["workflow_only"])
            self.assertIn("person", d["reply"])
        self.assertEqual(self.prompts, [])
        self.assertEqual(self.ask(tid, "Has the resident given consent?")[1]["kind"], "answer")

    def test_model_failure_falls_back_to_workflow_only(self) -> None:
        tid = self.thread()
        for outcome in ("provider-unavailable", "timeout", "disabled"):
            self.model = lambda _p, o=outcome: envelope(None, o)
            code, d = self.ask(tid)
            self.assertEqual(
                (code, d["kind"], d["reply"], d["workflow_only"]), (200, "fallback", FALLBACK, True)
            )
        self.assertEqual(self.api(ROLE, "/api/cases/ZF-1")[0], 200)

    def test_every_turn_rechecks_role_and_case(self) -> None:
        tid = self.thread()
        self.assertEqual(self.ask(tid)[0], 200)
        rec = self.store.staff[self.email(ROLE)]
        rec["role"] = "Mystery"
        try:
            self.assertEqual(self.ask(tid, "again")[0], 403)
        finally:
            rec["role"] = ROLE
        self.assertEqual(self.ask(tid, "back again")[0], 200)
        other = "Quality Inspector"
        self.assertEqual(self.ask(tid, "not mine", role=other)[0], 404)
        detail = self.store.detail
        self.store.detail = lambda *a, **k: None
        try:
            self.assertEqual(self.ask(tid, "case out of scope")[0], 404)
        finally:
            self.store.detail = detail

    def test_follow_up_keeps_case_context(self) -> None:
        tid = self.thread()
        self.ask(tid, "FIRST-QUESTION-CANARY")
        self.prompts.clear()
        self.ask(tid, "And the status?")
        self.assertIn("FIRST-QUESTION-CANARY", self.prompts[0])
        self.assertIn("ZF-1/stage", self.prompts[0])
        self.assertNotIn("From the case card.", self.prompts[0])

    def test_plain_prose_action_claims_are_withheld_without_changing_case(self) -> None:
        tid = self.thread()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        for answer in (
            "I have approved the case.",
            "I recorded the resident's consent.",
            "Consent has been re\u200bcorded.",
        ):
            self.model = lambda _p, a=answer: envelope(
                json.dumps(dict(answer=a, citations=["ZF-1/stage"]))
            )
            code, d = self.ask(tid)
            self.assertEqual((code, d["kind"], d["citations"]), (200, "withheld", []))
            self.assertNotIn(answer, d["reply"])
        self.assertEqual(self.store.cases["ZF-1"], before)

    def test_chat_cannot_change_a_controlled_record(self) -> None:
        tid = self.thread()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        self.model = lambda _p: envelope(
            json.dumps(dict(answer='approve: {"tool_call": {}}', citations=["ZF-1/stage"]))
        )
        d = self.ask(tid, "What is the case stage?")[1]
        self.assertEqual(d["kind"], "withheld")
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(self.api(ROLE, f"/api/chat/threads/{tid}/approve", {})[0], 404)

    def test_proposal_request_uses_the_assistants_path_and_checks_role(self) -> None:
        tid = self.thread()
        self.assertEqual(
            self.api(ROLE, f"/api/chat/threads/{tid}/proposals", {"capability": "nope"})[0], 400
        )
        code, d = self.api(
            ROLE, f"/api/chat/threads/{tid}/proposals", {"capability": "funding-evidence"}
        )
        self.assertIn(code, (400, 403), d)
        bare = str(self.api(ROLE, "/api/chat/threads", {})[1]["id"])
        self.assertEqual(
            self.api(
                ROLE, f"/api/chat/threads/{bare}/proposals", {"capability": "quality-evidence"}
            )[0],
            400,
        )
        self.assertEqual(
            self.api(
                "Retrofit Programme Manager",
                f"/api/chat/threads/{tid}/proposals",
                {"capability": "quality-evidence"},
            )[0],
            404,
        )

    def test_web_panel_is_keyboard_operable_and_announces(self) -> None:
        js, index = (WEB / "chat.js").read_text(), (WEB / "index.html").read_text()
        self.assertIn("/chat.js", index)
        for needle in (
            'role: "log"',
            '"aria-live": "polite"',
            'role: "status"',
            'h("details"',
            'h("form"',
            'type: "submit"',
            'h("label", { for: "chat-question" }',
            "AI suggestion, not approved",
            "optional",
        ):
            self.assertIn(needle, js)
        self.assertNotIn("tabindex", js)
        self.assertNotIn("innerHTML", js)
        self.assertIn("chatCasePanel(id)", (WEB / "app.js").read_text())

    def test_all_five_skills_and_general_use_one_bounded_model_turn(self) -> None:
        tid = self.thread()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        for skill in (*REGISTRY, "general"):
            self.prompts.clear()
            code, answer = self.api(
                ROLE,
                f"/api/chat/threads/{tid}/ask",
                {"content": "What stage is it?", "skill": skill},
            )
            self.assertEqual((code, answer["kind"], answer["skill"]), (200, "answer", skill))
            self.assertEqual(len(self.prompts), 1)
            self.assertIn(f"Selected advisory skill: {skill}.", self.systems[-1])
            self.assertTrue(
                all(c["id"].startswith(("ZF-1/", "workflow/")) for c in answer["citations"])
            )
        self.assertEqual(self.store.cases["ZF-1"], before)
        code, skills = self.api(ROLE, "/api/chat/skills")
        self.assertEqual(code, 200)
        self.assertEqual([s["id"] for s in skills["skills"]], list(REGISTRY))

    def test_general_help_has_workflow_sources_and_no_record(self) -> None:
        tid = str(self.api(ROLE, "/api/chat/threads", {})[1]["id"])
        self.model = lambda _p: envelope(
            json.dumps(
                dict(answer="A person reviews decisions.", citations=["workflow/boundaries"])
            )
        )
        code, answer = self.api(
            ROLE,
            f"/api/chat/threads/{tid}/ask",
            {"content": "How can the team use chat?", "skill": "general"},
        )
        self.assertEqual((code, answer["kind"], answer["context"]), (200, "answer", "general"))
        self.assertIn("No case or home record is visible", self.prompts[-1])
        self.assertNotIn("ZF-1/", self.prompts[-1])
        self.assertEqual([c["id"] for c in answer["citations"]], ["workflow/boundaries"])
        self.model = lambda _p: envelope(None, "timeout")
        self.assertEqual(
            self.api(ROLE, f"/api/chat/threads/{tid}/ask", {"content": "Help", "skill": "general"})[
                1
            ]["kind"],
            "fallback",
        )

    def test_invalid_skills_do_not_store_or_infer(self) -> None:
        tid = self.thread()
        for invalid in ("router", "", None, 4, [], {}):
            code, _ = self.api(
                ROLE, f"/api/chat/threads/{tid}/ask", {"content": "Stage?", "skill": invalid}
            )
            self.assertEqual(code, 400, invalid)
        self.assertEqual(self.api(ROLE, f"/api/chat/threads/{tid}")[1]["messages"], [])
        self.assertEqual(self.prompts, [])

    def test_skill_scope_and_thread_owner_rechecked_without_inference(self) -> None:
        tid = self.thread()
        body = {"content": "Stage?", "skill": "quality-evidence"}
        self.assertEqual(
            self.api("Quality Inspector", f"/api/chat/threads/{tid}/ask", body)[0], 404
        )
        original = self.store.detail
        self.store.detail = lambda *a, **k: None
        try:
            self.assertEqual(self.api(ROLE, f"/api/chat/threads/{tid}/ask", body)[0], 404)
        finally:
            self.store.detail = original
        self.assertEqual(self.prompts, [])
        self.assertEqual(self.api(ROLE, f"/api/chat/threads/{tid}")[1]["messages"], [])

    def test_skill_question_outcome_audit_contains_reference_not_content(self) -> None:
        tid = self.thread()
        body = {"content": "CANARY private@example.test", "skill": "assessment-preparation"}
        code, answer = self.api(ROLE, f"/api/chat/threads/{tid}/ask", body)
        self.assertEqual((code, answer["kind"]), (200, "answer"))
        events = [row for row in self.store.audit_entries() if row["action"] == "chat.answer"]
        self.assertTrue(events)
        serialized = json.dumps(events)
        self.assertNotIn("CANARY", serialized)
        self.assertNotIn("private@example.test", serialized)
        self.assertIn("assessment-preparation", serialized)
        self.assertIn('"question_seq": 1', serialized.replace('\\"', '"'))

    def test_skill_help_never_bypasses_role_projection_or_privacy_gate(self) -> None:
        self.model = lambda _p: envelope(
            json.dumps(dict(answer="Check the workflow.", citations=["workflow/boundaries"]))
        )
        for role in roles.ROLES:
            if role == "Contractor":
                self.assertEqual(self.api(role, "/api/chat/skills")[0], 403)
                continue
            tid = self.thread(role=role)
            for skill in (*REGISTRY, "general"):
                code, answer = self.api(
                    role,
                    f"/api/chat/threads/{tid}/ask",
                    {"content": "Explain the workflow", "skill": skill},
                )
                self.assertEqual((code, answer["kind"]), (200, "answer"))
                self.assertNotIn(roles.PHONE, self.prompts[-1])
                if not projection.can_see_reason(dict(role=role)):
                    self.assertNotIn(roles.REASON, self.prompts[-1])
        tid = self.thread()
        self.prompts.clear()
        with patch.dict(os.environ, {"CHAT_DPIA_REF": ""}):
            self.assertEqual(
                self.api(
                    ROLE, f"/api/chat/threads/{tid}/ask", {"content": "Help", "skill": "general"}
                )[0],
                403,
            )
        self.assertEqual(self.prompts, [])
        self.assertEqual(self.api(ROLE, f"/api/chat/threads/{tid}")[1]["messages"], [])


if __name__ == "__main__":
    unittest.main()
