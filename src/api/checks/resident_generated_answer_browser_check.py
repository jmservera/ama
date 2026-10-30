"""Local HTTP/UI evidence with constructed residents and scripted inference, never cloud."""

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any
from unittest.mock import Mock

from playwright.sync_api import Page, Route, expect, sync_playwright
from test_resident_aoai import ENDPOINT, question_reply
from test_resident_demo_api import FAKE_PASSWORD, DemoTestCase

from zava_forward.api.resident_demo.aoai import AzureAdvisor
from zava_forward.api.resident_demo.assistant import EXPIRES
from checks.regulatory_ux_check import AXE_SHA256


def sizing(page: Page, out: Path, axe: str | None) -> list[dict[str, Any]]:
    panel = page.locator("#resident-chat")
    log = panel.get_by_role("log")
    question = panel.locator("textarea")
    dock = panel.get_by_role("button", name="Dock to right edge", exact=True)
    sizes = panel.locator(".chat-widget-size")
    sizes.locator("summary").click()
    width = panel.get_by_label("Preferred width (% of screen)")
    height = panel.get_by_label("Preferred height (% of screen)")
    question.fill("Retained resize draft")
    count = log.locator("article").count()
    records: list[dict[str, Any]] = []
    for follow in (False, True):
        for control, key in (
            (width, "End"), (width, "Home"), (height, "Home"),
            (height, "End"), (dock, "Enter"), (dock, "Enter"),
        ):
            control.focus()
            log.evaluate(
                "(el, follow) => { el.scrollTop = follow ? el.scrollHeight : 100; }", follow
            )
            before = log.evaluate("""el => {
              const top = el.getBoundingClientRect().top;
              const i = [...el.children].findIndex(x => x.getBoundingClientRect().bottom > top);
              const box = el.children[i].getBoundingClientRect();
              return {i, fraction:(top-box.top)/box.height};
            }""")
            old_box = panel.bounding_box()
            control.press(key)
            expect(control).to_be_focused()
            after = log.evaluate("""(el, before) => {
              const box = el.children[before.i].getBoundingClientRect();
              return {fraction:(el.getBoundingClientRect().top-box.top)/box.height,
                bottom:el.scrollHeight-el.clientHeight-el.scrollTop};
            }""", before)
            if follow:
                assert abs(after["bottom"]) <= 3, after
            else:
                assert abs(after["fraction"] - before["fraction"]) <= .02, (before, after)
            expect(question).to_have_value("Retained resize draft")
            assert log.locator("article").count() == count
            box = panel.bounding_box()
            assert box and old_box
            delta = (
                box["width"] - old_box["width"]
                if control == width
                else box["height"] - old_box["height"]
            )
            assert abs(delta) > 1, (old_box, box)
            records.append({"following": follow, "key": key, "before": before, "after": after, "box": box})
    old_box = panel.bounding_box()
    width.click(position={"x": 80, "y": 12})
    expect(width).to_be_focused()
    assert width.input_value() != "20"
    box = panel.bounding_box()
    assert box and old_box and abs(box["width"] - old_box["width"]) > 1
    preferred = int(width.input_value())
    width.press("ArrowRight")
    expect(width).to_have_value(str(preferred + 1))
    expect(width).to_be_focused()
    dock.focus()
    dock.press("Enter")
    expect(dock).to_have_attribute("aria-pressed", "true")
    expect(height).to_be_disabled()
    expect(page.locator("#chat-launcher")).to_be_hidden()
    for screen_width, screen_height in ((1280, 900), (390, 900), (320, 900), (1280, 500)):
        page.set_viewport_size({"width": screen_width, "height": screen_height})
        for scale in (100, 200):
            page.evaluate("n => document.documentElement.style.fontSize = n + '%'", scale)
            box = panel.bounding_box()
            assert box and abs(box["y"]) <= 1 and abs(box["height"] - screen_height) <= 1
            assert abs(box["x"] + box["width"] - screen_width) <= 1
            assert box["x"] >= 0
            assert panel.evaluate("el => el.scrollWidth <= el.clientWidth")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            if axe:
                page.evaluate(axe)
                violations = page.evaluate("""async () => (await axe.run(
                  document.querySelector('#resident-chat'), {
                    runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}
                  })).violations""")
                assert not violations, violations
            for control in (width, question, panel.get_by_role("button", name="Send", exact=True)):
                control.focus()
                expect(control).to_be_in_viewport()
                assert control.evaluate("""el => {
                  const r = el.getBoundingClientRect();
                  const x = r.left + r.width/2, y = r.top + r.height/2;
                  return el.contains(document.elementFromPoint(x,y));
                }"""), "Docked control is obscured"
            log.focus()
            log.press("End")
            page.wait_for_function("""() => {
              const el = document.querySelector('#resident-chat [role="log"]');
              return el.scrollHeight-el.clientHeight-el.scrollTop <= 3;
            }""")
            page.screenshot(path=str(out / f"docked-{screen_width}-{screen_height}-{scale}.png"))
            records.append({"viewport": [screen_width, screen_height], "text_percent": scale, "box": box})
    page.evaluate("document.documentElement.style.fontSize = ''")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    launcher = page.get_by_role("button", name="Chat", exact=True)
    expect(launcher).to_be_focused()
    launcher.press("Enter")
    expect(panel).to_be_visible()
    expect(launcher).to_be_hidden()
    dock.focus()
    dock.press("Enter")
    expect(dock).to_have_attribute("aria-pressed", "false")
    expect(height).to_be_enabled()
    expect(launcher).to_be_visible()
    sizes.locator("summary").click()
    expect(question).to_have_value("Retained resize draft")
    question.fill("")
    return records


