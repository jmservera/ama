"""Bounded capture-free live acceptance; output is aggregate evidence only."""

from __future__ import annotations

import hashlib
import json
import os
import resource
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import TimeoutError as BrowserTimeout
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
EMPLOYEE = (
    "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
)
RESIDENT = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
USERNAME = "AadiK@DIAx90853289.OnMicrosoft.com"
PROVIDERS = {"https://login.microsoftonline.com", "https://login.microsoft.com"}
SECRETS: list[str] = []

BINDING = r"""async expected => {
  const r = await fetch('/api/me', {redirect:'error',
    signal:AbortSignal.timeout(120000)});
  const responseOk = r.status === 200 && !r.redirected &&
    (r.headers.get('content-type') || '').includes('application/json');
  if (!responseOk) return {responseOk:false, authenticated:false};
  const d=await r.json(), u=d?.user, a=d?.account;
  const guid = x => typeof x === 'string' &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(x);
  const schemaValid = Boolean(u && a && typeof a.email === 'string' &&
    typeof u.code === 'string' && u.code && typeof u.email === 'string' &&
    u.email && guid(u.tid) && guid(u.oid) && typeof u.view_only === 'boolean' &&
    Array.isArray(u.app_roles));
  const providerMatches = a?.provider === 'trusted-proxy' &&
    u?.auth_provider === 'trusted-proxy';
  const expectedIdentity = typeof a?.email === 'string' &&
    a.email.trim().toLowerCase() === expected.toLowerCase();
  const employeeRole = u?.role === 'Retrofit Programme Manager' &&
    Array.isArray(u?.app_roles) && u.app_roles.includes('ZavaForward.ProgrammeManager');
  const notViewOnly = u?.view_only === false;
  return {responseOk, schemaValid, providerMatches, expectedIdentity, employeeRole,
    notViewOnly, authenticated:schemaValid && providerMatches && expectedIdentity &&
      employeeRole && notViewOnly,
    rosterBound:Boolean(u?.bound?.code && u?.bound?.email)};
}"""

CHAT = """e => {
 const log=e.querySelector('[role=log]'), form=e.querySelector('form');
 const launcher=document.querySelector('[aria-controls="'+e.id+'"]');
 const r=launcher.getBoundingClientRect();
 return {dialog:e.getAttribute('role')==='dialog' && !e.hidden,
  bottomRight:innerWidth-r.right>=0 && innerWidth-r.right<=32 &&
    innerHeight-r.bottom>=0 && innerHeight-r.bottom<=32,
  logLive:log.getAttribute('aria-live')==='polite',
  composer:!!form.querySelector('textarea') && !!form.querySelector('select'),
  send:!!form.querySelector('button[type=submit]'),
  unsupported:['Attach','Voice'].every(name=>[...form.querySelectorAll('button')]
    .some(b=>b.textContent===name && b.disabled && !!document.getElementById(
      b.getAttribute('aria-describedby'))?.textContent)),
  messageCount:log.querySelectorAll('article').length,
  assistantCount:log.querySelectorAll('.chat-widget-assistant').length,
  ordered:[...log.querySelectorAll('article')].every((x,i)=>
    x.classList.contains(i%2?'chat-widget-assistant':'chat-widget-user')),
  collapsedSources:[...log.querySelectorAll('details')].every(d=>!d.open),
  noAiLabel:[...log.querySelectorAll('.chat-widget-assistant>small')]
    .every(x=>!/^AI(?:-| |$)/i.test(x.textContent)),
  logScroll: ['auto','scroll'].includes(getComputedStyle(log).overflowY),
  atBottom:Math.abs(log.scrollHeight-log.clientHeight-log.scrollTop)<=2,
  scrollHeight:log.scrollHeight, clientHeight:log.clientHeight};
}"""


def now():
    return datetime.now(UTC).isoformat()


def failure_code(error):
    if isinstance(error, BrowserTimeout):
        return "browser_timeout_unproven"
    if isinstance(error, BrowserError):
        return "browser_operation_failed_unproven"
    if isinstance(error, ValueError):
        return "safety_or_schema_refused"
    if isinstance(error, OSError):
        return "local_io_failed"
    return "unexpected_failure_unproven"


def credentials(raw, resident=False):
    lines = raw.splitlines()
    required = 2 if resident else 1
    if len(lines) != required or any(not line.strip() for line in lines):
        raise ValueError("credential_shape")
    return tuple(line.strip() for line in lines)


