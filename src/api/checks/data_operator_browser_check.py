"""Browser evidence for the read-only data steward and operator screen (#229)."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import check, main
from checks.role_screens_fixtures import synthetic_data

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
SCREEN = "Data steward and operator view"
EXPECTED = (
    "D; source SYN-STOCK-A v1",
    "C; source SYN-STOCK-B v2",
    "Unresolved",
    "Eligibility",
    "Not selected. No latest-wins or silent correction is applied.",
    "Preserved unchanged in the table above",
    "Returned",
    "Reopened",
    "SYN missing roof reference",
    "SYN-EVENT-229",
    "not an operational audit trail",
    "Integration run and queue state",
    "No interface run record is supplied to this screen.",
    "Stock query SQ-1 remains unresolved.",
    "No handoff is recorded for this home.",
)


def operator_data() -> dict[str, Any]:
    data = synthetic_data()
    case = data["cases"][0]
    owner = data["staff"][0]
    first = case["stock_reconciliation"][0]
    case["stock_reconciliation"].append(dict(first, id="SQ-2", field="age"))
    case["stock_reconciliation_events"] = [dict(
        id="SQE-1", query_id="SQ-2", status="Withdrawn", at="2026-10-28T10:00:00Z",
        recorded_by=owner, reason="SYN duplicate query", evidence="SYN-EVENT-229")]
    case["returns"].append(dict(case["returns"][0], reopened=True, reason="SYN reopened for evidence"))
    case["returns"].append(dict(case["returns"][0], event_type="advance", reason="SYN forward move"))
    return data


def check_accessibility(page: Page) -> bool:
    """Return True when the axe scan ran, False when it was skipped."""
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    text = evidence.text_content() or ""
    check("no write controls in the evidence region",
          evidence.locator("button, form, input, select, textarea").count() == 0)
    check("states that nothing is replayed, corrected, resolved or retried",
          "does not replay, correct, resolve or retry anything" in text)
    for phrase in EXPECTED:
        check(f"shows: {phrase}", phrase in text)
    check("forward moves are not shown as returns", "SYN forward move" not in text)
    check("source A is shown for both queries (SQ-1, SQ-2)", text.count("SYN-STOCK-A") >= 2)
    check("source B is shown for both queries (SQ-1, SQ-2)", text.count("SYN-STOCK-B") >= 2)
    check("withdrawn query is shown as withdrawn, not removed", "Withdrawn" in text)
    regions = evidence.locator('div.table-scroll[role="region"]')
    expected = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check("at least four table regions", len(expected) >= 4)
    check("every table region has a label", all(expected))
    check("every table region is focusable and has a caption", regions.evaluate_all(
        "els => els.every(el => el.tabIndex === 0 && el.querySelector('caption'))"))
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    reached: list[str] = []
    for _ in range(120):
        page.keyboard.press("Tab")
        label = page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''")
        if label in expected and label not in reached:
            reached.append(label)
        if len(reached) == len(set(expected)):
            break
    check(f"Tab reaches every table region: {reached}", len(reached) == len(set(expected)))
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        print("SKIP axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return False
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    page.evaluate(raw.decode())
    result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
      runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
    check(f"axe 4.10.3 finds no violations in main at 1280px: {[v['id'] for v in result['violations']]}",
          not result["violations"])
    print(f"INFO axe incomplete: {[i['id'] for i in result['incomplete']]}")
    return True


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            try:
                page = context.new_page()
                errors: list[str] = []
                writes: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(base + "/app")
                page.locator("#email").fill("pam@example.test")
                page.locator("#pw").fill("synthetic-check")
                page.locator("button[type=submit]").click()
                page.locator("#nav").wait_for()
                # Registered after sign-in so the sign-in POST is excluded; any later
                # method other than a safe read counts as a write.
                page.on("request", lambda r: writes.append(f"{r.method} {r.url}")
                        if r.method not in ("GET", "HEAD", "OPTIONS") else None)
                page.get_by_role("link", name="Specialist screens", exact=True).click()
                page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                page.get_by_role("link", name=SCREEN, exact=True).click()
                page.locator('a.item[href*="case=ZF-1"]').click()
                page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
                axe_ran = check_accessibility(page)
                for width in (320, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    check(f"reflow {width}px",
                          page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
                check(f"made no writes: {writes}", not writes)
                check(f"no JavaScript errors: {errors}", not errors)
                print("RESULT PASS (axe scan ran)" if axe_ran
                      else "RESULT PARTIAL: axe scan SKIPPED, no automated WCAG evidence")
            finally:
                context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, operator_data)
