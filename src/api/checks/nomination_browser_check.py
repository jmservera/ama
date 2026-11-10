"""Actual loopback check of the read-only nomination section; public synthetic fixture only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from checks.regulatory_ux_check import AXE_SHA256, scan
from playwright.sync_api import expect, sync_playwright
from test_resident_api import ResidentApi

TAB = "/app#/case/ZF-1?tab=resident"


def run(axe_path: Path) -> dict[str, Any]:
    raw = axe_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
    axe = raw.decode("utf-8")
    fixture = ResidentApi("test_http_nomination_manual_routes_correction_and_no_automatic_decision")
    fixture.setUp()
    reports: list[dict[str, Any]] = []
    try:
        code, detail = fixture.call(
            "/api/cases/ZF-1/resident", "sam", fixture.intake_payload(channel="Phone")
        )
        assert code == 200, detail
        record_id = detail["nomination_records"][0]["id"]
        review = dict(
            case_id="ZF-1",
            id=record_id,
            expected_version=1,
            outcome="Accepted for human eligibility review",
            rationale="SYN plain reasons",
            evidence_ref="SYN evidence considered",
            next_update="2099-01-03",
        )
        code, detail = fixture.action("nomination_review", "rae", **review)
        assert code == 200, detail
        code, detail = fixture.action(
            "nomination_correct",
            case_id="ZF-1",
            id=record_id,
            expected_version=1,
            reported_subject_ref="SYN-CORRECTED",
            account="SYN competing corrected account",
            source="SYN correction evidence",
            channel="Letter",
            next_update="2099-01-02",
            challenge_id=None,
        )
        assert code == 200, detail
        before = json.loads(json.dumps(fixture.store.cases["ZF-1"]))
        non_get: list[str] = []
        api_paths: set[str] = set()
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

            def watch(request: Any) -> None:
                path = request.url.removeprefix(fixture.base)
                if path.startswith("/api/"):
                    api_paths.add(f"{request.method} {path.split('?')[0]}")
                if request.method != "GET":
                    non_get.append(f"{request.method} {path}")

            def login(actor: str, hash_path: str = TAB) -> None:
                context.clear_cookies()
                page.goto(fixture.base + "/app")
                page.locator("#email").fill(f"{actor}@example.test")
                page.locator("#pw").fill("synthetic-only")
                page.locator("button[type=submit]").click()
                page.locator("#nav").wait_for(state="visible")
                page.goto(fixture.base + hash_path)

            login("sam")
            page.on("request", watch)
            expect(page.locator("#nominations-title")).to_have_text(
                "Nominations and self-referrals"
            )
            section = page.locator("#nominations")
            expect(section).to_contain_text("Original supplied account")
            expect(section).to_contain_text("SYN-ACCOUNT-PRIVATE")
            expect(section).to_contain_text(
                "Corrected account, version 2 (competing evidence; the original is kept)"
            )
            expect(section).to_contain_text("SYN competing corrected account")
            expect(section).to_contain_text("Delivery unverified")
            expect(section).to_contain_text("Stale: recorded for version 1")
            expect(section).to_contain_text("Correction awaiting human re-review.")
            expect(section).to_contain_text("Accepted for human eligibility review")
            expect(section).to_contain_text("not an approval or an eligibility decision")
            for label in ("Identity status", "Support needs", "Risk flags"):
                value = (
                    section.locator("dt", has_text=label)
                    .first.locator("xpath=following-sibling::dd")
                    .inner_text()
                )
                assert value == "Unknown", (label, value)
            # The existing generic challenge and manual-channel paths stay in the tab.
            expect(page.locator("#affected-challenges")).to_be_attached()
            expect(page.get_by_role("heading", name="Decision for each measure")).to_be_visible()
            # Keyboard: Tab reaches the record summary; Enter and Space toggle it.
            page.locator("#nominations-title").evaluate("e => { e.tabIndex = -1; e.focus(); }")
            page.keyboard.press("Tab")
            summary = page.locator("#nominations summary").first
            expect(summary).to_be_focused()
            details = page.locator("#nominations details").first
            expect(details).to_have_attribute("open", "")
            page.keyboard.press("Enter")
            assert page.evaluate("document.querySelector('#nominations details').open") is False
            page.keyboard.press("Space")
            assert page.evaluate("document.querySelector('#nominations details').open") is True
            assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
            for width in (320, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                scan(page, axe, reports, f"nomination-stale-{width}", "#nominations")
            # Authorised case with no records shows the empty state.
            page.goto(fixture.base + "/app#/case/ZF-4?tab=resident")
            empty = page.locator("#nominations")
            expect(empty).to_contain_text(
                "No nomination or self-referral is recorded for this home."
            )
            assert not non_get, non_get
            page.remove_listener("request", watch)
            # A second independent review for the corrected version is constructed outside the page.
            code, detail = fixture.action(
                "nomination_review", "rae", **dict(review, expected_version=2)
            )
            assert code == 200, detail
            page.goto(fixture.base + TAB)
            page.reload()
            page.locator("#nominations").wait_for()
            expect(page.locator("#nominations")).to_contain_text("Current for version 2")
            expect(page.locator("#nominations")).to_contain_text("Stale: recorded for version 1")
            scan(page, axe, reports, "nomination-current", "#nominations")
            for actor in ("rex", "bea", "kim"):
                login(actor)
                page.locator("#nav").wait_for(state="visible")
                expect(page.locator("#nominations")).to_have_count(0)
                assert "SYN-ACCOUNT-PRIVATE" not in page.locator("body").inner_text()
            assert not errors, errors
            version = browser.version
            browser.close()
        after = fixture.store.cases["ZF-1"]
        assert after.get("nomination_records")[0]["version"] == 2
        for key in ("decision", "measure_decisions", "hazards", "closed", "service_requests"):
            assert after.get(key) == before.get(key), key
        for report in reports:
            assert not report.get("violations"), report
        return dict(
            outcome="passed",
            browser=version,
            axe_version="4.10.3",
            axe_sha256=AXE_SHA256,
            non_get_requests_while_viewing=non_get,
            api_requests_while_viewing=sorted(api_paths),
            scans=reports,
            screen_reader="Not run",
            human_acceptance="Not run",
            scope="Constructed synthetic nomination view only; no whole-system conformance",
        )
    finally:
        fixture.doCleanups()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.axe)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
