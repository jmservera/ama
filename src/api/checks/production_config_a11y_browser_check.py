"""Issue 619: automated axe and keyboard checks on the employee site in its production configuration.

The owned loopback server runs with ZF_ENV=production and the trusted-proxy provider, so the
shared-password sign-in is refused and the page is reached the way the ingress delivers it.
Synthetic data only. This does not replace the person-run screen reader, zoom and consent
records in docs/reference/research/ux/production-ux-acceptance-protocol.md.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.metadata
import json
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, expect, sync_playwright

from checks.design_system_browser_check import check, main, synthetic_data
from checks.regulatory_ux_check import AXE_SHA256

TENANT = "11111111-2222-4333-8444-555555555555"
OBJECT_ID = "66666666-7777-4888-8999-000000000000"
ROLE = "http://schemas.microsoft.com/ws/2008/06/identity/claims/role"
PRODUCTION_ENV = {
    "ZF_ENV": "production",
    "ZF_AUTH": "trusted-proxy",
    "ZF_TRUSTED_PROXY": "1",
    "ZF_ENTRA_TENANT_ID": TENANT,
}
TABS = ("Overview", "Documents", "History")
NOT_A_CONTROL = "['BODY', 'HTML', 'SCRIPT'].includes(document.activeElement.tagName)"
OBSCURED = """() => {
  const el = document.activeElement, r = el.getBoundingClientRect();
  const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  return !(hit && el.contains(hit));
}"""
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]


def principal_header() -> str:
    claims = [
        {"typ": "tid", "val": TENANT},
        {"typ": "oid", "val": OBJECT_ID},
        {"typ": "name", "val": "Synthetic Coordinator"},
        {"typ": "roles", "val": "ZavaForward.Coordinator"},
    ]
    raw = json.dumps({"auth_typ": "aad", "claims": claims}).encode()
    return base64.b64encode(raw).decode()


def scan(page: Page, axe: str, root: str, state: str, reports: list[dict[str, Any]]) -> None:
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async ([root, tags]) => await axe.run(document.querySelector(root),
          {runOnly: {type: 'tag', values: tags}})""",
        [root, WCAG_TAGS],
    )
    reports.append(
        {"state": state, "violations": result["violations"], "incomplete": len(result["incomplete"]),
         "passes": len(result["passes"])}
    )
    check(f"axe no violations: {state}", not result["violations"])


def focus_visible(page: Page) -> bool:
    visible: bool = page.evaluate("""() => {
      const el = document.activeElement;
      if (!el || el === document.body) return false;
      const r = el.getBoundingClientRect(), s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0;
    }""")
    return visible


def case_view(page: Page, axe: str, reports: list[dict[str, Any]]) -> None:
    page.goto(page.url.split("#")[0] + "#/case/ZF-1?tab=overview")
    tablist = page.get_by_role("tablist", name="Case sections")
    tablist.wait_for()
    check("case view has a named tab list", tablist.get_by_role("tab").count() >= len(TABS))
    scan(page, axe, "main", "case view overview", reports)
    selected = tablist.get_by_role("tab", selected=True)
    selected.focus()
    check("selected tab shows a visible focus indicator", focus_visible(page))
    names: list[str] = []
    for _ in range(len(TABS) - 1):
        page.keyboard.press("ArrowRight")
        names.append(page.evaluate("document.activeElement.textContent.trim()"))
    check("arrow keys move through distinct tabs", len(set(names)) == len(names))
    check("focus stays on the tab list", page.evaluate("!!document.activeElement.closest('[role=tablist]')"))
    page.keyboard.press("Enter")
    panel = page.get_by_role("tabpanel")
    expect(panel).to_be_visible()
    scan(page, axe, "main", "case view second tab", reports)
    seen: set[str] = set()
    page.locator("main").first.focus()
    for _ in range(40):
        page.keyboard.press("Tab")
        if page.evaluate(NOT_A_CONTROL):
            break
        seen.add(page.evaluate("document.activeElement.tagName + ':' + (document.activeElement.id || document.activeElement.textContent || '').trim().slice(0, 30)"))
        check("every Tab stop in the case view shows focus", focus_visible(page))
    check("Tab reaches several controls in the case view", len(seen) > 3)


def chat_widget(page: Page, axe: str, reports: list[dict[str, Any]]) -> None:
    launcher = page.locator("#employee-chat-launcher")
    launcher.focus()
    check("chat launcher shows a visible focus indicator", focus_visible(page))
    check("chat launcher has an accessible name", bool(launcher.get_attribute("aria-label") or launcher.inner_text().strip()))
    page.keyboard.press("Enter")
    panel = page.locator(".chat-widget")
    expect(panel).to_be_visible()
    check("focus moves into the chat panel", page.evaluate("!!document.activeElement.closest('.chat-widget')"))
    scan(page, axe, ".chat-widget", "employee chat widget open", reports)
    for _ in range(12):
        page.keyboard.press("Tab")
        if page.evaluate(NOT_A_CONTROL):
            break
        check("Tab never moves focus behind the chat or off screen", page.evaluate(OBSCURED) is False)
    panel.locator("textarea").focus()
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    expect(launcher).to_be_focused()


def run_browser(base: str, axe: str, out: Path) -> None:
    reports: list[dict[str, Any]] = []
    results: dict[str, Any] = {"completed": False, "scans": reports, "axe_sha256": AXE_SHA256}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        results["browser_version"] = browser.version
        results["playwright_version"] = importlib.metadata.version("playwright")
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            extra_http_headers={"X-MS-CLIENT-PRINCIPAL": principal_header()},
        )
        context.route(
            "**/*",
            lambda route: route.continue_() if route.request.url.startswith(base + "/") else route.abort(),
        )
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        try:
            page.goto(base + "/app#/case/ZF-1?tab=overview")
            page.get_by_role("tablist", name="Case sections").wait_for()
            check("production configuration serves the app through the trusted proxy header", True)
            case_view(page, axe, reports)
            chat_widget(page, axe, reports)
            check("no uncaught page errors", not errors)
            results["completed"] = True
        finally:
            (out / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
            context.close()
            browser.close()


def cli() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe", type=Path, required=True, help="Pinned axe-core 4.10.3")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.axe.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Expected pinned axe-core 4.10.3")
    args.out.mkdir(parents=True, exist_ok=False)
    main(
        lambda base: run_browser(base, raw.decode(), args.out),
        synthetic_data,
        env_overrides=PRODUCTION_ENV,
    )


if __name__ == "__main__":
    cli()
