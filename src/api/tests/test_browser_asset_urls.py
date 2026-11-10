"""Regression coverage for release-independent browser asset instrumentation."""

import unittest
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, patch

from checks import workspace_scripts_browser_check as workspace_check
from checks.asset_urls import asset_url
from checks.chat_widget_browser_check import recovery_case
from checks.workspace_scripts_browser_check import (
    companion_coverage,
    delayed_companion,
    observe_companion,
)
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Route, sync_playwright

BASE = "http://127.0.0.1:12345"


class BrowserAssetUrls(unittest.TestCase):
    def test_bare_query_and_version_directory_paths_match(self) -> None:
        for path in (
            "/app.js",
            "/workspace-shell.js",
            "/async-action.js",
            "/role-screens.js",
            "/case-workspace.js",
            "/chat-widget.js",
            "/chat-widget.css",
            "/vendor/leaflet.js",
        ):
            for prefix in ("", "/v/release-123", "/assets/release-456"):
                for suffix in ("", "?v=release-123", "?lang=en&v=release-123#loaded"):
                    url = prefix + path + suffix
                    with self.subTest(url=url):
                        self.assertIsNotNone(asset_url(path).search(url))
                        self.assertIsNotNone(asset_url(path).search(BASE + url))
                        self.assertIsNotNone(asset_url(path, BASE).search(BASE + url))

    def test_lookalikes_query_spoofing_and_other_origins_do_not_match(self) -> None:
        for url in (
            BASE + "/not-app.js",
            BASE + "/app.js.map",
            BASE + "/app.js/extra",
            BASE + "/other.js?asset=/app.js",
            BASE + "/other.js#/app.js",
            BASE + ".invalid/app.js?v=release",
            "https://example.invalid/app.js?v=release",
        ):
            with self.subTest(url=url):
                self.assertIsNone(asset_url("/app.js", BASE).search(url))
        self.assertIsNone(asset_url("/vendor/leaflet.js").search(BASE + "/leaflet.js?v=123"))
        self.assertIsNone(asset_url("/app.js").search(BASE + "/other.js?next=/app.js"))

    def test_native_routes_waits_dom_observation_and_actual_coverage(self) -> None:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
            except PlaywrightError as error:
                if "Executable doesn't exist" in str(error):
                    self.skipTest("Chromium is installed by the later browser-check step")
                raise
            try:
                for path in (
                    "/role-screens.js",
                    "/role-screens.js?v=release-123",
                    "/assets/release-123/role-screens.js?v=release-123",
                ):
                    with self.subTest(path=path):
                        context = browser.new_context()
                        try:
                            blocked: list[str] = []

                            def local_fixture(
                                route: Route, *, blocked: list[str] = blocked
                            ) -> None:
                                if route.request.url == BASE + "/":
                                    route.fulfill(
                                        content_type="text/html",
                                        body="<!doctype html><head><title>Synthetic</title></head>",
                                    )
                                else:
                                    blocked.append(route.request.url)
                                    route.abort()

                            context.route("**/*", local_fixture)
                            page = context.new_page()
                            session = observe_companion(page, BASE)
                            page.goto(BASE + "/")
                            requests: list[str] = []

                            def companion(route: Route, *, requests: list[str] = requests) -> None:
                                requests.append(route.request.url)
                                route.fulfill(
                                    content_type="text/javascript",
                                    body="function roleScreensView() {}",
                                )

                            matcher = asset_url("/role-screens.js", BASE)
                            page.route(matcher, companion)
                            with page.expect_request(matcher), page.expect_response(matcher):
                                page.evaluate(
                                    """url => {
                                        const script = document.createElement('script');
                                        script.src = url;
                                        document.head.append(script);
                                    }""",
                                    BASE + path,
                                )
                            page.wait_for_function(
                                """pattern => [...document.querySelectorAll('head script[src]')]
                                    .filter(script => new RegExp(pattern).test(script.src))
                                    .length === 1""",
                                arg=matcher.pattern,
                            )
                            page.wait_for_function(
                                "() => window.workspaceScriptEvents.length === 1"
                            )
                            self.assertEqual(
                                page.evaluate("window.workspaceScriptEvents"),
                                [{"outcome": "load", "ready": True}],
                            )
                            page.evaluate("roleScreensView()")
                            self.assertEqual(companion_coverage(session, BASE), (1, 1))
                            self.assertEqual(requests, [BASE + path])
                            page.unroute(asset_url("/role-screens.js", BASE), companion)
                            with page.expect_event("requestfailed") as failed:
                                page.evaluate("url => fetch(url).catch(() => null)", BASE + path)
                            self.assertEqual(failed.value.url, BASE + path)
                            self.assertEqual(blocked, [BASE + path])
                            page.route(matcher, companion)
                            external = "http://example.invalid" + path
                            with page.expect_event("requestfailed") as failed:
                                page.evaluate("url => fetch(url).catch(() => null)", external)
                            self.assertEqual(failed.value.url, external)
                            self.assertEqual(blocked, [BASE + path, external])
                            self.assertEqual(requests, [BASE + path])
                        finally:
                            context.close()
            finally:
                browser.close()

    def test_coverage_filters_versions_and_preserves_original_counts(self) -> None:
        session = Mock()
        for path in (
            "/role-screens.js",
            "/role-screens.js?v=release",
            "/v/release/role-screens.js",
        ):
            script: dict[str, Any] = {
                "url": BASE + path,
                "functions": [
                    {"functionName": "", "ranges": [{"count": 1}]},
                    {"functionName": "roleScreensView", "ranges": [{"count": 2}]},
                ],
            }
            unrelated = dict(script, url="http://example.invalid" + path)
            session.send.return_value = {"result": [unrelated, script]}
            with self.subTest(path=path):
                self.assertEqual(companion_coverage(session, BASE), (1, 2))
            session.send.return_value = {"result": [unrelated]}
            self.assertEqual(companion_coverage(session, BASE), (0, 0))

    def test_coverage_rejects_duplicate_versions_and_missing_original_view(self) -> None:
        session = Mock()
        session.send.return_value = {
            "result": [
                {"url": BASE + "/role-screens.js?v=one"},
                {"url": BASE + "/v/two/role-screens.js"},
            ]
        }
        with self.assertRaisesRegex(AssertionError, "must not be evaluated twice"):
            companion_coverage(session, BASE)
        session.send.return_value = {
            "result": [{"url": BASE + "/role-screens.js?v=one", "functions": []}]
        }
        with self.assertRaisesRegex(AssertionError, "original view entry"):
            companion_coverage(session, BASE)

    def test_chat_recovery_context_registers_local_only_guard(self) -> None:
        browser = Mock()
        context = browser.new_context.return_value
        with patch("checks.chat_widget_browser_check.expect"):
            recovery_case(browser, BASE, 1)
        context.route.assert_called_once()
        pattern, guard = context.route.call_args.args
        self.assertEqual(pattern, "**/*")
        for url, local in (
            (BASE + "/chat-widget.js", True),
            (BASE + "/v/release/chat-widget.js?v=release", True),
            ("http://example.invalid/chat-widget.js?v=release", False),
            (BASE + ".invalid/chat-widget.js?v=release", False),
        ):
            with self.subTest(url=url):
                route = Mock()
                route.request.url = url
                guard(route)
                if local:
                    route.continue_.assert_called_once()
                    route.abort.assert_not_called()
                else:
                    route.abort.assert_called_once()
                    route.continue_.assert_not_called()
        context.close.assert_called_once()


