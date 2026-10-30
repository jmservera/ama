"""Capture-free, task-scoped employee acceptance. Secrets never leave automation."""

from __future__ import annotations

import fcntl
import hashlib
import html
import json
import os
import re
import resource
import sys
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

BINDING_JS = r"""async ({expected,timeoutMs}) => {
  const r = await fetch('/api/me', {redirect:'error', signal:AbortSignal.timeout(timeoutMs)});
  const responseOk = r.status === 200 && !r.redirected &&
    (r.headers.get('content-type') || '').includes('application/json');
  if (!responseOk) return {responseOk:false, authenticated:false};
  const d=await r.json(), u=d?.user, a=d?.account;
  const guid = x => typeof x === 'string' &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(x);
  const schemaValid = Boolean(u && typeof u === 'object' && a && typeof a === 'object' &&
    typeof a.email === 'string' && typeof u.code === 'string' && u.code &&
    typeof u.email === 'string' && u.email && guid(u.tid) && guid(u.oid) &&
    typeof u.view_only === 'boolean' && Array.isArray(u.app_roles));
  const providerMatches = a?.provider === 'trusted-proxy' &&
    u?.auth_provider === 'trusted-proxy';
  const expectedIdentity = typeof a?.email === 'string' &&
    a.email.trim().toLowerCase() === expected.toLowerCase();
  const employeeRole = u?.role === 'Retrofit Programme Manager' &&
    Array.isArray(u?.app_roles) && u.app_roles.includes('ZavaForward.ProgrammeManager');
  const notViewOnly = u?.view_only === false;
  return {responseOk, schemaValid, providerMatches, expectedIdentity, employeeRole,
    notViewOnly, authenticated: schemaValid && providerMatches && expectedIdentity &&
      employeeRole && notViewOnly,
    codePresent:typeof u?.code === 'string' && Boolean(u.code),
    rosterBound:Boolean(u?.bound && typeof u.bound === 'object' &&
      typeof u.bound.code === 'string' && u.bound.code &&
      typeof u.bound.email === 'string' && u.bound.email),
    codeEqualsEmail:Boolean(u?.code && u?.email && u.code === u.email)};
}"""


def now():
    return datetime.now(UTC).isoformat()


def parse_credentials(raw):
    lines = raw.splitlines()
    if not lines or not lines[0].strip():
        raise ValueError("missing_first_line")
    password = re.sub(
        r"^password\s*[:=]\s*", "", lines[0].strip(), flags=re.IGNORECASE
    ).strip()
    tap = (
        re.sub(
            r"^(?:tap|temporary access pass)\s*[:=]\s*",
            "",
            lines[1].strip(),
            flags=re.IGNORECASE,
        ).strip()
        if len(lines) > 1
        else ""
    )
    if (
        not password
        or password.casefold() == USERNAME.casefold()
        or password.startswith(("{", "["))
    ):
        raise ValueError("unsupported_credential_format")
    return password, tap or None


def allowed(url, app=False):
    try:
        p = urlsplit(url)
        return (
            p.scheme == "https"
            and p.username is None
            and p.password is None
            and p.port in (None, 443)
            and p.hostname in ({urlsplit(APP).hostname} if app else PROVIDERS)
        )
    except ValueError:
        return False


def sanitize(text, secrets):
    for secret in (*secrets, USERNAME, USERNAME.split("@")[0]):
        if not secret:
            continue
        variants = {
            secret,
            quote(secret, safe=""),
            quote_plus(secret, safe=""),
            html.escape(secret),
        }
        for variant in sorted(variants, key=len, reverse=True):
            text = re.sub(re.escape(variant), "[redacted]", text, flags=re.IGNORECASE)
    text = re.sub(r"https?://[^\s<>]+", "[url]", text, flags=re.IGNORECASE)
    text = re.sub(r"[\w.+%-]+@[\w.%-]+", "[identity]", text)
    text = re.sub(
        r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b",
        "[identifier]",
        text,
        flags=re.IGNORECASE,
    )
    return text


