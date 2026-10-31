"""Maintained employee admission caller contracts, using public synthetic data only."""

from __future__ import annotations

import os
import unittest
from contextlib import ExitStack
from typing import Any
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlsplit

from checks import employee_acceptance_check as check
from checks.employee_identity_check import BINDING
from playwright.sync_api import Error as BrowserError
from playwright.sync_api import Page, Request, Route, sync_playwright

import test_employee_identity_check as identity_fixture
from test_auth import OID_NEW, OID_SAM, TENANT, principal

EXPECTED = {"tid": TENANT, "oid": OID_NEW, "email": "expected@example.test"}
GOOD = {
    key: key not in {"displayEmailMatches", "rosterBound", "transportFailed", "jsonFailed"}
    for key in check.FLAGS
}
POINT = {
    "id": "SYNTH-MAP",
    "name": "Synthetic home",
    "lat": 54.9,
    "lon": -1.6,
    "kind": "hazard",
}
CLUSTER = {"lat": 54.9, "lon": -1.6, "count": 3, "hazards": 1, "long": 2}
POINTS = {
    "mode": "points",
    "total": 1,
    "shown": 1,
    "bounds": [54.9, -1.6, 54.9, -1.6],
    "items": [POINT],
}
CLUSTERS = {
    "mode": "clusters",
    "total": 3,
    "shown": 1,
    "bounds": [54.9, -1.6, 54.9, -1.6],
    "items": [CLUSTER],
}
EMPTY = {"mode": "points", "total": 0, "shown": 0, "bounds": None, "items": []}


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

    def test_navigation_admission(self) -> None:
        def run_boundary(stage: str, boundary: str, failure: str) -> None:
            page = self.page()
            options = page.locator.return_value.locator.return_value.locator.return_value
            options.count.return_value = 2
            options.nth.return_value.get_attribute.return_value = "synthetic-skill"
            lost = False

            def change() -> None:
                nonlocal lost
                lost = True
                if failure == "origin":
                    page.url = "https://unapproved.example.test/"

            def evaluate(script: str, *args: object) -> dict[str, bool]:
                if script.startswith("location.hash"):
                    if boundary == "hash":
                        change()
                    return {}
                if stage == "chat" and script == BINDING:
                    if page.wait_for_function.called:
                        change()
                return dict(GOOD, authenticated=not lost, expectedIdentity=not lost)

            page.evaluate.side_effect = evaluate
            link = page.locator.return_value.first
            link.click.side_effect = change
            observer = check.OBSERVERS[stage]
            later = Mock(return_value={"passed": True})
            with patch.dict(check.OBSERVERS, {stage: observer, "later": later}, clear=True):
                result = check.verify_employee(page, EXPECTED)
            self.assertFalse(result["passed"])
            self.assertEqual(result["stages"][stage]["status"], "blocked")
            if stage == "map":
                page.get_by_role.assert_not_called()
            elif stage == "case" and boundary == "hash":
                page.locator.assert_not_called()
            elif stage == "case":
                page.locator.assert_called_once()
            elif stage == "chat":
                page.locator.return_value.locator.return_value.fill.assert_not_called()
                page.locator.return_value.get_by_role.assert_not_called()
            self.assertNotIn("unapproved", str(result))
            self.assertEqual(result["stages"]["later"]["status"], "blocked")
            later.assert_not_called()

        for stage in ("map", "case", "chat"):
            for boundary in ("hash", "link") if stage == "case" else ("hash",):
                for failure in ("origin", "identity"):
                    with self.subTest(stage=stage, boundary=boundary, failure=failure):
                        run_boundary(stage, boundary, failure)
        page = self.page()
        first = Mock(side_effect=check.AdmissionLost("PRIVATE_CANARY"))
        later = Mock(return_value={"passed": True})
        with patch.dict(check.OBSERVERS, chat=first, map=later, case=later):
            result = check.verify_employee(page, EXPECTED)
        self.assertEqual(result["stages"]["chat"]["status"], "blocked")
        later.assert_not_called()
        self.assertNotIn("PRIVATE_CANARY", str(result))

    def test_map_payload(self) -> None:
        for payload in (POINTS, CLUSTERS, EMPTY):
            self.assertIsNotNone(check.map_projection(payload))
        invalid = [
            None,
            {"total": 1},
            dict(POINTS, items=None),
            dict(POINTS, total=True),
            dict(POINTS, shown=2),
            dict(POINTS, bounds=[54.9, -1.6, 54.8, -1.6]),
            dict(POINTS, bounds=[54.9, -1.6]),
            dict(POINTS, bounds=None),
            dict(EMPTY, bounds=[0, 0, 0, 0]),
            dict(CLUSTERS, total=4),
            dict(CLUSTERS, items=[dict(CLUSTER, hazards=4)]),
            dict(CLUSTERS, items=[dict(CLUSTER, count=True)]),
            dict(POINTS, items=[dict(POINT, kind="unknown")]),
            dict(POINTS, items=[dict(POINT, lat=float("nan"))]),
            dict(POINTS, items=[dict(POINT, lon=181)]),
        ]
        for index, invalid_payload in enumerate(invalid):
            with self.subTest(index=index):
                self.assertIsNone(check.map_projection(invalid_payload))

    def chromium(self, oid: str, admitted: bool, map_contract: bool = False) -> None:
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
                    if map_contract:
                        replacement = dict(
                            POINTS, items=[dict(POINT, name="Synthetic replacement")]
                        )
                        cases = [
                            ("points", POINTS, POINTS, True, False),
                            ("clusters", CLUSTERS, CLUSTERS, True, False),
                            ("empty", EMPTY, EMPTY, True, False),
                            ("missing-items", {"total": 1}, {"total": 1}, False, False),
                            (
                                "unknown-kind",
                                dict(POINTS, items=[dict(POINT, kind="unknown")]),
                                POINTS,
                                False,
                                False,
                            ),
                            (
                                "coordinates",
                                dict(POINTS, items=[dict(POINT, lat=91)]),
                                POINTS,
                                False,
                                False,
                            ),
                            ("bounds", dict(POINTS, bounds=[54.9]), POINTS, False, False),
                            ("counts", dict(CLUSTERS, total=4), CLUSTERS, False, False),
                            ("followup-valid", POINTS, replacement, True, False),
                            ("followup-malformed", POINTS, {"total": 1}, False, False),
                            ("followup-http-failure", POINTS, None, False, False),
                            ("mismatched-render", POINTS, POINTS, False, False),
                            ("pre-activation-stale", POINTS, replacement, True, True),
                        ]
                        for label, initial, final, passed, stale in cases:
                            with self.subTest(contract=label):
                                page.goto(fixture.url)
                                page.goto(base + "/app#/overview")
                                page.locator(".overview-map-filters").wait_for()
                                held: list[Route] = []
                                calls = 0

                                def map_response(
                                    route: Route,
                                    request: Request,
                                    stale: bool = stale,
                                    held: list[Route] = held,
                                    initial: object = initial,
                                    final: object = final,
                                    label: str = label,
                                ) -> None:
                                    nonlocal calls
                                    query = parse_qs(urlsplit(route.request.url).query)
                                    if query.get("flag") != ["hazard"]:
                                        if stale:
                                            held.append(route)
                                        else:
                                            route.continue_()
                                        return
                                    for pending in held:
                                        pending.fulfill(json={"total": 999})
                                    held.clear()
                                    payload = initial if calls == 0 else final
                                    calls += 1
                                    if label == "mismatched-render":
                                        page.evaluate(
                                            """() => {
                                              const observer = new MutationObserver(() => {
                                                const list = document.querySelector('.maplist ul');
                                                if (list?.firstChild) list.replaceChildren();
                                              });
                                              observer.observe(document.body,
                                                {subtree: true, childList: true});
                                            }"""
                                        )
                                    route.fulfill(
                                        status=200 if payload is not None else 500,
                                        json=payload
                                        if payload is not None
                                        else {"error": "synthetic"},
                                    )

                                page.route("**/api/map?*", map_response)
                                try:
                                    # Hold the old draw until the new selection is active.
                                    if stale:
                                        page.evaluate("location.hash = '#/all'")
                                        page.locator('a.item[href^="#/case/"]').first.wait_for()
                                    with (
                                        patch.dict(
                                            check.OBSERVERS, {"map": check.map_filters}, clear=True
                                        ),
                                        patch.object(check, "MAP_TIMEOUT", 2000),
                                        patch.object(page, "on", wraps=page.on) as on,
                                        patch.object(
                                            page, "remove_listener", wraps=page.remove_listener
                                        ) as remove,
                                    ):
                                        result = check.verify_employee(page, EXPECTED, base)
                                    self.assertEqual(result["passed"], passed)
                                    self.assertEqual(
                                        result["stages"]["map"]["status"],
                                        "passed" if passed else "failed",
                                    )
                                    self.assertGreater(calls, 0)
                                    if label.startswith("followup"):
                                        self.assertGreaterEqual(calls, 2)
                                    self.assertEqual(on.call_args_list, remove.call_args_list)
                                finally:
                                    page.unroute("**/api/map?*", map_response)
                                    for pending in held:
                                        pending.abort()
        finally:
            fixture.tearDown()

    def test_chromium_rosterless(self) -> None:
        self.chromium(OID_NEW, True)

    def test_chromium_wrong_account(self) -> None:
        self.chromium(OID_SAM, False)

    def test_chromium_map_contract(self) -> None:
        self.chromium(OID_NEW, True, map_contract=True)


if __name__ == "__main__":
    unittest.main()
