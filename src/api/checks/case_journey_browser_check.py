"""Synthetic real-server journey, tab, keyboard, axe and actual browser-zoom checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, Route, sync_playwright

from checks.design_system_browser_check import check, main
from checks.regulatory_ux_check import AXE_SHA256
from checks.workbench_browser_check import synthetic_data


def journey_data() -> dict[str, Any]:
    data = synthetic_data()
    for case in data["cases"]:
        for document in case.get("documents", []):
            document.setdefault("name", f"{document['id']}.txt")
            document.setdefault("mime", "text/plain")
    return data


def tab(page: Page, name: str) -> None:
    page.get_by_role("tab", name=name, exact=False).click()


def sign_in(page: Page, base: str) -> None:
    page.goto(base + "/app#/case/ZF-1?tab=overview")
    page.locator("#email").fill("sam@example.test")
    page.locator("#pw").fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()
    page.get_by_role("tab", name="Overview", exact=True).wait_for()


def scan(page: Page, axe: str, reports: list[dict[str, Any]], state: str) -> None:
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async () => await axe.run(document.querySelector('main'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a',
            'wcag21aa', 'wcag22aa']}})"""
    )
    serious = [item for item in result["violations"] if item["impact"] in ("serious", "critical")]
    reports.append(
        dict(
            state=state,
            violations=result["violations"],
            incomplete=result["incomplete"],
            passes=len(result["passes"]),
        )
    )
    check(f"axe no serious/critical: {state}", not serious)


