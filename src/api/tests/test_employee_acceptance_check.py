"""Maintained employee admission caller contracts, using public synthetic data only."""

from __future__ import annotations

import os
import unittest
from contextlib import ExitStack
from typing import Any
from unittest.mock import Mock, patch

from checks import employee_acceptance_check as check
from playwright.sync_api import Error as BrowserError
from playwright.sync_api import Page, sync_playwright

import test_employee_identity_check as identity_fixture
from test_auth import OID_NEW, OID_SAM, TENANT, principal

EXPECTED = {"tid": TENANT, "oid": OID_NEW, "email": "expected@example.test"}
GOOD = {
    key: key not in {"displayEmailMatches", "rosterBound", "transportFailed", "jsonFailed"}
    for key in check.FLAGS
}


class AcceptanceTests(unittest.TestCase):
    def page(self) -> Mock:
        page = Mock(spec=Page)
        page.url = check.APP + "/app"
        page.evaluate.return_value = dict(GOOD)
        return page

    def test_expectations(self) -> None:
        for expected in ({}, {"tid": TENANT, "oid": "bad"}, dict(EXPECTED, oid=OID_NEW + "\n")):
            with self.subTest(expected=expected):
                page = self.page()
                self.assertFalse(check.verify_employee(page, expected)["passed"])
                page.evaluate.assert_not_called()

    def test_projection(self) -> None:
        for projection in (
            None,
            {"authenticated": True},
            dict(GOOD, authenticated="true"),
            dict(GOOD, expectedIdentity=False),
            dict(GOOD, schemaValid=False),
            dict(GOOD, transportFailed=True),
            dict(GOOD, displayEmailMatches=True, expectedIdentity=False),
            dict(GOOD, PRIVATE_CANARY=True),
        ):
            with self.subTest(projection=projection):
                page = self.page()
                page.evaluate.return_value = projection
                self.assertFalse(check.verify_employee(page, EXPECTED)["passed"])
                self.assertNotIn("PRIVATE_CANARY", str(check.probe(page, EXPECTED)))

    def test_origin_and_debug(self) -> None:
        for url in (
            "https://login.microsoftonline.com/",
            check.APP + ".evil.test/app",
            check.APP.replace("https:", "http:") + "/app",
            check.APP.replace("https://", "https://user@") + "/app",
        ):
            page = self.page()
            page.url = url
            self.assertFalse(check.verify_employee(page, EXPECTED)["passed"])
            page.evaluate.assert_not_called()
        for variable in ("DEBUG", "PWDEBUG", "PLAYWRIGHT_DEBUG", "DEBUG_FILE"):
            with patch.dict(os.environ, {variable: "1"}):
                page = self.page()
                self.assertFalse(check.verify_employee(page, EXPECTED)["passed"])
                page.evaluate.assert_not_called()
        page = self.page()

        def redirect(*args: object) -> dict[str, bool]:
            page.url = "https://login.microsoftonline.com/"
            return dict(GOOD)

        page.evaluate.side_effect = redirect
        self.assertFalse(check.verify_employee(page, EXPECTED)["passed"])

    def test_downstream_and_session_loss(self) -> None:
        for failure in (
            {"passed": False},
            {"passed": "yes"},
            {"passed": True, "PRIVATE_CANARY": True},
            BrowserError("PRIVATE_CANARY"),
        ):
            with self.subTest(failure=str(type(failure))):
                page = self.page()
                observer = Mock(
                    side_effect=failure if isinstance(failure, BrowserError) else None,
                    return_value=failure,
                )
                later = Mock(return_value={"passed": True})
                with patch.dict(check.OBSERVERS, chat=observer, map=later, case=later):
                    result = check.verify_employee(page, EXPECTED)
                self.assertFalse(result["passed"])
                self.assertEqual(result["stages"]["chat"]["status"], "failed")
                self.assertNotIn("PRIVATE_CANARY", str(result))
                later.assert_not_called()
        for responses in (
            [dict(GOOD, expectedIdentity=False, authenticated=False)],
            [dict(GOOD), dict(GOOD, expectedIdentity=False, authenticated=False)],
            [dict(GOOD), dict(GOOD), dict(GOOD, expectedIdentity=False, authenticated=False)],
        ):
            page = self.page()
            page.evaluate.side_effect = responses
            observer = Mock(return_value={"passed": True})
            with patch.dict(check.OBSERVERS, chat=observer, map=observer, case=observer):
                result = check.verify_employee(page, EXPECTED)
            self.assertFalse(result["passed"])
            self.assertEqual(observer.call_count, 1 if len(responses) == 3 else 0)

    def chromium(self, oid: str, admitted: bool) -> None:
        privacy = patch.dict(
            os.environ,
            {
                "CHAT_DPIA_REF": "SYNTH-BROWSER-DPIA",
                "CHAT_LAWFUL_BASIS_REF": "SYNTH-BROWSER-BASIS",
                "CHAT_NOTICE_REF": "SYNTH-BROWSER-NOTICE",
            },
        )
        privacy.start()
        self.addCleanup(privacy.stop)
        fixture = identity_fixture.EmployeeIdentityTests(
            methodName="test_correct_rosterless_account_needs_no_display_email"
        )
        fixture.setUp()
        try:
            for case in fixture.store.data["cases"]:
                case["home"].update(lat=54.9, lon=-1.6)
            payload = fixture.payload(
                oid=oid, emails=("expected@example.test",) if not admitted else ()
            )
            self.assertEqual(payload["user"]["oid"], oid)
            with sync_playwright() as driver, ExitStack() as cleanup:
                browser = driver.chromium.launch()
                cleanup.callback(browser.close)
                make_principal: Any = principal
                context = browser.new_context(
                    extra_http_headers={
                        "X-MS-CLIENT-PRINCIPAL": make_principal(
                            roles=("ZavaForward.ProgrammeManager",),
                            oid=oid,
                            email=None if admitted else EXPECTED["email"],
                        )
                    }
                )
                cleanup.callback(context.close)
                base = fixture.url.removesuffix("/api/me")
                context.route(
                    "**/*",
                    lambda route: (
                        route.continue_()
                        if route.request.url.startswith(base + "/")
                        else route.abort()
                    ),
                )
                page = context.new_page()
                page.goto(fixture.url)
                observer = Mock(return_value={"passed": True})
                with patch.dict(check.OBSERVERS, chat=observer, map=observer, case=observer):
                    result = check.verify_employee(page, EXPECTED, base)
                self.assertEqual(result["passed"], admitted)
                self.assertEqual(result["identity"]["expectedIdentity"], admitted)
                self.assertEqual(result["identity"]["displayEmailMatches"], not admitted)
                self.assertEqual(observer.call_count, 3 if admitted else 0)
                if admitted:
                    self.assertFalse(result["identity"]["rosterBound"])
                    page.goto(base + "/app")
                    actual = check.verify_employee(page, EXPECTED, base)
                    self.assertTrue(actual["passed"], actual)
                    self.assertTrue(actual["stages"]["chat"]["observations"]["workflowOnly"])
                    self.assertFalse(actual["stages"]["chat"]["observations"]["actualAiLabel"])
        finally:
            fixture.tearDown()

    def test_chromium_rosterless(self) -> None:
        self.chromium(OID_NEW, True)

    def test_chromium_wrong_account(self) -> None:
        self.chromium(OID_SAM, False)


if __name__ == "__main__":
    unittest.main()
