"""Run the real local API with constructed data and check design-system foundations.

Run from src/api with the src packages and Playwright/Chromium installed:
python -m checks.design_system_browser_check
"""

from __future__ import annotations

import base64
import copy
import json
import os
import runpy
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]


def check(name: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(name)
    print(f"PASS {name}", flush=True)


def synthetic_data() -> dict[str, Any]:
    data: dict[str, Any] = runpy.run_path(str(ROOT / "src/core/tests/dataset.py"))["DATA"]
    normal = copy.deepcopy(data["cases"][0])
    normal["stage_since"] = date.today().isoformat()
    normal["home"].update(lat=54.9, lon=-1.6, area="Point examples")
    waiting = copy.deepcopy(normal)
    waiting.update(id="ZF-2", stage_since="2026-01-01", days_in_stage=90)
    waiting["home"].update(lat=54.902, lon=-1.598)
    hazard = copy.deepcopy(data["cases"][3])
    hazard["home"].update(lat=54.898, lon=-1.602, area="Point examples")
    data["cases"] = [normal, waiting, hazard]
    for number in range(502):
        extra = copy.deepcopy(normal)
        extra["id"] = f"CLUSTER-{number:04}"
        extra["home"].update(lat=54.92, lon=-1.62, area="Cluster examples")
        data["cases"].append(extra)
    return data


def run_browser(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.route(
                "https://tile.openstreetmap.org/**",
                lambda route: route.fulfill(
                    content_type="image/png",
                    body=base64.b64decode(
                        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
                        "+A8AAQUBAScY42YAAAAASUVORK5CYII="
                    ),
                ),
            )
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("synthetic-check")
            page.locator("button[type=submit]").click()
            page.get_by_role("heading", name="My cases today").wait_for()
            page.locator(".item").first.wait_for()
            check("real app login and synthetic workbench", page.locator(".item").count() > 0)
            page.get_by_text("AI suggestion, not approved", exact=False).first.wait_for()
            registry = page.request.get(base + "/api/assistants")
            check("existing assistant registry remains available", registry.status == 200)
            check(
                "Fluent native card, heading and control values resolve",
                page.evaluate("""() => {
                  const card = getComputedStyle(document.querySelector('.card'));
                  const heading = getComputedStyle(document.querySelector('h1'));
                  const button = getComputedStyle(document.querySelector('#signout'));
                  return card.borderRadius === '8px' && card.paddingLeft === '24px'
                    && heading.fontSize === '24px' && heading.lineHeight === '32px'
                    && button.borderRadius === '4px' && button.minHeight === '40px';
                }"""),
            )
            page.get_by_role("button", name="Show more", exact=False).click()
            page.wait_for_function("() => document.querySelectorAll('.item').length === 100")
            page.locator(".item").first.click()
            page.get_by_role("link", name="Back to the list", exact=True).wait_for()
            page.get_by_role("link", name="Back to the list", exact=True).click()
            page.wait_for_function("() => document.querySelectorAll('.item').length === 50")
            check(
                "paged queue return intentionally reloads first page",
                "first page" in page.locator(".side").inner_text(),
            )
            page.get_by_role("link", name="Overview", exact=True).click()
            page.locator(".cluster.hazard").wait_for()
            page.wait_for_function("""() => Array.from(document.querySelectorAll(
              '.cluster:not(.hazard) .cluster-safety')).some(x => x.textContent === 'Safety: 0')""")
            check(
                "real >500-home endpoint renders safety and zero-safety clusters",
                page.locator(".cluster.hazard .cluster-safety").inner_text() == "Safety: 1",
            )
            page.locator("#maplist-h").click()
            check(
                "cluster list includes explicit safety counts",
                "with a safety issue open" in page.locator(".maplist").inner_text(),
            )
            cluster = page.locator(".map-cluster").first
            page.keyboard.press("Tab")
            cluster.focus()
            check(
                "cluster keyboard focus is visible",
                cluster.evaluate("el => getComputedStyle(el).outlineStyle === 'solid'"),
            )
            with page.expect_response(lambda response: "/api/map?" in response.url):
                cluster.press("Enter")
            check("cluster Enter requests a zoomed map", True)
            page.locator("#mapArea").select_option(label="Point examples")
            page.locator(".map-marker .map-symbol.hazard").wait_for()
            check(
                "real area filter renders all three point states",
                page.locator(".map-marker").count() == 3,
            )
            for kind, shape, code, label in (
                ("normal", "circle", "O", "Normal"),
                ("long", "rect", "W", "Waiting 60+ days"),
                ("hazard", "path", "!", "Safety issue open"),
            ):
                marker = page.locator(f".map-marker:has(.map-symbol.{kind})")
                check(
                    f"{kind} marker has distinct geometry and visible code",
                    marker.locator(f"svg {shape}").count() == 1
                    and marker.locator(".marker-code").inner_text() == code,
                )
                check(
                    f"{kind} marker has a status name",
                    page.get_by_role("button", name=f"Pat Test, {label}", exact=True).count() == 1,
                )
            check("key uses the same three symbols", page.locator(".key .map-symbol").count() == 3)
            check(
                "point list retains status text",
                "Waiting 60+ days" in page.locator(".maplist").inner_text(),
            )
            selected = page.locator(".tile[aria-pressed=true]")
            check(
                "selected tile has visible words",
                selected.locator(".tile-selection").inner_text() == "Selected",
            )
            safety_tile = page.get_by_role("button", name="Safety issues open", exact=False)
            safety_tile.click()
            page.wait_for_function("""() => document.querySelector(
              '.tile.danger').getAttribute('aria-pressed') === 'true'
              && document.querySelectorAll('.map-marker').length === 1""")
            check(
                "filter change moves selected words and keeps safety label",
                safety_tile.locator(".tile-selection").inner_text() == "Selected",
            )
            page.get_by_role("button", name="Open cases", exact=False).click()
            page.wait_for_function("() => document.querySelectorAll('.map-marker').length === 3")
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                page.wait_for_timeout(100)
                overflow = page.evaluate("""() => [...document.querySelectorAll(
                  'main, main .grid, main .card, main table, .top')].filter(
                  el => !el.closest('.table-scroll')
                    && el.getBoundingClientRect().right > innerWidth).map(
                  el => [el.tagName, el.className, el.getBoundingClientRect().width])""")
                check(
                    f"Overview reflows at {width}px (overflow: {overflow})",
                    page.evaluate(
                        "() => document.documentElement.scrollWidth <= window.innerWidth"
                    ),
                )
                if width == 320:
                    table_region = page.get_by_role("region", name="Team workload table")
                    table_region.focus()
                    table_region.press("ArrowRight")
                    page.wait_for_function("""() => document.querySelector(
                      '[aria-label="Team workload table"]').scrollLeft > 0""")
                    check("wide data table scrolls with keyboard at 320px", True)
            page.emulate_media(reduced_motion="reduce")
            check(
                "reduced motion resolves to zero",
                selected.first.evaluate("""el => getComputedStyle(el).transitionDuration
                  .split(',').every(value => value.trim() === '0s')"""),
            )
            page.emulate_media(forced_colors="active")
            for kind in ("normal", "long", "hazard"):
                symbol = page.locator(f".map-marker .map-symbol.{kind}")
                check(
                    f"forced colours retain {kind} geometry and text",
                    symbol.locator("svg").is_visible()
                    and bool(symbol.locator(".marker-code").inner_text()),
                )
            check(
                "forced colours retain selected words",
                page.locator(".tile[aria-pressed=true] .tile-selection").inner_text() == "Selected",
            )
            marker = page.locator(".map-marker:has(.map-symbol.hazard)")
            marker.focus()
            marker.press("Enter")
            page.get_by_role("link", name="Open home", exact=True).click()
            page.wait_for_url("**#/case/ZF-4")
            page.get_by_role("heading", name="Pat Test", exact=False).first.wait_for()
            check("point marker Enter opens the real case", "ZF-4" in page.url)
            page.get_by_role("link", name="Overview", exact=True).click()
            page.locator(".map-marker .map-symbol.normal").wait_for()
            page.locator(".map-marker:has(.map-symbol.normal)").press("Space")
            page.get_by_role("link", name="Open home", exact=True).click()
            page.wait_for_url("**#/case/ZF-1")
            check("point marker Space opens the real case", "ZF-1" in page.url)
            check(f"no uncaught JavaScript errors ({errors})", not errors)
            print(f"Browser: Chromium {browser.version}; no live model/SQL/Azure calls.")
        finally:
            browser.close()


def main(
    browser_check: Callable[[str], None] = run_browser,
    data_factory: Callable[[], dict[str, Any]] = synthetic_data,
) -> None:
    (ROOT / ".venv").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="zf-browser-", dir=ROOT / ".venv") as scratch:
        work = Path(scratch)
        data = work / "synthetic.json"
        data.write_text(json.dumps(data_factory()), encoding="utf-8")
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        base = f"http://127.0.0.1:{port}"
        # Do not inherit model endpoints, credentials, private data or deployment settings.
        env = {key: os.environ[key] for key in ("PATH", "HOME", "LANG") if key in os.environ}
        env.update(
            PYTHONPATH=os.pathsep.join(
                str(ROOT / "src" / project / "src") for project in ("core", "agents", "api")
            ),
            ZF_DATA=str(data),
            ZF_STATE=str(work),
            ZF_STORE="json",
            ZF_PASSWORD="synthetic-check",
            ZF_BIND="127.0.0.1",
            PORT=str(port),
            ZF_ENV="development",
            ZF_AUTH="password",
        )
        with (work / "server.log").open("w+", encoding="utf-8") as log:
            process = subprocess.Popen(
                [sys.executable, "-m", "zava_forward.api.server"],
                env=env,
                stdout=log,
                stderr=log,
            )
            try:
                for _ in range(100):
                    try:
                        with urllib.request.urlopen(base + "/healthz", timeout=1) as response:
                            if response.status == 200:
                                break
                    except (urllib.error.URLError, TimeoutError):
                        if process.poll() is not None:
                            log.seek(0)
                            raise RuntimeError(f"Local server exited: {log.read()}") from None
                        time.sleep(0.1)
                else:
                    raise TimeoutError("Local synthetic server did not become healthy")
                check("owned server is running and responsive on loopback", process.poll() is None)
                browser_check(base)
            finally:
                process.terminate()
                process.wait(timeout=10)


if __name__ == "__main__":
    main()
    from checks.workbench_browser_check import run_browser as workbench_check
    from checks.workbench_browser_check import synthetic_data as workbench_data

    main(workbench_check, workbench_data)
