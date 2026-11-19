"""Loopback check of the three standalone nomination route forms with axe; public synthetic fixture only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from checks.regulatory_ux_check import AXE_SHA256, CONTROLS
from playwright.sync_api import sync_playwright
from test_nomination_api_routes import NominationApiRoutesTests

PAGE = "/api/cases/ZF-1?view=nomination-routes-html"
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]


def scan(page: Any, axe: str, reports: list[dict[str, Any]], state: str) -> None:
    """Run axe on the page and record every result; the caller asserts none remain."""
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        "async tags => await axe.run({include: [['main']]}, {runOnly: {type: 'tag', values: tags}})",
        TAGS,
    )
    small = (
        page.locator("main")
        .locator(CONTROLS)
        .evaluate_all(
            """nodes => nodes.map(el => { const r = el.getBoundingClientRect();
          return {control: el.id || el.tagName, width: r.width, height: r.height}; })
          .filter(s => s.width < 24 || s.height < 24)"""
        )
    )
    reports.append(
        dict(
            state=state,
            violations=[v for v in result["violations"] if v["id"] != "target-size"],
            target_size_violations=[
                [n["target"] for n in v["nodes"]]
                for v in result["violations"]
                if v["id"] == "target-size"
            ],
            passes=len(result["passes"]),
            incomplete=[item["id"] for item in result["incomplete"]],
            controls_under_24px=small,
        )
    )


def run(axe_path: Path) -> dict[str, Any]:
    raw = axe_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
    axe = raw.decode("utf-8")
    fixture = NominationApiRoutesTests("test_standalone_route_forms_submit_in_browser")
    fixture.setUp()
    reports: list[dict[str, Any]] = []
    statuses: list[int] = []
    try:
        code, _ = fixture.call_json("/api/cases/ZF-1/resident", "sam", fixture.nomination_payload())
        assert code == 200
        nom_id = fixture.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0]["id"]
        fixture.seed_priority_proposal()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            context.add_cookies(
                [
                    {
                        "name": "zf_session",
                        "value": fixture._login_cookie("sam").split("=", 1)[1],
                        "url": fixture.base,
                    }
                ]
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
            page.on(
                "response",
                lambda r: statuses.append(r.status) if "/resident" in r.url else None,
            )
            page.goto(fixture.base + PAGE)
            for summary in page.locator("summary").all():
                summary.click()
            scan(page, axe, reports, "routes-forms-open")
            steps = (
                (
                    f"#nomination-ack-{nom_id}",
                    {
                        "channel": "digital",
                        "acknowledgement_ref": "SYN-CHECK-ACK",
                        "non_digital_route": "Phone Sam or visit housing hub",
                        "next_update": "2099-03-01",
                    },
                ),
                (
                    f"#nomination-correct-{nom_id}",
                    {
                        "channel": "digital",
                        "account": "Synthetic corrected account",
                        "source": "SYN-CHECK-CORRECTION",
                        "reported_subject_ref": "SYN-SUBJECT",
                        "next_update": "2099-03-02",
                    },
                ),
                (
                    "#challenge-open-route",
                    {
                        "channel": "digital",
                        "source": "SYN-CHECK-CHALLENGE",
                        "request": "Synthetic supplied challenge",
                        "explanation": "Synthetic explanation",
                        "non_digital_route": "Phone Sam or visit housing hub",
                        "next_update": "2099-03-03",
                    },
                ),
            )
            for key, fields in steps:
                page.locator(f"{key}").locator("xpath=ancestor::details").evaluate(
                    "e => { e.open = true; }"
                )
                for name, value in fields.items():
                    field = page.locator(f"{key}-{name}")
                    if field.evaluate("e => e.tagName") == "SELECT":
                        field.select_option(value)
                    else:
                        field.fill(value)
                with page.expect_navigation():
                    page.locator(f"{key} button[type='submit']").click()
            scan(page, axe, reports, "routes-after-submissions")
            assert not errors, errors
            version = browser.version
            browser.close()
        assert statuses == [200, 200, 200], statuses
        detail = fixture.call_json("/api/cases/ZF-1", "sam")[1]
        record = detail["nomination_records"][0]
        assert record["acknowledgement"]["reference"] == "SYN-CHECK-ACK"
        assert [c["source"] for c in record["corrections"]] == ["SYN-CHECK-CORRECTION"]
        assert "SYN-CHECK-CHALLENGE" in json.dumps(detail["affected_challenges"])
        for report in reports:
            assert not report.get("violations"), report
            assert not report.get("target_size_violations"), report
        return dict(
            outcome="passed",
            browser=version,
            axe_version="4.10.3",
            axe_sha256=AXE_SHA256,
            resident_post_statuses=statuses,
            scans=reports,
            screen_reader="Not run",
            human_acceptance="Not run",
            scope="Constructed synthetic standalone route forms only; no whole-system conformance",
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
