import copy
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
            self.assertEqual({p.name for p in Path(a).iterdir()},
                             {f"{name}.jsonl" for name in self.d} | {"manifest.json"})
            for path in Path(a).iterdir():
                self.assertEqual(path.read_bytes(), Path(b, path.name).read_bytes(), path.name)

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
            "role_revoked_mid_thread", "administrator_access", "contractor_access_denied"})
        keys = {p["user_key"]: p for p in self.d["personas"]}
        covered = {keys[c["owner"]]["persona_id"] for c in cases
                   if c["kind"] == "same_role_cross_user" and c["resource"] == "memory"}
        self.assertEqual(len(covered), 11)
        for c in cases:
            if c["kind"] in ("same_role_cross_user", "spoofed_user_key", "cross_role"):
                self.assertNotEqual(c["actor"], c["owner"])
                self.assertEqual(c["expected"], "deny")
        admin = [c["expected"] for c in cases if c["kind"] == "administrator_access"]
        self.assertTrue({"deny", "allow_time_limited_audited"} <= set(admin))
        self.assertEqual(len({c["case_id"] for c in cases}), len(cases))

    def test_thread_isolation_covers_exactly_the_eligible_owners(self):
        people = {p["user_key"]: p for p in self.d["personas"]}
        eligible = {key for key, p in people.items() if p["eligible_tasks"]}
        threads = {t["thread_id"]: t for t in self.d["threads"]}
        self.assertTrue(eligible)
        self.assertEqual({t["user_key"] for t in threads.values()}, eligible)
        cases = [c for c in self.d["isolation_cases"]
                 if c["kind"] == "same_role_cross_user" and c["resource"] == "thread"]
        expected = {(owner, action) for owner in eligible for action in ("read", "list", "search")}
        self.assertEqual({(c["owner"], c["action"]) for c in cases}, expected)
        self.assertEqual(len(cases), len(expected))
        for c in cases:
            self.assertIn(c["resource_id"], threads)
            self.assertEqual(threads[c["resource_id"]]["user_key"], c["owner"])
            self.assertNotEqual(c["actor"], c["owner"])
            self.assertEqual(people[c["actor"]]["role"], people[c["owner"]]["role"])
            self.assertIn(threads[c["resource_id"]]["task"], people[c["owner"]]["eligible_tasks"])
            self.assertEqual(c["expected"], "deny")

    def assert_contractor_denials(self, cases, people, threads):
        by_key = {p["user_key"]: p for p in people}
        by_thread = {t["thread_id"]: t for t in threads}
        contractors = {key for key, p in by_key.items() if p["app_role"] == "ZavaForward.Contractor"}
        self.assertEqual(len(contractors), cf.USERS_PER_PERSPECTIVE)
        for key in contractors:
            self.assertEqual(by_key[key]["eligible_tasks"], [])
        self.assertFalse(contractors & {t["user_key"] for t in threads})
        probes = [c for c in cases if c["kind"] == "contractor_access_denied"]
        expected = {(key, action) for key in contractors for action in ("read", "list", "search")}
        self.assertEqual({(c["actor"], c["action"]) for c in probes}, expected)
        self.assertEqual(len(probes), len(expected))
        for c in probes:
            self.assertEqual((c["resource"], c["expected"], c["is_synthetic"]), ("thread", "deny", True))
            self.assertNotEqual(c["actor"], c["owner"])
            self.assertIn(c["owner"], by_key)
            self.assertNotIn(c["owner"], contractors)
            self.assertIn(c["resource_id"], by_thread)
            target = by_thread[c["resource_id"]]
            self.assertEqual(target["user_key"], c["owner"])
            self.assertEqual(target["state"], "active")
            self.assertTrue(target["content_present"])
            self.assertIn(target["task"], by_key[c["owner"]]["eligible_tasks"])

    def test_contractors_have_explicit_denials_against_eligible_owner_threads(self):
        for seed in (cf.SEED, 0, 1, 999):
            with self.subTest(seed=seed):
                data = cf.build(seed)
                self.assert_contractor_denials(data["isolation_cases"], data["personas"], data["threads"])

    def test_contractor_coverage_rejects_missing_or_invalid_probes(self):
        cases = self.d["isolation_cases"]
        probes = [c for c in cases if c["kind"] == "contractor_access_denied"]
        self.assert_contractor_denials(cases, self.d["personas"], self.d["threads"])
        for probe in probes:
            with self.subTest(actor=probe["actor"], action=probe["action"], mutation="removed"):
                remaining = [c for c in cases if c["case_id"] != probe["case_id"]]
                with self.assertRaises(AssertionError):
                    self.assert_contractor_denials(remaining, self.d["personas"], self.d["threads"])
        probe = probes[0]
        alternate_owner = next(t for t in self.d["threads"]
                               if t["user_key"] != probe["owner"] and t["state"] == "active")
        inactive = next(t for t in self.d["threads"] if t["state"] != "active")
        for fields in (
            {"owner": probe["actor"]},
            {"resource_id": "THR-SYN-MISSING"},
            {"resource_id": alternate_owner["thread_id"]},
            {"owner": inactive["user_key"], "resource_id": inactive["thread_id"]},
            {"expected": "allow"},
            {"resource": "memory"},
        ):
            with self.subTest(mutation=fields):
                mutated = copy.deepcopy(cases)
                next(c for c in mutated if c["case_id"] == probe["case_id"]).update(fields)
                with self.assertRaises(AssertionError):
                    self.assert_contractor_denials(mutated, self.d["personas"], self.d["threads"])

    def test_contractor_denials_require_a_legitimate_active_target(self):
        for threads in (
            [],
            [dict(t, state="expired", content_present=False) for t in self.d["threads"]],
            [dict(t, task="unregistered-task") for t in self.d["threads"]],
        ):
            with self.subTest(thread_count=len(threads)):
                with self.assertRaisesRegex(ValueError, "active eligible staff-owned thread"):
                    cf.isolation_cases(self.d["personas"], threads, self.d["memory_items"])

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
