"""Issue 1288: stale, offline and uncalibrated telemetry gets a text badge and advisory text."""

import importlib.util
import unittest
from pathlib import Path

API = Path(__file__).resolve().parents[1] / "src/zava_forward/api"
_spec = importlib.util.spec_from_file_location("sensor_badges", API / "sensor_badges.py")
sensor_badges = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sensor_badges)
OPS = API / "web/ops.js"
SERVER = API / "server.py"
ADVISORY = "Advisory telemetry \u2014 officer review required"


class BadgeModel(unittest.TestCase):
    def kinds(self, **view: object) -> dict[str, dict[str, str]]:
        return {b["kind"]: b for b in sensor_badges.badges(view)}

    def test_each_state_has_a_plain_text_label(self) -> None:
        cases = [
            (dict(state="ok", latest={"x": 1}, freshness="fresh"), "fresh", "Fresh"),
            (dict(state="ok", latest={"x": 1}, freshness="stale"), "stale", "Stale"),
            (
                dict(state="ok", latest={"x": 1}, freshness="unknown"),
                "unknown",
                "Freshness unknown",
            ),
            (dict(state="no-readings", latest=None, freshness="unknown"), "offline", "Offline"),
            (dict(state="unavailable", latest=None), "unavailable", "Unavailable"),
        ]
        for view, state, label in cases:
            with self.subTest(state=state):
                badge = self.kinds(**view)["freshness"]
                self.assertEqual((badge["state"], badge["label"]), (state, label))
                self.assertTrue(badge["text"].endswith("."))
                self.assertEqual(self.kinds(**view)["calibration"]["label"], "Uncalibrated")


class Annotate(unittest.TestCase):
    def test_response_keeps_fields_and_adds_advisory_and_badges(self) -> None:
        stale = dict(state="ok", latest={"reading_id": "R-1"}, freshness="stale")
        out = sensor_badges.annotate(stale)
        self.assertEqual(out["latest"], stale["latest"])
        self.assertEqual(out["advisory"], ADVISORY)
        self.assertEqual([b["state"] for b in out["badges"]], ["stale", "uncalibrated"])
        self.assertNotIn("advisory", stale)

    def test_withheld_or_empty_is_never_fresh(self) -> None:
        for view in (dict(state="consent-withheld", latest=None), dict(state="no-readings")):
            self.assertNotEqual(sensor_badges.annotate(view)["badges"][0]["state"], "fresh")

    def test_endpoint_annotates_the_sensor_response(self) -> None:
        src = SERVER.read_text(encoding="utf-8")
        self.assertIn("sensor_badges.annotate(app.assistants.sensors(", src)


class UiSource(unittest.TestCase):
    def test_panel_renders_text_badges_without_new_invalid_state(self) -> None:
        src = OPS.read_text(encoding="utf-8")
        start = src.index("function sensorPanel")
        panel = src[start : src.index("function simulationPanel")]
        self.assertIn("data-sensor-badges", panel)
        self.assertIn("data-sensor-advisory", panel)
        self.assertIn("${b.label}:", panel)
        self.assertIn(ADVISORY.replace("\u2014", "\\u2014"), panel)
        self.assertNotIn("aria-invalid", panel)


if __name__ == "__main__":
    unittest.main()