class _AfterCount(Exception):
    """Raised by the page double on the first interaction after the pending-count assertion."""


class _Route:
    def __init__(self) -> None:
        self.request = SimpleNamespace(url=BASE + "/role-screens.js")
        self.calls: list[str] = []

    def abort(self) -> None:
        self.calls.append("abort")

    def continue_(self) -> None:
        self.calls.append("continue")

    def fulfill(self, **_: Any) -> None:
        self.calls.append("fulfill")


class _Page:
    """Page double: the retry route reaches the routine's own callback only where the case says."""

    def __init__(self, deliver_at: int | None, copies: int = 1) -> None:
        self.deliver_at = deliver_at
        self.first = _Route()
        self.retries = [_Route() for _ in range(copies)]
        self.handler: Callable[[Any], None] | None = None
        self.events: list[str] = []
        self.pumps = 0
        self.clock = 0.0
        self.ready = False

    def on(self, *_: Any) -> None:
        return None

    def route(self, _pattern: Any, handler: Callable[[Any], None]) -> None:
        self.handler = self.handler or handler

    def locator(self, *_: Any) -> Mock:
        return self.interact()

    def get_by_role(self, *_: Any, **__: Any) -> Mock:
        return self.interact()

    def evaluate(self, *_: Any) -> Mock:
        return self.interact()

    def interact(self) -> Mock:
        if self.ready:
            raise _AfterCount
        return Mock()

    def wait_for_function(self, *_: Any, **__: Any) -> None:
        assert self.handler is not None
        self.handler(self.first)
        if self.deliver_at == 0:
            self.deliver()
        self.events.append("dom-ready")
        self.ready = True

    def wait_for_timeout(self, milliseconds: float) -> None:
        self.pumps += 1
        self.clock += milliseconds / 1000
        if self.pumps == self.deliver_at:
            self.deliver()

    def deliver(self) -> None:
        assert self.handler is not None
        self.events.append("deliver")
        for route in self.retries:
            self.handler(route)


