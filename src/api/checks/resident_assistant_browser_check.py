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


def run(browser: Browser, base: str, axe: str | None, out: Path) -> dict[str, Any]:
    # Deliberately different from the demo's explicit Europe/London display/filter zone.
    context = browser.new_context(
        viewport={"width": 1280, "height": 900}, timezone_id="America/New_York", has_touch=True
    )
    page = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    reports: list[dict[str, Any]] = []
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
        ("documents", "Survey: Missing"), ("forms", "Do not guess"),
        ("consents", "cannot say whether"), ("regulations", "retrieved 2026-09-19"),
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
            "Survey: Missing", "secure upload link", "Page 2 is hard to read",
            "home address does not match your case", "file check has not finished",
            "document request R-SURVEY", "document D-EPC", "not a decision",
            "cannot upload or send", "Summary by rules",
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
    before = requests.count(base + "/demo/assistant")
    button.press("Enter")
    expect(page.locator("#assistant-status")).to_have_text("Getting your advice\u2026")
    expect(button).to_have_attribute("aria-disabled", "true")
    expect(button).to_be_focused()
    button.press("Enter")
    # Moving focus out closes the nonmodal overlay rather than hiding a background control.
    summary = page.locator("#account > summary")
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
    open_chat(page)
    page.locator("#assistant-consent").uncheck()
    expect(page.locator("#assistant-result")).to_be_empty()
    page.get_by_role("button", name="Close chat", exact=True).click()
    expect(page.locator("#chat-launcher")).to_be_focused()

    # Fully independent manual form, real HTTP search/confirm/cancel and stored inventory.
    page.locator("#callback-consent").check()
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
            scan(page, axe, reports, f"chat-{width}-text-{text_size}", "#resident-chat, #chat-launcher")
            page.screenshot(path=str(out / f"chat-{width}-{text_size}.png"))
            page.keyboard.press("Escape")
            expect(page.locator("#chat-launcher")).to_be_focused()
            scan(page, axe, reports, f"manual-{width}-text-{text_size}", ".callbacks, #chat-launcher")
        assert page.evaluate(
            "getComputedStyle(document.documentElement).getPropertyValue('--motion').trim()"
        ) == "0s"
    page.evaluate("document.documentElement.style.fontSize = ''")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.locator("#cancel-callback-0").check()
    page.get_by_role("button", name="Cancel this callback").click()
    expect(page.locator("#callback-status")).to_contain_text("cancelled")
    expect(page.locator("#callback-bookings")).to_contain_text("no reserved")
    page.route(
        "**/demo/agenda",
        lambda route: route.fulfill(
            status=503, content_type="application/json",
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
    assert not errors, errors
    assert all(url.startswith(base) for url in requests), requests
    result = dict(
        scans=reports, axe_status="executed" if axe else "Not run",
        browser=browser.version, keyboard="Passed engineering assertions",
        human_and_assistive_technology="Not run; pending acceptance",
        zoom="320 CSS px is 400%-equivalent reflow from 1280; not native browser zoom",
        text_resize="root font-size 200%, not device scale",
        time_zone="America/New_York browser; Europe/London app dates",
        console_errors=errors, external_requests=[],
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
        fixture.reader.rows["C-2"] = replace(
            fixture.reader.rows["C-2"], stage="Design in progress"
        )
        with tempfile.TemporaryDirectory(prefix="ama-520-agenda-") as temp:
            fixture.app.agenda = Agenda.create(
                Path(temp) / "agenda.sqlite",
                [(NOW + timedelta(days=1, hours=h), NOW + timedelta(days=1, hours=h, minutes=30))
                 for h in (-3, -1, 2, 4)],
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