def booleans(value):
    if not isinstance(value, dict) or not value:
        raise ValueError("invalid_boolean_projection")
    if any(type(item) is not bool for item in value.values()):
        raise ValueError("non_boolean_projection")
    return value


class Deadline:
    def __init__(self, seconds=180, clock=time.monotonic):
        self.clock = clock
        self.end = clock() + seconds

    def timeout(self, maximum=8000):
        remaining = int((self.end - self.clock()) * 1000)
        if remaining <= 0:
            raise TimeoutError("authentication_deadline")
        return min(maximum, remaining)

    def pause(self, page, milliseconds=500):
        amount = self.timeout(milliseconds)
        page.wait_for_timeout(amount)
        self.timeout()


class RunGuard:
    """Exclusive file admission persists even after process interruption."""

    def __init__(self, path, script_hash):
        self.path = path
        self.data = {
            "started": now(),
            "script_sha256": script_hash,
            "status": "in_progress",
            "attempts": [],
            "captures": {
                "screenshots": False,
                "video": False,
                "har": False,
                "trace": False,
            },
        }
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w") as stream:
            self.write(stream)

    def write(self, stream):
        json.dump(self.data, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())

    def save(self):
        with self.path.open("w") as stream:
            self.write(stream)

    @classmethod
    def continue_completed_precredential(cls, path, script_hash):
        stream = path.open("r+")
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            data = json.load(stream)
            attempts = data.get("attempts", [])
            if (
                data.get("status") != "completed"
                or len(attempts) != 1
                or attempts[0].get("number") != 1
                or attempts[0].get("status") != "browser_or_route_failure_stop"
                or attempts[0].get("username_submission_attempted", False)
                or attempts[0].get("credential_fill_attempted", True)
                or attempts[0].get("submission_attempted", True)
                or attempts[0].get("steps", [])
                or data.get("evidence") != "attempt3-evidence.json"
            ):
                raise ValueError("completed_safe_continuation_refused")
            evidence_path = path.parent / "attempt3-evidence.json"
            source_path = path.parent / "attempt3-first-run.py.txt"
            if (
                hashlib.sha256(evidence_path.read_bytes()).hexdigest()
                != data["evidence_sha256"]
                or hashlib.sha256(source_path.read_bytes()).hexdigest()
                != data["script_sha256"]
                or json.loads(evidence_path.read_text())["attempts"] != attempts
            ):
                raise ValueError("continuation_provenance_mismatch")
            guard = cls.__new__(cls)
            guard.path, guard.data, guard.lock_stream = path, data, stream
            data.update(
                status="in_progress",
                safe_completed_continuation=True,
                current_script_sha256=script_hash,
                source_versions=[
                    {"file": source_path.name, "sha256": data["script_sha256"]},
                    {"file": Path(__file__).name, "sha256": script_hash},
                ],
                evidence_files=[
                    {"file": evidence_path.name, "sha256": data["evidence_sha256"]}
                ],
            )
            guard.save()
            return guard
        except (OSError, ValueError, KeyError, TypeError):
            stream.close()
            raise

    def admit(self):
        if len(self.data["attempts"]) >= 2 or any(
            attempt["status"] != "definitive_rejection"
            and not (
                self.data.get("safe_completed_continuation")
                and attempt["number"] == 1
                and attempt["status"] == "browser_or_route_failure_stop"
                and not attempt["credential_fill_attempted"]
                and not attempt.get("username_submission_attempted", False)
            )
            for attempt in self.data["attempts"]
        ):
            raise ValueError("attempt_admission_refused")
        attempt = {
            "number": len(self.data["attempts"]) + 1,
            "started": now(),
            "status": "launch_admitted",
            "credential_fill_attempted": False,
            "credential_fill_completed": False,
            "submission_attempted": False,
            "submission_delivery": "not_attempted",
        }
        self.data["attempts"].append(attempt)
        self.save()
        return attempt


