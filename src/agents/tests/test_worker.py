import contextlib
import io
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from test_dispatch import Sink, good_text, limits, message, returned
from zava_forward.agents.dispatch import AgentWorker, InMemoryQueue, TaskMessage
from zava_forward.agents.runtime import HEARTBEAT_MAX_AGE_SECONDS, HEARTBEAT_NAME, healthy
from zava_forward.agents.version import __version__
from zava_forward.agents.worker import (
    ERROR_BACKOFF_SECONDS,
    EXPIRED,
    IDLE_SECONDS,
    NOT_CONFIGURED,
    main,
    serve,
)


def provider(*_: Any) -> dict[str, Any]:
    return returned(good_text())


class ServeTests(unittest.TestCase):
    def test_drains_queue_then_stops_on_event(self) -> None:
        stop = threading.Event()
        queue = InMemoryQueue([message(), message()])
        sink = Sink()
        timer = threading.Timer(0.3, stop.set)
        timer.start()
        done = serve(queue, AgentWorker(provider), sink, limits(), stop, idle=0.05)
        timer.cancel()
        self.assertEqual(done, 2)
        self.assertEqual(len(sink.results), 2)
        self.assertEqual(queue.acked, ["0", "1"])

    def test_post_failure_releases_for_redelivery(self) -> None:
        stop = threading.Event()
        queue = InMemoryQueue([message()])
        sink = Sink(fail=True)
        timer = threading.Timer(0.2, stop.set)
        timer.start()
        done = serve(queue, AgentWorker(provider), sink, limits(), stop, idle=0.05)
        timer.cancel()
        self.assertEqual(done, 0)
        self.assertEqual(queue.acked, [])
        self.assertEqual(len(queue.pending), 1)

    def test_receive_fault_does_not_end_the_loop(self) -> None:
        stop = threading.Event()

        class Flaky:
            calls = 0

            def receive(self) -> tuple[str, TaskMessage] | None:
                self.calls += 1
                if self.calls == 1:
                    raise OSError("queue unavailable")
                stop.set()
                return None

            def ack(self, receipt: str) -> None:
                pass

            def release(self, receipt: str) -> None:
                pass

        flaky = Flaky()
        serve(flaky, AgentWorker(provider), Sink(), limits(), stop, idle=0.01, backoff=0.01)
        self.assertEqual(flaky.calls, 2)

    def test_stop_marks_worker_stopping(self) -> None:
        stop = threading.Event()
        stop.set()
        worker = AgentWorker(provider)
        serve(InMemoryQueue(), worker, Sink(), limits(), stop)
        self.assertTrue(worker.stop_event.is_set())


