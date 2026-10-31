"""Sole bounded live executor; emits no credentials, identity claims or case text."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode, urlsplit

from playwright.sync_api import Error as BrowserError
from playwright.sync_api import Page, Response, sync_playwright

from checks.employee_acceptance_check import APP, probe, valid_expected, verify_employee
from checks.resident_assistant_browser_check import open_chat

RESIDENT = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "src/api/src/zava_forward/api/web"
RESIDENT_WEB = ROOT / "src/api/src/zava_forward/api/resident_demo/web"
RESULT = Path(__file__).with_name("live-azure-verification-results.json")
TASK = "3a44be57-db3a-46d1-b9e4-fe82bd7c74e7"
ERRORS = (BrowserError, OSError, ValueError, AssertionError, subprocess.TimeoutExpired)


def utc() -> str:
    return datetime.now(UTC).isoformat()


def may_start(record: dict) -> bool:
    return record.get("task_id") == TASK and record.get("execution") == "prepared"


def may_submit(record: dict, slot: str) -> bool:
    count = record.get("attempts", {}).get(slot)
    return record.get("execution") == "running" and type(count) is int and 0 <= count < 2


def save(handle, record: dict) -> None:
    handle.seek(0)
    json.dump(record, handle, indent=2, sort_keys=True, allow_nan=False)
    handle.write("\n")
    handle.truncate()
    handle.flush()
    os.fsync(handle.fileno())


def consume(handle, record: dict, slot: str) -> None:
    if not may_submit(record, slot):
        raise ValueError("Attempt admission refused")
    record["attempts"][slot] += 1
    save(handle, record)


def credentials(slot: str) -> tuple[str, str]:
    name = ".ama-test-user" if slot == "employee" else ".ama-resident-test-user"
    text = (Path.home() / name).read_text().strip()
    values = {}
    if text.startswith("{"):
        values = json.loads(text)
        if not isinstance(values, dict):
            raise ValueError("Credential format refused")
    else:
        for line in text.splitlines():
            match = re.match(r"^\s*([\w -]+)\s*[:=]\s*(.*?)\s*$", line)
            if match:
                values[match[1].lower().strip().replace(" ", "_")] = match[2].strip("'\"")
        if not values:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if len(lines) == 2:
                return lines[0], lines[1]
            if len(lines) == 1:
                fields = lines[0].split(maxsplit=1)
                if len(fields) == 2 and "@" in fields[0]:
                    return fields[0], fields[1]
                if slot == "employee" and len(fields) == 1 and "@" not in text:
                    return "", text
    normalized = {str(key).lower(): value for key, value in values.items()}
    user = next(
        (value for key, value in normalized.items()
         if any(key.endswith(suffix) for suffix in ("username", "email", "user", "upn"))),
        None,
    )
    password = next(
        (value for key, value in normalized.items() if key.endswith("password")),
        None,
    )
    if not isinstance(user, str) or not user or not isinstance(password, str) or not password:
        raise ValueError("Credential format refused")
    return user, password


def directory_expectation(user: str) -> tuple[dict, dict]:
    result = {"status": "blocked", "reason": "independent_directory_attestation_unavailable"}
    account = subprocess.run(
        ["az", "account", "show", "--query", "tenantId", "-o", "json"],
        capture_output=True, text=True, timeout=60,
    )
    command = (
        ["az", "ad", "user", "show", "--id", user, "--query", "{oid:id,upn:userPrincipalName}", "-o", "json"]
        if user else
        ["az", "ad", "user", "list", "--filter", "startswith(displayName,'Aadi')",
         "--query", "[].{oid:id,upn:userPrincipalName}", "-o", "json"]
    )
    directory = subprocess.run(
        command,
        capture_output=True, text=True, timeout=90,
    )
    result["tenant_lookup_exit"] = account.returncode
    result["directory_lookup_exit"] = directory.returncode
    result["directory_access_denied"] = any(
        word in directory.stderr.lower() for word in ("insufficient privileges", "forbidden", "authorization")
    )
    if account.returncode or directory.returncode:
        return {}, result
    tid, identity = json.loads(account.stdout), json.loads(directory.stdout)
    if not user:
        if not isinstance(identity, list) or len(identity) != 1:
            result["reason"] = "directory_test_user_ambiguous"
            return {}, result
        identity = identity[0]
    expected = {"tid": tid, "oid": identity.get("oid"), "email": identity.get("upn")}
    same = isinstance(identity.get("upn"), str) and bool(identity["upn"]) and (
        not user or identity["upn"].lower() == user.lower())
    if not valid_expected(expected) or not same:
        result["reason"] = "directory_expectation_invalid_or_account_mismatch"
        return {}, result
    return expected, {"status": "passed", "provenance": "independent_az_directory_lookup"}


def watch(page: Page, origin: str) -> dict:
    evidence = {"assets": [], "request_failures": 0, "page_errors": 0}

    def response_seen(response: Response) -> None:
        parsed = urlsplit(response.url)
        if f"{parsed.scheme}://{parsed.netloc}" != origin:
            return
        path = parsed.path
        if not path.endswith((".js", ".css")):
            return
        item = {"path": path, "status": response.status, "observed_at": utc()}
        try:
            body = response.body()
            item.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
            candidate = (
                RESIDENT_WEB / path.lstrip("/")
                if origin == RESIDENT and path not in ("/chat-widget.js", "/chat-widget.css")
                else WEB / path.lstrip("/")
            )
            item["source_match"] = (
                candidate.is_file()
                and hashlib.sha256(candidate.read_bytes()).hexdigest() == item["sha256"]
            )
        except (BrowserError, OSError):
            item["body_unavailable"] = True
        evidence["assets"].append(item)

    def request_failed(request) -> None:
        if request.resource_type in ("script", "stylesheet"):
            evidence["request_failures"] += 1

    def page_error(error) -> None:
        evidence["page_errors"] += 1

    page.on("response", response_seen)
    page.on("requestfailed", request_failed)
    page.on("pageerror", page_error)
    return evidence


def health(context, origin: str) -> dict:
    observations = []
    for _ in range(3):
        started = time.monotonic()
        try:
            response = context.request.get(origin + "/healthz", timeout=120000)
            observations.append({"status": response.status, "elapsed_seconds": round(time.monotonic() - started, 3)})
            if response.status == 200:
                return {"status": "passed", "requests": observations}
        except BrowserError:
            observations.append({"transport_failed": True})
    return {"status": "failed", "requests": observations}


def tabs(page: Page) -> dict:
    controls = page.locator(".case-tabs [role=tab]")
    controls.first.wait_for(state="visible", timeout=120000)
    initial = page.locator(".case-tabs [role=tab][aria-selected=true]").count() == 1
    linked = []
    for index in range(controls.count()):
        control = controls.nth(index)
        control.click()
        identifier = control.get_attribute("aria-controls")
        linked.append(
            control.get_attribute("aria-selected") == "true"
            and bool(identifier)
            and page.locator(f"#{identifier}").is_visible()
            and page.locator('[role=tabpanel]:visible').count() == 1
        )
    return {"status": "passed" if initial and all(linked) else "failed",
            "initial_one_selected": initial, "count": len(linked), "switches_passed": sum(linked)}


def capacity(page: Page) -> dict:
    responses = {}

    def capture(response: Response) -> None:
        parsed = urlsplit(response.url)
        if parsed.netloc == urlsplit(APP).netloc and parsed.path in ("/api/packages", "/api/workorders"):
            responses[parsed.path] = response

    page.on("response", capture)
    try:
        page.evaluate("location.hash = '#/capacity'")
        page.get_by_role("heading", name="Capacity and work orders", exact=True).wait_for(timeout=120000)
        page.wait_for_timeout(1000)
        projected = {}
        for path in ("/api/packages", "/api/workorders"):
            response = responses.get(path)
            if response is None or response.status != 200:
                projected[path] = {"status": response.status if response else None}
                continue
            data = response.json()
            projected[path] = {"status": 200, "list_schema": isinstance(data, list)}
            if isinstance(data, list):
                projected[path]["count"] = len(data)
        package_count = projected.get("/api/packages", {}).get("count")
        order_count = projected.get("/api/workorders", {}).get("count")
        rendered_packages = page.locator('section .table-scroll[aria-label^="Capacity for "]').count()
        rendered_orders = page.locator('section[aria-label^="Appointment controls for"]').count()
        package_empty = page.locator("#app").get_by_text("No packages yet.", exact=True).count() > 0
        order_empty = page.locator("#app").get_by_text("No work orders yet.", exact=True).count() > 0
        agrees = (
            type(package_count) is int and type(order_count) is int
            and (package_count == rendered_packages if package_count else package_empty)
            and (order_count == rendered_orders if order_count else order_empty)
        )
        alerts = page.locator("#app [role=alert]:visible").count()
        return {"status": "passed" if agrees and not alerts else "failed",
                "api": projected, "render_agreement": agrees, "visible_alerts": alerts,
                "rendered_packages": rendered_packages, "rendered_orders": rendered_orders,
                "retry_offered": page.get_by_role("button", name="Try again", exact=True).count() > 0}
    finally:
        page.remove_listener("response", capture)


def metering(page: Page, as_of: str) -> dict:
    query = urlencode({"start": "2026-10-31T00:00:00Z", "end": as_of, "as_of": as_of})
    return page.evaluate(
        """async query => {
          const r = await fetch('/api/ai/report?' + query, {redirect:'error', signal:AbortSignal.timeout(120000)});
          const out = {http_status:r.status, status:r.ok ? 'observed' : 'failed'};
          if (!r.ok) return out;
          const data = await r.json(), c = data.consumption;
          out.consumption_present = !!c && typeof c === 'object' && !Array.isArray(c);
          if (!out.consumption_present) {out.status = 'unavailable'; return out;}
          out.fields = Object.keys(c).filter(k => /^[a-z_]+$/.test(k)).sort();
          out.coverage = ['unavailable','incomplete','complete','partial'].includes(c.coverage) ? c.coverage : 'other';
          out.token_cost_unknown = c.token_cost === 'Unknown';
          out.cost_per_accepted_unknown = c.cost_per_accepted_proposal === 'Unknown';
          out.status = out.coverage === 'unavailable' ? 'unavailable' : 'observed';
          return out;
        }""", query,
    )


def employee(browser, handle, record: dict) -> dict:
    out = {"origin": APP, "observed_at": utc()}
    record["apps"]["employee"] = out
    with browser.new_context(viewport={"width": 1280, "height": 900}) as context:
        out["health"] = health(context, APP)
        page = context.new_page()
        page.set_default_timeout(120000)
        out["first_navigation"] = watch(page, APP)
        page.goto(APP + "/app", wait_until="domcontentloaded", timeout=180000)
        out["stage"] = "credential_format"
        user, password = credentials("employee")
        out["stage"] = "independent_directory_attestation"
        expected, attestation = directory_expectation(user)
        out["independent_identity"] = attestation
        if not expected:
            out.update(acceptance={"status": "blocked", "reason": "independent_identity_unavailable"},
                       tabs={"status": "blocked"}, capacity={"status": "blocked"},
                       metering={"status": "blocked"}, other_manager_pages={"status": "blocked"})
            return out
        user = expected["email"]
        if urlsplit(page.url).hostname != "login.microsoftonline.com":
            page.goto(APP + "/.auth/login/aad?post_login_redirect_uri=/app", timeout=180000)
        if urlsplit(page.url).hostname != "login.microsoftonline.com":
            raise ValueError("Employee credential origin refused")
        consume(handle, record, "employee")
        page.locator('input[type=email]').fill(user)
        page.locator('input[type=submit]').click()
        page.locator('input[type=password]').wait_for(state="visible")
        if urlsplit(page.url).hostname != "login.microsoftonline.com":
            raise ValueError("Employee password origin refused")
        page.locator('input[type=password]').fill(password)
        page.locator('input[type=submit]').click()
        try:
            page.wait_for_url(APP + "/**", timeout=15000)
        except BrowserError:
            no = page.locator("#idBtn_Back")
            if no.is_visible() and urlsplit(page.url).hostname == "login.microsoftonline.com":
                no.click()
            page.wait_for_url(APP + "/**", timeout=120000)
        page.locator("#app .layout").wait_for(state="visible")
        out["acceptance"] = verify_employee(page, expected)
        admitted = probe(page, expected)["authenticated"]
        if admitted and out["acceptance"]["stages"]["case"]["status"] == "passed":
            out["tabs"] = tabs(page)
        else:
            out["tabs"] = {"status": "blocked"}
        if not admitted:
            out["capacity"] = out["metering"] = {"status": "blocked"}
            return out
        out["capacity"] = capacity(page)
        out["metering"] = metering(page, record["started_at"])
        out["other_manager_pages"] = {}
        for route, heading, selector in (
            ("overview", "Overview", "#mapArea"),
            ("progress", "Progress dashboard", "#app .progress-facts"),
            ("visits", "Visits coming up", "#app .list, #app p"),
            ("funding", "Funding applications", "#app table"),
            ("finance", "Finance queue", "#app table, #app p"),
            ("closed", "Closed cases", "#app table"),
        ):
            if not probe(page, expected)["authenticated"]:
                out["other_manager_pages"][route] = {"status": "blocked"}
                continue
            try:
                page.evaluate("route => {location.hash = '#/' + route;}", route)
                page.get_by_role("heading", name=heading, exact=True).wait_for()
                page.locator(selector).first.wait_for()
                alerts = page.locator("#app [role=alert]:visible").count()
                out["other_manager_pages"][route] = {"status": "passed" if not alerts else "failed",
                                                    "visible_alerts": alerts}
            except BrowserError:
                out["other_manager_pages"][route] = {"status": "failed", "reason": "route_render_timeout"}
    return out


def geometry(panel) -> dict:
    return panel.evaluate(
        """e => {const r=e.getBoundingClientRect();return {
        x:Math.round(r.x),y:Math.round(r.y),width:Math.round(r.width),height:Math.round(r.height),
        contained:r.left>=-1 && r.top>=-1 && r.right<=innerWidth+1 && r.bottom<=innerHeight+1,
        page_overflow:document.documentElement.scrollWidth>innerWidth};}"""
    )


def resident_geometry(page: Page) -> dict:
    open_chat(page)
    panel = page.locator("#resident-chat")
    panel.locator(".chat-widget-size summary").click()
    width = panel.locator("#resident-chat-width")
    height = panel.locator("#resident-chat-height")
    before = geometry(panel)
    width.focus()
    width.press("End")
    width.press("ArrowLeft")
    width.press("ArrowLeft")
    after_width = geometry(panel)
    height.focus()
    height.press("Home")
    after_height = geometry(panel)
    dock = panel.get_by_role("button", name="Dock to right edge", exact=True)
    dock.click()
    docked = geometry(panel)
    dock_pass = dock.get_attribute("aria-pressed") == "true" and height.is_disabled() and abs(
        docked["x"] + docked["width"] - 1280) <= 2
    dock.click()
    undock_pass = dock.get_attribute("aria-pressed") == "false" and height.is_enabled()
    narrow = []
    for w, h in ((390, 844), (1280, 900)):
        page.set_viewport_size({"width": w, "height": h})
        narrow.append({"viewport": [w, h], **geometry(panel)})
    panel.get_by_role("button", name="Close chat", exact=True).click()
    closed = not panel.is_visible()
    page.get_by_role("button", name="Chat", exact=True).click()
    reopened = panel.is_visible()
    resized = abs(before["width"] - after_width["width"]) >= 20 and abs(
        after_width["height"] - after_height["height"]) >= 20
    bounded = all(x["contained"] and not x["page_overflow"] for x in
                  (before, after_width, after_height, docked, *narrow))
    return {"status": "passed" if resized and bounded and dock_pass and undock_pass and closed and reopened else "failed",
            "before": before, "after_width": after_width, "after_height": after_height,
            "docked": docked, "viewports": narrow, "resize_changed": resized,
            "dock_passed": dock_pass, "undock_passed": undock_pass,
            "contained_no_overflow": bounded, "close_reopen_passed": closed and reopened,
            "resident_acceptance_helper": "checks.resident_assistant_browser_check.open_chat"}


def resident(browser, handle, record: dict) -> dict:
    out = {"origin": RESIDENT, "observed_at": utc()}
    record["apps"]["resident"] = out
    with browser.new_context(viewport={"width": 1280, "height": 900}) as context:
        out["health"] = health(context, RESIDENT)
        page = context.new_page()
        page.set_default_timeout(120000)
        out["first_navigation"] = watch(page, RESIDENT)
        page.goto(RESIDENT, wait_until="domcontentloaded", timeout=180000)
        page.locator("#signin").wait_for(state="visible")
        if urlsplit(page.url).netloc != urlsplit(RESIDENT).netloc:
            raise ValueError("Resident credential origin refused")
        user, password = credentials("resident")
        page.get_by_label("Email address", exact=True).fill(user)
        page.get_by_label("Password", exact=True).fill(password)
        consume(handle, record, "resident")
        with page.expect_response(RESIDENT + "/demo/login") as login:
            page.get_by_role("button", name="Sign in", exact=True).click()
        out["sign_in_http_status"] = login.value.status
        if login.value.status != 200:
            out["sign_in"] = {"status": "failed", "reason": "login_rejected"}
            out["chat_geometry"] = {"status": "blocked"}
            return out
        page.locator("#account").wait_for(state="visible")
        page.locator("#content").wait_for(state="visible")
        out["sign_in"] = {"status": "passed", "account_visible": True, "own_content_visible": True}
        try:
            out["chat_geometry"] = resident_geometry(page)
        except ERRORS as error:
            out["chat_geometry"] = {"status": "failed", "reason": "geometry_check_error",
                                    "error_type": type(error).__name__}
        out["chat_send"] = {"status": "not_run", "reason": "geometry_only_no_own_case_ai_consent"}
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--continue-employee", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert not may_submit({"execution": "running", "attempts": {"employee": 2}}, "employee")
        assert not may_submit({"execution": "interrupted", "attempts": {"employee": 0}}, "employee")
        assert not may_start({"task_id": TASK, "execution": "running"})
        assert not may_start({"task_id": TASK, "execution": "completed"})
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as checkpoint:
            test_record = {"execution": "running", "attempts": {"employee": 0}}
            consume(checkpoint, test_record, "employee")
            consume(checkpoint, test_record, "employee")
            checkpoint.seek(0)
            assert json.load(checkpoint)["attempts"]["employee"] == 2
            try:
                consume(checkpoint, test_record, "employee")
            except ValueError:
                pass
            else:
                raise AssertionError("Third attempt was admitted")
            checkpoint.seek(0)
            assert json.load(checkpoint)["attempts"]["employee"] == 2
        print("PASS credential-free durable checkpoint overwrite, attempt exhaustion and restart refusal")
        return 0
    if not args.run or any(os.environ.get(key) for key in ("DEBUG", "PWDEBUG", "PLAYWRIGHT_DEBUG", "DEBUG_FILE")):
        print("REFUSED live execution: explicit --run and capture-free environment required")
        return 2
    descriptor = os.open(RESULT, os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(descriptor, "r+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        handle.seek(0)
        existing = handle.read()
        if existing and not args.continue_employee:
            print("REFUSED existing execution record; no sign-in budget reset")
            return 2
        if args.continue_employee:
            decoder = json.JSONDecoder()
            checkpoints = []
            remaining = existing.strip()
            while remaining:
                checkpoint, end = decoder.raw_decode(remaining)
                if checkpoint.get("task_id") != TASK:
                    raise ValueError("Checkpoint identity refused")
                checkpoints.append(checkpoint)
                remaining = remaining[end:].lstrip()
            if not checkpoints:
                raise ValueError("Missing continuation checkpoint")
            record = checkpoints[-1]
            if record.get("execution") != "completed" or record.get("attempts", {}).get("employee") != 0:
                raise ValueError("Continuation admission refused")
            for slot in ("employee", "resident"):
                counts = [item["attempts"][slot] for item in checkpoints]
                if any(type(count) is not int or not 0 <= count <= 2 for count in counts) or counts != sorted(counts):
                    raise ValueError("Uncertain attempt history refused")
            record = json.loads(json.dumps(record))
            record["original_execution_checkpoints"] = checkpoints
            record["continued_at"] = utc()
            record["continuation_reason"] = "credential_format_repaired_zero_employee_attempts_preserved"
        else:
            record = {"task_id": TASK, "execution": "prepared", "attempts": {"employee": 0, "resident": 0},
                      "started_at": utc(), "source_head": subprocess.check_output(
                          ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "apps": {}}
            save(handle, record)
            if not may_start(record):
                return 2
        record["execution"] = "running"
        save(handle, record)
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                try:
                    for slot, check in (("employee", employee), ("resident", resident)):
                        if args.continue_employee and slot != "employee":
                            continue
                        try:
                            record["apps"][slot] = check(browser, handle, record)
                        except ERRORS as error:
                            record["apps"].setdefault(slot, {}).update(
                                status="failed", reason="bounded_check_error", error_type=type(error).__name__)
                        save(handle, record)
                finally:
                    browser.close()
        except ERRORS as error:
            record["executor_error"] = {"status": "failed", "error_type": type(error).__name__}
        record["execution"] = "completed"
        record["finished_at"] = utc()
        save(handle, record)
    print("Sanitized observations saved (not whole-app acceptance):", RESULT.relative_to(ROOT))
    failed = record.get("executor_error") or any(
        app.get("status") == "failed" for app in record["apps"].values()
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
