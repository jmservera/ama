"""Local synthetic Playwright proof for issue 76; run from src/api: python3 ../../<this file>."""

import json
import os
import sys

sys.path.insert(0, os.getcwd())
from playwright.sync_api import sync_playwright

from checks.design_system_browser_check import main
from checks.workbench_browser_check import MANIFEST, synthetic_data

OUT = os.environ["I76_OUT"]


def proof(base: str) -> None:
    email = next(r["email"] for r in MANIFEST["roles"] if r["role"] == "Retrofit Coordinator")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.route("https://tile.openstreetmap.org/**", lambda r: r.abort())
        page.goto(base + "/app")
        page.locator("#email").fill(email)
        page.locator("#pw").fill("synthetic-check")
        page.locator("button[type=submit]").click()
        page.get_by_role("heading", name="My cases today").wait_for()
        rows = page.request.get(base + "/api/cases?view=all").json()["items"]
        report = []
        for row in rows:
            card = page.request.get(base + "/api/cases/" + row["id"]).json()
            work = card["work"]
            report.append(
                dict(
                    id=row["id"],
                    hazard=[
                        {k: c.get(k) for k in ("clock_status", "clock_remaining_hours", "clock_label", "accountable_owner", "named_owner")}
                        for c in work["hazard_clocks"]
                    ],
                )
            )
            if work["hazard_clocks"]:
                page.goto(base + "/app#/case/" + row["id"])
                page.get_by_role("heading", name="Recorded task context").wait_for()
                clock = page.locator(".safety-clock:visible").first
                clock.wait_for()
                shown = clock.inner_text()
                report[-1]["visible_text"] = shown
                report[-1]["safety_panel_text"] = page.locator(".safety-clock-owner").first.inner_text()
                page.screenshot(path=f"{OUT}/shots/case-card-{row['id']}.png", full_page=True)
        json.dump(report, open(f"{OUT}/local-proof.out.json", "w"), indent=1)
        browser.close()


main(proof, synthetic_data)
