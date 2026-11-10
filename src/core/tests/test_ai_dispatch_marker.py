"""The per-invocation dispatch witness records transport hand-offs of the real Ai (#891).

Constructed data only: the transport, token and guard are stubs; no network, SDK or provider call.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import threading
import unittest
import urllib.error
from contextlib import nullcontext
from email.message import Message
from typing import Any
from unittest import mock

from zava_forward.core import ai as core_ai
from zava_forward.core import data_protection
from zava_forward.core.ai import Ai as UntypedAi
from zava_forward.core.ai_consumption import DispatchHeld, DispatchWithdrawn

Ai: Any = UntypedAi
count_dispatches: Any = getattr(core_ai, "count_dispatches", None)


class Ledger:
    """Synthetic financial meter: each step can hold, as the core ledger does."""

    def __init__(self, **holds: str) -> None:
        self.holds = holds

    def hold(self, step: str) -> None:
        if self.holds.get(step):
            raise DispatchHeld(self.holds[step])

    def reserve(self, *args: Any, **kwargs: Any) -> str:
        self.hold("reserve")
        return "synthetic-reservation"

    def dispatch_check(self, rid: str) -> None:
        self.hold("check")

    def complete(self, *args: Any, **kwargs: Any) -> None:
        self.hold("complete")


class DispatchWitness(unittest.TestCase):
    def setUp(self) -> None:
        self.ai = Ai()
        self.ai.endpoint = "https://synthetic.invalid"
        self.ai.consumption = Ledger()
        self.reply = dict(
            model=self.ai.model_version,
            choices=[dict(message=dict(content="ANSWER"))],
            usage=dict(prompt_tokens=5, completion_tokens=2, total_tokens=7),
        )
        self.transport = mock.Mock(side_effect=self.respond)
        for patcher in (
            mock.patch.object(self.ai, "_token", return_value="synthetic"),
            mock.patch("urllib.request.urlopen", self.transport),
            mock.patch("zava_forward.core.ai.data_protection.dispatch_hold", return_value=None),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def respond(self, *args: Any, **kwargs: Any) -> Any:
        return nullcontext(io.BytesIO(json.dumps(self.reply).encode()))

    def attempts(self, user: str = "p") -> tuple[int, dict[str, Any]]:
        with count_dispatches() as witness:
            envelope = self.ai.evidence("s", user)
        self.assertTrue(witness.witnessed)
        return witness.attempts, envelope

    def test_attempts_equal_the_transport_for_every_pre_dispatch_exit(self) -> None:
        def broken_token() -> Any:
            return mock.patch.object(self.ai, "_token", side_effect=OSError("synthetic"))

        cases: dict[str, Any] = {
            "unconfigured": dict(endpoint=""),
            "meter missing": dict(consumption=None),
            "reserve held": dict(consumption=Ledger(reserve="held")),
            "check held after reservation": dict(consumption=Ledger(check="held")),
            "token failure": dict(patch=broken_token),
            "guard denial": dict(
                patch=lambda: mock.patch.object(
                    data_protection, "dispatch_hold", return_value="denied"
                )
            ),
            "input refusal": dict(user="x" * (core_ai.MAX_TEXT_BYTES + 1)),
        }
        for label, case in cases.items():
            with self.subTest(label), contextlib.ExitStack() as stack:
                for name in ("endpoint", "consumption"):
                    if name in case:
                        stack.enter_context(mock.patch.object(self.ai, name, case[name]))
                if "patch" in case:
                    stack.enter_context(case["patch"]())
                attempts, envelope = self.attempts(case.get("user", "p"))
                self.assertEqual((attempts, self.transport.call_count), (0, 0))
                self.assertNotEqual(envelope["outcome"], "returned")

    def test_attempts_include_success_failure_and_completion_hold(self) -> None:
        self.assertEqual(self.attempts()[0], 1)
        self.assertEqual(self.transport.call_count, 1)
        self.transport.reset_mock()
        self.transport.side_effect = OSError("synthetic")
        attempts, envelope = self.attempts()
        self.assertEqual((attempts, self.transport.call_count), (1, 1))
        self.assertEqual(envelope["outcome"], "provider-unavailable")
        self.transport.reset_mock()
        self.transport.side_effect = self.respond
        self.ai.consumption = Ledger(complete="held")
        attempts, envelope = self.attempts()
        self.assertEqual((attempts, self.transport.call_count), (1, 1))
        self.assertEqual(envelope["outcome"], "financial-held")

    def handed_off(self, error: Exception) -> tuple[int, dict[str, Any]]:
        opener = mock.Mock()
        opener.open.side_effect = error
        with (
            mock.patch("zava_forward.core.ai.ai_consumption.SEND_FENCE") as fence,
            mock.patch("zava_forward.core.ai.ai_transport.opener", return_value=opener),
        ):
            fence.get.return_value = lambda: None
            attempts, envelope = self.attempts()
        self.assertEqual(
            (attempts, opener.open.call_count, self.transport.call_count), (attempts, 1, 0)
        )
        return attempts, envelope

    def test_withdrawal_timeout_and_http_error_after_handoff_count_one(self) -> None:
        for error, outcome in (
            (
                DispatchWithdrawn("fence-stalled"),
                "suspended-before-dispatch",
            ),
            (TimeoutError("synthetic"), "timeout"),
            (
                urllib.error.HTTPError(
                    "https://synthetic.invalid", 500, "x", Message(), io.BytesIO()
                ),
                "provider-unavailable",
            ),
        ):
            with self.subTest(outcome):
                attempts, envelope = self.handed_off(error)
                self.assertEqual((attempts, envelope["outcome"]), (1, outcome))

    def test_opener_construction_failure_is_not_an_attempt(self) -> None:
        with (
            mock.patch("zava_forward.core.ai.ai_consumption.SEND_FENCE") as fence,
            mock.patch("zava_forward.core.ai.ai_transport.opener", side_effect=OSError("x")),
        ):
            fence.get.return_value = lambda: None
            attempts, _ = self.attempts()
        self.assertEqual((attempts, self.transport.call_count), (0, 0))

    def test_concurrent_invocations_keep_separate_counts(self) -> None:
        barrier = threading.Barrier(2)
        results: dict[str, int] = {}

        class Gate(Ledger):
            def reserve(self, *args: Any, **kwargs: Any) -> str:
                barrier.wait(5)
                return super().reserve()

        def call(name: str, ledger: Ledger) -> None:
            ai = Ai()
            ai.endpoint = self.ai.endpoint
            ai.consumption = ledger
            with mock.patch.object(ai, "_token", return_value="synthetic"):
                with count_dispatches() as witness:
                    ai.evidence("s", "p")
            results[name] = witness.attempts

        threads = [
            threading.Thread(target=call, args=("sent", Gate())),
            threading.Thread(target=call, args=("held", Gate(check="held"))),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(10)
        self.assertEqual(results, dict(sent=1, held=0))
        self.assertEqual(self.transport.call_count, 1)

    def test_nested_scope_counts_only_its_own_invocation(self) -> None:
        with count_dispatches() as outer:
            with count_dispatches() as inner:
                self.ai.evidence("s", "p")
        self.assertEqual((inner.attempts, outer.attempts, outer.witnessed), (1, 0, False))

    def test_late_dispatch_after_the_scope_closes_is_ignored(self) -> None:
        import contextvars

        with count_dispatches() as witness:
            context = contextvars.copy_context()
        context.run(self.ai.evidence, "s", "p")
        self.ai.evidence("s", "p")
        self.assertEqual((witness.witnessed, witness.attempts), (False, 0))
        self.assertEqual(self.transport.call_count, 2)

    def test_context_copied_into_a_thread_counts_while_open(self) -> None:
        import contextvars

        with count_dispatches() as witness:
            context = contextvars.copy_context()
            thread = threading.Thread(target=context.run, args=(self.ai.evidence, "s", "p"))
            thread.start()
            thread.join(10)
        self.assertEqual((witness.attempts, self.transport.call_count), (1, 1))

    def test_without_a_witness_evidence_is_unchanged(self) -> None:
        self.assertEqual(self.ai.evidence("s", "p")["outcome"], "returned")


ISOLATION_SCRIPT = """
import sys, unittest
from unittest import mock
from zava_forward.core import data_protection
import test_ai_dispatch_marker as marker
original = data_protection.dispatch_hold
suite = unittest.defaultTestLoader.loadTestsFromTestCase(marker.DispatchWitness)
result = unittest.TextTestRunner(stream=sys.stderr).run(suite)
assert result.wasSuccessful()
assert data_protection.dispatch_hold is original, "guard leaked after the suite"
mock.patch.stopall()
assert data_protection.dispatch_hold is original, "guard leaked after stopall"
import test_ai_input_bounds as bounds
result = unittest.TextTestRunner(stream=sys.stderr).run(
    unittest.defaultTestLoader.loadTestsFromModule(bounds))
assert result.wasSuccessful()
"""


class GuardPatchIsolation(unittest.TestCase):
    def test_witness_cases_leave_the_process_guard_restored_for_later_modules(self) -> None:
        here = os.path.dirname(os.path.abspath(__file__))
        env = dict(os.environ, PYTHONPATH=os.pathsep.join([here, *sys.path]))
        done = subprocess.run(
            [sys.executable, "-c", ISOLATION_SCRIPT],
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(done.returncode, 0, done.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
