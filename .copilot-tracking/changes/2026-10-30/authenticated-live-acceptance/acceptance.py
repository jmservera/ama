"""Bounded live acceptance. Never emit credentials or raw authentication data."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

EMPLOYEE = (
    "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
)
RESIDENT = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
USERNAME = "AadiK@DIAx90853289.OnMicrosoft.com"
OUT = Path(__file__).resolve().parent


def now():
    return datetime.now(UTC).isoformat()


def credential():
    raw = (Path.home() / ".ama-test-user").read_text().strip()
    if raw.startswith("{"):
        value = json.loads(raw)
        password = value.get("password") or value.get("Password")
        if not isinstance(password, str) or not password:
            raise ValueError("Unsupported credential format")
        return password
    lines = raw.splitlines()
    for line in lines:
        match = re.match(r"^(?:password|PASSWORD)\s*[:=]\s*(.+)$", line)
        if match:
            return match.group(1).strip()
    if len(lines) == 1 and raw:
        return raw
    raise ValueError("Unsupported credential format")


def controls(page, public=False):
    return (
        page.locator(
            "button, a, input, select, textarea, [role=button], [role=link]"
        ).evaluate_all(
            """els => els.filter(el => el.getBoundingClientRect().width
          && el.getBoundingClientRect().height).map(el => ({
          tag:el.tagName.toLowerCase(), type:el.getAttribute('type'),
          id:el.id, name:el.getAttribute('aria-label') ||
            (el.tagName === 'INPUT' ? el.getAttribute('placeholder') : el.textContent.trim()),
          disabled:el.disabled === true
        })).slice(0,45)"""
        )
        if public
        else page.locator(
            "button, a, input, select, textarea, [role=button], [role=link]"
        ).evaluate_all(
            """els => els.filter(el => el.getBoundingClientRect().width
          && el.getBoundingClientRect().height).map(el => ({
          tag:el.tagName.toLowerCase(), type:el.getAttribute('type'),
          id:el.id, disabled:el.disabled === true
        })).slice(0,70)"""
        )
    )


def safe_origin(page):
    return urlsplit(page.url).hostname


def login_employee(page, password, record):
    record.update(started=now(), password_submitted=False)
    page.goto(EMPLOYEE + "/app", wait_until="domcontentloaded", timeout=90000)
    record["initial_provider_host"] = safe_origin(page)
    path = urlsplit(page.url).path
    record["authority_class"] = next(
        (
            name
            for name in ("common", "organizations", "consumers")
            if f"/{name}/" in path
        ),
        "tenant_specific_or_other",
    )
    if safe_origin(page) != "login.microsoftonline.com":
        record["outcome"] = "expected_provider_not_reached"
        return record
    email = page.locator('input[type="email"]')
    email.fill(USERNAME)
    record["username_value_confirmed"] = email.input_value() == USERNAME
    submit = page.locator('input[type="submit"]')
    record["initial_submit_label"] = submit.input_value()
    if submit.input_value().lower() == "next":
        submit.press("Enter")
        page.wait_for_timeout(2000)
    headings = page.get_by_role("heading").all_text_contents()
    record["passkey_prompt_observed"] = any(
        "security key" in title.lower() for title in headings
    )
    if record["passkey_prompt_observed"]:
        page.keyboard.press("Escape")
        page.get_by_role("button", name="Back", exact=True).press("Enter")
        page.get_by_role("button", name="Sign-in options", exact=True).press("Enter")
        page.wait_for_timeout(500)
        choices = page.get_by_role("button", name=re.compile("password", re.IGNORECASE))
        record["password_option_offered"] = choices.count() > 0
        record["alternate_options"] = [
            item["name"]
            for item in controls(page, public=True)
            if item["tag"] == "div" and item["name"]
        ]
        if not choices.count():
            record["outcome"] = "passkey_prompt_no_password_option"
            record["final_host"] = safe_origin(page)
            record["ended"] = now()
            return record
        choices.first.press("Enter")
        page.wait_for_timeout(500)
    headings = page.get_by_role("heading").all_text_contents()
    if not any("password" in title.lower() for title in headings):
        record["outcome"] = "password_entry_step_not_reached"
        record["ended"] = now()
        return record
    if safe_origin(page) not in ("login.microsoftonline.com", "login.microsoft.com"):
        record["outcome"] = "password_origin_refused"
        return record
    page.locator('input[type="password"]').fill(password)
    page.locator('input[type="submit"]').press("Enter")
    record["password_submitted"] = True
    for _ in range(45):
        page.wait_for_timeout(1000)
        if safe_origin(page) == urlsplit(EMPLOYEE).hostname:
            record["outcome"] = "returned_to_employee"
            break
        no = page.get_by_role("button", name="No", exact=True)
        if no.count() and no.is_visible():
            no.press("Enter")
        error = page.locator("#passwordError")
        if error.count() and error.is_visible():
            record["outcome"] = "provider_password_error"
            break
    else:
        record["outcome"] = "provider_callback_not_completed"
    record["ended"] = now()
    return record


def account_probe(page):
    return page.evaluate(
        """async () => {
          const r = await fetch('/api/me');
          if (!r.ok) return {status:r.status};
          const data = await r.json();
          const u = data.user || data;
          return {status:r.status, topLevelKeys:Object.keys(data),
            userKeys:Object.keys(u), codePresent:Boolean(u.code),
            rosterBound:Boolean(u.bound),
            codeEqualsEmail:Boolean(u.code && u.email && u.code === u.email),
            authenticated:Boolean(u.name || u.email || u.oid),
            viewOnly:u.view_only === true};
        }"""
    )


def auth_methods(page):
    page.goto(EMPLOYEE + "/app", wait_until="domcontentloaded", timeout=90000)
    page.locator('input[type="email"]').wait_for()
    before = {
        "headings": page.get_by_role("heading").all_text_contents(),
        "submit_labels": page.locator('input[type="submit"]').evaluate_all(
            "els=>els.map(el=>el.value)"
        ),
        "controls": controls(page, public=True),
    }
    page.locator('input[type="email"]').fill(USERNAME)
    page.locator('input[type="submit"]').click(no_wait_after=True)
    page.wait_for_timeout(2000)
    after = {
        "headings": page.get_by_role("heading").all_text_contents(),
        "submit_labels": page.locator('input[type="submit"]').evaluate_all(
            "els=>els.map(el=>el.value)"
        ),
        "controls": controls(page, public=True),
    }
    back_state = None
    options_state = None
    if safe_origin(page) == "login.microsoft.com":
        page.keyboard.press("Escape")
        page.get_by_role("button", name="Back", exact=True).press("Enter")
        page.wait_for_timeout(1500)
        back_state = {
            "headings": page.get_by_role("heading").all_text_contents(),
            "controls": controls(page, public=True),
        }
        options = page.get_by_role("button", name="Sign-in options", exact=True)
        if options.count():
            options.press("Enter")
            page.wait_for_timeout(500)
            options_state = {
                "headings": page.get_by_role("heading").all_text_contents(),
                "controls": controls(page, public=True),
            }
    encoded = json.dumps(
        {
            "before": before,
            "after_username": after,
            "after_back": back_state,
            "sign_in_options": options_state,
        }
    )
    encoded = re.sub(
        re.escape(USERNAME), "[test identity]", encoded, flags=re.IGNORECASE
    )
    encoded = re.sub(r"[\w.+-]+@[\w.-]+", "[identity]", encoded)
    return json.loads(encoded)


def login_resident(page, password):
    page.goto(RESIDENT, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(1500)
    resident = {"started": now()}

    def response_seen(response):
        if urlsplit(response.url).path == "/demo/login":
            resident["login_response_status"] = response.status

    page.on("response", response_seen)
    email = page.locator('input[type="email"]')
    secret = page.locator('input[type="password"]')
    if (
        email.count()
        and secret.count()
        and safe_origin(page) == urlsplit(RESIDENT).hostname
    ):
        email.fill(USERNAME)
        secret.fill(password)
        with page.expect_response(
            lambda response: urlsplit(response.url).path == "/demo/login"
        ):
            page.get_by_role("button", name="Sign in", exact=True).click()
        page.wait_for_timeout(1000)
        resident["password_submitted"] = True
        resident["password_field_remaining"] = secret.count() > 0
        resident["sign_in_error"] = page.locator('[role="alert"]:visible').count() > 0
        resident["error_categories"] = page.locator("body").evaluate(
            """el => { const t=el.innerText.toLowerCase(); return {
              invalidCredentials:t.includes('email or password') || t.includes('sign-in details')
                || t.includes('sign-in failed'),
              expiredShowcase:t.includes('expired'), unavailable:t.includes('unavailable'),
              signInAgain:t.includes('sign in again')}; }"""
        )
        if secret.count():
            secret.fill("")
        if email.count():
            email.fill("")
        resident["controls"] = controls(page)
    else:
        resident["outcome"] = "supported_sign_in_form_not_found"
    page.remove_listener("response", response_seen)
    return resident


def public_resident_chat(page):
    observed = {"authenticated": False, "started": now(), "assistant_requests": 0}
    capture_id = datetime.now(UTC).strftime("%H%M%S")

    def request_seen(request):
        if urlsplit(request.url).path == "/demo/assistant":
            observed["assistant_requests"] += 1

    page.on("request", request_seen)
    page.goto(RESIDENT, wait_until="domcontentloaded", timeout=90000)
    page.get_by_role("button", name="Chat", exact=True).wait_for()
    launcher = page.get_by_role("button", name="Chat", exact=True)
    observed["launcher"] = launcher.evaluate(
        """el => { const r = el.getBoundingClientRect();
        return {rightGap:innerWidth-r.right,bottomGap:innerHeight-r.bottom,
          name:el.getAttribute('aria-label'),hasPopup:el.getAttribute('aria-haspopup')}; }"""
    )
    launcher.press("Enter")
    panel = page.locator(".chat-widget")
    observed["popup_visible"] = panel.is_visible()
    observed["popup_role"] = panel.get_attribute("role")
    observed["static_text"] = panel.inner_text()
    observed["controls"] = controls(page)
    observed["viewport_checks"] = []
    for width in (1280, 390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        observed["viewport_checks"].append(
            panel.evaluate(
                """el => {const r=el.getBoundingClientRect(); return {
              width:innerWidth,popupWidth:r.width,withinViewport:r.left>=0
                && r.right<=innerWidth && r.top>=0 && r.bottom<=innerHeight,
              documentOverflow:document.documentElement.scrollWidth>innerWidth};}"""
            )
        )
        name = f"resident-public-chat-{capture_id}-{width}.png"
        panel.screenshot(path=str(OUT / name))
        observed["viewport_checks"][-1]["screenshot"] = name
    observed["motion"] = []
    for motion in ("no-preference", "reduce"):
        page.emulate_media(reduced_motion=motion)
        observed["motion"].append(
            panel.evaluate(
                """el => ({reduced:matchMedia('(prefers-reduced-motion:reduce)').matches,
              duration:getComputedStyle(el).transitionDuration,
              animation:getComputedStyle(el).animationName,
              token:getComputedStyle(el).getPropertyValue('--motion').trim()})"""
            )
        )
    page.keyboard.press("Escape")
    observed["escape_closes"] = not panel.is_visible()
    observed["focus_returns_to_launcher"] = launcher.evaluate(
        "el=>el===document.activeElement"
    )
    observed["ended"] = now()
    page.remove_listener("request", request_seen)
    return observed


def run(mode):
    result = {"started": now(), "mode": mode, "sites": {}}
    with tempfile.TemporaryDirectory(prefix="ama-live-acceptance-") as scratch:
        os.chmod(scratch, 0o700)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                downloads_path=scratch,
                env={**os.environ, "TMPDIR": scratch},
                args=["--disable-breakpad", "--disable-crash-reporter"],
            )
            result["browser_version"] = browser.version
            context = browser.new_context(
                viewport={"width": 1280, "height": 900}, accept_downloads=False
            )
            page = context.new_page()
            page.set_default_timeout(20000)
            try:
                if mode == "auth-methods":
                    result["sites"]["employee"] = auth_methods(page)
                elif mode == "public-features":
                    result["sites"]["resident"] = public_resident_chat(page)
                elif mode in ("inspect", "auth-inspect"):
                    targets = (
                        (("employee", EMPLOYEE + "/app"),)
                        if mode == "auth-inspect"
                        else (("employee", EMPLOYEE), ("resident", RESIDENT))
                    )
                    for site, origin in targets:
                        try:
                            page.goto(
                                origin, wait_until="domcontentloaded", timeout=90000
                            )
                            page.wait_for_timeout(2000)
                            result["sites"][site] = {
                                "host": safe_origin(page),
                                "controls": controls(page, public=True),
                                "passwordFields": page.locator(
                                    'input[type="password"]'
                                ).count(),
                            }
                        except PlaywrightError as error:
                            result["sites"][site] = {
                                "failure_type": type(error).__name__
                            }
                else:
                    password = credential()
                    employee = result["sites"]["employee"] = {}
                    try:
                        login_employee(page, password, employee)
                        if safe_origin(page) == urlsplit(EMPLOYEE).hostname:
                            result["sites"]["employee"]["account"] = account_probe(page)
                            result["sites"]["employee"]["controls"] = controls(page)
                    except PlaywrightError as error:
                        employee["failure_type"] = type(error).__name__
                        employee["host"] = safe_origin(page)
                        employee["remaining_controls"] = controls(page)
                        employee["provider_page_categories"] = page.locator(
                            "body"
                        ).evaluate(
                            """el => {
                              const t = el.innerText.toLowerCase();
                              return {staySignedIn:t.includes('stay signed in'),
                                invalidPassword:t.includes('password is incorrect'),
                                permissionConsent:t.includes('permissions requested'),
                                browserError:t.includes('err_'),
                                updatePassword:t.includes('update your password'),
                                signInBlocked:t.includes('sign-in is blocked')};
                            }"""
                        )
                    if mode != "employee-only":
                        result["sites"]["resident"] = login_resident(page, password)
                    if mode == "final":
                        result["sites"]["resident_public_chat"] = public_resident_chat(
                            page
                        )
                    result["credential_not_in_evidence"] = password not in json.dumps(
                        result
                    )
                    result["existing_evidence_credential_free"] = all(
                        password.encode() not in item.read_bytes()
                        for item in OUT.iterdir()
                        if item.is_file()
                    )
                    if (
                        not result["credential_not_in_evidence"]
                        or not result["existing_evidence_credential_free"]
                    ):
                        raise ValueError("Evidence hygiene check failed")
                    del password
            finally:
                context.close()
                browser.close()
        result["browser_closed"] = True
    result["owned_scratch_removed"] = not Path(scratch).exists()
    result["ended"] = now()
    output = OUT / (
        mode + "-" + datetime.now(UTC).strftime("%H%M%S") + "-evidence.json"
    )
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=(
            "inspect",
            "auth-inspect",
            "auth-methods",
            "accept",
            "employee-only",
            "public-features",
            "final",
        ),
        default="inspect",
    )
    args = parser.parse_args()
    try:
        run(args.mode)
    except (PlaywrightError, OSError, ValueError) as error:
        print(
            json.dumps(
                {"automation_failed": True, "failure_type": type(error).__name__}
            )
        )
        raise SystemExit(1) from None
