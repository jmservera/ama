"""Keyboard-only walk of the installed specialist screens against an owned synthetic local API.

Refs #134 (C1, C5; AC-034 to AC-043 context). For each constructed fixture login it presses only Tab,
Shift+Tab and Enter from the case list to the Specialist screens entry, a screen, an explicitly
selected home, the labelled evidence region, the handoff link and the Reset screen view recovery
link. It asserts measured focus visibility at every reached target, the `#workspace-status` text
plus role=status, aria-live=polite and aria-atomic=true on each state, and that the evidence tables
(enumerated by tag, independent of label and tabindex) match the declared per-screen fixture
expectation, each reached by Tab. Run-only mutations must be rejected by those same walk assertions.
Logging in as a constructed fixture
role is role selection on synthetic data, not authentication, resident or human acceptance. The
status text is browser DOM evidence, not assistive-technology output. Endpoint and handoff wording
is reported as observed text presence only, never as a pass. Roles or screens that are not served
are listed as gaps, not inferred. Screens with no table on this fixture are declared gaps.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import check, main
from checks.workbench_browser_check import MANIFEST, synthetic_data

MAX_TABS = 150
ENTRY = '#nav a[href="#/screens"]'
MENU = 'nav[aria-label="Specialist screens"]'
HOME = "a.item"
HANDOFF = '.screen-evidence a[href^="#/case/"]'
RESET = "a[data-reset]"
ENDPOINT_TEXT = re.compile(
    r"Cannot confirm readiness|Recorded evidence is complete|Not shown for this role"
    r"|No records supplied"
)
HANDOFF_TEXT = re.compile(r"\bOwner\b|Next action|\bRoute\b|Defect owner|competent reviewer")
STATUS_ATTRS = {"role": "status", "aria-live": "polite", "aria-atomic": "true"}
# Declared from the owned constructed fixture (discovery run 2026-11-10); a lost, added or
# relabelled region fails the walk instead of silently reducing coverage.
EXPECTED_REGIONS: dict[str, tuple[str, ...]] = {
    "resident-choice": ("Measure choices by version",),
    "hazard-triage": ("Hazard referrals for this home", "Scoped pause and release evidence"),
    "asset-board": ("Investment inputs", "Phase checks and benefits"),
    "programme-queue": ("Same-home step states",),
    "technical-queue": ("Sign-off validity after design changes",),
    "safety-lead": ("Hazard referrals for this home", "Scoped pause and release evidence"),
    "data-operator": ("Open exceptions and prerequisites",),
    "contractor-job-pack": ("Evidence checklist for this job pack",),
}
# Legitimate no-table states on this fixture. They are gaps, not passes and not invented tables.
NO_REGION_GAPS: dict[str, str] = {
    screen: "fixture renders no evidence table for the selected home"
    for screen in (
        "resident-service-issues",
        "quality-queue",
        "procurement-packages",
        "finance-invoices",
        "finance-funding",
        "staff-job-pack-intake",
    )
}


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


def _tab(page: Page, expr: str, arg: Any, back: bool, limit: int) -> int | None:
    for count in range(1, limit + 1):
        page.keyboard.press("Shift+Tab" if back else "Tab")
        if page.evaluate(expr, arg):
            return count
    return None


def tab_to(page: Page, selector: str, *, back: bool = False, limit: int = MAX_TABS) -> int | None:
    """Press only Tab or Shift+Tab until the selector is focused; return the key count."""
    return _tab(page, "sel => document.activeElement?.matches(sel) ?? false", selector, back, limit)


def tab_to_region(page: Page, index: int) -> int | None:
    """Tab to the wrapper of the index-th evidence table, enumerated by the table tag."""
    expr = (
        "i => document.activeElement === document.querySelectorAll('.screen-evidence table')[i]"
        "?.closest('.table-scroll, [role=region]')"
    )
    return _tab(page, expr, index, False, MAX_TABS)


def transparent(colour: str) -> bool:
    return colour.strip() == "transparent" or bool(re.search(r",\s*0\)$", colour.strip()))


def width_px(value: str | None) -> float:
    match = re.match(r"\s*([0-9.]+)", value or "")
    return float(match.group(1)) if match else 0.0


SHADOW_RING = re.compile(r"^rgba?\(([^)]*)\) 0px 0px 0px ([0-9.]+)px$")


def ring_shadow(value: str) -> bool:
    """Only the supported computed ring shape: one coloured, centred, blur-free shadow of 2px+."""
    match = SHADOW_RING.match(value.strip())
    if not match:
        return False
    channels = [part.strip() for part in match.group(1).split(",")]
    alpha = float(channels[3]) if len(channels) == 4 else 1.0
    return alpha > 0 and float(match.group(2)) >= 2


def focus_failures(style: dict[str, str]) -> list[str]:
    """A visible indicator is a non-transparent outline of 2px or more, or a coloured shadow."""
    outline = (
        style.get("outlineStyle") not in (None, "none", "hidden")
        and width_px(style.get("outlineWidth")) >= 2
        and not transparent(style.get("outlineColor") or "transparent")
    )
    shadow = ring_shadow(style.get("boxShadow") or "")
    return [] if outline or shadow else [f"no measured visible focus indicator: {style}"]


def status_contract_failures(
    attrs: Mapping[str, str | None], text: str, role: str, title: str, case_id: str | None
) -> list[str]:
    failures = status_failures(text, role, title, case_id)
    for name, want in STATUS_ATTRS.items():
        if attrs.get(name) != want:
            failures.append(f"#workspace-status {name}={attrs.get(name)!r} is not {want!r}")
    return failures


def region_failures(screen_id: str, found: Sequence[Mapping[str, str | None]]) -> list[str]:
    """Compare tables enumerated by tag with the declared fixture expectation for the screen."""
    if screen_id in NO_REGION_GAPS:
        expected: tuple[str, ...] = ()
    elif screen_id in EXPECTED_REGIONS:
        expected = EXPECTED_REGIONS[screen_id]
    else:
        return [f"screen {screen_id} has no declared region expectation or declared gap"]
    failures = []
    for entry in found:
        label = entry.get("label") or ""
        if entry.get("role") != "region":
            failures.append(f"table {label!r} is not inside a role=region wrapper")
        if not label.strip():
            failures.append("an evidence table region has no accessible label")
        if entry.get("tabindex") != "0":
            failures.append(f"evidence region {label!r} is not keyboard focusable")
    labels = sorted(e.get("label") or "" for e in found)
    if labels != sorted(expected):
        failures.append(f"evidence regions {labels} differ from declared {sorted(expected)}")
    return failures


# Inline CSSOM edits on the focused element; an injected <style> is not applied under the page CSP.
FOCUS_SCRIPT = """kind => {
  const style = document.activeElement.style;
  if (kind === 'transparent-shadow') {
    style.setProperty('box-shadow', 'rgba(0, 90, 158, 0) 0px 0px 0px 2px', 'important');
    style.setProperty('outline', 'none', 'important');
    const now = getComputedStyle(document.activeElement);
    if (now.boxShadow !== 'rgba(0, 90, 158, 0) 0px 0px 0px 2px' || now.outlineStyle !== 'none')
      throw new Error('transparent-shadow mutation not in effect: ' + now.boxShadow);
    return;
  }
  style.setProperty('box-shadow', 'none', 'important');
  if (kind === 'transparent') style.setProperty('outline-color', 'transparent', 'important');
  else style.setProperty('outline', 'none', 'important');
}"""


@dataclass(frozen=True)
class Sabotage:
    """A run-only DOM mutation applied at one stage; the same walk assertion must reject it."""

    stage: str
    script: str
    arg: str | None
    expect: str


def focus_off(stage: str, kind: str = "none") -> Sabotage:
    return Sabotage(stage, FOCUS_SCRIPT, kind, "focus visible at " + stage)


def hook(page: Page, sabotage: Sabotage | None, stage: str) -> None:
    if sabotage and sabotage.stage == stage:
        page.evaluate(sabotage.script, sabotage.arg)


def assert_focus(page: Page, label: str, stage: str, sabotage: Sabotage | None = None) -> bool:
    hook(page, sabotage, stage)
    page.wait_for_function("() => document.getAnimations().every(a => a.playState !== 'running')")
    style = page.evaluate(
        """() => { const s = getComputedStyle(document.activeElement);
        return {outlineStyle: s.outlineStyle, outlineWidth: s.outlineWidth,
          outlineColor: s.outlineColor, boxShadow: s.boxShadow}; }"""
    )
    failures = focus_failures(style)
    check(f"{label}: focus visible at {stage}; failures={failures}", not failures)
    return True


def assert_status(
    page: Page,
    role: str,
    title: str,
    case_id: str | None,
    stage: str,
    sabotage: Sabotage | None = None,
) -> None:
    hook(page, sabotage, stage)
    found = page.evaluate(
        """() => { const el = document.querySelector('#workspace-status');
        return {text: el.textContent, attrs: {role: el.getAttribute('role'),
          'aria-live': el.getAttribute('aria-live'),
          'aria-atomic': el.getAttribute('aria-atomic')}}; }"""
    )
    failures = status_contract_failures(found["attrs"], found["text"], role, title, case_id)
    check(f"{role}: {title} status contract at {stage}; failures={failures}", not failures)


def region_inventory(page: Page) -> list[dict[str, str | None]]:
    return list(
        page.evaluate(
            """() => [...document.querySelectorAll('.screen-evidence table')].map(t => {
            const w = t.closest('.table-scroll, [role=region]');
            return {label: w ? (w.getAttribute('aria-label') || '') : '',
              tabindex: w ? w.getAttribute('tabindex') : null,
              role: w ? w.getAttribute('role') : null}; })"""
        )
    )


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


def walk_screen(
    page: Page, role: str, screen_id: str, title: str, sabotage: Sabotage | None = None
) -> dict[str, Any]:
    obs: dict[str, Any] = {"role": role, "screen": screen_id}
    label = f"{role}: {title}"
    link = f'{MENU} a[href="#/screens?screen={screen_id}"]'
    obs["screen_keys"] = tab_to(page, link, back=True, limit=60) or tab_to(page, link)
    check(f"{label} reachable by keyboard from the specialist menu", obs["screen_keys"])
    assert_focus(page, label, "screen", sabotage)
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, None))
    assert_status(page, role, title, None, "unselected", sabotage)
    obs["home_keys"] = tab_to(page, HOME)
    check(f"{label} a permitted home is reachable by keyboard", obs["home_keys"])
    assert_focus(page, label, "home", sabotage)
    case_id = page.evaluate(
        "() => decodeURIComponent(document.activeElement.getAttribute('href').split('case=')[1]"
        ".split('&')[0])"
    )
    obs["case"] = case_id
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, case_id))
    assert_status(page, role, title, case_id, "selected", sabotage)
    obs.update(text_markers(page.locator(".screen-evidence").inner_text()))
    hook(page, sabotage, "regions")
    found = region_inventory(page)
    failures = region_failures(screen_id, found)
    check(f"{label} evidence regions match the declared fixture; failures={failures}", not failures)
    obs["regions"] = [entry["label"] for entry in found]
    if screen_id in NO_REGION_GAPS:
        obs["no_region_gap"] = NO_REGION_GAPS[screen_id]
    obs["region_keys"] = []
    for index, entry in enumerate(found):
        keys = tab_to_region(page, index)
        check(f"{label} region {entry['label']!r} reachable by Tab", keys is not None)
        assert_focus(page, label, "region", sabotage)
        obs["region_keys"].append(keys)
    obs["handoff_keys"] = tab_to(page, HANDOFF)
    check(f"{label} existing case workspace link reachable by Tab", bool(obs["handoff_keys"]))
    assert_focus(page, label, "handoff", sabotage)
    hook(page, sabotage, "before-reset")
    obs["reset_keys"] = tab_to(page, RESET, back=True, limit=MAX_TABS)
    check(f"{label} Reset screen view reachable by Shift+Tab", obs["reset_keys"])
    assert_focus(page, label, "reset", sabotage)
    page.keyboard.press("Enter")
    wait_status(page, expected_status(role, title, None))
    assert_status(page, role, title, None, "reset-status", sabotage)
    check(f"{label} reset clears the selected home", page.locator(".screen-evidence").count() == 0)
    return obs


def fresh(page: Page, base: str) -> None:
    page.goto(base + "/app#/screens")
    page.reload()
    page.locator(MENU).wait_for()


def status_off(stage: str, attribute: str) -> Sabotage:
    script = "a => document.querySelector('#workspace-status').removeAttribute(a)"
    return Sabotage(stage, script, attribute, "status contract at " + stage)


def region_edit(script: str, expect: str) -> Sabotage:
    return Sabotage("regions", f"() => {{ {script} }}", None, expect)


def negative_controls(page: Page, base: str, role: str, screens: list[tuple[str, str]]) -> int:
    """Each run-only mutation must be rejected by the same walk assertion that production uses."""
    titles = dict(screens)
    two = "safety-lead"
    one = "technical-queue"
    wrappers = "[...document.querySelectorAll('.screen-evidence .table-scroll')]"
    controls: list[tuple[str, str, Sabotage]] = [
        ("focus style removed on a home link", two, focus_off("home")),
        ("focus style removed on an evidence region", two, focus_off("region")),
        ("focus style removed on the handoff link", two, focus_off("handoff")),
        ("focus style removed on the reset link", two, focus_off("reset")),
        ("focus made transparent on a screen link", two, focus_off("screen", "transparent")),
        (
            "focus shadow transparent, not none, on a home link",
            two,
            focus_off("home", "transparent-shadow"),
        ),
        ("status role removed, text kept", two, status_off("unselected", "role")),
        ("status role removed at reset, text kept", two, status_off("reset-status", "role")),
        ("status aria-live removed, text kept", two, status_off("selected", "aria-live")),
        ("status aria-atomic removed, text kept", two, status_off("selected", "aria-atomic")),
        (
            "evidence region label removed",
            two,
            region_edit(
                f"{wrappers}.forEach(w => w.removeAttribute('aria-label'));",
                "evidence regions match the declared fixture",
            ),
        ),
        (
            "evidence region made unfocusable",
            two,
            region_edit(
                f"{wrappers}.forEach(w => w.setAttribute('tabindex', '-1'));",
                "evidence regions match the declared fixture",
            ),
        ),
        (
            "one of two evidence regions removed",
            two,
            region_edit(f"{wrappers}[0].remove();", "evidence regions match the declared fixture"),
        ),
        (
            "the only evidence region removed",
            one,
            region_edit(f"{wrappers}.forEach(w => w.remove());", "evidence regions match"),
        ),
        (
            "recovery link removed",
            two,
            Sabotage(
                "before-reset",
                "() => document.querySelectorAll('a[data-reset]').forEach(el => el.remove())",
                None,
                "Reset screen view reachable",
            ),
        ),
    ]
    fresh(page, base)
    walk_screen(page, role, two, titles[two])
    for name, screen, sabotage in controls:
        fresh(page, base)
        try:
            walk_screen(page, role, screen, titles[screen], sabotage)
        except AssertionError as error:
            check(f"negative control rejected by the walk: {name}", sabotage.expect in str(error))
        else:
            check(f"negative control rejected by the walk: {name}", False)
    return len(controls)


def run_browser(base: str) -> None:
    served: dict[str, list[str]] = {}
    observations: list[dict[str, Any]] = []
    negatives = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        errors: list[str] = []
        try:
            for role in MANIFEST["roles"]:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                page.on("pageerror", lambda error: errors.append(str(error)))
                login(page, base, role)
                name = role["role"]
                entry = tab_to(page, ENTRY)
                check(f"{name}: Specialist screens entry reachable by Tab", entry is not None)
                assert_focus(page, f"{name}: Specialist screens entry", "entry")
                page.keyboard.press("Enter")
                page.locator(MENU).wait_for()
                screens = screen_links(page)
                served[name] = [screen_id for screen_id, _ in screens]
                for screen_id, title in screens:
                    observations.append(walk_screen(page, name, screen_id, title))
                if {"safety-lead", "technical-queue"} <= set(served[name]) and not negatives:
                    negatives = negative_controls(page, base, name, screens)
                context.close()
            check(f"no uncaught JavaScript errors in the keyboard walk ({errors})", not errors)
            check(
                "negative controls ran against real two-region and one-region screens",
                negatives > 0,
            )
            report(served, observations, negatives)
        finally:
            browser.close()


def report(
    served: dict[str, list[str]], observations: list[dict[str, Any]], negatives: int
) -> None:
    print("OBSERVATIONS (DOM evidence on constructed fixtures; not authentication, not AT output)")
    for role, ids in served.items():
        print(f"role {role}: {len(ids)} screens served: {', '.join(ids) or 'none'}")
    for obs in observations:
        print("OBS", {k: v for k, v in obs.items()})
    gaps = [o for o in observations if o.get("no_region_gap")]
    print(f"NEGATIVES: {negatives} mutations rejected by the same walk assertions")
    print(f"GAPS: {len(gaps)} walks on declared no-evidence-table states (not passes)")
    print("Perspectives without a login role (Asset, Procurement, Auditor) stay proxy/deferred.")
    print("Partial coverage only; no AC is marked passed by this check.")


if __name__ == "__main__":
    main(run_browser, synthetic_data)
