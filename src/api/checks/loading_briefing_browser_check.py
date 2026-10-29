"""Synthetic loading, real action, HAX briefing and axe regressions for issue 531."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright

from checks.design_system_browser_check import main
from checks.employee_briefing_browser_check import briefing_data
from checks.regulatory_ux_check import AXE_SHA256


def sign_in(page: Page, base: str) -> None:
    page.get_by_label("Work email", exact=True).fill("sam@example.test")
    page.get_by_label("Password", exact=True).fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
    expect(page.locator(".briefing [data-record-id]")).to_be_visible()


def shell_check(browser: Browser, base: str) -> None:
    context = browser.new_context()
    try:
        page = context.new_page()
        page.clock.install()
        held: list[Route] = []
        page.route("**/app.js", lambda route: held.append(route))
        with page.expect_request("**/app.js"):
            page.goto(base + "/app", wait_until="commit")
        expect(page.locator("#startup-status")).to_contain_text("up to a minute")
        expect(page.locator("#app")).to_be_empty()
        page.clock.fast_forward(4000)
        expect(page.locator("#startup-status")).to_contain_text("Still starting")
        expect(page.locator("#startup-retry")).to_be_visible()
        page.clock.fast_forward(11000)
        expect(page.locator("#startup-status")).to_contain_text("longer than expected")
        expect(page.locator("#startup-status")).to_have_attribute("aria-live", "polite")
        held[0].continue_()
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        expect(page.locator("#startup")).to_be_hidden()
        page.unroute("**/app.js")
        page.route("**/api/me", lambda route: route.fulfill(
            status=503, json={"error": "Synthetic service is unavailable"}))
        page.reload()
        expect(page.get_by_role("heading", name="Workspace unavailable")).to_be_visible()
        expect(page.get_by_role("alert")).to_contain_text("Synthetic service")
        page.unroute("**/api/me")
        page.get_by_role("button", name="Try again", exact=True).click()
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        page.route("**/app.js", lambda route: route.abort())
        page.reload()
        page.clock.fast_forward(16000)
        expect(page.locator("#startup-retry")).to_be_visible()
        page.unroute("**/app.js")
        page.locator("#startup-retry").click()
        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
        print("PASS static shell, held/failed script, slow/deadline and service retry")
    finally:
        context.close()


def run_browser(base: str, axe: str, output: Path) -> None:
    reports: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            shell_check(browser, base)
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            context.route("**/*", lambda route: route.continue_()
                          if route.request.url.startswith(base + "/") else route.abort())
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "/app")
            sign_in(page, base)
            briefing = page.locator(".briefing")
            expect(briefing).to_contain_text("Summary by rules")
            expect(briefing.locator("time")).to_have_count(1)
            expect(briefing.get_by_role("textbox")).to_have_count(0)
            # Hidden controls remain in the DOM but only the chosen outcome exposes them.
            assert briefing.locator("textarea:visible").count() == 0
            briefing.get_by_role("button", name="Hide briefing", exact=True).click()
            expect(briefing.locator(".briefing-content")).to_be_hidden()
            briefing.get_by_role("button", name="Show briefing", exact=True).click()
            briefing.get_by_role("button", name="Edit this draft", exact=True).click()
            edit = briefing.get_by_label("Edited draft", exact=True)
            reason = briefing.get_by_label("Reason", exact=True)
            edit.fill("Locally corrected briefing")
            reason.fill("Checked the records")
            briefing.get_by_role("button", name="Cancel review", exact=True).click()
            expect(edit).to_be_hidden()
            briefing.get_by_role("button", name="Edit this draft", exact=True).click()
            expect(edit).to_have_value("Locally corrected briefing")
            expect(reason).to_have_value("Checked the records")
            reads: list[str] = []
            page.on("request", lambda request: reads.append(request.url)
                    if "/api/briefing" in request.url else None)
            refresh = briefing.get_by_role("button", name="Refresh briefing", exact=True)
            mode = briefing.get_by_label(
                "How to prepare briefings and draft requests", exact=True)
            page.once("dialog", lambda dialog: dialog.dismiss())
            refresh.click()
            expect(edit).to_have_value("Locally corrected briefing")
            assert not reads, "cancelled refresh must not read or replace evidence"
            page.once("dialog", lambda dialog: dialog.dismiss())
            mode.select_option("workflow")
            expect(mode).to_have_value("ai")
            expect(reason).to_have_value("Checked the records")
            assert not reads, "cancelled mode change must not read or replace evidence"
            page.route("**/api/briefing", lambda route: route.fulfill(
                status=503, json={"error": "Synthetic refresh failure"}))
            page.once("dialog", lambda dialog: dialog.accept())
            refresh.click()
            expect(briefing.get_by_role("status").filter(
                has_text="Synthetic refresh failure")).to_be_visible()
            expect(edit).to_have_value("Locally corrected briefing")
            expect(reason).to_have_value("Checked the records")
            page.unroute("**/api/briefing")
            page.once("dialog", lambda dialog: dialog.accept())
            refresh.click()
            expect(edit).to_be_hidden()
            briefing.get_by_role("button", name="Edit this draft", exact=True).click()
            expect(edit).not_to_have_value("Locally corrected briefing")
            expect(reason).to_have_value("")
            edit.fill("Locally corrected briefing")
            reason.fill("Checked the records")
            held: list[Route] = []
            page.route("**/api/ai/review/*/edit", lambda route: held.append(route))
            submit = briefing.get_by_role("button", name="Save edited draft review", exact=True)
            with page.expect_request("**/api/ai/review/*/edit"):
                submit.click()
            expect(submit).to_be_disabled()
            expect(briefing.locator(".async-feedback").first).to_be_visible()
            expect(briefing.locator(".async-spinner").first).to_be_visible()
            before_reads = len(reads)
            refresh.click()
            mode.select_option("workflow")
            expect(mode).to_have_value("ai")
            expect(briefing).to_contain_text("Finish the pending review first")
            assert len(reads) == before_reads
            submit.evaluate("el => el.click()")
            assert len(held) == 1, "refresh cannot remount a second review dispatcher"
            assert held[0].request.post_data_json == {
                "reason": "Checked the records", "text": "Locally corrected briefing"}
            held[0].fulfill(status=503, json={"error": "Synthetic review failed"})
            expect(briefing.get_by_role("status").filter(
                has_text="Synthetic review failed")).to_be_visible()
            expect(submit).to_be_enabled()
            page.unroute("**/api/ai/review/*/edit")
            briefing.get_by_role("button", name="Cancel review", exact=True).click()
            briefing.get_by_role("button", name="Do not use this draft", exact=True).click()
            expect(edit).to_be_hidden()
            expect(reason).to_be_visible()
            reason.fill("")
            briefing.get_by_role("button", name="Record rejection", exact=True).click()
            expect(reason).to_have_attribute("aria-invalid", "true")
            print("PASS source/time/type labels, local undo and conditional review/error")

            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.evaluate(axe)
                result = page.evaluate("""async () => await axe.run(
                    {include: [['.briefing']]},
                    {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa',
                    'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
                reports.append(dict(state=f"briefing-{width}", result=result))
                assert not result["violations"], json.dumps(result["violations"], indent=2)
            page.emulate_media(reduced_motion="reduce")
            page.evaluate("""() => {
                const icon = document.createElement('span');
                icon.id = 'motion-check'; icon.className = 'async-spinner';
                document.body.append(icon);
            }""")
            assert page.locator("#motion-check").evaluate(
                "el => getComputedStyle(el).animationName") == "none"
            page.locator("#motion-check").evaluate("el => el.remove()")
            original = page.request.get(base + "/api/briefing").json()
            original.update(
                source="ai", verified=False, label="AI suggestion, not approved",
                reason=None, source_case_ids=["ZF-1"],
                text="Synthetic cited statement.\nSynthetic unsupported statement.",
                citations=["Stage: Contacting resident"],
                unresolved=["ZF-1: Invented fact"],
                statements=[
                    dict(text="Synthetic cited statement.",
                         citations=["Stage: Contacting resident"], unresolved=[]),
                    dict(text="Synthetic unsupported statement.",
                         citations=[], unresolved=["ZF-1: Invented fact"]),
                ],
            )
            held_briefing: list[Route] = []
            page.route("**/api/briefing", lambda route: held_briefing.append(route))
            page.once("dialog", lambda dialog: dialog.accept())
            with page.expect_request("**/api/briefing"):
                refresh.click()
            expect(briefing.locator(".briefing-content")).to_have_attribute("aria-busy", "true")
            assert briefing.get_by_role("status").filter(
                has_text="Reading case summaries").evaluate(
                    "el => !el.closest('[aria-busy=true]')")
            held_briefing[0].fulfill(json=original)
            expect(briefing).to_contain_text("Generated briefing and its sources")
            assert briefing.locator(".field-error").evaluate(
                "el => getComputedStyle(el, ':before').content") == "none"
            expect(briefing.get_by_role("button", name="Use this draft", exact=True)
                   ).to_be_disabled()
            briefing.get_by_text("Sources used (1)", exact=True).click()
            expect(briefing.get_by_role("link", name="Stage: Contacting resident")
                   ).to_have_attribute("href", "#/case/ZF-1")
            briefing.get_by_text("Sources used (0)", exact=True).click()
            expect(briefing).to_contain_text("ZF-1: Invented fact. Do not rely")
            page.evaluate(axe)
            result = page.evaluate("""async () => await axe.run(
                {include: [['.briefing']]},
                {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa',
                'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
            reports.append(dict(state="ai-unverified-sources", result=result))
            assert not result["violations"], json.dumps(result["violations"], indent=2)
            page.unroute("**/api/briefing")
            page.route("**/api/briefing", lambda route: route.fulfill(json=original))
            for http_status, outcome in ((409, "committed"), (503, "uncertain")):
                page.reload()
                expect(briefing).to_contain_text("Generated briefing and its sources")
                briefing.get_by_role(
                    "button", name="Do not use this draft", exact=True).click()
                briefing.get_by_label("Reason", exact=True).fill("Check this review history")
                held.clear()
                page.route("**/api/ai/review/*/reject", lambda route: held.append(route))
                rejection = briefing.get_by_role("button", name="Record rejection", exact=True)
                with page.expect_request("**/api/ai/review/*/reject"):
                    rejection.click()
                held[0].fulfill(status=http_status, json={
                    "error": "Synthetic confirmation needs checking", "outcome": outcome})
                expect(briefing).to_contain_text("Confirmation needs checking")
                expect(rejection).to_be_disabled()
                before_reads = len(reads)
                refresh.click()
                mode.select_option("workflow")
                expect(mode).to_have_value("ai")
                expect(briefing).to_contain_text("Finish the pending review first")
                assert len(reads) == before_reads
                rejection.evaluate("el => el.click()")
                assert len(held) == 1, "history barrier must not allow a second review"
                page.unroute("**/api/ai/review/*/reject")
            print("PASS guarded refresh/mode, retained failed-refresh edits and outcome barriers")
            page.unroute("**/api/briefing")
            page.screenshot(path=str(output / "briefing.png"), full_page=True)
            # Actual resident draft action, with getText-backed review.
            page.once("dialog", lambda dialog: dialog.accept())
            page.goto(base + "/app#/case/ZF-1?tab=resident")
            draft = page.get_by_role("button", name="Draft with AI", exact=True)
            held.clear()
            page.route("**/api/cases/ZF-1/ai", lambda route: held.append(route))
            with page.expect_request("**/api/cases/ZF-1/ai"):
                draft.click()
            expect(draft).to_be_disabled()
            expect(page.locator("#case-panel-resident .async-spinner").first).to_be_visible()
            draft.evaluate("el => el.click()")
            assert len(held) == 1
            held[0].fulfill(response=held[0].fetch())
            page.unroute("**/api/cases/ZF-1/ai")
            expect(draft).to_be_enabled()
            draft_text = page.get_by_label("Draft", exact=True)
            draft_text.fill("Visible resident replacement")
            resident_review = page.locator("#resident-draft-output .aimeta")
            resident_review.get_by_role("button", name="Edit this draft", exact=True).click()
            resident_review.get_by_label("Reason", exact=True).fill("Checked resident wording")
            with page.expect_request("**/api/ai/review/*/edit") as review_request:
                resident_review.get_by_role(
                    "button", name="Save edited draft review", exact=True).click()
            review_body = review_request.value.post_data_json
            assert isinstance(review_body, dict)
            assert review_body["text"] == draft_text.input_value()
            expect(resident_review).to_have_attribute("data-review-state", "Edited")
            print("PASS real async draft deduplication and visible resident review payload")

            # Mount the shipped appointment control with an explicit synthetic binding.
            page.evaluate("""() => {
                const state = {current_binding: {measure: 'Synthetic', revision: 1},
                    offer: null, status: 'No offer', case_id: 'ZF-1', case_version: 1,
                    missing: [], closure_history: [], counts: {}, case_closed: true};
                const panel = appointmentControls({id: 'SYN-531', case_id: 'ZF-1',
                    appointment_control: state},
                    body => api('/api/workorders/SYN-531/appointment-control', body));
                panel.id = 'synthetic-appointment';
                app.append(panel);
            }""")
            appointment = page.locator("#synthetic-appointment")
            appointment.get_by_text("Record appointment offer for SYN-531", exact=True).click()
            form = appointment.locator('form[data-appointment-form="SYN-531-offer"]')
            for field in form.locator("input[required]").all():
                field.fill("2026-11-01" if field.get_attribute("type") == "date"
                           else "Synthetic appointment detail")
            held.clear()
            page.route("**/api/workorders/SYN-531/appointment-control",
                       lambda route: held.append(route))
            appointment_submit = form.get_by_role(
                "button", name="Record appointment offer", exact=True)
            with page.expect_request("**/api/workorders/SYN-531/appointment-control"):
                appointment_submit.click()
            expect(appointment_submit).to_be_disabled()
            expect(appointment.locator(".async-spinner")).to_be_visible()
            assert appointment.locator(".async-feedback").evaluate(
                "el => !el.closest('[aria-busy=true]')")
            form.evaluate("el => el.requestSubmit()")
            assert len(held) == 1
            held[0].fulfill(status=503, json={"error": "Synthetic appointment failure"})
            expect(appointment.get_by_role("status").filter(
                has_text="Synthetic appointment failure")).to_be_visible()
            expect(appointment_submit).to_be_enabled()
            # Test-only UI is removed; no synthetic mutation reached the store.
            page.locator("#synthetic-appointment").evaluate("el => el.remove()")
            page.unroute("**/api/workorders/SYN-531/appointment-control")
            print("PASS actual appointment submit promise, disabled duplicates and errors")

            held.clear()
            page.route("**/api/map?**", lambda route: held.append(route))
            page.once("dialog", lambda dialog: dialog.accept())
            page.goto(base + "/app#/overview")
            map_panel = page.locator("section").filter(has=page.get_by_role(
                "heading", name="Map of open cases", exact=True))
            expect(page.locator("#leaflet")).to_have_attribute("aria-busy", "true")
            expect(map_panel).to_contain_text("Loading map records")
            expect(map_panel.locator(".async-spinner").first).to_be_visible()
            held[0].fulfill(response=held[0].fetch())
            page.unroute("**/api/map?**")
            expect(page.locator("#leaflet")).not_to_have_attribute("aria-busy", "true")
            print("PASS library-driven map refresh regional feedback")

            # Real standalone law viewer action uses the same helper, without app.js.
            page.route("**/api/law/sources", lambda route: route.fulfill(
                json={"sources": [], "gaps": []}))
            page.goto(base + "/law.html")
            expect(page.get_by_role("heading", name="Sources held", exact=True)).to_be_visible()
            page.unroute("**/api/law/sources")
            held.clear()
            page.route("**/api/law/sources", lambda route: held.append(route))
            law = page.get_by_role("button", name="All sources", exact=True)
            with page.expect_request("**/api/law/sources"):
                law.click()
            expect(law).to_be_disabled()
            expect(page.locator(".async-spinner").first).to_be_visible()
            law.evaluate("el => el.click()")
            assert len(held) == 1
            held[0].fulfill(status=503, json={"error": "Synthetic law read failed"})
            expect(page.locator("#law-status")).to_contain_text("Synthetic law read failed")
            expect(law).to_be_enabled()
            page.unroute("**/api/law/sources")
            page.route("**/api/law/sources", lambda route: route.fulfill(
                json={"sources": [], "gaps": []}))
            law.click()
            expect(page.locator("#law-status")).to_have_text("0 sources and 0 gaps shown.")
            assert not errors, errors
            context.close()
            print(f"PASS law feedback/error/recovery; Chromium {browser.version}; no Azure/live AI")
        finally:
            browser.close()
            (output / "axe-results.json").write_text(json.dumps(reports, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    axe_bytes = args.axe.read_bytes()
    if hashlib.sha256(axe_bytes).hexdigest() != AXE_SHA256:
        raise ValueError("Expected the pinned axe-core 4.10.3 file")
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, axe_bytes.decode(), args.out), briefing_data)