class DelayedCompanionRouteDelivery(unittest.TestCase):
    variants: tuple[dict[str, bool], ...] = (
        {},
        {"timed_out": True},
        {"sign_out": True},
        {"session_ended": True},
    )

    def drive(self, page: _Page, variant: dict[str, bool]) -> BaseException | None:
        context = Mock()
        context.new_page.return_value = page
        browser = Mock()
        browser.new_context.return_value = context
        outcome: BaseException | None = None
        # create=True lets the original routine, which has no clock, still reach its assertion.
        with (
            patch.object(workspace_check, "expect"),
            patch.object(workspace_check, "sign_in"),
            patch.object(workspace_check, "observe_companion"),
            patch.object(workspace_check, "monotonic", create=True, side_effect=lambda: page.clock),
        ):
            try:
                delayed_companion(browser, BASE, **variant)
            except (AssertionError, _AfterCount) as error:
                outcome = error
        context.close.assert_called_once_with()
        return outcome

    def test_retry_delivered_after_dom_ready_is_awaited(self) -> None:
        for variant in self.variants:
            for deliver_at in (1, 3):
                with self.subTest(variant=variant, deliver_at=deliver_at):
                    page = _Page(deliver_at)
                    self.assertIsInstance(self.drive(page, variant), _AfterCount)
                    self.assertEqual(page.events, ["dom-ready", "deliver"])
                    self.assertEqual(page.pumps, deliver_at)
                    self.assertEqual(page.first.calls, ["abort"])
                    self.assertEqual(page.retries[0].calls, [])

    def test_prompt_delivery_needs_no_pump(self) -> None:
        for variant in self.variants:
            with self.subTest(variant=variant):
                page = _Page(0)
                self.assertIsInstance(self.drive(page, variant), _AfterCount)
                self.assertEqual(page.events, ["deliver", "dom-ready"])
                self.assertEqual(page.pumps, 0)

    def test_zero_delivery_fails_at_the_bounded_deadline(self) -> None:
        for variant in self.variants:
            with self.subTest(variant=variant):
                page = _Page(None)
                outcome = self.drive(page, variant)
                self.assertIsInstance(outcome, AssertionError)
                self.assertRegex(str(outcome), "saw 0")
                self.assertEqual(page.events, ["dom-ready"])
                self.assertAlmostEqual(page.clock, 5.0, delta=0.011)

    def test_double_delivery_fails_instead_of_first_wins(self) -> None:
        for variant in self.variants:
            with self.subTest(variant=variant):
                page = _Page(1, copies=2)
                outcome = self.drive(page, variant)
                self.assertIsInstance(outcome, AssertionError)
                self.assertRegex(str(outcome), "saw 2")
                self.assertEqual(page.retries[0].calls, [])
                self.assertEqual(page.retries[1].calls, [])
