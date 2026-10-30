"""Constructed synthetic replay and finite-run contracts."""

import asyncio
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from zava_forward.core.synthetic import sensor_backfill, sensor_faults, sensor_stock
from zava_forward.core.synthetic.sensor_stream import (
    Pacer,
    Replay,
    RunBudget,
    StreamError,
    descriptor,
    replay,
    wire,
)


def selection() -> sensor_stock.Selection:
    return sensor_stock.select(
        [
            {
                "synthetic_home_id": home,
                "is_synthetic": "true",
                "monitoring_consent": consent,
                "building_form_osm": "terrace",
            }
            for home, consent in (("ZF-1", "granted"), ("ZF-2", "declined"), ("ZF-3", "unknown"))
        ],
        3,
    )


class ReplayTests(unittest.TestCase):
    def test_selected_subset_and_fabric_consent_mutations_bind_frame_provenance(self) -> None:
        selected, spec = selection(), Replay()
        subset = sensor_stock.select(selected.rows, 1)
        self.assertEqual(subset.input_sha256, selected.input_sha256)
        original = descriptor(selected, spec)
        self.assertNotEqual(original, descriptor(subset, spec))
        self.assertEqual(original["selected_homes"], 3)
        self.assertEqual(original["monitored_homes"], 1)
        self.assertEqual(original["selected_home_ids"], ["ZF-1", "ZF-2", "ZF-3"])
        frames = replay(selected, spec)
        self.assertEqual(
            {frame.selected_stock_sha256 for frame in frames},
            {original["selected_stock_sha256"]},
        )
        for field, value in (
            ("building_form_osm", "detached"),
            ("locality_theme", "urban"),
            ("monitoring_consent", "granted"),
        ):
            with self.subTest(field=field):
                mutated = replace(selected, rows=tuple(dict(row) for row in selected.rows))
                target = 1 if field == "monitoring_consent" else 0
                mutated.rows[target][field] = value
                changed = descriptor(mutated, spec)
                changed_frames = replay(mutated, spec)
                self.assertNotEqual(
                    changed["selected_stock_sha256"], original["selected_stock_sha256"]
                )
                self.assertEqual(changed["stock_sha256"], original["stock_sha256"])
                self.assertEqual(
                    {frame.selected_stock_sha256 for frame in changed_frames},
                    {changed["selected_stock_sha256"]},
                )
                self.assertNotEqual(changed_frames, frames)
        selected.rows[0]["building_form_osm"] = "detached"
        self.assertNotEqual(descriptor(selected, spec), original)
        self.assertEqual(
            {frame.selected_stock_sha256 for frame in frames},
            {original["selected_stock_sha256"]},
        )

    def test_selected_provenance_is_canonical_and_validation_matches_replay(self) -> None:
        selected, spec = selection(), Replay()
        reordered = replace(
            selected,
            rows=tuple(
                {**row, "is_synthetic": "TRUE", "ignored": "not a model input"}
                for row in reversed(selected.rows)
            ),
        )
        self.assertEqual(descriptor(selected, spec), descriptor(reordered, spec))
        self.assertEqual(replay(selected, spec), replay(reordered, spec))
        for field, value in (
            ("is_synthetic", "false"),
            ("monitoring_consent", "invalid"),
            ("synthetic_home_id", " "),
        ):
            bad = replace(selected, rows=({**selected.rows[0], field: value},))
            with (
                self.subTest(field=field),
                patch.object(sensor_backfill, "outdoor_series") as model,
            ):
                for operation in (descriptor, replay):
                    with self.assertRaises(ValueError):
                        operation(bad, spec)
                model.assert_not_called()
        excluded = replace(
            selected,
            rows=({**selected.rows[0], "monitoring_consent": "declined"},),
        )
        for operation in (descriptor, replay):
            with self.assertRaisesRegex(StreamError, "REPLAY_SCALE_LIMIT"):
                operation(excluded, spec)
        expected = replay(selected, spec)
        original_descriptor = descriptor(selected, spec)
        outdoor_series = sensor_backfill.outdoor_series

        def mutate_after_snapshot(
            seed: int, days: int, cadence_minutes: int, origin: object
        ) -> object:
            selected.rows[0]["is_synthetic"] = "false"
            selected.rows[0]["building_form_osm"] = "detached"
            return outdoor_series(seed, days, cadence_minutes, origin)

        with patch.object(sensor_backfill, "outdoor_series", side_effect=mutate_after_snapshot):
            actual = replay(selected, spec)
        self.assertEqual(actual, expected)
        self.assertEqual(
            {frame.selected_stock_sha256 for frame in actual},
            {original_descriptor["selected_stock_sha256"]},
        )

    def test_exact_existing_generator_suffix_and_three_per_day(self) -> None:
        selected, spec = selection(), Replay()
        sensor = selected.sensors(spec.seed)[0]
        source = sensor_backfill.readings(
            {**sensor, "fault_profile": "none"},
            spec.seed,
            spec.days,
            spec.cadence_minutes,
            start=spec.origin,
        )
        expected = [sensor_faults.observation(row) for row in source]
        frames = replay(selected, spec)
        self.assertEqual(len(frames), 6)
        self.assertEqual([frame.row for frame in frames], expected)
        suffix = replay(selected, replace(spec, first_slot=3, end_slot=5))
        self.assertEqual([frame.row for frame in suffix], expected[3:5])
        self.assertEqual({frame.row["home_id"] for frame in frames}, {"ZF-1"})
        self.assertEqual({frame.device_id for frame in frames}, {"SYN-" + str(sensor["sensor_id"])})
        self.assertTrue(
            all(set(frame.row) == set(sensor_faults.READING_FIELDS) for frame in frames)
        )
        self.assertEqual(descriptor(selected, spec)["source_type"], "SYNTHETIC")
        self.assertEqual(descriptor(selected, spec)["stock_sha256"], selected.input_sha256)

    def test_nominal_timing_uses_configured_origin_cadence_and_suffix(self) -> None:
        spec = Replay(
            origin=datetime(2025, 2, 1, 3, 15, tzinfo=UTC),
            cadence_minutes=60,
            first_slot=3,
            end_slot=5,
        )
        frames = replay(selection(), spec)
        self.assertEqual(
            [frame.nominal_at for frame in frames],
            [spec.origin + timedelta(hours=slot) for slot in (3, 4)],
        )
        self.assertEqual(
            [frame.nominal_at for frame in frames],
            [datetime.fromisoformat(frame.row["observed_at"]) for frame in frames],
        )

    def test_faults_are_separate_truth_and_nominal_slot_replay(self) -> None:
        for fault in (
            "duplicate",
            "out_of_order",
            "unmapped",
            "wrong_unit",
            "clock_skewed",
            "uncalibrated",
            "burst",
            "disconnect",
        ):
            with self.subTest(fault=fault):
                spec = Replay(fault=fault)
                full = replay(selection(), spec)
                suffix = replay(selection(), replace(spec, first_slot=3, end_slot=5))
                self.assertEqual(suffix, tuple(frame for frame in full if 3 <= frame.slot < 5))
                self.assertTrue(all(frame.truth == fault for frame in full))
                self.assertTrue(all("truth" not in frame.row for frame in full))
                self.assertEqual(
                    [frame.nominal_at for frame in full],
                    [
                        spec.origin + timedelta(minutes=frame.slot * spec.cadence_minutes)
                        for frame in full
                    ],
                )
                self.assertEqual(len(full), 12 if fault == "duplicate" else 6)
        self.assertEqual(replay(selection(), Replay(fault="gap")), ())
        odd = replay(selection(), Replay(days=1, fault="out_of_order"))
        self.assertEqual([frame.slot for frame in odd], [0, 1, 2])
        self.assertLess(odd[1].row["observed_at"], odd[0].row["observed_at"])

    def test_bad_selection_limits_and_invalid_replay_fail_before_model(self) -> None:
        invalid = (
            Replay(seed=True),
            Replay(days=0),
            Replay(cadence_minutes=7),
            Replay(first_slot=6),
            Replay(end_slot=True),
            Replay(fault="real"),
        )
        for spec in invalid:
            with self.subTest(spec=spec), self.assertRaises(StreamError):
                replay(selection(), spec)
        with patch.object(sensor_backfill, "outdoor_series") as model:
            with self.assertRaisesRegex(StreamError, "REPLAY_SCALE_LIMIT"):
                replay(selection(), Replay(days=3660, cadence_minutes=1))
            model.assert_not_called()
        bad = replace(selection(), rows=({**selection().rows[0], "is_synthetic": "false"},))
        with self.assertRaisesRegex(ValueError, "is_synthetic"):
            replay(bad, Replay())
        with self.assertRaisesRegex(StreamError, "STREAM_MESSAGE_TOO_LARGE"):
            wire({"a": "x" * 4097})

    def test_budget_counts_duplicates_bytes_and_headroom(self) -> None:
        frames = replay(selection(), Replay(fault="duplicate"))
        budget = RunBudget("Fixture Owner", "USD60 source model", "fixture alert")
        self.assertEqual(budget.validate(frames), 12)
        for bad in (
            replace(budget, owner=""),
            replace(budget, alert_reference=""),
            replace(budget, max_messages=11),
            replace(budget, max_messages=True),
            replace(budget, max_seconds=float("inf")),
            replace(budget, max_seconds=3601),
            replace(budget, max_per_second=0),
            replace(budget, daily_used_units=360000),
            replace(budget, reserved_headroom_units=0),
        ):
            with self.subTest(bad=bad), self.assertRaises(StreamError):
                bad.validate(frames)


