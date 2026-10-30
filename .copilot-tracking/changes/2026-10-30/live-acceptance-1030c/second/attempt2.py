"""Second and final employee launch, bound to immutable first-run evidence."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import resource
import time
from pathlib import Path

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
FIRST = OUT.parent
SPEC = importlib.util.spec_from_file_location(
    "first_acceptance", FIRST / "acceptance.py"
)
assert SPEC and SPEC.loader
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

EXPECTED = {
    "acceptance.py": "bfca66bdc4623e35c33f056497613592d417a3db3e98d61363b64bd2fe8e10ee",
    "evidence.json": "fe5f0dcb185774c2c62a5e036386ebf80b7cc936acd7c2bc737a9c57d0bafa4c",
    "manifest.json": "099da77011f5b443f54435b563980187c81dbecc03441cb463ce3cc4ba460c19",
}


def verify_first():
    for name, digest in EXPECTED.items():
        if hashlib.sha256((FIRST / name).read_bytes()).hexdigest() != digest:
            raise ValueError("first_provenance_refused")
    manifest = json.loads((FIRST / "manifest.json").read_text())
    evidence = json.loads((FIRST / "evidence.json").read_text())
    attempts = manifest["attempts"]["employee"]
    if not (
        manifest["completed"]
        and len(attempts) == 1
        and attempts[0]["number"] == 1
        and attempts[0]["submission_intent"]
        and evidence["browserClosed"]
        and evidence["employeeContextClosed"]
        and evidence["script_sha256"] == evidence["script_sha256_after"]
    ):
        raise ValueError("first_completion_refused")
    auth = next(
        row
        for row in evidence["steps"]
        if row["command"].startswith("employee: bounded actual")
    )
    if not (
        auth["status"] == "observed"
        and auth["result"]["kmsiHandled"]
        and auth["result"]["passwordSubmissionIntent"]
        and auth["result"]["callbackWaitExhausted"]
    ):
        raise ValueError("second_slot_not_authorized")
    return EXPECTED


def authenticate(page, guard):
    entry = guard.admit("employee")
    entry["task_attempt_number"] = 2
    guard.save()
    base.navigate(
        page, base.EMPLOYEE + "/.auth/login/aad?post_login_redirect_uri=%2Fapp"
    )
    username_sent = False
    submitted = False
    kmsi = False
    deadline = time.monotonic() + 300
    last_binding = None
    binding_failures = 0
    last_http = None
    app_seen = False
    while time.monotonic() < deadline:
        if base.allowed(page.url, {base.EMPLOYEE}) and submitted:
            app_seen = True
            try:
                # Status only; no payload or headers cross the browser boundary.
                last_http = page.evaluate("""async()=>{
                  const r=await fetch('/api/me',{redirect:'error',
                    signal:AbortSignal.timeout(120000)});
                  return r.status;
                }""")
                if last_http == 200:
                    last_binding = page.evaluate(base.BINDING, base.USERNAME)
                    if last_binding.get("authenticated"):
                        return {
                            "authenticated": True,
                            "binding": last_binding,
                            "http": last_http,
                            "kmsiHandled": kmsi,
                            "appOriginSeen": app_seen,
                            "bindingFailures": binding_failures,
                        }
            except BrowserError:
                binding_failures += 1
        elif base.allowed(page.url, base.PROVIDERS):
            email = page.locator("input[type=email]:visible")
            password = page.locator("input[name=passwd][type=password]:visible")
            if email.count() and not username_sent:
                base.origin_guard(page, base.PROVIDERS)
                email.fill(base.USERNAME)
                base.origin_guard(page, base.PROVIDERS)
                page.locator("input[type=submit]:visible").press(
                    "Enter", no_wait_after=True
                )
                username_sent = True
            elif password.count() and not submitted and username_sent:
                value = base.credentials((Path.home() / ".ama-test-user").read_text())[
                    0
                ]
                base.SECRETS.append(value)
                base.origin_guard(page, base.PROVIDERS)
                password.fill(value)
                base.origin_guard(page, base.PROVIDERS)
                guard.submit(entry)
                submitted = True
                deadline = time.monotonic() + 180
                page.locator("input[type=submit]:visible").press(
                    "Enter", no_wait_after=True
                )
            elif submitted and not kmsi:
                no = page.get_by_role("button", name="No", exact=True)
                if no.count() and no.is_visible():
                    base.origin_guard(page, base.PROVIDERS)
                    kmsi = True
                    no.press("Enter", no_wait_after=True)
        else:
            return {"authenticated": False, "unexpectedOrigin": True}
        page.wait_for_timeout(1000)
    return {
        "authenticated": False,
        "lastBinding": last_binding,
        "lastHttp": last_http,
        "usernameSubmitted": username_sent,
        "passwordSubmissionIntent": submitted,
        "kmsiHandled": kmsi,
        "appOriginSeen": app_seen,
        "finalAppOrigin": base.allowed(page.url, {base.EMPLOYEE}),
        "finalProviderOrigin": base.allowed(page.url, base.PROVIDERS),
        "bindingFailures": binding_failures,
        "callbackWaitExhausted": True,
    }


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    base.diagnostics_guard(os.environ)
    provenance = verify_first()
    base.OUT = OUT
    guard = base.Guard(OUT / "manifest.json")
    evidence = base.Evidence()
    evidence.data["firstProvenance"] = provenance
    evidence.data["second_runner_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    evidence.data["taskEmployeeLaunchCeiling"] = 2
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        evidence.data["browser"] = browser.version
        context = browser.new_context(
            viewport={"width": 1280, "height": 900}, has_touch=True
        )
        try:
            warmed = evidence.step(
                "employee attempt 2: GET /healthz timeout=120000 retries=3",
                lambda: base.warm(context.request, base.EMPLOYEE),
            )
            if not warmed or not warmed["warm"]:
                evidence.data["employeeFeatures"] = "blocked_cold_start_unresolved"
                return
            page = context.new_page()
            page.set_default_timeout(120000)
            page.set_default_navigation_timeout(120000)
            admitted = evidence.step(
                "employee attempt 2 FINAL: actual login, KMSI, 180s callback, /api/me",
                lambda: authenticate(page, guard),
            )
            if not admitted or not admitted.get("authenticated"):
                evidence.data["employeeFeatures"] = "blocked_no_verified_session"
                return
            evidence.step(
                "employee authenticated: GET /chat-widget.js hash",
                lambda: {
                    "http": (
                        response := context.request.get(
                            base.EMPLOYEE + "/chat-widget.js", timeout=120000
                        )
                    ).status,
                    "sha256": hashlib.sha256(response.body()).hexdigest(),
                },
            )
            opened = evidence.step(
                "employee: Chat Enter opens native shared dialog",
                lambda: base.chat_open(page, False),
            )
            if opened:
                evidence.step(
                    "employee: select next skill, actual Enter reply",
                    lambda: base.skill_check(page),
                )
                evidence.step(
                    "employee: Shift+Enter, Send, Escape/reopen, scroll, widths, motion",
                    lambda: base.chat_interactions(page, "#employee-chat"),
                )
            evidence.step(
                "employee: expanded map keyboard filters/API totals/narrow/restore",
                lambda: base.map_check(page),
            )
            evidence.step(
                "employee: actual case icons/blocker keyboard+touch/tabs/widths",
                lambda: base.case_check(page),
            )
        finally:
            context.close()
            browser.close()
            evidence.data.update(
                contextClosed=True, browserClosed=True, finished=base.now()
            )
            evidence.data["second_runner_sha256_after"] = hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest()
            base.write(OUT / "evidence.json", evidence.data)
            guard.data["completed"] = True
            guard.save()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # noqa: BLE001 - never emit browser/credential diagnostics
        print("Second attempt stopped safely: " + base.failure_code(error))
        raise SystemExit(1) from None
    print("Final employee attempt finished; inspect aggregate evidence.")
