"""Outdoor-record-derived exercise envelopes, not calibrated building physics."""
# mypy: disallow-untyped-calls=False

import math
import random
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from test_climate_history import META_SHA, METADATA, RAW, RAW_SHA
from zava_forward.core.synthetic import household_conditions as hc
from zava_forward.core.synthetic import indoor_projection as ip
from zava_forward.core.synthetic import provenance
from zava_forward.core.synthetic import retrofit_effects as re
from zava_forward.core.synthetic import sensor_backfill as sb
from zava_forward.core.synthetic.climate_history import ClimateHistory


def sat(temperature: float) -> float:
    return 6.112 * math.exp(17.62 * temperature / (243.12 + temperature))


def model(
    sensor: dict[str, object],
    at: datetime,
    t_out: float,
    rh_out: float,
    household: hc.Condition | None = None,
    multiplier: float = 1.0,
) -> tuple[float, float]:
    loss = ip.DWELLINGS[str(sensor["dwelling_type"])] * ip.AGE_BANDS[str(sensor["age_band"])]
    if household is None:
        loss *= 0.75 if sensor["retrofitted"] else 1.0
        loss *= float(str(sensor.get("construction_loss", 1.0)))
        heated = {
            "all_day": 7 <= at.hour < 23,
            "morning_evening": 6 <= at.hour < 9 or 17 <= at.hour < 22,
            "low": 17 <= at.hour < 21,
        }[str(sensor["heating_pattern"])]
        setpoint = 20.5 if heated and t_out < 15 else 17.0
        moisture = (1.6 if heated else 1.2) * loss
    else:
        loss *= float(str(sensor.get("construction_loss", 1.0)))
        loss *= multiplier
        setpoint = household.setpoint_c
        moisture = household.moisture_increment_hpa * loss / household.ventilation_multiplier
    base = setpoint + min(0.0, (t_out - 5) * 0.08 * loss) + max(0.0, (t_out - 16) * 0.35)
    return base, sat(t_out) * rh_out / 100 + moisture


def reference(base: float, vapour: float, rng: random.Random) -> tuple[float, float]:
    temperature = base + max(-3 * 0.3, min(3 * 0.3, rng.gauss(0, 0.3)))
    humidity = max(
        0.0, min(100.0, 100 * vapour / sat(temperature) + max(-4.5, min(4.5, rng.gauss(0, 1.5))))
    )
    return temperature, humidity


def envelope(base: float, vapour: float) -> tuple[tuple[float, float], tuple[float, float]]:
    return (base - 0.9, base + 0.9), (
        max(0.0, min(100.0, 100 * vapour / sat(base + 0.9) - 4.5)),
        max(0.0, min(100.0, 100 * vapour / sat(base - 0.9) + 4.5)),
    )


def sensor() -> dict[str, object]:
    return dict(
        home_id="ZF-1",
        sensor_id="SYNTHETIC-1",
        fault_profile="none",
        dwelling_type="terrace",
        age_band="pre-1919",
        retrofitted=False,
        heating_pattern="morning_evening",
        construction_loss=1.15,
    )