def allowed(url, origins):
    parsed = urlsplit(url)
    return (
        parsed.scheme == "https"
        and parsed.username is None
        and parsed.password is None
        and parsed.port in (None, 443)
        and f"https://{parsed.hostname}" in origins
    )


def origin_guard(page, origins):
    if not allowed(page.url, origins):
        raise ValueError("origin_refused")


def diagnostics_guard(environ):
    if any(
        environ.get(key)
        for key in ("DEBUG", "PWDEBUG", "PLAYWRIGHT_DEBUG", "DEBUG_FILE")
    ):
        raise ValueError("diagnostics_refused")


def safe_json(value, secrets):
    text = json.dumps(value, indent=2)
    if any(secret and secret in text for secret in secrets):
        raise ValueError("secret_output_refused")
    return text + "\n"


def write(path, value):
    content = safe_json(value, SECRETS)
    with path.open("w") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


class Guard:
    def __init__(self, path):
        self.path = path
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
        self.data = {"started": now(), "attempts": {}, "completed": False}
        self.save()

    def save(self):
        write(self.path, self.data)

    def admit(self, site):
        attempts = self.data["attempts"].setdefault(site, [])
        if len(attempts) >= 2 or any(a["submission_intent"] for a in attempts):
            raise ValueError("attempt_refused")
        entry = {
            "number": len(attempts) + 1,
            "started": now(),
            "submission_intent": False,
        }
        attempts.append(entry)
        self.save()
        return entry

    def submit(self, entry):
        if entry["submission_intent"]:
            raise ValueError("resubmit_refused")
        entry["submission_intent"] = True
        self.save()


