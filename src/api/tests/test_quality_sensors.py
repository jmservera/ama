"""Retained readings: bounded read model, API and Quality evidence (issue 1288, C1 and C2).

The model provider here is a local MOCK that records the request it receives. These prove which
retained values reach the model request and how a returned output is cited and projected. They are
not evidence that a real model ran, and nothing here accepts quality work. Seed rows follow the
actual retained contract (sensor consumer controls, live simulator and backfill row shapes).
"""

import contextlib
import dataclasses
import json
import os
import threading
import time
import unittest
from datetime import UTC, datetime
from unittest.mock import patch

import release_support
from dataset import supplied_resident_fixture
from sensor_consumer_fixture import CONTROL, POLICY
from zava_forward.core import quality, sensor_view
from zava_forward.core.assistants import capture, digest, signature
from zava_forward.core.sensor_consumer import READING_COLUMNS, SensorConsumer
from zava_forward.core.synthetic import live_readings

import test_assistants as ta

SEAL = sensor_view.SEAL_SECONDS
DEFAULT = "SENS-SYN-1"


def stamp(seconds):
    return datetime.fromtimestamp(seconds, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class CapturingProvider(ta.Provider):
    """Mock: cites the first retained readings it was given, or only the home when told not to."""

    def __init__(self, cite=True, leak=None, gate=None, fail=0, **kw):
        super().__init__(**kw)
        self.cite, self.leak, self.prompts = cite, leak, []
        self.gate, self.fail = gate, fail

    def evidence(self, system, prompt, max_tokens, timeout):
        self.prompts.append(json.loads(prompt))
        if self.gate:
            self.gate["entered"].set()
            self.gate["proceed"].wait(20)
        if self.fail:
            self.fail -= 1
            raise RuntimeError("scripted provider failure")
        keys = self.prompts[-1]["evidence"]["citations"]
        cited = sorted(k for k in keys if k.startswith("sensor:"))[:2] if self.cite else []
        result = super().evidence(system, prompt, max_tokens, timeout)
        value = json.loads(result["text"])
        value["findings"] = [
            dict(
                text="Cited retained readings are supplied evidence for a person to review.",
                citations=cited or ["source:home"],
            )
        ]
        if self.leak:
            value["summary"] = f"Indoor {self.leak} degC was recorded."
            value["unknowns"] = [f"Whether {self.leak} degC is typical."]
            value["findings"][0]["text"] = f"Reading of {self.leak} degC."
        result["text"] = ta.canonical(value)
        return result


class Seed:
    def setUp(self):
        super().setUp()
        self.controls = {}
        with self.service.transaction() as db:
            for table in (
                "sensor_reading",
                "sensor_consumer_control",
                "sensor_consumer_control_home",
                "sensor_consumer_index_state",
                "sensor_consumer_policy",
            ):
                db.execute(f"DROP TABLE IF EXISTS {table}")

    def mock(self, **kw):
        self.provider = self.store.ai = CapturingProvider(**kw)
        release_support.install(self.store)

    def configure(self):
        controls = [
            dataclasses.replace(CONTROL, sensor_id=s, home_id=h, consent=c)
            for s, (h, c) in sorted(self.controls.items())
        ]
        SensorConsumer(self.store).configure(POLICY, controls)

    def set_consent(self, consent, home="ZF-1", sensor=DEFAULT):
        self.controls[sensor] = (home, consent)
        self.configure()

    def put(self, count=3, consent="granted", home="ZF-1", offset=3 * 3600, **kw):
        sensor = kw.setdefault("sensor", "SENS-SYN-" + home[3:])
        if consent:
            self.controls[sensor] = (home, consent)
        self.configure()
        self.add_readings(count, home, offset, **kw)

    def add_readings(
        self,
        count,
        home="ZF-1",
        offset=3 * 3600,
        tag="R",
        source="SYNTHETIC",
        sensor=None,
        scenario="BACKFILL_2Y",
        version="reading-v1",
        base=None,
    ):
        base = int(time.time()) // SEAL * SEAL if base is None else base
        sensor = sensor or "SENS-SYN-" + home[3:]
        with self.service.transaction() as db:
            for i in range(count):
                row = dict(
                    sensor_id=sensor,
                    reading_id=f"{tag}-{home}-{i:03d}",
                    home_id=home,
                    observed_at=stamp(base - offset + i * 60),
                    temperature_c=f"{19 + i * 0.1:.1f}",
                    humidity_pct=f"{50 + i}",
                    source_type=source,
                    scenario=scenario,
                    seed="1",
                    schema_version=version,
                    injected_fault="none",
                )
                db.execute(
                    f"INSERT INTO sensor_reading VALUES ({','.join('?' * len(READING_COLUMNS))})",
                    tuple(row[c] for c in READING_COLUMNS),
                )

    def add_live(self, minute, home="ZF-1", sensor=DEFAULT, base=None):
        """A row built by the actual live simulator contract."""
        base = int(time.time()) // SEAL * SEAL if base is None else base
        reading = live_readings.Reading(
            home_id=home,
            sensor_id=sensor,
            device_id="device-1",
            observed_at=datetime.fromtimestamp(base - minute * 60, UTC),
            temperature_c=11.25,
            humidity_pct=71.5,
            sunlight_wm2=120.0,
            seed=184,
        )
        row = reading.row()
        with self.service.transaction() as db:
            db.execute(
                f"INSERT INTO sensor_reading VALUES ({','.join('?' * len(READING_COLUMNS))})",
                tuple(row[c] for c in READING_COLUMNS),
            )
        return reading.reading_id

    def quality_ready(self):
        cl = quality.checklist_for("Loft insulation")
        items = {label: "SYN current photo" for label in cl["items"]}
        with self.store.lock:
            supplied_resident_fixture(self.store._case("ZF-1"))
            self.store.save()
        self.store.submit_quality(
            self.pm,
            "ZF-1",
            "Loft insulation",
            "SYN installer",
            "Installer",
            items,
            context_revision=1,
        )
        self.store.accept_quality(self.people["Quality Inspector"], "ZF-1", 0)

    def clock(self, seconds):
        return patch.object(self.service, "now", side_effect=lambda db=None: time.time() + seconds)

    def quality_task(self):
        with self.service.transaction() as db:
            rows = db.execute(
                "SELECT id FROM assistant_tasks WHERE capability='quality-evidence'"
                " AND case_id='ZF-1' ORDER BY id"
            ).fetchall()
        return [r[0] for r in rows]


class ReadModel(Seed, ta.Base):
    def view(self):
        return self.service.sensors(self.pm, "ZF-1")

    def test_states_fail_closed(self):
        self.assertEqual(self.view()["state"], "unavailable")
        self.put(0, consent=None)
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.put(0, consent="declined")
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.put(0)
        self.assertEqual(self.view()["state"], "no-readings")

    def test_bounded_synthetic_home_only_with_units_and_utc(self):
        self.put(40)
        self.add_readings(3, tag="X", source="WEATHER")
        self.add_readings(3, home="ZF-2", tag="O")
        v = self.view()
        self.assertEqual(v["state"], "ok")
        self.assertEqual(len(v["readings"]), sensor_view.WINDOW_MAX)
        self.assertEqual(v["units"], dict(temperature_c="degC", humidity_pct="%RH"))
        for r in v["readings"]:
            self.assertTrue(r["observed_at"].endswith("Z"))
            self.assertTrue(r["reading_id"].startswith("R-ZF-1-"))
        self.assertEqual(v["latest"], v["readings"][-1])
        self.assertEqual(v["latest"]["reading_id"], "R-ZF-1-039")
        self.assertEqual(v["freshness"], "stale")
        self.assertIn("older than 15 minutes", v["freshness_text"])

    def test_live_contract_rows_are_weather_derived_and_not_calibrated(self):
        self.put(2)
        live = self.add_live(10)
        self.add_readings(1, tag="U", scenario="odd", version="x-v9")
        v = self.view()
        by_id = {r["reading_id"]: r["provenance_class"] for r in v["readings"]}
        self.assertEqual(by_id[live], "synthetic-weather-derived")
        self.assertEqual(by_id["R-ZF-1-000"], "synthetic-modelled-indoor")
        self.assertEqual(by_id["U-ZF-1-000"], "synthetic-unclassified")
        self.assertIs(v["calibrated"], False)
        self.assertIn("outdoor weather", v["provenance"]["synthetic-weather-derived"])
        for label in v["provenance"].values():
            self.assertIn("Not calibrated", label)
        self.assertNotIn("indoor-observation", json.dumps(v))

    def test_latest_is_in_the_captured_source_and_citations(self):
        self.put(4)
        newest = self.add_live(0)
        v = self.view()
        with self.service.transaction() as db:
            snap = self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))
        sensors = snap["sources"]["sensors"]
        self.assertEqual(v["latest"]["reading_id"], newest)
        self.assertEqual(sensors["latest"], v["latest"])
        self.assertIn(sensor_view.key_of(v["latest"]), snap["citations"])
        self.assertEqual(
            {k: v[k] for k in ("readings", "before", "after")},
            {k: sensors[k] for k in ("readings", "before", "after")},
        )

    def test_capture_is_stable_across_clock_only_changes(self):
        self.put(4)
        with self.service.transaction() as db:
            first = self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))
        with self.clock(3 * SEAL), self.service.transaction() as db:
            later = self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))
        self.assertEqual(digest(first), digest(later))

    def test_same_reading_id_from_two_sensors_has_two_citations(self):
        self.put(2)
        self.set_consent("granted", sensor="SENS-SYN-1B")
        self.add_readings(2, sensor="SENS-SYN-1B")
        v = self.view()
        keys = v["citation_keys"]
        self.assertEqual(len(v["readings"]), 4)
        self.assertEqual(len(set(keys)), 4)
        self.assertIn("sensor:SENS-SYN-1:R-ZF-1-000", keys)
        self.assertIn("sensor:SENS-SYN-1B:R-ZF-1-000", keys)
        with self.service.transaction() as db:
            snap = self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))
        locators = {snap["citations"][k]["locator"] for k in keys}
        self.assertEqual(len(locators), 4)

    def test_second_sensor_without_consent_withholds_the_home(self):
        self.put(2)
        self.add_readings(1, sensor="SENS-SYN-1B", tag="B")
        self.assertEqual(self.view()["state"], "consent-withheld")

    def test_retrofit_context_is_unavailable_and_anchor_is_not_retrofit(self):
        self.put(5)
        v = self.view()
        self.assertIs(v["retrofit_context"]["available"], False)
        self.assertIn("No installation date", v["retrofit_context"]["text"])
        self.assertEqual(v["anchor"]["name"], "quality_record_anchor")
        self.assertIsNone(v["anchor"]["at"])
        self.assertIn("no comparison", v["before_absent"])
        self.quality_ready()
        v = self.view()
        self.assertTrue(v["anchor"]["at"])
        self.assertIn("not an installation date", v["anchor"]["meaning"])
        self.assertIs(v["retrofit_context"]["available"], False)
        self.assertEqual(len(v["before"]), 4)
        self.assertEqual(v["after"], [])
        self.assertIn("onward", v["after_absent"])

    def test_read_is_side_effect_free_and_generates_nothing(self):
        self.put(5)

        def count():
            with self.service.transaction() as db:
                return db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]

        before = count()
        self.view()
        self.assertEqual(before, count())
        self.assertEqual(self.provider.calls, 0)

    def test_controls_and_readings_are_read_by_key_not_by_table_scan(self):
        self.put(3)
        self.set_consent("granted", home="ZF-2", sensor="SENS-SYN-2")
        statements = []

        class Spy:
            def __init__(self, db):
                self.db = db

            def execute(self, sql, args=()):
                statements.append(" ".join(sql.split()))
                return self.db.execute(sql, args)

        with self.service.transaction() as db:
            sensor_view.view(Spy(db), "ZF-1", None, time.time(), self.service.mssql)
        controls = [s for s in statements if "sensor_consumer_control" in s]
        self.assertTrue(controls)
        for s in controls:
            if s.startswith("SELECT COUNT(*)") or "sys.triggers" in s:
                continue
            if "sensor_consumer_control_home" in s:
                self.assertIn("WHERE home_id=?", s)
                self.assertTrue("FETCH NEXT" in s or "LIMIT" in s, s)
            else:
                self.assertIn("WHERE sensor_id=?", s)
        readings = [s for s in statements if "FROM sensor_reading" in s]
        self.assertTrue(readings)
        for s in readings:
            self.assertIn("home_id=?", s)
            self.assertTrue("observed_at<?" in s or "observed_at>=?" in s, s)
            self.assertTrue("FETCH NEXT" in s or "LIMIT" in s, s)
        with self.service.transaction() as db:
            if self.service.mssql:
                row = db.execute(
                    "SELECT 1 FROM sys.indexes WHERE name='ix_sensor_reading_home_time'"
                    " AND object_id=OBJECT_ID(N'sensor_reading')"
                ).fetchone()
            else:
                row = db.execute(
                    "SELECT 1 FROM sqlite_master WHERE name='ix_sensor_reading_home_time'"
                ).fetchone()
        self.assertIsNotNone(row)

    def capture(self, now, reference=None):
        with self.service.transaction() as db:
            return sensor_view.capture_source(db, "ZF-1", reference, now, self.service.mssql)

    def test_declined_unsampled_control_for_the_home_withholds(self):
        self.put(3)
        self.assertEqual(self.view()["state"], "ok")
        self.set_consent("declined", sensor="SENS-OTHER-9")
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.assertEqual(self.view()["latest"], None)

    def test_control_missing_from_the_home_index_fails_closed(self):
        self.put(3)
        self.assertEqual(self.view()["state"], "ok")
        with self.service.transaction() as db:
            db.execute("DELETE FROM sensor_consumer_control_home")
        self.assertEqual(self.view()["state"], "consent-withheld")

    def test_other_homes_declined_control_does_not_withhold_this_home(self):
        self.put(3)
        self.set_consent("declined", home="ZF-2", sensor="SENS-SYN-2")
        self.assertEqual(self.view()["state"], "ok")

    def test_future_boundary_old_and_missing_readings(self):
        self.put(0)
        now = int(time.time())
        horizon = sensor_view.WINDOW_DAYS * 86400
        self.assertEqual(self.capture(now)["state"], "no-readings")
        self.assertIs(self.capture(now)["future_dated_excluded"], False)
        self.add_readings(1, tag="F", base=now, offset=-3600)
        only_future = self.capture(now)
        self.assertEqual((only_future["state"], only_future["latest"]), ("no-readings", None))
        self.assertIs(only_future["future_dated_excluded"], True)
        self.add_readings(1, tag="B", base=now, offset=0)
        self.add_readings(1, tag="E", base=now, offset=horizon)
        self.add_readings(1, tag="O", base=now, offset=horizon + 1)
        ids = [r["reading_id"] for r in self.capture(now)["readings"]]
        self.assertEqual(ids, ["E-ZF-1-000", "B-ZF-1-000"])
        self.assertIs(self.capture(now)["future_dated_excluded"], True)
        later = self.capture(now + 7200)
        self.assertEqual(later["latest"]["reading_id"], "F-ZF-1-000")
        self.assertIs(later["future_dated_excluded"], False)

    def test_future_reading_is_never_the_latest_or_fresh(self):
        self.put(2)
        self.add_readings(1, tag="F", base=int(time.time()), offset=-3600)
        v = self.view()
        self.assertEqual(v["latest"]["reading_id"], "R-ZF-1-001")
        self.assertNotEqual(v["freshness"], "fresh")
        self.assertTrue(v["future_dated_excluded"])
        self.assertIn("Current freshness is not asserted", v["as_of_rule"])

    def test_context_rows_are_bounded_in_time_and_by_as_of(self):
        self.put(0)
        now = int(time.time())
        ref = datetime.fromtimestamp(now - 3 * 86400, UTC).replace(microsecond=0)
        day = 86400
        self.add_readings(1, tag="A", base=now, offset=3 * day + 31 * day)
        self.add_readings(1, tag="B", base=now, offset=3 * day + 29 * day)
        self.add_readings(1, tag="C", base=now, offset=3 * day - 29 * day)
        cap = self.capture(now, ref)
        self.assertEqual([r["reading_id"] for r in cap["before"]], ["B-ZF-1-000"])
        self.assertEqual(cap["after"], [])

    def test_context_change_outside_the_window_changes_the_capture_identity(self):
        self.put(0)
        now = int(time.time())
        ref = datetime.fromtimestamp(now - 3600, UTC).replace(microsecond=0)
        self.add_readings(20, base=now, offset=3600 + 120)
        first = self.capture(now, ref)
        self.add_readings(1, tag="C", base=now, offset=3600 + 90)
        second = self.capture(now, ref)
        self.assertEqual(first["readings"], second["readings"])
        self.assertEqual(first["latest"], second["latest"])
        self.assertNotEqual(first["before"], second["before"])
        self.assertNotEqual(digest(first), digest(second))

    def _old_anchor(self, days=500):
        now = int(time.time())
        ref = datetime.fromtimestamp(now - days * 86400, UTC).replace(microsecond=0)
        self.add_readings(2, base=int(ref.timestamp()), offset=3600, tag="OLD")
        return now, ref

    def test_context_only_capture_is_an_ok_capture_with_no_latest(self):
        self.put(0)
        now, ref = self._old_anchor()
        cap = self.capture(now, ref)
        self.assertEqual(cap["state"], "ok")
        self.assertIsNone(cap["latest"])
        self.assertEqual(len(cap["before"]), 2)
        self.assertEqual(sorted(cap["citation_keys"]), sorted(sensor_view.citations(cap)))
        with patch.object(sensor_view, "reference_for", return_value=ref):
            v = self.view()
        self.assertEqual((v["state"], v["freshness"]), ("ok", "unknown"))
        self.assertEqual(v["before"], cap["before"])

    def _control_state(self):
        with self.service.transaction() as db:
            return [
                db.execute(f"SELECT * FROM {t} ORDER BY 1").fetchall()
                for t in ("sensor_consumer_policy", "sensor_consumer_control")
            ]

    def _index(self):
        with self.service.transaction() as db:
            return db.execute(
                "SELECT home_id,sensor_id FROM sensor_consumer_control_home ORDER BY 1,2"
            ).fetchall()

    def test_migration_restores_a_missing_index_without_replacing_policy_or_controls(self):
        self.put(3)
        self.set_consent("granted", sensor="SENS-OTHER-9")
        want, state = self._index(), self._control_state()
        with self.service.transaction() as db:
            db.execute("DROP TABLE sensor_consumer_control_home")
        self.assertEqual(self.view()["state"], "unavailable")
        self.service.migrate()
        self.assertEqual((self._index(), self._control_state()), (want, state))
        self.assertEqual(self.view()["state"], "ok")
        self.service.migrate()
        SensorConsumer(self.store).migrate_control_index()
        self.assertEqual((self._index(), self._control_state()), (want, state))

    def test_partial_index_fails_closed_until_migrated_and_then_sees_the_decline(self):
        self.put(3)
        self.set_consent("declined", sensor="SENS-OTHER-9")
        with self.service.transaction() as db:
            db.execute("DELETE FROM sensor_consumer_control_home WHERE sensor_id='SENS-OTHER-9'")
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.assertEqual(self.view()["latest"], None)
        self.service.migrate()
        self.assertIn(("ZF-1", "SENS-OTHER-9"), self._index())
        self.assertEqual(self.view()["state"], "consent-withheld")

    def test_orphan_index_row_fails_closed_and_is_removed_by_migration(self):
        self.put(3)
        with self.service.transaction() as db:
            db.execute(
                "INSERT INTO sensor_consumer_control_home (home_id, sensor_id)"
                " VALUES ('ZF-1','GONE-1')"
            )
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.service.migrate()
        self.assertNotIn(("ZF-1", "GONE-1"), self._index())
        self.assertEqual(self.view()["state"], "ok")

    def _tamper(self, sql, *args):
        with self.service.transaction() as db:
            db.execute(sql, args)

    def test_equal_count_wrong_home_index_fails_closed_and_migration_repairs_it(self):
        self.put(3)
        self.set_consent("declined", sensor="SENS-OTHER-9")
        want = self._index()
        self._tamper(
            "UPDATE sensor_consumer_control_home SET home_id='ZF-2' WHERE sensor_id='SENS-OTHER-9'"
        )
        v = self.view()
        self.assertEqual((v["state"], v["latest"]), ("consent-withheld", None))
        self.service.migrate()
        self.assertEqual(self._index(), want)

    def test_equal_count_missing_plus_orphan_fails_closed_until_migrated(self):
        self.put(3)
        self.set_consent("granted", sensor="SENS-OTHER-9")
        want = self._index()
        self._tamper("DELETE FROM sensor_consumer_control_home WHERE sensor_id='SENS-OTHER-9'")
        self._tamper(
            "INSERT INTO sensor_consumer_control_home (home_id, sensor_id) VALUES ('ZF-9','GONE-1')"
        )
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.service.migrate()
        self.assertEqual((self._index(), self.view()["state"]), (want, "ok"))

    def test_failed_reconciliation_fails_all_consent_closed_until_repaired(self):
        self.put(3)
        self.set_consent("declined", sensor="SENS-OTHER-9")
        want, state = self._index(), self._control_state()
        self._tamper(
            "UPDATE sensor_consumer_control_home SET home_id='ZF-2' WHERE sensor_id='SENS-OTHER-9'"
        )
        self._tamper("INSERT INTO sensor_consumer_control (sensor_id, body) VALUES ('BAD-1','x')")
        self._tamper(
            "INSERT INTO sensor_consumer_control_home (home_id, sensor_id) VALUES ('ZF-9','BAD-1')"
        )
        self.service.migrate()
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.assertEqual(self.view()["latest"], None)
        self._tamper("DELETE FROM sensor_consumer_control WHERE sensor_id='BAD-1'")
        self.service.migrate()
        self.assertEqual((self._index(), self._control_state()), (want, state))

    def test_failed_reconciliation_does_not_grant_a_granted_home(self):
        self.put(3)
        self._tamper("INSERT INTO sensor_consumer_control (sensor_id, body) VALUES ('BAD-1','x')")
        self._tamper(
            "INSERT INTO sensor_consumer_control_home (home_id, sensor_id) VALUES ('ZF-9','BAD-1')"
        )
        self.service.migrate()
        self.assertEqual(self.view()["state"], "consent-withheld")

    def test_missing_state_marker_fails_closed_until_migrated_and_migration_is_idempotent(self):
        self.put(3)
        self._tamper("DROP TABLE IF EXISTS sensor_consumer_index_state")
        self.assertNotEqual(self.view()["state"], "ok")
        self.service.migrate()
        self.assertEqual(self.view()["state"], "ok")
        before = self._control_state()
        self.service.migrate()
        self.assertEqual((self.view()["state"], self._control_state()), ("ok", before))

    def _move_control_home(self, sensor, home):
        modify = (
            "JSON_MODIFY(body,'$.home_id',?)"
            if self.service.mssql
            else "json_set(body,'$.home_id',?)"
        )
        self._tamper(
            f"UPDATE sensor_consumer_control SET body={modify} WHERE sensor_id=?", home, sensor
        )

    def test_changed_control_home_with_a_valid_marker_fails_closed_until_migrated(self):
        self.put(3)
        self.set_consent("declined", home="ZF-2", sensor="SENS-B1")
        self.assertEqual(self.view()["state"], "ok")
        self._move_control_home("SENS-B1", "ZF-1")
        v = self.view()
        self.assertEqual((v["state"], v["latest"]), ("consent-withheld", None))
        self.service.migrate()
        self.assertEqual(self.view()["state"], "consent-withheld")
        self._move_control_home("SENS-B1", "ZF-2")
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.service.migrate()
        self.assertEqual(self.view()["state"], "ok")

    def test_previous_format_marker_or_missing_guard_fails_closed_until_migrated(self):
        self.put(3)
        drop = "JSON_MODIFY(body,'$.v',NULL)" if self.service.mssql else "json_remove(body,'$.v')"
        self._tamper(f"UPDATE sensor_consumer_index_state SET body={drop}")
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.service.migrate()
        self.assertEqual(self.view()["state"], "ok")
        # SQL Server has one trigger for all three events; SQLite has one per event.
        guard = (
            "sensor_consumer_control_guard"
            if self.service.mssql
            else "sensor_consumer_control_guard_upd"
        )
        self._tamper(f"DROP TRIGGER {guard}")
        self.assertEqual(self.view()["state"], "consent-withheld")
        before = self._control_state()
        self.service.migrate()
        self.service.migrate()
        self.assertEqual((self.view()["state"], self._control_state()), ("ok", before))
        with self.service.transaction() as db:
            catalog = (
                "SELECT name FROM sys.triggers WHERE name LIKE 'sensor_consumer_control_guard%'"
                if self.service.mssql
                else "SELECT name FROM sqlite_master WHERE type='trigger'"
                " AND name LIKE 'sensor_consumer_control_guard_%'"
            )
            names = db.execute(catalog).fetchall()
        self.assertEqual(len(names), 1 if self.service.mssql else 3)

    def test_future_readings_beyond_a_day_are_reported_not_absent(self):
        self.put(0)
        now = int(time.time())
        for tag, ahead in (("A", 86400 + 60), ("B", 2 * 86400), ("C", 40 * 86400)):
            with self.subTest(tag=tag):
                self._tamper("DELETE FROM sensor_reading")
                self.add_readings(1, tag=tag, base=now, offset=-ahead)
                v = self.capture(now)
                self.assertEqual((v["state"], v["latest"]), ("no-readings", None))
                self.assertIs(v["future_dated_excluded"], True)


