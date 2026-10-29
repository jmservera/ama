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
      document.querySelector('dialog.employee-chat'),
      {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']}}
    )""")
    assert not result["violations"], (state, result["violations"])
    return {"state": state, "violations": result["violations"], "passes": len(result["passes"])}


def run_browser(base: str, axe: str, output: Path) -> None:
    reports = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(reduced_motion="reduce")
        context.route("**/*", lambda route: route.continue_()
                      if route.request.url.startswith(base + "/") else route.abort())
        try:
            page = context.new_page()
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
            expect(question).to_be_focused()
            expect(dialog.locator("select option")).to_have_count(6)
            question.fill("What can chat do?")
            dialog.get_by_role("button", name="Ask", exact=True).click()
            expect(dialog.get_by_role("log")).to_contain_text("ordinary case workflow")
            expect(dialog.get_by_role("log")).to_contain_text("AI suggestion, not approved")
            expect(dialog).to_contain_text("No case or home record is visible")
            expect(dialog.get_by_role("log")).to_have_attribute("aria-live", "polite")
            reports.append(scan(page, axe, "actual-model-unavailable"))
            page.keyboard.press("Escape")
            expect(dialog).to_have_count(0)
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
                page.get_by_role("dialog").get_by_role("button", name="Ask", exact=True).click()
                expect(page.get_by_role("log", name="Employee conversation")).to_contain_text(f"Skill: {skill}.")
                expect(page.get_by_role("log", name="Employee conversation")).to_contain_text("ZF-1/stage")
            reports.append(scan(page, axe, "synthetic-cited-answer"))
            close = page.get_by_role("button", name="Close chat", exact=True)
            close.focus()
            for key in ("Shift+Tab", "Tab", "Tab", "Tab", "Tab", "Tab", "Tab"):
                page.keyboard.press(key)
                assert page.get_by_role("dialog").evaluate(
                    "el => el.contains(document.activeElement)")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                assert page.get_by_role("dialog").evaluate(
                    "el => el.scrollWidth <= el.clientWidth")
            assert page.evaluate("""() => getComputedStyle(
              document.querySelector('dialog')).transitionDuration === '0s'""")

            page.unroute("**/api/chat/threads/*/ask", answer)
            held: list[Route] = []
            page.route("**/api/chat/threads/*/ask", lambda route: held.append(route))
            question.fill("Delayed case question")
            page.get_by_role("dialog").get_by_role("button", name="Ask", exact=True).click()
            page.wait_for_function("() => document.querySelector('dialog [aria-busy=true]')")
            page.evaluate("() => { location.hash = '#/progress'; }")
            expect(page.get_by_role("dialog")).to_have_count(0)
            if held:
                try:
                    answer(held[0])
                except PlaywrightError as error:
                    # The navigation abort is an expected transport failure, not a result.
                    assert "Invalid" in str(error) or "Target" in str(error), str(error)
            launcher.click()
            expect(page.get_by_role("dialog")).not_to_contain_text("Synthetic cited case explanation")
            page.keyboard.press("Escape")
            page.unroute("**/api/chat/threads/*/ask")

            for denied in (403, 404, 401):
                launcher.click()
                expect(page.get_by_label("Agent skill", exact=True)).to_be_enabled()
                question.fill("Check access")
                def denied_reply(route: Route) -> None:
                    route.fulfill(status=denied, json={"error": "Synthetic access ended"})

                page.route("**/api/chat/threads/*/ask", denied_reply)
                page.get_by_role("dialog").get_by_role("button", name="Ask", exact=True).click()
                expect(page.get_by_role("dialog")).to_have_count(0)
                page.unroute("**/api/chat/threads/*/ask")
            expect(page.get_by_label("Work email", exact=True)).to_be_visible()
            expect(launcher).to_be_hidden()
            assert not errors, errors
            print("PASS employee chat: real fallback; all six selections; route/session disposal; keyboard, focus, live, reduced motion, reflow and dialog axe")
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
