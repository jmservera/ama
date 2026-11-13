"""Native browser proof of the programme queue paging (#230) on an owned synthetic server.

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.programme_paging_browser_check

The check signs in as the Retrofit Programme Manager, opens the installed programme
queue over 60 constructed permitted cases and drives Next and Previous by keyboard at
1280 and 320 px. It then opens a page-2 row's connected-view link by keyboard (GET only).
One paging GET is deliberately aborted by the check itself: that is a
constructed transport failure, not an observed network incident and not backend proof.
It is an engineering check, not assistive-technology or WCAG acceptance (#155); axe is
not run here.
"""

from __future__ import annotations

import copy
import hashlib
import sys
import urllib.request
from pathlib import Path
from typing import Any

import checks.design_system_browser_check as harness
from checks import role_screens_fixtures
from checks.design_system_browser_check import ROOT, check, main
from checks.role_screens_fixtures import synthetic_data
from playwright.sync_api import Browser, Page, Request, Route, expect, sync_playwright

TOTAL = 60
PAGE_SIZE = 50
TABLE = "Shared queue: returned and handed-off work"
EMAIL = "pam@example.test"
SELECTED = "ZF-1"
PAGING = "/api/cases?view=all&limit=50&offset="
WEB_ROLE_SCREENS = ROOT / "src/api/src/zava_forward/api/web/role-screens.js"
QUEUE_CONTROLS = {"Previous page", "Next page", "Apply filter", "Reset to default view"}


def paging_data() -> dict[str, Any]:
    """Private fixture: shared synthetic data widened to 60 uniquely labelled cases."""
    data = synthetic_data()
    cases = data["cases"]
    first = cases[0]
    # Same adjustment the programme story makes: the return targets the home's current stage.
    first["returns"][0]["to_stage"] = first["stage"]
    for number in range(len(cases), TOTAL):
        extra = copy.deepcopy(first)
        extra["id"] = f"ZF-PG-{number + 1:03}"
        if number % 2:
            extra["returns"] = []
        cases.append(extra)
    for number, case in enumerate(cases, 1):
        case["home"]["address"] = f"SYN paging home {number:03}"
    return data


def visible_by_default(item: dict[str, Any]) -> bool:
    work = item.get("work") or {}
    return bool(work.get("returned")) or "unowned" in (work.get("queues") or [])


def get_json(page: Page, base: str, path: str) -> Any:
    response = page.request.get(base + path)
    check(f"read-only GET {path} is 200", response.status == 200)
    return response.json()


def row_ids(page: Page) -> list[str]:
    table = page.get_by_role("table", name=TABLE)
    table.wait_for()
    cells = table.locator("tbody tr").evaluate_all(
        "rows => rows.map(r => r.querySelector('th, td').textContent)"
    )
    return [cell.split(":", 1)[0] for cell in cells]


def label_of_row(page: Page, case_id: str) -> str:
    row = page.get_by_role("table", name=TABLE).locator("tbody tr").filter(has_text=case_id)
    return str(row.first.locator("th, td").first.text_content())


def focused(page: Page) -> str:
    return str(
        page.evaluate(
            "() => document.activeElement.id || document.activeElement.textContent.trim()"
        )
    )


def press_until(page: Page, key: str, wanted: str, limit: int = 6) -> None:
    for _ in range(limit):
        page.keyboard.press(key)
        if focused(page) == wanted:
            return
    raise AssertionError(f"{key} did not reach {wanted!r}; focus is {focused(page)!r}")


def no_overflow(page: Page, label: str, width: int) -> None:
    check(
        f"{width}px {label}: no horizontal overflow (not a full 1.4.10 test)",
        page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
    )


def check_provenance(base: str) -> None:
    served = hashlib.sha256(urllib.request.urlopen(base + "/role-screens.js").read()).hexdigest()
    local = hashlib.sha256(WEB_ROLE_SCREENS.read_bytes()).hexdigest()
    check(f"served role-screens.js is this worktree's file ({local[:12]})", served == local)
    for module in (sys.modules[__name__], harness, role_screens_fixtures):
        path = Path(str(module.__file__)).resolve()
        check(
            f"module {module.__name__} comes from this worktree: {path}", path.is_relative_to(ROOT)
        )
    print(f"INFO checker interpreter {sys.executable}; server uses the same executable", flush=True)