def method_action(names, used, tap_available):
    patterns = [
        (
            "tap",
            r"(?:temporary access pass|use (?:a |your )?temporary access pass(?: instead)?)",
        ),
        (
            "other_ways",
            r"(?:other ways to sign in|sign in another way|use another method)",
        ),
        ("options", r"sign.in options"),
        (
            "password",
            r"(?:use (?:your |my |a )?password(?: instead)?|sign in with (?:a |your )?password|password)",
        ),
        ("cancel", r"cancel"),
        ("back", r"back"),
    ]
    for kind, pattern in patterns:
        if kind == "tap" and not tap_available:
            continue
        for name in names:
            if (kind, name) not in used and re.fullmatch(
                pattern, name.strip(), flags=re.IGNORECASE
            ):
                return kind, name
    return None


def public_state(page, secrets, budget):
    if not allowed(page.url):
        return {"category": "unexpected_origin_no_text_capture"}
    text = page.locator("body").inner_text(timeout=budget.timeout())
    names = page.locator(
        'button, a, input[type="submit"], [role="button"], [role="link"]'
    ).evaluate_all(
        """els => els.filter(e=>e.getBoundingClientRect().width &&
        e.getBoundingClientRect().height).map(e=>e.getAttribute('aria-label') ||
        (e.tagName==='INPUT'?e.value:e.innerText)).filter(Boolean)"""
    )
    return {
        "host": urlsplit(page.url).hostname,
        "text": sanitize(text, secrets),
        "controls": [sanitize(name, secrets) for name in names],
    }


def click_named(page, name, budget):
    for role in ("button", "link"):
        locator = page.get_by_role(role, name=name, exact=True)
        for index in range(locator.count()):
            target = locator.nth(index)
            if target.is_visible():
                target.press("Enter", timeout=budget.timeout(), no_wait_after=True)
                return
    raise ValueError("offered_control_not_actionable")


def submit_secret(page, field, submit, secret, attempt, guard, budget, method):
    if not allowed(page.url):
        raise ValueError("secret_origin_refused")
    if attempt["submission_attempted"]:
        raise ValueError("repeat_submit_refused")
    budget.timeout()
    attempt.update(credential_fill_attempted=True, credential_method=method)
    guard.save()
    field.fill(secret, timeout=budget.timeout())
    attempt["credential_fill_completed"] = True
    guard.save()
    budget.timeout()
    attempt.update(submission_attempted=True, submission_delivery="unknown")
    guard.save()
    submit.press("Enter", timeout=budget.timeout(), no_wait_after=True)
    attempt["submission_delivery"] = "keypress_completed_not_authentication"
    guard.save()


