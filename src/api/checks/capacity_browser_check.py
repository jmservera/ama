"""Generated-demo capacity and manager navigation checks on owned local stores."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib
import json
import os
import re
import secrets
import subprocess
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from zava_forward.core.sqlstore import SqlStore

from zava_forward.api import server

if TYPE_CHECKING:
    from playwright.sync_api import Page, Request, Response, Route

generated = importlib.import_module("test_generated_dataset")
fixtures = importlib.import_module("dataset")
AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"

MANAGER_ROUTES = {
    "#/": ("My cases today", ("/api/facets", "/api/cases?view=mine"), "#app .layout"),
    "#/all": ("All open cases", ("/api/facets", "/api/cases?view=all"), "#app .layout"),
    "#/overview": ("Overview", ("/api/stats", "/api/map"), "#mapArea"),
    "#/progress": ("Progress dashboard", ("/api/progress",), "#app .progress-facts"),
    "#/visits": ("Visits coming up", ("/api/visits?view=all",), "#app .list, #app p"),
    "#/funding": ("Funding applications", ("/api/funding",), "#app table"),
    "#/finance": ("Finance queue", ("/api/finance",), "#app table, #app p"),
    "#/capacity": (
        "Capacity and work orders",
        ("/api/packages", "/api/workorders"),
        "#app section[aria-label^='Appointment controls for']",
    ),
    "#/closed": ("Closed cases", ("/api/closed-cases",), "#app table"),
    "#/assistants": (
        "Role-owned assistant proposals",
        ("/api/assistants/proposals",),
        "#app button",
    ),
    "#/time": ("Staff time capture", ("/api/time/status",), "#app ul"),
    "#/screens": ("Specialist screens", (), "#app > a[href='#/']"),
}


def load_axe(path: Path) -> str:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Expected pinned axe-core 4.10.3")
    return raw.decode()


def scan_capacity(page: Page, axe: str | None, state: str) -> None:
    if axe is None:
        print(f"Capacity axe {state}: NOT RUN (--axe not supplied)", flush=True)
        return
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async () => await axe.run(document.querySelector('#app'), {
          runOnly: {type: 'tag', values: [
            'wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'
          ]}
        })"""
    )
    print(
        json.dumps(
            dict(state=state, violations=result["violations"], incomplete=result["incomplete"])
        ),
        flush=True,
    )
    assert not result["violations"], (state, result["violations"])


@contextmanager
def owned_store(seed: Path, mssql: bool) -> Any:
    if not mssql:
        store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
        try:
            yield store
        finally:
            store.db.close()
        return

    import mssql_python
    from zava_forward.core.mssqlstore import MssqlStore

    name = "ama-capacity523-" + uuid.uuid4().hex[:12]
    password = "Aa1!" + secrets.token_urlsafe(24)
    started = False
    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--detach",
                "--name",
                name,
                "--label",
                "ama.issue=523",
                "--memory",
                "3g",
                "--cpus",
                "2",
                "-e",
                "ACCEPT_EULA",
                "-e",
                "MSSQL_SA_PASSWORD",
                "-p",
                "127.0.0.1::1433",
                "mcr.microsoft.com/mssql/server:2022-latest",
            ],
            env=dict(os.environ, ACCEPT_EULA="Y", MSSQL_SA_PASSWORD=password),
            check=True,
            stdout=subprocess.DEVNULL,
        )
        started = True
        port = (
            subprocess.check_output(["docker", "port", name, "1433/tcp"], text=True)
            .strip()
            .rsplit(":", 1)[1]
        )
        connection = (
            f"Server=tcp:127.0.0.1,{port};Database=master;UID=sa;PWD={password};"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )
        for _ in range(90):
            try:
                db = mssql_python.connect(connection, autocommit=True)
            except mssql_python.Error:
                time.sleep(2)
                continue
            try:
                db.cursor().execute("CREATE DATABASE capacity523")
            finally:
                db.close()
            break
        else:
            raise RuntimeError("Owned local SQL Server did not become ready.")
        settings = dict(
            ZF_SQL_SERVER="127.0.0.1",
            ZF_SQL_PORT=port,
            ZF_SQL_DATABASE="capacity523",
            ZF_SQL_AUTH="password",
            ZF_SQL_USER="sa",
            ZF_SQL_PASSWORD=password,
            ZF_SQL_TRUST_CERT="1",
        )
        with patch.dict(os.environ, settings):
            store = MssqlStore(str(seed), state_dir=str(seed.parent))
            print(f"Owned SQL Server: {name}, loopback port {port}", flush=True)
            try:
                yield store
            finally:
                store.db.close()
    finally:
        if started:
            subprocess.run(["docker", "rm", "--force", name], check=True, stdout=subprocess.DEVNULL)