def run(out: Path, axe_path: Path | None = None) -> None:
    out.mkdir(parents=True, exist_ok=False)
    axe = None
    if axe_path:
        raw = axe_path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == AXE_SHA256
        axe = raw.decode("utf-8")
    fixture = DemoTestCase()
    fixture.setUp()
    fixture.app.allowed_hosts = ("127.0.0.1",)
    fixture.reader.rows["C-1"] = replace(fixture.reader.rows["C-1"], stage="Survey being booked")
    prompts: list[dict[str, Any]] = []
    mode = {"unavailable": False}
    generated = (
        "You mentioned a dead-rat-like smell. Your recorded survey update does not explain "
        "the cause. I cannot confirm what is causing it. Ask your housing officer how to "
        "report it, including where it is and when it started. "
    ) * 4 + (
        "<script>window.injected = true</script>"
    )

    def transport(url: str, data: bytes, token: str) -> bytes:
        prompts.append(json.loads(data))
        if mode["unavailable"]:
            raise OSError("Constructed model outage")
        return question_reply(generated)

    accounting = Mock()
    accounting.reserve.return_value = "constructed-ticket"
    fixture.app.assistant_advisor = AzureAdvisor(
        ENDPOINT,
        accounting,
        lambda: "FAKE-LOCAL-TOKEN",
        transport=transport,
        clock=lambda: EXPIRES - 10,
    )
    base = f"http://127.0.0.1:{fixture.app.port}"
    external: list[str] = []
    errors: list[str] = []
    geometries: list[dict[str, Any]] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 900})

            def local_only(route: Route) -> None:
                if route.request.url.startswith(base + "/"):
                    route.continue_()
                else:
                    external.append(route.request.url)
                    route.abort()

            context.route("**/*", local_only)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            requests: list[str] = []
            page.on("request", lambda request: requests.append(request.url))
            try:
                page.goto(base, wait_until="domcontentloaded")
                expect(page.locator("#signin")).to_be_visible()
                page.get_by_label("Email address", exact=True).fill("one@example.com")
                page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
                page.get_by_role("button", name="Sign in", exact=True).click()
                expect(page.locator("#content")).to_be_visible()
                page.get_by_role("button", name="Chat", exact=True).click()
                panel = page.locator("#resident-chat")
                question = page.locator("#assistant-question")
                send = panel.get_by_role("button", name="Send", exact=True)
                question.fill("My home smells like a dead rat")
                question.press("Enter")
                expect(panel.get_by_role("alert")).to_contain_text("Agree to use")
                assert base + "/demo/assistant" not in requests
                assert not prompts
                accounting.reserve.assert_not_called()
                consent = page.locator("#assistant-consent")
                expect(consent.locator("..")).to_contain_text("question and limited own-case")
                consent.check()
                assert not prompts
                question.fill("There is a smell of dead rat in my house")
                question.focus()
                with page.expect_response("**/demo/assistant") as response:
                    question.press("Enter")
                assert response.value.status == 200
                assert response.value.json()["label"] == "AI-generated"
                latest = page.locator("#assistant-result .chat-widget-assistant").last
                expect(latest).to_contain_text(generated)
                expect(latest).to_contain_text("Not approved")
                expect(latest).to_contain_text("AI-generated content may be incorrect")
                expect(latest).to_contain_text("housing officer")
                expect(latest).to_contain_text("cannot submit forms")
                expect(latest).to_contain_text("Chat cannot confirm the cause")
                expect(latest).to_contain_text("has not sent a report")
                assert latest.locator("script").count() == 0
                assert page.evaluate("window.injected === undefined")
                expect(question).to_be_focused()
                expect(panel).to_be_visible()
                assert len(prompts) == 1
                content = json.loads(prompts[0]["messages"][1]["content"])
                assert content["question"] == "There is a smell of dead rat in my house"
                assert "arranging a survey" in content["sources"]["case"]
                for excluded in ("C-1", "C-2", "Test Street", "example.com"):
                    assert excluded not in json.dumps(prompts)
                details = latest.locator("details")
                assert details.evaluate("el => !el.open")
                summary = details.locator("summary")
                summary.focus()
                summary.press("Enter")
                expect(details).to_have_attribute("open", "")
                expect(details).to_contain_text("Your case: Where things are")
                summary.press("Enter")
                assert details.evaluate("el => !el.open")
                label = latest.locator(".chat-widget-meta").first
                expect(label).to_have_text("AI-generated")
                geometry = label.evaluate(
                    """el => {
                      const style = getComputedStyle(el);
                      return {height:el.getBoundingClientRect().height,
                        font:parseFloat(style.fontSize), weight:style.fontWeight,
                        padding:style.padding, border:style.borderWidth,
                        bodyFont:parseFloat(getComputedStyle(el.parentElement).fontSize)};
                    }"""
                )
                assert geometry["height"] <= 24
                assert geometry["font"] <= geometry["bodyFont"] * 0.85
                assert geometry["weight"] == "400"
                assert geometry["padding"] == geometry["border"] == "0px"
                question.focus()
                for width in (1280, 390, 320):
                    page.set_viewport_size({"width": width, "height": 900})
                    for scale in (100, 200):
                        page.evaluate(
                            "n => document.documentElement.style.fontSize = n + '%'", scale
                        )
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                        box = panel.bounding_box()
                        assert box and 0 <= box["x"] and box["x"] + box["width"] <= width
                        assert panel.evaluate("el => el.scrollWidth <= el.clientWidth")
                        label.scroll_into_view_if_needed()
                        geometries.append({"width": width, "text_percent": scale, "panel": box})
                        page.screenshot(path=str(out / f"generated-{width}-{scale}.png"))
                page.evaluate("document.documentElement.style.fontSize = ''")
                page.set_viewport_size({"width": 1280, "height": 900})
                page.emulate_media(reduced_motion="reduce")
                assert (
                    page.evaluate(
                        "getComputedStyle(document.documentElement).getPropertyValue('--motion').trim()"
                    )
                    == "0s"
                )
                size_results = sizing(page, out, axe)
                mode["unavailable"] = True
                question.fill("My home smells strange")
                send.click()
                latest = page.locator("#assistant-result .chat-widget-assistant").last
                expect(latest).to_contain_text("AI unavailable: the AI service could not provide a verified reply")
                expect(latest).to_contain_text("cannot confirm the cause")
                expect(latest).to_contain_text("housing officer")
                expect(latest).to_contain_text("has not sent a report")
                page.screenshot(path=str(out / "unavailable.png"))
                fixture.app.assistant_advisor = None
                question.fill("My home smells strange")
                send.click()
                expect(
                    page.locator("#assistant-result .chat-widget-assistant").last
                ).to_contain_text("AI is not enabled")
                consent.uncheck()
                expect(page.locator("#assistant-result")).to_be_empty()
                assert len(prompts) == 2
                assert not external and not errors
                result = {
                    "status": "Passed",
                    "browser": browser.version,
                    "model": "Scripted Azure transport; no actual model or cloud call",
                    "consent_before_request_and_reservation": True,
                    "own_case_grounding_and_cross_case_exclusion": True,
                    "thin_label": geometry,
                    "sources_initially_collapsed_keyboard_operable": True,
                    "generated_html_rendered_as_text": True,
                    "unavailable_and_disabled_fallback": True,
                    "consent_withdrawal_clears_thread": True,
                    "reduced_motion": "0s",
                    "geometry": geometries,
                    "sizing_and_docking": size_results,
                    "docked_expanded_controls_axe": "Passed" if axe else "Not run",
                    "external_requests": external,
                    "page_errors": errors,
                    "human_AT_live_acceptance": "Not run",
                }
                (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
                print("PASS local generated-answer HTTP/UI contracts; actual model/live not run")
            finally:
                context.close()
                browser.close()
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--axe", type=Path)
    args = parser.parse_args()
    run(args.out, args.axe)
