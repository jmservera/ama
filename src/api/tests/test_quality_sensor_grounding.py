"""Retained sensor values in the panel, case chat and Quality review flag (issue 1288).

Local engineering evidence with a MOCK model provider and a constructed fixture store. It proves the
exact retained values, `[sensor:...]` citations and Origin labels, not real model behaviour.
"""

import re
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any

import test_assistants as ta
import test_quality_sensors as qs
from zava_forward.core import sensor_view
from zava_forward.core.chat_case_answers import answer, sensor_facts
from zava_forward.core.chat_isolation import ChatIsolation

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

    def test_quality_review_flag_carries_cited_values_and_generative_origin(self) -> None:
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(flag["status"], "review-suggested")
        self.assertEqual(flag["origin"], "generative_model")
        self.assertIn("Origin: generative_model", flag["origin_text"])
        self.assertEqual(flag["not_retained"], ["dew_point_c", "mould_risk_index"])
        self.assertTrue(flag["readings"])
        source = self.provider.prompts[-1]["evidence"]["sources"]["sensors"]
        sent = sensor_view.citations(source)
        for reading in flag["readings"]:
            row = sent[reading["citation"]]
            self.assertEqual(reading["temperature_c"], row["temperature_c"])
            self.assertEqual(reading["humidity_pct"], row["humidity_pct"])
            self.assertEqual(reading["observed_at"], row["observed_at"])
            self.assertEqual(CITATION.findall(reading["text"]), [reading["citation"]])
            self.assertIn(f"temperature_c {row['temperature_c']} degC", reading["text"])


class WebGrounding(unittest.TestCase):
    def test_panel_and_flag_render_origin_and_values(self) -> None:
        ops = (WEB / "ops.js").read_text(encoding="utf-8")
        assistants = (WEB / "assistants.js").read_text(encoding="utf-8")
        self.assertIn("data-sensor-grounding", ops)
        self.assertIn("Origin: ${v.grounding.origin}", ops)
        self.assertIn("data-flag-readings", assistants)
        self.assertIn("data-flag-origin", assistants)


if __name__ == "__main__":
    unittest.main()
