"""Employee chat: real synthetic API fallback, dialog keyboard states and pinned axe."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, Route, expect, sync_playwright

from checks.design_system_browser_check import main, synthetic_data
from checks.regulatory_ux_check import AXE_SHA256

def scan(page: Page, axe: str, state: str) -> dict[str, Any]:
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate("""async () => await axe.run(
      document.querySelector('#employee-chat'),
      {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']}}
    )""")
    assert not result["violations"], (state, result["violations"])
    return {"state": state, "violations": result["violations"], "passes": len(result["passes"])}


def late_success(page: Page, pending: str, transition: str) -> None:
    """Settle an actual successful API promise independently of transport abort."""
    page.evaluate("""pending => {
      employeeChat.reset();
      const state = window.employeeLate = {pending, api, askCalls: 0};
      api = (path, body, signal) => {
        if (path.endsWith('/ask')) state.askCalls++;
        const hold = pending === 'skills' ? path === '/api/chat/skills'
          : pending === 'thread' ? path === '/api/chat/threads' : path.endsWith('/ask');
        if (!hold || state.resolve) return state.api(path, body, signal);
        state.signal = signal;
        return new Promise(resolve => { state.resolve = resolve; }).then(value => {
          state.fulfilled = true;
          return value;
        });
      };
      state.open = document.getElementById('employee-chat-launcher').onclick();
      if (pending === 'skills') state.task = state.open;
    }""", pending)
    try:
        dialog = page.get_by_role("dialog", name="Employee assistant")
        expect(dialog).to_be_visible()
        if pending != "skills":
            expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
            page.get_by_label("Your work question", exact=True).fill("Controlled late question")
            page.evaluate("""() => {
              employeeLate.task = document.querySelector('#employee-chat form')
                .onsubmit(new Event('submit', {cancelable: true}));
            }""")
        page.wait_for_function("() => typeof window.employeeLate.resolve === 'function'")
        page.evaluate("""() => {
          const state = window.employeeLate;
          state.root = document.querySelector('#employee-chat');
          state.log = state.root.querySelector('[role=log]');
          state.status = state.root.querySelector('p[role=status]');
        }""")
        if transition == "close":
            page.keyboard.press("Escape")
            expect(page.locator("#employee-chat")).to_be_hidden()
            expect(page.locator("#employee-chat-launcher")).to_be_focused()
            page.evaluate("""async () => {
              const state = window.employeeLate;
              if (state.signal.aborted) throw new Error('Hide cancelled current read');
              state.resolve(state.pending === 'skills' ? {skills: []}
                : state.pending === 'thread' ? await state.api('/api/chat/threads', {case_id: ''})
                : {kind: 'answer', reply: 'CURRENT HIDDEN ANSWER', skill: 'general',
                   label: 'AI suggestion, not approved', workflow_only: false, citations: []});
              await state.task;
              if (!state.fulfilled) throw new Error('Hidden current read did not finish');
            }""")
            expect(page.locator("#employee-chat")).to_be_hidden()
            expect(page.locator("#employee-chat-launcher")).to_be_focused()
            return
        elif transition == "route":
            destination = "#/" if page.url.endswith("#/progress") else "#/progress"
            page.evaluate("hash => { location.hash = hash; }", destination)
            expect(page.locator("#employee-chat")).to_have_count(0)
            expect(page.locator("#app h1").first).to_be_visible()
            page.locator("#employee-chat-launcher").click()
            expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
            page.get_by_label("Your work question", exact=True).fill("Replacement draft")
        else:
            assert transition == "session"
            page.evaluate("""() => {
              window.employeeLate.session = me;
              me = null;
              login('Synthetic session change');
            }""")
            expect(page.locator("#employee-chat")).to_have_count(0)
            page.get_by_label("Work email", exact=True).focus()

        before = page.evaluate("""() => {
          const state = window.employeeLate;
          state.focus = document.activeElement;
          state.snapshot = () => ({
            oldLog: state.log.textContent, oldStatus: state.status.textContent,
            log: document.querySelector('#employee-chat [role=log]')?.textContent ?? null,
            status: document.querySelector('#employee-chat p[role=status]')?.textContent ?? null,
            question: document.querySelector('#employee-chat-question')?.value ?? null,
            workspace: document.getElementById('workspace-status').textContent,
            dialogs: document.querySelectorAll('#employee-chat').length
          });
          return state.snapshot();
        }""")
        after = page.evaluate("""async () => {
          const state = window.employeeLate;
          if (!state.signal.aborted) throw new Error(`Expected disposal to abort ${state.pending} transport`);
          if (typeof state.task?.then !== 'function') throw new Error('Missing tracked API consumer task');
          state.resolve(state.pending === 'skills' ? {skills: []}
            : state.pending === 'thread' ? {id: 'controlled-stale-thread'}
            : {kind: 'answer', reply: 'CONTROLLED LATE SUCCESS', skill: 'general',
               label: 'AI suggestion, not approved', workflow_only: false, citations: []});
          await state.task;
          if (!state.fulfilled) throw new Error('Successful API promise did not settle');
          if (state.askCalls !== (state.pending === 'ask' ? 1 : 0))
            throw new Error('Obsolete thread completion started an ask');
          if (document.activeElement !== state.focus) throw new Error('Late success moved focus');
          return state.snapshot();
        }""")
        assert after == before, (pending, transition, before, after)
    finally:
        page.evaluate("""async () => {
          const state = window.employeeLate;
          api = state.api;
          employeeChat.reset();
          if (state.session) await start();
          delete window.employeeLate;
        }""")


def run_browser(base: str, axe: str, output: Path) -> None:
    reports = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(reduced_motion="reduce")
        context.route("**/*", lambda route: route.continue_()
                      if route.request.url.startswith(base + "/") else route.abort())
        try:
            page = context.new_page()
            page.on("dialog", lambda dialog: dialog.accept())
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "/app")
            expect(page.locator("#employee-chat-launcher")).to_be_hidden()
            page.get_by_label("Work email", exact=True).fill("sam@example.test")
            page.get_by_label("Password", exact=True).fill("synthetic-check")
            page.get_by_role("button", name="Sign in", exact=True).click()
            expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
            launcher = page.locator("#employee-chat-launcher")
            launcher.focus()
            launcher.press("Enter")
            dialog = page.get_by_role("dialog", name="Employee assistant")
            expect(dialog).to_be_visible()
            question = page.get_by_label("Your work question", exact=True)
            expect(dialog.get_by_role("heading", name="Employee assistant")).to_be_focused()
            expect(dialog.locator("select option")).to_have_count(6)
            question.fill("What can chat do?")
            dialog.get_by_role("button", name="Send", exact=True).click()
            expect(dialog.get_by_role("log")).to_contain_text("ordinary case workflow")
            expect(dialog.get_by_role("log")).to_contain_text("Workflow-only help, no record changed")
            expect(dialog).to_contain_text("No case or home record is visible")
            expect(dialog.get_by_role("log")).to_have_attribute("aria-live", "polite")
            reports.append(scan(page, axe, "actual-model-unavailable"))
            page.keyboard.press("Escape")
            expect(page.locator("#employee-chat")).to_be_hidden()
            expect(launcher).to_be_focused()

            for destination in ("#/", "#/all", "#/overview", "#/time", "#/progress",
                                "#/closed", "#/assistants", "#/case/ZF-1"):
                page.evaluate("(hash) => { location.hash = hash; }", destination)
                expect(page.locator("#app h1").first).to_be_visible()
                launcher.click()
                expect(page.get_by_role("dialog")).to_be_visible()
                page.keyboard.press("Escape")
            page.evaluate("() => { location.hash = '#/case/ZF-1'; }")
            expect(page.get_by_role("link", name="Back to the list", exact=True)).to_be_visible()
            launcher.click()
            expect(page.get_by_role("dialog")).to_contain_text("Context: case ZF-1")

            skills = page.get_by_label("Agent skill", exact=True)
            expect(skills).to_be_enabled()
            ids = skills.locator("option").evaluate_all("nodes => nodes.map(n => n.value)")

            def answer(route: Route) -> None:
                body = route.request.post_data_json
                assert isinstance(body, dict)
                route.fulfill(json={
                    "kind": "answer", "reply": "Synthetic cited case explanation.",
                    "label": "AI suggestion, not approved", "skill": body["skill"],
                    "workflow_only": False,
                    "citations": [{"id": "ZF-1/stage", "text": "Survey"}],
                })

            page.route("**/api/chat/threads/*/ask", answer)
            for skill in ids:
                skills.select_option(skill)
                question.fill("Explain the next check")
                page.get_by_role("dialog").get_by_role("button", name="Send", exact=True).click()
                expect(page.get_by_role("log", name="Employee assistant conversation")).to_contain_text(f"Skill: {skill}.")
                expect(page.get_by_role("log", name="Employee assistant conversation")).to_contain_text("ZF-1/stage")
            reports.append(scan(page, axe, "synthetic-cited-answer"))
            close = page.get_by_role("button", name="Close chat", exact=True)
            close.focus()
            for key in ("Shift+Tab", "Tab", "Tab", "Tab", "Tab", "Tab", "Tab"):
                page.keyboard.press(key)
                assert page.evaluate("document.activeElement !== null")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.get_by_role("dialog").evaluate(
                    "el => el.scrollWidth <= el.clientWidth")
            assert page.evaluate("""() => getComputedStyle(
              document.querySelector('#employee-chat')).transitionDuration === '0s'""")

            page.unroute("**/api/chat/threads/*/ask", answer)
            held: list[Route] = []
            def hold(route: Route) -> None:
                held.append(route)
                page.evaluate("() => { window.employeeAskArrived = true; }")

            page.route("**/api/chat/threads/*/ask", hold)
            question.fill("Delayed case question")
            page.get_by_role("dialog").get_by_role("button", name="Send", exact=True).click()
            page.wait_for_function("() => window.employeeAskArrived === true")
            assert len(held) == 1
            page.evaluate("() => { location.hash = '#/progress'; }")
            expect(page.locator("#employee-chat")).to_have_count(0)
            try:
                answer(held[0])
            except PlaywrightError as error:
                # Transport cancellation is separate from the successful API proof below.
                assert "Invalid" in str(error) or "Target" in str(error), str(error)
            launcher.click()
            expect(page.get_by_role("dialog")).not_to_contain_text("Synthetic cited case explanation")
            page.keyboard.press("Escape")
            page.unroute("**/api/chat/threads/*/ask")

            for pending in ("skills", "thread", "ask"):
                for transition in ("close", "route", "session"):
                    try:
                        late_success(page, pending, transition)
                    except PlaywrightError as error:
                        raise AssertionError(f"Late success failed: {pending}/{transition}") from error

            for endpoint in ("skills", "threads", "threads/*/ask"):
                for denied in (403, 404, 401):
                    if page.get_by_label("Work email", exact=True).is_visible():
                        page.get_by_label("Work email", exact=True).fill("sam@example.test")
                        page.get_by_label("Password", exact=True).fill("synthetic-check")
                        page.get_by_role("button", name="Sign in", exact=True).click()
                        expect(launcher).to_be_visible()
                        expect(page.locator("#app h1").first).to_be_visible()
                    page.evaluate("() => { location.hash = '#/case/ZF-1'; }")
                    expect(page.get_by_role("link", name="Back to the list", exact=True)).to_be_visible()
                    def denied_reply(route: Route) -> None:
                        route.fulfill(status=denied, json={"error": "Synthetic access ended"})

                    pattern = f"**/api/chat/{endpoint}"
                    page.route(pattern, denied_reply)
                    launcher.click()
                    if endpoint != "skills":
                        expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
                        question.fill("Check access")
                        page.get_by_role("dialog").get_by_role("button", name="Send", exact=True).click()
                    expect(page.locator("#employee-chat")).to_have_count(0)
                    expect(page.locator("#app")).to_be_focused()
                    if denied != 401:
                        expect(page.locator("#workspace-status")).to_contain_text("Chat access ended.")
                        expect(launcher).to_be_visible()
                    else:
                        expect(page.get_by_label("Work email", exact=True)).to_be_visible()
                        expect(launcher).to_be_hidden()
                    page.unroute(pattern, denied_reply)
            expect(page.get_by_label("Work email", exact=True)).to_be_visible()
            expect(launcher).to_be_hidden()
            assert not errors, errors
            print("PASS employee chat: real fallback; six selections; arrived transport; nine controlled late successes; metadata/thread/ask denials; route/session disposal; keyboard, focus, live, reduced motion, reflow and dialog axe")
        finally:
            context.close()
            browser.close()
    output.mkdir(parents=True, exist_ok=True)
    (output / "axe-results.json").write_text(json.dumps(reports, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.axe.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Expected pinned axe-core 4.10.3")
    main(
        lambda base: run_browser(base, raw.decode(), args.out),
        synthetic_data,
        synthetic_chat_privacy=True,
    )
