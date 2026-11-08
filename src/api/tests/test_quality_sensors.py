"""Retained readings: bounded read model, API and Quality evidence (issue 1288, correction 1).

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

    def __init__(self, cite=True, **kw):
        super().__init__(**kw)
        self.cite, self.prompts = cite, []

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
        result["text"] = ta.canonical(value)
        return result


class Seed:
    def setUp(self):
        super().setUp()
        self.controls = {}
        with self.service.transaction() as db:
            for table in ("sensor_reading", "sensor_consumer_control", "sensor_consumer_policy"):
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
        self.assertTrue(all("WHERE sensor_id=?" in s for s in controls), controls)
        readings = [s for s in statements if "FROM sensor_reading" in s]
        self.assertTrue(readings)
        self.assertTrue(
            all("home_id=?" in s and "FETCH NEXT" in s or "LIMIT" in s for s in readings)
        )
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

    def test_dedupe_restart_bucket_and_fresh_evidence(self):
        self.ready()
        first = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertEqual(
            self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"]
        )
        self.assertEqual(
            self.other().invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"]
        )
        bucket = int(time.time()) // SEAL * SEAL
        newer = self.add_live(1, base=bucket)
        with self.service.transaction() as db:
            snap = self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))
        # A fresh reading in the same bucket reaches the evidence without another request.
        self.assertEqual(snap["sources"]["sensors"]["latest"]["reading_id"], newer)
        self.assertFalse(self.service.detail(self.pm, first["id"])["stale"])
        self.assertEqual(
            self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"]
        )
        # A reading in a later six-hour bucket is a substantive change.
        self.add_live(0, base=bucket + SEAL, sensor=DEFAULT)
        self.assertTrue(self.service.detail(self.pm, first["id"])["stale"])
        self.assertNotEqual(
            self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"]
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


if __name__ == "__main__":
    unittest.main()
