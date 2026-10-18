"""Local fictional capacity screen exercise; no model or external request."""

from typing import Any
import os

from playwright.sync_api import expect, sync_playwright
from test_procurement_api import ProcurementApi


def main() -> None:
    fixture = ProcurementApi("test_capacity_http_exact_threshold_and_source_inputs")
    fixture.setUp()
    try:
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
                page.locator("#pw").fill("synthetic-password")
                page.locator("button[type=submit]").click()
                page.locator("#nav").wait_for(state="visible")

            login("pam")
            page.goto(fixture.base + "/app#/capacity")
            page.get_by_role("heading", name="Capacity and work orders", exact=True).wait_for()
            package_fields = (
                ("Package name", "SYN browser package"),
                ("Starts", "2026-01-01"),
                ("Ends", "2099-12-31"),
                ("What it covers", "SYN Loft"),
                ("Contract or call-off reference", "SYN-BROWSER"),
            )
            for label, value in package_fields:
                page.get_by_label(label, exact=True).fill(value)
            version = page.get_by_label("Contract or call-off version", exact=True)
            before = len(fixture.store.data["procurement"]["packages"])
            for invalid in ("", " \t "):
                version.fill(invalid)
                page.get_by_role("button", name="Create package", exact=True).click()
                page.locator("#capacity-version-error").get_by_text(
                    "Enter the contract or call-off version", exact=False
                ).wait_for()
                assert version.evaluate("(el) => el === document.activeElement")
                assert version.get_attribute("aria-invalid") == "true"
                for label, value in package_fields:
                    assert page.get_by_label(label, exact=True).input_value() == value
                assert len(fixture.store.data["procurement"]["packages"]) == before
            page.get_by_role("button", name="Save capacity", exact=True).click()
            page.get_by_role("status").get_by_text("whole number", exact=False).wait_for()
            assert (
                page.get_by_role("status")
                .filter(has_text="whole number")
                .evaluate("(el) => el === document.activeElement")
            )
            assert fixture.store.list_packages(fixture.manager)[0]["capacity"] == []

            def record(contractor: str, details: dict[str, Any]) -> None:
                for label, value in (
                    ("Contractor", contractor),
                    ("Offered (home orders)", "9"),
                    ("Committed with evidence (home orders)", "1"),
                    ("Evidence for the commitment", "SYN browser accepted commitment"),
                    ("Case holding the commitment document", details["source_case_id"]),
                    ("Commitment document ID", details["document_id"]),
                    ("Commitment document version", details["source_version"]),
                    ("Commitment source date", details["source_date"]),
                    ("Manager reviewed on", details["reviewed_on"]),
                    ("Capacity delivery starts", details["valid_from"]),
                    ("Capacity delivery ends", details["valid_to"]),
                    (
                        "Covered case references, separated by semicolons",
                        ";".join(details["case_ids"]),
                    ),
                ):
                    page.get_by_label(label, exact=True).fill(value)
                page.get_by_role("button", name="Save capacity", exact=True).focus()
                page.keyboard.press("Enter")
                page.get_by_role("cell", name=contractor, exact=True).wait_for()

            def issue(cid: str, wid: str) -> None:
                page.get_by_label("Case reference to issue a work order for", exact=True).fill(cid)
                page.get_by_label(
                    "Affected measures and scope revisions: Measure|revision; Measure|revision",
                    exact=True,
                ).fill("Loft insulation|1")
                page.get_by_role("button", name="Issue work order", exact=True).click()
                page.get_by_text(f"{wid}, version 1", exact=True).wait_for()

            record("Test Ltd", fixture.details)
            issue("ZF-1", "WO-0001")
            page.get_by_role("heading", name="Appointment: Unknown", exact=True).wait_for()
            page.get_by_text("Record separate confirmation for WO-0001", exact=True).click()
            page.get_by_label("Confirming person (WO-0001)", exact=True).fill("Pat Test")
            page.get_by_label("Confirmation source (WO-0001)", exact=True).fill("SYN phone")
            page.get_by_label(
                "Confirmation channel, including phone or in person (WO-0001)", exact=True
            ).fill("Phone")
            page.get_by_role("button", name="Record separate confirmation", exact=True).click()
            page.get_by_role("status").get_by_text(
                "current specific appointment offer", exact=False
            ).wait_for()
            page.once("dialog", lambda dialog: dialog.accept())
            page.get_by_role("button", name="Record separate confirmation", exact=True).locator("..").get_by_role("button", name="Discard this draft").click()
            fixture.store.resident_action(
                fixture.manager,
                "ZF-1",
                dict(
                    action="update_record",
                    expected_version=0,
                    owner=fixture.manager["email"],
                    purpose="SYN appointment update",
                    due_at="2099-01-01T10:00:00+00:00",
                    basis="SYN manual arrangement",
                    status="Outstanding",
                ),
            )
            page.get_by_text("Record appointment offer for WO-0001", exact=True).click()
            for label, value in (
                ("Offer date", "2099-01-01"),
                ("Visit period", "Morning"),
                ("Options offered, separated by semicolons", "Morning;Different day;Pause"),
                ("Household constraints or Unknown", "Morning only"),
                ("Necessary provider instructions only, no diagnoses", "Knock and wait"),
            ):
                page.get_by_label(f"{label} (WO-0001)", exact=True).fill(value)
            page.get_by_role("button", name="Record appointment offer", exact=True).focus()
            page.keyboard.press("Enter")
            page.get_by_role("heading", name="Appointment: Offer", exact=True).wait_for()
            if os.environ.get("ZF_APPOINTMENT_REPRO") != "draft":
                page.get_by_text("Selected visit: 1 Jan 2099. Period: Morning.", exact=True).first.wait_for(timeout=3000)
                page.get_by_text("Necessary instructions: Knock and wait", exact=True).first.wait_for()
                assert fixture.store._work_order("WO-0001")["appointments"] == []
            page.get_by_text("Record provisional threshold for WO-0001", exact=True).click()
            draft = page.get_by_label("Threshold configuration evidence (WO-0001)", exact=True)
            draft.fill("SYN pending manual draft")
            draft.focus()
            page.keyboard.press("End")
            page.keyboard.type(" retained")
            page.once("dialog", lambda dialog: dialog.dismiss())
            link = page.get_by_role("link", name="Record or review the named resident-update commitment and safe contact").first
            link.focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(200)
            assert draft.input_value(timeout=3000) == "SYN pending manual draft retained"
            assert page.url.endswith("#/capacity")
            for kind, person in (
                ("resident", "Pat Test"),
                ("staff", fixture.manager["name"]),
                ("capacity", "SYN supplier contact"),
            ):
                page.get_by_text("Record separate confirmation for WO-0001", exact=True).click()
                page.get_by_label("Confirmation kind (WO-0001)", exact=True).select_option(kind)
                page.get_by_label("Confirming person (WO-0001)", exact=True).fill(person)
                page.get_by_label("Confirmation source (WO-0001)", exact=True).fill(
                    "SYN explicit " + kind
                )
                page.get_by_label(
                    "Confirmation channel, including phone or in person (WO-0001)", exact=True
                ).fill("Phone, manual route")
                page.get_by_role("button", name="Record separate confirmation", exact=True).focus()
                page.keyboard.press("Enter")
                page.get_by_role(
                    "heading",
                    name="Appointment: " + ("Committed" if kind == "capacity" else "Offer"),
                    exact=True,
                ).wait_for()
                assert page.get_by_label("Threshold configuration evidence (WO-0001)", exact=True).input_value() == "SYN pending manual draft retained"
                expect(page.get_by_label("Confirmation source (WO-0001)", exact=True)).to_have_value("")
            page.locator('form[data-appointment-form="WO-0001-configure"]').locator("..").evaluate("(el) => el.open = true")
            saved_form = page.locator(
                'form[data-appointment-form="WO-0001-configure"]'
            ).element_handle()
            assert saved_form is not None
            page.get_by_role("button", name="Record provisional threshold", exact=True).click()
            page.wait_for_function("(form) => !form.isConnected", arg=saved_form)
            saved_form.dispose()
            expect(page.locator('form[data-unsaved="true"]')).to_have_count(0)
            refreshed_form = page.locator('form[data-appointment-form="WO-0001-configure"]')
            expect(refreshed_form).not_to_have_attribute("data-unsaved", "true")
            expect(
                refreshed_form.get_by_label(
                    "Threshold configuration evidence (WO-0001)", exact=True
                )
            ).to_have_value("")
            provider_context = browser.new_context(reduced_motion="reduce")
            provider_context.route(
                "**/*",
                lambda route: route.continue_()
                if route.request.url.startswith(fixture.base + "/") else route.abort(),
            )
            provider_page = provider_context.new_page()
            provider_page.goto(fixture.base + "/app")
            provider_page.locator("#email").fill("kim@example.test")
            provider_page.locator("#pw").fill("synthetic-password")
            provider_page.locator("button[type=submit]").click()
            provider_page.get_by_role("heading", name="Your work orders", exact=True).wait_for()
            provider_page.get_by_text("Appointment: Committed.", exact=True).wait_for()
            provider_page.get_by_text("Selected visit: 1 Jan 2099. Period: Morning.", exact=True).wait_for()
            provider_page.get_by_text("Necessary instructions: Knock and wait", exact=True).wait_for()
            assert fixture.store._work_order("WO-0001")["appointments"] == []
            provider_context.close()
            page.get_by_label("Note or date for WO-0001", exact=True).fill("2099-01-01")
            page.get_by_role(
                "button", name="Record appointment (date for Booked)", exact=True
            ).click()
            page.get_by_text("WO-0001, version 2", exact=True).wait_for()
            record("Other Ltd", fixture.other_details)
            issue("ZF-2", "WO-0002")
            page.get_by_text("Record appointment offer for WO-0001", exact=True).click()
            pending = page.get_by_label("Household constraints or Unknown (WO-0001)", exact=True)
            pending.fill("SYN other order must not erase this draft")
            page.get_by_text("Record provisional threshold for WO-0002", exact=True).click()
            page.get_by_label("Threshold configuration evidence (WO-0002)", exact=True).fill("SYN another order rule")
            page.locator('form[data-appointment-form="WO-0002-configure"]').get_by_role("button", name="Record provisional threshold", exact=True).focus()
            page.keyboard.press("Enter")
            expect(page.get_by_label("Threshold configuration evidence (WO-0002)", exact=True)).to_have_value("")
            expect(pending).to_have_value("SYN other order must not erase this draft")
            assert page.locator('form[data-appointment-form="WO-0001-offer"]').get_attribute("data-unsaved") == "true"
            page.once("dialog", lambda dialog: dialog.dismiss())
            page.locator('form[data-appointment-form="WO-0001-offer"]').get_by_role("button", name="Discard this draft").focus()
            page.keyboard.press("Enter")
            expect(pending).to_have_value("SYN other order must not erase this draft")
            page.once("dialog", lambda dialog: dialog.accept())
            page.locator('form[data-appointment-form="WO-0001-offer"]').get_by_role("button", name="Discard this draft").click()
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                for field in page.locator("input").all():
                    assert field.get_attribute("aria-label") or field.evaluate(
                        "(el) => el.labels && el.labels.length > 0"
                    )
            page.get_by_text(
                "Record human underlying home-case closure for WO-0001", exact=True
            ).click()
            for label, value in (
                ("Human home-case closure decision source", "SYN supplied human decision"),
                ("Human closure source version", "SYN-1"),
                ("Human underlying home-case closure reason", "SYN human closure decision"),
            ):
                page.get_by_label(f"{label} (WO-0001)", exact=True).fill(value)
            closure_button = page.get_by_role(
                "button", name="Record human underlying home-case closure", exact=True
            ).first
            closure_button.focus()
            page.keyboard.press("Enter")
            assert not fixture.store.detail("ZF-1")["closed"]
            confirm = page.get_by_label(
                "I am recording the supplied human underlying home-case closure, not investigation task disposition (WO-0001)",
                exact=True,
            )
            confirm.focus()
            page.keyboard.press("Space")
            page.once("dialog", lambda dialog: dialog.dismiss())
            closure_button.focus()
            page.keyboard.press("Enter")
            assert not fixture.store.detail("ZF-1")["closed"]
            update_before = fixture.store.detail("ZF-1")["resident_update"]
            page.once("dialog", lambda dialog: dialog.accept())
            closure_button.focus()
            page.keyboard.press("Enter")
            page.get_by_text(
                "Underlying home case ZF-1: Closed. Recorded human closures: 1. History is retained.",
                exact=True,
            ).wait_for()
            assert fixture.store.detail("ZF-1")["closed"]
            assert fixture.store.detail("ZF-1")["resident_update"] == update_before
            assert len(fixture.store.cases["ZF-1"]["home_case_closures"]) == 1
            for actor, own, foreign in (
                ("kim", "WO-0001", "WO-0002"),
                ("kai", "WO-0002", "WO-0001"),
            ):
                login(actor)
                page.get_by_role("heading", name="Your work orders", exact=True).wait_for()
                assert own in page.locator("main").inner_text()
                assert foreign not in page.locator("main").inner_text()
                assert fixture.call("/api/packages", actor=actor)[0] == 403
                assert fixture.call("/api/workorders/WO-0001/withdraw", {}, actor)[0] == 403
            login("pam")
            page.goto(fixture.base + "/app#/capacity")
            page.get_by_role("heading", name="Capacity and work orders", exact=True).wait_for()
            for label, value in package_fields:
                page.get_by_label(label, exact=True).fill(value)
            page.get_by_label("Contract or call-off version", exact=True).fill(" SYN-1 ")
            page.get_by_role("button", name="Create package", exact=True).focus()
            page.keyboard.press("Enter")
            page.get_by_role("heading", name="SYN browser package (PKG-002)", exact=True).wait_for()
            assert fixture.store._package("PKG-002")["contract_version"] == "SYN-1"
            assert fixture.call("/api/workorders/WO-0001/withdraw", {"reason": "SYN withdrawn"})[0] == 200
            login("kim")
            page.get_by_text("Appointment: Ended. Work order withdrawn; historical agreement only.", exact=True).wait_for()
            page.get_by_text("Historical visit (ended): 1 Jan 2099. Period: Morning.", exact=True).wait_for()
            assert not errors, errors
            browser.close()
        print(
            "PASS: required contract version, inline refusal/field focus/input preservation, "
            "valid keyboard package creation, original-source capacity inputs, keyboard save, "
            "issue/book at quota with new version, both contractor views/write denials, "
            "Unknown/Offer/Committed, missing-offer refusal, separate manual keyboard confirmations, "
            "human underlying-case closure requires explicit checkbox and cancellable confirmation, preserves update, "
            "selected localized slot before confirmation and provider Committed/Ended without legacy visits, "
            "keyboard navigation/discard cancellation preserves drafts, unrelated-order save retains only pending drafts, "
            "320/390/1280px reflow, reduced motion, no page errors or external requests."
        )
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    main()
