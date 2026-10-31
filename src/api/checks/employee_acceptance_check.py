"""Capture-free employee checks for an independently verified authenticated Page."""

from __future__ import annotations

import os
import re
from collections.abc import Callable, Mapping
from typing import Literal, TypedDict
from urllib.parse import urlsplit

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import Page

from checks.employee_identity_check import BINDING

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
FLAGS = frozenset(
    "expectationValid responseOk schemaValid providerMatches expectedIdentity employeeRole "
    "notViewOnly displayEmailMatches rosterBound transportFailed jsonFailed authenticated".split()
)
ADMISSION = FLAGS - {"displayEmailMatches", "rosterBound", "transportFailed", "jsonFailed"}
GUID = re.compile(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", re.IGNORECASE)
Observation = dict[str, bool | int]


class Stage(TypedDict):
    status: Literal["passed", "failed", "blocked"]
    observations: Observation


class Acceptance(TypedDict):
    identity: dict[str, bool]
    stages: dict[str, Stage]
    passed: bool


def valid_expected(expected: Mapping[str, object]) -> bool:
    return all(
        isinstance(expected.get(key), str) and GUID.fullmatch(str(expected[key])) is not None
        for key in ("tid", "oid")
    )


def allowed_page(page: Page, origin: str) -> bool:
    try:
        target = urlsplit(origin)
        current = urlsplit(page.url)
        local = (
            target.scheme == "http"
            and target.hostname in {"127.0.0.1", "localhost", "::1"}
            and target.port is not None
        )
        return (
            (origin == APP or local)
            and target.path == ""
            and not target.query
            and not target.fragment
            and target.username is None
            and target.password is None
            and current.username is None
            and current.password is None
            and (current.scheme, current.hostname, current.port)
            == (target.scheme, target.hostname, target.port)
        )
    except ValueError:
        return False


def probe(page: Page, expected: Mapping[str, object], origin: str = APP) -> dict[str, bool]:
    denied = {key: False for key in FLAGS}
    if (
        not valid_expected(expected)
        or any(
            os.environ.get(key) for key in ("DEBUG", "PWDEBUG", "PLAYWRIGHT_DEBUG", "DEBUG_FILE")
        )
        or not allowed_page(page, origin)
    ):
        return denied
    try:
        expectation = {key: expected[key] for key in ("tid", "oid")}
        if isinstance(expected.get("email"), str):
            expectation["email"] = expected["email"]
        result = page.evaluate(BINDING, expectation)
    except BrowserError:
        return dict(denied, transportFailed=True)
    if (
        not allowed_page(page, origin)
        or not isinstance(result, dict)
        or result.keys() != FLAGS
        or any(type(value) is not bool for value in result.values())
    ):
        return denied
    if not all(result[key] is True for key in ADMISSION) or any(
        result[key] is True for key in ("transportFailed", "jsonFailed")
    ):
        result["authenticated"] = False
    return {key: result[key] for key in FLAGS}


def chat(page: Page) -> Observation:
    page.locator("#employee-chat-launcher").press("Enter")
    panel = page.locator("#employee-chat")
    panel.wait_for(state="visible", timeout=120000)
    skill = panel.locator("form select")
    page.wait_for_function(
        "() => document.querySelector('#employee-chat form select')?.disabled === false",
        timeout=120000,
    )
    options = skill.locator("option")
    if options.count() < 2:
        return {"passed": False}
    selected = options.nth(1).get_attribute("value")
    if not selected:
        return {"passed": False}
    skill.select_option(selected)
    previous = panel.locator(".chat-widget-assistant").count()
    panel.locator("textarea").fill(
        "What can this advisory skill help me do? Do not include resident or case details."
    )
    panel.get_by_role("button", name="Send", exact=True).click()
    page.wait_for_function(
        """before => {
          const panel = document.querySelector('#employee-chat');
          if (!panel) return true;
          const alert = panel?.querySelector('[role=alert]');
          return panel?.querySelector('form')?.getAttribute('aria-busy') === 'false'
            && (panel.querySelectorAll('.chat-widget-assistant').length > before
              || (alert && !alert.hidden));
        }""",
        arg=previous,
        timeout=120000,
    )
    result: Observation = panel.evaluate(
        """(e, skill) => {
          const reply = [...e.querySelectorAll('.chat-widget-assistant')].at(-1);
          const label = reply?.querySelector('.chat-widget-meta')?.textContent || '';
          const alert = e.querySelector('[role=alert]');
          return {
            passed: !e.hidden && !!reply && reply.textContent.includes('Skill: ' + skill)
              && !!reply.querySelector('p')?.textContent.trim()
              && (!alert || alert.hidden),
            workflowOnly: /workflow.only|no AI|rules/i.test(label),
            actualAiLabel: /AI suggestion|AI.generated/i.test(label) && !/no AI|workflow.only/i.test(label)
          };
        }""",
        selected,
    )
    page.keyboard.press("Escape")
    return result


def map_filters(page: Page) -> Observation:
    page.evaluate("location.hash = '#/overview'")
    page.locator(".overview-map-filters").wait_for(state="visible", timeout=120000)
    page.get_by_role("button", name="Expand map", exact=True).press("Enter")
    buttons = page.locator(".map-dialog[open] .overview-map-filters button[aria-pressed]")
    candidates = [
        index
        for index in range(buttons.count())
        if buttons.nth(index).get_attribute("aria-pressed") == "false"
    ]
    if not candidates:
        return {"passed": False}
    button = buttons.nth(candidates[0])
    with page.expect_response(
        lambda response: (
            urlsplit(response.url).path == "/api/map" and allowed_response(response.url, page.url)
        ),
        timeout=120000,
    ) as response:
        button.press("Space")
    if response.value.status != 200:
        return {"passed": False}
    payload = response.value.json()
    total = payload.get("total") if isinstance(payload, dict) else None
    page.wait_for_function(
        """() => {
          const map = document.querySelector('#leaflet');
          return !!map && map.getAttribute('aria-busy') !== 'true';
        }""",
        timeout=120000,
    )
    passed = (
        type(total) is int
        and total >= 0
        and button.get_attribute("aria-pressed") == "true"
        and button.locator(".tile-selection").inner_text() == "Selected"
        and button.evaluate("e => document.activeElement === e")
    )
    page.keyboard.press("Escape")
    return {"passed": passed}


def allowed_response(url: str, page_url: str) -> bool:
    response, current = urlsplit(url), urlsplit(page_url)
    return (response.scheme, response.netloc) == (current.scheme, current.netloc)


def case_view(page: Page) -> Observation:
    page.evaluate("location.hash = '#/all'")
    link = page.locator('a.item[href^="#/case/"]').first
    link.wait_for(state="visible", timeout=120000)
    link.click()
    page.locator(".case-journey").wait_for(state="visible", timeout=120000)
    return {
        "passed": page.locator(".step").count() > 0
        and page.locator("#app [role=alert]:visible").count() == 0
    }


OBSERVERS: dict[str, Callable[[Page], Observation]] = {
    "chat": chat,
    "map": map_filters,
    "case": case_view,
}


def verify_employee(page: Page, expected: Mapping[str, object], origin: str = APP) -> Acceptance:
    result: Acceptance = {
        "identity": probe(page, expected, origin),
        "stages": {key: {"status": "blocked", "observations": {}} for key in OBSERVERS},
        "passed": False,
    }
    if result["identity"]["authenticated"] is not True:
        return result
    for name, observe in OBSERVERS.items():
        if probe(page, expected, origin)["authenticated"] is not True:
            return result
        try:
            values = observe(page)
        except (BrowserError, ValueError):
            result["stages"][name]["status"] = "failed"
            return result
        if probe(page, expected, origin)["authenticated"] is not True:
            return result
        if (
            not isinstance(values, dict)
            or not values.keys() <= {"passed", "workflowOnly", "actualAiLabel"}
            or any(type(value) is not bool for value in values.values())
        ):
            result["stages"][name]["status"] = "failed"
            return result
        passed = values.get("passed") is True
        result["stages"][name] = {
            "status": "passed" if passed else "failed",
            "observations": values,
        }
        if not passed:
            return result
    result["passed"] = True
    return result


if __name__ == "__main__":
    import unittest

    suite = unittest.defaultTestLoader.loadTestsFromNames(
        [
            "test_employee_acceptance_check.AcceptanceTests.test_chromium_rosterless",
            "test_employee_acceptance_check.AcceptanceTests.test_chromium_wrong_account",
        ]
    )
    raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
