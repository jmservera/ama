"""Rendered check of the atlas tension sequence on three installed specialist screens (#233).

Signs in through the real /app as a synthetic Retrofit Programme Manager and opens
Programme queue, Resident choice and Package queue for the same synthetic home. It
checks what Chromium actually shows, not the source text: the "Not shown for this
role" panel next to permitted same-home context, the resident choice and withdrawal
panels before "Choice comes before offered capacity", the explanation before the
capacity table, and package rows in reference order although the browser receives them
in another order and utilisation and headroom point elsewhere.

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.atlas_tensions_browser_check

Set ZF_TENSIONS_SCREENSHOTS to a new directory to keep full-page screenshots.
This is an engineering check on one synthetic home. It is not the connected eight-stage
walk, assistive-technology, WCAG, Fluent 2 or user acceptance (#150, #151, #155).
"""

from __future__ import annotations

import hashlib
import json
import os
import runpy
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, Route, sync_playwright

from checks.design_system_browser_check import ROOT, check, main
from checks.role_screens_fixtures import synthetic_data

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
MANAGER = "pam@example.test"
HOME = "ZF-1"
PROGRAMME = "Programme queue and connected home view"
RESIDENT = "Resident choice and update queue"
PACKAGES = "Package queue"
WITHHELD = "Not shown for this role"
PRECEDENCE = "Choice comes before offered capacity"
CAPACITY_PANEL = "Package queue"
PACKAGE_TABLE = "Packages with period, scope, version and capacity"
# Reference order is PKG-001..003. The browser is given another order on purpose.
DELIVERED_ORDER = ("PKG-002", "PKG-003", "PKG-001")
VIEWPORTS = (1280, 320)
STEP_NAMES = ("Technical", "Resident", "Delivery", "Quality", "Finance")
WITHHELD_ITEMS = {
    PROGRAMME: (
        "Resident contact details and access history "
        "(use the safe route reference in the case workspace)",
        "Household and vulnerability details beyond what a step state needs",
        "Funding amounts and claim values",
    ),
    RESIDENT: (
        "Resident phone, email and postal contact history (shown only as a safe route reference)",
        "Detailed access and household history beyond the contact needs above",
        "Contractor capacity and offered slots",
    ),
    PACKAGES: (
        "Resident contact details and access history "
        "(open the case workspace for the safe route reference)",
        "Contract rates, prices and invoice values",
        "Contractor submissions and acknowledgements, which are recorded outside this screen",
    ),
}


def tension_data() -> dict[str, Any]:
    """The shared synthetic home plus three packages.

    Headroom and use conflict with reference order.
    """
    data = synthetic_data()
    dataset = runpy.run_path(str(ROOT / "src/core/tests/dataset.py"))
    # Another contractor's home with no safety stop lets one real work order raise utilisation.
    dataset["supplied_resident_fixture"](data["cases"][2])
    from zava_forward.core.store import Store

    with tempfile.TemporaryDirectory(prefix="zf-tension-fixture-") as scratch:
        path = Path(scratch) / "synthetic.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        store = Store(str(path))
        manager = store.staff[MANAGER]
        # (call-off, offered, committed): headroom and offered both disagree with reference order.
        for number, (ref, offered, committed) in enumerate(
            (("SYN-CALL-OFF-A", 7, 5), ("SYN-CALL-OFF-B", 6, 2), ("SYN-CALL-OFF-C", 9, 9)), 1
        ):
            pid = store.create_package(
                manager,
                f"SYN wave {number}",
                "2026-01-01",
                "2099-12-31",
                "Loft insulation",
                ref,
                "SYN-1",
            )
            details = dataset["supplied_contract_fixture"](store, pid, manager)
            store.set_capacity(
                manager, pid, "Test Ltd", offered, committed, "SYN accepted commitment", details
            )
            if number == 2:
                other = dataset["supplied_contract_fixture"](store, pid, manager, "Other Ltd")
                store.set_capacity(
                    manager, pid, "Other Ltd", 3, 3, "SYN accepted commitment", other
                )
        store.issue_work_order(
            manager, "PKG-002", "ZF-5", resident_bindings=dataset["RESIDENT_BINDINGS"]
        )
        merged: dict[str, Any] = json.loads(json.dumps(store.data))
    return merged


