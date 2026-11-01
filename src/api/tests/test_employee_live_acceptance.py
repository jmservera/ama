"""Offline contract for the credential-free live acceptance entry point."""

from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from checks import employee_live_acceptance as live
from checks.employee_acceptance_check import APP

TID = "11111111-1111-4111-8111-111111111111"
OID = "22222222-2222-4222-8222-222222222222"
ENV = {"ZF_EXPECTED_TID": TID, "ZF_EXPECTED_OID": OID}


class FakePlaywright:
    def __init__(self, pages: list[object]) -> None:
        browser = SimpleNamespace(contexts=[SimpleNamespace(pages=pages)], close=lambda: None)
        self.chromium = SimpleNamespace(connect_over_cdp=lambda url: browser)

    def __enter__(self) -> FakePlaywright:
        return self

    def __exit__(self, *args: object) -> None:
        return None


def run(argv: list[str], env: dict[str, str], pages: list[object], passed: bool = True):
    out = io.StringIO()
    with (
        patch.object(live, "sync_playwright", lambda: FakePlaywright(pages)),
        patch.object(live, "allowed_page", lambda page, origin: True),
        patch.object(live, "verify_employee", lambda page, expected, origin: {"passed": passed}),
        redirect_stdout(out),
    ):
        code = live.main(argv, env)
    return code, json.loads(out.getvalue())


class LiveAcceptanceTests(unittest.TestCase):
    def test_refuses_bad_expectation_and_remote_cdp(self) -> None:
        self.assertEqual(run([], {"ZF_EXPECTED_TID": "x"}, [object()])[0], 2)
        for url in ("http://example.test:9222", "http://u:p@127.0.0.1:9222", "http://127.0.0.1"):
            self.assertEqual(run(["--cdp-url", url], ENV, [object()])[0], 2)

    def test_no_matching_page(self) -> None:
        code, body = run([], ENV, [])
        self.assertEqual((code, body["status"]), (2, "no-page"))

    def test_exit_code_follows_passed_and_output_has_no_identity(self) -> None:
        code, body = run(["--origin", APP], ENV, [object()], passed=True)
        self.assertEqual((code, body["passed"]), (0, True))
        code, body = run([], ENV, [object()], passed=False)
        self.assertEqual((code, body["passed"]), (1, False))
        self.assertNotIn(TID, json.dumps(body))


if __name__ == "__main__":
    unittest.main()
