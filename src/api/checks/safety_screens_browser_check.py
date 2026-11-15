"""Browser evidence for the read-only Building safety and hazard triage screens (#227)."""

from __future__ import annotations

import copy
import hashlib
import os
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import check, main
from checks.role_screens_fixtures import synthetic_data

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
SKIPPED: list[str] = []
SCREENS = (
    ("safety@example.test", "Building safety referral queue", "#/role/building_safety_lead"),
    ("sam@example.test", "Repairs and hazard triage", "#/role/repairs"),
)
EXPECTED = (
    "Every referral, clock, and stop-work state is written as words first",
    "Pending receipt. Follow-up owner:",
    "Pending acceptance. Follow-up owner:",
    "owns the accepted scope",
    "Legacy referral with no recorded send time",
    "No referral sent.",
    "Confirmed: Stop-work indicator: released.",
    "Decided by",
    "Evidence: SYN-RELEASE-227",
    "Action needed: Stop-work indicator: released.",
    "No authoritative decision evidence is recorded; do not rely on this release.",
    "Action needed: Stop-work indicator: retrofit work is paused.",
    "Release needs an authorised human decision.",
    "SYN-SOURCE-5",
)
BOUNDARY = "does not classify hazards, set clocks, close hazards or authorise work"


def safety_data() -> dict[str, Any]:
    data = synthetic_data()
    case = data["cases"][0]
    owner, destination = data["staff"][0], data["staff"][3]
    base = copy.deepcopy(case["hazards"][0])
    base.update(sender=owner, destination=destination, owner=owner["name"], referral_version=1,
                aware_at="2026-10-27T08:00:00Z", response_due_at=None, responded_at=None,
                sent_at="2026-10-27T08:05:00Z", received_at=None, accepted_at=None,
                referred="SYN-REFERRAL-227", state="Sent")
    base["hold"] = dict(scope="Home", case_id=case["id"], status="Active", decision=None)
    items = [copy.deepcopy(base) for _ in range(6)]
    for index, item in enumerate(items, 1):
        item["source"] = f"SYN-SOURCE-{index}"
    items[1].update(received_at="2026-10-27T09:00:00Z", state="Received", follow_up=owner)
    items[2].update(received_at="2026-10-27T09:00:00Z", accepted_at="2026-10-27T10:00:00Z",
                    accepted_by=destination, state="Accepted")
    items[3].update(sent_at=None, state="Referred")
    items[4].update(sent_at=None, referred=None, state="Open")
    decision = dict(actor=destination, at="2026-10-27T11:00:00Z", reason="SYN lawful release",
                    evidence="SYN-RELEASE-227")
    items[2]["hold"] = dict(base["hold"], status="Released", decision=decision)
    items[5]["hold"] = dict(base["hold"], status="Released", decision=None)
    case["hazards"] = items
    return data


def set_panel_rendering(page: Page, rendered: bool) -> None:
    """Panels use content-visibility: auto; render them all to read or scan every panel."""
    page.evaluate(
        """rendered => document.querySelectorAll('.screen-record').forEach(el => rendered
          ? el.style.setProperty('content-visibility', 'visible', 'important')
          : el.style.removeProperty('content-visibility'))""",
        rendered,
    )


