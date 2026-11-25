"""Employee map sensor summary (issue 1818): bounded, consent-gated and role-projected.

Seed rows follow the retained synthetic contract. Nothing here claims live Azure IoT Hub transport.
"""

import json
import time
import unittest
from typing import Any, cast
from unittest.mock import patch

from zava_forward.core import identity, insights, mssqlstore, sensor_map

import test_assistants as ta
from test_quality_sensors import Seed


class MapSensors(Seed, ta.ApiTests):
    def put(
        self,
        count: int = 3,
        consent: str | None = "granted",
        home: str = "ZF-1",
        offset: int = 3 * 3600,
        **kw: Any,
    ) -> None:
        super().put(count, consent, home, offset, base=int(time.time()), **kw)

    def map_view(self) -> tuple[int, dict[str, Any]]:
        return cast(
            tuple[int, dict[str, Any]],
            self.request("/api/map?zoom=14&sensors=1"),  # type: ignore[no-untyped-call]
        )

    def sensor(self, case: str = "ZF-1") -> dict[str, Any]:
        status, view = self.map_view()
        self.assertEqual(status, 200)
        self.assertEqual(view["mode"], "points")
        return cast(dict[str, Any], {i["id"]: i["sensor"] for i in view["items"]}[case])

    def test_recent_reading_is_summarised_without_history_or_ids(self) -> None:
        self.put(3, offset=120)
        s = self.sensor()
        self.assertEqual((s["state"], s["alert"], s["calibrated"]), ("fresh", False, False))
        self.assertIn("Synthetic", s["source"])
        self.assertEqual(s["temperature_c"], 19.2)
        self.assertEqual(s["humidity_pct"], 52.0)
        text = json.dumps(self.map_view()[1])
        for private in ("SENS-SYN-1", "R-ZF-1-", "reading_id", "sensor_id"):
            self.assertNotIn(private, text)

    def test_default_map_does_not_read_sensors(self) -> None:
        self.put(3, offset=120)
        with patch.object(self.service, "map_sensors", side_effect=AssertionError("eager read")):
            for query in ("", "&sensors=0", "&bbox=-90,-180,90,180"):
                status, view = self.request(f"/api/map?zoom=14{query}")  # type: ignore[no-untyped-call]
                self.assertEqual(status, 200)
                self.assertTrue(view["items"])
                self.assertTrue(
                    all(item["sensor"]["state"] == "not-loaded" for item in view["items"])
                )
                self.assertNotIn("temperature_c", json.dumps(view))

    def test_selected_summary_reads_only_one_home_and_preserves_projection(self) -> None:
        self.put(3, offset=120)
        with patch.object(self.service, "map_sensors", wraps=self.service.map_sensors) as read:
            status, summary = self.request("/api/cases/ZF-1/sensor-summary")  # type: ignore[no-untyped-call]
        self.assertEqual(status, 200)
        expected = self.sensor()
        self.assertEqual(
            {key: value for key, value in summary.items() if key != "age_seconds"},
            {key: value for key, value in expected.items() if key != "age_seconds"},
        )
        self.assertEqual(read.call_count, 1)
        self.assertEqual(read.call_args.args[1], ["ZF-1"])
        self.user = self.people["Resident Liaison Officer"]
        status, summary = self.request("/api/cases/ZF-1/sensor-summary")  # type: ignore[no-untyped-call]
        self.assertEqual(status, 200)
        self.assertEqual(summary["state"], "restricted")
        self.assertNotIn("temperature_c", summary)

    def test_sensor_read_options_reject_invalid_or_unbounded_requests(self) -> None:
        for path in (
            "/api/map?sensors=invalid",
            "/api/map?sensors=1&sensors=0",
            f"/api/cases/{'A' * 65}/sensor-summary",
            "/api/cases/ZF-1/sensor-summary?extra=1",
        ):
            status, _ = self.request(path)  # type: ignore[no-untyped-call]
            self.assertEqual(status, 400, path)

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

    def test_sensor_reads_do_not_take_the_write_lock(self) -> None:
        self.put(3, offset=120)

        def busy() -> Any:
            raise AssertionError("sensor reads must not take the write lock")

        self.service.transaction = busy
        self.assertEqual(self.service.sensors(self.pm, "ZF-1")["case_id"], "ZF-1")
        self.assertEqual(self.sensor()["state"], "fresh")

    def test_a_failing_sensor_connection_keeps_the_map_available(self) -> None:
        self.put(3, offset=120)
        self.service._read_connection = self.fail_transaction
        with self.assertLogs("zava_forward.core.assistants", "WARNING") as logs:
            s = self.sensor()
        self.assertEqual(s["state"], "unavailable")
        self.assertNotIn("temperature_c", s)
        self.assertIn("exc=ProgrammingError", logs.output[0])

    def test_a_write_lock_timeout_in_the_overlay_is_logged_with_its_cause(self) -> None:
        self.put(3, offset=120)
        self.service._read_connection = self.lock_transaction
        with self.assertLogs("zava_forward.core.assistants", "WARNING") as logs:
            s = self.sensor()
        self.assertEqual(s["state"], "unavailable")
        self.assertIn("cause=sql-write-lock-busy", logs.output[0])
        self.assertNotIn("driver detail", logs.output[0])

    def test_an_other_overlay_failure_logs_only_the_sqlstate_code(self) -> None:
        self.put(3, offset=120)
        self.service._read_connection = self.state_transaction
        with self.assertLogs("zava_forward.core.assistants", "WARNING") as logs:
            self.sensor()
        self.assertIn("cause=other sqlstate=40001", logs.output[0])
        self.assertNotIn("driver detail", logs.output[0])

    @staticmethod
    def state_transaction() -> Any:
        class DatabaseError(Exception):
            pass

        DatabaseError.__module__ = "pyodbc"
        raise DatabaseError("40001", "driver detail")

    @staticmethod
    def lock_transaction() -> Any:
        class ProgrammingError(Exception):
            pass

        ProgrammingError.__module__ = "pyodbc"
        raise ProgrammingError(f"driver detail: {mssqlstore.LOCK_FAILED}")

    @staticmethod
    def fail_transaction() -> Any:
        class ProgrammingError(Exception):
            pass

        raise ProgrammingError("driver detail that must not be logged")

    TID = "11111111-1111-4111-8111-111111111111"
    OID = "22222222-2222-4222-8222-222222222222"

    def entra(self, role: str, **kw: Any) -> dict[str, Any]:
        return cast(dict[str, Any], identity.principal(self.TID, self.OID, role, **kw))

    def test_entra_principals_read_sensors_without_a_roster_row(self) -> None:
        self.put(2, offset=120)
        for role in ("Retrofit Programme Manager", "Quality Inspector"):
            user = self.entra(role)
            self.assertNotIn(user["email"], [p["email"] for p in self.people.values()])
            self.assertEqual(self.service.sensors(user, "ZF-1")["case_id"], "ZF-1")
            self.assertEqual(self.service.map_sensors(user, ["ZF-1"])["ZF-1"]["state"], "fresh")

    def test_entra_principal_with_another_role_or_admin_only_is_denied(self) -> None:
        self.put(2, offset=120)
        for user in (
            self.entra("Resident Liaison Officer"),
            self.entra("Application Administrator", app_admin=True),
            self.entra("Viewer", view_only=True),
        ):
            with self.assertRaises(PermissionError):
                self.service.sensors(user, "ZF-1")
            self.assertEqual(
                self.service.map_sensors(user, ["ZF-1"])["ZF-1"]["state"], "restricted"
            )

    def test_entra_principal_with_revoked_or_forged_keys_is_denied(self) -> None:
        self.put(2, offset=120)
        for change in (
            {"oid": "33333333-3333-4333-8333-333333333333"},
            {"code": "E-FORGED"},
            {"email": "pm@example.test"},
            {"identity_source": "password"},
        ):
            user = self.entra("Retrofit Programme Manager") | change
            with self.assertRaises(PermissionError):
                self.service.sensors(user, "ZF-1")
            self.assertEqual(
                self.service.map_sensors(user, ["ZF-1"])["ZF-1"]["state"], "restricted"
            )


if __name__ == "__main__":
    unittest.main()
