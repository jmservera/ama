"""Observation-only diagnostic for issue 1384 (not part of the product or the checks).

Runs the unmodified scenario functions of the two generic workspace browser checks against the
owned synthetic loopback server and records, per scenario: every request for the target asset
(identity, resource type, offset, response status or failure), every script element added to,
loaded by, errored on or removed from the page (so an aborted load, a successful evaluation
without the readiness global and a timeout are distinguishable), and the terminal page state.
The original assertions are executed as written; a failure is recorded with its traceback and
the scenario list continues. The output file is created exclusively and never overwritten.

Usage (from src/api): PYTHONPATH=. python <this file> employee|scripts <new-output.json>
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from typing import Any

from playwright.sync_api import BrowserContext, Page, sync_playwright

import checks.employee_workspace_browser_check as employee
import checks.workspace_scripts_browser_check as scripts
from checks.design_system_browser_check import main

TARGETS = ("/ops.js", "/vendor/leaflet.js", "/role-screens.js")
START = time.monotonic()
SCENARIOS: list[dict[str, Any]] = []
CURRENT: dict[str, Any] = {}

INIT = """
window.__scriptLog = [];
const stamp = () => Math.round(performance.now());
const watch = script => {
  if (script.__watched) return;
  script.__watched = true;
  const ready = () => ({ops: typeof qualityPanel === 'function', leaflet: typeof L === 'object',
    roleScreens: typeof roleScreensView === 'function'});
  window.__scriptLog.push({t: stamp(), ev: 'added', src: script.getAttribute('src')});
  script.addEventListener('load', () => window.__scriptLog.push(
    {t: stamp(), ev: 'load', src: script.getAttribute('src'), ready: ready()}));
  script.addEventListener('error', () => window.__scriptLog.push(
    {t: stamp(), ev: 'error', src: script.getAttribute('src')}));
};
new MutationObserver(records => {
  for (const record of records) {
    for (const node of record.addedNodes) if (node.tagName === 'SCRIPT') watch(node);
    for (const node of record.removedNodes) if (node.tagName === 'SCRIPT') {
      window.__scriptLog.push({t: stamp(), ev: 'removed', src: node.getAttribute('src')});
    }
  }
}).observe(document, {childList: true, subtree: true});
"""


def relevant(url: str) -> bool:
    path = url.split("?")[0]
    return any(path.endswith(target) for target in TARGETS)


def attach(context: BrowserContext) -> None:
    network: list[dict[str, Any]] = []
    CURRENT.setdefault("contexts", []).append({"network": network, "context": context})
    context.add_init_script(INIT)

    def entry(kind: str, request: Any, **extra: Any) -> None:
        if relevant(request.url):
            network.append({
                "event": kind, "t_ms": round((time.monotonic() - START) * 1000),
                "url": request.url, "resource_type": request.resource_type, **extra,
            })

    context.on("request", lambda request: entry("request", request))
    context.on("requestfailed", lambda request: entry(
        "requestfailed", request, failure=request.failure))
    context.on("response", lambda response: entry(
        "response", response.request, status=response.status))


def snapshot(context: BrowserContext, record: dict[str, Any], key: str = "pages") -> None:
    pages: list[dict[str, Any]] = []
    for page in context.pages:
        state: dict[str, Any] = {"url": page.url}
        try:
            state["script_log"] = page.evaluate("() => window.__scriptLog")
            state["workspace_status"] = page.locator("#workspace-status").inner_text(timeout=500)
            state["alert"] = page.get_by_role("alert").all_inner_texts()
            state["headings"] = page.get_by_role("heading").all_inner_texts()
            state["ready"] = page.evaluate(
                "() => ({ops: typeof qualityPanel === 'function', leaflet: typeof L === 'object',"
                " roleScreens: typeof roleScreensView === 'function'})")
            state["head_script_srcs"] = page.evaluate(
                "() => [...document.querySelectorAll('script[src]')].map(s => s.getAttribute('src'))")
        except Exception as error:  # observation only
            state["snapshot_error"] = repr(error)
        pages.append(state)
    record[key] = pages


original_close = BrowserContext.close


def close(self: BrowserContext, **kwargs: Any) -> None:
    for item in CURRENT.get("contexts", []):
        if item["context"] is self and "pages" not in item:
            snapshot(self, item)
    return original_close(self, **kwargs)


original_unroute = Page.unroute


def unroute(self: Page, *args: Any, **kwargs: Any) -> Any:
    # The checks unroute immediately before the native reload: capture the terminal failed state.
    for item in CURRENT.get("contexts", []):
        if item["context"] is self.context and "pre_unroute_pages" not in item:
            snapshot(self.context, item, "pre_unroute_pages")
    return original_unroute(self, *args, **kwargs)


Page.unroute = unroute  # type: ignore[method-assign]
BrowserContext.close = close  # type: ignore[method-assign]


def run(label: str, function: Any, *args: Any, **kwargs: Any) -> None:
    CURRENT.clear()
    record: dict[str, Any] = {"scenario": label, "started_ms": round((time.monotonic() - START) * 1000)}
    try:
        function(*args, **kwargs)
        record["original_assertions"] = "passed"
    except BaseException as error:  # record, then continue with the next scenario
        record["original_assertions"] = "FAILED"
        record["exception"] = repr(error)
        record["traceback"] = traceback.format_exc()
    record["contexts"] = [
        {"network": item["network"], "pre_unroute_pages": item.get("pre_unroute_pages"),
         "pages": item.get("pages")}
        for item in CURRENT.get("contexts", [])
    ]
    SCENARIOS.append(record)
    print(f"DIAG {label}: {record['original_assertions']}", flush=True)


def patch_new_contexts(browser: Any) -> None:
    original = browser.new_context

    def new_context(*args: Any, **kwargs: Any) -> BrowserContext:
        context = original(*args, **kwargs)
        attach(context)
        return context

    browser.new_context = new_context


def run_scripts(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        patch_new_contexts(browser)
        try:
            run("exhaustion (repeated aborted loads)", scripts.exhaustion, browser, base)
            run("exhaustion missing_global", scripts.exhaustion, browser, base, missing_global=True)
            run("delayed companion timed_out", scripts.delayed_companion, browser, base,
                timed_out=True)
        finally:
            browser.close()


def run_employee(base: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        patch_new_contexts(browser)
        try:
            run("missing_ops_recovery (404 on /ops.js)", employee.missing_ops_recovery, browser, base)
        finally:
            browser.close()


if __name__ == "__main__":
    which, out = sys.argv[1], sys.argv[2]
    try:
        if which == "employee":
            main(run_employee, employee.employee_data)
        else:
            main(run_scripts, scripts.synthetic_data)
    finally:
        with open(out, "x", encoding="utf-8") as handle:
            json.dump({"which": which, "scenarios": SCENARIOS}, handle, indent=2)
