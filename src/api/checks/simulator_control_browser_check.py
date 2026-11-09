"""Browser and axe check of the administrator simulator control on a synthetic local store (#189)."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import tempfile
import threading
from datetime import UTC, datetime, timedelta
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

from playwright.sync_api import Page, sync_playwright
from zava_forward.core import identity
from zava_forward.core.store import Store

from zava_forward.api import auth, live_control, server, simulator_admin

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
test_auth: Any = importlib.import_module("test_auth")
test_mvp: Any = importlib.import_module("test_mvp")
ADMIN = "ZavaForward.ApplicationAdmin"
STAFF = "ZavaForward.LiaisonOfficer"


def load_axe(path: Path) -> str:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
        raise ValueError("Expected pinned axe-core 4.10.3")
    return raw.decode()


def scan(page: Page, axe: str | None, state: str) -> None:
    if axe is None:
        print(f"Simulator control axe {state}: NOT RUN (--axe not supplied)", flush=True)
        return
    page.evaluate(axe)
    result: dict[str, Any] = page.evaluate(
        """async () => await axe.run(document.querySelector('#app'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}
        })"""
    )
    print(json.dumps(dict(state=state, violations=result["violations"])), flush=True)
    assert not result["violations"], (state, result["violations"])


def control_file(path: Path, enabled: bool, days: float) -> None:
    expires = datetime.now(UTC) + timedelta(days=days)
    path.write_text(
        json.dumps(
            {
                "version": "live-sim-control-v1",
                "enabled": enabled,
                "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "approval_reference": "issue-184-comment-6652226413",
                "owner": "demo owner",
                "homes": ["HOME-001", "HOME-002"],
            }
        )
    )


def open_screen(page: Page, base: str) -> None:
    page.goto(base + "/app#/simulator")
    page.reload()
    page.get_by_role("heading", name="Simulator run control").wait_for()


def stop(page: Page) -> None:
    page.get_by_label("I confirm I want to stop this run.").check()
    page.get_by_role("button", name="Stop Run").click()


def stop_state(
    page: Page,
    control: Path,
    axe: str | None,
    base: str,
    state: str,
    label: str,
    enabled: bool,
    days: float,
) -> None:
    control_file(control, enabled, days)
    before = json.loads(control.read_text())
    open_screen(page, base)
    assert label in page.inner_text("#app"), (state, page.inner_text("#app"))
    scan(page, axe, state)
    assert page.get_by_role("button", name="Stop Run").count() == 1, state
    stop(page)
    page.get_by_text("saved and read back", exact=False).first.wait_for()
    after = json.loads(control.read_text())
    assert after["enabled"] is False, (state, after)
    assert {k: v for k, v in after.items() if k != "enabled"} == {
        k: v for k, v in before.items() if k != "enabled"
    }, (state, "stop must keep cohort, owner and expiry")
    assert page.get_by_role("button", name="Stop Run").count() == 1, (state, "Stop stays available")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path)
    args = parser.parse_args()
    axe = load_axe(args.axe) if args.axe else None
    with tempfile.TemporaryDirectory() as tmp:
        data = json.loads(json.dumps(test_mvp.DATA))
        data[identity.LEGACY_TENANT_KEY] = test_auth.TENANT
        seed = Path(tmp) / "zavaforward.json"
        seed.write_text(json.dumps(data))
        store = Store(str(seed))
        control = Path(tmp) / "control.json"
        header = test_auth.principal(roles=(ADMIN, STAFF), oid=test_auth.OID_NEW)
        read_only_header = test_auth.principal(roles=(ADMIN,), oid=test_auth.OID_NEW)
        provider = auth.TrustedProxyProvider(store, test_auth.ENV)
        httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), server.make_handler(server.App(store, provider=provider))
        )
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}"
        try:
            with (
                patch.dict("os.environ", {simulator_admin.ENV: str(control)}),
                sync_playwright() as pw,
            ):
                browser = pw.chromium.launch()
                page = browser.new_context(
                    extra_http_headers={"X-MS-CLIENT-PRINCIPAL": header}
                ).new_page()
                open_screen(page, base)
                text = page.locator("#app").inner_text()
                assert "Unavailable" in text and "not verified live" in text, text
                assert page.get_by_role("button", name="Stop Run").count() == 0
                scan(page, axe, "unavailable")
                page.get_by_label("Named owner").fill("demo owner")
                page.get_by_label("Approval reference").fill("issue-184-comment-6652226413")
                expiry = (datetime.now(UTC) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
                page.get_by_label("Expiry time (UTC)").fill(expiry)
                page.get_by_label("Home ids").fill("HOME-001, HOME-002")
                page.get_by_role("button", name="Start Finite Run").click()
                page.locator("#app [role=alert]").first.wait_for()
                assert not control.exists(), "start without confirmation must write nothing"
                scan(page, axe, "rejected start")
                page.get_by_label("I confirm this permits sending", exact=False).check()
                page.get_by_role("button", name="Start Finite Run").click()
                page.get_by_text("Permitted", exact=False).first.wait_for()
                assert json.loads(control.read_text())["enabled"] is True
                assert "cannot see whether a simulator job is running" in page.inner_text("#app")
                assert page.get_by_role("button", name="Start Finite Run").count() == 0
                scan(page, axe, "permitted")
                stop(page)
                page.get_by_text("Stopped", exact=False).first.wait_for()
                assert json.loads(control.read_text())["enabled"] is False
                scan(page, axe, "stopped after stop")
                stop_state(page, control, axe, base, "permitted stop", "Permitted", True, 1)
                stop_state(page, control, axe, base, "expired enabled", "Expired", True, -1)
                stop_state(page, control, axe, base, "invalid window", "Not valid", True, 30)
                stop_state(page, control, axe, base, "already stopped", "Stopped", False, 1)
                scan(page, axe, "already stopped after repeat")
                control_file(control, True, 1)
                open_screen(page, base)
                control_file(control, True, 2)
                changed = control.read_bytes()
                stop(page)
                page.locator("#simulator-control-notice[role=alert]").wait_for()
                assert "changed since this screen loaded" in page.inner_text("#app")
                assert control.read_bytes() == changed, "stale stop must write nothing"
                scan(page, axe, "stale")
                control_file(control, True, 1)
                open_screen(page, base)
                unchanged = control.read_bytes()
                with patch.object(live_control, "write", side_effect=OSError("disk")):
                    stop(page)
                    page.locator("#simulator-control-notice[role=alert]").wait_for()
                assert "could not be saved" in page.inner_text("#app")
                assert control.read_bytes() == unchanged, "failed write must leave the control"
                scan(page, axe, "write error")
                control.unlink()
                control.parent.joinpath("blocked").write_text("x")
                with patch.dict(
                    "os.environ", {simulator_admin.ENV: str(control.parent / "blocked" / "c.json")}
                ):
                    open_screen(page, base)
                    assert "Unavailable" in page.inner_text("#app")
                    assert "manual route" in page.inner_text("#app").lower()
                    assert page.get_by_role("button", name="Stop Run").count() == 0
                    scan(page, axe, "manual route, not writable")
                control_file(control, True, 1)
                read_only = browser.new_context(
                    extra_http_headers={"X-MS-CLIENT-PRINCIPAL": read_only_header}
                ).new_page()
                open_screen(read_only, base)
                shown = read_only.inner_text("#app")
                assert "Permitted" in shown and "changes nothing" in shown, shown
                assert read_only.get_by_role("button", name="Stop Run").count() == 0
                assert read_only.get_by_role("button", name="Start Finite Run").count() == 0
                scan(read_only, axe, "view-only administrator")
                browser.close()
        finally:
            httpd.shutdown()
            httpd.server_close()
    print("Simulator control browser check passed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
