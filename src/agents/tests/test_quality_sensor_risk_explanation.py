"""Synthetic fixtures for Quality damp and mould risk explanation; not resident evidence."""

from __future__ import annotations

import unittest

from zava_forward.agents.quality_sensor_risk import explain_inspection_risk, rank_homes

AS_OF = "2026-11-14T09:00:00+00:00"


def series(rh: float, n: int = 12) -> list[dict[str, object]]:
    return [
        dict(observed_at=f"2026-11-14T{h:02d}:00:00+00:00", relative_humidity=rh) for h in range(n)
    ]


class QualitySensorRiskExplanationTests(unittest.TestCase):
    def test_sensor_and_inspection_age_factors_ranked(self) -> None:
        out = explain_inspection_risk("h1", series(85), "2024-01-01T00:00:00+00:00", AS_OF)
        self.assertEqual(
            [f["factor"] for f in out["factors"]], ["sustained_high_humidity", "inspection_age"]
        )
        self.assertEqual([f["rank"] for f in out["factors"]], [1, 2])
        self.assertTrue(all(f["evidence"] for f in out["factors"]))

    def test_advisory_and_signoff_gate(self) -> None:
        out = explain_inspection_risk("h1", series(40), "2026-10-01T00:00:00+00:00", AS_OF)
        self.assertIs(out["advisory_only"], True)
        self.assertIs(out["requires_inspector_signoff"], True)
        self.assertEqual(out["signoff_state"], "pending_human_inspector")
        self.assertEqual(out["factors"], [])

    def test_missing_telemetry_never_lowers_priority(self) -> None:
        old = "2024-01-01T00:00:00+00:00"
        missing = explain_inspection_risk("h1", None, old, AS_OF)
        stale = explain_inspection_risk("h2", series(90, 3), old, AS_OF)
        self.assertEqual(missing["telemetry_status"], "insufficient")
        self.assertEqual(stale["telemetry_status"], "insufficient")
        self.assertEqual([f["factor"] for f in missing["factors"]], ["inspection_age"])
        quiet = explain_inspection_risk("h3", series(40), old, AS_OF)
        self.assertGreaterEqual(missing["total_score"], quiet["total_score"])

    def test_stale_and_invalid_readings_ignored(self) -> None:
        bad = [
            dict(observed_at="nope", relative_humidity=99),
            dict(observed_at=AS_OF, relative_humidity=True),
        ]
        out = explain_inspection_risk("h1", bad, None, AS_OF)
        self.assertEqual(out["telemetry_status"], "insufficient")
        self.assertEqual(out["factors"][0]["evidence"], "no valid previous inspection recorded")
        with self.assertRaises(ValueError):
            explain_inspection_risk("h1", None, None, "2026-11-14")

    def test_rank_homes_and_determinism(self) -> None:
        a = explain_inspection_risk("a", series(85), "2024-01-01T00:00:00+00:00", AS_OF)
        b = explain_inspection_risk("b", None, "2026-10-01T00:00:00+00:00", AS_OF)
        self.assertEqual([e["home_id"] for e in rank_homes([b, a])], ["a", "b"])
        self.assertEqual(
            a, explain_inspection_risk("a", series(85), "2024-01-01T00:00:00+00:00", AS_OF)
        )


if __name__ == "__main__":
    unittest.main()
