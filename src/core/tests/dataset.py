"""Shared constructed dataset and store behaviour cases (moved from mvp/tests/test_mvp.py in M2 of #199)."""
import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.store import Store
from zava_forward.core.workflows import _today


def supplied_contract_fixture(store: Any, pid: str, manager: dict[str, Any], contractor: str = "Test Ltd") -> dict[str, Any]:
    """Explicit fictional delegation and original commitment bytes, never production seeding."""
    with store.lock:
        p = store._package(pid)
        p["contract_version"] = "SYN-1"
        actor = store.staff[manager["email"]]
        authority = dict(reference="SYN-DELEGATION", version="1", contract_ref=p["contract_ref"],
                         contract_version="SYN-1", revoked=False, valid_from="2026-01-01", valid_to="2099-12-31",
                         actions=["rescope", "capacity", "issue", "reissue", "appointment", "complete", "correct", "withdraw"],
                         suppliers=[contractor], scope_versions=[1, 2])
        actor.setdefault("contract_authorities", []).append(authority)
        if hasattr(store, "db"):
            store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(actor), actor["email"]))
        ids = [cid for cid, c in store.cases.items() if c["contractor"]["name"] == contractor]
        c = store._case(ids[0])
        content = b"SYNTHETIC ONLY: accepted one-home-order package quota; no real instruction or legal authority."
        doc_id = "SYN-COMMITMENT"
        doc = dict(id=doc_id, name="synthetic-commitment.txt", kind="Other", version="1",
                   content_sha256=hashlib.sha256(content).hexdigest(), at=_today(),
                   scan=dict(status="clean", scanner="Synthetic fixture"))
        c["documents"] = [d for d in c["documents"] if d["id"] != doc_id] + [doc]
        store.docstore.put(c["id"], doc_id, content, "text/plain")
        store.save()
        return dict(source_case_id=c["id"], document_id=doc_id, source_version="1",
                    source_date=_today(), reviewed_on=_today(), valid_from=p["period_from"],
                    valid_to=p["period_to"], unit="home-work-order", case_ids=ids, status="Committed")


def change_metadata(store: Any, cid: str = "ZF-1") -> dict[str, Any]:
    """Explicit test-only caller inputs, not production metadata defaults."""
    with store.lock:
        return dict(source="SYN fixture supplied register", source_version="fixture-1",
                    reason="Synthetic test operation",
                    handoff_version=len(store.cases[cid].get("handoff_history", [])))


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

RESIDENT_BINDINGS = [dict(measure="Loft insulation", context_revision=1)]


def supplied_resident_fixture(c: dict[str, Any]) -> None:
    """Explicit constructed source/design/answer fixture, never a generator backfill."""
    c["technical"] = dict(design_version=1, signoffs={
        key: dict(status="Signed off") for key in ("assessment", "design", "building", "coordination")})
    c["documents"] = [dict(id=f"SYN-{kind}", kind=kind, name=f"SYN-{kind}.pdf", at="2026-01-01",
                           by="Synthetic reviewer", scan=dict(status="clean", scanner="Synthetic metadata fixture"))
                      for kind in Store.EVIDENCE]
    c["resident_scopes"] = {"Loft insulation": [dict(
        revision=1, case_id=c["id"], measure="Loft insulation", scope="SYN-LOFT",
        design_version=1, source="SYN-SCOPE", recorded_by="sam@example.test", at="2026-01-01")]}
    c["measure_decisions"] = {"Loft insulation": [dict(
        version=1, context_revision=1, status="Accepted", answered_by="The resident",
        case_id=c["id"], measure="Loft insulation", scope="SYN-LOFT", design_version=1,
        source="SYN-SUPPLIED-RESIDENT-ANSWER", recorded_by="Sam Example",
        recorded_by_email="sam@example.test", at="2026-01-01")]}


supplied_resident_fixture(DATA["cases"][2])


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
            self.store.add_document(self.sam, "ZF-1", "x.exe", "EPC", b"abc", metadata=change_metadata(self.store, "ZF-1"))
        self.store.add_document(self.sam, "ZF-1", "epc.pdf", "EPC", b"%PDF", metadata=change_metadata(self.store, "ZF-1"))
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
            self.store.add_document(self.sam, "ZF-1", "a.pdf", k, b"%PDF-x", metadata=change_metadata(self.store, "ZF-1"))
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
