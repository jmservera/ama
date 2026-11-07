"""Browser evidence for the form schema catalogue download on the Funding screen (#80).

Run from src/api with the src packages and Playwright/Chromium installed:
PYTHONDONTWRITEBYTECODE=1 python -m checks.schema_download_browser_check

Real server authorization throughout: no route is mocked. The catalogue is registered through
the real POST /api/form-schemas as the Retrofit Programme Manager.
"""

from __future__ import annotations

import csv
import io
import runpy
import sys
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import ROOT, check, main
from checks.role_screens_fixtures import synthetic_data

SCREEN = "Funding route and claim pack"
LINK = 'a[href="/api/form-schemas.csv"]'
HEADER = [
    "definition",
    "digest",
    "approval",
    "approval_evidence",
    "source_policy_status",
    "recorded_by",
    "recorded_at",
]
SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
# Finance viewers without the resident-record or reason-view right: denied by forms._actor.
DENIED = ("support@example.test", "grants@example.test")


def schema_body() -> dict[str, Any]:
    tests = str(ROOT / "src/core/tests")
    if tests not in sys.path:
        sys.path.insert(0, tests)
    body: dict[str, Any] = runpy.run_path(str(ROOT / "src/core/tests/test_form_staging.py"))[
        "schema"
    ]()
    return body


def open_funding_screen(page: Page, base: str, email: str) -> None:
    page.goto(base + "/app")
    page.locator("#email").fill(email)
    page.locator("#pw").fill("synthetic-check")
    page.locator("button[type=submit]").click()
    page.locator("#nav").wait_for()
    page.get_by_role("link", name="Specialist screens", exact=True).click()
    page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
    page.get_by_role("link", name=SCREEN, exact=True).click()
    page.locator('a.item[href*="case=ZF-1"]').click()
    page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()


def tab_to_link(page: Page) -> bool:
    for _ in range(150):
        page.keyboard.press("Tab")
        if page.evaluate("(sel) => document.activeElement.matches(sel)", LINK):
            return True
    return False


def authorized_story(browser: Any, base: str) -> None:
    story = "pam catalogue download"
    context = browser.new_context(viewport={"width": 1280, "height": 900}, accept_downloads=True)
    try:
        page = context.new_page()
        errors: list[str] = []
        writes: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        open_funding_screen(page, base, "pam@example.test")
        registered = page.request.post(base + "/api/form-schemas", data=schema_body())
        check(
            f"{story} registers the synthetic schema through the real API", registered.status == 201
        )
        page.reload()
        page.get_by_role("region", name="Evidence for ZF-1", exact=True).wait_for()
        page.on(
            "request",
            lambda r: (
                writes.append(f"{r.method} {r.url}") if r.method not in SAFE_METHODS else None
            ),
        )
        link = page.locator(LINK)
        link.wait_for()
        check(f"{story} link text", link.inner_text() == "Download for Excel")
        check(f"{story} reaches the link by keyboard Tab", tab_to_link(page))
        with page.expect_download() as pending:
            page.keyboard.press("Enter")
        download = pending.value
        check(
            f"{story} suggests form-schemas.csv", download.suggested_filename == "form-schemas.csv"
        )
        with tempfile.TemporaryDirectory(prefix="zf-r9-") as scratch:
            saved = Path(scratch) / "form-schemas.csv"
            download.save_as(saved)
            rows = list(csv.reader(io.StringIO(saved.read_text(encoding="utf-8"))))
        check(f"{story} header is the catalogue columns: {rows[:1]}", rows[:1] == [HEADER])
        check(f"{story} has one catalogue row", len(rows) == 2)
        check(f"{story} row names the schema", "SYN-TECH" in rows[1][0])
        check(
            f"{story} row records the registrant",
            rows[1][HEADER.index("recorded_by")] == "pam@example.test",
        )
        check(f"{story} made no non-GET/HEAD/OPTIONS page requests: {writes}", not writes)
        check(f"{story} has no JavaScript errors: {errors}", not errors)
    finally:
        context.close()


def denied_story(browser: Any, base: str, email: str) -> None:
    story = f"{email.split('@')[0]} catalogue denied"
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        page = context.new_page()
        open_funding_screen(page, base, email)
        evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
        check(f"{story} shows no download link", page.locator(LINK).count() == 0)
        check(
            f"{story} says the review could not be read",
            "could not be read" in evidence.inner_text(),
        )
        direct = page.request.get(base + "/api/form-schemas.csv")
        body = direct.text()
        check(f"{story} direct export is refused: {direct.status}", direct.status == 403)
        check(
            f"{story} refusal is not an attachment",
            "attachment" not in direct.headers.get("content-disposition", ""),
        )
        check(
            f"{story} refusal leaks no catalogue content",
            not any(token in body for token in ("SYN-TECH", "pam@example.test", "definition")),
        )
    finally:
        context.close()


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            authorized_story(browser, base)
            for email in DENIED:
                denied_story(browser, base, email)
        finally:
            browser.close()
    print(
        "COMPLETE: catalogue download (authorized, keyboard) and denials checked; no axe scan here"
    )


if __name__ == "__main__":
    main(run_browser, synthetic_data)
