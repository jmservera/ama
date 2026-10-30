"""Exercise issues 532/551 on the constructed real app, with integrity-pinned axe."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from checks.design_system_browser_check import check, main
from checks.regulatory_ux_check import AXE_SHA256
from playwright.sync_api import Page, Playwright, Request, Route, expect, sync_playwright


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


def check_expanded_filters(
    page: Page, base: str, axe: str, out: Path, reports: list[dict[str, Any]]
) -> None:
    filters = page.locator(".overview-map-filters")
    tiles = filters.get_by_role("group", name="Choose what the map shows")
    area = page.get_by_label("Show map for", exact=True)
    original = filters.element_handle()
    original_area = area.element_handle()
    assert original is not None and original_area is not None
    header_count_size = tiles.locator("strong").first.evaluate(
        "el => parseFloat(getComputedStyle(el).fontSize)"
    )
    page.get_by_role("button", name="Expand map", exact=True).press("Enter")
    expect(page.get_by_role("dialog").locator(".overview-map-filters")).to_have_count(1)
    expect(tiles.locator(".static")).to_be_hidden()
    check(
        "expanded filters use smaller count text",
        tiles.locator("strong").first.evaluate("el => parseFloat(getComputedStyle(el).fontSize)")
        < header_count_size,
    )
    flags = (
        ("", "Open cases"),
        ("hazard", "Safety issues open"),
        ("long", "Waiting 60+ days"),
        ("nodecision", "Awaiting resident decision"),
        ("fundingprog", "Funding in progress"),
        ("support", "Residents needing extra support"),
    )
    selections: list[dict[str, Any]] = []
    for index, (flag, label) in enumerate(flags):
        expected = page.request.get(
            base + "/api/map?zoom=15&area=Point%20examples&flag=" + flag
        ).json()
        button = tiles.get_by_role("button", name=label, exact=False)
        button.focus()
        button.press("Space" if index % 2 else "Enter")
        expect(button).to_have_attribute("aria-pressed", "true")
        expect(button.locator(".tile-selection")).to_have_text("Selected")
        expect(tiles.locator('[aria-pressed="true"]')).to_have_count(1)
        expect(page.locator(".map-marker")).to_have_count(expected["total"])
        expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
        expect(button).to_be_focused()
        check(
            f"{label} keeps visible keyboard focus",
            button.evaluate("el => getComputedStyle(el).outlineStyle === 'solid'"),
        )
        check(f"{label} API supplies individual homes", expected["mode"] == "points")
        expected_ids = sorted(point["id"] for point in expected["items"])
        summary_ids: list[str] = []
        for marker in page.locator(".map-marker").all():
            marker.press("Enter")
            card = page.locator(".map-home-card")
            expect(card).to_be_visible()
            case_id = card.locator("dd").first.inner_text()
            expect(card.get_by_role("link", name="Open home", exact=True)).to_have_attribute(
                "href", f"#/case/{case_id}"
            )
            summary_ids.append(case_id)
            page.get_by_role("button", name="Close home summary", exact=True).press("Space")
            expect(marker).to_be_focused()
        check(f"{label} renders the exact selected homes", sorted(summary_ids) == expected_ids)

        page.get_by_role("button", name="Exit expanded map", exact=True).press("Enter")
        check(
            f"{label} restores original header controls",
            original.evaluate("el => el.parentElement.classList.contains('map-filter-slot')")
            and original_area.evaluate("el => el === document.getElementById('mapArea')"),
        )
        expect(button).to_have_attribute("aria-pressed", "true")
        expect(button.locator(".tile-selection")).to_have_text("Selected")
        expect(tiles.locator('[aria-pressed="true"]')).to_have_count(1)
        expect(area).to_have_value("Point examples")
        alternate_flag, alternate_label = flags[1 if not flag else 0]
        alternate = tiles.get_by_role("button", name=alternate_label, exact=False)
        alternate_expected = page.request.get(
            base + "/api/map?zoom=15&area=Point%20examples&flag=" + alternate_flag
        ).json()
        alternate.press("Space")
        expect(alternate).to_have_attribute("aria-pressed", "true")
        expect(button).to_have_attribute("aria-pressed", "false")
        expect(button.locator(".tile-selection")).to_have_text("Select filter")
        expect(page.locator(".map-marker")).to_have_count(alternate_expected["total"])
        expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
        expect(alternate).to_be_focused()
        page.get_by_role("button", name="Expand map", exact=True).press("Space")
        expect(alternate).to_have_attribute("aria-pressed", "true")
        expect(alternate.locator(".tile-selection")).to_have_text("Selected")
        button.press("Enter")
        expect(button).to_have_attribute("aria-pressed", "true")
        expect(page.locator(".map-marker")).to_have_count(expected["total"])
        expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
        check(
            f"{label} restores the exact home list after header round trip",
            page.locator(".maplist li a").evaluate_all(
                "links => links.map(link => link.getAttribute('href')).sort()"
            )
            == [f"#/case/{case_id}" for case_id in expected_ids],
        )
        selections.append(
            dict(
                flag=flag,
                total=expected["total"],
                expected_ids=expected_ids,
                summary_ids=sorted(summary_ids),
                header_alternate=alternate_flag,
            )
        )
    check("zero-result support filter is exercised", selections[-1]["total"] == 0)
    expect(page.locator(".map-info [role=status]")).to_have_text("0 homes shown")

    # Hold a genuine older fit read while a newer area selection completes.
    held: list[Route] = []

    def hold_first(route: Route) -> None:
        if not held:
            held.append(route)
        else:
            route.continue_()

    page.route("**/api/map?**", hold_first)
    try:
        safety = tiles.get_by_role("button", name="Safety issues open", exact=False)
        requests: list[str] = []

        def record_request(request: Request) -> None:
            if "/api/map?" in request.url:
                requests.append(request.url)

        page.on("request", record_request)
        try:
            with page.expect_request("**/api/map?**"):
                safety.press("Space")
            expect(safety).to_be_focused()
            expect(safety).to_be_enabled()
            expect(page.locator("#leaflet")).to_have_attribute("aria-busy", "true")
            check(
                "filter progress stays outside the compact control group",
                filters.locator(".async-feedback").count() == 0,
            )
            check("first flag activation issues one map request", len(requests) == 1)
            before_repeat = len(requests)
            safety.press("Space")
            page.evaluate(
                """async () => await new Promise(resolve => requestAnimationFrame(() =>
                  requestAnimationFrame(resolve)))"""
            )
            check("selected flag suppresses duplicate reads", len(requests) == before_repeat)
        finally:
            page.remove_listener("request", record_request)
        page.keyboard.press("Tab")
        expect(tiles.get_by_role("button", name="Waiting 60+ days", exact=False)).to_be_focused()
        older = held[0].fetch()
        check("held safety read comes from real local API", older.ok)
        area.focus()
        area.select_option(label="Cluster examples")
        expect(area).to_be_focused()
        expect(area).to_be_enabled()
        expect(page.locator(".map-marker")).to_have_count(0)
        expect(page.locator(".map-info [role=status]")).to_have_text("0 homes shown")
        held[0].fulfill(response=older)
        expect(page.locator(".map-panel .async-feedback")).to_have_count(0)
        expect(page.locator(".map-marker")).to_have_count(0)
        expect(page.locator(".map-info [role=status]")).to_have_text("0 homes shown")
        check(
            "latest area selection survives older successful flag response",
            area.input_value() == "Cluster examples",
        )
    finally:
        page.unroute("**/api/map?**", hold_first)

    # Hold an area read too: changing the selector must remain focus-safe.
    held.clear()
    page.route("**/api/map?**", hold_first)
    try:
        with page.expect_request("**/api/map?**"):
            area.select_option(label="Point examples")
        expect(area).to_be_focused()
        expect(area).to_be_enabled()
        expect(page.locator("#leaflet")).to_have_attribute("aria-busy", "true")
        response = held[0].fetch()
        held[0].fulfill(response=response)
        expect(page.locator(".map-marker")).to_have_count(1)
        expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
        expect(area).to_be_focused()
    finally:
        page.unroute("**/api/map?**", hold_first)

    page.get_by_role("button", name="Exit expanded map", exact=True).click()
    check(
        "original filter and area nodes return to header",
        original.evaluate("el => el.parentElement.classList.contains('map-filter-slot')")
        and original_area.evaluate("el => el === document.getElementById('mapArea')"),
    )
    expect(safety).to_have_attribute("aria-pressed", "true")
    expect(area).to_have_value("Point examples")
    expect(tiles.locator(".static")).to_be_visible()
    open_cases = tiles.get_by_role("button", name="Open cases", exact=False)
    open_cases.press("Enter")
    expect(page.locator(".map-marker")).to_have_count(3)
    page.get_by_role("button", name="Expand map", exact=True).press("Space")
    expect(open_cases).to_have_attribute("aria-pressed", "true")
    expect(open_cases.locator(".tile-selection")).to_have_text("Selected")

    geometry: list[dict[str, Any]] = []
    for width, height in ((320, 900), (390, 900), (1280, 900), (390, 568)):
        page.set_viewport_size({"width": width, "height": height})
        expect(page.locator(".map-marker")).to_have_count(3)
        if height == 568:
            held.clear()
            page.route("**/api/map?**", hold_first)
        with page.expect_request("**/api/map?**"):
            area.dispatch_event("change")
        if height == 568:
            expect(page.locator("#leaflet")).to_have_attribute("aria-busy", "true")
        else:
            expect(page.locator(".map-panel .async-feedback")).to_have_count(0)
        dimensions = page.evaluate(
            """() => {
              const filters = document.querySelector('.overview-map-filters');
              const map = document.querySelector('.leafmap');
              const workspace = document.querySelector('.map-workspace');
              const rect = filters.getBoundingClientRect();
              const mapRect = map.getBoundingClientRect();
              return {
                width: innerWidth, height: innerHeight,
                pageWidth: document.documentElement.scrollWidth,
                filtersWidth: filters.clientWidth, filtersScroll: filters.scrollWidth,
                filtersBottom: rect.bottom, workspaceTop: workspace.getBoundingClientRect().top,
                mapWidth: mapRect.width, mapHeight: mapRect.height,
                minimumHeight: 14 * parseFloat(getComputedStyle(document.documentElement).fontSize)
              };
            }"""
        )
        geometry.append(dimensions)
        check(
            f"filters and map fit at {width}x{height}",
            (
                dimensions["pageWidth"] <= width
                and dimensions["filtersScroll"] <= dimensions["filtersWidth"]
                and dimensions["filtersBottom"] <= dimensions["workspaceTop"]
                and dimensions["mapWidth"] > 80
                and dimensions["mapHeight"] >= dimensions["minimumHeight"]
            ),
        )
        if height == 568:
            held[0].continue_()
            page.unroute("**/api/map?**", hold_first)
            expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
            expect(page.locator(".map-panel .async-feedback")).to_have_count(0)
        for button in tiles.get_by_role("button").all():
            button.focus()
            check(
                f"filter label and focus fit at {width}x{height}",
                button.evaluate(
                    """el => {
                  const r = el.getBoundingClientRect();
                  const p = el.closest('.overview-map-filters').getBoundingClientRect();
                  return r.height >= 40 && el.scrollWidth <= el.clientWidth
                    && r.top >= p.top && r.bottom <= p.bottom
                    && getComputedStyle(el).outlineStyle === 'solid';
                }"""
                ),
            )
        area.focus()
        expect(area).to_be_in_viewport()
        exit_map = page.get_by_role("button", name="Exit expanded map", exact=True)
        exit_map.focus()
        expect(exit_map).to_be_in_viewport()
        manual = page.get_by_role("link", name="Show these as a list", exact=True)
        manual.focus()
        expect(manual).to_be_in_viewport()
        scan(page, axe, reports, f"expanded-filters-{width}x{height}")
        filters.evaluate("el => el.scrollTop = 0")
        exit_map.focus()
        page.screenshot(path=str(out / f"expanded-filters-{width}x{height}.png"))
    (out / "filters.json").write_text(
        json.dumps(dict(selections=selections, geometry=geometry), indent=2), encoding="utf-8"
    )
    page.get_by_role("button", name="Exit expanded map", exact=True).press("Enter")
    page.set_viewport_size({"width": 1280, "height": 900})
    area.dispatch_event("change")
    expect(page.locator(".map-marker")).to_have_count(3)
    expect(page.locator(".map-panel .async-feedback")).to_have_count(0)


def check_pending_navigation(page: Page, out: Path) -> None:
    page.get_by_role("link", name="Overview", exact=True).click()
    page.get_by_role("heading", name="Overview", exact=True).wait_for()
    page.locator(".leaflet-map-pane").wait_for(state="attached")
    toggle = page.get_by_role("button", name="Expand map", exact=True)
    toggle.scroll_into_view_if_needed()
    original_toggle = toggle.element_handle()
    original_slot = page.locator(".map-slot").element_handle()
    bounds = toggle.bounding_box()
    scroll = page.evaluate("() => ({left: scrollX, top: scrollY})")
    assert original_toggle is not None and original_slot is not None and bounds is not None
    page.evaluate(
        """() => {
          window.mapNavigationCheck = {facetsHeld: false, signal: routeController.signal};
        }"""
    )
    held: list[Route] = []
    released = False
    results: dict[str, Any] = {}
    clean_map = """() => !document.querySelector('.map-dialog, .map-slot')
      && !document.body.classList.contains('map-expanded')"""

    def hold(route: Route) -> None:
        held.append(route)
        page.evaluate("mapNavigationCheck.facetsHeld = true")

    page.route("**/api/facets", hold)
    try:
        page.get_by_role("link", name="Show these as a list", exact=True).click()
        page.wait_for_function("() => mapNavigationCheck.facetsHeld")
        results["pending"] = page.evaluate(
            """() => ({
              oldRouteAborted: mapNavigationCheck.signal.aborted,
              destinationPending: location.hash === '#/all'
                && document.querySelector('h1').textContent === 'Overview'
                && !routeController.signal.aborted
            })"""
        )
        check(
            "facets held after map route disposal and before destination rendering",
            len(held) == 1
            and results["pending"]["oldRouteAborted"]
            and results["pending"]["destinationPending"],
        )
        page.evaluate("position => window.scrollTo(position)", scroll)
        page.mouse.click(bounds["x"] + bounds["width"] / 2, bounds["y"] + bounds["height"] / 2)
        results["pointer"] = page.evaluate(
            """() => ({
              dialogOpen: Boolean(document.querySelector('.map-dialog[open]')),
              scrollLocked: document.body.classList.contains('map-expanded')
            })"""
        )
        results["pointerClean"] = page.evaluate(clean_map)
        check(
            "Expand click during pending facets cannot reopen disposed map", results["pointerClean"]
        )
        results["slot"] = original_slot.evaluate(
            "el => ({connected: el.isConnected, inert: el.inert})"
        )
        results["toggle"] = original_toggle.evaluate(
            "el => ({connected: el.isConnected, disabled: el.disabled})"
        )
        check(
            "obsolete map slot is disconnected and controls are inert and disabled",
            results["slot"] == {"connected": False, "inert": True}
            and results["toggle"] == {"connected": False, "disabled": True},
        )
        original_toggle.evaluate(
            """el => {
              el.click();
              el.dispatchEvent(new MouseEvent('click', {bubbles: true}));
            }"""
        )
        results["retainedClickClean"] = page.evaluate(clean_map)
        check("retained Expand events cannot reopen disposed map", results["retainedClickClean"])
        held[0].continue_()
        released = True
        page.get_by_role("heading", name="All open cases", exact=True).wait_for()
        results["destinationClean"] = page.evaluate(clean_map)
        check(
            "case list renders without disposed map, dialog or scroll lock",
            results["destinationClean"],
        )
    finally:
        if held and not released:
            held[0].continue_()
        page.unroute("**/api/facets", hold)
        (out / "pending-navigation.json").write_text(
            json.dumps(results, indent=2), encoding="utf-8"
        )


def check_session_expiry(page: Page, base: str, out: Path) -> None:
    results: list[dict[str, Any]] = []
    for expanded in (False, True):
        mode = "expanded" if expanded else "embedded"
        page.reload()
        page.goto(base + "/app#/coordinator")
        page.get_by_role("heading", name="Coordinator flow", exact=True).wait_for()
        expect(page.locator(".map-cluster")).not_to_have_count(0)
        page.evaluate(
            """() => {
              const state = window.mapDisposalCheck = {
                armed: false, requests: [], draws: [], fits: 0, clears: 0,
                forceCollapseDraw: false
              };
              const originalPanel = mapPanel;
              mapPanel = (...args) => {
                const panel = originalPanel(...args);
                const draw = panel.draw;
                panel.draw = fit => {
                  const attempt = {fit, settled: false, error: null};
                  state.draws.push(attempt);
                  const pending = draw(fit);
                  pending.then(() => { attempt.settled = true; }, error => {
                    attempt.error = String(error);
                    attempt.settled = true;
                  });
                  return pending;
                };
                return panel;
              };
              const originalApi = api;
              api = (path, body, signal) => {
                if (!state.armed || !path.startsWith('/api/map?'))
                  return originalApi(path, body, signal);
                const request = {path, signal: signal || routeController.signal,
                  settled: false};
                state.requests.push(request);
                return originalApi(path, body, signal).finally(() => {
                  request.settled = true;
                });
              };
              const fitBounds = L.Map.prototype.fitBounds;
              L.Map.prototype.fitBounds = function (...args) {
                state.fits++;
                return fitBounds.apply(this, args);
              };
              const clearLayers = L.LayerGroup.prototype.clearLayers;
              L.LayerGroup.prototype.clearLayers = function (...args) {
                state.clears++;
                return clearLayers.apply(this, args);
              };
              const invalidateSize = L.Map.prototype.invalidateSize;
              L.Map.prototype.invalidateSize = function (...args) {
                const result = invalidateSize.apply(this, args);
                if (state.forceCollapseDraw
                  && !document.querySelector('.map-dialog[open]')) {
                  state.forceCollapseDraw = false;
                  this.fire('moveend');
                }
                return result;
              };
            }"""
        )
        page.get_by_role("link", name="Overview", exact=True).click()
        page.locator(".map-cluster").first.wait_for()
        page.locator("#mapArea").select_option(label="Point examples")
        expect(page.locator(".map-marker")).to_have_count(3)
        if expanded:
            page.get_by_role("button", name="Expand map", exact=True).click()
        page.wait_for_function("() => mapDisposalCheck.draws.every(draw => draw.settled)")
        page.evaluate(
            """async () => {
              await new Promise(resolve => requestAnimationFrame(() =>
                requestAnimationFrame(resolve)));
              mapDisposalCheck.draws = [];
              mapDisposalCheck.armed = true;
            }"""
        )
        held: list[Route] = []

        def hold(route: Route) -> None:
            held.append(route)
            page.evaluate("count => { mapDisposalCheck.heldRequests = count; }", len(held))

        page.route("**/api/map?**", hold)
        try:
            for _ in range(2):
                with page.expect_request("**/api/map?**"):
                    page.locator("#mapArea").dispatch_event("change")
            page.wait_for_function("() => mapDisposalCheck.heldRequests === 2")
            check(f"{mode} two latest fit requests held", len(held) == 2)
            check(
                f"{mode} both draws request bounds without viewport clipping",
                page.evaluate(
                    """() => mapDisposalCheck.draws.length === 2
                      && mapDisposalCheck.draws.every(draw => draw.fit && !draw.settled)
                      && mapDisposalCheck.requests.every(request =>
                        !new URL(request.path, location.origin).searchParams.has('bbox'))"""
                ),
            )
            response = held[1].fetch()
            data = response.json()
            check(
                f"{mode} genuine successful fit response has bounds",
                response.ok and bool(data["bounds"]),
            )
            page.evaluate(
                "(expanded) => { mapDisposalCheck.forceCollapseDraw = expanded; }",
                expanded,
            )
            held[0].fulfill(status=401, json={"error": "Synthetic session expiry"})
            expect(page.get_by_role("heading", name="Sign in", exact=True)).to_be_visible()
            expect(page.get_by_role("alert")).to_have_text("Your session has ended. Sign in again.")
            if expanded:
                page.wait_for_function("() => mapDisposalCheck.heldRequests >= 3")
                check("collapse resize starts a real viewport draw", len(held) >= 3)
            expected_requests = len(held)
            before = page.evaluate(
                "() => ({fits: mapDisposalCheck.fits, clears: mapDisposalCheck.clears})"
            )
            for route in held[1:]:
                route.fulfill(json=data)
            page.wait_for_function(
                """() => mapDisposalCheck.requests.every(request => request.settled)
                  && mapDisposalCheck.draws.every(draw => draw.settled)"""
            )
            result = page.evaluate(
                """async before => {
                  await new Promise(resolve => requestAnimationFrame(() =>
                    requestAnimationFrame(resolve)));
                  const state = mapDisposalCheck;
                  return {
                    before, after: {fits: state.fits, clears: state.clears},
                    errors: state.draws.map(draw => draw.error).filter(Boolean),
                    signalsLive: state.requests.every(request => !request.signal.aborted),
                    requests: state.requests.map(request => request.path),
                    clean: !document.querySelector('.map-dialog, .map-slot')
                      && !document.body.classList.contains('map-expanded')
                  };
                }""",
                before,
            )
            results.append(dict(mode=mode, **result))
            check(f"{mode} session expiry leaves route signals live", result["signalsLive"])
            check(
                f"{mode} late successful draw settles without rejection",
                not result["errors"],
            )
            check(
                f"{mode} late responses never fit or redraw the disposed map",
                result["before"] == result["after"],
            )
            check(
                f"{mode} late responses start no further map requests",
                len(result["requests"]) == expected_requests,
            )
            check(f"{mode} session expiry removes map, dialog and body lock", result["clean"])
        finally:
            page.unroute("**/api/map?**", hold)
            (out / "session-expiry.json").write_text(
                json.dumps(results, indent=2), encoding="utf-8"
            )


def check_enlarged_font(
    playwright: Playwright, base: str, axe: str, out: Path, reports: list[dict[str, Any]]
) -> None:
    browser = playwright.chromium.launch(args=["--blink-settings=defaultFontSize=32"])
    try:
        context = browser.new_context(viewport={"width": 640, "height": 900})
        context.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(base + "/") else route.abort()
            ),
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        check(
            "browser default font is 32px on an unstyled document",
            page.evaluate("getComputedStyle(document.body).fontSize") == "32px",
        )
        page.goto(base + "/app")
        page.locator("#email").fill("sam@example.test")
        page.locator("#pw").fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        page.get_by_role("heading", name="My cases today").wait_for()
        check(
            "real app inherits the 32px browser default",
            page.evaluate("getComputedStyle(document.documentElement).fontSize") == "32px",
        )
        page.get_by_role("link", name="Overview", exact=True).click()
        page.locator(".map-cluster").first.wait_for()
        page.locator("#mapArea").select_option(label="Point examples")
        expect(page.locator(".map-marker")).to_have_count(3)
        page.get_by_role("button", name="Expand map", exact=True).click()
        page.locator(".map-marker:has(.map-symbol.hazard)").press("Enter")
        expect(page.locator(".map-home-card")).to_be_visible()
        geometry = page.evaluate(
            """() => {
              const dialog = document.querySelector('.map-dialog');
              const workspace = dialog.querySelector('.map-workspace');
              const sidebar = dialog.querySelector('.map-info');
              const map = dialog.querySelector('.leafmap');
              return {
                viewport: innerWidth, rootFont: getComputedStyle(document.documentElement).fontSize,
                documentWidth: document.documentElement.scrollWidth,
                dialogWidth: dialog.clientWidth, dialogScroll: dialog.scrollWidth,
                workspaceWidth: workspace.clientWidth, workspaceScroll: workspace.scrollWidth,
                sidebarWidth: sidebar.getBoundingClientRect().width,
                sidebarScroll: sidebar.scrollWidth, sidebarClient: sidebar.clientWidth,
                mapWidth: map.clientWidth, mapHeight: map.getBoundingClientRect().height,
                minimumHeight: 14 * parseFloat(getComputedStyle(document.documentElement).fontSize),
                filterWidth: dialog.querySelector('.overview-map-filters').clientWidth,
                filterScroll: dialog.querySelector('.overview-map-filters').scrollWidth
              };
            }"""
        )
        (out / "enlarged-font.json").write_text(json.dumps(geometry, indent=2), encoding="utf-8")
        check(
            "expanded map reflows at 640px with a 32px browser default",
            geometry["viewport"] == 640
            and geometry["documentWidth"] <= 640
            and geometry["dialogScroll"] <= geometry["dialogWidth"]
            and geometry["workspaceScroll"] <= geometry["workspaceWidth"]
            and geometry["sidebarScroll"] <= geometry["sidebarClient"]
            and geometry["sidebarWidth"] <= geometry["workspaceWidth"] * 0.45 + 1
            and geometry["mapWidth"] > 80,
        )
        check(
            "enlarged-text filters preserve width and minimum map height",
            geometry["filterScroll"] <= geometry["filterWidth"]
            and geometry["mapHeight"] >= geometry["minimumHeight"],
        )
        for button in page.locator(".overview-map-filters button").all():
            button.focus()
            expect(button).to_be_in_viewport()
            check(
                "enlarged-text filter labels fit",
                button.evaluate("el => el.scrollWidth <= el.clientWidth"),
            )
        close = page.get_by_role("button", name="Close home summary", exact=True)
        close.scroll_into_view_if_needed()
        expect(close).to_be_in_viewport()
        close.click()
        expect(page.locator(".map-home-card")).to_be_hidden()
        expect(page.locator(".map-marker:has(.map-symbol.hazard)")).to_be_focused()
        scan(page, axe, reports, "expanded-640-default-font-32")
        page.screenshot(path=str(out / "expanded-640-default-font-32.png"))
        page.get_by_role("button", name="Exit expanded map", exact=True).click()
        expect(page.get_by_role("dialog")).to_have_count(0)
        expect(page.get_by_role("button", name="Expand map", exact=True)).to_be_focused()
        check(f"enlarged-font map has no uncaught JavaScript errors ({errors})", not errors)
    finally:
        browser.close()


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
            check_expanded_filters(page, base, axe, out, reports)
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
            check_pending_navigation(page, out)
            check_session_expiry(page, base, out)
            check_enlarged_font(playwright, base, axe, out, reports)
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
