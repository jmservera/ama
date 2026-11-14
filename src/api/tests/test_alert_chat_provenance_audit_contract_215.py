"""#215: chat replies and recorded audit metadata keep provenance, outcome and citations explicit.

Synthetic fixtures only; the model is a stand-in and no network is used. Contract checks on the
API payload and the audit ledger, not live model, browser, screen reader or staff evidence.
"""

import json
import os
import re
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import patch

from regulatory_fixture import ENV, NOW, Fixture
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import SOURCE_LABELS
from zava_forward.core.regulatory_chat import RegulatoryChat

sys.path.append(str(Path(__file__).resolve().parent))
import test_role_matrix as roles  # noqa: E402
from zava_forward.api.server import App

APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
CASE = "ZF-4"
UNBLOCK = "what can I do to unblock this case?"
VISIT = "how can we fix this safety? Should we schedule a visit?"
HELD = "zzz quantum bananas"
UNSUPPORTED = "The safety stop is cleared and the visit is booked."
GENERATIVE = "generative-grounded"
RULES = "decision-rules-fallback"


def envelope(text: str | None) -> dict[str, Any]:
    return dict(outcome="returned", text=text, usage=None, source="ai", model="synthetic")


class CaseChatProvenanceTests(roles.Matrix):
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
    def first_id(prompt: str) -> str:
        first = re.search(rf'"({CASE}/[^"]+)"', prompt)
        assert first
        return first.group(1)

    def cite_first(self, prompt: str) -> dict[str, Any]:
        draft = dict(answer="From the case card.", citations=[self.first_id(prompt)])
        return envelope(json.dumps(draft))

    def api(self, path: str, body: Any = None) -> tuple[int, Any]:
        code, text = self.call(self.cookie, path, body)
        return code, (json.loads(text) if text.startswith(("{", "[")) else text)

    def ask(self, question: str) -> tuple[dict[str, Any], dict[str, Any]]:
        code, thread = self.api("/api/chat/threads", {"case_id": CASE})
        self.assertEqual(code, 200, thread)
        code, reply = self.api(f"/api/chat/threads/{thread['id']}/ask", {"content": question})
        self.assertEqual(code, 200, reply)
        assert isinstance(reply, dict)
        return thread, reply

    def record(self) -> str:
        return json.dumps(self.store.data["cases"], sort_keys=True, default=str)

    def stored(self, tid: str) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = self.store.chat_repo.doc[tid]["messages"]
        return messages

    def answer_audits(self, tid: str) -> list[dict[str, Any]]:
        rows = [e for e in self.store.audit_entries() if e["action"] == "chat.answer"]
        details = [json.loads(e["detail"]) for e in rows]
        return [d for d in details if d["thread_id"] == tid]

    def check_citations(self, reply: dict[str, Any]) -> None:
        ids = [c["id"] for c in reply["citations"]]
        self.assertTrue(ids, reply)
        self.assertEqual(len(ids), len(set(ids)), ids)
        self.assertTrue(all(i.startswith(f"{CASE}/") for i in ids), ids)

    def test_generative_turns_disclose_the_model_and_record_the_same_citations(self) -> None:
        for question in (UNBLOCK, VISIT):
            with self.subTest(question=question):
                thread, reply = self.ask(question)
                self.assertEqual(reply["kind"], "answer", reply)
                self.assertEqual(reply["answer_source"], GENERATIVE)
                self.assertNotEqual(reply["model"], "workflow-only")
                self.assertIn("generative AI model", reply["answer_source_label"])
                self.check_citations(reply)
                saved = self.stored(thread["id"])[-1]
                self.assertEqual((saved["role"], saved["model"]), ("assistant", reply["model"]))
                self.assertEqual(saved["evidence"], [c["id"] for c in reply["citations"]])
                audit = self.answer_audits(thread["id"])
                self.assertEqual([a["outcome"] for a in audit], ["answer"])

    def test_decision_model_turns_never_claim_a_generative_origin(self) -> None:
        self.model = lambda _p: envelope("not json")
        for question in (UNBLOCK, VISIT):
            with self.subTest(question=question):
                thread, reply = self.ask(question)
                self.assertEqual(reply["kind"], "answer", reply)
                self.assertEqual(reply["answer_source"], RULES)
                self.assertEqual(reply["model"], "workflow-only")
                self.assertEqual(reply["answer_source_label"], SOURCE_LABELS[RULES])
                self.assertNotIn("generative AI model", reply["answer_source_label"])
                self.check_citations(reply)
                saved = self.stored(thread["id"])[-1]
                self.assertEqual(saved["model"], "workflow-only")
                self.assertEqual(saved["evidence"], [c["id"] for c in reply["citations"]])

    def test_withheld_draft_is_not_shown_stored_or_attributed_to_a_model(self) -> None:
        self.model = lambda p: envelope(
            json.dumps(dict(answer=UNSUPPORTED, citations=[self.first_id(p)]))
        )
        thread, reply = self.ask(VISIT)
        self.assertNotIn(UNSUPPORTED, reply["reply"])
        self.assertEqual(reply["answer_source"], RULES)
        self.assertEqual(reply["model"], "workflow-only")
        self.check_citations(reply)
        saved = self.stored(thread["id"])
        self.assertTrue(all(UNSUPPORTED not in m["content"] for m in saved))
        self.assertEqual(saved[-1]["model"], "workflow-only")

    def test_held_turn_has_no_citations_and_no_generative_answer_origin(self) -> None:
        self.model = lambda _p: envelope(json.dumps(dict(answer="Unsourced.", citations=[])))
        thread, reply = self.ask(HELD)
        self.assertNotEqual(reply["kind"], "answer", reply)
        self.assertEqual(reply["citations"], [])
        self.assertNotEqual(reply["answer_source"], GENERATIVE)
        self.assertNotIn("generative AI model", reply.get("answer_source_label", ""))
        saved = self.stored(thread["id"])[-1]
        self.assertEqual((saved["model"], saved["evidence"]), (reply["model"], []))
        audit = self.answer_audits(thread["id"])
        self.assertEqual([a["outcome"] for a in audit], [reply["kind"]])
        self.assertNotEqual(audit[0]["outcome"], "answer")

    def test_receipts_record_outcome_without_question_text_and_leave_cases_unchanged(self) -> None:
        before = self.record()
        questions = (UNBLOCK, VISIT, HELD)
        for generative in (True, False):
            self.model = self.cite_first if generative else (lambda _p: envelope("not json"))
            for question in questions:
                thread, reply = self.ask(question)
                receipts = [
                    json.loads(e["detail"])
                    for e in self.store.audit_entries()
                    if e["action"] == "chat.turn" and thread["id"] in e["detail"]
                ]
                self.assertEqual(receipts[-1]["outcome"], reply["kind"])
                self.assertEqual(reply["consumption"]["outcome"], reply["kind"])
        text = json.dumps(list(self.store.audit_entries()))
        self.assertNotIn("quantum bananas", text)
        self.assertEqual(self.record(), before)
        self.assertTrue(self.store.verify_audit())


