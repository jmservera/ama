import contextlib
import io
import threading
import unittest
from typing import Any

from test_dispatch import Sink, good_text, limits, message, returned
from zava_forward.agents.dispatch import AgentWorker, InMemoryQueue, TaskMessage
from zava_forward.agents.version import __version__
from zava_forward.agents.worker import NOT_CONFIGURED, main, serve


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

    def test_serve_refuses_without_transport(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(main(["serve"]), NOT_CONFIGURED)
        self.assertIn("no tasks will be processed", err.getvalue())


if __name__ == "__main__":
    unittest.main()
