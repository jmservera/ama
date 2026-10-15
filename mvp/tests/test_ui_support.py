"""Server behaviour the new screens rely on: closed list and reopen, contractor projection, map list data, tile config."""
import copy
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from zavaforward_mvp import auth
from zavaforward_mvp.server import App, make_handler
from zava_forward.core.store import Store

REASON = "SEEDED-REASON-hearing-loss"
STAFF = [dict(code="RLO-01", name="Sam Example", email="sam@example.test", role="Resident Liaison Officer"),
         dict(code="PM-01", name="Pam Lead", email="pam@example.test", role="Retrofit Programme Manager"),
         dict(code="CON-1", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Test Ltd")]


def data():
    d = copy.deepcopy(test_mvp.DATA)
    d["staff"] = STAFF
    for i, c in enumerate(d["cases"]):
        c["home"].update(lat=54.0 + i * 0.01, lon=-1.5)
        c["resident"]["name"] = f"Resident {i}"
    d["cases"][0]["resident"].update(adjustment=REASON, priority_support=True)
    d["cases"][1]["contractor"]["name"] = "Other Ltd"
    d["cases"].append(dict(test_mvp.case("ZF-9", stage="Completed"), closed=True))
    return d


class Base(unittest.TestCase):
    ENV = {}

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        p = Path(cls.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(data()))
        cls.store = Store(str(p))
        prov = auth.make_provider(cls.store, "pw")
        old = {k: os.environ.get(k) for k in cls.ENV}
        os.environ.update(cls.ENV)
        try:
            cls.app = App(cls.store, "pw", provider=prov)
        finally:
            for k, v in old.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(cls.app))
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmp.cleanup()

    def login(self, email):
        req = urllib.request.Request(self.base + "/api/login", json.dumps(dict(email=email, password="pw")).encode())
        return urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0]

    def call(self, ck, path, body=None):
        req = urllib.request.Request(self.base + path, json.dumps(body).encode() if body is not None else None, headers={"Cookie": ck})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read() or b"{}"), r.headers
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}"), e.headers


class ScreensApi(Base):
    def test_closed_list_is_manager_only_and_reopen_works(self):
        sam, pam = self.login("sam@example.test"), self.login("pam@example.test")
        self.assertEqual(self.call(sam, "/api/cases?view=closed")[0], 403)
        self.assertEqual(self.call(self.login("kim@example.test"), "/api/cases?view=closed")[0], 403)
        st, d, _ = self.call(pam, "/api/cases?view=closed")
        self.assertEqual((st, d["total"], [r["id"] for r in d["items"]]), (200, 1, ["ZF-9"]))
        self.assertEqual(self.call(sam, "/api/cases/ZF-9/reopen", {"reason": "x"})[0], 403)
        self.assertEqual(self.call(pam, "/api/cases/ZF-9/reopen", {"reason": ""})[0], 400)
        st, d, _ = self.call(pam, "/api/cases/ZF-9/reopen", {"reason": "Aftercare fault"})
        self.assertEqual((st, d["closed"], d["stage"]), (200, False, "Aftercare issue"))
        self.assertEqual(self.call(pam, "/api/cases?view=closed")[1]["total"], 0)

    def test_handoff_and_hazard_states_reach_the_case_card(self):
        sam, pam = self.login("sam@example.test"), self.login("pam@example.test")
        st, d, _ = self.call(sam, "/api/cases/ZF-1/offer-handoff", {"to": "pam@example.test", "note": "cover"})
        self.assertEqual((st, d["handoff"]["state"]), (200, "Offered"))
        self.assertEqual(self.call(pam, "/api/handoffs")[1][0]["case_id"], "ZF-1")
        st, d, _ = self.call(pam, "/api/cases/ZF-1/decline-handoff", {"reason": ""})
        self.assertEqual(st, 400)
        self.assertEqual(self.call(pam, "/api/cases/ZF-1/decline-handoff", {"reason": "full"})[1]["handoff"]["state"], "Declined")
        st, d, _ = self.call(sam, "/api/cases/ZF-5/hazard-raise", {"category": "Electrical", "priority": "Routine", "note": "n"})
        self.assertEqual(st, 200)
        self.assertEqual(d["hazards"][-1]["released"], False)
        self.assertEqual(self.call(sam, "/api/cases/ZF-5/hazard-raise", {"category": "Nope", "priority": "Routine"})[0], 400)

    def test_contractor_sees_only_notice_and_contact_never_the_reason(self):
        kim = self.login("kim@example.test")
        st, d, _ = self.call(kim, "/api/cases?limit=100")
        self.assertEqual(st, 200)
        ids = {r["id"] for r in d["items"]}
        self.assertNotIn("ZF-2", ids)
        self.assertIn("ZF-1", ids)
        item = next(r for r in d["items"] if r["id"] == "ZF-1")
        self.assertTrue(item["needs_notice"])
        self.assertEqual(item["named_contact"], "Sam Example")
        for r in d["items"]:
            for banned in ("resident", "phone", "reasons", "rank", "focus", "owner", "hazard", "support"):
                self.assertNotIn(banned, r)
        _, detail, _ = self.call(kim, "/api/cases/ZF-1")
        blob = json.dumps([d, detail])
        for secret in (REASON, "Resident 0", "01000 000000", "priority_support", "adjustment"):
            self.assertNotIn(secret, blob)
        self.assertEqual(self.call(kim, "/api/cases/ZF-2")[0], 404)
        for path in ("/api/facets", "/api/stats", "/api/map", "/api/handoffs", "/api/docs/ZF-1/x", "/api/briefing"):
            self.assertEqual(self.call(kim, path)[0], 403, path)
        self.assertEqual(self.call(kim, "/api/cases/ZF-1/call", {"outcome": "x"})[0], 403)

    def test_contractor_cannot_search_by_resident_name(self):
        kim = self.login("kim@example.test")
        self.assertEqual(self.call(kim, "/api/cases?q=Resident%200")[1]["total"], 0)

    def test_document_endpoints_audit_and_refuse_contractor(self):
        import base64
        sam, kim = self.login("sam@example.test"), self.login("kim@example.test")
        raw = base64.b64encode(b"%PDF-1").decode()
        st, d, _ = self.call(sam, "/api/cases/ZF-3/upload", {"name": "epc.pdf", "kind": "EPC", "data": raw})
        self.assertEqual(st, 200)
        did = d["documents"][-1]["id"]
        req = urllib.request.Request(self.base + f"/api/docs/ZF-3/{did}", headers={"Cookie": sam})
        with urllib.request.urlopen(req) as r:
            self.assertEqual(r.read(), b"%PDF-1")
        self.assertEqual(self.call(kim, f"/api/docs/ZF-3/{did}")[0], 403)
        self.assertEqual(self.call(kim, "/api/cases/ZF-3/upload", {"name": "a.pdf", "data": raw})[0], 403)
        self.assertEqual(self.call(sam, "/api/cases/ZF-3/upload", {"name": "a.exe", "data": raw})[0], 400)
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertIn("upload_document", actions)
        self.assertIn("download_document", actions)


