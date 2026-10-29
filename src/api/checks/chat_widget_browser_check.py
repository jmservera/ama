"""Shared chat acceptance against two owned synthetic loopback applications."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, Route, expect, sync_playwright
from test_resident_demo_api import FAKE_PASSWORD, DemoTestCase

from checks.design_system_browser_check import main as employee_server
from checks.design_system_browser_check import synthetic_data
from checks.regulatory_ux_check import AXE_SHA256

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


def scan(page: Page, axe: str, root: str) -> None:
    page.evaluate(axe)
    violations = page.evaluate(
        """async root => (await axe.run(document.querySelector(root), {
          runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag22aa']}
        })).violations""",
        root,
    )
    assert not violations, violations


def shared_ui(page: Page, root: str, endpoint: str, out: Path, audience: str, axe: str) -> None:
    panel = page.locator(root)
    question = panel.locator("textarea")
    send = panel.get_by_role("button", name="Send", exact=True)
    log = panel.get_by_role("log")
    requests: list[dict[str, Any]] = []
    answers = 0

    def answer(route: Route) -> None:
        nonlocal answers
        answers += 1
        body = route.request.post_data_json
        assert isinstance(body, dict)
        requests.append(body)
        route.fulfill(
            json={
                "answer": f"Resident answer {answers}. " + "Grounded fictional explanation. " * 25,
                "reply": f"Employee answer {answers}. " + "Grounded fictional explanation. " * 25,
                "label": "AI suggestion, not approved",
                "kind": "answer",
                "skill": "general",
                "workflow_only": False,
                "sources": ["Synthetic own-case source"],
                "citations": [{"id": "ZF-1/stage", "text": "Survey"}],
            }
        )

    page.route(endpoint, answer)
    question.fill("First question")
    question.press("Shift+Enter")
    expect(question).to_have_value("First question\n")
    assert not requests
    question.evaluate("""el => el.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Enter', isComposing: true, bubbles: true, cancelable: true
    }))""")
    assert not requests
    question.press("Enter")
    expect(log).to_contain_text("answer 1.")
    expect(send).to_be_enabled()
    assert len(requests) == 1
    expect(panel).to_be_visible()
    expect(log.locator("details").first).not_to_have_attribute("open", "")
    expect(
        log.locator(".chat-widget-meta").filter(has_text="AI suggestion, not approved").last
    ).to_be_visible()
    for index in range(2, 5):
        question.fill(f"Question {index}")
        send.click()
        expect(log).to_contain_text(f"answer {index}.")
        expect(send).to_be_enabled()
    assert len(requests) == 4
    for name in ("Attach", "Voice"):
        control = panel.get_by_role("button", name=name, exact=True)
        expect(control).to_be_disabled()
        reason = control.get_attribute("aria-describedby")
        assert reason
        expect(page.locator("#" + reason)).to_contain_text("not supported")
    for width in (320, 390, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        page.evaluate("document.documentElement.style.fontSize = ''")
        expect(panel).to_be_visible()
        assert panel.evaluate("el => el.scrollWidth <= el.clientWidth")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        composer = panel.locator("form")
        before = composer.bounding_box()
        assert before
        assert log.evaluate("el => el.scrollHeight > el.clientHeight")
        log.evaluate("el => { el.scrollTop = 0; }")
        assert composer.bounding_box() == before
        log.evaluate("el => { el.scrollTop = el.scrollHeight; }")
        assert log.evaluate("el => Math.abs(el.scrollHeight - el.clientHeight - el.scrollTop) < 3")
        assert composer.bounding_box() == before
        expect(send).to_be_in_viewport()
        scan(page, axe, root)
        page.screenshot(path=str(out / f"{audience}-{width}.png"))
    page.locator("html").evaluate("el => { el.style.fontSize = '200%'; }")
    page.set_viewport_size({"width": 320, "height": 900})
    assert panel.evaluate("el => el.scrollWidth <= el.clientWidth")
    page.locator("html").evaluate("el => { el.style.fontSize = ''; }")
    page.set_viewport_size({"width": 1280, "height": 900})
    question.fill("Draft survives closing")
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    expect(page.get_by_role("button", name="Chat", exact=True)).to_be_focused()
    page.get_by_role("button", name="Chat", exact=True).click()
    expect(log).to_contain_text("answer 1.")
    expect(log).to_contain_text("answer 4.")
    expect(question).to_have_value("Draft survives closing")
    # A nonmodal popup must permit normal Tab traversal into the page.
    send.focus()
    left = False
    for _ in range(6):
        page.keyboard.press("Tab")
        if not panel.evaluate("el => el.contains(document.activeElement)"):
            left = True
            break
    assert left, "Nonmodal chat trapped Tab"
    page.clock.install(time=datetime(2030, 1, 1, tzinfo=UTC))
    page.clock.pause_at(datetime(2030, 1, 1, 0, 0, 1, tzinfo=UTC))
    loading = panel.locator(".chat-widget-loading")
    question.fill("Fast answer")
    send.click()
    expect(log).to_contain_text("answer 5.")
    expect(send).to_be_enabled()
    page.clock.run_for(250)
    expect(loading).to_be_hidden()
    page.unroute(endpoint, answer)

    def fast_failure(route: Route) -> None:
        route.fulfill(status=503, json={"error": "Synthetic immediate failure"})

    page.route(endpoint, fast_failure)
    question.fill("Fast failure")
    send.click()
    expect(panel.get_by_role("alert")).to_contain_text("Synthetic immediate failure")
    expect(send).to_be_enabled()
    page.clock.run_for(250)
    expect(loading).to_be_hidden()
    page.unroute(endpoint, fast_failure)
    held: list[Route] = []
    page.route(endpoint, lambda route: held.append(route))
    question.fill("Controlled delayed question")
    send.click()
    page.wait_for_function(
        "() => document.querySelector('.chat-widget form').getAttribute('aria-busy') === 'true'"
    )
    expect(loading).to_be_hidden()
    page.clock.run_for(199)
    expect(loading).to_be_hidden()
    page.clock.run_for(1)
    expect(loading).to_be_visible()
    for motion in ("no-preference", "reduce"):
        page.emulate_media(reduced_motion=motion)
        animation = loading.evaluate("el => getComputedStyle(el, '::before').animationName")
        assert (animation == "none") == (motion == "reduce"), animation
    assert len(held) == 1
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    page.get_by_role("button", name="Chat", exact=True).focus()
    held.pop().fulfill(status=503, json={"error": "Synthetic failure. Try again."})
    page.get_by_role("button", name="Chat", exact=True).click()
    expect(panel.get_by_role("alert")).to_contain_text("Synthetic failure")
    expect(question).to_have_value("Controlled delayed question")
    expect(send).to_be_enabled()
    expect(loading).to_be_hidden()
    page.clock.run_for(500)
    expect(loading).to_be_hidden()
    page.clock.resume()
    scan(page, axe, root)
    page.unroute(endpoint)
    print(
        f"PASS {audience}: thread, pinned input, keyboard, labels, controls; "
        "200ms loading, errors, focus, axe, reflow"
    )


def employee_stale(page: Page) -> None:
    """Resolve obsolete successful/rejected promises, independently of AbortSignal."""
    for pending in ("skills", "thread", "ask"):
        for outcome in ("success", "rejection"):
            for transition in ("route", "session"):
                page.evaluate(
                    """({pending}) => {
                  employeeChat.reset();
                  const state = window.staleChat = {api, pending, asks: 0};
                  api = (path, body, signal) => {
                    if (path.endsWith('/ask')) state.asks++;
                    const hold = pending === 'skills' ? path === '/api/chat/skills'
                      : pending === 'thread' ? path === '/api/chat/threads' : path.endsWith('/ask');
                    if (!hold || state.resolve) return state.api(path, body, signal);
                    state.signal = signal;
                    return new Promise((resolve, reject) => {
                      state.resolve = resolve; state.reject = reject;
                    });
                  };
                  state.open = document.getElementById('employee-chat-launcher').onclick();
                }""",
                    {"pending": pending},
                )
                expect(page.locator("#employee-chat")).to_be_visible()
                if pending != "skills":
                    expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
                    page.get_by_label("Your work question", exact=True).fill("Obsolete question")
                    page.evaluate("""() => {
                      window.staleChat.task = document.querySelector('#employee-chat form')
                        .onsubmit(new Event('submit', {cancelable: true}));
                    }""")
                page.wait_for_function("() => typeof staleChat.resolve === 'function'")
                page.evaluate(
                    """transition => {
                  const state = window.staleChat;
                  if (transition === 'session') {
                    state.session = me;
                    me = null;
                    employeeChat.reset(true);
                  } else {
                    location.hash = location.hash === '#/progress' ? '#/' : '#/progress';
                  }
                }""",
                    transition,
                )
                expect(page.locator("#employee-chat")).to_have_count(0)
                if transition == "session":
                    page.evaluate("() => { me = staleChat.session; employeeChat.install(); }")
                page.evaluate("""() => {
                  api = staleChat.api;
                  document.getElementById('employee-chat-launcher').onclick();
                }""")
                expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
                page.get_by_label("Your work question", exact=True).fill("Replacement draft")
                snapshot = page.locator("#employee-chat").inner_text()
                page.evaluate(
                    """async outcome => {
                  const state = window.staleChat;
                  if (!state.signal.aborted) throw new Error('Old operation was not aborted');
                  state.focus = document.activeElement;
                  if (outcome === 'rejection') state.reject(new Error('OBSOLETE ERROR'));
                  else state.resolve(state.pending === 'skills' ? {skills: []}
                    : state.pending === 'thread' ? {id: 'obsolete'}
                    : {reply:'OBSOLETE ANSWER', label:'AI suggestion, not approved',
                       kind:'answer', citations:[]});
                  await (state.pending === 'skills' ? state.open : state.task);
                  if (document.activeElement !== state.focus)
                    throw new Error('Old result moved focus');
                  if (state.asks !== (state.pending === 'ask' ? 1 : 0))
                    throw new Error('Obsolete thread started an ask');
                }""",
                    outcome,
                )
                assert page.locator("#employee-chat").inner_text() == snapshot
                expect(page.get_by_label("Your work question", exact=True)).to_have_value(
                    "Replacement draft"
                )
                expect(page.get_by_role("button", name="Send", exact=True)).to_be_enabled()
                page.evaluate("() => { employeeChat.reset(); delete window.staleChat; }")
    print(
        "PASS employee: 12 obsolete success/rejection combinations; "
        "no stale request, text, focus or busy cleanup"
    )


def employee(browser: Browser, base: str, out: Path, axe: str) -> None:
    context = browser.new_context()
    context.route(
        "**/*",
        lambda route: (
            route.continue_() if route.request.url.startswith(base + "/") else route.abort()
        ),
    )
    try:
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(base + "/app")
        page.get_by_label("Work email", exact=True).fill("sam@example.test")
        page.get_by_label("Password", exact=True).fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
        for asset in ("chat-widget.js", "chat-widget.css"):
            assert page.request.get(base + "/" + asset).body() == (WEB / asset).read_bytes()
        page.get_by_role("button", name="Chat", exact=True).click()
        expect(page.locator("#employee-chat select option")).to_have_count(6)
        question = page.get_by_label("Your work question", exact=True)
        question.fill("What can chat do?")
        page.get_by_role("button", name="Send", exact=True).click()
        expect(page.locator("#employee-chat [role=log]")).to_contain_text("ordinary case workflow")
        expect(page.get_by_role("button", name="Send", exact=True)).to_be_enabled()
        shared_ui(page, "#employee-chat", "**/api/chat/threads/*/ask", out, "employee", axe)
        employee_stale(page)
        for endpoint in ("skills", "threads", "threads/*/ask"):
            for code in (401, 403, 404):
                if page.get_by_label("Work email", exact=True).is_visible():
                    page.get_by_label("Work email", exact=True).fill("sam@example.test")
                    page.get_by_label("Password", exact=True).fill("synthetic-check")
                    page.get_by_role("button", name="Sign in", exact=True).click()
                pattern = f"**/api/chat/{endpoint}"
                page.route(
                    pattern,
                    lambda route, *, code=code: route.fulfill(
                        status=code, json={"error": "Synthetic access ended"}
                    ),
                )
                page.get_by_role("button", name="Chat", exact=True).click()
                if endpoint != "skills":
                    expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
                    page.get_by_label("Your work question", exact=True).fill("Check access")
                    page.get_by_role("button", name="Send", exact=True).click()
                expect(page.locator("#employee-chat")).to_have_count(0)
                page.unroute(pattern)
        assert not errors, errors
    finally:
        context.close()


def resident(browser: Browser, out: Path, axe: str) -> None:
    fixture = DemoTestCase()
    fixture.setUp()
    fixture.app.allowed_hosts = ("127.0.0.1",)
    base = f"http://127.0.0.1:{fixture.app.port}"
    context = browser.new_context()
    context.route(
        "**/*",
        lambda route: (
            route.continue_() if route.request.url.startswith(base + "/") else route.abort()
        ),
    )
    try:
        page = context.new_page()
        errors: list[str] = []
        calls: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: calls.append(request.url))
        page.goto(base)
        expect(page.locator("#signin")).to_be_visible()
        for asset in ("chat-widget.js", "chat-widget.css"):
            assert page.request.get(base + "/" + asset).body() == (WEB / asset).read_bytes()
        page.get_by_label("Email address", exact=True).fill("one@example.com")
        page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
        page.get_by_role("button", name="Sign in", exact=True).click()
        expect(page.locator("#content")).to_be_visible()
        page.get_by_role("button", name="Chat", exact=True).click()
        panel = page.locator("#resident-chat")
        expect(panel.locator("select option")).to_have_count(1)
        question = panel.locator("textarea")
        question.fill("My home smells like a dead rat")
        panel.get_by_role("button", name="Send", exact=True).click()
        expect(panel.get_by_role("alert")).to_contain_text("Agree to use")
        assert base + "/demo/assistant" not in calls
        page.locator("#assistant-consent").check()
        # Consent alone cannot read data or call a model.
        assert base + "/demo/assistant" not in calls
        question.fill("My home smells like a dead rat")
        panel.get_by_role("button", name="Send", exact=True).click()
        expect(panel.get_by_role("log")).to_contain_text("cannot answer that")
        expect(panel.get_by_role("log")).to_contain_text("housing officer")
        expect(panel.get_by_role("log")).not_to_contain_text("Test Street")
        question.fill("What is my address?")
        panel.get_by_role("button", name="Send", exact=True).click()
        expect(panel.get_by_role("log")).to_contain_text("C-1 Test Street")
        shared_ui(page, "#resident-chat", "**/demo/assistant", out, "resident", axe)
        held: list[Route] = []
        page.route("**/demo/assistant", lambda route: held.append(route))
        question.fill("Obsolete request")
        panel.get_by_role("button", name="Send", exact=True).click()
        expect(panel.locator("form")).to_have_attribute("aria-busy", "true")
        page.wait_for_timeout(30)
        assert len(held) == 1
        page.locator("#assistant-consent").uncheck()
        expect(panel.get_by_role("log")).to_be_empty()
        page.locator("#assistant-consent").check()
        question.fill("New consent request")
        panel.get_by_role("button", name="Send", exact=True).click()
        page.wait_for_timeout(30)
        assert len(held) == 2
        held[0].fulfill(json={"answer": "OBSOLETE", "label": "Summary by rules", "sources": []})
        expect(panel.locator("form")).to_have_attribute("aria-busy", "true")
        expect(panel.get_by_role("log")).not_to_contain_text("OBSOLETE")
        held[1].fulfill(
            json={"answer": "Current consent result", "label": "Summary by rules", "sources": []}
        )
        expect(panel.get_by_role("log")).to_contain_text("Current consent result")
        expect(panel.locator("form")).to_have_attribute("aria-busy", "false")
        page.unroute("**/demo/assistant")
        page.keyboard.press("Escape")
        page.locator("#account summary").click()
        page.get_by_role("button", name="Sign out", exact=True).click()
        expect(page.locator("#assistant-result")).to_be_empty()
        expect(page.locator("#assistant-consent")).not_to_be_checked()
        assert not errors, errors
        assert all(url.startswith(base) for url in calls), calls
        print(
            "PASS resident: actual rat refusal, own record, consent-before-request; "
            "pending withdrawal/re-consent and session clear"
        )
    finally:
        context.close()
        fixture.doCleanups()


def recovery(browser: Browser, base: str) -> None:
    for failures in (1, 99):
        recovery_case(browser, base, failures)
    print(
        "PASS shared script: transient recovery and bounded exhaustion preserve ordinary workflows"
    )


def recovery_case(browser: Browser, base: str, failures: int) -> None:
    context = browser.new_context()
    try:
        page = context.new_page()
        errors: list[str] = []
        attempts: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def asset(route: Route) -> None:
            attempts.append(route.request.url)
            route.abort() if len(attempts) <= failures else route.continue_()

        page.route("**/chat-widget.js", asset)
        page.goto(base + "/app")
        page.get_by_label("Work email", exact=True).fill("sam@example.test")
        page.get_by_label("Password", exact=True).fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
        if failures == 1:
            expect(page.get_by_role("button", name="Chat", exact=True)).to_be_visible()
        else:
            expect(page.locator("#workspace-status")).to_contain_text("Chat could not load")
            assert len(attempts) == 3
            page.evaluate("location.hash = '#/progress'")
            expect(page.locator("#app h1").first).to_be_visible()
            expect(page.locator("#workspace-status")).to_contain_text("Chat could not load")
            assert len(attempts) == 3
        assert not errors, errors
    finally:
        context.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.axe.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Expected pinned axe-core 4.10.3")
    args.out.mkdir(parents=True, exist_ok=True)
    axe = raw.decode()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:

            def check_employee(base: str) -> None:
                employee(browser, base, args.out, axe)
                recovery(browser, base)

            employee_server(check_employee, synthetic_data, synthetic_chat_privacy=True)
            resident(browser, args.out, axe)
            (args.out / "results.json").write_text(
                json.dumps(
                    {
                        "status": "passed",
                        "browser": browser.version,
                        "scope": "owned synthetic loopback apps; intercepted UI edge cases",
                        "live_model": "not run",
                        "human_assistive_technology": "not run",
                    },
                    indent=2,
                )
            )
        finally:
            browser.close()


if __name__ == "__main__":
    main()
