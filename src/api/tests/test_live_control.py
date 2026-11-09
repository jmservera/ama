import asyncio
import json
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import live_readings as lr
from zava_forward.core.synthetic.sensor_stream import StreamError

from zava_forward.api import live_control as lc
from zava_forward.api import live_receiver as rx
from zava_forward.api import live_simulator as ls

HOMES = [f"HOME-{i:03d}" for i in range(12)]
NOW = datetime(2026, 11, 9, 10, 0, tzinfo=UTC)
EXPIRES = "2026-11-10T10:00:00Z"


def document(**changes: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "version": lc.VERSION,
        "enabled": True,
        "expires_at": EXPIRES,
        "approval_reference": "issue-184-comment-6652226413",
        "owner": "demo owner",
        "homes": HOMES[:3],
    }
    return base | changes


class ControlTests(unittest.TestCase):
    def test_valid_document_round_trips(self) -> None:
        control = lc.parse(document())
        self.assertEqual(lc.parse(control.as_document()), control)
        self.assertEqual(lc.decide(control, NOW), lc.SEND)

    def test_refuses_invalid_documents_with_a_fixed_code(self) -> None:
        bad = [
            document(version="v0"),
            document(enabled="yes"),
            document(owner="tbd"),
            document(approval_reference=" "),
            document(homes=[]),
            document(homes=[HOMES[0], HOMES[0]]),
            document(homes=[" HOME-001"]),
            document(homes=[f"HOME-{i:03d}" for i in range(101)]),
            document(expires_at="2026-11-10"),
            document(expires_at="2026-13-10T10:00:00Z"),
            document(homes=[["a"]]),
            document(extra=1),
            [],
        ]
        for item in bad:
            with self.subTest(item=str(item)[:60]):
                with self.assertRaises(StreamError) as caught:
                    lc.parse(item)
                self.assertEqual(str(caught.exception), "CONTROL_INVALID")

    def test_one_hundred_homes_is_the_largest_cohort(self) -> None:
        homes = [f"HOME-{i:03d}" for i in range(100)]
        self.assertEqual(len(lc.parse(document(homes=homes)).homes), 100)

    def test_stop_and_expiry_are_final_decisions(self) -> None:
        control = lc.parse(document())
        self.assertEqual(lc.decide(control, control.expires_at), lc.EXPIRED)
        self.assertEqual(lc.decide(control, control.expires_at - timedelta(seconds=1)), lc.SEND)
        stopped = lc.parse(document(enabled=False))
        self.assertEqual(lc.decide(stopped, NOW), lc.STOPPED)

    def test_readers_refuse_an_expiry_beyond_fourteen_days(self) -> None:
        cases = {
            "2026-11-23T10:00:00Z": lc.SEND,
            "2026-11-23T10:00:01Z": lc.INVALID,
            "2027-11-09T10:00:00Z": lc.INVALID,
            "2026-11-10T10:00:00Z": lc.SEND,
        }
        for expires, expected in cases.items():
            with self.subTest(expires=expires):
                self.assertEqual(lc.decide(lc.parse(document(expires_at=expires)), NOW), expected)
        far = document(expires_at="2027-11-09T10:00:00Z")
        self.assertEqual(lc.decide(lc.parse(far | {"enabled": False}), NOW), lc.INVALID)
        self.assertEqual(lc.decide(lc.parse(document(enabled=False)), NOW), lc.STOPPED)

    def test_expired_stays_expired_not_invalid_or_send(self) -> None:
        for expires in ("2026-11-09T10:00:00Z", "2020-01-01T00:00:00Z"):
            self.assertEqual(lc.decide(lc.parse(document(expires_at=expires)), NOW), lc.EXPIRED)

    def test_window_must_be_future_and_at_most_fourteen_days(self) -> None:
        lc.check_window(lc.parse(document()), NOW)
        for expires in ("2026-11-09T10:00:00Z", "2026-11-23T10:00:01Z"):
            with self.subTest(expires=expires), self.assertRaises(StreamError):
                lc.check_window(lc.parse(document(expires_at=expires)), NOW)
        lc.check_window(lc.parse(document(expires_at="2026-11-23T10:00:00Z")), NOW)

    def test_missing_or_corrupt_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            with self.assertRaises(StreamError):
                lc.load(path)
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(StreamError):
                lc.load(path)


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> int:
        return lc.main(list(args), now=NOW)

    def test_start_status_stop_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            base = ["--file", str(path)]
            start = [
                "start",
                *base,
                "--expires-at",
                EXPIRES,
                "--approval",
                "ref-1",
                "--owner",
                "demo owner",
                "--homes",
                ",".join(HOMES[:2]),
            ]
            self.assertEqual(self.run_cli(*start), 0)
            self.assertTrue(lc.load(path).enabled)
            self.assertEqual(self.run_cli("stop", *base), 0)
            stopped = lc.load(path)
            self.assertFalse(stopped.enabled)
            self.assertEqual(stopped.homes, tuple(HOMES[:2]))
            self.assertEqual(self.run_cli("status", *base), 0)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_start_refuses_an_unbounded_or_past_window_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            for expires in ("2026-11-08T10:00:00Z", "2027-01-01T00:00:00Z", ""):
                args = ["start", "--file", str(path), "--expires-at", expires]
                args += ["--approval", "r", "--owner", "o", "--homes", HOMES[0]]
                self.assertEqual(self.run_cli(*args), 2)
            self.assertFalse(path.exists())


