"""Verify employee briefing scope on the real server using public synthetic fixtures."""

from __future__ import annotations

from typing import Any

from playwright.sync_api import Route, sync_playwright

from checks.design_system_browser_check import check, main
from checks.workbench_browser_check import MANIFEST, ids, synthetic_data, wait_cases
from zava_forward.core.workflows import MANAGER_ROLES


def briefing_data() -> dict[str, Any]:
    data = synthetic_data()
    for case in data["cases"]:
        for document in case.get("documents", []):
            document["name"] = f"synthetic-{document['id']}.pdf"
    return data


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for role in MANIFEST["roles"]:
                if role["role"] == "Contractor":
                    continue
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                context.route("**/*", lambda route: route.continue_()
                              if route.request.url.startswith(base + "/") else route.abort())
                page = context.new_page()
                held: list[Route] = []
                page.route("**/api/cases?**", lambda route: held.append(route))
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                try:
                    page.goto(base + "/app")
                    page.locator("#email").fill(role["email"])
                    page.locator("#pw").fill("synthetic-check")
                    page.get_by_role("button", name="Sign in", exact=True).click()
                    page.get_by_role("heading", name="My cases today", exact=True).wait_for()
                    manager = role["role"] in MANAGER_ROLES
                    label = "All programme cases" if manager else "My assigned cases"
                    section = page.locator("section.ai").filter(
                        has=page.get_by_role("heading", name="Today's briefing", exact=True)
                    )
                    section.get_by_role("heading", name=label, exact=True).wait_for()
                    check(f"{role['role']} briefing loads independently of queue", len(held) == 1)
                    held[0].continue_()
                    page.unroute("**/api/cases?**")
                    wait_cases(page, len(role["ids"]))
                    response = page.request.get(base + "/api/briefing?mode=workflow")
                    check(f"{role['role']} briefing request authorized", response.status == 200)
                    briefing = response.json()
                    expected = len(MANIFEST["all_case_ids"] if manager else role["ids"])
                    check(f"{role['role']} API label and full count",
                          briefing["scope_label"] == label and briefing["case_count"] == expected)
                    check(f"{role['role']} renders programme/personal scope",
                          f"{expected} permitted open" in section.inner_text()
                          and f"{min(expected, 3)} included in this summary"
                          in section.inner_text())
                    check(f"{role['role']} retains exact personal queue", ids(page) == role["ids"])
                    if manager:
                        check(f"{role['role']} briefing does not claim personal cases",
                              "your cases" not in section.inner_text().lower())
                    if role["role"] == "Programme Support Officer":
                        check("unassigned manager still has programme briefing",
                              expected > 0 and not ids(page)
                              and "No open cases are assigned to you."
                              in page.locator("main").inner_text())
                    toggle = section.get_by_label("How to prepare briefings and draft requests")
                    toggle.focus()
                    with page.expect_response(
                        lambda result: "/api/briefing?mode=workflow" in result.url
                    ):
                        toggle.select_option("workflow")
                    section.get_by_role("heading", name=label, exact=True).wait_for()
                    check(f"{role['role']} workflow choice retains scope",
                          toggle.input_value() == "workflow")
                    for width in (320, 390, 1280):
                        page.set_viewport_size({"width": width, "height": 900})
                        check(f"{role['role']} briefing reflows at {width}px",
                              page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
                    check(f"{role['role']} has no uncaught JavaScript errors", not errors)
                finally:
                    context.close()
            print(f"Chromium {browser.version}; synthetic loopback only; "
                  "no live AI, SQL Server or Azure.")
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, briefing_data)
