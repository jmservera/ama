"""Local HTTP/UI evidence with constructed residents and scripted inference, never cloud."""

import argparse
import json
from dataclasses import replace
from pathlib import Path
from typing import Any
from unittest.mock import Mock

from playwright.sync_api import Route, expect, sync_playwright
from test_resident_aoai import ENDPOINT, question_reply
from test_resident_demo_api import FAKE_PASSWORD, DemoTestCase

from zava_forward.api.resident_demo.aoai import AzureAdvisor
from zava_forward.api.resident_demo.assistant import EXPIRES


def run(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=False)
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
                question.fill("My home smells like a dead rat")
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
                assert content["question"] == "My home smells like a dead rat"
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
                mode["unavailable"] = True
                question.fill("My home smells strange")
                send.click()
                latest = page.locator("#assistant-result .chat-widget-assistant").last
                expect(latest).to_contain_text("AI unavailable or usage limit reached")
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
    run(parser.parse_args().out)
