"""Browser evidence for the read-only data steward and operator screen (#229)."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from playwright.sync_api import Page, Route, sync_playwright

from checks import data_operator_ai_state as ai
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
    "SYN missing roof reference",
    "SYN-EVENT-229",
    "not an operational audit trail",
    "Integration run and queue state",
    "No interface run record is supplied to this screen.",
    "Stock query SQ-1 remains unresolved.",
    "No handoff is recorded for this home.",
)


PAGE_EXPECTED = (
    "not a portfolio total",
    "no winning source is selected",
    "does not establish that none exists",
    "SYN-STOCK-A v1",
    "SYN-STOCK-B v2",
    "Unresolved",
    "Withdrawn",
    "Returned",
    "SYN missing roof reference",
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
    return ai.add_ai_records(data)


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
    returns = evidence.get_by_role("region", name="Recorded returns and reopens", exact=True)
    returns_text = returns.text_content() or ""
    for phrase in ("Returned", "Reopened", "SYN missing roof reference", "SYN reopened for evidence"):
        check(f"returns table shows: {phrase}", phrase in returns_text)
    conflicts = evidence.get_by_role(
        "region", name="Source conflicts with both values and source details", exact=True)
    conflicts_text = conflicts.text_content() or ""
    for phrase in ("SYN-STOCK-A", "SYN-STOCK-B", "Unresolved"):
        check(f"conflict table shows: {phrase}", phrase in conflicts_text)
    check("source A is shown for both queries (SQ-1, SQ-2)", text.count("SYN-STOCK-A") >= 2)
    check("source B is shown for both queries (SQ-1, SQ-2)", text.count("SYN-STOCK-B") >= 2)
    check("withdrawn query is shown as withdrawn, not removed", "Withdrawn" in text)
    regions = evidence.locator('div.table-scroll[role="region"]')
    expected = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check("at least four table regions", len(expected) >= 4)
    check("every table region has a label", all(expected))
    check("every table region is focusable and has a caption", regions.evaluate_all(
        "els => els.every(el => el.tabIndex === 0 && el.querySelector('caption'))"))
    tab_to_regions(page, expected)
    return scan_axe(page, "per-home view")


def tab_to_regions(page: Page, expected: list[str]) -> None:
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


def scan_axe(page: Page, view: str) -> bool:
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        print("SKIP axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        if os.environ.get("ZF_AXE_REQUIRED") == "1":
            raise AssertionError("axe scan skipped but ZF_AXE_REQUIRED=1")
        return False
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    page.evaluate(raw.decode())
    result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
      runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
    check(f"axe 4.10.3 finds no violations in main at 1280px, {view}: {[v['id'] for v in result['violations']]}",
          not result["violations"])
    print(f"INFO axe incomplete: {[i['id'] for i in result['incomplete']]}")
    return True


def check_page_queue(page: Page) -> bool:
    """Page-level queue shown before any home is selected."""
    page.get_by_role("heading", name="Conflict and return queue across this page of homes", exact=True).wait_for()
    main = page.locator("section.screen-record").filter(
        has=page.get_by_role("heading", name="Conflict and return queue across this page of homes", exact=True))
    text = main.text_content() or ""
    check("page queue has no write controls", main.locator("button, form, input, select, textarea").count() == 0)
    for phrase in PAGE_EXPECTED:
        check(f"page queue shows: {phrase}", phrase in text)
    check("page queue shows both sources for both queries",
          text.count("SYN-STOCK-A") >= 2 and text.count("SYN-STOCK-B") >= 2)
    check("page queue lists the reopen with its reason", "Reopened" in text and "SYN reopened for evidence" in text)
    check("forward moves are not shown as returns in the page queue", "SYN forward move" not in text)
    labels = main.locator('div.table-scroll[role="region"]').evaluate_all(
        "els => els.map(el => el.getAttribute('aria-label'))")
    check(f"page queue has both labelled table regions: {labels}",
          "Source conflicts by home with both values" in labels and "Returns and reopens by home" in labels)
    tab_to_regions(page, labels)
    return scan_axe(page, "page-level queue")


MODEL_PATHS = ("/api/ai", "/api/assistants", "/api/chat")
REGISTER_LINK = "Open the exception register"


def open_screen(page: Page) -> None:
    page.get_by_role("link", name="Specialist screens", exact=True).click()
    page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
    page.get_by_role("link", name=SCREEN, exact=True).click()
    page.get_by_role("link", name=REGISTER_LINK, exact=True).wait_for()


def register_panel(page: Page) -> Any:
    return page.locator("section.screen-record").filter(
        has=page.get_by_role("heading", name="Exception register", exact=True))


def open_register_by_keyboard(page: Page) -> Any:
    link = page.get_by_role("link", name=REGISTER_LINK, exact=True)
    link.focus()
    check("the register link is keyboard focusable", link.evaluate("el => document.activeElement === el"))
    page.keyboard.press("Enter")
    link.wait_for(state="detached")
    return register_panel(page)


def row_text(panel: Any, record_id: str) -> str:
    rows = panel.locator("tr").filter(has_text=record_id)
    check(f"exactly one register row for {record_id}", rows.count() == 1)
    return rows.first.text_content() or ""


def check_register_entry(page: Page, requests: list[tuple[str, str]]) -> None:
    check("the register is not opened automatically: no request to /api/exceptions yet",
          not any(path == "/api/exceptions" for _, path in requests))
    panel = register_panel(page)
    check("the entry offers an explicit link and no register table",
          panel.locator("table").count() == 0 and "Opening it is a read-only request" in (panel.text_content() or ""))


def check_register(page: Page) -> None:
    panel = open_register_by_keyboard(page)
    panel.get_by_role("region", name=ai.REGISTER_TABLES[0], exact=True).wait_for()
    text = panel.text_content() or ""
    for phrase in (*ai.REGISTER_EXPECTED, *ai.CONFLICT_EXPECTED):
        check(f"register shows: {phrase}", phrase in text)
    for phrase in ai.REGISTER_FORBIDDEN:
        check(f"register does not claim: {phrase}", phrase not in text)
    quarantined = row_text(panel, ai.QUARANTINED_ID)
    fallback = row_text(panel, ai.FALLBACK_ID)
    check("quarantined row says Quarantined with its reason, not a fallback",
          ai.QUARANTINED_TEXT in quarantined and "Fell back" not in quarantined)
    check("fallback row says it fell back with its reason, not Quarantined",
          ai.FALLBACK_TEXT in fallback and "Quarantined." not in fallback)
    for label, row in (("quarantined", quarantined), ("fallback", fallback)):
        check(f"{label} row keeps owner as configuration, eligibility Unknown and placeholder recovery",
              "not an appointment" in row and "Unknown" in row and "Placeholder guidance" in row)
    check("workflow-only record is not listed as a failure", ai.WORKFLOW_ID not in text)
    check("no controls in the register panel",
          panel.locator("button, form, input, select, textarea").count() == 0)
    # The running app records its own "AI is not configured" fallback, so other rows may exist.
    cells = panel.get_by_role("region", name=ai.REGISTER_TABLES[0], exact=True).locator("tbody tr").evaluate_all(
        "rows => rows.map(row => [...row.cells].map(cell => cell.textContent || ''))")
    failed = ai.failed_ai_rows(cells)
    ids = [row[ai.SOURCE_COLUMN] for row in failed]
    check("both synthetic failed AI rows are listed once each by Kind",
          ids.count(ai.QUARANTINED_ID) == 1 and ids.count(ai.FALLBACK_ID) == 1)
    check("every failed AI row says Quarantined or Fell back, none claims a model result",
          all(ai.says_failure_outcome(row[ai.HAPPENED_COLUMN]) for row in failed))
    labels = [name for name in ai.REGISTER_TABLES
              if panel.get_by_role("region", name=name, exact=True).count() == 1]
    check(f"register table regions are labelled: {labels}", labels == list(ai.REGISTER_TABLES))
    check("register table regions are focusable and captioned", all(
        panel.get_by_role("region", name=name, exact=True).evaluate(
            "el => el.tabIndex === 0 && !!el.querySelector('caption')") for name in labels))
    tab_to_regions(page, labels)
    for width in (320, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        check(f"register reflow {width}px",
              page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))


def intercepted_register(page: Page, status: int, body: dict[str, Any]) -> str:
    def reply(route: Route) -> None:
        route.fulfill(status=status, content_type="application/json", body=json.dumps(body))

    page.route("**/api/exceptions", reply)
    try:
        open_screen(page)
        panel = open_register_by_keyboard(page)
        panel.locator("p").first.wait_for()
        check("intercepted register shows no controls",
              panel.locator("button, form, input, select, textarea").count() == 0)
        return panel.text_content() or ""
    finally:
        page.unroute("**/api/exceptions")


def check_unavailable_and_empty(page: Page) -> None:
    text = intercepted_register(page, 503, {"error": "synthetic outage"})
    check("an unavailable register is not an all-clear", ai.UNAVAILABLE_TEXT in text)
    check("an unavailable register lists no items", "Exception items returned for you" not in text)
    text = intercepted_register(page, 200, ai.EMPTY_CONTRACT)
    check("an empty register is not an all-clear", ai.EMPTY_TEXT in text)
    check("an empty register still says service state is Unknown", "Service state Unknown" in text)


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            try:
                page = context.new_page()
                errors: list[str] = []
                requests: list[tuple[str, str]] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(base + "/app")
                page.locator("#email").fill("pam@example.test")
                page.locator("#pw").fill("synthetic-check")
                page.locator("button[type=submit]").click()
                page.locator("#nav").wait_for()
                # Registered after sign-in so the sign-in POST is excluded. These are
                # browser-observed requests: they cannot show what the server did.
                page.on("request", lambda r: requests.append((r.method, urlparse(r.url).path)))
                open_screen(page)
                # The landing view reads its own priority data; only count what follows.
                page.wait_for_load_state("networkidle")
                register_start = len(requests)
                check_register_entry(page, requests)
                page_axe = check_page_queue(page)
                for width in (320, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    check(f"page queue reflow {width}px",
                          page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
                check_register(page)
                check_unavailable_and_empty(page)
                page.set_viewport_size({"width": 1280, "height": 900})
                open_screen(page)
                page.locator('a.item[href*="case=ZF-1"]').click()
                page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
                axe_ran = check_accessibility(page) and page_axe
                for width in (320, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    check(f"reflow {width}px",
                          page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
                writes = [f"{method} {path}" for method, path in requests
                          if method not in ("GET", "HEAD", "OPTIONS")]
                models = [path for _, path in requests[register_start:] if path.startswith(MODEL_PATHS)]
                check(f"made no writes: {writes}", not writes)
                check(f"made no model or AI requests: {models}", not models)
                check(f"no JavaScript errors: {errors}", not errors)
                print("RESULT PASS (axe scan ran)" if axe_ran
                      else "RESULT PARTIAL: axe scan SKIPPED, no automated WCAG evidence")
            finally:
                context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, operator_data, env_overrides=ai.STAFF_ENV)