def authenticate(page, password, tap, attempt, guard):
    budget = Deadline()
    attempt["failure_stage"] = "initial_navigation"
    guard.save()
    page.goto(
        APP + "/.auth/login/aad?post_login_redirect_uri=%2Fapp",
        wait_until="domcontentloaded",
        timeout=budget.timeout(60000),
    )
    attempt["failure_stage"] = "provider_route"
    used = set()
    username_submitted = False
    attempt["steps"] = []
    for _ in range(18):
        page.set_default_timeout(budget.timeout())
        if allowed(page.url, app=True):
            if not username_submitted or not attempt["submission_attempted"]:
                return "unexpected_preexisting_callback"
            page.set_default_timeout(budget.timeout())
            attempt["binding"] = booleans(
                page.evaluate(
                    BINDING_JS,
                    {"expected": USERNAME, "timeoutMs": budget.timeout(8000)},
                )
            )
            return (
                "authenticated"
                if attempt["binding"]["authenticated"]
                else "callback_authentication_unconfirmed"
            )
        if not allowed(page.url):
            return "unexpected_origin"
        budget.pause(page, 1000)
        if allowed(page.url, app=True):
            continue
        page.wait_for_function(
            """() => [...document.querySelectorAll(
            'input[type=email],input[type=submit],h1,h2,[role=heading],button,[role=button]'
            )].some(e=> {const r=e.getBoundingClientRect();
            return r.width && r.height && (e.matches('input[type=email],input[type=submit]') ||
              /password|sign.in|security key|passkey|cancel|back|other ways|access pass/i.test(
              e.innerText || e.getAttribute('aria-label') || ''));})""",
            timeout=budget.timeout(15000),
        )
        if allowed(page.url, app=True):
            continue
        state = public_state(page, (password, tap), budget)
        attempt["steps"].append(state)
        guard.save()
        email = page.locator('input[type="email"]:visible')
        submit = page.locator('input[type="submit"]:visible')
        if email.count() and not username_submitted:
            if not allowed(page.url):
                return "username_origin_refused"
            budget.timeout()
            email.fill(USERNAME, timeout=budget.timeout())
            if (
                submit.count() != 1
                or (submit.get_attribute("value") or "").casefold() != "next"
            ):
                return "username_next_not_offered"
            budget.timeout()
            attempt["username_submission_attempted"] = True
            guard.save()
            submit.press("Enter", timeout=budget.timeout(), no_wait_after=True)
            username_submitted = True
            continue
        if attempt["submission_attempted"]:
            no = page.get_by_role("button", name="No", exact=True)
            if no.count() and no.is_visible() and ("kmsi", "No") not in used:
                used.add(("kmsi", "No"))
                click_named(page, "No", budget)
                continue
            if re.search(
                r"(?:password is incorrect|incorrect password|temporary access pass is incorrect)",
                state.get("text", ""),
                flags=re.IGNORECASE,
            ):
                return "definitive_rejection"
            return "post_submission_challenge_unconfirmed"
        headings = page.get_by_role("heading").all_text_contents()
        tap_step = any(
            "temporary access pass" in heading.casefold() for heading in headings
        )
        password_step = any(
            re.fullmatch(
                r"(?:Enter (?:your )?)?password", heading.strip(), re.IGNORECASE
            )
            for heading in headings
        )
        action = method_action(state.get("controls", []), used, tap is not None)
        secret_input = page.locator(
            'input[type="password"]:visible, input[name="otc"]:visible, input[name="passwd"]:visible'
        )
        if username_submitted and submit.count() == 1 and secret_input.count() == 1:
            if tap_step and tap is not None:
                submit_secret(
                    page, secret_input, submit, tap, attempt, guard, budget, "tap"
                )
                continue
            if password_step:
                if (
                    tap is not None
                    and action
                    and action[0]
                    in (
                        "tap",
                        "other_ways",
                        "options",
                    )
                ):
                    pass
                else:
                    submit_secret(
                        page,
                        secret_input,
                        submit,
                        password,
                        attempt,
                        guard,
                        budget,
                        "password",
                    )
                    continue
        budget.timeout()
        page.keyboard.press("Escape")
        budget.timeout()
        if action is None:
            attempt["final_offered_page"] = state
            return "credential_route_not_offered"
        used.add(action)
        attempt["steps"][-1]["selected_action"] = action[0]
        guard.save()
        click_named(page, action[1], budget)
    return "transition_budget_exhausted"


