"""Actual loopback challenge journey; public synthetic fixture, no model or cloud."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import APIResponse, Route, expect, sync_playwright
from test_resident_api import ResidentApi

from checks.regulatory_ux_check import AXE_SHA256, scan


def run(axe_path: Path) -> dict[str, Any]:
    raw = axe_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
    axe = raw.decode("utf-8")
    fixture = ResidentApi("test_http_challenge_both_routes_resolution_and_denied_reads")
    fixture.setUp()
    reports: list[dict[str, Any]] = []
    try:
        payload = fixture.challenge_payload()
        before = json.loads(json.dumps(fixture.store.cases["ZF-1"]))
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(
                viewport={"width": 1280, "height": 900}, reduced_motion="reduce"
            )
            context.route(
                "**/*",
                lambda route: (
                    route.continue_()
                    if route.request.url.startswith(fixture.base + "/")
                    else route.abort()
                ),
            )
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            def login(actor: str) -> None:
                context.clear_cookies()
                page.goto(fixture.base + "/app")
                page.locator("#email").fill(f"{actor}@example.test")
                page.locator("#pw").fill("synthetic-only")
                page.locator("button[type=submit]").click()
                page.locator("#nav").wait_for(state="visible")
                page.goto(fixture.base + "/app#/case/ZF-1")
                page.get_by_role(
                    "heading",
                    name="Requirements and doubt route"
                    if actor == "kim"
                    else "Decision for each measure",
                    exact=True,
                ).wait_for()

            login("sam")
            page.get_by_text("Record supplied challenge", exact=True).first.focus()
            page.keyboard.press("Enter")
            page.locator("#challenge-open button[type=submit]").click()
            expect(page.locator("#challenge-open-proposal_id")).to_be_focused()
            expect(page.locator("#challenge-open-feedback")).to_contain_text(
                "Enter suggestion reference"
            )
            scan(page, axe, reports, "challenge-validation", "#affected-challenges")
            for channel in ("Digital", "Phone"):
                if channel == "Phone":
                    page.get_by_text("Record supplied challenge", exact=True).first.click()
                page.locator("#challenge-open-proposal_id").fill(payload["proposal_id"])
                for name in ("target_kind", "channel", "owner"):
                    page.locator("#challenge-open-" + name).select_option(
                        channel if name == "channel" else payload[name]
                    )
                for name in (
                    "source",
                    "request",
                    "explanation",
                    "non_digital_route",
                    "next_update",
                ):
                    page.locator("#challenge-open-" + name).fill(payload[name])
                if channel == "Digital":
                    page.once("dialog", lambda dialog: dialog.dismiss())
                    page.get_by_role("link", name="Back to the list", exact=True).click()
                    expect(page.locator("#challenge-open-request")).to_have_value(
                        payload["request"]
                    )
                    # A genuine unrelated write rebuilds the case; the old draft/binding must survive.
                    page.locator("#outcome").fill("SYN unrelated call")
                    page.locator("#note").fill("SYN manual work continues")
                    page.get_by_role("button", name="Save", exact=True).click()
                    page.get_by_text("SYN unrelated call", exact=False).first.wait_for()
                    expect(page.locator("#challenge-open-request")).to_have_value(
                        payload["request"]
                    )
                    expect(page.locator("#challenge-open-proposal_id")).to_have_value(
                        payload["proposal_id"]
                    )
                page.locator("#challenge-open-next_update").press("Enter")
                page.get_by_text(
                    f"CH-{1 if channel == 'Digital' else 2}: Open.", exact=False
                ).wait_for()
            assert [r["channel"] for r in fixture.store.cases["ZF-1"]["affected_challenges"]] == [
                "Digital",
                "Phone",
            ]
            page.get_by_text("Record supplied resolution for CH-1", exact=True).first.click()
            page.locator("#challenge-resolve-CH-1-resolution").select_option("Correction recorded")
            page.locator("#challenge-resolve-CH-1-resolution_ref").fill(
                "SYN browser human correction"
            )
            page.locator("#challenge-resolve-CH-1-explanation").fill(
                "SYN corrected information needs fresh review"
            )
            page.locator("#challenge-resolve-CH-1-next_update").fill("2099-01-02")
            page.once("dialog", lambda dialog: dialog.dismiss())
            page.locator("#challenge-resolve-CH-1-next_update").press("Enter")
            assert fixture.store.cases["ZF-1"]["affected_challenges"][0]["status"] == "Open"
            page.once("dialog", lambda dialog: dialog.accept())
            page.locator("#challenge-resolve-CH-1-next_update").press("Enter")
            page.get_by_text("CH-1: Resolved.", exact=False).wait_for()
            page.get_by_text(
                f"Suggestion {payload['proposal_id']}: Needs a fresh review", exact=True
            ).click()
            page.get_by_text(
                "Historical decision only; needs a fresh review.", exact=False
            ).wait_for()
            page.get_by_text("Record supplied challenge", exact=True).first.click()
            page.get_by_text("Record supplied resolution for CH-2", exact=True).first.click()
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                scan(page, axe, reports, f"challenge-resolved-{width}", "#affected-challenges")
            assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
            for actor in ("rex", "bea", "kim"):
                login(actor)
                expect(page.locator("#affected-challenges")).to_have_count(0)
                assert "SYN-CHALLENGE-REQUEST-CANARY" not in page.locator("body").inner_text()
            assert not errors, errors
            version = browser.version
            browser.close()
        after = fixture.store.cases["ZF-1"]
        for key in ("decision", "measure_decisions", "hazards", "closed", "service_requests"):
            assert after.get(key) == before.get(key), key
        assert fixture.store.latest_priority(fixture.store.staff["sam@example.test"])[
            "review_stale"
        ]
        return dict(
            outcome="passed",
            browser=version,
            channels=["Digital", "Phone"],
            axe_version="4.10.3",
            axe_sha256=AXE_SHA256,
            scans=reports,
            screen_reader="Not run",
            human_acceptance="Not run",
            scope="Constructed retained priority challenge only; no whole-system conformance",
        )
    finally:
        fixture.doCleanups()


def run_history(axe_path: Path) -> dict[str, Any]:
    """Exercise retained actions outside both initial 50-record windows."""
    raw = axe_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
    fixture = ResidentApi("test_http_challenge_both_routes_resolution_and_denied_reads")
    fixture.setUp()
    reports: list[dict[str, Any]] = []
    try:
        payload = fixture.challenge_payload()
        payload["target_kind"] = "proposal"
        original = json.loads(json.dumps(fixture.store.data["recommendations"][0]))
        for _ in range(51):
            fixture.store.ai_priority(fixture.store.staff["sam@example.test"], mode="workflow-only")
        # All records are constructed through the real authorized HTTP operation.
        for index in range(52):
            code, detail = fixture.call(
                "/api/cases/ZF-1/resident",
                "sam",
                dict(payload, target_kind="proposal", request=f"SYN history request {index + 1}"),
            )
            assert code == 200, detail
        code, detail = fixture.action(
            "challenge_resolve",
            id="CH-2",
            expected_version=1,
            resolution="Explanation recorded",
            resolution_ref="SYN retained explanation",
            explanation="SYN older resolved explanation",
            next_update="2099-01-02",
        )
        assert code == 200, detail
        before = json.loads(json.dumps(fixture.store.cases["ZF-1"]))
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(
                viewport={"width": 1280, "height": 900}, reduced_motion="reduce"
            )
            page.route(
                "**/*",
                lambda route: (
                    route.continue_()
                    if route.request.url.startswith(fixture.base + "/")
                    else route.abort()
                ),
            )
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(fixture.base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-only")
            page.locator("button[type=submit]").click()
            page.locator("#nav").wait_for(state="visible")
            page.goto(fixture.base + "/app#/case/ZF-1")
            page.locator("#affected-challenges").wait_for()
            expect(page.get_by_role("button", name="Older suggestions", exact=True)).to_be_visible()
            expect(page.get_by_text("CH-1: Open.", exact=False)).to_have_count(0)
            page.get_by_role("button", name="Older suggestions", exact=True).focus()
            page.keyboard.press("Enter")
            page.get_by_text(
                f"Suggestion {payload['proposal_id']}: No recorded correction", exact=True
            ).click()
            expect(page.get_by_text("Human draft decision: Accepted.", exact=False)).to_be_visible()
            page.get_by_text("Record supplied challenge", exact=True).first.click()
            page.locator("#challenge-open-proposal_id").fill(payload["proposal_id"])
            for name in ("target_kind", "channel", "owner"):
                page.locator("#challenge-open-" + name).select_option(payload[name])
            for name in ("source", "request", "explanation", "non_digital_route", "next_update"):
                page.locator("#challenge-open-" + name).fill(payload[name])
            page.locator("#challenge-open-proposal_id").fill("SYN-not-recorded")
            page.locator("#challenge-open-next_update").press("Enter")
            expect(page.locator("#challenge-open-feedback")).to_contain_text(
                "Enter an exact recorded suggestion reference"
            )
            assert len(fixture.store.cases["ZF-1"]["affected_challenges"]) == 52
            page.locator("#challenge-open-proposal_id").fill(payload["proposal_id"])
            # Target paging must not erase or rebind an in-progress opening.
            page.get_by_role("button", name="Newer suggestions", exact=True).click()
            expect(page.locator("#challenge-open-proposal_id")).to_have_value(
                payload["proposal_id"]
            )
            page.get_by_role("button", name="Older suggestions", exact=True).click()
            page.locator("#challenge-open-next_update").press("Enter")
            expect(page.get_by_text("CH-53: Open.", exact=False)).to_be_visible()
            page.get_by_role("button", name="Older challenges", exact=True).focus()
            page.keyboard.press("Enter")
            expect(page.get_by_text("SYN older resolved explanation", exact=False)).to_be_visible()
            page.get_by_text("Record supplied resolution for CH-1", exact=True).first.click()
            page.locator("#challenge-resolve-CH-1-resolution").select_option("Correction recorded")
            page.locator("#challenge-resolve-CH-1-resolution_ref").fill("SYN history correction")
            page.locator("#challenge-resolve-CH-1-explanation").fill("SYN history fresh review")
            page.locator("#challenge-resolve-CH-1-next_update").fill("2099-01-03")
            page.once("dialog", lambda dialog: dialog.dismiss())
            page.get_by_role("button", name="Newer challenges", exact=True).click()
            expect(page.locator("#challenge-resolve-CH-1-resolution_ref")).to_have_value(
                "SYN history correction"
            )
            page.once("dialog", lambda dialog: dialog.accept())
            page.locator("#challenge-resolve-CH-1-next_update").press("Enter")
            expect(page.get_by_text("CH-1: Resolved.", exact=False)).to_be_visible()
            expect(page.get_by_text("SYN history fresh review", exact=False)).to_be_visible()
            page.get_by_text(
                f"Suggestion {payload['proposal_id']}: Needs a fresh review", exact=True
            ).click()
            expect(
                page.get_by_text("Historical decision only; needs a fresh review.", exact=False)
            ).to_be_visible()
            # URL-bound page survives a full reload; both lists remain bounded.
            page.reload()
            expect(page.get_by_text("CH-1: Resolved.", exact=False)).to_be_visible()
            assert page.locator("#challenge-target-history > div > details").count() <= 50
            assert page.locator("#challenge-record-history > div > div").count() <= 50
            page.get_by_text("Record supplied resolution for CH-3", exact=True).first.click()
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                scan(
                    page,
                    raw.decode("utf-8"),
                    reports,
                    f"challenge-history-{width}",
                    "#affected-challenges",
                )
            assert not errors, errors
            version = browser.version
            browser.close()
        after = fixture.store.cases["ZF-1"]
        for key in ("decision", "measure_decisions", "hazards", "closed", "service_requests"):
            assert after.get(key) == before.get(key), key
        assert after["affected_challenges"][0]["resolution"]["outcome"] == "Correction recorded"
        assert (
            after["affected_challenges"][-1]["target"] == after["affected_challenges"][0]["target"]
        )
        assert fixture.store.data["recommendations"][0] == original
        targets = fixture.call("/api/cases/ZF-1", "sam")[1]["challenge_targets"]
        assert {row["proposal_id"] for row in targets if row["stale"]} == {payload["proposal_id"]}
        for actor in ("rex", "bea", "kim"):
            code, denied = fixture.call("/api/cases/ZF-1", actor)
            assert code == 200
            assert "challenge_targets" not in denied and "affected_challenges" not in denied
        return dict(
            outcome="passed",
            browser=version,
            targets=len(targets),
            challenges=len(after["affected_challenges"]),
            historical_target=payload["proposal_id"],
            resolved="CH-1",
            older_resolution="CH-2",
            exact_stale_ids=[payload["proposal_id"]],
            scans=reports,
            scope="Actual constructed historical UI/HTTP/SQLite correction; no whole issue acceptance",
        )
    finally:
        fixture.doCleanups()


def run_navigation() -> dict[str, Any]:
    """Delay a committed POST acknowledgement across confirmed route navigation."""
    fixture = ResidentApi("test_http_challenge_both_routes_resolution_and_denied_reads")
    fixture.setUp()
    try:
        payload = fixture.challenge_payload()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(reduced_motion="reduce")
            page.route(
                "**/*",
                lambda route: route.continue_()
                if route.request.url.startswith(fixture.base + "/") else route.abort(),
            )
            page.goto(fixture.base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-only")
            page.locator("button[type=submit]").click()
            page.locator("#nav").wait_for(state="visible")
            pending: list[tuple[Route, APIResponse]] = []
            writes: list[str] = []
            old_case_reads: list[str] = []
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            def hold_acknowledgement(route: Route) -> None:
                writes.append(route.request.url)
                response = route.fetch()
                assert response.ok
                pending.append((route, response))
                page.evaluate("(count) => { window.challengeCommitted = count; }", len(pending))

            page.route("**/api/cases/ZF-1/resident", hold_acknowledgement)
            for index, destination in enumerate(("#/case/ZF-5", "#/"), start=1):
                page.goto(fixture.base + "/app#/case/ZF-1")
                page.locator("#affected-challenges").wait_for()
                page.get_by_text("Record supplied challenge", exact=True).first.click()
                page.locator("#challenge-open-proposal_id").fill(payload["proposal_id"])
                for name in ("target_kind", "channel", "owner"):
                    page.locator("#challenge-open-" + name).select_option(payload[name])
                for name in ("source", "request", "explanation", "non_digital_route", "next_update"):
                    page.locator("#challenge-open-" + name).fill(payload[name])
                with page.expect_request("**/api/cases/ZF-1/resident"):
                    page.locator("#challenge-open-next_update").press("Enter")
                expect(page.locator("#challenge-open button[type=submit]")).to_be_disabled()
                page.wait_for_function("(count) => window.challengeCommitted === count", arg=index)
                assert len(pending) == index
                code, detail = fixture.call("/api/cases/ZF-1", "sam")
                assert code == 200 and len(detail["affected_challenges"]) == index
                # A normal hash change exercises the real unsaved-draft confirmation.
                page.once("dialog", lambda dialog: dialog.accept())
                page.evaluate("(destination) => { location.hash = destination; }", destination)
                page.wait_for_url("**/app" + destination)
                if destination.endswith("ZF-5"):
                    expect(page.get_by_text("Reference ZF-5", exact=True)).to_be_visible()
                else:
                    expect(page.get_by_role("link", name="See all cases", exact=True)).to_be_visible()
                destination_heading = page.locator("main h1").inner_text()
                old_case_reads.clear()

                def record_read(request: Any) -> None:
                    if request.method == "GET" and request.url == fixture.base + "/api/cases/ZF-1":
                        old_case_reads.append(request.url)

                page.on("request", record_read)
                route, response = pending[-1]
                route.fulfill(response=response)
                page.wait_for_load_state("networkidle")
                assert page.url.endswith("/app" + destination), page.url
                expect(page.locator("main h1")).to_have_text(destination_heading)
                if destination.endswith("ZF-5"):
                    expect(page.get_by_text("Reference ZF-5", exact=True)).to_be_visible()
                assert not old_case_reads, old_case_reads
                assert len(writes) == index, "A committed write must not be cancelled or retried"
                page.remove_listener("request", record_read)
            assert not errors, errors
            version = browser.version
            browser.close()
        code, detail = fixture.call("/api/cases/ZF-1", "sam")
        assert code == 200 and len(detail["affected_challenges"]) == 2
        return dict(outcome="passed", browser=version, committed_writes=2,
                    destinations=["case ZF-5", "case list"], stale_refresh_reads=0,
                    cancelled_or_retried_writes=0, page_errors=errors)
    finally:
        fixture.doCleanups()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--navigation", action="store_true")
    args = parser.parse_args()
    result = (run_navigation() if args.navigation else
              run_history(args.axe) if args.history else run(args.axe))
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
