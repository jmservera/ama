"""Pending-handoff read-failure guidance (issue 153): reason, owner and next action.

The Node cases run the real pendingHandoffs source with stubbed rendering helpers. The opt-in
browser cases serve the real app on loopback with synthetic data: success and empty use the actual
backend projection, while the rejected GET is explicitly constructed by a page fetch wrapper.
Neither is human, assistive-technology or live acceptance.
"""

import json
import os
import re
import subprocess
import tempfile
import threading
import unittest
from collections.abc import Callable
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any, cast

from dataset import change_metadata
from zava_forward.core.store import Store

import test_mvp
from zava_forward.api.server import App, make_handler

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
# App.__init__ is untyped; this is the verified (store, password) construction contract.
build_app = cast(Callable[[Store, str], App], App)
SAM = test_mvp.DATA["staff"][0]
CANARY = "CANARY_TRANSPORT_7f3 TypeError at /srv/x.py"
BANNED = re.compile(r"\b(gate|hold|provenance|trace)\b", re.I)
START = "function pendingHandoffs"
END = "let briefingBox"

NODE = r"""
const fs = require("node:fs"), vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const fn = src.indexOf(process.argv[2]), end = src.indexOf(process.argv[3]);
const constant = src.indexOf("const HANDOFF_READ_ERROR");
const start = constant >= 0 && constant < fn ? constant : fn;
if (fn < 0 || end < fn) throw new Error("pendingHandoffs source markers not found");
const slice = src.slice(start, end);
const element = (tag, attrs, kids) => ({tag, attrs, kids, hidden: false,
  replaceChildren(...next) { this.kids = next; },
  text() { return this.kids.map(k => typeof k === "string" ? k : k.text()).join(" "); }});
const h = (tag, attrs, ...kids) => element(tag, attrs || {}, kids.flat().filter(k => k != null));
const tick = () => new Promise(resolve => setTimeout(resolve, 0));
const row = {case_id: "ZF-1", resident: "Pat Test", address: "1 Test Road", status: "Sent",
  accountable_owner: "Sam Example", to_code: "PM-01"};
const out = {};
(async () => {
  const scenarios = {
    transport: new TypeError("Failed to fetch CANARY"),
    abort: Object.assign(new Error("signal is aborted"), {name: "AbortError"}),
    http: Object.assign(new Error("Handoff service said no"), {status: 500}),
    ended: Object.assign(new Error("Your session has ended. Sign in again."), {status: 401}),
    rows: [row],
    empty: [],
  };
  for (const [name, result] of Object.entries(scenarios)) {
    let calls = [];
    const api = (...args) => { calls.push(args); return result instanceof Error
      ? Promise.reject(result) : Promise.resolve(result); };
    const ctx = vm.createContext({h, api, me: {user: {code: "RLO-01"}}, encodeURIComponent});
    vm.runInContext(slice + "\nthis.pendingHandoffs = pendingHandoffs;", ctx);
    const box = ctx.pendingHandoffs();
    await tick();
    out[name] = {hidden: box.hidden, text: box.text(),
      alert: box.kids.some(k => k.attrs && k.attrs.role === "alert"), calls};
  }
  console.log(JSON.stringify(out));
})();
"""