def shown(value: Any) -> str:
    return "Unknown" if value is None or value == "" else str(value)


def panels(evidence: Any, prefix: str | None) -> tuple[list[str], dict[str, str], dict[str, float]]:
    """Titles in document order, their visible text and their rendered vertical position."""
    # Panels use content-visibility: auto, so each one is read while it is scrolled into view.
    titles: list[str] = []
    texts: dict[str, str] = {}
    tops: dict[str, float] = {}
    for section in evidence.locator("section.screen-record").all():
        section.scroll_into_view_if_needed()
        title = (section.locator("h2").first.text_content() or "").strip()
        check(f"panel '{title}' is visible", bool(title) and section.is_visible())
        titles.append(title)
        if prefix:
            # Full-page screenshots show skipped panels blank,
            # so each panel is also captured on its own.
            section.screenshot(path=f"{prefix}-panel-{len(titles):02}.png")
        texts[title] = section.inner_text()
        tops[title] = section.evaluate("el => el.getBoundingClientRect().top + window.scrollY")
    return titles, texts, tops


def precedes(
    titles: list[str], tops: dict[str, float], first: str, second: str, where: str
) -> None:
    check(
        f"{where}: '{first}' precedes '{second}' in the document",
        first in titles and second in titles and titles.index(first) < titles.index(second),
    )
    check(f"{where}: '{first}' renders above '{second}'", tops[first] < tops[second])


def check_regions_and_keys(page: Page, evidence: Any, where: str) -> None:
    regions = evidence.locator('div.table-scroll[role="region"]')
    labels = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check(
        f"{where}: every table is a labelled focusable region with a caption",
        bool(labels)
        and regions.evaluate_all(
            "els => els.every(el => el.tabIndex === 0 && el.querySelector('caption'))"
        ),
    )
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    reached: list[str] = []
    for _ in range(120):
        page.keyboard.press("Tab")
        label = page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''")
        if label in labels and label not in reached:
            reached.append(label)
        if len(reached) == len(set(labels)):
            break
    check(
        f"{where}: Tab reaches every table region: {reached}",
        sorted(reached) == sorted(set(labels)),
    )


def check_readonly(page: Page, evidence: Any, detail: dict[str, Any], where: str) -> None:
    text = evidence.inner_text()
    check(
        f"{where}: no write controls in the evidence panels",
        evidence.locator("button, form, input, select, textarea").count() == 0,
    )
    check(
        f"{where}: no contact actions",
        page.locator('main a[href^="tel:"], main a[href^="mailto:"]').count() == 0,
    )
    resident = detail["resident"]
    check(
        f"{where}: withheld resident contact and name are not displayed",
        resident["phone"] not in text and resident["name"] not in text,
    )


def check_withheld(texts: dict[str, str], screen: str, where: str) -> None:
    panel = texts[WITHHELD]
    check(
        f"{where}: withheld panel is not authorisation", "Withholding is not authorisation" in panel
    )
    for item in WITHHELD_ITEMS[screen]:
        check(f"{where}: withheld item shown: {item}", item in panel)


