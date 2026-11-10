"""Browser evidence for the synthetic assisted aftercare journey (#133).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.aftercare_browser_check
Keyboard, focus and constructed-failure observations only; this is not assistive technology or human acceptance.
"""

from __future__ import annotations

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import check, main
from checks.workbench_browser_check import synthetic_data as workbench_data


def sign_in(page: Page, base: str, email: str) -> None:
    page.goto(base + "/app")
    page.locator("#email").fill(email)
    page.locator("#pw").fill("synthetic-check")
    page.locator("button[type=submit]").click()
    page.locator("#nav").wait_for()


def active_id(page: Page) -> str:
    return str(page.evaluate("() => document.activeElement && document.activeElement.id"))


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            sign_in(page, base, "sam@example.test")
            page.get_by_role("link", name="Aftercare concerns", exact=True).click()
            page.locator("#ac-form").wait_for()
            check(
                "synthetic notice is visible",
                "synthetic" in page.locator("main, #app").first.inner_text().lower(),
            )
            check(
                "no quality-note action on the intake screen",
                page.get_by_text("quality note", exact=False).count() == 0,
            )

            page.locator("#ac-form button[type=submit]").click()
            page.locator("#ac-error-summary").wait_for()
            check(
                "refused save moves focus to the error summary",
                active_id(page) == "ac-error-summary",
            )
            link = page.locator("#ac-error-summary a").first
            check(
                "error summary links to a field", (link.get_attribute("href") or "").startswith("#")
            )

            options = page.locator("#ac-home_ref option").all_inner_texts()
            check(
                f"home choices are the constructed allowlist: {options}",
                len([o for o in options if o.strip()]) >= 1,
            )
            page.locator("#ac-home_ref").select_option(index=len(options) - 1)
            page.locator("#ac-kind").select_option(index=1)
            page.locator("#ac-statement").fill("Synthetic: the loft hatch is cold to touch.")
            page.locator("#ac-channel").select_option(index=1)
            page.locator("#ac-next_update").fill("2099-01-01")
            raised = page.locator("#ac-raised_by")
            raised.select_option(index=1)
            request_id = page.locator("#ac-form").get_attribute("data-request-id")

            page.route(
                "**/api/aftercare/concerns",
                lambda route: (
                    route.abort() if route.request.method == "POST" else route.continue_()
                ),
            )
            page.locator("#ac-form button[type=submit]").click()
            page.locator("#ac-status", has_text="Saving could not be confirmed").wait_for()
            first_id = page.locator("#ac-form").get_attribute("data-request-id")
            check("uncertain save keeps a request reference", bool(first_id))
            check(
                "draft statement is kept after an uncertain save",
                "loft hatch" in page.locator("#ac-statement").input_value(),
            )

            page.evaluate("() => { location.hash = '#/map'; }")
            page.wait_for_function("() => !document.getElementById('ac-form')")
            page.get_by_role("link", name="Aftercare concerns", exact=True).click()
            page.locator("#ac-form").wait_for()
            check(
                "draft survives a route change",
                "loft hatch" in page.locator("#ac-statement").input_value(),
            )
            check(
                "same request reference after route change",
                page.locator("#ac-form").get_attribute("data-request-id") == first_id,
            )
            _ = request_id

            page.unroute("**/api/aftercare/concerns")
            page.locator("#ac-form button[type=submit]").click()
            page.locator("#ac-receipt-title").wait_for()
            check("receipt heading takes focus", active_id(page) == "ac-receipt-title")
            check(
                "receipt shows an unknown owner",
                "Unknown" in page.locator("main, #app").first.inner_text(),
            )
            page.get_by_role("button", name="Back to aftercare concerns").click()
            page.locator("#ac-list-title").wait_for()
            check(
                "recorded concern is listed",
                "AC-001" in page.locator("#ac-list-title + *").first.inner_text(),
            )
            check(
                "evaluator readback shows the unknown denominator",
                "nknown" in page.locator("#ac-eval-title").locator("xpath=..").inner_text(),
            )

            page.set_viewport_size({"width": 320, "height": 900})
            check(
                "reflow at 320px",
                page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
            )
            check(f"no JavaScript errors: {errors}", not errors)
            context.close()

            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            sign_in(page, base, "contractor@example.test")
            check(
                "contractor has no aftercare navigation",
                page.get_by_role("link", name="Aftercare concerns", exact=True).count() == 0,
            )
            context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, workbench_data)
