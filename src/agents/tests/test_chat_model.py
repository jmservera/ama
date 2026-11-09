import io
import json
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import dataset
from zava_forward.core.ai import Ai
from zava_forward.core.ai_consumption import DispatchHeld
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel, ModelReply, ModelUnavailable
from zava_forward.core.store import Store

from zava_forward.agents.chat import ChatModel
from zava_forward.agents.dispatch import AgentWorker, foundry_provider


def worker(result: Any) -> AgentWorker:
    def provider(system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
        if isinstance(result, Exception):
            raise result
        return result  # type: ignore[no-any-return]

    return AgentWorker(provider)


class Ledger:
    """Synthetic financial meter: each step can hold, as the core ledger does."""

    def __init__(
        self, reserve: str | None = None, check: str | None = None, complete: str | None = None
    ) -> None:
        self.holds = dict(reserve=reserve, check=check, complete=complete)

    def hold(self, step: str) -> None:
        if self.holds[step]:
            raise DispatchHeld(self.holds[step])

    def reserve(self, *args: Any, **kwargs: Any) -> str:
        self.hold("reserve")
        return "synthetic-reservation"

    def dispatch_check(self, rid: str) -> None:
        self.hold("check")

    def complete(self, *args: Any, **kwargs: Any) -> None:
        self.hold("complete")


def metered_model(ledger: Ledger | None, fail_transport: bool = False) -> tuple[ChatModel, Mock]:
    """The real core Ai behind the real adapter; only the transport is a counted stub."""
    ai = Ai()
    ai.endpoint = "https://synthetic.invalid"
    ai.consumption = ledger
    reply = dict(
        model=ai.model_version,
        choices=[dict(message=dict(content="PRIVATE-ANSWER"))],
        usage=dict(prompt_tokens=5, completion_tokens=2, total_tokens=7),
    )
    transport = Mock(
        side_effect=OSError("PRIVATE-TRANSPORT") if fail_transport else None,
        return_value=nullcontext(io.BytesIO(json.dumps(reply).encode())),
    )
    model = ChatModel(AgentWorker(foundry_provider(ai)), admission=lambda: None)
    patches = (
        patch.object(ai, "_token", return_value="synthetic"),
        patch("urllib.request.urlopen", transport),
        patch("zava_forward.core.ai.data_protection.dispatch_hold", return_value=None),
    )
    for item in patches:
        item.start()
    return model, transport


class ChatModelTests(unittest.TestCase):
    def tearDown(self) -> None:
        patch.stopall()

    def test_returns_text_from_a_returned_envelope(self) -> None:
        model = ChatModel(worker(dict(outcome="returned", text="hello")), admission=lambda: None)
        self.assertEqual(model("s", "p"), ModelReply("hello"))

    def test_every_failure_is_model_unavailable_without_provider_text(self) -> None:
        for result in (
            RuntimeError("secret provider detail"),
            dict(outcome="timeout", text=None),
            dict(outcome="disabled", text=None),
            dict(outcome="returned", text="  "),
            dict(outcome="returned", text=5),
            "not an envelope",
        ):
            with self.assertRaises(ModelUnavailable) as caught:
                ChatModel(worker(result), admission=lambda: None)("s", "p")
            self.assertNotIn("secret", str(caught.exception))

    def test_denied_admission_makes_no_provider_call(self) -> None:
        def forbidden(*args: Any) -> dict[str, Any]:
            self.fail("provider called without admission")

        for admission in (None, lambda: "not approved"):
            with self.assertRaises(ModelUnavailable) as caught:
                ChatModel(AgentWorker(forbidden), admission=admission)("s", "p")
            self.assertEqual(caught.exception.calls, 0)

    def test_completion_revocation_preserves_usage_but_not_text(self) -> None:
        allowed = True
        usage = dict(prompt_tokens=5, completion_tokens=2, total_tokens=7)

        def provider(*args: Any) -> dict[str, Any]:
            nonlocal allowed
            allowed = False
            return dict(outcome="returned", text="PRIVATE-ANSWER", usage=usage)

        with self.assertRaises(ModelUnavailable) as caught:
            ChatModel(AgentWorker(provider), admission=lambda: None if allowed else "revoked")(
                "s", "p"
            )
        self.assertEqual((caught.exception.calls, caught.exception.usage), (1, usage))
        self.assertNotIn("PRIVATE", str(caught.exception))

    def test_callback_exceptions_preserve_only_actual_provider_consumption(self) -> None:
        usage = dict(prompt_tokens=5, completion_tokens=2, total_tokens=7)
        for completion, disabled in ((False, False), (True, False), (True, True)):
            with self.subTest(completion=completion, disabled=disabled):
                provider = Mock(
                    return_value=dict(
                        outcome="disabled" if disabled else "returned",
                        text="PRIVATE-ANSWER",
                        usage=None if disabled else usage,
                    )
                )
                admission = Mock(
                    side_effect=[None, RuntimeError("PRIVATE-CALLBACK")]
                    if completion
                    else RuntimeError("PRIVATE-CALLBACK")
                )
                with self.assertLogs("zava_forward.agents.chat", level="WARNING") as logs:
                    with self.assertRaises(ModelUnavailable) as caught:
                        ChatModel(AgentWorker(provider), admission=admission)("s", "p")
                self.assertEqual(provider.call_count, int(completion))
                self.assertEqual(caught.exception.calls, int(completion and not disabled))
                self.assertEqual(
                    caught.exception.usage, usage if completion and not disabled else None
                )
                self.assertEqual(
                    caught.exception.outcome,
                    "completion-check-failed" if completion else "admission-check-failed",
                )
                self.assertNotIn("PRIVATE", str(caught.exception))
                self.assertNotIn("PRIVATE", " ".join(logs.output))

    def test_callback_exception_receipts_match_provider_and_audit(self) -> None:
        usage = dict(prompt_tokens=5, completion_tokens=2, total_tokens=7)
        for completion in (False, True):
            with self.subTest(completion=completion), tempfile.TemporaryDirectory() as work:
                path = Path(work) / "synthetic.json"
                path.write_text(json.dumps(dataset.DATA))
                store = Store(str(path))
                user = store.data["staff"][0]
                iso = ChatIsolation(
                    store,
                    env=dict(
                        CHAT_DPIA_REF="SYN-DPIA",
                        CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
                        CHAT_NOTICE_REF="SYN-NOTICE",
                    ),
                )
                provider = Mock(
                    return_value=dict(outcome="returned", text="PRIVATE-ANSWER", usage=usage)
                )
                admission = Mock(
                    side_effect=[None, RuntimeError("PRIVATE-CALLBACK")]
                    if completion
                    else RuntimeError("PRIVATE-CALLBACK")
                )
                panel = ChatPanel(iso, ChatModel(AgentWorker(provider), admission=admission))
                tid = store.chat_create_thread(user)["id"]
                with self.assertLogs("zava_forward.agents.chat", level="WARNING"):
                    answer = panel.ask(user, tid, "What help is available?", skill="general")
                receipt = answer["consumption"]
                self.assertEqual(answer["kind"], "fallback")
                self.assertNotIn("PRIVATE", json.dumps(answer))
                self.assertEqual(receipt["model_calls"], provider.call_count)
                self.assertEqual(receipt["tokens"], usage if completion else None)
                self.assertEqual(
                    receipt["provider_outcome"],
                    "completion-check-failed" if completion else "admission-check-failed",
                )
                turns = [r for r in store.audit_entries() if r["action"] == "chat.turn"]
                self.assertEqual(json.loads(turns[-1]["detail"]), receipt)

    def test_hold_before_reservation_reports_zero_calls_like_the_transport(self) -> None:
        for label, ledger in (
            ("meter missing", None),
            ("reserve held", Ledger(reserve="authority-unknown")),
        ):
            with self.subTest(label), self.assertRaises(ModelUnavailable) as caught:
                model, transport = metered_model(ledger)
                try:
                    model("s", "p")
                finally:
                    self.assertEqual(transport.call_count, 0)
            self.assertEqual((caught.exception.calls, caught.exception.usage), (0, None))
            self.assertEqual(caught.exception.outcome, "provider-unavailable")
            self.assertNotIn("PRIVATE", str(caught.exception))

    def test_hold_after_transport_keeps_the_actual_attempt_count(self) -> None:
        for label, fail in (("response then hold", False), ("failure then hold", True)):
            with self.subTest(label), self.assertRaises(ModelUnavailable) as caught:
                model, transport = metered_model(Ledger(complete="meter-capacity-reached"), fail)
                try:
                    model("s", "p")
                finally:
                    self.assertEqual(transport.call_count, 1)
            self.assertEqual(caught.exception.calls, 1)
            self.assertNotIn("PRIVATE", str(caught.exception))

    def test_reserved_hold_before_transport_is_counted_conservatively(self) -> None:
        # The envelope cannot tell this hold from a later failure; never under-report an attempt.
        model, transport = metered_model(Ledger(check="liability-unknown"))
        with self.assertRaises(ModelUnavailable) as caught:
            model("s", "p")
        self.assertEqual((transport.call_count, caught.exception.calls), (0, 1))

    def test_provider_failure_still_counts_the_attempt(self) -> None:
        model, transport = metered_model(Ledger(), fail_transport=True)
        with self.assertRaises(ModelUnavailable) as caught:
            model("s", "p")
        self.assertEqual((transport.call_count, caught.exception.calls), (1, 1))
        self.assertNotIn("PRIVATE", str(caught.exception))

    def test_input_refusal_is_a_pre_call_outcome(self) -> None:
        model = ChatModel(
            worker(dict(outcome="input-refused", text=None, reason="input-too-large")),
            admission=lambda: None,
        )
        with self.assertRaises(ModelUnavailable) as caught:
            model("s", "p")
        self.assertEqual(caught.exception.calls, 0)

    def test_panel_receipt_and_audit_match_the_transport_for_financial_holds(self) -> None:
        for label, ledger, expected in (
            ("meter missing", None, 0),
            ("reserve held", Ledger(reserve="authority-unknown"), 0),
            ("hold after transport", Ledger(complete="meter-capacity-reached"), 1),
        ):
            with self.subTest(label), tempfile.TemporaryDirectory() as work:
                path = Path(work) / "synthetic.json"
                path.write_text(json.dumps(dataset.DATA))
                store = Store(str(path))
                user = store.data["staff"][0]
                iso = ChatIsolation(
                    store,
                    env=dict(
                        CHAT_DPIA_REF="SYN-DPIA",
                        CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
                        CHAT_NOTICE_REF="SYN-NOTICE",
                    ),
                )
                model, transport = metered_model(ledger)
                panel = ChatPanel(iso, model)
                tid = store.chat_create_thread(user)["id"]
                answer = panel.ask(user, tid, "What help is available?", skill="general")
                receipt = answer["consumption"]
                self.assertEqual(answer["kind"], "fallback")
                self.assertNotIn("PRIVATE", json.dumps(answer))
                self.assertEqual(receipt["model_calls"], transport.call_count)
                self.assertEqual(receipt["model_calls"], expected)
                self.assertEqual(receipt["provider_outcome"], "provider-unavailable")
                turns = [r for r in store.audit_entries() if r["action"] == "chat.turn"]
                self.assertEqual(json.loads(turns[-1]["detail"]), receipt)

    def test_usage_is_per_invocation_and_rejects_malformed_values(self) -> None:
        for usage in (
            dict(prompt_tokens=5, completion_tokens=2, total_tokens=7),
            dict(prompt_tokens=True, completion_tokens=2, total_tokens=3),
            dict(prompt_tokens=-1, completion_tokens=2, total_tokens=1),
            dict(prompt_tokens=5, completion_tokens=2, total_tokens=8),
            None,
        ):
            model = ChatModel(
                worker(dict(outcome="returned", text="ok", usage=usage)), admission=lambda: None
            )
            result = model("s", "p")
            self.assertEqual(result.usage, usage if usage and usage["total_tokens"] == 7 else None)


if __name__ == "__main__":
    unittest.main()
