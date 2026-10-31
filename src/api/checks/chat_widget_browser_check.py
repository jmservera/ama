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

from checks.asset_urls import asset_url
from checks.chat_submit_browser_check import employee as submit_employee
from checks.design_system_browser_check import main as employee_server
from checks.design_system_browser_check import synthetic_data
from checks.regulatory_ux_check import AXE_SHA256

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


def focused_control_visible(page: Page) -> None:
    assert page.evaluate("""() => {
      const el = document.activeElement, r = el.getBoundingClientRect();
      const x = (Math.max(0, r.left) + Math.min(innerWidth, r.right)) / 2;
      const y = (Math.max(0, r.top) + Math.min(innerHeight, r.bottom)) / 2;
      return r.width > 0 && r.height > 0 && x >= 0 && x < innerWidth
        && y >= 0 && y < innerHeight && el.contains(document.elementFromPoint(x, y));
    }"""), "Focused control is obscured or outside the viewport"


def external_note(page: Page) -> None:
    page.evaluate("""() => {
      const note = document.createElement('textarea');
      note.id = 'focus-check-note';
      note.setAttribute('aria-label', 'Synthetic external work note');
      note.style.cssText = 'position:fixed;right:24px;top:120px;width:120px;height:60px';
      document.body.append(note);
    }""")


def short_window_launcher(page: Page, root: str) -> None:
    panel = page.locator(root)
    launcher = page.get_by_role("button", name="Chat", exact=True)
    page.set_viewport_size({"width": 1280, "height": 500})
    panel.locator("h2").focus()
    page.keyboard.press("Shift+Tab")
    expect(launcher).to_be_focused()
    expect(panel).to_be_visible()
    focused_control_visible(page)
    launcher.click()
    expect(panel).to_be_hidden()
    launcher.click()
    expect(panel).to_be_visible()
    page.set_viewport_size({"width": 1280, "height": 900})


def current_reply_focus(page: Page, root: str, endpoint: str) -> None:
    panel = page.locator(root)
    launcher = page.get_by_role("button", name="Chat", exact=True)
    question = panel.locator("textarea")
    send = panel.get_by_role("button", name="Send", exact=True)
    external_note(page)
    try:
        for outcome in ("success", "error"):
            for target in ("external", "launcher", "internal"):
                if not panel.is_visible():
                    launcher.click()
                held: list[Route] = []
                page.route(endpoint, lambda route, *, held=held: held.append(route))
                question.fill(f"Current {outcome} {target}")
                send.click()
                page.wait_for_function(
                    "() => document.querySelector('.chat-widget form')"
                    ".getAttribute('aria-busy') === 'true'"
                )
                chosen = (
                    page.locator("#focus-check-note")
                    if target == "external"
                    else launcher
                    if target == "launcher"
                    else panel.locator("h2")
                )
                chosen.focus()
                expect(panel).to_be_hidden() if target == "external" else expect(
                    panel
                ).to_be_visible()
                assert len(held) == 1
                if outcome == "success":
                    held[0].fulfill(
                        json={
                            "answer": "Current focus-safe reply",
                            "reply": "Current focus-safe reply",
                            "label": "Summary by rules",
                            "workflow_only": True,
                            "citations": [],
                            "sources": [],
                        }
                    )
                else:
                    held[0].fulfill(status=503, json={"error": "Current focus-safe failure"})
                expect(panel.locator("form")).to_have_attribute("aria-busy", "false")
                expect(chosen).to_be_focused()
                focused_control_visible(page)
                expect(panel.locator('[role="log"]')).to_have_attribute("aria-live", "polite")
                if outcome == "success":
                    expect(panel.locator('[role="log"]')).to_contain_text(
                        "Current focus-safe reply"
                    )
                    expect(question).to_have_value("")
                else:
                    expect(panel.locator('[role="alert"]')).to_have_attribute("aria-live", "polite")
                    expect(panel.locator('[role="alert"]')).to_contain_text(
                        "Current focus-safe failure"
                    )
                    expect(question).to_have_value(f"Current {outcome} {target}")
                if target == "external":
                    expect(panel).to_be_hidden()
                    launcher.click()
                    expect(panel).to_be_visible()
                page.unroute(endpoint)
    finally:
        page.locator("#focus-check-note").evaluate("el => el.remove()")


