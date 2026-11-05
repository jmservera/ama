"""Issue 920: expected 503/403 denials show plain words and leave the browser console quiet.

Owned synthetic loopback server behind the trusted-proxy provider with the law store off, no
profile-photo token and no RegulatoryChat capability. No live model, SQL or Azure calls.
"""

from __future__ import annotations

import json
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

import test_mvp
from playwright.sync_api import sync_playwright
from test_auth import ENV, OID_NEW, OID_SAM, TENANT, principal
from zava_forward.api import auth
from zava_forward.api.server import App, make_handler
from zava_forward.core import identity
from zava_forward.core.store import Store

DENIED_PATHS = ("/api/account/photo", "/api/law/alerts", "/api/chat/regulatory/status")
ASSISTANTS_PATH = "/api/assistants"
CASE_ROUTES = (
    "#/overview",
    "#/visits",
    "#/funding",
    "#/coordinator",
    "#/finance",
    "#/capacity",
    "#/progress",
    "#/closed",
    "#/time",
    "#/all",
    "#/case/ZF-1",
)
CASE_API = (
    "/api/stats",
    "/api/visits",
    "/api/funding",
    "/api/coordinator",
    "/api/finance",
    "/api/facets",
)
OID_ADMIN = OID_NEW
OID_CONTRACTOR = "aaaaaaaa-0000-0000-0000-000000000009"
STAFF_ROLES = (
    "Coordinator",
    "LiaisonOfficer",
    "SafetyLiaison",
    "GrantsOfficer",
    "QualityInspector",
    "ProgrammeManager",
    "SupportOfficer",
)
ADMIN_ONLY = ("ZavaForward.ApplicationAdmin",)


def check(label: str, ok: bool) -> None:
    print(("PASS " if ok else "FAIL ") + label)
    assert ok, label


