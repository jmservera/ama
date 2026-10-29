"""Synthetic local app checks for issue 215; no private data or provider calls."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import timedelta
from pathlib import Path
from threading import Event
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

from regulatory_fixture import NOW
from test_regulatory_chat_api import RegulatoryApi

if TYPE_CHECKING:
    from playwright.sync_api import Page

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
ROLES = {
    "Resident Liaison Officer": "Repairs and intake",
    "Building Safety Liaison": "Building Safety:",
    "Retrofit Coordinator": "Assessment and coordination",
    "Quality Inspector": "Assessment and quality",
    "Retrofit Programme Manager": "Programme:",
    "Programme Support Officer": "Programme support",
    "Grants and Evidence Officer": "Finance and grants",
}
COPY_SOURCE_CANARY = (
    "Synthetic hazard reports go to a human reviewer; this fixture is not law. "
    "Exact source terms: gate, hold, provenance, trace, snapshot, envelope."
)
CONTROLS = (
    "summary:visible, a[href]:visible, button:visible:enabled, "
    "input:visible:enabled, select:visible:enabled, textarea:visible:enabled"
)


def target_sizes(page: Page, selector: str) -> list[dict[str, Any]]:
    controls = page.locator(selector).locator(CONTROLS)
    # Preserve the shipped 44px disclosure target as well as the 24px AA floor.
    sizes: list[dict[str, Any]] = controls.evaluate_all(
        """nodes => nodes.map(el => {
          const r = el.getBoundingClientRect();
          return {control: el.id || el.outerHTML.slice(0, 180),
            width: r.width, height: r.height,
            min_height: el.matches('.regulatory summary') ? 44 : 24};
        })"""
    )
    assert sizes or selector == "#regulatory-supplier", (
        f"No interactive targets checked: {selector}"
    )
    for size in sizes:
        assert size["width"] >= 24 and size["height"] >= size["min_height"], (
            f"Target size below 24px width / {size['min_height']}px height: {size['control']} "
            f"({size['width']} x {size['height']})"
        )
    return sizes


def scan(
    page: Page,
    axe: str | None,
    reports: list[dict[str, Any]],
    state: str,
    selector: str = "#regulatory-alerts, #chat-panel",
) -> None:
    sizes = target_sizes(page, selector)
    if axe is None:
        reports.append(dict(state=state, axe="skipped: not supplied", target_sizes=sizes))
        return
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async selector => await axe.run(
          {include: [[selector]]},
          {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a',
            'wcag21aa', 'wcag22aa']}})""",
        selector,
    )
    reports.append(
        dict(
            state=state,
            target_sizes=sizes,
            violations=result["violations"],
            incomplete=[
                dict(
                    id=item["id"],
                    nodes=[
                        dict(target=node["target"], reason=node.get("failureSummary"))
                        for node in item["nodes"]
                    ],
                )
                for item in result["incomplete"]
            ],
            passes=len(result["passes"]),
        )
    )
    assert not result["violations"], json.dumps(result["violations"], indent=2)


def scan_mid_fade(page: Page, axe: str | None, reports: list[dict[str, Any]], state: str) -> None:
    """Scan the cited lookup button while a disabled-to-enabled fade is frozen mid-way."""
    selector = "#regulatory-chat > form > button[type=submit]"
    for percent in (35, 50):
        frozen: dict[str, Any] = page.evaluate(
            """async ([selector, fraction]) => {
              const button = document.querySelector(selector);
              const field = document.querySelector('#regulatory-question');
              button.disabled = true;
              await new Promise(resolve => setTimeout(resolve, 200));
              button.disabled = false;
              await new Promise(resolve => requestAnimationFrame(
                () => requestAnimationFrame(resolve)));
              const animations = button.getAnimations();
              for (const animation of animations) {
                animation.pause();
                animation.currentTime = fraction * animation.effect.getComputedTiming().duration;
              }
              return {
                background: getComputedStyle(button).backgroundColor,
                properties: animations.map(animation => animation.transitionProperty)
              };
            }""",
            [selector, percent / 100],
        )
        try:
            assert frozen["background"] == "rgb(11, 93, 107)", (
                f"Re-enabled lookup button background is {frozen['background']} "
                f"at {percent}% of its fade; expected the brand colour "
                f"(animated: {frozen['properties']})"
            )
            assert "background-color" not in frozen["properties"], frozen["properties"]
            scan(page, axe, reports, f"{state}-{percent}pct")
        finally:
            page.evaluate(
                """selector => {
                  for (const animation of document.querySelector(selector).getAnimations()) {
                    animation.cancel();
                  }
                  document.querySelector('#regulatory-question').focus();
                }""",
                selector,
            )