def scan(page: Page, axe: str, root: str) -> None:
    page.evaluate(axe)
    violations = page.evaluate(
        """async root => (await axe.run(document.querySelector(root), {
          runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag22aa']}
        })).violations""",
        root,
    )
    assert not violations, violations


def close_hover(page: Page, root: str, audience: str) -> None:
    close = page.locator(root).get_by_role("button", name="Close chat", exact=True)
    close.hover()
    ratio = close.evaluate("""el => {
      const style = getComputedStyle(el);
      const luminance = color => {
        const rgb = color.match(/[\\d.]+/g).slice(0, 3).map(Number);
        return rgb.map(v => v / 255).map(v =>
          v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4
        ).reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0);
      };
      const foreground = luminance(style.color), background = luminance(style.backgroundColor);
      return (Math.max(foreground, background) + .05)
        / (Math.min(foreground, background) + .05);
    }""")
    assert ratio >= 4.5, f"{audience} Close chat hover contrast: {ratio:.2f}:1"
    page.mouse.move(0, 0)
    print(f"PASS {audience}: Close chat hover contrast {ratio:.2f}:1 >= 4.5:1")


def reply_scroll(page: Page, root: str, endpoint: str, audience: str) -> None:
    panel = page.locator(root)
    log = panel.get_by_role("log")
    question = panel.locator("textarea")
    send = panel.get_by_role("button", name="Send", exact=True)
    for mode in (
        "older",
        "sources-older",
        "sources-bottom",
        "log-bottom",
        "follow",
        "older-before-loading",
        "sources-before-loading",
    ):
        held: list[Route] = []
        page.route(endpoint, lambda route, *, held=held: held.append(route))
        try:
            question.fill(f"Scroll regression {mode}")
            chosen = question
            if mode == "follow":
                if audience == "resident":
                    expect(panel.locator('[role="status"]')).to_be_empty()
                log.evaluate("el => { el.scrollTop = el.scrollHeight; }")
                assert log.evaluate("el => el.scrollHeight > el.clientHeight")
            send.click()
            expect(panel.locator("form")).to_have_attribute("aria-busy", "true")
            page.wait_for_function(
                "() => document.querySelector('.chat-widget form')"
                ".getAttribute('aria-busy') === 'true'"
            )
            assert len(held) == 1
            if mode == "follow":
                assert log.evaluate(
                    "el => Math.abs(el.scrollHeight - el.clientHeight - el.scrollTop) <= 2"
                ), (audience, "send/status lost bottom-follow intent")
            elif mode.endswith("before-loading"):
                if mode == "older-before-loading":
                    log.evaluate("el => { el.scrollTop = 0; }")
                else:
                    chosen = log.locator("summary").last
                    chosen.focus()
                    log.evaluate("el => { el.scrollTop = el.scrollHeight; }")
                before_loading = log.evaluate("el => el.scrollTop")
            expect(panel.locator(".chat-widget-loading")).to_be_hidden()
            page.clock.run_for(200)
            expect(panel.locator(".chat-widget-loading")).to_be_visible()
            assert log.evaluate("el => el.scrollHeight > el.clientHeight")
            if mode == "follow":
                assert log.evaluate(
                    "el => Math.abs(el.scrollHeight - el.clientHeight - el.scrollTop) <= 2"
                ), (audience, "loading lost bottom-follow intent")
            elif mode.endswith("before-loading"):
                assert abs(log.evaluate("el => el.scrollTop") - before_loading) <= 1
            elif mode.startswith("sources"):
                summaries = log.locator("summary")
                chosen = summaries.first if mode == "sources-older" else summaries.last
            elif mode == "log-bottom":
                chosen = log
            if mode != "follow":
                chosen.focus()
            focused = chosen.element_handle()
            assert focused is not None
            if mode in ("older", "sources-older"):
                if mode == "older":
                    log.evaluate("el => { el.scrollTop = 0; }")
            elif mode not in ("follow", "older-before-loading", "sources-before-loading"):
                log.evaluate("el => { el.scrollTop = el.scrollHeight; }")
            before = log.evaluate("el => el.scrollTop")
            focused_control_visible(page)
            held[0].fulfill(
                json={
                    "answer": f"Scroll result {mode}. " + "Long fictional reply. " * 60,
                    "reply": f"Scroll result {mode}. " + "Long fictional reply. " * 60,
                    "label": "Summary by rules",
                    "workflow_only": True,
                    "sources": ["Synthetic own-case source"],
                    "citations": [{"id": "ZF-1/stage", "text": "Survey"}],
                }
            )
            expect(log).to_contain_text(f"Scroll result {mode}.")
            expect(panel.locator("form")).to_have_attribute("aria-busy", "false")
            assert focused.evaluate("el => el === document.activeElement"), (
                audience,
                mode,
                "Reply moved focus",
            )
            if mode == "follow":
                distance = log.evaluate(
                    "el => Math.abs(el.scrollHeight - el.clientHeight - el.scrollTop)"
                )
                assert distance <= 2, (audience, "bottom reader did not follow reply", distance)
            else:
                after = log.evaluate("el => el.scrollTop")
                assert abs(after - before) <= 1, (audience, mode, before, after)
            focused_control_visible(page)
        finally:
            page.unroute(endpoint)
    print(
        f"PASS {audience}: pre-send bottom follows delayed loading/reply without repositioning; "
        "older history and focused Sources/log stay put before/after loading"
    )


