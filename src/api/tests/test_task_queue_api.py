"""Real loopback queue API, field projection and unchanged action authority."""

import copy
import csv
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class TaskQueueApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["as_of"] = "2026-10-16"
        data["staff"].extend(
            [
                dict(
                    code="RC-1", name="Rex", email="rex@example.test", role="Retrofit Coordinator"
                ),
                dict(
                    code="CON-1",
                    name="Kim",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        data["cases"][0].update(stage_since="2026-10-15", reason="PRIVATE-REASON")
        data["cases"][0]["technical"] = dict(
            design_version=1, design_by="sam@example.test", signoffs={}
        )
        data["cases"][0]["returns"] = [
            dict(
                from_stage="Survey booked",
                to_stage="Contacting resident",
                reason="PRIVATE-RETURN",
                source="PRIVATE-SOURCE",
                next_action="PRIVATE-ACTION",
                version=2,
            )
        ]
        for index in range(120):
            case = copy.deepcopy(DATA["cases"][0])
            case.update(
                id=f"Q-{index:03}", stage_since="2026-10-15" if index % 2 == 0 else "2026-10-01"
            )
            case["home"]["area"] = "Paging"
            case["resident"]["name"] = f"Person {119 - index:03}"
            data["cases"].append(case)
        path = Path(self.tmp.name) / "seed.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler(App(self.store, "synthetic-check"))
        )
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(self, actor: str, path: str, body: object = None) -> tuple[int, Any]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-check")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                raw = response.read().decode()
                return response.status, raw if path.split("?")[0].endswith(".csv") else (
                    json.loads(raw)
                )
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_metadata_filters_csv_and_consistent_context(self) -> None:
        meta = self.call("sam", "/api/me")[1]["work_queues"]
        self.assertEqual(meta["version"], "work-queues-1")
        self.assertEqual(meta["default"]["view"], "mine")
        self.assertIsNone(meta["selection"])
        path = "/api/cases?view=all&queue=new&area=Test&limit=1"
        code, page = self.call("sam", path)
        self.assertEqual(code, 200)
        self.assertEqual(page["total"], 1)
        self.assertEqual([r["id"] for r in page["items"]], ["ZF-1"])
        detail = self.call("sam", "/api/cases/ZF-1")[1]
        self.assertEqual(page["items"][0]["work"], detail["work"])
        self.assertEqual(detail["work"]["reason"], "PRIVATE-RETURN")
        self.assertEqual(detail["work"]["version"], 2)
        code, text = self.call("sam", "/api/cases.csv?view=all&queue=new&area=Test")
        self.assertEqual(code, 200)
        self.assertEqual([r[0] for r in list(csv.reader(io.StringIO(text)))[1:]], ["ZF-1"])
        self.assertEqual(self.call("sam", "/api/cases?queue=priority")[1]["total"], 0)
        for suffix in ("", ".csv"):
            code, error = self.call("sam", f"/api/cases{suffix}?queue=invented")
            self.assertEqual(code, 400)
            self.assertIn("published work queues", error["error"])

    def test_projection_and_direct_action_permissions_cannot_be_changed_by_view(self) -> None:
        for path in (
            "/api/cases?view=all&queue=new&role=Resident%20Liaison%20Officer",
            "/api/cases/ZF-1",
            "/api/cases.csv?view=all&queue=new",
        ):
            code, result = self.call("rex", path)
            self.assertEqual(code, 200)
            self.assertNotIn("PRIVATE-", json.dumps(result))
        for path in ("/api/cases?view=all", "/api/cases/ZF-1"):
            code, result = self.call("kim", path)
            self.assertEqual(code, 200)
            self.assertNotIn('"work"', json.dumps(result))
            self.assertNotIn("PRIVATE-", json.dumps(result))
        self.assertNotIn("work_queues", self.call("kim", "/api/me")[1])
        self.assertEqual(self.call("kim", "/api/cases?queue=new")[0], 403)
        self.assertEqual(self.call("kim", "/api/cases/ZF-1/hazard-raise", {})[0], 403)
        self.assertEqual(
            self.call(
                "rex",
                "/api/cases/ZF-1/technical",
                dict(
                    action="signoff_give",
                    type="building",
                    role="Building Safety Liaison",
                ),
            )[0],
            403,
        )
        with self.assertRaises(urllib.error.HTTPError) as denied:
            urllib.request.urlopen(self.base + "/api/cases?queue=new")
        self.assertEqual(denied.exception.code, 401)

    def test_http_queue_filter_precedes_count_cursor_sort_and_export(self) -> None:
        query = "view=all&queue=new&area=Paging&wave=Wave%201&owner=RLO-01"
        first = self.call("sam", "/api/cases?" + query + "&limit=50")[1]
        self.assertEqual(first["total"], 60)
        cursor = urllib.parse.quote(first["next_cursor"], safe="")
        second = self.call("sam", "/api/cases?" + query + "&limit=50&after=" + cursor)[1]
        expected = [f"Q-{index:03}" for index in range(0, 120, 2)]
        actual = [row["id"] for row in first["items"] + second["items"]]
        self.assertEqual(actual, expected)
        self.assertEqual(len(set(actual)), 60)
        self.assertEqual(second["total"], 60)
        by_name = self.call("sam", "/api/cases?" + query + "&limit=100&sort=name")[1]
        self.assertEqual([row["id"] for row in by_name["items"]], expected[::-1])
        code, text = self.call("sam", "/api/cases.csv?" + query + "&sort=name")
        self.assertEqual(code, 200)
        self.assertEqual(
            [row[0] for row in list(csv.reader(io.StringIO(text)))[1:]], expected[::-1]
        )


if __name__ == "__main__":
    unittest.main()
