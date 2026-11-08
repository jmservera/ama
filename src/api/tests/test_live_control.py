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

            async def run(self, *, max_seconds: float, max_events: int) -> tuple[int, ...]:
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


class SecretHygieneTests(unittest.TestCase):
    def test_control_document_holds_no_credential_field(self) -> None:
        text = json.dumps(lc.parse(document()).as_document()).lower()
        for word in ("key", "secret", "connection", "password", "token", "sas"):
            self.assertNotIn(word, text)


if __name__ == "__main__":
    unittest.main()
