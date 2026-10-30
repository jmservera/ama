"""Issue 552: real local case UI density, disclosure and attached-tab checks."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright

from checks.case_journey_browser_check import journey_data, sign_in
from checks.design_system_browser_check import check, main


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


def geometry(page: Page) -> dict[str, Any]:
    result: dict[str, Any] = page.evaluate("""() => ({
      width: innerWidth,
      overflow: document.documentElement.scrollWidth > innerWidth,
      heights: [...document.querySelectorAll('.step')].map(el => el.getBoundingClientRect().height),
      labels: [...document.querySelectorAll('.step-name')].map(el => el.textContent)
    })""")
    return result


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

        page.route("**/case-workspace.js", workspace_script)
        try:
            page.goto(base + "/app#/case/ZF-1?tab=overview")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-check")
            page.get_by_role("button", name="Sign in", exact=True).click()
            page.get_by_text("Tab navigation unavailable", exact=False).wait_for()
            panels = page.locator(".case-tab-panel")
            check(f"fallback lists all nine panels/{mode}", panels.count() == 9)
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


def run_browser(base: str, out: Path, baseline: bool) -> None:
    results: dict[str, Any] = {"baseline": baseline, "viewports": [], "checks": []}
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
            for width in (1280, 390, 320):
                page.set_viewport_size({"width": width, "height": 800})
                record = geometry(page)
                results["viewports"].append(record)
                check(f"no page overflow/{width}", not record["overflow"])
                page.locator(".case-journey").screenshot(path=str(out / f"journey-{width}.png"))
                if not baseline:
                    ceiling = 132 if width == 1280 else 116
                    check(
                        f"compact step height <= {ceiling}px/{width}",
                        max(record["heights"]) <= ceiling,
                    )
            if baseline:
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
            panel = page.get_by_role("tabpanel", name="Resident", exact=True)
            tablist = page.get_by_role("tablist", name="Case sections")
            tablist.scroll_into_view_if_needed()
            before = tablist.bounding_box()
            panel.focus()
            panel.press("Control+End")
            page.wait_for_function(
                "() => document.querySelector('#case-panel-resident').scrollTop > 0"
            )
            check(
                "panel scrolls while attached tabs stay stationary",
                panel.evaluate(
                    "el => el.scrollTop > 0 && !el.contains(document.querySelector('[role=tablist]'))"
                )
                and before == tablist.bounding_box(),
            )
            results["checks"].append("manual tab keys, URL/back, retained fields, stationary tabs")
            page.emulate_media(reduced_motion="reduce")
            check(
                "reduced motion token remains zero",
                page.evaluate(
                    "getComputedStyle(document.documentElement).getPropertyValue('--motion').trim() === '0s'"
                ),
            )
            page.screenshot(path=str(out / "attached-tabs-1280.png"))
            results["touch"] = touch_disclosure(browser, base, out)
            results["fallbacks"] = fallback_cases(browser, base)
            check("no unexpected JavaScript errors", not errors)
            results["errors"] = errors
        finally:
            (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
            context.close()
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--baseline", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, args.out, args.baseline), journey_data)
