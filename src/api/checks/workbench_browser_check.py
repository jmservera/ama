"""Bounded shared-IA checks against the real API and constructed public fixtures."""

from __future__ import annotations

import copy
import json
import runpy
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, Route, sync_playwright

from checks.design_system_browser_check import ROOT, check, main

MANIFEST = json.loads(Path(__file__).with_name("workbench-manifest.json").read_text())


def synthetic_data() -> dict[str, Any]:
    data: dict[str, Any] = copy.deepcopy(
        runpy.run_path(str(ROOT / "src/core/tests/dataset.py"))["DATA"]
    )
    data["as_of"] = "2026-10-16"
    data["cases"] = [data["cases"][0], data["cases"][3], data["cases"][4]]
    data["cases"][2]["contractor"]["name"] = "Other Ltd"
    data["staff"] = [
        {
            "code": role["code"],
            "name": role["role"] + " Example",
            "email": role["email"],
            "role": role["role"],
            **({"contractor": "Test Ltd"} if role["role"] == "Contractor" else {}),
        }
        for role in MANIFEST["roles"]
    ]
    data["staff"].append(
        dict(
            code="OTHER",
            name="Other Contractor",
            email="other@example.test",
            role="Contractor",
            contractor="Other Ltd",
        )
    )
    for case in data["cases"]:
        owner = next(user for user in data["staff"] if user["code"] == case["owner_code"])
        case["owner"] = owner["name"]
        case["home"].update(lat=0, lon=0)
    data["cases"][1]["hazards"][0]["source"] = "Synthetic-source-" + "x" * 180
    data["cases"][0].update(stage_since="2026-10-15", reason="SYN-NEW-WORK")
    data["cases"][0]["documents"] = [
        dict(id="SYN-EPC-76", kind="EPC", at="2026-09-15", version=2)
    ]
    data["cases"][1]["hazards"][0].update(
        aware_at="2026-10-15T12:00:00Z", response_due_at="2026-10-15T18:00:00Z"
    )
    return data


def ids(page: Page) -> list[str]:
    values = page.locator(".item").evaluate_all(
        "els => els.map(el => decodeURIComponent(el.getAttribute('href').split('/').pop()))"
    )
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise TypeError("Case links must produce a list of string IDs")
    return [value for value in values if isinstance(value, str)]


def wait_cases(page: Page, count: int) -> None:
    page.wait_for_function(
        """count => document.querySelectorAll('.item').length === count
        && document.querySelector('#workspace-status').textContent.includes(`${count} case`)""",
        arg=count,
    )


