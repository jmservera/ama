"""Loopback checks for the versioned home case API and its separated screen."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from building_fixture import fixture, hold, open_store

from zava_forward.api.server import App, make_handler

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"


class HomeCaseApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        data = fixture()
        data["schemes"] = [{"id": "SCH-1", "name": "Fictional scheme", "source": "SYN-SCHEME"}]
        data["staff"].append(
            {
                "code": "CON-1",
                "email": "provider@example.test",
                "name": "Synthetic Provider",
                "role": "Contractor",
                "contractor": "Test Ltd",
            }
        )
        self.store = open_store(self.tmp.name, True, data)
        app_type: Any = App
        self.app = app_type(self.store, "synthetic-only")
        handler: Any = make_handler
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler(self.app))
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.store.db.close()
        self.tmp.cleanup()

    def call(
        self, path: str, cookie: str = "", body: dict[str, Any] | None = None
    ) -> tuple[int, Any, Any]:
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Cookie": cookie, "X-ZF-CSRF": "1"},
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read()), response.headers
        except HTTPError as exc:
            return exc.code, json.loads(exc.read() or b"{}"), {}

    def login(self, email: str) -> str:
        code, _, headers = self.call(
            "/api/login", body={"email": email, "password": "synthetic-only"}
        )
        self.assertEqual(code, 200)
        return str(headers["Set-Cookie"]).split(";")[0]

    def test_view_separates_home_and_building_and_denies_unauthorised(self) -> None:
        self.assertEqual(self.call("/api/cases/ZF-2/home-case")[0], 401)
        pam = self.login("pam@example.test")
        code, view, _ = self.call("/api/cases/ZF-2/home-case", pam)
        self.assertEqual(code, 200)
        self.assertEqual(view["version"], 0)
        self.assertEqual(view["links"]["building_id"], "SYN-B1")
        self.assertNotIn("homes", view["building"])
        self.assertIn("does not transfer", view["notice"])
        self.assertEqual(view["home"]["decision"]["status"], "Accepted")
        self.assertEqual(self.call("/api/cases/NOPE/home-case", pam)[0], 404)
        self.assertEqual(self.call("/api/cases/ZF-2/extra/home-case", pam)[0], 404)
        provider = self.login("provider@example.test")
        self.assertEqual(self.call("/api/cases/ZF-2/home-case", provider)[0], 403)
        self.assertEqual(
            self.call("/api/cases/ZF-2/home-case-version", provider, {"expected_version": 0})[0],
            403,
        )

    def test_absent_funding_reads_as_not_confirmed_not_missing_case(self) -> None:
        pam = self.login("pam@example.test")
        self.store.cases["ZF-2"].pop("funding_ok")
        code, view, _ = self.call("/api/cases/ZF-2/home-case", pam)
        self.assertEqual(code, 200)
        self.assertIs(view["home"]["funding_confirmed"], False)

    def test_version_recorded_through_http_and_retained(self) -> None:
        pam = self.login("pam@example.test")
        meta = {
            "expected_version": 0,
            "source": "SYN-CASE-REVIEW",
            "source_version": "1",
            "reason": "Check links before ordering",
            "scheme_id": "SCH-1",
        }
        code, view, _ = self.call("/api/cases/ZF-2/home-case-version", pam, meta)
        self.assertEqual(code, 200)
        self.assertEqual(view["version"], 1)
        self.assertEqual(view["links"]["scheme_id"], "SCH-1")
        self.assertEqual(self.call("/api/cases/ZF-2/home-case-version", pam, meta)[0], 409)
        self.assertEqual(
            self.call("/api/cases/ZF-2/home-case-version", pam, {"reason": "x"})[0], 400
        )
        other = self.call("/api/cases/ZF-3/home-case", pam)[1]
        self.assertEqual(other["version"], 0)
        self.assertEqual(other["links"]["scheme_id"], None)
        _, again, _ = self.call("/api/cases/ZF-2/home-case", pam)
        self.assertEqual([v["version"] for v in again["versions"]], [1])

    def test_screen_is_wired_with_manual_path(self) -> None:
        script = (WEB / "app.js").read_text()
        self.assertIn("#/case-home/", script)
        self.assertIn("/home-case`", script)
        self.assertIn("This home only", script)
        self.assertIn("Shared at building level", script)
        self.assertIn("Use the case and building screens instead", script)
        self.assertIn("This home's share of shared cost", script)
        self.assertNotIn("JSON.stringify(x)", script)

    def test_payload_keeps_building_and_home_records_in_separate_regions(self) -> None:
        building = self.store.data["buildings"][0]
        building["holds"] = [hold()]
        building["dependencies"] = [
            {
                "id": "DEP-1",
                "label": "Roof access needed before loft works",
                "status": "Open",
                "owner": "Synthetic coordinator",
                "source": "SYN-DEPENDENCY",
                "case_ids": ["ZF-2"],
                "package_ids": ["PKG-SHARED"],
            }
        ]
        pam = self.login("pam@example.test")
        home_keys = {"documents", "quality", "decision", "stage", "cost_allocation", "closed"}
        building_keys = {"systems", "dependencies", "holds", "works", "costs"}
        views = {c: self.call(f"/api/cases/{c}/home-case", pam)[1] for c in ("ZF-2", "ZF-3")}
        for case_id, view in views.items():
            with self.subTest(case=case_id):
                self.assertFalse(home_keys & set(view["building"]), "home data in building region")
                self.assertFalse(building_keys & set(view["home"]), "building data in home region")
                self.assertEqual(view["building"]["dependencies"][0]["id"], "DEP-1")
                self.assertEqual(view["building"]["holds"][0]["id"], hold()["id"])
                self.assertTrue(view["building"]["works"])
                self.assertEqual(view["building"]["costs"][0]["id"], "COST-1")
                home_body = json.dumps(view["home"])
                for token in ("DEP-1", hold()["id"], "WORK-1", "COST-1: ", "12000.00"):
                    self.assertNotIn(token, home_body)
                building_body = json.dumps(view["building"])
                for doc in view["home"]["documents"]:
                    self.assertNotIn(doc["name"], building_body)
                for item in view["home"]["quality"]:
                    self.assertNotIn(item["measure"], building_body)
                self.assertNotIn("6000.00", building_body)
        own_body = json.dumps(views["ZF-2"]["home"])
        sibling_body = json.dumps(views["ZF-3"]["home"])
        for token in ("SIBLING-EVIDENCE", "Loft insulation"):
            self.assertIn(token, sibling_body)
            self.assertNotIn(token, own_body)
        self.assertEqual(views["ZF-2"]["building"], views["ZF-3"]["building"])

    def test_screen_source_renders_each_record_type_in_one_region_only(self) -> None:
        script = (WEB / "app.js").read_text()
        start = script.index("async function homeCaseView")
        body = script[start : script.index("async function buildingView", start)]
        home_start = body.index('"aria-labelledby": "hc-home"')
        building_start = body.index('"aria-labelledby": "hc-building"')
        versions_start = body.index('"aria-labelledby": "hc-versions"')
        self.assertLess(home_start, building_start)
        self.assertLess(building_start, versions_start)
        home_region = body[home_start:building_start]
        building_region = body[building_start:versions_start]
        for token in ("home.documents", "home.quality", "home.decision", "home.cost_allocation"):
            self.assertIn(token, home_region)
            self.assertNotIn(token, building_region)
        for token in ('shared("dependencies"', 'shared("holds"', 'shared("works"', "b.costs"):
            self.assertIn(token, building_region)
            self.assertNotIn(token, home_region)
        self.assertNotIn("b.", home_region.replace("b.costs", ""))
        self.assertNotRegex(building_region, r"home\.")

    def test_non_finance_staff_get_no_cost_amounts_over_http(self) -> None:
        sam = self.login("sam@example.test")
        for case_id in ("ZF-2", "ZF-3"):
            code, view, _ = self.call(f"/api/cases/{case_id}/home-case", sam)
            self.assertEqual(code, 200)
            self.assertIs(view["home"]["cost_allocation_restricted"], True)
            self.assertIsNone(view["home"]["cost_allocation"])
            self.assertIs(view["building"]["costs_restricted"], True)
            self.assertIsNone(view["building"].get("costs"))
            body = json.dumps(view)
            for amount in ("6000.00", "12000.00", "SYN-ALLOCATION", "SYN-ESTIMATE"):
                self.assertNotIn(amount, body)

    def test_finance_staff_get_building_cost_and_own_home_allocation_over_http(self) -> None:
        pam = self.login("pam@example.test")
        for case_id in ("ZF-2", "ZF-3"):
            code, view, _ = self.call(f"/api/cases/{case_id}/home-case", pam)
            self.assertEqual(code, 200)
            self.assertIs(view["home"]["cost_allocation_restricted"], False)
            self.assertEqual(
                view["home"]["cost_allocation"],
                [{"shared_cost_id": "COST-1", "amount_gbp": "6000.00", "source": "SYN-ALLOCATION"}],
            )
            self.assertFalse(view["building"].get("costs_restricted"))
            self.assertEqual(
                view["building"]["costs"],
                [
                    {
                        "id": "COST-1",
                        "work_id": "WORK-1",
                        "amount_gbp": "12000.00",
                        "source": "SYN-ESTIMATE",
                    }
                ],
            )
            self.assertNotIn("cost_allocation", view["building"])
