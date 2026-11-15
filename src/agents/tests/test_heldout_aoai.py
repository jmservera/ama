"""Azure OpenAI adapter for the held-out runner: mocked HTTP only, no network (#435)."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import traceback
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest import mock

from heldout_freeze_fixture import manifest
from test_heldout_batch import auth, proposals
from zava_forward.agents import heldout_aoai as aoai
from zava_forward.agents import heldout_batch as hb

ENDPOINT = "https://aif-cutover-test-rzsrg.openai.azure.com/"
SECRET = "tok-SECRET-123"


def body(**over: Any) -> dict[str, Any]:
    data: dict[str, Any] = dict(
        model="m-1-2025-04-14",
        usage=dict(
            prompt_tokens=100,
            completion_tokens=20,
            total_tokens=120,
            prompt_tokens_details=dict(cached_tokens=10),
        ),
    )
    data.update(over)
    return data


class Response:
    def __init__(self, raw: bytes) -> None:
        self.raw = raw

    def __enter__(self) -> Response:
        return self

    def __exit__(self, *exc: Any) -> None:
        return None

    def read(self, n: int) -> bytes:
        return self.raw[:n]


class Opener:
    def __init__(self, raw: bytes | Exception) -> None:
        self.raw = raw
        self.requests: list[tuple[Any, int]] = []

    def __call__(self, request: Any, timeout: int) -> Response:
        self.requests.append((request, timeout))
        if isinstance(self.raw, Exception):
            raise self.raw
        return Response(self.raw)


def provider(opener: Any) -> Any:
    return aoai.make_provider(ENDPOINT, "standard", "m-1", SECRET, opener)


class TokenTests(unittest.TestCase):
    def test_az_cli_token_uses_argument_list_without_shell(self) -> None:
        run = mock.Mock(return_value=SimpleNamespace(returncode=0, stdout=f" {SECRET}\n"))
        self.assertEqual(aoai.az_cli_token(run), SECRET)
        argv = run.call_args.args[0]
        self.assertEqual(argv[:3], ["az", "account", "get-access-token"])
        self.assertNotIn("shell", run.call_args.kwargs)

    def test_az_cli_failures_are_fixed_and_unchained(self) -> None:
        bad = [
            mock.Mock(return_value=SimpleNamespace(returncode=1, stdout=SECRET)),
            mock.Mock(return_value=SimpleNamespace(returncode=0, stdout="  ")),
            mock.Mock(side_effect=OSError(SECRET)),
            mock.Mock(side_effect=subprocess.TimeoutExpired(["az", SECRET], 1)),
        ]
        for run in bad:
            with self.assertRaises(aoai.AdapterError) as caught:
                aoai.az_cli_token(run)
            text = "".join(traceback.format_exception(caught.exception))
            self.assertNotIn(SECRET, text)

    def test_managed_identity(self) -> None:
        credential = mock.Mock()
        credential.return_value.get_token.return_value = SimpleNamespace(token=SECRET)
        self.assertEqual(aoai.managed_identity_token(credential), SECRET)
        credential.return_value.get_token.assert_called_once_with(
            "https://cognitiveservices.azure.com/.default"
        )
        failing = mock.Mock(side_effect=RuntimeError(SECRET))
        with self.assertRaises(aoai.AdapterError) as caught:
            aoai.managed_identity_token(failing)
        self.assertNotIn(SECRET, "".join(traceback.format_exception(caught.exception)))

    def test_managed_identity_default_credential_is_lazy(self) -> None:
        with mock.patch.dict("sys.modules", {"azure.identity": None, "azure": None}):
            with self.assertRaises(aoai.AdapterError):
                aoai.managed_identity_token()

    def test_get_token_selects_source(self) -> None:
        with (
            mock.patch.object(aoai, "az_cli_token", return_value="a") as az,
            mock.patch.object(aoai, "managed_identity_token", return_value="m") as mi,
        ):
            self.assertEqual(aoai.get_token("az-cli"), "a")
            self.assertEqual(aoai.get_token("managed-identity"), "m")
            az.assert_called_once()
            mi.assert_called_once()


class ProviderTests(unittest.TestCase):
    def test_request_shape_and_envelope(self) -> None:
        opener = Opener(json.dumps(body()).encode())
        envelope = provider(opener)("sys", "hello", 300, 45)
        request, timeout = opener.requests[0]
        self.assertEqual(timeout, 45)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(
            request.full_url,
            ENDPOINT.rstrip("/")
            + "/openai/deployments/standard/chat/completions?api-version=2024-10-21",
        )
        self.assertEqual(request.get_header("Authorization"), f"Bearer {SECRET}")
        sent = json.loads(request.data)
        self.assertEqual(sent["max_tokens"], 300)
        self.assertEqual(sent["temperature"], 0)
        self.assertEqual([m["role"] for m in sent["messages"]], ["system", "user"])
        self.assertEqual(
            envelope,
            dict(
                outcome="returned",
                text=None,
                usage=dict(
                    prompt_tokens=100, completion_tokens=20, total_tokens=120, cached_tokens=10
                ),
            ),
        )
        self.assertNotIn(SECRET, json.dumps(envelope))

    def test_empty_system_is_omitted(self) -> None:
        opener = Opener(json.dumps(body()).encode())
        provider(opener)("", "hello", 10, 5)
        self.assertEqual(len(json.loads(opener.requests[0][0].data)["messages"]), 1)

    def test_every_failure_is_an_unmeasured_envelope(self) -> None:
        usage = body()["usage"]
        no_cached = dict(usage, prompt_tokens_details={})
        cases: list[bytes | Exception] = [
            json.dumps(body(model="other")).encode(),
            json.dumps(body(model="m-10")).encode(),
            json.dumps(body(model="m-1-pro")).encode(),
            json.dumps(body(model=None)).encode(),
            json.dumps(body(usage=None)).encode(),
            json.dumps(body(usage=no_cached)).encode(),
            json.dumps(
                body(usage=dict(usage, prompt_tokens_details=dict(cached_tokens=True)))
            ).encode(),
            json.dumps([1]).encode(),
            b"not json",
            b"x" * (aoai.MAX_RESPONSE_BYTES + 1),
            OSError(SECRET),
            TimeoutError(),
        ]
        for raw in cases:
            self.assertEqual(provider(Opener(raw))("", "p", 10, 5), dict(outcome="failed"))

    def test_unsafe_targets_are_rejected(self) -> None:
        for endpoint, deployment in (
            ("http://x1.openai.azure.com", "standard"),
            ("https://evil.example.com", "standard"),
            ("https://x1.openai.azure.com.evil.com", "standard"),
            ("https://x1.openai.azure.com/path", "standard"),
            (ENDPOINT, "a/b"),
            (ENDPOINT, ""),
            (ENDPOINT.rstrip("/") + "\n", "standard"),
            (ENDPOINT, "standard\n"),
        ):
            with self.assertRaises(ValueError):
                aoai.make_provider(endpoint, deployment, "m-1", SECRET)

    def test_default_opener_refuses_redirects(self) -> None:
        handler = aoai._NoRedirect()
        redirect: Any = handler.redirect_request
        self.assertIsNone(redirect(None, None, 302, "", {}, "https://x"))


class CliTests(unittest.TestCase):
    def files(self, tmp: str, **over: Any) -> list[str]:
        root = Path(tmp)
        bound = dict(endpoint=ENDPOINT.rstrip("/"), deployment="standard")
        (root / "a.json").write_text(
            json.dumps(auth(expires_utc="2099-01-01T00:00:00+00:00", **{**bound, **over}))
        )
        (root / "m.json").write_text(json.dumps(manifest()))
        (root / "p.json").write_text(json.dumps(proposals(2)))
        return [
            "--authorization", str(root / "a.json"),
            "--manifest", str(root / "m.json"),
            "--proposals", str(root / "p.json"),
        ]  # fmt: skip

    def call(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = hb.main(argv)
        return code, out.getvalue(), err.getvalue()

    live = ["--execute-live", "--endpoint", ENDPOINT, "--deployment", "standard", "--model", "m-1"]

    def test_live_needs_every_target_option(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(aoai, "get_token") as token:
            files = self.files(tmp)
            for argv in (
                ["--execute-live"],
                ["--execute-live", "--endpoint", ENDPOINT, "--deployment", "standard"],
                ["--execute-live", "--endpoint", "http://x.openai.azure.com", "--deployment", "s",
                 "--model", "m-1"],
            ):  # fmt: skip
                code, _, err = self.call([*files, *argv])
                self.assertEqual(code, hb.NOT_CONFIGURED)
                self.assertIn("no live call was made", err)
            token.assert_not_called()

    def test_over_cap_authorization_refuses_before_token_or_http(self) -> None:
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(aoai, "get_token") as token,
            mock.patch("urllib.request.OpenerDirector.open") as http,
        ):
            code, out, _ = self.call([*self.files(tmp, max_budget_usd="5.01"), *self.live])
            self.assertEqual(code, 1)
            self.assertIn("refused", out)
            token.assert_not_called()
            http.assert_not_called()

    def test_endpoint_and_deployment_must_match_authorization(self) -> None:
        for over in (
            dict(endpoint="https://other-res.openai.azure.com"),
            dict(deployment="premium"),
            dict(endpoint=None),
        ):
            with (
                tempfile.TemporaryDirectory() as tmp,
                mock.patch.object(aoai, "get_token") as token,
            ):
                code, _, err = self.call([*self.files(tmp, **over), *self.live])
                self.assertEqual(code, hb.NOT_CONFIGURED)
                self.assertIn("must equal the authorization", err)
                token.assert_not_called()

    def test_token_failure_exits_before_any_call(self) -> None:
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(aoai, "get_token", side_effect=aoai.AdapterError("unavailable")),
            mock.patch("urllib.request.OpenerDirector.open") as http,
        ):
            code, _, err = self.call([*self.files(tmp), *self.live])
            self.assertEqual(code, hb.NOT_CONFIGURED)
            self.assertIn("no live call was made", err)
            http.assert_not_called()

    def test_live_batch_through_mocked_http_labels_measured_and_hides_token(self) -> None:
        opener = Opener(json.dumps(body()).encode())
        real = aoai.make_provider
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(aoai, "get_token", return_value=SECRET) as token,
            mock.patch.object(
                aoai,
                "make_provider",
                side_effect=lambda e, d, m, t: real(e, d, m, t, opener),
            ),
        ):
            code, out, err = self.call([*self.files(tmp), *self.live, "--auth", "managed-identity"])
        self.assertEqual(code, 0)
        token.assert_called_once_with("managed-identity")
        report = json.loads(out)
        self.assertEqual(report["evidence_label"], "measured held-out batch")
        self.assertEqual(report["calls"], 2)
        self.assertEqual(len(opener.requests), 2)
        self.assertNotIn(SECRET, out + err)

    def test_wrong_provider_model_refuses_live(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(aoai, "get_token") as token:
            argv = [*self.files(tmp), *self.live[:-1], "other"]
            code, out, _ = self.call(argv)
        self.assertEqual(code, 1)
        self.assertIn("provider model", out)
        token.assert_not_called()


if __name__ == "__main__":
    unittest.main()
