"""Retained sensor values in the panel, case chat and Quality review flag (issue 1288).

Local engineering evidence with a MOCK model provider and a constructed fixture store. It proves the
exact retained values, `[sensor:...]` citations and Origin labels, not real model behaviour.
"""

import json
import re
import unittest
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from zava_forward.core import sensor_view
from zava_forward.core.chat_case_answers import answer, sensor_facts
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel
from zava_forward.core.sensor_consumer import READING_COLUMNS

import test_assistants as ta
import test_quality_sensors as qs

WEB = Path(sensor_view.__file__).parents[4] / "api/src/zava_forward/api/web"
CITATION = re.compile(r"\[(sensor:[^\]]+)\]")


class Grounding(qs.Seed, ta.ApiTests):
    def request(self, path: str, body: Any = None) -> tuple[int, Any]:
        base_request: Callable[..., tuple[int, Any]] = super().request
        return base_request(path, body)

    def ready(self) -> None:
        self.mock()
        self.put(4)
        self.add_live(10)
        self.quality_ready()

    def chat(self, question: str) -> tuple[str, list[str]]:
        iso = ChatIsolation(self.store)
        iso.sensors = self.service.sensors
        facts = iso.case_facts(iso.current_user(self.pm), "ZF-1")
        assert facts is not None
        kind, text, cites = answer("ZF-1", question, facts)
        self.assertEqual(kind, "answer")
        return text, cites

    def test_panel_grounding_states_exact_latest_values_and_unretained_variables(self) -> None:
        self.ready()
        view = self.request("/api/cases/ZF-1/sensors")[1]
        latest, grounding = view["latest"], view["grounding"]
        self.assertEqual(grounding["origin"], "decision_rule")
        self.assertEqual(grounding["citation"], sensor_view.key_of(latest))
        self.assertEqual(grounding["provenance_class"], latest["provenance_class"])
        self.assertEqual(grounding["source_text"], view["provenance"][latest["provenance_class"]])
        self.assertEqual(
            grounding["values"],
            dict(
                temperature_c=latest["temperature_c"],
                humidity_pct=latest["humidity_pct"],
                observed_at=latest["observed_at"],
            ),
        )
        self.assertIn(f"[{grounding['citation']}]", grounding["text"])
        self.assertEqual(grounding["not_retained"], ["dew_point_c", "mould_risk_index"])
        self.assertIn("not retained", grounding["not_retained_text"])

    def test_chat_answers_sensor_questions_with_retained_values_and_citations(self) -> None:
        self.ready()
        latest = self.request("/api/cases/ZF-1/sensors")[1]["latest"]
        for question in (
            "What are the sensor readings?",
            "Is the moisture above the threshold?",
            "Any fault flags on the temperature sensor?",
        ):
            with self.subTest(question=question):
                text, cites = self.chat(question)
                key = sensor_view.key_of(latest)
                self.assertIn(f"[{key}]", text)
                self.assertIn(f"temperature_c {latest['temperature_c']} degC", text)
                self.assertIn(f"humidity_pct {latest['humidity_pct']} %RH", text)
                self.assertIn("mould_risk_index", text)
                self.assertTrue(any(c.endswith("sensor.latest.temperature_c") for c in cites))

    def test_chat_does_not_invent_values_when_consent_withheld_or_role_denied(self) -> None:
        self.ready()
        self.set_consent("declined")
        text, cites = self.chat("What are the sensor readings?")
        self.assertNotRegex(text, r"temperature_c \d")
        self.assertIn("no values are shown", text)
        self.assertEqual(sensor_facts({}).get("sensor.latest.citation"), None)
        iso = ChatIsolation(self.store)
        iso.sensors = self.service.sensors
        denied = self.people["Programme Support Officer"]
        facts = iso.case_facts(iso.current_user(denied), "ZF-1") or {}
        self.assertFalse([k for k in facts if k.startswith("sensor.")])

    def test_panel_ask_answers_sensor_questions_from_rules_with_a_model_configured(self) -> None:
        self.ready()
        latest = self.request("/api/cases/ZF-1/sensors")[1]["latest"]
        prompts: list[str] = []

        def model(system: str, prompt: str) -> str:
            prompts.append(prompt)
            return "{}"

        refs = dict(
            CHAT_DPIA_REF="SYN-DPIA",
            CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
            CHAT_NOTICE_REF="SYN-NOTICE",
        )
        iso = ChatIsolation(self.store, env=refs)
        iso.sensors = self.service.sensors
        panel = ChatPanel(iso, model)
        with patch.object(self.store, "ai", SimpleNamespace(consumption=None), create=True):
            self.assert_panel_rules_answers(panel, latest, prompts)

    def assert_panel_rules_answers(
        self, panel: ChatPanel, latest: dict[str, Any], prompts: list[str]
    ) -> None:
        for skill in ("general", "quality-evidence"):
            tid = self.store.chat_create_thread(self.pm, case_id="ZF-1")["id"]
            reply = panel.ask(self.pm, tid, "What are the sensor readings?", skill=skill)
            self.assertEqual(reply["kind"], "answer", skill)
            self.assertIn(f"temperature_c {latest['temperature_c']} degC", reply["reply"])
            self.assertTrue(
                any(c["id"].endswith("sensor.latest.temperature_c") for c in reply["citations"])
            )
            sources = {c["id"]: c["source_kind"] for c in reply["citations"]}
            self.assertEqual(sources["ZF-1/sensor.source"], "decision-rule")
            self.assertEqual(sources["ZF-1/sensor.watch"], "decision-rule")
            self.assertEqual(sources["ZF-1/sensor.latest.temperature_c"], "case-record")
        self.assertEqual(prompts, [])
        denied = self.people["Programme Support Officer"]
        tid = self.store.chat_create_thread(denied, case_id="ZF-1")["id"]
        reply = panel.ask(denied, tid, "What are the sensor readings?")
        self.assertEqual(reply["kind"], "answer")
        self.assertTrue(reply["citations"])
        self.assertNotRegex(reply["reply"], r"temperature_c \d")
        self.assertEqual(prompts, [])

    def test_workflow_questions_naming_moisture_keep_their_intent(self) -> None:
        from zava_forward.core.chat_case_answers import intent

        self.assertEqual(intent("Who owns the moisture hazard?"), "blocked")
        self.assertEqual(intent("Why is this case blocked by moisture?"), "blocked")
        self.assertEqual(intent("Is the moisture above the threshold?"), "sensor")

    def _insert_conflict_at(
        self,
        observed_at: str,
        reading_id: str = "R-CLASH-1",
        temp: str = "24.8",
        humidity: str = "88.0",
        scenario: str = "BACKFILL_2Y",
    ) -> None:
        row = dict(
            sensor_id=qs.DEFAULT,
            reading_id=reading_id,
            home_id="ZF-1",
            observed_at=observed_at,
            temperature_c=temp,
            humidity_pct=humidity,
            source_type="SYNTHETIC",
            scenario=scenario,
            seed="1",
            schema_version="reading-v1",
            injected_fault="none",
        )
        with self.service.transaction() as db:
            db.execute(
                f"INSERT INTO sensor_reading VALUES ({','.join('?' * len(READING_COLUMNS))})",
                tuple(row[c] for c in READING_COLUMNS),
            )

    def test_quality_review_flag_carries_cited_values_and_generative_origin(self) -> None:
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        detail = self.service.detail(self.pm, tid)
        flag = detail["review_flag"]
        snap_citations = detail["snapshot"]["citations"]
        self.assertEqual(flag["status"], "review-suggested")
        self.assertEqual(flag["origin"], "generative_model")
        self.assertIn("Origin: generative_model", flag["origin_text"])
        self.assertEqual(flag["not_retained"], ["dew_point_c", "mould_risk_index"])
        self.assertEqual(flag["invocation_modes"], ["proactive"])
        self.assertTrue(flag["readings"])
        self.assertEqual([s["citation"] for s in flag["source_provenance"]], flag["cited_ids"])
        source = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        sent = sensor_view.citations(source)
        for reading in flag["readings"]:
            row = sent[reading["citation"]]
            self.assertEqual(reading["temperature_c"], row["temperature_c"])
            self.assertEqual(reading["humidity_pct"], row["humidity_pct"])
            self.assertEqual(reading["observed_at"], row["observed_at"])
            self.assertEqual(reading["provenance_class"], row["provenance_class"])
            self.assertEqual(reading["source_text"], source["provenance"][row["provenance_class"]])
            self.assertEqual(reading["locator"], snap_citations[reading["citation"]]["locator"])
            self.assertEqual(
                reading["content_hash"], snap_citations[reading["citation"]]["content_hash"]
            )
            self.assertEqual(CITATION.findall(reading["text"]), [reading["citation"]])
            self.assertIn(f"temperature_c {row['temperature_c']} degC", reading["text"])
        for src_entry in flag["source_provenance"]:
            cid = src_entry["citation"]
            self.assertEqual(src_entry["locator"], snap_citations[cid]["locator"])
            self.assertEqual(src_entry["content_hash"], snap_citations[cid]["content_hash"])
            if cid.startswith("sensor:"):
                self.assertEqual(src_entry["kind"], "sensor-reading")
                self.assertIn(src_entry["provenance_class"], flag["cited_provenance_classes"])

    def test_conflicting_readings_block_proactive_flag_and_route_chat_without_picking_one(
        self,
    ) -> None:
        self.ready()
        initial = self.request("/api/cases/ZF-1/sensors")[1]
        self._insert_conflict_at(
            initial["latest"]["observed_at"],
            reading_id="R-PRECLASH",
            scenario="SYNTHETIC_LIVE_WEATHER",
        )
        self.service.scan()
        self.assertEqual(self.quality_task(), [])

        refs = dict(
            CHAT_DPIA_REF="SYN-DPIA",
            CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
            CHAT_NOTICE_REF="SYN-NOTICE",
        )
        iso = ChatIsolation(self.store, env=refs)
        iso.sensors = self.service.sensors
        panel = ChatPanel(iso, lambda s, p: "{}")
        with patch.object(self.store, "ai", SimpleNamespace(consumption=None), create=True):
            ctid = self.store.chat_create_thread(self.pm, case_id="ZF-1")["id"]
            reply = panel.ask(self.pm, ctid, "What are the sensor readings?")
        self.assertIn("conflict", reply["reply"].lower())
        self.assertNotIn("No retained sensor reading is shown", reply["reply"])
        self.assertNotRegex(reply["reply"], r"temperature_c \d")
        chat_sources = {c["id"]: c["source_kind"] for c in reply["citations"]}
        self.assertEqual(chat_sources["ZF-1/sensor.conflict"], "decision-rule")

        # Clean capture followed by same-bucket conflicting arrival downgrades autonomous L4 flag.
        with self.service.transaction() as db:
            db.execute("DELETE FROM sensor_reading WHERE reading_id='R-PRECLASH'")
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        self.assertEqual(
            self.service.detail(self.pm, tid)["review_flag"]["status"], "review-suggested"
        )

        self._insert_conflict_at(
            initial["latest"]["observed_at"],
            reading_id="R-LATECLASH",
            scenario="OTHER_SIM_SCENARIO",
        )
        downgraded = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(
            (downgraded["status"], downgraded["autonomous"], downgraded["level"]),
            ("conflicting-readings", False, None),
        )
        self.assertTrue(downgraded["conflicting_readings"])
        self.assertIn("Do not choose between conflicting readings", downgraded["effect"])

        self.set_consent("declined")
        withheld_detail = self.service.detail(self.pm, tid)
        self.assertEqual(withheld_detail["review_flag"]["status"], "withheld")
        self.assertNotIn("R-LATECLASH", json.dumps(withheld_detail))


class WebGrounding(unittest.TestCase):
    def test_panel_and_flag_render_origin_and_values(self) -> None:
        ops = (WEB / "ops.js").read_text(encoding="utf-8")
        assistants = (WEB / "assistants.js").read_text(encoding="utf-8")
        self.assertIn("data-sensor-grounding", ops)
        self.assertIn("data-sensor-conflict", ops)
        self.assertIn("Origin: ${v.grounding.origin}", ops)
        self.assertIn("data-flag-readings", assistants)
        self.assertIn("data-flag-sources", assistants)
        self.assertIn("data-flag-conflict", assistants)
        self.assertIn("data-flag-origin", assistants)
        self.assertIn("conflicting-readings", assistants)


if __name__ == "__main__":
    unittest.main()
