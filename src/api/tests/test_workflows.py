
from dataset import RESIDENT_BINDINGS, change_metadata, supplied_contract_fixture
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

import test_mvp
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import GateError, Store

STAFF = [dict(code="RLO-01", name="Sam Example", email="sam@example.test", role="Resident Liaison Officer"),
         dict(code="RLO-02", name="Rae Other", email="rae@example.test", role="Resident Liaison Officer"),
         dict(code="PM-01", name="Pam Lead", email="pam@example.test", role="Retrofit Programme Manager"),
         dict(code="BSL-01", name="Bea Safe", email="bea@example.test", role="Building Safety Liaison"),
         dict(code="BSL-02", name="Bo Safe", email="bo@example.test", role="Building Safety Liaison"),
         dict(code="CON-01", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Test Ltd")]
PROVENANCE = dict(source="Synthetic workflow report", next_action="Review the changed evidence")
HAZARD_SOURCE = dict(source="Synthetic report", aware_at="2026-01-01T10:00:00Z")
SENT = dict(evidence="Synthetic sending reference")


class Flows:
    def make(self, data, tmp):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = copy.deepcopy(test_mvp.DATA)
        d["staff"] = STAFF
        d["cases"].append(test_mvp.case("ZF-6", stage="Install booked", decision="Accepted", funding=True))
        d["cases"][-1]["appointments"].append(dict(type="Installation", date="2099-01-01", slot="AM", outcome="Booked", note="", who="Test Ltd", person="Kim Builder"))
        d["cases"].append(dict(test_mvp.case("ZF-7", stage="Completed"), closed=True))
        self.store = self.make(d, self.tmp.name)
        self.sam, self.rae, self.pam, self.bea, self.bo = STAFF[:5]

    def tearDown(self):
        self.tmp.cleanup()

    def stage(self, cid):
        return self.store.detail(cid)["stage"]

    def actions(self):
        return [e["action"] for e in self.store.audit_entries()]

    # return and reopen
    def test_return_needs_reason_and_earlier_stage(self):
        with self.assertRaises(ValueError):
            self.store.return_case(self.sam, "ZF-6", "Funding check", "")
        with self.assertRaises(ValueError):
            self.store.return_case(self.sam, "ZF-6", "Quality check", "later stage")
        self.store.return_case(self.sam, "ZF-6", "Final checks before ordering", "Funding changed", PROVENANCE)
        d = self.store.detail("ZF-6")
        self.assertEqual(d["stage"], "Final checks before ordering")
        self.assertEqual(d["appointments"][-1]["outcome"], "Cancelled")
        self.assertEqual(d["returns"][-1]["reason"], "Funding changed")
        self.assertIn("return_case", self.actions())

    def test_return_to_resident_stage_resets_decision(self):
        self.store.return_case(self.sam, "ZF-6", "Contacting resident", "Resident changed mind", PROVENANCE)
        self.assertEqual(self.store.detail("ZF-6")["decision"]["status"], "Not yet asked")
        with self.assertRaises(ValueError):
            self.store.advance(self.sam, "ZF-6")

    def test_reopen_is_manager_only_and_only_closed(self):
        with self.assertRaises(PermissionError):
            self.store.reopen_case(self.sam, "ZF-7", "Damp returned")
        with self.assertRaises(ValueError):
            self.store.reopen_case(self.pam, "ZF-6", "x")
        with self.assertRaises(ValueError):
            self.store.reopen_case(self.pam, "ZF-7", " ")
        self.store.reopen_case(self.pam, "ZF-7", "Damp returned", PROVENANCE)
        d = self.store.detail("ZF-7")
        self.assertFalse(d["closed"])
        self.assertEqual(d["stage"], "Aftercare issue")
        with self.assertRaises(ValueError):
            self.store.return_case(self.sam, "ZF-7", "Contacting resident", "")

    # handoff
    def test_handoff_offer_accept(self):
        self.store.offer_handoff(self.sam, "ZF-1", "rae@example.test", "On leave", metadata=change_metadata(self.store, "ZF-1"))
        self.assertEqual(self.store.detail("ZF-1")["owner"], "Sam Example")
        self.assertEqual(self.store.pending_handoffs(self.rae)[0]["case_id"], "ZF-1")
        with self.assertRaises(PermissionError):
            self.store.accept_handoff(self.sam, "ZF-1", metadata=change_metadata(self.store, "ZF-1"))
        with self.assertRaises(ValueError):
            self.store.offer_handoff(self.sam, "ZF-1", "pam@example.test", metadata=change_metadata(self.store, "ZF-1"))
        self.store.accept_handoff(self.rae, "ZF-1", metadata=change_metadata(self.store, "ZF-1"))
        d = self.store.detail("ZF-1")
        self.assertEqual((d["owner"], d["handoff"]["state"], d["owner_code"]), ("Rae Other", "Accepted", "RLO-02"))
        self.assertEqual(self.store.pending_handoffs(self.rae), [])
        with self.assertRaises(ValueError):
            self.store.accept_handoff(self.rae, "ZF-1", metadata=change_metadata(self.store, "ZF-1"))

    def test_handoff_decline_withdraw_and_rules(self):
        with self.assertRaises(PermissionError):
            self.store.offer_handoff(self.rae, "ZF-1", "pam@example.test", metadata=change_metadata(self.store, "ZF-1"))
        with self.assertRaises(ValueError):
            self.store.offer_handoff(self.sam, "ZF-1", "kim@example.test", metadata=change_metadata(self.store, "ZF-1"))
        with self.assertRaises(ValueError):
            self.store.offer_handoff(self.sam, "ZF-1", "sam@example.test", metadata=change_metadata(self.store, "ZF-1"))
        self.store.offer_handoff(self.sam, "ZF-1", "rae@example.test", metadata=change_metadata(self.store, "ZF-1"))
        with self.assertRaises(ValueError):
            self.store.decline_handoff(self.rae, "ZF-1", "")
        self.store.decline_handoff(self.rae, "ZF-1", "Full caseload")
        d = self.store.detail("ZF-1")
        self.assertEqual((d["owner"], d["handoff"]["state"]), ("Sam Example", "Declined"))
        self.store.offer_handoff(self.pam, "ZF-1", "rae@example.test", metadata=change_metadata(self.store, "ZF-1"))
        with self.assertRaises(ValueError):
            self.store.offer_handoff(self.sam, "ZF-1", "rae@example.test", metadata=change_metadata(self.store, "ZF-1"))
        with self.assertRaises(PermissionError):
            self.store.withdraw_handoff(self.rae, "ZF-1")
        self.store.withdraw_handoff(self.sam, "ZF-1")
        self.assertEqual(self.store.detail("ZF-1")["handoff"]["state"], "Withdrawn")
        self.assertEqual(len(self.store.detail("ZF-1")["handoff_log"]), 2)

    # safety referral
    def test_safety_flow_blocks_booking_until_released_by_someone_else(self):
        i = self.store.raise_hazard(self.sam, "ZF-3", "Damp and mould", "Emergency", "Black mould", HAZARD_SOURCE)
        self.assertIn("safety_emergency", self.actions())
        self.assertTrue(self.store.status_line(self.store.cases["ZF-3"]).startswith("Stopped"))
        with self.assertRaises(GateError):
            self.store.advance(self.sam, "ZF-3")
        with self.assertRaises(ValueError):
            self.store.record_repair(self.bea, "ZF-3", i)
        with self.assertRaises(ValueError):
            self.store.refer_hazard(self.sam, "ZF-3", i, "rae@example.test", "J1")
        with self.assertRaises(ValueError):
            self.store.refer_hazard(self.sam, "ZF-3", i, "bea@example.test", "")
        self.store.refer_hazard(self.sam, "ZF-3", i, "bea@example.test", "J-100", SENT)
        with self.assertRaises(ValueError):
            self.store.refer_hazard(self.sam, "ZF-3", i, "bea@example.test", "J-100")
        with self.assertRaises(ValueError):
            self.store.release_hazard(self.bea, "ZF-3", i)
        self.store.receive_hazard(self.bea, "ZF-3", i, "Synthetic receipt")
        self.store.accept_hazard(self.bea, "ZF-3", i, "Synthetic acceptance")
        self.store.record_repair(self.bea, "ZF-3", i, "Synthetic repair report")
        with self.assertRaises(PermissionError):
            self.store.release_hazard(self.sam, "ZF-3", i)
        self.assertEqual(self.store.hazard_states("ZF-3")[i]["state"], "Repair evidenced, hold active")
        self.store.release_hazard(self.bo, "ZF-3", i, "Checked on site", "Synthetic clearance")
        self.assertEqual(self.store.hazard_states("ZF-3")[i]["state"], "Retrofit hold released")
        pid = self.store.create_package(self.pam, "SYN", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1")
        details = supplied_contract_fixture(self.store, pid, self.pam)
        self.store.set_capacity(self.pam, pid, "Test Ltd", 1, 1, "SYN commitment", details)
        wid = self.store.issue_work_order(self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
        self.store.advance(self.sam, "ZF-3")
        self.assertEqual(self.stage("ZF-3"), "Install booked")
        for a in ("safety_raised", "safety_referred", "safety_repaired", "safety_released"):
            self.assertIn(a, self.actions())

    def test_raiser_cannot_release_own_issue(self):
        i = self.store.raise_hazard(self.bea, "ZF-3", "Electrical", "Routine", metadata=HAZARD_SOURCE)
        self.store.refer_hazard(self.bea, "ZF-3", i, "bo@example.test", "J-5", SENT)
        self.store.receive_hazard(self.bo, "ZF-3", i, "Synthetic receipt")
        self.store.accept_hazard(self.bo, "ZF-3", i, "Synthetic acceptance")
        self.store.record_repair(self.bo, "ZF-3", i, "Synthetic repair report")
        with self.assertRaises(PermissionError):
            self.store.release_hazard(self.bea, "ZF-3", i, "Reason", "Synthetic clearance")
        self.store.release_hazard(self.pam, "ZF-3", i, "Reason", "Synthetic clearance")

    def test_hazard_inputs_validated(self):
        with self.assertRaises(ValueError):
            self.store.raise_hazard(self.sam, "ZF-3", "Made up", "Routine")
        with self.assertRaises(ValueError):
            self.store.release_hazard(self.bea, "ZF-3", 5)
        self.assertTrue(self.store.ledger_head()[0] == 0 and self.store.verify_audit())

    def test_chain_intact_after_all_flows(self):
        self.store.offer_handoff(self.sam, "ZF-1", "rae@example.test", metadata=change_metadata(self.store, "ZF-1"))
        self.store.accept_handoff(self.rae, "ZF-1", metadata=change_metadata(self.store, "ZF-1"))
        self.store.return_case(self.rae, "ZF-6", "Funding check", "Evidence gap", PROVENANCE)
        self.assertTrue(self.store.verify_audit())


class JsonFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return Store(str(p))


class SqlFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))


class RouteTests(unittest.TestCase):
    def test_routes_are_wired_and_enforce_roles(self):
        import threading
        import urllib.error
        import urllib.request
        from http.server import ThreadingHTTPServer
        from zava_forward.api.server import App, make_handler
        with tempfile.TemporaryDirectory() as tmp:
            d = copy.deepcopy(test_mvp.DATA)
            d["staff"] = STAFF
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(d))
            store = Store(str(p))
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "zf-test")))
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            base = f"http://127.0.0.1:{httpd.server_address[1]}"

            def call(email, path, body=None):
                if body is not None and path.rsplit("/", 1)[-1] in ("offer-handoff", "accept-handoff"):
                    body = {**change_metadata(store), **body}
                req = urllib.request.Request(base + "/api/login", json.dumps(dict(email=email, password="zf-test")).encode())
                ck = urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0]
                req = urllib.request.Request(base + path, json.dumps(body).encode() if body is not None else None, headers={"Cookie": ck})
                try:
                    with urllib.request.urlopen(req) as r:
                        return r.status, json.loads(r.read())
                except urllib.error.HTTPError as e:
                    return e.code, json.loads(e.read())
            try:
                self.assertEqual(call("sam@example.test", "/api/cases/ZF-1/offer-handoff", {"to": "rae@example.test"})[0], 200)
                self.assertEqual(call("sam@example.test", "/api/cases/ZF-1/accept-handoff", {})[0], 403)
                self.assertEqual(call("rae@example.test", "/api/handoffs")[1][0]["case_id"], "ZF-1")
                self.assertEqual(call("rae@example.test", "/api/cases/ZF-1/accept-handoff", {})[1]["owner"], "Rae Other")
                self.assertEqual(call("rae@example.test", "/api/cases/ZF-1/hazard-raise", dict(category="Structural", priority="Routine", **HAZARD_SOURCE))[0], 200)
                self.assertEqual(call("rae@example.test", "/api/cases/ZF-1/hazard-release", {"index": 0})[0], 403)
                self.assertEqual(call("pam@example.test", "/api/cases/ZF-1/return", {"to_stage": "Contacting resident", "reason": ""})[0], 400)
                self.assertEqual(call("kim@example.test", "/api/cases/ZF-1/offer-handoff", {"to": "sam@example.test"})[0], 403)
            finally:
                httpd.shutdown()
                httpd.server_close()
