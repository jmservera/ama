"""Exercise installed specialist screens against an owned synthetic local API."""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

from playwright.sync_api import Browser, Page, Route, sync_playwright

from checks.design_system_browser_check import check, main
from checks.role_screens_fixtures import synthetic_data, technical_quality_data

# Independent child branches extend only their own installed-screen expectation.
SCENARIOS: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "231": (
        "quality@example.test",
        "Technical queue",
        (
            "Cannot confirm readiness",
            "Evidence: EPC",
            "Current design version",
            "Needs reassessment",
            "Retrofit Coordinator (competent reviewer for this sign-off, not a generic approval)",
            "Coordination sign-off (not given)",
        ),
    ),
    "231q": (
        "quality@example.test",
        "Quality queue",
        (
            "Cannot confirm readiness",
            "Loft insulation: Returned",
            "Defect owner",
            "Test Ltd",
            "Awaiting independent reinspection",
            "No evidence",
            "SYN photo 14",
        ),
    ),
    "232": (
        "sam@example.test",
        "Resident choice and update queue",
        (
            "Loft insulation",
            "Paused or withdrawn by the resident",
            "SYN resident requested time",
            "SYN-SAFE-232",
            "SYN-REQUEST-232",
            "Large print",
        ),
    ),
}


AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
STORY_231 = ("231", "231q")