def open_home(page: Page, base: str) -> None:
    from playwright.sync_api import expect

    page.goto(base + "/app#/case/ZF-1?tab=blockers")
    page.reload()
    expect(page.locator("#regulatory-alerts")).to_be_visible()
    expect(page.locator("#regulatory-alerts [role=status]")).not_to_contain_text("Loading")


def keyboard_activate(page: Page, selector: str, key: str = "Enter") -> None:
    from playwright.sync_api import expect

    target = page.locator(selector)
    target.focus()
    expect(target).to_be_focused()
    assert target.evaluate(
        """el => {
          const s = getComputedStyle(el), r = el.getBoundingClientRect();
          return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2 &&
            r.width >= 24 && r.height >= 24;
        }"""
    ), f"Visible focus or target size: {selector}"
    page.keyboard.press(key)


def keyboard_walk(page: Page, selector: str) -> None:
    from playwright.sync_api import expect

    controls = page.locator(selector).locator(
        "summary:visible, a:visible, button:visible:enabled, "
        "input:visible:enabled, textarea:visible:enabled"
    )
    count = controls.count()
    assert count > 0
    controls.first.focus()
    for index in range(count):
        control = controls.nth(index)
        expect(control).to_be_focused()
        assert control.evaluate(
            """el => {
              const r = el.getBoundingClientRect(), s = getComputedStyle(el);
              const top = Math.max(0, r.top), bottom = Math.min(innerHeight, r.bottom);
              return bottom > top && s.outlineStyle !== 'none' &&
                parseFloat(s.outlineWidth) >= 2;
            }"""
        ), f"Focus hidden or not visible: {selector}/{index}"
        page.keyboard.press("Tab")
    page.keyboard.press("Shift+Tab")
    expect(controls.last).to_be_focused()


