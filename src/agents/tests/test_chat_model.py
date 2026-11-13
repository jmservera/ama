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


def metered_model(
    ledger: Ledger | None,
    fail_transport: bool = False,
    guard: str | None = None,
    token_error: bool = False,
) -> tuple[ChatModel, Mock]:
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
        patch.object(
            ai,
            "_token",
            **(
                dict(side_effect=OSError("PRIVATE-TOKEN"))
                if token_error
                else dict(return_value="synthetic")
            ),
        ),
        patch("urllib.request.urlopen", transport),
        patch("zava_forward.core.ai.data_protection.dispatch_hold", return_value=guard),
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
                # A stub provider is unverified: one call is assumed.
                self.assertEqual(caught.exception.calls, int(completion))
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

    def test_every_pre_dispatch_exit_reports_the_zero_transport_count(self) -> None:
        for label, ledger, options in (
            ("meter missing", None, {}),
            ("reserve held", Ledger(reserve="authority-unknown"), {}),
            ("check held after reservation", Ledger(check="liability-unknown"), {}),
            ("prompt-output guard denial", Ledger(), dict(guard="held")),
            ("token failure after reservation", Ledger(), dict(token_error=True)),
        ):
            with self.subTest(label), self.assertRaises(ModelUnavailable) as caught:
                model, transport = metered_model(ledger, **options)
                try:
                    model("s", "p")
                finally:
                    self.assertEqual(transport.call_count, 0)
            self.assertEqual((caught.exception.calls, caught.exception.usage), (0, None))
            self.assertEqual(caught.exception.outcome, "provider-unavailable")
            self.assertNotIn("PRIVATE", str(caught.exception))

    def test_real_input_refusal_is_zero_calls(self) -> None:
        model, transport = metered_model(Ledger())
        with self.assertRaises(ModelUnavailable) as caught:
            model("s", "x" * 200_000)
        self.assertEqual((transport.call_count, caught.exception.calls), (0, 0))

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

    def test_provider_failure_still_counts_the_attempt(self) -> None:
        model, transport = metered_model(Ledger(), fail_transport=True)
        with self.assertRaises(ModelUnavailable) as caught:
            model("s", "p")
        self.assertEqual((transport.call_count, caught.exception.calls), (1, 1))
        self.assertNotIn("PRIVATE", str(caught.exception))

    def test_post_dispatch_failures_carry_the_meter_reference(self) -> None:
        for outcome in ("timeout", "disabled", "provider-unavailable", "returned"):
            envelope = dict(outcome=outcome, text=" ", meter_id="rid-1", meter_root="root-1")
            with self.subTest(outcome), self.assertRaises(ModelUnavailable) as caught:
                ChatModel(worker(envelope), admission=lambda: None)("s", "p")
            self.assertEqual(
                (getattr(caught.exception, "meter_id", "missing"), caught.exception.meter_root),
                ("rid-1", "root-1"),
            )

    def test_completion_check_failures_carry_the_meter_reference(self) -> None:
        envelope = dict(outcome="returned", text="x", meter_id="rid-2", meter_root="root-2")

        def second_check(result: str | Exception) -> Any:
            calls = iter([None, result])

            def admission() -> str | None:
                value = next(calls)
                if isinstance(value, Exception):
                    raise value
                return value

            return admission

        for label, result in (("revoked", "revoked"), ("raises", RuntimeError("down"))):
            with self.subTest(label), self.assertRaises(ModelUnavailable) as caught:
                ChatModel(worker(envelope), admission=second_check(result))("s", "p")
            self.assertEqual(
                (caught.exception.calls, caught.exception.meter_id, caught.exception.meter_root),
                (1, "rid-2", "root-2"),
            )

    def test_unusable_meter_values_and_pre_dispatch_denials_carry_none(self) -> None:
        bad = dict(outcome="timeout", meter_id=7, meter_root=["x"])
        with self.assertRaises(ModelUnavailable) as caught:
            ChatModel(worker(bad), admission=lambda: None)("s", "p")
        self.assertEqual((caught.exception.meter_id, caught.exception.meter_root), (None, None))

        def boom() -> None:
            raise RuntimeError("x")

        for admission in (None, lambda: "not approved", boom):
            with self.assertRaises(ModelUnavailable) as caught:
                ChatModel(worker(dict(outcome="returned", text="x")), admission=admission)("s", "p")
            self.assertEqual(
                (caught.exception.calls, caught.exception.meter_id, caught.exception.meter_root),
                (0, None, None),
            )

    def test_real_ai_failures_keep_the_reference_only_once_reserved(self) -> None:
        for label, ledger, fail, reserved in (
            ("transport failure", Ledger(), True, True),
            ("hold after response", Ledger(complete="meter-capacity-reached"), False, True),
            ("check hold before transport", Ledger(check="meter-capacity-reached"), False, True),
            ("hold at reserve", Ledger(reserve="meter-capacity-reached"), False, False),
        ):
            model, _ = metered_model(ledger, fail)
            with self.subTest(label), self.assertRaises(ModelUnavailable) as caught:
                model("s", "p")
            self.assertEqual(
                caught.exception.meter_id, "synthetic-reservation" if reserved else None
            )
            self.assertEqual(isinstance(caught.exception.meter_root, str), reserved)

    def test_a_provider_that_is_not_core_ai_is_an_explicit_unverified_count(self) -> None:
        spoofed = dict(outcome="disabled", text=None, usage=None, meter_id=None, dispatches=0)
        model = ChatModel(worker(spoofed), admission=lambda: None)
        with (
            self.assertLogs("zava_forward.agents.chat", level="WARNING") as logs,
            self.assertRaises(ModelUnavailable) as caught,
        ):
            model("s", "p")
        self.assertEqual(caught.exception.calls, 1)
        self.assertIn("unverified", " ".join(logs.output))

    def test_panel_receipt_and_audit_match_the_transport_for_financial_holds(self) -> None:
        for label, ledger, expected in (
            ("meter missing", None, 0),
            ("reserve held", Ledger(reserve="authority-unknown"), 0),
            ("check held after reservation", Ledger(check="liability-unknown"), 0),
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
