import json
import tempfile
import unittest
from pathlib import Path

import dataset
import test_sqlstore as base
from zava_forward.core import chat_privacy as cp
from zava_forward.core.chat_privacy import ChatNotApproved, ChatPrivacy
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

U1, ADMIN = dataset.DATA["staff"]
TASK = "stock-prioritisation"
APPROVED = dict(CHAT_DPIA_REF="SYNTH-DPIA-1", CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1", CHAT_NOTICE_REF="SYNTH-NOTICE-1")
OTHER = dict(U1, email="other@example.test")


class MemoryLifecycle:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = self.make_store(self.tmp.name)
        self.c = ChatPrivacy(self.store, env=APPROVED)

    def test_off_by_default_and_needs_informed_opt_in(self):
        self.assertEqual(self.c.memory_status(U1)["reason"], "not opted in")
        with self.assertRaises(ChatNotApproved):
            self.c.add_memory(U1, "short summaries", task=TASK)
        with self.assertRaises(ValueError):
            self.c.opt_in(U1, "yes")
        with self.assertRaises(ChatNotApproved):
            ChatPrivacy(self.store, env={}).opt_in(U1, True)
        self.c.opt_in(U1, True)
        self.assertTrue(self.c.memory_status(U1)["active"])
        self.assertEqual(self.c.prompt_memory(OTHER, TASK), [])

    def test_items_are_inspectable_editable_deletable_and_clearable(self):
        self.c.opt_in(U1, True)
        a = self.c.add_memory(U1, "short summaries", "working_preference", "typed in chat", task=TASK)
        b = self.c.add_memory(U1, "team abbreviations", "terminology", task=TASK)
        item = self.c.list_memory(U1)[0]
        self.assertEqual((item["content"], item["source"], item["item_class"]), ("short summaries", "typed in chat", "working_preference"))
        self.assertTrue(item["created_at"] and "Unknown" in item["expiry"])
        self.c.edit_memory(U1, a, "bullet summaries")
        self.assertEqual(self.c.list_memory(U1)[0]["content"], "bullet summaries")
        with self.assertRaises(ValueError):
            self.c.edit_memory(U1, a, "tenant has asthma")
        with self.assertRaises(LookupError):
            self.c.delete_memory(OTHER, a)
        with self.assertRaises(LookupError):
            self.c.edit_memory(OTHER, a, "x")
        self.c.delete_memory(U1, a)
        self.assertEqual([m["id"] for m in self.c.list_memory(U1)], [b])
        self.c.add_memory(U1, "another", task=TASK)
        self.assertEqual(self.c.clear_memory(U1), 2)
        self.assertEqual(self.c.list_memory(U1), [])

    def test_special_category_and_unknown_class_refused(self):
        self.c.opt_in(U1, True)
        for text in ("tenant has dementia", "vulnerable resident at 12 High St"):
            with self.assertRaises(ValueError):
                self.c.add_memory(U1, text, task=TASK)
        with self.assertRaises(ValueError):
            self.c.add_memory(U1, "ok", item_class="resident_health", task=TASK)
        self.assertEqual(self.c.list_memory(U1), [])

    def test_retention_unknown_per_class_until_dpo_approves(self):
        self.assertTrue(all(v.startswith("Unknown") for v in self.c.memory_status(U1)["retention"].values()))
        self.assertEqual(set(self.c.memory_status(U1)["retention"]), set(cp.MEMORY_CLASSES))
        c = ChatPrivacy(self.store, env=dict(APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="7"))
        c.opt_in(U1, True)
        c.add_memory(U1, "tables", task=TASK)
        self.assertTrue(c.list_memory(U1)[0]["expires_at"])
        self.assertEqual(c.memory_status(U1)["retention"]["terminology"], "7 days")

    def test_global_and_task_switches_need_an_administrator(self):
        self.c.opt_in(U1, True)
        with self.assertRaises(PermissionError):
            self.c.set_global(U1, False)
        self.c.add_memory(U1, "tables", task=TASK)
        self.c.set_global(ADMIN, False)
        self.assertEqual(self.c.prompt_memory(U1, TASK), [])
        self.assertIn("administrator", self.c.memory_status(U1)["reason"])
        with self.assertRaises(ChatNotApproved):
            self.c.add_memory(U1, "more", task=TASK)
        self.assertEqual(len(self.c.list_memory(U1)), 1)
        self.c.set_global(ADMIN, True)
        self.assertEqual(len(self.c.prompt_memory(U1, TASK)), 1)
        self.c.set_task(ADMIN, TASK, False)
        self.assertEqual(self.c.prompt_memory(U1, TASK), [])
        self.assertEqual(len(self.c.prompt_memory(U1, "funding-evidence")), 1)
        with self.assertRaises(ValueError):
            self.c.set_task(ADMIN, "nope", False)
        with self.assertRaises(PermissionError):
            self.c.set_task(U1, TASK, True)

    def test_task_is_required_and_role_comes_from_the_register(self):
        self.c.opt_in(U1, True)
        with self.assertRaises(TypeError):
            self.c.add_memory(U1, "tables")
        with self.assertRaises(ValueError):
            self.c.add_memory(U1, "tables", task="")
        with self.assertRaises(PermissionError):
            self.c.set_global(dict(U1, role=ADMIN["role"]), False)

    def test_expired_items_are_hidden_and_not_editable(self):
        self.c.opt_in(U1, True)
        i = self.c.add_memory(U1, "tables", task=TASK)
        self.store.chat_repo.update_memory(cp.user_key(U1), i, expires_at="2000-01-01T00:00:00.000+00:00")
        self.assertEqual(self.c.list_memory(U1), [])
        with self.assertRaises(LookupError):
            self.c.edit_memory(U1, i, "new")

    def test_prompt_memory_is_non_authoritative_and_never_evidence(self):
        self.c.opt_in(U1, True)
        self.c.add_memory(U1, "tables", task=TASK)
        self.assertEqual(self.c.prompt_memory(U1, TASK), [dict(preference="tables", authority="none", evidence=False, item_class="working_preference")])
        mid = self.store.chat_repo.memories("sam@example.test")[0]["id"]
        t = self.store.chat_create_thread(U1)
        with self.assertRaises(ValueError):
            self.store.chat_add_message(U1, t["id"], "assistant", "x", evidence=[mid])

    def test_opt_out_deletes_items_and_ledger_has_no_content(self):
        self.c.opt_in(U1, True)
        self.c.add_memory(U1, "secret-ish preference", task=TASK)
        self.assertEqual(self.c.opt_out(U1), 1)
        self.assertFalse(self.c.memory_status(U1)["active"])
        self.assertEqual(self.c.list_memory(U1), [])
        log = json.dumps(list(self.store.audit_entries()))
        self.assertIn("chat.memory.opt_out", log)
        self.assertNotIn("secret-ish", log)

    def test_erase_and_purge_cover_memory(self):
        self.c.opt_in(U1, True)
        self.c.add_memory(U1, "tables", task=TASK)
        self.assertEqual(self.c.erase(U1)["memory"], 1)


class MemoryStoreLifecycle(MemoryLifecycle, unittest.TestCase):
    def make_store(self, tmp):
        data = Path(tmp) / "zavaforward.json"
        data.write_text(json.dumps(dataset.DATA))
        return Store(str(data))


class SqlLifecycle(MemoryLifecycle, unittest.TestCase):
    def make_store(self, tmp):
        data, db = base.seed(tmp)
        return SqlStore(data, db)

    def test_old_chat_memory_table_gains_new_columns(self):
        self.store.db.execute("DROP TABLE chat_memory")
        self.store.db.execute("CREATE TABLE chat_memory (id TEXT PRIMARY KEY, owner TEXT NOT NULL, owner_role TEXT NOT NULL, "
                              "content TEXT NOT NULL, redactions TEXT NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NULL)")
        self.store._create_schema()
        cols = {r[1] for r in self.store.db.execute("PRAGMA table_info(chat_memory)").fetchall()}
        self.assertTrue({"item_class", "source", "updated_at"} <= cols)


if __name__ == "__main__":
    unittest.main()
