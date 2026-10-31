"""Issue 159: conversation panel answers are cited, labelled, proposal-only and fall back to the workflow.

Synthetic fixtures only (ADR 0005). The model is a stand-in for `store.ai.evidence`; no network is used.
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

import test_role_matrix as roles
from zava_forward.api.server import chat_admission
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

    def test_maximum_stored_question_with_expanding_mask_falls_back_safely(self) -> None:
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
                self.assertEqual((code, answer["kind"]), (200, "fallback"))
                self.assertEqual(answer["consumption"]["model_calls"], 0)
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
        widget = (WEB / "chat-widget.js").read_text()
        self.assertIn("/chat.js", index)
        self.assertIn("/chat-widget.js", index)
        for needle in (
            'role: "status"',
            'h("details"',
            "employeeChat.open()",
            "window.ChatWidget.create(",
            "AI suggestion, not approved",
            "optional",
        ):
            self.assertIn(needle, js)
        for needle in ('role: "log"', '"aria-live": "polite"', 'type: "submit"'):
            self.assertIn(needle, widget)
        self.assertNotIn('id: "chat-question"', js)
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

    def test_status_warning_is_role_scoped_and_describes_input(self) -> None:
        from zava_forward.core.chat_privacy import WARNING

        code, result = self.api(ROLE, "/api/chat/status")
        self.assertEqual((code, result["warning"]), (200, WARNING))
        self.assertIn("Unknown", result["retention"])
        self.assertEqual(self.api("Contractor", "/api/chat/status")[0], 403)
        self.assertEqual(self.call("", "/api/chat/status")[0], 401)
        js = (WEB / "chat.js").read_text()
        self.assertIn("chat-privacy employee-chat-error", js)
        self.assertIn("if (send.disabled) return;", js)
        self.assertIn('api("/api/chat/status", undefined, signal)', js)

    def test_status_reports_storage_approval_in_both_states(self) -> None:
        self.assertIs(self.api(ROLE, "/api/chat/status")[1]["storage_approved"], True)
        with patch.dict(os.environ, {k: "" for k in APPROVED}):
            self.assertIs(self.api(ROLE, "/api/chat/status")[1]["storage_approved"], False)

    def test_unstored_ask_is_rules_only_without_storage_or_model(self) -> None:
        with patch.dict(os.environ, {k: "" for k in APPROVED}):
            before = json.dumps(self.store.data.get("chat_threads"), sort_keys=True)
            code, reply = self.api(
                ROLE, "/api/chat/unstored-ask", {"content": "Stage?", "case_id": "ZF-1"}
            )
            self.assertEqual((code, reply["kind"]), (200, "fallback"))
            self.assertEqual(reply["context"], "ZF-1")
            self.assertEqual(self.prompts, [])
            self.assertEqual(json.dumps(self.store.data.get("chat_threads"), sort_keys=True), before)
            self.assertNotIn("Stage?", json.dumps(self.store.data))
            self.assertEqual(
                self.api(ROLE, "/api/chat/unstored-ask", {"content": "Stage?"})[1]["context"],
                "general",
            )

    def test_unstored_ask_rejections(self) -> None:
        path = "/api/chat/unstored-ask"
        self.assertEqual(self.api(ROLE, path, {"content": "Stage?"})[0], 400)
        with patch.dict(os.environ, {k: "" for k in APPROVED}):
            self.assertEqual(self.api("Contractor", path, {"content": "Stage?"})[0], 403)
            self.assertEqual(self.call("", path, {"content": "Stage?"})[0], 401)
            for bad in (
                {"content": "Stage?", "extra": 1},
                {"content": ""},
                {"content": 5},
                {"content": "x" * (MAX_CONTENT + 1)},
                {"content": "Stage?", "skill": "nope"},
            ):
                self.assertEqual(self.api(ROLE, path, bad)[0], 400, bad)
            self.assertEqual(
                self.api(ROLE, path, {"content": "Stage?", "case_id": "ZF-NOPE"})[0], 404
            )
        self.assertEqual(self.prompts, [])

    def test_both_turn_routes_deny_unapproved_model_without_calling_provider(self) -> None:
        with patch("zava_forward.api.server.chat_admission", wraps=chat_admission):
            for route in ("ask", "messages"):
                tid = self.thread()
                code, reply = self.api(
                    ROLE, f"/api/chat/threads/{tid}/{route}", {"content": "Stage?"}
                )
                self.assertEqual((code, reply["kind"]), (200, "fallback"))
                self.assertEqual(reply["consumption"]["model_calls"], 0)
                self.assertEqual(
                    reply["consumption"]["provider_outcome"], "activation-not-approved"
                )
        self.assertEqual(self.prompts, [])

    def test_legacy_route_uses_citations_and_refusals(self) -> None:
        tid = self.thread()
        code, reply = self.api(ROLE, f"/api/chat/threads/{tid}/messages", {"content": "Stage?"})
        self.assertEqual((code, reply["kind"], reply["withheld"]), (200, "answer", False))
        self.assertTrue(reply["citations"])
        self.prompts.clear()
        reply = self.api(ROLE, f"/api/chat/threads/{tid}/messages", {"content": "Approve it"})[1]
        self.assertEqual(reply["kind"], "refused")
        self.assertEqual(self.prompts, [])

    def test_receipt_survives_revocation_disappearance_and_failed_provider(self) -> None:
        user = self.store.staff[self.email(ROLE)]
        for event in ("role", "case", "thread", "failure"):
            tid = self.thread()
            case = self.store.cases["ZF-1"]
            original_role = user["role"]

            def provider(_prompt: str, event: str = event, tid: str = tid) -> dict[str, Any]:
                if event == "role":
                    user["role"] = "Mystery"
                elif event == "case":
                    self.store.cases.pop("ZF-1")
                elif event == "thread":
                    self.store.chat_delete(dict(user), tid)
                return dict(
                    outcome="timeout" if event == "failure" else "returned",
                    text="PRIVATE-COMPLETION",
                    usage=dict(prompt_tokens=5, completion_tokens=2, total_tokens=7),
                )

            self.model = provider
            before = len([e for e in self.store.audit_entries() if e["action"] == "chat.turn"])
            try:
                code, reply = self.ask(tid)
                self.assertEqual(
                    code, 200 if event == "failure" else 403 if event == "role" else 404
                )
                self.assertNotIn("PRIVATE-COMPLETION", json.dumps(reply))
                events = [e for e in self.store.audit_entries() if e["action"] == "chat.turn"]
                self.assertEqual(len(events), before + 1)
                receipt = json.loads(events[-1]["detail"])
                self.assertEqual(receipt["model_calls"], 1)
                self.assertEqual(receipt["tokens"]["total_tokens"], 7)
                self.assertNotIn("PRIVATE-COMPLETION", json.dumps(events))
            finally:
                user["role"] = original_role
                self.store.cases["ZF-1"] = case

    def test_prompt_bounds_fall_back_without_calls_and_sources_are_complete(self) -> None:
        from zava_forward.core import chat_panel

        tid = self.thread()
        self.assertEqual(self.ask(tid, "x" * 1001)[1]["kind"], "fallback")
        self.assertEqual(self.prompts, [])
        self.assertEqual(self.ask(tid, "x" * 1000)[1]["kind"], "answer")
        with patch.object(chat_panel, "MAX_INPUT_CHARS", 50):
            self.prompts.clear()
            reply = self.ask(tid)[1]
            self.assertEqual((reply["kind"], reply["consumption"]["model_calls"]), ("fallback", 0))
            self.assertEqual(self.prompts, [])
        self.ask(tid)
        prompt = self.prompts[-1]
        source_json = prompt.split("<<UNTRUSTED sources\n", 1)[1].split("\nUNTRUSTED>>", 1)[0]
        sources = json.loads(source_json)
        self.assertIn("ZF-1/stage", sources)
        self.assertLessEqual(len(chat_panel.SYSTEM) + len(prompt), chat_panel.MAX_INPUT_CHARS)
        for _ in range(6):
            self.ask(tid, "x" * 1000)
        history = self.prompts[-1].split("<<UNTRUSTED thread\n", 1)[1].split("\nUNTRUSTED>>", 1)[0]
        self.assertLessEqual(len(history), chat_panel.MAX_HISTORY_CHARS)

    def test_source_change_during_call_withholds_reply(self) -> None:
        tid = self.thread()
        case = self.store.cases["ZF-1"]
        stage = case["stage"]

        def mutate(_prompt: str) -> dict[str, Any]:
            case["stage"] = "Source changed during inference"
            return envelope(json.dumps(dict(answer="STALE-COMPLETION", citations=["ZF-1/stage"])))

        self.model = mutate
        try:
            reply = self.ask(tid)[1]
            self.assertEqual(reply["kind"], "withheld")
            self.assertNotIn("STALE-COMPLETION", json.dumps(reply))
            self.assertEqual(reply["consumption"]["model_calls"], 1)
        finally:
            case["stage"] = stage

    def test_skill_source_change_during_call_withholds_and_keeps_usage(self) -> None:
        case = self.store.cases["ZF-1"]
        stage = case["stage"]
        for skill in ("general", *REGISTRY):
            with self.subTest(skill=skill):
                tid = self.thread()

                def mutate(_prompt: str) -> dict[str, Any]:
                    case["stage"] = "Source changed during skill inference"
                    return dict(
                        outcome="returned",
                        text=json.dumps(dict(answer="STALE-SKILL", citations=["ZF-1/stage"])),
                        usage=dict(prompt_tokens=5, completion_tokens=2, total_tokens=7),
                    )

                self.model = mutate
                try:
                    code, answer = self.api(
                        ROLE, f"/api/chat/threads/{tid}/ask", {"content": "Stage?", "skill": skill}
                    )
                    self.assertEqual(
                        (code, answer["kind"], answer["skill"]), (200, "withheld", skill)
                    )
                    self.assertNotIn("STALE-SKILL", json.dumps(answer))
                    self.assertEqual(answer["consumption"]["tokens"]["total_tokens"], 7)
                finally:
                    case["stage"] = stage

    def test_skill_context_limit_counts_selected_system_and_preserves_audit(self) -> None:
        from zava_forward.core import chat_panel

        tid = self.thread()
        body = {"content": "Stage?", "skill": "general"}
        self.api(ROLE, f"/api/chat/threads/{tid}/ask", body)
        limit = len(chat_panel.SYSTEM) + len(self.prompts[-1])
        self.prompts.clear()
        tid = self.thread()
        with patch.object(chat_panel, "MAX_INPUT_CHARS", limit):
            code, answer = self.api(ROLE, f"/api/chat/threads/{tid}/ask", body)
        self.assertEqual((code, answer["kind"], answer["skill"]), (200, "fallback", "general"))
        self.assertEqual(answer["context"], "ZF-1")
        self.assertEqual(answer["consumption"]["model_calls"], 0)
        self.assertEqual(self.prompts, [])
        events = [row for row in self.store.audit_entries() if row["action"] == "chat.answer"]
        self.assertEqual(json.loads(events[-1]["detail"])["outcome"], "fallback")

    def test_role_change_does_not_replay_previous_role_questions(self) -> None:
        tid = self.thread()
        self.ask(tid, "PRIOR-ROLE-CONTEXT")
        user = self.store.staff[self.email(ROLE)]
        user["role"] = "Quality Inspector"
        self.prompts.clear()
        try:
            self.assertEqual(self.ask(tid)[1]["kind"], "answer")
            self.assertNotIn("PRIOR-ROLE-CONTEXT", self.prompts[-1])
        finally:
            user["role"] = ROLE

    @unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")
    def test_browser_warning_failure_keyboard_refusal_and_live_log(self) -> None:
        from playwright.sync_api import expect, sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.context.add_cookies(
                [{"name": "zf_session", "value": self.cks[ROLE].split("=", 1)[1], "url": self.base}]
            )
            page.route(
                "**/*",
                lambda route: (
                    route.continue_() if route.request.url.startswith(self.base) else route.abort()
                ),
            )
            page.route("**/api/chat/status", lambda route: route.abort())
            page.goto(self.base + "/app#/case/ZF-1?tab=ai")
            summary = page.locator("#chat-panel > summary")
            summary.focus()
            summary.press("Enter")
            page.get_by_role("button", name="Open chat", exact=True).click()
            expect(page.locator("#employee-chat-question")).to_be_visible()
            expect(
                page.locator("#employee-chat").get_by_role("button", name="Send")
            ).to_be_disabled()
            expect(page.locator("#employee-chat").get_by_role("alert")).to_contain_text(
                "Chat unavailable"
            )
            page.unroute("**/api/chat/status")
            page.reload()
            summary = page.locator("#chat-panel > summary")
            summary.focus()
            summary.press("Enter")
            page.get_by_role("button", name="Open chat", exact=True).click()
            question = page.get_by_label("Your work question", exact=True)
            expect(question).to_be_enabled()
            expect(
                page.locator("#employee-chat").get_by_role("button", name="Send")
            ).to_be_enabled()
            self.assertIn("chat-privacy", question.get_attribute("aria-describedby") or "")
            expect(page.locator("#chat-privacy")).to_contain_text("Do not type health")
            question.focus()
            question.fill("Approve this case")
            expect(page.locator("#employee-chat form")).to_have_attribute("data-unsaved", "true")
            question.press("Enter")
            expect(question).to_be_focused()
            expect(page.locator(".chat-widget-assistant").last).to_contain_text("cannot do it")
            expect(
                page.get_by_role("log", name="Employee assistant conversation")
            ).to_have_attribute("aria-live", "polite")
            page.route("**/api/chat/threads/*/ask", lambda route: route.abort())
            question.fill("Keep my unsent question")
            question.press("Enter")
            expect(page.locator("#employee-chat").get_by_role("alert")).to_contain_text(
                "Chat unavailable"
            )
            expect(question).to_have_value("Keep my unsent question")
            expect(page.locator("#employee-chat form")).to_have_attribute("data-unsaved", "true")
            page.set_viewport_size({"width": 390, "height": 844})
            expect(question).to_be_visible()
            self.assertEqual(self.prompts, [])
            browser.close()


if __name__ == "__main__":
    unittest.main()
