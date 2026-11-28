import inspect
import json
import re
import tempfile
import unittest
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

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


if TYPE_CHECKING:
    _TestCase = unittest.TestCase
else:
    _TestCase = object


class ChatPrivacyBehaviour(_TestCase):
    """Shared behaviour over the #160 chat repository; subclasses supply make_store."""

    store: Any
    make_store: Callable[[str], Any]

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = self.make_store(self.tmp.name)

    def cp(self, **env: str) -> ChatPrivacy:
        return ChatPrivacy(self.store, env=env)

    def test_data_map_covers_required_classes(self) -> None:
        ids = {r["id"] for r in cp.DATA_MAP}
        self.assertTrue({"message", "memory", "prompt", "diagnostic_log"} <= ids)
        self.assertFalse(cp.MODEL_PROVIDER_POSITION["zava_stores_prompts"])
        self.assertIn("uksouth", cp.MODEL_PROVIDER_POSITION["region"])

    def test_provider_position_is_documented_but_not_accepted(self) -> None:
        terms = cp.MODEL_PROVIDER_POSITION["documented_terms"]
        self.assertEqual(terms["status"], "vendor_documentation_not_dpo_accepted")
        self.assertEqual(terms["source"], "https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy")
        self.assertRegex(terms["retrieved"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertTrue(any("DPO and Legal" in i for i in cp.MODEL_PROVIDER_POSITION["open_items"]))

    def test_storage_refused_without_dpo_legal_references(self) -> None:
        c = self.cp(CHAT_DPIA_REF="SYNTH-DPIA-1")
        self.assertEqual(c.decision()["missing"], ["lawful_basis_ref", "notice_ref"])
        with self.assertRaises(ChatNotApproved):
            c.start_thread(U1, "ZF-1", TASK)
        with self.assertRaises(ChatNotApproved):
            c.add_memory(U1, "prefers short summaries", task=TASK)
        self.assertEqual(self.store.chat_list_threads(U1), [])

    def test_no_retention_period_before_approval(self) -> None:
        self.assertIsNone(self.cp(CHAT_RETENTION_DAYS="30", CHAT_RETENTION_REF="SYNTH-RET-1").decision()["retention_days"])
        self.assertIsNone(self.cp(**APPROVED, CHAT_RETENTION_DAYS="30").decision()["retention_days"])
        self.assertEqual(self.cp(**APPROVED, CHAT_RETENTION_DAYS="30", CHAT_RETENTION_REF="SYNTH-RET-1").decision()["retention_days"], 30)

    def test_storage_refused_when_provider_or_region_unapproved(self) -> None:
        c = self.cp(**APPROVED, CHAT_PROVIDER_REGION="eastus")
        self.assertFalse(c.decision()["approved"])
        with self.assertRaises(ChatNotApproved):
            c.start_thread(U1, "ZF-1", TASK)
        for bad_days in ("\u00b2", "\u0663\u0660", "36501", "9" * 5000):
            d = self.cp(
                **APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS=bad_days
            ).decision()
            self.assertIsNone(d["retention_days"])
        actual = self.cp(
            ZF_DATA_PROCESSING="actual",
            CHAT_DPIA_REF="DPIA-2026-99",
            CHAT_LAWFUL_BASIS_REF="LB-2026-99",
            CHAT_NOTICE_REF="NOTICE-2026-99",
            CHAT_RETENTION_REF="RET-2026-99",
            CHAT_RETENTION_DAYS="30",
        )
        self.assertFalse(actual.decision()["approved"])
        self.assertTrue(actual.decision()["actual_mode_unapproved"])
        self.assertIsNone(actual.decision()["retention_days"])
        with self.assertRaises(ChatNotApproved):
            actual.start_thread(U1, "ZF-1", TASK)

    def test_thread_cannot_be_bound_to_a_case_the_role_cannot_see(self) -> None:
        c = self.cp(**APPROVED)
        outsider = {"email": "outsider@example.test", "name": "Outsider", "role": "Contractor", "contractor": "Not The Contractor Ltd"}
        for hidden in ("ZF-1", "ZF-NO-SUCH-CASE"):
            with self.assertRaises(ChatNotFound):
                c.start_thread(outsider, hidden, TASK)
        self.assertEqual(self.store.chat_list_threads(outsider), [])
        self.assertTrue(c.start_thread(U1, "ZF-1", TASK))

    def test_no_expiry_without_retention(self) -> None:
        c = self.cp(**APPROVED)
        c.opt_in(U1, True)
        c.add_memory(U1, "likes tables", task=TASK)
        self.assertIsNone(c.export(U1)["memory"][0]["expires_at"])
        self.assertEqual(c.purge_expired("9999"), 0)
        seeded = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="1")
        seeded.add_memory(U1, "expiring note", task=TASK)
        self.assertEqual(len(c.export(U1)["memory"]), 2)
        invalid_provider = self.cp(**APPROVED, CHAT_PROVIDER_REGION="eastus")
        self.assertFalse(invalid_provider.memory_status(U1, TASK)["active"])
        self.assertEqual(invalid_provider.prompt_memory(U1, TASK), [])
        self.assertEqual(invalid_provider.purge_expired("0000-01-01T00:00:00+00:00"), 0)
        self.assertEqual(invalid_provider.purge_expired("9999-01-01T00:00:00+00:00"), 1)
        remaining = c.export(U1)["memory"]
        self.assertEqual(len(remaining), 1)
        self.assertIsNone(remaining[0]["expires_at"])
        self.assertEqual(remaining[0]["content"], "likes tables")
        seeded.add_memory(U1, "second expiring note", task=TASK)
        actual_hold = self.cp(
            ZF_DATA_PROCESSING="actual",
            CHAT_DPIA_REF="DPIA-2026-99",
            CHAT_LAWFUL_BASIS_REF="LB-2026-99",
            CHAT_NOTICE_REF="NOTICE-2026-99",
            CHAT_RETENTION_REF="RET-2026-99",
            CHAT_RETENTION_DAYS="1",
            CHAT_PROVIDER_REGION="uksouth",
            CHAT_DEPLOYMENT_TYPE="Standard",
        )
        self.assertFalse(actual_hold.memory_status(U1, TASK)["active"])
        self.assertEqual(actual_hold.prompt_memory(U1, TASK), [])
        self.assertEqual(actual_hold.purge_expired("9999-01-01T00:00:00+00:00"), 1)
        self.assertEqual([m["content"] for m in c.export(U1)["memory"]], ["likes tables"])

    def test_rights_run_through_the_160_chat_repository(self) -> None:
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

    def test_cannot_write_to_another_users_thread(self) -> None:
        c = self.cp(**APPROVED)
        t = c.start_thread(U1, "ZF-1", TASK)
        with self.assertRaises(ChatNotFound):
            c.add_message(U2, t, "user", "hi")

    def test_redaction_masks_identifiers_and_cues(self) -> None:
        text, kinds = cp.redact("Call 07700 900123 or a@example.test, AB 12 34 56 C, SW1A 1AA, resident has dementia")
        for leak in ("07700", "a@example.test", "AB 12", "SW1A", "dementia"):
            self.assertNotIn(leak, text)
        self.assertEqual(kinds, ["email", "ni_number", "phone", "postcode", "special_category"])

    def test_message_stored_redacted_and_memory_rejects_special_category(self) -> None:
        c = self.cp(**APPROVED)
        t = c.start_thread(U1, "ZF-1", TASK)
        c.opt_in(U1, True)
        self.assertEqual(c.add_message(U1, t, "user", "tenant has asthma"), ["special_category"])
        self.assertNotIn("asthma", c.export(U1)["messages"][0]["content"])
        with self.assertRaises(ValueError):
            c.add_memory(U1, "tenant has asthma", task=TASK)
        self.assertIn("special-category", cp.WARNING)

    def test_redaction_leaves_benign_text_and_masks_every_occurrence(self) -> None:
        self.assertEqual(cp.redact("Order 12 radiators for the Maple block"), ("Order 12 radiators for the Maple block", []))
        text, kinds = cp.redact("a@example.test and b@example.test, +44 7700 900123, ab 12 34 56 c")
        for leak in ("a@example.test", "b@example.test", "7700", "ab 12"):
            self.assertNotIn(leak, text)
        self.assertEqual(text.count("[email removed]"), 2)
        self.assertEqual(kinds, ["email", "ni_number", "phone"])
        self.assertEqual(cp.redact(text), (text, []))

    def test_diagnostic_allowlist_names_no_content_field(self) -> None:
        for name in ("content", "prompt", "memory", "message", "text", "reply"):
            self.assertNotIn(name, cp.DIAGNOSTIC_FIELDS)
        noisy = dict(thread_id="t", status="ok", message="m", text="x", reply="r", email="a@example.test")
        self.assertEqual(cp.diagnostic_safe(noisy), dict(thread_id="t", status="ok"))

    def test_erase_is_idempotent_and_leaves_other_users_export_untouched(self) -> None:
        c = self.cp(**APPROVED)
        self.assertEqual(c.erase(U1), dict(threads=0, messages=0, memory=0))
        for u in (U1, U2):
            c.add_message(u, c.start_thread(u, "ZF-1", TASK), "user", f"from {u['name']}")
        self.assertEqual(c.erase(U1)["messages"], 1)
        self.assertEqual(c.erase(U1), dict(threads=0, messages=0, memory=0))
        self.assertEqual([m["content"] for m in c.export(U2)["messages"]], [f"from {U2['name']}"])
        self.assertEqual(c.export(U1), dict(messages=[], memory=[]))

    def test_memory_is_stored_masked_and_edit_applies_the_same_checks(self) -> None:
        c = self.cp(**APPROVED)
        c.opt_in(U1, True)
        mid = c.add_memory(U1, "reach me on a@example.test", task=TASK)
        self.assertNotIn("a@example.test", c.list_memory(U1)[0]["content"])
        c.edit_memory(U1, mid, "call 07700 900123")
        stored = c.list_memory(U1)[0]["content"]
        self.assertNotIn("07700", stored)
        self.assertIn("[phone removed]", stored)
        with self.assertRaises(ValueError):
            c.edit_memory(U1, mid, "tenant has asthma")
        self.assertEqual(c.list_memory(U1)[0]["content"], stored)

    def test_other_user_cannot_edit_or_delete_memory_item(self) -> None:
        c = self.cp(**APPROVED)
        for u in (U1, U2):
            c.opt_in(u, True)
        mid = c.add_memory(U1, "table layout", task=TASK)
        with self.assertRaises(LookupError):
            c.edit_memory(U2, mid, "overwritten")
        with self.assertRaises(LookupError):
            c.delete_memory(U2, mid)
        self.assertEqual([m["content"] for m in c.list_memory(U1)], ["table layout"])

    def test_edit_does_not_extend_expiry(self) -> None:
        c = self.cp(**APPROVED, CHAT_RETENTION_DAYS="30", CHAT_RETENTION_REF="SYNTH-RET-1")
        c.opt_in(U1, True)
        mid = c.add_memory(U1, "first", task=TASK)
        before = c.list_memory(U1)[0]["expires_at"]
        self.assertIsNotNone(before)
        c.edit_memory(U1, mid, "second")
        item = c.list_memory(U1)[0]
        self.assertEqual((item["content"], item["expires_at"]), ("second", before))

    def test_locate_returns_ids_and_counts_not_content(self) -> None:
        c = self.cp(**APPROVED)
        c.opt_in(U1, True)
        c.add_message(U1, c.start_thread(U1, "ZF-1", TASK), "user", "distinctive-marker-text")
        c.add_memory(U1, "distinctive-memory-text", task=TASK)
        found = c.locate(U1)
        self.assertEqual(set(found), {"threads", "messages", "memory"})
        self.assertNotIn("distinctive", json.dumps(found))

    def test_diagnostics_exclude_content(self) -> None:
        out = cp.diagnostic_safe(dict(thread_id="t", content="secret", prompt="p", memory="m", count=2))
        self.assertEqual(out, dict(thread_id="t", count=2))

    def test_expiry_set_and_purged_when_retention_approved(self) -> None:
        c = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="1")
        c.opt_in(U1, True)
        c.add_memory(U1, "likes tables", task=TASK)
        self.assertIsNotNone(c.export(U1)["memory"][0]["expires_at"])
        self.assertEqual(c.purge_expired("0000"), 0)
        self.assertEqual(c.purge_expired("9999"), 1)
        self.assertEqual(c.locate(U1)["memory"], [])

    def test_retention_purge_does_nothing_without_a_recorded_period(self) -> None:
        c = self.cp(**APPROVED)
        c.add_message(U1, c.start_thread(U1, "ZF-1", TASK), "user", "synthetic question")
        self.assertEqual(c.purge_retention("9999-01-01T00:00:00+00:00"), dict(threads=0, messages=0, memory=0, applied=False))
        self.assertEqual(len(c.locate(U1)["threads"]), 1)

    def test_retention_purge_is_age_based_and_ignores_later_activity(self) -> None:
        c = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="30")
        old = c.start_thread(U1, "ZF-1", TASK)
        c.add_message(U1, old, "user", "synthetic question")
        c.add_message(U1, old, "assistant", "synthetic answer")
        c.start_thread(U2, "ZF-2", TASK)
        self.assertEqual(c.purge_retention(), dict(threads=0, messages=0, memory=0, applied=True))
        later = (datetime.now(timezone.utc) + timedelta(days=31)).isoformat(timespec="milliseconds")
        keep = c.start_thread(U1, "ZF-3", TASK)
        with c.store.chat_repo.txn():
            c.store.chat_repo.update(old, cp.user_key(U1), 3, updated_at=(datetime.now(timezone.utc) + timedelta(days=40)).isoformat(timespec="milliseconds"))
            c.store.chat_repo.update(keep, cp.user_key(U1), 1, created_at=(datetime.now(timezone.utc) + timedelta(days=40)).isoformat(timespec="milliseconds"))
            c.store.chat_repo.commit()
        result = c.purge_retention(later)
        self.assertEqual((result["threads"], result["messages"]), (2, 2))
        self.assertEqual(c.locate(U1)["threads"], [keep])
        self.assertEqual(c.locate(U2)["threads"], [])


    def _age_thread(self, c: ChatPrivacy, tid: str, owner: dict[str, Any], days: int) -> None:
        old = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="milliseconds")
        with c.store.chat_repo.txn():
            c.store.chat_repo.update(tid, cp.user_key(owner), 1, created_at=old)
            c.store.chat_repo.commit()

    def test_sweep_enforces_the_period_and_is_throttled(self) -> None:
        c = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="30")
        stale = c.start_thread(U1, "ZF-1", TASK)
        self._age_thread(c, stale, U1, 31)
        self.assertEqual(c.sweep_retention()["threads"], 1)
        self.assertEqual(c.locate(U1)["threads"], [])
        stale = c.start_thread(U1, "ZF-1", TASK)
        self._age_thread(c, stale, U1, 31)
        self.assertIsNone(c.sweep_retention())
        self.assertEqual(c.locate(U1)["threads"], [stale])
        self.assertEqual(c.sweep_retention(interval=0)["threads"], 1)

    def test_sweep_keeps_everything_without_a_recorded_period(self) -> None:
        c = self.cp(**APPROVED)
        tid = c.start_thread(U1, "ZF-1", TASK)
        self._age_thread(c, tid, U1, 400)
        self.assertFalse(c.sweep_retention()["applied"])
        self.assertEqual(c.locate(U1)["threads"], [tid])

    def test_expired_memory_does_not_count_toward_the_limit(self) -> None:
        c = self.cp(**APPROVED, CHAT_RETENTION_REF="SYNTH-RET-1", CHAT_RETENTION_DAYS="30")
        c.opt_in(U1, True)
        ids = [c.add_memory(U1, f"synthetic preference {i}", task=TASK) for i in range(cp.MEMORY_LIMIT)]
        with self.assertRaises(ValueError):
            c.add_memory(U1, "one too many", task=TASK)
        self.store.chat_repo.update_memory(cp.user_key(U1), ids[0], expires_at="2000-01-01T00:00:00.000+00:00")
        self.assertEqual(len(c.list_memory(U1)), cp.MEMORY_LIMIT - 1)
        c.add_memory(U1, "fits once one is expired", task=TASK)
        self.assertEqual(len(c.list_memory(U1)), cp.MEMORY_LIMIT)