class PacingTests(unittest.IsolatedAsyncioTestCase):
    async def test_high_rate_and_short_nominal_targets_do_not_wait_for_poll_interval(self) -> None:
        for rate in (25, 50, 100):
            with self.subTest(rate=rate):
                now = [0.0]
                sleeps: list[float] = []

                def clock(now: list[float] = now) -> float:
                    return now[0]

                pacer = Pacer(
                    RunBudget("owner", "cost", "alert", max_per_second=rate),
                    clock=clock,
                )

                async def advance(
                    seconds: float, sleeps: list[float] = sleeps, now: list[float] = now
                ) -> None:
                    sleeps.append(seconds)
                    now[0] += seconds

                with patch("zava_forward.core.synthetic.sensor_stream.asyncio.sleep", advance):
                    admissions = []
                    for _ in range(4):
                        await pacer.admit_send()
                        admissions.append(now[0])
                    for index, actual in enumerate(admissions):
                        self.assertAlmostEqual(actual, index / rate)
                    self.assertTrue(all(0 < delay <= 1 / rate for delay in sleeps))
                    before = now[0]
                    await pacer.wait(0.005)
                    self.assertAlmostEqual(now[0] - before, 0.005)

    async def test_paused_elapsed_target_uses_positive_bounded_deadline_polling(self) -> None:
        now = [0.0]
        sleeps: list[float] = []
        pacer = Pacer(
            RunBudget("owner", "cost", "alert", max_seconds=1),
            clock=lambda: now[0],
        )
        pacer.paused = True
        pacer.deadline = 0.12

        async def advance(seconds: float) -> None:
            self.assertGreater(seconds, 0)
            self.assertLessEqual(seconds, 0.05)
            sleeps.append(seconds)
            now[0] += seconds

        with patch("zava_forward.core.synthetic.sensor_stream.asyncio.sleep", advance):
            with self.assertRaisesRegex(StreamError, "^RUN_DEADLINE$"):
                await pacer.wait(0)
        self.assertEqual(len(sleeps), 3)
        self.assertAlmostEqual(sleeps[-1], 0.02)
        self.assertAlmostEqual(now[0], pacer.deadline)

    async def test_send_admission_rate_pause_stop_deadline_and_cancel(self) -> None:
        now = [0.0]
        pacer = Pacer(
            RunBudget("owner", "cost", "alert", max_seconds=10, max_per_second=5),
            clock=lambda: now[0],
        )

        async def advance(seconds: float) -> None:
            now[0] += seconds
            if now[0] >= 1:
                pacer.paused = False

        with patch("zava_forward.core.synthetic.sensor_stream.asyncio.sleep", advance):
            await pacer.wait(0)
            now[0] = 0.25
            await pacer.admit_send()
            first = now[0]
            await pacer.wait(0)
            await pacer.admit_send()
            self.assertGreaterEqual(now[0] - first, 0.2)
            pacer.paused = True
            await pacer.admit_send()
            self.assertGreaterEqual(now[0], 1)
            pacer.stopped = True
            with self.assertRaisesRegex(StreamError, "^RUN_STOPPED$"):
                await pacer.admit_send()
            pacer.stopped = False
            pacer.deadline = now[0] + 0.1
            with self.assertRaisesRegex(StreamError, "^RUN_DEADLINE$"):
                await pacer.admit_send()
        pacer.deadline = now[0] + 10
        pacer.paused = True
        task = asyncio.create_task(pacer.admit_send())
        await asyncio.sleep(0)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task

    async def test_speed_pause_stop_and_deadline(self) -> None:
        now = [0.0]
        pacer = Pacer(
            RunBudget("owner", "cost", "alert", max_seconds=100, max_per_second=10),
            speed=1000,
            clock=lambda: now[0],
        )

        async def advance(seconds: float) -> None:
            now[0] += seconds
            if now[0] >= 1:
                pacer.paused = False

        pacer.paused = True
        with patch("zava_forward.core.synthetic.sensor_stream.asyncio.sleep", advance):
            await pacer.wait(0)
            self.assertGreaterEqual(now[0], 1)
            await pacer.wait(1000)
            self.assertGreaterEqual(now[0], 2)
            pacer.stopped = True
            with self.assertRaisesRegex(StreamError, "RUN_STOPPED"):
                await pacer.wait(0)
            pacer.stopped = False
            pacer.paused = True
            pacer.deadline = now[0] + 0.1
            with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
                await pacer.wait(1000)

    async def test_invalid_speed_and_cancellation(self) -> None:
        for speed in (0, -1, float("nan"), True, 1001):
            with self.assertRaisesRegex(StreamError, "INVALID_REPLAY_SPEED"):
                Pacer(RunBudget("owner", "cost", "alert"), speed=speed)
        pacer = Pacer(RunBudget("owner", "cost", "alert"))
        pacer.paused = True
        task = asyncio.create_task(pacer.wait(0))
        await asyncio.sleep(0)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
