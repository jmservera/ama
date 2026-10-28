"""Actual loopback resident chat and callback flows with constructed fixtures only."""

import argparse
import hashlib
import json
import tempfile
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright
from test_resident_chat_api import document_fixture
from test_resident_demo_api import FAKE_PASSWORD, NOW, DemoTestCase
from checks.regulatory_ux_check import AXE_SHA256, scan
from zava_forward.api.resident_demo.agenda import Agenda


def sign_in(page: Page, email: str) -> None:
    page.get_by_label("Email address").fill(email)
    page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("heading", name="Synthetic callbacks", exact=True)).to_be_visible()


def open_chat(page: Page) -> None:
    if not page.locator("#resident-chat").is_visible():
        page.get_by_role("button", name="Chat", exact=True).click()
    expect(page.locator("#assistant-title")).to_be_focused()


def shared_session_checks(
    browser: Browser, base: str, axe: str | None, reports: list[dict[str, Any]]
) -> None:
    context = browser.new_context()
    first = context.new_page()
    second = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    for tab in (first, second):
        tab.on("pageerror", lambda error: errors.append(str(error)))
    context.on("request", lambda request: requests.append(request.url))
    pending: dict[str, Any] = {}

    def hold(route: Route) -> None:
        pending["response"] = route.fetch()
        pending["route"] = route

    try:
        first.goto(base)
        expect(first.locator("#signin")).to_be_visible()
        second.route("**/demo/session", hold, times=1)
        second.goto(base)
        expect(second.locator("#status")).to_have_text("Loading\u2026")
        with first.expect_response("**/demo/login") as login:
            sign_in(first, "one@example.com")
        old_sid = login.value.json()["session_id"]
        pending["route"].fulfill(response=pending["response"])
        expect(second.locator("#signin")).to_be_visible()
        open_chat(first)
        first.locator("#assistant-consent").check()
        first.locator("#assistant-question").fill("my home")
        first.get_by_role("button", name="Get advice").click()
        expect(first.locator("#assistant-result")).to_contain_text("C-1 Test Street")
        first.route("**/demo/assistant", hold)
        first.locator("#assistant-question").fill("my home")
        first.get_by_role("button", name="Get advice").click()
        expect(first.get_by_role("button", name="Get advice")).to_have_attribute(
            "aria-disabled", "true"
        )
        first.keyboard.press("Escape")
        first.locator("#callback-consent").check()
        first.get_by_role("button", name="Check my callbacks").click()
        expect(first.locator("#callback-bookings")).to_contain_text("no reserved")
        with second.expect_response("**/demo/login") as login:
            sign_in(second, "two@example.com")
        new_login = login.value.json()
        assert new_login["session_id"] != old_sid
        expect(first.locator("#signin-error")).to_contain_text("changed in another tab")
        expect(first.locator("#content")).to_be_empty()
        expect(first.locator("#assistant-result")).to_be_empty()
        expect(first.locator("#assistant-consent")).not_to_be_checked()
        assert first.locator("#callback-consent").count() == 0
        pending["route"].fulfill(response=pending["response"])
        first.unroute("**/demo/assistant")
        expect(first.locator("#assistant-result")).to_be_empty()
        open_chat(first)
        scan(first, axe, reports, "shared-browser-old-tab-cleared", "#main, #resident-chat")
        headers = {
            "Origin": base,
            "X-CSRF-Token": new_login["csrf"],
            "X-Resident-Session": old_sid,
        }
        for path, body in (
            ("/demo/assistant", {"question": "my home", "use_record": True}),
            ("/demo/agenda", {"action": "list", "use_record": True}),
        ):
            response = first.request.post(base + path, headers=headers, data=body)
            assert response.status == 409
            assert response.json()["session_changed"]
            assert "C-2 Test Street" not in response.text()
        first.keyboard.press("Escape")
        with first.expect_response("**/demo/login") as login:
            sign_in(first, "two@example.com")
        assert login.value.json()["session_id"] != new_login["session_id"]
        expect(second.locator("#content")).to_be_empty()
        expect(second.locator("#assistant-consent")).not_to_be_checked()
        open_chat(first)
        first.locator("#assistant-consent").check()
        # A late change hint revalidates the cookie, never adopts the message's identity.
        with first.expect_response("**/demo/session"):
            second.evaluate(
                "() => { const c = new BroadcastChannel('resident-demo-session');"
                " c.postMessage('changed'); c.close(); }"
            )
        expect(first.locator("#assistant-consent")).to_be_checked()
        expect(first.locator("#content")).to_be_visible()
        scan(first, axe, reports, "same-resident-new-login-and-late-hint", "#resident-chat")

        # An obsolete view failure must not erase a later successful local login.
        second.route("**/demo/view", hold, times=1)
        second.get_by_label("Email address").fill("one@example.com")
        second.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
        second.get_by_role("button", name="Sign in", exact=True).click()
        expect(second.locator("#status")).to_have_text("Loading your progress\u2026")
        expect(first.locator("#signin")).to_be_visible()
        sign_in(first, "two@example.com")
        expect(second.locator("#signin")).to_be_visible()
        sign_in(second, "one@example.com")
        pending["route"].fulfill(
            status=503, content_type="application/json", body='{"error":"Obsolete failure."}'
        )
        expect(second.locator("#content")).to_contain_text("C-1 Test Street")
        expect(second.locator("#error")).to_be_hidden()
        expect(second.locator("#assistant-consent")).not_to_be_checked()
        scan(second, axe, reports, "stale-session-view-failure-fenced", "#main")

        # A cookie replacement without any tab notification still fails closed.
        sign_in(first, "two@example.com")
        open_chat(first)
        first.locator("#assistant-consent").check()
        first.locator("#assistant-question").fill("my home")
        first.get_by_role("button", name="Get advice").click()
        expect(first.locator("#assistant-result")).to_contain_text("C-2 Test Street")
        csrf = next(
            cookie["value"]
            for cookie in context.cookies()
            if cookie["name"] == "__Host-zfdemo-csrf"
        )
        response = second.request.post(
            base + "/demo/login",
            headers={"Origin": base, "X-CSRF-Token": csrf},
            data={"email": "one@example.com", "password": FAKE_PASSWORD},
        )
        assert response.ok
        first.locator("#assistant-question").fill("my home")
        first.get_by_role("button", name="Get advice").click()
        expect(first.locator("#signin-error")).to_contain_text("Your sign-in changed")
        expect(first.locator("#content")).to_be_empty()
        expect(first.locator("#assistant-result")).to_be_empty()
        expect(first.locator("#assistant-consent")).not_to_be_checked()
        open_chat(first)
        scan(first, axe, reports, "unnotified-cookie-switch-rejected", "#main, #resident-chat")
        assert not errors, errors
        assert all(url.startswith(base) for url in requests), requests
    finally:
        context.close()


