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

from zava_forward.api import auth, server, simulator_admin

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
test_auth: Any = importlib.import_module("test_auth")
test_mvp: Any = importlib.import_module("test_mvp")
ADMIN = "ZavaForward.ApplicationAdmin"


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
        header = test_auth.principal(roles=(ADMIN,), oid=test_auth.OID_NEW)
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
                page.goto(base + "/app#/simulator")
                page.get_by_role("heading", name="Simulator run control").wait_for()
                text = page.locator("#app").inner_text()
                assert "Unavailable" in text and "not verified live" in text, text
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
                page.get_by_label("I confirm", exact=False).first.check()
                page.get_by_role("button", name="Start Finite Run").click()
                page.get_by_text("Permitted", exact=False).first.wait_for()
                assert json.loads(control.read_text())["enabled"] is True
                assert "cannot see whether a simulator job is running" in page.inner_text("#app")
                scan(page, axe, "permitted")
                page.get_by_label("I confirm", exact=False).last.check()
                page.get_by_role("button", name="Stop Run").click()
                page.get_by_text("Stopped", exact=False).first.wait_for()
                assert json.loads(control.read_text())["enabled"] is False
                scan(page, axe, "stopped")
                browser.close()
        finally:
            httpd.shutdown()
            httpd.server_close()
    print("Simulator control browser check passed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
