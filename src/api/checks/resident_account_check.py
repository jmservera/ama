"""Focused account UI check over the real local HTTP app and synthetic test rows.

Run from src/api: PYTHONPATH=tests python -m checks.resident_account_check
No SQL, Azure, private data or stored credentials are used.
"""

from __future__ import annotations

import threading
from datetime import timedelta
from typing import TypedDict

from playwright.sync_api import Browser, Page, expect, sync_playwright
from test_resident_demo_api import (
    FAKE_PASSWORD,
    KEY,
    NOW,
    Clock,
    FakeReader,
    make_row,
)
from zava_forward.core import resident_showcase as rs

from zava_forward.api.resident_demo import app as demo

LONG_EMAIL = "a" * 64 + "@example.com"


class Bounds(TypedDict):
    x: float
    y: float
    width: float
    height: float


def sign_in(page: Page, email: str) -> None:
    page.get_by_label("Email address").fill(email)
    page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.locator("#account")).to_be_visible()
    expect(page.locator("#account-email")).to_have_text(email)


def check_browser(browser: Browser, base: str, clock: Clock) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        page.goto(base)
        expect(page.locator("#signin")).to_be_visible()
        expect(page.locator("#account")).to_be_hidden()
        expect(page.locator("#account-email")).to_be_empty()
        sign_in(page, "one@example.com")
        expect(page.locator("#content")).to_contain_text("C-1 Test Street")
        expect(page.locator("#content")).not_to_contain_text("C-2")
        summary = page.locator("#account > summary")
        expect(summary).to_have_accessible_name("Your account")
        summary.focus()
        summary.press("Enter")
        expect(page.get_by_role("button", name="Sign out", exact=True)).to_be_visible()
        expect(page.locator("#account")).to_have_attribute("open", "")
        summary.press("Tab")
        expect(page.locator("#signout")).to_be_focused()
        page.keyboard.press("Escape")
        expect(summary).to_be_focused()
        expect(page.locator("#account")).not_to_have_attribute("open", "")
        summary.press("Space")
        expect(page.locator("#signout")).to_be_visible()
        page.locator("h1").click()
        expect(page.locator("#account")).not_to_have_attribute("open", "")
        page.reload()
        expect(page.locator("#account")).to_be_visible()
        expect(page.locator("#account-email")).to_have_text("one@example.com")
        summary.click()
        page.locator("#signout").focus()
        page.keyboard.press("Enter")
        expect(page.locator("#signin-title")).to_be_focused()
        expect(page.locator("#status")).to_have_text("You have signed out.")
        expect(page.locator("#account")).to_be_hidden()
        expect(page.locator("#account-email")).to_be_empty()
        expect(page.locator("#content")).to_be_empty()
        assert page.request.get(base + "/demo/view").status == 401
        print(
            "PASS anonymous, own identity, reload, keyboard, dismissal and logout focus/revocation"
        )

        sign_in(page, "two@example.com")
        expect(page.locator("#content")).to_contain_text("C-2 Test Street")
        assert "one@example.com" not in page.locator("body").inner_text()
        summary.click()
        page.route("**/demo/logout", lambda route: route.fulfill(status=503, body="{}"))
        page.locator("#signout").click()
        expect(page.locator("#error-title")).to_be_focused()
        expect(page.locator("#error-text")).to_contain_text("could not confirm")
        expect(page.locator("#account")).to_be_hidden()
        expect(page.locator("#account-email")).to_be_empty()
        expect(page.locator("#content")).to_be_hidden()
        page.unroute("**/demo/logout")
        page.get_by_role("button", name="Try again").click()
        expect(page.locator("#account")).to_be_visible()
        summary.click()
        page.locator("#signout").click()
        expect(page.locator("#signin")).to_be_visible()
        print("PASS second identity, failed logout privacy/focus and retry")

        sign_in(page, LONG_EMAIL)
        for width in (320, 390, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            page.emulate_media(reduced_motion="reduce")
            summary.click()
            panel = page.locator(".account-panel")
            expect(panel).to_be_visible()
            bounds: Bounds = panel.evaluate(
                "(el) => {const r = el.getBoundingClientRect(); "
                "return {x:r.x,y:r.y,width:r.width,height:r.height};}"
            )
            assert bounds["x"] >= 0 and bounds["x"] + bounds["width"] <= width
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            header = page.locator(".top").bounding_box()
            trigger = summary.bounding_box()
            assert header and trigger
            assert abs(trigger["x"] + trigger["width"] - (width - 16)) <= 1
            assert trigger["y"] >= header["y"]
            assert trigger["height"] >= 44
            assert (
                page.locator(":root").evaluate(
                    "(el) => getComputedStyle(el).getPropertyValue('--motion').trim()"
                )
                == "0s"
            )
            page.keyboard.press("Escape")
            expect(summary).to_be_focused()
        print("PASS long-email account panel at 320/390/1280px, top-right and reduced motion")

        clock.now += rs.SESSION_SECONDS + 1
        page.reload()
        expect(page.locator("#signin")).to_be_visible()
        expect(page.locator("#account")).to_be_hidden()
        expect(page.locator("#account-email")).to_be_empty()
        expect(page.locator("#content")).to_be_hidden()
        assert not errors, errors
        print("PASS expired-session identity hiding and no JavaScript errors")
    finally:
        context.close()


def main() -> None:
    clock = Clock()
    reader = FakeReader(
        [
            make_row("C-1", "one@example.com"),
            make_row("C-2", "two@example.com"),
            make_row("C-3", LONG_EMAIL),
        ]
    )
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
                base = f"http://127.0.0.1:{app.port}"
                with browser.new_context() as context:
                    assert context.request.get(base + "/healthz").status == 200
                check_browser(browser, base, clock)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
