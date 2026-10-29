"""Exercise issue 532 on the constructed real app, with integrity-pinned axe."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from checks.design_system_browser_check import check, main
from checks.regulatory_ux_check import AXE_SHA256
from playwright.sync_api import Page, Request, expect, sync_playwright


def scan(page: Page, axe: str, reports: list[dict[str, Any]], state: str) -> None:
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async () => await axe.run(document.querySelector(
          '.map-dialog[open]') || document.querySelector('.map-panel'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a',
            'wcag21aa', 'wcag22aa']}})"""
    )
    reports.append(dict(state=state, **result))
    check(f"axe zero violations: {state}", not result["violations"])
    check(
        f"axe no unresolved ARIA references: {state}",
        not any(item["id"].startswith("aria-") for item in result["incomplete"]),
    )


def check_browser_shortcuts(page: Page, mode: str) -> None:
    requests: list[str] = []

    def record_request(request: Request) -> None:
        if "/api/map?" in request.url:
            requests.append(request.url)

    page.on("request", record_request)
    try:
        for selector in ("#leaflet", ".map-marker:has(.map-symbol.normal)"):
            target = page.locator(selector)
            target.focus()
            results = target.evaluate(
                """async el => {
                  const pane = document.querySelector('.leaflet-map-pane');
                  const before = pane.outerHTML;
                  const url = location.href;
                  const results = [];
                  for (const modifiers of [
                    {ctrlKey: true}, {metaKey: true}, {altKey: true},
                    {ctrlKey: true, metaKey: true, altKey: true, shiftKey: true}
                  ]) {
                    for (const key of ['=', '+', '-', 'ArrowLeft', 'ArrowRight',
                      'ArrowUp', 'ArrowDown']) {
                      const event = new KeyboardEvent('keydown', {
                        key, bubbles: true, cancelable: true, ...modifiers
                      });
                      const allowed = el.dispatchEvent(event);
                      results.push({
                        key, modifiers, allowed,
                        unchanged: pane.outerHTML === before
                          && location.href === url && document.activeElement === el
                      });
                    }
                  }
                  await new Promise(resolve => requestAnimationFrame(() =>
                    requestAnimationFrame(resolve)));
                  return results;
                }"""
            )
            for result in results:
                check(
                    f"{mode} {selector} leaves browser shortcut unchanged: "
                    f"{result['modifiers']} {result['key']}",
                    result["allowed"] and result["unchanged"],
                )
        check(f"{mode} browser shortcuts issue no map requests", not requests)
    finally:
        page.remove_listener("request", record_request)


