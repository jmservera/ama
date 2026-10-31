"""Warm-cache release turnover on actual loopback handlers; no external services."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.parse import urlsplit

from playwright.sync_api import Browser, expect, sync_playwright
from test_resident_demo_api import FAKE_PASSWORD, DemoTestCase
from test_ui_support import Base

from zava_forward.api import server as employee
from zava_forward.api.resident_demo import app as resident
from checks.asset_urls import asset_url


def exercise(browser: Browser, site: str, out: Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    if site == "employee":
        Base.setUpClass()
        httpd = Base.httpd
        local_web, shared_web = employee.WEB, employee.WEB
        entry, script, style = "/app", "/app.js", "/style.css"
    else:
        fixture = DemoTestCase()
        fixture.setUp()
        fixture.app.allowed_hosts = ("127.0.0.1",)
        httpd = fixture.server
        local_web, shared_web = resident.WEB, resident.SHARED_WEB
        entry, script, style = "/", "/demo.js", "/demo.css"
    base = f"http://127.0.0.1:{httpd.server_port}"
    legacy = {script: b'window.cacheRelease = "legacy";',
              style: b"body { --cache-release: legacy; }",
              "/chat-widget.js": b'window.cacheShared = "legacy";'}
    if site == "employee":
        legacy["/vendor/leaflet.js"] = b'window.cacheVendor = "legacy";'
    prime = ("<!doctype html><title>Constructed legacy cache</title>"
             f'<link rel="stylesheet" href="{style}">'
             + "".join(f'<script src="{url}"></script>' for url in legacy if url.endswith(".js")))

    def instrument(
        handler: type[BaseHTTPRequestHandler], *, old: bool = False
    ) -> type[BaseHTTPRequestHandler]:
        class Observed(handler):  # type: ignore[valid-type, misc]
            def send_response(self, code: int, message: str | None = None) -> None:
                records.append({"url": self.path, "status": code,
                                "validator": self.headers.get("If-None-Match")})
                super().send_response(code, message)

            def do_GET(self) -> None:
                if self.path == "/cache-prime" or (old and self.path in legacy):
                    body = prime.encode() if self.path == "/cache-prime" else legacy[self.path]
                    ctype = "text/html" if self.path == "/cache-prime" else (
                        "text/css" if self.path.endswith(".css") else "text/javascript")
                    self.send_response(200)
                    self.send_header("Content-Type", ctype)
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("Cache-Control", "no-store" if self.path == "/cache-prime"
                                     else "public, max-age=31536000")
                    self.end_headers()
                    self.wfile.write(body)
                    return
                if (not old and asset_url("/chat-widget.js").search(self.path)
                        and not failures):
                    failures.append(self.path)
                    self.send_response(503)
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                super().do_GET()
        return Observed

    context = browser.new_context()
    try:
        with tempfile.TemporaryDirectory(prefix="asset-release-") as work:
            root = Path(work)
            shutil.copytree(local_web, root / "local")
            shutil.copytree(shared_web, root / "shared")

            def release(label: str) -> type[BaseHTTPRequestHandler]:
                for name, target in ((script, "cacheRelease"), ("/chat-widget.js", "cacheShared")):
                    folder = root / ("shared" if name == "/chat-widget.js" else "local")
                    path = folder / name.lstrip("/")
                    original = (shared_web if name == "/chat-widget.js" else local_web) / name.lstrip("/")
                    path.write_bytes(original.read_bytes() + f'\nwindow.{target} = "{label}";\n'.encode())
                    if site == "employee" and name == "/chat-widget.js":
                        shutil.copyfile(path, root / "local/chat-widget.js")
                if site == "employee":
                    path = root / "local/vendor/leaflet.js"
                    path.write_bytes((local_web / "vendor/leaflet.js").read_bytes()
                                     + f'\nwindow.cacheVendor = "{label}";\n'.encode())
                css = root / "local" / style.lstrip("/")
                css.write_bytes((local_web / style.lstrip("/")).read_bytes()
                                + f"\nbody {{ --cache-release: {label}; }}\n".encode())
                if site == "employee":
                    with patch.object(employee, "WEB", root / "local"):
                        return employee.make_handler(Base.app)
                with patch.object(resident, "WEB", root / "local"), patch.object(
                    resident, "SHARED_WEB", root / "shared"
                ):
                    return resident.make_handler(fixture.app)

            httpd.RequestHandlerClass = instrument(release("A"), old=True)
            page = context.new_page()
            page.goto(base + "/cache-prime")
            assert page.evaluate("window.cacheRelease") == "legacy"
            assert page.evaluate("window.cacheShared") == "legacy"
            counts = {url: sum(row["url"] == url for row in records) for url in legacy}
            page.goto(base + "/cache-prime")
            assert all(sum(row["url"] == url for row in records) == count
                       for url, count in counts.items()), "Legacy cache was not warm/reused"
            old_links = context.request.get(base + entry).text()
            httpd.RequestHandlerClass = instrument(release("B"))
            page.goto(base + entry)
            page.wait_for_function("() => window.cacheRelease === 'B'")
            if site == "employee":
                # The shared-widget first download failed; ordinary launcher admission recovers it.
                page.get_by_label("Work email", exact=True).fill("sam@example.test")
                page.get_by_label("Password", exact=True).fill("pw")
                page.get_by_role("button", name="Sign in", exact=True).click()
                expect(page.get_by_role("heading", name="My cases today", exact=True)).to_be_visible()
                page.wait_for_function("() => window.cacheShared === 'B'")
                assert page.evaluate("window.cacheVendor") == "B"
            else:
                # Resident failure retains its visible manual help, with fresh code on next load.
                page.get_by_label("Email address", exact=True).fill("one@example.com")
                page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
                page.get_by_role("button", name="Sign in", exact=True).click()
                expect(page.locator("body")).to_contain_text("Chat could not load")
                page.reload()
                page.wait_for_function("() => window.cacheShared === 'B'")
            assert page.evaluate("getComputedStyle(document.body).getPropertyValue('--cache-release').trim()") == "B"
            urls = page.locator("script[src], link[rel=stylesheet]").evaluate_all(
                "nodes => nodes.map(node => node.getAttribute('src') || node.getAttribute('href'))")
            assert all(urlsplit(url).query.startswith("v=") for url in urls), urls
            assert all(url not in old_links for url in urls), "Release URLs did not change"
            widget_url = next(url for url in urls if asset_url("/chat-widget.js").search(url))
            assert failures == [widget_url], failures
            assert sum(row["url"] == widget_url for row in records) == 2, records
            page.reload()
            page.wait_for_function("() => window.cacheRelease === 'B' && window.cacheShared === 'B'")
            assert any(row["status"] == 304 and row["validator"] for row in records), records
            page.screenshot(path=str(out / f"{site}-release-B.png"))
            result = {"site": site, "origin": base, "same_context": True,
                      "legacy_cache_reused": True, "executed_release": "B", "applied_css": "B",
                      "shared_widget": "B", "vendor": "B" if site == "employee" else None,
                      "failed_initial_widget_url": widget_url, "initial_and_recovery_requests": 2,
                      "requests": records}
            print(f"PASS {site}: warm legacy cache, same-origin release B, JS/CSS/shared/vendor and ETags")
            return result
    finally:
        context.close()
        if site == "employee":
            Base.tearDownClass()
        else:
            fixture.doCleanups()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            results = [exercise(browser, site, args.out) for site in ("employee", "resident")]
            (args.out / "results.json").write_text(json.dumps(
                {"status": "passed", "browser": browser.version, "results": results}, indent=2))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
