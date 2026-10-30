"""Exercise employee asset recovery on the real server with public synthetic fixtures."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from playwright.sync_api import Browser, Page, Route, sync_playwright

from checks.design_system_browser_check import check, main
from checks.workbench_browser_check import synthetic_data

CASE = "ZF-2026-0597"
CASE_PATH = f"/app?synthetic=employee-recovery#/case/{CASE}?tab=quality"
QUALITY = "Quality checks and defects"


def employee_data() -> dict[str, Any]:
    data = synthetic_data()
    data["cases"][0]["id"] = CASE
    return data


def sign_in(page: Page, base: str) -> None:
    page.goto(base + CASE_PATH)
    page.locator("#email").fill("sam@example.test")
    page.locator("#pw").fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()


def case_ready(page: Page) -> None:
    page.get_by_role("tab", name="Quality and handover", exact=True).click()
    page.get_by_role("heading", name=QUALITY, exact=True).wait_for()
    check("case renders without partial-workspace error", page.get_by_role(
        "heading", name="Workspace unavailable", exact=True
    ).count() == 0)


def new_page(browser: Browser, base: str) -> tuple[Page, list[str], list[str]]:
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    # This focused journey never needs a remote resource, including map tiles.
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    page = context.new_page()
    errors: list[str] = []
    documents: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: documents.append(request.url)
            if request.resource_type in ("document", "script") else None)
    return page, errors, documents


def healthy_and_api_retry(browser: Browser, base: str) -> None:
    page, errors, documents = new_page(browser, base)
    scripts: dict[str, tuple[int, str]] = {}
    page.on("response", lambda response: scripts.__setitem__(
        urlparse(response.url).path,
        (response.status, response.headers.get("content-type", "")),
    ) if response.request.resource_type == "script" else None)
    try:
        sign_in(page, base)
        case_ready(page)
        paths = page.locator("script[src]").evaluate_all("els => els.map(el => new URL(el.src).pathname)")
        check("all actual shell scripts return JavaScript 200",
              all(scripts[path][0] == 200 and "text/javascript" in scripts[path][1] for path in paths))
        check("ops executes before app with no service worker",
              paths.index("/ops.js") < paths.index("/app.js")
              and page.evaluate("typeof qualityPanel === 'function' && !navigator.serviceWorker.controller"))
        original_documents = list(documents)
        case_api = f"**/api/cases/{CASE}"
        page.route(case_api, lambda route: route.fulfill(
            status=503, json={"error": "Synthetic case API unavailable"}
        ))
        page.get_by_role("link", name="Back to the list", exact=True).click()
        page.get_by_role("heading", name="My cases today", exact=True).wait_for()
        page.locator(f'a.item[href="#/case/{CASE}"]').click()
        page.get_by_role("alert").filter(has_text="Synthetic case API unavailable").wait_for()
        page.unroute(case_api)
        retry = page.get_by_role("button", name="Try again", exact=True)
        retry.focus()
        retry.press("Enter")
        case_ready(page)
        check("ordinary API retry does not reload document/scripts", documents == original_documents)
        check("healthy and API retry produce no pageerrors", not errors)
    finally:
        page.context.close()


def missing_ops_recovery(browser: Browser, base: str) -> None:
    page, errors, documents = new_page(browser, base)

    def missing(route: Route) -> None:
        route.fulfill(status=404, content_type="text/plain", body="Synthetic missing ops.js")

    page.route("**/ops.js", missing)
    try:
        sign_in(page, base)
        page.get_by_role("heading", name="Workspace unavailable", exact=True).wait_for()
        check("missing ops names the actual dependency",
              "/ops.js" in page.get_by_role("alert").inner_text())
        check("case controls are not silently omitted",
              page.get_by_role("heading", name=QUALITY, exact=True).count() == 0)
        for width in (320, 390, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            check(f"asset error reflows at {width}px",
                  page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
        original_url, original_count = page.url, len(documents)
        page.unroute("**/ops.js", missing)
        reload_button = page.get_by_role("button", name="Reload workspace", exact=True)
        reload_button.focus()
        reload_button.press("Enter")
        case_ready(page)
        check("keyboard document reload keeps full case URL and session",
              page.url == original_url and page.locator("#email").count() == 0)
        check("reload refetches the previously failed ops file",
              len(documents) > original_count
              and sum(urlparse(url).path == "/ops.js" for url in documents) == 2)
        check("missing dependency uses handled feedback, not ReferenceError", not errors)
    finally:
        page.context.close()


def unrelated_script_failure(browser: Browser, base: str) -> None:
    page, errors, _ = new_page(browser, base)
    page.route("**/role-screens.js", lambda route: route.fulfill(
        status=404, content_type="text/plain", body="Synthetic missing specialist module"
    ))
    try:
        sign_in(page, base)
        case_ready(page)
        page.get_by_role("link", name="Back to the list", exact=True).click()
        page.get_by_role("heading", name="My cases today", exact=True).wait_for()
        check("missing specialist module leaves ordinary case and queue usable", True)
        page.evaluate("location.hash = '#/screens'")
        page.get_by_role("heading", name="Workspace unavailable", exact=True).wait_for()
        check("affected specialist route names its dependency",
              "/role-screens.js" in page.get_by_role("alert").inner_text())
        check("unrelated and affected routes produce no pageerrors", not errors)
    finally:
        page.context.close()


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            healthy_and_api_retry(browser, base)
            missing_ops_recovery(browser, base)
            unrelated_script_failure(browser, base)
            print(f"Chromium {browser.version}; synthetic loopback only; no live AI or Azure.")
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, employee_data)
