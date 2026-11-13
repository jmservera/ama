import json
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from dataset import DATA as DATA
from dataset import supplied_appointment_fixture
from dataset import ImproveTests, case  # noqa: F401  shared fixtures live in src/core/tests (M2 of #199)
from zava_forward.core.store import Store
from zava_forward.api import server
from zava_forward.api.server import App, make_handler


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(DATA))
        self.store = Store(str(p))
        self.sam = DATA["staff"][0]
        self.pam = DATA["staff"][1]

    def tearDown(self):
        self.tmp.cleanup()

    def test_my_cases_hazard_first_and_scoped(self):
        rows = self.store.list_cases(self.sam)
        self.assertEqual({r["id"] for r in rows}, {"ZF-1", "ZF-2", "ZF-3", "ZF-4"})
        self.assertEqual(rows[0]["id"], "ZF-4")
        self.assertTrue(rows[0]["status"].startswith("Stopped until Bea Safe"))

    def test_all_cases_open_to_everyone_mine_is_scoped_with_role_focus(self):
        self.assertEqual(len(self.store.list_cases(self.pam, "all")), 5)
        self.assertEqual(len(self.store.list_cases(self.sam, "all")), 5)
        self.assertNotIn("focus", self.store.list_cases(self.sam, "all")[0])
        mine = self.store.list_cases(self.sam)
        self.assertEqual(len(mine), 4)
        self.assertTrue(all(r["focus"] for r in mine))
        self.assertNotEqual(mine[0]["focus"], self.store.list_cases(self.pam)[0]["focus"])

    def test_gate_blocks_until_everything_confirmed(self):
        from zava_forward.core.store import GateError
        with self.assertRaises(GateError) as ctx:
            self.store.advance(self.sam, "ZF-2")
        self.assertEqual(len(ctx.exception.reasons), 2)
        from dataset import RESIDENT_BINDINGS, supplied_contract_fixture
        pid = self.store.create_package(self.pam, "SYN", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1")
        details = supplied_contract_fixture(self.store, pid, self.pam)
        self.store.set_capacity(self.pam, pid, "Test Ltd", 1, 1, "SYN-CAPACITY", details)
        wid = self.store.issue_work_order(self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        supplied_appointment_fixture(self.store, self.pam, wid)
        self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
        self.store.advance(self.sam, "ZF-3")
        self.assertEqual(self.store.detail("ZF-3")["stage"], "Install booked")

    def test_unknown_decision_is_rejected_and_never_inferred(self):
        with self.assertRaises(ValueError):
            self.store.set_decision(self.sam, "ZF-1", "Probably")
        self.assertEqual(self.store.detail("ZF-1")["decision"]["status"], "Waiting")

    def test_call_log_and_audit_chain_detects_tampering(self):
        self.store.log_call(self.sam, "ZF-1", "Spoke to resident", "Visit agreed")
        self.store.set_decision(self.sam, "ZF-1", "Accepted")
        self.assertTrue(self.store.verify_audit())
        lines = Path(self.store.audit_path).read_text().splitlines()
        lines[0] = lines[0].replace("Spoke to resident", "Nothing")
        Path(self.store.audit_path).write_text("\n".join(lines) + "\n")
        self.assertFalse(self.store.verify_audit())

    def test_import_check_maps_columns_and_reports_rows(self):
        r = self.store.import_check("Tenant Name,Address,Post Code,Mobile\nA B,1 X St,TE1 1ST,07\n,2 Y St,bad,07\n")
        self.assertEqual(r["ready"], 1)
        self.assertEqual(r["matched_existing"], 1)
        self.assertEqual(r["to_fix"][0]["row"], 3)

    def test_draft_never_claims_it_was_sent(self):
        self.assertIn("Nothing is sent", self.store.draft("ZF-1", "visit")["note"])

    def test_csv_export_has_header(self):
        self.assertTrue(self.store.export_csv(self.store.list_cases(self.sam)).startswith("Reference,"))


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(DATA))
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(Store(str(p)), "zf-test")))
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def call(self, path, body=None, cookie=None):
        req = urllib.request.Request(self.base + path, data=None if body is None else json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", **({"Cookie": cookie} if cookie else {})})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read(), r.headers
        except urllib.error.HTTPError as e:
            return e.code, e.read(), e.headers

    def test_requires_sign_in_and_headers(self):
        self.assertEqual(self.call("/api/cases")[0], 401)
        code, _, hdr = self.call("/")
        self.assertEqual(code, 200)
        self.assertIn("frame-ancestors", hdr["Content-Security-Policy"])

    def test_login_flow_and_gate_conflict(self):
        self.assertEqual(self.call("/api/login", {"email": "sam@example.test", "password": "wrong"})[0], 401)
        code, _, hdr = self.call("/api/login", {"email": "sam@example.test", "password": "zf-test"})
        self.assertEqual(code, 200)
        cookie = hdr["Set-Cookie"].split(";")[0]
        self.assertIn("HttpOnly", hdr["Set-Cookie"])
        code, body, _ = self.call("/api/cases", cookie=cookie)
        self.assertEqual(len(json.loads(body)["items"]), 4)
        code, body, _ = self.call("/api/cases/ZF-2/advance", {}, cookie)
        self.assertEqual(code, 409)
        self.assertEqual(len(json.loads(body)["reasons"]), 2)

    def test_stale_advance_refusal_names_case_owner_and_next_action(self):
        from dataset import RESIDENT_BINDINGS, supplied_contract_fixture
        store = Store(str(Path(self.tmp.name) / "zavaforward.json"))
        pam = DATA["staff"][1]
        pid = store.create_package(pam, "SYN", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1")
        details = supplied_contract_fixture(store, pid, pam)
        store.set_capacity(pam, pid, "Test Ltd", 1, 1, "SYN-CAPACITY", details)
        wid = store.issue_work_order(pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        supplied_appointment_fixture(store, pam, wid)
        store.record_wo_appointment(pam, wid, "Booked", "2099-01-01")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "zf-test")))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        self.base = f"http://127.0.0.1:{httpd.server_address[1]}"

        def sign_in(email):
            return self.call("/api/login", {"email": email, "password": "zf-test"})[2]["Set-Cookie"].split(";")[0]

        first, second = sign_in("sam@example.test"), sign_in("pam@example.test")
        self.assertEqual(self.call("/api/cases/ZF-3/advance", {}, second)[0], 200)
        events = len(store.cases["ZF-3"]["returns"])
        for case_id, owner in (("ZF-3", "Sam Example"), ("ZF-1", "Sam Example")):
            code, body, _ = self.call(f"/api/cases/{case_id}/advance", {}, first)
            payload = json.loads(body)
            self.assertEqual(code, 400)
            self.assertNotIn("reasons", payload)
            self.assertTrue(payload["error"].startswith("This case is not at the final checks. It may have changed since you opened it."))
            self.assertIn(f"Case owner: {owner}.", payload["error"])
            self.assertIn("Next action: copy any unsaved notes, then reload the case and check its current stage", payload["error"])
        self.assertEqual(store.cases["ZF-3"]["stage"], "Install booked")
        self.assertEqual(len(store.cases["ZF-3"]["returns"]), events)

    def test_advance_with_missing_funding_is_a_funding_conflict_not_a_missing_case(self):
        import copy

        data = copy.deepcopy(DATA)
        for c in data["cases"]:
            if c["id"] == "ZF-3":
                del c["funding_ok"]
        p = Path(self.tmp.name) / "missing-funding.json"
        p.write_text(json.dumps(data))
        store = Store(str(p))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "zf-test")))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        self.base = f"http://127.0.0.1:{httpd.server_address[1]}"
        _, _, hdr = self.call("/api/login", {"email": "sam@example.test", "password": "zf-test"})
        cookie = hdr["Set-Cookie"].split(";")[0]
        code, body, _ = self.call("/api/cases/ZF-3/advance", {}, cookie)
        self.assertEqual(code, 409)
        out = json.loads(body)
        self.assertEqual(out["error"], "Not ready yet.")
        self.assertTrue(any("Funding has not been confirmed" in r for r in out["reasons"]))
        self.assertEqual(store.cases["ZF-3"]["stage"], "Final checks before ordering")

    def test_static_path_traversal_blocked(self):
        self.assertEqual(self.call("/..%2f..%2fREADME.md")[0], 404)

    def test_header_logo_is_served_as_the_packaged_png(self):
        code, html, _ = self.call("/")
        self.assertEqual(code, 200)
        self.assertRegex(html, rb'src="/zava-logo\.png\?v=[0-9a-f]{64}"')
        code, body, headers = self.call("/zava-logo.png")
        self.assertEqual(code, 200)
        self.assertEqual(headers["Content-Type"], "image/png")
        self.assertTrue(body.startswith(b"\x89PNG\r\n\x1a\n"))
        expected = Path(server.__file__).resolve().parent / "web" / "zava-logo.png"
        self.assertEqual(body, expected.read_bytes())


if __name__ == "__main__":
    unittest.main()
