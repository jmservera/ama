"""Synthetic loading, real action, HAX briefing and axe regressions for issue 531."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright

from checks.asset_urls import asset_url
from checks.design_system_browser_check import main
from checks.employee_briefing_browser_check import briefing_data
from checks.regulatory_ux_check import AXE_SHA256


def sign_in(page: Page, base: str) -> None:
    page.get_by_label("Work email", exact=True).fill("sam@example.test")
    page.get_by_label("Password", exact=True).fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
    expect(page.locator(".briefing [data-record-id]")).to_be_visible()


def static_shell_check(browser: Browser, base: str, output: Path) -> None:
    context = browser.new_context(java_script_enabled=False)
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        script_requests: list[str] = []
        page.on("request", lambda request: script_requests.append(request.url)
                if request.resource_type == "script" else None)
        page.goto(base + "/app")
        status = page.locator("#startup-status")
        expect(status).to_have_text(
            "Starting the workspace, this can take up to a minute when the service has been idle.")
        expect(status).to_have_attribute("role", "status")
        expect(status).to_have_attribute("aria-live", "polite")
        expect(page.locator("#app")).to_be_empty()
        expect(page.locator("#startup-retry")).to_be_hidden()
        assert page.locator("#startup").evaluate("""shell => [...document.scripts].every(
            script => Boolean(shell.compareDocumentPosition(script)
                & Node.DOCUMENT_POSITION_FOLLOWING))""")
        for width in (320, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            expect(status).to_be_in_viewport()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.screenshot(path=str(output / f"static-shell-{width}.png"), full_page=True)
        assert not script_requests, script_requests
        print("PASS static shell at 320/1280px with page JavaScript disabled; no scripts requested")
    finally:
        context.close()


def shell_check(browser: Browser, base: str) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        page.clock.install()
        held: list[Route] = []
        page.route(asset_url("/app.js", base), lambda route: held.append(route))
        with page.expect_request(asset_url("/app.js", base)):
            page.goto(base + "/app", wait_until="commit")
        expect(page.locator("#startup-status")).to_contain_text("up to a minute")
        expect(page.locator("#app")).to_be_empty()
        page.clock.fast_forward(4000)
        expect(page.locator("#startup-status")).to_contain_text("Still starting")
        expect(page.locator("#startup-retry")).to_be_visible()
        page.clock.fast_forward(11000)
        expect(page.locator("#startup-status")).to_contain_text("longer than expected")
        expect(page.locator("#startup-status")).to_have_attribute("aria-live", "polite")
        held[0].continue_()
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        expect(page.locator("#startup")).to_be_hidden()
        page.unroute(asset_url("/app.js", base))
        page.route("**/api/me", lambda route: route.fulfill(
            status=503, json={"error": "Synthetic service is unavailable"}))
        page.reload()
        expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible()
        expect(page.locator("#startup")).to_have_count(0)
        expect(page.get_by_role("alert")).to_contain_text("Synthetic service")
        page.unroute("**/api/me")
        page.get_by_role("button", name="Try again", exact=True).click()
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        page.route(asset_url("/app.js", base), lambda route: route.abort())
        page.reload()
        page.clock.fast_forward(16000)
        expect(page.locator("#startup-retry")).to_be_visible()
        page.unroute(asset_url("/app.js", base))
        page.locator("#startup-retry").click()
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        print("PASS static shell, held/failed script, slow/deadline and service retry")
    finally:
        context.close()


def watchdog_failure_check(browser: Browser, base: str, outcome: str) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        page.clock.install()
        errors: list[str] = []
        failures: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("requestfailed", lambda request: failures.append(request.url)
                if asset_url("/workspace-shell.js", base).search(request.url) else None)
        page.route(asset_url("/workspace-shell.js", base), lambda route: route.abort())
        if outcome == "error":
            page.route("**/api/me", lambda route: route.fulfill(
                status=503, json={"error": "Synthetic startup failure without watchdog"}))
        page.goto(base + "/app")
        if outcome == "authenticated":
            sign_in(page, base)
            page.reload()
            expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
        elif outcome == "error":
            expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible()
            expect(page.get_by_role("alert")).to_contain_text("Synthetic startup failure")
        else:
            expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        expect(page.locator("#startup")).to_have_count(0)
        page.clock.fast_forward(16000)
        expect(page.locator("#startup")).to_have_count(0)
        assert failures, "exercise an actual failed watchdog request"
        assert not errors, errors
        if outcome == "error":
            page.unroute("**/api/me")
            page.get_by_role("button", name="Try again", exact=True).click()
            expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        print(f"PASS failed workspace-shell.js: {outcome}, independent main cleanup")
    finally:
        context.close()


def companion_failure_check(browser: Browser, base: str, path: str, hash_: str) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        errors: list[str] = []
        requests: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def intercept(route: Route) -> None:
            requests.append(route.request.url)
            route.abort()

        page.route(asset_url(path, base), intercept)
        page.goto(base + "/app" + hash_)
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        expect(page.locator("#startup")).to_have_count(0)
        page.get_by_label("Work email", exact=True).fill("sam@example.test")
        page.get_by_label("Password", exact=True).fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        if path == "/case-workspace.js":
            expect(page.get_by_role("link", name="Back to the list", exact=True)).to_be_visible()
            expect(page.get_by_role("status").filter(
                has_text="Tab navigation unavailable. Case sections are listed below"
            )).to_be_visible()
            expect(page.locator("#case-panel-survey")).to_be_visible()
            expect(page.locator("#case-panel-history")).to_be_visible()
            assert len(requests) == 1, "optional enhancement must not trigger required retries"
        else:
            expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible()
            expect(page.get_by_role("alert")).to_contain_text(
                "Required workspace files did not load: " + path)
            expect(page.get_by_role("button", name="Reload workspace", exact=True)).to_be_visible()
            assert len(requests) == 3, requests
        expect(page.locator("#startup")).to_have_count(0)
        assert not errors, errors
        print(f"PASS failed {path}: bounded terminal recovery or explicit plain-case fallback")
    finally:
        context.close()


def law_startup_check(
    browser: Browser, base: str, blocked_script: str | None = None,
    service_failure: str | None = None,
) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        page.clock.install()
        errors: list[str] = []
        failures: list[str] = []
        reads: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("requestfailed", lambda request: failures.append(request.url))
        if blocked_script:
            page.route(asset_url(blocked_script, base), lambda route: route.abort())

        def sources(route: Route) -> None:
            reads.append(route.request.url)
            if service_failure == "rejected":
                route.abort()
            elif service_failure:
                route.fulfill(status=503, json={"error": "Synthetic initial sources failure"})
            else:
                route.fulfill(json={"sources": [], "gaps": []})

        page.route("**/api/law/sources", sources)
        page.goto(base + "/law.html")
        if blocked_script == "/law.js":
            expect(page.locator("#startup-status")).to_have_text("Loading sources...")
            page.clock.fast_forward(4000)
            expect(page.locator("#startup-status")).to_contain_text("Still starting the law viewer")
            page.clock.fast_forward(11000)
            expect(page.locator("#startup-status")).to_contain_text("longer than expected")
            expect(page.locator("#startup-retry")).to_be_visible()
            assert not reads, reads
            page.unroute(asset_url("/law.js", base))
            page.locator("#law-out").focus()
            page.keyboard.press("Tab")
            expect(page.locator("#startup-retry")).to_be_focused()
            page.keyboard.press("Enter")
        if service_failure:
            status = page.locator("#law-status")
            expect(status).to_contain_text("Try All sources or search again")
            error_text = status.inner_text()
            expect(page.locator("#startup")).to_have_count(0)
            page.clock.fast_forward(16000)
            expect(status).to_have_text(error_text)
            expect(page.locator("#startup")).to_have_count(0)
            service_failure = None
            page.get_by_role("button", name="All sources", exact=True).click()
        expect(page.get_by_role("heading", name="Sources held", exact=True)).to_be_visible()
        expect(page.locator("#startup")).to_have_count(0)
        page.clock.fast_forward(16000)
        expect(page.locator("#law-status")).to_have_text("0 sources and 0 gaps shown.")
        if blocked_script:
            assert any(asset_url(blocked_script, base).search(url) for url in failures), failures
        assert not errors, errors
        print(f"PASS law startup: blocked={blocked_script}, reads={len(reads)}, terminal cleanup")
    finally:
        context.close()


def helper_bootstrap_check(
    browser: Browser, base: str, failures: int, *, missing_global: bool = False,
    unready_helper: bool = False, unready_method: str | None = None,
) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        errors: list[str] = []
        requests: list[str] = []
        documents: list[str] = []
        service_reads: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: documents.append(request.url)
                if request.resource_type == "document" else None)
        page.on("request", lambda request: service_reads.append(request.url)
                if request.url == base + "/api/me" else None)

        def intercept(route: Route) -> None:
            requests.append(route.request.url)
            if len(requests) <= failures:
                route.abort()
            elif missing_global:
                route.fulfill(content_type="text/javascript", body="/* Missing helper. */")
            elif unready_helper:
                route.fulfill(content_type="text/javascript", body="var AsyncAction = {};")
            elif unready_method:
                route.fulfill(content_type="text/javascript", body=(
                    "var AsyncAction = {handler: task => task, run() {}, feedback() {}};"
                    f"AsyncAction.{unready_method} = true;"))
            else:
                route.continue_()

        page.route(asset_url("/async-action.js", base), intercept)
        page.goto(base + "/app#/case/ZF-1?tab=resident")
        terminal = failures == 3 or missing_global or unready_helper or bool(unready_method)
        if terminal:
            expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible()
            expect(page.get_by_role("alert")).to_contain_text(
                "Required workspace files did not load: /async-action.js")
            expect(page.locator("#workspace-status")).to_contain_text(
                "Workspace unavailable:")
            expect(page.locator("#workspace-status")).to_have_attribute("aria-live", "polite")
            expect(page.get_by_label("Work email", exact=True)).to_have_count(0)
            expect(page.get_by_role("button", name="Try again", exact=True)).to_have_count(0)
            assert not service_reads, "do not call start before helper readiness"
            expected_requests = 2 if missing_global or unready_helper or unready_method else 3
            assert len(requests) == expected_requests, requests
            if unready_helper:
                assert page.evaluate(
                    "() => typeof AsyncAction === 'object' && "
                    "typeof AsyncAction.handler !== 'function'")
            if unready_method:
                assert page.evaluate(
                    "(method) => typeof AsyncAction[method] !== 'function'", unready_method)
            page.wait_for_timeout(800)
            assert len(requests) == expected_requests, requests
            assert not errors, errors
            page.unroute(asset_url("/async-action.js", base))
            reload = page.get_by_role("button", name="Reload workspace", exact=True)
            page.locator("#app").focus()
            page.keyboard.press("Tab")
            expect(reload).to_be_focused()
            reload.press("Enter")
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        assert page.evaluate("() => typeof AsyncAction.handler === 'function'")
        if not terminal:
            assert len(requests) == failures + 1, requests
            assert len(documents) == 1, "automatic helper recovery must not reload the page"
        submit = page.get_by_role("button", name="Sign in", exact=True)
        page.get_by_label("Work email", exact=True).fill("sam@example.test")
        page.get_by_label("Password", exact=True).fill("synthetic-check")
        submit.click()
        expect(page.get_by_role("link", name="Back to the list", exact=True)).to_be_visible()
        expect(page.get_by_role("button", name="Draft with AI", exact=True)).to_be_visible()
        page.locator("#account > summary").click()
        logout: list[Route] = []
        page.route("**/api/logout", lambda route: logout.append(route))
        signout = page.get_by_role("button", name="Sign out", exact=True)
        with page.expect_request("**/api/logout"):
            signout.click()
        expect(signout).to_be_disabled()
        expect(signout).to_have_attribute("aria-busy", "true")
        assert len(logout) == 1
        logout[0].fulfill(status=503, json={"error": "Synthetic sign-out failure"})
        expect(page.locator("#account-error")).to_have_text("Synthetic sign-out failure")
        expect(signout).to_be_enabled()
        assert not errors, errors
        print(f"PASS helper bootstrap: failures={failures}, missing_global={missing_global}, "
              f"unready_helper={unready_helper}, unready_method={unready_method}")
    finally:
        context.close()


def law_helper_check(browser: Browser, base: str, failure: str) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        errors: list[str] = []
        reads: list[str] = []
        helper_reads: list[str] = []
        documents: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: reads.append(request.url)
                if "/api/law/" in request.url else None)
        page.on("request", lambda request: documents.append(request.url)
                if request.resource_type == "document" else None)

        def intercept(route: Route) -> None:
            helper_reads.append(route.request.url)
            if failure == "blocked":
                route.abort()
            else:
                scripts = {
                    "missing": "/* No helper exported. */",
                    "null": "var AsyncAction = null;",
                    "handler-only": "var AsyncAction = {handler: task => task};",
                    "run-only": "var AsyncAction = {run() {}};",
                }
                route.fulfill(content_type="text/javascript", body=scripts[failure])

        page.route(asset_url("/async-action.js", base), intercept)
        meta: dict[str, Any] = dict(
            status="Synthetic reference", completeness="Complete",
            effective=None, retrieved="2026-10-29", version="1", caveats=[])
        source = dict(meta, id="synthetic-source", title="Synthetic source",
                      owner="Synthetic owner", official_url=None)
        provision = dict(meta, id="synthetic-provision", heading_path="Synthetic provision",
                         text="Constructed reference text.")
        page.route("**/api/law/sources", lambda route: route.fulfill(
            json={"sources": [source], "gaps": []}))
        page.route("**/api/law/sources/synthetic-source", lambda route: route.fulfill(
            json={"source": source, "versions": [dict(meta, content_hash="synthetic")],
                  "provisions": [provision]}))
        page.route("**/api/law/provisions/synthetic-provision", lambda route: route.fulfill(
            json=provision))
        page.route("**/api/law/search?**", lambda route: route.fulfill(json={
            "caveats": [], "no_source_held": [], "results": [
                dict(provision, title="Synthetic source")]}))
        page.goto(base + "/law.html")
        expect(page.get_by_role("heading", name="Law viewer unavailable")).to_be_visible()
        expect(page.get_by_role("alert")).to_contain_text(
            "Required law viewer file did not load: /async-action.js")
        expect(page.locator("#law-status")).not_to_contain_text("Loading sources")
        expect(page.locator("#law-status")).to_have_attribute("aria-live", "polite")
        expect(page.get_by_role("button", name="All sources", exact=True)).to_be_disabled()
        expect(page.get_by_role("button", name="Search", exact=True)).to_be_disabled()
        expect(page.get_by_label("Search the provisions", exact=True)).to_be_disabled()
        page.locator("#law-form").evaluate("form => form.requestSubmit()")
        page.wait_for_timeout(800)
        assert not reads, reads
        assert not errors, errors
        assert len(documents) == 1, documents
        assert len(helper_reads) == 1, helper_reads
        page.unroute(asset_url("/async-action.js", base))
        reload = page.get_by_role("button", name="Reload law viewer", exact=True)
        expect(page.locator("#law-out")).to_be_focused()
        page.keyboard.press("Tab")
        expect(reload).to_be_focused()
        reload.press("Enter")
        expect(page.get_by_role("heading", name="Sources held", exact=True)).to_be_visible()
        assert len(documents) == 2, documents
        assert reads == [base + "/api/law/sources"], reads
        page.get_by_role("button", name="Synthetic source", exact=True).click()
        expect(page.get_by_role("heading", name="Synthetic source", exact=True)).to_be_visible()
        page.get_by_role("button", name="Synthetic provision", exact=True).click()
        expect(page.locator("#law-out pre")).to_have_text("Constructed reference text.")
        page.get_by_role("button", name="All sources", exact=True).click()
        expect(page.get_by_role("heading", name="Sources held", exact=True)).to_be_visible()
        page.get_by_label("Search the provisions", exact=True).fill("Synthetic")
        page.get_by_role("button", name="Search", exact=True).click()
        expect(page.get_by_role("heading", name="Search results", exact=True)).to_be_visible()
        page.get_by_role("button", name="Synthetic source: Synthetic provision").click()
        expect(page.locator("#law-out pre")).to_have_text("Constructed reference text.")
        assert not errors, errors
        print(f"PASS law helper {failure}: native keyboard reload and restored list/search/details")
    finally:
        context.close()


def run_browser(base: str, axe: str, output: Path) -> None:
    reports: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            static_shell_check(browser, base, output)
            shell_check(browser, base)
            for outcome in ("signed-out", "authenticated", "error"):
                watchdog_failure_check(browser, base, outcome)
            for path, hash_ in (
                ("/panels.js", "#/case/ZF-1"), ("/ops.js", "#/case/ZF-1"),
                ("/assistants.js", "#/case/ZF-1"), ("/chat.js", "#/case/ZF-1"),
                ("/timecapture.js", "#/time"), ("/role-screens.js", "#/screens"),
                ("/vendor/leaflet.js", "#/overview"), ("/case-workspace.js", "#/case/ZF-1"),
            ):
                companion_failure_check(browser, base, path, hash_)
            law_startup_check(browser, base, "/law.js")
            law_startup_check(browser, base, "/workspace-shell.js")
            for blocked in (None, "/workspace-shell.js"):
                for failure in ("503", "rejected"):
                    law_startup_check(browser, base, blocked, failure)
            for failures in (1, 2, 3):
                helper_bootstrap_check(browser, base, failures)
            helper_bootstrap_check(browser, base, 1, missing_global=True)
            helper_bootstrap_check(browser, base, 0, unready_helper=True)
            for method in ("run", "feedback"):
                helper_bootstrap_check(browser, base, 0, unready_method=method)
            for failure in ("blocked", "missing", "null", "handler-only", "run-only"):
                law_helper_check(browser, base, failure)
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            context.route("**/*", lambda route: route.continue_()
                          if route.request.url.startswith(base + "/") else route.abort())
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "/app")
            sign_in(page, base)
            # Keep typing during overlapping debounced reads; newest response wins.
            search = page.get_by_role("searchbox", name="Find", exact=True)
            cases = page.request.get(base + "/api/cases?view=mine&limit=50").json()
            search_reads: list[Route] = []
            page.route("**/api/cases?**", lambda route: search_reads.append(route))
            with page.expect_request("**/api/cases?**"):
                search.fill("First query")
            expect(search).to_be_enabled()
            expect(search).to_be_focused()
            expect(page.locator(".side .async-feedback")).to_contain_text("Finding cases")
            with page.expect_request("**/api/cases?**"):
                search.press("End")
                search.press_sequentially(" updated")
            expect(search).to_have_value("First query updated")
            expect(search).to_be_enabled()
            expect(search).to_be_focused()
            assert len(search_reads) == 2
            search_reads[1].fulfill(json={**cases, "items": [], "total": 0, "next_cursor": None})
            expect(page.locator(".empty")).to_contain_text("No cases match these filters")
            search_reads[0].fulfill(json=cases)
            expect(page.locator(".side .async-feedback")).to_have_count(0)
            expect(page.locator(".empty")).to_contain_text("No cases match these filters")
            expect(search).to_be_focused()
            page.unroute("**/api/cases?**")
            page.get_by_role("button", name="Reset my queue", exact=True).click()
            expect(page.locator(".item").first).to_be_visible()
            print("PASS editable/focused debounced search and out-of-order response guard")
            briefing = page.locator(".briefing")
            expect(briefing).to_contain_text("Summary by rules")
            expect(briefing.locator("time")).to_have_count(1)
            expect(briefing.get_by_role("textbox")).to_have_count(0)
            # Hidden controls remain in the DOM but only the chosen outcome exposes them.
            assert briefing.locator("textarea:visible").count() == 0
            briefing.get_by_role("button", name="Hide briefing", exact=True).click()
            expect(briefing.locator(".briefing-content")).to_be_hidden()
            briefing.get_by_role("button", name="Show briefing", exact=True).click()
            briefing.get_by_role("button", name="Edit this draft", exact=True).click()
            edit = briefing.get_by_label("Edited draft", exact=True)
            reason = briefing.get_by_label("Reason", exact=True)
            edit.fill("Locally corrected briefing")
            reason.fill("Checked the records")
            briefing.get_by_role("button", name="Cancel review", exact=True).click()
            expect(edit).to_be_hidden()
            expect(briefing.get_by_role("button", name="Edit this draft", exact=True)
                   ).to_be_focused()
            briefing.get_by_role("button", name="Edit this draft", exact=True).click()
            expect(edit).to_have_value("Locally corrected briefing")
            expect(reason).to_have_value("Checked the records")
            reads: list[str] = []
            page.on("request", lambda request: reads.append(request.url)
                    if "/api/briefing" in request.url else None)
            refresh = briefing.get_by_role("button", name="Refresh briefing", exact=True)
            mode = briefing.get_by_label(
                "How to prepare briefings and draft requests", exact=True)
            page.once("dialog", lambda dialog: dialog.dismiss())
            refresh.click()
            expect(edit).to_have_value("Locally corrected briefing")
            assert not reads, "cancelled refresh must not read or replace evidence"
            page.once("dialog", lambda dialog: dialog.dismiss())
            mode.select_option("workflow")
            expect(mode).to_have_value("ai")
            expect(reason).to_have_value("Checked the records")
            assert not reads, "cancelled mode change must not read or replace evidence"
            page.route("**/api/briefing", lambda route: route.fulfill(
                status=503, json={"error": "Synthetic refresh failure"}))
            page.once("dialog", lambda dialog: dialog.accept())
            refresh.click()
            expect(briefing.get_by_role("status").filter(
                has_text="Synthetic refresh failure")).to_be_visible()
            expect(edit).to_have_value("Locally corrected briefing")
            expect(reason).to_have_value("Checked the records")
            page.unroute("**/api/briefing")
            page.once("dialog", lambda dialog: dialog.accept())
            refresh.click()
            expect(edit).to_be_hidden()
            briefing.get_by_role("button", name="Edit this draft", exact=True).click()
            expect(edit).not_to_have_value("Locally corrected briefing")
            expect(reason).to_have_value("")
            edit.fill("Locally corrected briefing")
            reason.fill("Checked the records")
            held: list[Route] = []
            page.route("**/api/ai/review/*/edit", lambda route: held.append(route))
            submit = briefing.get_by_role("button", name="Save edited draft review", exact=True)
            with page.expect_request("**/api/ai/review/*/edit"):
                submit.click()
            expect(submit).to_be_disabled()
            expect(briefing.locator(".async-feedback").first).to_be_visible()
            expect(briefing.locator(".async-spinner").first).to_be_visible()
            before_reads = len(reads)
            refresh.click()
            mode.select_option("workflow")
            expect(mode).to_have_value("ai")
            expect(briefing).to_contain_text("Finish the pending review first")
            assert len(reads) == before_reads
            submit.evaluate("el => el.click()")
            assert len(held) == 1, "refresh cannot remount a second review dispatcher"
            assert held[0].request.post_data_json == {
                "reason": "Checked the records", "text": "Locally corrected briefing"}
            held[0].fulfill(status=503, json={"error": "Synthetic review failed"})
            expect(briefing.get_by_role("status").filter(
                has_text="Synthetic review failed")).to_be_visible()
            expect(submit).to_be_enabled()
            page.unroute("**/api/ai/review/*/edit")
            briefing.get_by_role("button", name="Cancel review", exact=True).click()
            briefing.get_by_role("button", name="Do not use this draft", exact=True).click()
            expect(edit).to_be_hidden()
            expect(reason).to_be_visible()
            cancel_review = briefing.get_by_role("button", name="Cancel review", exact=True)
            cancel_review.focus()
            cancel_review.press("Enter")
            expect(briefing.get_by_role("button", name="Do not use this draft", exact=True)
                   ).to_be_focused()
            briefing.get_by_role("button", name="Do not use this draft", exact=True).click()
            reason.fill("")
            briefing.get_by_role("button", name="Record rejection", exact=True).click()
            expect(reason).to_have_attribute("aria-invalid", "true")
            print("PASS source/time/type labels, local undo and conditional review/error")

            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.evaluate(axe)
                result = page.evaluate("""async () => await axe.run(
                    {include: [['.briefing']]},
                    {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa',
                    'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
                reports.append(dict(state=f"briefing-{width}", result=result))
                assert not result["violations"], json.dumps(result["violations"], indent=2)
            page.emulate_media(reduced_motion="reduce")
            page.evaluate("""() => {
                const icon = document.createElement('span');
                icon.id = 'motion-check'; icon.className = 'async-spinner';
                document.body.append(icon);
            }""")
            assert page.locator("#motion-check").evaluate(
                "el => getComputedStyle(el).animationName") == "none"
            page.locator("#motion-check").evaluate("el => el.remove()")
            original = page.request.get(base + "/api/briefing").json()
            original.update(
                source="ai", verified=False, label="AI suggestion, not approved",
                reason=None, source_case_ids=["ZF-1"],
                text="Synthetic cited statement.\nSynthetic unsupported statement.",
                citations=["Stage: Contacting resident"],
                unresolved=["ZF-1: Invented fact"],
                statements=[
                    dict(text="Synthetic cited statement.",
                         citations=["Stage: Contacting resident"], unresolved=[]),
                    dict(text="Synthetic unsupported statement.",
                         citations=[], unresolved=["ZF-1: Invented fact"]),
                ],
            )
            held_briefing: list[Route] = []
            page.route("**/api/briefing", lambda route: held_briefing.append(route))
            page.once("dialog", lambda dialog: dialog.accept())
            with page.expect_request("**/api/briefing"):
                refresh.click()
            expect(briefing.locator(".briefing-content")).to_have_attribute("aria-busy", "true")
            assert briefing.get_by_role("status").filter(
                has_text="Reading case summaries").evaluate(
                    "el => !el.closest('[aria-busy=true]')")
            held_briefing[0].fulfill(json=original)
            expect(briefing).to_contain_text("Generated briefing and its sources")
            assert briefing.locator(".field-error").evaluate(
                "el => getComputedStyle(el, ':before').content") == "none"
            expect(briefing.get_by_role("button", name="Use this draft", exact=True)
                   ).to_be_disabled()
            for unavailable in ({"verified": False}, {"verified": True, "stale": True}):
                if unavailable.get("stale"):
                    held_briefing.clear()
                    with page.expect_request("**/api/briefing"):
                        refresh.click()
                    held_briefing[0].fulfill(json={**original, **unavailable})
                expect(briefing.get_by_role("button", name="Edit this draft", exact=True)
                       ).to_be_disabled()
                reject = briefing.get_by_role(
                    "button", name="Do not use this draft", exact=True)
                expect(reject).to_be_enabled()
                reject.focus()
                reject.press("Enter")
                expect(briefing.get_by_label("Reason", exact=True)).to_be_focused()
                cancel_review.focus()
                cancel_review.press("Enter")
                expect(cancel_review).to_be_hidden()
                expect(reject).to_be_focused()
            briefing.get_by_text("Sources used (1)", exact=True).click()
            expect(briefing.get_by_role("link", name="Stage: Contacting resident")
                   ).to_have_attribute("href", "#/case/ZF-1")
            briefing.get_by_text("Sources used (0)", exact=True).click()
            expect(briefing).to_contain_text("ZF-1: Invented fact. Do not rely")
            page.evaluate(axe)
            result = page.evaluate("""async () => await axe.run(
                {include: [['.briefing']]},
                {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa',
                'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
            reports.append(dict(state="ai-unverified-sources", result=result))
            assert not result["violations"], json.dumps(result["violations"], indent=2)
            page.unroute("**/api/briefing")
            page.route("**/api/briefing", lambda route: route.fulfill(json=original))
            for http_status, outcome in ((409, "committed"), (503, "uncertain")):
                page.reload()
                expect(briefing).to_contain_text("Generated briefing and its sources")
                briefing.get_by_role(
                    "button", name="Do not use this draft", exact=True).click()
                briefing.get_by_label("Reason", exact=True).fill("Check this review history")
                held.clear()
                page.route("**/api/ai/review/*/reject", lambda route: held.append(route))
                rejection = briefing.get_by_role("button", name="Record rejection", exact=True)
                with page.expect_request("**/api/ai/review/*/reject"):
                    rejection.click()
                held[0].fulfill(status=http_status, json={
                    "error": "Synthetic confirmation needs checking", "outcome": outcome})
                expect(briefing).to_contain_text("Confirmation needs checking")
                expect(rejection).to_be_disabled()
                before_reads = len(reads)
                refresh.click()
                mode.select_option("workflow")
                expect(mode).to_have_value("ai")
                expect(briefing).to_contain_text("Finish the pending review first")
                assert len(reads) == before_reads
                rejection.evaluate("el => el.click()")
                assert len(held) == 1, "history barrier must not allow a second review"
                page.unroute("**/api/ai/review/*/reject")
            print("PASS guarded refresh/mode, retained failed-refresh edits and outcome barriers")
            page.unroute("**/api/briefing")
            page.screenshot(path=str(output / "briefing.png"), full_page=True)
            # Actual resident draft action, with getText-backed review.
            page.once("dialog", lambda dialog: dialog.accept())
            page.goto(base + "/app#/case/ZF-1?tab=resident")
            draft = page.get_by_role("button", name="Draft with AI", exact=True)
            held.clear()
            page.route("**/api/cases/ZF-1/ai", lambda route: held.append(route))
            with page.expect_request("**/api/cases/ZF-1/ai"):
                draft.click()
            expect(draft).to_be_disabled()
            expect(page.locator("#case-panel-resident .async-spinner").first).to_be_visible()
            draft.evaluate("el => el.click()")
            assert len(held) == 1
            held[0].fulfill(response=held[0].fetch())
            page.unroute("**/api/cases/ZF-1/ai")
            expect(draft).to_be_enabled()
            draft_text = page.get_by_label("Draft", exact=True)
            draft_text.fill("Visible resident replacement")
            resident_review = page.locator("#resident-draft-output .aimeta")
            resident_review.get_by_role("button", name="Edit this draft", exact=True).click()
            resident_review.get_by_label("Reason", exact=True).fill("Checked resident wording")
            with page.expect_request("**/api/ai/review/*/edit") as review_request:
                resident_review.get_by_role(
                    "button", name="Save edited draft review", exact=True).click()
            review_body = review_request.value.post_data_json
            assert isinstance(review_body, dict)
            assert review_body["text"] == draft_text.input_value()
            expect(resident_review).to_have_attribute("data-review-state", "Edited")
            print("PASS real async draft deduplication and visible resident review payload")

            # Mount the shipped appointment control with an explicit synthetic binding.
            page.evaluate("""() => {
                const state = {current_binding: {measure: 'Synthetic', revision: 1},
                    offer: null, status: 'No offer', case_id: 'ZF-1', case_version: 1,
                    missing: [], closure_history: [], counts: {}, case_closed: true};
                const panel = appointmentControls({id: 'SYN-531', case_id: 'ZF-1',
                    appointment_control: state},
                    body => api('/api/workorders/SYN-531/appointment-control', body));
                panel.id = 'synthetic-appointment';
                app.append(panel);
            }""")
            appointment = page.locator("#synthetic-appointment")
            appointment.get_by_text("Record appointment offer for SYN-531", exact=True).click()
            form = appointment.locator('form[data-appointment-form="SYN-531-offer"]')
            for field in form.locator("input[required]").all():
                field.fill("2026-11-01" if field.get_attribute("type") == "date"
                           else "Synthetic appointment detail")
            held.clear()
            page.route("**/api/workorders/SYN-531/appointment-control",
                       lambda route: held.append(route))
            appointment_submit = form.get_by_role(
                "button", name="Record appointment offer", exact=True)
            with page.expect_request("**/api/workorders/SYN-531/appointment-control"):
                appointment_submit.click()
            expect(appointment_submit).to_be_disabled()
            expect(appointment.locator(".async-spinner")).to_be_visible()
            assert appointment.locator(".async-feedback").evaluate(
                "el => !el.closest('[aria-busy=true]')")
            form.evaluate("el => el.requestSubmit()")
            assert len(held) == 1
            held[0].fulfill(status=503, json={"error": "Synthetic appointment failure"})
            expect(appointment.get_by_role("status").filter(
                has_text="Synthetic appointment failure")).to_be_visible()
            expect(appointment_submit).to_be_enabled()
            # Test-only UI is removed; no synthetic mutation reached the store.
            page.locator("#synthetic-appointment").evaluate("el => el.remove()")
            page.unroute("**/api/workorders/SYN-531/appointment-control")
            print("PASS actual appointment submit promise, disabled duplicates and errors")

            held.clear()
            page.route("**/api/map?**", lambda route: held.append(route))
            page.once("dialog", lambda dialog: dialog.accept())
            page.goto(base + "/app#/overview")
            map_panel = page.locator("section").filter(has=page.get_by_role(
                "heading", name="Map of open cases", exact=True))
            expect(page.locator("#leaflet")).to_have_attribute("aria-busy", "true")
            expect(map_panel).to_contain_text("Loading map records")
            expect(map_panel.locator(".async-spinner").first).to_be_visible()
            held[0].fulfill(response=held[0].fetch())
            page.unroute("**/api/map?**")
            expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
            print("PASS library-driven map refresh regional feedback")

            # Real standalone law viewer action uses the same helper, without app.js.
            page.route("**/api/law/sources", lambda route: route.fulfill(
                json={"sources": [], "gaps": []}))
            page.goto(base + "/law.html")
            expect(page.get_by_role("heading", name="Sources held", exact=True)).to_be_visible()
            page.unroute("**/api/law/sources")
            held.clear()
            page.route("**/api/law/sources", lambda route: held.append(route))
            law = page.get_by_role("button", name="All sources", exact=True)
            with page.expect_request("**/api/law/sources"):
                law.click()
            expect(law).to_be_disabled()
            expect(page.locator(".async-spinner").first).to_be_visible()
            law.evaluate("el => el.click()")
            assert len(held) == 1
            held[0].fulfill(status=503, json={"error": "Synthetic law read failed"})
            expect(page.locator("#law-status")).to_contain_text("Synthetic law read failed")
            expect(law).to_be_enabled()
            page.unroute("**/api/law/sources")
            page.route("**/api/law/sources", lambda route: route.fulfill(
                json={"sources": [], "gaps": []}))
            law.click()
            expect(page.locator("#law-status")).to_have_text("0 sources and 0 gaps shown.")
            assert not errors, errors
            context.close()
            print(f"PASS law feedback/error/recovery; Chromium {browser.version}; no Azure/live AI")
        finally:
            browser.close()
            (output / "axe-results.json").write_text(json.dumps(reports, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    axe_bytes = args.axe.read_bytes()
    if hashlib.sha256(axe_bytes).hexdigest() != AXE_SHA256:
        raise ValueError("Expected the pinned axe-core 4.10.3 file")
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, axe_bytes.decode(), args.out), briefing_data)
