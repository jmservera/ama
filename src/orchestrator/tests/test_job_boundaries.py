"""Deterministic offline job boundaries: synthetic data only, no secret in any output."""

from __future__ import annotations

import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from source_monitor_fixture import DAY, RAW, SOURCE, MonitorFixture

from zava_forward.orchestrator import document_rescan, source_monitor, token_store

PRIVATE = "SYNTHETIC-PRIVATE-SAS-sig=abc123"
VAULT = "https://testvault.vault.azure.net"


class TokenStorePutSecretTests(unittest.TestCase):
    def test_non_200_response_is_rejected_without_echoing_the_secret(self) -> None:
        credential = MagicMock()
        credential.get_token.return_value.token = "fake-token"
        with patch("zava_forward.orchestrator.token_store.urlopen") as open_url:
            open_url.return_value.__enter__.return_value.status = 202
            with self.assertRaises(RuntimeError) as raised:
                token_store.put_secret(  # type: ignore[no-untyped-call]
                    VAULT, credential, PRIVATE, datetime.now(UTC)
                )
        self.assertNotIn(PRIVATE, str(raised.exception))

    def test_request_headers_carry_bearer_only_and_body_is_not_logged(self) -> None:
        credential = MagicMock()
        credential.get_token.return_value.token = "fake-token"
        with patch("zava_forward.orchestrator.token_store.urlopen") as open_url:
            open_url.return_value.__enter__.return_value.status = 200
            token_store.put_secret(  # type: ignore[no-untyped-call]
                VAULT, credential, PRIVATE, datetime(2026, 10, 17, tzinfo=UTC)
            )
        request = open_url.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer fake-token")
        self.assertEqual(open_url.call_args.kwargs["timeout"], 30)


class TokenStoreMainTests(unittest.TestCase):
    ENV = {
        "TOKEN_STORAGE_ACCOUNT": "teststorage",
        "AZURE_CLIENT_ID": "00000000-0000-0000-0000-000000000000",
        "KEY_VAULT_URI": VAULT,
    }

    def run_main(self, renew: Any) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with (
            patch.dict(os.environ, self.ENV),
            patch("azure.identity.ManagedIdentityCredential"),
            patch("azure.storage.blob.BlobServiceClient"),
            patch.object(token_store, "renew", renew),
            contextlib.redirect_stdout(out),
            contextlib.redirect_stderr(err),
        ):
            code = token_store.main()  # type: ignore[no-untyped-call]
        return code, out.getvalue(), err.getvalue()

    def test_success_prints_status_json_without_secret(self) -> None:
        code, out, err = self.run_main(
            MagicMock(return_value={"status": "token-store-renewed", "container": "auth-tokens"})
        )
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out)["status"], "token-store-renewed")

    def test_failures_return_one_with_a_generic_message_only(self) -> None:
        for exc in (
            URLError(PRIVATE),
            OSError(PRIVATE),
            ValueError(PRIVATE),
            RuntimeError(PRIVATE),
        ):
            with self.subTest(exc=type(exc).__name__):
                code, out, err = self.run_main(MagicMock(side_effect=exc))
                self.assertEqual((code, out), (1, ""))
                self.assertIn("token-store-renewal-failed", err)
                self.assertNotIn(PRIVATE, err)

    def test_missing_configuration_fails_closed(self) -> None:
        out, err = io.StringIO(), io.StringIO()
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("azure.identity.ManagedIdentityCredential"),
            contextlib.redirect_stdout(out),
            contextlib.redirect_stderr(err),
        ):
            self.assertEqual(token_store.main(), 1)  # type: ignore[no-untyped-call]
        self.assertEqual(out.getvalue(), "")


class SourceMonitorBoundaryTests(MonitorFixture):
    def test_invalid_observation_shapes_are_rejected(self) -> None:
        bad_shapes: list[Any] = ["text", {"content": b"bytes"}, {"unexpected": 1}]
        for bad in bad_shapes:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                source_monitor.run(self.monitor, {SOURCE: bad}, today=DAY)
        self.assertEqual(self.monitor.changes(), [])

    def test_observation_error_is_reported_as_failure_not_change_content(self) -> None:
        report = source_monitor.run(
            self.monitor,
            {SOURCE: dict(error="Synthetic outage", provenance="Synthetic outage")},
            today=DAY,
        )
        self.assertEqual([f["source_id"] for f in report["failures"]], [SOURCE])

    def run_cli(self, observations: Any, *extra: str) -> tuple[int, str]:
        fixture = Path(self.tmp.name) / "obs.json"
        fixture.write_text(json.dumps(observations), encoding="utf-8")
        env = {
            "ZF_LAW_DB": str(self.path),
            "ZF_LAW_BLOBS": str(self.blobs),
            "ZF_LAW_STORE": "sqlite",
        }
        err = io.StringIO()
        with (
            patch.dict(os.environ, env),
            contextlib.redirect_stderr(err),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                code = source_monitor.main([str(fixture), "--today", DAY, *extra])
            except SystemExit as stop:
                code = int(stop.code or 0)
        return code, err.getvalue()

    def test_cli_success_returns_zero(self) -> None:
        observation = {SOURCE: dict(content=RAW.decode(), provenance="Synthetic fixture")}
        self.assertEqual(self.run_cli(observation)[0], 0)

    def test_cli_rejects_non_object_and_invalid_observations(self) -> None:
        bad_files: list[Any] = [[], {SOURCE: {"unexpected": 1}}]
        for bad in bad_files:
            with self.subTest(bad=bad):
                code, err = self.run_cli(bad)
                self.assertEqual(code, 1)
                self.assertIn("SOURCE_MONITOR_ERROR", err)

    def test_cli_requires_a_configured_law_store(self) -> None:
        err = io.StringIO()
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("zava_forward.core.lawstore.LawStore.from_env", return_value=None),
            contextlib.redirect_stderr(err),
            self.assertRaises(SystemExit) as stop,
        ):
            source_monitor.main(["missing.json", "--today", DAY])
        self.assertEqual(stop.exception.code, 2)

    def test_module_entry_point_exits_through_main(self) -> None:
        with (
            patch.object(sys, "argv", ["x"]),
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit) as stop,
        ):
            runpy.run_module("zava_forward.orchestrator.source_monitor", run_name="__main__")
        self.assertEqual(stop.exception.code, 2)


