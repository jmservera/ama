"""Synthetic real-server journey, tab, keyboard, axe and actual browser-zoom checks."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from playwright.sync_api import Dialog, Page, Route, expect, sync_playwright

from checks.design_system_browser_check import check, main
from checks.regulatory_ux_check import AXE_SHA256
from checks.workbench_browser_check import synthetic_data


def journey_data() -> dict[str, Any]:
    data = synthetic_data()
    data["cases"][0]["measures"] = "Loft insulation, Solar panels"
    final = copy.deepcopy(data["cases"][0])
    final.update(id="SYN-526-FINAL", stage="Final checks before ordering")
    data["cases"].append(final)
    for case in data["cases"]:
        for document in case.get("documents", []):
            document.setdefault("name", f"{document['id']}.txt")
            document.setdefault("mime", "text/plain")
    return data


def tab(page: Page, name: str) -> None:
    page.get_by_role("tab", name=name, exact=False).click()


def refresh_proposals(page: Page) -> None:
    workspace = page.locator("[data-case-workspace]").element_handle()
    page.get_by_role("button", name="Refresh proposals", exact=True).click()
    page.wait_for_function("old => !old.isConnected", arg=workspace)


def save_quality(page: Page) -> dict[str, Any]:
    for field in page.locator("#quality [data-label]").all():
        field.fill("Submitted current measure evidence")
    page.locator("#q-by").fill("Synthetic installer")
    page.locator("#q-revision").fill("1")
    previous = page.locator("#q-i0").element_handle()
    with page.expect_request("**/api/cases/ZF-1/quality-submit") as request:
        page.get_by_role("button", name="Save evidence", exact=True).click()
    page.wait_for_function("old => !old.isConnected", arg=previous)
    body = request.value.post_data_json
    if not isinstance(body, dict):
        raise AssertionError("Quality request must contain a JSON object")
    page.locator("#q-measure").select_option(body["measure"])
    expect(page.locator("#q-i0")).to_have_value("")
    return body


def sign_in(page: Page, base: str, email: str = "sam@example.test") -> None:
    page.goto(base + "/app#/case/ZF-1?tab=overview")
    page.locator("#email").fill(email)
    page.locator("#pw").fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()
    page.get_by_role("tab", name="Overview", exact=True).wait_for()


def quality_pending_cleanup(page: Page, base: str) -> None:
    for change in ("none", "later", "other-measure", "cache-only", "refusal", "reload-failure"):
        page.goto(base + f"/app?quality-round6={change}#/case/ZF-1?tab=quality")
        page.locator("#q-i0").wait_for()
        original = page.locator("#q-measure").input_value()
        other = next(
            name for name in page.locator("#q-measure option").all_text_contents()
            if name != original
        )
        for field in page.locator("#quality [data-label]").all():
            field.fill("Submitted synthetic quality evidence")
        page.locator("#q-by").fill("Synthetic installer")
        page.locator("#q-revision").fill("1")
        pending: list[Route] = []
        page.route("**/api/cases/ZF-1/quality-submit", lambda route: pending.append(route))
        button = page.locator("[data-quality-save]")
        with page.expect_request("**/api/cases/ZF-1/quality-submit"):
            button.click()
        expect(button).to_be_disabled()
        button.evaluate("el => el.click()")
        check(f"quality duplicate pending submission excluded/{change}", len(pending) == 1)
        if change == "later":
            page.locator("#q-i0").fill("Submitted synthetic quality evidence ")
        page.locator("#q-measure").select_option(other)
        if change == "other-measure":
            page.locator("#q-i0").fill("Unsubmitted other measure evidence")
        loads: list[Route] = []
        if change == "cache-only":
            page.route("**/api/checklists", lambda route: loads.append(route))
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Quality and handover")
            expect(page.locator("#q-i0")).to_have_count(0)
        if change == "reload-failure":
            page.route(
                "**/api/cases/ZF-1",
                lambda route: route.fulfill(status=503, json={"error": "Synthetic reload failure"}),
            )
        before = page.locator("[data-case-workspace]").element_handle()
        pending[0].fulfill(
            status=409 if change == "refusal" else 200,
            json={"error": "Synthetic quality refusal"} if change == "refusal" else {"ok": True},
        )
        page.unroute("**/api/cases/ZF-1/quality-submit")
        if change in ("refusal", "reload-failure"):
            page.locator("#app").get_by_text(
                "Synthetic quality refusal" if change == "refusal"
                else re.compile("Your change was recorded, but the case could not reload")
            ).wait_for()
        else:
            page.wait_for_function("old => !old.isConnected", arg=before)
        if loads:
            page.wait_for_function("() => !document.querySelector('#q-i0')")
            for route in loads:
                route.fulfill(response=route.fetch())
            page.unroute("**/api/checklists")
        if change == "reload-failure":
            expect(button).to_be_disabled()
            button.evaluate("el => el.click()")
            page.unroute("**/api/cases/ZF-1")
        else:
            expect(button).to_be_enabled()
        if change != "refusal":
            expect(page.locator("#q-by")).to_have_value("")
            expect(page.locator("#q-revision")).to_have_value("")
        expected_dirty = change in ("later", "other-measure", "refusal")
        check(
            f"quality semantic success/recovery dirtiness/{change}",
            page.evaluate("hasUnsavedChanges()") == expected_dirty,
        )
        check(
            f"quality actual unload guard/{change}",
            page.evaluate("""() => {
              const event = new Event('beforeunload', {cancelable: true});
              window.dispatchEvent(event); return event.defaultPrevented;
            }""") == expected_dirty,
        )
        if change != "reload-failure":
            page.locator("#q-measure").select_option(original)
            expect(page.locator("#q-i0")).to_have_value(
                "Submitted synthetic quality evidence " if change == "later"
                else "Submitted synthetic quality evidence" if change == "refusal" else ""
            )
            check(f"quality consumed cache cannot resurrect/{change}", True)
        if change == "other-measure":
            page.locator("#q-measure").select_option(other)
            expect(page.locator("#q-i0")).to_have_value("Unsubmitted other measure evidence")
            check("quality retains later other-measure evidence", True)


def quality_outcome_history(
    page: Page, base: str, axe: str, reports: list[dict[str, Any]]
) -> None:
    for status in (409, 503):
        for outcome in ("committed", "uncertain"):
            page.goto(base + f"/app?round7={status}-{outcome}#/case/ZF-1?tab=quality")
            page.locator("#q-i0").wait_for()
            page.locator("#q-i0").fill("Retained outcome evidence")
            page.locator("#q-by").fill("Synthetic installer")
            page.locator("#q-revision").fill("1")
            pending: list[Route] = []
            reads: list[Route] = []
            page.route("**/api/cases/ZF-1/quality-submit", lambda route: pending.append(route))
            button = page.locator("[data-quality-save]")
            button.click()
            expect(button).to_be_disabled()
            page.route("**/api/cases/ZF-1", lambda route: reads.append(route))
            # Start a case read before the outcome, then deliver that old snapshot late.
            tab(page, "AI assistance")
            with page.expect_request("**/api/cases/ZF-1"):
                page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.wait_for_function("() => document.querySelector('[data-quality-save]').disabled")
            with page.expect_response("**/api/cases/ZF-1/quality-submit"):
                pending[0].fulfill(
                    status=status, json={"error": "Synthetic recorded outcome", "outcome": outcome}
                )
            expect(page.locator("#app")).to_contain_text("Refresh and check the history")
            check(f"quality API preserves outcome/{status}/{outcome}", page.evaluate(
                "Boolean(caseSession.historyBarrier)"
            ))
            page.wait_for_function("() => document.querySelector('[data-quality-save]').disabled")
            check(f"quality old read was dispatched/{status}/{outcome}", len(reads) == 1)
            workspace = page.locator("[data-case-workspace]").element_handle()
            with page.expect_response("**/api/cases/ZF-1"):
                old = reads.pop()
                old.fulfill(response=old.fetch())
            tab(page, "Quality and handover")
            expect(button).to_be_disabled()
            check(f"quality pre-outcome read cannot unlock/{status}/{outcome}",
                  workspace is not None and workspace.evaluate("el => el.isConnected"))
            page.locator("#q-measure").select_option(index=1)
            button.evaluate("el => el.click()")
            check(f"quality changed measure cannot resubmit/{status}/{outcome}", len(pending) == 1)
            scan(page, axe, reports, f"quality-history-{status}-{outcome}")
            tab(page, "AI assistance")
            with page.expect_request("**/api/cases/ZF-1"):
                page.get_by_role("button", name="Refresh proposals", exact=True).click()
            check(f"quality recovery read dispatched/{status}/{outcome}", len(reads) == 1)
            reads.pop().fulfill(status=503, json={"error": "Synthetic recovery read failure"})
            expect(page.locator("#app")).to_contain_text("Synthetic recovery")
            tab(page, "Quality and handover")
            expect(button).to_be_disabled()
            page.unroute("**/api/cases/ZF-1")
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Quality and handover")
            expect(button).to_be_enabled()
            page.locator("#q-measure").select_option(index=0)
            expect(page.locator("#q-i0")).to_have_value("Retained outcome evidence")
            check(f"quality authoritative reload recovers/{status}/{outcome}", len(pending) == 1)
            page.unroute("**/api/cases/ZF-1/quality-submit")


def chat_cleanup(page: Page, base: str) -> None:
    usage = {
        "role": "Retrofit Programme Manager",
        "period": "2026-10-29",
        "recorded_turns": 0,
        "outcomes": {"answer": 0, "refused": 0, "conflict": 0},
        "coverage": "recorded_audit_only",
    }

    def admission(route: Route) -> None:
        route.fulfill(
            json={
                "privacy": {"chat": {"status": "simulated", "days": 1}},
                "warning": "Constructed chat lifecycle fixture, not legal approval.",
                "usage": usage,
            }
        )

    def usage_response(route: Route) -> None:
        route.fulfill(json=usage)

    page.route("**/api/chat/regulatory/status", admission)
    page.route("**/api/chat/regulatory/usage", usage_response)
    for regulatory in (False, True):
        prefix = "/api/chat/regulatory" if regulatory else "/api/chat"
        question_id = "#regulatory-question" if regulatory else "#chat-question"
        for change in ("none", "text", "space", "answer-failure", "thread-failure"):
            held: list[Route] = []
            thread_path = f"**{prefix}/threads"
            ask_path = f"**{prefix}/threads/SYN-ROUND5/ask"

            def threads(route: Route) -> None:
                if route.request.method == "GET":
                    route.fulfill(json=[])
                elif change == "thread-failure":
                    held.append(route)
                else:
                    route.fulfill(json={"id": "SYN-ROUND5"})

            def hold(route: Route) -> None:
                held.append(route)

            page.route(thread_path, threads)
            page.route(ask_path, hold)
            page.goto(
                base + f"/app?chat-check={int(regulatory)}-{change}#/case/ZF-1?tab=ai"
            )
            page.locator("#chat-panel > summary").click()
            if regulatory:
                page.locator("#regulatory-chat > summary").click()
            field = page.locator(question_id)
            button = page.get_by_role(
                "button", name="Look up cited sources" if regulatory else "Ask", exact=True
            )
            expect(button).to_be_enabled()
            field.fill("  Synthetic submitted question  ")
            node = field.element_handle()
            with page.expect_request(thread_path if change == "thread-failure" else ask_path):
                button.click()
            expect(button).to_be_disabled()
            if change == "text":
                field.fill("Later question")
            elif change == "space":
                field.fill("  Synthetic submitted question   ")
            tab(page, "Resident")
            page.locator("#outcome").fill("Save during pending chat")
            old = page.locator("[data-case-workspace]").element_handle()
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_function("old => !old.isConnected", arg=old)
            page.locator("#note").fill("Unrelated unsaved note")
            tab(page, "AI assistance")
            expect(field).to_be_visible()
            check(
                f"chat retained pending controls/{regulatory}/{change}",
                field.evaluate("(el, old) => el === old", node) and button.is_disabled(),
            )
            before = len(held)
            field.evaluate("el => el.form.requestSubmit()")
            expect(button).to_be_disabled()
            check(f"pending chat excludes resubmit/{regulatory}/{change}", len(held) == before)
            if change.endswith("failure"):
                held[0].fulfill(status=503, json={"error": "Synthetic question failure"})
            else:
                held[0].fulfill(
                    json={"reply": "Synthetic answer", "kind": "answer", "citations": []}
                )
            expect(button).to_be_enabled()
            expected = (
                ""
                if change == "none"
                else "Later question"
                if change == "text"
                else "  Synthetic submitted question   "
                if change == "space"
                else "  Synthetic submitted question  "
            )
            expect(field).to_have_value(expected)
            check(
                f"chat success/failure raw cleanup/{regulatory}/{change}",
                (field.get_attribute("data-case-dirty") == "true") == (change != "none"),
            )
            tab(page, "Resident")
            expect(page.locator("#note")).to_have_value("Unrelated unsaved note")
            page.locator("#note").fill("")
            page.locator("#note").evaluate("el => el.removeAttribute('data-case-dirty')")
            dirty = page.evaluate("hasUnsavedChanges()")
            check(f"chat cached dirty guard/{regulatory}/{change}", dirty == (change != "none"))
            check(
                f"chat unload guard/{regulatory}/{change}",
                page.evaluate(
                    """() => {
                      const event = new Event('beforeunload', {cancelable: true});
                      window.dispatchEvent(event);
                      return event.defaultPrevented;
                    }"""
                )
                == (change != "none"),
            )
            page.unroute(thread_path, threads)
            page.unroute(ask_path, hold)
    page.unroute("**/api/chat/regulatory/status", admission)
    page.unroute("**/api/chat/regulatory/usage", usage_response)
    page.goto(base + "/app#/case/ZF-1?tab=overview")
    page.get_by_role("tab", name="Overview", exact=True).wait_for()


def mutation_reconstruction(
    page: Page, base: str, axe: str, reports: list[dict[str, Any]]
) -> None:
    for family in ("advance", "resident", "challenge", "challenge-rebuilt"):
        for outcome in (
            "refusal", "committed", "uncertain", "malformed-200", "malformed-409", "malformed-503",
            "reload-failure",
        ):
            case_id = "SYN-526-FINAL" if family == "advance" else "ZF-1"
            case_path = f"**/api/cases/{case_id}"
            snapshot = page.request.get(base + f"/api/cases/{case_id}").json()
            snapshot["challenge_targets"] = [{"proposal_id": "SYN-PENDING", "source": "workflow"}]
            page.route(case_path, lambda route: route.fulfill(json=snapshot))
            page.goto(base + f"/app?round8={family}-{outcome}#/case/{case_id}?tab=overview")
            pending: list[Route] = []
            path = f"**/api/cases/{case_id}/{'advance' if family == 'advance' else 'resident'}"
            page.route(path, lambda route: pending.append(route))
            if family == "advance":
                button = page.get_by_role("button", name="Ready to book the installation")
            else:
                tab(page, "Resident")
                if family == "resident":
                    page.locator("#ru-record-purpose").locator("..").locator("..").locator(
                        "summary"
                    ).click()
                    form = page.locator("#ru-record-purpose").locator("..")
                else:
                    page.locator("#challenge-open").locator("..").locator("summary").click()
                    form = page.locator("#challenge-open")
                form.evaluate("""form => {
                  for (const field of form.querySelectorAll('input, select')) {
                    if (field.tagName === 'SELECT') field.value = [...field.options]
                      .find(option => option.value)?.value || '';
                    else field.value = field.type === 'date' ? '2026-11-01'
                      : field.type === 'datetime-local' ? '2026-11-01T10:00'
                      : field.name === 'proposal_id' ? 'SYN-PENDING' : 'Retained supplied evidence';
                    field.dispatchEvent(new Event('input', {bubbles: true}));
                  }
                }""")
                label = (
                    "Record or reassign update commitment" if family == "resident"
                    else "Record supplied challenge"
                )
                button = form.get_by_role(
                    "button", name=re.compile("^" + re.escape(label) + r"(?: \(loading\))?$")
                )
            with page.expect_request(path):
                button.click()
            page.wait_for_function("() => pendingMutations.size === 1")
            tab(page, "AI assistance")
            refresh_proposals(page)
            if family == "advance":
                tab(page, "Overview")
            else:
                tab(page, "Resident")
                if family == "challenge-rebuilt":
                    # Exercise fresh shipped handlers even when draft retention reused the form.
                    page.evaluate("""snapshot => {
                      const old = document.querySelector('#affected-challenges');
                      const replacement = affectedChallengePanel(snapshot, snapshot.id,
                        () => caseView(snapshot.id));
                      old.replaceWith(replacement);
                      replacement.querySelector('#challenge-open').parentElement.open = true;
                    }""", snapshot)
                    form = page.locator("#challenge-open")
                    form.evaluate("""form => {
                      for (const field of form.querySelectorAll('input, select')) {
                        if (field.tagName === 'SELECT') field.value = [...field.options]
                          .find(option => option.value)?.value || '';
                        else field.value = field.type === 'date' ? '2026-11-01'
                          : field.name === 'proposal_id' ? 'SYN-PENDING' : 'Later evidence';
                        field.dispatchEvent(new Event('input', {bubbles: true}));
                      }
                    }""")
                elif family == "resident":
                    page.locator("#ru-record-purpose").fill("Later changed update purpose")
                else:
                    page.locator("#challenge-open-request").fill("Later evidence")
            if family == "advance":
                button.evaluate("el => el.click()")
                page.wait_for_function("() => document.querySelector('#app').textContent"
                                       ".includes('This action is still pending')")
            else:
                expect(button).to_be_disabled()
                feedback = page.locator(
                    "#ru-record-feedback" if family == "resident" else "#challenge-open-feedback"
                )
                expect(feedback).to_contain_text("Recording the supplied evidence")
            check(f"rebuilt pending entry dispatches once/{family}/{outcome}", len(pending) == 1)
            check(f"pending duplicate is not an outcome barrier/{family}/{outcome}",
                  not page.evaluate("Boolean(caseSession.historyBarrier)"))
            def failed_recovery(route: Route) -> None:
                route.fulfill(status=503, json={"error": "Synthetic raw recovery failed"})

            if outcome == "reload-failure":
                page.route(case_path, failed_recovery)
                pending[0].fulfill(json={"ok": True})
            elif outcome.startswith("malformed"):
                pending[0].fulfill(
                    status=int(outcome.split("-")[1]), content_type="application/json", body="{"
                )
            else:
                pending[0].fulfill(status=409 if outcome == "refusal" else 503, json={
                    "error": "Synthetic mutation result",
                    **({"outcome": outcome} if outcome in ("committed", "uncertain") else {}),
                })
            page.wait_for_function("() => pendingMutations.size === 0")
            page.wait_for_function(
                "expected => Boolean(caseSession.historyBarrier) === expected",
                arg=outcome != "refusal",
            )
            if family != "advance":
                field = page.locator(
                    "#ru-record-purpose" if family == "resident" else "#challenge-open-request"
                )
                expect(field).to_have_value(
                    "Later changed update purpose" if family == "resident" else "Later evidence"
                )
                expect(feedback).to_contain_text(
                    "Synthetic mutation result" if outcome == "refusal"
                    else "Reload and check the history"
                )
                if outcome != "refusal":
                    expect(button).to_be_disabled()
            if outcome == "refusal":
                with page.expect_request(path):
                    button.evaluate("el => el.click()")
                page.wait_for_function("() => pendingMutations.size === 1")
                check(f"explicit refusal remains retryable/{family}", len(pending) == 2)
                pending[1].fulfill(status=409, json={"error": "Synthetic retry refusal"})
                page.wait_for_function("() => pendingMutations.size === 0")
            else:
                button.evaluate("el => el.click()")
                check(f"unconfirmed outcome blocks repeats/{family}/{outcome}", len(pending) == 1)
            scan(page, axe, reports, f"rebuilt-mutation-{family}-{outcome}")
            if family != "advance" and outcome != "refusal":
                if outcome != "reload-failure":
                    page.route(case_path, failed_recovery)
                tab(page, "AI assistance")
                with page.expect_response(case_path):
                    page.get_by_role("button", name="Refresh proposals", exact=True).click()
                tab(page, "Resident")
                expect(button).to_be_disabled()
                page.unroute(case_path, failed_recovery)
                tab(page, "AI assistance")
                refresh_proposals(page)
                tab(page, "Resident")
                expect(field).to_have_value(
                    "Later changed update purpose" if family == "resident" else "Later evidence"
                )
                if family == "challenge" and outcome == "reload-failure":
                    expect(button).to_be_disabled()
                    expect(feedback).to_contain_text("Only the submitted values were recorded")
                    button.evaluate("el => el.click()")
                    check("acknowledged challenge draft never repeats its submitted action",
                          len(pending) == 1)
                    page.unroute(path)
                    page.unroute(case_path)
                    continue
                expect(feedback).to_contain_text("Case history reloaded")
                expect(button).to_be_enabled()
                with page.expect_request(path):
                    button.click()
                page.wait_for_function("() => pendingMutations.size === 1")
                check(f"fresh history permits retained draft retry/{family}/{outcome}",
                      len(pending) == 2)
                pending[1].fulfill(status=409, json={"error": "Synthetic corrected retry refusal"})
                expect(button).to_be_enabled()
                scan(page, axe, reports, f"raw-history-recovered-{family}-{outcome}")
            page.unroute(path)
            page.unroute(case_path)
    page.goto(base + "/app#/case/ZF-1?tab=overview")
    page.get_by_role("tab", name="Overview", exact=True).wait_for()


def scan(page: Page, axe: str, reports: list[dict[str, Any]], state: str) -> None:
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async () => await axe.run(document.querySelector('main'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a',
            'wcag21aa', 'wcag22aa']}})"""
    )
    serious = [item for item in result["violations"] if item["impact"] in ("serious", "critical")]
    reports.append(
        dict(
            state=state,
            violations=result["violations"],
            incomplete=result["incomplete"],
            passes=len(result["passes"]),
        )
    )
    check(f"axe no serious/critical: {state}", not serious)


