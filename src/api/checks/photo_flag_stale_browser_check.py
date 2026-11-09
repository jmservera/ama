"""Issue 954: a stale-true photo flag followed by a predictable 503/403 in a real Chromium page.

Owned synthetic loopback server behind the trusted-proxy provider. Only `/api/me` services.photo
and `/api/account/photo` are intercepted; the denials stay real 503/403 responses and every other
response is the real app, `app.js` and DOM. No Entra identity, Azure call, credential, model or
private data.

Owner definition of quiet (2026-11-09): no disruptive employee-facing toast and no unhandled
application error after an expected 503/403. An inline unavailable status, the initials fallback
and browser-native failed-resource diagnostics are acceptable. Every console event is recorded
unfiltered; native diagnostics are classified separately and never suppressed.
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

import test_auth
import test_mvp
from playwright.sync_api import Page, sync_playwright
from test_auth import ENV, OID_SAM, TENANT, principal
from zava_forward.api import auth
from zava_forward.api import server as api_server
from zava_forward.api.server import App, make_handler
from zava_forward.core import identity
from zava_forward.core import store as core_store
from zava_forward.core.store import Store

STATUSES = (503, 403)
PHOTO = "/api/account/photo"
NATIVE_PREFIX = "Failed to load resource"
WORKTREE = Path(__file__).resolve().parents[3]
DISRUPTIVE = (
    "[role=alert],[role=alertdialog],dialog,[aria-modal=true],"
    "[class*=toast],[class*=snackbar],[id*=toast]"
)
WATCH = (
    "window.__zfDisruptive = [];"
    "new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) {"
    "if (n.nodeType !== 1) continue;"
    f"const hit = n.matches('{DISRUPTIVE}') ? n : n.querySelector('{DISRUPTIVE}');"
    "if (hit) window.__zfDisruptive.push(hit.outerHTML.slice(0, 200)); } })"
    ".observe(document, {childList: true, subtree: true});"
)


def check(label: str, ok: bool) -> None:
    print(("PASS " if ok else "FAIL ") + label)
    assert ok, label


def assert_worktree_imports() -> None:
    modules = (api_server, core_store, test_mvp, test_auth)
    for module in modules:
        path = Path(module.__file__ or "").resolve()
        check(f"{module.__name__} resolves inside this worktree", WORKTREE in path.parents)


def refresh(page: Page, state: dict[str, Any], photo: bool, label: str) -> None:
    """Make a real tab-return re-check: lift the one-minute bound and fire visibilitychange."""
    state["photo"] = photo
    page.evaluate("photoServiceCheckedAt = 0")
    page.locator("#photo-status").evaluate("el => { el.textContent = 'refresh pending'; }")
    check(
        f"{label}: page is visible for the re-check",
        page.evaluate("document.visibilityState") == "visible",
    )
    with page.expect_response("**/api/me") as pending:
        page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
    check(f"{label}: re-check /api/me answered", pending.value.status == 200)
    # The handler runs after the response: the sentinel text changing proves it was processed.
    page.wait_for_function(
        "() => document.getElementById('photo-status').textContent !== 'refresh pending'"
    )


def observe(browser: Any, base: str, status: int, result: dict[str, Any]) -> None:
    page = browser.new_context(
        extra_http_headers={"X-MS-CLIENT-PRINCIPAL": principal(oid=OID_SAM)}
    ).new_page()
    page.add_init_script(WATCH)
    state: dict[str, Any] = {"photo": True}
    console: list[dict[str, Any]] = []
    page_errors: list[str] = []
    dialogs: list[str] = []
    loads: list[str] = []
    photo_requests: list[int] = []
    photo_responses: list[int] = []
    me_flags: list[bool | None] = []
    page.on(
        "console",
        lambda m: console.append(
            {"type": m.type, "text": m.text, "url": (m.location or {}).get("url", "")}
        ),
    )
    page.on("pageerror", lambda e: page_errors.append(str(e)))
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    page.on("load", lambda: loads.append(page.url))
    page.on(
        "response",
        lambda r: photo_responses.append(r.status) if r.url.endswith(PHOTO) else None,
    )

    def me_route(route: Any) -> None:
        real = route.fetch()
        body = real.json()
        body["services"] = {**(body.get("services") or {}), "photo": state["photo"]}
        me_flags.append(body["services"]["photo"])
        route.fulfill(status=200, content_type="application/json", body=json.dumps(body))

    def photo_route(route: Any) -> None:
        photo_requests.append(status)
        route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps({"error": f"synthetic predictable {status}"}),
        )

    page.route("**/api/me", me_route)
    page.route(f"**{PHOTO}", photo_route)
    result.update(status=status, console_events=console, page_errors=page_errors)
    try:
        page.goto(base + "/app")
        page.get_by_role("heading", name="My cases today").wait_for()
        page.wait_for_function(
            "() => document.getElementById('photo-status').textContent.includes('token-store')"
        )
        page.evaluate("window.__zfMarker = 'no-reload'")
        origin = page.evaluate("performance.timeOrigin")
        check(f"{status}: startup /api/me said photo=true (stale)", me_flags == [True])
        check(f"{status}: one photo request, answered {status}", photo_requests == [status])
        check(
            f"{status}: flag is off after the denial", page.evaluate("me.services.photo") is False
        )
        check(
            f"{status}: initials fallback is visible, photo hidden",
            page.locator("#account-initials").is_visible()
            and page.locator("#account-photo").is_hidden(),
        )
        fallback = page.locator("#photo-status").text_content() or ""
        check(f"{status}: inline unavailable status is shown", "token-store" in fallback)
        check(
            f"{status}: status is a native role=status element",
            page.locator("p#photo-status[role=status]").count() == 1,
        )
        check(
            f"{status}: no account error text",
            not (page.locator("#account-error").text_content() or ""),
        )
        result["fallback_text"] = fallback

        refresh(page, state, photo=False, label=f"{status} false refresh")
        check(f"{status}: false refresh was served, flag false", me_flags == [True, False])
        page.wait_for_timeout(500)
        check(f"{status}: no photo request after a false refresh", len(photo_requests) == 1)

        refresh(page, state, photo=True, label=f"{status} true refresh")
        for _ in range(50):
            if len(photo_requests) >= 2:
                break
            page.wait_for_timeout(100)
        page.wait_for_function("() => me.services.photo === false")
        check(f"{status}: flags served were true, false, true", me_flags == [True, False, True])
        check(
            f"{status}: a true refresh after a failed load retries once ({len(photo_requests)})",
            len(photo_requests) == 2,
        )
        page.wait_for_timeout(500)
        check(f"{status}: no further photo request", len(photo_requests) == 2)
        check(
            f"{status}: denials stayed {status} responses, never converted to success",
            photo_responses == [status, status],
        )
        check(
            f"{status}: no full reload (marker kept, one load event, same time origin)",
            page.evaluate("window.__zfMarker") == "no-reload"
            and len(loads) == 1
            and page.evaluate("performance.timeOrigin") == origin,
        )
        result["fallback_after_retry"] = page.locator("#photo-status").text_content()
        result["disruptive_nodes"] = page.evaluate("window.__zfDisruptive")
    except BaseException as error:
        result["failure"] = repr(error)
        raise
    finally:
        result.update(
            photo_requests=len(photo_requests),
            photo_response_statuses=photo_responses,
            me_flags=me_flags,
            dialogs=dialogs,
            load_events=len(loads),
        )
        page.context.close()


def classify(item: dict[str, Any]) -> None:
    status = item["status"]
    console = item["console_events"]
    native = [
        c
        for c in console
        if c["type"] == "error"
        and c["text"].startswith(NATIVE_PREFIX)
        and c["url"].endswith(PHOTO)
        and str(status) in c["text"]
    ]
    other = [c for c in console if c not in native]
    unexpected = [c for c in other if c["type"] in ("error", "warning")]
    item.update(
        native_failed_resource=len(native),
        other_console_events=other,
        unexpected_console_events=unexpected,
        literal_no_console_event=not console and not item["page_errors"],
        quiet_per_owner_definition=not (
            item["page_errors"]
            or unexpected
            or item.get("disruptive_nodes")
            or item["dialogs"]
            or "failure" in item
        ),
    )


def main() -> None:
    assert_worktree_imports()
    results: list[dict[str, Any]] = []
    out = os.environ.get("ZF_OBSERVATION_DIR")
    try:
        with tempfile.TemporaryDirectory(prefix="zf-954-") as scratch:
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
                        for status in STATUSES:
                            item: dict[str, Any] = {}
                            results.append(item)
                            observe(browser, base, status, item)
                    finally:
                        browser.close()
            finally:
                httpd.shutdown()
                httpd.server_close()
        for item in results:
            classify(item)
            status = item["status"]
            check(f"{status}: no unhandled application page error", not item["page_errors"])
            check(
                f"{status}: no unexpected console error or warning",
                not item["unexpected_console_events"],
            )
            check(
                f"{status}: no disruptive toast, alert, dialog or modal",
                not (item["disruptive_nodes"] or item["dialogs"]),
            )
            check(f"{status}: quiet per the owner definition", item["quiet_per_owner_definition"])
            print(
                f"OBSERVED {status}: native failed-resource diagnostics="
                f"{item['native_failed_resource']} literal_no_console_event="
                f"{item['literal_no_console_event']} quiet_per_owner_definition="
                f"{item['quiet_per_owner_definition']}"
            )
    finally:
        if out:
            for item in results:
                if "native_failed_resource" not in item:
                    classify(item)
            (Path(out) / "photo-flag-stale-console.json").write_text(
                json.dumps(results, indent=2), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