def scan_axe(page: Page, story: str) -> None:
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        SKIPPED.append(story)
        print(f"SKIPPED {story} axe scan (not a pass): set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    set_panel_rendering(page, True)
    try:
        page.evaluate(raw.decode())
        result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
    finally:
        set_panel_rendering(page, False)
    check(f"{story} axe (main only, 1280px) finds no violations: {[v['id'] for v in result['violations']]}",
          not result["violations"])
    print(f"INFO {story} axe incomplete: {[i['id'] for i in result['incomplete']]}")


def check_accessibility(page: Page, story: str) -> None:
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    set_panel_rendering(page, True)
    try:
        text = evidence.inner_text()
    finally:
        set_panel_rendering(page, False)
    check(f"{story} states are text, no write controls",
          evidence.locator("button, form, input, select, textarea").count() == 0)
    check(f"{story} boundary text names what the screen does not do", BOUNDARY in text)
    check(f"{story} every hazard is listed (SA-007)", all(f"H-{n}" in text for n in range(1, 7)))
    for phrase in EXPECTED:
        check(f"{story} shows: {phrase}", phrase in text)
    jump_nav = evidence.get_by_role("navigation", name="Sections on this screen", exact=True)
    jump_links = jump_nav.locator("a[data-jump]")
    check(
        f"{story} jump links have >=24px height and underline cue",
        jump_links.count() == 4
        and jump_links.evaluate_all(
            """els => els.every(el => el.getBoundingClientRect().height >= 24
              && getComputedStyle(el).textDecorationLine.includes('underline'))"""
        ),
    )
    before_hash = page.evaluate("() => location.hash")
    restart_link = jump_nav.get_by_role("link", name="Go to Retrofit pause and restart decision", exact=True)
    restart_link.focus()
    page.keyboard.press("Enter")
    check(
        f"{story} Enter on jump link focuses section heading without routing away",
        page.evaluate("() => ({id: document.activeElement?.id, hash: location.hash})")
        == {"id": "hazard-restart-heading", "hash": before_hash},
    )
    check(f"{story} no contact links", evidence.locator('a[href^="tel:"], a[href^="mailto:"]').count() == 0)
    regions = evidence.locator('div.table-scroll[role="region"]')
    expected = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check(f"{story} tables are labelled focusable regions with captions",
          len(expected) == 2 and regions.evaluate_all(
              "els => els.every(el => el.tabIndex === 0 && el.querySelector('caption'))"))
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    reached: list[str] = []
    for _ in range(80):
        page.keyboard.press("Tab")
        label = page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''")
        if label in expected and label not in reached:
            reached.append(label)
        if len(reached) == len(expected):
            break
    check(f"{story} Tab reaches every table region: {reached}", len(reached) == len(expected))
    scan_axe(page, story)


QUEUE_HEADINGS = ("Home and item", "Aware at", "Source", "Destination", "Sent", "Received", "Accepted",
                  "State", "Follow-up", "Pause status")
QUEUE_EXPECTED = ("Pending receipt. Follow-up owner:", "Pending acceptance. Follow-up owner:",
                  "No referral sent.", "SYN-SOURCE-5", "Released")
SIMULATOR = ("simulat", "impersonat", "view as", "switch role", "act as")


def check_queue(page: Page, story: str) -> None:
    panel = page.locator("section.screen-record", has=page.get_by_role("heading", name="Hazard referrals across this page of homes"))
    panel.wait_for()
    table = panel.get_by_role("table", name="Hazard referrals by home", exact=True)
    text = panel.inner_text()
    head = table.locator("thead th").all_inner_texts()
    check(f"{story} queue has awareness, source, destination and separate sent, received, accepted columns",
          all(name in head for name in QUEUE_HEADINGS))
    check(f"{story} queue lists every hazard of the home (SA-007)", all(f"ZF-1 H-{n}" in text for n in range(1, 7)))
    for phrase in QUEUE_EXPECTED:
        check(f"{story} queue shows: {phrase}", phrase in text)
    check(f"{story} queue says it is not a portfolio total", "not a portfolio total" in text)
    check(f"{story} queue has no write controls",
          panel.locator("button, form, input, select, textarea").count() == 0)
    main_text = page.locator("main").inner_text().lower()
    check(f"{story} no role simulator in the view", not any(term in main_text for term in SIMULATOR))
    region = panel.locator('div.table-scroll[role="region"]')
    check(f"{story} queue table is a labelled focusable region",
          region.get_attribute("aria-label") == "Hazard referrals by home" and region.evaluate("el => el.tabIndex === 0"))
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    reached = False
    for _ in range(80):
        page.keyboard.press("Tab")
        if page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''") == "Hazard referrals by home":
            reached = True
            break
    check(f"{story} Tab reaches the queue table", reached)
    scan_axe(page, f"{story} cross-home table")


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for email, screen, alias_hash in SCREENS:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                try:
                    page = context.new_page()
                    errors: list[str] = []
                    writes: list[str] = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.goto(base + "/app")
                    page.locator("#email").fill(email)
                    page.locator("#pw").fill("synthetic-check")
                    page.locator("button[type=submit]").click()
                    page.locator("#nav").wait_for()
                    page.on("request", lambda r: writes.append(r.url) if r.method not in ("GET", "HEAD", "OPTIONS") else None)
                    page.goto(base + "/app" + alias_hash)
                    page.get_by_role("heading", name=screen, exact=True).wait_for()
                    check_queue(page, screen)
                    page.locator('a.item[href*="case=ZF-1"]').click()
                    page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
                    check_accessibility(page, screen)
                    for width in (320, 1280):
                        page.set_viewport_size({"width": width, "height": 900})
                        check(f"{screen} reflow {width}px",
                              page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
                    check(f"{screen} made no writes: {writes}", not writes)
                    check(f"{screen} has no JavaScript errors: {errors}", not errors)
                finally:
                    context.close()
        finally:
            browser.close()
    if SKIPPED:
        print(f"PARTIAL: axe scan SKIPPED for {SKIPPED}; automated evidence is incomplete")


if __name__ == "__main__":
    main(run_browser, safety_data)