def run_browser(base: str, axe: str, out: Path) -> None:
    reports: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        context.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(base + "/") else route.abort()
            ),
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def accept_dialog(dialog: Dialog) -> None:
            dialog.accept()

        page.on("dialog", accept_dialog)
        try:
            sign_in(page, base)
            page.wait_for_function(
                "() => !document.querySelector('[data-case-ai-summary]')"
                ".textContent.includes('Loading assistance')"
            )
            check(
                "one h1 and six ordered journey items",
                page.locator("main h1").count() == 1 and page.locator(".stepper > li").count() == 6,
            )
            check(
                "one current step and all steps navigate",
                page.locator('.stepper [aria-current="step"]').count() == 1
                and page.locator(".stepper a[href]").count() == 6,
            )
            summary_bottom = page.locator(".case-summary").evaluate(
                "el => el.getBoundingClientRect().bottom"
            )
            check(f"all summary values fit 1280x800 ({summary_bottom})", summary_bottom <= 800)
            check("all six summary values", page.locator(".case-summary dt").count() == 6)
            page.screenshot(path=str(out / "desktop-1280.png"))
            quality_pending_cleanup(page, base)
            quality_outcome_history(page, base, axe, reports)
            chat_cleanup(page, base)
            mutation_reconstruction(page, base, axe, reports)
            check(
                "nine tabs, one selected and one tab stop",
                page.get_by_role("tab").count() == 9
                and page.locator("[role=tab][aria-selected=true]").count() == 1
                and page.locator('[role=tab][tabindex="0"]').count() == 1,
            )
            first = page.get_by_role("tab", name="Overview", exact=True)
            first.focus()
            first.press("ArrowRight")
            check(
                "arrows focus without activation",
                page.locator(":focus").get_attribute("id") == "case-tab-blockers"
                and first.get_attribute("aria-selected") == "true",
            )
            page.keyboard.press("Enter")
            page.wait_for_url("**?tab=blockers")
            check("Enter activates focused tab", "tab=blockers" in page.url)
            page.keyboard.press("End")
            page.keyboard.press("Space")
            page.wait_for_url("**?tab=history")
            check("End and Space activate History", "tab=history" in page.url)
            page.keyboard.press("Home")
            page.keyboard.press("Enter")
            page.get_by_role("button", name="Open next action", exact=True).focus()
            page.keyboard.press("Enter")
            check(
                "summary jump focuses panel heading",
                page.locator(":focus").evaluate(
                    "el => el.tagName === 'H2' && !el.closest('[hidden]')"
                ),
            )
            paged_case = page.request.get(base + "/api/cases/ZF-1").json()
            paged_case["challenge_targets"] = [
                {"proposal_id": f"SYN-JOURNEY-{index}", "source": "workflow"}
                for index in range(101)
            ]

            def paged_history(route: Route) -> None:
                route.fulfill(json=paged_case)

            page.route("**/api/cases/ZF-1", paged_history)
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Resident")
            page.locator("#outcome").fill("Retained pagination draft")
            workspace = page.locator("[data-case-workspace]").element_handle()
            page.get_by_role("button", name="Older suggestions", exact=True).click()
            check(
                "in-place pagination synchronizes every native journey destination",
                page.locator(".stepper a").evaluate_all(
                    """links => links.every(link => new URLSearchParams(
                      link.hash.split('?')[1]).get('challenge-target-history') === '1')"""
                ),
            )
            dialogs: list[str] = []

            def cancel_leave(dialog: Dialog) -> None:
                dialogs.append(dialog.message)
                dialog.dismiss()

            page.remove_listener("dialog", accept_dialog)
            page.on("dialog", cancel_leave)
            page.locator(".stepper a[data-case-tab=funding]").click()
            page.wait_for_function(
                "() => document.querySelector('#case-tab-funding')"
                ".getAttribute('aria-selected') === 'true'"
            )
            check(
                "journey changes retained sections after pagination without discarding",
                not dialogs
                and "challenge-target-history=1" in page.url
                and page.locator("[data-case-workspace]").evaluate(
                    "(el, old) => el === old", workspace
                )
                and page.locator("#outcome").input_value() == "Retained pagination draft",
            )
            page.remove_listener("dialog", cancel_leave)
            page.on("dialog", accept_dialog)
            page.go_back()
            expect(page.locator("#case-tab-resident")).to_have_attribute("aria-selected", "true")
            page.go_forward()
            expect(page.locator("#case-tab-funding")).to_have_attribute("aria-selected", "true")
            page.unroute("**/api/cases/ZF-1", paged_history)
            tab(page, "Resident")
            page.locator("#outcome").fill("Unsaved synthetic call")
            page.get_by_role("button", name="Plain visit template", exact=True).click()
            page.get_by_role("textbox", name="Draft message", exact=True).fill("Edited template")
            original = page.locator("#resident-draft-output").element_handle()
            tab(page, "AI assistance")
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.get_by_role("tab", name="AI assistance").wait_for()
            tab(page, "Resident")
            check(
                "unrelated refresh preserves call and complete dynamic draft",
                page.locator("#outcome").input_value() == "Unsaved synthetic call"
                and page.get_by_role("textbox", name="Draft message", exact=True).input_value()
                == "Edited template"
                and page.locator("#resident-draft-output").evaluate(
                    "(el, old) => el === old", original
                ),
            )
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_function("() => document.querySelector('#outcome').value === ''")
            check(
                "successful call clears itself, not unrelated draft",
                page.get_by_role("textbox", name="Draft message", exact=True).input_value()
                == "Edited template",
            )
            tab(page, "History")
            check(
                "saved call reaches actual history",
                "Unsaved synthetic call" in page.locator("#case-panel-history").inner_text(),
            )
            finance_context = browser.new_context(viewport={"width": 1280, "height": 800})
            finance_context.route(
                "**/*",
                lambda route: (
                    route.continue_() if route.request.url.startswith(base + "/") else route.abort()
                ),
            )
            finance = finance_context.new_page()
            finance.on("pageerror", lambda error: errors.append(str(error)))
            sign_in(finance, base, "pam@example.test")
            tab(finance, "Funding")
            budget = finance.locator("details").filter(
                has=finance.get_by_text("Propose a budget", exact=True)
            )
            commitment = finance.locator("details").filter(
                has=finance.get_by_text("Raise a commitment", exact=True)
            )
            budget.locator("summary").click()
            budget.get_by_label("Amount in pounds", exact=True).fill("321")
            commitment.locator("summary").click()
            commitment.get_by_label("Supplier", exact=True).fill("Synthetic supplier")
            finance.route(
                "**/api/cases/ZF-1/finance",
                lambda route: route.fulfill(status=409, json={"error": "Synthetic conflict"}),
            )
            commitment.get_by_role("button", name="Raise commitment", exact=True).click()
            finance.get_by_text("Synthetic conflict", exact=True).wait_for()
            check(
                "failed action preserves submitted and adjacent drafts",
                budget.get_by_label("Amount in pounds", exact=True).input_value() == "321"
                and commitment.get_by_label("Supplier", exact=True).input_value()
                == "Synthetic supplier",
            )
            finance.unroute("**/api/cases/ZF-1/finance")
            finance.route(
                "**/api/cases/ZF-1/finance",
                lambda route: route.fulfill(status=200, json={"ok": True}),
            )
            commitment.get_by_role("button", name="Raise commitment", exact=True).click()
            finance.wait_for_function(
                "() => document.querySelector('[id=\"f-Raise a commitment-supplier\"]').value"
                " === ''"
            )
            check(
                "client success clears only explicitly submitted same-card fields",
                budget.get_by_label("Amount in pounds", exact=True).input_value() == "321",
            )
            # Keep mutations pending while a person continues editing their forms.
            tab(finance, "Resident")
            finance.get_by_text("Open a request or complaint", exact=True).click()
            finance.locator("#request-open-summary").fill("Dispatched complaint")
            pending_resident: list[Route] = []
            finance.route(
                "**/api/cases/ZF-1/resident", lambda route: pending_resident.append(route)
            )
            finance.get_by_role("button", name="Open", exact=True).click()
            finance.wait_for_function(
                "() => document.querySelector('#request-open-feedback').textContent"
                ".includes('Recording the supplied evidence')"
            )
            finance.locator("#request-open-summary").fill("Later complaint edit")
            resident_body = pending_resident[0].request.post_data_json
            check(
                "resident request uses dispatch-time text",
                isinstance(resident_body, dict)
                and resident_body["summary"] == "Dispatched complaint",
            )
            pending_resident[0].fulfill(json={"ok": True})
            finance.unroute("**/api/cases/ZF-1/resident")
            expect(finance.locator("#request-open-summary")).to_have_value("Later complaint edit")
            finance.wait_for_function(
                "() => document.querySelector('#request-open-summary')"
                ".dataset.caseDirty === 'true'"
                " && document.querySelector('#request-open-feedback').textContent"
                ".includes('Supplied evidence recorded')"
            )
            check("resident mutation preserves later dirty edits", True)

            tab(finance, "Quality and handover")
            finance.locator("#ho-to").select_option("coordinator@example.test")
            finance.locator("#ho-note").fill("Dispatched handoff")
            finance.locator("#ho-next").fill("Review synthetic evidence")
            finance.locator("#ho-offer-source").fill("Synthetic handoff source")
            finance.locator("#ho-offer-source_version").fill("1")
            finance.locator("#ho-offer-reason").fill("Synthetic dispatch regression")
            pending_handoff: list[Route] = []
            finance.route(
                "**/api/cases/ZF-1/offer-handoff", lambda route: pending_handoff.append(route)
            )
            finance.get_by_role("button", name="Offer the case", exact=True).click()
            finance.locator("#ho-note").fill("Later handoff edit")
            finance.locator("#ho-offer-reason").fill("Later handoff reason")
            handoff_body = pending_handoff[0].request.post_data_json
            check(
                "handoff request uses dispatch-time text",
                isinstance(handoff_body, dict) and handoff_body["note"] == "Dispatched handoff",
            )
            handoff_response = pending_handoff[0].fetch()
            if handoff_response.status != 200:
                raise AssertionError(f"Actual handoff failed: {handoff_response.text()}")
            check("actual synthetic handoff mutation succeeds", True)
            pending_handoff[0].fulfill(response=handoff_response)
            finance.unroute("**/api/cases/ZF-1/offer-handoff")
            expect(finance.get_by_label("Earlier note", exact=True)).to_have_value(
                "Later handoff edit"
            )
            check(
                "removed handoff form preserves later dirty edits copyably",
                finance.get_by_label("Earlier reason", exact=True).input_value()
                == "Later handoff reason"
                and finance.get_by_label("Earlier note", exact=True).get_attribute(
                    "data-case-dirty"
                )
                == "true",
            )

            tab(finance, "Funding")
            draft = finance.get_by_label("Funding application draft", exact=True)
            before_funding = draft.element_handle()
            with finance.expect_response("**/api/cases/ZF-1/funding-draft") as first_funding:
                finance.get_by_role("button", name="Draft application with AI", exact=True).click()
            if first_funding.value.status != 200:
                raise AssertionError(f"Funding fixture failed: {first_funding.value.text()}")
            finance.wait_for_function("old => !old.isConnected", arg=before_funding)
            first_record = finance.locator("#case-panel-funding [data-record-id]").get_attribute(
                "data-record-id"
            )
            check("first funding draft has an AI record identity", bool(first_record))
            draft.fill("Earlier unsent funding wording")
            finance.route(
                "**/api/cases/ZF-1/funding-draft",
                lambda route: route.fulfill(
                    json={
                        "ai": {
                            "record_id": "SYN-FUNDING-NEW",
                            "approval": "Not reviewed",
                            "label": "Synthetic AI draft",
                            "text": "Fresh synthetic AI wording",
                        }
                    }
                ),
            )

            def fresh_funding(route: Route) -> None:
                response = route.fetch()
                case = response.json()
                case["funding"]["draft"] = "Fresh synthetic AI wording"
                route.fulfill(response=response, json=case)

            finance.route("**/api/cases/ZF-1", fresh_funding)
            finance.get_by_role("button", name="Draft application with AI", exact=True).click()
            expect(draft).to_have_value("Fresh synthetic AI wording")
            earlier = finance.get_by_label("Earlier Funding application draft", exact=True)
            expect(earlier).to_have_value("Earlier unsent funding wording")
            check(
                "new funding record never inherits earlier text",
                draft.get_attribute("data-case-dirty") is None
                and finance.locator("#case-panel-funding [data-record-id]").get_attribute(
                    "data-record-id"
                )
                == "SYN-FUNDING-NEW",
            )
            tab(finance, "AI assistance")
            refresh_proposals(finance)
            tab(finance, "Funding")
            expect(earlier).to_have_value("Earlier unsent funding wording")
            expect(draft).to_have_value("Fresh synthetic AI wording")
            check("earlier funding edits survive subsequent refresh separately", True)
            expect(finance.get_by_label("Earlier note", exact=True)).to_have_value(
                "Later handoff edit"
            )
            check("removed form drafts also survive subsequent refresh", True)
            finance.locator("#case-panel-funding").get_by_role(
                "button", name="Discard earlier review edits", exact=True
            ).click()
            finance.unroute("**/api/cases/ZF-1", fresh_funding)
            finance.unroute("**/api/cases/ZF-1/funding-draft")
            finance_context.close()
            tab(page, "Survey and assessment")
            page.get_by_label("Choose a file", exact=True).set_input_files(
                {
                    "name": "constructed-review.txt",
                    "mimeType": "text/plain",
                    "buffer": b"Constructed journey review fixture. No resident data.",
                }
            )
            page.locator("#doc-upload-source").fill("Constructed browser fixture")
            page.locator("#doc-upload-source_version").fill("1")
            page.locator("#doc-upload-reason").fill("Verify document review counts")
            pending_upload: list[Route] = []
            page.route("**/api/cases/ZF-1/upload", lambda route: pending_upload.append(route))
            with page.expect_request("**/api/cases/ZF-1/upload"):
                page.get_by_role("button", name="Add document", exact=True).click()
            page.locator("#doc-upload-reason").fill("Later upload edit")
            page.get_by_label("Type of document", exact=True).select_option("Survey")
            page.get_by_label("Choose a file", exact=True).set_input_files(
                {"name": "later-selection.txt", "mimeType": "text/plain", "buffer": b"Later file"}
            )
            upload_body = pending_upload[0].request.post_data_json
            check(
                "upload captures immutable metadata and document kind",
                isinstance(upload_body, dict)
                and upload_body["reason"] == "Verify document review counts"
                and upload_body["kind"] == "EPC",
            )
            response = pending_upload[0].fetch()
            if response.status != 200:
                raise AssertionError(f"Constructed upload failed: {response.text()}")
            pending_upload[0].fulfill(response=response)
            page.unroute("**/api/cases/ZF-1/upload")
            page.get_by_role("link", name="constructed-review.txt", exact=True).wait_for()
            check(
                "upload preserves edits typed during mutation",
                page.locator("#doc-upload-reason").input_value() == "Later upload edit"
                and page.locator("#doc-upload-reason").get_attribute("data-case-dirty") == "true"
                and page.get_by_label("Type of document", exact=True).input_value() == "Survey",
            )
            check(
                "upload retains a file selected after dispatch",
                page.get_by_label("Choose a file", exact=True).evaluate(
                    "el => el.files[0]?.name === 'later-selection.txt'"
                ),
            )
            with page.expect_response("**/api/cases/ZF-1/read-doc") as document_response:
                page.get_by_role("button", name="Read with AI", exact=True).last.click()
            if document_response.value.status != 200:
                raise AssertionError(f"Document read failed: {document_response.value.text()}")
            page.locator("#case-panel-survey .aimeta").wait_for()
            local_count = page.locator("[data-case-ai-summary]").inner_text()
            tab_count = page.get_by_role("tab", name="AI assistance").inner_text()
            check(
                f"document review updates summary and tab ({local_count}; {tab_count})",
                (
                    "1 AI suggestions waiting" in local_count
                    or "1 local drafts to review" in local_count
                )
                and ("1 to review" in tab_count or "1 local drafts to review" in tab_count),
            )
            document_review = page.locator("#case-panel-survey .aimeta")
            document_review.get_by_role("button", name="Edit this draft", exact=True).click()
            document_review.get_by_label("Edited draft", exact=True).fill(
                "Reviewed replacement synthetic document text"
            )
            document_review.get_by_label("Reason", exact=True).fill("Checked document wording")
            original_document = document_review.element_handle()
            tab(page, "Resident")
            page.locator("#outcome").fill("Call with pending document review")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator("#outcome")).to_have_value("")
            tab(page, "AI assistance")
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            tab(page, "Survey and assessment")
            expect(document_review.get_by_label("Edited draft", exact=True)).to_have_value(
                "Reviewed replacement synthetic document text"
            )
            expect(document_review.get_by_label("Reason", exact=True)).to_have_value(
                "Checked document wording"
            )
            check(
                "document review retains record, handlers and edits across call and refresh",
                document_review.evaluate("(el, old) => el === old", original_document),
            )
            # The call changes source hashes. A new review must use fresh evidence.
            with page.expect_response("**/api/cases/ZF-1/read-doc"):
                page.get_by_role("button", name="Read with AI", exact=True).last.click()
            document_review.get_by_role("button", name="Edit this draft", exact=True).click()
            document_review.get_by_label("Edited draft", exact=True).fill(
                "Reviewed replacement synthetic document text"
            )
            document_review.get_by_label("Reason", exact=True).fill("Checked document wording")
            pending_review: list[Route] = []
            page.route("**/api/ai/review/*/edit", lambda route: pending_review.append(route))
            with page.expect_request("**/api/ai/review/*/edit"):
                document_review.get_by_role(
                    "button", name="Save edited draft review", exact=True
                ).click()
            document_review.get_by_label("Edited draft", exact=True).fill(
                "Later unsubmitted document text"
            )
            document_review.get_by_label("Reason", exact=True).fill("Later unsubmitted reason")
            review_body = pending_review[0].request.post_data_json
            check(
                "document review dispatch retains immutable text and reason",
                isinstance(review_body, dict)
                and review_body["text"] == "Reviewed replacement synthetic document text"
                and review_body["reason"] == "Checked document wording",
            )
            response = pending_review[0].fetch()
            if response.status != 200:
                raise AssertionError(f"Document edit failed: {response.text()}")
            pending_review[0].fulfill(response=response)
            page.unroute("**/api/ai/review/*/edit")
            page.wait_for_function(
                "() => document.querySelector('#case-panel-survey .aimeta')"
                ".dataset.reviewState === 'Edited'"
            )
            check(
                "edited document displays submitted replacement read-only",
                page.locator("[data-document-text]").inner_text()
                == "Reviewed replacement synthetic document text"
                and page.locator("[data-document-text]").get_attribute("aria-label")
                == "Reviewed replacement document text",
            )
            record_id = document_review.get_attribute("data-record-id")
            expect(document_review.locator("legend")).to_have_text(
                f"Unsubmitted edits for reviewed record {record_id}"
            )
            check(
                "later document values stay copyable, dirty and cannot review again",
                document_review.get_by_label("Edited draft", exact=True).input_value()
                == "Later unsubmitted document text"
                and document_review.get_by_label("Reason", exact=True).input_value()
                == "Later unsubmitted reason"
                and document_review.locator('[data-case-dirty="true"][readonly]').count() == 2
                and document_review.locator("button:not([disabled])").count() == 0,
            )
            tab(page, "Resident")
            page.locator("#outcome").fill("Refresh reviewed document recovery")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator("#outcome")).to_have_value("")
            tab(page, "Survey and assessment")
            expect(document_review.get_by_label("Edited draft", exact=True)).to_have_value(
                "Later unsubmitted document text"
            )
            expect(document_review.get_by_label("Reason", exact=True)).to_have_value(
                "Later unsubmitted reason"
            )
            check("reviewed document recovery survives case refresh with record identity", True)
            page.remove_listener("dialog", accept_dialog)
            page.on("dialog", cancel_leave)
            page.get_by_role("button", name="Read with AI", exact=True).last.click()
            check(
                "replacing recovered document edits requires explicit discard",
                len(dialogs) == 1
                and "Replace this draft" in dialogs[0]
                and document_review.get_by_label("Edited draft", exact=True).input_value()
                == "Later unsubmitted document text",
            )
            page.remove_listener("dialog", cancel_leave)
            page.on("dialog", accept_dialog)
            check(
                "document review removes count without approving the case",
                "local drafts to review" not in page.locator("[data-case-ai-summary]").inner_text()
                and "1 AI suggestions waiting"
                not in page.locator("[data-case-ai-summary]").inner_text()
                and "1 local drafts to review"
                not in page.get_by_role("tab", name="AI assistance").inner_text(),
            )
            tab(page, "Quality and handover")
            page.locator("#q-i0").wait_for()
            page.locator("#q-i0").fill("Unsubmitted checklist evidence")
            original_measure = page.locator("#q-measure").input_value()
            pending_checklists: list[Route] = []
            page.route("**/api/checklists", lambda route: pending_checklists.append(route))
            tab(page, "Resident")
            page.locator("#outcome").fill("Call with pending checklist evidence")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator("#outcome")).to_have_value("")
            tab(page, "Quality and handover")
            check(
                "checklist restoration waits for construction", page.locator("#q-i0").count() == 0
            )
            pending_checklists[0].fulfill(response=pending_checklists[0].fetch())
            page.unroute("**/api/checklists")
            expect(page.locator("#q-i0")).to_have_value("Unsubmitted checklist evidence")
            check(
                "async checklist restores matching measure and version",
                page.locator("#q-measure").input_value() == original_measure
                and page.locator("#q-i0").get_attribute("data-case-dirty") == "true",
            )
            scan(page, axe, reports, "restored-quality-evidence")
            choices = page.locator("#q-measure option").all_text_contents()
            other = next(name for name in choices if name != original_measure)
            page.locator("#q-measure").select_option(other)
            expect(page.locator("#q-i0")).to_have_value("")
            page.locator("#q-i0").fill("Other measure evidence")
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Quality and handover")
            expect(page.locator("#q-i0")).to_have_value("Other measure evidence")
            earlier_a = (
                page.locator("#quality details > div")
                .filter(has_text=original_measure)
                .get_by_label("Earlier checklist-evidence", exact=True)
            )
            expect(earlier_a).to_have_value("Unsubmitted checklist evidence")
            page.locator("#q-measure").select_option(original_measure)
            expect(page.locator("#q-i0")).to_have_value("Unsubmitted checklist evidence")
            expect(earlier_a).to_have_count(0)
            page.locator("#q-i0").fill("Newer evidence after returning to recovered measure")
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Quality and handover")
            expect(page.locator("#q-i0")).to_have_value(
                "Newer evidence after returning to recovered measure"
            )
            check("recovered measure never overwrites newer live evidence", True)
            check("checklist evidence stays bound to its measure", True)
            page.locator("#q-measure").select_option(other)
            page.route(
                "**/api/cases/ZF-1/quality-submit",
                lambda route: route.fulfill(json={"ok": True}),
            )
            quality_body = save_quality(page)
            check(
                "quality cleanup covers only evidence present in the request",
                quality_body["measure"] == other
                and all(
                    text == "Submitted current measure evidence"
                    for text in quality_body["items"].values()
                ),
            )
            expect(earlier_a).to_have_value("Newer evidence after returning to recovered measure")
            check(
                "successful other-measure save leaves recovery dirty",
                earlier_a.get_attribute("data-case-dirty") == "true",
            )
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Quality and handover")
            expect(earlier_a).to_have_value("Newer evidence after returning to recovered measure")
            check("other-measure recovery survives save and further refresh", True)

            page.locator("#q-i0").fill("Unsent prior-version evidence")
            changed_lists = page.request.get(base + "/api/checklists").json()
            for checklist in changed_lists.values():
                checklist["version"] += "-synthetic-replacement"
            page.route("**/api/checklists", lambda route: route.fulfill(json=changed_lists))
            tab(page, "AI assistance")
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            tab(page, "Quality and handover")
            expect(page.locator("#q-i0")).to_have_value("")
            earlier_b = (
                page.locator("#quality details > div")
                .filter(has_text=other)
                .get_by_label("Earlier checklist-evidence", exact=True)
            )
            expect(earlier_b).to_have_value("Unsent prior-version evidence")
            check("changed checklist version keeps old evidence separately", True)
            save_quality(page)
            expect(earlier_b).to_have_value("Unsent prior-version evidence")
            check(
                "successful current-version save leaves prior-version recovery dirty",
                earlier_b.get_attribute("data-case-dirty") == "true",
            )
            tab(page, "AI assistance")
            refresh_proposals(page)
            tab(page, "Quality and handover")
            expect(earlier_b).to_have_value("Unsent prior-version evidence")
            check("prior-version recovery survives save and further refresh", True)
            page.unroute("**/api/cases/ZF-1/quality-submit")
            page.unroute("**/api/checklists")
            tab(page, "Resident")
            with page.expect_response("**/api/cases/ZF-1/ai") as draft_response:
                page.get_by_role("button", name="Draft with AI", exact=True).click()
            if draft_response.value.status != 200:
                raise AssertionError(f"Draft API failed: {draft_response.value.text()}")
            page.wait_for_function(
                "() => !document.querySelector('#resident-draft-output')"
                ".textContent.includes('Working on it')"
            )
            if page.locator("#resident-draft-output .err").count():
                raise AssertionError(page.locator("#resident-draft-output").inner_text())
            page.get_by_role("textbox", name="Draft", exact=True).wait_for()
            card = page.locator("#resident-draft-output .ai-suggestion")
            draft_label = (
                "AI suggestion, not approved" if draft_response.value.json()["source"] == "ai"
                else "Template draft, not approved"
            )
            check(
                "AI card exact warning and missing confidence",
                f"{draft_label}. Not an instruction." in card.inner_text()
                and "Confidence: not provided" in card.inner_text(),
            )
            record = card.get_attribute("data-record-id")
            page.get_by_role("textbox", name="Draft", exact=True).fill("Edited synthetic wording")
            card.get_by_role("button", name="Edit this draft", exact=True).focus()
            page.keyboard.press("Enter")
            card.get_by_role("button", name="Save edited draft review", exact=True).focus()
            page.keyboard.press("Enter")
            check(
                "edit requires linked reason",
                card.get_by_label("Reason", exact=True).get_attribute("aria-invalid") == "true",
            )
            card.get_by_label("Reason", exact=True).fill("Checked wording")
            tab(page, "AI assistance")
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.get_by_role("tab", name="AI assistance").wait_for()
            tab(page, "Resident")
            check(
                "AI record and review context survive refresh",
                card.get_attribute("data-record-id") == record
                and card.get_by_label("Reason", exact=True).input_value() == "Checked wording"
                and page.get_by_role("textbox", name="Draft", exact=True).input_value()
                == "Edited synthetic wording",
            )
            card.get_by_role("button", name="Save edited draft review", exact=True).focus()
            page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.querySelector('#resident-draft-output .aimeta')"
                ".dataset.reviewState === 'Edited'"
            )
            check(
                "recorded edit keeps approval boundary",
                "not an approval, consent or safety" in card.inner_text(),
            )
            for action, reviewed in (
                ("Use this draft", "Accepted"), ("Do not use this draft", "Rejected")
            ):
                page.get_by_role("button", name="Draft with AI", exact=True).focus()
                with page.expect_response("**/api/cases/ZF-1/ai"):
                    page.keyboard.press("Enter")
                card = page.locator("#resident-draft-output .ai-suggestion")
                card.get_by_role("button", name=action, exact=True).wait_for()
                if reviewed == "Rejected":
                    card.get_by_role("button", name=action, exact=True).focus()
                    page.keyboard.press("Enter")
                    card.get_by_role("button", name="Record rejection", exact=True).focus()
                    page.keyboard.press("Enter")
                    check(
                        "keyboard reject focuses required reason",
                        card.get_by_label("Reason", exact=True).evaluate(
                            "el => el === document.activeElement"
                            " && el.getAttribute('aria-invalid') === 'true'"
                        ),
                    )
                    page.keyboard.type("Checked synthetic rejection")
                card.get_by_role(
                    "button", name="Record rejection" if reviewed == "Rejected" else action,
                    exact=True
                ).focus()
                page.keyboard.press("Enter")
                page.wait_for_function(
                    "state => document.querySelector('#resident-draft-output .aimeta')"
                    ".dataset.reviewState === state",
                    arg=reviewed,
                )
                check(
                    f"keyboard {action.lower()} records draft-only review",
                    "not an approval, consent or safety" in card.inner_text(),
                )
            tab(page, "Overview")
            page.reload()
            page.get_by_role("tab", name="Overview", exact=True).wait_for()
            check("tab URL survives document refresh", "tab=overview" in page.url)
            tab(page, "Funding")
            tab(page, "History")
            page.go_back()
            page.get_by_role("tabpanel", name="Funding", exact=True).wait_for()
            check("browser Back restores retained tab", True)

            held: list[Route] = []
            page.route("**/api/cases/ZF-1", lambda route: held.append(route))
            page.reload(wait_until="domcontentloaded")
            page.locator('[aria-label="Case summary"][aria-busy=true]').wait_for()
            check(
                "loading case has explicit busy state and no tabs",
                page.get_by_role("tab").count() == 0,
            )
            scan(page, axe, reports, "loading")
            response = page.request.get(base + "/api/cases/ZF-1")
            held[0].fulfill(response=response)
            page.unroute("**/api/cases/ZF-1")
            page.get_by_role("tab", name="Funding", exact=True).wait_for()

            def proposal(index: int, ready: bool = False) -> dict[str, Any]:
                return dict(
                    id=f"SYN-{index}",
                    case_id="ZF-1",
                    capability="assessment-preparation",
                    version="1",
                    display_state="ready" if ready else "queued",
                    state="ready" if ready else "queued",
                    stale=False,
                    manual="Manual route.",
                    attempts=0,
                    provenance=[],
                    snapshot={},
                    envelope={},
                    history_next_offset=None,
                    output=dict(summary="Synthetic cited output", findings=[], unknowns=[])
                    if ready
                    else None,
                )

            held_queue: list[Route] = []

            def pages(route: Route) -> None:
                if "after=" in route.request.url:
                    route.fulfill(json={"proposals": [proposal(51, True)], "next_after": None})
                else:
                    held_queue.append(route)

            page.route(
                "**/api/assistants",
                lambda route: route.fulfill(
                    json={
                        "assistants": [],
                        "disabled": None,
                        "proactive": False,
                    }
                ),
            )
            page.route("**/api/assistants/proposals?**", pages)
            page.reload()
            count_live = page.locator("[data-case-ai-count]")
            expect(count_live).to_have_attribute("role", "status")
            expect(count_live).to_have_attribute("aria-live", "polite")
            expect(count_live).to_have_attribute("aria-atomic", "true")
            expect(count_live).to_contain_text("loading")
            expect(count_live.locator("button")).to_have_count(0)
            tab(page, "Resident")
            page.locator("#outcome").fill("Retain while assistance is loading")
            call_node = page.locator("#outcome").element_handle()
            tab(page, "Overview")
            expect(page.locator("#case-panel-ai")).to_be_hidden()
            held_queue[0].fulfill(
                json={
                    "proposals": [proposal(index) for index in range(50)],
                    "next_after": "page-two",
                }
            )
            page.wait_for_function(
                "() => document.querySelector('#case-tab-ai').textContent.includes('(1 to review)')"
            )
            check(
                "full cursor count includes output beyond first 50",
                page.locator("article.ai-suggestion").count() == 51
                and "1 AI suggestions waiting"
                in page.locator("[data-case-ai-summary]").inner_text(),
            )
            check(
                "hidden AI tab count is announced by the visible summary",
                count_live.is_visible() and "1 AI suggestions waiting" in count_live.inner_text(),
            )
            check(
                "unchanged count events do not repeat live mutations",
                page.evaluate(
                    """async () => {
                      const count = document.querySelector('[data-case-ai-count]');
                      let updates = 0;
                      const observer = new MutationObserver(rows => updates += rows.length);
                      observer.observe(count, {
                        childList: true, subtree: true, characterData: true});
                      caseSession.controller.counts();
                      app.dispatchEvent(new Event('ai-review-change'));
                      await new Promise(resolve => setTimeout(resolve, 0));
                      observer.disconnect();
                      return updates === 0;
                    }"""
                ),
            )
            tab(page, "Resident")
            check(
                "tab-only navigation preserves DOM and pending work",
                page.locator("#outcome").evaluate("(el, old) => el === old", call_node)
                and page.locator("#outcome").input_value() == "Retain while assistance is loading",
            )
            page.unroute("**/api/assistants/proposals?**", pages)
            page.unroute("**/api/assistants")
            page.reload()

            def case_variant(state: str) -> Callable[[Route], None]:
                def handle(route: Route) -> None:
                    response = route.fetch()
                    case = response.json()
                    if state == "empty":
                        case["work"]["blockers"] = []
                    if state == "closed":
                        case["closed"] = True
                    route.fulfill(response=response, json=case)

                return handle

            for state in ("blocked", "empty", "closed", "ai-unavailable"):
                variant = case_variant(state)
                page.route("**/api/cases/ZF-1", variant)
                if state == "ai-unavailable":
                    page.route(
                        "**/api/assistants",
                        lambda route: route.fulfill(
                            status=503, json={"error": "Synthetic assistance outage"}
                        ),
                    )
                page.goto(base + "/app#/case/ZF-1?tab=overview")
                with (
                    page.expect_response("**/api/cases/ZF-1"),
                    page.expect_response("**/api/assistants") as assistance,
                ):
                    page.reload()
                page.get_by_role("tab", name="Overview", exact=True).wait_for()
                if state == "ai-unavailable":
                    check("injected assistance outage observed", assistance.value.status == 503)
                    expect(page.locator("[data-case-ai-count]")).to_contain_text("unavailable")
                    expect(page.locator("#case-tab-overview")).to_have_attribute(
                        "aria-selected", "true"
                    )
                    check(
                        "unavailable count stays live on Overview while AI is hidden",
                        page.locator("[data-case-ai-count]").is_visible()
                        and page.locator("#case-panel-ai").is_hidden(),
                    )
                if state == "closed":
                    check(
                        "closed all done, no current",
                        page.locator(".step.done").count() == 6
                        and page.locator(".step[aria-current]").count() == 0,
                    )
                if state == "empty":
                    check(
                        "empty blocker wording: " + page.locator(".case-summary").inner_text(),
                        "No recorded blockers." in page.locator(".case-summary").inner_text(),
                    )
                names = page.get_by_role("tab").all_text_contents()
                for name in names:
                    page.get_by_role("tab", name=name, exact=True).click()
                    scan(page, axe, reports, f"{state}/{name}")
                page.unroute("**/api/cases/ZF-1", variant)
                if state == "ai-unavailable":
                    page.unroute("**/api/assistants")

            page.goto(base + "/app#/case/SYN-526-FINAL?tab=overview")
            advance = page.get_by_role("button", name="Ready to book the installation", exact=True)
            advance.wait_for()
            advance.focus()
            with page.expect_response("**/api/cases/SYN-526-FINAL/advance") as refused:
                page.keyboard.press("Enter")
            check("keyboard final checks preserve blocked approval", refused.value.status == 409)
            page.get_by_role("status").filter(has_text="Funding").last.wait_for()
            check(
                "blocked keyboard action does not advance case",
                page.request.get(base + "/api/cases/SYN-526-FINAL").json()["stage"]
                == "Final checks before ordering",
            )
            page.goto(base + "/app#/case/ZF-4?tab=resident")
            page.get_by_role("tab", name="Resident", exact=True).wait_for()
            check(
                "open safety visible on Resident tab",
                page.locator("#case-safety").is_visible()
                and page.locator("#hz-source").is_visible(),
            )
            tab(page, "Funding")
            check(
                "blocked steps leave unrelated Funding tab available",
                page.get_by_role("tabpanel", name="Funding", exact=True).is_visible(),
            )
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 800})
                for name in page.get_by_role("tab").all_text_contents():
                    page.get_by_role("tab", name=name, exact=True).click()
                    check(
                        f"reflow {width}/{name}",
                        page.evaluate("document.documentElement.scrollWidth <= innerWidth"),
                    )
                if width == 320:
                    page.evaluate("window.scrollTo(0, 0)")
                    bottom = page.locator(".case-summary").evaluate(
                        "el => el.getBoundingClientRect().bottom"
                    )
                    check(f"320x800 summary within one viewport scroll ({bottom})", bottom <= 1600)
                    page.screenshot(path=str(out / "mobile-320.png"))
            page.emulate_media(reduced_motion="reduce", forced_colors="active")
            check(
                "reduced motion and forced-colour states retained",
                page.evaluate(
                    """() => [...document.querySelectorAll('.step a, [role=tab]')].every(
                  el => getComputedStyle(el).transitionDuration === '0s')
                  && [...document.querySelectorAll('.step-state')].every(el => el.textContent)"""
                ),
            )
            page.screenshot(path=str(out / "forced-colours.png"), full_page=True)
            page.emulate_media(forced_colors="none")
            page.route(
                "**/case-workspace.js",
                lambda route: route.fulfill(
                    status=404, content_type="text/plain", body="Synthetic missing enhancement"
                ),
            )
            page.reload()
            page.get_by_text("Tab navigation unavailable.", exact=False).wait_for()
            check(
                "missing enhancement keeps stacked sections and safety",
                page.locator("#case-panel-resident").is_visible()
                and page.locator("#case-panel-funding").is_visible()
                and page.locator("#hz-source").is_visible(),
            )
            page.unroute("**/case-workspace.js")
            check("no uncaught page errors", not errors)

            # chrome.tabs.setZoom changes real browser zoom, not device scale or CSS.
            with tempfile.TemporaryDirectory(prefix="zf-journey-zoom-") as scratch:
                root = Path(scratch)
                extension = root / "extension"
                extension.mkdir()
                (extension / "manifest.json").write_text(
                    json.dumps(
                        {
                            "manifest_version": 3,
                            "name": "Synthetic local zoom check",
                            "version": "1.0",
                            "permissions": ["tabs"],
                            "background": {"service_worker": "worker.js"},
                        }
                    )
                )
                (extension / "worker.js").write_text(
                    "chrome.runtime.onInstalled.addListener(() => {});"
                )
                zoom = playwright.chromium.launch_persistent_context(
                    str(root / "profile"),
                    channel="chromium",
                    headless=True,
                    no_viewport=True,
                    args=[
                        "--window-size=1280,800",
                        f"--disable-extensions-except={extension}",
                        f"--load-extension={extension}",
                    ],
                )
                try:
                    for cookie in context.cookies():
                        zoom.add_cookies(
                            [
                                {
                                    "name": cookie["name"],
                                    "value": cookie["value"],
                                    "url": base,
                                }
                            ]
                        )
                    zoom.route(
                        "**/*",
                        lambda route: (
                            route.continue_()
                            if route.request.url.startswith(base + "/")
                            else route.abort()
                        ),
                    )
                    zoom_page = zoom.pages[0]
                    zoom_page.goto(base + "/app#/case/ZF-1?tab=overview")
                    zoom_page.get_by_role("tab", name="Overview", exact=True).wait_for()
                    worker = (
                        zoom.service_workers[0]
                        if zoom.service_workers
                        else (zoom.wait_for_event("serviceworker"))
                    )
                    actual = worker.evaluate(
                        """async () => {
                          const [tab] = await chrome.tabs.query({active: true});
                          await chrome.tabs.setZoom(tab.id, 2);
                          return await chrome.tabs.getZoom(tab.id);
                        }"""
                    )
                    zoom_page.wait_for_function("innerWidth <= 640")
                    check("actual Chromium tab zoom is 200%", actual == 2)
                    for name in zoom_page.get_by_role("tab").all_text_contents():
                        button = zoom_page.get_by_role("tab", name=name, exact=True)
                        button.focus()
                        zoom_page.keyboard.press("Enter")
                        check(
                            f"200% browser zoom reflows/{name}",
                            zoom_page.evaluate(
                                "document.documentElement.scrollWidth <= innerWidth"
                            ),
                        )
                        focus = button.evaluate(
                            """el => {
                              const r = el.getBoundingClientRect();
                              return {active: el === document.activeElement,
                                outline: getComputedStyle(el).outlineStyle,
                                top: r.top, bottom: r.bottom, left: r.left, right: r.right,
                                width: innerWidth, height: innerHeight};
                            }"""
                        )
                        visible = (
                            focus["active"]
                            and focus["outline"] != "none"
                            and focus["top"] >= 0
                            and focus["bottom"] <= focus["height"]
                            and focus["left"] >= 0
                            and focus["right"] <= focus["width"]
                        )
                        if not visible:
                            zoom_page.screenshot(
                                path=str(out / "zoom-focus-failure.png"), full_page=True
                            )
                        check(f"200% keyboard focus visible/{name}: {focus}", visible)
                    zoom_page.screenshot(path=str(out / "browser-zoom-200.png"), full_page=True)
                finally:
                    zoom.close()
            (out / "results.json").write_text(
                json.dumps(
                    dict(
                        browser=browser.version,
                        axe_version="4.10.3",
                        scans=reports,
                        page_errors=errors,
                        zoom="chrome.tabs.setZoom=2; innerWidth<=640",
                    ),
                    indent=2,
                )
                + "\n"
            )
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.axe.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Unexpected axe 4.10.3 bytes")
    args.out.mkdir(parents=True, exist_ok=False)
    main(lambda base: run_browser(base, raw.decode(), args.out), journey_data)
