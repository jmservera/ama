"""Seeded synthetic home telemetry to the Quality UI home card and AI snapshot (#165, #1288).

Demo contract only. Rows come from the deterministic live simulator generator and are written in
the retained `sensor_reading` shape. No Azure IoT Hub, network or model provider is used. The
retained contract carries temperature (degC) and relative humidity (%RH, the moisture channel).
It has no CO2 channel, so these tests prove CO2 is never invented.
"""

import dataclasses
import json
import socket
import sys
import unittest
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch

# Sibling test modules import each other by bare name, so `tests.<module>` runs need this.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import release_support  # noqa: E402
from sensor_consumer_fixture import CONTROL, POLICY  # noqa: E402
from zava_forward.core import sensor_view
from zava_forward.core.assistants import digest
from zava_forward.core.sensor_consumer import READING_COLUMNS, SensorConsumer
from zava_forward.core.synthetic.live_readings import Generator, Reading

import test_assistants as ta  # noqa: E402

HOME = "ZF-1"
SEED = 184
NOW = datetime(2026, 11, 14, 10, 0, tzinfo=UTC)
SLOTS = 6
FORBIDDEN = ("co2", "carbon_dioxide", "ppm")


def seeded(seed: int = SEED) -> list[Reading]:
    """The newest SLOTS five-minute readings before NOW, oldest first."""
    generator = Generator(seed)
    return [generator.reading(HOME, NOW - timedelta(minutes=5 * i)) for i in range(SLOTS, 0, -1)]