class MemoryStoreChatPrivacy(ChatPrivacyBehaviour, unittest.TestCase):
    def make_store(self, tmp: str) -> Any:
        data = Path(tmp) / "zavaforward.json"
        data.write_text(json.dumps(dataset.DATA))
        return Store(str(data))


class SqlChatPrivacy(ChatPrivacyBehaviour, unittest.TestCase):
    def make_store(self, tmp: str) -> Any:
        data, db = base.seed(tmp)
        return SqlStore(data, db)

    def test_memory_table_comes_from_the_store_dialect_hooks(self) -> None:
        import sqlite3
        raw = sqlite3.connect(self.store.db_path)
        tables = {r[0] for r in raw.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({"chat_thread", "chat_message", "chat_memory"} <= tables)
        self.assertNotIn("user_key", [r[1] for r in raw.execute("PRAGMA table_info(chat_thread)")])
        self.assertIn("owner", [r[1] for r in raw.execute("PRAGMA table_info(chat_memory)")])


class PortabilityTests(unittest.TestCase):
    BANNED = re.compile(r"(?i)\bINSERT\s+OR\b|\bREPLACE\s+INTO\b|\bAUTOINCREMENT\b|\bPRAGMA\b")

    def test_chat_privacy_has_no_own_sql_or_connection(self) -> None:
        src = inspect.getsource(cp)
        code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("*", "#")))
        self.assertEqual([l.strip() for l in code.splitlines() if self.BANNED.search(l)], [])
        for forbidden in ("sqlite3", "CREATE TABLE", "chat.sqlite", "executescript", "OBJECT_ID"):
            self.assertNotIn(forbidden, code)
        self.assertNotRegex(code, r"(?i)\b(SELECT|DELETE FROM|INSERT INTO|UPDATE)\b.*\bchat_")

    def test_memory_ddl_is_dialect_specific_and_shared_sql_portable(self) -> None:
        self.assertTrue(any("chat_memory" in d for d in chatthreads.SQLITE_DDL))
        self.assertTrue(any("chat_memory" in d for d in chatthreads.MSSQL_DDL))
        self.assertIn("chat_memory", chatthreads.TABLE_NAMES)
        src = Path(chatthreads.__file__).read_text()
        a, b = src.index("SQLITE_DDL = ("), src.index("MSSQL_DDL = (")
        shared = src[:a] + src[b:]
        self.assertEqual([l.strip() for l in shared.splitlines() if self.BANNED.search(l)], [])


if __name__ == "__main__":
    unittest.main()
