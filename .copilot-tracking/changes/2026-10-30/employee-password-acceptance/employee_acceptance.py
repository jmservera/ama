"""Employee-only bounded acceptance; no credential, token or pixel capture."""

from __future__ import annotations

import hashlib
import json
import os
import re
import resource
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote, quote_plus, urlsplit

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import sync_playwright

APP = (
    "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
)
USERNAME = "AadiK@DIAx90853289.OnMicrosoft.com"
PROVIDERS = {"login.microsoftonline.com", "login.microsoft.com"}
OUT = Path(__file__).resolve().parent


def parse_password(raw):
    value = raw.strip()
    if not value:
        raise ValueError("credential_empty")
    if value.startswith("{"):

        def pairs(items):
            result = {}
            for key, item in items:
                if key in result:
                    raise ValueError("credential_duplicate_key")
                result[key] = item
            return result

        try:
            data = json.loads(value, object_pairs_hook=pairs)
        except (json.JSONDecodeError, ValueError):
            raise ValueError("credential_invalid_json") from None
        if not isinstance(data, dict):
            raise ValueError("credential_invalid_json")
        keys = [key for key in ("password", "Password") if key in data]
        if len(keys) != 1 or not isinstance(data[keys[0]], str):
            raise ValueError("credential_ambiguous")
        password = data[keys[0]].strip()
    else:
        first = value.splitlines()[0].strip()
        match = re.fullmatch(r"password\s*[:=]\s*(.+)", first, re.IGNORECASE)
        if match:
            password = match.group(1).strip()
        elif re.match(r"password\s*[:=]", first, re.IGNORECASE):
            raise ValueError("credential_empty")
        elif first.startswith(("[", '"')) or first.casefold() == USERNAME.casefold():
            raise ValueError("credential_unsupported")
        else:
            password = first
    if not password or password.casefold() == USERNAME.casefold():
        raise ValueError("credential_empty_or_identity")
    return password


def allowed_origin(url, app=False):
    try:
        parts = urlsplit(url)
        return (
            parts.scheme == "https"
            and parts.username is None
            and parts.password is None
            and parts.port in (None, 443)
            and parts.hostname in ({urlsplit(APP).hostname} if app else PROVIDERS)
        )
    except ValueError:
        return False


def sanitize(text, password):
    for secret in (password, USERNAME):
        for variant in sorted(
            {secret, quote(secret, safe=""), quote_plus(secret, safe="")},
            key=len,
            reverse=True,
        ):
            text = re.sub(re.escape(variant), "[redacted]", text, flags=re.IGNORECASE)
    text = re.sub(r"https?://[^\s<>]+", "[url]", text, flags=re.IGNORECASE)
    text = re.sub(r"[\w.+%-]+@[\w.%-]+", "[identity]", text)
    if password in text or USERNAME.casefold() in text.casefold():
        raise ValueError("sanitization_failed")
    return text


def public_state(page, password):
    if not allowed_origin(page.url):
        return {"category": "unexpected_origin_no_text_capture"}
    # DOM text never includes input values; scripts/styles are not extracted.
    text = page.locator("body").inner_text(timeout=8000)
    names = page.locator(
        'button, a, input[type="submit"], [role="button"], [role="link"]'
    ).evaluate_all(
        """els => els.filter(e => e.getBoundingClientRect().width &&
        e.getBoundingClientRect().height).map(e =>
        e.getAttribute('aria-label') ||
        (e.tagName === 'INPUT' ? e.value : e.innerText)).filter(Boolean)"""
    )
    return {
        "host": urlsplit(page.url).hostname,
        "text": sanitize(text, password),
        "controls": [sanitize(name, password) for name in names],
    }


