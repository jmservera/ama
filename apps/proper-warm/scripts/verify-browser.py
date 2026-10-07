"""Verify the synthetic local workbench against its rendered controls."""

import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://127.0.0.1:3410")
parser.add_argument("--artifacts", type=Path)
args = parser.parse_args()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(args.url, wait_until="networkidle")
    expect(page.locator("#demo-role")).to_be_enabled()
    expect(page.locator("#workflow-nav button")).to_have_count(10)
    expect(page.locator("#case-list .case-row")).to_have_count(9)
    expect(page.locator("#simulation-banner")).to_contain_text("Synthetic")

    def home(identifier):
        page.locator("#reset-button").click()
        page.locator("#search").fill(identifier)
        page.locator("#search-form").get_by_role("button", name="Search").click()
        expect(page.locator("#case-list .case-row")).to_have_count(1)
        page.locator("#case-list .case-row").click()
        expect(page.locator("#detail-heading")).to_have_text(identifier)

    def actor(role):
        page.locator("#demo-role").select_option(role)
        expect(page.locator("#case-detail")).to_have_attribute("aria-busy", "false")
        page.wait_for_load_state("networkidle")

    def source(reason):
        page.locator("#payload-reason").fill(reason)
        page.locator("#payload-source").fill("exercise:browser-validation")

    home("EX-HOME-531")
    actor("programme_manager")
    page.locator("#command-action").select_option("advance")
    source("Browser verifies a hazard hold never permits progression")
    page.get_by_role("button", name="Submit exercise command").click()
    expect(page.locator("#error-panel")).to_be_visible()
    expect(page.locator("#error-panel")).to_contain_text("GATE_BLOCKED")
    expect(page.locator("#pending-panel")).to_be_hidden()

    home("EX-HOME-900")
    actor("resident_officer")
    page.locator("#command-action").select_option("set_update")
    page.locator("#payload-dueAt").fill("2026-10-09T16:00:00Z")
    source("Browser records an independent synthetic resident-update commitment")
    before = page.locator(".version").inner_text()
    page.get_by_role("button", name="Submit exercise command").click()
    expect(page.locator("#status")).to_contain_text("Exercise command committed")
    assert page.locator(".version").inner_text() != before
    expect(page.locator("#case-detail")).to_contain_text("2026-10-09T16:00:00Z")

    page.locator("#assistant-mode").select_option("draft")
    page.get_by_role("button", name="Run simulator").click()
    expect(page.locator(".assistant-output")).to_contain_text("human review required")
    page.locator("#assistant-mode").select_option("failure")
    page.get_by_role("button", name="Run simulator").click()
    expect(page.locator("#error-panel")).to_be_visible()
    expect(page.locator("#case-detail")).to_contain_text("manual")

    # Commit on the server, then deliberately lose the response in transport.
    lost = {"done": False}

    def lose_response(route):
        response = route.fetch(headers={
            **route.request.headers,
            "origin": args.url,
            "sec-fetch-site": "same-origin",
        })
        assert response.status == 200, response.text()
        lost["done"] = True
        route.fulfill(
            status=503,
            content_type="application/json",
            body=json.dumps(
                {"error": {"code": "TEST_RESPONSE_LOST", "message": "Commit response lost", "owner": "test operator"}}
            ),
        )
        page.unroute("**/api/cases/EX-HOME-900/commands", lose_response)

    page.route("**/api/cases/EX-HOME-900/commands", lose_response)
    page.locator("#command-action").select_option("set_update")
    page.locator("#payload-dueAt").fill("2026-10-10T16:00:00Z")
    source("Synthetic commit followed by lost response to verify exact retry")
    page.get_by_role("button", name="Submit exercise command").click()
    expect(page.locator("#pending-panel")).to_contain_text("Outcome unknown")
    expect(page.locator("#demo-role")).to_be_disabled()
    retained = page.locator("#pending-panel pre").text_content()
    page.get_by_role("button", name="Retry exact retained request").click()
    expect(page.locator("#status")).to_contain_text("Original committed intent replayed")
    expect(page.locator("#pending-panel")).to_be_hidden()
    expect(page.locator("#demo-role")).to_be_enabled()
    assert lost["done"] and "idempotencyKey" in retained, {"lost": lost, "retained": retained}
    expect(page.locator("#case-detail")).to_contain_text("2026-10-10T16:00:00Z")

    with page.expect_download() as download_event:
        page.locator("#export-button").click()
    download = download_event.value
    assert download.failure() is None

    page.locator("#reset-button").click()
    expect(page.locator("#case-list .case-row")).to_have_count(9)
    page.locator("#metric-cards button").first.click()
    expect(page.locator("#drilldown")).to_be_visible()
    page.locator("#clear-drilldown").click()
    expect(page.locator("#drilldown")).to_be_hidden()

    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(args.artifacts / "proper-warm-desktop.png"))
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_load_state("networkidle")
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "Mobile horizontal overflow"
    expect(page.locator("#demo-role")).to_be_visible()
    if args.artifacts:
        page.screenshot(path=str(args.artifacts / "proper-warm-mobile.png"))
    assert not errors, errors
    print(json.dumps({
        "execution": "local-synthetic-browser",
        "checks": ["nine views", "search/reset", "held progression denial", "sourced command",
                   "cited draft", "failure task", "lost-response replay", "export",
                   "metric drilldown", "390px reflow", "no page errors"],
        "pass": True,
        "limitations": "Not user validation or accessibility conformance certification.",
    }))
    context.close()
    browser.close()
