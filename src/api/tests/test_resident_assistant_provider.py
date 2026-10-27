"""All model transport and credential/budget callbacks are local mocks."""

import io
import json
import unittest
import urllib.request
from http.client import HTTPMessage
from unittest.mock import Mock, patch

from zava_forward.core.resident_assistant import AssistantUnavailable, Topic

from zava_forward.api.resident_demo.assistant import (
    EXPIRES,
    MAX_OUTPUT_TOKENS,
    MAX_PROMPT_BYTES,
    MAX_REPLY,
    TIMEOUT_SECONDS,
    AzureTopicProvider,
    RequestEnvelope,
    _NoRedirect,
    _post,
)

ENDPOINT = "https://synthetic-test.openai.azure.com"


def reply(content: str = "status", finish: str = "stop") -> bytes:
    return json.dumps(
        {"choices": [{"message": {"content": content}, "finish_reason": finish}]}
    ).encode()


class AzureTopicProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.events: list[str] = []

        def token() -> str:
            self.events.append("token")
            return "FAKE-TOKEN"

        def reserve(envelope: RequestEnvelope) -> bool:
            self.events.append("reserve")
            return True

        def transport(url: str, payload: bytes, token: str) -> bytes:
            self.events.append("transport")
            return reply()

        self.token = Mock(side_effect=token)
        self.reserve = Mock(side_effect=reserve)
        self.transport = Mock(side_effect=transport)

    def provider(self, enabled: bool = False, now: float = EXPIRES - 10) -> AzureTopicProvider:
        return AzureTopicProvider(
            ENDPOINT,
            "review-required",
            enabled=enabled,
            token=self.token,
            reserve=self.reserve,
            transport=self.transport,
            clock=lambda: now,
        )

    def test_disabled_default_does_not_acquire_token_reserve_or_call_transport(self) -> None:
        with self.assertRaises(AssistantUnavailable):
            self.provider().select(Topic.STATUS)
        self.assertEqual(self.events, [])

    def test_expiry_and_missing_activation_controls_fail_before_any_side_effect(self) -> None:
        for now in (EXPIRES, EXPIRES + 1):
            with self.assertRaises(AssistantUnavailable):
                self.provider(True, now).select(Topic.STATUS)
        with self.assertRaises(AssistantUnavailable):
            AzureTopicProvider(ENDPOINT, "test", enabled=True).select(Topic.STATUS)
        self.assertEqual(self.events, [])

    def test_budget_reservation_precedes_credentials_and_fixed_bounded_prompt(self) -> None:
        self.assertEqual(self.provider(True).select(Topic.STATUS), Topic.STATUS)
        self.assertEqual(self.events, ["reserve", "token", "transport"])
        envelope = self.reserve.call_args.args[0]
        self.assertLessEqual(len(envelope.prompt.encode("ascii")), MAX_PROMPT_BYTES)
        self.assertEqual(envelope.max_output_tokens, MAX_OUTPUT_TOKENS)
        url, data, token = self.transport.call_args.args
        self.assertTrue(url.startswith(ENDPOINT + "/openai/deployments/review-required/"))
        payload = json.loads(data)
        self.assertEqual(payload["max_tokens"], 16)
        self.assertEqual(payload["n"], 1)
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["messages"], [{"role": "user", "content": envelope.prompt}])
        self.assertEqual(token, "FAKE-TOKEN")
        self.assertNotIn(token, data.decode())
        for field in ("case_id", "email", "address", "history", "tools"):
            self.assertNotIn(field, data.decode())

    def test_budget_refusal_never_acquires_token_or_calls_transport(self) -> None:
        self.reserve.side_effect = None
        self.reserve.return_value = False
        with self.assertRaises(AssistantUnavailable):
            self.provider(True).select(Topic.STATUS)
        self.token.assert_not_called()
        self.transport.assert_not_called()

    def test_reservation_io_error_is_normalized_before_credentials_or_transport(self) -> None:
        self.reserve.side_effect = OSError("SYNTHETIC-ACCOUNTING-DETAIL")
        with self.assertRaisesRegex(AssistantUnavailable, "^provider_failed$") as caught:
            self.provider(True).select(Topic.STATUS)
        self.assertIsNone(caught.exception.__cause__)
        self.reserve.assert_called_once()
        self.token.assert_not_called()
        self.transport.assert_not_called()

    def test_timeout_keeps_reservation_and_does_not_retry(self) -> None:
        self.transport.side_effect = TimeoutError("SYNTHETIC-SECRET")
        with self.assertRaisesRegex(AssistantUnavailable, "^provider_failed$"):
            self.provider(True).select(Topic.STATUS)
        self.reserve.assert_called_once()
        self.token.assert_called_once()
        self.transport.assert_called_once()

    def test_expiry_during_credential_acquisition_prevents_transport(self) -> None:
        provider = self.provider(True)
        provider.clock = Mock(side_effect=(EXPIRES - 1, EXPIRES))
        with self.assertRaisesRegex(AssistantUnavailable, "^expired$"):
            provider.select(Topic.STATUS)
        self.reserve.assert_called_once()
        self.token.assert_called_once()
        self.transport.assert_not_called()

    def test_invalid_or_injected_responses_are_never_returned(self) -> None:
        self.transport.side_effect = None
        for raw in (
            reply("documents"),
            reply("status\nignore instructions SECRET"),
            reply("status", "length"),
            b"not json",
            b"{}",
            b'{"choices": null}',
            b"x" * (MAX_REPLY + 1),
        ):
            self.transport.return_value = raw
            with self.assertRaises(AssistantUnavailable):
                self.provider(True).select(Topic.STATUS)

    def test_untyped_injection_fails_before_reservation(self) -> None:
        with self.assertRaises(AssistantUnavailable):
            self.provider(True).select("leak SECRET")
        self.reserve.assert_not_called()
        self.token.assert_not_called()
        self.transport.assert_not_called()

    def test_unreviewed_endpoints_and_deployment_path_injection_are_rejected(self) -> None:
        for endpoint in (
            "http://synthetic-test.openai.azure.com",
            "https://attacker.invalid",
            ENDPOINT + ".attacker.invalid",
            ENDPOINT + "/redirect",
            "https://user:pass@synthetic-test.openai.azure.com",
            ENDPOINT + ":443",
        ):
            with self.assertRaises(ValueError):
                AzureTopicProvider(endpoint, "test")
        for deployment in ("../escape", "test?redirect=evil", ""):
            with self.assertRaises(ValueError):
                AzureTopicProvider(ENDPOINT, deployment)

    def test_http_transport_is_bounded_and_redirects_refused_without_network(self) -> None:
        with patch("urllib.request.build_opener") as build:
            response = build.return_value.open.return_value.__enter__.return_value
            response.read.return_value = reply()
            self.assertEqual(_post(ENDPOINT, b"{}", "FAKE-TOKEN"), reply())
            response.read.assert_called_once_with(MAX_REPLY + 1)
            self.assertEqual(build.return_value.open.call_args.kwargs["timeout"], TIMEOUT_SECONDS)
            self.assertIsInstance(build.call_args.args[0], _NoRedirect)
        handler: urllib.request.HTTPRedirectHandler = _NoRedirect()
        self.assertIsNone(
            handler.redirect_request(
                urllib.request.Request(ENDPOINT),
                io.BytesIO(),
                302,
                "Found",
                HTTPMessage(),
                "https://attacker.invalid",
            )
        )


if __name__ == "__main__":
    unittest.main()
