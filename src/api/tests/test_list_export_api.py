"""Issue 80: every staff list offers a CSV copy with the staff roles only."""

import copy
import csv
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import LIST_EXPORTS, App, make_handler

LISTS = ("packages", "workorders", "handoffs", "visits", "funding")


class ListExportApi(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"].append(
            dict(
                code="CON-1",
                name="Kim",
                email="kim@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
        )
        data["cases"][0]["resident"]["name"] = "=HYPERLINK(\"x\")"
        path = Path(tmp.name) / "seed.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler(App(self.store, "synthetic-check"))
        )
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        self.base = f"http://127.0.0.1:{httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def call(self, actor: str, path: str) -> tuple[int, str, dict[str, str]]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-check")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(self.base + path, headers={"Cookie": self.cookies[actor]})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read().decode(), dict(response.headers)
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode(), dict(error.headers)

    def test_registry_matches_lists(self) -> None:
        self.assertEqual({p[len("/api/"):-4] for p in LIST_EXPORTS}, set(LISTS))

    def test_staff_get_csv_matching_json_rows(self) -> None:
        for name in LISTS:
            with self.subTest(name=name):
                code, text, headers = self.call("sam", f"/api/{name}.csv?view=all")
                self.assertEqual(code, 200)
                self.assertTrue(headers["Content-Type"].startswith("text/csv"))
                self.assertIn(f'filename="{name}.csv"', headers["Content-Disposition"])
                rows = list(csv.reader(io.StringIO(text)))
                _, body, _ = self.call("sam", f"/api/{name}?view=all")
                self.assertEqual(len(rows) - 1, len(json.loads(body)))

    def test_formula_text_is_neutralised(self) -> None:
        _, text, _ = self.call("sam", "/api/funding.csv")
        self.assertNotIn(",=HYPERLINK", text)
        self.assertIn("'=HYPERLINK", text)

    def test_contractor_and_signed_out_callers_get_no_export(self) -> None:
        for name in LISTS:
            self.assertEqual(self.call("kim", f"/api/{name}.csv")[0], 403, name)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(self.base + "/api/packages.csv")
        self.assertEqual(ctx.exception.code, 401)

    def test_export_is_read_only(self) -> None:
        before = copy.deepcopy(self.store.cases)
        for name in LISTS:
            self.call("sam", f"/api/{name}.csv")
        self.assertEqual(self.store.cases, before)


if __name__ == "__main__":
    unittest.main()