def chat_check(page):
    result = {}
    launcher = page.locator("#employee-chat-launcher")
    launcher.wait_for(state="visible", timeout=15000)
    result.update(
        booleans(
            launcher.evaluate(
                """e=>{const r=e.getBoundingClientRect();return {
                bottomRight:innerWidth-r.right>=0 && innerWidth-r.right<=32 &&
                  innerHeight-r.bottom>=0 && innerHeight-r.bottom<=32,
                dialogLauncher:e.getAttribute('aria-haspopup')==='dialog'};}"""
            )
        )
    )
    launcher.press("Enter")
    panel = page.locator("#employee-chat")
    panel.wait_for(state="visible")
    question = panel.locator("textarea")
    question.wait_for(state="visible")
    page.wait_for_function(
        "()=>document.querySelector('#employee-chat textarea')?.disabled===false",
        timeout=20000,
    )
    result.update(
        booleans(
            panel.evaluate(
                """e=>({dialogVisible:!e.hidden && e.getAttribute('role')==='dialog',
                skillInComposer:Boolean(e.querySelector('form select')),
                multipleSkills:e.querySelectorAll('select option').length>1,
                sendPresent:Boolean(e.querySelector('button[type=submit]')),
                unsupportedReasons:['Attach','Voice'].every(name=>
                  [...e.querySelectorAll('button')].some(b=>b.textContent===name &&
                  b.disabled && Boolean(document.getElementById(
                    b.getAttribute('aria-describedby'))?.textContent))),
                logPolite:e.querySelector('[role=log]')?.getAttribute('aria-live')==='polite'})"""
            )
        )
    )
    skill = panel.locator("select")
    if result["multipleSkills"]:
        original = skill.input_value()
        chosen = skill.locator("option").nth(1).get_attribute("value")
        skill.select_option(chosen)
        result["skillChangesAndVisible"] = (
            skill.input_value() == chosen and chosen != original and skill.is_visible()
        )
    question.fill("Acceptance")
    question.press("Shift+Enter")
    result["shiftEnterNewline"] = "\n" in question.input_value()
    for index, prompt in enumerate(
        (
            "What can you help me with? Give a short answer without any case or resident details.",
            "Which advisory skills are available? Do not include any case or resident details.",
        )
    ):
        question.fill(prompt)
        if index == 0:
            question.press("Enter")
        else:
            panel.get_by_role("button", name="Send", exact=True).click()
        page.wait_for_function(
            "()=>document.querySelector('#employee-chat form')?.getAttribute('aria-busy')==='false'",
            timeout=60000,
        )
        result[f"turn{index + 1}RemainsOpen"] = panel.is_visible()
    result.update(
        booleans(
            panel.evaluate(
                """e=>{const l=e.querySelector('[role=log]'),f=e.querySelector('form'),
                a=[...e.querySelectorAll('.chat-widget-assistant')];return {
                multiTurn:e.querySelectorAll('.chat-widget-user').length>=2 && a.length>=2,
                actualAiLabel:a.some(x=>/AI suggestion|AI.generated/i.test(
                  x.querySelector('.chat-widget-meta')?.textContent || '') &&
                  !/no AI|workflow.only/i.test(x.querySelector('.chat-widget-meta')?.textContent || '')),
                rulesOnlyLabel:a.some(x=>/workflow.only|no AI/i.test(
                  x.querySelector('.chat-widget-meta')?.textContent || '')),
                sourcesExist:a.length>0 && a.every(x=>Boolean(x.querySelector('details'))),
                sourcesCollapsed:a.length>0 && a.every(x=>!x.querySelector('details')?.open),
                thinLabels:a.length>0 && a.every(x=>x.querySelector('.chat-widget-meta')?.tagName==='SMALL'),
                logScrollable:['auto','scroll'].includes(getComputedStyle(l).overflowY),
                newestAtBottom:l.scrollHeight-l.clientHeight-l.scrollTop<=2,
                composerBelowLog:f.getBoundingClientRect().top>=l.getBoundingClientRect().bottom-1,
                naturalChatError:Boolean(e.querySelector('[role=alert]') &&
                  !e.querySelector('[role=alert]').hidden)};}"""
            )
        )
    )
    page.emulate_media(reduced_motion="reduce")
    result["reducedMotionTokenZero"] = panel.evaluate(
        "e=>['0s','0ms'].includes(getComputedStyle(e).getPropertyValue('--dur').trim())"
    )
    page.emulate_media(reduced_motion="no-preference")
    question.press("Escape")
    result["escapeReturnsFocus"] = launcher.evaluate("e=>document.activeElement===e")
    return booleans(result)


