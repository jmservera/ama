"""Browser evidence for the read-only Package queue and contractor job pack screens (#228).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.procurement_screens_browser_check
"""

from __future__ import annotations

import hashlib
import json
import os
import runpy
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import ROOT, check, main
from checks.workbench_browser_check import synthetic_data as workbench_data

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
SCREENS = (
    (
        "pam@example.test",
        "Package queue",
        (
            "Draft readiness only. This is not a release or approval.",
            "Contract or call-off reference",
            "SYN-CALL-OFF",
            "Offered",
            "Recorded committed",
            "Unmet prerequisites for PKG-001",
            "Next reviewer (role)",
            "Named reviewer",
            "Unassigned. Contracts manager to name a person.",
            "A contractor acknowledgement is not acceptance",
            "Separate step by a named reviewer; not available from this screen",
        ),
        ("Package queue", "Work orders for this home", "Contractor submission and review"),
    ),
    (
        "contractor@example.test",
        "Job pack and evidence checklist",
        (
            "not a provider portal",
            "Evidence checklist for this job pack",
            "Unknown. Not assessed on this screen.",
            "Your submission",
            "Not recorded on this screen",
            "The reason for any notice is not shared with contractors.",
        ),
        ("Your job pack", "Evidence checklist", "Submission and review are separate"),
    ),
)
# Words that would turn a read-only draft into a claim of release, approval or vulnerability detail.
AXE_SKIPPED: list[str] = []
SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
FORBIDDEN = ("Approved", "Accepted by", "Booked", "Release approved", "Vulnerab")


def procurement_data() -> dict[str, Any]:
    """Synthetic home with one package, recorded capacity and one issued work order."""
    scenario = workbench_data()
    dataset = runpy.run_path(str(ROOT / "src/core/tests/dataset.py"))
    dataset["supplied_resident_fixture"](scenario["cases"][0])
    from zava_forward.core.store import Store

    with tempfile.TemporaryDirectory(prefix="zf-proc-fixture-") as scratch:
        path = Path(scratch) / "synthetic.json"
        path.write_text(json.dumps(scenario), encoding="utf-8")
        store = Store(str(path))
        manager = store.staff["pam@example.test"]
        pid = store.create_package(
            manager,
            "SYN north wave",
            "2026-01-01",
            "2099-12-31",
            "Loft insulation",
            "SYN-CALL-OFF",
            "SYN-1",
        )
        details = dataset["supplied_contract_fixture"](store, pid, manager)
        store.set_capacity(manager, pid, "Test Ltd", 9, 1, "SYN accepted commitment", details)
        store.issue_work_order(manager, pid, "ZF-1", resident_bindings=dataset["RESIDENT_BINDINGS"])
        data: dict[str, Any] = json.loads(json.dumps(store.data))
    return data


def check_accessibility(page: Page, story: str, panels: tuple[str, ...]) -> None:
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    text = evidence.inner_text()
    check(
        f"{story} read-only: no write controls",
        evidence.locator("button, form, input, select, textarea").count() == 0,
    )
    check(
        f"{story} no contact links",
        evidence.locator('a[href^="tel:"], a[href^="mailto:"]').count() == 0,
    )
    check(f"{story} names its panels: {panels}", all(panel in text for panel in panels))
    check(
        f"{story} no approval, booking or vulnerability wording",
        not any(word in text for word in FORBIDDEN),
    )
    regions = evidence.locator('div.table-scroll[role="region"]')
    expected = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check(
        f"{story} every table is a labelled focusable region with a caption",
        bool(expected)
        and regions.evaluate_all(
            "els => els.every(el => el.tabIndex === 0 && el.querySelector('caption'))"
        ),
    )
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    reached: list[str] = []
    for _ in range(80):
        page.keyboard.press("Tab")
        label = page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''")
        if label in expected and label not in reached:
            reached.append(label)
        if len(reached) == len(expected):
            break
    check(
        f"{story} Tab reaches every table region: {reached}",
        sorted(reached) == sorted(set(expected)),
    )
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        AXE_SKIPPED.append(story)
        print(f"SKIP {story} axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    page.evaluate(raw.decode())
    result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
      runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
    check(
        f"{story} axe 4.10.3 (main, 1280px) finds no violations: "
        f"{[v['id'] for v in result['violations']]}",
        not result["violations"],
    )
    print(
        f"INFO {story} axe incomplete (needs manual review): {[i['id'] for i in result['incomplete']]}"
    )


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for email, screen, expected, panels in SCREENS:
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
                    # Attached after sign-in on purpose: the sign-in POST is expected.
                    # Any later request that is not a safe read method is a write.
                    page.on(
                        "request",
                        lambda r: (
                            writes.append(f"{r.method} {r.url}")
                            if r.method not in SAFE_METHODS
                            else None
                        ),
                    )
                    page.get_by_role("link", name="Specialist screens", exact=True).click()
                    page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                    page.get_by_role("link", name=screen, exact=True).click()
                    page.locator('a.item[href*="case=ZF-1"]').click()
                    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
                    evidence.wait_for()
                    text = evidence.inner_text()
                    for phrase in expected:
                        check(f"{screen} shows: {phrase}", phrase in text)
                    if screen == "Package queue":
                        row = evidence.locator("tr", has_text="SYN-CALL-OFF").first.inner_text()
                        check(
                            f"{screen} row shows period, scope version, offered and committed: {row!r}",
                            "2026-01-01 to 2099-12-31" in row
                            and "(v1)" in row
                            and "Test Ltd" in row
                            and "\t9\t1" in row,
                        )
                        check(
                            f"{screen} shows the issued work order reference",
                            evidence.locator("table", has_text="Work-order references")
                            .locator("tbody tr")
                            .count()
                            == 1,
                        )
                        check(
                            f"{screen} unconfirmed capacity evidence is not shown as met",
                            "Unknown - not confirmed" in row and "Unmet or Unknown" in text,
                        )
                    else:
                        check(
                            f"{screen} lists the contractor's own work order",
                            evidence.locator("table", has_text="Work order and version")
                            .locator("tbody tr")
                            .count()
                            == 1,
                        )
                    check_accessibility(page, screen, panels)
                    for width in (320, 1280):
                        page.set_viewport_size({"width": width, "height": 900})
                        check(
                            f"{screen} reflow {width}px",
                            page.evaluate(
                                "() => document.documentElement.scrollWidth <= innerWidth"
                            ),
                        )
                    check(f"{screen} made no non-GET/HEAD/OPTIONS requests: {writes}", not writes)
                    check(f"{screen} has no JavaScript errors: {errors}", not errors)
                finally:
                    context.close()
        finally:
            browser.close()
    if AXE_SKIPPED:
        if os.environ.get("ZF_AXE_REQUIRED") == "1":
            raise AssertionError(f"axe scan skipped for {AXE_SKIPPED} but ZF_AXE_REQUIRED=1")
        print(f"PARTIAL: axe scan SKIPPED for {AXE_SKIPPED}; no automated accessibility result")
    else:
        print("COMPLETE: all checks ran, including axe 4.10.3 (main, 1280px, both roles)")


if __name__ == "__main__":
    main(run_browser, procurement_data)
