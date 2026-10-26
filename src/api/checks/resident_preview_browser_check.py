"""Run the real resident preview server and check keyboard, focus, error and mobile behaviour.

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.resident_preview_browser_check
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright


def check(name: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(name)
    print(f"PASS {name}", flush=True)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def clean_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if k in ("PATH", "HOME", "LANG")}


@contextmanager
def preview(root: Path, subject: str) -> Iterator[str]:
    port = free_port()
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "zava_forward.api.resident_preview",
            "--data-dir", str(root), "--subject", subject, "--port", str(port),
        ],
        env=clean_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            try:
                urllib.request.urlopen(base + "/healthz", timeout=1).read()
                break
            except OSError:
                time.sleep(0.1)
        else:
            raise AssertionError("preview did not become ready")
        yield base
    finally:
        proc.terminate()
        proc.wait(10)


def new_page(browser: Any, width: int = 1024, height: int = 800) -> tuple[Page, list[str], list[str]]:
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    errors: list[str] = []
    requests: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: requests.append(f"{r.method} {r.url}"))
    return page, errors, requests


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ama444-browser-") as tmp:
        root = Path(tmp) / "fixture"
        build = subprocess.run(
            [sys.executable, "-m", "zava_forward.api.resident_preview", "--build-fixture", str(root)],
            env=clean_env(), capture_output=True, text=True,
        )
        check("fixture builds in a clean environment", build.returncode == 0)
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            check_resident_a(browser, root)
            check_offer_only(browser, root)
            check_mobile(browser, root)
            check_error_and_recovery(browser, root)
            check_retry_focus_and_announcements(browser, root)
            check_skip_target_and_no_script(browser, root)
            check_representative(browser, root)
            browser.close()
    print("resident preview browser check complete", flush=True)


def check_resident_a(browser: Any, root: Path) -> None:
    with preview(root, "SYN-RES-A") as base:
        page, errors, requests = new_page(browser)
        page.goto(base + "/")
        page.wait_for_selector("#content:not([hidden])")
        text = page.inner_text("body")
        check("banner says synthetic preview and not live", "Synthetic preview - not a live resident service" in text)
        check("confirmed arrangements shown", "Confirmed arrangements" in text and "1 January 2098" in text)
        check("offered section states not confirmed", "Offered times (not confirmed)" in text)
        check("help and non-digital route visible", "Speak to your housing officer" in text)
        check("no staff canary text", "SYN-CANARY" not in text and "Blake" not in text)
        check("page title says synthetic", "synthetic preview" in page.title().lower())
        check("one h1", page.locator("h1").count() == 1)

        page.keyboard.press("Tab")
        check("skip link is first focus stop", page.evaluate("document.activeElement.className") == "skip")
        outline = page.evaluate("getComputedStyle(document.activeElement).outlineWidth")
        check("focus ring is at least 3px", float(outline.replace("px", "")) >= 3)
        page.keyboard.press("Enter")
        check("skip link moves focus to main", page.evaluate("document.activeElement.id") == "main")

        disabled = page.locator("button[disabled]")
        check("unavailable features are disabled buttons", disabled.count() >= 6)
        page.keyboard.press("Tab")
        for _ in range(12):
            page.keyboard.press("Tab")
        check("disabled buttons are never keyboard focus stops", page.evaluate("document.activeElement.disabled") is not True)
        before = len(requests)
        disabled.first.click(force=True)
        check("disabled feature sends no request", len(requests) == before)

        check("only same-origin GETs", all(r.startswith("GET " + base) for r in requests))
        check("no console errors", errors == [])
        page.context.close()


def check_offer_only(browser: Any, root: Path) -> None:
    with preview(root, "SYN-RES-B") as base:
        page, _, _ = new_page(browser)
        page.goto(base + "/")
        page.wait_for_selector("#content:not([hidden])")
        offered = page.locator("section", has=page.get_by_role("heading", name="Offered times (not confirmed)"))
        confirmed = page.locator("section", has=page.get_by_role("heading", name="Confirmed arrangements"))
        check("offer is listed as an offer", "1 February 2098" in offered.inner_text())
        check("offer is not listed as confirmed", "1 February 2098" not in confirmed.inner_text())
        check("no confirmed arrangement is honest", "No confirmed arrangement is recorded" in confirmed.inner_text())
        check("resident B sees own home only", "2 Synthetic Row" in page.inner_text("body") and "1 Synthetic Row" not in page.inner_text("body"))
        page.context.close()


def check_mobile(browser: Any, root: Path) -> None:
    with preview(root, "SYN-RES-A") as base:
        page, _, _ = new_page(browser, 320, 640)
        page.goto(base + "/")
        page.wait_for_selector("#content:not([hidden])")
        check("320px has no horizontal scroll", page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"))
        check("banner visible at 320px", page.locator(".synthetic").is_visible())
        zoom = page.evaluate("getComputedStyle(document.body).fontSize")
        check("body text is at least 16px", float(zoom.replace("px", "")) >= 16)
        page.emulate_media(reduced_motion="reduce")
        check("reduced motion removes transitions", page.evaluate("getComputedStyle(document.querySelector('button')).transitionDuration") in ("0s", "0s, 0s"))
        page.context.close()


def check_error_and_recovery(browser: Any, root: Path) -> None:
    grants = root / "grants.json"
    original = grants.read_text()
    with preview(root, "SYN-RES-A") as base:
        page, errors, _ = new_page(browser)
        page.goto(base + "/")
        page.wait_for_selector("#content:not([hidden])")
        data = json.loads(original)
        data["grants"][0]["revoked"] = True
        grants.write_text(json.dumps(data))
        page.reload()
        page.wait_for_selector("#error:not([hidden])")
        check("revoked access shows a visible error panel", page.locator("#error").is_visible())
        check("error heading receives focus", page.evaluate("document.activeElement.id") == "error-title")
        check("error offers a human route", "housing officer" in page.inner_text("#error"))
        check("no resident data after revocation", "Synthetic Row" not in page.inner_text("body"))
        grants.write_text(original)
        page.keyboard.press("Tab")
        check("retry reachable by keyboard", page.evaluate("document.activeElement.id") == "retry")
        page.keyboard.press("Enter")
        page.wait_for_selector("#content:not([hidden])")
        check("recovers after grant restored", "Confirmed arrangements" in page.inner_text("body"))
        page.context.close()
    with preview(root, "SYN-RES-EXPIRED") as base:
        page, _, _ = new_page(browser)
        page.goto(base + "/")
        page.wait_for_selector("#error:not([hidden])")
        check("expired grant shows the same plain error", "You cannot see this page" in page.inner_text("#error"))
        check("expired view shows no data", "Synthetic Row" not in page.inner_text("body"))
        page.context.close()
    with preview(root, "SYN-RES-A") as base:
        page, errors, _ = new_page(browser)
        page.route("**/resident/view", lambda route: route.abort())
        page.goto(base + "/")
        page.wait_for_selector("#error:not([hidden])")
        check("network failure shows a recoverable error", "could not reach" in page.inner_text("#error"))
        check("network failure error is focused", page.evaluate("document.activeElement.id") == "error-title")
        page.context.close()


def active_id(page: Page) -> str:
    return str(page.evaluate("document.activeElement.id || document.activeElement.tagName"))


def release(page: Page, held: list[Any]) -> None:
    for _ in range(100):
        if held:
            held.pop().continue_()
            return
        page.wait_for_timeout(50)
    raise AssertionError("resident view request was not held")


def check_retry_focus_and_announcements(browser: Any, root: Path) -> None:
    grants = root / "grants.json"
    original = grants.read_text()
    data = json.loads(original)
    data["grants"][0]["revoked"] = True
    grants.write_text(json.dumps(data))
    try:
        with preview(root, "SYN-RES-A") as base:
            page, errors, _ = new_page(browser, 320, 640)
            held: list[Any] = []
            page.route("**/resident/view", lambda route: held.append(route))
            page.goto(base + "/")
            page.wait_for_selector("#status:not(:empty)")
            check("initial loading status is announced by the live region", "Loading your progress" in page.inner_text("#status"))
            check("status is a polite live region", page.get_attribute("#status", "role") == "status" and page.get_attribute("#status", "aria-live") == "polite")
            release(page, held)
            page.wait_for_selector("#error:not([hidden])")
            check("error container is not also an alert live region", page.locator("[role=alert]").count() == 0)
            check("error heading is the focus target", active_id(page) == "error-title")
            check("error heading is described by the error text", page.get_attribute("#error-title", "aria-describedby") == "error-text")
            check("error text and human route are in the described panel", "housing officer" in page.inner_text("#error") and page.inner_text("#error-text") != "")
            page.keyboard.press("Tab")
            check("retry is the next keyboard stop", active_id(page) == "retry")
            page.keyboard.press("Enter")
            check("focus moves to main immediately after retry", active_id(page) == "main")
            check("loading status is announced during retry", "Loading your progress" in page.inner_text("#status"))
            check("error panel is hidden while loading", page.locator("#error").is_hidden())
            page.wait_for_timeout(200)
            check("focus stays on main while the request is pending", active_id(page) == "main")
            release(page, held)
            page.wait_for_selector("#error:not([hidden])")
            check("repeat failure returns focus to the error heading", active_id(page) == "error-title")
            grants.write_text(original)
            page.keyboard.press("Tab")
            page.keyboard.press("Enter")
            check("focus is on main after the second retry starts", active_id(page) == "main")
            release(page, held)
            page.wait_for_selector("#content:not([hidden])")
            check("focus stays on main after recovery, never body", active_id(page) == "main")
            check("recovery is announced in the status region", page.inner_text("#status") == "Your progress has loaded.")
            check("recovered view has no error panel or alert", page.locator("#error").is_hidden() and page.locator("[role=alert]").count() == 0)
            check("320px has no horizontal scroll after recovery", page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"))
            check("only the expected refused-request console errors in the retry flow", all("status of 403" in e for e in errors))
            page.context.close()
    finally:
        grants.write_text(original)


def check_skip_target_and_no_script(browser: Any, root: Path) -> None:
    with preview(root, "SYN-RES-A") as base:
        context = browser.new_context(java_script_enabled=False, viewport={"width": 1024, "height": 800})
        page = context.new_page()
        page.goto(base + "/")
        check("no loading text is shown without JavaScript", page.inner_text("#status").strip() == "")
        check("no-script message gives a human route", "speak to your housing officer" in page.inner_text("noscript").lower())
        context.close()
        page, _, _ = new_page(browser)
        page.goto(base + "/")
        page.wait_for_selector("#content:not([hidden])")
        page.keyboard.press("Tab")
        page.keyboard.press("Enter")
        check("skip link target is focused", active_id(page) == "main")
        width = page.evaluate("getComputedStyle(document.activeElement).outlineWidth")
        style = page.evaluate("getComputedStyle(document.activeElement).outlineStyle")
        check("skip link target shows a focus indicator of at least 3px", style != "none" and float(width.replace("px", "")) >= 3)
        page.context.close()


def check_representative(browser: Any, root: Path) -> None:
    with preview(root, "SYN-REP-B") as base:
        page, _, _ = new_page(browser)
        page.goto(base + "/")
        page.wait_for_selector("#content:not([hidden])")
        text = page.inner_text("body")
        check("representative sees covered tasks only", "Who this is for" in text and "Works decision: not shown" in text)
        check("representative sees no address", "Synthetic Row" not in text)
        page.context.close()


if __name__ == "__main__":
    main()
