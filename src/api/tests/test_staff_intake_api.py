"""Actual HTTP controls for the staff-mediated synthetic field-evidence intake (#132)."""

import json
import os
import unittest
import uuid
from pathlib import Path
from typing import Any
from unittest import mock

from dataset import supplied_appointment_fixture

from test_procurement_api import ProcurementApiFixture

ROUTE = "/api/workorders/WO-0001/"
WORKER = "Wren Fictional"
OMIT = object()
LOFT = [
    "Depth measured and photo taken",
    "Ventilation at the eaves kept clear",
    "Hatch insulated and sealed",
    "Pipes and tanks protected",
    "Cables and lights checked",
]


def notes(prefix: str = "Seen") -> dict[str, str]:
    return {label: f"{prefix}: {label[:12].strip()}" for label in LOFT}


class StaffIntakeApi(ProcurementApiFixture):
    def setUp(self) -> None:
        super().setUp()
        self.assertEqual(self.call(f"/api/packages/{self.pid}/capacity", self.capacity())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 200)
        supplied_appointment_fixture(self.store, self.manager, "WO-0001", "2099-01-01")
        self.assertEqual(
            self.call(ROUTE + "appointment", dict(outcome="Booked", date="2099-01-01"))[0], 200
        )

    def body(self, **over: Any) -> dict[str, Any]:
        base: dict[str, Any] = dict(
            measure="Loft insulation",
            notes=notes(),
            confirmed_by=WORKER,
            confirmed=True,
            capture_ref="SYN-CAPTURE-0001",
        )
        base.update(over)
        return base

    def capture(self, actor: str = "sam", **over: Any) -> tuple[int, Any]:
        body = self.body(**over)
        if "pack_digest" not in over:
            body["pack_digest"] = self.view(actor)["pack"]["pack_digest"]
        elif over["pack_digest"] is OMIT:
            del body["pack_digest"]
        return self.call(ROUTE + "field-capture", body, actor)

    def accept(self, actor: str, record: int) -> tuple[int, Any]:
        return self.call(
            "/api/cases/ZF-3/quality-accept", dict(index=record, note="Synthetic"), actor
        )

    def correction(self, record: int, label: str = LOFT[0], note: str = "Corrected") -> dict:
        return dict(record=record, label=label, note=note, confirmed_by=WORKER, confirmed=True)

    def view(self, actor: str = "sam") -> dict[str, Any]:
        code, out = self.call(ROUTE + "field-intake", actor=actor)
        self.assertEqual(code, 200, out)
        return out

    def restart(self) -> None:
        self.store.save()
        if hasattr(self.store, "db"):
            self.store.db.close()
        self.store = self.reopen_store()
        self.app.store = self.store

    def test_capture_restart_readback_and_distinct_acknowledgement(self) -> None:
        pack = self.view()["pack"]
        self.assertTrue(pack["ready"])
        code, out = self.capture(pack_digest=pack["pack_digest"])
        self.assertEqual((code, out["outcome"]), (200, "recorded"))
        receipt = out["receipt"]
        self.assertEqual(receipt["original_notes"], notes())
        self.assertEqual(receipt["quality_state"], "Submitted")
        self.assertIsNone(receipt["acknowledgement"])
        self.assertFalse(receipt["accepted"])
        self.restart()
        back = self.view()["receipts"][0]
        self.assertEqual(back["original_notes"], notes())
        self.assertEqual(back["confirmed_by"], WORKER)
        self.assertEqual(back["recorded_by"], "Sam Example")
        code, ack = self.call(ROUTE + "field-acknowledge", dict(record=back["record"]), "pam")
        self.assertEqual(code, 200, ack)
        self.assertEqual(ack["receipt"]["status"], "Receipt acknowledged - not accepted")
        self.assertEqual(ack["receipt"]["quality_state"], "Submitted")
        self.assertEqual(ack["receipt"]["acknowledgement"]["by"], "Pam Lead")
        self.restart()
        again = self.view("pam")["receipts"][0]
        self.assertEqual(again["acknowledgement"]["by"], "Pam Lead")
        self.assertEqual(again["quality_state"], "Submitted")
        self.assertFalse(again["accepted"])
        code, repeat = self.call(ROUTE + "field-acknowledge", dict(record=back["record"]), "quil")
        self.assertEqual(code, 409, repeat)
        self.assertEqual(self.view()["receipts"][0]["acknowledgement"]["by"], "Pam Lead")
        self.assertTrue(self.store.verify_audit())

    def test_stale_pack_rejected_and_duplicate_replays_without_second_record(self) -> None:
        pack = self.view()["pack"]
        code, out = self.capture(pack_digest="0" * 64)
        self.assertEqual(code, 409, out)
        self.assertEqual(self.view()["receipts"], [])
        self.assertEqual(self.capture(pack_digest=pack["pack_digest"])[0], 200)
        code, dup = self.capture(
            pack_digest="0" * 64, mode="offline", captured_at="2099-01-01T09:00"
        )
        self.assertEqual((code, dup["outcome"]), (200, "duplicate"))
        self.assertEqual(len(self.view()["receipts"]), 1)
        code, clash = self.capture(notes=notes("Changed"))
        self.assertEqual(code, 409, clash)
        self.assertEqual(self.view()["receipts"][0]["original_notes"], notes())

    def test_offline_capture_keeps_capture_time(self) -> None:
        code, out = self.capture(mode="offline", captured_at="2099-01-01T09:15")
        self.assertEqual(code, 200, out)
        self.assertEqual(out["receipt"]["captured_at"], "2099-01-01T09:15")
        self.assertEqual(out["receipt"]["mode"], "offline")

    def test_validation_rejects_unconfirmed_overlong_and_staff_as_worker(self) -> None:
        for over in (
            dict(confirmed=False),
            dict(notes={**notes(), LOFT[0]: "x" * 201}),
            dict(notes={k: v for k, v in notes().items() if k != LOFT[1]}),
            dict(confirmed_by="sam@example.test"),
            dict(confirmed_by="Sam Example"),
            dict(capture_ref="short"),
            dict(measure="Wall insulation"),
        ):
            code, out = self.capture(**over)
            self.assertEqual(code, 400, (over, out))
        self.assertEqual(self.view()["receipts"], [])

    def test_correction_is_append_only_until_acknowledged(self) -> None:
        record = self.capture()[1]["receipt"]["record"]
        fix = dict(
            record=record,
            label=LOFT[0],
            note="Corrected depth",
            confirmed_by=WORKER,
            confirmed=True,
        )
        code, out = self.call(ROUTE + "field-correct", fix, "pam")
        self.assertEqual(code, 200, out)
        receipt = out["receipt"]
        self.assertEqual(receipt["original_notes"], notes())
        self.assertEqual(receipt["corrections"][0]["note"], "Corrected depth")
        self.assertEqual(
            self.call(ROUTE + "field-correct", dict(fix, confirmed_by="Someone Else"), "pam")[0],
            400,
        )
        self.assertEqual(self.call(ROUTE + "field-acknowledge", dict(record=record), "pam")[0], 200)
        self.assertEqual(self.call(ROUTE + "field-correct", fix, "pam")[0], 409)
        self.assertEqual(self.view()["receipts"][0]["original_notes"], notes())

    def test_self_review_denial_for_worker_recorder_acknowledger_and_corrector(self) -> None:
        record = self.capture()[1]["receipt"]["record"]
        fix = dict(record=record, label=LOFT[0], note="Fix", confirmed_by=WORKER, confirmed=True)
        self.assertEqual(self.call(ROUTE + "field-correct", fix, "pam")[0], 200)
        self.assertEqual(self.call(ROUTE + "field-acknowledge", dict(record=record), "pam")[0], 200)
        for actor in ("sam", "pam"):
            review = self.view(actor)["receipts"][0]["review"]
            self.assertFalse(review["you_may_review"], actor)
            self.assertIn("did not", review["blocker"])
            code, _ = self.call(f"/api/cases/ZF-3/quality/{record}/accept", dict(note="x"), actor)
            self.assertIn(code, (400, 403, 404), actor)
        self.assertTrue(self.view("quil")["receipts"][0]["review"]["you_may_review"])
        rec = self.store.cases["ZF-3"]["quality"][record]
        for email in ("sam@example.test", "pam@example.test"):
            with self.assertRaises((ValueError, PermissionError)):
                self.store._independent(rec, self.store.staff[email], "accept this work")
        self.store._independent(rec, self.store.staff["quil@example.test"], "accept this work")
        self.assertEqual(rec["state"], "Submitted")

    def test_acknowledge_denied_for_worker_identity(self) -> None:
        self.store.staff["sam@example.test"]["name"] = WORKER
        record = self.capture("pam")[1]["receipt"]["record"]
        self.assertEqual(self.call(ROUTE + "field-acknowledge", dict(record=record), "sam")[0], 403)

    def test_contractor_and_unknown_routes_denied(self) -> None:
        for actor in ("kim", "kai"):
            self.assertEqual(self.call(ROUTE + "field-intake", actor=actor)[0], 403, actor)
            for action in ("field-capture", "field-correct", "field-acknowledge"):
                self.assertEqual(
                    self.call(ROUTE + action, self.body(), actor)[0], 403, (actor, action)
                )
        self.assertEqual(self.call("/api/workorders/WO-9999/field-intake")[0], 404)
        self.assertEqual(self.call(ROUTE + "field-acknowledge", dict(record=99))[0], 400)

    def test_not_ready_pack_cannot_capture(self) -> None:
        self.call(ROUTE + "appointment", dict(outcome="No access"))
        code, out = self.capture()
        self.assertEqual(code, 400, out)
        self.assertIn("do not start work", out["error"])

    def test_privacy_allow_list_and_no_show_recovery_and_escalation_unknown(self) -> None:
        self.capture()
        out = self.view()
        text = json.dumps(out).lower()
        resident = self.store.cases["ZF-3"]["resident"]
        for key in ("health", "vulnerab", "reason"):
            self.assertNotIn(f'"{key}"', text)
        for value in (v for v in resident.values() if isinstance(v, str) and len(v) > 8):
            self.assertNotIn(value.lower(), text)
        events = {r["event"]: r for r in out["recovery"]}
        self.assertEqual(
            set(events),
            {"provider no-show", "provider cancelled", "resident cancelled", "no access"},
        )
        for row in events.values():
            self.assertFalse(row["resident_refusal"])
        esc = out["escalation"]
        self.assertEqual(
            (esc["owner"], esc["contact"], esc["configured"]),
            ("Unknown - not configured",) * 2 + (False,),
        )
        self.assertFalse(esc["contract_instruction"])
        self.assertFalse(out["boundaries"]["contract_instruction"])

    def test_escalation_destination_shown_only_when_configured(self) -> None:
        env = {
            "ZF_STAFF_INTAKE_ESCALATION_OWNER": "Pam Lead",
            "ZF_STAFF_INTAKE_ESCALATION_ROLE": "Retrofit Programme Manager",
            "ZF_STAFF_INTAKE_ESCALATION_CONTACT": "pam@example.test",
        }
        with mock.patch.dict(os.environ, env):
            esc = self.view()["escalation"]
        self.assertTrue(esc["configured"])
        self.assertEqual(esc["owner"], "Pam Lead")
        self.assertFalse(esc["contract_instruction"])

    def test_injected_failure_leaves_no_partial_receipt(self) -> None:
        self.view()
        with mock.patch.object(type(self.store), "audit", side_effect=RuntimeError("boom")):
            code, _ = self.capture()
        self.assertGreaterEqual(code, 400)
        self.restart()
        self.assertEqual(self.view()["receipts"], [])
        self.assertEqual(self.capture()[0], 200)

    def test_recorder_is_denied_and_independent_qa_accepts(self) -> None:
        record = self.capture("pam")[1]["receipt"]["record"]
        rec = self.store.cases["ZF-3"]["quality"][record]
        self.assertEqual(
            rec["resident_binding"], dict(measure="Loft insulation", context_revision=1)
        )
        code, out = self.accept("pam", record)
        self.assertIn("independent", out["error"], (code, out))
        self.assertEqual(self.store.cases["ZF-3"]["quality"][record]["state"], "Submitted")
        self.assertEqual(self.accept("quil", record)[0], 200)
        self.restart()
        self.assertEqual(self.view("quil")["receipts"][0]["quality_state"], "Accepted")

    def test_corrector_is_denied_by_the_real_accept_path(self) -> None:
        record = self.capture("sam")[1]["receipt"]["record"]
        self.assertEqual(
            self.call(ROUTE + "field-correct", self.correction(record), "quil")[0], 200
        )
        code, out = self.accept("quil", record)
        self.assertIn("independent", out["error"], (code, out))
        self.assertEqual(self.accept("pam", record)[0], 200)

    def test_acknowledger_is_denied_by_the_real_accept_path(self) -> None:
        record = self.capture("sam")[1]["receipt"]["record"]
        self.assertEqual(self.call(ROUTE + "field-acknowledge", dict(record=record), "pam")[0], 200)
        code, out = self.accept("pam", record)
        self.assertIn("independent", out["error"], (code, out))
        self.assertEqual(self.accept("quil", record)[0], 200)

    def test_worker_identity_denied_and_replacement_after_acceptance(self) -> None:
        record = self.capture("sam")[1]["receipt"]["record"]
        rec = self.store.cases["ZF-3"]["quality"][record]
        worker = dict(self.store.staff["quil@example.test"], name=WORKER, email="w@example.test")
        with self.assertRaises(PermissionError):
            self.store._independent(rec, worker, "accept this work")
        self.assertEqual(self.accept("quil", record)[0], 200)
        code, out = self.capture("sam", capture_ref="SYN-CAPTURE-0002", notes=notes("Later"))
        self.assertEqual((code, out["outcome"]), (200, "recorded"), out)
        quality = self.store.cases["ZF-3"]["quality"]
        self.assertEqual(
            (quality[record]["state"], quality[-1]["supersedes"]), ("Superseded", [record])
        )
        self.assertEqual(quality[-1]["resident_binding"]["context_revision"], 1)

    def test_unbound_or_changed_resident_scope_is_refused(self) -> None:
        case = self.store.cases["ZF-3"]
        case["resident_scopes"]["Loft insulation"].append(
            dict(case["resident_scopes"]["Loft insulation"][0], revision=2)
        )
        code, out = self.capture()
        self.assertEqual(code, 409, out)
        self.assertEqual(self.view()["receipts"], [])
        case["technical"]["design_version"] = 2
        self.assertEqual(self.capture(pack_digest="f" * 64)[0], 409)
        self.assertEqual(self.view()["receipts"], [])

    def test_unbound_legacy_receipt_shows_blocker(self) -> None:
        record = self.capture("sam")[1]["receipt"]["record"]
        self.store.cases["ZF-3"]["quality"][record]["resident_binding"] = None
        review = self.view("quil")["receipts"][0]["review"]
        self.assertFalse(review["you_may_review"])
        self.assertIn("resident scope", review["blocker"])

    def test_correction_updates_current_quality_item_and_survives_restart(self) -> None:
        record = self.capture("sam")[1]["receipt"]["record"]
        for note in ("First fix", "Second fix"):
            code, out = self.call(
                ROUTE + "field-correct", self.correction(record, note=note), "quil"
            )
            self.assertEqual(code, 200, out)
        self.restart()
        rec = self.store.cases["ZF-3"]["quality"][record]
        items = {i["label"]: i["evidence"] for i in rec["items"]}
        self.assertEqual(items[LOFT[0]], "Second fix")
        self.assertEqual(items[LOFT[1]], notes()[LOFT[1]])
        self.assertEqual(rec["field_receipt"]["original_notes"], notes())
        self.assertEqual(
            [c["note"] for c in rec["field_receipt"]["corrections"]], ["First fix", "Second fix"]
        )
        self.assertEqual(self.view("pam")["receipts"][0]["original_notes"], notes())
        self.assertEqual(self.store.cases["ZF-3"]["quality"][record]["evidence_version"], 1)

    def test_correction_failure_leaves_item_and_history_unchanged(self) -> None:
        record = self.capture("sam")[1]["receipt"]["record"]
        with mock.patch.object(type(self.store), "audit", side_effect=RuntimeError("boom")):
            code, _ = self.call(ROUTE + "field-correct", self.correction(record), "quil")
        self.assertGreaterEqual(code, 400)
        self.restart()
        rec = self.store.cases["ZF-3"]["quality"][record]
        self.assertEqual(rec["items"][0]["evidence"], notes()[LOFT[0]])
        self.assertEqual(rec["field_receipt"].get("corrections", []), [])

    def test_explicit_valid_digest_is_required_for_new_evidence(self) -> None:
        for bad in (OMIT, "", None, 5, "xyz", "A" * 64, "0" * 63):
            code, out = self.capture(pack_digest=bad)
            self.assertEqual(code, 400, (bad, out))
        self.assertEqual(self.view()["receipts"], [])
        digest = self.view()["pack"]["pack_digest"]
        self.assertEqual(self.capture(pack_digest=digest)[0], 200)
        code, dup = self.capture(pack_digest=OMIT)
        self.assertEqual((code, dup["outcome"]), (200, "duplicate"))
        self.assertEqual(len(self.view()["receipts"]), 1)
        self.assertEqual(self.view()["receipts"][0]["pack_digest"], digest)

    def test_offline_evidence_before_a_design_change_is_stale(self) -> None:
        old = self.view()["pack"]["pack_digest"]
        self.store.cases["ZF-3"]["technical"]["design_version"] = 2
        code, out = self.capture(pack_digest=old, mode="offline", captured_at="2099-01-01T08:00")
        self.assertEqual(code, 409, out)
        self.assertEqual(self.view()["receipts"], [])

    def test_lost_response_retry_replays_after_the_pack_changed(self) -> None:
        digest = self.view()["pack"]["pack_digest"]
        self.assertEqual(self.capture(pack_digest=digest)[0], 200)
        self.call(ROUTE + "appointment", dict(outcome="No access"))
        code, dup = self.capture(pack_digest=digest)
        self.assertEqual((code, dup["outcome"]), (200, "duplicate"), dup)
        self.assertEqual(len(self.view()["receipts"]), 1)


class JsonStaffIntakeApi(StaffIntakeApi):
    sql = False


@unittest.skipUnless(
    os.environ.get("ZF_STAFF_INTAKE_MSSQL") == "1"
    and os.environ.get("ZF_SQL_SERVER") == "127.0.0.1",
    "needs the task-owned loopback SQL Server (ZF_STAFF_INTAKE_MSSQL=1)",
)
class MssqlStaffIntakeApi(StaffIntakeApi):
    database: str | None = None

    def make_store(self, path: Path) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore, _Conn, connection_string

        if self.database is None:
            self.database = "zf_intake132_" + uuid.uuid4().hex
            admin = _Conn(connection_string(dict(os.environ, ZF_SQL_DATABASE="master")))
            admin.execute(f"CREATE DATABASE [{self.database}]")
            admin.close()
            patcher = mock.patch.dict(os.environ, ZF_SQL_DATABASE=self.database)
            patcher.start()
            self.addCleanup(patcher.stop)
            return MssqlStore(str(path), state_dir=str(path.parent))
        return MssqlStore("unused-seed", state_dir=str(path.parent))
