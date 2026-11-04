"""Manifest default queues compared with the real API (partial AC-034/043 evidence)."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from checks.workbench_browser_check import MANIFEST, synthetic_data
from zava_forward.core.store import Store

from zava_forward.api.server import App, make_handler

PASSWORD = "synthetic-only"


class ManifestDefaultsMatchApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        seed = Path(self.tmp.name) / "zavaforward.json"
        seed.write_text(json.dumps(synthetic_data()), encoding="utf-8")
        app_type: Any = App
        handler: Any = make_handler
        self.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), handler(app_type(Store(str(seed)), PASSWORD))
        )
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def call(self, path: str, cookie: str = "", body: dict[str, Any] | None = None) -> Any:
        request = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Cookie": cookie, "X-ZF-CSRF": "1"},
        )
        with urlopen(request, timeout=5) as response:
            return json.loads(response.read()), response.headers.get("Set-Cookie", "")

    def login(self, email: str) -> str:
        _, cookie = self.call("/api/login", body={"email": email, "password": PASSWORD})
        return str(cookie).split(";")[0]

    def test_default_ids_count_and_order_match_the_real_own_queue(self) -> None:
        checked = 0
        for profile in MANIFEST["profiles"]:
            default = profile.get("default")
            if default is None:
                continue
            checked += 1
            with self.subTest(profile=profile["perspective"]):
                cookie = self.login(profile["identity"])
                page, _ = self.call(f"/api/cases?view=mine&sort={default['order']}", cookie)
                self.assertEqual([row["id"] for row in page["items"]], default["ids"])
                self.assertEqual(page["total"], default["count"])
        self.assertEqual(checked, 8)

    def test_all_cases_scope_is_the_declared_fixture_set_for_staff(self) -> None:
        cookie = self.login("pam@example.test")
        page, _ = self.call("/api/cases?view=all&sort=urgent", cookie)
        self.assertEqual({row["id"] for row in page["items"]}, set(MANIFEST["all_case_ids"]))

    def test_declared_endpoints_are_reachable_for_each_partial_profile(self) -> None:
        for profile in MANIFEST["profiles"]:
            endpoint = profile.get("endpoint", "")
            if not endpoint.startswith("#/case/"):
                continue
            with self.subTest(profile=profile["perspective"]):
                cookie = self.login(profile["identity"])
                case, _ = self.call("/api/cases/" + endpoint.removeprefix("#/case/"), cookie)
                self.assertEqual(case["id"], endpoint.removeprefix("#/case/"))


if __name__ == "__main__":
    unittest.main()