def check_programme(
    page: Page, evidence: Any, detail: dict[str, Any], where: str, prefix: str | None
) -> None:
    titles, texts, tops = panels(evidence, prefix)
    check(f"{where}: selected home is {HOME}", f"Selected home {HOME}" in evidence.inner_text())
    connected = f"Connected view for {HOME}"
    stages = f"Journey stages for {HOME}"
    check(f"{where}: same-home context panels shown", connected in titles and stages in titles)
    step_table = evidence.get_by_role("table", name="Same-home step states")
    step_table.scroll_into_view_if_needed()
    steps = step_table.locator("tbody tr")
    check(
        f"{where}: five same-home steps in order",
        steps.evaluate_all("rows => rows.map(r => r.cells[0].innerText)") == list(STEP_NAMES),
    )
    precedes(titles, tops, connected, WITHHELD, where)
    precedes(titles, tops, stages, WITHHELD, where)
    check_withheld(texts, PROGRAMME, where)
    items = evidence.locator(
        "section.screen-record", has=page.locator("h2", has_text=stages)
    ).locator("ol > li")
    stage_text = items.all_inner_texts()
    check(
        f"{where}: eight stages rendered in order",
        [t[:2] for t in stage_text] == [f"{n}." for n in range(1, 9)],
    )
    check(
        f"{where}: stage 4 states an offer is not a booking",
        "An offer is not a booking." in stage_text[3],
    )
    for number, screen_id in ((2, "resident-choice"), (3, "procurement-packages")):
        href = items.nth(number).locator("a").get_attribute("href")
        check(
            f"{where}: stage {number + 1} links to {screen_id} for {HOME}",
            f"screen={screen_id}" in href and f"case={HOME}" in href,
        )
    check_readonly(page, evidence, detail, where)


def check_resident(
    page: Page, evidence: Any, detail: dict[str, Any], where: str, prefix: str | None
) -> None:
    titles, texts, tops = panels(evidence, prefix)
    check(f"{where}: selected home is {HOME}", f"Selected home {HOME}" in evidence.inner_text())
    choice, stopped = "Choice for each measure", "Paused or withdrawn by the resident"
    commitment = "Linked update commitment"
    access = "Service requests and access needs (separate from choice)"
    precedes(titles, tops, choice, stopped, where)
    precedes(titles, tops, stopped, PRECEDENCE, where)
    precedes(titles, tops, commitment, PRECEDENCE, where)
    precedes(titles, tops, access, PRECEDENCE, where)
    precedes(titles, tops, PRECEDENCE, WITHHELD, where)
    check_withheld(texts, RESIDENT, where)
    for decision in detail["measure_decisions"]:
        latest = decision["versions"][-1]
        binding = (
            f"scope {shown(latest['scope'])}, revision {shown(latest['context_revision'])}, "
            f"design {shown(latest['design_version'])}"
        )
        for text in (
            decision["measure"],
            decision["status"],
            f"v{latest['version']}",
            binding,
            latest["note"],
        ):
            check(f"{where}: choice panel shows fixture value '{text}'", str(text) in texts[choice])
        check(
            f"{where}: paused panel names {decision['measure']} and {decision['status']}",
            decision["measure"] in texts[stopped] and decision["status"] in texts[stopped],
        )
        check(
            f"{where}: paused panel shows scope and version: {binding}", binding in texts[stopped]
        )
    update = detail["resident_update"]
    check(f"{where}: safe route reference shown", update["safe_contact_ref"] in texts[commitment])
    check(f"{where}: update status shown", update["status"] in texts[commitment])
    request = detail["service_requests"][0]
    need = request["accessibility"][0]
    check(
        f"{where}: contact need is in the separate access panel",
        need in texts[access] and request["id"] in texts[access],
    )
    check(
        f"{where}: choice and withdrawal panels do not carry contact or access",
        need not in texts[choice]
        and need not in texts[stopped]
        and request["id"] not in texts[stopped]
        and update["safe_contact_ref"] not in texts[stopped],
    )
    check(f"{where}: access panel does not carry the pause", "Paused" not in texts[access])
    rule = texts[PRECEDENCE]
    check(
        f"{where}: precedence panel states offer is neither booking nor promise",
        "takes precedence over any offered contractor slot" in rule
        and "not a booking and not a promise to the resident" in rule,
    )
    check_readonly(page, evidence, detail, where)


