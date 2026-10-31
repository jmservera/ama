"""Capture-free employee checks for an independently verified authenticated Page."""

from __future__ import annotations

import os
import re
import time
from collections.abc import Callable, Mapping
from math import isfinite
from typing import Literal, TypedDict
from urllib.parse import parse_qs, quote, urlsplit

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import Page, Request, Response

from checks.employee_identity_check import BINDING

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
FLAGS = frozenset(
    "expectationValid responseOk schemaValid providerMatches expectedIdentity employeeRole "
    "notViewOnly displayEmailMatches rosterBound transportFailed jsonFailed authenticated".split()
)
ADMISSION = FLAGS - {"displayEmailMatches", "rosterBound", "transportFailed", "jsonFailed"}
GUID = re.compile(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", re.IGNORECASE)
MAP_TIMEOUT = 120000
MAP_FLAGS = ("", "hazard", "long", "nodecision", "fundingprog", "support")
MAP_LABELS = {"normal": "Normal", "long": "Waiting 60+ days", "hazard": "Safety issue open"}
Observation = dict[str, bool | int]
Admission = Callable[[], None]


class AdmissionLost(Exception):
    """A fresh identity/origin check refused the next observer action."""


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


def chat(page: Page, admit: Admission) -> Observation:
    admit()
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
    admit()
    skill.select_option(selected)
    previous = panel.locator(".chat-widget-assistant").count()
    admit()
    panel.locator("textarea").fill(
        "What can this advisory skill help me do? Do not include resident or case details."
    )
    admit()
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
    admit()
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
    admit()
    page.keyboard.press("Escape")
    return result


def map_projection(payload: object) -> dict[str, object] | None:
    if not isinstance(payload, dict):
        return None
    mode, total, shown, items = (payload.get(key) for key in ("mode", "total", "shown", "items"))
    if (
        mode not in ("points", "clusters")
        or type(total) is not int
        or total < 0
        or type(shown) is not int
        or not isinstance(items, list)
        or shown != len(items)
        or (mode == "points" and total != shown)
    ):
        return None

    def coordinate(value: object, limit: int) -> bool:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and -limit <= value <= limit
            and isfinite(value)
        )

    bounds = payload.get("bounds")
    if total == 0:
        if mode != "points" or bounds is not None:
            return None
    elif (
        not isinstance(bounds, list)
        or len(bounds) != 4
        or not all(
            coordinate(value, 90 if index % 2 == 0 else 180) for index, value in enumerate(bounds)
        )
        or bounds[0] > bounds[2]
        or bounds[1] > bounds[3]
    ):
        return None
    labels: list[str] = []
    links: list[str] = []
    marker_labels: list[str] = []
    counts = 0
    # Cluster centroids accumulate roundoff; original point coordinates do not.
    tolerance = 1e-9 if mode == "clusters" else 0
    for item in items:
        if (
            not isinstance(item, dict)
            or not coordinate(item.get("lat"), 90)
            or not coordinate(item.get("lon"), 180)
            or (
                bounds is not None
                and not (
                    bounds[0] - tolerance <= item["lat"] <= bounds[2] + tolerance
                    and bounds[1] - tolerance <= item["lon"] <= bounds[3] + tolerance
                )
            )
        ):
            return None
        if mode == "points":
            identifier, name, kind = (item.get(key) for key in ("id", "name", "kind"))
            if (
                not isinstance(identifier, str)
                or not identifier.strip()
                or not isinstance(name, str)
                or not name.strip()
                or not isinstance(kind, str)
                or kind not in MAP_LABELS
            ):
                return None
            label = f"{name}, {MAP_LABELS[kind]}"
            labels.append(label)
            links.append("#/case/" + quote(identifier, safe="~()*!.'-"))
            marker_labels.append(label)
        else:
            count, hazards, long = (item.get(key) for key in ("count", "hazards", "long"))
            if (
                type(count) is not int
                or count <= 0
                or type(hazards) is not int
                or not 0 <= hazards <= count
                or type(long) is not int
                or not 0 <= long <= count
            ):
                return None
            counts += count
            label = f"{count} homes, {hazards} with a safety issue open"
            labels.append(label)
            marker_labels.append(label + ". Zoom in to this area")
    if (mode == "clusters" and counts != total) or len(links) != len(set(links)):
        return None
    return {
        "labels": labels,
        "links": links,
        "markers": marker_labels,
        "status": (
            f"{total} homes in this view, grouped into {shown} areas. Zoom in to see each home."
            if mode == "clusters"
            else f"{total} {'home' if total == 1 else 'homes'} shown"
        ),
    }


MAP_RENDERED = """expected => {
  const panel = document.querySelector('.map-dialog[open] .map-panel');
  const map = panel?.querySelector('#leaflet');
  if (!map || map.getAttribute('aria-busy') === 'true'
      || panel.querySelector('[role=alert]')) return false;
  const list = [...panel.querySelectorAll('.maplist li')];
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  return panel.querySelector('.map-info [role=status]')?.textContent === expected.status
    && same(list.map(e => e.textContent), expected.labels)
    && same(list.flatMap(e => [...e.querySelectorAll('a')].map(a => a.getAttribute('href'))),
            expected.links)
    && same([...map.querySelectorAll('.leaflet-marker-icon')].map(e => e.title).sort(),
            [...expected.markers].sort());
}"""


