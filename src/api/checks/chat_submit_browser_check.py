"""Enter/Send stay open through actual workspace and equivalent session refreshes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright
from test_resident_demo_api import FAKE_PASSWORD, DemoTestCase

from checks.design_system_browser_check import main as employee_server
from checks.design_system_browser_check import synthetic_data


def sign_in(page: Page, base: str) -> None:
    page.goto(base + "/app")
    page.get_by_label("Work email", exact=True).fill("sam@example.test")
    page.get_by_label("Password", exact=True).fill("synthetic-check")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
    page.evaluate("async () => { await route(); }")


def open_employee(page: Page) -> None:
    page.evaluate("() => { employeeChat.reset(); employeeChat.install(); }")
    page.locator("#employee-chat-launcher").click()
    expect(page.locator("#employee-chat-question")).to_be_enabled()
    expect(page.locator("#employee-chat")).to_be_visible()


def send_matrix(page: Page) -> list[dict[str, Any]]:
    results = []
    for case in (False, True):
        page.evaluate(
            """async hash => {
              history.replaceState(null, '', hash);
              await route();
            }""",
            "#/case/ZF-1" if case else "#/",
        )
        for activation in ("Enter", "Send"):
            for refresh in ("none", "route", "session"):
                open_employee(page)
                panel = page.locator("#employee-chat")
                question = panel.locator("textarea")
                skill = panel.locator("select")
                skill.select_option("stock-prioritisation")
                held: list[Route] = []
                endpoint = "**/api/chat/threads/*/ask"
                page.route(endpoint, lambda route: held.append(route))
                try:
                    question.fill("What can chat do?")
                    if activation == "Enter":
                        question.press("Enter")
                    else:
                        panel.get_by_role("button", name="Send", exact=True).click()
                    expect(panel.locator("form")).to_have_attribute("aria-busy", "true")
                    expect(question).to_be_focused()
                    for _ in range(500):
                        if held:
                            break
                        page.wait_for_timeout(10)
                    assert len(held) == 1, "Answer request did not reach the local interceptor"
                    page.evaluate("window.sentFocus = document.activeElement")
                    if refresh != "none":
                        page.evaluate(
                            """async refresh => {
                              if (refresh === 'route') await route();
                              else await start();
                            }""",
                            refresh,
                        )
                    label = f"{case}/{activation}/{refresh}"
                    assert panel.is_visible(), f"{label}: refresh dismissed submitted chat"
                    expect(page.locator("#employee-chat-launcher")).to_have_attribute(
                        "aria-expanded", "true"
                    )
                    assert page.evaluate("document.activeElement === sentFocus"), label
                    expect(question).to_have_value("What can chat do?")
                    expect(skill).to_have_value("stock-prioritisation")
                    held[0].fulfill(
                        json={
                            "reply": f"Visible answer {label}",
                            "skill": "stock-prioritisation",
                            "workflow_only": True,
                            "citations": [],
                        }
                    )
                    expect(panel.get_by_role("log")).to_contain_text(f"Visible answer {label}")
                    expect(panel.locator("form")).to_have_attribute("aria-busy", "false")
                    expect(panel).to_be_visible()
                    expect(question).to_have_value("")
                    assert page.evaluate("document.activeElement === sentFocus"), label
                    results.append({"case": case, "activation": activation, "refresh": refresh})
                finally:
                    page.unroute(endpoint)
    print("PASS employee: 12 Enter/Send x case/no-case x none/route/session combinations")
    return results


def render_focus(page: Page) -> None:
    open_employee(page)
    page.evaluate("""() => {
      document.querySelector('#employee-chat textarea').value = 'Retained draft';
      window.focusLog = document.querySelector('#employee-chat [role=log]');
      focusLog.innerHTML = '<details><summary>Sources</summary>Constructed source</details>';
    }""")
    panel = page.locator("#employee-chat")
    for selector in ("textarea", "[role=log]", "summary"):
        panel.locator(selector).last.focus()
        page.evaluate("window.renderFocus = document.activeElement")
        page.evaluate("async () => { await route(); }")
        expect(panel).to_be_visible()
        assert page.evaluate("document.activeElement === renderFocus"), selector
    for dismissal in ("Escape", "external"):
        panel.locator("h2").focus()
        page.evaluate("""() => {
          window.renderWait = {api};
          api = (path, body, signal) => {
            if (path === '/api/cases/ZF-1' && !renderWait.resolve)
              return new Promise(resolve => { renderWait.resolve = resolve; })
                .then(() => renderWait.api(path, body, signal));
            return renderWait.api(path, body, signal);
          };
          renderWait.task = route();
        }""")
        page.wait_for_function("() => typeof renderWait.resolve === 'function'")
        if dismissal == "Escape":
            page.keyboard.press("Escape")
            expect(page.locator("#employee-chat-launcher")).to_be_focused()
        else:
            page.locator("#nav a").first.focus()
        page.evaluate("window.renderFocus = document.activeElement")
        expect(panel).to_be_hidden()
        page.evaluate("""async () => {
          renderWait.resolve();
          await renderWait.task;
          api = renderWait.api;
          delete window.renderWait;
        }""")
        expect(panel).to_be_hidden()
        expect(page.locator("#employee-chat-launcher")).to_have_attribute("aria-expanded", "false")
        # A normal render can focus the app when chat no longer owns focus.
        expect(page.locator("#app")).to_be_focused()
        page.locator("#employee-chat-launcher").click()
        expect(panel.locator("textarea")).to_have_value("Retained draft")
    print("PASS employee: composer/history/Sources focus retained; dismissed chat never reopens")


def session_lifecycle(page: Page) -> None:
    for stage in ("skills", "thread", "ask"):
        for change in ("equivalent", "user", "capability", "account"):
            page.evaluate("""stage => {
              employeeChat.reset();
              window.authCheck = {api, original: me, stage, asks: 0};
              api = (path, body, signal) => {
                if (path.endsWith('/ask')) authCheck.asks++;
                const hold = stage === 'skills' ? path === '/api/chat/skills'
                  : stage === 'thread' ? path === '/api/chat/threads' : path.endsWith('/ask');
                if (!hold || authCheck.resolve) return authCheck.api(path, body, signal);
                authCheck.signal = signal;
                return new Promise(resolve => { authCheck.resolve = resolve; });
              };
              authCheck.open = employeeChat.open();
              authCheck.task = authCheck.open;
            }""", stage)
            if stage != "skills":
                expect(page.locator("#employee-chat-question")).to_be_enabled()
                page.locator("#employee-chat-question").fill("Delayed session question")
                page.evaluate("""() => {
                  authCheck.task = document.querySelector('#employee-chat form')
                    .onsubmit(new Event('submit', {cancelable: true}));
                }""")
            page.wait_for_function("() => typeof authCheck.resolve === 'function'")
            page.evaluate("""() => {
              authCheck.focus = document.activeElement;
              authCheck.root = document.querySelector('#employee-chat');
            }""")

            def refreshed(route: Route) -> None:
                data = route.fetch().json()
                if change == "user":
                    data["user"]["code"] = "SYNTHETIC-OTHER"
                elif change == "capability":
                    data["user"]["rule_roles"] = ["synthetic-changed-capability"]
                elif change == "account":
                    data["account"]["email"] = "changed@example.test"
                else:
                    data["counts"]["synthetic_refresh"] = 123
                    data["navigation"][0]["scope"] = "Synthetic refreshed scope"
                route.fulfill(json=data)

            page.route("**/api/me", refreshed)
            try:
                page.evaluate("async () => { await start(); }")
            finally:
                page.unroute("**/api/me", refreshed)
            if change == "equivalent":
                expect(page.locator("#employee-chat")).to_be_visible()
                assert page.evaluate("""() => me === authCheck.original
                  && me.counts.synthetic_refresh === 123
                  && me.navigation[0].scope === 'Synthetic refreshed scope'
                  && document.activeElement === authCheck.focus
                  && !authCheck.signal.aborted"""), (stage, change)
            else:
                expect(page.locator("#employee-chat")).to_have_count(0)
                assert page.evaluate("authCheck.signal.aborted"), (stage, change)
                page.evaluate("() => { api = authCheck.api; }")
                page.locator("#employee-chat-launcher").click()
                expect(page.locator("#employee-chat-question")).to_be_enabled()
                page.locator("#employee-chat-question").fill("Replacement draft")
                page.evaluate("""() => {
                  authCheck.replacement = document.querySelector('#employee-chat').innerHTML;
                  authCheck.focus = document.activeElement;
                }""")
            page.evaluate("""async () => {
              const s = authCheck;
              s.resolve(s.stage === 'skills' ? {skills: []}
                : s.stage === 'thread' ? (me === s.original
                  ? await s.api('/api/chat/threads', {case_id: 'ZF-1'})
                  : {id: 'obsolete-synthetic-thread'})
                : {reply:'Session-safe answer', workflow_only:true, skill:'general', citations:[]});
              await s.task;
            }""")
            if change == "equivalent":
                expect(page.locator("#employee-chat form")).to_have_attribute("aria-busy", "false")
                expect(page.locator("#employee-chat-question")).to_be_enabled()
                if stage != "skills":
                    expect(page.locator("#employee-chat .chat-widget-assistant")).to_have_count(1)
                if stage == "ask":
                    expect(page.locator("#employee-chat [role=log]")).to_contain_text(
                        "Session-safe answer"
                    )
                assert page.evaluate("document.activeElement === authCheck.focus")
            else:
                assert page.evaluate("""() =>
                  document.querySelector('#employee-chat').innerHTML === authCheck.replacement
                  && document.activeElement === authCheck.focus
                  && authCheck.asks === (authCheck.stage === 'ask' ? 1 : 0)"""), (stage, change)
            page.evaluate("""async () => {
              api = authCheck.api;
              employeeChat.reset();
              delete window.authCheck;
              await start();
            }""")
    page.evaluate("""() => {
      window.authRace = {api};
      api = (path, body, signal) => path === '/api/me'
        ? new Promise(resolve => { authRace.resolve = resolve; })
          .then(() => authRace.api(path, body, signal))
        : authRace.api(path, body, signal);
      authRace.task = start();
      me = null;
      login('Synthetic expired session');
      document.getElementById('email').focus();
    }""")
    page.evaluate("""async () => {
      authRace.resolve();
      await authRace.task;
      api = authRace.api;
      delete window.authRace;
      if (me !== null) throw new Error('Obsolete re-check restored the session');
    }""")
    expect(page.locator("#email")).to_be_focused()
    expect(page.locator("#nav")).to_be_hidden()
    expect(page.locator("#employee-chat")).to_have_count(0)
    print("PASS employee: real start() setup/thread/ask auth equivalence/change and stale-auth race")


def resident(browser: Browser) -> None:
    fixture = DemoTestCase()
    fixture.setUp()
    fixture.app.allowed_hosts = ("127.0.0.1",)
    base = f"http://127.0.0.1:{fixture.app.port}"
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        page.goto(base)
        page.get_by_label("Email address", exact=True).fill("one@example.com")
        page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
        page.get_by_role("button", name="Sign in", exact=True).click()
        expect(page.locator("#content")).to_be_visible()
        page.locator("#chat-launcher").click()
        panel = page.locator("#resident-chat")
        page.locator("#assistant-consent").check()
        for activation in ("Enter", "Send"):
            panel.locator("textarea").fill("What is my address?")
            before = panel.locator(".chat-widget-assistant").count()
            if activation == "Enter":
                panel.locator("textarea").press("Enter")
            else:
                panel.get_by_role("button", name="Send", exact=True).click()
            expect(panel.locator(".chat-widget-assistant")).to_have_count(before + 1)
            expect(panel.locator(".chat-widget-assistant").last).to_contain_text("C-1 Test Street")
            expect(panel).to_be_visible()
            expect(panel.locator("textarea")).to_be_focused()
            expect(panel.locator("form")).to_have_attribute("aria-busy", "false")
        page.keyboard.press("Escape")
        expect(panel).to_be_hidden()
        expect(page.locator("#chat-launcher")).to_be_focused()
        page.locator("#chat-launcher").click()
        page.locator("#account summary").focus()
        expect(panel).to_be_hidden()
        expect(page.locator("#account summary")).to_be_focused()
        print("PASS resident: actual rules answers with Enter/Send; Escape and external focus")
    finally:
        context.close()
        fixture.doCleanups()


def employee(browser: Browser, base: str, out: Path) -> None:
    context = browser.new_context()
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        sign_in(page, base)
        results = send_matrix(page)
        page.screenshot(path=str(out / "employee-answer-visible.png"))
        render_focus(page)
        session_lifecycle(page)
        assert not errors, errors
        (out / "employee-matrix.json").write_text(json.dumps(results, indent=2))
    finally:
        context.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            employee_server(
                lambda base: employee(browser, base, args.out),
                synthetic_data,
                synthetic_chat_privacy=True,
            )
            resident(browser)
            (args.out / "results.json").write_text(json.dumps({
                "status": "passed", "browser": browser.version,
                "scope": "owned loopback apps; actual rules and controlled response timing",
                "live_site_model_and_human_accessibility": "not run",
            }, indent=2))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
