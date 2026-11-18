"""Issue 1288: conflicting retained readings are named, not silently resolved."""

import sqlite3
import tempfile
import unittest
from datetime import UTC, datetime
from typing import Any

import sensor_consumer_fixture as scf
from zava_forward.core import sensor_view
from zava_forward.core.sensor_consumer import READING_COLUMNS, SensorConsumer


def row(
    reading_id: str,
    temp: str,
    observed: str = "2026-11-01T10:00:00Z",
    humidity: str = "85",
    scenario: str = "SYNTHETIC_LIVE_WEATHER",
) -> dict[str, Any]:
    return dict(
        reading_id=reading_id,
        sensor_id="s1",
        observed_at=observed,
        temperature_c=temp,
        humidity_pct=humidity,
        provenance_class="synthetic-weather-derived",
        scenario=scenario,
    )


class Conflicts(unittest.TestCase):
    def test_same_time_different_values_conflict(self) -> None:
        out = sensor_view.conflicts([row("r1", "18.0"), row("r2", "21.0")])
        self.assertEqual(
            out,
            [
                dict(
                    sensor_id="s1",
                    observed_at="2026-11-01T10:00:00Z",
                    citation_keys=["sensor:s1:r1", "sensor:s1:r2"],
                )
            ],
        )

    def test_identical_values_and_distinct_times_do_not_conflict(self) -> None:
        rows = [row("r1", "18.0"), row("r2", "18.0"), row("r3", "21.0", "2026-11-01T10:05:00Z")]
        self.assertEqual(sensor_view.conflicts(rows), [])

    def test_conflict_propagates_to_health_grounding_advisory_without_changing_bucket_signature(
        self,
    ) -> None:
        r1, r2 = row("r1", "14.0"), row("r2", "21.0")
        clean: dict[str, Any] = dict(
            state="ok",
            anchor=dict(name="case_created", at="2026-10-31T00:00:00Z"),
            provenance={
                "synthetic-weather-derived": sensor_view.CLASSES["synthetic-weather-derived"]
            },
            readings=[r1],
            latest=r1,
        )
        clashed: dict[str, Any] = dict(
            clean,
            readings=[r1, r2],
            latest=r2,
            conflicting_readings=sensor_view.conflicts([r1, r2]),
            conflict_notice=(
                "Retained readings disagree for the same sensor and time. "
                "Do not pick one; route to a person."
            ),
        )
        clean_grounding = sensor_view.grounding(clean)
        self.assertEqual(clean_grounding["provenance_class"], "synthetic-weather-derived")
        self.assertIn("Synthetic simulator reading", clean_grounding["source_text"])
        self.assertEqual(
            set(clean_grounding["values"]), {"temperature_c", "humidity_pct", "observed_at"}
        )

        self.assertEqual(sensor_view.reading_health(clashed)["state"], "conflict")
        clashed_grounding = sensor_view.grounding(clashed)
        self.assertIsNone(clashed_grounding["citation"])
        self.assertIsNone(clashed_grounding["values"])
        self.assertEqual(
            clashed_grounding["conflicting_citations"], ["sensor:s1:r1", "sensor:s1:r2"]
        )
        self.assertIn("Do not pick one", clashed_grounding["text"])

        adv = sensor_view.advisory(clashed)
        self.assertFalse(adv["watch"])
        self.assertEqual(adv["label"], "No watch")
        self.assertIn("disagree", adv["text"])

        self.assertEqual(sensor_view.signature(clean), sensor_view.signature(clashed))

    def test_trend_summary_reports_insufficient_instead_of_averaging_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = scf.store_at(tmp, reset=True)
            SensorConsumer(store).configure(scf.POLICY, [scf.CONTROL])
            stamps = [
                "2026-10-28T10:00:00Z",
                "2026-10-29T10:00:00Z",
                "2026-10-30T10:00:00Z",
                "2026-10-31T10:00:00Z",
                "2026-11-01T09:00:00Z",
                "2026-11-01T10:00:00Z",
            ]
            db = sqlite3.connect(str(store.db_path))
            self.addCleanup(db.close)
            marks = ",".join("?" * len(READING_COLUMNS))
            with db:
                for idx, ts in enumerate(stamps):
                    entry = dict(
                        sensor_id=scf.CONTROL.sensor_id,
                        reading_id=f"r-{idx}",
                        home_id="ZF-1",
                        observed_at=ts,
                        temperature_c=f"{17.0 + idx:.1f}",
                        humidity_pct="55",
                        source_type="SYNTHETIC",
                        scenario="SYNTHETIC_LIVE_WEATHER",
                        seed="1",
                        schema_version="reading-v1",
                        injected_fault="none",
                    )
                    db.execute(
                        f"INSERT INTO sensor_reading VALUES ({marks})",
                        tuple(entry[c] for c in READING_COLUMNS),
                    )
                clash = dict(
                    sensor_id=scf.CONTROL.sensor_id,
                    reading_id="r-clash",
                    home_id="ZF-1",
                    observed_at="2026-11-01T10:00:00Z",
                    temperature_c="11.0",
                    humidity_pct="89",
                    source_type="SYNTHETIC",
                    scenario="SYNTHETIC_LIVE_WEATHER",
                    seed="1",
                    schema_version="reading-v1",
                    injected_fault="none",
                )
                db.execute(
                    f"INSERT INTO sensor_reading VALUES ({marks})",
                    tuple(clash[c] for c in READING_COLUMNS),
                )
            now = datetime(2026, 11, 1, 10, 5, tzinfo=UTC).timestamp()
            rendered = sensor_view.view(db, "ZF-1", None, now)
            self.assertEqual(rendered["health"]["state"], "conflict")
            self.assertEqual(
                rendered["trend"]["variables"]["temperature_c"]["direction"], "insufficient"
            )
            self.assertIn("disagree", rendered["trend"]["reason"])


if __name__ == "__main__":
    unittest.main()