def choose_action(names, used):
    patterns = [
        (
            "password",
            r"(?:use (?:your |my |a )?password(?: instead)?|sign in with (?:a |your )?password|password)",
        ),
        (
            "other_ways",
            r"(?:other ways to sign in|sign in another way|use another (?:method|sign.in option))",
        ),
        ("options", r"sign.in options"),
        ("cancel", r"cancel"),
        ("back", r"back"),
    ]
    for kind, pattern in patterns:
        for name in names:
            if (
                re.fullmatch(pattern, name.strip(), re.IGNORECASE)
                and (kind, name) not in used
            ):
                return kind, name
    return None


def click_named(page, name):
    for role in ("button", "link"):
        elements = page.get_by_role(role, name=name, exact=True)
        for index in range(elements.count()):
            element = elements.nth(index)
            if element.is_visible():
                element.press("Enter", timeout=8000, no_wait_after=True)
                return
    raise ValueError("offered_control_not_actionable")


def binding_probe(page):
    if not allowed_origin(page.url, app=True):
        raise ValueError("callback_origin_refused")
    return page.evaluate(
        """async () => {
        const r = await fetch('/api/me', {redirect: 'error'});
        if (!r.ok) return {authenticated:false, responseOk:false};
        const d = await r.json(); const u = d.user || d;
        return {responseOk:true, authenticated:Boolean(u.name || u.email || u.oid),
          codePresent:Boolean(u.code), rosterBound:Boolean(u.bound),
          codeEqualsEmail:Boolean(u.code && u.email && u.code === u.email),
          viewOnly:u.view_only === true};
        }"""
    )


def authenticate(page, password, record):
    start = time.monotonic()
    page.goto(APP + "/app", wait_until="domcontentloaded", timeout=60000)
    record["steps"] = []
    used = set()
    fingerprints = {}
    username_submitted = False
    password_submitted = False
    for _ in range(12):
        if time.monotonic() - start > 180:
            return "authentication_deadline"
        if allowed_origin(page.url, app=True):
            record["binding"] = binding_probe(page)
            return (
                "authenticated_callback"
                if record["binding"]["authenticated"]
                else "callback_authentication_unconfirmed"
            )
        if not allowed_origin(page.url):
            return "unexpected_origin"
        page.wait_for_timeout(1500)
        # Modern Entra redirects can render a logo-only shell before the form.
        page.wait_for_function(
            """() => [...document.querySelectorAll(
              'input[type=email], input[type=submit], [role=heading], h1, h2, button, [role=button]'
            )].some(e => {
              const r=e.getBoundingClientRect();
              if (!r.width || !r.height) return false;
              if (e.matches('input[type=email], input[type=submit]')) return true;
              return /password|sign.in|security key|passkey|cancel|back|other ways/i.test(
                e.innerText || e.getAttribute('aria-label') || '');
            })""",
            timeout=15000,
        )
        if allowed_origin(page.url, app=True):
            continue
        state = public_state(page, password)
        record["steps"].append(state)
        fingerprint = json.dumps(state, sort_keys=True)
        fingerprints[fingerprint] = fingerprints.get(fingerprint, 0) + 1
        if fingerprints[fingerprint] > 2:
            return "repeated_state_no_password_route"
        email = page.locator('input[type="email"]:visible')
        if email.count() and not username_submitted:
            if not allowed_origin(page.url):
                return "username_origin_refused"
            email.fill(USERNAME)
            submit = page.locator('input[type="submit"]:visible')
            if submit.get_attribute("value").casefold() != "next":
                return "username_next_not_offered"
            submit.press("Enter", timeout=8000)
            username_submitted = True
            record["username_submitted"] = True
            continue
        secret_input = page.locator('input[type="password"]:visible')
        password_heading = page.get_by_role(
            "heading",
            name=re.compile(r"^(?:Enter (?:your )?)?password$", re.IGNORECASE),
        )
        submit = page.locator('input[type="submit"]:visible')
        password_step = (
            username_submitted
            and password_heading.count() > 0
            and password_heading.first.is_visible()
            and secret_input.count() > 0
            and submit.count() == 1
            and (submit.get_attribute("value") or "").casefold() == "sign in"
        )
        if password_step:
            if password_submitted:
                return "password_rejected_or_challenge_repeated"
            if not allowed_origin(page.url):
                return "password_origin_refused"
            secret_input.fill(password)
            submit.press("Enter", timeout=8000)
            password_submitted = True
            record["password_submitted"] = True
            record["password_field_filled"] = True
            continue
        if password_submitted:
            no = page.get_by_role("button", name="No", exact=True)
            if no.count() and no.is_visible() and ("kmsi", "No") not in used:
                used.add(("kmsi", "No"))
                no.click(timeout=8000, no_wait_after=True)
                continue
            return "post_password_challenge_unconfirmed"
        page.keyboard.press("Escape")
        action = choose_action(state.get("controls", []), used)
        if action is None:
            return "password_route_not_offered"
        used.add(action)
        record["steps"][-1]["selected_action"] = action[0]
        click_named(page, action[1])
    return "transition_budget_exhausted"


