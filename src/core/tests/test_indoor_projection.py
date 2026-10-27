"""Exercise equations and provenance, not acceptance of historical climate."""
# mypy: disallow-untyped-calls=False

import math
import random
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.synthetic import indoor_projection as ip
from zava_forward.core.synthetic import provenance
from zava_forward.core.synthetic import sensor_backfill as sb


def legacy(
    sensor: dict[str, object], rng: random.Random, hour: int, t_out: float, rh_out: float
) -> tuple[float, float]:
    loss = (
        ip.DWELLINGS[str(sensor["dwelling_type"])]
        * ip.AGE_BANDS[str(sensor["age_band"])]
        * (0.75 if sensor["retrofitted"] else 1.0)
    )
    loss *= float(str(sensor.get("construction_loss", 1.0)))
    heated = {
        "all_day": 7 <= hour < 23,
        "morning_evening": 6 <= hour < 9 or 17 <= hour < 22,
        "low": 17 <= hour < 21,
    }[str(sensor["heating_pattern"])]
    setpoint = 20.5 if heated and t_out < 15 else 17.0
    base = setpoint + min(0.0, (t_out - 5) * 0.08 * loss) + max(0.0, (t_out - 16) * 0.35)
    t_in = max(8.0, base + rng.gauss(0, 0.3))

    def sat(t: float) -> float:
        return 6.112 * math.exp(17.62 * t / (243.12 + t))

    vapour = sat(t_out) * rh_out / 100 + (1.6 * loss if heated else 1.2 * loss)
    rh_in = max(15.0, min(98.0, 100 * vapour / sat(t_in) + rng.gauss(0, 1.5)))
    return t_in, rh_in


def sensor() -> dict[str, object]:
    return dict(
        dwelling_type="terrace",
        age_band="pre-1919",
        retrofitted=False,
        heating_pattern="morning_evening",
        construction_loss=1.15,
    )


class ProjectionTests(unittest.TestCase):
    def test_exact_legacy_equation_and_rng_state(self) -> None:
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
                                ip.project(s, a, at, t_out, 80), legacy(s, b, hour, t_out, 80)
                            )
                            self.assertEqual(a.getstate(), b.getstate())

    def test_supported_endpoints_and_exercise_output_bounds(self) -> None:
        at = datetime(2025, 1, 1, 18, tzinfo=UTC)
        for t in (-80.0, 60.0):
            for rh in (0.0, 100.0):
                result = ip.project(sensor(), random.Random(7), at, t, rh)
                self.assertTrue(all(math.isfinite(v) for v in result))
                self.assertGreaterEqual(result[0], 8.0)
                self.assertTrue(15 <= result[1] <= 98)
        poor = ip.project(sensor(), random.Random(7), at, 0, 80)
        better = ip.project({**sensor(), "construction_loss": 0.75}, random.Random(7), at, 0, 80)
        self.assertLess(poor[0], better[0])
        self.assertGreater(poor[1], better[1])

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
