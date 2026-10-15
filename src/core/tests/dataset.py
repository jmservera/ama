"""Shared constructed dataset and store behaviour cases (moved from mvp/tests/test_mvp.py in M2 of #199)."""
import json
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.store import Store


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
    cases=[case("ZF-1"), case("ZF-2", stage="Final checks before ordering"),
           case("ZF-3", stage="Final checks before ordering", decision="Accepted", funding=True),
           case("ZF-4", hazards=[dict(category="Damp", priority="P1", noticed="2026-01-01", referred=None,
                                      repaired=None, released=False, job="J1", owner="Bea Safe")]),
           case("ZF-5", owner_code="PM-01")])


class ImproveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(DATA))
        self.store = Store(str(p))
        self.sam, self.pam = DATA["staff"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_filter_and_sort(self):
        rows = self.store.list_cases(self.pam, "all", filters={"flag": "hazard"})
        self.assertEqual([r["id"] for r in rows], ["ZF-4"])
        rows = self.store.list_cases(self.pam, "all", filters={"stage": "Final checks before ordering"}, sort="name")
        self.assertEqual(len(rows), 2)

    def test_stats_and_map(self):
        st = self.store.stats()
        self.assertEqual(st["kpis"]["open"], 5)
        self.assertEqual(st["kpis"]["hazards"], 1)
        self.assertEqual(len(self.store.map_points({})), 5)

    def test_handover_suggestions_have_reasons(self):
        s = self.store.detail("ZF-1")["suggestions"]
        self.assertTrue(s and s[0]["reasons"])

    def test_upload_rejects_bad_type_and_lists_document(self):
        with self.assertRaises(ValueError):
            self.store.add_document(self.sam, "ZF-1", "x.exe", "EPC", b"abc")
        self.store.add_document(self.sam, "ZF-1", "epc.pdf", "EPC", b"%PDF")
        d = self.store.detail("ZF-1")
        self.assertTrue(next(x for x in d["checklist"] if x["kind"] == "EPC")["present"])
        self.assertEqual(self.store.get_document("ZF-1", d["documents"][0]["id"])[1], "application/pdf")

    def test_funding_needs_evidence_and_role(self):
        self.store.funding_draft(self.sam, "ZF-1")
        with self.assertRaises(PermissionError):
            self.store.funding_step(self.sam, "ZF-1", "approve")
        from zava_forward.core.store import GateError
        with self.assertRaises(GateError):
            self.store.funding_step(self.pam, "ZF-1", "approve")
        for k in ("EPC", "Survey", "Design", "Consent"):
            self.store.add_document(self.sam, "ZF-1", "a.pdf", k, b"%PDF-x")
        self.store.funding_step(self.pam, "ZF-1", "approve")
        with self.assertRaises(ValueError):
            self.store.funding_step(self.pam, "ZF-1", "submit", "")
        self.store.funding_step(self.pam, "ZF-1", "submit", "REF-1")
        self.store.funding_step(self.pam, "ZF-1", "confirm")
        self.assertTrue(self.store.detail("ZF-1")["funding_ok"])

    def test_briefing_cached_until_data_changes(self):
        calls = []
        self.store.ai.endpoint = "http://x"
        self.grant()
        self.store.ai._chat = lambda *a, **k: calls.append(1) or "All good today."
        self.store.briefing(self.sam)
        self.store.briefing(self.sam)
        self.assertEqual(len(calls), 1)
        self.store.log_call(self.sam, "ZF-1", "Spoke", "")
        self.store.briefing(self.sam)
        self.assertEqual(len(calls), 2)

    def test_funding_in_progress_filter(self):
        self.store.funding_draft(self.sam, "ZF-1")
        ids = [p["id"] for p in self.store.map_points({"flag": "fundingprog"})]
        self.assertEqual(ids, ["ZF-1"])

    def grant(self):
        if hasattr(self.store, "assistant_connection"):
            import release_support
            release_support.install(self.store)

    def test_ai_falls_back_to_template_and_is_audited(self):
        r = self.store.ai_run(self.sam, "ZF-1", "message")
        self.assertEqual(r["source"], "template")
        self.assertTrue(self.store.verify_audit())

    def test_ai_output_claiming_sent_is_rejected(self):
        ai = self.store.ai
        ai.endpoint = "http://x"
        self.grant()
        ai._chat = lambda *a, **k: "I have sent the letter."
        r = self.store.ai_run(self.sam, "ZF-1", "message")
        self.assertEqual(r["source"], "template")
        self.assertFalse(r["validated"])
