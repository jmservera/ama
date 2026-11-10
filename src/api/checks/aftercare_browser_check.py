"""Browser evidence for the synthetic assisted aftercare journey (#133).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.aftercare_browser_check
Keyboard, focus and constructed-failure observations only; this is not assistive technology or human acceptance.
"""

from __future__ import annotations

from playwright.sync_api import APIResponse, Browser, Dialog, Page, Route, sync_playwright

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


def fill_draft(page: Page, text: str) -> None:
    page.locator("#ac-home_ref").select_option(index=1)
    page.locator("#ac-kind").select_option(index=1)
    page.locator("#ac-statement").fill(text)
    page.locator("#ac-channel").select_option(index=1)
    page.locator("#ac-next_update").fill("2099-01-01")
    page.locator("#ac-raised_by").select_option(index=1)


def unload_prevented(page: Page) -> bool:
    return bool(
        page.evaluate(
            "() => { const e = new Event('beforeunload', {cancelable: true});"
            " window.dispatchEvent(e); return e.defaultPrevented; }"
        )
    )


def concern_count(page: Page) -> int:
    return int(
        page.evaluate(
            "async () => (await (await fetch('/api/aftercare/concerns')).json()).count"
        )
    )


def run_session_and_unload_checks(browser: Browser, base: str) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    posted: list[str] = []
    page.on(
        "request",
        lambda request: posted.append(request.post_data or "")
        if request.method == "POST" and request.url.endswith("/api/aftercare/concerns")
        else None,
    )
    sign_in(page, base, "sam@example.test")
    page.get_by_role("link", name="Aftercare concerns", exact=True).click()
    page.locator("#ac-form").wait_for()
    check("a pristine form does not warn on document navigation", not unload_prevented(page))
    fill_draft(page, "Synthetic: the back bedroom radiator stays cold.")
    check("an edited draft warns on document navigation", unload_prevented(page))
    page.evaluate("() => { location.hash = '#/map'; }")
    page.wait_for_function("() => !document.getElementById('ac-form')")
    check("the edited draft still warns after a safe hash-route change", unload_prevented(page))
    page.get_by_role("link", name="Aftercare concerns", exact=True).click()
    page.locator("#ac-form").wait_for()
    check(
        "hash routes keep the draft",
        "back bedroom" in page.locator("#ac-statement").input_value(),
    )

    before = concern_count(page)
    context.clear_cookies()
    page.locator("#ac-form button[type=submit]").click()
    page.locator("#email").wait_for()
    page.wait_for_timeout(300)
    check(
        "a real 401 on POST leaves the sign-in screen in place",
        page.locator("#email").is_visible() and page.locator("#ac-form").count() == 0,
    )
    check(
        "no stale staff data is shown after the 401",
        "Recorded concerns" not in page.locator("#app").inner_text(),
    )
    check("the unconfirmed draft still warns before a reload", unload_prevented(page))
    page.locator("#email").fill("sam@example.test")
    page.locator("#pw").fill("synthetic-check")
    page.locator("button[type=submit]").click()
    page.locator("#ac-form").wait_for()
    first = posted[-1]
    request_id = page.locator("#ac-form").get_attribute("data-request-id") or ""
    check(
        "same actor sees the original draft and request reference after sign-in",
        "back bedroom" in page.locator("#ac-statement").input_value()
        and bool(request_id)
        and request_id in first,
    )
    page.locator("#ac-form button[type=submit]").click()
    page.locator("#ac-receipt-title").wait_for()
    check("retry after sign-in saves once", concern_count(page) == before + 1)
    check("a confirmed receipt does not warn", not unload_prevented(page))

    page.get_by_role("button", name="Back to aftercare concerns").click()
    page.locator("#ac-form").wait_for()
    fill_draft(page, "Synthetic: late reply check.")
    held: list[tuple[Route, APIResponse]] = []

    def hold(route: Route) -> None:
        if route.request.method == "POST":
            held.append((route, route.fetch()))
        else:
            route.continue_()

    page.route("**/api/aftercare/concerns", hold)
    page.locator("#ac-form button[type=submit]").click()
    page.wait_for_function("() => true")
    page.evaluate("() => { location.hash = '#/map'; }")
    page.wait_for_function("() => !document.getElementById('ac-form')")
    page.wait_for_timeout(1000)
    page_before = page.locator("#app").inner_text()
    for route, response in held:
        try:
            route.fulfill(response=response)
        except Exception:
            pass
    page.wait_for_timeout(500)
    check(
        "a late reply cannot overwrite the page after a safe hash-route change",
        page.locator("#app").inner_text() == page_before
        and page.locator("#ac-form, #ac-receipt-title").count() == 0,
    )
    page.unroute("**/api/aftercare/concerns")
    check(f"no JavaScript errors in the session checks: {errors}", not errors)
    context.close()

    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    sign_in(page, base, "sam@example.test")
    page.get_by_role("link", name="Aftercare concerns", exact=True).click()
    page.locator("#ac-form").wait_for()
    fill_draft(page, "Synthetic: dialog check.")
    page.locator("#ac-statement").click()
    page.keyboard.type(" More detail.")
    dialogs: list[str] = []

    def on_dialog(dialog: Dialog) -> None:
        dialogs.append(dialog.type)
        dialog.dismiss()

    page.on("dialog", on_dialog)
    page.close(run_before_unload=True)
    page.wait_for_timeout(500)
    check(f"closing the tab with an edited draft raises a beforeunload dialog: {dialogs}", dialogs == ["beforeunload"])
    context.close()

    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    sign_in(page, base, "sam@example.test")
    page.get_by_role("link", name="Aftercare concerns", exact=True).click()
    page.locator("#ac-form").wait_for()
    fill_draft(page, "Synthetic: sign-out check.")
    page.locator("#account summary").click()
    page.locator("#signout").click(timeout=5000)
    page.wait_for_url("**/", timeout=10000)
    check(
        "explicit sign-out discards the draft without a warning",
        not page.evaluate("() => typeof acDraftState !== 'undefined' && acDraftState !== null"),
    )
    context.close()


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
            run_session_and_unload_checks(browser, base)
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, workbench_data)