def check(store: Any, axe: str | None = None) -> None:
    from playwright.sync_api import expect, sync_playwright

    manager = next(
        user for user in store.staff.values() if user["role"] == "Retrofit Programme Manager"
    )
    app_factory: Any = server.App
    handler_factory: Any = server.make_handler
    app = app_factory(store, "synthetic-password")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler_factory(app))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{httpd.server_port}"
    try:
        with sync_playwright() as playwright:
            expect.set_options(timeout=60000)
            browser = playwright.chromium.launch()
            try:
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900}, reduced_motion="reduce"
                )
                context.route(
                    "**/*",
                    lambda route: (
                        route.continue_()
                        if route.request.url.startswith(base + "/")
                        else route.abort()
                    ),
                )
                page = context.new_page()
                page.goto(base + "/app")
                expect(page.locator("#email")).to_be_visible()
                errors: list[str] = []
                failures: list[str] = []
                console_errors: list[str] = []
                reads: list[Response] = []
                posts: list[Response] = []
                expected_failures: set[Request] = set()
                cancelled_requests: set[Request] = set()
                origins: dict[Request, str] = {}
                held: list[Route] = []
                scenario = "sign-in"

                def paged(endpoint: str) -> re.Pattern[str]:
                    return re.compile(
                        re.escape(f"{base}/api/{endpoint}") + r"\?limit=\d+&offset=\d+$"
                    )

                def inject(route: Route, *, status: int | None = 503) -> None:
                    expected_failures.add(route.request)
                    if status is None:
                        held.append(route)
                    elif status == 0:
                        route.abort("failed")
                    elif status == 503:
                        route.fulfill(status=503, body="Unavailable")
                    else:
                        route.fulfill(
                            status=status,
                            json={
                                "error": (
                                    "Ask the contract manager to review access."
                                    if status == 403
                                    else "Session expired"
                                )
                            },
                        )

                page.on("request", lambda request: origins.update({request: scenario}))
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on(
                    "response",
                    lambda response: (
                        reads.append(response)
                        if response.url.startswith(base + "/api/")
                        and response.request.method == "GET"
                        and response.status == 200
                        else None
                    ),
                )
                page.on(
                    "response",
                    lambda response: (
                        posts.append(response)
                        if response.url.startswith(base + "/api/")
                        and response.request.method == "POST"
                        else None
                    ),
                )
                page.on(
                    "response",
                    lambda response: (
                        failures.append(
                            f"{origins[response.request]}: "
                            f"{response.status} {response.url.removeprefix(base)}"
                        )
                        if response.url.startswith(base + "/api/")
                        and response.status >= 400
                        and response.request not in expected_failures
                        else None
                    ),
                )
                page.on(
                    "requestfailed",
                    lambda request: (
                        failures.append(
                            f"{origins[request]}: {request.failure} "
                            f"{request.url.removeprefix(base)}"
                        )
                        if request.url.startswith(base + "/api/")
                        and request not in expected_failures
                        and not (
                            request in cancelled_requests and request.failure == "net::ERR_ABORTED"
                        )
                        else None
                    ),
                )
                page.on(
                    "console",
                    lambda message: (
                        console_errors.append(message.text)
                        if message.type == "error"
                        and message.location.get("url", "").startswith(base)
                        and not any(
                            request.url == message.location.get("url")
                            for request in expected_failures
                        )
                        else None
                    ),
                )
                page.locator("#email").fill(manager["email"])
                page.locator("#pw").fill("synthetic-password")
                page.locator("button[type=submit]").click()
                expect(page.locator("#nav")).to_be_visible()
                me = context.request.get(base + "/api/me").json()
                page.wait_for_load_state("networkidle")
                assert not errors, errors
                assert not failures, failures
                assert not console_errors, console_errors

                def verify_route(href: str) -> None:
                    heading, endpoints, content = MANAGER_ROUTES[href]
                    expect(page.locator("#app h1")).to_have_text(heading)
                    page.wait_for_load_state("networkidle")
                    expect(page.locator(content).first).to_be_visible()
                    expect(page.locator("#app [role=alert]")).to_have_count(0)
                    expect(page.locator(f'#nav a[href="{href}"]')).to_have_attribute(
                        "aria-current", "page"
                    )
                    payloads: dict[str, Any] = {}
                    for endpoint in endpoints:
                        target = urlsplit(endpoint)
                        matching = [
                            response
                            for response in reads
                            if urlsplit(response.url).path == target.path
                            and all(
                                parse_qs(urlsplit(response.url).query).get(key) == value
                                for key, value in parse_qs(target.query).items()
                            )
                        ]
                        assert matching, (
                            href,
                            "Missing successful browser GET",
                            endpoint,
                            [response.url.removeprefix(base) for response in reads],
                        )
                        payloads[target.path] = matching[-1].json()
                    if href == "#/closed":
                        rows = payloads["/api/closed-cases"]["items"]
                        links = page.locator("#app tbody a")
                        expect(links).to_have_count(len(rows))
                        if rows:
                            expect(links.first).to_contain_text(rows[0]["resident"])
                        else:
                            expect(page.locator("#app tbody")).to_contain_text(
                                "No recorded data for this view."
                            )
                    elif href == "#/progress":
                        expect(page.locator("#app .progress-chart")).to_have_count(6)
                        expect(page.locator("#app")).to_contain_text("Demonstration data")
                    elif href in ("#/", "#/all"):
                        rows = payloads["/api/cases"]["items"]
                        links = page.locator("#app .list > li > a.item")
                        expect(links).to_have_count(len(rows))
                        if rows:
                            expect(links.first).to_contain_text(rows[0]["resident"])
                        else:
                            expect(page.locator("#app .empty")).to_be_visible()
                    elif href == "#/visits":
                        rows = payloads["/api/visits"]
                        expect(page.locator("#app .list > li")).to_have_count(len(rows))
                        if not rows:
                            expect(
                                page.get_by_text("No booked visits.", exact=True)
                            ).to_be_visible()
                    elif href in ("#/funding", "#/finance"):
                        rows = payloads["/api/funding" if href == "#/funding" else "/api/finance"]
                        expect(page.locator("#app tbody > tr")).to_have_count(
                            min(150, len(rows)) if href == "#/funding" else len(rows)
                        )
                        if href == "#/finance" and not rows:
                            expect(
                                page.get_by_text("Nothing is waiting.", exact=True)
                            ).to_be_visible()
                    elif href == "#/overview":
                        expect(
                            page.get_by_role("heading", name="Team workload", exact=True)
                        ).to_be_visible()
                    elif href == "#/assistants":
                        if not payloads["/api/assistants/proposals"]["proposals"]:
                            expect(
                                page.get_by_text(
                                    "No proposals in your current role and case scope. "
                                    "Use the ordinary case controls.",
                                    exact=True,
                                )
                            ).to_be_visible()
                    elif href == "#/time":
                        status = payloads["/api/time/status"]
                        expect(page.locator("#app [role=status]").first).to_have_text(
                            "Time capture is on." if status["enabled"] else status["reason"]
                        )
                    elif href == "#/screens":
                        expect(
                            page.get_by_role("link", name="Back to my work", exact=True)
                        ).to_be_visible()
                        if not page.locator("#app nav[aria-label='Specialist screens'] a").count():
                            expect(
                                page.get_by_text(
                                    "No specialist screens are installed for your role "
                                    "on this branch. Use your existing work list.",
                                    exact=True,
                                )
                            ).to_be_visible()
                    assert not errors, (href, errors)
                    assert not failures, (href, failures)
                    assert not console_errors, (href, console_errors)

                def capacity() -> None:
                    nonlocal scenario
                    scenario = "#/capacity"
                    reads.clear()
                    page.goto(base + f"/app?check={uuid.uuid4().hex}#/capacity")
                    verify_route("#/capacity")
                    packages = next(
                        response.json()["items"]
                        for response in reads
                        if urlsplit(response.url).path == "/api/packages"
                    )
                    orders = next(
                        response.json()["items"]
                        for response in reads
                        if urlsplit(response.url).path == "/api/workorders"
                    )
                    for package in packages:
                        expect(
                            page.get_by_role(
                                "heading", name=f"{package['name']} ({package['id']})", exact=True
                            )
                        ).to_be_visible()
                    rendered = (
                        page.locator("#app section")
                        .filter(has=page.get_by_role("heading", name="Work orders", exact=True))
                        .locator(":scope > ul > li > strong")
                    )
                    assert rendered.all_text_contents() == [
                        f"{order['id']}, version {order['version']}" for order in orders
                    ]
                    print(
                        f"Capacity browser GET/render: {len(packages)} packages, "
                        f"{len(orders)} work orders",
                        flush=True,
                    )

                capacity()
                scan_capacity(page, axe, "seeded capacity")
                expect(
                    page.get_by_role(
                        "heading", name="Synthetic year-one delivery (PKG-SYN-001)", exact=True
                    )
                ).to_be_visible()
                expect(page.get_by_text("WO-SYN-0001, version 1", exact=True)).to_be_visible()
                assert not errors, errors
                assert not failures, failures

                for destination in me["navigation"]:
                    href = destination["href"]
                    assert href in MANAGER_ROUTES, ("Unchecked manager route", href)
                    scenario = href
                    reads.clear()
                    page.goto(base + f"/app?check={uuid.uuid4().hex}" + href)
                    verify_route(href)
                    print(
                        f"Manager route {href}: PASS; heading={MANAGER_ROUTES[href][0]}; "
                        f"reads={MANAGER_ROUTES[href][1]}",
                        flush=True,
                    )

                for endpoint, label in (("packages", "packages"), ("workorders", "work orders")):
                    scenario = f"initial {endpoint} 503/retry"
                    pattern = paged(endpoint)
                    page.route(pattern, inject)
                    page.goto(base + f"/app?check={uuid.uuid4().hex}#/capacity")
                    expect(page.get_by_role("alert")).to_contain_text(
                        f"We could not load {label}. Try again."
                    )
                    expect(page.get_by_role("alert")).not_to_contain_text("Something went wrong")
                    page.wait_for_load_state("networkidle")
                    scan_capacity(page, axe, f"{endpoint} unavailable")
                    page.unroute(pattern)
                    reads.clear()
                    retry = page.get_by_role("button", name="Try again", exact=True)
                    retry.focus()
                    expect(retry).to_be_focused()
                    page.keyboard.press("Enter")
                    expect(
                        page.get_by_role("heading", name="Capacity and work orders", exact=True)
                    ).to_be_visible()
                    verify_route("#/capacity")

                scenario = "initial transport/403"
                pattern = paged("workorders")
                page.route(pattern, lambda route: inject(route, status=0))
                page.goto(base + f"/app?check={uuid.uuid4().hex}#/capacity")
                expect(page.get_by_role("alert")).to_contain_text(
                    "We could not load work orders. Try again."
                )
                expect(page.get_by_role("alert")).not_to_contain_text("Failed to fetch")
                page.unroute(pattern)
                page.route(pattern, lambda route: inject(route, status=403))
                page.reload()
                expect(page.get_by_role("alert")).to_contain_text(
                    "Ask the contract manager to review access."
                )
                page.unroute(pattern)

                scenario = "initial cancellation"
                reads.clear()
                package_pattern = paged("packages")
                page.route(package_pattern, lambda route: inject(route, status=None))
                with (
                    page.expect_request(package_pattern),
                    page.expect_request(paged("workorders")),
                ):
                    page.goto(
                        base + f"/app?check={uuid.uuid4().hex}#/capacity",
                        wait_until="domcontentloaded",
                    )
                cancelled_requests.update(
                    request
                    for request, origin in origins.items()
                    if origin == scenario
                    and urlsplit(request.url).path in ("/api/packages", "/api/workorders")
                )
                page.evaluate("location.hash = '#/time'")
                expect(page.locator("#app h1")).to_have_text("Staff time capture")
                page.wait_for_load_state("networkidle")
                for route in held:
                    route.abort()
                page.unroute(package_pattern)
                verify_route("#/time")
                expect(page.locator("#app")).not_to_contain_text("We could not load packages")

                order = context.request.get(base + "/api/workorders?limit=1&offset=0").json()[
                    "items"
                ][0]
                fixtures.supplied_contract_fixture(
                    store, order["package"], manager, order["contractor"]
                )
                for endpoint, label in (("packages", "packages"), ("workorders", "work orders")):
                    capacity()
                    scenario = f"draft-safe {endpoint} refresh/retry"
                    saved = page.locator(f'form[data-appointment-form="{order["id"]}-configure"]')
                    draft = page.locator(f'form[data-appointment-form="{order["id"]}-offer"]')
                    saved.locator("..").locator("summary").click()
                    saved.get_by_label(f"Threshold configuration evidence ({order['id']})").fill(
                        f"SYNTHETIC {endpoint} recovery regression"
                    )
                    draft.locator("..").locator("summary").click()
                    period = draft.get_by_label(f"Visit period ({order['id']})", exact=True)
                    period.fill("Unsaved morning visit")
                    paused = draft.get_by_label(f"Household paused ({order['id']})", exact=True)
                    paused.check()
                    before = draft.evaluate(
                        "(form) => ({context: form.appointmentContext, "
                        "event: form.elements[0].value})"
                    )
                    post_count = len(posts)
                    configurations = len(
                        store.data["procurement"].get("appointment_configurations", [])
                    )
                    pattern = paged(endpoint)
                    page.route(pattern, inject)
                    saved.get_by_role(
                        "button", name="Record provisional threshold", exact=True
                    ).click()
                    status = page.locator("#app > [role=status]")
                    expect(status).to_contain_text(f"We could not load {label}")
                    expect(saved).not_to_have_attribute("data-unsaved", "true")
                    expect(draft).to_have_attribute("data-unsaved", "true")
                    period.fill("Edited while refresh unavailable")
                    with page.expect_response(pattern) as retried:
                        status.get_by_role("button", name="Try again", exact=True).click()
                    assert retried.value.status == 503
                    expect(status.get_by_role("button", name="Try again")).to_be_enabled()
                    expect(period).to_have_value("Edited while refresh unavailable")
                    expect(paused).to_be_checked()
                    expect(draft.locator("..")).to_have_attribute("open", "")
                    page.unroute(pattern)
                    reads.clear()
                    old_form = draft.element_handle()
                    with (
                        page.expect_response(paged("packages")) as recovered_packages,
                        page.expect_response(paged("workorders")) as recovered_orders,
                    ):
                        status.get_by_role("button", name="Try again", exact=True).click()
                    assert recovered_packages.value.status == 200
                    assert recovered_orders.value.status == 200
                    expect(status).to_be_empty()
                    page.wait_for_function("(form) => !form.isConnected", arg=old_form)
                    verify_route("#/capacity")
                    expect(period).to_have_value("Edited while refresh unavailable")
                    expect(paused).to_be_checked()
                    expect(draft).to_have_attribute("data-unsaved", "true")
                    expect(draft.locator("..")).to_have_attribute("open", "")
                    assert (
                        draft.evaluate(
                            "(form) => ({context: form.appointmentContext, "
                            "event: form.elements[0].value})"
                        )
                        == before
                    )
                    expect(saved).not_to_have_attribute("data-unsaved", "true")
                    assert len(posts) == post_count + 1, posts[post_count:]
                    assert posts[-1].status == 200
                    assert (
                        len(store.data["procurement"]["appointment_configurations"])
                        == configurations + 1
                    )
                    print(f"{scenario}: PASS; one real POST, saved clean, other draft retained")
                    page.once("dialog", lambda dialog: dialog.accept())
                    page.locator('#nav a[href="#/time"]').click()
                    expect(page.locator("#app h1")).to_have_text("Staff time capture")

                for endpoint in ("packages", "workorders"):
                    capacity()
                    scenario = f"delayed sibling 401 after {endpoint} refresh failure"
                    payloads = {
                        response.url: response.json()
                        for response in reads
                        if urlsplit(response.url).path in ("/api/packages", "/api/workorders")
                    }
                    saved = page.locator(f'form[data-appointment-form="{order["id"]}-configure"]')
                    saved.locator("..").locator("summary").click()
                    saved.get_by_label(f"Threshold configuration evidence ({order['id']})").fill(
                        f"SYNTHETIC delayed sibling 401 after {endpoint}"
                    )
                    post_count = len(posts)
                    configurations = len(store.data["procurement"]["appointment_configurations"])
                    held.clear()
                    page.evaluate("window.capacityHeldReads = 0")

                    def hold_capacity_read(route: Route) -> None:
                        inject(route, status=None)
                        page.evaluate("window.capacityHeldReads += 1")

                    order_pattern = paged("workorders")
                    page.route(package_pattern, hold_capacity_read)
                    page.route(order_pattern, hold_capacity_read)
                    with (
                        page.expect_request(package_pattern),
                        page.expect_request(order_pattern),
                    ):
                        saved.get_by_role(
                            "button", name="Record provisional threshold", exact=True
                        ).click()
                    page.wait_for_function("() => window.capacityHeldReads === 2")
                    assert len(held) == 2, held
                    failed = next(
                        route
                        for route in held
                        if urlsplit(route.request.url).path == "/api/" + endpoint
                    )
                    sibling = next(route for route in held if route is not failed)
                    failed.fulfill(status=503, body="Unavailable")
                    status = page.locator("#app > [role=status]")
                    expect(status).to_contain_text(
                        "We could not load "
                        + ("work orders" if endpoint == "workorders" else endpoint)
                    )
                    retry = status.get_by_role("button", name="Try again", exact=True)
                    retry_button = retry.element_handle()
                    assert retry_button is not None
                    held.clear()
                    page.evaluate("window.capacityHeldReads = 0")
                    with (
                        page.expect_request(package_pattern),
                        page.expect_request(order_pattern),
                    ):
                        retry.click()
                    page.wait_for_function("() => window.capacityHeldReads === 2")
                    assert len(held) == 2, held
                    assert retry_button.evaluate(
                        "(button) => button.disabled && button.getAttribute('aria-busy') === 'true'"
                    )
                    sibling.fulfill(status=401, json={"error": "Session expired"})
                    expect(page.locator("#app h1")).to_have_text("Sign in")
                    expect(page.get_by_role("alert")).to_have_text(
                        "Your session has ended. Sign in again."
                    )
                    expect(page.locator("#app")).to_be_focused()
                    for route in held:
                        route.fulfill(status=200, json=payloads[route.request.url])
                    page.wait_for_function(
                        "(button) => !button.disabled && !button.hasAttribute('aria-busy')",
                        arg=retry_button,
                    )
                    print(f"{scenario}: retry continuation settled", flush=True)
                    expect(page.locator("#app h1")).to_have_text("Sign in")
                    expect(page.locator("#email")).to_be_visible()
                    expect(page.get_by_role("alert")).to_have_text(
                        "Your session has ended. Sign in again."
                    )
                    expect(
                        page.get_by_role("heading", name="Capacity and work orders", exact=True)
                    ).to_have_count(0)
                    expect(page.get_by_role("button", name="Try again")).to_have_count(0)
                    expect(page.locator("#app")).to_be_focused()
                    assert len(posts) == post_count + 1
                    assert posts[-1].status == 200
                    assert (
                        len(store.data["procurement"]["appointment_configurations"])
                        == configurations + 1
                    )
                    assert not errors, errors
                    assert not failures, failures
                    assert not console_errors, console_errors
                    page.unroute(package_pattern)
                    page.unroute(order_pattern)
                    print(f"{scenario}: PASS; sign-in retained, one persisted POST", flush=True)
                    page.locator("#email").fill(manager["email"])
                    page.locator("#pw").fill("synthetic-password")
                    page.locator("button[type=submit]").click()
                    expect(page.locator("#nav")).to_be_visible()
                    page.wait_for_load_state("networkidle")

                for recovery in ("cancel", "401"):
                    capacity()
                    scenario = f"mutation-refresh {recovery}"
                    saved = page.locator(f'form[data-appointment-form="{order["id"]}-configure"]')
                    saved.locator("..").locator("summary").click()
                    saved.get_by_label(f"Threshold configuration evidence ({order['id']})").fill(
                        f"SYNTHETIC recovery {recovery}"
                    )
                    post_count = len(posts)
                    held.clear()
                    page.route(package_pattern, lambda route: inject(route, status=None))
                    with (
                        page.expect_request(package_pattern),
                        page.expect_request(paged("workorders")),
                    ):
                        saved.get_by_role(
                            "button", name="Record provisional threshold", exact=True
                        ).click()
                    assert len(posts) == post_count + 1
                    if recovery == "cancel":
                        reads.clear()
                        departing_requests = set(origins)
                        cancelled_requests.update(
                            request
                            for request, origin in origins.items()
                            if origin == scenario
                            and urlsplit(request.url).path in ("/api/packages", "/api/workorders")
                        )
                        page.locator('#nav a[href="#/time"]').click()
                        expect(page.locator("#app h1")).to_have_text("Staff time capture")
                        for route in held:
                            route.abort()
                        page.unroute(package_pattern)
                        verify_route("#/time")
                        expect(page.locator("#workspace-status")).not_to_contain_text(
                            "could not load"
                        )
                        assert page.locator("#app").evaluate(
                            "(app) => app.contains(document.activeElement)"
                        )
                        assert not any(
                            urlsplit(request.url).path in ("/api/packages", "/api/workorders")
                            for request in set(origins) - departing_requests
                        )
                    else:
                        for route in held:
                            route.fulfill(status=401, json={"error": "Session expired"})
                        page.unroute(package_pattern)
                        expect(page.locator("#email")).to_be_visible()
                        expect(page.locator("#app h1")).to_have_text("Sign in")
                        expect(page.get_by_role("alert")).to_have_text(
                            "Your session has ended. Sign in again."
                        )
                        expect(page.get_by_role("button", name="Try again")).to_have_count(0)
                        expect(page.locator("#app")).to_be_focused()
                        page.wait_for_load_state("networkidle")
                    assert len(posts) == post_count + 1
                    assert not errors, errors
                    assert not failures, failures
                    assert not console_errors, console_errors
                    print(f"{scenario}: PASS; no stale render or mutation replay", flush=True)

                page.locator("#email").fill(manager["email"])
                page.locator("#pw").fill("synthetic-password")
                page.locator("button[type=submit]").click()
                expect(page.locator("#nav")).to_be_visible()
                page.wait_for_load_state("networkidle")

                with store.lock:
                    store.data["procurement"] = dict(packages=[], work_orders=[])
                    store.save()
                scenario = "empty capacity"
                page.goto(base + f"/app?check={uuid.uuid4().hex}#/capacity")
                expect(page.locator("#app h1")).to_have_text("Capacity and work orders")
                page.wait_for_load_state("networkidle")
                expect(page.get_by_text("No packages yet.", exact=True)).to_be_visible()
                expect(page.get_by_text("No work orders yet.", exact=True)).to_be_visible()
                scan_capacity(page, axe, "empty capacity")
                page.route(pattern, lambda route: inject(route, status=401))
                page.reload()
                expect(page.locator("#email")).to_be_visible()
                expect(page.locator("#app")).not_to_contain_text("We could not load work orders")
                assert not errors, errors
                assert not failures, failures
                assert not console_errors, console_errors
                print("Capacity seeded/empty, failures/retry, transport, 403, abort, 401: PASS")
            finally:
                browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mssql", action="store_true", help="Create an owned local SQL container")
    parser.add_argument("--axe", type=Path, help="Pinned axe-core 4.10.3 asset for capacity scans")
    args = parser.parse_args()
    axe = load_axe(args.axe) if args.axe is not None else None
    safe_env = {
        key: os.environ[key]
        for key in ("PATH", "HOME", "TMPDIR", "LANG", "LD_LIBRARY_PATH")
        if key in os.environ
    }
    with (
        patch.dict(os.environ, safe_env, clear=True),
        Path("/tmp/ama-rpi-heavy.lock").open("a+") as lock,
    ):
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit(
                "BLOCKED: shared heavy lock busy; no browser or SQL started."
            ) from None
        with tempfile.TemporaryDirectory(prefix="ama-capacity523-") as directory:
            seed = Path(directory) / "synthetic.json"
            argv = ["builder", "--seed", "20260901", "--as-of", "2026-10-13", "--out", str(seed)]
            with patch.object(
                generated.builder, "load_register", return_value=generated.register()
            ):
                with patch("sys.argv", argv):
                    generated.builder.main()
            with owned_store(seed, args.mssql) as store:
                check(store, axe)


if __name__ == "__main__":
    main()