def employee_stacking(page: Page, out: Path) -> None:
    page.evaluate("location.hash = '#/overview'")
    expect(page.get_by_role("heading", name="Overview", exact=True)).to_be_visible()
    expect(page.locator(".map-cluster").first).to_be_attached()
    page.locator("#mapArea").select_option(label="Point examples")
    expect(page.locator(".map-marker")).to_have_count(3)
    page.locator(".map-marker:has(.map-symbol.hazard)").press("Enter")
    expect(page.locator(".map-home-card")).to_be_visible()
    page.locator("#leaflet").evaluate("el => el.scrollIntoView({block: 'center'})")
    page.get_by_role("button", name="Chat", exact=True).click()
    expect(page.locator("#employee-chat select")).to_be_enabled()
    expect(page.locator(".leaflet-map-pane")).to_be_attached()
    results = page.evaluate("""() => {
      const panel = document.querySelector('#employee-chat');
      const launcher = document.querySelector('#employee-chat-launcher');
      const results = [];
      try {
        for (const selector of ['#leaflet', '.leaflet-control-zoom', '.map-home-card']) {
          const target = document.querySelector(selector), r = target.getBoundingClientRect();
          const x = (Math.max(0, r.left) + Math.min(innerWidth, r.right)) / 2;
          const y = (Math.max(0, r.top) + Math.min(innerHeight, r.bottom)) / 2;
          for (const el of [panel, launcher]) {
            panel.hidden = el !== panel;
            el.style.cssText = `left:${x - 24}px;top:${y - 24}px;right:auto;bottom:auto`;
            const stack = document.elementsFromPoint(x, y);
            results.push({selector, control:el.id, above:el.contains(stack[0]),
              overlaps:stack.some(node => target.contains(node)),
              tier:Number(getComputedStyle(el).zIndex)});
            el.removeAttribute('style');
          }
        }
        panel.hidden = false;
        window.scrollTo(0, 0);
        const account = document.querySelector('#account');
        account.open = true;
        try {
          const menu = account.querySelector('.account-panel'), r = menu.getBoundingClientRect();
          const x = r.left + 24, y = r.top + 24;
          for (const el of [panel, launcher]) {
            panel.hidden = el !== panel;
            el.style.cssText = `left:${x - 12}px;top:${y - 12}px;right:auto;bottom:auto`;
            const stack = document.elementsFromPoint(x, y);
            results.push({selector:'.account-panel', control:el.id,
              above:menu.contains(stack[0]), overlaps:stack.some(node => el.contains(node)),
              tier:Number(getComputedStyle(el).zIndex)});
            el.removeAttribute('style');
          }
        } finally { account.open = false; }
      } finally {
        panel.hidden = false;
        panel.removeAttribute('style');
        launcher.removeAttribute('style');
      }
      return results;
    }""")
    assert len(results) == 8
    assert all(
        item["above"] and item["overlaps"] and 1000 < item["tier"] < 1200 for item in results
    ), results
    (out / "employee-stacking.json").write_text(json.dumps(results, indent=2))
    page.keyboard.press("Escape")
    print("PASS employee: popup/launcher above real map, controls, home card; below account menu")


