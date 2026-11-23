import importlib.util
import threading
import unittest
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "seed_demo_hazard_clock", ROOT / "infra/scripts/seed_demo_hazard_clock.py"
)
SEED = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SEED)

NOW = datetime(2026, 11, 22, 12, 0, tzinfo=UTC)


class FakeStore:
    def __init__(self, cases, as_of=None):
        self.cases, self.lock, self.as_of = cases, threading.RLock(), as_of
        self.touched, self.audits, self.saves = [], [], 0

    def _case(self, case_id):
        self.touched.append(case_id)
        return self.cases[case_id]

    def audit(self, who, action, case_id, detail):
        self.audits.append((who, action, case_id, detail))

    def save(self):
        self.saves += 1


def hazard(**fields):
    base = {
        "category": "Damp and mould",
        "priority": "Routine",
        "noticed": "2026-10-01",
        "released": False,
    }
    return {**base, **fields}


class SeedDemoHazardClock(unittest.TestCase):
    def store(self):
        return FakeStore(
            {
                "C1": {"hazards": [hazard()]},
                "C2": {"hazards": [hazard(aware_at="2026-10-02T08:00:00Z")]},
                "C3": {"hazards": [hazard(released=True), hazard(category="Safeguarding")]},
                "C4": {"hazards": [hazard(noticed="2027-01-01"), hazard(noticed="")]},
                "C5": {"hazards": [hazard(recorded_at="2026-11-01T10:30:00+00:00")]},
            }
        )

    def test_inspect_writes_nothing_and_counts_by_reason(self):
        store = self.store()
        report = SEED.run(store, apply=False, now=NOW)
        self.assertEqual(report["hazards_to_write"], 2)
        self.assertEqual(
            report["skipped"],
            {
                "already_has_aware_at": 1,
                "released_or_invalid": 1,
                "safeguarding": 1,
                "no_usable_anchor": 2,
            },
        )
        self.assertFalse(report["applied"])
        self.assertEqual((store.touched, store.audits, store.saves), ([], [], 0))
        self.assertNotIn("aware_at", store.cases["C1"]["hazards"][0])

    def test_apply_uses_the_record_time_and_never_overwrites(self):
        store = self.store()
        report = SEED.run(store, apply=True, now=NOW)
        self.assertTrue(report["applied"])
        self.assertEqual(report["projected"], {"overdue": 2})
        first = store.cases["C1"]["hazards"][0]
        self.assertEqual(first["aware_at"], "2026-10-01T09:00:00Z")
        self.assertEqual(first["noticed"], "2026-10-01")
        self.assertTrue(first[SEED.MARK]["synthetic"])
        self.assertEqual(store.cases["C5"]["hazards"][0]["aware_at"], "2026-11-01T10:30:00Z")
        self.assertEqual(store.cases["C2"]["hazards"][0]["aware_at"], "2026-10-02T08:00:00Z")
        self.assertEqual(first["response_due_at"], "2026-10-15T09:00:00Z")
        self.assertNotIn("responded_at", first)
        self.assertEqual((store.saves, len(store.audits)), (1, 1))
        self.assertEqual(store.audits[0][1], SEED.ACTION)
        again = SEED.run(store, apply=True, now=NOW)
        self.assertEqual((again["hazards_to_write"], again["applied"], store.saves), (0, False, 1))

    def test_running_subset_is_marked_and_keeps_the_original_date(self):
        store = FakeStore(
            {f"C{i}": {"hazards": [hazard(priority="Significant")]} for i in range(6)}
        )
        report = SEED.run(store, apply=True, running=2, now=NOW)
        self.assertEqual(report["projected"], {"running": 2, "overdue": 4})
        running = [
            h for c in store.cases.values() for h in c["hazards"] if h["noticed"] != "2026-10-01"
        ]
        self.assertEqual(len(running), 2)
        for item in running:
            self.assertEqual(item[SEED.MARK]["noticed_was"], "2026-10-01")
            self.assertEqual(item["aware_at"], "2026-11-19T16:00:00Z")
            self.assertEqual(item["noticed"], "2026-11-19")

    def test_reference_time_is_the_dataset_snapshot_and_revert_restores(self):
        cases = {f"C{i}": {"hazards": [hazard(priority="Emergency")]} for i in range(2)}
        cases["C9"] = {"hazards": [hazard(noticed="2026-10-20")]}
        store = FakeStore(cases, as_of="2026-10-16")
        report = SEED.run(store, apply=True, running=1, now=None)
        self.assertEqual(report["hazards_to_write"], 2)
        self.assertEqual(report["skipped"], {"no_usable_anchor": 1})
        self.assertEqual(cases["C0"]["hazards"][0]["aware_at"], "2026-10-15T14:00:00Z")
        self.assertEqual(SEED.revert(store), {"hazards_reverted": 2, "applied": True})
        for case_id in ("C0", "C1"):
            self.assertEqual(cases[case_id]["hazards"][0], hazard(priority="Emergency"))
        self.assertEqual(SEED.revert(store)["applied"], False)

    def test_revert_removes_a_noticed_date_the_seeder_invented(self):
        original = hazard(priority="Significant", recorded_at="2026-10-01T09:00:00Z")
        del original["noticed"]
        store = FakeStore({"C0": {"hazards": [dict(original)]}})
        SEED.run(store, apply=True, running=1, now=NOW)
        self.assertIn("noticed", store.cases["C0"]["hazards"][0])
        SEED.revert(store)
        self.assertEqual(store.cases["C0"]["hazards"][0], original)


if __name__ == "__main__":
    unittest.main()
