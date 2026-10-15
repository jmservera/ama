"""Plausibility and statistical range tests for the synthetic sensor backfill (#191).

All expected ranges are labelled EXERCISE values: the Met Office / Environment Agency climate source
(#178) has not been retrieved, so nothing here is a verified climate figure. Replace OUTDOOR_EXERCISE
when #178 records a source. Data is wholly synthetic (ADR 0005).
"""
import collections
import statistics
import unittest

from zava_forward.core.synthetic import scale_fixture
from zava_forward.core.synthetic import sensor_backfill as sb

DAYS, CADENCE, HOMES = 730, 360, 150
# Exercise values for a North East England-style outdoor climate (labelled, not retrieved data).
OUTDOOR_EXERCISE = dict(temp_c=(-8.0, 30.0), annual_mean_c=(8.0, 12.0), summer_minus_winter_c=(6.0, 16.0),
                        rh_pct=(35.0, 100.0))
INDOOR_HEALTHY_C = (8.0, 35.0)
FLATLINE_RUN = 12
RATE_TOLERANCE = dict(dropout=(0.01, 0.03), outlier=(0.002, 0.007))


def out_of_bounds(values, lo, hi):
    return [v for v in values if not lo <= v <= hi]


def longest_flatline(values):
    best = run = 1
    for a, b in zip(values, values[1:]):
        run = run + 1 if a == b else 1
        best = max(best, run)
    return best if values else 0


def _build():
    outdoor = sb.outdoor_series(days=DAYS, cadence=CADENCE)
    sensors = [sb.sensor_for(h) for h in scale_fixture.homes(HOMES, scale_fixture.SEED)]
    series = {s["sensor_id"]: list(sb.readings(s, days=DAYS, cadence=CADENCE, outdoor=outdoor)) for s in sensors}
    return outdoor, sensors, series


class Fixture:
    outdoor, sensors, series = _build()


class CheckerTests(unittest.TestCase):
    def test_checkers_fail_on_bad_series(self):
        self.assertEqual(out_of_bounds([20.0, 60.0, -30.0], -10, 45), [60.0, -30.0])
        self.assertGreaterEqual(longest_flatline([19.0] * FLATLINE_RUN + [20.0]), FLATLINE_RUN)
        self.assertLess(longest_flatline([19.0, 19.1, 19.0, 19.1]), FLATLINE_RUN)


class BoundsTests(unittest.TestCase):
    def test_outdoor_series_inside_exercise_bounds_with_seasons_and_diurnal_cycle(self):
        temps = [t for t, _ in Fixture.outdoor]
        rhs = [r for _, r in Fixture.outdoor]
        self.assertEqual(out_of_bounds(temps, *OUTDOOR_EXERCISE["temp_c"]), [])
        self.assertEqual(out_of_bounds(rhs, *OUTDOOR_EXERCISE["rh_pct"]), [])
        self.assertTrue(OUTDOOR_EXERCISE["annual_mean_c"][0] <= statistics.mean(temps) <= OUTDOOR_EXERCISE["annual_mean_c"][1])
        month, hour = collections.defaultdict(list), collections.defaultdict(list)
        for k, (t, _) in enumerate(Fixture.outdoor):
            ts = sb.START + sb.timedelta(minutes=k * CADENCE)
            month[ts.month].append(t)
            hour[ts.hour].append(t)
        swing = statistics.mean(month[7]) - statistics.mean(month[1])
        self.assertTrue(OUTDOOR_EXERCISE["summer_minus_winter_c"][0] <= swing <= OUTDOOR_EXERCISE["summer_minus_winter_c"][1], swing)
        self.assertGreater(statistics.mean(hour[18]), statistics.mean(hour[6]) + 2)

    def test_indoor_series_inside_physical_bounds_and_only_injected_outliers_escape(self):
        for sid, rows in Fixture.series.items():
            for r in rows:
                t, h = float(r["temperature_c"]), float(r["humidity_pct"])
                self.assertTrue(0.0 <= h <= 100.0, (sid, h))
                self.assertTrue(sb.BOUNDS["temperature_c"][0] <= t <= sb.BOUNDS["temperature_c"][1] or r["injected_fault"] == "OUTLIER", (sid, t))
                if r["injected_fault"] != "OUTLIER":
                    self.assertTrue(INDOOR_HEALTHY_C[0] <= t <= INDOOR_HEALTHY_C[1], (sid, t))

    def test_no_flat_line_outside_injected_stuck_faults(self):
        stuck_seen = False
        for s in Fixture.sensors:
            rows = Fixture.series[s["sensor_id"]]
            temps = [r["temperature_c"] for r in rows if r["injected_fault"] != "STUCK"]
            self.assertLess(longest_flatline(temps), FLATLINE_RUN, s["sensor_id"])
            stuck = [r["temperature_c"] for r in rows if r["injected_fault"] == "STUCK"]
            if stuck:
                stuck_seen = True
                self.assertEqual(s["fault_profile"], "stuck")
                self.assertGreaterEqual(longest_flatline(stuck), FLATLINE_RUN)
        self.assertTrue(stuck_seen)