def employee_refresh(page: Page) -> None:
    page.evaluate("location.hash = '#/coordinator?as_of=2026-01-01T00%3A00%3A00Z'")
    expect(page.get_by_role("button", name="Apply coordinator filters", exact=True)).to_be_visible()
    launcher = page.get_by_role("button", name="Chat", exact=True)
    launcher.click()
    panel = page.locator("#employee-chat")
    expect(panel.locator("select")).to_be_enabled()
    panel.locator("textarea").fill("Retained refresh draft")
    page.evaluate("""() => {
      window.refreshChat = {
        panel:document.querySelector('#employee-chat'),
        toggle:document.querySelector('#employee-chat-launcher').onclick,
        icon:document.querySelector('#employee-chat-launcher svg')
      };
    }""")
    try:
        for opened, area in ((True, "Point examples"), (False, "Cluster examples")):
            if panel.is_visible() != opened:
                launcher.click()
            with page.expect_response("**/api/coordinator?**"):
                page.locator(".coordinator-filters").evaluate(
                    """(form, area) => {
                  form.querySelector('[name=area]').value = area;
                  form.requestSubmit();
                }""",
                    area,
                )
            expect(page.locator("#co-area")).to_have_value(area)
            assert page.evaluate("""() => {
              const button = document.querySelector('#employee-chat-launcher');
              return document.querySelector('#employee-chat') === refreshChat.panel
                && button.onclick === refreshChat.toggle
                && button.querySelector('svg') === refreshChat.icon;
            }"""), "Same-context route refresh replaced widget, toggle or decoration"
            expect(panel).to_be_visible() if opened else expect(panel).to_be_hidden()
            expect(launcher).to_have_attribute("aria-expanded", str(opened).lower())
            if opened:
                expect(panel.locator("textarea")).to_be_focused()
                launcher.click()
            else:
                expect(launcher).to_be_focused()
            expect(panel).to_be_hidden()
            focused_control_visible(page)
            launcher.click()
            expect(panel).to_be_visible()
            expect(launcher).to_have_attribute("aria-expanded", "true")
            launcher.click()
            expect(panel).to_be_hidden()
            expect(launcher).to_have_attribute("aria-expanded", "false")
            expect(panel.locator("textarea")).to_have_value("Retained refresh draft")
            launcher.click()
            panel.locator("h2").focus()
            focused_control_visible(page)
    finally:
        page.evaluate("delete window.refreshChat")
        page.evaluate("employeeChat.reset()")
    print("PASS employee: actual coordinator filter refresh retains open/closed launcher toggle")


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
    close_hover(page, root, audience)
    page.clock.install(time=datetime(2030, 1, 1, tzinfo=UTC))
    page.clock.pause_at(datetime(2030, 1, 1, 0, 0, 1, tzinfo=UTC))
    reply_scroll(page, root, endpoint, audience)
    page.clock.resume()
    page.route(endpoint, answer)
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
    short_window_launcher(page, root)
    for key in ("Tab", "Shift+Tab"):
        (send if key == "Tab" else panel.locator("h2")).focus()
        left = False
        for _ in range(12):
            page.keyboard.press(key)
            inside = panel.evaluate("el => el.contains(document.activeElement)")
            at_launcher = page.get_by_role("button", name="Chat", exact=True).evaluate(
                "el => el === document.activeElement"
            )
            at_page_control = page.evaluate(
                "document.activeElement !== document.body && "
                "document.activeElement !== document.documentElement"
            )
            if not inside and not at_launcher and at_page_control:
                left = True
                break
        assert left, "Nonmodal chat trapped keyboard traversal"
        expect(panel).to_be_hidden()
        focused_control_visible(page)
        page.get_by_role("button", name="Chat", exact=True).click()
        expect(question).to_have_value("Draft survives closing")
        expect(log).to_contain_text("answer 4.")
    page.clock.pause_at(page.evaluate("Date.now() + 1000"))
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
    current_reply_focus(page, root, endpoint)
    print(
        f"PASS {audience}: thread, pinned input, keyboard, labels, controls; "
        "200ms loading, errors, unobscured external focus, "
        "no current-reply focus theft, axe, reflow"
    )