class CohortAndGateTests(unittest.TestCase):
    def test_cohort_is_the_control_homes_present_in_the_store(self) -> None:
        control = lc.parse(document(homes=[HOMES[2], "HOME-900", HOMES[0]]))
        self.assertEqual(ls.cohort_homes(control, HOMES), [HOMES[2], HOMES[0]])
        with self.assertRaises(StreamError):
            ls.cohort_homes(lc.parse(document(homes=["HOME-900"])), HOMES)

    def test_gate_stops_the_run_before_any_send(self) -> None:
        sink = ls.MemorySink()
        summaries = asyncio.run(
            ls.run(
                lambda: HOMES,
                lr.Generator(1),
                sink,
                ls.Limits(max_per_second=100.0),
                once=True,
                now=lambda: NOW,
                gate=lambda moment: False,
            )
        )
        self.assertEqual((summaries, sink.messages), ([], []))

    def test_over_window_control_sends_nothing_through_main(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            far = (datetime.now(UTC) + timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
            lc.write(path, lc.parse(document(expires_at=far)))
            env = {"ZF_STORE": "json", "ZF_DATA": str(Path(directory) / "none.json")}
            code = ls.main(["--sink", "stdout", "--once", "--control-file", str(path)], env)
            self.assertEqual(code, 0)

    def test_iothub_sink_needs_a_control_file(self) -> None:
        env = {"ZF_SIM_HUB_HOSTNAME": "hub-x.azure-devices.net", "ZF_SIM_APPROVAL": "r"}
        self.assertEqual(ls.main(["--sink", "iothub", "--once"], env), 2)

    def test_stopped_control_sends_nothing_through_main(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            far = (datetime.now(UTC) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
            lc.write(path, lc.parse(document(enabled=False, expires_at=far)))
            env = {"ZF_STORE": "json", "ZF_DATA": str(Path(directory) / "none.json")}
            code = ls.main(["--sink", "stdout", "--once", "--control-file", str(path)], env)
            self.assertEqual(code, 0)


class ReceiverTests(unittest.TestCase):
    def test_bindings_match_the_simulator_device_identity(self) -> None:
        control = lc.parse(document())
        bound = rx.bindings(control)
        reading = lr.Generator(1).reading(HOMES[0], NOW)
        self.assertEqual(bound[0].device_id, reading.device_id)
        self.assertEqual((bound[0].sensor_id, bound[0].home_id), (reading.sensor_id, HOMES[0]))
        self.assertEqual(len(bound), 3)

    def test_activation_never_ready_by_default(self) -> None:
        control = lc.parse(document())
        env = {"ZF_SIM_HUB_HOSTNAME": "hub-x.azure-devices.net"}
        with self.assertRaises(StreamError):
            rx.activation(env, control).validate()
        ready = rx.activation(env | {"ZF_SIM_ROUTING_READY": "1"}, control)
        ready.validate()

    def test_window_is_refused_for_an_expiry_beyond_fourteen_days(self) -> None:
        control = lc.parse(document(expires_at="2027-11-09T10:00:00Z"))
        with self.assertRaises(StreamError):
            rx.window_seconds(control, 60.0, NOW)
        with self.assertRaises(StreamError):
            asyncio.run(rx.run_window(control, {}, object(), 60.0, 10, NOW))  # type: ignore[arg-type]

    def test_window_is_refused_when_stopped_or_expired(self) -> None:
        for control in (lc.parse(document(enabled=False)), lc.parse(document())):
            moment = NOW if not control.enabled else control.expires_at
            with self.assertRaises(StreamError) as caught:
                asyncio.run(rx.run_window(control, {}, object(), 60.0, 10, moment))  # type: ignore[arg-type]
            self.assertEqual(str(caught.exception), "CONTROL_NOT_SENDING")

    def test_window_is_capped_at_the_expiry(self) -> None:
        seen: dict[str, Any] = {}

        class Fake:
            def __init__(self, ingestion: object, act: object, bound: tuple[object, ...]) -> None:
                seen["bound"] = len(bound)

            async def run(
                self, *, max_seconds: float, max_events: int, stop: asyncio.Event
            ) -> tuple[int, ...]:
                seen["seconds"] = max_seconds
                return (1, 2)

        control = lc.parse(document())
        count = asyncio.run(
            rx.run_window(
                control,
                {},
                object(),  # type: ignore[arg-type]
                240.0,
                10,
                control.expires_at - timedelta(seconds=30),
                receiver_type=Fake,  # type: ignore[arg-type]
            )
        )
        self.assertEqual((count, seen), (2, {"bound": 3, "seconds": 30.0}))

    def test_main_without_control_file_is_refused(self) -> None:
        self.assertEqual(rx.main([], {}), 2)


class RefreshRegressionTests(unittest.TestCase):
    def test_cohort_changed_to_absent_homes_sends_nothing_more(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            lc.write(path, lc.parse(document(homes=HOMES[:2])))
            sink, calls = ls.MemorySink(), {"n": 0}

            def list_homes() -> list[str]:
                calls["n"] += 1
                if calls["n"] == 2:
                    lc.write(path, lc.parse(document(homes=["HOME-900"])))
                return ls.cohort_homes(lc.load(path), HOMES)

            summaries = asyncio.run(
                ls.run(
                    list_homes,
                    lr.Generator(1),
                    sink,
                    ls.Limits(max_per_second=100.0),
                    max_slots=5,
                    refresh_slots=1,
                    now=lambda: NOW,
                    sleep=_no_sleep,
                )
            )
        self.assertEqual(len(summaries), 1)
        self.assertEqual(len(sink.messages), 2)

    def test_cohort_removal_is_refused_not_cached(self) -> None:
        sink = ls.MemorySink()

        def list_homes() -> list[str]:
            raise StreamError("COHORT_NOT_IN_STORE")

        summaries = asyncio.run(
            ls.run(
                list_homes,
                lr.Generator(1),
                sink,
                ls.Limits(max_per_second=100.0),
                once=True,
                now=lambda: NOW,
            )
        )
        self.assertEqual((summaries, sink.messages), ([], []))


async def _no_sleep(seconds: float) -> None:
    return None


class ReceiverStopTests(unittest.TestCase):
    def run_with_change(self, change: Any, expires: str = EXPIRES) -> dict[str, Any]:
        seen: dict[str, Any] = {"ingested": 0}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            control = lc.parse(document(expires_at=expires))
            lc.write(path, control)

            class Fake:
                def __init__(self, i: object, a: object, b: tuple[object, ...]) -> None:
                    pass

                async def run(
                    self, *, max_seconds: float, max_events: int, stop: asyncio.Event
                ) -> tuple[int, ...]:
                    seen["seconds"] = max_seconds
                    change(path, control)
                    for _ in range(50):
                        if stop.is_set():
                            break
                        await asyncio.sleep(0.01)
                        seen["ingested"] += 1
                    seen["stopped"] = stop.is_set()
                    return ()

            asyncio.run(
                rx.run_window(
                    control,
                    {},
                    object(),  # type: ignore[arg-type]
                    240.0,
                    10,
                    NOW,
                    receiver_type=Fake,  # type: ignore[arg-type]
                    reload=lambda: lc.load(path),
                    clock=lambda: NOW,
                    poll=0.01,
                )
            )
        return seen

    def test_stop_during_window_signals_the_receiver(self) -> None:
        seen = self.run_with_change(
            lambda p, c: lc.write(p, lc.parse(c.as_document() | {"enabled": False}))
        )
        self.assertTrue(seen["stopped"])
        self.assertLess(seen["ingested"], 5)

    def test_invalid_file_and_changed_cohort_also_stop(self) -> None:
        self.assertTrue(
            self.run_with_change(lambda p, c: p.write_text("{", encoding="utf-8"))["stopped"]
        )
        other = lambda p, c: lc.write(p, lc.parse(c.as_document() | {"homes": [HOMES[5]]}))  # noqa: E731
        self.assertTrue(self.run_with_change(other)["stopped"])

    def test_expiry_during_window_stops(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            control = lc.parse(document())
            lc.write(path, control)
            ticks = iter([NOW, control.expires_at, control.expires_at])
            stop = asyncio.Event()
            asyncio.run(rx._watch(control, lambda: lc.load(path), lambda: next(ticks), stop, 0.0))
        self.assertTrue(stop.is_set())

    def test_rewrite_beyond_fourteen_days_during_window_stops(self) -> None:
        seen = self.run_with_change(
            lambda p, c: lc.write(
                p, lc.parse(c.as_document() | {"expires_at": "2027-11-09T10:00:00Z"})
            )
        )
        self.assertTrue(seen["stopped"])
        self.assertLess(seen["ingested"], 5)

    def test_sub_second_remaining_is_refused_not_rounded_up(self) -> None:
        control = lc.parse(document())
        with self.assertRaises(StreamError):
            asyncio.run(
                rx.run_window(
                    control,
                    {},
                    object(),  # type: ignore[arg-type]
                    60.0,
                    10,
                    control.expires_at - timedelta(milliseconds=500),
                )
            )


class ReceiverStartupTests(unittest.TestCase):
    """A refused control must not reach persistence; a valid one builds the sensor connector."""

    def run_main(self, change: dict[str, Any] | str, env: dict[str, str]) -> tuple[int, list[str]]:
        built: list[str] = []
        future = (datetime.now(UTC) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.json"
            if isinstance(change, str):
                path.write_text(change, encoding="utf-8")
            else:
                path.write_text(json.dumps(document(expires_at=future) | change), encoding="utf-8")

            def persistence(_env: Any) -> object:
                built.append("persistence")
                return object()

            class Ingestion:
                def __init__(self, _store: object) -> None:
                    built.append("ingestion")

            async def window(*_a: Any, **_k: Any) -> int:
                return 3

            saved = (rx.persistence, rx.SensorIngestion, rx.run_window)  # type: ignore[attr-defined]
            rx.persistence, rx.SensorIngestion, rx.run_window = persistence, Ingestion, window  # type: ignore[assignment,attr-defined]
            try:
                code = rx.main(["--control-file", str(path)], env)
            finally:
                rx.persistence, rx.SensorIngestion, rx.run_window = saved  # type: ignore[attr-defined]
        return code, built

    def test_stopped_expired_and_invalid_control_never_reach_persistence(self) -> None:
        cases: list[dict[str, Any] | str] = [
            {"enabled": False},
            {"expires_at": "2026-01-01T00:00:00Z"},
            {
                "expires_at": (datetime.now(UTC) + timedelta(milliseconds=400)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            },
            "{",
        ]
        for case in cases:
            with self.subTest(case=str(case)[:40]):
                code, built = self.run_main(case, {})
                self.assertEqual((code, built), (2, []))

    def test_valid_control_builds_persistence_then_runs(self) -> None:
        code, built = self.run_main({}, {})
        self.assertEqual((code, built), (0, ["persistence", "ingestion"]))

    def test_mssql_uses_the_sensor_connector_without_connecting_or_open_store(self) -> None:
        from zava_forward.core import factory
        from zava_forward.core.sensor_sql import SensorMssqlConnector

        env = {
            "ZF_STORE": "mssql",
            "ZF_SQL_SERVER": "sql.example.invalid",
            "ZF_SQL_DATABASE": "db",
            "ZF_SQL_AUTH": "msi",
            "ZF_SQL_CLIENT_ID": "00000000-0000-0000-0000-000000000000",
        }
        saved = factory.open_store

        def forbidden(_env: Any = None) -> object:
            raise AssertionError("application store must not be opened")

        factory.open_store = forbidden
        try:
            self.assertIsInstance(rx.persistence(env), SensorMssqlConnector)
        finally:
            factory.open_store = saved
        with self.assertRaises(SystemExit):
            rx.persistence({"ZF_STORE": "mssql"})


class ReceiverJobContractTests(unittest.TestCase):
    text = (Path(__file__).resolve().parents[3] / "infra" / "live-receiver-job.bicep").read_text()
    sim = (Path(__file__).resolve().parents[3] / "infra" / "live-simulator-job.bicep").read_text()

    def test_receiver_job_is_manual_with_its_own_identity_and_command(self) -> None:
        for needle in (
            "triggerType: 'Manual'",
            "zava_forward.api.live_receiver",
            "ZF_SIM_CLIENT_ID",
            "ZF_SIM_ROUTING_READY",
            "param routingReady bool = false",
            "/certs/control.json",
            "ZF_STORE', value: 'mssql'",
            "mountOptions: 'ro'",
        ):
            self.assertIn(needle, self.text)
        self.assertNotIn("zava_forward.api.live_simulator", self.text)

    def test_simulator_job_keeps_its_read_only_scheduled_shape(self) -> None:
        self.assertIn("zava_forward.api.live_simulator", self.sim)
        self.assertIn("triggerType: 'Schedule'", self.sim)
        self.assertNotIn("ZF_SIM_CLIENT_ID", self.sim)
        self.assertNotIn("live_receiver", self.sim)


class SecretHygieneTests(unittest.TestCase):
    def test_control_document_holds_no_credential_field(self) -> None:
        text = json.dumps(lc.parse(document()).as_document()).lower()
        for word in ("key", "secret", "connection", "password", "token", "sas"):
            self.assertNotIn(word, text)


if __name__ == "__main__":
    unittest.main()