def map_check(page):
    filters = page.locator(".overview-map-filters")
    before_size = filters.locator("strong").first.evaluate(
        "e=>parseFloat(getComputedStyle(e).fontSize)"
    )
    original = filters.element_handle()
    page.get_by_role("button", name="Expand map", exact=True).press("Enter")
    dialog = page.locator(".map-dialog[open]")
    filters = dialog.locator(".overview-map-filters")
    filters.wait_for(state="visible")
    result = booleans(
        filters.evaluate(
            """(e,before)=>({compactCounts:parseFloat(
            getComputedStyle(e.querySelector('strong')).fontSize)<before,
            alongTop:e.getBoundingClientRect().bottom <=
              document.querySelector('#leaflet').getBoundingClientRect().top+1})""",
            before_size,
        )
    )
    buttons = filters.locator("button[aria-pressed]")
    result["sixFiltersOffered"] = buttons.count() == 6
    outcomes = []
    marker_outcomes = []
    for index in [*range(1, buttons.count()), 0]:
        button = buttons.nth(index)
        with page.expect_response(
            lambda response: (
                urlsplit(response.url).path == "/api/map"
                and allowed(response.url, app=True)
            ),
            timeout=15000,
        ) as response:
            button.press("Enter" if index % 2 == 0 else "Space")
        result_ok = response.value.ok
        page.wait_for_function(
            "()=>document.querySelector('#leaflet')?.getAttribute('aria-busy')!=='true'",
            timeout=15000,
        )
        predicates = button.evaluate(
            """e=>({selected:e.getAttribute('aria-pressed')==='true',
            nonColour:e.querySelector('.tile-selection')?.textContent.includes('Selected')===true,
            focus:document.activeElement===e,
            visibleFocus:getComputedStyle(e).outlineStyle==='solid',
            exclusive:e.closest('.overview-map-filters').querySelectorAll(
              '[aria-pressed=true]').length===1})"""
        )
        outcomes.append(result_ok and all(booleans(predicates).values()))
        marker_outcomes.append(
            page.evaluate(
                """async url=>{
                const r=await fetch(url,{redirect:'error',signal:AbortSignal.timeout(8000)});
                if(!r.ok)return false;
                const d=await r.json();
                return Array.isArray(d.items) &&
                  document.querySelectorAll(d.mode==='clusters'?'.map-cluster':'.map-marker').length
                    ===d.items.length;
                }""",
                response.value.url,
            )
        )
    result["allKeyboardSelections"] = bool(outcomes) and all(outcomes)
    result["markersAgreeWithSelectedApi"] = bool(marker_outcomes) and all(
        marker_outcomes
    )
    for width in (390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        result[f"narrow{width}Readable"] = filters.evaluate(
            """e=>e.getBoundingClientRect().left>=0 &&
            e.getBoundingClientRect().right<=innerWidth &&
            document.documentElement.scrollWidth<=innerWidth &&
            [...e.querySelectorAll('button')].every(b=>b.getBoundingClientRect().width>0)"""
        )
    page.keyboard.press("Escape")
    result["sameHeaderRestored"] = original.evaluate(
        """e=>document.contains(e) && !e.closest('dialog') &&
        e.querySelectorAll('[aria-pressed=true]').length===1"""
    )
    page.set_viewport_size({"width": 1280, "height": 900})
    return booleans(result)


def case_check(page):
    page.locator('a[href^="#/case/"]').first.click(timeout=10000)
    page.locator(".case-journey").wait_for(state="visible", timeout=20000)
    result = {}
    for width in (1280, 390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        predicates = booleans(
            page.evaluate(
                """()=>{const icons=[...document.querySelectorAll('.step-icon')],
                labels=[...document.querySelectorAll('.step-name')],
                tabs=document.querySelector('[role=tablist]'),
                panel=document.querySelector('[role=tabpanel]:not([hidden])'),
                steps=[...document.querySelectorAll('.step a')];return {
                noPageOverflow:document.documentElement.scrollWidth<=innerWidth,
                iconsLoaded:icons.length===6 && icons.every(e=>e.complete && e.naturalWidth>0),
                labelsPresent:labels.length===6 && labels.every(e=>Boolean(e.textContent.trim())),
                servedJourneyIcons:icons.length===6 && icons.every(e=>
                  new URL(e.src).origin===location.origin &&
                  new URL(e.src).pathname.startsWith('/journey-icons/')),
                compactLinks:steps.length===6 && steps.every(e=>e.getBoundingClientRect().height<=100),
                tabsPresent:Boolean(tabs && panel),
                tabsOutsidePanel:Boolean(tabs && panel && !tabs.closest('[role=tabpanel]')),
                tabsAttached:Boolean(tabs && panel && tabs.parentElement===panel.parentElement &&
                  Math.abs(tabs.getBoundingClientRect().bottom-panel.getBoundingClientRect().top)<=2),
                panelScrollable:Boolean(panel && ['auto','scroll'].includes(getComputedStyle(panel).overflowY)),
                blockerOneLine:[...document.querySelectorAll('.case-blocker-summary')].length>0 &&
                  [...document.querySelectorAll('.case-blocker-summary')].every(e=>
                    getComputedStyle(e).whiteSpace==='nowrap')};}"""
            )
        )
        result.update({f"{key}{width}": value for key, value in predicates.items()})
    trigger = page.locator(".case-blocker-trigger").first
    result["blockerOffered"] = trigger.count() > 0
    if result["blockerOffered"]:
        trigger.press("Enter")
        popup = page.locator(".case-blocker-popover:popover-open")
        result["keyboardFullDetail"] = popup.count() == 1 and popup.locator(
            "dl dd"
        ).evaluate_all(
            "els=>els.length>=3 && els.every(e=>Boolean(e.textContent.trim()))"
        )
        page.keyboard.press("Escape")
        page.context.set_default_timeout(10000)
        session = page.context.new_cdp_session(page)
        try:
            session.send(
                "Emulation.setTouchEmulationEnabled",
                {"enabled": True, "maxTouchPoints": 1},
            )
            result["touchEventsSupported"] = page.evaluate(
                "()=>navigator.maxTouchPoints>0"
            )
            trigger.scroll_into_view_if_needed()
            box = trigger.bounding_box()
            if box:
                x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                session.send(
                    "Input.dispatchTouchEvent",
                    {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]},
                )
                session.send(
                    "Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []}
                )
                page.wait_for_timeout(300)
                result["touchFullDetail"] = (
                    page.locator(".case-blocker-popover:popover-open").count() == 1
                )
                page.keyboard.press("Escape")
        finally:
            session.send("Emulation.setTouchEmulationEnabled", {"enabled": False})
            session.detach()
    return booleans(result)


def inspect_shell(page, record):
    page.set_default_timeout(10000)
    record["employee"] = {}
    record["feature_execution"] = {}
    for name, check in (("chat", chat_check), ("map", map_check), ("case", case_check)):
        try:
            record["employee"][name] = check(page)
            record["feature_execution"][name] = "completed_scoped_observations"
        except (BrowserError, ValueError, TypeError):
            record["feature_execution"][name] = "observation_failed_no_raw_details"


def write_json(path, data):
    with path.open("w") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    for key in ("DEBUG", "PWDEBUG"):
        os.environ.pop(key, None)
    digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    continuation = sys.argv[1:] == ["--final-precredential-continuation"]
    if sys.argv[1:] and not continuation:
        print('{"outcome":"unsupported_invocation_refused"}')
        return
    try:
        guard = (
            RunGuard.continue_completed_precredential(
                OUT / "attempt3-manifest.json", digest
            )
            if continuation
            else RunGuard(OUT / "attempt3-manifest.json", digest)
        )
    except (OSError, ValueError, KeyError, TypeError):
        print('{"outcome":"manifest_admission_refused_no_attempt"}')
        return
    record = {
        "started": now(),
        "script_sha256": digest,
        "captures": guard.data["captures"],
        "outcome": "not_started",
    }
    secrets = ()
    try:
        if not allowed(APP, app=True) or not USERNAME or "@" not in USERNAME:
            raise ValueError("trusted_configuration_missing")
        password, tap = parse_credentials((Path.home() / ".ama-test-user").read_text())
        secrets = (password, tap)
        with tempfile.TemporaryDirectory(prefix="ama-acceptance-attempt3-") as scratch:
            old_tmp = os.environ.get("TMPDIR")
            os.environ["TMPDIR"] = scratch
            try:
                with sync_playwright() as driver:
                    browser = driver.chromium.launch(
                        headless=True, args=[f"--disk-cache-dir={scratch}/cache"]
                    )
                    record["browser_version"] = browser.version
                    try:
                        for _ in range(2 - len(guard.data["attempts"])):
                            attempt = guard.admit()
                            context = browser.new_context(
                                viewport={"width": 1280, "height": 900}
                            )
                            page = context.new_page()
                            context.set_default_timeout(8000)
                            try:
                                outcome = authenticate(
                                    page, password, tap, attempt, guard
                                )
                                attempt["status"] = outcome
                                if outcome == "authenticated":
                                    inspect_shell(page, record)
                            except (BrowserError, TimeoutError, ValueError) as error:
                                outcome = (
                                    "submission_delivery_uncertain_stop"
                                    if attempt["submission_attempted"]
                                    else "browser_or_route_failure_stop"
                                )
                                attempt["status"] = outcome
                                attempt["http_navigation_failure"] = (
                                    "ERR_HTTP_RESPONSE_CODE_FAILURE" in str(error)
                                )
                                attempt["final_origin_is_app"] = allowed(
                                    page.url, app=True
                                )
                                attempt["final_origin_is_provider"] = allowed(page.url)
                                if allowed(page.url):
                                    attempt["terminal_page"] = public_state(
                                        page, secrets, Deadline(10)
                                    )
                                elif (
                                    not attempt.get("username_submission_attempted")
                                    and not attempt["credential_fill_attempted"]
                                    and urlsplit(page.url).scheme
                                    in ("about", "chrome-error")
                                ):
                                    attempt["terminal_public_browser_text"] = sanitize(
                                        page.locator("body").inner_text(timeout=5000),
                                        secrets,
                                    )
                            finally:
                                guard.save()
                                context.close()
                            record["outcome"] = outcome
                            if outcome != "definitive_rejection":
                                break
                    finally:
                        browser.close()
                        record["browser_closed"] = True
            finally:
                if old_tmp is None:
                    os.environ.pop("TMPDIR", None)
                else:
                    os.environ["TMPDIR"] = old_tmp
        record["owned_scratch_removed"] = not Path(scratch).exists()
    except (OSError, ValueError, BrowserError, TimeoutError, TypeError):
        record["outcome"] = "automation_failure_no_raw_details"
    record["ended"] = now()
    record["attempts"] = guard.data["attempts"]
    encoded = json.dumps(record)
    if any(secret and secret in encoded for secret in secrets):
        guard.data["status"] = "unsafe_evidence_refused"
        guard.save()
        print('{"outcome":"unsafe_evidence_refused"}')
        return
    target = OUT / (
        "attempt3-second-evidence.json" if continuation else "attempt3-evidence.json"
    )
    write_json(target, record)
    guard.data.update(
        status="completed",
        ended=now(),
        evidence=target.name,
        evidence_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
    )
    if continuation:
        guard.data["evidence_files"].append(
            {"file": target.name, "sha256": guard.data["evidence_sha256"]}
        )
    guard.save()
    print(
        json.dumps(
            {
                "outcome": record["outcome"],
                "attempts": len(record["attempts"]),
                "evidence_file": target.name,
            }
        )
    )


if __name__ == "__main__":
    main()
