import unittest
from datetime import date

from zava_forward.core import discovery_flow as f

D = date


class PopulationTests(unittest.TestCase):
    def test_summary_keeps_non_progressing_and_flags_limits(self) -> None:
        rows = [
            f.Candidate("P1", D(2026, 1, 5)),
            f.Candidate("P2", D(2026, 2, 1), excluded_reason="not social stock"),
            f.Candidate("P2", D(2026, 3, 1), outcome_known=False),
            f.Candidate("P3", D(2025, 12, 31)),
            f.Candidate("P4", D(2027, 1, 1)),
        ]
        s = f.baseline_summary(rows, D(2026, 1, 1), D(2026, 12, 31))
        self.assertEqual(s["candidates"], 3)
        self.assertEqual(s["before_window"], 1)
        self.assertEqual(s["after_window"], 1)
        self.assertEqual(s["excluded"], {"not social stock": 1})
        self.assertEqual(s["open_outcome_unknown"], 1)
        self.assertEqual(s["duplicate_ids"], ["P2"])
        self.assertIn("Not a company finding", str(s["notice"]))

    def test_bad_window_rejected(self) -> None:
        with self.assertRaises(ValueError):
            f.baseline_summary([], D(2026, 2, 1), D(2026, 1, 1))


class LegTests(unittest.TestCase):
    def test_legs_and_missing_or_out_of_order(self) -> None:
        ev = [
            f.LifecycleEvent("P1", "installation", D(2026, 1, 1)),
            f.LifecycleEvent("P1", "physical acceptance", D(2026, 1, 11)),
            f.LifecycleEvent("P1", "evidence acceptance", D(2026, 1, 5)),
        ]
        legs = f.leg_days(ev, "P1")
        self.assertEqual(legs["installation to physical acceptance"], 10)
        self.assertIsNone(legs["physical acceptance to evidence acceptance"])
        self.assertIsNone(legs["evidence acceptance to resident handover"])
        self.assertTrue(all(v is None for v in f.leg_days(ev, "P9").values()))


class WaitTests(unittest.TestCase):
    def test_by_party_orders_and_never_infers_cause(self) -> None:
        waits = [
            f.Wait("P1", "Supplier A", D(2026, 1, 1), D(2026, 1, 11), "capacity"),
            f.Wait("P2", "Supplier A", D(2026, 2, 1), None),
            f.Wait("P3", "", D(2026, 1, 1), D(2026, 1, 4), f.DISPUTED),
        ]
        rows = f.waits_by_party(waits, D(2026, 2, 11))
        self.assertEqual([r["party"] for r in rows], ["Supplier A", f.UNATTRIBUTED])
        self.assertEqual(rows[0]["days"], 20)
        self.assertEqual(rows[0]["open_waits"], 1)
        self.assertEqual(rows[0]["unknown_or_disputed_cause"], 1)
        self.assertEqual(rows[1]["unknown_or_disputed_cause"], 1)

    def test_negative_wait_rejected(self) -> None:
        with self.assertRaises(ValueError):
            f.wait_days(f.Wait("P1", "A", D(2026, 2, 1), D(2026, 1, 1)), D(2026, 3, 1))


class LoopTests(unittest.TestCase):
    def test_counts_per_property(self) -> None:
        loops = [f.Loop("P1", "return", D(2026, 1, 1)), f.Loop("P1", "return", D(2026, 1, 2))]
        self.assertEqual(f.loop_counts(loops)["P1"]["return"], 2)
        self.assertEqual(f.loop_counts(loops)["P1"]["reopen"], 0)
        with self.assertRaises(ValueError):
            f.loop_counts([f.Loop("P1", "other", D(2026, 1, 1))])


if __name__ == "__main__":
    unittest.main()
