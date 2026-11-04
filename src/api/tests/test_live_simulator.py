import asyncio
import io
import json
import logging
import random
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import live_readings as lr
from zava_forward.core.synthetic.sensor_stream import StreamError

from zava_forward.api import live_simulator as ls
from zava_forward.api.iot_stream import DeviceActivation

HOMES = [f"HOME-{i:03d}" for i in range(12)]
SLOT = datetime(2026, 11, 4, 15, 55, tzinfo=UTC)
FAST = ls.Limits(max_per_second=100.0, batch_size=5, attempts=3)


class Clock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    async def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def run_async(coro: Any) -> Any:
    return asyncio.run(coro)


class SendSlotTests(unittest.TestCase):
    def test_every_home_gets_one_labelled_message_per_slot(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        summary = run_async(
            ls.send_slot(
                HOMES, SLOT, lr.Generator(184), sink, FAST, sleep=clock.sleep, clock=clock.monotonic
            )
        )
        self.assertEqual((summary.sent, summary.failed, summary.homes), (12, 0, 12))
        self.assertEqual(len({m[0] for m in sink.messages}), 12)
        self.assertEqual(len({m[1] for m in sink.messages}), 12)
        for device, message_id, body in sink.messages:
            row = json.loads(body)
            self.assertEqual(row["source_type"], "SYNTHETIC")
            self.assertEqual(row["observed_at"], "2026-11-04T15:55:00Z")
            self.assertEqual(device, "SYN-" + row["sensor_id"])
            self.assertEqual(message_id, row["reading_id"])

    def test_throttle_spaces_sends_by_the_configured_rate(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        limits = ls.Limits(max_per_second=4.0, batch_size=3, attempts=1)
        run_async(
            ls.send_slot(
                HOMES, SLOT, lr.Generator(1), sink, limits, sleep=clock.sleep, clock=clock.monotonic
            )
        )
        self.assertGreaterEqual(clock.now, (len(HOMES) - 1) / 4.0 - 1e-9)

    def test_transient_failure_retries_with_bounded_backoff_then_succeeds(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        device = "SYN-" + lr.Generator(1).reading(HOMES[0], SLOT).sensor_id
        sink._failures = {device: 2}
        limits = ls.Limits(max_per_second=100.0, batch_size=2, attempts=4, backoff_cap_seconds=3.0)
        summary = run_async(
            ls.send_slot(
                HOMES[:2],
                SLOT,
                lr.Generator(1),
                sink,
                limits,
                sleep=clock.sleep,
                clock=clock.monotonic,
                rng=random.Random(0),
            )
        )
        self.assertEqual((summary.sent, summary.failed, summary.retries), (2, 0, 2))
        backoffs = [s for s in clock.sleeps if s >= 0.4]
        self.assertEqual(len(backoffs), 2)
        self.assertTrue(all(s <= 3.0 for s in backoffs))
        self.assertLess(backoffs[0], backoffs[1] + 3.0)

    def test_exhausted_retries_count_as_failed_without_stopping_other_homes(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        device = "SYN-" + lr.Generator(1).reading(HOMES[0], SLOT).sensor_id
        sink._failures = {device: 99}
        summary = run_async(
            ls.send_slot(
                HOMES[:3],
                SLOT,
                lr.Generator(1),
                sink,
                FAST,
                sleep=clock.sleep,
                clock=clock.monotonic,
            )
        )
        self.assertEqual((summary.sent, summary.failed), (2, 1))
        self.assertEqual(summary.codes, {"FAKE_TRANSIENT": 3})

    def test_non_retryable_error_is_not_retried(self) -> None:
        class Denied:
            attempts = 0

            async def send(self, device_id: str, message_id: str, body: bytes) -> None:
                Denied.attempts += 1
                raise ls.SinkError("DEVICE_CREDENTIAL_MISSING", retryable=False)

            async def close(self) -> None:
                return None

        clock = Clock()
        summary = run_async(
            ls.send_slot(
                HOMES[:2],
                SLOT,
                lr.Generator(1),
                Denied(),
                FAST,
                sleep=clock.sleep,
                clock=clock.monotonic,
            )
        )
        self.assertEqual((summary.failed, Denied.attempts), (2, 2))

    def test_invalid_home_id_is_counted_not_fatal(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        summary = run_async(
            ls.send_slot(
                ["HOME-001", " bad "],
                SLOT,
                lr.Generator(1),
                sink,
                FAST,
                sleep=clock.sleep,
                clock=clock.monotonic,
            )
        )
        self.assertEqual((summary.sent, summary.failed), (1, 1))
        self.assertEqual(summary.codes, {"INVALID_HOME_ID": 1})


class CapacityTests(unittest.TestCase):
    def test_within_b1_budget(self) -> None:
        plan = ls.check_capacity(1000, ls.Limits(max_per_second=10.0))
        self.assertEqual(plan["messages_per_day"], 288_000)
        self.assertEqual(plan["quota_fraction"], 0.72)
        self.assertEqual(plan["hub_usd_per_month"], 10.0)

    def test_over_b1_daily_budget_is_refused(self) -> None:
        with self.assertRaises(StreamError) as ctx:
            ls.check_capacity(1251, ls.Limits(max_per_second=20.0))
        self.assertEqual(str(ctx.exception), "B1_QUOTA_HEADROOM")

    def test_rate_too_low_to_finish_inside_the_slot_is_refused(self) -> None:
        with self.assertRaises(StreamError) as ctx:
            ls.check_capacity(1000, ls.Limits(max_per_second=1.0))
        self.assertEqual(str(ctx.exception), "RATE_TOO_LOW_FOR_HOMES")

    def test_bad_inputs_are_refused(self) -> None:
        for homes, limits in (
            (0, FAST),
            (5, ls.Limits(max_per_second=0)),
            (5, ls.Limits(attempts=0)),
        ):
            with self.assertRaises(StreamError):
                ls.check_capacity(homes, limits)


class RunTests(unittest.TestCase):
    def test_once_sends_the_current_slot_and_closes(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        summaries = run_async(
            ls.run(
                lambda: HOMES,
                lr.Generator(184),
                sink,
                FAST,
                once=True,
                now=lambda: datetime(2026, 11, 4, 15, 58, 19, tzinfo=UTC),
                sleep=clock.sleep,
                clock=clock.monotonic,
            )
        )
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0].slot, SLOT)
        self.assertTrue(sink.closed)

    def test_loop_waits_for_each_five_minute_boundary(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        times = [datetime(2026, 11, 4, 15, 58, tzinfo=UTC)]

        async def sleep(seconds: float) -> None:
            if seconds >= 1:
                times.append(times[-1] + timedelta(seconds=seconds))
            await clock.sleep(seconds)

        summaries = run_async(
            ls.run(
                lambda: HOMES[:2],
                lr.Generator(184),
                sink,
                FAST,
                max_slots=3,
                now=lambda: times[-1],
                sleep=sleep,
                clock=clock.monotonic,
            )
        )
        self.assertEqual([s.slot.strftime("%H:%M") for s in summaries], ["15:55", "16:00", "16:05"])
        self.assertEqual(len(sink.messages), 6)

    def test_enumeration_failure_reuses_previous_homes(self) -> None:
        calls = {"n": 0}

        def homes() -> list[str]:
            calls["n"] += 1
            if calls["n"] > 1:
                raise OSError("store unavailable")
            return HOMES[:2]

        sink, clock = ls.MemorySink(), Clock()
        times = [datetime(2026, 11, 4, 15, 58, tzinfo=UTC)]

        async def sleep(seconds: float) -> None:
            if seconds >= 1:
                times.append(times[-1] + timedelta(seconds=seconds))
            await clock.sleep(seconds)

        with self.assertLogs("zava_forward.live_simulator", level="ERROR"):
            summaries = run_async(
                ls.run(
                    homes,
                    lr.Generator(1),
                    sink,
                    FAST,
                    max_slots=2,
                    refresh_slots=1,
                    now=lambda: times[-1],
                    sleep=sleep,
                    clock=clock.monotonic,
                )
            )
        self.assertEqual([s.sent for s in summaries], [2, 2])

    def test_no_homes_sends_nothing(self) -> None:
        sink, clock = ls.MemorySink(), Clock()
        with self.assertLogs("zava_forward.live_simulator", level="ERROR"):
            summaries = run_async(
                ls.run(
                    lambda: [],
                    lr.Generator(1),
                    sink,
                    FAST,
                    once=True,
                    sleep=clock.sleep,
                    clock=clock.monotonic,
                )
            )
        self.assertEqual((summaries, sink.messages), ([], []))


class FakeClient:
    instances: list["FakeClient"] = []

    def __init__(self, fail: bool = False) -> None:
        self.sent: list[Any] = []
        self.connected = self.down = False
        self.fail = fail
        FakeClient.instances.append(self)

    async def connect(self) -> None:
        self.connected = True

    async def send_message(self, message: Any) -> None:
        if self.fail:
            raise RuntimeError("PRIVATE-KEY-MATERIAL-99")
        self.sent.append(message)

    async def shutdown(self) -> None:
        self.down = True


ACTIVATION = DeviceActivation("iot-fixture.azure-devices.net", "owner-approval-ref")


class IotHubSinkTests(unittest.TestCase):
    def setUp(self) -> None:
        FakeClient.instances = []
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name)
        for device in ("SYN-A", "SYN-B", "SYN-C"):
            (self.path / f"{device}.pem").write_text("fixture")
            (self.path / f"{device}.key").write_text("fixture")
        self.fail_sends = False

    def sink(self, max_open: int = 100) -> ls.IotHubSink:
        return ls.IotHubSink(
            ACTIVATION,
            self.path,
            max_open,
            lambda host, device, cert, key: FakeClient(self.fail_sends),
        )

    def test_activation_without_approval_is_refused(self) -> None:
        with self.assertRaises(StreamError):
            ls.IotHubSink(DeviceActivation("iot-fixture.azure-devices.net", ""), self.path)

    def test_missing_credential_is_non_retryable_and_never_connects(self) -> None:
        sink = self.sink()
        with self.assertRaises(ls.SinkError) as ctx:
            run_async(sink.send("SYN-NONE", "m1", b"{}"))
        self.assertEqual(
            (ctx.exception.code, ctx.exception.retryable), ("DEVICE_CREDENTIAL_MISSING", False)
        )
        self.assertEqual(FakeClient.instances, [])

    def test_path_like_device_id_is_refused(self) -> None:
        with self.assertRaises(ls.SinkError):
            run_async(self.sink().send("../SYN-A", "m1", b"{}"))

    def test_connection_is_reused_and_capped(self) -> None:
        async def go() -> None:
            sink = self.sink(max_open=2)
            for device in ("SYN-A", "SYN-A", "SYN-B", "SYN-C"):
                await sink.send(device, "m", b"{}")
            await sink.close()

        run_async(go())
        self.assertEqual(len(FakeClient.instances), 3)
        self.assertTrue(all(c.down for c in FakeClient.instances))
        self.assertEqual(sum(len(c.sent) for c in FakeClient.instances), 4)

    def test_sdk_failure_text_never_leaks_credentials(self) -> None:
        self.fail_sends = True
        with self.assertLogs(level="DEBUG") as logs, self.assertRaises(ls.SinkError) as ctx:
            logging.getLogger("probe").debug("start")
            run_async(self.sink().send("SYN-A", "m1", b"{}"))
        self.assertEqual(str(ctx.exception), "IOT_SEND_FAILED")
        self.assertIsNone(ctx.exception.__cause__)
        self.assertNotIn("PRIVATE-KEY-MATERIAL", "".join(logs.output) + repr(ctx.exception))


class StoreHomesTests(unittest.TestCase):
    def test_json_like_store_lists_open_cases_only(self) -> None:
        from unittest.mock import patch

        class Json:
            cases = {"B": {}, "A": {}, "C": {"closed": True}}

        with patch("zava_forward.core.factory.open_store", return_value=Json()):
            self.assertEqual(ls.store_home_ids({}), ["A", "B"])

    def test_sql_like_store_is_paged_by_keyset(self) -> None:
        from unittest.mock import patch

        class Sql:
            ids = [f"C{i:04d}" for i in range(1203)]

            def query_case_ids(self, after: str | None = None, limit: int = 50) -> list[str]:
                rest = [i for i in self.ids if after is None or i > after]
                return rest[:limit]

        with patch("zava_forward.core.factory.open_store", return_value=Sql()):
            self.assertEqual(ls.store_home_ids({}), Sql.ids)


class CliTests(unittest.TestCase):
    def test_dry_run_prints_labelled_messages_and_sends_nothing(self) -> None:
        original = ls.store_home_ids
        ls.store_home_ids = lambda env=None: HOMES[:3]
        self.addCleanup(setattr, ls, "store_home_ids", original)
        out = io.StringIO()
        with redirect_stdout(out):
            code = ls.main(["--once"], env={})
        lines = out.getvalue().strip().splitlines()
        self.assertEqual(code, 0)
        self.assertEqual(len(lines), 3)
        self.assertTrue(
            all(line.startswith("DRY-RUN SYN-") and "SYNTHETIC" in line for line in lines)
        )

    def test_iothub_sink_without_activation_is_refused(self) -> None:
        err = io.StringIO()
        from contextlib import redirect_stderr

        with redirect_stderr(err):
            code = ls.main(["--sink", "iothub", "--once"], env={})
        self.assertEqual(code, 2)
        self.assertIn("IOT_ACTIVATION_REQUIRED", err.getvalue())

    def test_over_capacity_fleet_is_refused_before_any_send(self) -> None:
        original = ls.store_home_ids
        ls.store_home_ids = lambda env=None: [f"H{i}" for i in range(1300)]
        self.addCleanup(setattr, ls, "store_home_ids", original)
        out = io.StringIO()
        with redirect_stdout(out):
            code = ls.main(["--once", "--max-per-second", "50"], env={})
        self.assertEqual((code, out.getvalue()), (2, ""))


if __name__ == "__main__":
    unittest.main()
