"""Exercise installed specialist screens against an owned synthetic local API."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from playwright.sync_api import Route, sync_playwright

from checks.design_system_browser_check import check, main
from checks.role_screens_fixtures import synthetic_data

# Independent child branches extend only their own installed-screen expectation.
SCENARIOS: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "231": ("quality@example.test", "Technical and independent quality evidence", (
        "Needs reassessment", "SYN-MISSING-DESIGN-231", "SYN-PHOTO-231",
        "SYN missing edge photo", "SYN Contractor", "Loft insulation: Returned",
        "Not signed off; follow the source review decision",
        "Incomplete, returned, replaced or stale evidence blocks handover",
    )),
}


def run_browser(base: str) -> None:
    selected = sys.argv[1] if len(sys.argv) > 1 else None
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            errors: list[str] = []
            writes: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            email = SCENARIOS[selected][0] if selected else "sam@example.test"
            page.goto(base + "/app")
            page.locator("#email").fill(email)
            page.locator("#pw").fill("synthetic-check")
            page.locator("button[type=submit]").click()
            page.get_by_role("heading", name="My cases today", exact=True).wait_for()
            page.on("request", lambda request: writes.append(request.url) if request.method == "POST" else None)
            page.get_by_role("link", name="Specialist screens", exact=True).click()
            page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
            if not selected:
                check("parent empty registry is explicit, not delivered screens",
                      "No specialist screens are installed" in page.locator("main").inner_text())
            else:
                _, screen, expected = SCENARIOS[selected]
                page.get_by_role("link", name=screen, exact=True).click()
                page.get_by_text("No home selected. Choose a home from this queue.", exact=True).wait_for()
                check("specialist navigation does not inherit white header text",
                      page.locator(".screen-links a").first.evaluate(
                          "el => getComputedStyle(el).color !== 'rgb(255, 255, 255)'"
                      ))
                check("no automatic selection or detail fetch", "case=" not in page.url)
                page.locator('a.item[href*="case=ZF-1"]').click()
                evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
                evidence.wait_for()
                for phrase in expected:
                    field = evidence.get_by_text(re.compile(re.escape(phrase))).last
                    field.scroll_into_view_if_needed()
                    page.wait_for_function(
                        "([element, text]) => element.innerText.includes(text)",
                        arg=[field.element_handle(), phrase],
                    )
                    check(f"story {selected} exact visible evidence: {phrase}",
                          phrase in field.inner_text() and field.is_visible())
                check("same home remains ZF-1",
                      evidence.get_by_role("heading", name="Selected home ZF-1", exact=True).count() == 1)
                if selected == "231":
                    reviews = evidence.get_by_role("table", name="Independent technical reviews", exact=True)
                    for title in ("Assessment", "Design", "Building and safety dependency"):
                        row = reviews.get_by_role("row").filter(
                            has=page.get_by_role("cell", name=title, exact=True)
                        )
                        row.scroll_into_view_if_needed()
                        page.wait_for_function(
                            "element => element.innerText.includes('Recorded sign-off; verify professional evidence')",
                            arg=row.element_handle(),
                        )
                        check(f"unaffected {title} retains supplied older-version sign-off",
                              row.get_by_role("cell", name="Signed off", exact=True).is_visible()
                              and row.get_by_role("cell", name="1", exact=True).is_visible()
                              and "stale" not in row.inner_text().lower())
                    changed = reviews.get_by_role("row").filter(
                        has=page.get_by_role("cell", name="Coordination", exact=True)
                    )
                    changed.scroll_into_view_if_needed()
                    check("affected coordination does not display its stale signed-off state",
                          changed.get_by_role("cell", name="Needs reassessment", exact=True).is_visible()
                          and changed.get_by_role("cell", name="Signed off", exact=True).count() == 0
                          and "Design changed to version 2" in changed.inner_text())
                check("no contact actions", evidence.locator('a[href^="tel:"], a[href^="mailto:"]').count() == 0)
                for width in (320, 390, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    check(f"story {selected} reflow {width}px",
                          page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
                page.emulate_media(reduced_motion="reduce")
                check("existing reduced motion retained",
                      page.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--motion').trim()") == "0s")
                reset = page.get_by_role("link", name="Reset screen view", exact=True)
                page.keyboard.press("Tab")
                reset.focus()
                check("native keyboard focus visible",
                      reset.evaluate("el => getComputedStyle(el).outlineStyle === 'solid'"))
                reset.press("Enter")
                page.get_by_text("No home selected. Choose a home from this queue.", exact=True).wait_for()
                check("reset removes selection without writes", "case=" not in page.url)
                screenshot_root = os.environ.get("ZF_ROLE_SCREENSHOTS")
                if screenshot_root:
                    Path(screenshot_root).mkdir(parents=True, exist_ok=True)
                    page.locator('a.item[href*="case=ZF-1"]').click()
                    evidence.wait_for()
                    page.screenshot(path=str(Path(screenshot_root) / f"story-{selected}.png"), full_page=True)
                screen_id = page.evaluate(
                    "() => new URLSearchParams(location.hash.split('?')[1]).get('screen')"
                )
                target = f"{base}/app#/screens?screen={screen_id}&case=ZF-1"
                page.goto(base + "/app#/screens")
                page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                page.route("**/api/cases?view=all&limit=20&offset=0",
                           lambda route: route.fulfill(status=503, json={"error": "Synthetic list unavailable. Try again."}),
                           times=1)
                page.goto(target)
                page.get_by_role("heading", name="Workspace unavailable", exact=True).wait_for()
                check("failed list is not an empty success", "Synthetic list unavailable" in page.locator("main").inner_text())
                page.get_by_role("button", name="Try again", exact=True).click()
                evidence.wait_for()
                page.goto(base + "/app#/screens")
                page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                page.route("**/api/cases/ZF-1",
                           lambda route: route.fulfill(status=403, json={"error": "Synthetic access denied. Ask your manager."}),
                           times=1)
                page.goto(target)
                page.get_by_role("heading", name="Workspace unavailable", exact=True).wait_for()
                check("denied detail is explicit and clears old evidence",
                      "Synthetic access denied" in page.locator("main").inner_text()
                      and page.get_by_role("region", name="Evidence for ZF-1").count() == 0)
                held: list[Route] = []
                detail = page.request.get(base + "/api/cases/ZF-1").json()
                page.goto(base + "/app#/screens")
                page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                page.route("**/api/cases/ZF-1", lambda route: held.append(route), times=1)
                page.goto(target)
                page.wait_for_timeout(200)
                check("delayed detail intercepted", len(held) == 1)
                page.evaluate("() => { location.hash = '#/screens'; }")
                page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                held[0].fulfill(json=detail)
                page.wait_for_timeout(100)
                check("late response cannot restore prior selected home",
                      page.get_by_role("region", name="Evidence for ZF-1").count() == 0)
                page.goto(f"{base}/app#/screens?screen={screen_id}&page=100")
                page.get_by_text("No cases on this page. Reset the view or return to your work list.", exact=True).wait_for()
                check("empty page is distinct from failed request", True)
                forbidden_context = browser.new_context()
                try:
                    forbidden = forbidden_context.new_page()
                    forbidden.goto(base + f"/app#/screens?screen={screen_id}")
                    forbidden.locator("#email").fill(
                        "sam@example.test" if selected == "228" else "contractor@example.test"
                    )
                    forbidden.locator("#pw").fill("synthetic-check")
                    forbidden.locator("button[type=submit]").click()
                    forbidden.get_by_role("heading", name="Screen unavailable", exact=True).wait_for()
                    check("actual other identity cannot open specialist module",
                          forbidden.get_by_role("region", name="Evidence for ZF-1").count() == 0)
                finally:
                    forbidden_context.close()
            page.goto(base + "/app#/screens?screen=unavailable")
            page.get_by_role("heading", name="Screen unavailable", exact=True).wait_for()
            check("unknown or uninstalled screen not exposed",
                  "Your access has not changed" in page.locator("main").inner_text())
            page.goto(base + "/app#/screens?page=bad")
            page.get_by_role("heading", name="Invalid screen page", exact=True).wait_for()
            check("malformed pagination refused explicitly", True)
            check(f"specialist reads made no POSTs: {writes}", not writes)
            if selected:
                page.route("**/api/cases?view=all&limit=20&offset=0",
                           lambda route: route.fulfill(status=401, json={"error": "Session ended"}),
                           times=1)
                page.goto(target)
                page.get_by_role("heading", name="Sign in", exact=True).wait_for()
                check("expired session clears authenticated evidence and navigation",
                      not page.locator("#nav").is_visible()
                      and page.get_by_role("region", name="Evidence for ZF-1").count() == 0)
            check(f"no uncaught JavaScript errors: {errors}", not errors)
            print(f"Chromium {browser.version}; synthetic loopback only; selector={selected or 'parent'}")
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, synthetic_data)