class RegulatoryHeldProvenanceTests(unittest.TestCase):
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
        self.user: dict[str, Any] = self.f.store.staff[self.f.user["email"]]

    def cases(self) -> str:
        return json.dumps(self.f.store.cases, sort_keys=True, default=str)

    def test_held_and_answered_turns_are_workflow_only_and_doubt_changes_no_record(self) -> None:
        before = self.cases()
        tid = self.reg.start(self.user, "ZF-1")
        answered = self.reg.ask(self.user, tid, "What are the hazard sources?")
        held = self.reg.ask(self.user, tid, HELD)
        self.assertEqual((answered["kind"], held["kind"]), ("answer", "refused"))
        self.assertTrue(answered["citations"])
        ids = [c["id"] for c in answered["citations"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual((held["citations"], held["cards"]), ([], []))
        for reply in (answered, held):
            self.assertEqual(reply["usage"]["model_calls"], 0)
            self.assertIn("synthetic-demo", reply["label"])
        self.assertTrue(held["requires_human"] and held["workflow_only"])
        receipt = self.reg.doubt(self.user, tid, held["turn"])
        self.assertEqual(receipt["referred_turn"], held["turn"])
        self.assertEqual(receipt["status"], "sent-to-exercise-inbox")
        turns = [e for e in self.f.store.audit_entries() if e["action"] == "chat.regulatory.turn"]
        self.assertEqual(len(turns), 2)
        self.assertEqual(self.cases(), before)


if __name__ == "__main__":
    unittest.main()
