"""Issue 1288: stale, offline and uncalibrated telemetry gets a text badge and advisory text."""

import unittest
from pathlib import Path
from typing import Any

from zava_forward.api import sensor_badges

API = Path(__file__).resolve().parents[1] / "src/zava_forward/api"
OPS = API / "web/ops.js"
SERVER = API / "server.py"
ADVISORY = "Advisory telemetry \u2014 officer review required"


class BadgeModel(unittest.TestCase):
    def kinds(self, **view: Any) -> dict[str, dict[str, str]]:
        return {b["kind"]: b for b in sensor_badges.badges(view)}

    def test_each_state_has_a_plain_text_label(self) -> None:
        cases: list[tuple[dict[str, Any], str, str]] = [
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
        stale: dict[str, Any] = dict(state="ok", latest={"reading_id": "R-1"}, freshness="stale")
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


class FaultGuidance(unittest.TestCase):
    def view(self, state: str, **extra: Any) -> dict[str, Any]:
        base: dict[str, Any] = dict(state="ok", latest={"x": 1}, freshness="fresh")
        return sensor_badges.annotate(dict(base, health=dict(state=state), **extra))

    def test_fault_and_out_of_range_get_text_badges_and_next_action(self) -> None:
        for state, label in (("fault", "Sensor fault"), ("out_of_range", "Out of range")):
            with self.subTest(state=state):
                out = self.view(state)
                badge = out["badges"][1]
                self.assertEqual(
                    (badge["kind"], badge["state"], badge["label"]), ("health", state, label)
                )
                self.assertIn("Do not use this reading", out["next_action"])

    def test_states_are_distinct_with_one_next_action_each(self) -> None:
        views: dict[str, dict[str, Any]] = {
            "withheld": dict(state="consent-withheld", latest=None),
            "offline": dict(state="no-readings", latest=None),
            "stale": dict(state="ok", latest={"x": 1}, freshness="stale"),
        }
        actions = {k: sensor_badges.annotate(v)["next_action"] for k, v in views.items()}
        self.assertEqual(
            sensor_badges.annotate(views["withheld"])["badges"][0]["label"], "Withheld"
        )
        self.assertEqual(len(set(actions.values())), 3)

    def test_usable_reading_has_no_action_and_withheld_hides_health(self) -> None:
        self.assertIsNone(self.view("ok")["next_action"])
        hidden = sensor_badges.annotate(
            dict(state="consent-withheld", latest=None, health=dict(state="fault"))
        )
        self.assertEqual([b["kind"] for b in hidden["badges"]], ["freshness", "calibration"])

    def test_fault_outranks_stale(self) -> None:
        out = self.view("fault", freshness="stale")
        self.assertIn("sensor fault", out["next_action"])

    def test_conflict_gets_badge_and_action_ahead_of_stale_and_context_only_offline(self) -> None:
        stale_clash = self.view("conflict", freshness="stale")
        badge = stale_clash["badges"][1]
        self.assertEqual(
            (badge["kind"], badge["state"], badge["label"]),
            ("health", "conflict", "Conflicting readings"),
        )
        self.assertIn("Do not choose between conflicting readings", stale_clash["next_action"])

        context_only_clash = sensor_badges.annotate(
            dict(
                state="ok",
                latest=None,
                freshness="unknown",
                conflicting_readings=[dict(sensor_id="s1", observed_at="2026-11-01T10:00:00Z")],
            )
        )
        self.assertEqual(
            [b["state"] for b in context_only_clash["badges"]],
            ["offline", "conflict", "uncalibrated"],
        )
        self.assertIn(
            "Do not choose between conflicting readings", context_only_clash["next_action"]
        )

        withheld = sensor_badges.annotate(
            dict(
                state="consent-withheld",
                latest=None,
                conflicting_readings=[dict(sensor_id="s1", observed_at="2026-11-01T10:00:00Z")],
            )
        )
        self.assertEqual([b["kind"] for b in withheld["badges"]], ["freshness", "calibration"])

    def test_panel_renders_next_action_as_text(self) -> None:
        panel = OPS.read_text(encoding="utf-8")
        self.assertIn("data-sensor-next-action", panel)
        self.assertIn("Next action:", panel)


class UiSource(unittest.TestCase):
    def test_panel_renders_text_badges_without_new_invalid_state(self) -> None:
        src = OPS.read_text(encoding="utf-8")
        start = src.index("function sensorPanel")
        panel = src[start : src.index("function simulationPanel")]
        self.assertIn("data-sensor-badges", panel)
        self.assertIn("data-sensor-advisory", panel)
        self.assertIn("b.state", panel)
        self.assertNotIn("\u2014", panel)
        self.assertNotIn("\\u2014", panel)
        self.assertNotIn("aria-invalid", panel)


if __name__ == "__main__":
    unittest.main()
