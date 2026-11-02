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
SCREENS = (
    ("safety@example.test", "Building safety referral queue"),
    ("sam@example.test", "Repairs and hazard triage"),
)
EXPECTED = (
    "Pending receipt. Follow-up owner:",
    "Pending acceptance. Follow-up owner:",
    "owns the accepted scope",
    "Legacy referral with no recorded send time",
    "No referral sent.",
    "Decided by",
    "Evidence: SYN-RELEASE-227",
    "No authoritative decision evidence is recorded; do not rely on this release.",
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


def check_accessibility(page: Page, story: str) -> None:
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    text = evidence.inner_text()
    check(f"{story} states are text, no write controls",
          evidence.locator("button, form, input, select, textarea").count() == 0)
    check(f"{story} boundary text names what the screen does not do", BOUNDARY in text)
    check(f"{story} every hazard is listed (SA-007)", all(f"H-{n}" in text for n in range(1, 7)))
    for phrase in EXPECTED:
        check(f"{story} shows: {phrase}", phrase in text)
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
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        print(f"SKIP {story} axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    page.evaluate(raw.decode())
    result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
      runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
    check(f"{story} axe finds no violations: {[v['id'] for v in result['violations']]}",
          not result["violations"])
    print(f"INFO {story} axe incomplete: {[i['id'] for i in result['incomplete']]}")


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for email, screen in SCREENS:
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
                    page.on("request", lambda r: writes.append(r.url) if r.method == "POST" else None)
                    page.get_by_role("link", name="Specialist screens", exact=True).click()
                    page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                    page.get_by_role("link", name=screen, exact=True).click()
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


if __name__ == "__main__":
    main(run_browser, safety_data)
