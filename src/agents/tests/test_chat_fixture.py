import re
import tempfile
import unittest
from pathlib import Path

import chat_fixture as cf
from zava_forward.core.synthetic import scale_fixture

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


class ChatFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = cf.build()

    def test_same_seed_is_byte_identical_and_other_seed_differs(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            ma, mb, mc = cf.write(a), cf.write(b), cf.write(c, seed=1)
            self.assertEqual(ma, mb)
            self.assertNotEqual(ma["sha256"], mc["sha256"])
            self.assertEqual(Path(a, "threads.jsonl").read_bytes(), Path(b, "threads.jsonl").read_bytes())

    def test_personas_cover_eleven_perspectives_with_known_app_roles(self):
        people = self.d["personas"]
        self.assertEqual(len({p["persona_id"] for p in people}), 11)
        self.assertEqual(len(people), 11 * cf.USERS_PER_PERSPECTIVE)
        self.assertEqual(len({p["user_key"] for p in people}), len(people))
        for p in people:
            self.assertIn(p["app_role"], cf.ROLE_NAMES)
            self.assertTrue(p["is_synthetic"])
        contractor = next(p for p in people if p["persona_id"] == "provider-contractor")
        self.assertEqual(contractor["eligible_tasks"], [])

    def test_cases_resolve_to_the_60000_home_stock(self):
        self.assertEqual(scale_fixture.HOMES, 60000)
        for t in self.d["threads"]:
            self.assertRegex(t["case_id"], r"^ZF-\d{5}$")
            self.assertLess(int(t["case_id"][3:]), scale_fixture.HOMES)

    def test_threads_include_expiry_and_deletion_with_content_removed(self):
        states = {t["state"] for t in self.d["threads"]}
        self.assertTrue({"active", "expired", "deleted_by_owner"} <= states)
        turns = {}
        for x in self.d["turns"]:
            turns.setdefault(x["thread_id"], []).append(x)
        for t in self.d["threads"]:
            gone = t["state"] != "active"
            self.assertEqual(t["content_present"], not gone)
            for x in turns[t["thread_id"]]:
                self.assertEqual(x["user_text"] is None and x["assistant_text"] is None, gone)
                self.assertEqual(x["user_key"], t["user_key"])
        for e in self.d["ledger_events"]:
            self.assertIsNone(e["content"])
        deleted = {t["thread_id"] for t in self.d["threads"] if t["state"] != "active"}
        self.assertTrue(deleted <= {e["thread_id"] for e in self.d["ledger_events"] if e["event"] != "thread_created"})

    def test_expiry_is_consistent_with_as_of_date(self):
        for t in self.d["threads"]:
            if t["state"] == "active":
                self.assertGreaterEqual(t["expires"], cf.AS_OF.isoformat())
        for m in self.d["memory_items"]:
            if m["state"] == "expired":
                self.assertLess(m["expires"], cf.AS_OF.isoformat())
            if m["state"] in ("active", "edited"):
                self.assertGreaterEqual(m["expires"], cf.AS_OF.isoformat())

    def test_memory_is_opt_in_with_expiry_and_no_excluded_categories(self):
        states = {s["memory_state"]: s for s in self.d["memory_state"]}
        self.assertEqual(set(states), {"not_opted_in", "opted_in", "withdrawn"})
        opted_out = {s["user_key"] for s in self.d["memory_state"] if s["memory_state"] == "not_opted_in"}
        withdrawn = {s["user_key"] for s in self.d["memory_state"] if s["memory_state"] == "withdrawn"}
        for m in self.d["memory_items"]:
            self.assertNotIn(m["user_key"], opted_out)
            self.assertIn(m["category"], cf.MEMORY_CATEGORIES)
            self.assertTrue(m["expires"] and m["source"])
            if m["user_key"] in withdrawn:
                self.assertEqual((m["state"], m["text"]), ("deleted", None))
        self.assertEqual({p["category"] for p in self.d["exclusion_probes"]}, set(cf.EXCLUDED_CATEGORIES))
        for p in self.d["exclusion_probes"]:
            self.assertEqual(p["expected"], "rejected_not_stored")

    def test_isolation_cases_cover_every_perspective_and_kind(self):
        cases = self.d["isolation_cases"]
        self.assertEqual({c["kind"] for c in cases}, {
            "same_role_cross_user", "owner_access", "cross_role", "spoofed_user_key",
            "role_revoked_mid_thread", "administrator_access"})
        keys = {p["user_key"]: p for p in self.d["personas"]}
        covered = {keys[c["owner"]]["persona_id"] for c in cases if c["kind"] == "same_role_cross_user"}
        self.assertEqual(len(covered), 11)
        for c in cases:
            if c["kind"] in ("same_role_cross_user", "spoofed_user_key", "cross_role"):
                self.assertNotEqual(c["actor"], c["owner"])
                self.assertEqual(c["expected"], "deny")
        admin = [c["expected"] for c in cases if c["kind"] == "administrator_access"]
        self.assertTrue({"deny", "allow_time_limited_audited"} <= set(admin))
        self.assertEqual(len({c["case_id"] for c in cases}), len(cases))

    def test_deletion_cases_keep_only_ledger_metadata(self):
        cases = self.d["deletion_cases"]
        self.assertTrue({c["resource"] for c in cases} == {"thread", "memory"})
        for c in cases:
            self.assertEqual((c["expected_content"], c["expected_ledger"]), ("absent", "metadata_only"))

    def test_every_row_is_labelled_synthetic_and_pii_free(self):
        for name, rows in self.d.items():
            for r in rows:
                self.assertTrue(r["is_synthetic"], name)
                self.assertFalse(EMAIL.search(str(r)), name)
        for x in self.d["turns"]:
            for text in (x["user_text"], x["assistant_text"]):
                if text:
                    self.assertTrue(text.startswith("[SYNTHETIC"))


if __name__ == "__main__":
    unittest.main()