def inspect_employee_shell(page):
    """Only boolean observations/geometry leave the authorized employee UI."""
    result = {}
    try:
        launcher = page.locator("#employee-chat-launcher")
        launcher.wait_for(state="visible", timeout=15000)
        result["launcher"] = launcher.evaluate(
            """el => { const r = el.getBoundingClientRect(); return {
            rightGap:innerWidth-r.right, bottomGap:innerHeight-r.bottom,
            dialogSemantics:el.getAttribute('aria-haspopup') === 'dialog'}; }"""
        )
        launcher.press("Enter")
        panel = page.locator("#employee-chat")
        panel.wait_for(state="visible")
        skill = panel.locator("select")
        skill.wait_for(state="visible")
        result["chat"] = {
            "dialogVisible": panel.is_visible(),
            "skillInComposer": skill.evaluate("e => Boolean(e.closest('form'))"),
            "skillOptions": skill.locator("option").count(),
            "disabledUnsupportedControls": panel.evaluate(
                """e => ['Attach','Voice'].every(name => [...e.querySelectorAll('button')]
                .some(b => b.textContent === name && b.disabled &&
                  Boolean(document.getElementById(b.getAttribute('aria-describedby'))?.textContent)))"""
            ),
            "sendButton": panel.get_by_role("button", name="Send", exact=True).count()
            == 1,
        }
        options = skill.locator("option")
        if options.count() > 1:
            target = options.nth(1).get_attribute("value")
            skill.select_option(target)
            result["chat"]["skillSelectionChanges"] = skill.input_value() == target
        question = panel.locator("textarea")
        question.fill("Acceptance check")
        question.press("Shift+Enter")
        result["chat"]["shiftEnterNewline"] = "\n" in question.input_value()
        question.fill(
            "What can you help me with? Give a short answer without mentioning any resident or case details."
        )
        question.press("Enter")
        page.wait_for_timeout(250)
        result["chat"]["loadingVisibleAfter250ms"] = panel.locator(
            ".chat-widget-loading"
        ).is_visible()
        page.wait_for_function(
            "() => document.querySelector('#employee-chat form')?.getAttribute('aria-busy') === 'false'",
            timeout=60000,
        )
        result["chat"].update(
            panel.evaluate(
                """e => ({
              remainsOpen:!e.hidden,
              userMessages:e.querySelectorAll('.chat-widget-user').length,
              assistantMessages:e.querySelectorAll('.chat-widget-assistant').length,
              actualAiLabel:[...e.querySelectorAll('.chat-widget-assistant .chat-widget-meta')]
                .some(x => /AI suggestion|AI.generated/i.test(x.textContent) &&
                  !/no AI|workflow.only/i.test(x.textContent)),
              rulesOnly:[...e.querySelectorAll('.chat-widget-assistant .chat-widget-meta')]
                .some(x => /no AI|workflow.only|rules/i.test(x.textContent)),
              sourcesInitiallyCollapsed:[...e.querySelectorAll('.chat-widget-assistant details')]
                .every(d => !d.open),
              sourcesCount:e.querySelectorAll('.chat-widget-assistant details').length,
              logPolite:e.querySelector('[role=log]')?.getAttribute('aria-live') === 'polite',
              visibleChatError:!e.querySelector('[role=alert]').hidden
            })"""
            )
        )
        question.fill(
            "Please explain which advisory skills are available, without case details."
        )
        panel.get_by_role("button", name="Send", exact=True).click()
        page.wait_for_function(
            "() => document.querySelector('#employee-chat form')?.getAttribute('aria-busy') === 'false'",
            timeout=60000,
        )
        result["chat"]["multiTurn"] = panel.evaluate(
            """e => !e.hidden && e.querySelectorAll('.chat-widget-user').length >= 2 &&
            e.querySelectorAll('.chat-widget-assistant').length >= 2"""
        )
        result["chat"]["threadGeometry"] = panel.evaluate(
            """e => {const l=e.querySelector('[role=log]'), f=e.querySelector('form');
            return {logScrollable:['auto','scroll'].includes(getComputedStyle(l).overflowY),
              newestAtBottom:l.scrollHeight-l.clientHeight-l.scrollTop<=2,
              composerBelowLog:f.getBoundingClientRect().top>=l.getBoundingClientRect().bottom-1};}"""
        )
        question.press("Escape")
    except BrowserError:
        result["chat_error_category"] = (
            "employee_chat_observation_failed_no_details_retained"
        )
    try:
        page.get_by_role("button", name="Expand map", exact=True).press("Enter")
        dialog = page.locator(".map-dialog[open]")
        filters = dialog.locator(".overview-map-filters")
        filters.wait_for(state="visible")
        buttons = filters.locator("button[aria-pressed]")
        result["map"] = {
            "expandedFiltersVisible": True,
            "filterButtons": buttons.count(),
        }
        changes = []
        for index in range(min(buttons.count(), 6)):
            button = buttons.nth(index)
            button.press("Enter" if index % 2 == 0 else "Space")
            page.wait_for_timeout(1500)
            changes.append(
                button.evaluate(
                    """e => ({
                  selected:e.getAttribute('aria-pressed')==='true',
                  nonColourSelected:Boolean(e.querySelector('.tile-selection')?.textContent.includes('Selected')),
                  focus:document.activeElement===e,
                  markers:document.querySelectorAll('.map-marker').length,
                  mapBusy:document.querySelector('#leaflet')?.getAttribute('aria-busy')==='true'
                })"""
                )
            )
        result["map"]["selections"] = changes
        page.set_viewport_size({"width": 390, "height": 800})
        result["map"]["narrow"] = filters.evaluate(
            """e => ({withinViewport:e.getBoundingClientRect().left>=0 &&
            e.getBoundingClientRect().right<=innerWidth,
            pageOverflow:document.documentElement.scrollWidth>innerWidth})"""
        )
        page.keyboard.press("Escape")
        result["map"]["restoredHeaderSelectedCount"] = page.locator(
            '.overview-map-filters button[aria-pressed="true"]'
        ).count()
        page.set_viewport_size({"width": 1280, "height": 900})
    except BrowserError:
        result["map_error_category"] = (
            "expanded_map_observation_failed_no_details_retained"
        )
    try:
        link = page.locator('a[href^="#/case/"]').first
        href = link.get_attribute("href", timeout=8000)
        if not href or not href.startswith("#/case/"):
            result["case_error_category"] = "no_case_link_offered"
            return result
        page.goto(APP + "/app" + href, wait_until="domcontentloaded", timeout=60000)
        page.locator(".case-journey").wait_for(state="visible", timeout=15000)
        result["case"] = {"viewports": []}
        for width in (1280, 390, 320):
            page.set_viewport_size({"width": width, "height": 800})
            result["case"]["viewports"].append(
                page.evaluate(
                    """() => ({width:innerWidth,
                pageOverflow:document.documentElement.scrollWidth>innerWidth,
                stepHeights:[...document.querySelectorAll('.step')].map(e=>e.getBoundingClientRect().height),
                iconsLoaded:[...document.querySelectorAll('.step-icon')].every(e=>e.complete&&e.naturalWidth>0),
                iconsCount:document.querySelectorAll('.step-icon').length,
                stepLabelsPresent:[...document.querySelectorAll('.step-name')].every(e=>Boolean(e.textContent.trim())),
                tablistCount:document.querySelectorAll('[role=tablist]').length,
                tabsOutsidePanel:!document.querySelector('[role=tablist]')?.closest('[role=tabpanel]'),
                blockerOneLine:[...document.querySelectorAll('.case-blocker-summary')]
                  .every(e=>getComputedStyle(e).whiteSpace==='nowrap')
                })"""
                )
            )
        trigger = page.locator("button[popovertarget]").first
        if trigger.count():
            trigger.press("Enter")
            result["case"]["keyboardPopoverVisible"] = (
                page.locator(".case-blocker-popover:popover-open").count() > 0
            )
            page.keyboard.press("Escape")
    except BrowserError:
        result["case_error_category"] = "case_observation_failed_no_details_retained"
    return result


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    run_id = datetime.now(UTC).strftime("%H%M%S-%f")
    record = {
        "started": datetime.now(UTC).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "password_submitted": False,
        "captures": {
            "screenshots": False,
            "video": False,
            "trace": False,
            "har": False,
        },
    }
    password = None
    # All secret access and browser use remain in this automation process.
    try:
        password = parse_password((Path.home() / ".ama-test-user").read_text())
        record["credential_parsed"] = True
        with tempfile.TemporaryDirectory(prefix="ama-employee-accept-") as scratch:
            previous_tmp = os.environ.get("TMPDIR")
            os.environ["TMPDIR"] = scratch
            with sync_playwright() as driver:
                browser = driver.chromium.launch(
                    headless=True,
                    args=[f"--disk-cache-dir={scratch}/cache"],
                )
                record["browser_version"] = browser.version
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                context.set_default_timeout(8000)
                page = context.new_page()
                try:
                    record["outcome"] = authenticate(page, password, record)
                    if record["outcome"] == "authenticated_callback":
                        record["employee_shell"] = inspect_employee_shell(page)
                    else:
                        record["final_offered_page"] = public_state(page, password)
                except BrowserError:
                    record["outcome"] = "browser_action_failed"
                    record["error_category"] = "playwright_error_details_not_retained"
                    record["final_offered_page"] = public_state(page, password)
                finally:
                    context.close()
                    browser.close()
                    record["browser_closed"] = True
            record["owned_scratch_cleanup_expected"] = True
            if previous_tmp is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = previous_tmp
        record["owned_scratch_removed"] = not Path(scratch).exists()
    except (OSError, ValueError, BrowserError):
        record["outcome"] = "automation_input_or_sanitization_failed"
        record["error_category"] = "details_not_retained"
    record["ended"] = datetime.now(UTC).isoformat()
    encoded = json.dumps(record, indent=2) + "\n"
    if password is not None and password in encoded:
        raise SystemExit("Unsafe evidence refused")
    target = OUT / f"employee-{run_id}-evidence.json"
    target.write_text(encoded)
    manifest = {
        "evidence": target.name,
        "evidence_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "script": Path(__file__).name,
        "script_sha256": record["script_sha256"],
        "screenshots": [],
    }
    (OUT / f"employee-{run_id}-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print(json.dumps({"evidence_file": target.name, "outcome": record["outcome"]}))


if __name__ == "__main__":
    main()