class MainTests(unittest.TestCase):
    def test_default_prints_version(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main([]), 0)
        self.assertEqual(out.getvalue().strip(), f"zava-forward-agents {__version__}")

    def test_serve_refuses_naming_missing_settings_only(self) -> None:
        err = io.StringIO()
        with (
            patch.dict(
                os.environ,
                {"IDENTITY_HEADER": "sentinel-secret-value", "ZF_AGENT_RESULT_ROUTE": "enabled"},
                clear=True,
            ),
            contextlib.redirect_stderr(err),
        ):
            self.assertEqual(main(["serve"]), NOT_CONFIGURED)
        self.assertIn("QUEUE_ENDPOINT", err.getvalue())
        self.assertIn("No tasks will be processed", err.getvalue())
        self.assertNotIn("sentinel-secret-value", err.getvalue())

    def test_serve_stands_by_without_building_a_queue_when_route_is_off(self) -> None:
        for env in (
            {},
            {"ZF_AGENT_RESULT_ROUTE": "disabled"},
            {"ZF_AGENT_RESULT_ROUTE": "Enabled"},
        ):
            err = io.StringIO()
            with (
                self.subTest(env=env),
                tempfile.TemporaryDirectory() as state,
                patch.dict(os.environ, {**env, "ZF_STATE": state}, clear=True),
                patch("zava_forward.agents.worker.build_runtime") as build,
                patch("zava_forward.agents.worker.install_signal_handlers") as handlers,
                patch("zava_forward.agents.worker.IDLE_SECONDS", 0.01),
                contextlib.redirect_stderr(err),
            ):
                stop = threading.Timer(0.2, lambda: handlers.call_args.args[0].set())
                stop.start()
                self.assertEqual(main(["serve"]), 0)
                stop.cancel()
                build.assert_not_called()
                self.assertTrue(os.path.exists(os.path.join(state, HEARTBEAT_NAME)))
            self.assertEqual(err.getvalue().count("standby"), 1)

    def test_standby_process_is_healthy_and_exits_zero_on_sigterm(self) -> None:
        with tempfile.TemporaryDirectory() as state:
            env = {**os.environ, "ZF_STATE": state}
            env.pop("ZF_AGENT_RESULT_ROUTE", None)
            proc = subprocess.Popen(
                [sys.executable, "-m", "zava_forward.agents", "serve"],
                env=env,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                beat_file = os.path.join(state, HEARTBEAT_NAME)
                for _ in range(100):
                    if os.path.exists(beat_file) or proc.poll() is not None:
                        break
                    time.sleep(0.1)
                self.assertIsNone(proc.poll())
                health = subprocess.run(
                    [sys.executable, "-m", "zava_forward.agents", "health"], env=env
                )
                self.assertEqual(health.returncode, 0)
                proc.send_signal(signal.SIGTERM)
                self.assertEqual(proc.wait(timeout=10), 0)
            finally:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()
                if proc.stderr:
                    proc.stderr.close()

    def test_serve_runs_built_runtime_until_stopped(self) -> None:
        runtime = SimpleNamespace(
            queue=InMemoryQueue([message()]),
            worker=AgentWorker(provider),
            sink=Sink(),
            limits=limits(),
        )
        with (
            patch.dict(os.environ, {"ZF_AGENT_RESULT_ROUTE": "enabled"}),
            patch("zava_forward.agents.worker.build_runtime", return_value=runtime),
            patch("zava_forward.agents.worker.install_signal_handlers") as handlers,
            patch("zava_forward.agents.worker.beat") as heartbeat,
            patch("zava_forward.agents.worker.IDLE_SECONDS", 0.01),
        ):
            stop = threading.Timer(0.3, lambda: handlers.call_args.args[0].set())
            stop.start()
            self.assertEqual(main(["serve"]), 0)
            stop.cancel()
        self.assertEqual(runtime.queue.acked, ["0"])
        self.assertTrue(heartbeat.called)

    def test_expired_allowance_stops_the_loop(self) -> None:
        stop = threading.Event()
        queue = InMemoryQueue([message()])
        done = serve(
            queue, AgentWorker(provider), Sink(), limits(), stop, idle=0.01, alive=lambda: False
        )
        self.assertEqual(done, 0)
        self.assertEqual(queue.acked, [])
        self.assertEqual(EXPIRED, 3)

    def test_health_command_follows_heartbeat(self) -> None:
        with patch("zava_forward.agents.worker.healthy", return_value=True):
            self.assertEqual(main(["health"]), 0)
        with patch("zava_forward.agents.worker.healthy", return_value=False):
            self.assertEqual(main(["health"]), 1)


class Crash(BaseException):
    """Models a replica killed mid-task; `serve` only catches Exception, so this ends it."""


class HeartbeatMarginTests(unittest.TestCase):
    def test_idle_loop_pulses_once_per_iteration(self) -> None:
        stop = threading.Event()
        pulses: list[int] = []

        def pulse() -> None:
            pulses.append(1)
            if len(pulses) == 3:
                stop.set()

        serve(
            InMemoryQueue(), AgentWorker(provider), Sink(), limits(), stop, idle=0.01, pulse=pulse
        )
        self.assertEqual(len(pulses), 3)

    def test_max_age_covers_the_provider_call_bound_and_idle_cadence(self) -> None:
        # Only the provider-call bound (timeout at most 40 s), the fault backoff and the
        # idle wait are covered. Queue, token, post and ack calls are not bounded here.
        self.assertLessEqual(message().timeout, 40)
        margin = 40 + ERROR_BACKOFF_SECONDS + IDLE_SECONDS
        self.assertGreaterEqual(HEARTBEAT_MAX_AGE_SECONDS, 2 * margin)

    def test_age_equal_to_the_limit_is_healthy_and_just_over_is_not(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            beat_file = Path(tmp) / HEARTBEAT_NAME
            beat_file.write_text("1000.0", encoding="utf-8")
            at_limit = 1000.0 + HEARTBEAT_MAX_AGE_SECONDS
            self.assertTrue(healthy(beat_file, HEARTBEAT_MAX_AGE_SECONDS, now=at_limit))
            self.assertFalse(healthy(beat_file, HEARTBEAT_MAX_AGE_SECONDS, now=at_limit + 0.1))


class ReplicaRestartTests(unittest.TestCase):
    def replace_worker(self, queue: InMemoryQueue) -> Sink:
        """A fresh replica drains the queue after the lease of the dead one has expired."""
        for receipt in list(queue.leased):
            queue.release(receipt)
        stop = threading.Event()
        sink = Sink()
        original_ack = queue.ack

        def ack_then_stop(receipt: str) -> None:
            original_ack(receipt)
            stop.set()

        queue.ack = ack_then_stop  # type: ignore[method-assign]
        serve(queue, AgentWorker(provider), sink, limits(), stop, idle=0.01)
        return sink

    def test_crash_before_post_is_redelivered_and_handled_once(self) -> None:
        queue = InMemoryQueue([message()])

        class DyingSink(Sink):
            def post(self, result: Any) -> None:
                raise Crash

        first = DyingSink()
        with self.assertRaises(Crash):
            serve(queue, AgentWorker(provider), first, limits(), threading.Event(), idle=0.01)
        self.assertEqual((first.results, queue.acked, len(queue.leased)), ([], [], 1))
        replacement = self.replace_worker(queue)
        self.assertEqual(len(replacement.results), 1)
        self.assertEqual(queue.acked, ["0"])
        self.assertEqual((queue.pending, queue.leased), ([], {}))

    def test_crash_between_post_and_ack_redelivers_and_reposts(self) -> None:
        queue = InMemoryQueue([message()])
        first = Sink()

        def dying_ack(receipt: str) -> None:
            raise Crash

        queue.ack = dying_ack  # type: ignore[method-assign]
        with self.assertRaises(Crash):
            serve(queue, AgentWorker(provider), first, limits(), threading.Event(), idle=0.01)
        self.assertEqual(len(first.results), 1)
        del queue.ack
        replacement = self.replace_worker(queue)
        # At-least-once: the result is posted again; any dedupe belongs to the receiver.
        self.assertEqual(len(replacement.results), 1)
        self.assertEqual(
            (replacement.results[0].task_id, replacement.results[0].fence),
            (first.results[0].task_id, first.results[0].fence),
        )
        self.assertEqual(queue.acked, ["0"])


if __name__ == "__main__":
    unittest.main()
