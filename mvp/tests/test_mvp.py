import json
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from properwarm_mvp.server import App, make_handler
from properwarm_mvp.store import Store


def case(cid, owner_code="RLO-01", stage="Contacting resident", decision="Waiting", funding=False, hazards=()):
    return dict(
        id=cid, wave="Wave 1", closed=False, stage=stage, stage_since="2026-01-01", days_in_stage=10,
        waiting_on="Sam Example", reason="to agree a visit", owner_code=owner_code, owner="Sam Example",
        owner_role="Resident Liaison Officer",
        resident=dict(title="Ms", name="Pat Test", formal="Ms Test", phone="01000 000000", email="", preferred="Phone",
                      adjustment="None", priority_support=False, unavailable="", representative=None),
        home=dict(address="1 Test Road", town="Testville", postcode="TE1 1ST", area="Test", type="Mid terrace",
                  built=1950, epc="D", tenure="Social rent", lat=0, lon=0),
        measures="Loft insulation", contractor=dict(name="Test Ltd", phone="0", scope="x", contact="Kim Builder"),
        decision=dict(status=decision, by=None, at=None), funding_ok=funding, contacts=[], appointments=[],
        hazards=list(hazards), history=[])


DATA = dict(
    staff=[dict(code="RLO-01", name="Sam Example", email="sam@example.test", role="Resident Liaison Officer"),
           dict(code="PM-01", name="Pam Lead", email="pam@example.test", role="Retrofit Programme Manager")],
    cases=[case("PW-1"), case("PW-2", stage="Final checks before ordering"),
           case("PW-3", stage="Final checks before ordering", decision="Accepted", funding=True),
           case("PW-4", hazards=[dict(category="Damp", priority="P1", noticed="2026-01-01", referred=None,
                                      repaired=None, released=False, job="J1", owner="Bea Safe")]),
           case("PW-5", owner_code="PM-01")])


class ImproveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(DATA))
        self.store = Store(str(p))
        self.sam, self.pam = DATA["staff"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_filter_and_sort(self):
        rows = self.store.list_cases(self.pam, "all", filters={"flag": "hazard"})
        self.assertEqual([r["id"] for r in rows], ["PW-4"])
        rows = self.store.list_cases(self.pam, "all", filters={"stage": "Final checks before ordering"}, sort="name")
        self.assertEqual(len(rows), 2)

    def test_stats_and_map(self):
        st = self.store.stats()
        self.assertEqual(st["kpis"]["open"], 5)
        self.assertEqual(st["kpis"]["hazards"], 1)
        self.assertEqual(len(self.store.map_points({})), 5)

    def test_handover_suggestions_have_reasons(self):
        s = self.store.detail("PW-1")["suggestions"]
        self.assertTrue(s and s[0]["reasons"])

    def test_upload_rejects_bad_type_and_lists_document(self):
        with self.assertRaises(ValueError):
            self.store.add_document(self.sam, "PW-1", "x.exe", "EPC", b"abc")
        self.store.add_document(self.sam, "PW-1", "epc.pdf", "EPC", b"%PDF")
        d = self.store.detail("PW-1")
        self.assertTrue(next(x for x in d["checklist"] if x["kind"] == "EPC")["present"])
        self.assertEqual(self.store.get_document("PW-1", d["documents"][0]["id"])[1], "application/pdf")

    def test_funding_needs_evidence_and_role(self):
        self.store.funding_draft(self.sam, "PW-1")
        with self.assertRaises(PermissionError):
            self.store.funding_step(self.sam, "PW-1", "approve")
        from properwarm_mvp.store import GateError
        with self.assertRaises(GateError):
            self.store.funding_step(self.pam, "PW-1", "approve")
        for k in ("EPC", "Survey", "Design", "Consent"):
            self.store.add_document(self.sam, "PW-1", "a.pdf", k, b"x")
        self.store.funding_step(self.pam, "PW-1", "approve")
        with self.assertRaises(ValueError):
            self.store.funding_step(self.pam, "PW-1", "submit", "")
        self.store.funding_step(self.pam, "PW-1", "submit", "REF-1")
        self.store.funding_step(self.pam, "PW-1", "confirm")
        self.assertTrue(self.store.detail("PW-1")["funding_ok"])

    def test_briefing_cached_until_data_changes(self):
        calls = []
        self.store.ai.endpoint = "http://x"
        self.store.ai._chat = lambda *a, **k: calls.append(1) or "All good today."
        self.store.briefing(self.sam)
        self.store.briefing(self.sam)
        self.assertEqual(len(calls), 1)
        self.store.log_call(self.sam, "PW-1", "Spoke", "")
        self.store.briefing(self.sam)
        self.assertEqual(len(calls), 2)

    def test_funding_in_progress_filter(self):
        self.store.funding_draft(self.sam, "PW-1")
        ids = [p["id"] for p in self.store.map_points({"flag": "fundingprog"})]
        self.assertEqual(ids, ["PW-1"])

    def test_ai_falls_back_to_template_and_is_audited(self):
        r = self.store.ai_run(self.sam, "PW-1", "message")
        self.assertEqual(r["source"], "template")
        self.assertTrue(self.store.verify_audit())

    def test_ai_output_claiming_sent_is_rejected(self):
        ai = self.store.ai
        ai.endpoint = "http://x"
        ai._chat = lambda *a, **k: "I have sent the letter."
        r = self.store.ai_run(self.sam, "PW-1", "message")
        self.assertEqual(r["source"], "template")
        self.assertFalse(r["validated"])


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(DATA))
        self.store = Store(str(p))
        self.sam = DATA["staff"][0]
        self.pam = DATA["staff"][1]

    def tearDown(self):
        self.tmp.cleanup()

    def test_my_cases_hazard_first_and_scoped(self):
        rows = self.store.list_cases(self.sam)
        self.assertEqual({r["id"] for r in rows}, {"PW-1", "PW-2", "PW-3", "PW-4"})
        self.assertEqual(rows[0]["id"], "PW-4")
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
        from properwarm_mvp.store import GateError
        with self.assertRaises(GateError) as ctx:
            self.store.advance(self.sam, "PW-2")
        self.assertEqual(len(ctx.exception.reasons), 2)
        self.store.advance(self.sam, "PW-3")
        self.assertEqual(self.store.detail("PW-3")["stage"], "Install booked")

    def test_unknown_decision_is_rejected_and_never_inferred(self):
        with self.assertRaises(ValueError):
            self.store.set_decision(self.sam, "PW-1", "Probably")
        self.assertEqual(self.store.detail("PW-1")["decision"]["status"], "Waiting")

    def test_call_log_and_audit_chain_detects_tampering(self):
        self.store.log_call(self.sam, "PW-1", "Spoke to resident", "Visit agreed")
        self.store.set_decision(self.sam, "PW-1", "Accepted")
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
        self.assertIn("Nothing is sent", self.store.draft("PW-1", "visit")["note"])

    def test_csv_export_has_header(self):
        self.assertTrue(self.store.export_csv(self.store.list_cases(self.sam)).startswith("Reference,"))


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(DATA))
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(Store(str(p)), "pw-test")))
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
        code, _, hdr = self.call("/api/login", {"email": "sam@example.test", "password": "pw-test"})
        self.assertEqual(code, 200)
        cookie = hdr["Set-Cookie"].split(";")[0]
        self.assertIn("HttpOnly", hdr["Set-Cookie"])
        code, body, _ = self.call("/api/cases", cookie=cookie)
        self.assertEqual(len(json.loads(body)["items"]), 4)
        code, body, _ = self.call("/api/cases/PW-2/advance", {}, cookie)
        self.assertEqual(code, 409)
        self.assertEqual(len(json.loads(body)["reasons"]), 2)

    def test_static_path_traversal_blocked(self):
        self.assertEqual(self.call("/..%2f..%2fREADME.md")[0], 404)


if __name__ == "__main__":
    unittest.main()
