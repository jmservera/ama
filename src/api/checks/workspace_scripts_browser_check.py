"""Check bounded workspace recovery against an owned synthetic loopback API."""

from __future__ import annotations

from urllib.parse import urlsplit

from playwright.sync_api import (
    Browser, BrowserContext, CDPSession, Page, Route, expect, sync_playwright,
)

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
    submit_sign_in(page)


def submit_sign_in(page: Page) -> None:
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
        failed: list[str] = []
        pending: list[Route] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "requestfailed",
            lambda request: failed.append(request.failure or "")
            if urlsplit(request.url).path == path else None,
        )
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
                pending.append(route)
                page.evaluate("() => { window.workspaceRetryPending = true; }")

        page.route("**" + path, intercept)
        page.goto(base + "/app" + hash_)
        assert len(requests) == 1, "The initial HTML load must fail before recovery"
        assert len(failed) == 1 and failed[0], failed
        readiness = "typeof L === 'object'" if path == LEAFLET else (
            "typeof roleScreensView === 'function'"
        )
        assert page.evaluate("() => !(" + readiness + ")"), "Initial failure must omit readiness"
        submit_sign_in(page)
        expect(page.locator("#workspace-status")).to_have_text(
            "Loading workspace files. Please wait."
        )
        page.wait_for_function("() => window.workspaceRetryPending === true")
        assert len(requests) == failures + 1 and len(pending) == 1, requests
        assert page.evaluate("() => !(" + readiness + ")"), "Retry must still be pending"
        with page.expect_response(base + path) as response:
            pending[0].continue_()
        assert response.value.status == 200
        page.wait_for_function("() => " + readiness)
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
        page.locator("#app").focus()
        page.keyboard.press("Tab")
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


def observe_companion(page: Page) -> CDPSession:
    session = page.context.new_cdp_session(page)
    session.send("Profiler.enable")
    session.send("Profiler.startPreciseCoverage", {"callCount": True, "detailed": True})
    page.add_init_script("""
      window.workspaceScriptEvents = [];
      new MutationObserver(records => {
        for (const record of records) for (const script of record.addedNodes) {
          if (script.tagName !== 'SCRIPT'
              || new URL(script.src, location.href).pathname !== '/role-screens.js') continue;
          script.addEventListener('load', () => {
            const ready = typeof roleScreensView === 'function';
            window.workspaceScriptEvents.push({outcome: 'load', ready});
          }, {once: true});
          script.addEventListener('error', () => {
            window.workspaceScriptEvents.push({outcome: 'error', ready: false});
          }, {once: true});
        }
      }).observe(document, {childList: true, subtree: true});
    """)
    return session


def companion_coverage(session: CDPSession, base: str) -> tuple[int, int]:
    coverage = session.send("Profiler.takePreciseCoverage")["result"]
    scripts = [script for script in coverage if script["url"] == base + "/role-screens.js"]
    assert len(scripts) <= 1, "The actual lexical companion must not be evaluated twice"
    if not scripts:
        return 0, 0
    functions = scripts[0]["functions"]
    views = [function for function in functions if function["functionName"] == "roleScreensView"]
    assert len(views) == 1, "Measure the original view entry, not a later-installed wrapper"
    return functions[0]["ranges"][0]["count"], views[0]["ranges"][0]["count"]


def delayed_companion(
    browser: Browser, base: str, *, sign_out: bool = False, timed_out: bool = False,
    session_ended: bool = False,
) -> None:
    context = local_context(browser, base)
    try:
        page = context.new_page()
        errors: list[str] = []
        pending: list[Route] = []
        requests: list[str] = []
        documents: list[str] = []
        session = observe_companion(page)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "request",
            lambda request: documents.append(request.url)
            if request.resource_type == "document" else None,
        )

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
            if session_ended:
                page.route(
                    "**/api/correction-session",
                    lambda route: route.fulfill(
                        status=401, content_type="application/json", body="{}"
                    ),
                )
                ended = page.evaluate("""async () => {
                  try { await api('/api/correction-session'); }
                  catch (error) { return error.message; }
                  throw new Error('Constructed session expiry must reject');
                }""")
                assert ended == "Your session has ended. Sign in again."
                expect(page.get_by_role("heading", name="Sign in", exact=True)).to_be_visible()
                expect(page.get_by_role("alert")).to_have_text(ended)
                assert page.evaluate("() => me === null && !routeController.signal.aborted")
            if timed_out:
                expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible(
                    timeout=7000
                )
                expect_failure(page, "/role-screens.js")
                assert len(requests) == 2, "Timeout must not overlap lexical script executions"
            if not session_ended:
                page.get_by_role("link", name="My cases", exact=True).click()
                expect(
                    page.get_by_role("heading", name="My cases today", exact=True)
                ).to_be_visible()
                expect(page.locator("#workspace-status")).to_contain_text(
                    "Perspective: Resident Liaison Officer. My assigned cases. 2 cases."
                )
            else:
                expect(page.locator("#workspace-status")).to_have_text("")
            status = page.locator("#workspace-status").inner_text()
            hash_ = page.evaluate("() => location.hash")
            before = page.evaluate("() => window.workspaceScriptEvents.length")
            pending[0].continue_()
            page.wait_for_function(
                "before => window.workspaceScriptEvents.length > before", arg=before,
                timeout=10000,
            )
            settled = page.evaluate("() => window.workspaceScriptEvents.at(-1)")
            evaluations, view_calls = companion_coverage(session, base)
            assert evaluations == (1 if settled["ready"] else 0), (settled, evaluations)
            assert settled["outcome"] == ("load" if evaluations else "error"), settled
            assert view_calls == 0, "No original view invocation may escape session/route guards"
            assert page.evaluate("() => location.hash") == hash_
            expect(page.locator("#workspace-status")).to_have_text(status)
            expect(page.get_by_role("heading", name="Workspace unavailable")).to_have_count(0)
            if session_ended:
                expect(page.get_by_role("heading", name="Sign in", exact=True)).to_be_visible()
                expect(page.get_by_role("alert")).to_have_text(ended)
                assert page.evaluate("() => me === null && !routeController.signal.aborted")
            else:
                expect(
                    page.get_by_role("heading", name="My cases today", exact=True)
                ).to_be_visible()
                page.get_by_role("link", name="Specialist screens", exact=True).click()
                if evaluations:
                    expect(
                        page.get_by_role("heading", name="Specialist screens", exact=True)
                    ).to_be_visible()
                    _, view_calls = companion_coverage(session, base)
                    assert view_calls == 1, "A legitimate revisit must invoke the original view"
                else:
                    expect_failure(page, "/role-screens.js")
                    assert page.evaluate("() => typeof roleScreensView === 'undefined'")
            assert len(requests) == 2
            assert len(documents) == 1, "Recovery must not refresh the document"
            print(f"PASS real companion settlement: {settled}, evaluations={evaluations}")
        assert not errors, errors
        scenario = "timeout and late load" if timed_out else "navigation"
        if sign_out:
            scenario = "sign-out"
        if session_ended:
            scenario = "same-document 401/login"
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
            delayed_companion(browser, base, session_ended=True)
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
