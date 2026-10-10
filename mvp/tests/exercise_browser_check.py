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


def main() -> int:
    """Run browser profiles, parser journey and viewport/focus probes locally."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
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
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(channel="chrome")
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
                        page.evaluate("document.documentElement.style.fontSize = '200%'")
                        record("text-resize-200-percent",
                               not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"))
                        page.evaluate("document.documentElement.style.fontSize = ''")
                        page.keyboard.press("Tab")
                        record("keyboard-visible-focus", page.evaluate(
                            "document.activeElement !== document.body && getComputedStyle(document.activeElement).outlineStyle !== 'none'"))
                        record("form-input-labels", page.evaluate(
                            """[...document.querySelectorAll('#app input:not([type=hidden]),#app select,#app textarea')]
                            .every(e => e.getAttribute('aria-label') || e.labels.length)"""))
                        record("no-duplicate-dom-ids", page.evaluate(
                            """(() => {const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
                            return new Set(ids).size===ids.length})()"""))
                        page.goto(base + "#/exercise")
                        page.get_by_role("heading", name="Nine connected workflows", exact=True).wait_for()
                        record("nine-workflow-navigation", page.locator("#app article h3").count() >= 9)
                        record("forecast-table-equivalent", page.locator("#exercise-forecast table caption").count() == 5
                               and "missing_input: abstained" in page.locator("#exercise-forecast").inner_text())
                        page.locator("#exercise-forecast summary").first.click()
                        page.screenshot(path=str(args.output.parent / "exercise-overview.png"), full_page=True)
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
