"""Actual loopback challenge journey; public synthetic fixture, no model or cloud."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from checks.regulatory_ux_check import AXE_SHA256, scan
from playwright.sync_api import APIResponse, Request, Route, expect, sync_playwright
from test_resident_api import ResidentApi


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
                    # An unrelated write must preserve the draft and its original binding.
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
            scope="Constructed historical UI/HTTP/SQLite correction; no whole issue acceptance",
        )
    finally:
        fixture.doCleanups()


def run_refresh_draft(axe_path: Path) -> dict[str, Any]:
    """Keep an off-page resolution draft inside the guarded history renderer."""
    raw = axe_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
    fixture = ResidentApi("test_http_challenge_both_routes_resolution_and_denied_reads")
    fixture.setUp()
    reports: list[dict[str, Any]] = []
    try:
        payload = fixture.challenge_payload()
        for index in range(50):
            code, detail = fixture.call(
                "/api/cases/ZF-1/resident",
                "sam",
                dict(payload, request=f"SYN refresh request {index + 1}"),
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
            writes: list[dict[str, Any]] = []
            dialogs: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            def record_write(request: Request) -> None:
                if (
                    request.method == "POST"
                    and request.url == fixture.base + "/api/cases/ZF-1/resident"
                ):
                    body = request.post_data_json
                    assert isinstance(body, dict), "Challenge POST must contain a JSON object"
                    writes.append(body)

            page.on("request", record_write)
            page.goto(fixture.base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-only")
            page.locator("button[type=submit]").click()
            page.locator("#nav").wait_for(state="visible")
            page.goto(fixture.base + "/app#/case/ZF-1")
            page.locator("#affected-challenges").wait_for()
            page.get_by_text("Record supplied resolution for CH-1", exact=True).first.click()
            values = {
                "resolution": "Correction recorded",
                "resolution_ref": "SYN preserved refresh correction",
                "explanation": "SYN supplied off-page explanation",
                "next_update": "2099-01-03",
            }
            for name, value in values.items():
                control = page.locator("#challenge-resolve-CH-1-" + name)
                if name == "resolution":
                    control.select_option(value)
                else:
                    control.fill(value)
            page.evaluate(
                "window.savedChallengeDraft = document.getElementById('challenge-resolve-CH-1')"
            )
            page.get_by_text("Record supplied challenge", exact=True).first.click()
            page.locator("#challenge-open-proposal_id").fill(payload["proposal_id"])
            for name in ("target_kind", "channel", "owner"):
                page.locator("#challenge-open-" + name).select_option(payload[name])
            for name in ("source", "request", "explanation", "non_digital_route", "next_update"):
                page.locator("#challenge-open-" + name).fill(payload[name])
            page.locator("#challenge-open-next_update").press("Enter")
            expect(page.get_by_text("CH-51: Open.", exact=False)).to_be_visible()

            def assert_preserved() -> None:
                expect(page.locator("#challenge-resolve-CH-1")).to_have_count(1)
                expect(
                    page.locator('#challenge-record-history form[data-unsaved="true"]')
                ).to_have_count(1)
                assert page.evaluate(
                    "document.getElementById('challenge-resolve-CH-1')"
                    " === window.savedChallengeDraft"
                ), "Refresh must retain the actual draft and its original version binding"
                for name, value in values.items():
                    control = page.locator("#challenge-resolve-CH-1-" + name)
                    expect(control).to_have_count(1)
                    expect(control).to_have_value(value)
                assert page.locator("#challenge-resolve-CH-1 label").evaluate_all(
                    "(labels) => labels.every(label => label.control"
                    " && label.control.form === label.closest('form'))"
                ), "Native labels must target controls in their own preserved form"
                assert page.locator("#affected-challenges [id]").evaluate_all(
                    "(nodes) => new Set(nodes.map(node => node.id)).size === nodes.length"
                ), "Challenge panel IDs must stay unique"

            if page.locator('#challenge-record-history form[data-unsaved="true"]').count() != 1:
                page.on("dialog", lambda dialog: dialog.dismiss())
                page.get_by_role("button", name="Older challenges", exact=True).click()
                print(
                    json.dumps(
                        {
                            "observed_defect": "Off-page draft bypasses paging guard",
                            "resolution_forms": page.locator("#challenge-resolve-CH-1").count(),
                            "resolution_reference_inputs": page.locator(
                                "#challenge-resolve-CH-1-resolution_ref"
                            ).count(),
                            "preserved_labels_target_own_form": page.locator(
                                '#challenge-resolve-CH-1[data-unsaved="true"] label'
                            ).evaluate_all(
                                "(labels) => labels.every(label => label.control"
                                " && label.control.form === label.closest('form'))"
                            ),
                            "writes": len(writes),
                        }
                    )
                )
            assert_preserved()
            scan(
                page,
                raw.decode("utf-8"),
                reports,
                "challenge-off-page-draft",
                "#affected-challenges",
            )

            def cancel_paging(dialog: Any) -> None:
                dialogs.append(dialog.message)
                dialog.dismiss()

            page.once("dialog", cancel_paging)
            page.get_by_role("button", name="Older challenges", exact=True).click()
            assert dialogs == ["Discard the unsaved resolution draft on this page?"]
            assert_preserved()
            assert "challenge-record-history=1" not in page.url
            assert len(writes) == 1 and writes[0]["action"] == "challenge_open"
            assert len(fixture.store.cases["ZF-1"]["affected_challenges"]) == 51
            assert (
                fixture.store.cases["ZF-1"]["affected_challenges"][:50]
                == before["affected_challenges"]
            )

            # Explicit confirmation discards the draft; history must not retain a duplicate.
            page.once("dialog", lambda dialog: dialog.accept())
            page.get_by_role("button", name="Older challenges", exact=True).click()
            expect(page.get_by_text("CH-1: Open.", exact=False)).to_be_visible()
            expect(page.locator("#challenge-resolve-CH-1")).to_have_count(1)
            assert page.locator("#affected-challenges [id]").evaluate_all(
                "(nodes) => new Set(nodes.map(node => node.id)).size === nodes.length"
            )
            expect(page.locator("#challenge-resolve-CH-1-resolution_ref")).to_have_value("")
            assert page.locator("#challenge-resolve-CH-1 label").evaluate_all(
                "(labels) => labels.every(label => label.control"
                " && label.control.form === label.closest('form'))"
            )
            page.get_by_text("Record supplied resolution for CH-1", exact=True).first.click()
            label = page.locator('label[for="challenge-resolve-CH-1-resolution_ref"]')
            label.click()
            expect(page.locator("#challenge-resolve-CH-1-resolution_ref")).to_be_focused()
            scan(
                page,
                raw.decode("utf-8"),
                reports,
                "challenge-draft-discarded",
                "#affected-challenges",
            )
            page.get_by_role("button", name="Newer challenges", exact=True).click()
            expect(page.locator("#challenge-resolve-CH-1")).to_have_count(0)
            page.get_by_role("button", name="Older challenges", exact=True).click()
            expect(page.locator("#challenge-resolve-CH-1")).to_have_count(1)
            assert len(writes) == 1, "Paging must never submit or retry a challenge"
            assert not errors, errors
            version = browser.version
            browser.close()
        after = fixture.store.cases["ZF-1"]
        assert after["affected_challenges"][:50] == before["affected_challenges"]
        for key in ("decision", "measure_decisions", "hazards", "closed", "service_requests"):
            assert after.get(key) == before.get(key), key
        return dict(
            outcome="passed",
            browser=version,
            challenges_before=50,
            challenges_after=51,
            preserved_draft="CH-1",
            unique_ids_and_labels=True,
            paging_confirmation=dialogs,
            committed_writes=1,
            resolution_writes_or_retries=0,
            scans=reports,
            scope="Constructed Chromium refresh/paging only; no human or whole-system acceptance",
        )
    finally:
        fixture.doCleanups()


def run_pending_draft(axe_path: Path) -> dict[str, Any]:
    """Edit actual opening/resolution forms after commit but before acknowledgement."""
    raw = axe_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
    fixture = ResidentApi("test_http_challenge_both_routes_resolution_and_denied_reads")
    fixture.setUp()
    reports: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    try:
        payload = fixture.challenge_payload()
        before = json.loads(json.dumps(fixture.store.cases["ZF-1"]))
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(reduced_motion="reduce")
            page.route(
                "**/*",
                lambda route: (
                    route.continue_()
                    if route.request.url.startswith(fixture.base + "/")
                    else route.abort()
                ),
            )
            errors: list[str] = []
            writes: list[dict[str, Any]] = []
            pending: list[tuple[Route, APIResponse]] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(fixture.base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-only")
            page.locator("button[type=submit]").click()
            page.locator("#nav").wait_for(state="visible")
            for action in ("challenge_open", "challenge_resolve"):
                page.goto(fixture.base + "/app#/case/ZF-1")
                page.locator("#affected-challenges").wait_for()
                opening = action == "challenge_open"
                key = "challenge-open" if opening else "challenge-resolve-CH-1"
                title = (
                    "Record supplied challenge"
                    if opening
                    else "Record supplied resolution for CH-1"
                )
                page.get_by_text(title, exact=True).first.click()
                values = (
                    {
                        name: payload[name]
                        for name in (
                            "proposal_id",
                            "target_kind",
                            "channel",
                            "source",
                            "request",
                            "explanation",
                            "owner",
                            "non_digital_route",
                            "next_update",
                        )
                    }
                    if opening
                    else dict(
                        resolution="Explanation recorded",
                        resolution_ref="SYN submitted resolution reference",
                        explanation="SYN submitted resolution explanation",
                        next_update="2099-01-02",
                    )
                )
                for name, value in values.items():
                    control = page.locator(f"#{key}-{name}")
                    if name in ("target_kind", "channel", "owner", "resolution"):
                        control.select_option(value)
                    else:
                        control.fill(value)
                page.evaluate(
                    "(key) => { window.savedChallengeDraft = document.getElementById(key); }",
                    key,
                )

                def hold_acknowledgement(route: Route) -> None:
                    body = route.request.post_data_json
                    assert isinstance(body, dict)
                    writes.append(body)
                    response = route.fetch()
                    assert response.ok
                    pending.append((route, response))
                    page.evaluate("window.challengeCommitted = true")

                page.route("**/api/cases/ZF-1/resident", hold_acknowledgement)
                page.evaluate("window.challengeCommitted = false")
                with page.expect_request("**/api/cases/ZF-1/resident"):
                    page.locator(f"#{key} button[type=submit]").click()
                page.wait_for_function("() => window.challengeCommitted === true")
                expect(page.locator(f"#{key} button[type=submit]")).to_be_disabled()
                for name, value in values.items():
                    assert writes[-1][name] == value, name
                draft = (
                    dict(
                        channel="Letter",
                        source="SYN later source",
                        request="SYN later request",
                        explanation="SYN later opening explanation",
                        non_digital_route="SYN later manual route",
                        next_update="2099-02-03",
                    )
                    if opening
                    else dict(
                        resolution="Correction recorded",
                        resolution_ref="SYN later resolution reference",
                        explanation="SYN later resolution explanation",
                        next_update="2099-02-03",
                    )
                )
                for name, value in draft.items():
                    control = page.locator(f"#{key}-{name}")
                    expect(control).to_be_enabled()
                    if name in ("channel", "resolution"):
                        control.select_option(value)
                    else:
                        control.fill(value)
                # Enter is a real implicit submission attempt while the button is disabled.
                page.locator(f"#{key}-next_update").press("Enter")
                page.locator(f"#{key}").evaluate("(form) => form.requestSubmit()")
                assert len(writes) == len(results) + 1
                with page.expect_request(fixture.base + "/api/cases/ZF-1"):
                    route, response = pending[-1]
                    route.fulfill(response=response)
                page.wait_for_load_state("networkidle")
                for name, value in draft.items():
                    expect(page.locator(f"#{key}-{name}")).to_have_value(value)
                assert page.evaluate(
                    "(key) => document.getElementById(key) === window.savedChallengeDraft", key
                ), "Keep the actual form and its original tokens"
                expect(page.locator(f"#{key}")).to_have_attribute("data-unsaved", "true")
                expect(page.locator(f"#{key}-feedback")).to_contain_text(
                    "Only the submitted values were recorded"
                )
                expect(page.locator(f"#{key} button[type=submit]")).to_be_disabled()
                # Even programmatic submission must not write the acknowledged action again.
                page.locator(f"#{key}").evaluate("(form) => form.requestSubmit()")
                page.wait_for_load_state("networkidle")
                assert len(writes) == len(results) + 1
                code, detail = fixture.call("/api/cases/ZF-1", "sam")
                assert code == 200 and len(detail["affected_challenges"]) == 1
                record = detail["affected_challenges"][0]
                persisted = record if opening else record["resolution"]
                for name, value in values.items():
                    if name in ("proposal_id", "target_kind", "owner"):
                        continue
                    field = (
                        "outcome"
                        if name == "resolution"
                        else "reference"
                        if name == "resolution_ref"
                        else name
                    )
                    assert persisted[field] == value, name
                scan(
                    page,
                    raw.decode("utf-8"),
                    reports,
                    action + "-pending-draft",
                    "#affected-challenges",
                )
                page.evaluate("window.challengeNavigationCancelled = false")

                def cancel_navigation(dialog: Any) -> None:
                    assert "unsaved" in dialog.message
                    dialog.dismiss()
                    page.evaluate("window.challengeNavigationCancelled = true")

                page.once("dialog", cancel_navigation)
                page.get_by_role("link", name="Back to the list", exact=True).click()
                page.wait_for_function("() => window.challengeNavigationCancelled === true")
                expect(page).to_have_url(fixture.base + "/app#/case/ZF-1")
                expect(page.locator(f"#{key}-explanation")).to_have_value(draft["explanation"])
                page.once("dialog", lambda dialog: dialog.accept())
                page.locator(f"#{key} button[type=reset]").click()
                page.unroute("**/api/cases/ZF-1/resident", hold_acknowledgement)
                results.append(dict(action=action, submitted=values, unsent_draft=draft))
            assert not errors, errors
            version = browser.version
            browser.close()
        after = fixture.store.cases["ZF-1"]
        for field in ("decision", "measure_decisions", "hazards", "closed", "service_requests"):
            assert after.get(field) == before.get(field), field
        return dict(
            outcome="passed",
            browser=version,
            journeys=results,
            committed_writes=len(writes),
            cancelled_or_retried_writes=0,
            scans=reports,
            page_errors=errors,
            scope="Constructed delayed-acknowledgement Chromium; no human/WCAG acceptance",
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
                lambda route: (
                    route.continue_()
                    if route.request.url.startswith(fixture.base + "/")
                    else route.abort()
                ),
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
                for name in (
                    "source",
                    "request",
                    "explanation",
                    "non_digital_route",
                    "next_update",
                ):
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
                    expect(
                        page.get_by_role("link", name="See all cases", exact=True)
                    ).to_be_visible()
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
        return dict(
            outcome="passed",
            browser=version,
            committed_writes=2,
            destinations=["case ZF-5", "case list"],
            stale_refresh_reads=0,
            cancelled_or_retried_writes=0,
            page_errors=errors,
        )
    finally:
        fixture.doCleanups()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--navigation", action="store_true")
    parser.add_argument("--refresh-draft", action="store_true")
    parser.add_argument("--pending-draft", action="store_true")
    args = parser.parse_args()
    result = (
        run_pending_draft(args.axe)
        if args.pending_draft
        else run_refresh_draft(args.axe)
        if args.refresh_draft
        else run_navigation()
        if args.navigation
        else run_history(args.axe)
        if args.history
        else run(args.axe)
    )
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
