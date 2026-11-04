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

import test_mvp
from playwright.sync_api import sync_playwright
from test_auth import ENV, OID_NEW, OID_SAM, TENANT, principal
from zava_forward.api import auth
from zava_forward.api.server import App, make_handler
from zava_forward.core import identity
from zava_forward.core.store import Store

DENIED_PATHS = ("/api/account/photo", "/api/law/alerts", "/api/chat/regulatory/status")
ASSISTANTS_PATH = "/api/assistants"
OID_ADMIN = OID_NEW
ADMIN_ONLY = ("ZavaForward.ApplicationAdmin",)


def check(label: str, ok: bool) -> None:
    print(("PASS " if ok else "FAIL ") + label)
    assert ok, label


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="zf-920-") as scratch:
        data = json.loads(json.dumps(test_mvp.DATA))
        data["staff"][0]["oid"] = OID_SAM
        data[identity.LEGACY_TENANT_KEY] = TENANT
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
                        "response", lambda r: admin_denied.append(r.url) if r.status >= 400 else None
                    )
                    admin.goto(base + "/app")
                    admin.locator("#workspace-status").wait_for()
                    for route in ("#/assistants",):
                        admin.evaluate(f"location.hash = '{route}'")
                        admin.wait_for_timeout(1500)
                    check(
                        "assistants denial is worded plainly",
                        "not available for your role" in (admin.locator("body").text_content() or ""),
                    )
                    check(
                        "no assistants request was sent for an admin-only account",
                        not [u for u in admin_requested if ASSISTANTS_PATH in u],
                    )
                    # The admin-only landing list still gets 403 on /api/facets (follow-up of #920).
                    check(
                        f"no assistants 403 reached the console for admin-only ({admin_denied})",
                        not [u for u in admin_denied if ASSISTANTS_PATH in u],
                    )
                finally:
                    browser.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    main()
