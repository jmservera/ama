import os
import tempfile
import unittest

from zavaforward_mvp import chat_privacy as cp
from zavaforward_mvp.chat_privacy import ChatNotApproved, ChatPrivacy

APPROVED = dict(CHAT_DPIA_REF="SYNTH-DPIA-1", CHAT_LAWFUL_BASIS_REF="SYNTH-LB-1", CHAT_NOTICE_REF="SYNTH-NOTICE-1")


class ChatPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "chat.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def cp(self, **env):
        return ChatPrivacy(env=env, db_path=self.db)

    def test_data_map_covers_required_classes(self):
        ids = {r["id"] for r in cp.DATA_MAP}
        self.assertTrue({"message", "memory", "prompt", "diagnostic_log"} <= ids)
        self.assertFalse(cp.MODEL_PROVIDER_POSITION["zava_stores_prompts"])
        self.assertIn("uksouth", cp.MODEL_PROVIDER_POSITION["region"])

    def test_storage_refused_without_dpo_legal_references(self):
        c = self.cp(CHAT_DPIA_REF="SYNTH-DPIA-1")
        self.assertEqual(c.decision()["missing"], ["lawful_basis_ref", "notice_ref"])
        with self.assertRaises(ChatNotApproved):
            c.start_thread("u1", "Officer", "C1", "summarise")
        with self.assertRaises(ChatNotApproved):
            c.add_memory("u1", "Officer", "prefers short summaries")

    def test_no_retention_period_before_approval(self):
        self.assertIsNone(self.cp(**APPROVED, CHAT_RETENTION_DAYS="30").decision()["retention_days"])
        self.assertEqual(self.cp(**APPROVED, CHAT_RETENTION_DAYS="30", CHAT_RETENTION_REF="SYNTH-RET-1").decision()["retention_days"], 30)

    def test_no_expiry_without_retention(self):
        c = self.cp(**APPROVED)
        c.add_memory("u1", "Officer", "likes tables")
        self.assertEqual(c.export("u1")["memory"][0]["expires_at"], None)
        self.assertEqual(c.purge_expired(), 0)

    def test_rights_locate_export_erase_only_own_data(self):
        c = self.cp(**APPROVED)
        for u in ("u1", "u2"):
            t = c.start_thread(u, "Officer", "C1", "summarise")
            c.add_message(u, t, "user", f"hello from {u}")
            c.add_memory(u, "Officer", f"note {u}")
        found = c.locate("u1")
        self.assertEqual((len(found["threads"]), found["messages"], len(found["memory"])), (1, 1, 1))
        self.assertEqual([m["content"] for m in c.export("u1")["messages"]], ["hello from u1"])
        self.assertEqual(c.erase("u1"), dict(threads=1, messages=1, memory=1))
        self.assertEqual(c.locate("u1"), dict(threads=[], messages=0, memory=[]))
        self.assertEqual(c.locate("u2")["messages"], 1)

    def test_cannot_write_to_another_users_thread(self):
        c = self.cp(**APPROVED)
        t = c.start_thread("u1", "Officer", "C1", "summarise")
        with self.assertRaises(PermissionError):
            c.add_message("u2", t, "user", "hi")

    def test_redaction_masks_identifiers_and_cues(self):
        text, kinds = cp.redact("Call 07700 900123 or a@example.test, AB 12 34 56 C, SW1A 1AA, resident has dementia")
        for leak in ("07700", "a@example.test", "AB 12", "SW1A", "dementia"):
            self.assertNotIn(leak, text)
        self.assertEqual(kinds, ["email", "ni_number", "phone", "postcode", "special_category"])

    def test_message_stored_redacted_and_memory_rejects_special_category(self):
        c = self.cp(**APPROVED)
        t = c.start_thread("u1", "Officer", "C1", "summarise")
        self.assertEqual(c.add_message("u1", t, "user", "tenant has asthma"), ["special_category"])
        self.assertNotIn("asthma", c.export("u1")["messages"][0]["content"])
        with self.assertRaises(ValueError):
            c.add_memory("u1", "Officer", "tenant has asthma")
        self.assertIn("special-category", cp.WARNING)

    def test_diagnostics_exclude_content(self):
        out = cp.diagnostic_safe(dict(thread_id="t", content="secret", prompt="p", memory="m", count=2))
        self.assertEqual(out, dict(thread_id="t", count=2))

    def test_expiry_set_and_purged_when_retention_approved(self):
        c = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="1")
        c.add_memory("u1", "Officer", "likes tables")
        self.assertIsNotNone(c.export("u1")["memory"][0]["expires_at"])
        with c._conn() as db:
            db.execute("UPDATE chat_memory SET expires_at='2000-01-01T00:00:00'")
        self.assertEqual(c.purge_expired(), 1)

    def test_portable_sql(self):
        import inspect
        src = inspect.getsource(cp).upper()
        for banned in ("INSERT OR", "AUTOINCREMENT", "PRAGMA"):
            self.assertNotIn(banned, src.replace('"INSERT OR", "AUTOINCREMENT", "PRAGMA"', ""))


if __name__ == "__main__":
    unittest.main()
