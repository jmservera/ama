"""Issue 1836: the map result count and the tile fallback note are separate, unambiguous statuses.

The map sidebar holds two adjacent ``role=status`` paragraphs: the count notice and the tile
fallback note. A selector that matches both is rejected by Playwright strict mode in every tile
state. This check uses synthetic data, a real loopback API and synthetic tile responses; it
never reaches an external map service.
"""

from __future__ import annotations

import base64
import re

from checks.design_system_browser_check import check, main
from playwright.sync_api import Browser, Locator, Page, Route, expect, sync_playwright

TILE_HOST = "https://tile.openstreetmap.org/"
TILE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)
# Matches the count notice and the tile note, so it is ambiguous. Use count_notice or tile_notice.
MAP_STATUSES = ".map-info [role=status]"
COUNT_NOTICE = re.compile(r"^\d+ homes? shown$")
TILE_FALLBACK_TEXT = "The map background could not load."


def count_notice(page: Page) -> Locator:
    """The result count notice, for example "0 homes shown"."""
    return page.locator(MAP_STATUSES).filter(has_text=COUNT_NOTICE)


def tile_notice(page: Page) -> Locator:
    """The tile fallback note: empty until a tile fails, then the fallback message.

    Not an adjacent-sibling selector: the hidden retry button sits between the two statuses.
    """
    return page.locator(MAP_STATUSES).filter(has_not_text=COUNT_NOTICE)


def check_old_locator_is_ambiguous(page: Page, state: str) -> None:
    """INTENTIONAL regression demonstration: the pre-fix locator must hit strict mode."""
    old = page.locator(MAP_STATUSES)
    expect(old).to_have_count(2)
    try:
        expect(old).to_have_text("0 homes shown", timeout=1000)
    except AssertionError as error:
        message = str(error)
    else:
        message = ""
    check(
        f"INTENTIONAL demonstration, not a harness failure ({state}): "
        "the old ambiguous locator raises a strict-mode violation",
        "strict mode violation" in message and "resolved to 2 elements" in message,
    )


def check_tile_state(browser: Browser, base: str, tiles_available: bool) -> None:
    state = "tiles available" if tiles_available else "tiles unavailable"
    external: list[str] = []

    def route(route: Route) -> None:
        url = route.request.url
        if url.startswith(base + "/"):
            route.continue_()
            return
        external.append(url)
        if tiles_available and url.startswith(TILE_HOST):
            route.fulfill(content_type="image/png", body=TILE_PNG)
        else:
            route.abort()

    context = browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        context.route("**/*", route)
        page = context.new_page()
        page.goto(base + "/app")
        page.locator("#email").fill("sam@example.test")
        page.locator("#pw").fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        page.get_by_role("heading", name="My cases today").wait_for()
        page.get_by_role("link", name="Overview", exact=True).click()
        page.locator(".map-cluster").first.wait_for()
        page.locator("#mapArea").select_option(label="Point examples")
        expect(page.locator(".map-marker")).to_have_count(3)
        expect(count_notice(page)).to_have_text("3 homes shown")

        page.get_by_role("button", name="Residents needing extra support", exact=False).click()
        expect(page.locator(".map-marker")).to_have_count(0)
        expect(count_notice(page)).to_have_count(1)
        expect(count_notice(page)).to_have_text("0 homes shown")
        expect(tile_notice(page)).to_have_count(1)
        check_old_locator_is_ambiguous(page, state)

        if tiles_available:
            loaded = page.locator(".leaflet-tile-loaded")
            expect(loaded.first).to_be_attached()
            expect(page.locator(".leaflet-tile:not(.leaflet-tile-loaded)")).to_have_count(0)
            expect(tile_notice(page)).to_have_text("")
            expect(tile_notice(page)).to_be_hidden()
        else:
            expect(tile_notice(page)).to_be_visible()
            expect(tile_notice(page)).to_contain_text(TILE_FALLBACK_TEXT)
        expect(count_notice(page)).not_to_contain_text("background")
        expect(count_notice(page)).to_have_text("0 homes shown")
        check(
            f"{state}: exact zero count is independent of the tile fallback",
            True,
        )
        check(
            f"{state}: only the synthetic tile host was requested, and nothing left the check",
            bool(external) and all(url.startswith(TILE_HOST) for url in external),
        )
    finally:
        context.close()


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            check_tile_state(browser, base, tiles_available=True)
            check_tile_state(browser, base, tiles_available=False)
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser)
