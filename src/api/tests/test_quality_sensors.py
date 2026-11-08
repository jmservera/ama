"""Retained indoor readings: bounded read model, API and Quality evidence (issue 1288).

The model provider here is a local MOCK that records the request it receives. These prove which
retained values reach the model request and how a returned output is cited and flagged. They are not
evidence that a real model ran, and nothing here accepts quality work.
"""

import json
import time
import unittest
from datetime import UTC, datetime

import release_support
from dataset import supplied_resident_fixture
from zava_forward.core import quality, sensor_view
from zava_forward.core.assistants import capture, digest
from zava_forward.core.sensor_consumer import READING_COLUMNS

import test_assistants as ta

SEAL = sensor_view.SEAL_SECONDS


def stamp(seconds):
    return datetime.fromtimestamp(seconds, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class CapturingProvider(ta.Provider):
    """Mock: cites the first retained reading in the evidence it was given."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.prompts = []

    def evidence(self, system, prompt, max_tokens, timeout):
        self.prompts.append(json.loads(prompt))
        sensors = self.prompts[-1]["evidence"]["citations"]
        cited = sorted(k for k in sensors if k.startswith("sensor:"))[:2] or ["source:home"]
        result = super().evidence(system, prompt, max_tokens, timeout)
        value = json.loads(result["text"])
        value["findings"] = [
            dict(
                text="Cited retained readings are supplied evidence for a person to review.",
                citations=cited,
            )
        ]
        result["text"] = ta.canonical(value)
        return result


class Seed:
    def mock(self, **kw):
        self.provider = self.store.ai = CapturingProvider(**kw)
        release_support.install(self.store)

    def put(self, count=3, consent="granted", home="ZF-1", offset=3 * 3600):
        with self.service.transaction() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS sensor_reading ("
                + ", ".join(f"{c} TEXT" for c in READING_COLUMNS)
                + ", PRIMARY KEY (sensor_id, reading_id))"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS sensor_consumer_control "
                "(sensor_id TEXT PRIMARY KEY, body TEXT NOT NULL)"
            )
            if consent:
                db.execute(
                    "INSERT OR REPLACE INTO sensor_consumer_control VALUES (?,?)",
                    (f"SENS-{home}", ta.canonical(dict(home_id=home, consent=consent))),
                )
        self.add_readings(count, home, offset)

    def add_readings(self, count, home="ZF-1", offset=3 * 3600, tag="R", source="SYNTHETIC"):
        seal = int(time.time()) // SEAL * SEAL
        with self.service.transaction() as db:
            for i in range(count):
                row = dict(
                    sensor_id=f"SENS-{home}",
                    reading_id=f"{tag}-{home}-{i:03d}",
                    home_id=home,
                    observed_at=stamp(seal - offset + i * 60),
                    temperature_c=f"{19 + i * 0.1:.1f}",
                    humidity_pct=f"{50 + i}",
                    source_type=source,
                    scenario="demo",
                    seed="1",
                    schema_version="1",
                    injected_fault="none",
                )
                db.execute(
                    f"INSERT INTO sensor_reading VALUES ({','.join('?' * len(READING_COLUMNS))})",
                    tuple(row[c] for c in READING_COLUMNS),
                )

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
        self.assertLessEqual(len(v["readings"]), sensor_view.WINDOW_MAX)
        self.assertEqual(len(v["readings"]), sensor_view.WINDOW_MAX)
        self.assertEqual(v["units"], dict(temperature_c="degC", humidity_pct="%RH"))
        for r in v["readings"]:
            self.assertTrue(r["observed_at"].endswith("Z"))
            self.assertTrue(r["reading_id"].startswith("R-ZF-1-"))
        self.assertEqual(v["freshness"], "stale")
        self.assertIn("older than 15 minutes", v["freshness_text"])

    def test_read_is_side_effect_free_and_generates_nothing(self):
        self.put(5)

        def count():
            with self.service.transaction() as db:
                return db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]

        before = count()
        self.view()
        self.assertEqual(before, count())
        self.assertEqual(self.provider.calls, 0)

    def test_before_after_context_or_explicit_absence(self):
        self.put(5)
        self.quality_ready()
        v = self.view()
        self.assertTrue(v["reference"])
        self.assertEqual(len(v["before"]), 4)
        self.assertEqual(v["after"], [])
        self.assertIn("onward", v["after_absent"])


class Http(Seed, ta.ApiTests):
    def test_sensors_api_roles_and_values(self):
        self.put(4)
        status, v = self.request("/api/cases/ZF-1/sensors")
        self.assertEqual((status, v["state"], v["case_id"]), (200, "ok", "ZF-1"))
        self.user = self.people["Quality Inspector"]
        self.assertEqual(self.request("/api/cases/ZF-1/sensors")[0], 200)
        for role in ("Contractor", "Unknown"):
            self.user = self.people[role]
            self.assertEqual(self.request("/api/cases/ZF-1/sensors")[0], 403, role)
        self.user = self.pm
        self.assertEqual(self.request("/api/cases/NOPE/sensors")[0], 404)

    def test_same_ids_and_values_reach_model_and_flag(self):
        # MOCK provider: proves the request content and flag shape, not real AI behaviour.
        self.mock()
        self.put(4)
        self.quality_ready()
        api = self.request("/api/cases/ZF-1/sensors")[1]
        p = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        ok = self.service.execute(p["id"])
        p = self.service.detail(self.pm, p["id"])
        self.assertTrue(ok, (p["state"], p.get("reason"), p.get("release_denial")))
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        for key in ("readings", "before", "after"):
            self.assertEqual(sent.get(key, []), api.get(key, []))
        ids = {r["reading_id"] for r in sent["readings"] + sent.get("before", [])}
        flag = p["review_flag"]
        self.assertEqual(flag["level"], "L4")
        self.assertTrue(flag["unapproved"] and flag["sensor_grounded"])
        self.assertTrue(set(flag["reading_ids"]) <= ids and flag["reading_ids"])
        self.assertEqual(flag["model"]["model"], "test-model")
        self.assertNotIn("approved", p["state"])
        sensor_cites = [k for k in p["snapshot"]["citations"] if k.startswith("sensor:")]
        self.assertEqual({k[len("sensor:") :] for k in sensor_cites}, ids)

    def test_no_flag_without_returned_model_output(self):
        self.mock(bad="template")
        self.put(4)
        self.quality_ready()
        p = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.service.execute(p["id"])
        detail = self.service.detail(self.pm, p["id"])
        self.assertIsNone(detail.get("review_flag"))

    def test_dedupe_restart_and_seal(self):
        self.mock()
        self.put(4)
        self.quality_ready()
        first = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        again = self.service.invoke(self.pm, "quality-evidence", "ZF-1")
        self.assertEqual(first["id"], again["id"])
        restarted = self.other()
        self.assertEqual(restarted.invoke(self.pm, "quality-evidence", "ZF-1")["id"], first["id"])
        with self.service.transaction() as db:
            c = self.store.detail("ZF-1")
            live = digest(self.service.snapshot(db, "quality-evidence", c))
        # A reading in the live (unsealed) window never changes the captured source.
        self.add_readings(1, tag="LIVE", offset=-60)
        with self.service.transaction() as db:
            self.assertEqual(
                live,
                digest(self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))),
            )
        # A new reading inside the sealed window does, so the earlier output becomes stale.
        self.add_readings(1, tag="NEW", offset=2 * 3600)
        with self.service.transaction() as db:
            self.assertNotEqual(
                live,
                digest(self.service.snapshot(db, "quality-evidence", self.store.detail("ZF-1"))),
            )

    def test_capture_without_sensors_keeps_prior_shape(self):
        c = self.store.detail("ZF-1")
        self.assertNotIn("sensors", capture("quality-evidence", c)["sources"])
        self.assertEqual(
            capture("quality-evidence", c, None, dict(state="unavailable"))["sources"]["sensors"][
                "state"
            ],
            "unavailable",
        )


if __name__ == "__main__":
    unittest.main()