def check_packages(
    page: Page,
    evidence: Any,
    detail: dict[str, Any],
    packages: list[dict[str, Any]],
    where: str,
    prefix: str | None,
) -> None:
    titles, texts, tops = panels(evidence, prefix)
    check(f"{where}: selected home is {HOME}", f"Selected home {HOME}" in evidence.inner_text())
    explanation = "Offered capacity and resident choice"
    precedes(titles, tops, explanation, CAPACITY_PANEL, where)
    table = evidence.get_by_role("table", name=PACKAGE_TABLE)
    table.scroll_into_view_if_needed()
    table_top = table.evaluate("el => el.getBoundingClientRect().top + window.scrollY")
    check(
        f"{where}: precedence explanation renders above the capacity table",
        tops[explanation] < table_top,
    )
    note = texts[explanation]
    check(
        f"{where}: offered capacity is neither booking nor promise and yields to resident choice",
        "not a booking and not a promise to any resident" in note
        and "takes precedence over any offered slot" in note
        and "never ranked by utilisation or headroom" in note,
    )
    check_withheld(texts, PACKAGES, where)
    expected = [
        [
            f"{p['id']}: {p['name']}",
            f"{p['period_from']} to {p['period_to']}",
            f"{p['scope']} (v{p['scope_version']})",
            f"{p['contract_ref']} v{p['contract_version']}",
            cap["contractor"],
            str(cap["offered"]),
            str(cap["committed"]),
            str(cap["in_use"]),
            str(cap["headroom"]),
            cap["evidence_status"],
        ]
        for p in sorted(packages, key=lambda item: item["id"])
        for cap in p["capacity"]
    ]
    table.scroll_into_view_if_needed()
    rows = table.locator("tbody tr").evaluate_all(
        "rows => rows.map(r => [...r.cells].map(c => c.innerText))"
    )
    check(
        f"{where}: package rows follow reference order: {[r[0][:7] for r in rows]}",
        rows == expected,
    )
    reference = [r[0][:7] for r in rows]
    rankings = (
        rank_by(expected, 8, True),
        rank_by(expected, 8, False),
        rank_by(expected, 5, True),
        rank_by(expected, 7, True),
    )
    check(
        f"{where}: reference order differs from every headroom, offered and use "
        f"ranking: {rankings}",
        all(reference != ranking for ranking in rankings),
    )
    check_readonly(page, evidence, detail, where)


def rank_by(rows: list[list[str]], column: int, descending: bool) -> list[str]:
    return [r[0][:7] for r in sorted(rows, key=lambda r: int(r[column]), reverse=descending)]


def open_screen(page: Page, title: str) -> Any:
    page.get_by_role("navigation", name="Specialist screens").get_by_role(
        "link", name=title, exact=True
    ).click()
    page.get_by_role("heading", name=title, exact=True).wait_for()
    return page.get_by_role("region", name=f"Evidence for {HOME}", exact=True)


