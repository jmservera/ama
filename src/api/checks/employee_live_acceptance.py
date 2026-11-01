"""Credential-free operator entry point for live employee acceptance (#570).

The operator signs in manually in a Chromium started with a loopback remote
debugging port; this command only attaches and runs the strict observers.
"""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Mapping, Sequence
from urllib.parse import urlsplit

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import Page, sync_playwright

from checks.employee_acceptance_check import APP, allowed_page, valid_expected, verify_employee

LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def loopback_cdp(url: str) -> bool:
    try:
        parts = urlsplit(url)
        return (
            parts.scheme in {"http", "ws"}
            and parts.hostname in LOOPBACK
            and parts.port is not None
            and parts.username is None
            and parts.password is None
        )
    except ValueError:
        return False


def option(argv: Sequence[str], name: str, default: str = "") -> str:
    for index, arg in enumerate(argv[:-1]):
        if arg == name:
            return argv[index + 1]
    return default


def find_page(pages: Sequence[Page], origin: str) -> Page | None:
    return next((page for page in pages if allowed_page(page, origin)), None)


def main(argv: Sequence[str], env: Mapping[str, str]) -> int:
    expected = {"tid": env.get("ZF_EXPECTED_TID", ""), "oid": env.get("ZF_EXPECTED_OID", "")}
    cdp = option(argv, "--cdp-url", "http://127.0.0.1:9222")
    origin = option(argv, "--origin", APP)
    if not valid_expected(expected) or not loopback_cdp(cdp):
        print(json.dumps({"status": "refused", "passed": False}))
        return 2
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(cdp)
            try:
                pages = [p for context in browser.contexts for p in context.pages]
                page = find_page(pages, origin)
                if page is None:
                    print(json.dumps({"status": "no-page", "passed": False}))
                    return 2
                result = verify_employee(page, expected, origin)
            finally:
                browser.close()
    except BrowserError:
        print(json.dumps({"status": "browser-error", "passed": False}))
        return 2
    print(json.dumps({"status": "done", **result}, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:], os.environ))