def run(browser: Browser, base: str, axe: str | None, out: Path) -> dict[str, Any]:
    # Deliberately different from the demo's explicit Europe/London display/filter zone.
    context = browser.new_context(
        viewport={"width": 1280, "height": 900}, timezone_id="America/New_York", has_touch=True
    )
    page = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    reports: list[dict[str, Any]] = []
    shared_session_checks(browser, base, axe, reports)
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: requests.append(request.url))
    page.goto(base)
    expect(page.get_by_role("button", name="Chat", exact=True)).to_be_visible()
    open_chat(page)
    expect(page.locator("#resident-chat")).to_contain_text("Sign in to ask")
    expect(page.locator("#resident-chat form")).to_be_hidden()
    scan(page, axe, reports, "anonymous", "#resident-chat, #chat-launcher")
    page.keyboard.press("Escape")
    expect(page.locator("#chat-launcher")).to_be_focused()
    expect(page.locator("#resident-chat")).to_be_hidden()
    page.get_by_role("button", name="Chat", exact=True).tap()
    expect(page.locator("#resident-chat")).to_be_visible()
    page.get_by_role("button", name="Close chat", exact=True).tap()
    expect(page.locator("#chat-launcher")).to_be_focused()
    sign_in(page, "one@example.com")
    open_chat(page)
    panel = page.locator("#resident-chat")
    expect(panel).to_contain_text("Advisory only")
    expect(panel).to_contain_text("Each answer says whether AI or rules were used")
    select = page.get_by_label("Your question", exact=True)
    button = page.get_by_role("button", name="Get advice")
    button.click()
    expect(page.locator("#assistant-consent")).to_be_focused()
    expect(page.locator("#assistant-result")).to_be_empty()
    page.locator("#assistant-consent").check()
    select.focus()
    select.select_option("status")
    button.focus()
    page.keyboard.press("Enter")
    expect(page.locator("#assistant-result")).to_contain_text("arranging a survey")
    expect(page.locator("#assistant-result")).not_to_contain_text("Design work")
    expect(page.locator("#assistant-result")).to_contain_text("Your case: Where things are")
    expect(button).to_be_focused()
    expect(page.locator("#assistant-result")).to_contain_text("Summary by rules")
    for topic, text in (
        ("documents", "Survey: Missing"),
        ("forms", "Do not guess"),
        ("consents", "cannot say whether"),
        ("regulations", "retrieved 2026-09-19"),
        ("safety", "has not sent a report"),
    ):
        select.select_option(topic)
        button.click()
        expect(page.locator("#assistant-result")).to_contain_text(text)
    for question in (
        "Which documents are missing from my case?",
        "How do I send the document?",
        "What does my document warning or error mean?",
    ):
        page.locator("#assistant-question").fill(question)
        button.click()
        for text in (
            "Survey: Missing",
            "secure upload link",
            "Page 2 is hard to read",
            "home address does not match your case",
            "file check has not finished",
            "document request R-SURVEY",
            "document D-EPC",
            "not a decision",
            "cannot upload or send",
            "Summary by rules",
        ):
            expect(page.locator("#assistant-result")).to_contain_text(text)
        expect(page.locator("#assistant-result")).not_to_contain_text("C-2 Test Street")
    scan(page, axe, reports, "document-facts", "#resident-chat, #chat-launcher")
    page.set_viewport_size({"width": 320, "height": 900})
    page.evaluate("document.documentElement.style.fontSize = '200%'")
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    document_source = page.locator("#assistant-result li").filter(has_text="document D-EPC").last
    document_source.scroll_into_view_if_needed()
    expect(document_source).to_be_in_viewport()
    assert panel.evaluate("element => element.scrollWidth <= element.clientWidth")
    scan(page, axe, reports, "document-facts-320-text-200", "#resident-chat, #chat-launcher")
    page.screenshot(path=str(out / "document-facts-320-200.png"))
    page.evaluate("document.documentElement.style.fontSize = ''")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.locator("#assistant-question").fill("my home")
    button.click()
    expect(page.locator("#assistant-result")).to_contain_text("C-1 Test Street")
    expect(page.locator("#assistant-result")).not_to_contain_text("C-2 Test Street")
    scan(page, axe, reports, "signed-in-chat", "#resident-chat, #chat-launcher")

    page.route("**/demo/assistant", lambda route: route.abort())
    button.click()
    expect(page.locator("#assistant-status")).to_contain_text("could not reach")
    expect(button).to_be_focused()
    page.unroute("**/demo/assistant")
    page.route(
        "**/demo/assistant",
        lambda route: route.fulfill(
            status=503, content_type="application/json", body='{"error":"Try again later."}'
        ),
    )
    button.press("Enter")
    expect(page.locator("#assistant-status")).to_have_text("Try again later.")
    expect(select).to_be_enabled()
    expect(button).to_be_focused()
    page.unroute("**/demo/assistant")
    select.select_option("status")
    pending: dict[str, Any] = {}

    def hold(route: Route) -> None:
        pending["response"] = route.fetch()
        pending["route"] = route

    page.route("**/demo/assistant", hold)
    page.locator("#assistant-question").fill("  my home?  ")
    button.click()
    expect(button).to_have_attribute("aria-disabled", "true")
    page.locator("#assistant-question").fill("My next question about documents")
    pending["route"].fulfill(response=pending["response"])
    expect(select).to_be_enabled()
    expect(page.locator("#assistant-question")).to_have_value("My next question about documents")
    scan(page, axe, reports, "typed-ahead-draft-preserved", "#resident-chat")
    page.locator("#assistant-question").fill("my home")
    button.click()
    expect(button).to_have_attribute("aria-disabled", "true")
    pending["route"].fulfill(response=pending["response"])
    expect(page.locator("#assistant-question")).to_have_value("")
    summary = page.locator("#account > summary")
    for dismissal in ("Escape", "outside"):
        page.locator("#assistant-question").fill("appointments in the afternoon?")
        button.click()
        expect(button).to_have_attribute("aria-disabled", "true")
        before_agenda = requests.count(base + "/demo/agenda")
        if dismissal == "Escape":
            page.keyboard.press("Escape")
            focus = page.locator("#chat-launcher")
        else:
            summary.focus()
            focus = summary
        expect(panel).to_be_hidden()
        pending["route"].fulfill(response=pending["response"])
        expect(select).to_be_enabled()
        expect(focus).to_be_focused()
        assert requests.count(base + "/demo/agenda") == before_agenda
        scan(page, axe, reports, f"dismissed-appointments-{dismissal}", "#main, #chat-launcher")
        open_chat(page)
        page.get_by_role("button", name="Use the manual callback form").click()
        expect(page.locator("#callback-title")).to_be_focused()
        open_chat(page)
    select.select_option("status")
    before = requests.count(base + "/demo/assistant")
    button.press("Enter")
    expect(page.locator("#assistant-status")).to_have_text("Getting your advice\u2026")
    expect(button).to_have_attribute("aria-disabled", "true")
    expect(button).to_be_focused()
    button.press("Enter")
    # Moving focus out closes the nonmodal overlay rather than hiding a background control.
    summary.focus()
    expect(panel).to_be_hidden()
    pending["route"].fulfill(response=pending["response"])
    expect(select).to_be_enabled()
    expect(summary).to_be_focused()
    assert requests.count(base + "/demo/assistant") == before + 1
    open_chat(page)
    button.click()
    expect(button).to_have_attribute("aria-disabled", "true")
    summary.click()
    page.get_by_role("button", name="Sign out", exact=True).click()
    expect(page.get_by_role("button", name="Sign in", exact=True)).to_be_visible()
    expect(page.locator("#signin-title")).to_be_focused()
    expect(page.locator("#assistant-result")).to_be_empty()
    sign_in(page, "two@example.com")
    pending["route"].fulfill(response=pending["response"])
    expect(page.locator("#assistant-result")).to_be_empty()
    page.unroute("**/demo/assistant")
    open_chat(page)
    expect(page.locator("#assistant-consent")).not_to_be_checked()
    page.locator("#assistant-consent").check()
    button.click()
    expect(page.locator("#assistant-result")).to_contain_text("Design work is under way")
    expect(page.locator("#assistant-result")).not_to_contain_text("arranging a survey")
    select.select_option("documents")
    button.click()
    expect(page.locator("#assistant-result")).to_contain_text("cannot tell you what to send")
    expect(page.locator("#assistant-result")).not_to_contain_text("R-SURVEY")
    expect(page.locator("#assistant-result")).not_to_contain_text("D-EPC")
    select.select_option("appointments")
    button.click()
    expect(panel).to_be_hidden()
    expect(page.locator("#callback-proposals .callback-item")).to_have_count(3)
    expect(page.locator("#callback-title")).to_be_focused()
    expect(page.locator("#callback-consent")).to_be_checked()
    expect(page.locator("#callback-bookings")).to_contain_text("no reserved")
    for period, times in (("morning", ("09:00", "11:00")), ("afternoon", ("14:00", "16:00"))):
        open_chat(page)
        page.locator("#assistant-question").fill(f"appointments in the {period}?")
        button.click()
        expect(panel).to_be_hidden()
        expect(page.locator("#callback-period")).to_have_value(period)
        expect(page.locator("#callback-proposals .callback-item")).to_have_count(2)
        for time in times:
            expect(page.locator("#callback-proposals")).to_contain_text(time)
        other_times = ("14:00", "16:00") if period == "morning" else ("09:00", "11:00")
        for time in other_times:
            expect(page.locator("#callback-proposals")).not_to_contain_text(time)
        expect(page.locator("#callback-title")).to_be_focused()
        scan(page, axe, reports, f"punctuated-{period}-proposals", ".callbacks, #chat-launcher")
    open_chat(page)
    page.locator("#assistant-consent").uncheck()
    expect(page.locator("#assistant-result")).to_be_empty()
    page.get_by_role("button", name="Close chat", exact=True).click()
    expect(page.locator("#chat-launcher")).to_be_focused()

    # Fully independent manual form, real HTTP search/confirm/cancel and stored inventory.
    page.locator("#callback-consent").check()
    page.locator("#callback-period").select_option("any")
    page.locator("#callback-date").fill("2026-10-26")
    page.get_by_role("button", name="Find callback times", exact=True).click()
    expect(page.locator("#callback-proposals .callback-item")).to_have_count(3)
    expect(page.locator("#callback-proposals")).to_contain_text("Nobody will call you")
    expect(page.locator("#callback-proposals")).to_contain_text("09:00")
    expect(page.locator("#callback-proposals")).to_contain_text("UK time")
    book = page.get_by_role("button", name="Book this callback").first
    before = requests.count(base + "/demo/agenda")
    book.click()
    expect(page.locator("#book-callback-0")).to_be_focused()
    assert requests.count(base + "/demo/agenda") == before
    page.locator("#book-callback-0").check()
    book.click()
    expect(page.locator("#callback-bookings")).to_contain_text("Reserved synthetic callback")
    expect(page.locator("#callback-bookings")).to_contain_text("Nobody will call you")
    expect(page.get_by_role("button", name="Check my callbacks")).to_be_focused()
    scan(page, axe, reports, "callback-booked", ".callbacks, #chat-launcher")
    for width in (1280, 390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        page.emulate_media(reduced_motion="reduce")
        for text_size in (100, 200):
            page.evaluate("size => document.documentElement.style.fontSize = size + '%'", text_size)
            open_chat(page)
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            panel_box = panel.bounding_box()
            assert panel_box and panel_box["x"] >= 0 and panel_box["width"] <= width
            page.get_by_role("button", name="Close chat", exact=True).focus()
            box = page.get_by_role("button", name="Close chat", exact=True).bounding_box()
            assert box and 0 <= box["y"] and box["y"] + box["height"] <= 900
            scan(
                page,
                axe,
                reports,
                f"chat-{width}-text-{text_size}",
                "#resident-chat, #chat-launcher",
            )
            page.screenshot(path=str(out / f"chat-{width}-{text_size}.png"))
            page.keyboard.press("Escape")
            expect(page.locator("#chat-launcher")).to_be_focused()
            scan(
                page, axe, reports, f"manual-{width}-text-{text_size}", ".callbacks, #chat-launcher"
            )
        assert (
            page.evaluate(
                "getComputedStyle(document.documentElement).getPropertyValue('--motion').trim()"
            )
            == "0s"
        )
    page.evaluate("document.documentElement.style.fontSize = ''")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.locator("#cancel-callback-0").check()
    page.get_by_role("button", name="Cancel this callback").click()
    expect(page.locator("#callback-status")).to_contain_text("cancelled")
    expect(page.locator("#callback-bookings")).to_contain_text("no reserved")
    page.route(
        "**/demo/agenda",
        lambda route: route.fulfill(
            status=503,
            content_type="application/json",
            body='{"error":"Agenda unavailable. Ask your housing officer."}',
        ),
    )
    page.get_by_role("button", name="Check my callbacks").click()
    expect(page.locator("#callback-status")).to_contain_text("Agenda unavailable")
    page.unroute("**/demo/agenda")
    open_chat(page)
    page.locator("#assistant-consent").check()
    page.route(
        "**/demo/assistant",
        lambda route: route.fulfill(
            status=401, content_type="application/json", body='{"error":"Please sign in again."}'
        ),
    )
    button.click()
    expect(page.locator("#signin-error")).to_have_text("Please sign in again.")
    expect(page.locator("#content")).to_be_hidden()
    expect(page.locator("#resident-chat")).to_be_hidden()
    expect(page.locator("#assistant-result")).to_be_empty()
    expect(page.locator("#chat-launcher")).to_be_visible()
    page.unroute("**/demo/assistant")
    page.route(
        "**/demo/view",
        lambda route: route.fulfill(
            status=503, content_type="application/json", body='{"error":"Try again later."}'
        ),
    )
    page.reload()
    expect(page.locator("#error-title")).to_be_focused()
    expect(page.locator("#chat-launcher")).to_be_visible()
    open_chat(page)
    expect(panel).to_contain_text("Sign in to ask")
    scan(page, axe, reports, "page-error-help", "#resident-chat, #chat-launcher")
    page.get_by_role("button", name="Use the manual callback form").click()
    expect(page.locator("#retry")).to_be_focused()
    scan(page, axe, reports, "page-error-manual-retry-focus", "#main, #chat-launcher")
    page.route("**/demo/session", hold)
    page.locator("#retry").click()
    expect(page.locator("#status")).to_have_text("Loading\u2026")
    open_chat(page)
    page.get_by_role("button", name="Use the manual callback form").click()
    expect(page.locator("#chat-launcher")).to_be_focused()
    scan(page, axe, reports, "loading-manual-launcher-focus", "#main, #chat-launcher")
    pending["route"].fulfill(response=pending["response"])
    expect(page.locator("#error-title")).to_be_focused()
    assert not errors, errors
    assert all(url.startswith(base) for url in requests), requests
    result = dict(
        scans=reports,
        axe_status="executed" if axe else "Not run",
        browser=browser.version,
        keyboard="Passed engineering assertions",
        human_and_assistive_technology="Not run; pending acceptance",
        zoom="320 CSS px is 400%-equivalent reflow from 1280; not native browser zoom",
        text_resize="root font-size 200%, not device scale",
        time_zone="America/New_York browser; Europe/London app dates",
        console_errors=errors,
        external_requests=[],
    )
    context.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    out = args.out or Path(tempfile.mkdtemp(prefix="ama-520-browser-"))
    out.mkdir(exist_ok=True)
    axe = None
    if args.axe:
        raw = args.axe.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
        axe = raw.decode()
    fixture = DemoTestCase()
    fixture.setUp()
    try:
        fixture.app.allowed_hosts = ("127.0.0.1",)
        fixture.reader.rows["C-1"] = replace(
            fixture.reader.rows["C-1"], stage="Survey being booked", documents=document_fixture()
        )
        fixture.reader.rows["C-2"] = replace(fixture.reader.rows["C-2"], stage="Design in progress")
        with tempfile.TemporaryDirectory(prefix="ama-520-agenda-") as temp:
            fixture.app.agenda = Agenda.create(
                Path(temp) / "agenda.sqlite",
                [
                    (NOW + timedelta(days=1, hours=h), NOW + timedelta(days=1, hours=h, minutes=30))
                    for h in (-3, -1, 2, 4)
                ],
            )
            with sync_playwright() as pw:
                browser = pw.chromium.launch()
                try:
                    result = run(browser, f"http://127.0.0.1:{fixture.app.port}", axe, out)
                finally:
                    browser.close()
        (out / "report.json").write_text(json.dumps(result, indent=2) + "\n")
        print(f"PASS resident chat and callback flows; axe {result['axe_status']}; evidence {out}")
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    main()