class IotSeedToQualityBridge(ta.Base):  # type: ignore[misc]
    def setUp(self) -> None:
        base_set_up: Callable[[], None] = super().setUp
        base_set_up()
        with self.service.transaction() as db:
            for table in (
                "sensor_reading",
                "sensor_consumer_control",
                "sensor_consumer_control_home",
                "sensor_consumer_index_state",
                "sensor_consumer_policy",
            ):
                db.execute(f"DROP TABLE IF EXISTS {table}")
        self.provider = ta.Provider()
        self.store.ai = self.provider
        release_support.install(self.store)
        self.readings: list[Reading] = seeded()
        self.set_consent("granted")
        self.insert(self.readings)

    def set_consent(self, consent: str) -> None:
        control = dataclasses.replace(
            CONTROL, sensor_id=self.readings[0].sensor_id, home_id=HOME, consent=consent
        )
        SensorConsumer(self.store).configure(POLICY, [control])

    def insert(self, readings: list[Reading]) -> None:
        with self.service.transaction() as db:
            for reading in readings:
                row = reading.row()
                db.execute(
                    f"INSERT INTO sensor_reading VALUES ({','.join('?' * len(READING_COLUMNS))})",
                    tuple(row[c] for c in READING_COLUMNS),
                )

    def clock_at(self, moment: datetime) -> Any:
        return patch.object(self.service, "now", side_effect=lambda db=None: moment.timestamp())

    def card(self) -> dict[str, Any]:
        with self.clock_at(NOW):
            out: dict[str, Any] = self.service.sensors(self.pm, HOME)
        return out

    def snapshot(self) -> dict[str, Any]:
        with self.clock_at(NOW), self.service.transaction() as db:
            out: dict[str, Any] = self.service.snapshot(
                db, "quality-evidence", self.store.detail(HOME)
            )
        return out

    def state(self) -> dict[str, list[tuple[Any, ...]]]:
        tables = ("sensor_reading", "cases", "assistant_tasks")
        with self.service.transaction() as db:
            return {
                t: [tuple(r) for r in db.execute(f"SELECT * FROM {t} ORDER BY 1, 2").fetchall()]
                for t in tables
            }

    def test_seeded_values_reach_the_home_card_exactly(self) -> None:
        card = self.card()
        self.assertEqual(card["state"], "ok")
        expected: list[dict[str, str]] = [
            dict(
                reading_id=r.reading_id,
                sensor_id=r.sensor_id,
                observed_at=r.row()["observed_at"],
                temperature_c=r.row()["temperature_c"],
                humidity_pct=r.row()["humidity_pct"],
            )
            for r in self.readings
        ]
        shown: list[dict[str, str]] = [
            {k: str(r[k]) for k in expected[0]} for r in card["readings"]
        ]
        self.assertEqual(shown, expected)
        self.assertEqual(card["latest"]["reading_id"], self.readings[-1].reading_id)
        self.assertEqual(card["units"], dict(temperature_c="degC", humidity_pct="%RH"))
        self.assertEqual(
            {r["provenance_class"] for r in card["readings"]}, {"synthetic-weather-derived"}
        )
        self.assertIs(card["calibrated"], False)
        self.assertEqual(card["freshness"], "fresh")

    def test_same_seed_is_deterministic_and_a_new_seed_differs(self) -> None:
        self.assertEqual(
            [r.row() for r in seeded()], [r.row() for r in seeded()], "same seed, same rows"
        )
        other: list[str] = [r.row()["temperature_c"] for r in seeded(SEED + 1)]
        self.assertNotEqual([r.row()["temperature_c"] for r in self.readings], other)
        self.assertEqual(digest(self.snapshot()), digest(self.snapshot()))

    def test_home_card_and_ai_snapshot_carry_the_same_readings(self) -> None:
        card = self.card()
        sensors: dict[str, Any] = self.snapshot()["sources"]["sensors"]
        keys: list[str] = ["readings", "before", "after", "latest"]
        self.assertEqual({k: card[k] for k in keys}, {k: sensors[k] for k in keys})
        citations: dict[str, Any] = self.snapshot()["citations"]
        expected = {sensor_view.key_of(r) for r in card["readings"]}
        self.assertLessEqual(expected, set(citations))
        self.assertIn(sensor_view.key_of(card["latest"]), citations)
        self.assertEqual(sorted(expected), sorted(sensors["citation_keys"]))

    def test_snapshot_digest_ignores_clock_only_changes(self) -> None:
        first = digest(self.snapshot())
        with self.clock_at(NOW + timedelta(minutes=3)), self.service.transaction() as db:
            later = self.service.snapshot(db, "quality-evidence", self.store.detail(HOME))
        self.assertEqual(first, digest(later))

    def test_read_and_snapshot_do_not_mutate_or_go_online(self) -> None:
        before = self.state()
        calls: int = self.provider.calls

        def refuse(*_: object, **__: object) -> None:
            raise AssertionError("network access is not allowed")

        with patch.object(socket.socket, "connect", refuse):
            self.card()
            self.snapshot()
        self.assertEqual(before, self.state())
        self.assertEqual(calls, self.provider.calls)

    def test_moisture_is_humidity_and_co2_is_never_invented(self) -> None:
        card = self.card()
        snapshot = self.snapshot()
        self.assertEqual(
            sorted(card["readings"][0]),
            sorted(
                [
                    "reading_id",
                    "sensor_id",
                    "observed_at",
                    "temperature_c",
                    "humidity_pct",
                    "provenance_class",
                ]
            ),
        )
        text = json.dumps([card, snapshot["sources"]["sensors"]]).lower()
        for word in FORBIDDEN:
            self.assertNotIn(word, text)
        for reading in card["readings"]:
            self.assertTrue(0.0 <= float(reading["humidity_pct"]) <= 100.0)

    def test_declined_consent_withholds_every_seeded_value_from_both_surfaces(self) -> None:
        self.set_consent("declined")
        card = self.card()
        sensors: dict[str, Any] = self.snapshot()["sources"]["sensors"]
        for view in (card, sensors):
            self.assertEqual(view["state"], "consent-withheld")
            self.assertEqual(view["readings"], [])
            self.assertIsNone(view["latest"])
        self.assertNotIn(self.readings[-1].row()["temperature_c"], json.dumps([card, sensors]))


if __name__ == "__main__":
    unittest.main()
