"""Resident case summary, section navigation and sign-in loading UI check.

Run from src/api: PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.resident_summary_browser_check
Uses the real local HTTP app and synthetic rows. No SQL, Azure or model is used,
so the AI summary shows its documented rules fallback (the AI success path is not run here).
"""

from __future__ import annotations

import threading
from datetime import timedelta

from playwright.sync_api import Page, Route, expect, sync_playwright
from test_resident_demo_api import FAKE_PASSWORD, KEY, NOW, Clock, FakeReader, make_row
from zava_forward.core import resident_showcase as rs

from zava_forward.api.resident_demo import app as demo

ORDER = [
    "sec-summary",
    "sec-status",
    "sec-actions",
    "sec-timeline",
    "sec-documents",
    "sec-funding",
    "sec-help",
    "sec-unavailable",
]


def check(page: Page, base: str) -> None:
    page.goto(base)
    page.get_by_label("Email address").fill("one@example.com")

    def slow_login(route: Route) -> None:
        page.wait_for_timeout(300)
        route.continue_()

    page.route("**/demo/login", slow_login)
    page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.locator("#signin")).to_be_hidden()
    expect(page.locator("#status")).to_contain_text("Signing you in")
    expect(page.locator("#main")).to_have_attribute("aria-busy", "true")
    expect(page.locator("#account")).to_be_visible()
    expect(page.locator("#main")).not_to_have_attribute("aria-busy", "true")

    ids = page.evaluate(
        "[...document.querySelectorAll('#content section[id^=sec-]')].map(e => e.id)"
    )
    assert [i for i in ids if i in ORDER] == ORDER, ids

    expect(page.locator("#page-nav")).to_have_attribute("aria-label", "Page sections")
    assert page.locator("#page-nav svg.icon").count() >= 8
    assert page.locator("#page-nav").evaluate("e => getComputedStyle(e).position") == "sticky"
    page.locator("#page-nav a[href='#sec-documents']").click()
    expect(page.locator("#page-nav a[href='#sec-documents']")).to_have_attribute(
        "aria-current", "location"
    )
    expect(page.locator("#sec-timeline li[aria-current=step]")).to_have_count(1)

    expect(page.locator("#sec-summary")).to_contain_text("Summary by rules. Not an instruction.")
    expect(page.locator("#sec-summary a[href='#sec-status']")).to_be_visible()

    page.locator("#summary-ai-button").click()
    expect(page.locator("#summary-ai-consent")).to_be_focused()
    expect(page.locator("#summary-ai-consent")).to_have_attribute("aria-invalid", "true")
    page.locator("#summary-ai-consent").check()
    page.locator("#summary-ai-button").click()
    expect(page.locator("#summary-status")).to_contain_text("AI summary is not available right now")
    expect(page.locator("#sec-summary")).to_contain_text("Summary by rules. Not an instruction.")
    page.locator("#summary-ai-consent").uncheck()
    expect(page.locator("#summary-status")).to_contain_text("stopped")
    expect(page.locator("#summary-status")).to_have_attribute("role", "status")

    for width in (320, 390, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width

    page.emulate_media(reduced_motion="reduce")
    page.reload()
    assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"


def main() -> None:
    clock = Clock()
    reader = FakeReader([make_row("C-1", "one@example.com", stage="Survey booked")])
    expiry = NOW + timedelta(hours=6)
    app = demo.ResidentDemo(
        reader,
        rs.build_identity_map(reader.list_rows(), NOW),
        rs.PasswordVerifier(rs.make_verifier(FAKE_PASSWORD, n=2**14)),
        rs.SessionCodec(KEY, expiry, clock),
        rs.LoginLimiter(clock=clock),
        ("127.0.0.1",),
        expiry,
        port=0,
        clock=clock,
    )
    server = demo.serve(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                check(page, f"http://127.0.0.1:{app.port}")
                assert not errors, errors
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    print("PASS resident summary, section navigation and sign-in loading checks")


if __name__ == "__main__":
    main()
