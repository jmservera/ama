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
# ZF-2 own evidence, seeded below, must never appear on the view of ZF-3.
OWN_ONLY = ("Synthetic own-home survey", "Ventilation extract")
SYSTEM_ITEM = "SYS-1: Shared ventilation Source: SYN-SURVEY"


BUILDING_ONLY = ("DEP-1", "HOLD-1", "WORK-1", "WORK-M", "SYS-1", "COST-1: GBP 12000.00")
HOME_HEADINGS = ("Evidence documents", "Quality outcomes", "Cost allocation")
BUILDING_HEADINGS = (
    "Shared systems",
    "Dependencies",
    "Work stopped pending review",
    "Shared works",
)


def check_regions_apart(label: str, home: Any, shared: Any, own_tokens: tuple[str, ...]) -> None:
    """Each record type sits in exactly one region; neither region carries the other's records."""
    home_text, shared_text = home.inner_text(), shared.inner_text()
    home_h3 = home.locator("h3").all_inner_texts()
    shared_h3 = shared.locator("h3").all_inner_texts()
    check(
        f"{label}: building dependency, hold, works, system and shared cost never enter the home region",
        all(token in shared_text and token not in home_text for token in BUILDING_ONLY),
    )
    check(
        f"{label}: own evidence, decision, allocation and outcome never enter the building region",
        all(token in home_text and token not in shared_text for token in own_tokens)
        and "Decision:" not in shared_text
        and "This home's share" not in shared_text
        and "GBP 6000.00" not in shared_text,
    )
    check(
        f"{label}: sub-headings stay in their own region: {home_h3} / {shared_h3}",
        all(t in home_h3 for t in HOME_HEADINGS)
        and not any(t in shared_h3 for t in HOME_HEADINGS)
        and all(t in shared_h3 for t in BUILDING_HEADINGS)
        and not any(t in home_h3 for t in BUILDING_HEADINGS),
    )
    check(
        f"{label}: the two regions do not nest or overlap",
        home.locator("section").count() == 0
        and shared.locator("[aria-labelledby=hc-home]").count() == 0
        and home.locator("[aria-labelledby=hc-building]").count() == 0
        and home.evaluate("(a, b) => !a.contains(b) && !b.contains(a)", shared.element_handle()),
    )


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
    scopes = [
        ("WORK-U", None, []),
        ("WORK-N", [], None),
        ("WORK-M", ["ZF-2", "ZF-3"], ["PKG-SHARED"]),
    ]
    building["works"] += [
        {**building["works"][0], "id": wid, "case_ids": homes, "package_ids": packages}
        for wid, homes, packages in scopes
    ]
    own, sibling = data["cases"]
    own["documents"].append(
        {
            "id": "OWN-EVIDENCE",
            "name": "Synthetic own-home survey",
            "kind": "Survey",
            "source": "SYN-EVIDENCE",
            "at": "2026-10-16",
            "by": "Synthetic surveyor",
        }
    )
    own["quality"] = [
        {**sibling["quality"][0], "measure": "Ventilation extract", "source": "SYN-QA-OWN"}
    ]
    own["quality"][0]["resident_binding"] = {
        "measure": "Ventilation extract",
        "context_revision": 1,
    }
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

            def item(wid: str) -> str:
                return shared.locator("li", has_text=wid).first.inner_text()

            check(
                "recorded scopes show listed IDs, unknown and none apart, in the building panel only",
                "Homes: ZF-2. Packages: PKG-SHARED." in item("DEP-1")
                and "Homes: Unknown. Packages: None." in item("WORK-U")
                and "Homes: None. Packages: Unknown." in item("WORK-N")
                and "Homes: ZF-2, ZF-3. Packages: PKG-SHARED." in item("WORK-M")
                and "Homes: " not in home_text
                and "do not establish eligibility, approval or coverage" in shared_text,
            )
            check(
                "systems carry no scope line",
                "Homes:" not in item("SYS-1"),
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
                "ZF-2 shows its own document and quality in the home panel only",
                all(t in home_text and t not in shared_text for t in OWN_ONLY),
            )
            check(
                "shared system item is in the building panel only on ZF-2",
                SYSTEM_ITEM in shared_text and "SYS-1" not in home_text,
            )
            check_regions_apart(
                "ZF-2", home, shared, ("Synthetic own-home survey", "Ventilation extract")
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
            page.evaluate("() => { location.hash = '#/case-home/ZF-3'; }")
            page.get_by_role("heading", name="Home case ZF-3", exact=True).wait_for()
            home = page.get_by_role("region", name="This home only", exact=False)
            shared = page.get_by_role("region", name="Shared at building level", exact=False)
            home_text = home.inner_text()
            shared_text = shared.inner_text()
            main_text = page.locator("main").inner_text()
            check(
                "ZF-3 has its own labelled home and building panels",
                home.count() == shared.count() == 1,
            )
            check(
                "ZF-3 shows its own document and quality in the home panel only",
                all(
                    t in home_text and t not in shared_text
                    for t in ("Synthetic survey metadata only", "Loft insulation")
                ),
            )
            check(
                "ZF-3 view carries none of ZF-2's own document or quality",
                not any(token in main_text for token in OWN_ONLY),
            )
            check(
                "shared system item is in the building panel only on ZF-3",
                SYSTEM_ITEM in shared_text and "SYS-1" not in home_text,
            )
            check(
                "ZF-3 shows its own GBP 6000.00 allocation at home and GBP 12000.00 only in the building panel",
                "GBP 6000.00" in home_text
                and "GBP 12000.00" in shared_text
                and "GBP 12000.00" not in home_text,
            )
            check_regions_apart(
                "ZF-3", home, shared, ("Synthetic survey metadata only", "Loft insulation")
            )
            check(
                "ZF-3 has one h1 then four h2 panels",
                len(page.locator("main h1, main h2").all_inner_texts()) == 5,
            )
            check(f"made no non-GET/HEAD/OPTIONS requests: {writes}", not writes)
            check(f"no JavaScript errors: {errors}", not errors)
            context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main(run_browser, home_case_data)