def run_browser(base: str, axe: str, out: Path) -> None:
    reports: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
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
        page.on("dialog", lambda dialog: dialog.accept())
        try:
            sign_in(page, base)
            page.wait_for_function(
                "() => !document.querySelector('[data-case-ai-summary]')"
                ".textContent.includes('Loading assistance')"
            )
            check(
                "one h1 and six ordered journey items",
                page.locator("main h1").count() == 1 and page.locator(".stepper > li").count() == 6,
            )
            check(
                "one current step and all steps navigate",
                page.locator('.stepper [aria-current="step"]').count() == 1
                and page.locator(".stepper a[href]").count() == 6,
            )
            summary_bottom = page.locator(".case-summary").evaluate(
                "el => el.getBoundingClientRect().bottom"
            )
            check(f"all summary values fit 1280x800 ({summary_bottom})", summary_bottom <= 800)
            check("all six summary values", page.locator(".case-summary dt").count() == 6)
            page.screenshot(path=str(out / "desktop-1280.png"))
            check(
                "nine tabs, one selected and one tab stop",
                page.get_by_role("tab").count() == 9
                and page.locator("[role=tab][aria-selected=true]").count() == 1
                and page.locator('[role=tab][tabindex="0"]').count() == 1,
            )
            first = page.get_by_role("tab", name="Overview", exact=True)
            first.focus()
            first.press("ArrowRight")
            check(
                "arrows focus without activation",
                page.locator(":focus").get_attribute("id") == "case-tab-blockers"
                and first.get_attribute("aria-selected") == "true",
            )
            page.keyboard.press("Enter")
            page.wait_for_url("**?tab=blockers")
            check("Enter activates focused tab", "tab=blockers" in page.url)
            page.keyboard.press("End")
            page.keyboard.press("Space")
            page.wait_for_url("**?tab=history")
            check("End and Space activate History", "tab=history" in page.url)
            page.keyboard.press("Home")
            page.keyboard.press("Enter")
            page.get_by_role("button", name="Open next action", exact=True).click()
            check(
                "summary jump focuses panel heading",
                page.locator(":focus").evaluate(
                    "el => el.tagName === 'H2' && !el.closest('[hidden]')"
                ),
            )
            tab(page, "Resident")
            page.locator("#outcome").fill("Unsaved synthetic call")
            page.get_by_role("button", name="Plain visit template", exact=True).click()
            page.get_by_role("textbox", name="Draft message", exact=True).fill("Edited template")
            original = page.locator("#resident-draft-output").element_handle()
            tab(page, "AI assistance")
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.get_by_role("tab", name="AI assistance").wait_for()
            tab(page, "Resident")
            check(
                "unrelated refresh preserves call and complete dynamic draft",
                page.locator("#outcome").input_value() == "Unsaved synthetic call"
                and page.get_by_role("textbox", name="Draft message", exact=True).input_value()
                == "Edited template"
                and page.locator("#resident-draft-output").evaluate(
                    "(el, old) => el === old", original
                ),
            )
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_function("() => document.querySelector('#outcome').value === ''")
            check(
                "successful call clears itself, not unrelated draft",
                page.get_by_role("textbox", name="Draft message", exact=True).input_value()
                == "Edited template",
            )
            tab(page, "History")
            check(
                "saved call reaches actual history",
                "Unsaved synthetic call" in page.locator("#case-panel-history").inner_text(),
            )
            tab(page, "Resident")
            with page.expect_response("**/api/cases/ZF-1/ai") as draft_response:
                page.get_by_role("button", name="Draft with AI", exact=True).click()
            if draft_response.value.status != 200:
                raise AssertionError(f"Draft API failed: {draft_response.value.text()}")
            page.wait_for_function(
                "() => !document.querySelector('#resident-draft-output')"
                ".textContent.includes('Working on it')"
            )
            if page.locator("#resident-draft-output .err").count():
                raise AssertionError(page.locator("#resident-draft-output").inner_text())
            page.get_by_role("textbox", name="Draft", exact=True).wait_for()
            card = page.locator("#resident-draft-output .ai-suggestion")
            check(
                "AI card exact warning and missing confidence",
                "AI suggestion, not approved. Not an instruction." in card.inner_text()
                and "Confidence: not provided" in card.inner_text(),
            )
            record = card.get_attribute("data-record-id")
            page.get_by_role("textbox", name="Draft", exact=True).fill("Edited synthetic wording")
            card.get_by_role("button", name="Edit", exact=True).click()
            check(
                "edit requires linked reason",
                card.get_by_label("Reason", exact=True).get_attribute("aria-invalid") == "true",
            )
            card.get_by_label("Reason", exact=True).fill("Checked wording")
            tab(page, "AI assistance")
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.get_by_role("tab", name="AI assistance").wait_for()
            tab(page, "Resident")
            check(
                "AI record and review context survive refresh",
                card.get_attribute("data-record-id") == record
                and card.get_by_label("Reason", exact=True).input_value() == "Checked wording"
                and page.get_by_role("textbox", name="Draft", exact=True).input_value()
                == "Edited synthetic wording",
            )
            card.get_by_role("button", name="Edit", exact=True).click()
            page.wait_for_function(
                "() => document.querySelector('#resident-draft-output .aimeta')"
                ".dataset.reviewState === 'Edited'"
            )
            check(
                "recorded edit keeps approval boundary",
                "not an approval, consent or safety" in card.inner_text(),
            )
            tab(page, "Overview")
            page.reload()
            page.get_by_role("tab", name="Overview", exact=True).wait_for()
            check("tab URL survives document refresh", "tab=overview" in page.url)
            tab(page, "Funding")
            tab(page, "History")
            page.go_back()
            page.get_by_role("tabpanel", name="Funding", exact=True).wait_for()
            check("browser Back restores retained tab", True)

            held: list[Route] = []
            page.route("**/api/cases/ZF-1", lambda route: held.append(route))
            page.reload(wait_until="domcontentloaded")
            page.locator('[aria-label="Case summary"][aria-busy=true]').wait_for()
            check(
                "loading case has explicit busy state and no tabs",
                page.get_by_role("tab").count() == 0,
            )
            scan(page, axe, reports, "loading")
            response = page.request.get(base + "/api/cases/ZF-1")
            held[0].fulfill(response=response)
            page.unroute("**/api/cases/ZF-1")
            page.get_by_role("tab", name="Funding", exact=True).wait_for()

            def proposal(index: int, ready: bool = False) -> dict[str, Any]:
                return dict(
                    id=f"SYN-{index}",
                    case_id="ZF-1",
                    capability="assessment-preparation",
                    version="1",
                    display_state="ready" if ready else "queued",
                    state="ready" if ready else "queued",
                    stale=False,
                    manual="Manual route.",
                    attempts=0,
                    provenance=[],
                    snapshot={},
                    envelope={},
                    history_next_offset=None,
                    output=dict(summary="Synthetic cited output", findings=[], unknowns=[])
                    if ready
                    else None,
                )

            held_queue: list[Route] = []

            def pages(route: Route) -> None:
                if "after=" in route.request.url:
                    route.fulfill(json={"proposals": [proposal(51, True)], "next_after": None})
                else:
                    held_queue.append(route)

            page.route(
                "**/api/assistants",
                lambda route: route.fulfill(
                    json={
                        "assistants": [],
                        "disabled": None,
                        "proactive": False,
                    }
                ),
            )
            page.route("**/api/assistants/proposals?**", pages)
            page.reload()
            tab(page, "Resident")
            page.locator("#outcome").fill("Retain while assistance is loading")
            call_node = page.locator("#outcome").element_handle()
            tab(page, "AI assistance")
            page.wait_for_function(
                "() => document.querySelector('#case-tab-ai').getAttribute('aria-selected')"
                " === 'true'"
            )
            held_queue[0].fulfill(
                json={
                    "proposals": [proposal(index) for index in range(50)],
                    "next_after": "page-two",
                }
            )
            page.wait_for_function(
                "() => document.querySelector('#case-tab-ai').textContent.includes('(1 to review)')"
            )
            check(
                "full cursor count includes output beyond first 50",
                page.locator("article.ai-suggestion").count() == 51
                and "1 AI suggestions waiting"
                in page.locator("[data-case-ai-summary]").inner_text(),
            )
            tab(page, "Resident")
            check(
                "tab-only navigation preserves DOM and pending work",
                page.locator("#outcome").evaluate("(el, old) => el === old", call_node)
                and page.locator("#outcome").input_value() == "Retain while assistance is loading",
            )
            page.unroute("**/api/assistants/proposals?**", pages)
            page.unroute("**/api/assistants")
            page.reload()

            for state in ("blocked", "empty", "closed", "ai-unavailable"):

                def variant(route: Route) -> None:
                    response = route.fetch()
                    case = response.json()
                    if state == "empty":
                        case["work"]["blockers"] = []
                    if state == "closed":
                        case["closed"] = True
                    route.fulfill(response=response, json=case)

                page.route("**/api/cases/ZF-1", variant)
                if state == "ai-unavailable":
                    page.route(
                        "**/api/assistants",
                        lambda route: route.fulfill(
                            status=503, json={"error": "Synthetic assistance outage"}
                        ),
                    )
                page.goto(base + "/app#/case/ZF-1?tab=overview")
                with page.expect_response("**/api/cases/ZF-1"):
                    page.reload()
                page.get_by_role("tab", name="Overview", exact=True).wait_for()
                if state == "closed":
                    check(
                        "closed all done, no current",
                        page.locator(".step.done").count() == 6
                        and page.locator(".step[aria-current]").count() == 0,
                    )
                if state == "empty":
                    check(
                        "empty blocker wording: " + page.locator(".case-summary").inner_text(),
                        "No recorded blockers." in page.locator(".case-summary").inner_text(),
                    )
                names = page.get_by_role("tab").all_text_contents()
                for name in names:
                    page.get_by_role("tab", name=name, exact=True).click()
                    scan(page, axe, reports, f"{state}/{name}")
                page.unroute("**/api/cases/ZF-1", variant)
                if state == "ai-unavailable":
                    page.unroute("**/api/assistants")

            page.goto(base + "/app#/case/ZF-4?tab=resident")
            page.get_by_role("tab", name="Resident", exact=True).wait_for()
            check(
                "open safety visible on Resident tab",
                page.locator("#case-safety").is_visible()
                and page.locator("#hz-source").is_visible(),
            )
            tab(page, "Funding")
            check(
                "blocked steps leave unrelated Funding tab available",
                page.get_by_role("tabpanel", name="Funding", exact=True).is_visible(),
            )
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 800})
                for name in page.get_by_role("tab").all_text_contents():
                    page.get_by_role("tab", name=name, exact=True).click()
                    check(
                        f"reflow {width}/{name}",
                        page.evaluate("document.documentElement.scrollWidth <= innerWidth"),
                    )
                if width == 320:
                    page.evaluate("window.scrollTo(0, 0)")
                    bottom = page.locator(".case-summary").evaluate(
                        "el => el.getBoundingClientRect().bottom"
                    )
                    check(f"320x800 summary within one viewport scroll ({bottom})", bottom <= 1600)
                    page.screenshot(path=str(out / "mobile-320.png"))
            page.emulate_media(reduced_motion="reduce", forced_colors="active")
            check(
                "reduced motion and forced-colour states retained",
                page.evaluate(
                    """() => [...document.querySelectorAll('.step a, [role=tab]')].every(
                  el => getComputedStyle(el).transitionDuration === '0s')
                  && [...document.querySelectorAll('.step-state')].every(el => el.textContent)"""
                ),
            )
            page.screenshot(path=str(out / "forced-colours.png"), full_page=True)
            page.emulate_media(forced_colors="none")
            page.route(
                "**/case-workspace.js",
                lambda route: route.fulfill(
                    status=404, content_type="text/plain", body="Synthetic missing enhancement"
                ),
            )
            page.reload()
            page.get_by_text("Tab navigation unavailable.", exact=False).wait_for()
            check(
                "missing enhancement keeps stacked sections and safety",
                page.locator("#case-panel-resident").is_visible()
                and page.locator("#case-panel-funding").is_visible()
                and page.locator("#hz-source").is_visible(),
            )
            page.unroute("**/case-workspace.js")
            check("no uncaught page errors", not errors)

            # chrome.tabs.setZoom changes real browser zoom, not device scale or CSS.
            with tempfile.TemporaryDirectory(prefix="zf-journey-zoom-") as scratch:
                root = Path(scratch)
                extension = root / "extension"
                extension.mkdir()
                (extension / "manifest.json").write_text(
                    json.dumps(
                        {
                            "manifest_version": 3,
                            "name": "Synthetic local zoom check",
                            "version": "1.0",
                            "permissions": ["tabs"],
                            "background": {"service_worker": "worker.js"},
                        }
                    )
                )
                (extension / "worker.js").write_text(
                    "chrome.runtime.onInstalled.addListener(() => {});"
                )
                zoom = playwright.chromium.launch_persistent_context(
                    str(root / "profile"),
                    channel="chromium",
                    headless=True,
                    no_viewport=True,
                    args=[
                        "--window-size=1280,800",
                        f"--disable-extensions-except={extension}",
                        f"--load-extension={extension}",
                    ],
                )
                try:
                    for cookie in context.cookies():
                        zoom.add_cookies(
                            [
                                {
                                    "name": cookie["name"],
                                    "value": cookie["value"],
                                    "url": base,
                                }
                            ]
                        )
                    zoom.route(
                        "**/*",
                        lambda route: (
                            route.continue_()
                            if route.request.url.startswith(base + "/")
                            else route.abort()
                        ),
                    )
                    zoom_page = zoom.pages[0]
                    zoom_page.goto(base + "/app#/case/ZF-1?tab=overview")
                    zoom_page.get_by_role("tab", name="Overview", exact=True).wait_for()
                    worker = (
                        zoom.service_workers[0]
                        if zoom.service_workers
                        else (zoom.wait_for_event("serviceworker"))
                    )
                    actual = worker.evaluate(
                        """async () => {
                          const [tab] = await chrome.tabs.query({active: true});
                          await chrome.tabs.setZoom(tab.id, 2);
                          return await chrome.tabs.getZoom(tab.id);
                        }"""
                    )
                    zoom_page.wait_for_function("innerWidth <= 640")
                    check("actual Chromium tab zoom is 200%", actual == 2)
                    for name in zoom_page.get_by_role("tab").all_text_contents():
                        zoom_page.get_by_role("tab", name=name, exact=True).click()
                        check(
                            f"200% browser zoom reflows/{name}",
                            zoom_page.evaluate(
                                "document.documentElement.scrollWidth <= innerWidth"
                            ),
                        )
                    zoom_page.screenshot(path=str(out / "browser-zoom-200.png"), full_page=True)
                finally:
                    zoom.close()
            (out / "results.json").write_text(
                json.dumps(
                    dict(
                        browser=browser.version,
                        axe_version="4.10.3",
                        scans=reports,
                        page_errors=errors,
                        zoom="chrome.tabs.setZoom=2; innerWidth<=640",
                    ),
                    indent=2,
                )
                + "\n"
            )
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.axe.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Unexpected axe 4.10.3 bytes")
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, raw.decode(), args.out), journey_data)
