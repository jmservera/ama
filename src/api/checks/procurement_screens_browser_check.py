"""Browser evidence for the read-only Package queue and contractor job pack screens (#228).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.procurement_screens_browser_check

Each role and state is entered with the keyboard only. Per state the check reads
the rendered text, tabs through every focus stop, checks the focus indicator and
reflow, and runs the pinned axe 4.10.3 file (ZF_AXE_JS) at 1280 and 320 px. The
Issued state comes from the real store. The Completed, Withdrawn and Empty states
are the same real responses rewritten by a test route, so the checked record
shapes stay those the server produced. This is an engineering check, not
assistive-technology or human usability acceptance (#155, #151).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import runpy
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, Route, sync_playwright

from checks.design_system_browser_check import ROOT, check, main
from checks.workbench_browser_check import synthetic_data as workbench_data

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
AXE_SKIPPED: list[str] = []
SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
# Words that would turn a read-only draft into a claim of release, approval or vulnerability detail.
FORBIDDEN = ("Approved", "Accepted by", "Booked", "Release approved", "Vulnerab")
EMPTY = "No records supplied. This does not establish readiness."

Mutate = Callable[[list[dict[str, Any]], list[dict[str, Any]]], None]


def keep(packages: list[dict[str, Any]], orders: list[dict[str, Any]]) -> None:
    """Issued: the real store response, unchanged."""


def completed(packages: list[dict[str, Any]], orders: list[dict[str, Any]]) -> None:
    for package in packages:
        for row in package.get("capacity", []):
            row["evidence_status"] = "Evidenced: synthetic commitment record"
    for order in orders:
        order["state"] = "Completed"
        order["corrections"] = [{"reason": "Wrong depth", "by": "Pam Manager", "at": "2026-05-01"}]
        order["history"] = [
            *order.get("history", []),
            {"to_state": "Completed", "by": "Pam Manager", "at": "2026-05-02"},
        ]
        order["appointments"] = [{"outcome": "Attended", "at": "2026-05-02"}]


def withdrawn(packages: list[dict[str, Any]], orders: list[dict[str, Any]]) -> None:
    for order in orders:
        order["state"] = "Withdrawn"


def empty(packages: list[dict[str, Any]], orders: list[dict[str, Any]]) -> None:
    packages.clear()
    orders.clear()


@dataclass
class State:
    name: str
    mutate: Mutate
    expected: tuple[str, ...]
    rows: tuple[str, ...] = ()
    absent: tuple[str, ...] = ()
    status_regions: int | None = None
    empty_notes: int = 0


@dataclass
class Screen:
    email: str
    title: str
    panels: tuple[str, ...]
    always: tuple[str, ...]
    states: list[State] = field(default_factory=list)


MANAGER_ALWAYS = (
    "Contractor submission and review",
    "A contractor acknowledgement is not acceptance",
    "Separate step by a named reviewer; not available from this screen",
    "Not shown for this role",
)
READINESS_FIELDS = (
    "Next reviewer",
    "Named reviewer",
    "Unassigned. Contracts manager to name a person.",
)
CONTRACTOR_ALWAYS = (
    "not a provider portal",
    "Evidence checklist for this job pack",
    "Your submission",
    "Not recorded on this screen",
    "Acknowledgement",
    "Not recorded. An acknowledgement is not acceptance.",
    "The reason for any notice is not shared with contractors.",
    "Not shown for this role",
)
SCREENS = (
    Screen(
        "pam@example.test",
        "Package queue",
        ("Package queue", "Work orders for this home", "Contractor submission and review"),
        MANAGER_ALWAYS,
        [
            State(
                "Issued",
                keep,
                (
                    "Draft readiness only. This is not a release or approval.",
                    "Contract or call-off reference",
                    "SYN-CALL-OFF",
                    "Offered",
                    "Recorded committed",
                    "Unmet prerequisites for PKG-001",
                    "Next reviewer (role)",
                    "Issued",
                    "Unknown - not confirmed",
                    "Unmet or Unknown",
                    *READINESS_FIELDS,
                ),
                rows=(
                    "PKG-001: SYN north wave | 2026-01-01 to 2099-12-31 | Loft insulation (v1) | "
                    "SYN-CALL-OFF vSYN-1 | Test Ltd | 9 | 1 | 1 | 0 | Unknown - not confirmed",
                    "WO-0001 v1 | PKG-001 | Test Ltd | Issued | Loft insulation",
                    "WO-0001 v1 | None recorded | Not recorded | Unknown. No independent review",
                ),
                status_regions=1,
            ),
            State(
                "Completed and corrected",
                completed,
                (
                    "Completed",
                    "Evidenced: synthetic commitment record",
                    "Met on record",
                    *READINESS_FIELDS,
                ),
                rows=(
                    "WO-0001 v1 | Wrong depth (Pam Manager, 2026-05-01) | Recorded by Pam Manager "
                    "on 2026-05-02. A recorded completion is not acceptance. | Unknown. No independent review",
                ),
                absent=("Unknown - not confirmed",),
                status_regions=1,
            ),
            State(
                "Withdrawn",
                withdrawn,
                (
                    "Withdrawn",
                    "Unmet. Every work order for this home is withdrawn.",
                    *READINESS_FIELDS,
                ),
                status_regions=1,
            ),
            State(
                "Empty",
                empty,
                (EMPTY,),
                absent=("Draft readiness: PKG-001",),
                status_regions=0,
                empty_notes=3,
            ),
        ],
    ),
    Screen(
        "contractor@example.test",
        "Job pack and evidence checklist",
        ("Your job pack", "Evidence checklist", "Submission and review are separate"),
        CONTRACTOR_ALWAYS,
        [
            State(
                "Issued",
                keep,
                (
                    "Issued",
                    "Unknown. Not assessed on this screen.",
                    "Not marked Completed",
                    "Unknown. Review data is not available here. Done by someone other than you.",
                ),
                rows=("Appointment outcome recorded | Unknown. Not assessed on this screen.",),
                absent=("Marked Completed on the work order",),
            ),
            State(
                "Completed and corrected",
                completed,
                (
                    "Completed",
                    "Marked Completed on the work order by staff. This is a record, not acceptance.",
                ),
                rows=("Appointment outcome recorded | Recorded on a work order",),
                absent=("Not marked Completed",),
            ),
            State("Withdrawn", withdrawn, ("Withdrawn", "Not marked Completed")),
            State("Empty", empty, (EMPTY, "Unknown. Not assessed on this screen."), empty_notes=1),
        ],
    ),
)


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


def install_routes(page: Page, holder: dict[str, Mutate]) -> None:
    """Rewrite the two read responses for the current state; every request stays a GET."""

    def rewrite(route: Route) -> None:
        response = route.fetch()
        body = response.json()
        is_packages = "/api/packages" in route.request.url
        holder["mutate"](body if is_packages else [], [] if is_packages else body)
        route.fulfill(response=response, json=body)

    page.route(re.compile(r"/api/(packages|workorders)(\?|$)"), rewrite)


def restart_tabbing(page: Page) -> None:
    """Blur, scroll to the top and click the page heading so Tab starts from the top."""
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    page.locator("h1").first.click()


def tab_to(page: Page, selector: str, text: str = "") -> None:
    """Press Tab from the top of the page until the target has focus."""
    restart_tabbing(page)
    for _ in range(150):
        page.keyboard.press("Tab")
        if page.evaluate(
            "([sel, text]) => document.activeElement.matches(sel)"
            " && (!text || document.activeElement.textContent.trim() === text)",
            [selector, text],
        ):
            return
    raise AssertionError(f"Tab never reached {selector}")


def open_with_keyboard(page: Page, screen: Screen) -> None:
    """Reach the evidence using only Tab and Enter."""
    for href, name in (("#/screens", "Specialist screens"), ("screen=", screen.title)):
        tab_to(page, f'a[href*="{href}"]:not(.item)', name)
        page.keyboard.press("Enter")
        page.get_by_role("heading", name=name, exact=True).first.wait_for()
    tab_to(page, 'a.item[href*="case=ZF-1"]')
    page.keyboard.press("Enter")
    page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
    page.get_by_role("link", name="Open existing case workspace").wait_for()


def set_panel_rendering(page: Page, rendered: bool) -> None:
    """Panels use content-visibility: auto; render them all to read or scan every panel."""
    page.evaluate(
        """rendered => document.querySelectorAll('.screen-record').forEach(el => rendered
          ? el.style.setProperty('content-visibility', 'visible', 'important')
          : el.style.removeProperty('content-visibility'))""",
        rendered,
    )


FOCUS_STOP = """() => {
  const e = document.activeElement;
  const s = getComputedStyle(e);
  const r = e.getBoundingClientRect();
  const x = Math.min(Math.max(r.left + r.width / 2, 0), innerWidth - 1);
  const y = Math.min(Math.max(r.top, 0) + 2, innerHeight - 1, Math.max(r.bottom - 1, 0));
  const top = document.elementFromPoint(x, y);
  return {
    label: e.getAttribute('aria-label') || '',
    text: (e.innerText || '').trim().slice(0, 60),
    tag: e.tagName.toLowerCase(),
    inEvidence: !!e.closest('.screen-evidence'),
    outline: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2,
    ring: s.boxShadow !== 'none',
    covered: !(top && (e === top || e.contains(top))),
  };
}"""


def check_keyboard(page: Page, story: str, expected: list[str]) -> None:
    restart_tabbing(page)
    stops: list[dict[str, Any]] = []
    for _ in range(120):
        page.keyboard.press("Tab")
        stop = page.evaluate(FOCUS_STOP)
        if stop["inEvidence"]:
            stops.append(stop)
        if stop["text"] == "Open existing case workspace":
            break
    reached = [s["label"] for s in stops if s["label"]]
    check(f"{story} Tab visits the table regions in reading order: {reached}", reached == expected)
    check(
        f"{story} Tab ends on the case workspace link",
        bool(stops) and stops[-1]["text"] == "Open existing case workspace",
    )
    check(
        f"{story} every focus stop shows a visible indicator",
        all(s["outline"] and s["ring"] for s in stops),
    )
    check(
        f"{story} no focus stop is covered by other content", not any(s["covered"] for s in stops)
    )
    page.keyboard.press("Shift+Tab")
    back = page.evaluate(FOCUS_STOP)
    check(
        f"{story} Shift+Tab leaves the last stop (no keyboard trap)",
        back["text"] != "Open existing case workspace"
        and (not expected or (back["label"] == expected[-1] and back["inEvidence"])),
    )


def check_state_text(
    page: Page, story: str, screen: Screen, state: State, writes: list[str]
) -> None:
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    set_panel_rendering(page, True)
    text = evidence.inner_text()
    set_panel_rendering(page, False)
    spaced = " ".join(text.split())
    for phrase in (*screen.panels, *screen.always, *state.expected):
        check(f"{story} shows: {phrase}", phrase in spaced)
    for phrase in state.absent:
        check(f"{story} does not show: {phrase}", phrase not in spaced)
    rows = evidence.locator("tr").evaluate_all(
        "els => els.map(el => [...el.children].map(c => c.textContent.trim()).join(' | '))"
    )
    for row in state.rows:
        check(f"{story} row: {row[:70]}", any(r.startswith(row) for r in rows))
    check(
        f"{story} read-only: no write controls",
        evidence.locator("button, form, input, select, textarea").count() == 0,
    )
    check(
        f"{story} no contact links",
        evidence.locator('a[href^="tel:"], a[href^="mailto:"]').count() == 0,
    )
    check(
        f"{story} no approval, booking or vulnerability wording",
        not any(word in text for word in FORBIDDEN),
    )
    check(
        f"{story} every cell and field value carries text, so no state rests on colour or position",
        evidence.locator("td, dd").evaluate_all(
            "els => els.length > 0 ? els.every(el => el.textContent.trim().length > 0) : true"
        ),
    )
    check(
        f"{story} every table sits in a labelled focusable region",
        evidence.locator("table").evaluate_all(
            "els => els.every(t => {const r = t.parentElement; return r.matches("
            "'div.table-scroll[role=region]') && r.tabIndex === 0 && !!r.getAttribute('aria-label');})"
        ),
    )
    check(
        f"{story} every table is a labelled focusable region with a caption and column headers",
        evidence.locator('div.table-scroll[role="region"]').evaluate_all(
            "els => els.every(el => el.tabIndex === 0 && el.getAttribute('aria-label')"
            " && el.querySelector('caption') && el.querySelectorAll('th[scope=col]').length > 0"
            " && el.querySelector('caption').textContent === el.getAttribute('aria-label'))"
        ),
    )
    if state.status_regions is not None:
        check(
            f"{story} readiness statement is a status region ({state.status_regions})",
            evidence.locator('[role="status"]').count() == state.status_regions,
        )
    check(
        f"{story} empty tables say so in words ({state.empty_notes})",
        evidence.locator("p.empty").count() == state.empty_notes,
    )
    check(f"{story} made no non-GET/HEAD/OPTIONS requests: {writes}", not writes)


def check_axe(page: Page, story: str) -> None:
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        AXE_SKIPPED.append(story)
        print(f"SKIP {story} axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    if not page.evaluate("() => typeof axe !== 'undefined'"):
        page.evaluate(raw.decode())
    set_panel_rendering(page, True)
    for width in (1280, 320):
        page.set_viewport_size({"width": width, "height": 900})
        result = page.evaluate(
            """async (tags) => await axe.run(document.querySelector('main'),
              {runOnly: {type: 'tag', values: tags}})""",
            AXE_TAGS,
        )
        check(
            f"{story} axe 4.10.3 (main, {width}px) finds no violations: "
            f"{[v['id'] for v in result['violations']]}",
            not result["violations"],
        )
        print(
            f"INFO {story} {width}px axe passes {len(result['passes'])}, incomplete "
            f"(needs manual review): {[i['id'] for i in result['incomplete']]}"
        )


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for screen in SCREENS:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                try:
                    page = context.new_page()
                    errors: list[str] = []
                    writes: list[str] = []
                    holder: dict[str, Mutate] = {"mutate": keep}
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.goto(base + "/app")
                    page.locator("#email").fill(screen.email)
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
                    install_routes(page, holder)
                    for state in screen.states:
                        story = f"{screen.title} / {state.name}"
                        page.set_viewport_size({"width": 1280, "height": 900})
                        holder["mutate"] = state.mutate
                        open_with_keyboard(page, screen)
                        check_state_text(page, story, screen, state, writes)
                        evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
                        expected = evidence.locator("table > caption").all_text_contents()
                        check_keyboard(page, story, expected)
                        page.set_viewport_size({"width": 320, "height": 900})
                        check_keyboard(page, f"{story} at 320px", expected)
                        check_axe(page, story)
                        for width in (320, 1280):
                            page.set_viewport_size({"width": width, "height": 900})
                            check(
                                f"{story} reflow {width}px",
                                page.evaluate(
                                    "() => document.documentElement.scrollWidth <= innerWidth"
                                ),
                            )
                    check(f"{screen.title} has no JavaScript errors: {errors}", not errors)
                finally:
                    context.close()
        finally:
            browser.close()
    if AXE_SKIPPED:
        if os.environ.get("ZF_AXE_REQUIRED") == "1":
            raise AssertionError(f"axe scan skipped for {AXE_SKIPPED} but ZF_AXE_REQUIRED=1")
        print(f"PARTIAL: axe scan SKIPPED for {AXE_SKIPPED}; no automated accessibility result")
    else:
        print("COMPLETE: all checks ran, including axe 4.10.3 (main, 1280 and 320 px, every state)")


if __name__ == "__main__":
    main(run_browser, procurement_data)
