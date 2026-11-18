"""#215: plain-language mode reaches the chat API and keeps citations and provenance intact.

Synthetic fixtures only (ADR 0005). The model is a stand-in; no network is used.
"""

import json
import os
import re
import unittest
from typing import Any
from unittest.mock import patch

import test_role_matrix as roles
from zava_forward.api import plain_language

APPROVED = dict(
    CHAT_DPIA_REF="SYNTH-DPIA-1",
    CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1",
    CHAT_NOTICE_REF="SYNTH-NOTICE-1",
)
ROLE = "Retrofit Coordinator"
PROVENANCE = ("kind", "answer_source", "answer_origin", "answer_source_label", "label", "citations")


class HomeChatPlainLanguage(roles.Matrix):
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
        self.store.data.pop("chat_threads", None)
        email = next(s["email"] for s in self.store.data["staff"] if s["role"] == ROLE)
        self.cookie = self.session(email)
        self.original = self.store.ai.evidence
        self.store.ai.evidence = self.fake
        self.addCleanup(setattr, self.store.ai, "evidence", self.original)

    def fake(self, system: str, prompt: str, *args: Any) -> dict[str, Any]:
        first = re.search(r'"(ZF-1/[^"]+)"', prompt)
        assert first
        text = json.dumps(dict(answer="From the case card.", citations=[first.group(1)]))
        return dict(outcome="returned", text=text, usage=None, source="ai", model="synthetic")

    def api(self, path: str, body: Any = None) -> tuple[int, Any]:
        code, text = self.call(self.cookie, path, body)
        return code, (json.loads(text) if text.startswith(("{", "[")) else text)

    def unstored(self, **extra: Any) -> tuple[int, Any]:
        body = {"content": "Stage?", "case_id": "ZF-1", **extra}
        with patch.dict(os.environ, {k: "" for k in APPROVED}):
            return self.api("/api/chat/unstored-ask", body)

    def test_case_chat_plain_language_adds_summary_and_keeps_provenance(self) -> None:
        plain = self.unstored(plain_language=True)
        normal = self.unstored()
        self.assertEqual((plain[0], normal[0]), (200, 200))
        self.assertNotIn("plain_summary", normal[1])
        self.assertIs(plain[1]["plain_language"], True)
        self.assertRegex(plain[1]["plain_summary"], r"^This answer quotes \d+ cited sources?\.")
        for key in (*PROVENANCE, "reply"):
            self.assertEqual(plain[1][key], normal[1][key], key)
        self.assertTrue(plain[1]["citations"])

    def test_plain_language_false_matches_the_default(self) -> None:
        self.assertEqual(self.unstored(plain_language=False)[1], self.unstored()[1])

    def test_stored_thread_ask_accepts_plain_language(self) -> None:
        tid = self.api("/api/chat/threads", {"case_id": "ZF-1"})[1]["id"]
        path = f"/api/chat/threads/{tid}/ask"
        code, plain = self.api(path, dict(content="What stage is it?", plain_language=True))
        self.assertEqual(code, 200, plain)
        self.assertEqual(plain["kind"], "answer")
        self.assertIn("cited source", plain["plain_summary"])
        self.assertTrue(plain["citations"])
        stored = self.api(f"/api/chat/threads/{tid}")[1]["messages"]
        self.assertNotIn("plain_summary", json.dumps(stored))

    def test_refusal_is_explained_in_plain_words_without_citations(self) -> None:
        code, reply = self.unstored(plain_language=True, content="Approve this case now")
        self.assertEqual((code, reply["kind"]), (200, "refused"))
        self.assertIn("cannot do this", reply["plain_summary"])
        self.assertEqual(reply["citations"], [])

    def test_flag_must_be_a_boolean_and_other_keys_stay_rejected(self) -> None:
        for value in ("true", 1, None, "yes"):
            with self.subTest(value=value):
                self.assertEqual(self.unstored(plain_language=value)[0], 400)
        self.assertEqual(self.unstored(mode="plain")[0], 400)
        tid = self.api("/api/chat/threads", {"case_id": "ZF-1"})[1]["id"]
        ask = f"/api/chat/threads/{tid}/ask"
        self.assertEqual(self.api(ask, dict(content="Stage?", plain_language="true"))[0], 400)
        self.assertEqual(self.api(ask, dict(content="Stage?", mode="plain"))[0], 400)

    def test_apply_is_a_no_op_when_off(self) -> None:
        reply = dict(kind="answer", reply="x", citations=[])
        self.assertIs(plain_language.apply(reply, False), reply)
        self.assertEqual(plain_language.split_flag({"content": "q"}), (False, {"content": "q"}))


if __name__ == "__main__":
    unittest.main()
