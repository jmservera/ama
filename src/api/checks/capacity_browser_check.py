"""Generated-demo capacity and manager navigation checks on owned local stores."""

import argparse
import fcntl
import importlib
import os
import secrets
import subprocess
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

from playwright.sync_api import expect, sync_playwright
from zava_forward.api import server
from zava_forward.core.sqlstore import SqlStore

generated = importlib.import_module("test_generated_dataset")


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


def check(store: Any) -> None:
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
                errors: list[str] = []
                failures: list[str] = []
                console_errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on(
                    "response",
                    lambda response: (
                        failures.append(f"{response.status} {response.url.removeprefix(base)}")
                        if response.status >= 400 and response.url.startswith(base + "/api/")
                        else None
                    ),
                )
                page.on(
                    "console",
                    lambda message: (
                        console_errors.append(message.text)
                        if message.type == "error"
                        and message.location.get("url", "").startswith(base)
                        else None
                    ),
                )
                page.goto(base + "/app")
                page.locator("#email").fill(manager["email"])
                page.locator("#pw").fill("synthetic-password")
                page.locator("button[type=submit]").click()
                expect(page.locator("#nav")).to_be_visible()
                me = context.request.get(base + "/api/me").json()
                for endpoint in ("packages", "workorders"):
                    response = context.request.get(base + "/api/" + endpoint)
                    assert response.status == 200, (endpoint, response.status)
                    rows = response.json()
                    assert rows, endpoint
                    print(f"/api/{endpoint}: 200, {len(rows)} rows", flush=True)

                def capacity() -> None:
                    page.goto(base + "/app#/capacity")
                    expect(
                        page.get_by_role("heading", name="Capacity and work orders", exact=True)
                    ).to_be_visible()

                capacity()
                expect(
                    page.get_by_role(
                        "heading", name="Synthetic year-one delivery (PKG-SYN-001)", exact=True
                    )
                ).to_be_visible()
                expect(page.get_by_text("WO-SYN-0001, version 1", exact=True)).to_be_visible()
                assert not errors, errors
                assert not failures, failures

                for destination in me["navigation"]:
                    errors.clear()
                    failures.clear()
                    console_errors.clear()
                    page.goto(base + "/app" + destination["href"])
                    expect(page.locator("#app h1").first).to_be_visible()
                    page.wait_for_load_state("networkidle")
                    assert page.locator("#app h1").first.inner_text() != "Workspace unavailable"
                    assert not errors, (destination, errors)
                    assert not failures, (destination, failures)
                    assert not console_errors, (destination, console_errors)
                    print(f"Manager route {destination['href']}: PASS", flush=True)

                for endpoint, label in (("packages", "packages"), ("workorders", "work orders")):
                    pattern = base + "/api/" + endpoint
                    page.route(pattern, lambda route: route.fulfill(status=503, body="Unavailable"))
                    page.goto(base + "/app#/capacity")
                    expect(page.get_by_role("alert")).to_contain_text(
                        f"We could not load {label}. Try again."
                    )
                    expect(page.get_by_role("alert")).not_to_contain_text("Something went wrong")
                    page.unroute(pattern)
                    page.get_by_role("button", name="Try again", exact=True).click()
                    expect(
                        page.get_by_role("heading", name="Capacity and work orders", exact=True)
                    ).to_be_visible()

                pattern = base + "/api/workorders"
                page.route(pattern, lambda route: route.abort("failed"))
                page.goto(base + "/app#/capacity")
                expect(page.get_by_role("alert")).to_contain_text(
                    "We could not load work orders. Try again."
                )
                expect(page.get_by_role("alert")).not_to_contain_text("Failed to fetch")
                page.unroute(pattern)
                page.route(
                    pattern,
                    lambda route: route.fulfill(
                        status=403, json={"error": "Ask the contract manager to review access."}
                    ),
                )
                page.reload()
                expect(page.get_by_role("alert")).to_contain_text(
                    "Ask the contract manager to review access."
                )
                page.unroute(pattern)

                held: list[Any] = []
                package_pattern = base + "/api/packages"
                page.route(package_pattern, lambda route: held.append(route))
                with page.expect_request(package_pattern):
                    page.goto(base + "/app#/capacity", wait_until="domcontentloaded")
                page.evaluate("location.hash = '#/time'")
                expect(page.locator("#app h1").first).to_be_visible()
                page.wait_for_load_state("networkidle")
                for route in held:
                    route.abort()
                page.unroute(package_pattern)
                expect(page.locator("#app")).not_to_contain_text("We could not load packages")
                expect(page.locator("#app h1").first).not_to_have_text("Workspace unavailable")

                with store.lock:
                    store.data["procurement"] = dict(packages=[], work_orders=[])
                    store.save()
                capacity()
                expect(page.get_by_text("No packages yet.", exact=True)).to_be_visible()
                expect(page.get_by_text("No work orders yet.", exact=True)).to_be_visible()
                page.route(
                    pattern,
                    lambda route: route.fulfill(status=401, json={"error": "Session expired"}),
                )
                page.reload()
                expect(page.locator("#email")).to_be_visible()
                expect(page.locator("#app")).not_to_contain_text("We could not load work orders")
                assert not errors, errors
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
    args = parser.parse_args()
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
                check(store)


if __name__ == "__main__":
    main()
