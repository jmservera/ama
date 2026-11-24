import threading
import unittest
from datetime import UTC, datetime
from typing import Any

from zava_forward.core import demo_hazard_clock_seed as seed
from zava_forward.core import taskqueues

NOW = datetime(2026, 11, 24, 12, 0, tzinfo=UTC)


class FakeStore:
    def __init__(self, cases: dict[str, Any]) -> None:
        self.cases, self.lock = cases, threading.RLock()
        self.audits: list[tuple[str, str, str, str]] = []
        self.saves = 0

    def _case(self, case_id: str) -> Any:
        return self.cases[case_id]

    def audit(self, who: str, action: str, case_id: str, detail: str) -> None:
        self.audits.append((who, action, case_id, detail))

    def save(self) -> None:
        self.saves += 1


def make_store() -> FakeStore:
    return FakeStore(
        {
            "C1": dict(hazards=[dict(owner="Ann"), dict(owner="Ben", released=True)]),
            "C2": dict(hazards=[dict(owner="Cy", aware_at="2026-11-20T09:00+00:00")]),
            "C3": dict(hazards=[dict(owner="Di", responded_at="2026-11-21T09:00+00:00")]),
            "C4": dict(),
        }
    )


class DemoHazardClockSeed(unittest.TestCase):
    def test_inspect_writes_nothing(self) -> None:
        store = make_store()
        report = seed.run(store, apply=False, now=NOW)
        self.assertEqual(report["hazards_to_write"], 1)
        self.assertFalse(report["applied"])
        self.assertNotIn("aware_at", store.cases["C1"]["hazards"][0])
        self.assertEqual(store.saves, 0)

    def test_apply_shows_running_clock_and_is_idempotent(self) -> None:
        store = make_store()
        self.assertTrue(seed.run(store, apply=True, now=NOW)["applied"])
        hazard = store.cases["C1"]["hazards"][0]
        text = taskqueues.hazard_clock(dict(hazard), NOW)["clock_text"]
        self.assertIn("6 hours elapsed", text)
        self.assertIn("service response due", text)
        self.assertNotIn("unknown", text.lower().replace("response unknown", ""))
        self.assertEqual(store.cases["C2"]["hazards"][0]["aware_at"], "2026-11-20T09:00+00:00")
        again = seed.run(store, apply=True, now=NOW)
        self.assertEqual(again["hazards_to_write"], 0)
        self.assertEqual(store.saves, 1)

    def test_revert_restores_exactly(self) -> None:
        store = make_store()
        seed.run(store, apply=True, now=NOW)
        self.assertEqual(seed.revert(store)["hazards_reverted"], 1)
        self.assertEqual(store.cases["C1"]["hazards"][0], dict(owner="Ann"))


if __name__ == "__main__":
    unittest.main()