class MapListAndTiles(Base):
    ENV = {"ZF_TILE_URL": "https://tiles.example.org/{z}/{x}/{y}.png", "ZF_TILE_ATTRIBUTION": "Example Tiles"}

    def test_me_payload_carries_server_rendered_tile_config_and_csp_follows(self):
        st, d, h = self.call(self.login("sam@example.test"), "/api/me")
        self.assertEqual(d["map"], dict(tiles="https://tiles.example.org/{z}/{x}/{y}.png", attribution="Example Tiles"))
        self.assertIn("img-src 'self' data: blob: https://tiles.example.org;", h["Content-Security-Policy"])
        self.assertNotIn("openstreetmap", h["Content-Security-Policy"])

    def test_map_list_data_points_then_clusters(self):
        sam = self.login("sam@example.test")
        _, d, _ = self.call(sam, "/api/map")
        self.assertEqual(d["mode"], "points")
        self.assertEqual(d["total"], len(d["items"]))
        self.assertTrue(all({"id", "name", "kind"} <= set(p) for p in d["items"]))
        self.assertTrue(any(p["kind"] == "hazard" for p in d["items"]))
        from zava_forward.core import insights
        d = insights.map_view(self.store.cases.values(), {}, None, 8, cap=2)
        self.assertEqual(d["mode"], "clusters")
        self.assertEqual(sum(p["count"] for p in d["items"]), d["total"])
        _, narrow, _ = self.call(sam, "/api/map?bbox=53.99,-1.6,54.015,-1.4")
        self.assertLess(narrow["total"], d["total"])
        self.assertEqual(self.call(sam, "/api/map?bbox=bad")[0], 400)

    def test_front_end_wires_the_list_alternative_and_tile_config(self):
        js = (Path(__file__).resolve().parents[1] / "web" / "app.js").read_text()
        for needle in ("maplist", "me.map.tiles", "aria-live", "Show the map areas as a list"):
            self.assertIn(needle, js)


class ProductionTiles(Base):
    ENV = {"ZF_ENV": "production", "ZF_TILE_URL": ""}

    def test_production_without_url_loads_no_tiles(self):
        _, d, h = self.call(self.login("sam@example.test"), "/api/me")
        self.assertIsNone(d["map"]["tiles"])
        self.assertNotIn("tile.", h["Content-Security-Policy"])


if __name__ == "__main__":
    unittest.main()
