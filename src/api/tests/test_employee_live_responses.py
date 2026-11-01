"""Issue 691: vendor assets served whole, errors logged, expected denials worded plainly."""

import copy
import json
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

import test_mvp  # noqa: F401  (puts the shared fixtures on the path)
from zava_forward.api.server import App, make_handler

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class VendorAssets(unittest.TestCase):
    def setUp(self) -> None:
        import dataset
        from zava_forward.core.sqlstore import SqlStore

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "synthetic.json"
        path.write_text(json.dumps(copy.deepcopy(dataset.DATA)))
        self.store = store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(store.db.close)
        app = App(store, "SYN-691")  # type: ignore[no-untyped-call]
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(self.httpd.server_close)
        self.addCleanup(self.httpd.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.expected = (WEB / "vendor/leaflet.js").read_bytes()

    def fetch(
        self, path: str, method: str = "GET", headers: dict[str, str] | None = None
    ) -> tuple[int, bytes, Any]:
        request = urllib.request.Request(self.base + path, method=method, headers=headers or {})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read(), response.headers
        except urllib.error.HTTPError as error:
            return error.code, error.read(), error.headers

    def test_leaflet_is_served_whole_for_every_request_shape(self) -> None:
        status, body, headers = self.fetch("/vendor/leaflet.js")
        self.assertEqual((status, body), (200, self.expected))
        self.assertEqual(len(self.expected), 147552)
        self.assertEqual(self.fetch("/vendor/leaflet.js?v=anything")[:2], (200, self.expected))
        head_status, head_body, head_headers = self.fetch("/vendor/leaflet.js", "HEAD")
        self.assertEqual((head_status, head_body), (200, b""))
        self.assertEqual(head_headers["Content-Length"], str(len(self.expected)))
        status, body, _ = self.fetch(
            "/vendor/leaflet.js", headers={"If-None-Match": headers["ETag"]}
        )
        self.assertEqual((status, body), (304, b""))

    def test_concurrent_requests_never_return_a_server_error_or_short_body(self) -> None:
        with ThreadPoolExecutor(16) as pool:
            results = list(pool.map(lambda _: self.fetch("/vendor/leaflet.js")[:2], range(48)))
        self.assertEqual(set(results), {(200, self.expected)})

    def test_vendor_failures_and_server_errors_are_logged_without_the_query(self) -> None:
        with self.assertLogs("zava_forward.api.server", "WARNING") as logs:
            self.assertEqual(self.fetch("/vendor/missing.js?secret=1")[0], 404)
        self.assertEqual(len(logs.output), 1)
        self.assertIn("/vendor/missing.js status=404", logs.output[0])
        self.assertNotIn("secret", logs.output[0])
        with self.assertNoLogs("zava_forward.api.server", "WARNING"):
            self.fetch("/vendor/leaflet.js")
        with patch.object(self.store, "ready", return_value=False):
            with self.assertLogs("zava_forward.api.server", "WARNING") as logs:
                self.assertEqual(self.fetch("/healthz")[0], 503)
        self.assertIn("GET /healthz status=503", logs.output[0])
        with self.assertLogs("zava_forward.api.server", "WARNING") as logs:
            self.assertEqual(self.fetch("/vendor/leaflet.js", method="OPTIONS")[0], 501)
        self.assertEqual(len(logs.output), 1)
        self.assertIn("OPTIONS /vendor/leaflet.js status=501", logs.output[0])

    def test_vendor_asset_does_not_depend_on_the_identity_store(self) -> None:
        from zava_forward.core import identity

        class Provider:
            name = "trusted-proxy"

            def authenticate(self, headers: Any) -> dict[str, Any]:
                return {"identity_source": identity.SOURCE, "email": "x@example.test"}

        app = App(self.store, "SYN-691", provider=Provider())
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        with patch.object(identity, "bind", side_effect=RuntimeError("database is locked")):
            request = urllib.request.Request(
                f"http://127.0.0.1:{httpd.server_port}/vendor/leaflet.js"
            )
            with urllib.request.urlopen(request) as response:
                self.assertEqual((response.status, response.read()), (200, self.expected))

    def raw(self, request: bytes) -> bytes:
        import socket

        with socket.create_connection(("127.0.0.1", self.httpd.server_port), timeout=5) as sock:
            sock.sendall(request)
            chunks = []
            while chunk := sock.recv(4096):
                chunks.append(chunk)
        return b"".join(chunks)

    def test_malformed_request_lines_still_get_error_responses(self) -> None:
        cases = {
            b"GET /" + b"a" * 70000 + b" HTTP/1.1\r\n\r\n": b" 414 ",
            b"BAD\r\n\r\n": b" 400 ",
            b"OPTIONS http://[ HTTP/1.1\r\n\r\n": b" 501 ",
        }
        for request, status in cases.items():
            with self.subTest(status=status):
                self.assertIn(status, self.raw(request).split(b"\r\n")[0] + b" ")


class ExpectedDenialWording(unittest.TestCase):
    def run_node(self, script: str) -> None:
        result = subprocess.run(
            ["node", "-e", script, str(WEB)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_403_and_503_do_not_assert_a_cause_the_server_did_not_confirm(self) -> None:
        self.run_node(
            r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const source = fs.readFileSync(process.argv[1] + "/chat.js", "utf8");
const start = source.indexOf("function unavailableNote");
const body = source.slice(start, source.indexOf("const employeeChat"));
const fn = new Function(body + "; return unavailableNote;")();
const manual = "Continue manually.";
const err = (m, extra) => Object.assign(new Error(m), extra);
assert.equal(fn("Cited lookup", err("Demo not configured.", {status: 403}), manual),
  "Cited lookup is not available right now: Demo not configured. Continue manually.");
assert.equal(fn("Cited lookup", err("Law store off.", {status: 503}), manual),
  "Cited lookup is not available right now: Law store off. Continue manually.");
const roleError = err("Not available for your role.", {status: 403, roleDenied: true});
assert.equal(fn("Cited lookup", roleError, manual),
  "Cited lookup is not available for your role. Continue manually.");
"""
        )

    def test_administrator_role_does_not_request_staff_only_endpoints(self) -> None:
        self.run_node(
            r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(process.argv[1] + "/chat.js", "utf8");
const node = (tag, children) => ({
  tag, children, attrs: {}, dataset: {}, classList: {add() {}, remove() {}},
  setAttribute() {}, append() {}, replaceChildren() {}, addEventListener() {},
});
async function run(role) {
  const calls = [];
  const context = vm.createContext({
    document: {getElementById: () => node("div", [])},
    Intl,
    h: (tag, attrs, ...children) => node(tag, children),
    api: (path) => { calls.push(path); return new Promise(() => {}); },
    snapshotCaseFields: () => [],
    caseFieldUnchanged: () => true,
    me: {user: {role}},
  });
  vm.runInContext(source, context);
  vm.runInContext('chatCasePanel("c1"); regulatoryChatPanel("c1");', context);
  await new Promise((resolve) => setImmediate(resolve));
  return calls;
}
(async () => {
  const admin = await run("Application Administrator");
  assert.ok(!admin.includes("/api/assistants"), admin.join());
  assert.ok(!admin.includes("/api/chat/regulatory/status"), admin.join());
  const staff = await run("Housing Officer");
  assert.ok(staff.includes("/api/assistants"), staff.join());
  assert.ok(staff.includes("/api/chat/regulatory/status"), staff.join());
})().catch((e) => { console.error(e); process.exit(1); });
"""
        )


if __name__ == "__main__":
    unittest.main()
