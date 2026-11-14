"""Local engineering evidence: UI-displayed readings versus the Quality model request (issue 1288).

Everything here uses a local MOCK model provider and a constructed fixture store. It is not live
simulator, IoT Hub, Azure or real-model evidence (acceptance criterion 8 stays a separate gate). The
tests correlate what the employee read model and UI source present with the request the Quality
assistant sends, and the states for missing, stale, unavailable and failed paths.
"""

import json
import re
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core import sensor_view

import test_assistants as ta
import test_quality_sensors as qs

WEB = Path(sensor_view.__file__).parents[4] / "api/src/zava_forward/api/web"
READING_FIELDS = ("reading_id", "sensor_id", "temperature_c", "humidity_pct", "observed_at")


class Correlation(qs.Seed, ta.ApiTests):
    def request(self, path: str, body: Any = None) -> tuple[int, Any]:
        base_request: Callable[..., tuple[int, Any]] = super().request
        return base_request(path, body)

    def ready(self, **kw: Any) -> None:
        self.mock(**kw)
        self.put(4)
        self.add_live(10)
        self.quality_ready()

    def flag(self) -> tuple[str, Any]:
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        return tid, self.service.detail(self.pm, tid)

    def test_ui_values_ids_and_evidence_equal_the_model_request(self) -> None:
        self.ready()
        status, api = self.request("/api/cases/ZF-1/sensors")
        self.assertEqual((status, api["state"]), (200, "ok"))
        tid, task = self.flag()
        sent = self.provider.prompts[-1]["evidence"]["sources"]
        shown = {r["reading_id"]: r for r in api["readings"]}
        sent_rows = {r["reading_id"]: r for r in sent["sensors"]["readings"]}
        self.assertTrue(shown)
        self.assertEqual(set(shown), set(sent_rows))
        for rid, row in shown.items():
            for field in READING_FIELDS:
                self.assertEqual(row[field], sent_rows[rid][field], (rid, field))
            self.assertTrue(row["observed_at"].endswith("Z"))
        self.assertEqual(api["latest"]["reading_id"], sent["sensors"]["latest"]["reading_id"])
        self.assertEqual(api["latest"]["temperature_c"], sent["sensors"]["latest"]["temperature_c"])
        self.assertEqual(api["freshness"], sent["sensors"]["freshness"])
        self.assertEqual(api["retrofit_context"], sent["sensors"]["retrofit_context"])
        # Bounded checklist and document evidence travels in the same inert snapshot.
        self.assertTrue({"sensors"} < set(sent))
        stored = task["snapshot"]["sources"]["sensors"]
        self.assertEqual(sensor_view.citations(stored), sensor_view.citations(sent["sensors"]))
        self.assertEqual(
            {k: v for k, v in task["snapshot"]["citations"].items() if k.startswith("sensor:")},
            {
                k: v
                for k, v in task["snapshot"]["citations"].items()
                if k in sensor_view.citations(sent["sensors"])
            },
        )
        for key in set(sent) - {"sensors"}:
            self.assertEqual(task["snapshot"]["sources"][key], sent[key], key)
        blob = json.dumps(self.provider.prompts[-1])
        for secret in ("PRIVATE-VULNERABILITY-REASON", "PRIVATE-HANDOFF-NOTE"):
            self.assertNotIn(secret, blob)

    def test_retrofit_context_is_stated_missing_in_api_snapshot_and_ui_source(self) -> None:
        self.ready()
        api = self.request("/api/cases/ZF-1/sensors")[1]
        self.assertIs(api["retrofit_context"]["available"], False)
        self.assertIn("No installation date", api["retrofit_context"]["text"])
        self.flag()
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        self.assertIs(sent["retrofit_context"]["available"], False)
        ops = (WEB / "ops.js").read_text(encoding="utf-8")
        self.assertIn("v.retrofit_context.text", ops)
        for field in READING_FIELDS:
            self.assertIn(field, ops)
        self.assertIn("v.provenance", ops)
        self.assertIn("v.freshness", ops)

    def test_weather_derived_live_rows_keep_their_own_provenance_label(self) -> None:
        self.ready()
        api = self.request("/api/cases/ZF-1/sensors")[1]
        classes = {r["provenance_class"] for r in api["readings"]}
        self.assertGreaterEqual(len(classes), 2, classes)
        for cls in classes:
            self.assertTrue(api["provenance"][cls])
        self.assertEqual(len({api["provenance"][c] for c in classes}), len(classes))

    def test_role_denial_reaches_neither_the_read_model_nor_the_snapshot(self) -> None:
        self.ready()
        self.user = self.people["Programme Support Officer"]
        self.assertEqual(self.request("/api/cases/ZF-1/sensors")[0], 403)
        status = self.request("/api/assistants/quality-evidence/invoke", dict(case_id="ZF-1"))[0]
        self.assertEqual(status, 403)
        self.assertEqual(self.provider.prompts, [])
        self.assertEqual(self.quality_task(), [])

    def test_read_model_is_bounded_and_generates_nothing(self) -> None:
        self.mock()
        self.put(4)
        self.add_readings(400, tag="BULK", offset=10 * 3600)
        with self.service.transaction() as db:
            before = db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]
        api = self.request("/api/cases/ZF-1/sensors")[1]
        self.assertLessEqual(len(api["readings"]), api["max_readings"]["window"])
        with self.service.transaction() as db:
            after = db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]
        self.assertEqual(before, after)

    def test_burst_of_five_minute_readings_and_restart_make_one_flag_and_one_call(self) -> None:
        self.ready()
        tid, first = self.flag()
        self.assertEqual(first["review_flag"]["status"], "review-suggested")
        for minute in (9, 8, 7, 6):
            self.add_live(minute)
            self.service.scan_cursor = ""
            self.service.scan()
        restarted = self.other()
        restarted.scan()
        restarted.scan_cursor = ""
        restarted.scan()
        self.assertEqual(self.quality_task(), [tid])
        self.assertEqual(self.provider.calls, 1)
        flag = restarted.detail(self.pm, tid)["review_flag"]
        self.assertEqual((flag["status"], flag["trigger"]), ("review-suggested", "proactive"))
        self.assertTrue(flag["autonomous"] and flag["unapproved"])
        self.assertEqual(flag["model"]["model"], "test-model")

    def test_fresh_service_keeps_flag_status_and_a_new_release_marks_it_not_current(self) -> None:
        # The H0 note: equal status on a fresh service needs the same synthetic release and epoch.
        self.ready()
        tid, first = self.flag()
        fresh = self.other()
        same = fresh.detail(self.pm, tid)["review_flag"]
        self.assertEqual(same["status"], first["review_flag"]["status"])
        self.assertEqual(same["sensor_cited_ids"], first["review_flag"]["sensor_cited_ids"])
        with self.service.transaction() as db:
            released = self.service.release_reference(db, "quality-evidence")
        self.assertTrue(released)
        with patch.object(
            fresh,
            "release_reference",
            side_effect=lambda db, cap: dict(id="REL-OTHER", capability=cap),
        ):
            other = fresh.detail(self.pm, tid)["review_flag"]
        self.assertEqual(other["status"], "not-current")
        self.assertFalse(other["autonomous"])
        self.assertTrue(other["unapproved"])

    def test_flag_never_approves_and_leaves_human_acceptance_untouched(self) -> None:
        self.ready()
        tid, task = self.flag()
        flag = task["review_flag"]
        self.assertTrue(flag["unapproved"])
        self.assertIn("No named recipient", flag["delivery"])
        self.assertNotEqual(task["state"], "accepted")
        case = self.store.detail("ZF-1")
        before = json.dumps(case.get("quality"), sort_keys=True, default=str)
        self.service.scan()
        self.assertEqual(
            json.dumps(self.store.detail("ZF-1").get("quality"), sort_keys=True, default=str),
            before,
        )
        text = json.dumps(flag)
        for word in ("payment authorised", "consent granted", "defect closed"):
            self.assertNotIn(word, text)

    def test_stale_readings_are_stated_stale_and_still_reach_the_model_as_stale(self) -> None:
        self.mock()
        self.put(4, offset=3 * 86400)
        self.quality_ready()
        api = self.request("/api/cases/ZF-1/sensors")[1]
        self.assertNotEqual(api["freshness"], "fresh")
        self.assertTrue(api["freshness_text"])
        tid = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.service.execute(tid)
        sent = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        self.assertEqual(sent["freshness"], api["freshness"])

    def test_missing_and_unavailable_states_give_a_manual_route_and_no_zero(self) -> None:
        self.mock()
        api = self.request("/api/cases/ZF-1/sensors")[1]
        self.assertNotEqual(api["state"], "ok")
        self.assertTrue(api["manual_route"])
        self.assertFalse(api.get("latest"))
        self.assertFalse(api.get("readings"))
        text = json.dumps(api)
        self.assertNotRegex(text, r'"(temperature_c|humidity_pct)": ?"?0(\.0)?"?[,}]')

    def test_model_failure_gives_no_flag_and_no_fixture_labelled_as_ai(self) -> None:
        self.mock(bad="template")
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        for tid in self.quality_task():
            self.service.execute(tid)
            task = self.service.detail(self.pm, tid)
            self.assertIsNone(task.get("review_flag"))
            self.assertNotEqual(task["envelope"].get("source"), "ai")

    def test_ui_source_labels_the_flag_with_attribution_and_human_route(self) -> None:
        js = (WEB / "assistants.js").read_text(encoding="utf-8")
        for token in (
            "review_flag",
            "f.readings",
            "f.cited_ids",
            "f.model",
            "f.effect",
            "f.delivery",
            "f.source_time",
        ):
            self.assertIn(token, js)
        self.assertTrue(re.search(r"review-suggested", js))


if __name__ == "__main__":
    unittest.main()
