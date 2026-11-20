"""Issue 552: real local case UI density, disclosure and attached-tab checks.

It also measures journey strip alignment and the case header links (owner report 2026-11-20).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright

from checks.asset_urls import asset_url
from checks.case_journey_browser_check import journey_data, scan, sign_in
from checks.design_system_browser_check import check, main
from checks.regulatory_ux_check import AXE_SHA256

STRIP_WIDTHS = (1920, 1440, 1280, 1200, 1199, 1100, 1024, 900, 899, 768, 600, 390, 320)
# The server maps these blocker steps to Funding, Resident agreement and the current step.
STRIP_BLOCKERS = (
    ("Final checks: funding", "Funding has not been confirmed."),
    ("Final checks: resident decision", "Resident decision or authority needs confirmation."),
    ("Safety review", "A safety review is open for this home."),
)
# Fixture name: (blocker indexes, journey cards that show as blocked).
STRIP_FIXTURES: dict[str, tuple[tuple[int, ...], int]] = {
    "no blockers": ((), 0),
    "one blocked": ((0,), 1),
    "two blocked": ((0, 1), 2),
    "current and blocked": ((2,), 1),
    "closed": ((0, 1), 0),
}
STRESS_NAMES = (
    "Survey and condition assessment of a property",
    "Quality inspection and handover to a resident",
)
STRIP_MEASURE = """() => {
  const probe = document.createElement('i');
  probe.style.color = 'var(--warn)';
  document.body.append(probe);
  const warn = getComputedStyle(probe).color;
  probe.remove();
  const lines = el => el.getBoundingClientRect().height
    / parseFloat(getComputedStyle(el).lineHeight);
  const cards = [...document.querySelectorAll('.stepper > li')].map(card => {
    const box = card.getBoundingClientRect();
    const style = getComputedStyle(card);
    const trigger = card.querySelector('.case-blocker-trigger');
    const label = card.querySelector('.case-blocker-label');
    return {
      name: card.querySelector('.step-name').textContent,
      state: card.querySelector('.step-state').textContent,
      nameLines: Math.round(lines(card.querySelector('.step-name'))),
      top: Math.round(box.top + scrollY), height: box.height, bottom: box.bottom + scrollY,
      current: card.getAttribute('aria-current') === 'step',
      outline: style.outlineStyle + ' ' + style.outlineWidth,
      blocked: card.classList.contains('blocked'),
      bar: style.borderLeftWidth, red: style.borderLeftColor === warn,
      clipped: card.scrollWidth > card.clientWidth + 1,
      ellipsis: [...card.querySelectorAll('*')].some(
        el => getComputedStyle(el).textOverflow === 'ellipsis'),
      trigger: trigger && {
        text: trigger.textContent, hint: Boolean(card.querySelector('.case-blocker-hint')),
        lines: label ? Math.round(lines(label)) : 0, name: trigger.getAttribute('aria-label'),
        bottom: trigger.getBoundingClientRect().bottom + scrollY,
      },
    };
  });
  const rows = new Map();
  for (const card of cards) rows.set(card.top, [...(rows.get(card.top) || []), card.height]);
  return {cards, rows: [...rows.values()],
    overflow: document.documentElement.scrollWidth > innerWidth};
}"""


def fixture(route: Route) -> None:
    case = route.fetch().json()
    reason = "The funding evidence needs a named reviewer. " + "Check the supplied record. " * 18
    case["work"]["blockers"] = [
        {
            "step": "Final checks: funding",
            "reason": reason,
            "owner": "Synthetic finance reviewer",
            "next_action": "Check the funding evidence.",
        },
        {
            "step": "Final checks: funding",
            "reason": "Final synthetic reason. " + "Long-unbroken-record-" * 24,
            "owner": "",
            "next_action": "",
        },
    ]
    route.fulfill(json=case)


def strip_fixture(kind: str, indexes: tuple[int, ...]) -> Callable[[Route], None]:
    def handle(route: Route) -> None:
        case = route.fetch().json()
        case["work"]["blockers"] = [
            {
                "step": STRIP_BLOCKERS[index][0],
                "reason": STRIP_BLOCKERS[index][1],
                "owner": "Synthetic finance reviewer",
                "next_action": "Check the record and update it.",
                "current_stop": kind == "closed",
            }
            for index in indexes
        ]
        case["closed"] = kind == "closed"
        if kind == "closed":
            case["stage"] = "Completed"
        route.fulfill(json=case)

    return handle


def geometry(page: Page) -> dict[str, Any]:
    result: dict[str, Any] = page.evaluate("""() => ({
      width: innerWidth,
      overflow: document.documentElement.scrollWidth > innerWidth,
      heights: [...document.querySelectorAll('.step')].map(el => el.getBoundingClientRect().height),
      labels: [...document.querySelectorAll('.step-name')].map(el => el.textContent)
    })""")
    return result


def strip_problems(width: int, record: dict[str, Any], check_ceiling: bool = True) -> list[str]:
    """Spec B: equal heights per visual row, three columns from 900 to 1199, no clipped text."""
    rows: list[list[float]] = record["rows"]
    cards: list[dict[str, Any]] = record["cards"]
    problems: list[str] = []
    expected = 1 if width >= 1200 else 2 if width >= 900 else 6
    if len(rows) != expected:
        problems.append(f"{len(rows)} visual rows, expected {expected}")
    if any(max(row) - min(row) > 1 for row in rows):
        problems.append("heights differ within a row")
    limit = 140 if width >= 1200 else 116
    if check_ceiling and max(max(row) for row in rows) > limit:
        problems.append(f"a card is taller than {limit}px")
    split = [card["name"] for card in cards if " " not in card["name"] and card["nameLines"] > 1]
    if split:
        problems.append(f"names break inside a word: {split}")
    if record["overflow"] or any(card["clipped"] for card in cards):
        problems.append("content overflows")
    if any(card["ellipsis"] for card in cards):
        problems.append("a step card clips text with an ellipsis")
    return problems


def strip_card_problems(kind: str, blocked_cards: int, record: dict[str, Any]) -> list[str]:
    """Spec B states: one outlined current step, and each blocked card keeps its cues and button."""
    cards: list[dict[str, Any]] = record["cards"]
    problems: list[str] = []
    current = [card for card in cards if card["current"]]
    if len(current) != (0 if kind == "closed" else 1):
        problems.append(f"{len(current)} current steps")
    if any(card["outline"] != "solid 2px" for card in current):
        problems.append("the current step lost its outline")
    blocked = [card for card in cards if card["blocked"]]
    if len(blocked) != blocked_cards:
        problems.append(f"{len(blocked)} blocked cards, expected {blocked_cards}")
    for card in blocked:
        name, trigger = card["name"], card["trigger"]
        if not re.search("blocked", card["state"], re.IGNORECASE):
            problems.append(f"{name} does not say Blocked")
        if card["bar"] != "8px" or not card["red"]:
            problems.append(f"{name} lost its red left bar")
        if trigger is None:
            problems.append(f"{name} has no button")
            continue
        if trigger["text"] != "Why blocked" or trigger["lines"] != 1 or trigger["hint"]:
            problems.append(f"{name} button does not read one line Why blocked")
        if not trigger["name"].startswith(f"{name}: why blocked."):
            problems.append(f"{name} button lost its accessible name")
        if card["bottom"] - trigger["bottom"] > 8:
            problems.append(f"{name} button is not at the foot of its card")
    feet = [card["trigger"]["bottom"] for card in blocked if card["trigger"]]
    if feet and max(feet) - min(feet) > 1:
        problems.append("blocked buttons do not share a foot line")
    return problems


def strip_page_checks(page: Page, kind: str) -> None:
    """Closed summary wording and the two header links, on the page the strip was measured on."""
    text = page.locator(".case-summary").inner_text()
    jumps = page.locator(".case-summary").get_by_role("button")
    next_jump = jumps.filter(has_text=re.compile(r"^Open next action$"))
    blockers_jump = jumps.filter(has_text=re.compile(r"^See all blockers$"))
    if kind == "closed":
        check(
            "closed case summary agrees with its six done steps",
            all(
                sentence in text
                for sentence in (
                    "Closed, all six steps done",
                    "None. A manager can reopen this case.",
                    "No recorded blockers. This case is closed.",
                )
            )
            and "Step unknown" not in text
            and page.locator(".case-blocker").count() == 0,
        )
        check(
            "closed case summary offers no next action or blocker jump",
            next_jump.count() == 0 and blockers_jump.count() == 0,
        )
    elif kind == "no blockers":
        check(
            "open case without blockers offers the next action but no blocker jump",
            next_jump.count() == 1 and blockers_jump.count() == 0,
        )
    else:
        check(
            f"open case with blockers keeps both summary jumps/{kind}",
            next_jump.count() == 1 and blockers_jump.count() == 1,
        )
        page.get_by_role("tab", name="Funding", exact=True).click()
        blockers_jump.click()
        expect(page.get_by_role("tab", name="Blockers and safety", exact=False)).to_have_attribute(
            "aria-selected", "true"
        )
    if kind == "no blockers":
        check(
            "open case without blockers keeps its summary wording",
            "No recorded blockers." in text and "This case is closed." not in text,
        )
        links = page.locator(".case-links > li > a")
        boxes: list[dict[str, float]] = links.evaluate_all(
            "els => els.map(el => el.getBoundingClientRect().toJSON())"
        )
        apart = boxes[1]["left"] - boxes[0]["right"] >= 8 or boxes[1]["top"] >= boxes[0]["bottom"]
        check(
            "case header links are two separate links",
            links.all_inner_texts()[:2] == ["Back to the list", "Versioned home case"]
            and page.get_by_role("link", name="Back to the list", exact=True).count() == 1
            and page.get_by_role("link", name="Versioned home case", exact=True).count() == 1
            and apart,
        )


def strip_case(
    browser: Browser, base: str, out: Path, kind: str, indexes: tuple[int, ...], blocked: int
) -> list[dict[str, Any]]:
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    context.route(
        "**/*",
        lambda route: (
            route.continue_() if route.request.url.startswith(base + "/") else route.abort()
        ),
    )
    page = context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.route("**/api/cases/ZF-1", strip_fixture(kind, indexes))
    records: list[dict[str, Any]] = []
    try:
        sign_in(page, base)
        for width in STRIP_WIDTHS:
            page.set_viewport_size({"width": width, "height": 900})
            record: dict[str, Any] = page.evaluate(STRIP_MEASURE)
            problems = strip_problems(width, record)
            if width == 1280:
                problems += strip_card_problems(kind, blocked, record)
            heights = [[round(value, 1) for value in row] for row in record["rows"]]
            check(
                f"journey strip aligned/{kind}/{width}: {heights}"
                + (f" PROBLEMS {problems}" if problems else ""),
                not problems,
            )
            records.append({"fixture": kind, "width": width, "rows": heights})
            if width in (1440, 1100, 900, 390):
                shot = out / f"strip-{kind.replace(' ', '-')}-{width}.png"
                page.locator(".case-journey").screenshot(path=str(shot))
        page.set_viewport_size({"width": 1280, "height": 900})
        strip_page_checks(page, kind)
        check(f"no JavaScript errors: journey strip/{kind}", not errors)
    finally:
        context.close()
    return records


def strip_stress(browser: Browser, base: str) -> list[dict[str, Any]]:
    """Spec B.5: a 45 character name on cards one and six keeps rows equal and nothing overflows."""
    check("stress names are 45 characters", {len(name) for name in STRESS_NAMES} == {45})
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    context.route(
        "**/*",
        lambda route: (
            route.continue_() if route.request.url.startswith(base + "/") else route.abort()
        ),
    )
    page = context.new_page()
    page.route("**/api/cases/ZF-1", strip_fixture("two blocked", STRIP_FIXTURES["two blocked"][0]))
    records: list[dict[str, Any]] = []
    try:
        sign_in(page, base)
        page.evaluate(
            """names => document.querySelectorAll('.step-name').forEach((el, index) => {
              if (index === 0) el.textContent = names[0];
              if (index === 5) el.textContent = names[1];
            })""",
            list(STRESS_NAMES),
        )
        for width in (1440, 1024, 390):
            page.set_viewport_size({"width": width, "height": 900})
            record: dict[str, Any] = page.evaluate(STRIP_MEASURE)
            problems = strip_problems(width, record, check_ceiling=False)
            heights = [[round(value, 1) for value in row] for row in record["rows"]]
            check(
                f"journey strip stress names/{width}: {heights}"
                + (f" PROBLEMS {problems}" if problems else ""),
                not problems,
            )
            records.append({"fixture": "stress", "width": width, "rows": heights})
    finally:
        context.close()
    return records


def strip_alignment(browser: Browser, base: str, out: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for kind, (indexes, blocked) in STRIP_FIXTURES.items():
        records += strip_case(browser, base, out, kind, indexes, blocked)
    return records + strip_stress(browser, base)


def touch_disclosure(browser: Browser, base: str, out: Path) -> dict[str, Any]:
    context = browser.new_context(
        viewport={"width": 320, "height": 480}, has_touch=True, is_mobile=True
    )
    context.route(
        "**/*",
        lambda route: (
            route.continue_() if route.request.url.startswith(base + "/") else route.abort()
        ),
    )
    page = context.new_page()
    page.on("dialog", lambda dialog: dialog.accept())
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.route("**/api/cases/ZF-1", fixture)
    try:
        sign_in(page, base)
        page.get_by_role("button", name=re.compile("^Funding: why blocked")).tap()
        popup = page.locator(".case-blocker-popover:popover-open")
        expect(popup).to_be_visible()
        session = context.new_cdp_session(page)
        box = popup.bounding_box()
        assert box is not None
        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] * 0.8
        for _ in range(24):
            if popup.evaluate("el => el.scrollTop + el.clientHeight >= el.scrollHeight - 2"):
                break
            session.send(
                "Input.dispatchTouchEvent",
                {
                    "type": "touchStart",
                    "touchPoints": [{"x": x, "y": y}],
                },
            )
            for step in range(1, 9):
                session.send(
                    "Input.dispatchTouchEvent",
                    {
                        "type": "touchMove",
                        "touchPoints": [{"x": x, "y": y - box["height"] * 0.6 * step / 8}],
                    },
                )
                page.wait_for_timeout(16)
            session.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
            page.wait_for_timeout(100)
        page.screenshot(path=str(out / "popover-touch-320.png"))
        page.wait_for_function("""() => {
          const el = document.querySelector('.case-blocker-popover:popover-open');
          return el.scrollTop + el.clientHeight >= el.scrollHeight - 2;
        }""")
        record: dict[str, Any] = popup.evaluate("""el => {
          const last = el.querySelector('dl:last-child dd:last-child').getBoundingClientRect();
          const box = el.getBoundingClientRect();
          return {scrollTop: el.scrollTop, scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight, lastVisible: last.bottom <= box.bottom
              && last.top >= box.top};
        }""")
        check("touch swipe reaches final next action", record["lastVisible"])
        page.screenshot(path=str(out / "popover-touch-320.png"))
        page.touchscreen.tap(2, 2)
        expect(popup).to_have_count(0)
        check("touch light dismissal and no JavaScript errors", not errors)
        record["errors"] = errors
        return record
    finally:
        context.close()


def fallback_cases(browser: Browser, base: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for mode in ("script-unavailable", "enhancement-exception"):
        context = browser.new_context(viewport={"width": 390, "height": 800})
        context.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(base + "/") else route.abort()
            ),
        )
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        source = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/case-workspace.js"

        def workspace_script(route: Route) -> None:
            if mode == "script-unavailable":
                route.abort()
            else:
                # Mutate enhancement-only layout before a controlled failure.
                route.fulfill(
                    content_type="text/javascript",
                    body=source.read_text()
                    + """
                  const enhance552 = CaseWorkspace.enhance;
                  CaseWorkspace.enhance = (...args) => {
                    const ui = enhance552(...args);
                    const workspace = args[1][0].panel.parentElement;
                    workspace.prepend(ui.tabs);
                    workspace.classList.add('case-sections');
                    ui.dispose();
                    throw new Error('Deliberate 552 enhancement exception');
                  };
                """,
                )

        page.route(asset_url("/case-workspace.js", base), workspace_script)
        try:
            page.goto(base + "/app#/case/ZF-1?tab=overview")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-check")
            page.get_by_role("button", name="Sign in", exact=True).click()
            page.get_by_text("Tab navigation unavailable", exact=False).wait_for()
            panels = page.locator(".case-tab-panel")
            check(f"fallback lists all ten panels/{mode}", panels.count() == 10)
            check(
                f"fallback unbounded visible panels/{mode}",
                panels.evaluate_all(
                    "els => els.every(el => !el.hidden && getComputedStyle(el).maxBlockSize === 'none'"
                    " && getComputedStyle(el).overflowY === 'visible' && !el.hasAttribute('role'))"
                ),
            )
            expect(page.get_by_role("tablist")).to_have_count(0)
            page.locator("#note").fill("Fallback ordinary work")
            expect(page.locator("#note")).to_have_value("Fallback ordinary work")
            expect(page.locator("#case-safety")).to_be_visible()
            page.goto(base + "/app#/case/ZF-4")
            page.locator('[data-case-workspace="ZF-4"]').wait_for()
            page.get_by_text("Tab navigation unavailable", exact=False).wait_for()
            safety = page.locator("#case-safety")
            expect(safety).to_be_visible()
            check(
                f"fallback persistent open safety stays above workspace/{mode}",
                safety.evaluate("""el => Boolean(
                    el.compareDocumentPosition(document.querySelector('[data-case-workspace]'))
                      & Node.DOCUMENT_POSITION_FOLLOWING)
                    && !el.closest('[data-case-workspace]')"""),
            )
            check(f"fallback no unexpected JavaScript errors/{mode}", not errors)
            records.append(
                {
                    "mode": mode,
                    "visible_unbounded_panels": panels.count(),
                    "errors": errors,
                    "expected_message": page.get_by_text(
                        "Tab navigation unavailable", exact=False
                    ).inner_text(),
                    "ordinary_input_usable": True,
                    "safety_reachable": True,
                }
            )
        finally:
            context.close()
    return records


def populated_hazards(route: Route) -> None:
    case = route.fetch().json()
    hold = {"scope": "Home", "case_id": "ZF-1", "status": "Active", "decision": None}
    base = {
        "category": "Damp and mould",
        "priority": "Significant",
        "released": False,
        "source": "Resident phone call to the repairs desk",
        "aware_at": "2026-11-13T09:15:00Z",
        "job": "RJ-700047",
    }
    case["hazards"] = [
        {
            **base,
            "referral_version": 1,
            "sent_at": "2026-11-13T10:00:00Z",
            "destination": {"code": "BS-1", "name": "Bea Safe", "role": "Building Safety Liaison"},
            "hold": {**hold, "accountable_role": "Building Safety Liaison", "legacy": False},
        },
        {
            **base,
            "referral_version": 1,
            "sent_at": "2026-11-13T10:00:00Z",
            "received_at": "2026-11-13T10:05:00Z",
            "accepted_at": "2026-11-13T10:30:00Z",
            "destination": {"code": "PM-01", "name": "Pam Lead", "role": "Retrofit Programme Manager"},
            "hold": {**hold, "accountable_role": "Retrofit Programme Manager", "legacy": False},
        },
        {
            **base,
            "referred": "2026-01-02",
            "repaired": "2026-02-01",
            "repair_evidence": None,
            "hold": {**hold, "accountable_role": None, "legacy": True},
        },
    ]
    route.fulfill(json=case)


def populated_safety_panel(
    browser: Browser, base: str, out: Path, axe: str, reports: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Issue 1530: scan open and legacy hazards at 1280, 390, 320 px and 200% browser zoom."""
    states = (
        ("1280", 1280, 1, 1.0),
        ("390", 390, 1, 1.0),
        ("320", 320, 1, 1.0),
        ("zoom-200", 640, 2, 1.0),
    )
    records: list[dict[str, Any]] = []
    for name, width, scale, root in states:
        context = browser.new_context(
            viewport={"width": width, "height": 800}, device_scale_factor=scale
        )
        context.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(base + "/") else route.abort()
            ),
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route("**/api/cases/ZF-1", populated_hazards)
        try:
            sign_in(page, base, "pam@example.test")
            page.evaluate(f"document.documentElement.style.fontSize = '{root * 100}%'")
            panel = page.locator("#case-safety")
            expect(panel.locator("li.safety-item")).to_have_count(3)
            expect(panel.locator("#hz-aware-hint")).to_contain_text("Example:")
            for selector in (".safety-details", ".safety-optional"):
                disclosures = panel.locator(selector)
                check(f"disclosure rendered {selector}: populated-safety/{name}", disclosures.count() > 0)
                disclosures.evaluate_all("els => els.forEach(el => { el.open = true; })")
                expect(disclosures.first).to_have_attribute("open", "")
            scan(page, axe, reports, f"populated-safety/{name}")
            check(f"axe no violations: populated-safety/{name}", not reports[-1]["violations"])
            overflow = page.evaluate(
                "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
            )
            check(f"no horizontal overflow: populated-safety/{name}", not overflow)
            check(f"no JavaScript errors: populated-safety/{name}", not errors)
            page.screenshot(path=str(out / f"populated-safety-{name}.png"), full_page=True)
            records.append({"state": name, "width": width, "scale": scale, "root_scale": root})
        finally:
            context.close()
    return records


