"""Local engineering probes on fictional data; not human UX or WCAG conformance."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

from playwright.sync_api import sync_playwright

from properwarm_mvp.exercise import manifest

ROOT = Path(__file__).resolve().parents[1]

def native_zoom_keys(repetitions: int, reset: bool = False) -> None:
    """Send real X11 browser accelerators, not CSS/CDP viewport emulation."""
    import ctypes
    import ctypes.util
    x11 = ctypes.CDLL(ctypes.util.find_library("X11"))
    xtst = ctypes.CDLL(ctypes.util.find_library("Xtst"))
    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.c_void_p
    x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    x11.XKeysymToKeycode.restype = ctypes.c_uint
    x11.XFlush.argtypes = [ctypes.c_void_p]
    x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
    xtst.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]
    display = x11.XOpenDisplay(None)
    if not display:
        raise RuntimeError("Native zoom requires an explicitly available isolated X11 display.")
    try:
        control = x11.XKeysymToKeycode(display, 0xffe3)
        target = x11.XKeysymToKeycode(display, 0x30 if reset else 0x3d)
        if not control or not target:
            raise RuntimeError("Native zoom key mapping is unavailable.")
        for _ in range(repetitions):
            for key, pressed in ((control, 1), (target, 1), (target, 0), (control, 0)):
                xtst.XTestFakeKeyEvent(display, key, pressed, 0)
            x11.XFlush(display)
            time.sleep(.1)
    finally:
        x11.XCloseDisplay(display)


def main() -> int:
    """Run browser profiles, parser journey and viewport/focus probes locally."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--native-zoom", action="store_true", help="Headed Chrome, isolated X11 display and real 400% zoom accelerators")
    args = parser.parse_args()
    state = args.state.resolve()
    if state.exists():
        raise SystemExit("Use a new named state directory; no existing data is deleted.")
    state.mkdir(parents=True)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    password = secrets.token_urlsafe(24)
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(("PW_", "AI_", "IDENTITY_"))}
    env.update(PW_EXERCISE="1", PW_STATE=str(state), PW_STORE="sqlite",
               PW_DOC_STORE="local", PW_AI="off", PW_PASSWORD=password, PORT=str(port))
    results = []

    def record(name: str, passed: bool, detail: object = None) -> None:
        results.append({"check": name, "result": "Pass" if passed else "Fail", "detail": detail})

    with (state / "server.log").open("w") as log:
        cold_started = time.perf_counter()
        server = subprocess.Popen([sys.executable, "-m", "properwarm_mvp.server"],
                                  cwd=ROOT, env=env, stdout=log, stderr=log)
        try:
            for attempt in range(100):
                if server.poll() is not None:
                    raise RuntimeError("Exercise server exited; inspect named server.log.")
                try:
                    with urllib.request.urlopen(base + "/healthz", timeout=1) as response:
                        if response.status == 200:
                            break
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(.1)
            else:
                raise RuntimeError("Exercise health endpoint did not become ready.")
            record("initial-cold-exercise-startup", True,
                   {"seconds_to_first_health_200": time.perf_counter() - cold_started,
                    "fixture": "Fresh 18-home SQLite exercise state; no warm-up before initial health",
                    "boundary": "Local initial process startup, not cloud cold scaling or scale-fixture startup"})
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(channel="chrome", headless=not args.native_zoom,
                                                     args=["--window-size=1280,900"] if args.native_zoom else [])
                errors, bad_responses = [], []
                version = browser.version
                for profile in manifest()["profiles"]:
                    context = browser.new_context(viewport={"width": 1280, "height": 900})
                    context.route("**/*", lambda route: route.continue_()
                                  if route.request.url.startswith(base) else route.abort())
                    page = context.new_page()
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.on("response", lambda response: bad_responses.append(response.status)
                            if response.status >= 500 else None)
                    page.goto(base)
                    page.locator("#email").fill(profile["actor"].lower() + "@example.test")
                    page.locator("#pw").fill(password)
                    page.locator("button[type=submit]").click()
                    page.wait_for_function("() => document.getElementById('nav').hidden === false")
                    page.goto(base + "#/exercise/EX-HOME-001")
                    page.get_by_role("heading", name="EX-HOME-001: Intake", exact=True).wait_for()
                    text = page.locator("#app").inner_text()
                    record("profile-" + profile["id"], "Owner:" in text and "Blockers" in text,
                           {"role": profile["role"], "script": "Find owner, blocker and next route"})
                    page.get_by_role("link", name="Open building EX-BUILDING-001 (home gates stay independent)", exact=True).click()
                    page.get_by_role("heading", name="Building EX-BUILDING-001", exact=True).wait_for()
                    building_text = page.locator("#app").inner_text()
                    record("building-navigation-" + profile["id"],
                           "Independent linked homes" in building_text and "Unknown: home costs" in building_text
                           and page.get_by_role("link", name="EX-HOME-001", exact=True).count() == 1
                           and page.get_by_role("link", name="EX-HOME-002", exact=True).count() == 1)
                    page.get_by_role("link", name="EX-HOME-002", exact=True).click()
                    page.get_by_role("heading", name="EX-HOME-002: Intake", exact=True).wait_for()
                    page.get_by_role("link", name="Open building EX-BUILDING-001 (home gates stay independent)", exact=True).click()
                    page.get_by_role("heading", name="Building EX-BUILDING-001", exact=True).wait_for()
                    page.get_by_role("link", name="EX-HOME-001", exact=True).click()
                    page.get_by_role("heading", name="EX-HOME-001: Intake", exact=True).wait_for()
                    if profile["role"] == "Contractor":
                        record("profile-controlled-safe-block-" + profile["id"],
                               page.get_by_text("Read assigned scope only.", exact=False).count() == 1
                               and page.locator("#exercise-record-action").count() == 0,
                               {"task": "No funding event editor for assigned-scope contractor"})
                    else:
                        page.locator("summary").filter(has_text="Record one explicitly supplied exercise event").click()
                        page.get_by_label("Event type", exact=True).select_option("funding-event")
                        page.get_by_label("Separate external evidence state", exact=True).select_option("award")
                        page.get_by_role("button", name="Record one supplied event", exact=True).click()
                        page.locator("#app [role=alert][aria-live=polite]").wait_for()
                        refusal = page.locator("#app [role=alert][aria-live=polite]").inner_text()
                        finance_role = profile["role"] in ("Grants and Evidence Officer", "Retrofit Programme Manager",
                                                           "Programme Support Officer")
                        expected = "same-home reviewed form export" if finance_role else "Only Finance identities"
                        record("profile-controlled-safe-block-" + profile["id"], expected in refusal,
                               {"task": "Award without reviewed same-home export must fail without mutation",
                                "expected_refusal": expected, "observed": refusal})
                    if profile["id"] == "finance":
                        page.get_by_role("button", name="Create one draft", exact=True).click()
                        page.get_by_role("heading", name="FORM-001 competitive", exact=False).wait_for()
                        for source in ("EX-EPC-A", "EX-EPC-B"):
                            page.get_by_role("button", name=f"Parse {source}", exact=False).click()
                            page.get_by_role("heading", name="FORM-001 competitive", exact=False).wait_for()
                        page.locator("summary").filter(has_text="epc_band: conflict").wait_for()
                        record("browser-real-parser-conflict", page.locator("summary").filter(has_text="epc_band: conflict").count() == 1)
                        for width in (320, 390, 1280):
                            page.set_viewport_size({"width": width, "height": 900})
                            page.wait_for_timeout(100)
                            overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                            record(f"form-reflow-{width}px", not overflow)
                            if width == 390:
                                page.screenshot(path=str(args.output.parent / "exercise-form-390.png"), full_page=True)
                        page.evaluate("() => {document.documentElement.style.fontSize = '200%'; document.body.style.fontSize = '32px'}")
                        record("text-resize-200-percent",
                               page.evaluate("parseFloat(getComputedStyle(document.body).fontSize) >= 32")
                               and not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"))
                        page.evaluate("() => {document.documentElement.style.fontSize = ''; document.body.style.fontSize = ''}")
                        page.evaluate("document.body.style.zoom = '4'")
                        record("css-4x-zoom-reflow-probe-not-browser-zoom",
                               not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"))
                        page.evaluate("document.body.style.zoom = ''")
                        page.keyboard.press("Tab")
                        record("keyboard-visible-focus", page.evaluate(
                            "document.activeElement !== document.body && getComputedStyle(document.activeElement).outlineStyle !== 'none'"))
                        record("form-input-labels", page.evaluate(
                            """[...document.querySelectorAll('#app input:not([type=hidden]),#app select,#app textarea')]
                            .every(e => e.getAttribute('aria-label') || e.labels.length)"""))
                        record("no-duplicate-dom-ids", page.evaluate(
                            """(() => {const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
                            return new Set(ids).size===ids.length})()"""))
                        record("visible-form-control-target-size", page.evaluate("""() =>
                            [...document.querySelectorAll('#app button,#app input,#app select,#app summary')]
                            .filter(e=>e.getClientRects().length)
                            .every(e=>{const r=e.getBoundingClientRect();return r.width>=24 && r.height>=24})"""))
                        palette = page.evaluate("""() => {const c=getComputedStyle(document.documentElement);
                            return Object.fromEntries(['ink','muted','brand','brand-d','warn','soft','bg'].map(k=>[k,c.getPropertyValue('--'+k).trim()]))}""")
                        def luminance(color):
                            channels = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
                            linear = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in channels]
                            return sum(x * coefficient for x, coefficient in zip(linear, (.2126, .7152, .0722)))
                        ratios = {}
                        for foreground, background in (("ink", "#ffffff"), ("muted", "#ffffff"),
                                                       ("brand", "#ffffff"), ("brand-d", "soft"), ("warn", "#fde8e6")):
                            light, dark = sorted((luminance(palette.get(foreground, foreground)),
                                                  luminance(palette.get(background, background))), reverse=True)
                            ratios[foreground + "-on-" + background] = (light + .05) / (dark + .05)
                        record("declared-text-palette-contrast", all(ratio >= 4.5 for ratio in ratios.values()), ratios)
                        page.goto(base + "#/exercise")
                        page.get_by_role("heading", name="Nine connected workflows", exact=True).wait_for()
                        record("nine-workflow-navigation", page.locator("#app article h3").count() >= 9)
                        record("forecast-table-equivalent", page.locator("#exercise-forecast table caption").count() == 5
                               and "missing_input: abstained" in page.locator("#exercise-forecast").inner_text())
                        page.locator("#exercise-forecast summary").first.click()
                        page.screenshot(path=str(args.output.parent / "exercise-overview.png"), full_page=True)
                    context.close()
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                context.route("**/*", lambda route: route.continue_()
                              if route.request.url.startswith(base) else route.abort())
                csrf = {"X-PW-CSRF": "1"}
                for actor, endpoint, body in (
                    ("ex-rc-01", "technical", {"action": "design_submit", "note": "Fictional individual loft scope"}),
                    ("ex-rlo-01", "resident", {"action": "decision_record", "measure": "Loft insulation",
                     "scope": "Loft insulation", "design_version": 1, "status": "Withdrawn",
                     "answered_by": "The resident", "note": "Wholly fictional supplied individual withdrawal"}),
                ):
                    signed_in = context.request.post(base + "/api/login",
                        data={"email": actor + "@example.test", "password": password}, headers=csrf)
                    changed = context.request.post(base + "/api/cases/EX-HOME-001/" + endpoint,
                                                   data=body, headers=csrf)
                    if not signed_in.ok or not changed.ok:
                        raise RuntimeError("Distinct-home fixture action rejected: " + changed.text())
                page = context.new_page()
                page.goto(base + "#/exercise/building/EX-BUILDING-001")
                page.get_by_role("heading", name="Building EX-BUILDING-001", exact=True).wait_for()
                lead = page.locator("#app article").filter(has=page.get_by_role("link", name="EX-HOME-001", exact=True))
                sibling = page.locator("#app article").filter(has=page.get_by_role("link", name="EX-HOME-002", exact=True))
                lead.locator("summary").click()
                sibling.locator("summary").click()
                record("building-distinct-home-consent-and-design-display",
                       "Withdrawn" in lead.inner_text() and "Withdrawn" not in sibling.inner_text()
                       and '"design_version": 1' in lead.inner_text() and '"design_version": 1' not in sibling.inner_text(),
                       {"fixture": "Supplied fictional withdrawal/design on lead only; sibling retains own unchanged gates"})
                context.close()

                def home_session(actor):
                    session = browser.new_context(viewport={"width": 1280, "height": 900})
                    session.route("**/*", lambda route: route.continue_()
                                  if route.request.url.startswith(base) else route.abort())
                    view = session.new_page()
                    view.goto(base)
                    view.locator("#email").fill(actor + "@example.test")
                    view.locator("#pw").fill(password)
                    view.locator("button[type=submit]").click()
                    view.wait_for_function("() => document.getElementById('nav').hidden === false")
                    view.goto(base + "#/exercise/EX-HOME-001")
                    view.get_by_role("heading", name="EX-HOME-001: Intake", exact=True).wait_for()
                    return session, view

                def supplied_event(view, action, fields):
                    if not view.locator("#exercise-record-action").is_visible():
                        view.locator("summary").filter(has_text="Record one explicitly supplied exercise event").click()
                    view.locator("#exercise-record-action").select_option(action)
                    for key, value in fields.items():
                        control = view.locator(f"#exercise-event-{action}-{key}")
                        if control.evaluate("e=>e.tagName") == "SELECT":
                            control.select_option(value)
                        else:
                            control.fill(value)
                    view.get_by_role("button", name="Record one supplied event", exact=True).click()

                session, page = home_session("ex-rlo-01")
                supplied_event(page, "resident-update", dict(step="create", channel="Phone",
                    purpose="Fictional independent scope question", due="Unknown", due_basis="Unknown",
                    adjustment_reference="Unknown", evidence="Supplied fictional safe contact route",
                    next_update="Named liaison explains scope"))
                page.get_by_role("cell", name="UPDATE-001", exact=True).wait_for()
                record("browser-resident-commitment-owned-independently",
                       page.get_by_role("cell", name="ex-rlo-01@example.test", exact=True).count() == 1)
                session.close()
                session, page = home_session("ex-pm-01")
                supplied_event(page, "handoff", dict(step="sent", receiver="ex-pso-01@example.test",
                    reason="Fictional scope review", evidence="Explicit sent reference",
                    due="Unknown", urgency="Routine", next_action="Receiver reviews scope"))
                page.get_by_text("State Sent;", exact=False).wait_for()
                session.close()
                session, page = home_session("ex-pso-01")
                supplied_event(page, "handoff", dict(step="accepted", reason="Premature acceptance",
                    evidence="No separate receipt yet"))
                page.locator("#app [role=alert][aria-live=polite]").wait_for()
                record("browser-handoff-receipt-not-inferred",
                       "receipt never implies acceptance" in page.locator("#app [role=alert][aria-live=polite]").inner_text())
                supplied_event(page, "handoff", dict(step="received", reason="Supplied receipt",
                    evidence="Separately supplied receiver receipt"))
                page.get_by_text("State Received;", exact=False).wait_for()
                supplied_event(page, "handoff", dict(step="accepted", reason="Supplied acceptance",
                    evidence="Separate acceptance reference"))
                page.get_by_text("State Accepted;", exact=False).wait_for()
                supplied_event(page, "handoff", dict(step="completed", reason="Scope review complete",
                    evidence="Separately supplied completion reference"))
                page.get_by_text("State Completed;", exact=False).wait_for()
                record("browser-handoff-preserves-resident-commitment",
                       page.get_by_role("cell", name="ex-rlo-01@example.test", exact=True).count() == 1
                       and page.get_by_role("cell", name="Outstanding", exact=True).count() == 1,
                       {"task": "Sent/received/accepted/completed operational handoff never clears or reassigns resident update"})
                session.close()

                def resident_form(view, title, fields, button):
                    panel = view.locator("details").filter(has=view.get_by_text(title, exact=True))
                    if not panel.get_attribute("open"):
                        panel.locator("summary").click()
                    for key, value in fields.items():
                        control = panel.locator(f'[id="f-{title}-{key}"]')
                        if control.count() != 1:
                            raise AssertionError({"title": title, "field": key, "panel_html": panel.inner_html()})
                        if control.evaluate("e=>e.tagName") == "SELECT":
                            control.select_option(value)
                        else:
                            control.fill(value)
                    panel.get_by_role("button", name=button, exact=True).click()

                session, page = home_session("ex-rlo-01")
                page.goto(base + "#/case/EX-HOME-001")
                page.get_by_role("heading", name="Decision for each measure", exact=True).wait_for()
                resident_form(page, "Open a request or complaint", dict(route="Complaint",
                    summary="Fictional accessible scope explanation",
                    desired_outcome="Fictional officer-assisted explanation before deciding",
                    service_owner="ex-rlo-01@example.test", redress_owner="ex-pm-01@example.test",
                    accessibility="Safe route needed", representative_ref="BROWSER-CONTACT-REFERENCE",
                    next_update="2026-10-12"), "Open")
                page.get_by_text("SR-1: Complaint. Open.", exact=True).wait_for()
                record("browser-accessible-service-is-not-consent",
                       "Safe route needed" in page.locator("#app").inner_text()
                       and "BROWSER-CONTACT-REFERENCE" in page.locator("#app").inner_text()
                       and page.get_by_role("cell", name="Withdrawn", exact=True).count() == 1,
                       {"task": "Open supplied accessible complaint, retaining previously withdrawn works choice"})
                resident_form(page, "Update a request", dict(id="SR-1", status="Resolved",
                    next_update="2026-10-13", note="Supplied explanation, await redress review"), "Save update")
                page.get_by_text("SR-1: Complaint. Resolved.", exact=True).wait_for()
                resident_form(page, "Close a request", dict(id="SR-1",
                    note="Cannot self-close complaint"), "Close")
                page.get_by_text("Only the redress owner can close a complaint.", exact=True).wait_for()
                record("browser-complaint-independent-close-refusal",
                       page.get_by_text("SR-1: Complaint. Resolved.", exact=True).count() == 1)
                session.close()
                session, page = home_session("ex-pm-01")
                page.goto(base + "#/case/EX-HOME-001")
                page.get_by_text("SR-1: Complaint. Resolved.", exact=True).wait_for()
                resident_form(page, "Close a request", dict(id="SR-1",
                    note="Supplied independent redress outcome"), "Close")
                page.get_by_text("SR-1: Complaint. Closed.", exact=True).wait_for()
                record("browser-complaint-independent-redress-close",
                       page.get_by_role("cell", name="Withdrawn", exact=True).count() == 1)
                session.close()
                if args.native_zoom:
                    context = browser.new_context(no_viewport=True)
                    context.route("**/*", lambda route: route.continue_()
                                  if route.request.url.startswith(base) else route.abort())
                    page = context.new_page()
                    page.goto(base)
                    page.locator("#email").fill("ex-geo-01@example.test")
                    page.locator("#pw").fill(password)
                    page.locator("button[type=submit]").click()
                    page.wait_for_function("() => document.getElementById('nav').hidden === false")
                    page.goto(base + "#/exercise/EX-HOME-001")
                    page.get_by_role("heading", name="EX-HOME-001: Intake", exact=True).wait_for()
                    page.bring_to_front()
                    page.get_by_role("heading", name="EX-HOME-001: Intake", exact=True).click()
                    native_zoom_keys(1, reset=True)
                    native_zoom_keys(8)
                    page.wait_for_function("() => devicePixelRatio >= 3.99")
                    metrics = page.evaluate("""() => ({css_width:innerWidth,window_width:outerWidth,
                        device_pixel_ratio:devicePixelRatio,css_zoom:getComputedStyle(document.body).zoom,
                        overflow:document.documentElement.scrollWidth>innerWidth+1})""")
                    record("native-browser-400-percent-home-reflow",
                           abs(metrics["device_pixel_ratio"] - 4) < .01 and metrics["css_zoom"] == "1"
                           and not metrics["overflow"], metrics)
                    page.get_by_role("link", name="Open building EX-BUILDING-001 (home gates stay independent)", exact=True).click()
                    page.get_by_role("heading", name="Building EX-BUILDING-001", exact=True).wait_for()
                    record("native-browser-400-percent-building-reflow",
                           not page.evaluate("document.documentElement.scrollWidth>innerWidth+1"))
                    native_zoom_keys(1, reset=True)
                    context.close()
                record("browser-runtime-errors", not errors and not bad_responses,
                       {"page_errors": errors, "server_errors": bad_responses})
                browser.close()
        finally:
            server.terminate()
            server.wait(timeout=10)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "kind": "local-browser-engineering", "browser": version,
        "human_ux": "Not run", "screen_reader": "Not run", "wcag_conformance": "Not assessed",
        "checks": results,
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(results), "failed": sum(r["result"] == "Fail" for r in results)}))
    return int(any(row["result"] == "Fail" for row in results))


if __name__ == "__main__":
    raise SystemExit(main())