def survey_role(browser: Any, base: str, role: str, oid: str, extra: tuple[str, ...]) -> None:
    """Open every navigation route plus the extra routes; expect no 4xx and no console error."""
    page = browser.new_context(
        extra_http_headers={
            "X-MS-CLIENT-PRINCIPAL": principal(roles=(f"ZavaForward.{role}",), oid=oid)
        }
    ).new_page()
    denied: list[str] = []
    errors: list[str] = []
    page.on("response", lambda r: denied.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base + "/app")
    page.wait_for_function("() => typeof me !== 'undefined' && me && me.navigation")
    expected = auth.DEFAULT_ROLE_MAP[f"ZavaForward.{role}"]
    check(f"{role}: session role is {expected}", page.evaluate("me.user.role") == expected)
    navigation = page.evaluate("me.navigation.map((n) => n.href)")
    check(f"{role}: navigation is not empty", bool(navigation))
    routes = [*navigation, *extra]
    for route in routes:
        page.evaluate(f"location.hash = '{route}'")
        page.wait_for_timeout(1500)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    check(f"{role}: {len(routes)} routes without 4xx ({denied})", not denied)
    check(f"{role}: no console errors ({errors})", not errors)
    page.context.close()


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="zf-920-") as scratch:
        data = json.loads(json.dumps(test_mvp.DATA))
        data["staff"][0]["oid"] = OID_SAM
        data[identity.LEGACY_TENANT_KEY] = TENANT
        data["staff"].append(
            dict(
                code="CON-1",
                name="Kim Builder",
                email="kim@example.test",
                role="Contractor",
                contractor="Test Ltd",
                oid=OID_CONTRACTOR,
            )
        )
        path = Path(scratch) / "zavaforward.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        store = Store(str(path))
        app = App(store, provider=auth.TrustedProxyProvider(store, ENV))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{httpd.server_port}"
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                try:
                    context = browser.new_context(
                        extra_http_headers={"X-MS-CLIENT-PRINCIPAL": principal(oid=OID_SAM)}
                    )
                    page = context.new_page()
                    errors: list[str] = []
                    requested: list[str] = []
                    page.on(
                        "console", lambda m: errors.append(m.text) if m.type == "error" else None
                    )
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    page.on("request", lambda r: requested.append(r.url))
                    page.goto(base + "/app")
                    page.get_by_role("heading", name="My cases today").wait_for()
                    page.wait_for_function(
                        "() => document.getElementById('photo-status').textContent.includes('token-store')"
                    )
                    check(
                        "photo denial is worded plainly",
                        "token-store setup" in (page.locator("#photo-status").text_content() or ""),
                    )
                    page.evaluate("location.hash = '#/case/ZF-1'")
                    page.locator("#regulatory-alerts-title").wait_for(state="attached")
                    page.wait_for_function(
                        "() => document.body.textContent.includes('Alert coverage unknown')"
                    )
                    body = page.locator("body").text_content() or ""
                    check(
                        "alerts 503 is worded plainly with the human route",
                        "law store is not loaded" in body
                        and "human emergency or hazard service" in body,
                    )
                    page.wait_for_function(
                        "() => document.getElementById('chat-panel').textContent"
                        ".includes('is not available for your role')"
                    )
                    chat = page.locator("#chat-panel").text_content() or ""
                    check(
                        "regulatory chat 403 is worded plainly with the manual route",
                        "human owner route" in chat,
                    )
                    check(
                        "no request was sent to the predictably denied endpoints",
                        not [u for u in requested if any(p in u for p in DENIED_PATHS)],
                    )
                    check(f"no console errors ({errors})", not errors)
                    admin = browser.new_context(
                        extra_http_headers={
                            "X-MS-CLIENT-PRINCIPAL": principal(roles=ADMIN_ONLY, oid=OID_ADMIN)
                        }
                    ).new_page()
                    admin_requested: list[str] = []
                    admin.on("request", lambda r: admin_requested.append(r.url))
                    admin_denied: list[str] = []
                    admin.on(
                        "response",
                        lambda r: admin_denied.append(r.url) if r.status >= 400 else None,
                    )
                    admin_errors: list[str] = []
                    admin.on(
                        "console",
                        lambda m: admin_errors.append(m.text) if m.type == "error" else None,
                    )
                    admin.goto(base + "/app")
                    admin.get_by_role("heading", name="No case work for this account").wait_for()
                    check(
                        "admin-only landing is worded plainly",
                        "no case access" in (admin.locator("body").text_content() or ""),
                    )
                    admin.evaluate("location.hash = '#/assistants'")
                    admin.wait_for_timeout(1500)
                    check(
                        "assistants denial is worded plainly",
                        "not available for your role"
                        in (admin.locator("body").text_content() or ""),
                    )
                    for route in CASE_ROUTES:
                        admin.evaluate(f"location.hash = '{route}'")
                        admin.get_by_role(
                            "heading", name="No case work for this account"
                        ).wait_for()
                        admin.wait_for_timeout(300)
                    check(
                        f"{len(CASE_ROUTES)} case-data routes show plain words for an admin-only account",
                        "no case access" in (admin.locator("body").text_content() or ""),
                    )
                    check(
                        "no case-data request was sent for an admin-only account",
                        not [u for u in admin_requested if any(p in u for p in CASE_API)],
                    )
                    check(
                        "no assistants request was sent for an admin-only account",
                        not [u for u in admin_requested if ASSISTANTS_PATH in u],
                    )
                    check(f"no admin-only 4xx response ({admin_denied})", not admin_denied)
                    check(f"no admin-only console errors ({admin_errors})", not admin_errors)
                    for role in STAFF_ROLES:
                        survey_role(browser, base, role, OID_SAM, ("#/case/ZF-1", "#/assistants"))
                    survey_role(browser, base, "Contractor", OID_CONTRACTOR, ("#/case/ZF-1",))
                finally:
                    browser.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    main()