def map_filters(page: Page, admit: Admission) -> Observation:
    admit()
    page.evaluate("location.hash = '#/overview'")
    admit()
    page.locator(".overview-map-filters").wait_for(state="visible", timeout=MAP_TIMEOUT)
    admit()
    page.get_by_role("button", name="Expand map", exact=True).press("Enter")
    admit()
    buttons = page.locator(".map-dialog[open] .overview-map-filters button[aria-pressed]")
    candidates = [
        index
        for index in range(buttons.count())
        if buttons.nth(index).get_attribute("aria-pressed") == "false"
    ]
    if not candidates:
        return {"passed": False}
    index = candidates[0]
    if index >= len(MAP_FLAGS):
        return {"passed": False}
    button = buttons.nth(index)
    area = page.locator("#mapArea").input_value()
    origin_url = page.url
    requests: list[Request] = []
    pending: set[Request] = set()
    responses: dict[Request, Response] = {}
    errors = 0
    active = False

    def requested(request: Request) -> None:
        query = parse_qs(urlsplit(request.url).query, keep_blank_values=True)
        if (
            active
            and urlsplit(request.url).path == "/api/map"
            and allowed_response(request.url, origin_url)
            and query.get("flag", [""]) == [MAP_FLAGS[index]]
            and query.get("area", [""]) == [area]
        ):
            requests.append(request)
            pending.add(request)

    def responded(response: Response) -> None:
        if response.request in pending:
            responses[response.request] = response

    def finished(request: Request) -> None:
        pending.discard(request)

    def failed(request: Request) -> None:
        nonlocal errors
        if request in pending:
            errors += 1
            pending.discard(request)

    def page_error(error: BrowserError) -> None:
        nonlocal errors
        errors += 1

    listeners = {
        "request": requested,
        "response": responded,
        "requestfinished": finished,
        "requestfailed": failed,
        "pageerror": page_error,
    }
    page.on("request", requested)
    page.on("response", responded)
    page.on("requestfinished", finished)
    page.on("requestfailed", failed)
    page.on("pageerror", page_error)
    try:
        admit()
        active = True
        button.press("Space")
        deadline = time.monotonic() + MAP_TIMEOUT / 1000
        while time.monotonic() < deadline:
            admit()
            generation = len(requests)
            # Fit rendering starts its viewport refresh in the same JS task.
            page.evaluate(
                "() => new Promise(resolve => requestAnimationFrame("
                "() => requestAnimationFrame(resolve)))"
            )
            admit()
            if errors or page.locator(".map-dialog[open] [role=alert]").count():
                return {"passed": False}
            if requests and not pending and generation == len(requests):
                projections = []
                for request in requests:
                    response = responses.get(request)
                    if response is None or response.status != 200:
                        return {"passed": False}
                    projection = map_projection(response.json())
                    if projection is None:
                        return {"passed": False}
                    projections.append(projection)
                if page.evaluate(MAP_RENDERED, projections[-1]):
                    admit()
                    passed = (
                        not errors
                        and not pending
                        and generation == len(requests)
                        and button.get_attribute("aria-pressed") == "true"
                        and button.locator(".tile-selection").inner_text() == "Selected"
                        and button.evaluate("e => document.activeElement === e")
                    )
                    if passed:
                        admit()
                        page.keyboard.press("Escape")
                    return {"passed": passed}
            page.wait_for_timeout(25)
        return {"passed": False}
    finally:
        for event, listener in listeners.items():
            page.remove_listener(event, listener)


def allowed_response(url: str, page_url: str) -> bool:
    response, current = urlsplit(url), urlsplit(page_url)
    return (response.scheme, response.netloc) == (current.scheme, current.netloc)


def case_view(page: Page, admit: Admission) -> Observation:
    admit()
    page.evaluate("location.hash = '#/all'")
    admit()
    link = page.locator('a.item[href^="#/case/"]').first
    link.wait_for(state="visible", timeout=120000)
    admit()
    link.click()
    admit()
    page.locator(".case-journey").wait_for(state="visible", timeout=120000)
    admit()
    return {
        "passed": page.locator(".step").count() > 0
        and page.locator("#app [role=alert]:visible").count() == 0
    }


OBSERVERS: dict[str, Callable[[Page, Admission], Observation]] = {
    "chat": chat,
    "map": map_filters,
    "case": case_view,
}


def verify_employee(page: Page, expected: Mapping[str, object], origin: str = APP) -> Acceptance:
    def admit() -> None:
        if probe(page, expected, origin)["authenticated"] is not True:
            raise AdmissionLost()

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
            values = observe(page, admit)
        except AdmissionLost:
            return result
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
            "test_employee_acceptance_check.AcceptanceTests.test_chromium_map_contract",
        ]
    )
    execution = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(
        not (execution.wasSuccessful() and execution.testsRun == 3 and not execution.skipped)
    )