def run_browser(base: str, out: Path, baseline: bool, axe: str | None = None) -> None:
    if not baseline and axe is None:
        raise ValueError("Normal verification requires pinned axe-core via --axe")
    reports: list[dict[str, Any]] = []
    results: dict[str, Any] = {
        "baseline": baseline, "completed": False, "viewports": [], "checks": [],
        "scans": reports, "attached_tabs": [], "axe_sha256": AXE_SHA256 if axe else None,
    }

    def scan_state(page: Page, state: str) -> None:
        if axe is None:
            raise ValueError("Cannot scan without pinned axe-core")
        scan(page, axe, reports, state)
        check(f"axe no violations: {state}", not reports[-1]["violations"])

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        results["browser_version"] = browser.version
        results["playwright_version"] = importlib.metadata.version("playwright")
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        context.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(base + "/") else route.abort()
            ),
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route("**/api/cases/ZF-1", fixture)
        try:
            sign_in(page, base)
            for width in (1280, 1024, 900, 390, 320):
                page.set_viewport_size({"width": width, "height": 800})
                record = geometry(page)
                results["viewports"].append(record)
                check(f"no page overflow/{width}", not record["overflow"])
                page.locator(".case-journey").screenshot(path=str(out / f"journey-{width}.png"))
                if not baseline:
                    ceiling = 140 if width >= 1200 else 116
                    check(
                        f"compact step height <= {ceiling}px/{width}",
                        max(record["heights"]) <= ceiling,
                    )
            if baseline:
                results["completed"] = True
                return
            icons = page.locator(".step-icon")
            check(
                "six loaded decorative deck icons",
                icons.count() == 6
                and icons.evaluate_all(
                    "els => els.every(el => el.complete && el.naturalWidth > 0"
                    " && el.alt === '' && el.getAttribute('aria-hidden') === 'true')"
                ),
            )
            for width in (1280, 390, 320):
                page.set_viewport_size({"width": width, "height": 800})
                summary = page.locator(".case-blocker-summary").first
                check(
                    f"single-line blocker summary/{width}",
                    summary.evaluate(
                        "el => getComputedStyle(el).whiteSpace === 'nowrap'"
                        " && el.getBoundingClientRect().height <= parseFloat(getComputedStyle(el).lineHeight) + 1"
                    ),
                )
                page.screenshot(path=str(out / f"case-{width}.png"), full_page=True)
                scan_state(page, f"overview/{width}")
                page.get_by_role("button", name=re.compile("^Funding: why blocked")).click()
                expect(page.locator(".case-blocker-popover:popover-open")).to_be_visible()
                scan_state(page, f"blocker-open/{width}")
                page.keyboard.press("Escape")
            page.set_viewport_size({"width": 320, "height": 480})
            trigger = page.get_by_role("button", name=re.compile("^Funding: why blocked"))
            trigger.focus()
            page.keyboard.press("Tab")
            page.keyboard.press("Shift+Tab")
            expect(trigger).to_be_focused()
            check(
                "disclosure target and keyboard focus are visible",
                trigger.evaluate(
                    "el => el.getBoundingClientRect().height >= 40"
                    " && getComputedStyle(el).outlineStyle === 'solid'"
                ),
            )
            trigger.press("Enter")
            popup = page.locator(".case-blocker-popover:popover-open")
            expect(popup).to_contain_text("Final synthetic reason.")
            expect(popup).to_contain_text("Owner not recorded. Ask the case owner.")
            expect(popup).to_contain_text("Ask the case owner to record the next action.")
            popup.focus()
            popup.press("Control+End")
            page.wait_for_function("""() => {
              const el = document.querySelector('.case-blocker-popover:popover-open');
              return el.scrollTop + el.clientHeight >= el.scrollHeight - 2;
            }""")
            results["keyboard_popup"] = popup.evaluate("""el => ({
              top: el.getBoundingClientRect().top, bottom: el.getBoundingClientRect().bottom,
              last: el.querySelector('dl:last-child dd:last-child').getBoundingClientRect().toJSON(),
              scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight
            })""")
            check(
                "keyboard reaches final next action in bounded popover",
                popup.evaluate(
                    """el => {
                  const last = el.querySelector('dl:last-child dd:last-child').getBoundingClientRect();
                  const box = el.getBoundingClientRect();
                  return last.bottom <= box.bottom && last.top >= box.top
                    && box.left >= 0 && box.right <= innerWidth && box.bottom <= innerHeight;
                }"""
                ),
            )
            results["checks"].append(
                "keyboard long disclosure, missing owner/action, final item reachable"
            )
            page.screenshot(path=str(out / "popover-keyboard-320.png"))
            page.keyboard.press("Escape")
            expect(popup).to_have_count(0)
            expect(trigger).to_be_focused()
            trigger.press("Space")
            expect(popup).to_be_visible()
            page.keyboard.press("Escape")
            page.evaluate("document.documentElement.style.fontSize = '200%'")
            trigger.click()
            popup.focus()
            popup.press("Control+End")
            page.wait_for_function("""() => {
              const el = document.querySelector('.case-blocker-popover:popover-open');
              return el.scrollTop + el.clientHeight >= el.scrollHeight - 2;
            }""")
            check(
                "enlarged text disclosure remains within viewport",
                popup.evaluate(
                    """el => {
                      const last = el.querySelector('dl:last-child dd:last-child').getBoundingClientRect();
                      const box = el.getBoundingClientRect();
                      return box.width <= innerWidth && last.top >= box.top
                        && last.bottom <= box.bottom;
                    }"""
                ),
            )
            results["enlarged_text"] = {
                "width": 320,
                "height": 480,
                "root_scale": 2,
                "geometry": popup.evaluate(
                    "el => ({scrollTop: el.scrollTop, scrollHeight: el.scrollHeight,"
                    " clientHeight: el.clientHeight, width: el.getBoundingClientRect().width})"
                ),
            }
            page.screenshot(path=str(out / "popover-200-percent.png"))
            page.keyboard.press("Escape")
            page.evaluate("document.documentElement.style.fontSize = ''")

            page.set_viewport_size({"width": 1280, "height": 800})
            overview = page.get_by_role("tab", name="Overview", exact=True)
            overview.click()
            overview.press("End")
            history = page.get_by_role("tab", name="History", exact=True)
            expect(history).to_be_focused()
            expect(overview).to_have_attribute("aria-selected", "true")
            history.press("Enter")
            expect(history).to_have_attribute("aria-selected", "true")
            check("tab URL updates", "tab=history" in page.url)
            page.go_back()
            expect(overview).to_have_attribute("aria-selected", "true")
            overview.press("Home")
            expect(overview).to_be_focused()
            page.get_by_role("tab", name="Resident", exact=True).click()
            page.locator("#note").fill("Retained synthetic note")
            page.get_by_role("tab", name="Funding", exact=True).click()
            page.get_by_role("tab", name="Resident", exact=True).click()
            expect(page.locator("#note")).to_have_value("Retained synthetic note")
            for width in (1280, 390, 320):
                page.set_viewport_size({"width": width, "height": 800})
                panel = page.get_by_role("tabpanel", name="Resident", exact=True)
                tablist = page.get_by_role("tablist", name="Case sections")
                tablist.scroll_into_view_if_needed()
                panel.focus()
                panel.press("Control+Home")
                page.wait_for_function(
                    "() => document.querySelector('#case-panel-resident').scrollTop === 0"
                )
                before = tablist.bounding_box()
                panel.press("Control+End")
                page.wait_for_function(
                    "() => document.querySelector('#case-panel-resident').scrollTop > 0"
                )
                record = panel.evaluate("""el => {
                  const tabs = document.querySelector('[role=tablist]');
                  const surface = el.parentElement;
                  const scrolling = node => /(auto|scroll|hidden|clip)/.test(
                    getComputedStyle(node).overflowY);
                  return {width: innerWidth, scrollTop: el.scrollTop,
                    scrollHeight: el.scrollHeight, clientHeight: el.clientHeight,
                    sharedSurface: surface.classList.contains('case-sections')
                      && tabs.parentElement === surface,
                    tabsOutsideScroller: !scrolling(surface) && !scrolling(tabs)
                      && !el.contains(tabs),
                    adjacent: Math.abs(tabs.getBoundingClientRect().bottom
                      - el.getBoundingClientRect().top) <= 1};
                }""")
                record["tabs_before"] = before
                record["tabs_after"] = tablist.bounding_box()
                results["attached_tabs"].append(record)
                check(
                    f"panel scrolls beneath stationary attached tabs/{width}",
                    record["scrollTop"] > 0
                    and record["sharedSurface"] and record["tabsOutsideScroller"]
                    and record["adjacent"] and before == record["tabs_after"],
                )
                expect(page.locator("#note")).to_have_value("Retained synthetic note")
                scan_state(page, f"resident-scrolled/{width}")
                page.screenshot(path=str(out / f"attached-tabs-{width}.png"), full_page=True)
            results["checks"].append("manual tab keys, URL/back, retained fields, stationary tabs")
            page.emulate_media(reduced_motion="reduce")
            check(
                "reduced motion token remains zero",
                page.evaluate(
                    "getComputedStyle(document.documentElement).getPropertyValue('--motion').trim() === '0s'"
                ),
            )
            results["strip_alignment"] = strip_alignment(browser, base, out)
            results["touch"] = touch_disclosure(browser, base, out)
            results["fallbacks"] = fallback_cases(browser, base)
            if axe is None:
                raise ValueError("Cannot scan without pinned axe-core")
            results["populated_safety"] = populated_safety_panel(browser, base, out, axe, reports)
            check("no unexpected JavaScript errors", not errors)
            results["errors"] = errors
            results["completed"] = True
        finally:
            (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
            context.close()
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--axe", type=Path, help="Pinned axe-core 4.10.3, required unless --baseline")
    args = parser.parse_args()
    if not args.baseline and args.axe is None:
        parser.error("--axe is required unless --baseline")
    axe = None
    if args.axe is not None:
        raw = args.axe.read_bytes()
        if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
            raise ValueError("Expected pinned axe-core 4.10.3")
        axe = raw.decode()
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, args.out, args.baseline, axe), journey_data)