class DocumentRescanBoundaryTests(unittest.TestCase):
    def run_main(self, argv: list[str], env: dict[str, str]) -> tuple[int, str]:
        err = io.StringIO()
        with (
            patch.dict(os.environ, env, clear=True),
            contextlib.redirect_stderr(err),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                code = document_rescan.main(argv)
            except SystemExit as stop:
                code = int(stop.code or 0)
        return code, err.getvalue()

    def test_unsafe_or_incomplete_configuration_is_refused_before_opening_a_store(self) -> None:
        base = {"ZF_DATA": "/tmp/synthetic.db", "ZF_STORE": "sqlite", "ZF_SCANNER": "local"}
        cases = [
            ([], {}),
            (["--synthetic-local"], {**base, "ZF_STORE": "json"}),
            (["--synthetic-local"], {**base, "ZF_SCANNER": "other"}),
            ([], base),
            (["--synthetic-local", "--limit", "0"], base),
            (["--synthetic-local", "--limit", "101"], base),
            (["--synthetic-local", "--after", "case", " "], base),
        ]
        with patch.object(document_rescan, "open_store") as opened:
            for argv, env in cases:
                with self.subTest(argv=argv, env=env):
                    self.assertEqual(self.run_main(argv, env)[0], 2)
            opened.assert_not_called()

    def test_result_exit_codes_and_store_is_always_closed(self) -> None:
        env = {"ZF_DATA": "/tmp/synthetic.db", "ZF_STORE": "sqlite", "ZF_SCANNER": "local"}
        cases: list[tuple[dict[str, Any], int]] = [
            ({"failed": 0, "committed": 0, "pending": 0, "next_after": None}, 0),
            ({"failed": 1, "committed": 0, "pending": 0, "next_after": None}, 1),
            ({"failed": 0, "committed": 1, "pending": 0, "next_after": None}, 1),
            ({"failed": 0, "committed": 0, "pending": 1, "next_after": None}, 2),
            ({"failed": 0, "committed": 0, "pending": 0, "next_after": ["c", "d"]}, 2),
        ]
        for result, expected in cases:
            store = MagicMock()
            store.scanner.name = "synthetic-local"
            with (
                self.subTest(result=result),
                patch.object(document_rescan, "open_store", return_value=store),
                patch.object(document_rescan, "run", return_value=dict(result)),
            ):
                code, _ = self.run_main(["--synthetic-local", "--after", "c1", "d1"], env)
            self.assertEqual(code, expected)
            store.db.close.assert_called_once_with()

    def test_failure_prints_a_generic_message_without_exception_detail(self) -> None:
        env = {"ZF_DATA": "/tmp/synthetic.db", "ZF_STORE": "sqlite", "ZF_SCANNER": "local"}
        store = MagicMock()
        with (
            patch.object(document_rescan, "open_store", return_value=store),
            patch.object(document_rescan, "run", side_effect=OSError(PRIVATE)),
        ):
            code, err = self.run_main(["--synthetic-local"], env)
        self.assertEqual(code, 1)
        self.assertIn("DOCUMENT_RESCAN_ERROR", err)
        self.assertNotIn(PRIVATE, err)
        store.db.close.assert_called_once_with()

    def test_open_failure_has_no_store_to_close(self) -> None:
        env = {"ZF_DATA": "/tmp/synthetic.db", "ZF_STORE": "sqlite", "ZF_SCANNER": "local"}
        with patch.object(document_rescan, "open_store", side_effect=ValueError(PRIVATE)):
            code, err = self.run_main(["--synthetic-local"], env)
        self.assertEqual(code, 1)
        self.assertNotIn(PRIVATE, err)

    def test_module_entry_point_exits_through_main(self) -> None:
        with (
            patch.object(sys, "argv", ["x"]),
            patch.dict(os.environ, {}, clear=True),
            contextlib.redirect_stderr(io.StringIO()),
            tempfile.TemporaryDirectory(),
            self.assertRaises(SystemExit) as stop,
        ):
            runpy.run_module("zava_forward.orchestrator.document_rescan", run_name="__main__")
        self.assertEqual(stop.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