def employee_current_focus(page: Page) -> None:
    external_note(page)
    try:
        for stage in ("skills", "status", "thread", "ask"):
            for outcome in ("success", "error", "403", "404"):
                for target in ("external", "launcher", "internal"):
                    page.evaluate(
                        """stage => {
                      employeeChat.reset();
                      const state = window.currentChat = {api, stage};
                      api = (path, body, signal) => {
                        const hold = stage === 'skills' ? path === '/api/chat/skills'
                          : stage === 'status' ? path === '/api/chat/status'
                          : stage === 'thread' ? path === '/api/chat/threads'
                          : path.endsWith('/ask');
                        if (!hold) return state.api(path, body, signal);
                        return new Promise((resolve, reject) => {
                          state.resolve = resolve; state.reject = reject;
                        });
                      };
                      state.task = employeeChat.open();
                    }""",
                        stage,
                    )
                    panel = page.locator("#employee-chat")
                    expect(panel).to_be_visible()
                    if stage in ("thread", "ask"):
                        expect(panel.locator("select")).to_be_enabled()
                        expect(panel.locator("h2")).to_be_focused()
                        panel.locator("textarea").fill("Current controlled question")
                        page.evaluate("""() => {
                          currentChat.task = document.querySelector('#employee-chat form')
                            .onsubmit(new Event('submit', {cancelable: true}));
                        }""")
                    page.wait_for_function("() => typeof currentChat.resolve === 'function'")
                    chosen = (
                        page.locator("#focus-check-note")
                        if target == "external"
                        else page.locator("#employee-chat-launcher")
                        if target == "launcher"
                        else panel.locator("h2")
                    )
                    chosen.focus()
                    page.evaluate(
                        """async outcome => {
                      const state = currentChat;
                      api = state.api;
                      if (outcome === 'success') state.resolve(
                        state.stage === 'skills' ? {skills: []}
                        : state.stage === 'status'
                          ? {warning:'Synthetic warning', retention:'Local'}
                        : state.stage === 'thread' ? await state.api('/api/chat/threads', {})
                        : {reply:'Current controlled reply', citations:[], workflow_only:true});
                      else {
                        const error = new Error('Current controlled failure');
                        if (outcome !== 'error') error.status = Number(outcome);
                        state.reject(error);
                      }
                      await state.task;
                    }""",
                        outcome,
                    )
                    denied = outcome in ("403", "404")
                    if denied:
                        expect(panel).to_have_count(0)
                        expect(
                            page.locator("#app") if target == "internal" else chosen
                        ).to_be_focused()
                    else:
                        expect(chosen).to_be_focused()
                        if target == "external":
                            expect(panel).to_be_hidden()
                        else:
                            expect(panel).to_be_visible()
                        expect(panel.locator("form")).to_have_attribute("aria-busy", "false")
                        if outcome == "error":
                            expect(panel.locator('[role="alert"]')).to_have_attribute(
                                "aria-live", "polite"
                            )
                            expect(panel.locator('[role="alert"]')).to_contain_text(
                                "Current controlled failure"
                            )
                        if stage in ("thread", "ask"):
                            expect(panel.locator("textarea")).to_have_value(
                                "" if outcome == "success" else "Current controlled question"
                            )
                    focused_control_visible(page)
                    page.evaluate("() => { employeeChat.reset(); delete window.currentChat; }")
    finally:
        page.locator("#focus-check-note").evaluate("el => el.remove()")
    print("PASS employee: 48 current setup/thread/ask focus and denial combinations")


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
                else:
                    destination = page.evaluate("location.hash")
                    expect(page.locator("#app h1").first).to_have_text(
                        "Progress dashboard" if destination == "#/progress" else "My cases today"
                    )
                    expect(
                        page.get_by_text("Loading demonstration data\u2026", exact=True)
                    ).to_have_count(0)
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
        employee_stacking(page, out)
        employee_refresh(page)
        employee_current_focus(page)
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
        page.set_viewport_size({"width": 320, "height": 800})
        page.get_by_role("button", name="Chat", exact=True).click()
        page.keyboard.press("Shift+Tab")
        page.keyboard.press("Shift+Tab")
        expect(page.locator("#signin-button")).to_be_focused()
        expect(page.locator("#resident-chat")).to_be_hidden()
        focused_control_visible(page)
        page.screenshot(path=str(out / "resident-external-focus-320.png"))
        page.set_viewport_size({"width": 1280, "height": 900})
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
        expect(panel.get_by_role("log")).to_contain_text("cannot confirm the cause")
        expect(panel.get_by_role("log")).to_contain_text("AI is not enabled")
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
            "PASS resident: explicit disabled-AI repair fallback, own record, consent-before-request; "
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
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(base + "/") else route.abort())
    try:
        page = context.new_page()
        errors: list[str] = []
        attempts: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def asset(route: Route) -> None:
            attempts.append(route.request.url)
            route.abort() if len(attempts) <= failures else route.continue_()

        page.route(asset_url("/chat-widget.js", base), asset)
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
                submit_employee(browser, base, args.out)
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
