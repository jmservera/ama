"""Chat thread storage (issue #160) on the in-memory Store and the SQL store with identical behaviour.

All fixtures are labelled synthetic demonstration data (ADR 0005)."""
import json
import re
import sqlite3
import tempfile
import threading
import unittest
from copy import deepcopy
from pathlib import Path

import dataset
import test_sqlstore as base
from zava_forward.core import chatthreads
from zava_forward.core.assistants import REGISTRY
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import FALLBACK, LABEL, ChatPanel, ModelUnavailable
from zava_forward.core.chatthreads import ChatNotFound
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store

SAM, PAM = dataset.DATA["staff"]
SECRET = "SYNTHETIC-chat-text-must-not-reach-ledger"


class ChatBehaviour:
    """Shared behaviour; subclasses supply make_store."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = self.make_store(self.tmp.name)

    def thread(self, user=SAM, **kw):
        return self.store.chat_create_thread(user, case_id=kw.pop("case_id", "ZF-1"), task=kw.pop("task", "stock-prioritisation"),
                                             model=kw.pop("model", "synthetic-model-1"), **kw)

    def test_thread_records_owner_case_task_version_and_model(self):
        t = self.thread(title="SYNTHETIC demo")
        self.assertEqual((t["owner"], t["case_id"], t["task"], t["model"], t["status"], t["rowversion"]),
                         (SAM["email"], "ZF-1", "stock-prioritisation", "synthetic-model-1", "active", 1))
        self.assertTrue(t["task_version"])

    def test_messages_keep_order_evidence_and_model_identity(self):
        t = self.thread()
        self.store.chat_add_message(SAM, t["id"], "user", "Why is this home ranked first?")
        self.store.chat_add_message(SAM, t["id"], "assistant", "Because of the hazard.", evidence=["case:ZF-1", "ranking:v1"])
        got = self.store.chat_resume(SAM, t["id"])
        self.assertEqual([m["seq"] for m in got["messages"]], [1, 2])
        self.assertEqual(got["messages"][1]["evidence"], ["case:ZF-1", "ranking:v1"])
        self.assertEqual(got["messages"][1]["model"], "synthetic-model-1")
        self.assertEqual(got["messages"][1]["task_version"], t["task_version"])
        self.assertEqual(got["message_count"], 2)

    def test_messages_persist_the_role_of_the_asking_actor_after_restart(self):
        t = self.thread()
        role_b = dict(SAM, role="Retrofit Coordinator")
        for actor, text in ((SAM, "A first"), (role_b, "B first"), (SAM, "A second")):
            self.store.chat_add_message(actor, t["id"], "user", text)
        again = self.make_store(self.tmp.name)
        self.addCleanup(getattr(again, "close", lambda: None))
        messages = again.chat_resume(SAM, t["id"])["messages"]
        self.assertEqual([m["actor_role"] for m in messages],
                         [SAM["role"], role_b["role"], SAM["role"]])
        self.assertEqual([m["content"] for m in messages], ["A first", "B first", "A second"])

    def test_list_archive_and_delete_own_threads(self):
        a, b = self.thread(), self.thread()
        self.assertEqual({t["id"] for t in self.store.chat_list_threads(SAM)}, {a["id"], b["id"]})
        self.store.chat_archive(SAM, a["id"])
        self.assertEqual([t["id"] for t in self.store.chat_list_threads(SAM)], [b["id"]])
        self.assertEqual({t["id"] for t in self.store.chat_list_threads(SAM, include_archived=True)}, {a["id"], b["id"]})
        with self.assertRaises(ValueError):
            self.store.chat_add_message(SAM, a["id"], "user", "no")
        self.store.chat_delete(SAM, b["id"])
        with self.assertRaises(ChatNotFound):
            self.store.chat_resume(SAM, b["id"])

    def test_other_users_cannot_see_or_change_a_thread(self):
        t = self.thread()
        self.store.chat_add_message(SAM, t["id"], "user", "private")
        self.assertEqual(self.store.chat_list_threads(PAM), [])
        for call in (lambda: self.store.chat_resume(PAM, t["id"]), lambda: self.store.chat_archive(PAM, t["id"]),
                     lambda: self.store.chat_delete(PAM, t["id"]), lambda: self.store.chat_add_message(PAM, t["id"], "user", "x")):
            with self.assertRaises(ChatNotFound):
                call()
        self.assertEqual(len(self.store.chat_resume(SAM, t["id"])["messages"]), 1)

    def test_row_version_refuses_stale_writes(self):
        t = self.thread()
        self.store.chat_add_message(SAM, t["id"], "user", "one", expected_version=1)
        with self.assertRaises(ConflictError):
            self.store.chat_add_message(SAM, t["id"], "user", "two", expected_version=1)
        with self.assertRaises(ConflictError):
            self.store.chat_archive(SAM, t["id"], expected_version=1)
        with self.assertRaises(ConflictError):
            self.store.chat_delete(SAM, t["id"], expected_version=1)
        self.store.chat_archive(SAM, t["id"], expected_version=2)
        self.assertEqual(self.store.chat_resume(SAM, t["id"])["rowversion"], 3)

    def test_concurrent_appends_get_distinct_sequences(self):
        t = self.thread()
        errors = []

        def add(i):
            try:
                self.store.chat_add_message(SAM, t["id"], "user", f"m{i}")
            except Exception as e:
                errors.append(e)
        workers = [threading.Thread(target=add, args=(i,)) for i in range(8)]
        for w in workers:
            w.start()
        for w in workers:
            w.join()
        self.assertEqual(errors, [])
        self.assertEqual(sorted(m["seq"] for m in self.store.chat_resume(SAM, t["id"])["messages"]), list(range(1, 9)))

    def test_ledger_records_metadata_only_and_survives_deletion(self):
        t = self.thread(title=SECRET)
        self.store.chat_add_message(SAM, t["id"], "user", SECRET)
        self.store.chat_delete(SAM, t["id"])
        entries = [e for e in self.store.audit_entries() if e["action"].startswith("chat.")]
        self.assertEqual([e["action"] for e in entries], ["chat.thread.created", "chat.message.added", "chat.thread.deleted"])
        self.assertNotIn(SECRET, json.dumps(entries))
        self.assertEqual(json.loads(entries[1]["detail"])["thread"], t["id"])
        self.assertTrue(self.store.verify_audit())

    def test_employee_skills_persist_cited_answers_and_minimal_audit(self):
        if hasattr(self.store, "db"):
            self.addCleanup(self.store.db.close)
        env = dict(CHAT_DPIA_REF="SYN-DPIA", CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
                   CHAT_NOTICE_REF="SYN-NOTICE")
        calls = []

        def model(system, prompt):
            calls.append((system, prompt))
            return json.dumps(dict(answer="Check the case stage.", citations=["ZF-1/stage"]))

        panel = ChatPanel(ChatIsolation(self.store, env=env), model)
        before = deepcopy(self.store.cases["ZF-1"])
        turns = []
        for skill in (*REGISTRY, "general"):
            with self.subTest(skill=skill):
                thread = self.thread()
                count = len(calls)
                answer = panel.ask(SAM, thread["id"], f"{SECRET} private@example.test",
                                   skill=skill)
                self.assertEqual(len(calls), count + 1)
                self.assertIn(f"Selected advisory skill: {skill}.", calls[-1][0])
                self.assertEqual((answer["kind"], answer["skill"], answer["label"]),
                                 ("answer", skill, LABEL))
                self.assertEqual(answer["consumption"]["model_calls"], 1)
                self.assertEqual([c["id"] for c in answer["citations"]], ["ZF-1/stage"])
                self.assertIn('"ZF-1/stage"', calls[-1][1])
                turns.append((thread["id"], skill, answer))
        self.store.save()
        again = self.make_store(self.tmp.name)
        if hasattr(again, "db"):
            self.addCleanup(again.db.close)
        events = [json.loads(e["detail"]) for e in again.audit_entries()
                  if e["action"] == "chat.answer"]
        for tid, skill, answer in turns:
            with self.subTest(reopened_skill=skill):
                messages = again.chat_resume(SAM, tid)["messages"]
                self.assertEqual([m["role"] for m in messages], ["user", "assistant"])
                self.assertIn(SECRET, messages[0]["content"])
                self.assertNotIn("private@example.test", messages[0]["content"])
                self.assertEqual(messages[1]["content"], answer["reply"])
                self.assertEqual(messages[1]["evidence"], ["ZF-1/stage"])
                self.assertIn(dict(thread_id=tid, question_seq=messages[0]["seq"],
                                   skill=skill, outcome="answer"), events)
        self.assertNotIn(SECRET, json.dumps(list(again.audit_entries())))
        self.assertNotIn("private@example.test", json.dumps(list(again.audit_entries())))
        self.assertEqual(again.cases["ZF-1"], before)
        self.assertTrue(again.verify_audit())

    def test_employee_general_sources_fallback_and_foreign_owner_denial(self):
        if hasattr(self.store, "db"):
            self.addCleanup(self.store.db.close)
        env = dict(CHAT_DPIA_REF="SYN-DPIA", CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
                   CHAT_NOTICE_REF="SYN-NOTICE")
        calls = []

        def model(system, prompt):
            calls.append(prompt)
            self.assertIn("No case or home record is visible", prompt)
            self.assertNotIn("ZF-1/", prompt)
            return json.dumps(dict(answer="A person reviews decisions.",
                                   citations=["workflow/boundaries"]))

        def unavailable(system, prompt):
            raise ModelUnavailable("timeout", calls=1)

        panel = ChatPanel(ChatIsolation(self.store, env=env), model)
        for skill in (*REGISTRY, "general"):
            with self.subTest(skill=skill):
                tid = self.thread(case_id="")["id"]
                panel.model = model
                count = len(calls)
                answer = panel.ask(SAM, tid, "Explain the workflow", skill=skill)
                self.assertEqual((answer["kind"], answer["context"]), ("answer", "general"))
                self.assertEqual(len(calls), count + 1)
                self.assertEqual([c["id"] for c in answer["citations"]],
                                 ["workflow/boundaries"])
                messages = self.store.chat_resume(SAM, tid)["messages"]
                with self.assertRaises(ChatNotFound):
                    panel.ask(PAM, tid, "Read another employee's question", skill=skill)
                self.assertEqual(len(calls), count + 1)
                self.assertEqual(self.store.chat_resume(SAM, tid)["messages"], messages)
                for provider in (None, unavailable):
                    panel.model = provider
                    fallback = panel.ask(SAM, tid, "Explain the workflow", skill=skill)
                    self.assertEqual((fallback["kind"], fallback["reply"],
                                      fallback["workflow_only"]), ("fallback", FALLBACK, True))
                    event = [json.loads(e["detail"]) for e in self.store.audit_entries()
                             if e["action"] == "chat.answer"][-1]
                    self.assertEqual((event["thread_id"], event["skill"], event["outcome"]),
                                     (tid, skill, "fallback"))
        self.assertTrue(self.store.verify_audit())

    def test_validation(self):
        with self.assertRaises(ValueError):
            self.store.chat_create_thread(SAM, case_id="NO-SUCH")
        with self.assertRaises(ValueError):
            self.store.chat_create_thread(SAM, task="not-registered")
        with self.assertRaises(ValueError):
            self.store.chat_create_thread({"role": "x"})
        t = self.thread()
        for role, content in (("system", "x"), ("user", "  "), ("user", "x" * (chatthreads.MAX_CONTENT + 1))):
            with self.assertRaises(ValueError):
                self.store.chat_add_message(SAM, t["id"], role, content)


class MemoryChatTests(ChatBehaviour, unittest.TestCase):
    def make_store(self, tmp):
        data = Path(tmp) / "zavaforward.json"
        data.write_text(json.dumps(dataset.DATA))
        return Store(str(data))

    def test_restart_keeps_threads(self):
        t = self.thread()
        self.store.save()
        again = self.make_store(self.tmp.name)
        self.assertEqual([x["id"] for x in again.chat_list_threads(SAM)], [t["id"]])


class SqlChatTests(ChatBehaviour, unittest.TestCase):
    def make_store(self, tmp):
        data, db = base.seed(tmp)
        return SqlStore(data, db)

    def test_migration_is_idempotent_and_survives_restart(self):
        t = self.thread()
        self.store.chat_add_message(SAM, t["id"], "user", "kept")
        again = SqlStore(*base.seed(self.tmp.name))
        self.assertEqual(len(again.chat_resume(SAM, t["id"])["messages"]), 1)
        for ddl in chatthreads.SQLITE_DDL:
            again.db.execute(ddl)

    def test_content_tables_are_separate_from_the_ledger(self):
        t = self.thread()
        self.store.chat_add_message(SAM, t["id"], "user", SECRET)
        raw = sqlite3.connect(self.store.db_path)
        tables = {r[0] for r in raw.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({"chat_thread", "chat_message", "audit"} <= tables)
        self.assertEqual(raw.execute("SELECT COUNT(*) FROM audit WHERE detail LIKE ?", ("%" + SECRET + "%",)).fetchone()[0], 0)
        self.assertEqual(raw.execute("SELECT COUNT(*) FROM chat_message WHERE content=?", (SECRET,)).fetchone()[0], 1)

    def test_legacy_message_role_migration_is_unknown_and_idempotent(self):
        t = self.thread()
        self.store.chat_add_message(SAM, t["id"], "user", "legacy")
        self.store.db.execute("ALTER TABLE chat_message DROP COLUMN actor_role")
        again = SqlStore(*base.seed(self.tmp.name))
        self.addCleanup(again.db.close)
        self.assertEqual(again.chat_resume(SAM, t["id"])["messages"][0]["actor_role"], "")
        again.chat_add_message(SAM, t["id"], "user", "current")
        restarted = SqlStore(*base.seed(self.tmp.name))
        self.addCleanup(restarted.db.close)
        self.assertEqual([m["actor_role"] for m in restarted.chat_resume(SAM, t["id"])["messages"]],
                         ["", SAM["role"]])

    def test_chat_sql_is_portable(self):
        src = Path(chatthreads.__file__).read_text()
        a, b = src.index("SQLITE_DDL = ("), src.index("MSSQL_DDL = (")
        shared = src[:a] + src[b:]
        banned = re.compile(r"(?i)\bINSERT\s+OR\b|\bREPLACE\s+INTO\b|\bAUTOINCREMENT\b|\bPRAGMA\b")
        self.assertEqual([l.strip() for l in shared.splitlines() if banned.search(l)], [])
