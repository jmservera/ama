"""Real synthetic API, URL/history, keyboard, reflow and pinned axe checks for #533."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import Route, expect, sync_playwright
from test_progress_dashboard import synthetic_data

from checks.design_system_browser_check import check, main
from checks.regulatory_ux_check import AXE_SHA256


def data_factory() -> dict[str, Any]:
    data = synthetic_data()
    for index in range(21):
        case = copy.deepcopy(data["cases"][0])
        case["id"] = f"SYN-ARCHIVE-{index:03}"
        case["resident"]["name"] = f"Fictional resident {index}"
        data["cases"].append(case)
    return data


def run(axe: Path, out: Path) -> None:
    if hashlib.sha256(axe.read_bytes()).hexdigest() != AXE_SHA256:
        raise ValueError("Use the existing pinned axe-core 4.10.3 asset.")
    reports: list[dict[str, Any]] = []

    def browser_check(base: str) -> None:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(base + "/app#/progress")
                page.locator("#email").fill("pam@example.test")
                page.locator("#pw").fill("synthetic-check")
                page.get_by_role("button", name="Sign in", exact=True).click()
                page.get_by_role("heading", name="Progress summary", exact=True).wait_for()
                expect(page.locator(".progress-page")).to_contain_text("Demonstration data")
                data = page.request.get(base + "/api/progress").json()
                page.locator("#progress-start").fill("2026-09-28")
                page.locator("#progress-end").fill("2026-10-07")
                page.get_by_role("button", name="Apply filters").click()
                page.wait_for_url("**#/progress?start=2026-09-28&end=2026-10-07")
                page.get_by_role("heading", name="Progress summary", exact=True).wait_for()
                data = page.request.get(
                    base + "/api/progress?start=2026-09-28&end=2026-10-07"
                ).json()
                charts = page.locator(".progress-chart")
                expect(charts).to_have_count(6)
                check("all six charts have table alternatives", charts.count() == 6)
                expected_series = [
                    [[r[k] for k in ("opened", "closed", "reopened")] for r in data["daily"]],
                    [[r[k] for k in ("opened", "closed", "reopened")] for r in data["weekly"]],
                    [[r["backlog"]] for r in data["daily"]],
                    [[r["count"]] for r in data["current"]["journey"]],
                    [[r["count"]] for r in data["current"]["teams"]],
                    [[r["count"]] for r in data["ai"]["outcomes"]],
                ]
                for index, expected in enumerate(expected_series):
                    chart = charts.nth(index)
                    chart.locator("summary").focus()
                    chart.locator("summary").press("Enter")
                    expect(chart.locator("table")).to_be_visible()
                    actual = chart.locator("tbody tr").evaluate_all(
                        "rows => rows.map(row => [...row.querySelectorAll('td')]"
                        ".map(cell => Number(cell.textContent.replaceAll(',', ''))))"
                    )
                    bars = chart.locator("meter").evaluate_all("els => els.map(el => el.value)")
                    check(
                        f"chart {index} table and bars match real API",
                        actual == expected and bars == [value for row in expected for value in row],
                    )
                expect(page.locator(".progress-page")).to_contain_text("Stalled cases now")
                expect(page.locator(".progress-page")).to_contain_text("not a legal deadline")

                def scan(name: str) -> None:
                    page.evaluate(axe.read_text())
                    result = page.evaluate(
                        "async () => await axe.run(document.querySelector('main'), "
                        "{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})"
                    )
                    reports.append(dict(state=name, **result))
                    (out / f"{name}-axe.json").write_text(json.dumps(result))
                    check(name + " axe has no violations", not result["violations"])

                for width in (320, 390, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    if page.evaluate("() => document.documentElement.scrollWidth > innerWidth"):
                        print(
                            page.evaluate("""() => [...document.querySelectorAll('body *')]
                          .filter(el => el.getBoundingClientRect().right > innerWidth)
                          .map(el => ({tag: el.tagName, class: el.className,
                            right: el.getBoundingClientRect().right})).slice(0,20)""")
                        )
                    check(
                        f"dashboard reflows at {width}",
                        page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
                    )
                page.emulate_media(reduced_motion="reduce")
                scan("dashboard")
                page.get_by_role("link", name="Closed cases", exact=True).click()
                page.get_by_role("table", name="Matching closed cases", exact=True).wait_for()
                expect(page.locator("#closed-results")).to_have_text(
                    "24 matching closed cases. Page 1 of 2."
                )
                page.get_by_role("link", name="Next page", exact=True).click()
                page.wait_for_url("**#/closed?page=2")
                expect(page.locator("#closed-results")).to_contain_text("Page 2 of 2")
                check("last page has four cases", page.locator("tbody tr").count() == 4)
                page.reload()
                expect(page.locator("#closed-results")).to_contain_text("Page 2 of 2")
                page.get_by_role("link", name="Previous page", exact=True).click()
                expect(page.locator("#closed-results")).to_contain_text("Page 1 of 2")
                page.go_back()
                expect(page.locator("#closed-results")).to_contain_text("Page 2 of 2")
                page.go_forward()
                expect(page.locator("#closed-results")).to_contain_text("Page 1 of 2")
                page.goto(base + "/app#/closed?page=999")
                expect(page.locator("#closed-results")).to_contain_text("Page 2 of 2")
                page.wait_for_url("**#/closed?page=2")
                page.locator("#progress-status").select_option("Withdrawn")
                page.locator("#progress-team").select_option("Quality Inspector")
                page.locator("#progress-start").fill("2026-10-04")
                page.locator("#progress-end").fill("2026-10-04")
                page.locator("#progress-q").fill("ZF-3")
                page.get_by_role("button", name="Apply filters").click()
                expect(page.locator("#closed-results")).to_have_text(
                    "1 matching closed cases. Page 1 of 1."
                )
                check(
                    "filters reset page and persist in URL",
                    "page=" not in page.url
                    and "team=Quality+Inspector" in page.url
                    and "status=Withdrawn" in page.url
                    and "q=ZF-3" in page.url,
                )
                page.reload()
                expect(page.locator("#progress-q")).to_have_value("ZF-3")
                expect(page.locator("tbody")).to_contain_text("Withdrawn")
                page.locator("#progress-q").fill("No such fictional case")
                page.get_by_role("button", name="Apply filters").click()
                expect(page.locator("#closed-results")).to_contain_text("0 matching closed cases")
                expect(page.locator("tbody")).to_contain_text("No recorded data")
                page.get_by_role("link", name="Reset filters", exact=True).click()
                page.get_by_role("table", name="Matching closed cases", exact=True).wait_for()
                # The safety fixture is on page two in stable reference order.
                page.get_by_role("link", name="Next page", exact=True).click()
                expect(page.locator("tbody")).to_contain_text("Safety issue open")
                page.goto(base + "/app#/closed")
                page.locator("#progress-q").wait_for()
                page.locator("#progress-q").fill("edited")
                page.get_by_role("link", name="Reset filters", exact=True).click()
                expect(page.locator("#progress-q")).to_have_value("")
                page.goto(base + "/app#/closed")
                for width in (320, 390, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    check(
                        f"archive reflows at {width}",
                        page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
                    )
                page.locator("#progress-q").focus()
                check(
                    "keyboard focus visible",
                    page.locator("#progress-q").evaluate(
                        "el => getComputedStyle(el).outlineStyle === 'solid'"
                    ),
                )
                scan("closed-cases")
                for name, path, start, end in (
                    ("dashboard-reversed", "#/progress", "2026-10-08", "2026-10-07"),
                    ("dashboard-oversized", "#/progress", "2020-01-01", "2026-10-07"),
                    ("archive-reversed", "#/closed", "2026-10-08", "2026-10-07"),
                    ("dashboard-default-end", "#/progress", "2026-10-08", None),
                ):
                    if end is None:
                        page.goto(base + f"/app{path}?start={start}")
                    else:
                        page.goto(base + "/app" + path)
                        if path == "#/closed":
                            page.get_by_role("table", name="Matching closed cases").wait_for()
                        else:
                            page.get_by_role("heading", name="Progress summary").wait_for()
                        page.locator("#progress-start").fill(start)
                        page.locator("#progress-end").fill(end)
                        page.get_by_role("button", name="Apply filters").click()
                    expect(page.locator(".field-error")).to_have_count(2)
                    expect(page.locator("#progress-start")).to_be_focused()
                    for field, value in (("start", start), ("end", end or "")):
                        control = page.locator(f"#progress-{field}")
                        expect(control).to_have_value(value)
                        expect(control).to_have_attribute("aria-invalid", "true")
                        expect(control).to_have_attribute(
                            "aria-describedby", f"progress-{field}-error"
                        )
                        message = page.locator(f"#progress-{field}-error")
                        expect(message).to_be_visible()
                        expect(message).to_contain_text("end date on or after the start")
                        if name == "dashboard-oversized":
                            expect(message).to_contain_text("at most 366 days")
                    expect(page.get_by_role("alert")).to_have_count(0)
                    expect(page.get_by_role("button", name="Try again")).to_have_count(0)
                    scan(name)
                    page.locator("#progress-start").fill("2026-10-01")
                    page.locator("#progress-end").fill("2026-10-07")
                    page.get_by_role("button", name="Apply filters").click()
                    if path == "#/closed":
                        page.get_by_role("table", name="Matching closed cases").wait_for()
                    else:
                        page.get_by_role("heading", name="Progress summary").wait_for()
                    expect(page.locator("[aria-invalid=true]")).to_have_count(0)
                    expect(page.locator(".field-error")).to_have_count(0)
                    for field in ("start", "end"):
                        check(
                            name + f" clears {field} error association after correction",
                            page.locator(f"#progress-{field}").get_attribute("aria-describedby")
                            is None,
                        )
                    scan(name + "-recovered")

                page.goto(base + "/app#/progress?start=2025-10-07&end=2026-10-07")
                page.get_by_role("heading", name="Progress summary").wait_for()
                expect(page.get_by_role("alert")).to_have_count(0)
                expect(page.locator("[aria-invalid=true]")).to_have_count(0)
                check("inclusive 366-day dashboard range remains valid", True)
                page.goto(base + "/app#/closed?start=2020-01-01&end=2026-10-07")
                page.get_by_role("table", name="Matching closed cases").wait_for()
                expect(page.locator("[aria-invalid=true]")).to_have_count(0)
                check("archive has no dashboard duration cap", True)

                def fail(route: Route) -> None:
                    route.fulfill(
                        status=503, json={"error": "Synthetic progress read unavailable."}
                    )

                page.route("**/api/progress?*", fail)
                page.get_by_role("link", name="Progress dashboard", exact=True).click()
                expect(page.get_by_role("alert")).to_have_text(
                    "Synthetic progress read unavailable."
                )
                expect(page.locator("[aria-invalid=true], .field-error")).to_have_count(0)
                expect(page.locator("#progress-start")).not_to_have_attribute(
                    "aria-describedby", "progress-start-error"
                )
                expect(page.locator("main")).to_be_focused()
                scan("progress-read-failure")
                page.unroute("**/api/progress?*", fail)
                page.get_by_role("button", name="Try again", exact=True).click()
                page.get_by_role("heading", name="Progress summary", exact=True).wait_for()
                page.goto(base + "/app#/progress?unknown=value")
                expect(page.get_by_role("alert")).to_contain_text(
                    "Use each supported filter once."
                )
                expect(page.locator("[aria-invalid=true], .field-error")).to_have_count(0)
                expect(page.locator("main")).to_be_focused()
                check("unrelated validation failure does not invalidate date fields", True)
                held: list[Route] = []
                page.route("**/api/progress?*", lambda request: held.append(request))
                page.goto(base + "/app#/progress?start=2026-10-01&end=2026-10-07")
                expect(page.get_by_role("status").last).to_contain_text("Loading demonstration")
                page.get_by_role("link", name="Closed cases", exact=True).click()
                page.get_by_role("table", name="Matching closed cases", exact=True).wait_for()
                for request in held:
                    request.fulfill(json=data)
                expect(page.get_by_role("heading", name="Closed cases", exact=True)).to_be_visible()
                check(
                    "late progress response cannot overwrite another route", "#/closed" in page.url
                )
                check(f"no uncaught JavaScript errors ({errors})", not errors)
                (out / "browser.json").write_text(
                    json.dumps(
                        dict(
                            browser=browser.version,
                            axe_sha256=AXE_SHA256,
                            reports=reports,
                        )
                    )
                )
                page.screenshot(path=str(out / "closed-cases.png"), full_page=True)
            finally:
                browser.close()

    main(browser_check, data_factory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    run(args.axe, args.out)
