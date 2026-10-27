"""Focused Chromium check of the actual local app with existing constructed showcase fixtures.

Run from src/api:
PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.resident_assistant_browser_check
No SQL, Azure, private data, verifier file or actual model transport is used.
"""

from dataclasses import replace
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright
from test_resident_demo_api import FAKE_PASSWORD, DemoTestCase


def sign_in(page: Page, email: str) -> None:
    page.get_by_label("Email address").fill(email)
    page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("heading", name="Help with your case")).to_be_visible()


def run(browser: Browser, base: str) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: requests.append(request.url))
    page.goto(base)
    expect(page.locator(".assistant")).to_have_count(0)
    sign_in(page, "one@example.com")
    panel = page.locator(".assistant")
    expect(panel).to_contain_text("Advisory only")
    expect(panel).to_contain_text("No AI model is connected")
    select = page.get_by_label("Your question", exact=True)
    select.focus()
    page.keyboard.press("Home")
    page.keyboard.press("Tab")
    expect(page.get_by_role("button", name="Get advice")).to_be_focused()
    page.keyboard.press("Enter")
    expect(page.locator("#assistant-result")).to_contain_text("arranging a survey")
    expect(page.locator("#assistant-result")).not_to_contain_text("Design work")
    expect(page.locator("#assistant-result")).to_contain_text("Your case: Where things are")
    expect(select).to_be_enabled()
    print("PASS keyboard question, own-case status, sources and advisory notice")

    for topic, text in (("documents", "cannot tell you what to send"), ("forms", "Do not guess")):
        select.select_option(topic)
        page.get_by_role("button", name="Get advice").click()
        expect(page.locator("#assistant-result")).to_contain_text(text)
    print("PASS unknown requested documents and non-submitting form guidance")

    page.route("**/demo/assistant", lambda route: route.abort())
    page.get_by_role("button", name="Get advice").click()
    expect(page.locator("#assistant-status")).to_contain_text("could not reach")
    expect(page.locator("#assistant-result")).to_be_empty()
    expect(select).to_be_enabled()
    page.unroute("**/demo/assistant")
    page.get_by_role("button", name="Get advice").click()
    expect(page.locator("#assistant-result")).to_contain_text("Do not guess")
    print("PASS network failure, cleared result and retry")

    pending: dict[str, Any] = {}

    def hold(route: Route) -> None:
        pending["response"] = route.fetch()
        pending["route"] = route

    page.route("**/demo/assistant", hold)
    select.select_option("status")
    page.get_by_role("button", name="Get advice").click()
    expect(page.locator("#assistant-status")).to_have_text("Getting your advice\u2026")
    expect(page.get_by_role("button", name="Get advice")).to_be_disabled()
    page.get_by_role("button", name="Sign out", exact=True).click()
    expect(page.get_by_role("button", name="Sign in", exact=True)).to_be_visible()
    sign_in(page, "two@example.com")
    pending["route"].fulfill(response=pending["response"])
    expect(page.locator("#assistant-result")).to_be_empty()
    page.unroute("**/demo/assistant")
    page.get_by_role("button", name="Get advice").click()
    expect(page.locator("#assistant-result")).to_contain_text("Design work is under way")
    expect(page.locator("#assistant-result")).not_to_contain_text("arranging a survey")
    print("PASS delayed previous-resident response cannot populate next resident panel")

    out = Path("/tmp/ama-469-browser")
    out.mkdir(exist_ok=True)
    page.screenshot(path=str(out / "desktop.png"), full_page=True)
    page.set_viewport_size({"width": 320, "height": 800})
    page.emulate_media(reduced_motion="reduce")
    expect(panel).to_be_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    assert page.evaluate(
        "getComputedStyle(document.documentElement).getPropertyValue('--motion').trim()"
    ) == "0s"
    page.screenshot(path=str(out / "mobile.png"), full_page=True)
    print("PASS 320px reflow and reduced motion")

    page.route(
        "**/demo/assistant",
        lambda route: route.fulfill(
            status=401, content_type="application/json", body='{"error":"Please sign in again."}'
        ),
    )
    page.get_by_role("button", name="Get advice").click()
    expect(page.locator("#signin-error")).to_have_text("Please sign in again.")
    expect(page.locator("#content")).to_be_hidden()
    assert not errors, errors
    assert all(url.startswith(base) for url in requests), requests
    print("PASS expired-session recovery, no script errors or external page requests")
    context.close()


def main() -> None:
    fixture = DemoTestCase()
    fixture.setUp()
    try:
        fixture.app.allowed_hosts = ("127.0.0.1",)
        fixture.reader.rows["C-1"] = replace(
            fixture.reader.rows["C-1"], stage="Survey being booked"
        )
        fixture.reader.rows["C-2"] = replace(
            fixture.reader.rows["C-2"], stage="Design in progress"
        )
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                run(browser, f"http://127.0.0.1:{fixture.app.port}")
            finally:
                browser.close()
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    main()