def run_browser(base: str, axe: str, out: Path) -> None:
    reports: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        context.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(base + "/") else route.abort()
            ),
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        card = page.locator(".map-home-card")
        normal = page.locator(".map-marker:has(.map-symbol.normal)")
        hazard = page.locator(".map-marker:has(.map-symbol.hazard)")
        map_region = page.locator("#leaflet")
        toggle = page.get_by_role("button", name="Expand map", exact=True)
        close = page.get_by_role("button", name="Close home summary", exact=True)
        open_home = page.get_by_role("link", name="Open home", exact=True)
        try:
            page.goto(base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-check")
            page.get_by_role("button", name="Sign in", exact=True).click()
            page.get_by_role("heading", name="My cases today").wait_for()
            page.get_by_role("link", name="Overview", exact=True).click()
            page.locator(".map-cluster").first.wait_for()
            page.locator("#mapArea").select_option(label="Point examples")
            expect(page.locator(".map-marker")).to_have_count(3)
            check_browser_shortcuts(page, "embedded")
            normal.focus()
            normal.press("Enter")
            expect(card).to_be_visible()
            expect(page.locator("#map-home-title")).to_be_focused()
            expect(card).to_contain_text("1 Test Road")
            expect(card).to_contain_text("Current stage")
            expect(card).to_contain_text("Normal")
            expect(open_home).to_have_attribute("href", "#/case/ZF-1")
            check(
                "keyboard marker opens summary without navigation", page.url.endswith("#/overview")
            )
            page.keyboard.press("Tab")
            expect(close).to_be_focused()
            page.keyboard.press("Tab")
            expect(open_home).to_be_focused()
            original_marker = normal.element_handle()
            assert original_marker is not None
            page.evaluate("() => window.dispatchEvent(new Event('resize'))")
            expect(open_home).to_be_focused()
            scan(page, axe, reports, "embedded-home")
            page.screenshot(path=str(out / "embedded-desktop.png"))
            close.click()
            expect(card).to_be_hidden()
            expect(normal).to_be_focused()
            normal.press("Space")
            page.keyboard.press("Escape")
            expect(card).to_be_hidden()
            expect(normal).to_be_focused()
            hazard.click()
            expect(card).to_contain_text("Safety issue open")
            close_box = close.bounding_box()
            card_box = card.bounding_box()
            assert close_box and card_box
            check(
                "embedded close icon is at card top right",
                close_box["x"] > card_box["x"] + card_box["width"] / 2
                and close_box["y"] < card_box["y"] + 40,
            )
            map_region.click(position={"x": 20, "y": 200})
            expect(card).to_be_hidden()
            expect(hazard).to_be_focused()
            check("embedded map click dismisses and restores marker focus", True)
            for width in (320, 390):
                page.set_viewport_size({"width": width, "height": 900})
                expect(page.locator(".map-marker")).to_have_count(3)
                hazard.focus()
                hazard.press("Enter")
                expect(close).to_be_in_viewport()
                check(
                    f"embedded summary reflows at {width}px",
                    page.evaluate("document.documentElement.scrollWidth <= innerWidth"),
                )
                scan(page, axe, reports, f"embedded-{width}")
                close.click()
                expect(hazard).to_be_focused()
            page.set_viewport_size({"width": 1280, "height": 900})
            expect(page.locator(".map-marker")).to_have_count(3)

            normal.press("Enter")
            toggle.focus()
            toggle.press("Space")
            dialog = page.get_by_role("dialog")
            exit_map = page.get_by_role("button", name="Exit expanded map", exact=True)
            expect(dialog).to_be_visible()
            expect(exit_map).to_be_focused()
            expect(card).to_be_visible()
            check(
                "same card moves into left information panel",
                card.evaluate("el => el.parentElement.classList.contains('map-info')"),
            )
            left = page.locator(".map-info").bounding_box()
            right = map_region.bounding_box()
            bounds = dialog.bounding_box()
            assert left and right and bounds
            check(
                "near-fullscreen layout has narrow left panel and larger map",
                bounds["width"] >= 1200
                and bounds["height"] >= 850
                and left["x"] < right["x"]
                and left["width"] < right["width"],
            )
            page.keyboard.press("Shift+Tab")
            if not page.evaluate("Boolean(document.activeElement.closest('dialog[open]'))"):
                page.keyboard.press("Shift+Tab")
            check(
                "native dialog contains backward keyboard focus",
                page.evaluate("Boolean(document.activeElement.closest('dialog[open]'))"),
            )
            check(
                "modal background cannot receive application focus",
                page.evaluate(
                    """() => {
                      document.querySelector('#nav a').focus();
                      return Boolean(document.activeElement.closest('dialog[open]'));
                    }"""
                ),
            )
            normal.focus()
            normal.press("Enter")
            expect(page.locator("#map-home-title")).to_be_focused()
            page.keyboard.press("Escape")
            expect(card).to_be_hidden()
            expect(normal).to_be_focused()
            expect(dialog).to_be_visible()
            page.keyboard.press("Escape")
            expect(dialog).to_have_count(0)
            expect(toggle).to_be_focused()
            check("Escape closes summary first, then expanded map", True)
            expect(map_region).to_have_css("height", "460px")
            toggle.press("Enter")
            hazard.focus()
            hazard.press("Space")
            expect(card).to_contain_text("Safety issue open")
            expect(page.locator("#map-home-title")).to_be_focused()
            scan(page, axe, reports, "expanded-home")
            page.screenshot(path=str(out / "expanded-desktop.png"))
            check_browser_shortcuts(page, "expanded")

            # Background redraw replaces markers but not the focused summary action.
            open_home.focus()
            with page.expect_response("**/api/map?**"):
                page.evaluate("() => window.dispatchEvent(new Event('resize'))")
                page.set_viewport_size({"width": 1270, "height": 900})
            expect(open_home).to_be_focused()
            page.keyboard.press("Escape")
            expect(hazard).to_be_focused()
            old_marker = hazard.element_handle()
            page.set_viewport_size({"width": 1280, "height": 900})
            page.wait_for_function("old => !old.isConnected", arg=old_marker)
            expect(hazard).to_be_focused()
            check("redraw preserves action focus and restores recreated marker focus", True)
            check("original embedded marker was replaced safely", not original_marker.is_visible())

            page.emulate_media(reduced_motion="reduce")
            check(
                "map animations are disabled including reduced motion",
                page.evaluate(
                    """async () => {
                      const map = document.querySelector('.leafmap');
                      let animated = false;
                      const observer = new MutationObserver(() => {
                        animated ||= map.classList.contains('leaflet-zoom-anim');
                      });
                      observer.observe(map, {attributes: true, attributeFilter: ['class']});
                      map.querySelector('.leaflet-control-zoom-out').click();
                      await new Promise(resolve => setTimeout(resolve, 300));
                      observer.disconnect();
                      return !animated && getComputedStyle(document.documentElement)
                        .getPropertyValue('--motion').trim() === '0s';
                    }"""
                ),
            )
            map_region.focus()
            with page.expect_response("**/api/map?**") as zoom_response:
                page.locator(".leaflet-control-zoom-out").click()
            zoom = int(parse_qs(urlsplit(zoom_response.value.url).query)["zoom"][0])
            expect(page.locator(".map-marker")).to_have_count(3)
            map_region.focus()
            for key, delta in (("Shift++", 1), ("=", 1), ("-", -1)):
                old_marker = normal.element_handle()
                with page.expect_response("**/api/map?**") as zoom_response:
                    map_region.press(key)
                actual_zoom = int(parse_qs(urlsplit(zoom_response.value.url).query)["zoom"][0])
                check(f"{key} changes map zoom by {delta}", actual_zoom == zoom + delta)
                page.wait_for_function("old => !old.isConnected", arg=old_marker)
                zoom = actual_zoom
            old_marker = normal.element_handle()
            pane = page.locator(".leaflet-map-pane")
            before_pan = pane.evaluate(
                "el => new DOMMatrixReadOnly(getComputedStyle(el).transform).m41"
            )
            map_region.press("ArrowRight")
            check(
                "keyboard pan immediately reaches its 80px endpoint",
                abs(
                    pane.evaluate("el => new DOMMatrixReadOnly(getComputedStyle(el).transform).m41")
                    - before_pan
                )
                == 80,
            )
            page.wait_for_function("old => !old.isConnected", arg=old_marker)
            map_region.press("ArrowLeft")
            expect(page.locator(".map-marker")).to_have_count(3)
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                expect(page.locator(".map-marker")).to_have_count(3)
                hazard.focus()
                page.locator(".map-info").evaluate("el => el.scrollTop = el.scrollHeight")
                hazard.press("Enter")
                expect(card).to_be_visible()
                check(
                    f"summary focus scrolls into view at {width}px",
                    page.locator("#map-home-title").evaluate(
                        """el => {
                          const title = el.getBoundingClientRect();
                          const panel = el.closest('.map-info').getBoundingClientRect();
                          return title.top >= panel.top && title.bottom <= panel.bottom;
                        }"""
                    ),
                )
                check(
                    f"expanded map reflows at {width}px",
                    page.evaluate(
                        """() => document.documentElement.scrollWidth <= innerWidth
                          && document.querySelector('.map-dialog').scrollWidth
                            <= document.querySelector('.map-dialog').clientWidth
                          && document.querySelector('.leafmap').clientWidth > 80"""
                    ),
                )
                scan(page, axe, reports, f"expanded-{width}")
                if width != 1280:
                    page.screenshot(path=str(out / f"expanded-{width}.png"))
            page.emulate_media(forced_colors="active")
            expect(card.locator(".marker-code")).to_have_text("!")
            check(
                "forced colours keep status symbol and words",
                "Safety issue open" in card.inner_text(),
            )
            page.emulate_media(forced_colors="none")

            # A failed refresh must remove the stale selected card and recover focus.
            open_home.focus()
            page.route(
                "**/api/map?**",
                lambda route: route.fulfill(status=503, json={"error": "Synthetic map failure"}),
            )
            page.set_viewport_size({"width": 1275, "height": 900})
            expect(page.locator(".map-info [role=alert]")).to_contain_text("Map unavailable")
            expect(card).to_be_hidden()
            expect(map_region).to_be_focused()
            scan(page, axe, reports, "expanded-failed-map")
            page.unroute("**/api/map?**")
            page.set_viewport_size({"width": 1280, "height": 900})
            expect(page.locator(".map-marker")).to_have_count(3)
            normal.focus()
            normal.press("Enter")
            exit_map.click()
            expect(card).to_be_visible()
            page.get_by_role("button", name="Safety issues open", exact=False).click()
            expect(page.locator(".map-marker")).to_have_count(1)
            expect(card).to_be_hidden()
            check("filter removes a selected home rather than leaving stale details", True)
            toggle.click()
            hazard.focus()
            hazard.press("Enter")
            open_home.focus()
            open_home.press("Enter")
            page.wait_for_url("**#/case/ZF-4")
            expect(page.locator(".map-dialog")).to_have_count(0)
            expect(page.locator(".map-slot")).to_have_count(0)
            check("home navigation disposes map and dialog", True)

            page.get_by_role("link", name="Overview", exact=True).click()
            expect(page.locator(".map-marker")).to_have_count(1)
            toggle.click()
            page.get_by_role("link", name="Show these as a list", exact=True).click()
            page.wait_for_url("**#/all")
            expect(page.get_by_role("dialog")).to_have_count(0)
            check("expanded manual path exits modal and navigates to case list", True)

            page.goto(base + "/app#/coordinator")
            page.get_by_role("heading", name="Coordinator flow", exact=True).wait_for()
            expect(page.locator(".map-cluster")).not_to_have_count(0)
            page.get_by_label("Local authority", exact=True).select_option("Point examples")
            page.get_by_role("button", name="Apply coordinator filters", exact=True).click()
            expect(page.locator(".map-marker")).to_have_count(3)
            toggle.click()
            normal.focus()
            normal.press("Enter")
            expect(card).to_contain_text("ZF-1")
            expect(card).to_contain_text("Address not included in this map")
            check(
                "coordinator card never reconstructs withheld personal fields",
                "Pat Test" not in card.inner_text() and "Test Road" not in card.inner_text(),
            )
            scan(page, axe, reports, "coordinator-expanded-home")
            page.get_by_role("button", name="Show these as a list", exact=True).click()
            expect(page.locator("#coordinator-records")).to_be_focused()
            expect(page.get_by_role("dialog")).to_have_count(0)
            page.locator("#maplist-h").click()
            expect(page.locator(".maplist a").first).to_be_visible()
            check("coordinator manual list shortcut restores external list focus", True)
            check(f"no uncaught JavaScript errors ({errors})", not errors)
        finally:
            (out / "axe-results.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
            (out / "browser.json").write_text(
                json.dumps(dict(browser=browser.version, errors=errors), indent=2),
                encoding="utf-8",
            )
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.axe.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Unexpected axe 4.10.3 content")
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, raw.decode("utf-8"), args.out))