class Http(Seed, ta.ApiTests):
    def proactive(self):
        scanned = self.service.scan()
        quality_ids = self.quality_task()
        self.assertTrue(set(quality_ids) & set(scanned["enqueued"]), scanned)
        tid = quality_ids[0]
        self.assertTrue(self.service.execute(tid))
        return tid, self.service.detail(self.pm, tid)

    def ready(self, **kw):
        self.mock(**kw)
        self.put(4)
        self.add_live(10)
        self.quality_ready()

    def test_sensors_api_role_matrix(self):
        self.put(4)
        status, v = self.request("/api/cases/ZF-1/sensors")
        self.assertEqual((status, v["state"], v["case_id"]), (200, "ok", "ZF-1"))
        allowed = {"Retrofit Programme Manager", "Quality Inspector"}
        for role, person in self.people.items():
            self.user = person
            status = self.request("/api/cases/ZF-1/sensors")[0]
            self.assertEqual(status, 200 if role in allowed else 403, role)
        self.user = self.people["Programme Support Officer"]
        self.assertEqual(self.request("/api/cases/ZF-1")[0], 200)
        self.assertEqual(self.request("/api/assistants/proposals")[0], 200)
        self.assertEqual(
            self.request("/api/assistants/quality-evidence/invoke", dict(case_id="ZF-1"))[0], 403
        )
        self.user = self.pm
        self.assertEqual(self.request("/api/cases/NOPE/sensors")[0], 404)

    def test_same_ids_and_values_reach_model_and_proactive_flag(self):
        # MOCK provider: proves the request content and flag shape, not real AI behaviour.
        self.ready()
        api = self.request("/api/cases/ZF-1/sensors")[1]
        tid, p = self.proactive()
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        for key in ("readings", "before", "after", "latest"):
            self.assertEqual(sent.get(key), api.get(key), key)
        keys = set(sensor_view.citations(sent))
        flag = p["review_flag"]
        self.assertEqual(
            (flag["status"], flag["level"], flag["trigger"]),
            ("review-suggested", "L4", "proactive"),
        )
        self.assertTrue(flag["autonomous"] and flag["unapproved"] and flag["sensor_grounded"])
        self.assertTrue(set(flag["sensor_cited_ids"]) <= keys and flag["sensor_cited_ids"])
        pairs = {(r["sensor_id"], r["reading_id"]) for r in flag["readings"]}
        self.assertEqual(
            pairs, {tuple(k[len("sensor:") :].split(":", 1)) for k in flag["sensor_cited_ids"]}
        )
        self.assertEqual(flag["model"]["model"], "test-model")
        self.assertIn("No named recipient", flag["delivery"])
        self.assertEqual({k for k in p["snapshot"]["citations"] if k.startswith("sensor:")}, keys)

    def test_manual_request_is_not_an_autonomous_flag(self):
        self.ready()
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.service.execute(tid)
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(
            (flag["status"], flag["autonomous"], flag["level"]), ("manual-proposal", False, None)
        )

    def test_proactive_output_without_sensor_citation_is_not_a_sensor_flag(self):
        self.ready(cite=False)
        flag = self.proactive()[1]["review_flag"]
        self.assertEqual((flag["status"], flag["autonomous"]), ("uncited", False))

    def test_rejected_proposal_is_not_a_flag(self):
        self.ready()
        tid, p = self.proactive()
        self.service.review(self.pm, tid, "reject", p["revision"], note="Not needed.")
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual((flag["status"], flag["autonomous"]), ("rejected", False))

    def test_stale_proposal_is_not_a_flag(self):
        self.ready()
        tid, _ = self.proactive()
        self.add_live(0, base=int(time.time()) // SEAL * SEAL + SEAL)
        with self.clock(SEAL + 60):
            stale = self.service.detail(self.pm, tid)
        self.assertTrue(stale["stale"])
        self.assertEqual(stale["review_flag"]["status"], "not-current")
        self.assertFalse(stale["review_flag"]["autonomous"])

    def test_withdrawal_after_model_return_withholds_every_projection(self):
        self.ready()
        tid, p = self.proactive()
        self.assertEqual(p["review_flag"]["status"], "review-suggested")
        reading = p["review_flag"]["readings"][0]["reading_id"]
        self.set_consent("declined")
        shown = {
            "detail": self.request(f"/api/assistants/proposals/{tid}")[1],
            "list": self.request("/api/assistants/proposals?case_id=ZF-1")[1],
            "export": self.service.export(),
            "sensors": self.request("/api/cases/ZF-1/sensors")[1],
        }
        for name, body in shown.items():
            text = json.dumps(body)
            self.assertNotIn(reading, text, name)
            self.assertNotIn("R-ZF-1-", text, name)
            self.assertNotIn("sensor:SENS-SYN-1", text, name)
        detail = shown["detail"]
        self.assertTrue(detail["sensor_withheld"])
        self.assertEqual(detail["review_flag"]["status"], "withheld")
        self.assertEqual(detail["output"]["findings"], [])
        self.assertEqual(shown["sensors"]["state"], "consent-withheld")
        with self.service.transaction() as db:
            stored = db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()[0]
        self.assertIn(reading, stored)

    def test_same_bucket_arrival_is_new_evidence_for_the_model_and_stales_the_old_task(self):
        self.ready()
        first = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertEqual(
            self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"]
        )
        self.assertEqual(
            self.other().invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"]
        )
        self.assertTrue(self.service.execute(first["id"]))
        bucket = int(time.time()) // SEAL * SEAL
        newer = self.add_live(1, base=bucket)
        view = self.request("/api/cases/ZF-1/sensors")[1]
        self.assertEqual(view["latest"]["reading_id"], newer)
        old = self.service.detail(self.pm, first["id"])
        self.assertTrue(old["stale"])
        self.assertEqual(old["review_flag"]["status"], "not-current")
        second = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertNotEqual(second["id"], first["id"])
        self.assertEqual(
            self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], second["id"]
        )
        self.assertTrue(self.service.execute(second["id"]))
        sent = self.provider.prompts[-1]["evidence"]
        self.assertEqual(sent["sources"]["sensors"]["latest"], view["latest"])
        self.assertIn(sensor_view.key_of(view["latest"]), sent["citations"])
        fresh = self.service.detail(self.pm, second["id"])
        self.assertFalse(fresh["stale"])
        self.assertEqual(fresh["snapshot"]["sources"]["sensors"]["latest"], view["latest"])
        self.assertEqual(self.provider.calls, 2)

    def test_scan_does_not_start_new_work_for_each_arrival_in_one_bucket(self):
        self.ready()
        self.proactive()
        before = self.quality_task()
        bucket = int(time.time()) // SEAL * SEAL
        self.add_live(1, base=bucket)
        self.add_live(2, base=bucket)
        self.assertEqual(set(self.service.scan()["enqueued"]) & set(self.quality_task()), set())
        self.assertEqual(self.quality_task(), before)
        self.add_live(0, base=bucket + SEAL)
        self.assertTrue(set(self.service.scan()["enqueued"]) - set(before))

    def test_context_change_makes_the_old_task_stale(self):
        self.ready()
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.service.execute(tid)
        self.add_live(60 * 5)
        self.assertTrue(self.service.detail(self.pm, tid)["stale"])

    def test_manual_completion_then_proactive_scan_stays_manual(self):
        self.ready()
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.assertTrue(self.service.execute(tid))
        with self.service.transaction() as db:
            self.service._enqueue(
                db, "quality-evidence", self.store.detail("ZF-1"), "proactive", "scan"
            )
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(
            (flag["status"], flag["trigger"], flag["autonomous"]),
            ("manual-proposal", "requested", False),
        )

    def test_proactive_completion_then_manual_invocation_keeps_its_attribution(self):
        self.ready()
        tid, _ = self.proactive()
        self.assertEqual(self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], tid)
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual((flag["status"], flag["trigger"]), ("review-suggested", "proactive"))
        self.assertEqual(self.provider.calls, 1)

    def test_person_request_queued_before_dispatch_wins_over_a_scan(self):
        self.ready()
        scanned = self.service.scan()["enqueued"]
        tid = self.quality_task()[0]
        self.assertIn(tid, scanned)
        self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.service.execute(tid)
        self.assertEqual(
            self.service.detail(self.pm, tid)["review_flag"]["status"], "manual-proposal"
        )

    def _after_withdrawal(self, tid):
        return {
            "detail": self.request(f"/api/assistants/proposals/{tid}")[1],
            "list": self.request("/api/assistants/proposals?case_id=ZF-1")[1],
            "export": self.service.export(),
            "sensors": self.request("/api/cases/ZF-1/sensors")[1],
        }

    def test_withdrawal_withholds_uncited_derived_text_and_edited_output(self):
        self.ready(cite=False, leak="23.7")
        tid, p = self.proactive()
        self.assertEqual(p["review_flag"]["status"], "uncited")
        self.assertIn("23.7", json.dumps(p["output"]))
        qa = self.people["Quality Inspector"]
        p = self.service.review(
            qa, tid, "verify", p["revision"], "Compared the sources.", source_verified=True
        )
        edited = dict(p["output"], summary="Edited: indoor 24.9 degC was recorded.")
        p = self.service.review(qa, tid, "edit-accept", p["revision"], "Edited.", edited)
        self.assertIn("24.9", json.dumps(self.request(f"/api/assistants/proposals/{tid}")[1]))
        self.set_consent("declined")
        for name, body in self._after_withdrawal(tid).items():
            text = json.dumps(body)
            for derived in ("23.7", "24.9"):
                self.assertNotIn(derived, text, name)
        shown = self.request(f"/api/assistants/proposals/{tid}")[1]
        self.assertEqual(shown["output"]["findings"], [])
        self.assertTrue(any("edited_output" in e for e in shown["provenance"]))
        self.assertTrue(
            all(not (e.get("edited_output") or {}).get("findings") for e in shown["provenance"])
        )

    def test_declined_unsampled_control_withholds_every_historical_projection(self):
        self.ready()
        tid, p = self.proactive()
        reading = p["review_flag"]["readings"][0]["reading_id"]
        self.set_consent("declined", sensor="SENS-OTHER-9")
        for name, body in self._after_withdrawal(tid).items():
            self.assertNotIn(reading, json.dumps(body), name)
        self.assertEqual(
            self.request(f"/api/assistants/proposals/{tid}")[1]["review_flag"]["status"], "withheld"
        )

    def test_known_signature_is_not_proposed_again_by_scan(self):
        self.ready()
        first = set(self.service.scan()["enqueued"]) & set(self.quality_task())
        self.assertTrue(first)
        again = set(self.service.scan()["enqueued"]) & set(self.quality_task())
        self.assertFalse(again)

    def _unchanged_for_three_seals(self, prepare):
        self.mock()
        prepare()
        self.quality_ready()
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        sig = signature(self.service.detail(self.pm, tid)["snapshot"])
        for hours in (7, 14, 21):
            with self.clock(hours * 3600):
                detail = self.service.detail(self.pm, tid)
                self.assertFalse(detail["stale"], hours)
                self.assertEqual(
                    self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], tid
                )
                self.assertEqual(self.service.scan()["disabled"], None)
                self.assertEqual(self.quality_task(), [tid])
                self.assertEqual(signature(detail["snapshot"]), sig)
        self.assertEqual(self.provider.calls, 0)

    def test_empty_capture_is_stable_across_seals(self):
        self._unchanged_for_three_seals(lambda: self.put(0))

    def test_withheld_capture_is_stable_across_seals(self):
        self._unchanged_for_three_seals(lambda: self.put(3, consent="declined"))

    def test_unavailable_capture_is_stable_across_seals(self):
        self._unchanged_for_three_seals(lambda: None)

    def test_capture_without_sensors_keeps_prior_shape(self):
        c = self.store.detail("ZF-1")
        self.assertNotIn("sensors", capture("quality-evidence", c)["sources"])
        self.assertEqual(
            capture("quality-evidence", c, None, dict(state="unavailable"))["sources"]["sensors"][
                "state"
            ],
            "unavailable",
        )

    def test_unavailable_model_gives_no_flag(self):
        self.mock(bad="template")
        self.put(4)
        self.quality_ready()
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.service.execute(tid)
        self.assertIsNone(self.service.detail(self.pm, tid).get("review_flag"))

    def _roles(self):
        return self.people["Quality Inspector"]

    def _all_text(self, tid):
        return {k: json.dumps(v) for k, v in self._after_withdrawal(tid).items()}

    def test_context_only_capture_reaches_the_model_and_is_withheld_after_withdrawal(self):
        self.mock()
        self.put(0)
        now = int(time.time())
        ref = datetime.fromtimestamp(now - 500 * 86400, UTC).replace(microsecond=0)
        self.add_readings(2, base=int(ref.timestamp()), offset=3600, tag="OLD")
        self.quality_ready()
        with patch.object(sensor_view, "reference_for", return_value=ref):
            api = self.request("/api/cases/ZF-1/sensors")[1]
            tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
            self.assertTrue(self.service.execute(tid))
            sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
            self.assertEqual(sent["before"], api["before"])
            self.assertEqual(api["state"], "ok")
            self.assertTrue(api["before"])
            self.assertIn("OLD-ZF-1-000", json.dumps(self.service.detail(self.pm, tid)))
            self.set_consent("declined")
            for name, text in self._all_text(tid).items():
                self.assertNotIn("OLD-ZF-1-", text, name)
            shown = self.request(f"/api/assistants/proposals/{tid}")[1]
            self.assertTrue(shown["sensor_withheld"])
            self.assertEqual(shown["review_flag"]["status"], "withheld")

    def _verified_note_flow(self):
        self.ready()
        tid, p = self.proactive()
        reading = p["review_flag"]["readings"][0]["reading_id"]
        value = p["snapshot"]["sources"]["sensors"]["readings"][0]["temperature_c"]
        qa = self._roles()
        note = f"Checked {reading} at {value} degC against the photo."
        p = self.service.review(qa, tid, "verify", p["revision"], note, source_verified=True)
        edited = dict(p["output"], summary="Reviewed summary without readings.")
        self.service.review(qa, tid, "edit-accept", p["revision"], f"Accepted {reading}.", edited)
        return tid, reading, note

    def test_review_notes_are_withheld_with_consent_and_return_when_it_does(self):
        tid, reading, note = self._verified_note_flow()
        self.assertIn(note, json.dumps(self.request(f"/api/assistants/proposals/{tid}")[1]))
        self.set_consent("declined")
        for name, text in self._all_text(tid).items():
            self.assertNotIn(reading, text, name)
            self.assertNotIn("degC against the photo", text, name)
        self.set_consent("granted")
        shown = self.request(f"/api/assistants/proposals/{tid}")[1]
        self.assertIn(note, json.dumps(shown))
        self.assertEqual(shown["review"]["note"], f"Accepted {reading}.")

    def test_reject_after_withdrawal_keeps_the_stored_snapshot_and_output(self):
        self.ready()
        tid, p = self.proactive()
        reading = p["review_flag"]["readings"][0]["reading_id"]
        self.set_consent("declined")
        shown = self.request(f"/api/assistants/proposals/{tid}")[1]
        self.assertTrue(shown["sensor_withheld"])
        with self.service.transaction() as db:
            before = json.loads(
                db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()[0]
            )
        self.service.review(self._roles(), tid, "reject", shown["revision"], "Not relied on.")
        with self.service.transaction() as db:
            after = json.loads(
                db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()[0]
            )
        self.assertEqual(after["snapshot"], before["snapshot"])
        self.assertEqual(after["output"], before["output"])
        self.assertIn(reading, json.dumps(after["snapshot"]))
        self.assertEqual(after["review"]["action"], "reject")
        self.assertNotIn(reading, json.dumps(self.request(f"/api/assistants/proposals/{tid}")[1]))
        self.set_consent("granted")
        restored = self.request(f"/api/assistants/proposals/{tid}")[1]
        self.assertEqual(restored["output"], before["output"])
        self.assertIn(reading, json.dumps(restored["snapshot"]))
        self.assertNotIn("sensor_withheld", restored)

    def test_verification_and_acceptance_are_refused_while_consent_is_withheld(self):
        self.ready()
        tid, p = self.proactive()
        self.set_consent("declined")
        shown = self.request(f"/api/assistants/proposals/{tid}")[1]
        with self.assertRaises((PermissionError, ValueError)):
            self.service.review(
                self._roles(), tid, "verify", shown["revision"], "Looked.", source_verified=True
            )

    def _scan_counts(self):
        quality_ids = self.quality_task()
        bucket = int(time.time()) // SEAL * SEAL
        for minute in (1, 2, 3):
            self.add_live(minute, base=bucket)
            self.service.scan()
        forecast = {a["id"]: a for a in self.service.forecast(self.pm)["assistants"]}
        return quality_ids, self.quality_task(), forecast["quality-evidence"]["new_proposals"]

    def _gap_case(self, prepare):
        self.mock()
        self.put(4)
        self.add_live(10)
        prepare()
        self.service.scan()
        first = self.quality_task()
        self.assertEqual(len(first), 1)
        self.assertTrue(self.service.execute(first[0]))
        self.assertEqual(self.provider.calls, 1)
        _, after, new = self._scan_counts()
        self.assertEqual(after, first)
        self.assertEqual(new, 0)
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.assertNotEqual(tid, first[0])
        self.assertTrue(self.service.execute(tid))
        self.assertEqual(
            self.service.detail(self.pm, tid)["review_flag"]["status"], "manual-proposal"
        )
        return first

    def _measures_only(self):
        with self.store.lock:
            supplied_resident_fixture(self.store._case("ZF-1"))
            self.store.save()

    def _submitted_only(self):
        self._measures_only()
        items = {
            label: "SYN current photo"
            for label in quality.checklist_for("Loft insulation")["items"]
        }
        self.store.submit_quality(
            self.pm,
            "ZF-1",
            "Loft insulation",
            "SYN installer",
            "Installer",
            items,
            context_revision=1,
        )

    def test_throttle_applies_with_no_measures(self):
        self._gap_case(lambda: None)

    def test_throttle_applies_with_measures_and_no_quality_record(self):
        self._gap_case(self._measures_only)

    def test_throttle_applies_with_an_unaccepted_quality_record(self):
        first = self._gap_case(self._submitted_only)
        self.store.accept_quality(self.people["Quality Inspector"], "ZF-1", 0)
        self.assertTrue(set(self.service.scan()["enqueued"]) - set(first))

    def test_a_manual_request_after_many_events_is_not_labelled_proactive(self):
        self.ready()
        self.service.scan()
        tid = self.quality_task()[0]
        case = self.store.detail("ZF-1")
        with self.service.transaction() as db:
            for _ in range(60):
                self.service._enqueue(db, "quality-evidence", case, "proactive", "scan")
        self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertTrue(self.service.execute(tid))
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual((flag["status"], flag["trigger"]), ("manual-proposal", "requested"))

    def test_unknown_dispatch_authority_is_requested_not_proactive(self):
        self.ready()
        self.service.scan()
        tid = self.quality_task()[0]
        with self.service.transaction() as db:
            body = json.loads(
                db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()[0]
            )
            body.pop("manual_requested", None)
            db.execute("UPDATE assistant_tasks SET body=? WHERE id=?", (ta.canonical(body), tid))
        self.assertTrue(self.service.execute(tid))
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual((flag["status"], flag["trigger"]), ("manual-proposal", "requested"))

    def _tasks_of(self, cap):
        with self.service.transaction() as db:
            rows = db.execute(
                "SELECT id FROM assistant_tasks WHERE capability=? AND case_id='ZF-1' ORDER BY id",
                (cap,),
            ).fetchall()
        return [r[0] for r in rows]

    def _new(self, cap):
        found = {a["id"]: a for a in self.service.forecast(self.pm)["assistants"]}
        return found[cap]["new_proposals"]

    def _release(self, name):
        return patch.object(
            self.service,
            "release_reference",
            side_effect=lambda db, cap: dict(id=name, capability=cap),
        )

    def _epoch(self):
        """A later epoch with no suspension; only the epoch the schedule reads changes."""
        real = self.service.continuity
        stack = contextlib.ExitStack()
        stack.enter_context(
            patch.object(
                self.service,
                "continuity",
                side_effect=lambda db: dict(real(db), epoch=real(db)["epoch"] + 1),
            )
        )
        stack.enter_context(patch.object(self.service, "suspended", return_value=None))
        return stack

    def test_release_or_epoch_change_offers_fresh_work_for_an_unchanged_case(self):
        self.ready()
        caps = ("quality-evidence", "assessment-preparation")
        for name, scope in (("release", lambda: self._release("REL-2")), ("epoch", self._epoch)):
            with self.subTest(change=name):
                self.service.scan_cursor = ""
                self.service.scan()
                had = {cap: len(self._tasks_of(cap)) for cap in caps}
                self.assertTrue(all(n >= 1 for n in had.values()))
                self.assertEqual([self._new(cap) for cap in caps], [0, 0])
                with scope():
                    self.assertTrue(all(self._new(cap) >= 1 for cap in caps))
                    for _ in range(2):
                        self.service.scan_cursor = ""
                        self.service.scan()
                        self.assertEqual(
                            {cap: len(self._tasks_of(cap)) for cap in caps},
                            {cap: n + 1 for cap, n in had.items()},
                        )
                    self.assertEqual([self._new(cap) for cap in caps], [0, 0])

    def _set_epc(self, value):
        with self.store.lock:
            self.store._case("ZF-1")["home"]["epc"] = value
            self.store.save()

    def test_non_sensor_a_b_a_with_a_new_reading_is_new_work_but_sensor_only_is_throttled(self):
        self.ready()
        original = self.store.detail("ZF-1")["home"].get("epc")
        self.service.scan()
        self.assertEqual(len(self.quality_task()), 1)
        self._set_epc("Z")
        with self.clock(10):
            self.service.scan()
        self.assertEqual(len(self.quality_task()), 2)
        self._set_epc(original)
        self.add_live(5)
        with self.clock(20):
            self.assertEqual(self._new("quality-evidence"), 1)
            self.service.scan()
        self.assertEqual(len(self.quality_task()), 3)
        self.add_live(4)
        with self.clock(30):
            self.assertEqual(self._new("quality-evidence"), 0)
            self.service.scan()
        self.assertEqual(len(self.quality_task()), 3)

    def _used_calls(self):
        with self.service.transaction() as db:
            row = db.execute("SELECT SUM(used_calls) FROM assistant_allowance").fetchone()
        return row[0] or 0

    def _gated(self, **kw):
        gate = dict(entered=threading.Event(), proceed=threading.Event())
        self.mock(gate=gate, **kw)
        return gate

    def test_a_request_during_an_in_flight_proactive_call_does_not_relabel_it(self):
        gate = self._gated()
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        (tid,) = self.quality_task()
        worker = threading.Thread(target=self.service.execute, args=(tid,))
        worker.start()
        try:
            self.assertTrue(gate["entered"].wait(20))
            self.assertEqual(self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], tid)
        finally:
            gate["proceed"].set()
            worker.join(30)
        shown = self.service.detail(self.pm, tid)
        self.assertEqual(shown["review_flag"]["status"], "review-suggested")
        self.assertEqual(self.provider.calls, 1)
        claimed = [e for e in shown["provenance"] if e.get("kind") == "claimed"]
        self.assertEqual({e["trigger"] for e in claimed}, {"proactive"})

    def test_a_request_before_claim_is_manual_and_a_retry_follows_the_flag_at_its_own_claim(self):
        self.mock(fail=1)
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        for requested in (False, True):
            with self.subTest(requested=requested):
                self.provider.fail = 1
                with self.service.transaction() as db:
                    db.execute("DELETE FROM assistant_attempts")
                    db.execute("DELETE FROM assistant_tasks")
                self.service.scan()
                (tid,) = self.quality_task()
                self.assertTrue(self.service.execute(tid))
                self.assertEqual(self.service.detail(self.pm, tid)["state"], "pending")
                if requested:
                    self.service.invoke(self.pm, "quality-evidence", "ZF-1")
                with self.clock(3600 * (2 if requested else 1)):
                    self.assertTrue(self.service.execute(tid))
                want = "manual-proposal" if requested else "review-suggested"
                self.assertEqual(self.service.detail(self.pm, tid)["review_flag"]["status"], want)

    def test_old_anchor_wording_names_both_horizons_in_the_ui_and_the_model(self):
        self.mock()
        self.put(0)
        now = int(time.time())
        ref = datetime.fromtimestamp(now - 500 * 86400, UTC).replace(microsecond=0)
        self.add_readings(2, base=int(ref.timestamp()), offset=3600, tag="OLD")
        self.quality_ready()
        with patch.object(sensor_view, "reference_for", return_value=ref):
            api = self.request("/api/cases/ZF-1/sensors")[1]
            tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
            self.assertTrue(self.service.execute(tid))
        sent = self.provider.prompts[-1]["evidence"]
        rule = sent["sources"]["sensors"]["as_of_rule"]
        self.assertEqual(api["as_of_rule"], rule)
        self.assertIn("newest readings", rule)
        self.assertIn("within the last 366 days", rule)
        self.assertIn("within 30 days of the quality evidence record time", rule)
        self.assertIn("may be older than 366 days", rule)
        self.assertEqual(
            sorted(k for k in sent["citations"] if k.startswith("sensor:")),
            sorted(sensor_view.citations(api)),
        )

    def _ready_one(self, **kw):
        self.mock(**kw)
        self.put(4)
        self.add_live(10)
        self.quality_ready()

    def view_latest(self):
        return self.request("/api/cases/ZF-1/sensors")[1]["latest"]["reading_id"]

    def test_exact_a_b_a_return_requeues_the_stale_task_within_the_allowance(self):
        self._ready_one()
        original = self.store.detail("ZF-1")["home"].get("epc")
        self.service.scan()
        (first,) = self.quality_task()
        self._set_epc("Z")
        self.assertFalse(self.service.execute(first))
        self.assertEqual(self.service.detail(self.pm, first)["state"], "stale")
        self.service.scan()
        self._set_epc(original)
        self.assertEqual(self._new("quality-evidence"), 1)
        self.assertIn(first, self.service.scan()["enqueued"])
        self.assertEqual(self.service.detail(self.pm, first)["state"], "pending")
        self.assertTrue(self.service.execute(first))
        self.assertEqual((self.provider.calls, self._used_calls()), (1, 1))
        self.assertEqual(self.service.detail(self.pm, first)["state"], "ready")

    def test_exact_a_b_a_return_is_requeued_by_a_manual_request_and_for_other_assistants(self):
        self._ready_one()
        original = self.store.detail("ZF-1")["home"].get("epc")
        first = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self._set_epc("Z")
        self.assertFalse(self.service.execute(first))
        self._set_epc(original)
        again = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertEqual((again["id"], again["state"]), (first, "pending"))
        other = "assessment-preparation"
        mine = self.service.invoke(self.pm, other, "ZF-1")["id"]
        self._set_epc("Y")
        self.assertFalse(self.service.execute(mine))
        self._set_epc(original)
        back = self.service.invoke(self.pm, other, "ZF-1")
        self.assertEqual((back["id"], back["state"]), (mine, "pending"))

    def test_sensor_churn_before_claim_is_one_task_one_dispatch_and_survives_restart(self):
        self._ready_one()
        self.service.scan()
        (first,) = self.quality_task()
        for minute in (9, 8, 7, 6, 5):
            self.add_live(minute)
            self.service.scan_cursor = ""
            self.service.scan()
        self.assertEqual(self.quality_task(), [first])
        self.assertEqual(self._new("quality-evidence"), 0)
        self.assertFalse(self.service.execute(first))
        (second,) = set(self.quality_task()) - {first}
        self.assertTrue(self.service.execute(second))
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]["latest"]
        self.assertEqual(sent["reading_id"], self.view_latest())
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self.quality_task()), 2)
        self.assertEqual((self.provider.calls, self._used_calls()), (1, 1))

    def test_a_new_reading_keeps_the_returned_flag_with_a_newer_readings_note(self):
        self._ready_one()
        tid, p = self.proactive()
        self.assertEqual(p["review_flag"]["status"], "review-suggested")
        before = self.quality_task()
        self.add_live(5)
        shown = self.service.detail(self.pm, tid)
        flag = shown["review_flag"]
        self.assertTrue(shown["stale"])
        self.assertFalse(shown["actionable"])
        self.assertEqual((flag["status"], flag["autonomous"]), ("review-suggested", True))
        self.assertIs(flag["newer_readings"], True)
        self.service.scan_cursor = ""
        self.assertEqual(set(self.service.scan()["enqueued"]) & set(before), set())
        self.assertEqual(self.quality_task(), before)
        self.assertEqual(self.provider.calls, 1)

    def test_withdrawal_between_claim_and_dispatch_sends_nothing(self):
        self._ready_one()
        self.service.scan()
        (tid,) = self.quality_task()
        real = self.service.claim

        def claim(task, owner):
            got = real(task, owner)
            self.set_consent("declined")
            return got

        with patch.object(self.service, "claim", side_effect=claim):
            self.service.execute(tid)
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(self.provider.prompts, [])

    def test_withdrawal_after_the_pre_dispatch_check_sends_nothing(self):
        self._ready_one()
        self.service.scan()
        (tid,) = self.quality_task()
        outer = self

        class Barrier:
            def __init__(self, real):
                self.real = real

            def __enter__(self):
                outer.set_consent("declined")
                return self.real.__enter__()

            def __exit__(self, *a):
                return self.real.__exit__(*a)

        with patch.object(self.service, "dispatch_lock", Barrier(self.service.dispatch_lock)):
            self.service.execute(tid)
        self.assertEqual(self.provider.calls, 0)

    def test_withdrawal_during_a_started_call_is_withheld_everywhere(self):
        gate = self._gated()
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        (tid,) = self.quality_task()
        worker = threading.Thread(target=self.service.execute, args=(tid,))
        worker.start()
        try:
            self.assertTrue(gate["entered"].wait(20))
            self.set_consent("declined")
        finally:
            gate["proceed"].set()
            worker.join(30)
        reading = self.provider.prompts[0]["evidence"]["sources"]["sensors"]["latest"]["reading_id"]
        for name, body in self._after_withdrawal(tid).items():
            self.assertNotIn(reading, json.dumps(body), name)

    def test_scan_reads_schedule_by_key_with_many_historical_tasks(self):
        self._ready_one()
        self.service.scan()
        (first,) = self.quality_task()
        with self.service.transaction() as db:
            body = db.execute("SELECT body FROM assistant_tasks WHERE id=?", (first,)).fetchone()[0]
            for i in range(300):
                db.execute(
                    "INSERT INTO assistant_tasks (id,capability,case_id,signature,body,state,fence,"
                    "owner,lease_until,attempts,not_before,revision)"
                    " VALUES (?,?,?,?,?,'stale',0,'',0,0,0,1)",
                    (f"old{i:03d}", "quality-evidence", "ZF-1", f"s{i}", body),
                )
        seen = []
        real = self.store.assistant_connection

        class Recording:
            """Backend-neutral statement recorder; SQLite also traces natively."""

            def __init__(self, db):
                self.db = db

            def execute(self, sql, *args):
                seen.append(sql)
                return self.db.execute(sql, *args)

            def __enter__(self):
                self.db.__enter__()
                return self

            def __exit__(self, *exc):
                return self.db.__exit__(*exc)

            def __getattr__(self, name):
                return getattr(self.db, name)

        def traced():
            return Recording(real())

        with patch.object(self.store, "assistant_connection", side_effect=traced):
            self.service.scan_cursor = ""
            self.service.scan()
            self._new("quality-evidence")
        scans = [
            x
            for x in seen
            if "FROM assistant_tasks" in x and "WHERE id=" not in x and "state IN" not in x
        ]
        self.assertEqual(scans, [])
        self.assertEqual(self.quality_task().count(first), 1)

    def test_request_carries_as_of_and_freshness_and_the_flag_repeats_them(self):
        self._ready_one()
        self.service.scan()
        (tid,) = self.quality_task()
        with self.clock(1200):
            self.assertTrue(self.service.execute(tid))
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        self.assertTrue(sent["request_as_of"].endswith("Z"))
        self.assertEqual(sent["freshness"], "stale")
        self.assertGreaterEqual(sent["age_minutes"], 30)
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(flag["freshness"], "stale")
        self.assertEqual(flag["evidence_as_of"], sent["request_as_of"])

    def test_request_marks_missing_sensor_evidence_as_unknown(self):
        self.mock()
        self.put(0)
        self.quality_ready()
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.service.execute(tid)
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        self.assertEqual(sent["freshness"], "unknown")

    # C6: dispatch ordering, immutable identity, upgrade, manual slot, flag display.
    def _withdraw_in_thread(self):
        errors = []

        def withdraw():
            try:
                self.set_consent("declined")
            except Exception as error:  # noqa: BLE001 - recorded and asserted by the caller
                errors.append(error)

        thread = threading.Thread(target=withdraw)
        thread.start()
        return thread, errors

    def _consent_now(self):
        with self.service.transaction() as db:
            return sensor_view.consent(db, "ZF-1", {DEFAULT}, self.service.mssql)

    def test_withdrawal_cannot_commit_between_the_final_check_and_provider_transport(self):
        gate = self._gated()
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        (tid,) = self.quality_task()
        worker = threading.Thread(target=self.service.execute, args=(tid,))
        worker.start()
        try:
            self.assertTrue(gate["entered"].wait(20))
            thread, errors = self._withdraw_in_thread()
            thread.join(1.0)
            self.assertTrue(
                thread.is_alive(), "withdrawal committed while the provider call was in flight"
            )
            self.assertEqual(self._consent_now(), "granted")
        finally:
            gate["proceed"].set()
            worker.join(30)
        thread.join(30)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(self._consent_now(), "declined")
        self.assertEqual(self.provider.calls, 1)
        with self.service.transaction() as db:
            held = db.execute("SELECT COUNT(*) FROM assistant_dispatch_gate").fetchone()[0]
        self.assertEqual(held, 0)

    def test_provider_failure_releases_the_gate_and_an_expired_gate_does_not_block(self):
        self._ready_one(fail=1)
        self.service.scan()
        (tid,) = self.quality_task()
        self.service.execute(tid)
        with self.service.transaction() as db:
            self.assertEqual(
                db.execute("SELECT COUNT(*) FROM assistant_dispatch_gate").fetchone()[0], 0
            )
            db.execute(
                "INSERT INTO assistant_dispatch_gate (home_id,task_id,fence,expires_at)"
                " VALUES ('ZF-1','dead',1,?)",
                (self.service.now(db) - 5,),
            )
        started = time.time()
        self.set_consent("declined")
        self.assertLess(time.time() - started, 5)

    def test_a_gate_that_cannot_be_written_sends_nothing(self):
        self._ready_one()
        self.service.scan()
        (tid,) = self.quality_task()
        with self.service.transaction() as db:
            db.execute("DROP TABLE assistant_dispatch_gate")
        self.service.execute(tid)
        self.assertEqual(self.provider.calls, 0)

    def _two_tasks_after_arrival(self):
        self._ready_one()
        self.service.scan()
        (first,) = self.quality_task()
        self.add_live(5)
        return first

    def test_a_new_capture_in_the_same_schedule_is_its_own_task_and_a_request_reuses_it(self):
        first = self._two_tasks_after_arrival()
        self.assertFalse(self.service.execute(first))
        tasks = self.quality_task()
        self.assertEqual(len(tasks), 2)
        (second,) = set(tasks) - {first}
        old = self.service.detail(self.pm, first)
        self.assertEqual(old["state"], "stale")
        self.assertEqual(signature(old["snapshot"]), old["source_signature"])
        again = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertEqual(again["id"], second)
        self.assertEqual(len(self.quality_task()), 2)
        self.assertTrue(self.service.execute(second))
        done = self.service.detail(self.pm, second)
        self.assertEqual(done["dispatch"]["trigger"], "requested")
        self.assertEqual((self.provider.calls, self._used_calls()), (1, 1))
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]["latest"]
        self.assertEqual(sent["reading_id"], self.view_latest())

    def test_a_request_during_the_lease_of_a_new_capture_reuses_it_and_keeps_provenance(self):
        gate = self._gated()
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        (first,) = self.quality_task()
        self.add_live(5)
        self.assertFalse(self.service.execute(first))
        (second,) = set(self.quality_task()) - {first}
        worker = threading.Thread(target=self.service.execute, args=(second,))
        worker.start()
        try:
            self.assertTrue(gate["entered"].wait(20))
            again = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
            self.assertEqual(again["id"], second)
            self.assertEqual(len(self.quality_task()), 2)
        finally:
            gate["proceed"].set()
            worker.join(30)
        done = self.service.detail(self.pm, second)
        self.assertEqual(done["dispatch"]["trigger"], "proactive")
        self.assertEqual((self.provider.calls, self._used_calls()), (1, 1))

    def test_replacement_is_bounded_without_dispatch_and_recovers_when_stable(self):
        self._ready_one()
        self.service.scan()
        for minute in (9, 8, 7, 6, 5, 4, 3, 2, 1):
            (pending,) = [
                t
                for t in self.quality_task()
                if self.service.detail(self.pm, t)["state"] == "pending"
            ] or [None]
            if pending is None:
                break
            self.add_live(minute)
            self.service.execute(pending)
        self.assertEqual(self.provider.calls, 0)
        self.assertLessEqual(len(self.quality_task()), 5)
        self.service.scan_cursor = ""
        self.service.scan()
        pending = [
            t for t in self.quality_task() if self.service.detail(self.pm, t)["state"] == "pending"
        ]
        self.assertEqual(pending, [])
        with self.clock(400):
            self.service.scan_cursor = ""
            self.service.scan()
            pending = [
                t
                for t in self.quality_task()
                if self.service.detail(self.pm, t)["state"] == "pending"
            ]
            self.assertEqual(len(pending), 1)
            self.assertTrue(self.service.execute(pending[0]))
        self.assertEqual((self.provider.calls, self._used_calls()), (1, 1))
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(
            [
                t
                for t in self.quality_task()
                if self.service.detail(self.pm, t)["state"] == "pending"
            ],
            [],
        )

    def _legacy(self):
        """A pre-upgrade store: tasks exist, the schedule table has no rows."""
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_schedule")

    def test_upgrade_adopts_the_serviced_legacy_task_and_does_not_call_again_in_the_bucket(self):
        self._ready_one()
        tid, _ = self.proactive()
        self._legacy()
        self.add_live(5)
        self.service.scan_cursor = ""
        scanned = self.service.scan()
        self.assertEqual(self.quality_task(), [tid])
        self.assertEqual(self.provider.calls, 1)
        self.assertEqual(set(scanned["enqueued"]) & set(self.quality_task()), set())
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(self.quality_task(), [tid])
        with self.service.transaction() as db:
            rows = db.execute(
                "SELECT COUNT(*) FROM assistant_schedule"
                " WHERE case_id='ZF-1' AND capability='quality-evidence'"
            ).fetchone()[0]
        self.assertEqual(rows, 1)

    def test_upgrade_does_not_adopt_a_legacy_task_from_another_release(self):
        self._ready_one()
        tid, _ = self.proactive()
        self._legacy()
        with self.service.transaction() as db:
            body = json.loads(
                db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()[0]
            )
            body["release"] = "older-release"
            db.execute("UPDATE assistant_tasks SET body=? WHERE id=?", (json.dumps(body), tid))
        self.add_live(5)
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self.quality_task()), 2)

    def test_upgrade_makes_a_source_change_after_a_legacy_assessment_eligible(self):
        self._ready_one()
        cap = "assessment-preparation"
        first = self.service.invoke(self.pm, cap, "ZF-1")["id"]
        self.assertTrue(self.service.execute(first))
        self.service.scan_cursor = ""
        self.service.scan()
        quiet = self._tasks_of(cap)
        self._legacy()
        self._set_epc("Z")
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self._tasks_of(cap)), len(quiet) + 1)

    def test_a_manual_request_completed_before_a_scan_does_not_hide_the_autonomous_flag(self):
        self._ready_one()
        manual = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.assertTrue(self.service.execute(manual))
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(self.quality_task(), [manual])
        self.add_live(5)
        self.service.scan_cursor = ""
        self.assertTrue(set(self.service.scan()["enqueued"]) - {manual})
        (auto,) = set(self.quality_task()) - {manual}
        self.assertTrue(self.service.execute(auto))
        self.assertEqual(
            self.service.detail(self.pm, manual)["review_flag"]["status"], "not-current"
        )
        self.assertEqual(self.service.detail(self.pm, auto)["dispatch"]["trigger"], "proactive")
        self.assertEqual(self.service.detail(self.pm, manual)["dispatch"]["trigger"], "requested")
        self.add_live(4)
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self.quality_task()), 2)
        self.assertEqual((self.provider.calls, self._used_calls()), (2, 2))

    def test_a_manual_request_before_claim_or_after_failure_is_not_autonomous_and_recovers(self):
        self._ready_one(fail=1)
        self.service.scan()
        (first,) = self.quality_task()
        self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.service.execute(first)
        self.assertEqual(self.service.detail(self.pm, first)["dispatch"]["trigger"], "requested")
        self.add_live(5)
        self.service.scan_cursor = ""
        self.service.scan()
        pending = set(self.quality_task()) - {first}
        self.assertEqual(len(pending), 1)
        (auto,) = pending
        self.assertTrue(self.service.execute(auto))
        self.assertEqual(self.service.detail(self.pm, auto)["dispatch"]["trigger"], "proactive")
        self.assertLessEqual(self._used_calls(), 2)

    def test_flag_reports_matching_and_changed_readings_since_capture(self):
        self._ready_one()
        tid, p = self.proactive()
        flag = p["review_flag"]
        self.assertIs(flag["changed_since_capture"], False)
        self.assertEqual(flag["newer_reading_count"], 0)
        self.add_live(5)
        flag = self.service.detail(self.pm, tid)["review_flag"]
        # An extra uncited reading is counted apart; the cited rows still hold the same values.
        self.assertIs(flag["changed_since_capture"], False)
        self.assertEqual(flag["newer_reading_count"], 1)
        self.assertEqual(flag["status"], "review-suggested")

    def test_delayed_claim_flag_states_the_captured_as_of_and_unknown_is_explicit(self):
        self._ready_one()
        self.service.scan()
        (tid,) = self.quality_task()
        with self.clock(1200):
            self.assertTrue(self.service.execute(tid))
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(flag["freshness"], "stale")
        self.assertGreaterEqual(flag["age_minutes"], 30)
        self.assertTrue(flag["evidence_as_of"].endswith("Z"))


