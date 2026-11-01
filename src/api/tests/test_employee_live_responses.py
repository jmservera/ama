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

    def test_403_and_503_read_as_plain_language_not_failures(self) -> None:
        self.run_node(
            r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const source = fs.readFileSync(process.argv[1] + "/chat.js", "utf8");
const start = source.indexOf("function unavailableNote");
const body = source.slice(start, source.indexOf("const employeeChat"));
const fn = new Function(body + "; return unavailableNote;")();
const manual = "Continue manually.";
const err = (m, status) => Object.assign(new Error(m), {status});
const denied = fn("Proposal requests", err("Staff only.", 403), manual);
assert.equal(denied, "Proposal requests is not available for your role. Continue manually.");
const off = fn("Cited lookup", err("Law store off.", 503), manual);
assert.equal(off, "Cited lookup is not switched on in this environment. Continue manually.");
assert.match(fn("Cited lookup", err("Boom.", 500), manual), /unavailable: Boom\./);
"""
        )

    def test_administrator_role_does_not_request_staff_only_endpoints(self) -> None:
        source = (WEB / "chat.js").read_text()
        self.assertIn('const chatAdministratorRole = "Application Administrator";', source)
        assistants = source.index('api("/api/assistants")')
        self.assertLess(source.rindex("chatAdministratorRole", 0, assistants), assistants)
        status = source.index('api("/api/chat/regulatory/status")')
        self.assertLess(source.rindex("chatAdministratorRole", 0, status), status)
        self.assertIn("Rule alerts are not switched on in this environment.", source)


if __name__ == "__main__":
    unittest.main()