class StructureTests(unittest.TestCase):
    def test_indoor_diurnal_structure_for_all_day_heating_in_winter(self):
        by_hour = collections.defaultdict(list)
        for s in Fixture.sensors:
            if s["heating_pattern"] != "all_day" or s["fault_profile"] != "none":
                continue
            for r in Fixture.series[s["sensor_id"]]:
                hour, month = int(r["observed_at"][11:13]), int(r["observed_at"][5:7])
                if month in (12, 1, 2):
                    by_hour[hour].append(float(r["temperature_c"]))
        self.assertGreater(statistics.mean(by_hour[12]), statistics.mean(by_hour[0]) + 1)

    def test_humidity_follows_dwelling_and_age_band_expectations(self):
        def mean_rh(key, value):
            vals = [statistics.mean(float(r["humidity_pct"]) for r in Fixture.series[s["sensor_id"]])
                    for s in Fixture.sensors if s["fault_profile"] == "none" and not s["retrofitted"] and s[key] == value]
            self.assertTrue(vals, value)
            return statistics.mean(vals)

        self.assertGreater(mean_rh("age_band", "pre-1919"), mean_rh("age_band", "2003+") + 1.0)
        self.assertGreater(mean_rh("dwelling_type", "detached"), mean_rh("dwelling_type", "apartments"))


class InjectionRateTests(unittest.TestCase):
    def test_profile_mix_matches_configured_weights(self):
        sensors = [sb.sensor_for(h) for h in scale_fixture.homes(3000, scale_fixture.SEED)]
        share = {p: n / len(sensors) for p, n in collections.Counter(s["fault_profile"] for s in sensors).items()}
        for profile, expected in dict(none=0.70, outlier=0.12, stuck=0.06, dropout=0.12).items():
            self.assertAlmostEqual(share[profile], expected, delta=0.03, msg=profile)

    def test_missing_and_fault_rates_match_injection(self):
        steps = len(Fixture.outdoor)
        tally = collections.defaultdict(lambda: [0, 0, 0])
        for s in Fixture.sensors:
            rows = Fixture.series[s["sensor_id"]]
            t = tally[s["fault_profile"]]
            t[0] += steps
            t[1] += steps - len(rows)
            t[2] += sum(1 for r in rows if r["injected_fault"] == "OUTLIER")
            allowed = {"none": "", "outlier": "OUTLIER", "stuck": "STUCK", "dropout": ""}[s["fault_profile"]]
            self.assertTrue(all(r["injected_fault"] in ("", allowed) for r in rows), s["sensor_id"])
        for profile in ("none", "outlier", "stuck"):
            self.assertEqual(tally[profile][1], 0, profile)
        self.assertEqual(tally["none"][2], 0)
        lo, hi = RATE_TOLERANCE["dropout"]
        self.assertTrue(lo <= tally["dropout"][1] / tally["dropout"][0] <= hi)
        lo, hi = RATE_TOLERANCE["outlier"]
        self.assertTrue(lo <= tally["outlier"][2] / tally["outlier"][0] <= hi)


if __name__ == "__main__":
    unittest.main()
