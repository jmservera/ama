import inspect
import json
import re
import tempfile
import unittest
from pathlib import Path

import dataset
import test_sqlstore as base
from zava_forward.core import chatthreads
from zava_forward.core import chat_privacy as cp
from zava_forward.core.chat_privacy import ChatNotApproved, ChatPrivacy
from zava_forward.core.chatthreads import ChatNotFound
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

U1, U2 = dataset.DATA["staff"]
TASK = "stock-prioritisation"

APPROVED = dict(CHAT_DPIA_REF="SYNTH-DPIA-1", CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1", CHAT_NOTICE_REF="SYNTH-NOTICE-1")


class ChatPrivacyBehaviour:
    """Shared behaviour over the #160 chat repository; subclasses supply make_store."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = self.make_store(self.tmp.name)

    def cp(self, **env):
        return ChatPrivacy(self.store, env=env)

    def test_data_map_covers_required_classes(self):
        ids = {r["id"] for r in cp.DATA_MAP}
        self.assertTrue({"message", "memory", "prompt", "diagnostic_log"} <= ids)
        self.assertFalse(cp.MODEL_PROVIDER_POSITION["zava_stores_prompts"])
        self.assertIn("uksouth", cp.MODEL_PROVIDER_POSITION["region"])

    def test_provider_position_is_documented_but_not_accepted(self):
        terms = cp.MODEL_PROVIDER_POSITION["documented_terms"]
        self.assertEqual(terms["status"], "vendor_documentation_not_dpo_accepted")
        self.assertTrue(terms["source"].startswith("https://learn.microsoft.com/"))
        self.assertTrue(terms["retrieved"])
        self.assertTrue(any("DPO and Legal" in i for i in cp.MODEL_PROVIDER_POSITION["open_items"]))
    def test_storage_refused_without_dpo_legal_references(self):
        c = self.cp(CHAT_DPIA_REF="SYNTH-DPIA-1")
        self.assertEqual(c.decision()["missing"], ["lawful_basis_ref", "notice_ref"])
        with self.assertRaises(ChatNotApproved):
            c.start_thread(U1, "ZF-1", TASK)
        with self.assertRaises(ChatNotApproved):
            c.add_memory(U1, "prefers short summaries", task=TASK)
        self.assertEqual(self.store.chat_list_threads(U1), [])

    def test_no_retention_period_before_approval(self):
        self.assertIsNone(self.cp(**APPROVED, CHAT_RETENTION_DAYS="30").decision()["retention_days"])
        self.assertEqual(self.cp(**APPROVED, CHAT_RETENTION_DAYS="30", CHAT_RETENTION_REF="SYNTH-RET-1").decision()["retention_days"], 30)

    def test_no_expiry_without_retention(self):
        c = self.cp(**APPROVED)
        c.opt_in(U1, True)
        c.add_memory(U1, "likes tables", task=TASK)
        self.assertIsNone(c.export(U1)["memory"][0]["expires_at"])
        self.assertEqual(c.purge_expired("9999"), 0)

    def test_rights_run_through_the_160_chat_repository(self):
        c = self.cp(**APPROVED)
        for u in (U1, U2):
            t = c.start_thread(u, "ZF-1", TASK)
            c.add_message(u, t, "user", f"hello from {u['name']}")
            c.opt_in(u, True)
            c.add_memory(u, f"note {u['email']}", task=TASK)
        self.assertEqual(len(self.store.chat_list_threads(U1)), 1)
        found = c.locate(U1)
        self.assertEqual((len(found["threads"]), found["messages"], len(found["memory"])), (1, 1, 1))
        self.assertEqual([m["content"] for m in c.export(U1)["messages"]], [f"hello from {U1['name']}"])
        self.assertEqual(c.erase(U1), dict(threads=1, messages=1, memory=1))
        self.assertEqual(c.locate(U1), dict(threads=[], messages=0, memory=[]))
        self.assertEqual(self.store.chat_list_threads(U1), [])
        self.assertEqual(c.locate(U2)["messages"], 1)
        self.assertEqual(len(c.export(U2)["memory"]), 1)

    def test_cannot_write_to_another_users_thread(self):
        c = self.cp(**APPROVED)
        t = c.start_thread(U1, "ZF-1", TASK)
        with self.assertRaises(ChatNotFound):
            c.add_message(U2, t, "user", "hi")

    def test_redaction_masks_identifiers_and_cues(self):
        text, kinds = cp.redact("Call 07700 900123 or a@example.test, AB 12 34 56 C, SW1A 1AA, resident has dementia")
        for leak in ("07700", "a@example.test", "AB 12", "SW1A", "dementia"):
            self.assertNotIn(leak, text)
        self.assertEqual(kinds, ["email", "ni_number", "phone", "postcode", "special_category"])

    def test_message_stored_redacted_and_memory_rejects_special_category(self):
        c = self.cp(**APPROVED)
        t = c.start_thread(U1, "ZF-1", TASK)
        c.opt_in(U1, True)
        self.assertEqual(c.add_message(U1, t, "user", "tenant has asthma"), ["special_category"])
        self.assertNotIn("asthma", c.export(U1)["messages"][0]["content"])
        with self.assertRaises(ValueError):
            c.add_memory(U1, "tenant has asthma", task=TASK)
        self.assertIn("special-category", cp.WARNING)

    def test_diagnostics_exclude_content(self):
        out = cp.diagnostic_safe(dict(thread_id="t", content="secret", prompt="p", memory="m", count=2))
        self.assertEqual(out, dict(thread_id="t", count=2))

    def test_expiry_set_and_purged_when_retention_approved(self):
        c = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="1")
        c.opt_in(U1, True)
        c.add_memory(U1, "likes tables", task=TASK)
        self.assertIsNotNone(c.export(U1)["memory"][0]["expires_at"])
        self.assertEqual(c.purge_expired("0000"), 0)
        self.assertEqual(c.purge_expired("9999"), 1)
        self.assertEqual(c.locate(U1)["memory"], [])


class MemoryStoreChatPrivacy(ChatPrivacyBehaviour, unittest.TestCase):
    def make_store(self, tmp):
        data = Path(tmp) / "zavaforward.json"
        data.write_text(json.dumps(dataset.DATA))
        return Store(str(data))


class SqlChatPrivacy(ChatPrivacyBehaviour, unittest.TestCase):
    def make_store(self, tmp):
        data, db = base.seed(tmp)
        return SqlStore(data, db)

    def test_memory_table_comes_from_the_store_dialect_hooks(self):
        import sqlite3
        raw = sqlite3.connect(self.store.db_path)
        tables = {r[0] for r in raw.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({"chat_thread", "chat_message", "chat_memory"} <= tables)
        self.assertNotIn("user_key", [r[1] for r in raw.execute("PRAGMA table_info(chat_thread)")])
        self.assertIn("owner", [r[1] for r in raw.execute("PRAGMA table_info(chat_memory)")])


class PortabilityTests(unittest.TestCase):
    BANNED = re.compile(r"(?i)\bINSERT\s+OR\b|\bREPLACE\s+INTO\b|\bAUTOINCREMENT\b|\bPRAGMA\b")

    def test_chat_privacy_has_no_own_sql_or_connection(self):
        src = inspect.getsource(cp)
        code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("*", "#")))
        self.assertEqual([l.strip() for l in code.splitlines() if self.BANNED.search(l)], [])
        for forbidden in ("sqlite3", "CREATE TABLE", "chat.sqlite", "executescript", "OBJECT_ID"):
            self.assertNotIn(forbidden, code)
        self.assertNotRegex(code, r"(?i)\b(SELECT|DELETE FROM|INSERT INTO|UPDATE)\b.*\bchat_")

    def test_memory_ddl_is_dialect_specific_and_shared_sql_portable(self):
        self.assertTrue(any("chat_memory" in d for d in chatthreads.SQLITE_DDL))
        self.assertTrue(any("chat_memory" in d for d in chatthreads.MSSQL_DDL))
        self.assertIn("chat_memory", chatthreads.TABLE_NAMES)
        src = Path(chatthreads.__file__).read_text()
        a, b = src.index("SQLITE_DDL = ("), src.index("MSSQL_DDL = (")
        shared = src[:a] + src[b:]
        self.assertEqual([l.strip() for l in shared.splitlines() if self.BANNED.search(l)], [])


if __name__ == "__main__":
    unittest.main()
