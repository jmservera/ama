"""Keyboard-only walk of the installed specialist screens against an owned synthetic local API.

Refs #134 (C1, C5; AC-034 to AC-043 context). For each constructed fixture login it presses only Tab,
Shift+Tab and Enter from the case list to the Specialist screens entry, a screen, an explicitly
selected home, the labelled evidence region, the handoff link and the Reset screen view recovery
link, and reads the `#workspace-status` text after each state. Logging in as a constructed fixture
role is role selection on synthetic data, not authentication, resident or human acceptance. The
status text is browser DOM evidence, not assistive-technology output. Endpoint and handoff wording
is reported as observed text presence only, never as a pass. Roles or screens that are not served
are listed as gaps, not inferred.
"""

from __future__ import annotations

import re
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import check, main
from checks.workbench_browser_check import MANIFEST, synthetic_data

MAX_TABS = 150
ENTRY = '#nav a[href="#/screens"]'
MENU = 'nav[aria-label="Specialist screens"]'
HOME = "a.item"
REGION = '.screen-evidence [role="region"][aria-label]'
HANDOFF = '.screen-evidence a[href^="#/case/"]'
RESET = "a[data-reset]"
ENDPOINT_TEXT = re.compile(
    r"Cannot confirm readiness|Recorded evidence is complete|Not shown for this role"
    r"|No records supplied"
)
HANDOFF_TEXT = re.compile(r"\bOwner\b|Next action|\bRoute\b|Defect owner|competent reviewer")


def expected_status(role: str, title: str, case_id: str | None) -> str:
    state = f"Selected home {case_id}." if case_id else "No home selected."
    return f"{role}. {title}. {state}"


def status_failures(status: str, role: str, title: str, case_id: str | None) -> list[str]:
    expected = expected_status(role, title, case_id)
    return [] if status.strip() == expected else [f"status {status!r} is not {expected!r}"]


def text_markers(text: str) -> dict[str, bool]:
    return {
        "endpoint_text": bool(ENDPOINT_TEXT.search(text)),
        "handoff_text": bool(HANDOFF_TEXT.search(text)),
    }


def tab_to(page: Page, selector: str, *, back: bool = False, limit: int = MAX_TABS) -> int | None:
    """Press only Tab or Shift+Tab until the selector is focused; return the key count."""
    for count in range(1, limit + 1):
        page.keyboard.press("Shift+Tab" if back else "Tab")
        if page.evaluate("sel => document.activeElement?.matches(sel) ?? false", selector):
            return count
    return None


def focus_visible(page: Page) -> bool:
    return bool(
        page.evaluate(
            """() => { const s = getComputedStyle(document.activeElement);
            return (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2)
              || (s.boxShadow !== 'none' && s.boxShadow !== ''); }"""
        )
    )


def selected_state_failures(page: Page, role: str, title: str, case_id: str) -> list[str]:
    """Static selected-state contract the keyboard walk depends on."""
    failures = status_failures(page.locator("#workspace-status").inner_text(), role, title, case_id)
    if page.locator(RESET).count() == 0:
        failures.append("no Reset screen view recovery link")
    if page.locator(HANDOFF).count() == 0:
        failures.append("no link from the evidence to the existing case workspace")
    for region in page.locator(REGION).all():
        if region.get_attribute("tabindex") != "0":
            failures.append("evidence region is not keyboard focusable")
    return failures


def wait_status(page: Page, text: str) -> None:
    page.wait_for_function(
        "t => document.querySelector('#workspace-status').textContent.trim() === t", arg=text
    )


def login(page: Page, base: str, role: dict[str, Any]) -> None:
    page.goto(base + "/app")
    page.locator("#email").fill(role["email"])
    page.locator("#pw").fill("synthetic-check")
    page.locator("button[type=submit]").click()
    page.get_by_role(
        "heading",
        name="Your jobs" if role["role"] == "Contractor" else "My cases today",
        exact=True,
    ).wait_for()


def screen_links(page: Page) -> list[tuple[str, str]]:
    found = page.locator(f"{MENU} a").evaluate_all(
        "els => els.map(el => [el.getAttribute('href'), el.textContent])"
    )
    return [(href.split("screen=")[1].split("&")[0], title) for href, title in found]