def reflow(page: Page, label: str) -> None:
    check(
        label,
        page.evaluate("() => document.documentElement.scrollWidth <= innerWidth")
        and page.locator("#nav").is_visible(),
    )


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        errors: list[str] = []
        held: list[Route] = []
        try:
            for role in MANIFEST["roles"]:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                page.on("pageerror", lambda error: errors.append(str(error)))
                briefings: list[Route] = []
                if role["role"] == "Resident Liaison Officer":
                    page.route(
                        "**/api/briefing",
                        lambda route, _request, pending=briefings: pending.append(route),
                    )
                page.goto(base + "/app")
                page.locator("#email").fill(role["email"])
                page.locator("#pw").fill("synthetic-check")
                page.locator("button[type=submit]").click()
                page.get_by_role(
                    "heading",
                    name="Your jobs" if role["role"] == "Contractor" else "My cases today",
                    exact=True,
                ).wait_for()
                page.wait_for_function(
                    "n => document.querySelectorAll('.item').length === n", arg=len(role["ids"])
                )
                check(f"{role['role']} independent own IDs/order", ids(page) == role["ids"])
                check(
                    f"{role['role']} exact server-described navigation",
                    page.locator("#nav a").evaluate_all(
                        "els => els.map(el => el.getAttribute('href'))"
                    )
                    == role["navigation"],
                )
                check(
                    f"{role['role']} current own queue",
                    page.locator("#nav [aria-current=page]").get_attribute("href") == "#/",
                )
                finance = page.request.get(base + "/api/finance")
                check(
                    f"{role['role']} existing Finance endpoint authority",
                    finance.status == (200 if "#/finance" in role["navigation"] else 403),
                )
                if role["role"] == "Contractor":
                    detail = page.request.get(base + "/api/cases/ZF-4").json()
                    check(
                        "contractor projection and other-provider scope unchanged",
                        "resident" not in detail
                        and "hazards" not in detail
                        and page.request.get(base + "/api/cases/ZF-5").status == 404,
                    )
                if role["role"] == "Building Safety Liaison":
                    page.goto(base + "/app#/case/ZF-4")
                    page.get_by_role(
                        "heading", name="Safety referrals and stopped retrofit work"
                    ).wait_for()
                    check(
                        "safety-role permitted deep link", page.locator("#hz-source").is_visible()
                    )
                if role["role"] == "Grants and Evidence Officer":
                    page.get_by_role("link", name="Finance", exact=True).click()
                    page.wait_for_url("**#/finance")
                    page.wait_for_function(
                        "() => document.querySelector('#nav [aria-current=page]')"
                        ".getAttribute('href') === '#/finance'"
                    )
                if role["role"] != "Resident Liaison Officer":
                    context.close()
                    continue

                wait_cases(page, 2)
                page.wait_for_function(
                    "() => document.querySelector('.ai')?.textContent"
                    ".includes('Reading your cases...')"
                )
                check("initial briefing held before queue navigation", len(briefings) == 1)
                page.get_by_role("link", name="All cases", exact=True).click()
                wait_cases(page, 3)
                page.get_by_role("link", name="My cases", exact=True).click()
                wait_cases(page, 2)
                check("cancelled briefing retried on each queue return", len(briefings) == 3)
                briefings[-1].fulfill(
                    json={"text": "Current synthetic briefing", "label": "Synthetic check"}
                )
                page.get_by_text("Current synthetic briefing", exact=True).wait_for()
                for obsolete in briefings[:-1]:
                    obsolete.fulfill(
                        json={"text": "Obsolete synthetic briefing", "label": "Synthetic check"}
                    )
                page.wait_for_timeout(100)
                check(
                    "late cancelled briefings cannot replace the recovered briefing",
                    page.get_by_role("heading", name="Today's briefing", exact=True).count() == 1
                    and page.get_by_text("Current synthetic briefing", exact=True).is_visible()
                    and page.get_by_text("Reading your cases...", exact=True).count() == 0
                    and page.get_by_text("Obsolete synthetic briefing", exact=True).count() == 0,
                )
                page.get_by_role("link", name="All cases", exact=True).click()
                wait_cases(page, 3)
                page.get_by_role("link", name="My cases", exact=True).click()
                wait_cases(page, 2)
                check(
                    "completed briefing stays cached across queue navigation",
                    len(briefings) == 3
                    and page.get_by_text("Current synthetic briefing", exact=True).is_visible(),
                )
                page.unroute("**/api/briefing")
                page.route(
                    "**/api/briefing?mode=workflow",
                    lambda route: route.fulfill(
                        status=503, json={"error": "Synthetic briefing failure"}
                    ),
                    times=1,
                )
                page.locator("#wf-mode").check()
                page.get_by_role("alert").filter(has_text="Synthetic briefing failure").wait_for()
                page.route(
                    "**/api/briefing?mode=workflow",
                    lambda route: route.fulfill(
                        json={"text": "Retried synthetic briefing", "label": "Synthetic check"}
                    ),
                    times=1,
                )
                page.get_by_role("button", name="Try loading briefing again").click()
                page.get_by_text("Retried synthetic briefing", exact=True).wait_for()
                check(
                    "briefing failure explicitly retries in the selected workflow mode",
                    page.locator("#wf-mode").is_checked()
                    and page.get_by_role("alert").count() == 0,
                )
                before = page.request.get(base + "/api/cases/ZF-4").json()
                page.locator(".skip-link").focus()
                page.keyboard.press("Enter")
                check(
                    "keyboard skip focuses main without changing route",
                    page.locator("#app").evaluate("el => el === document.activeElement"),
                )
                for width in MANIFEST["widths"]:
                    page.set_viewport_size({"width": width, "height": 900})
                    reflow(page, f"own queue reflow {width}px")
                    check(
                        f"safety marker retained {width}px",
                        page.locator(".item .flag.danger").is_visible(),
                    )
                    page.locator('.item[href="#/case/ZF-4"]').focus()
                    page.keyboard.press("Enter")
                    safety = page.get_by_role(
                        "heading", name="Safety referrals and stopped retrofit work"
                    )
                    safety.wait_for()
                    reflow(page, f"hazard case reflow {width}px with long source")
                    check(
                        f"safety controls expanded before routine forms {width}px",
                        page.locator("#hz-source").is_visible()
                        and safety.evaluate(
                            "el => !!(el.compareDocumentPosition("
                            "document.querySelector('#outcome'))"
                            " & Node.DOCUMENT_POSITION_FOLLOWING)"
                        ),
                    )
                    page.get_by_role("link", name="Back to the list", exact=True).focus()
                    page.keyboard.press("Enter")
                    wait_cases(page, 2)
                page.set_viewport_size({"width": 1280, "height": 900})
                page.evaluate("() => { document.documentElement.style.fontSize = '200%'; }")
                reflow(page, "queue 200% root text enlargement")
                page.locator('.item[href="#/case/ZF-4"]').click()
                page.locator("#hz-source").wait_for()
                reflow(page, "hazard case 200% root text enlargement")
                page.get_by_role("link", name="Back to the list", exact=True).click()
                wait_cases(page, 2)
                page.evaluate("() => { document.documentElement.style.fontSize = '100%'; }")

                page.get_by_role("link", name="All cases", exact=True).click()
                wait_cases(page, 3)
                check(
                    "independent all-case membership/order", ids(page) == MANIFEST["all_case_ids"]
                )
                page.locator("#f-q").fill("Pat")
                page.locator('.item[href="#/case/ZF-4"]').click()
                page.locator("#hz-source").wait_for()
                page.get_by_role("link", name="Back to the list", exact=True).click()
                wait_cases(page, 3)
                check(
                    "type-before-debounce and all-scope return",
                    page.locator("#f-q").input_value() == "Pat" and page.url.endswith("#/all"),
                )
                page.locator("#f-q").fill("no-such-home")
                page.get_by_text("No cases match these filters.", exact=False).wait_for()
                page.locator("#f-sort").select_option("name")
                page.locator("#reset-queue").focus()
                page.keyboard.press("Enter")
                wait_cases(page, 2)
                check(
                    "reset exact IDs/order, own scope, urgent sort, search, focus and announcement",
                    ids(page) == role["ids"]
                    and page.url.endswith("#/")
                    and page.locator("#f-q").input_value() == ""
                    and page.locator("#f-sort").input_value() == "urgent"
                    and page.locator("#reset-queue").evaluate("el => el === document.activeElement")
                    and "My assigned cases. 2 cases"
                    in page.locator("#workspace-status").inner_text(),
                )
                page.get_by_text("Queue definitions", exact=True).click()
                check(
                    "six visible engineering definitions and unapproved priority limitation",
                    page.locator(".side details dt").count() == 6
                    and "approval with a named owner is not recorded" in page.locator(".side details").inner_text(),
                )
                for queue, expected in (
                    ("new", ["ZF-1"]), ("stale", ["ZF-1"]),
                    ("overdue", ["ZF-4"]), ("priority", []), ("unowned", []),
                ):
                    with page.expect_response(
                        lambda response: "/api/cases?" in response.url
                        and f"queue={queue}" in response.url
                    ):
                        page.locator("#f-queue").select_option(queue)
                    wait_cases(page, len(expected))
                    check(f"{queue} queue exact expected IDs", ids(page) == expected)
                page.locator("#f-queue").select_option("overdue")
                wait_cases(page, 1)
                check(
                    "queue clock and named owner use recorded snapshot",
                    "12 elapsed hours" in page.locator(".item").inner_text()
                    and "Bea Safe" in page.locator(".item").inner_text()
                    and "2026-10-16" in page.locator(".item").inner_text(),
                )
                queue_context = page.locator(".item .work-context").inner_text()
                page.locator(".item").click()
                page.get_by_role("heading", name="Recorded task context", exact=True).wait_for()
                check(
                    "queue case history and suggestion current context agree",
                    page.locator(".work-context").count() == 3
                    and all(text == queue_context
                            for text in page.locator(".work-context").all_inner_texts()),
                )
                page.get_by_text("Blocked steps and prerequisites", exact=True).click()
                check(
                    "blocked step reason owner and next action are visible",
                    "Safety review" in page.locator("[aria-label='Recorded task context']").inner_text()
                    and "Named owner: Bea Safe" in page.locator("[aria-label='Recorded task context']").inner_text(),
                )
                page.get_by_text("Task sources", exact=True).click()
                check(
                    "source trace belongs to selected case",
                    "Case ZF-4" in page.locator("[aria-label='Recorded task context']").inner_text(),
                )
                page.get_by_role("link", name="Back to the list", exact=True).click()
                wait_cases(page, 1)
                page.locator("#reset-queue").click()
                wait_cases(page, 2)
                page.locator('.item[href="#/case/ZF-1"]').click()
                page.get_by_role("heading", name="Recorded task context", exact=True).wait_for()
                check(
                    "case switching refreshes reason source and clock without carryover",
                    "SYN-NEW-WORK" in page.locator(".work-context").first.inner_text()
                    and "case:ZF-1/stage" in page.locator(".work-context").first.inner_text()
                    and "Bea Safe" not in page.locator(".work-context").first.inner_text(),
                )
                page.get_by_role("link", name="Back to the list", exact=True).click()
                wait_cases(page, 2)
                page.get_by_role("link", name="All cases", exact=True).click()
                wait_cases(page, 3)
                for key, value in (
                    ("stage", "Contacting resident"), ("area", "Test"), ("wave", "Wave 1"),
                    ("owner", "RLO-01"), ("flag", "hazard"), ("queue", "overdue"),
                ):
                    page.locator(f"#f-{key}").select_option(value)
                page.locator("#f-q").fill("Pat")
                page.locator("#f-sort").select_option("name")
                page.locator("#reset-queue").click()
                wait_cases(page, 2)
                check(
                    "single reset clears every queue override and selection",
                    all(page.locator(f"#f-{key}").input_value() == ""
                        for key in ("q", "stage", "area", "wave", "flag", "queue"))
                    and page.locator("#f-owner").count() == 0
                    and page.locator("#f-sort").input_value() == "urgent"
                    and page.url.endswith("#/")
                    and page.locator(".work-context").count() == 2
                    and "work-queues-1; selection: none"
                    in page.locator("#workspace-status").inner_text(),
                )

                def delay_name(route: Route) -> None:
                    if "sort=name" in route.request.url:
                        held.append(route)
                    else:
                        route.continue_()

                page.route("**/api/cases?**", delay_name)
                page.locator("#f-sort").select_option("name")
                page.wait_for_timeout(100)
                check("delayed list request intercepted", len(held) == 1)
                page.locator("#reset-queue").click()
                wait_cases(page, 2)
                held[0].fulfill(json={"items": [], "total": 0})
                page.wait_for_timeout(100)
                check(
                    "late pre-reset result cannot replace restored queue", ids(page) == role["ids"]
                )
                page.unroute("**/api/cases?**", delay_name)
                held.clear()
                page.route("**/api/facets", lambda route: held.append(route), times=1)
                page.get_by_role("link", name="All cases", exact=True).click()
                page.wait_for_timeout(100)
                check("delayed obsolete route intercepted", len(held) == 1)
                page.get_by_role("link", name="Overview", exact=True).click()
                page.get_by_role("heading", name="Overview", exact=True).wait_for()
                held[0].fulfill(json=page.request.get(base + "/api/facets").json())
                page.wait_for_timeout(100)
                check(
                    "obsolete queue cannot replace newer route",
                    page.get_by_role("heading", name="Overview", exact=True).is_visible()
                    and page.locator("#nav [aria-current=page]").get_attribute("href")
                    == "#/overview",
                )
                page.get_by_role("link", name="My cases", exact=True).click()
                wait_cases(page, 2)
                page.locator('.item[href="#/case/ZF-4"]').click()
                page.locator("#hz-source").wait_for()
                page.go_back()
                wait_cases(page, 2)
                page.go_forward()
                page.locator("#hz-source").wait_for()
                check(
                    "history restores case with own-queue current link",
                    page.locator("#nav [aria-current=page]").get_attribute("href") == "#/",
                )
                page.get_by_role("link", name="Back to the list", exact=True).click()
                wait_cases(page, 2)
                page.route(
                    "**/api/cases?**",
                    lambda route: route.fulfill(
                        status=503, json={"error": "Synthetic load failure"}
                    ),
                    times=1,
                )
                page.locator("#f-sort").select_option("name")
                page.get_by_role("alert").filter(has_text="Synthetic load failure").wait_for()
                check(
                    "list failure explicitly announced",
                    "Cases unavailable" in page.locator("#workspace-status").inner_text(),
                )
                page.get_by_role("button", name="Try loading cases again").click()
                wait_cases(page, 2)
                page.locator("#reset-queue").click()
                wait_cases(page, 2)
                after = page.request.get(base + "/api/cases/ZF-4").json()
                check(
                    "navigation/filter/reset leave complete case record unchanged", before == after
                )
                def alternate_default(route: Route) -> None:
                    response = route.fetch()
                    payload = response.json()
                    payload["work_queues"]["default"]["sort"] = "name"
                    payload["work_queues"]["version"] = "synthetic-default-contract"
                    route.fulfill(response=response, json=payload)

                page.route("**/api/me", alternate_default, times=1)
                page.reload()
                wait_cases(page, 2)
                page.locator("#f-sort").select_option("urgent")
                with page.expect_response(
                    lambda response: "/api/cases?" in response.url and "sort=name" in response.url
                ):
                    page.locator("#reset-queue").click()
                wait_cases(page, 2)
                check(
                    "reset consumes server default rather than a hardcoded browser order",
                    page.locator("#f-sort").input_value() == "name"
                    and "synthetic-default-contract" in page.locator("#workspace-status").inner_text()
                    and page.locator("#reset-queue").evaluate("el => el === document.activeElement"),
                )
                page.route(
                    "**/api/cases?**",
                    lambda route: route.fulfill(status=401, json={"error": "Synthetic expiry"}),
                    times=1,
                )
                page.locator("#f-sort").select_option("urgent")
                page.get_by_role("heading", name="Sign in", exact=True).wait_for()
                check(
                    "expired session returns explicit sign-in, no stale queue",
                    not page.locator("#nav").is_visible() and page.locator(".item").count() == 0,
                )
                context.close()
            check(f"no uncaught JavaScript errors in shared IA checks ({errors})", not errors)
            print(
                f"Manifest {MANIFEST['version']}; Chromium {browser.version}; "
                "partial AC-034/043 only."
            )
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, synthetic_data)
