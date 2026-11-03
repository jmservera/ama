"""Browser evidence for the read-only Finance and grants screens (#225).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.finance_screens_browser_check
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from checks.design_system_browser_check import check, main
from checks.role_screens_fixtures import synthetic_data as base_data

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
ECONOMICS = (
    "AI economics (ledger-wide, all homes)",
    "Usage reconciled to billing",
    "Total Cost of AI component: Token and API usage",
    "Total Cost of AI components",
    "Booked-value status",
    "No value is booked.",
)
# Role, screen and exact phrases. The invoice screen is read by the approver and the
# payment officer roles; the funding screen by the preparer role and the approver.
SCREENS = (
    (
        "pam@example.test",
        "Invoice queue",
        (
            "Read-only reader view for the approver and payment officer.",
            "It makes no payment, approval or decision and changes no record.",
            "Invoice line comparison",
            "SYN-INV-225",
            "Quantity 2, line total",
            "Unknown. No matched commitment.",
            "Unknown. No milestone reference supplied.",
            "This system never makes or releases a payment.",
            *ECONOMICS,
        ),
        ("Invoice line comparison", "Line comparison for SYN-INV-225"),
    ),
    (
        "support@example.test",
        "Invoice queue",
        (
            "Read-only reader view for the approver and payment officer.",
            "Invoice line comparison",
            "SYN-INV-225",
            *ECONOMICS,
        ),
        ("Invoice line comparison", "Line comparison for SYN-INV-225"),
    ),
    (
        "grants@example.test",
        "Funding route and claim pack",
        (
            "It is a reviewed export or readiness view only.",
            "No submission, award, eligibility decision or payment is made or inferred.",
            "Unknown. This page cannot confirm eligibility.",
            "Grant stages and approved evidence",
            "SYN-GR-225",
            "Unknown. No approved stage.",
            "Submission, award and payment",
            "Not recorded here. This screen never infers them.",
            *ECONOMICS,
        ),
        ("Funding route", "Grant stages", "Readiness export"),
    ),
)
AXE_SKIPPED: list[str] = []


def synthetic_data() -> dict[str, Any]:
    """Shared synthetic home plus one grant stage that has no approved evidence."""
    data = base_data()
    data["cases"][0]["grants"] = [
        dict(id="SYN-GR-225", scheme="SYN scheme", state="Opportunity", pending=None, history=[])
    ]
    return data


SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
# Words that would turn a reader view into a claim of approval, payment or award.
FORBIDDEN = (
    "Payment released",
    "Payment made",
    "Award confirmed",
    "Submitted to",
    "Approved for payment",
)
MAX_TABS = 120


def check_accessibility(page: Page, story: str) -> None:
    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
    text = evidence.inner_text()
    check(
        f"{story} read-only: no write controls",
        evidence.locator("button, form, input, select, textarea").count() == 0,
    )
    check(
        f"{story} no role simulator text",
        "simulat" not in text.lower() and "act as" not in text.lower(),
    )
    check(
        f"{story} no payment, award or submission wording",
        not any(word in text for word in FORBIDDEN),
    )
    regions = evidence.locator('div.table-scroll[role="region"]')
    expected = regions.evaluate_all("els => els.map(el => el.getAttribute('aria-label'))")
    check(
        f"{story} every table is a labelled focusable region with a caption",
        bool(expected)
        and regions.evaluate_all(
            "els => els.every(el => el.tabIndex === 0 && el.querySelector('caption'))"
        ),
    )
    page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
    reached: list[str] = []
    for _ in range(MAX_TABS):
        page.keyboard.press("Tab")
        label = page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''")
        if label in expected and label not in reached:
            reached.append(label)
        if len(reached) == len(set(expected)):
            break
    check(
        f"{story} Tab reaches every table region: {reached}",
        sorted(reached) == sorted(set(expected)),
    )
    axe_path = os.environ.get("ZF_AXE_JS")
    if not axe_path:
        AXE_SKIPPED.append(story)
        print(f"SKIP {story} axe scan: set ZF_AXE_JS to the pinned axe 4.10.3 file")
        return
    raw = Path(axe_path).read_bytes()
    check("axe file is the pinned 4.10.3 build", hashlib.sha256(raw).hexdigest() == AXE_SHA256)
    page.evaluate(raw.decode())
    result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
      runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
    check(
        f"{story} axe 4.10.3 (main, 1280px) finds no violations: "
        f"{[v['id'] for v in result['violations']]}",
        not result["violations"],
    )
    print(
        f"INFO {story} axe incomplete (needs manual review): {[i['id'] for i in result['incomplete']]}"
    )


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for email, screen, expected, panels in SCREENS:
                story = f"{email.split('@')[0]} {screen}"
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                try:
                    page = context.new_page()
                    errors: list[str] = []
                    writes: list[str] = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.goto(base + "/app")
                    page.locator("#email").fill(email)
                    page.locator("#pw").fill("synthetic-check")
                    page.locator("button[type=submit]").click()
                    page.locator("#nav").wait_for()
                    # Attached after sign-in on purpose: the sign-in POST is expected.
                    page.on(
                        "request",
                        lambda r: (
                            writes.append(f"{r.method} {r.url}")
                            if r.method not in SAFE_METHODS
                            else None
                        ),
                    )
                    page.get_by_role("link", name="Specialist screens", exact=True).click()
                    page.get_by_role("heading", name="Specialist screens", exact=True).wait_for()
                    page.get_by_role("link", name=screen, exact=True).click()
                    page.locator('a.item[href*="case=ZF-1"]').click()
                    evidence = page.get_by_role("region", name="Evidence for ZF-1", exact=True)
                    evidence.wait_for()
                    # Panels use content-visibility, so read each one after scrolling it in.
                    chunks = []
                    for panel in evidence.locator("section, .panel").all():
                        panel.scroll_into_view_if_needed()
                        chunks.append(panel.inner_text())
                    text = "\n".join(chunks) or evidence.inner_text()
                    for phrase in expected:
                        check(f"{story} shows: {phrase}", phrase in text)
                    check(f"{story} names its panels: {panels}", all(p in text for p in panels))
                    check_accessibility(page, story)
                    for width in (320, 1280):
                        page.set_viewport_size({"width": width, "height": 900})
                        check(
                            f"{story} reflow {width}px",
                            page.evaluate(
                                "() => document.documentElement.scrollWidth <= innerWidth"
                            ),
                        )
                    check(f"{story} made no non-GET/HEAD/OPTIONS requests: {writes}", not writes)
                    check(f"{story} has no JavaScript errors: {errors}", not errors)
                finally:
                    context.close()
        finally:
            browser.close()
    if AXE_SKIPPED:
        if os.environ.get("ZF_AXE_REQUIRED") == "1":
            raise AssertionError(f"axe scan skipped for {AXE_SKIPPED} but ZF_AXE_REQUIRED=1")
        print(f"PARTIAL: axe scan SKIPPED for {AXE_SKIPPED}; no automated accessibility result")
    else:
        print("COMPLETE: all checks ran, including axe 4.10.3 (main, 1280px, all roles)")


if __name__ == "__main__":
    main(run_browser, synthetic_data)