def check_readonly_accessibility(page: Page, story: str) -> None:
    """Keyboard reachability, text-only state meaning and optional pinned axe scan."""
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    text = evidence.inner_text()
    check(f"{story} reader view has no write controls",
          evidence.locator("button, form, input, select, textarea").count() == 0)
    check(f"{story} state is stated in text, not colour alone",
          "Cannot confirm readiness" in text and evidence.locator(".blocked-title").count() == 1)
    check(f"{story} no ready state is shown over missing evidence",
          "Recorded evidence is complete" not in text and "Every measure has accepted evidence" not in text)
    regions = evidence.locator('div.table-scroll[role="region"]')
    expected = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check(f"{story} every table is a labelled focusable region",
          bool(expected) and regions.evaluate_all(
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
    check(f"{story} keyboard Tab reaches every table region: {reached}", len(reached) == len(expected))
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


def check_projected_queue(browser: Browser, base: str) -> None:
    for email in ("sam@example.test", "contractor@example.test"):
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
            page.get_by_role(
                "heading", name="Your jobs" if email.startswith("contractor") else "My cases today",
                exact=True,
            ).wait_for()
            page.on("request", lambda request: writes.append(request.url) if request.method == "POST" else None)
            projected = page.request.get(base + "/api/cases?view=all&limit=20&offset=0").json()
            page.evaluate("""() => {
              registerRoleScreen({id: "synthetic-queue-check", title: "Synthetic queue check",
                roles: [me.user.role], render: () => h("p", {}, "Synthetic recorded evidence")});
              location.hash = "#/screens?screen=synthetic-queue-check";
            }""")
            page.get_by_text("No home selected. Choose a home from this queue.", exact=True).wait_for()
            queue = page.locator('section[aria-labelledby="screen-queue-heading"]')
            check(f"{email} queue retains all projected rows",
                  queue.locator("a.item").count() == len(projected["items"]) > 0)
            for row in projected["items"]:
                link = queue.locator(f'a.item[href*="case={row["id"]}"]')
                check(f"{email} {row['id']} marker matches projected safety",
                      link.locator(".flag.danger").count() == int(bool(row.get("hazard"))))
                work = row.get("work")
                if work is None:
                    check(f"{email} {row['id']} no work is invented",
                          link.locator(".work-context, .safety-clock").count() == 0)
                    continue
                text = link.inner_text()
                check(f"{email} {row['id']} retains recorded owner and next action",
                      f"Current owner: {work['owner']}" in text
                      and f"Next action: {work['next_action']}" in text)
                check(f"{email} {row['id']} retains every clock",
                      link.locator(".safety-clock").count() == len(work["hazard_clocks"]))
                for clock in work["hazard_clocks"]:
                    for field in ("aware_at", "owner", "response_due_at", "resident_update_due_at"):
                        check(f"{email} {row['id']} clock {field} remains visible", clock[field] in text)
                    check(f"{email} {row['id']} external timing authority remains visible",
                          f"{clock['authority']} owns timing." in text)
            if email.startswith("contractor"):
                check("actual contractor projection withholds staff safety context",
                      all("work" not in row and "hazard" not in row for row in projected["items"]))
            else:
                check("staff fixture exercises an actual open safety clock",
                      any(row["hazard"] and row["work"]["hazard_clocks"] for row in projected["items"]))
                check("projected safety marker has non-colour text",
                      queue.locator(".flag.danger").first.inner_text() == "Safety issue open")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                check(f"{email} queue context reflow {width}px",
                      page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
            link = queue.locator("a.item").first
            page.keyboard.press("Tab")
            link.focus()
            check(f"{email} queue native focus visible",
                  link.evaluate("el => getComputedStyle(el).outlineStyle === 'solid'"))
            check(f"{email} queue made no writes: {writes}", not writes)
            check(f"{email} queue has no JavaScript errors: {errors}", not errors)
        finally:
            context.close()

PROGRAMME_STEPS = ("Technical", "Resident", "Delivery", "Quality", "Finance")
PROGRAMME_STATES = ("Blocked", "No recorded blocker")


def programme_data() -> dict:
    data = synthetic_data()
    case = data["cases"][0]
    # The shared fixture's return targets another stage; make it the active return for this home.
    case["returns"][0]["to_stage"] = case["stage"]
    case["returns"][0]["by"] = "SYN sender"
    return data


def load_axe() -> str | None:
    path = os.environ.get("ZF_AXE_JS")
    if not path:
        return None
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Unexpected axe 4.10.3 bytes")
    return raw.decode()


def scan_main(page, axe: str | None, state: str) -> None:
    if axe is None:
        print(f"SKIP axe {state}: set ZF_AXE_JS to the pinned axe 4.10.3 file", flush=True)
        return
    page.evaluate(axe)
    result = page.evaluate(
        """async () => await axe.run(document.querySelector('main') || document, {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a',
            'wcag21aa', 'wcag22aa']}})"""
    )
    found = [f"{v['id']}:{v['impact']}" for v in result["violations"]]
    check(f"axe finds no violations in {state}: {found}", not found)


def focus_outline(page) -> bool:
    return bool(page.evaluate(
        """() => { const s = getComputedStyle(document.activeElement);
          return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2; }"""
    ))


def check_programme(browser: Browser, base: str, axe: str | None) -> None:
    for email in ("pam@example.test", "coordinator@example.test"):
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        try:
            page = context.new_page()
            errors: list[str] = []
            writes: list[str] = []
            page.on("pageerror", lambda error, sink=errors: sink.append(str(error)))
            page.goto(base + "/app")
            page.locator("#email").fill(email)
            page.locator("#pw").fill("synthetic-check")
            page.locator("button[type=submit]").click()
            page.get_by_role("link", name="Specialist screens", exact=True).wait_for()
            page.on("request", lambda r, sink=writes: sink.append(r.url) if r.method != "GET" else None)
            before = page.request.get(base + "/api/cases/ZF-1").json()
            page.goto(base + "/app#/screens?screen=programme-queue")
            page.get_by_role("heading", name="Programme queue and connected home view",
                             exact=True).wait_for()
            table = page.get_by_role("table", name="Shared queue: returned and handed-off work")
            table.wait_for()
            text = table.inner_text()
            detail = ("SYN missing roof reference", "SYN sender") if email.startswith("pam") \
                else ("Held for roles with a recorded need",)
            for phrase in ("ZF-1", *detail,
                           "Proposed receiver (not a confirmed owner)",
                           "Chase owner (chases the receiver)",
                           "Resident-update owner (updates the resident)"):
                check(f"{email} queue shows {phrase}", phrase in text)
            check(f"{email} no role simulator or switcher in the user view",
                  page.get_by_text("Simulate", exact=False).count() == 0
                  and page.get_by_role("combobox", name="Role").count() == 0)
            scan_main(page, axe, f"{email} programme overview")

            scope = page.locator("#programme-scope")
            scope.focus()
            check(f"{email} scope select shows a visible focus", focus_outline(page))
            page.keyboard.type("Blocked")
            page.keyboard.press("Tab")
            apply = page.get_by_role("button", name="Apply filter", exact=True)
            check(f"{email} Tab reaches Apply filter", apply.evaluate("el => el === document.activeElement"))
            check(f"{email} Apply filter shows a visible focus", focus_outline(page))
            page.keyboard.press("Enter")
            status = page.locator("#programme-filter-status")
            check(f"{email} keyboard Apply states the scope and no change",
                  "Scope: Blocked work" in status.inner_text()
                  and "no record is changed" in status.inner_text())
            check(f"{email} scope is kept in the address", "scope=blocked" in page.url)
            page.keyboard.press("Tab")
            reset = page.get_by_role("button", name="Reset to default view", exact=True)
            check(f"{email} Tab reaches Reset", reset.evaluate("el => el === document.activeElement"))
            check(f"{email} Reset shows a visible focus", focus_outline(page))
            page.keyboard.press("Shift+Tab")
            check(f"{email} Shift+Tab leaves Reset (no keyboard trap)",
                  apply.evaluate("el => el === document.activeElement"))
            page.keyboard.press("Tab")
            page.keyboard.press("Space")
            check(f"{email} keyboard Reset restores the default scope",
                  scope.input_value() == "default" and "scope=" not in page.url
                  and "Returned and handed-off work (default)" in status.inner_text())
            after = page.request.get(base + "/api/cases/ZF-1").json()
            check(f"{email} filter and reset change no record", before == after and not writes)

            page.goto(base + "/app#/screens?screen=programme-queue&case=ZF-1")
            region = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
            region.wait_for()
            steps = region.get_by_role("table", name="Same-home step states")
            steps.wait_for()
            rows = steps.locator("tbody tr")
            check(f"{email} five independent steps", rows.count() == 5)
            blocked = 0
            for index, step in enumerate(PROGRAMME_STEPS):
                cells = rows.nth(index).locator("th, td")
                state = cells.nth(1).inner_text()
                check(f"{email} {step} step has a textual state: {state}",
                      cells.nth(0).inner_text() == step and state.startswith(PROGRAMME_STATES))
                blocked += state.startswith("Blocked")
            check(f"{email} at least one gate is blocked in text", blocked > 0)
            check(f"{email} connected view makes no readiness claim",
                  "does not confirm readiness" in region.inner_text()
                  or "blocked" in region.inner_text())
            scan_main(page, axe, f"{email} connected home view")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                check(f"{email} programme reflow {width}px",
                      page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
            page.keyboard.press("Tab")
            check(f"{email} connected view makes no writes: {writes}", not writes)
            check(f"{email} programme screen has no JavaScript errors: {errors}", not errors)
        finally:
            context.close()


def run_browser(base: str) -> None:
    selected = sys.argv[1] if len(sys.argv) > 1 else None
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            if selected == "230":
                check_programme(browser, base, load_axe())
                print(f"Chromium {browser.version}; synthetic loopback only; selector=230")
                return
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
                installed = page.locator("nav[aria-label='Specialist screens'] a").count()
                check("parent registry is explicit: empty message or installed screen links",
                      installed > 0 or "No specialist screens are installed" in page.locator("main").inner_text())
                main_text = page.locator("main").inner_text()
                check("Resident Liaison Officer sees only the registered triage screen",
                      "Repairs and hazard triage" in main_text
                      and "Building safety referral queue" not in main_text
                      and "No specialist screens are installed" not in main_text)
                check_projected_queue(browser, base)
            else:
                _, screen, expected = SCENARIOS[selected]
                page.get_by_role("link", name=screen, exact=True).click()
                page.get_by_text("No home selected. Choose a home from this queue.", exact=True).wait_for()
                check("specialist navigation does not inherit white header text",
                      page.locator(".screen-links a").first.evaluate(
                          "el => getComputedStyle(el).color !== 'rgb(255, 255, 255)'"
                      ))
                check("no automatic selection or detail fetch", "case=" not in page.url)
                if selected == "232":
                    summary = page.get_by_role("region", name="Choice and update commitments by home", exact=True)
                    summary.wait_for()
                    summary_text = summary.inner_text()
                    check("232 queue summary lists ZF-1 choice, pause and update commitment",
                          "ZF-1" in summary_text and "Loft insulation" in summary_text
                          and "SYN-SAFE-232" in summary_text)
                    check("232 queue summary has no contact links",
                          summary.locator('a[href^="tel:"], a[href^="mailto:"], button').count() == 0)
                page.locator('a.item[href*="case=ZF-1"]').click()
                evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
                evidence.wait_for()
                text = evidence.inner_text()
                for phrase in expected:
                    check(f"story {selected} exact evidence: {phrase}", phrase in text)
                check("same home remains ZF-1", "Selected home ZF-1" in text)
                if selected in STORY_231:
                    check_readonly_accessibility(page, selected)
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
    story = sys.argv[1] if len(sys.argv) > 1 else None
    main(
        run_browser,
        technical_quality_data if story in STORY_231
        else programme_data if story == "230" else synthetic_data,
    )
