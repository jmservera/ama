"""Run the real resident showcase server against a loopback SQL Server and drive it in Chromium.

Run from src/api with the src packages and Playwright/Chromium installed, and with a throwaway
loopback SQL Server whose sa password is in ZF_SQL_PASSWORD (port in ZF_SQL_PORT):
ZF_SQL_PORT=... ZF_SQL_PASSWORD=... python -m checks.resident_demo_browser_check

It creates and drops its own database, uses a fake test password only and never reaches Azure.
The server runs with the real SQL view, the real HTTP app and the real __Host- cookies on the
loopback origin, so a browser that refused those cookies would fail this check.
"""

from __future__ import annotations

import base64
import os
import socket
import subprocess
import sys
import time
import urllib.request
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright
from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_sql as rsql
from zava_forward.core.mssqlstore import TABLES

FAKE_PASSWORD = "FAKE-TEST-FIXTURE-ONLY-not-a-real-demo-password"
RESIDENTS = {
    "alice.demo@example.com": ("1 Alder Close", "Loft insulation"),
    "bob.demo@example.com": ("2 Birch Close", "Cavity wall insulation"),
}
ROOT = Path(__file__).resolve().parents[3]
USER = "zf_showcase_user"


def check(name: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(name)
    print(f"PASS {name}", flush=True)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def sql_settings(database: str) -> dict[str, str]:
    return {
        "server": "127.0.0.1",
        "port": os.environ["ZF_SQL_PORT"],
        "database": database,
        "auth": "password",
        "user": "sa",
        "password": os.environ["ZF_SQL_PASSWORD"],
        "trust_cert": "1",
    }


def run_sql(database: str, statement: str, *params: Any) -> None:
    conn = rsql.connector(sql_settings(database))()
    try:
        conn.cursor().execute(statement, params) if params else conn.cursor().execute(statement)
    finally:
        conn.close()


@contextmanager
def database() -> Iterator[str]:
    name = "demo462_" + uuid.uuid4().hex[:8]
    run_sql("master", f"CREATE DATABASE [{name}] COLLATE Latin1_General_100_BIN2")
    try:
        run_sql(name, TABLES["cases"])
        run_sql(name, f"CREATE USER [{USER}] WITHOUT LOGIN")
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "applier", ROOT / "infra" / "scripts" / "resident_showcase_sql.py"
        )
        applier = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(applier)  # type: ignore[union-attr]
        for batch in applier.render(USER):
            run_sql(name, batch)
        for n, (email, (address, measure)) in enumerate(RESIDENTS.items(), start=1):
            body = (
                '{"resident":{"email":"%s"},"home":{"address":"%s","town":"Demotown",'
                '"postcode":"DE1 1MO"},"measures":["%s"]}' % (email, address, measure)
            )
            run_sql(
                name,
                "INSERT INTO cases (id, seq, stage, area, wave, owner_code, closed, hazard,"
                " postcode, address, body) VALUES (?, ?, 'Survey', 'A', 'W', 'O', 0, 0, 'P', 'A', ?)",
                f"SYN-{n}",
                n,
                body,
            )
            run_sql(
                name,
                "INSERT INTO resident_showcase.allowed_case (case_id, provenance, valid_from,"
                " valid_to, revoked) VALUES (?, 'browser-check synthetic fixture', ?, ?, 0)",
                f"SYN-{n}",
                (datetime.now(UTC) - timedelta(days=1)).replace(tzinfo=None),
                rs.AUTHORITY_END.replace(tzinfo=None),
            )
        yield name
    finally:
        conn = rsql.connector(sql_settings("master"))()
        cur = conn.cursor()
        cur.execute(f"ALTER DATABASE [{name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
        cur.execute(f"DROP DATABASE [{name}]")
        conn.close()


@contextmanager
def showcase(db: str) -> Iterator[str]:
    port = free_port()
    expires = min(datetime.now(UTC) + timedelta(hours=1), rs.AUTHORITY_END)
    settings = sql_settings(db)
    env = {k: v for k, v in os.environ.items() if k in ("PATH", "HOME", "LANG")}
    env.update(
        ZF_DEMO_EXPIRES_AT=expires.isoformat(),
        ZF_DEMO_ALLOWED_HOSTS="127.0.0.1",
        ZF_DEMO_PASSWORD_VERIFIER=rs.make_verifier(FAKE_PASSWORD, n=2**14),
        ZF_DEMO_SESSION_KEY=base64.urlsafe_b64encode(os.urandom(32)).decode(),
        ZF_DEMO_BIND="127.0.0.1",
        PORT=str(port),
        ZF_SQL_SERVER=settings["server"],
        ZF_SQL_DATABASE=db,
        ZF_SQL_AUTH="password",
        ZF_SQL_USER=settings["user"],
        ZF_SQL_PASSWORD=settings["password"],
        ZF_SQL_PORT=settings["port"],
        ZF_SQL_TRUST_CERT="1",
    )
    proc = subprocess.Popen(
        [sys.executable, "-m", "zava_forward.api.resident_demo"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(150):
            try:
                urllib.request.urlopen(base + "/healthz", timeout=1).read()
                break
            except OSError:
                if proc.poll() is not None:
                    raise AssertionError(
                        "showcase exited: " + (proc.stdout.read() if proc.stdout else "")
                    )
                time.sleep(0.2)
        else:
            raise AssertionError("showcase did not become ready")
        yield base
    finally:
        proc.terminate()
        proc.wait(10)


def new_page(browser: Any, width: int = 1024, height: int = 800) -> tuple[Any, Page, list[str]]:
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    errors: list[str] = []
    page.on(
        "console",
        lambda m: errors.append(m.text) if m.type == "error" and "401" not in m.text else None,
    )
    page.on("pageerror", lambda e: errors.append(str(e)))
    return context, page, errors


def sign_in_by_keyboard(page: Page, email: str, password: str) -> None:
    page.click("#email")
    page.keyboard.type(email)
    page.keyboard.press("Tab")
    page.keyboard.type(password)
    page.keyboard.press("Enter")


def main() -> None:
    with database() as db, showcase(db) as base, sync_playwright() as pw:
        browser = pw.chromium.launch()
        check_unauthenticated(browser, base)
        check_sign_in_and_cookies(browser, base)
        check_failure_and_forgery(browser, base)
        check_cross_case_and_logout(browser, base)
        check_mobile(browser, base)
        browser.close()
    print("resident demo browser check complete", flush=True)


def check_unauthenticated(browser: Any, base: str) -> None:
    context, page, errors = new_page(browser)
    page.goto(base + "/")
    page.wait_for_selector("#signin:not([hidden])")
    text = page.inner_text("body")
    check(
        "synthetic banner and shared-sign-in warning visible",
        "Synthetic showcase - not a live resident service" in text
        and "not proof of who you are" in text,
    )
    check(
        "no resident data before sign in", "Alder Close" not in text and "Birch Close" not in text
    )
    check("title says synthetic", "synthetic showcase" in page.title().lower())
    check("one h1", page.locator("h1").count() == 1)
    check(
        "email and password are labelled",
        page.get_by_label("Email address").count() == 1
        and page.get_by_label("Password").count() == 1,
    )
    page.keyboard.press("Tab")
    check(
        "skip link is first focus stop", page.evaluate("document.activeElement.className") == "skip"
    )
    status, _ = context.request.get(base + "/demo/view").status, None
    check("view is 401 without a session", status == 401)
    check("no script errors", not errors)
    context.close()


def check_sign_in_and_cookies(browser: Any, base: str) -> None:
    context, page, errors = new_page(browser)
    page.goto(base + "/")
    page.wait_for_selector("#signin:not([hidden])")
    check("email is not auto-focused", page.evaluate("document.activeElement.id") != "email")
    sign_in_by_keyboard(page, "  Alice.Demo@Example.COM ", FAKE_PASSWORD)
    page.wait_for_selector("#content:not([hidden])")
    text = page.inner_text("body")
    check(
        "keyboard-only sign in shows own home",
        "1 Alder Close" in text and "Loft insulation" in text,
    )
    check("other resident is not shown", "Birch Close" not in text and "bob.demo" not in text)
    check("password field is cleared", page.input_value("#password") == "")
    cookies = {c["name"]: c for c in context.cookies()}
    check(
        "session and CSRF cookies are stored by the browser",
        "__Host-zfdemo" in cookies and "__Host-zfdemo-csrf" in cookies,
    )
    session = cookies["__Host-zfdemo"]
    check(
        "session cookie is HttpOnly, Secure and SameSite=Strict",
        session["httpOnly"] and session["secure"] and session["sameSite"] == "Strict",
    )
    check(
        "session cookie is not readable by script",
        "__Host-zfdemo=" not in page.evaluate("document.cookie"),
    )
    check(
        "cookies are returned on the next request",
        context.request.get(base + "/demo/view").status == 200,
    )
    check("unavailable actions are disabled buttons", page.locator("button[disabled]").count() >= 1)
    check("sign out is reachable", page.locator("#signout").is_visible())
    check("no script errors", not errors)
    context.close()


def check_failure_and_forgery(browser: Any, base: str) -> None:
    context, page, _ = new_page(browser)
    page.goto(base + "/")
    page.wait_for_selector("#signin:not([hidden])")
    sign_in_by_keyboard(page, "alice.demo@example.com", "wrong")
    page.wait_for_selector("#signin-error:not([hidden])")
    check(
        "failed sign in shows one generic alert",
        "could not sign you in" in page.inner_text("#signin-error"),
    )
    check(
        "failed sign in moves focus to the alert",
        page.evaluate("document.activeElement.id") == "signin-error",
    )
    check("no resident data after failure", "Alder Close" not in page.inner_text("body"))
    sign_in_by_keyboard(page, "nobody@example.com", FAKE_PASSWORD)
    for _ in range(50):
        if page.evaluate("document.activeElement.id") == "signin-error":
            break
        page.wait_for_timeout(100)
    check(
        "unknown email gives the same message",
        "could not sign you in" in page.inner_text("#signin-error"),
    )
    forged = browser.new_context()
    for value in ("forged", "v1.a.b.c.d", "A" * 100):
        r = forged.request.get(base + "/demo/view", headers={"Cookie": f"__Host-zfdemo={value}"})
        check(f"forged session {value[:6]} is 401", r.status == 401)
    forged.close()
    context.close()


def check_cross_case_and_logout(browser: Any, base: str) -> None:
    ctx_a, page_a, _ = new_page(browser)
    page_a.goto(base + "/")
    page_a.wait_for_selector("#signin:not([hidden])")
    sign_in_by_keyboard(page_a, "alice.demo@example.com", FAKE_PASSWORD)
    page_a.wait_for_selector("#content:not([hidden])")
    token_a = {c["name"]: c for c in ctx_a.cookies()}["__Host-zfdemo"]["value"]
    ctx_b, page_b, _ = new_page(browser)
    page_b.goto(base + "/")
    page_b.wait_for_selector("#signin:not([hidden])")
    sign_in_by_keyboard(page_b, "bob.demo@example.com", FAKE_PASSWORD)
    page_b.wait_for_selector("#content:not([hidden])")
    token_b = {c["name"]: c for c in ctx_b.cookies()}["__Host-zfdemo"]["value"]
    check(
        "each resident sees only their own home",
        "2 Birch Close" in page_b.inner_text("body")
        and "1 Alder Close" not in page_b.inner_text("body"),
    )
    pa, pb = token_a.split("."), token_b.split(".")
    pa[1] = pb[1]
    cross = browser.new_context()
    check(
        "session with another case's handle is denied",
        cross.request.get(
            base + "/demo/view", headers={"Cookie": "__Host-zfdemo=" + ".".join(pa)}
        ).status
        == 401,
    )
    cross.close()
    page_a.click("#signout")
    page_a.wait_for_selector("#signin:not([hidden])")
    check(
        "sign out returns to the sign-in form with no data",
        "Alder Close" not in page_a.inner_text("body"),
    )
    check("session cookie is cleared", "__Host-zfdemo" not in {c["name"] for c in ctx_a.cookies()})
    replay = browser.new_context()
    check(
        "signed-out token cannot be replayed",
        replay.request.get(
            base + "/demo/view", headers={"Cookie": "__Host-zfdemo=" + token_a}
        ).status
        == 401,
    )
    check(
        "other resident session is unaffected", ctx_b.request.get(base + "/demo/view").status == 200
    )
    replay.close()
    ctx_a.close()
    ctx_b.close()


def check_mobile(browser: Any, base: str) -> None:
    context, page, _ = new_page(browser, 360, 640)
    page.goto(base + "/")
    page.wait_for_selector("#signin:not([hidden])")
    check(
        "sign-in has no horizontal scroll at 360px",
        page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"),
    )
    sign_in_by_keyboard(page, "alice.demo@example.com", FAKE_PASSWORD)
    page.wait_for_selector("#content:not([hidden])")
    check(
        "signed-in page has no horizontal scroll at 360px",
        page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"),
    )
    context.close()


if __name__ == "__main__":
    main()
