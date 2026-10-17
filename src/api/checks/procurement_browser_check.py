"""Local fictional capacity screen exercise; no model or external request."""

from typing import Any

from playwright.sync_api import sync_playwright
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
            page.get_by_label("Note or date for WO-0001", exact=True).fill("2099-01-01")
            page.get_by_role(
                "button", name="Record appointment (date for Booked)", exact=True
            ).click()
            page.get_by_text("WO-0001, version 2", exact=True).wait_for()
            record("Other Ltd", fixture.other_details)
            issue("ZF-2", "WO-0002")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                for field in page.locator("input").all():
                    assert field.get_attribute("aria-label") or field.evaluate(
                        "(el) => el.labels && el.labels.length > 0"
                    )
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
            assert not errors, errors
            browser.close()
        print(
            "PASS: original-source capacity inputs, inline refusal/focus, keyboard save, "
            "issue/book at quota with new version, both contractor views/write denials, "
            "320/390/1280px reflow, reduced motion, no page errors or external requests."
        )
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    main()