class Evidence:
    def __init__(self):
        self.data = {
            "started": now(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "steps": [],
            "captures": False,
        }

    def step(self, action, function):
        row = {"command": action, "started": now()}
        self.data["steps"].append(row)
        try:
            row["result"] = function()
            row["status"] = "observed"
            return row["result"]
        except BrowserTimeout:
            row["status"] = "timeout_unproven"
        except Exception as error:  # noqa: BLE001 - never emit credential-bearing diagnostics
            row["status"] = "operation_failed_unproven"
            row["failureCode"] = failure_code(error)
        finally:
            row["finished"] = now()
            write(OUT / "evidence.json", self.data)
        return None


def warm(request, base):
    results = []
    for _ in range(3):
        try:
            response = request.get(base + "/healthz", timeout=120000)
            results.append({"http": response.status})
            if response.status == 200:
                return {"warm": True, "tries": results}
        except BrowserTimeout:
            results.append({"cold_start_timeout": True})
        except BrowserError as error:
            results.append({"public_connectivity": failure_code(error)})
        time.sleep(3)
    return {"warm": False, "tries": results}


def navigate(page, url):
    for attempt in range(3):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            return
        except BrowserTimeout:
            if attempt == 2:
                raise
            time.sleep(3)


def resident_login(page, guard):
    entry = guard.admit("resident")
    navigate(page, RESIDENT + "/")
    email = page.locator("#email")
    password = page.locator("#password")
    email.wait_for(state="visible", timeout=120000)
    values = credentials((Path.home() / ".ama-resident-test-user").read_text(), True)
    SECRETS.extend(values)
    origin_guard(page, {RESIDENT})
    email.evaluate("e=>e.type='password'")
    email.fill(values[0])
    origin_guard(page, {RESIDENT})
    password.fill(values[1])
    origin_guard(page, {RESIDENT})
    guard.submit(entry)
    with page.expect_response(
        lambda r: r.url == RESIDENT + "/demo/login" and r.request.method == "POST",
        timeout=120000,
    ) as response:
        page.locator("#signin-button").click(no_wait_after=True)
    status = response.value.status
    email.evaluate("e=>e.value=''")
    password.evaluate("e=>e.value=''")
    if status != 200:
        return {"authenticated": False, "loginHttp": status}
    page.locator("#content").wait_for(state="visible", timeout=120000)
    return {"authenticated": True, "loginHttp": status, "fieldsCleared": True}


def employee_login(page, guard):
    entry = guard.admit("employee")
    navigate(page, EMPLOYEE + "/.auth/login/aad?post_login_redirect_uri=%2Fapp")
    username_sent = False
    submitted = False
    kmsi = False
    end = time.monotonic() + 300
    callback_end = None
    callback_transitions = 0
    while time.monotonic() < (callback_end or end):
        if allowed(page.url, {EMPLOYEE}) and submitted:
            try:
                result = page.evaluate(BINDING, USERNAME)
                if result.get("authenticated"):
                    return dict(
                        result,
                        kmsiHandled=kmsi,
                        callbackTransitions=callback_transitions,
                    )
            except BrowserError:
                # Navigation may destroy execution during an otherwise valid callback.
                callback_transitions += 1
        elif allowed(page.url, PROVIDERS):
            email = page.locator("input[type=email]:visible")
            password = page.locator("input[name=passwd][type=password]:visible")
            if email.count() and not username_sent:
                origin_guard(page, PROVIDERS)
                email.fill(USERNAME)
                origin_guard(page, PROVIDERS)
                page.locator("input[type=submit]:visible").press(
                    "Enter", no_wait_after=True
                )
                username_sent = True
            elif password.count() and not submitted and username_sent:
                password.wait_for(state="visible", timeout=120000)
                value = credentials((Path.home() / ".ama-test-user").read_text())[0]
                SECRETS.append(value)
                origin_guard(page, PROVIDERS)
                password.fill(value)
                origin_guard(page, PROVIDERS)
                guard.submit(entry)
                submitted = True
                callback_end = time.monotonic() + 180
                page.locator("input[type=submit]:visible").press(
                    "Enter", no_wait_after=True
                )
            elif submitted and not kmsi:
                no = page.get_by_role("button", name="No", exact=True)
                if no.count() and no.is_visible():
                    origin_guard(page, PROVIDERS)
                    kmsi = True
                    no.press("Enter", no_wait_after=True)
        else:
            return {"authenticated": False, "unexpectedOrigin": True}
        page.wait_for_timeout(1000)
    return {
        "authenticated": False,
        "usernameSubmitted": username_sent,
        "passwordSubmissionIntent": submitted,
        "kmsiHandled": kmsi,
        "callbackWaitExhausted": True,
        "callbackTransitions": callback_transitions,
    }


def chat_open(page, resident):
    root = "#resident-chat" if resident else "#employee-chat"
    launcher = page.get_by_role("button", name="Chat", exact=True)
    launcher.wait_for(state="visible", timeout=120000)
    launcher.press("Enter")
    panel = page.locator(root)
    panel.wait_for(state="visible", timeout=120000)
    page.wait_for_function(
        "root=>{const e=document.querySelector(root+' textarea');return e&&!e.disabled}",
        arg=root,
        timeout=120000,
    )
    return panel.evaluate(CHAT)


def send(page, root, question, key):
    panel = page.locator(root)
    before = panel.locator(".chat-widget-assistant").count()
    field = panel.locator("textarea")
    field.fill(question)
    if key == "Enter":
        field.press("Enter")
    else:
        panel.get_by_role("button", name="Send", exact=True).click()
    page.wait_for_function(
        """({root,before})=>document.querySelectorAll(
          root+' .chat-widget-assistant').length>before ||
          !document.querySelector(root+' [role=alert]').hidden""",
        arg={"root": root, "before": before},
        timeout=120000,
    )
    page.wait_for_function(
        "root=>document.querySelector(root+' form').getAttribute('aria-busy')==='false'",
        arg=root,
        timeout=120000,
    )
    return panel.evaluate(CHAT)


def resident_consent(page):
    requests = []

    def count(request):
        if request.url == RESIDENT + "/demo/assistant" and request.method == "POST":
            requests.append(now())

    page.on("request", count)
    try:
        field = page.locator("#assistant-question")
        field.fill("My home smells like a dead rat")
        field.press("Enter")
        page.locator("#resident-chat-error").wait_for(state="visible")
        result = {
            "noAssistantRequest": not requests,
            "explicitConsentError": page.locator("#resident-chat-error").evaluate(
                "e=>e.textContent.includes('Agree to use your own record')"
            ),
        }
        page.locator("#assistant-consent").check()
        result["consented"] = page.locator("#assistant-consent").is_checked()
        result["consentAt"] = now()
        result["ratSend"] = send(
            page, "#resident-chat", "My home smells like a dead rat", "Enter"
        )
        result["requestTimes"] = requests.copy()
        result["fallback"] = page.locator(
            "#resident-chat .chat-widget-assistant"
        ).first.evaluate("""e=>({
          aiNotEnabled:/AI (?:is )?not enabled/i.test(e.textContent),
          humanRoute:/housing officer|repairs service/i.test(e.textContent),
          noHomeSummary:!/^Your home/i.test(e.querySelector('p')?.textContent||''),
          advisory:/not.*(?:sent|alerted)|contact|ask/i.test(e.textContent),
          noAiLabel:[...e.querySelectorAll('small')].every(x=>
            !/^AI(?:-| |$)/i.test(x.textContent)),
          collapsedSources:!e.querySelector('details').open
        })""")
        return result
    finally:
        page.remove_listener("request", count)


def chat_interactions(page, root):
    panel = page.locator(root)
    field = panel.locator("textarea")
    before = panel.locator("article").count()
    field.fill("Line one")
    field.press("Shift+Enter")
    newline = "\n" in field.input_value()
    page.wait_for_timeout(300)
    no_message = panel.locator("article").count() == before
    second = send(page, root, "What is my case status?", "Send")
    count = panel.locator("article").count()
    page.keyboard.press("Escape")
    focus = page.get_by_role("button", name="Chat", exact=True).evaluate(
        "e=>e===document.activeElement"
    )
    page.get_by_role("button", name="Chat", exact=True).press("Enter")
    persisted = panel.locator("article").count() == count
    field.focus()
    focus_visible = field.evaluate(
        "e=>getComputedStyle(e).outlineStyle==='solid' && "
        "parseFloat(getComputedStyle(e).outlineWidth)>0"
    )
    widths = []
    for width in (1280, 390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        widths.append(
            panel.evaluate("""e=>{
              const log=e.querySelector('[role=log]'),f=e.querySelector('form');
              const top=f.getBoundingClientRect().top, r=e.getBoundingClientRect();
              log.scrollTop=0; const first=log.scrollTop;
              const stable=Math.abs(f.getBoundingClientRect().top-top)<=1;
              log.scrollTop=log.scrollHeight;
              return {width:innerWidth,contained:r.left>=0 && r.right<=innerWidth,
                pageOverflow:document.documentElement.scrollWidth>innerWidth,
                composerBelow:top>=log.getBoundingClientRect().bottom-1,
                scrollable:log.scrollHeight>log.clientHeight,
                directScroll:log.scrollTop>first,composerStable:stable,
                atBottom:Math.abs(log.scrollHeight-log.clientHeight-log.scrollTop)<=2};
            }""")
        )
    page.emulate_media(reduced_motion="no-preference")
    normal = panel.evaluate(
        "e=>getComputedStyle(e).getPropertyValue('--motion').trim()"
    )
    page.emulate_media(reduced_motion="reduce")
    reduced = panel.evaluate(
        "e=>getComputedStyle(e).getPropertyValue('--motion').trim()"
    )
    return {
        "newline": newline,
        "newlineNoMessage": no_message,
        "secondSend": second,
        "persisted": persisted,
        "escapeFocus": focus,
        "visibleFocus": focus_visible,
        "geometry": widths,
        "normalMotion": normal,
        "reducedMotion": reduced,
    }


def skill_check(page):
    panel = page.locator("#employee-chat")
    select = panel.locator("form select")
    options = select.locator("option").evaluate_all("es=>es.map(e=>e.value)")
    if len(options) < 2:
        return {"multiple": False}
    select.select_option(options[1])
    result = send(page, "#employee-chat", "What can this skill help me do?", "Enter")
    return {
        "multiple": True,
        "activeChoiceChanged": select.input_value() == options[1],
        "replyNamesSelectedSkill": panel.locator(
            ".chat-widget-assistant"
        ).last.evaluate(
            "(e,skill)=>e.textContent.includes('Skill: '+skill)", options[1]
        ),
        "send": result,
    }


def map_check(page):
    page.keyboard.press("Escape")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.evaluate("location.hash='#/overview'")
    page.locator(".overview-map-filters").wait_for(state="visible", timeout=120000)
    area = page.locator("#mapArea")
    before_size = page.locator(".overview-map-filters strong").first.evaluate(
        "e=>parseFloat(getComputedStyle(e).fontSize)"
    )
    page.get_by_role("button", name="Expand map", exact=True).press("Enter")
    filters = page.locator(".map-dialog[open] .overview-map-filters")
    filters.wait_for(state="visible")
    compact = (
        filters.locator("strong").first.evaluate(
            "e=>parseFloat(getComputedStyle(e).fontSize)"
        )
        < before_size
    )
    flags = []
    for index in range(min(3, filters.locator("button[aria-pressed]").count())):
        button = filters.locator("button[aria-pressed]").nth(index)
        # A filter may already be selected; choose a different one first.
        if button.get_attribute("aria-pressed") == "true":
            continue
        with page.expect_response(
            lambda r: r.url.startswith(EMPLOYEE + "/api/map?"), timeout=120000
        ) as response:
            button.press("Space" if index % 2 else "Enter")
        total = response.value.json().get("total")
        page.wait_for_function(
            "()=>document.querySelector('#leaflet')?.getAttribute('aria-busy')!=='true'",
            timeout=120000,
        )
        flags.append(
            {
                "http": response.value.status,
                "apiTotal": total,
                "markers": page.locator(".map-marker").count(),
                "selected": button.get_attribute("aria-pressed") == "true",
                "nonColour": button.locator(".tile-selection").inner_text()
                == "Selected",
                "focused": button.evaluate("e=>e===document.activeElement"),
            }
        )
    geometry = []
    for width in (1280, 390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        geometry.append(
            filters.evaluate("""e=>{
             const r=e.getBoundingClientRect(),m=document.querySelector('#leaflet').getBoundingClientRect();
             return {width:innerWidth,contained:r.left>=0&&r.right<=innerWidth,
               topOfMap:r.top<=m.top,
               noOverflow:e.scrollWidth<=e.clientWidth+1};
            }""")
        )
    selected_index = filters.locator("button[aria-pressed]").evaluate_all(
        "es=>es.findIndex(e=>e.getAttribute('aria-pressed')==='true')"
    )
    page.get_by_role("button", name="Exit expanded map", exact=True).click()
    restored = (
        page.locator(".map-filter-slot .overview-map-filters button[aria-pressed]")
        .nth(selected_index)
        .get_attribute("aria-pressed")
        == "true"
    )
    return {
        "compact": compact,
        "filters": flags,
        "geometry": geometry,
        "restored": restored,
        "areaPresent": area.count() == 1,
    }


def case_check(page):
    page.set_viewport_size({"width": 1280, "height": 900})
    page.evaluate("location.hash='#/all'")
    link = page.locator('a[href^="#/case/"]').first
    link.wait_for(state="visible", timeout=120000)
    link.click()
    page.locator(".case-journey").wait_for(state="visible", timeout=120000)
    icons = page.locator(".step-icon").evaluate_all(
        "es=>({count:es.length,loaded:es.every(e=>e.complete&&e.naturalWidth>0),"
        "decorative:es.every(e=>e.alt===''&&e.getAttribute('aria-hidden')==='true'),"
        "journeyAssets:es.every(e=>new URL(e.src).pathname.startsWith('/journey-icons/'))})"
    )
    geometry = []
    for width in (1280, 390, 320):
        page.set_viewport_size({"width": width, "height": 900})
        geometry.append(
            page.evaluate("""()=>({
              width:innerWidth,noOverflow:document.documentElement.scrollWidth<=innerWidth,
              heights:[...document.querySelectorAll('.step')].map(e=>e.getBoundingClientRect().height),
              labels:document.querySelectorAll('.step-name').length,
              tabsOutsidePanel:!document.querySelector('[role=tablist]')?.closest('.case-tab-panel'),
              attached:document.querySelector('[role=tablist]')?.parentElement.classList.contains('case-sections')
            })""")
        )
    trigger = page.locator(".case-blocker-trigger").first
    blocker = {"present": trigger.count() > 0}
    if trigger.count():
        blocker["oneLine"] = trigger.locator(".case-blocker-summary").evaluate(
            "e=>getComputedStyle(e).whiteSpace==='nowrap' && "
            "e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)+1"
        )
        trigger.press("Enter")
        popup = page.locator(".case-blocker-popover:popover-open")
        popup.wait_for(state="visible")
        blocker["keyboardDisclosure"] = popup.locator("dd").count() >= 3
        page.keyboard.press("Escape")
        blocker["escapeFocus"] = trigger.evaluate("e=>e===document.activeElement")
        page.touchscreen.tap(
            *trigger.evaluate(
                "e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"
            )
        )
        blocker["touchDisclosure"] = popup.is_visible()
        page.keyboard.press("Escape")
    tabs = page.get_by_role("tablist", name="Case sections")
    tab = tabs.get_by_role("tab").first
    tab.press("Home")
    tab.press("End")
    page.keyboard.press("Enter")
    selected = tabs.locator("[aria-selected=true]")
    tabpanel = page.get_by_role("tabpanel")
    panel_record = tabpanel.evaluate("""e=>{
      const t=document.querySelector('[role=tablist]'), b=t.getBoundingClientRect();
      e.scrollTop=0; const start=e.scrollTop; e.scrollTop=e.scrollHeight;
      return {scrollable:e.scrollHeight>e.clientHeight,
        directScroll:e.scrollTop>start,tabsStable:Math.abs(t.getBoundingClientRect().top-b.top)<=1,
        panelBelow:e.getBoundingClientRect().top>=b.bottom-1,
        overflow:['auto','scroll'].includes(getComputedStyle(e).overflowY)};
    }""")
    return {
        "icons": icons,
        "geometry": geometry,
        "blocker": blocker,
        "tabKeyboardSelected": selected.count() == 1,
        "tabPanel": panel_record,
    }


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    diagnostics_guard(os.environ)
    guard = Guard(OUT / "manifest.json")
    evidence = Evidence()
    browser = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            evidence.data["browser"] = browser.version
            request = pw.request.new_context()
            hashes = {}
            warm_sites = set()
            for name, base in (("employee", EMPLOYEE), ("resident", RESIDENT)):
                warmed = evidence.step(
                    name + ": GET /healthz timeout=120000 retries=3",
                    lambda base=base: warm(request, base),
                )
                if not warmed or not warmed["warm"]:
                    continue
                warm_sites.add(name)

                def widget_hash(base=base, name=name):
                    response = request.get(base + "/chat-widget.js", timeout=120000)
                    hashes[name] = hashlib.sha256(response.body()).hexdigest()
                    return {"http": response.status, "sha256": hashes[name]}

                evidence.step(name + ": GET /chat-widget.js", widget_hash)
            request.dispose()
            evidence.data["sharedWidgetBytes"] = (
                len(hashes) == 2 and hashes["employee"] == hashes["resident"]
            )
            for name in ("resident", "employee"):
                if name not in warm_sites:
                    evidence.data[name + "Features"] = "blocked_cold_start_unresolved"
                    continue
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900}, has_touch=True
                )
                page = context.new_page()
                page.set_default_timeout(120000)
                page.set_default_navigation_timeout(120000)
                try:
                    resident = name == "resident"
                    admitted = evidence.step(
                        name + ": bounded actual form sign-in, callback wait <=180s",
                        lambda page=page, resident=resident: (
                            resident_login(page, guard)
                            if resident
                            else employee_login(page, guard)
                        ),
                    )
                    if not admitted or not admitted.get("authenticated"):
                        evidence.data[name + "Features"] = "blocked_no_verified_session"
                        continue
                    root = "#resident-chat" if resident else "#employee-chat"
                    opened = evidence.step(
                        name + ": Chat Enter opens native shared dialog",
                        lambda page=page, resident=resident: chat_open(page, resident),
                    )
                    if opened:
                        if resident:
                            evidence.step(
                                "resident: no-consent Enter, consent, actual rat Enter reply",
                                lambda page=page: resident_consent(page),
                            )
                        else:
                            evidence.step(
                                "employee: select next skill, actual Enter reply",
                                lambda page=page: skill_check(page),
                            )
                        evidence.step(
                            name
                            + ": Shift+Enter, Send, Escape/reopen, scroll, widths, motion",
                            lambda page=page, root=root: chat_interactions(page, root),
                        )
                    if not resident:
                        evidence.step(
                            "employee: expanded map keyboard filters/API totals/narrow/restore",
                            lambda page=page: map_check(page),
                        )
                        evidence.step(
                            "employee: actual case icons/blocker keyboard+touch/tabs/widths",
                            lambda page=page: case_check(page),
                        )
                finally:
                    context.close()
                    evidence.data[name + "ContextClosed"] = True
            browser.close()
            browser = None
            evidence.data["browserClosed"] = True
    except Exception as error:  # noqa: BLE001 - record failure without raw browser diagnostics
        evidence.data["runnerFailure"] = failure_code(error)
    finally:
        if browser is not None:
            try:
                browser.close()
            except BrowserError as error:
                evidence.data["cleanupFailure"] = failure_code(error)
        evidence.data["finished"] = now()
        evidence.data["script_sha256_after"] = hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest()
        write(OUT / "evidence.json", evidence.data)
        guard.data["completed"] = True
        guard.save()
    print("Capture-free acceptance finished; inspect aggregate evidence.json.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # noqa: BLE001 - last capture-free process boundary
        print("Acceptance stopped safely: " + failure_code(error))
        raise SystemExit(1) from None