def run_browser(base: str) -> None:
    shots = os.environ.get("ZF_TENSIONS_SCREENSHOTS")
    if shots:
        Path(shots).mkdir(parents=True, exist_ok=True)
    else:
        print("SKIP screenshots: set ZF_TENSIONS_SCREENSHOTS to a new directory")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        try:
            page = context.new_page()
            errors: list[str] = []
            writes: list[str] = []
            delivered: list[list[str]] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "/app")
            page.locator("#email").fill(MANAGER)
            page.locator("#pw").fill("synthetic-check")
            page.locator("button[type=submit]").click()
            page.get_by_role("link", name="Specialist screens", exact=True).wait_for()
            # Attached after sign-in on purpose: the sign-in POST is expected.
            page.on(
                "request",
                lambda r: (
                    writes.append(f"{r.method} {r.url}") if r.method not in SAFE_METHODS else None
                ),
            )

            source = page.evaluate(
                "() => [...document.scripts].map(s => s.src).find(s => /role-screens\\.js/.test(s))"
            )
            served = page.request.get(source).body()
            candidate = ROOT / "src/api/src/zava_forward/api/web/role-screens.js"
            check(
                "served role-screens.js is this candidate's file",
                hashlib.sha256(served).hexdigest()
                == hashlib.sha256(candidate.read_bytes()).hexdigest(),
            )
            print(f"INFO role-screens.js sha256 {hashlib.sha256(served).hexdigest()}")

            detail = page.request.get(f"{base}/api/cases/{HOME}").json()
            packages_before = page.request.get(base + "/api/packages").json()
            check(
                "fixture supplies a paused choice, a safe route and three packages",
                detail["measure_decisions"][0]["status"] == "Paused"
                and bool(detail["resident_update"]["safe_contact_ref"])
                and [p["id"] for p in packages_before] == ["PKG-001", "PKG-002", "PKG-003"],
            )

            def reorder(route: Route) -> None:
                response = route.fetch()
                rows = response.json()
                shuffled = sorted(rows, key=lambda row: DELIVERED_ORDER.index(row["id"]))
                delivered.append([row["id"] for row in shuffled])
                route.fulfill(status=response.status, json=shuffled)

            page.route("**/api/packages", reorder)

            page.get_by_role("link", name="Specialist screens", exact=True).click()
            page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
            page.get_by_role("link", name=PROGRAMME, exact=True).click()
            check("no home is selected before the explicit choice", "case=" not in page.url)
            page.locator(f'a.item[href*="case={HOME}"]').click()
            evidence = page.get_by_role("region", name=f"Evidence for {HOME}", exact=True)
            evidence.wait_for()
            for width in VIEWPORTS:
                page.set_viewport_size({"width": width, "height": 900})
                where = f"programme-queue {width}px"
                prefix = f"{shots}/programme-queue-{width}" if shots else None
                check_programme(page, evidence, detail, where, prefix)
                check_regions_and_keys(page, evidence, where)
                check(
                    f"{where}: no horizontal scroll",
                    page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
                )
                if shots:
                    page.screenshot(
                        path=str(Path(shots) / f"programme-queue-{width}.png"), full_page=True
                    )
            page.set_viewport_size({"width": 1280, "height": 900})

            page.get_by_role(
                "link", name=f"3. Decide scope and feasibility: {RESIDENT}", exact=True
            ).click()
            page.get_by_role("heading", name=RESIDENT, exact=True).wait_for()
            evidence.wait_for()
            check(f"stage link keeps {HOME} selected", f"case={HOME}" in page.url)
            for width in VIEWPORTS:
                page.set_viewport_size({"width": width, "height": 900})
                where = f"resident-choice {width}px"
                prefix = f"{shots}/resident-choice-{width}" if shots else None
                check_resident(page, evidence, detail, where, prefix)
                check_regions_and_keys(page, evidence, where)
                check(
                    f"{where}: no horizontal scroll",
                    page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
                )
                if shots:
                    page.screenshot(
                        path=str(Path(shots) / f"resident-choice-{width}.png"), full_page=True
                    )
            page.set_viewport_size({"width": 1280, "height": 900})

            evidence = open_screen(page, PACKAGES)
            evidence.wait_for()
            check(f"screen menu keeps {HOME} selected", f"case={HOME}" in page.url)
            check(
                f"browser received packages in a different order: {delivered}",
                bool(delivered)
                and delivered[-1] == list(DELIVERED_ORDER)
                and delivered[-1] != sorted(delivered[-1]),
            )
            for width in VIEWPORTS:
                page.set_viewport_size({"width": width, "height": 900})
                where = f"procurement-packages {width}px"
                prefix = f"{shots}/procurement-packages-{width}" if shots else None
                check_packages(page, evidence, detail, packages_before, where, prefix)
                check_regions_and_keys(page, evidence, where)
                check(
                    f"{where}: no horizontal scroll",
                    page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
                )
                if shots:
                    page.screenshot(
                        path=str(Path(shots) / f"procurement-packages-{width}.png"), full_page=True
                    )

            page.unroute("**/api/packages", reorder)
            check(
                "case and package state are unchanged by the walk",
                page.request.get(f"{base}/api/cases/{HOME}").json() == detail
                and page.request.get(base + "/api/packages").json() == packages_before,
            )
            check(f"no non-GET/HEAD/OPTIONS requests after sign-in: {writes}", not writes)
            check(f"no JavaScript errors: {errors}", not errors)
            print(
                f"Chromium {browser.version}; synthetic loopback only; "
                f"one shared synthetic home {HOME}"
            )
            print(
                "COMPLETE: rendered tension sequence on three screens at 1280px and 320px; "
                "not the eight-stage walk, WCAG, assistive-technology or user acceptance"
            )
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    main(run_browser, tension_data)