def walk_screen(page: Page, role: str, screen_id: str, title: str) -> dict[str, Any]:
    obs: dict[str, Any] = {"role": role, "screen": screen_id}
    link = f'{MENU} a[href="#/screens?screen={screen_id}"]'
    obs["screen_keys"] = tab_to(page, link, back=True, limit=60) or tab_to(page, link)
    check(f"{role}: {title} reachable by keyboard from the specialist menu", obs["screen_keys"])
    obs["screen_focus_visible"] = focus_visible(page)
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, None))
    obs["status_unselected"] = True
    obs["home_keys"] = tab_to(page, HOME)
    if not obs["home_keys"]:
        obs["gap"] = "no permitted home reachable by keyboard on this screen"
        return obs
    case_id = page.evaluate(
        "() => decodeURIComponent(document.activeElement.getAttribute('href').split('case=')[1]"
        ".split('&')[0])"
    )
    obs["case"] = case_id
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, case_id))
    obs["status_selected"] = True
    failures = selected_state_failures(page, role, title, case_id)
    check(f"{role}: {title} selected-home contract; failures={failures}", not failures)
    body = page.locator(".screen-evidence").inner_text()
    obs.update(text_markers(body))
    obs["region_keys"] = None
    if page.locator(REGION).count():
        obs["region_keys"] = tab_to(page, REGION)
        check(f"{role}: {title} labelled evidence region reachable by Tab", obs["region_keys"])
        obs["region_focus_visible"] = focus_visible(page)
    obs["handoff_keys"] = tab_to(page, HANDOFF)
    check(f"{role}: {title} existing case workspace link reachable by Tab", obs["handoff_keys"])
    obs["reset_keys"] = tab_to(page, RESET, back=True, limit=MAX_TABS)
    check(f"{role}: {title} Reset screen view reachable by Shift+Tab", obs["reset_keys"])
    obs["reset_focus_visible"] = focus_visible(page)
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, None))
    check(
        f"{role}: {title} reset clears the selected home",
        page.locator(".screen-evidence").count() == 0,
    )
    return obs


def negative_controls(page: Page, role: str, screen_id: str, title: str, case_id: str) -> None:
    page.goto(page.url.split("#")[0] + f"#/screens?screen={screen_id}&case={case_id}")
    page.reload()
    wait_status(page, expected_status(role, title, case_id))
    check(
        f"negative control baseline is clean on {role}: {title}",
        not selected_state_failures(page, role, title, case_id),
    )
    page.evaluate("document.querySelectorAll('a[data-reset]').forEach(el => el.remove())")
    check(
        "negative control: a removed recovery link is detected",
        "no Reset screen view recovery link" in selected_state_failures(page, role, title, case_id),
    )
    page.evaluate("document.querySelector('#workspace-status').textContent = ''")
    check(
        "negative control: a blank status is detected",
        any("status" in f for f in selected_state_failures(page, role, title, case_id)),
    )
    page.evaluate(
        "document.querySelectorAll(\"[role='region']\").forEach(el => el.setAttribute('tabindex', '-1'))"
    )
    check(
        "negative control: an unfocusable evidence region is detected and not tabbable",
        "evidence region is not keyboard focusable"
        in selected_state_failures(page, role, title, case_id)
        and tab_to(page, REGION, limit=MAX_TABS) is None,
    )


def run_browser(base: str) -> None:
    served: dict[str, list[str]] = {}
    observations: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        errors: list[str] = []
        control_done = False
        try:
            for role in MANIFEST["roles"]:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                page.on("pageerror", lambda error: errors.append(str(error)))
                login(page, base, role)
                name = role["role"]
                entry = tab_to(page, ENTRY)
                check(f"{name}: Specialist screens entry reachable by Tab", entry is not None)
                check(f"{name}: entry link shows visible focus", focus_visible(page))
                page.keyboard.press("Enter")
                page.locator(MENU).wait_for()
                screens = screen_links(page)
                served[name] = [screen_id for screen_id, _ in screens]
                for screen_id, title in screens:
                    obs = walk_screen(page, name, screen_id, title)
                    observations.append(obs)
                    if not control_done and obs.get("region_keys") and obs.get("case"):
                        control_done = True
                        negative_controls(page, name, screen_id, title, obs["case"])
                        page.goto(base + "/app#/screens")
                        page.locator(MENU).wait_for()
                context.close()
            check(f"no uncaught JavaScript errors in the keyboard walk ({errors})", not errors)
            check("at least one negative control ran against a real region", control_done)
            report(served, observations)
        finally:
            browser.close()


def report(served: dict[str, list[str]], observations: list[dict[str, Any]]) -> None:
    print("OBSERVATIONS (DOM evidence on constructed fixtures; not authentication, not AT output)")
    for role, ids in served.items():
        print(f"role {role}: {len(ids)} screens served: {', '.join(ids) or 'none'}")
    for obs in observations:
        print("OBS", {k: v for k, v in obs.items()})
    gaps = [o for o in observations if o.get("gap")]
    print(f"GAPS: {len(gaps)} walked pairs without a permitted home")
    print("Perspectives without a login role (Asset, Procurement, Auditor) stay proxy/deferred.")
    print("Partial coverage only; no AC is marked passed by this check.")


if __name__ == "__main__":
    main(run_browser, synthetic_data)
