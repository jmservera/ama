"""Browser evidence for the read-only versioned home case screen (#74).

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.home_case_browser_check
Set ZF_AXE_JS to the pinned axe 4.10.3 file to add the automated scan.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from checks.design_system_browser_check import ROOT, check, main

sys.path.insert(0, str(ROOT / "src/core/tests"))

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
# Sibling home ZF-3 evidence must never appear on the view of ZF-2.
SIBLING_ONLY = ("Synthetic survey metadata only", "Loft insulation", "SIBLING-EVIDENCE")


def home_case_data() -> dict[str, Any]:
    """Two fictional homes sharing a building that lists a dependency, a hold, works and a cost."""
    from building_fixture import fixture, hold

    data = fixture()
    building = data["buildings"][0]
    building["dependencies"] = [
        {
            "id": "DEP-1",
            "label": "Roof access needed before loft works",
            "status": "Open",
            "owner": "Synthetic coordinator",
            "source": "SYN-DEPENDENCY",
            "case_ids": ["ZF-2"],
            "package_ids": ["PKG-SHARED"],
        }
    ]
    building["holds"] = [hold()]
    return data


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            errors: list[str] = []
            writes: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "/app")
            page.locator("#email").fill("pam@example.test")
            page.locator("#pw").fill("synthetic-check")
            page.locator("button[type=submit]").click()
            page.locator("#nav").wait_for()
            # Attached after sign-in on purpose: the sign-in POST is expected.
            page.on(
                "request",
                lambda r: (
                    writes.append(f"{r.method} {r.url}") if r.method not in SAFE_METHODS else None
                ),
            )
            page.evaluate("() => { location.hash = '#/case-home/ZF-2'; }")
            page.get_by_role("heading", name="Home case ZF-2", exact=True).wait_for()
            home = page.get_by_role("region", name="This home only", exact=False)
            shared = page.get_by_role("region", name="Shared at building level", exact=False)
            home_text = home.inner_text()
            shared_text = shared.inner_text()
            main_text = page.locator("main").inner_text()
            check("home panel is its own labelled region", home.count() == 1)
            check("building panel is its own labelled region", shared.count() == 1)
            check(
                "building dependency, hold, works and cost appear only in the building panel",
                all(
                    token in shared_text and token not in home_text
                    for token in ("DEP-1", "HOLD-1", "WORK-1", "GBP 12000.00")
                ),
            )
            check(
                "home panel shows this home's decision, stage and cost allocation",
                all(t in home_text for t in ("Decision: Accepted", "Stage:", "GBP 6000.00")),
            )
            check(
                "shared building ID does not carry the sibling home's evidence",
                not any(token in main_text for token in SIBLING_ONLY),
            )
            check(
                "version status and no-transfer notice are shown",
                "No version recorded yet" in main_text and "does not transfer" in main_text,
            )
            check(
                "manual path to the case and building screens is shown",
                page.get_by_role("link", name="Open full building context").count() == 1
                and page.get_by_role("link", name="Back to the case").count() == 1,
            )
            check(
                "read-only: no write controls on the screen",
                page.locator("main").locator("button, form, input, select, textarea").count() == 0,
            )
            headings = page.locator("main h1, main h2").all_inner_texts()
            check(f"one h1 then four h2 panels: {headings}", len(headings) == 5)
            for width in (320, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                check(
                    f"reflow {width}px",
                    page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"),
                )
            axe_path = os.environ.get("ZF_AXE_JS")
            if axe_path:
                raw = Path(axe_path).read_bytes()
                check(
                    "axe file is the pinned 4.10.3 build",
                    hashlib.sha256(raw).hexdigest() == AXE_SHA256,
                )
                page.evaluate(raw.decode())
                result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
                  runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
                check(
                    f"axe 4.10.3 finds no violations: {[v['id'] for v in result['violations']]}",
                    not result["violations"],
                )
                print("COMPLETE: all checks ran, including axe 4.10.3")
            else:
                print("PARTIAL: axe scan SKIPPED; set ZF_AXE_JS. No automated accessibility result")
            check(f"made no non-GET/HEAD/OPTIONS requests: {writes}", not writes)
            check(f"no JavaScript errors: {errors}", not errors)
            context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, home_case_data)
