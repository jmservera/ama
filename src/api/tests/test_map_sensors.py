"""Employee map sensor summary (issue 1818): bounded, consent-gated and role-projected.

Seed rows follow the retained synthetic contract. Nothing here claims live Azure IoT Hub transport.
"""

import json
import time
import unittest
from typing import Any

from zava_forward.core import insights, sensor_map

import test_assistants as ta
from test_quality_sensors import Seed


class MapSensors(Seed, ta.ApiTests):
    def put(self, count: int = 3, **kw: Any) -> None:
        super().put(count, base=int(time.time()), **kw)

    def sensor(self, case: str = "ZF-1") -> dict[str, Any]:
        status, view = self.request("/api/map?zoom=14")
        self.assertEqual(status, 200)
        self.assertEqual(view["mode"], "points")
        return {i["id"]: i["sensor"] for i in view["items"]}[case]

    def test_recent_reading_is_summarised_without_history_or_ids(self) -> None:
        self.put(3, offset=120)
        s = self.sensor()
        self.assertEqual((s["state"], s["alert"], s["calibrated"]), ("fresh", False, False))
        self.assertIn("Synthetic", s["source"])
        self.assertEqual(s["temperature_c"], 19.2)
        self.assertEqual(s["humidity_pct"], 52.0)
        text = json.dumps(self.request("/api/map?zoom=14")[1])
        for private in ("SENS-SYN-1", "R-ZF-1-", "reading_id", "sensor_id"):
            self.assertNotIn(private, text)

    def test_old_readings_are_stale_or_offline(self) -> None:
        self.put(1, offset=3600)
        self.assertEqual(self.sensor()["state"], "stale")
        self.assertTrue(self.sensor()["alert"])
        self.put(1, home="ZF-2", offset=3 * 86400)
        self.assertEqual(self.sensor("ZF-2")["state"], "offline")

    def test_missing_and_withheld_readings_carry_no_values(self) -> None:
        self.configure()
        self.assertEqual(self.sensor()["state"], "no-readings")
        self.put(2, consent="declined", offset=120)
        s = self.sensor()
        self.assertEqual(s["state"], "consent-withheld")
        self.assertNotIn("temperature_c", s)
        self.assertNotIn("observed_at", s)

    def test_only_quality_evidence_roles_see_values(self) -> None:
        self.put(2, offset=120)
        for role, person in self.people.items():
            if role == "Contractor" or role == "Unknown":
                continue
            self.user = person
            s = self.sensor()
            if role in ("Retrofit Programme Manager", "Quality Inspector"):
                self.assertEqual(s["state"], "fresh", role)
            else:
                self.assertEqual(s["state"], "restricted", role)
                self.assertNotIn("temperature_c", s, role)

    def test_homes_beyond_the_cap_are_not_loaded(self) -> None:
        self.put(1, offset=120)
        with self.service.transaction() as db:
            out = sensor_map.summaries(
                db, [f"H{i}" for i in range(sensor_map.HOME_CAP + 3)], time.time()
            )
        self.assertEqual(sum(v["state"] == "not-loaded" for v in out.values()), 3)
        self.assertEqual(len(out), sensor_map.HOME_CAP + 3)

    def test_clusters_carry_no_sensor_data(self) -> None:
        view = insights.map_view(self.store.cases.values(), {}, cap=1)
        self.assertEqual(view["mode"], "clusters")
        self.assertNotIn("sensor", json.dumps(view))

    def test_without_a_provider_points_say_not_connected(self) -> None:
        view = insights.map_view(self.store.cases.values(), {})
        self.assertTrue(all(i["sensor"]["state"] == "not-connected" for i in view["items"]))


if __name__ == "__main__":
    unittest.main()