def node_outputs() -> dict[str, Any]:
    done = subprocess.run(
        ["node", "-e", NODE, str(WEB), START, END],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if done.returncode:
        raise AssertionError(done.stderr)
    outputs: dict[str, Any] = json.loads(done.stdout)
    return outputs


class HandoffReadGuidanceText(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = node_outputs()

    def test_transport_rejection_states_reason_owner_and_next_action(self) -> None:
        case = self.out["transport"]
        text = case["text"]
        self.assertTrue(case["alert"])
        self.assertFalse(case["hidden"])
        self.assertRegex(text, r"could not load, so we cannot tell whether any are waiting\.")
        self.assertRegex(text, r"Owner: application support\. Next action: refresh to try again")
        self.assertIn("then contact application support if it continues.", text)
        self.assertNotIn("CANARY", text)
        self.assertNotIn("Failed to fetch", text)
        self.assertNotIn("Could not load handoffs", text)
        self.assertTrue(text.isascii())
        self.assertIsNone(BANNED.search(text), text)
        self.assertNotRegex(text, r"\b(no handoffs|nothing waiting|all clear)\b")

    def test_one_read_only_request_and_no_retry_or_mutation(self) -> None:
        for name, case in self.out.items():
            with self.subTest(name=name):
                self.assertEqual(case["calls"], [["/api/handoffs"]])

    def test_abort_paints_nothing_and_http_paths_keep_their_text(self) -> None:
        self.assertEqual(self.out["abort"]["text"], "Loading handoffs...")
        self.assertFalse(self.out["abort"]["alert"])
        self.assertEqual(
            self.out["http"]["text"], "Could not load handoffs: Handoff service said no"
        )
        self.assertEqual(
            self.out["ended"]["text"],
            "Could not load handoffs: Your session has ended. Sign in again.",
        )

    def test_success_lists_rows_and_empty_hides_the_card(self) -> None:
        self.assertFalse(self.out["rows"]["hidden"])
        self.assertIn("Pat Test, 1 Test Road", self.out["rows"]["text"])
        self.assertNotIn("Owner: application support", self.out["rows"]["text"])
        self.assertTrue(self.out["empty"]["hidden"])

    def test_source_keeps_the_alert_element_and_the_constant_is_the_only_new_text(self) -> None:
        source = (WEB / "app.js").read_text()
        body = source[source.index("const HANDOFF_READ_ERROR") : source.index(END)]
        self.assertEqual(body.count('role: "alert"'), 1)
        self.assertEqual(body.count("HANDOFF_READ_ERROR"), 2)
        self.assertNotIn("e.message}`)", body.split("}).catch")[1].split("HANDOFF_READ_ERROR")[0])
        self.assertNotIn("setTimeout", body)


class Served:
    """Isolated loopback app with one synthetic Sent handoff, or none."""

    def __init__(self, offer: bool) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(test_mvp.DATA))
        self.store = Store(str(path))
        if offer:
            self.store.offer_handoff(
                SAM,
                "ZF-1",
                "pam@example.test",
                "synthetic note",
                metadata=change_metadata(self.store, "ZF-1"),
            )
        app = build_app(self.store, "zf-test")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()


# Explicitly constructed failure: the page fetch wrapper rejects only GET /api/handoffs.
REJECT = """
window.__failHandoffs = true;
window.__attempts = 0;
const real = window.fetch;
window.fetch = function (input, init) {
  const url = new URL(typeof input === 'string' ? input : input.url, location.href);
  if (window.__failHandoffs && url.pathname === '/api/handoffs' && ++window.__attempts)
    return Promise.reject(new TypeError(CANARY_TEXT));
  return real.apply(this, arguments);
};
""".replace("CANARY_TEXT", json.dumps("Failed to fetch " + CANARY))


@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")
class HandoffReadGuidanceBrowser(unittest.TestCase):
    pw: Any
    browser: Any

    @classmethod
    def setUpClass(cls) -> None:
        from playwright.sync_api import sync_playwright

        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.pw.stop()

    def open(self, offer: bool, init: str = "") -> tuple[Any, list[Any]]:
        served = Served(offer)
        self.addCleanup(served.close)
        page = self.browser.new_page()
        self.addCleanup(page.close)
        requests: list[Any] = []
        page.on("request", lambda request: requests.append(request))
        page.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(served.base) else route.abort()
            ),
        )
        if init:
            page.add_init_script(init)
        page.goto(served.base + "/")
        status = page.evaluate(
            """async () => (await fetch('/api/login', {method: 'POST',
              headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'},
              body: JSON.stringify({email: 'sam@example.test', password: 'zf-test'})})).status"""
        )
        self.assertEqual(status, 200)
        page.goto(served.base + "/app#/")
        page.get_by_role("heading", name="My cases today").wait_for()
        return page, requests

    @staticmethod
    def card(page: Any) -> Any:
        return page.locator('section[aria-label="Handoffs waiting for you"]')

    def test_actual_success_and_empty_projection_are_unchanged(self) -> None:
        from playwright.sync_api import expect

        page, _ = self.open(True)
        expect(self.card(page)).to_contain_text("Pat Test, 1 Test Road")
        expect(self.card(page)).not_to_contain_text("Owner: application support")
        page, _ = self.open(False)
        expect(self.card(page)).to_be_hidden()
        self.assertNotIn("could not load", page.locator("main").inner_text())

    def test_constructed_transport_rejection_shows_guidance_not_empty(self) -> None:
        from playwright.sync_api import expect

        page, requests = self.open(True, REJECT)
        card = self.card(page)
        expect(card).to_be_visible()
        expect(card.get_by_role("alert")).to_contain_text(
            "could not load, so we cannot tell whether any are waiting."
        )
        expect(card).to_contain_text("Owner: application support")
        expect(card).to_contain_text("Next action: refresh to try again")
        self.assertNotIn("CANARY", page.locator("main").inner_text())
        self.assertNotIn("Failed to fetch", page.locator("main").inner_text())
        self.assertNotIn("Pat Test", card.inner_text())
        # One rejected attempt, no retry; the wrapper rejects before the network.
        self.assertEqual(page.evaluate("window.__attempts"), 1)
        self.assertEqual([r for r in requests if r.url.endswith("/api/handoffs")], [])
        self.assertEqual([r for r in requests if r.method == "POST" and "login" not in r.url], [])

    def test_session_ended_read_keeps_sign_in_path_and_no_load_guidance(self) -> None:
        page, _ = self.open(True)
        page.route(
            "**/api/handoffs",
            lambda route: route.fulfill(
                status=401, content_type="application/json", body='{"error": "x"}'
            ),
        )
        page.evaluate("location.reload()")
        page.get_by_text("Your session has ended. Sign in again.").first.wait_for()
        self.assertNotIn("Owner: application support", page.locator("body").inner_text())

    def test_navigation_during_pending_read_paints_nothing_in_the_new_view(self) -> None:
        page, _ = self.open(True)
        held: list[Any] = []
        page.route("**/api/handoffs", lambda route: held.append(route))
        page.goto(page.url.split("#")[0] + "#/")
        page.evaluate("location.reload()")
        page.get_by_role("heading", name="My cases today").wait_for()
        page.evaluate("location.hash = '#/all'")
        page.get_by_role("link", name="See my cases").wait_for()
        for route in held:
            route.abort("failed")
        page.wait_for_timeout(300)
        self.assertNotIn("could not load", page.locator("main").inner_text())
        self.assertEqual(self.card(page).count(), 0)