MSSQL = unittest.skipUnless(
    os.environ.get("ZF_TEST_MSSQL") == "1", "needs disposable SQL Server (ZF_TEST_MSSQL=1)"
)


@MSSQL
class MssqlReadModel(ta.MssqlFixture, ReadModel):
    def test_actual_store_is_sql_server(self):
        from zava_forward.core.mssqlstore import MssqlStore

        self.assertIsInstance(self.store, MssqlStore)
        self.assertTrue(self.service.mssql)


@MSSQL
class MssqlHttp(ta.MssqlFixture, Http):
    pass


class AccountSummaryName(unittest.TestCase):
    def test_account_summary_name_starts_with_visible_text(self):
        from pathlib import Path

        web = Path(sensor_view.__file__).parents[4] / "api/src/zava_forward/api/web"
        js = (web / "app.js").read_text(encoding="utf-8")
        self.assertIn('"aria-label", `${short}, your account`', js)
        self.assertIn('getElementById("account-short").textContent = short', js)


class WebWording(unittest.TestCase):
    """Static checks of the shipped web source; a rendered browser check is a separate gate."""

    def _web(self, name):
        from pathlib import Path

        root = Path(sensor_view.__file__).parents[4] / "api/src/zava_forward/api/web"
        return (root / name).read_text(encoding="utf-8")

    def test_sensor_panel_says_current_capture_not_the_models_capture(self):
        js = self._web("ops.js")
        self.assertNotIn("The Quality evidence assistant reads these same readings", js)
        self.assertNotIn("in the same capture the assistant uses", js)
        self.assertIn("current authorised capture", js)

    def test_flag_block_shows_captured_as_of_freshness_age_and_changes(self):
        js = self._web("assistants.js")
        for token in (
            "evidence_as_of",
            "freshness",
            "age_minutes",
            "changed_since_capture",
            "newer_reading_count",
        ):
            self.assertIn(token, js)

    def test_stale_review_suggested_flag_stays_in_the_main_path_and_counts_as_waiting(self):
        js = self._web("assistants.js")
        self.assertIn('p.review_flag?.status === "review-suggested"', js)
        self.assertIn("review_flag", self._web("case-workspace.js"))


if __name__ == "__main__":
    unittest.main()
