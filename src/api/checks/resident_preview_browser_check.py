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
        page.click("#retry") if page.locator("#retry").is_visible() else page.reload()
        page.wait_for_selector("#error:not([hidden])")
        check("revoked access shows an error alert", page.get_by_role("alert").is_visible())
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