def run(axe_path: Path | None) -> dict[str, Any]:
    axe = None
    if axe_path is not None:
        raw = axe_path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == AXE_SHA256, "Unexpected axe 4.10.3 content"
        axe = raw.decode()
    from playwright.sync_api import expect, sync_playwright

    fixture = RegulatoryApi("runTest")
    reports: list[dict[str, Any]] = []
    fixture.setUp()
    try:
        fixture.f.source(version=2, text=COPY_SOURCE_CANARY)
        fixture.f.card(pid="synthetic@v2#0001")
        # This clock is deliberately fictional and never supplied through HTTP.
        fixture.app.rule_engine().run(
            fixture.f.store, "ZF-1", "schedule", now=NOW + timedelta(days=1)
        )
        for index, role in enumerate((*ROLES, "Contractor")):
            person = dict(
                email=f"role-{index}@example.test",
                name=f"Synthetic role {index}",
                role=role,
                code=f"SYN-{index}",
                contractor="Test Ltd",
            )
            fixture.f.store.db.execute(
                "INSERT INTO staff (email, body) VALUES (?,?)",
                (person["email"], json.dumps(person)),
            )
            fixture.f.store.staff[person["email"]] = person
            fixture.f.store.data["staff"].append(person)
        with fixture.f.store.lock:
            pass
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            # Never load tiles, remote fonts or other third-party resources.
            context.route(
                "**/*",
                lambda route: (
                    route.continue_()
                    if route.request.url.startswith(fixture.base + "/")
                    else route.abort()
                ),
            )
            context.add_cookies(
                [
                    dict(
                        name="zf_session",
                        value=fixture.cookies["sam@example.test"].split("=", 1)[1],
                        url=fixture.base,
                    )
                ]
            )
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            open_home(page, fixture.base)
            alerts = page.locator("#regulatory-alerts")
            expect(alerts).to_contain_text("Status: breach risk")
            for field in (
                "What was noticed",
                "Safe action",
                "Decision owner",
                "Clock",
                "Check recorded at",
                "Source and status",
                "Retrieved/observed:",
                "Owner acknowledgement: required",
                "synthetic-demo",
            ):
                expect(alerts).to_contain_text(field)
            expect(alerts).to_contain_text("Coverage: unknown")
            expect(alerts).to_contain_text(
                "This panel cannot acknowledge, decide compliance or restart stopped retrofit work."
            )
            expect(alerts.locator(".notice")).to_contain_text(
                "Use the existing human emergency or hazard service now. "
                "Do not wait for alerts, chat or this application."
            )
            expect(page.locator(".work-context").first).to_contain_text("recorded as of:")
            expect(page.locator(".safety-clock").first).to_contain_text(
                "Safety clock in this recorded view:"
            )
            # The safety route is visible while optional chat is collapsed.
            expect(page.locator("#chat-panel")).not_to_have_attribute("open", "")
            expect(alerts.locator(".notice")).to_be_visible()
            scan(page, axe, reports, "alert-collapsed-chat")

            keyboard_activate(page, "#alerts-plain-mode", "Space")
            expect(alerts.locator(".plain-explanation")).not_to_be_visible()
            keyboard_activate(page, "#alerts-plain-mode", "Space")
            expect(alerts.locator(".plain-explanation")).to_be_visible()
            # Real sequential Tab and reverse traversal, not only programmatic focus.
            page.keyboard.press("Tab")
            expect(alerts.locator("a").first).to_be_focused()
            page.keyboard.press("Shift+Tab")
            expect(page.locator("#alerts-plain-mode")).to_be_focused()
            page.get_by_role("tab", name="AI assistance", exact=False).press("Enter")
            keyboard_activate(page, "#chat-panel > summary")
            disclaimer = page.locator("#chat-panel > summary + p.muted")
            expect(disclaimer).to_have_count(1)
            expect(disclaimer).to_be_visible()
            expect(disclaimer).to_contain_text("AI suggestion, not approved")
            expect(disclaimer).to_contain_text(
                "it can only request a proposal that someone else reviews"
            )
            keyboard_activate(page, "#regulatory-chat > summary", "Space")
            chat = page.locator("#regulatory-chat")
            expect(chat).to_contain_text("Synthetic source lookup available")
            keyboard_activate(page, "#chat-plain-mode", "Space")
            expect(chat.locator(".plain-explanation").first).not_to_be_visible()
            keyboard_activate(page, "#chat-plain-mode", "Space")
            question = page.locator("#regulatory-question")
            question.focus()
            page.keyboard.type("What do the hazard sources say for this home?")
            page.keyboard.press("Tab")
            expect(chat.locator("button[type=submit]")).to_be_focused()
            started, release = Event(), Event()
            render = fixture.app.regulatory.render

            def delayed_render(bundle: dict[str, Any]) -> dict[str, Any]:
                started.set()
                if not release.wait(10):
                    raise RuntimeError("Synthetic pending-answer test timed out")
                result: dict[str, Any] = render(bundle)
                return result

            with patch.object(fixture.app.regulatory, "render", side_effect=delayed_render):
                try:
                    with page.expect_request("**/api/chat/regulatory/threads/*/ask"):
                        page.keyboard.press("Enter")
                    question.fill("Next draft retained")
                finally:
                    release.set()
                expect(chat.locator(".regulatory-turn")).to_have_count(1)
                assert started.is_set(), "Local source lookup did not start"
            expect(question).to_have_value("Next draft retained")
            expect(chat.locator("ol > li").first).to_contain_text(
                "What do the hazard sources say for this home?"
            )
            expect(question).to_be_focused()
            for heading in (
                "What the sources say",
                "Recorded home facts",
                "Unknown or missing",
                "Safe next action",
                "Who decides",
            ):
                expect(chat.locator("h4", has_text=heading)).to_be_visible()
            expect(chat.locator("blockquote")).to_have_text(
                f"[synthetic@v2#0001] {COPY_SOURCE_CANARY}"
            )
            expect(chat).to_contain_text("Model calls for this question: 0")
            expect(page.locator("#regulatory-usage")).to_contain_text("1 turns")
            expect(page.locator("#regulatory-usage")).to_contain_text("Service cost: Unknown")
            expect(alerts).to_contain_text("Model calls per check and alert: 0")
            expect(chat).to_contain_text("Effective: 2026-01-01")
            expect(chat.locator("a").first).to_have_attribute(
                "href", "/api/law/provisions/synthetic%40v2%230001"
            )
            scan(page, axe, reports, "cited-answer")
            scan_mid_fade(page, axe, reports, "cited-answer-fade")
            doubt = chat.locator(".regulatory-turn button").first
            doubt.focus()
            page.keyboard.press("Enter")
            expect(chat.locator(":scope > p[role=status]")).to_contain_text("exercise inbox")
            expect(doubt).to_be_focused()
            expect(doubt).to_have_attribute("aria-disabled", "true")
            page.get_by_role("tab", name="Blockers and safety", exact=False).press("Enter")
            keyboard_walk(page, "#regulatory-alerts")
            page.get_by_role("tab", name="AI assistance", exact=False).press("Enter")
            keyboard_walk(page, "#regulatory-chat")
            inbox = fixture.call("/api/chat/regulatory/inbox", email="exercise-owner@example.test")[
                1
            ]
            assert len(inbox["threads"]) == 1

            question.fill("What are the lease terms?")
            question.press("Tab")
            page.keyboard.press("Enter")
            expect(chat.locator(".regulatory-turn")).to_have_count(2)
            expect(chat.locator(".regulatory-turn").last).to_contain_text("No source held")
            scan(page, axe, reports, "no-source-refused")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                for selector in ("#regulatory-alerts", "#regulatory-chat"):
                    name = (
                        "Blockers and safety"
                        if selector == "#regulatory-alerts"
                        else "AI assistance"
                    )
                    page.get_by_role("tab", name=name, exact=False).press("Enter")
                    assert page.locator(selector).evaluate(
                        "el => el.scrollWidth <= el.clientWidth + 1"
                    ), f"Horizontal overflow at {width}px: {selector}"
                scan(page, axe, reports, f"{width}px-reflow")
            page.locator("#regulatory-alerts, #regulatory-chat").evaluate_all(
                "nodes => nodes.forEach(el => el.style.fontSize = '200%')"
            )
            page.set_viewport_size({"width": 320, "height": 900})
            for selector in ("#regulatory-alerts", "#regulatory-chat"):
                name = (
                    "Blockers and safety" if selector == "#regulatory-alerts" else "AI assistance"
                )
                page.get_by_role("tab", name=name, exact=False).press("Enter")
                assert page.locator(selector).evaluate(
                    "el => el.scrollWidth <= el.clientWidth + 1"
                ), f"200% text overflow: {selector}"
            scan(page, axe, reports, "200-percent-text-320px")
            page.set_viewport_size({"width": 1280, "height": 900})
            page.reload()
            page.get_by_role("tab", name="Blockers and safety", exact=False).press("Enter")
            expect(page.locator("#regulatory-alerts")).to_be_visible()
            page.get_by_role("tab", name="AI assistance", exact=False).press("Enter")
            page.locator("#chat-panel > summary").click()
            page.locator("#regulatory-chat > summary").click()
            expect(chat.locator(".regulatory-turn")).to_have_count(2)
            expect(chat.locator(":scope > p[role=status]")).to_have_text(
                "Stored synthetic-demo excerpts restored. "
                "These are historical records; ask again for a fresh lookup."
            )
            expect(chat.locator("blockquote")).to_have_text(
                f"[synthetic@v2#0001] {COPY_SOURCE_CANARY}"
            )

            fixture.f.source(version=3)
            page.get_by_role("tab", name="Blockers and safety", exact=False).press("Enter")
            page.get_by_role("button", name="Refresh alerts", exact=True).click()
            expect(alerts).to_contain_text("Not active or source uncertain")
            expect(alerts).to_contain_text("Status: breach risk")
            scan(page, axe, reports, "source-changed-retained-risk")
            page.get_by_role("tab", name="AI assistance", exact=False).press("Enter")
            question.fill("What do the hazard sources say for this home?")
            question.press("Tab")
            page.keyboard.press("Enter")
            expect(chat.locator(".regulatory-turn")).to_have_count(3)
            conflict = chat.locator(".regulatory-turn").last
            expect(conflict).to_contain_text("Lookup status: conflict")
            expect(conflict.locator("blockquote")).to_have_count(2)
            expect(conflict).to_contain_text("Turn sent to Juan Manuel Servera's exercise inbox")
            expect(conflict.locator("button")).to_have_attribute("aria-disabled", "true")
            expect(page.locator("#regulatory-usage")).to_contain_text("1 conflicts")
            inbox = fixture.call("/api/chat/regulatory/inbox", email="exercise-owner@example.test")[
                1
            ]
            assert len(inbox["threads"]) == 2
            scan(page, axe, reports, "conflict-auto-referral")
            page.reload()
            page.locator("#chat-panel > summary").click()
            page.locator("#regulatory-chat > summary").click()
            expect(chat.locator(".regulatory-turn")).to_have_count(3)
            expect(chat.locator(".regulatory-turn").last).to_contain_text(
                "Turn sent to Juan Manuel Servera's exercise inbox"
            )
            scan(page, axe, reports, "conflict-referral-restored")

            # Actual service outage and disabled capability, not fake successful responses.
            law = fixture.app.law
            fixture.app.law = None
            page.get_by_role("tab", name="Blockers and safety", exact=False).press("Enter")
            page.get_by_role("button", name="Refresh alerts", exact=True).click()
            expect(alerts.locator(":scope > p[role=status]")).to_contain_text(
                "Alert coverage unknown"
            )
            expect(alerts.locator(".regulatory-alert")).to_have_count(0)
            fixture.app.law = law
            fixture.app.regulatory.env = {}
            page.get_by_role("tab", name="AI assistance", exact=False).press("Enter")
            page.reload()
            page.locator("#chat-panel > summary").click()
            page.locator("#regulatory-chat > summary").click()
            expect(question).to_be_disabled()
            expect(chat.locator(":scope > p[role=status]")).to_contain_text(
                "Cited lookup unavailable"
            )
            scan(page, axe, reports, "disabled-chat")
            fixture.app.regulatory.env = fixture.app.chat.env

            # Every existing account mapping is checked independently of audience designs.
            for index, (role, text) in enumerate(ROLES.items()):
                context.clear_cookies()
                response = context.request.post(
                    fixture.base + "/api/login",
                    data=dict(email=f"role-{index}@example.test", password="synthetic-local"),
                )
                assert response.ok, role
                open_home(page, fixture.base)
                expect(alerts.locator(".regulatory-guidance")).to_contain_text(text)
                expect(alerts).to_contain_text("For everyone handling data")
                if role == "Building Safety Liaison":
                    expect(alerts.locator(".regulatory-guidance")).to_contain_text(
                        "only an authorised human can make a restart decision "
                        "for stopped retrofit work."
                    )
                if role == "Quality Inspector":
                    expect(alerts.locator(".regulatory-guidance")).to_contain_text(
                        "Licensed PAS 2035 text and contract incorporation are unverified."
                    )
                if role == "Quality Inspector":
                    expect(alerts).to_contain_text("No visible alerts does not mean no risk")
                scan(page, axe, reports, role)
            context.clear_cookies()
            response = context.request.post(
                fixture.base + "/api/login",
                data=dict(email="role-7@example.test", password="synthetic-local"),
            )
            assert response.ok
            page.goto(fixture.base + "/app#/case/ZF-1")
            page.reload()
            expect(page.get_by_role("heading", name="Requirements and doubt route")).to_be_visible()
            expect(page.locator("#regulatory-alerts, #chat-panel")).to_have_count(0)
            scan(page, axe, reports, "supplier-human-route", "#regulatory-supplier")
            assert context.request.get(fixture.base + "/api/law/alerts?case=ZF-1").status == 403
            assert context.request.get(fixture.base + "/api/chat/regulatory/status").status == 403
            assert not errors, errors
            browser.close()
        return dict(
            outcome="passed",
            scope="Synthetic changed surfaces only; not a WCAG conformance certification",
            axe_version="4.10.3",
            axe_sha256=AXE_SHA256,
            axe_status="executed" if axe is not None else "skipped: not supplied",
            scans=reports,
            staff_comprehension="Not run; unmet",
            copy_audit=dict(
                application_owned_labels="chat/alerts and coupled recorded-time labels",
                source_canary=COPY_SOURCE_CANARY,
                source_preserved="exact before and after history restoration",
                human_restart_authority="retained",
                resident_wording_review="Not supplied; unmet",
            ),
        )
    finally:
        fixture.doCleanups()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--axe", type=Path, help="Pinned local axe 4.10.3 script; omit for non-axe checks"
    )
    parser.add_argument("--out", type=Path, required=True, help="Local JSON evidence output")
    args = parser.parse_args()
    result = run(args.axe)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"PASS: {len(result['scans'])} browser states, target sizes, keyboard, reflow, "
        f"roles and real local API; axe {result['axe_status']}"
    )


if __name__ == "__main__":
    main()