def check_width(browser: Browser, base: str, width: int) -> None:
    tag = f"{width}px"
    context = browser.new_context(viewport={"width": width, "height": 900})
    try:
        page = context.new_page()
        page.goto(base + "/app")
        page.locator("#email").fill(EMAIL)
        page.locator("#pw").fill("synthetic-check")
        page.locator("button[type=submit]").click()
        page.get_by_role("link", name="Specialist screens", exact=True).wait_for()
        errors: list[str] = []
        writes: list[str] = []
        paging_gets: list[str] = []
        aborted: list[str] = []

        def on_request(request: Request) -> None:
            if request.method not in ("GET", "HEAD", "OPTIONS"):
                writes.append(f"{request.method} {request.url}")
            if PAGING in request.url:
                paging_gets.append(request.url.split(PAGING)[1])

        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", on_request)

        first_api = get_json(page, base, PAGING + "0")
        second_api = get_json(page, base, PAGING + "50")
        paging_gets.clear()
        one, two = first_api["items"], second_api["items"]
        check(
            f"{tag} real API: 60 permitted cases, pages of 50 and 10",
            first_api["total"] == TOTAL and len(one) == PAGE_SIZE and len(two) == TOTAL - PAGE_SIZE,
        )
        ids_one, ids_two = [r["id"] for r in one], [r["id"] for r in two]
        labels = [r["address"] for r in one + two]
        check(
            f"{tag} page labels are unique and the pages are disjoint",
            len(set(labels)) == TOTAL and not set(ids_one) & set(ids_two),
        )
        for name, items in (("page 1", one), ("page 2", two)):
            shown = sum(visible_by_default(r) for r in items)
            check(
                f"{tag} fixture contract: {name} has default-visible and default-hidden rows "
                f"({shown} of {len(items)})",
                0 < shown < len(items),
            )
        expect_one = [i for i in ids_one if visible_by_default(one[ids_one.index(i)])]
        expect_two = [i for i in ids_two if visible_by_default(two[ids_two.index(i)])]
        watched = [SELECTED, ids_one[0], ids_two[0]]
        before = {cid: get_json(page, base, f"/api/cases/{cid}") for cid in watched}

        page.goto(base + f"/app#/screens?screen=programme-queue&case={SELECTED}")
        page.get_by_role("heading", name="Programme queue and connected home view").wait_for()
        evidence = page.get_by_role("region", name=f"Evidence for {SELECTED}", exact=True)
        evidence.wait_for()
        paging = page.locator("#programme-page-status")
        scope_status = page.locator("#programme-filter-status")
        expect(paging).to_contain_text("Showing cases 1 to 50 of 60 permitted cases.")
        for phrase in ("applies to this page only", "Not a portfolio total"):
            expect(paging).to_contain_text(phrase)
        expect(scope_status).to_contain_text(
            f"{len(expect_one)} of 50 records on this page shown. Scope: Returned and handed-off"
        )
        check(
            f"{tag} first page rows are the real page-1 default rows",
            sorted(row_ids(page)) == sorted(expect_one),
        )
        check(f"{tag} no page-2 row is shown on page 1", not set(row_ids(page)) & set(ids_two))
        evidence_before = evidence.text_content() or ""
        check(
            f"{tag} selected home context is shown",
            f"Selected home {SELECTED}" in evidence_before,
        )
        buttons = {
            (t or "").strip()
            for t in page.locator("main button").evaluate_all("els => els.map(e => e.textContent)")
        }
        forms = page.locator("main form").evaluate_all(
            "els => els.map(e => e.getAttribute('aria-label'))"
        )
        check(
            f"{tag} queue has only the read-only paging and filter controls: {sorted(buttons)}",
            buttons == QUEUE_CONTROLS and forms == ["Scope filter"],
        )
        no_overflow(page, "first page", width)

        paging_gets.clear()
        page.locator("aside a[data-reset]").focus()
        expect(page.locator("#programme-prev")).to_be_disabled()
        expect(page.locator("#programme-next")).to_be_enabled()
        check(f"{tag} Previous on the first page is disabled and requests nothing", not paging_gets)
        press_until(page, "Tab", "programme-next")
        press_until(page, "Tab", "programme-scope")
        page.keyboard.type("All permitted")
        press_until(page, "Tab", "Apply filter")
        page.keyboard.press("Enter")
        expect(scope_status).to_contain_text(
            "50 of 50 records on this page shown. Scope: All permitted"
        )
        check(f"{tag} scope is kept in the address", "scope=all" in page.url)
        check(f"{tag} all page-1 rows are shown", sorted(row_ids(page)) == sorted(ids_one))
        rows_one = row_ids(page)
        status_before = scope_status.text_content() or ""

        def fail_once(route: Route) -> None:
            aborted.append(route.request.url)
            route.abort("connectionfailed")

        page.route(f"**{PAGING}50", fail_once, times=1)
        press_until(page, "Shift+Tab", "programme-scope")
        press_until(page, "Shift+Tab", "programme-next")
        page.keyboard.press("Enter")
        expect(paging).to_contain_text("That page could not be loaded")
        expect(paging).to_contain_text("The rows shown are unchanged")
        expect(paging).to_contain_text("Try again")
        expect(paging).to_be_visible()
        check(
            f"{tag} the constructed fault was consumed exactly once: {aborted}", len(aborted) == 1
        )
        check(f"{tag} failed page keeps the page-1 rows", row_ids(page) == rows_one)
        check(
            f"{tag} failed page keeps the filter status",
            (scope_status.text_content() or "") == status_before,
        )
        check(
            f"{tag} failed page keeps the selected home",
            (evidence.text_content() or "") == evidence_before,
        )
        check(
            f"{tag} no page-2 row appears after the failure", not set(row_ids(page)) & set(ids_two)
        )
        no_overflow(page, "failed page state", width)

        check(f"{tag} focus stays on Next for the retry", focused(page) == "programme-next")
        page.keyboard.press("Enter")
        expect(paging).to_contain_text("Showing cases 51 to 60 of 60 permitted cases.")
        expect(scope_status).to_contain_text(
            "10 of 10 records on this page shown. Scope: All permitted"
        )
        check(
            f"{tag} retry reaches the real page-2 rows only",
            sorted(row_ids(page)) == sorted(ids_two),
        )
        check(
            f"{tag} page-2 labels render",
            all(
                label_of_row(page, cid).endswith(r["address"])
                for cid, r in zip(ids_two, two, strict=True)
            ),
        )
        check(f"{tag} filter stayed page-local and kept across pages", "scope=all" in page.url)
        check(
            f"{tag} no portfolio-wide filter claim",
            "of 60 records" not in (scope_status.text_content() or ""),
        )
        check(
            f"{tag} selected home kept on page 2",
            (evidence.text_content() or "") == evidence_before,
        )
        no_overflow(page, "second page", width)

        requests_at_end = len(paging_gets)
        expect(page.locator("#programme-next")).to_be_disabled()
        check(
            f"{tag} Next is disabled on the last page and focus moved to Previous",
            focused(page) == "programme-prev",
        )
        page.wait_for_timeout(300)
        check(f"{tag} the last page requests nothing more", len(paging_gets) == requests_at_end)
        press_until(page, "Tab", "Reset to default view", 4)
        page.keyboard.press("Space")
        expect(scope_status).to_contain_text(
            f"{len(expect_two)} of 10 records on this page shown. Scope: Returned and handed-off"
        )
        expect(paging).to_contain_text("Showing cases 51 to 60 of 60 permitted cases.")
        check(
            f"{tag} Reset restores the default scope without changing the page",
            "scope=" not in page.url and sorted(row_ids(page)) == sorted(expect_two),
        )

        press_until(page, "Shift+Tab", "programme-prev", 5)
        page.keyboard.press("Enter")
        expect(paging).to_contain_text("Showing cases 1 to 50 of 60 permitted cases.")
        expect(scope_status).to_contain_text(f"{len(expect_one)} of 50 records on this page shown.")
        check(
            f"{tag} Previous returns the real page-1 rows",
            sorted(row_ids(page)) == sorted(expect_one) and not set(row_ids(page)) & set(ids_two),
        )
        check(
            f"{tag} selected home kept after returning",
            (evidence.text_content() or "") == evidence_before,
        )
        no_overflow(page, "returned first page", width)

        check(f"{tag} paging GET sequence: {paging_gets}", paging_gets == ["50", "50", "0"])

        expect(page.locator("#programme-prev")).to_be_disabled()
        check(
            f"{tag} focus moved to Next when Previous became disabled",
            focused(page) == "programme-next",
        )
        page.keyboard.press("Enter")
        expect(paging).to_contain_text("Showing cases 51 to 60 of 60 permitted cases.")
        expect(page.locator("#programme-next")).to_be_disabled()
        expect(page.locator("#programme-prev")).to_be_enabled()
        check(
            f"{tag} focus moved to Previous when Next became disabled",
            focused(page) == "programme-prev",
        )
        page.locator("#programme-scope").select_option("all")
        page.get_by_role("button", name="Apply filter").click()
        expect(scope_status).to_contain_text(
            "10 of 10 records on this page shown. Scope: All permitted"
        )
        table = page.get_by_role("table", name=TABLE)
        names = table.get_by_role("link").evaluate_all("els => els.map(e => e.textContent.trim())")
        rows_two = row_ids(page)
        check(
            f"{tag} each page-2 row has one unique 'Open connected view for' link: {names}",
            names == [f"Open connected view for {cid}" for cid in rows_two]
            and len(set(names)) == len(names),
        )
        target = rows_two[0]
        page.get_by_role("region", name=TABLE).focus()
        page.keyboard.press("Tab")
        check(
            f"{tag} Tab from the table region reaches the first row link",
            focused(page) == f"Open connected view for {target}",
        )
        in_view = page.evaluate(
            """() => {
                const link = document.activeElement;
                const box = link.getBoundingClientRect();
                const region = link.closest('.table-scroll').getBoundingClientRect();
                return {
                    inside: box.left >= region.left - 1 && box.right <= region.right + 1,
                    outline: getComputedStyle(link).outlineStyle,
                };
            }"""
        )
        check(
            f"{tag} focused row link is visible inside the scroll region with a focus outline",
            in_view["inside"] and in_view["outline"] != "none",
        )
        page.keyboard.press("Enter")
        page.get_by_role("region", name=f"Evidence for {target}", exact=True).wait_for()
        check(f"{tag} Enter opens the connected view address", f"case={target}" in page.url)
        check(
            f"{tag} connected view shows the selected home",
            f"Selected home {target}"
            in (
                page.get_by_role("region", name=f"Evidence for {target}", exact=True).text_content()
                or ""
            ),
        )
        sidebar_row = page.locator("aside a.item[aria-current='true']")
        expect(paging).to_contain_text("Showing cases 51 to 60 of 60 permitted cases.")
        expect(scope_status).to_contain_text("Scope: All permitted")
        expect(sidebar_row).to_contain_text(target)
        expect(page.locator("aside [role=status]").first).to_contain_text("records on page 3")
        check(
            f"{tag} the opened row keeps its queue page, sidebar page and scope in the address",
            "page=2" in page.url and "scope=all" in page.url and f"case={target}" in page.url,
        )
        check(
            f"{tag} the selected home is the one current sidebar row",
            sidebar_row.count() == 1
            and sidebar_row.get_attribute("href")
            == f"#/screens?screen=programme-queue&case={target}&page=2&scope=all",
        )
        no_overflow(page, "opened row from page 2", width)

        page.goto(base + f"/app#/screens?screen=programme-queue&case={target}&page=2")
        page.get_by_role("region", name=f"Evidence for {target}", exact=True).wait_for()
        expect(paging).to_contain_text("Showing cases 51 to 60 of 60 permitted cases.")
        expect(scope_status).to_contain_text("Scope: Returned and handed-off")
        expect(sidebar_row).to_contain_text(target)
        page.goto(base + f"/app#/screens?screen=programme-queue&case={SELECTED}")
        page.get_by_role("region", name=f"Evidence for {SELECTED}", exact=True).wait_for()
        expect(paging).to_contain_text("Showing cases 1 to 50 of 60 permitted cases.")
        expect(sidebar_row).to_contain_text(SELECTED)
        after = {cid: get_json(page, base, f"/api/cases/{cid}") for cid in watched}
        check(f"{tag} no case record changed", before == after)
        check(f"{tag} no post-sign-in writes: {writes}", not writes)
        check(f"{tag} no uncaught JavaScript errors: {errors}", not errors)
    finally:
        context.close()


def run_browser(base: str) -> None:
    check_provenance(base)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for width in (1280, 320):
                check_width(browser, base, width)
            print(
                f"Chromium {browser.version}; synthetic loopback only; role {EMAIL}; "
                "widths 1280, 320; "
                "one constructed (intercepted) paging GET failure per width; axe not run",
                flush=True,
            )
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, paging_data)