class ProjectionTests(unittest.TestCase):
    def assert_envelope(
        self, result: tuple[float, float], base: float, vapour: float, tolerance: float = 0.0
    ) -> None:
        for value, (low, high) in zip(result, envelope(base, vapour), strict=True):
            self.assertTrue(math.isfinite(value))
            self.assertGreaterEqual(value, low - tolerance - 1e-12)
            self.assertLessEqual(value, high + tolerance + 1e-12)

    def test_exact_equation_and_rng_state(self) -> None:
        for dwelling in ip.DWELLINGS:
            for age in ip.AGE_BANDS:
                for pattern in ("all_day", "morning_evening", "low"):
                    for hour in (0, 6, 9, 17, 22):
                        for t_out in (-20.0, 0.0, 15.0, 30.0):
                            s = {
                                **sensor(),
                                "dwelling_type": dwelling,
                                "age_band": age,
                                "heating_pattern": pattern,
                            }
                            a, b = random.Random(7), random.Random(7)
                            at = datetime(2025, 1, 1, hour, tzinfo=UTC)
                            self.assertEqual(
                                ip.project(s, a, at, t_out, 80),
                                reference(*model(s, at, t_out, 80), b),
                            )
                            self.assertEqual(a.getstate(), b.getstate())

    def test_supported_endpoints_and_derived_output_bounds(self) -> None:
        at = datetime(2025, 1, 1, 18, tzinfo=UTC)
        for dwelling in ip.DWELLINGS:
            for age in ip.AGE_BANDS:
                for construction in sorted(ip.CONSTRUCTION_FACTORS):
                    for retrofitted in (False, True):
                        s = {
                            **sensor(),
                            "dwelling_type": dwelling,
                            "age_band": age,
                            "construction_loss": construction,
                            "retrofitted": retrofitted,
                        }
                        for t in (-80.0, 60.0):
                            for rh in (0.0, 100.0):
                                result = ip.project(s, random.Random(7), at, t, rh)
                                self.assert_envelope(result, *model(s, at, t, rh))

    def test_composed_exact_equation_and_rng_state(self) -> None:
        s = sensor()
        at = datetime(2025, 1, 1, 18, tzinfo=UTC)
        for ventilation in (0.8, 1.2):
            for multiplier in (0.1, 0.85, 1.0):
                for setpoint in (16.0, 20.0, 22.0):
                    condition = hc.Condition("ZF-1", at, True, setpoint, ventilation, 1.7)
                    for t, rh in ((-80.0, 0.0), (2.0, 70.0), (60.0, 100.0)):
                        a, b = random.Random(21), random.Random(21)
                        actual = ip.project_composed(s, a, at, t, rh, condition, multiplier)
                        inputs = model(s, at, t, rh, condition, multiplier)
                        self.assertEqual(actual, reference(*inputs, b))
                        self.assertEqual(a.getstate(), b.getstate())
                        self.assert_envelope(actual, *inputs)

    def test_forced_noise_tails_and_saturation_keep_exactly_two_draws(self) -> None:
        s = sensor()
        at = datetime(2025, 1, 1, 18, tzinfo=UTC)
        condition = hc.Condition("ZF-1", at, True, 20.0, 0.8, 1.7)
        for composed in (False, True):
            for t, rh in ((-80.0, 0.0), (2.0, 70.0), (60.0, 100.0)):
                for noise in ((0.1, 0.5), (-1e6, 1e6), (1e6, -1e6)):
                    rng = random.Random(7)
                    with patch.object(rng, "gauss", side_effect=noise) as gauss:
                        if composed:
                            result = ip.project_composed(s, rng, at, t, rh, condition, 0.85)
                        else:
                            result = ip.project(s, rng, at, t, rh)
                    self.assertEqual(
                        [call.args for call in gauss.call_args_list], [(0, 0.3), (0, 1.5)]
                    )
                    inputs = model(s, at, t, rh, condition if composed else None, 0.85)
                    reference_rng = random.Random(7)
                    with patch.object(reference_rng, "gauss", side_effect=noise):
                        self.assertEqual(result, reference(*inputs, reference_rng))
                    self.assert_envelope(result, *inputs)

    def test_composed_domain_extremes_remain_in_derived_envelopes(self) -> None:
        at = datetime(2025, 1, 1, tzinfo=UTC)
        s = {
            **sensor(),
            "dwelling_type": "detached",
            "construction_loss": 1.2,
        }
        for setpoint in (16.0, 22.0):
            for moisture in (0.0, 2.4):
                for ventilation in (0.8, 1.2):
                    for multiplier in (0.001, 1.0):
                        condition = hc.Condition("ZF-1", at, True, setpoint, ventilation, moisture)
                        for t in (-80.0, 60.0):
                            for rh in (0.0, 100.0):
                                result = ip.project_composed(
                                    s, random.Random(7), at, t, rh, condition, multiplier
                                )
                                self.assert_envelope(
                                    result, *model(s, at, t, rh, condition, multiplier)
                                )

    def test_bounds_change_with_weather_and_each_dwelling_factor(self) -> None:
        s = sensor()
        at = datetime(2025, 1, 1, 18, tzinfo=UTC)
        baseline = envelope(*model(s, at, 0, 80))
        for key, value in (
            ("dwelling_type", "apartments"),
            ("age_band", "2003+"),
            ("construction_loss", 0.75),
            ("retrofitted", True),
            ("heating_pattern", "low"),
        ):
            other_at = at.replace(hour=7) if key == "heating_pattern" else at
            with self.subTest(key=key):
                self.assertNotEqual(
                    envelope(*model(s, other_at, 0, 80)),
                    envelope(*model({**s, key: value}, other_at, 0, 80)),
                )
        self.assertNotEqual(baseline, envelope(*model(s, at, -10, 80)))
        self.assertNotEqual(baseline[1], envelope(*model(s, at, 0, 20))[1])
        poor = ip.project(s, random.Random(7), at, 0, 80)
        better = ip.project({**s, "construction_loss": 0.75}, random.Random(7), at, 0, 80)
        self.assertLess(poor[0], better[0])
        self.assertGreater(poor[1], better[1])

    def test_old_exercise_floor_and_clips_are_not_output_bounds(self) -> None:
        at = datetime(2025, 1, 1, 0, tzinfo=UTC)
        s = {
            **sensor(),
            "dwelling_type": "detached",
            "construction_loss": 1.2,
        }
        cold = ip.project(s, random.Random(7), at, -80, 0)
        dry = ip.project(sensor(), random.Random(7), at, 30, 0)
        saturated = ip.project(sensor(), random.Random(7), at, 60, 100)
        self.assertLess(cold[0], 8)
        self.assertLess(dry[1], 15)
        self.assertEqual(saturated[1], 100)

    def test_full_pinned_outdoor_record_bounds_both_generator_paths(self) -> None:
        history = ClimateHistory.read(
            RAW, METADATA, expected_sha256=RAW_SHA, expected_metadata_sha256=META_SHA
        )
        outdoor = history.series(history.start, 731, 60)
        original = list(outdoor)
        self.assertEqual(len(outdoor), 17544)
        timestamps = [history.start + timedelta(hours=k) for k in range(len(outdoor))]
        conditions = hc.conditions("ZF-1", 183, "granted", timestamps, is_synthetic=True)
        completed = history.start + timedelta(days=365)
        measure = re.Measure("M1", "ZF-1", "Cavity wall", completed, True)
        for dwelling in ("apartments", "detached"):
            s = {**sensor(), "dwelling_type": dwelling}
            for composed in (False, True):
                kwargs = dict(
                    seed=183,
                    days=731,
                    cadence=60,
                    outdoor=outdoor,
                    start=history.start,
                    composed=composed,
                    measures=(measure,),
                )
                rows = list(sb.readings(s, **kwargs))
                self.assertEqual(len(rows), len(outdoor))
                self.assertEqual(rows, list(sb.readings(s, **kwargs)))
                for k, row in enumerate(rows):
                    condition = conditions[k] if composed else None
                    multiplier = 0.85 if composed and timestamps[k] >= completed else 1.0
                    inputs = model(s, timestamps[k], *outdoor[k], condition, multiplier)
                    result = float(row["temperature_c"]), float(row["humidity_pct"])
                    self.assert_envelope(result, *inputs, tolerance=0.005)
                    self.assertEqual(row["source_type"], "SYNTHETIC")
                    self.assertEqual(row["injected_fault"], "")
                    self.assertEqual(
                        row["observed_at"], timestamps[k].strftime("%Y-%m-%dT%H:%M:%SZ")
                    )
        self.assertEqual(outdoor, original)

    def test_invalid_inputs_are_explicit_domain_errors(self) -> None:
        at = datetime(2025, 1, 1, tzinfo=UTC)
        for t in (-243.12, -80.001, 60.001, math.nan, math.inf, -math.inf):
            with self.subTest(t=t), self.assertRaises(ValueError):
                ip.project(sensor(), random.Random(1), at, t, 80)
        for rh in (-0.001, 100.001, math.nan, math.inf):
            with self.subTest(rh=rh), self.assertRaises(ValueError):
                ip.project(sensor(), random.Random(1), at, 10, rh)
        for key, value in (
            ("dwelling_type", "unknown"),
            ("age_band", "unknown"),
            ("heating_pattern", "unknown"),
            ("retrofitted", "true"),
            ("construction_loss", 0.8),
            ("construction_loss", math.nan),
            ("construction_loss", True),
        ):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                ip.project({**sensor(), key: value}, random.Random(1), at, 10, 80)
        with self.assertRaises(ValueError):
            ip.project(sensor(), random.Random(1), at.replace(tzinfo=None), 10, 80)

    def test_fingerprint_inclusion_sensitivity_and_manifest_binding(self) -> None:
        sources = sb.revision_sources()
        module = Path(ip.__file__)
        self.assertIn(module, sources)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            changed = root / module.name
            changed.write_bytes(module.read_bytes() + b"\n")
            replaced = tuple(changed if p == module else p for p in sources)
            self.assertNotEqual(
                provenance.source_revision(sources), provenance.source_revision(replaced)
            )
            manifest = sb.write(root / "output", homes=1, days=1, cadence=360)
            self.assertEqual(manifest["generator_revision"], provenance.source_revision(sources))
            parameters = manifest["parameters"]
            assert isinstance(parameters, dict)
            self.assertEqual(parameters["indoor_projection"], ip.PARAMETERS)
        for parameters in (ip.PARAMETERS, ip.COMPOSED_PARAMETERS):
            self.assertTrue(str(parameters["version"]).endswith("-v2"))
            self.assertIn("exercise", str(parameters["classification"]).lower())
            self.assertEqual(parameters["noise"], ip.NOISE_PARAMETERS)
            self.assertEqual(parameters["output_bounds"], ip.OUTPUT_BOUNDS)
