"""Bounded resident browser acceptance; deliberately no browser recordings."""

import os

for logging_key in ("DEBUG", "PWDEBUG", "DEBUG_FILE"):
    os.environ.pop(logging_key, None)

import hashlib
import json
import re
import resource
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright


ORIGIN = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUTPUT = Path(__file__).with_name("evidence.json")


def now():
    return datetime.now(timezone.utc).isoformat()


def execute():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    evidence = {
        "task_id": "resident-live-acceptance-2026-10-30",
        "started_at": now(),
        "origin": ORIGIN,
        "script_sha256_before": digest,
        "recording": {
            "screenshots": False, "trace": False, "video": False,
            "har": False, "storage_state_export": False,
        },
        "login_attempts": 0,
        "login_status": None,
        "authenticated": False,
        "stage": "setup",
        "checks": {},
    }
    secrets = []
    browser = None
    context = None

    def safe(text):
        for secret in secrets:
            text = text.replace(secret, "[redacted]")
        return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[redacted-email]", text)

    try:
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch(headless=True)
                evidence["browser"] = browser.version
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900},
                    record_har_path=None,
                    record_video_dir=None,
                    accept_downloads=False,
                )
                page = context.new_page()
                page.set_default_timeout(20000)
                requests = []
                page.on(
                    "request",
                    lambda request: requests.append(now())
                    if request.method == "POST"
                    and request.url == ORIGIN + "/demo/assistant"
                    else None,
                )
                evidence["stage"] = "load_signin"
                page.goto(ORIGIN, wait_until="domcontentloaded", timeout=60000)
                evidence["stage"] = "wait_signin_form"
                page.locator("#signin-form").wait_for(state="visible")
                page.locator("#email").evaluate(
                    "(element) => { element.type = 'password'; }"
                )
                evidence["masked_fields"] = page.locator(
                    "#email[type=password], #password[type=password]"
                ).count() == 2
                if not evidence["masked_fields"]:
                    raise RuntimeError("masking_failed")
                evidence["stage"] = "read_credentials_in_automation"
                with (Path.home() / ".ama-resident-test-user").open() as credential_file:
                    lines = credential_file.read().splitlines()
                if len(lines) != 2 or not all(line.strip() for line in lines):
                    raise ValueError("credential_file_shape")
                secrets = [line.strip() for line in lines]
                del lines
                page.locator("#email").fill(secrets[0])
                page.locator("#password").fill(secrets[1])
                evidence["stage"] = "real_form_submit"
                with page.expect_response(
                    lambda response: response.url == ORIGIN + "/demo/login"
                    and response.request.method == "POST"
                ) as login:
                    evidence["login_attempts"] += 1
                    page.locator("#signin-button").click()
                evidence["login_status"] = login.value.status
                page.wait_for_function(
                    "() => !document.getElementById('signin-error').hidden"
                    " || !document.getElementById('content').hidden"
                    " || !document.getElementById('error').hidden"
                )
                page.locator("#signin-form").evaluate(
                    "el => { el.querySelector('#email').value = '';"
                    " el.querySelector('#password').value = ''; }"
                )
                if evidence["login_status"] == 401:
                    evidence["stage"] = "stopped_on_401"
                    evidence["non_secret_page_text"] = safe(
                        page.locator("#signin-error").inner_text()
                    )
                    evidence["stop_reason"] = "HTTP 401; no retry or further live checks"
                    return evidence
                if evidence["login_status"] != 200:
                    evidence["stage"] = "stopped_on_other_login_status"
                    evidence["non_secret_page_text"] = safe(
                        page.locator("#signin-error").inner_text()
                    )
                    return evidence
                page.locator("#content").wait_for(state="visible")
                evidence["authenticated"] = True
                evidence["stage"] = "authenticated_chat"
                checks = evidence["checks"]
                launcher = page.locator("#chat-launcher")
                checks["launcher"] = launcher.evaluate(
                    """el => { const r = el.getBoundingClientRect(); return {
                      role: el.tagName, name: el.getAttribute('aria-label'),
                      right_gap: innerWidth-r.right, bottom_gap: innerHeight-r.bottom,
                      expanded: el.getAttribute('aria-expanded')
                    }; }"""
                )
                launcher.focus()
                launcher.press("Enter")
                panel = page.locator("#resident-chat")
                panel.wait_for(state="visible")
                checks["dialog_role"] = panel.get_attribute("role")
                question = page.locator("#assistant-question")
                consent = page.locator("#assistant-consent")
                if consent.count() != 1 or not consent.is_visible():
                    checks["initial_consent"] = "indeterminate"
                    evidence["stage"] = "blocked_indeterminate_consent"
                    return evidence
                checks["initial_consent"] = (
                    "already_consented" if consent.is_checked() else "unconsented"
                )
                if not consent.is_checked():
                    before = len(requests)
                    question.fill("My home smells like a dead rat")
                    question.press("Enter")
                    page.locator("#resident-chat-error").wait_for(state="visible")
                    checks["preconsent_error"] = safe(
                        page.locator("#resident-chat-error").inner_text()
                    )
                    checks["preconsent_no_assistant_request"] = len(requests) == before
                    consent.check()
                checks["permission_before_question"] = consent.is_checked()
                checks["permission_at"] = now()
                checks["selector"] = panel.locator("select").evaluate(
                    """el => ({label:el.getAttribute('aria-label'),
                      value:el.value, options:Array.from(el.options, o=>o.textContent)})"""
                )
                checks["capabilities"] = {
                    label: panel.get_by_role("button", name=label, exact=True).is_disabled()
                    for label in ("Attach", "Voice")
                }
                checks["unsupported_reason"] = safe(
                    page.locator("#resident-chat-unsupported").inner_text()
                )
                checks["send_present"] = panel.get_by_role(
                    "button", name="Send", exact=True
                ).is_visible()
                before = len(requests)
                question.fill("First line")
                question.press("Shift+Enter")
                checks["shift_enter_newline"] = question.input_value() == "First line\n"
                checks["shift_enter_no_request"] = len(requests) == before
                question.fill("My home smells like a dead rat")
                question.press("Enter")
                page.locator(".chat-widget-assistant").first.wait_for(state="visible")
                first = page.locator(".chat-widget-assistant").first
                answer = first.locator(":scope > p").first.inner_text()
                honest = bool(re.search(
                    r"(cannot|can't|unable|not able|do not know|don't know)",
                    answer, re.I,
                )) and bool(re.search(r"(housing officer|contact|phone|person)", answer, re.I))
                checks["rat_answer"] = {
                    "honest_inability_and_contact": honest,
                    "home_summary_marker": "home record" in answer.lower(),
                    "text": safe(answer) if honest else "Not retained: inspect relevance manually",
                    "label": safe(first.locator("small").first.inner_text()),
                    "sources_initially_collapsed": first.locator("details").get_attribute("open") is None,
                }
                checks["enter_sent"] = len(requests) == before + 1
                checks["open_after_enter"] = panel.is_visible()
                page.wait_for_function(
                    "() => document.querySelector('.chat-widget-composer')"
                    ".getAttribute('aria-busy') === 'false'"
                )
                question.fill("What is the status of my case?")
                panel.get_by_role("button", name="Send", exact=True).click()
                page.wait_for_function(
                    "() => document.querySelectorAll('.chat-widget-assistant').length >= 2"
                )
                checks["open_after_send_button"] = panel.is_visible()
                checks["thread"] = page.locator("#assistant-result").evaluate(
                    """el => { const s=getComputedStyle(el); return {
                      roles:Array.from(el.children, c=>c.className),
                      role:el.getAttribute('role'), live:el.getAttribute('aria-live'),
                      overflow:s.overflowY, scroll_top:el.scrollTop,
                      client_height:el.clientHeight, scroll_height:el.scrollHeight
                    }; }"""
                )
                checks["answer_labels"] = [
                    safe(label) for label in
                    page.locator(".chat-widget-assistant > small").all_text_contents()
                ]
                checks["viewports"] = []
                for width in (1280, 390, 320):
                    page.set_viewport_size({"width": width, "height": 900})
                    question.focus()
                    checks["viewports"].append(panel.evaluate(
                        """el => { const r=el.getBoundingClientRect();
                          const q=el.querySelector('textarea').getBoundingClientRect();
                          const log=el.querySelector('[role=log]').getBoundingClientRect();
                          const s=getComputedStyle(document.activeElement);
                          return {width:innerWidth, popup_width:r.width,
                            document_overflow:document.documentElement.scrollWidth>innerWidth,
                            popup_in_view:r.left>=0 && r.right<=innerWidth && r.bottom<=innerHeight,
                            composer_below_log:q.top>=log.bottom,
                            focus_outline_width:s.outlineWidth,
                            focus_outline_style:s.outlineStyle}; }"""
                    ))
                checks["motion"] = {}
                for motion in ("no-preference", "reduce"):
                    page.emulate_media(reduced_motion=motion)
                    checks["motion"][motion] = page.evaluate(
                        "() => getComputedStyle(document.documentElement)"
                        ".getPropertyValue('--motion').trim()"
                    )
                question.press("Escape")
                checks["escape_closed"] = not panel.is_visible()
                checks["escape_focus_return"] = launcher.evaluate(
                    "el => el === document.activeElement"
                )
                launcher.press("Enter")
                checks["reopen_retains_four_messages"] = (
                    page.locator(".chat-widget-message").count() == 4
                )
                checks["assistant_post_times"] = requests
                checks["exact_200ms_loading_threshold"] = "Not measured; no delayed/injected response"
                checks["human_screen_reader_conformance"] = "Not performed"
                evidence["stage"] = "resident_checks_complete"
                return evidence
            finally:
                if context is not None:
                    context.close()
                    evidence["context_closed"] = True
                if browser is not None:
                    browser.close()
                    evidence["browser_closed"] = True
    except Exception as error:
        evidence["failure"] = {
            "stage": evidence["stage"],
            "category": type(error).__name__,
            "detail": "Exception text suppressed to protect filled credentials",
        }
        return evidence
    finally:
        evidence["finished_at"] = now()
        evidence["script_sha256_after"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        serialized = json.dumps(evidence, indent=2)
        if any(secret in serialized for secret in secrets):
            raise RuntimeError("Evidence failed credential exclusion check") from None
        evidence["credential_literal_exclusion"] = True
        OUTPUT.write_text(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
    result = execute()
    print(json.dumps({
        "stage": result["stage"],
        "login_status": result["login_status"],
        "authenticated": result["authenticated"],
        "evidence": str(OUTPUT),
    }))
