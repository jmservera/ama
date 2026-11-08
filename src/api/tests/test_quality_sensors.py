"""Retained readings: bounded read model, API and Quality evidence (issue 1288, C1 and C2).

The model provider here is a local MOCK that records the request it receives. These prove which
retained values reach the model request and how a returned output is cited and projected. They are
not evidence that a real model ran, and nothing here accepts quality work. Seed rows follow the
actual retained contract (sensor consumer controls, live simulator and backfill row shapes).
"""

import dataclasses
import json
import os
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

    def __init__(self, cite=True, leak=None, **kw):
        super().__init__(**kw)
        self.cite, self.leak, self.prompts = cite, leak, []

    def evidence(self, system, prompt, max_tokens, timeout):
        self.prompts.append(json.loads(prompt))
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
            if "sensor_consumer_control_home" in s:
                self.assertIn("WHERE home_id=?", s)
                self.assertTrue("FETCH NEXT" in s or "LIMIT" in s, s)
            else:
                self.assertIn("WHERE sensor_id=?", s)
        readings = [s for s in statements if "FROM sensor_reading" in s]
        self.assertTrue(readings)
        for s in readings:
            self.assertIn("home_id=?", s)
            self.assertIn("observed_at<?", s)
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


if __name__ == "__main__":
    unittest.main()
