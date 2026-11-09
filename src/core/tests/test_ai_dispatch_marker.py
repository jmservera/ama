"""The per-invocation dispatch witness records transport hand-offs of the real Ai (#891).

Constructed data only: the transport, token and guard are stubs; no network, SDK or provider call.
"""

from __future__ import annotations

import io
import json
import threading
import unittest
from contextlib import nullcontext
from typing import Any
from unittest import mock

from zava_forward.core import ai as core_ai
from zava_forward.core.ai import Ai as UntypedAi
from zava_forward.core.ai_consumption import DispatchHeld

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
        cases: dict[str, Any] = {
            "unconfigured": lambda: setattr(self.ai, "endpoint", ""),
            "meter missing": lambda: setattr(self.ai, "consumption", None),
            "reserve held": lambda: setattr(self.ai, "consumption", Ledger(reserve="held")),
            "check held after reservation": lambda: setattr(
                self.ai, "consumption", Ledger(check="held")
            ),
            "token failure": lambda: setattr(
                self.ai, "_token", mock.Mock(side_effect=OSError("synthetic"))
            ),
            "guard denial": lambda: mock.patch(
                "zava_forward.core.ai.data_protection.dispatch_hold", return_value="denied"
            ).start(),
            "input refusal": lambda: None,
        }
        for label, arrange in cases.items():
            with self.subTest(label):
                self.setUp()
                arrange()
                user = "x" * (core_ai.MAX_TEXT_BYTES + 1) if label == "input refusal" else "p"
                attempts, envelope = self.attempts(user)
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


if __name__ == "__main__":
    unittest.main()
