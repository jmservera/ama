"""Check bounded workspace recovery against an owned synthetic loopback API."""

from __future__ import annotations

from urllib.parse import urlsplit

from playwright.sync_api import Browser, BrowserContext, Page, Route, expect, sync_playwright

from checks.design_system_browser_check import main
from checks.workbench_browser_check import synthetic_data

LEAFLET = "/vendor/leaflet.js"


def local_context(browser: Browser, base: str) -> BrowserContext:
    context = browser.new_context()

    def local_only(route: Route) -> None:
        if urlsplit(route.request.url).netloc == urlsplit(base).netloc:
            route.continue_()
        else:
            route.abort()

    context.route("**/*", local_only)
    return context


def sign_in(page: Page, base: str, hash_: str) -> None:
    page.goto(base + "/app" + hash_)
    page.get_by_label("Work email", exact=True).fill("sam@example.test")
    page.get_by_label("Password", exact=True).fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()


def error_message(path: str) -> str:
    return (
        f"Required workspace files did not load: {path}. Reload this page to try again. "
        "If this continues, ask application support to check these files."
    )


def expect_failure(page: Page, path: str) -> None:
    expect(page.get_by_role("heading", name="Workspace unavailable", exact=True)).to_be_visible()
    expect(page.get_by_role("alert")).to_have_text(error_message(path))
    expect(page.locator("#workspace-status")).to_have_text(
        "Workspace unavailable: " + error_message(path)
    )
    expect(page.locator("#workspace-status")).to_have_attribute("role", "status")
    expect(page.locator("#workspace-status")).to_have_attribute("aria-live", "polite")
    expect(page.get_by_role("button", name="Reload workspace", exact=True)).to_be_visible()


def recovery(browser: Browser, base: str, path: str, failures: int, hash_: str) -> None:
    context = local_context(browser, base)
    try:
        page = context.new_page()
        errors: list[str] = []
        requests: list[str] = []
        documents: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "request",
            lambda request: documents.append(request.url)
            if request.resource_type == "document" else None,
        )

        def intercept(route: Route) -> None:
            requests.append(route.request.url)
            if len(requests) <= failures:
                if len(requests) == 1:
                    route.abort()
                else:
                    route.fulfill(status=503, content_type="text/plain", body="Synthetic failure")
            else:
                route.continue_()

        page.route("**" + path, intercept)
        sign_in(page, base, hash_)
        if path == LEAFLET:
            expect(page.locator(".leaflet-container")).to_be_visible()
        else:
            expect(
                page.get_by_role("heading", name="Specialist screens", exact=True)
            ).to_be_visible()
        assert len(requests) == failures + 1
        assert len(documents) == 1, documents
        assert not errors, errors
        expect(page.get_by_role("heading", name="Workspace unavailable")).to_have_count(0)
        expect(page.locator("#workspace-status")).not_to_contain_text("Loading workspace files")
        print(f"PASS {path}: {failures} failed request(s), automatic actual-script recovery")
    finally:
        context.close()


def exhaustion(browser: Browser, base: str, missing_global: bool = False) -> None:
    context = local_context(browser, base)
    try:
        page = context.new_page()
        errors: list[str] = []
        requests: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def intercept(route: Route) -> None:
            requests.append(route.request.url)
            if missing_global and len(requests) > 1:
                route.fulfill(content_type="text/javascript", body="/* No readiness global. */")
            else:
                route.abort()

        page.route("**" + LEAFLET, intercept)
        sign_in(page, base, "#/overview")
        expect_failure(page, LEAFLET)
        count = 2 if missing_global else 3
        assert len(requests) == count
        page.get_by_role("link", name="My cases", exact=True).click()
        expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
        page.get_by_role("link", name="Overview", exact=True).click()
        expect_failure(page, LEAFLET)
        page.wait_for_timeout(800)
        assert len(requests) == count, "Route revisit must not reset the retry budget"
        reload_button = page.get_by_role("button", name="Reload workspace", exact=True)
        reload_button.focus()
        expect(reload_button).to_be_focused()
        assert reload_button.evaluate("el => getComputedStyle(el).outlineStyle === 'solid'")
        page.unroute("**" + LEAFLET)
        reload_button.press("Enter")
        expect(page.locator(".leaflet-container")).to_be_visible()
        assert not errors, errors
        scenario = "missing global" if missing_global else "exhaustion"
        print(f"PASS terminal {scenario}, native reload")
    finally:
        context.close()


def delayed_companion(
    browser: Browser, base: str, *, sign_out: bool = False, timed_out: bool = False
) -> None:
    context = local_context(browser, base)
    try:
        page = context.new_page()
        errors: list[str] = []
        pending: list[Route] = []
        requests: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def intercept(route: Route) -> None:
            requests.append(route.request.url)
            if len(requests) == 1:
                route.abort()
            else:
                pending.append(route)

        page.route("**/role-screens.js", intercept)
        sign_in(page, base, "#/screens")
        expect(page.locator("#workspace-status")).to_have_text(
            "Loading workspace files. Please wait."
        )
        page.wait_for_function(
            "() => document.querySelectorAll('head script[src=\"/role-screens.js\"]').length === 1"
        )
        assert len(pending) == 1
        if sign_out:
            page.locator("#account > summary").click()
            page.get_by_role("button", name="Sign out", exact=True).click()
            page.wait_for_url(base + "/")
            pending[0].abort()
            expect(page.get_by_role("heading", name="Workspace unavailable")).to_have_count(0)
        else:
            if timed_out:
                expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible(
                    timeout=7000
                )
                expect_failure(page, "/role-screens.js")
                assert len(requests) == 2, "Timeout must not overlap lexical script executions"
            page.get_by_role("link", name="My cases", exact=True).click()
            expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
            pending[0].continue_()
            page.wait_for_timeout(300)
            expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
            expect(page.locator("#workspace-status")).not_to_contain_text("unavailable")
            page.get_by_role("link", name="Specialist screens", exact=True).click()
            expect(
                page.get_by_role("heading", name="Specialist screens", exact=True)
            ).to_be_visible()
            assert len(requests) == 2
        assert not errors, errors
        scenario = "timeout and late load" if timed_out else "navigation"
        if sign_out:
            scenario = "sign-out"
        print(f"PASS delayed lexical companion: {scenario}")
    finally:
        context.close()


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for path, failures, hash_ in (
                (LEAFLET, 1, "#/overview"),
                (LEAFLET, 2, "#/overview"),
                ("/role-screens.js", 1, "#/screens"),
            ):
                recovery(browser, base, path, failures, hash_)
            exhaustion(browser, base)
            exhaustion(browser, base, missing_global=True)
            delayed_companion(browser, base)
            delayed_companion(browser, base, timed_out=True)
            delayed_companion(browser, base, sign_out=True)
            context = local_context(browser, base)
            try:
                response = context.request.get(base + LEAFLET)
                assert response.status == 200
                assert response.headers["content-type"] == "text/javascript; charset=utf-8"
                assert response.headers["cache-control"] == "no-store"
                assert int(response.headers["content-length"]) == len(response.body()) == 147552
                print("PASS local Leaflet HTTP 200, 147552 bytes, MIME, length and no-store")
            finally:
                context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, synthetic_data)
