import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

import test_finance_signoffs as tf
from zavaforward_mvp import governance as g
from zavaforward_mvp.sqlstore import SqlStore
from zavaforward_mvp.store import Store

PROTOCOL = {key: f"Synthetic demonstration {key}" for key, _ in g.PROTOCOL_FIELDS}
BENEFITS = {key: f"Synthetic demonstration {key}" for key, _ in g.BG011_FIELDS}
RELEASE = dict(scope_kind="phase", requirements="RULE-020", evidence="Synthetic evidence", unresolved="None", envelope_ref="ENV-DEMO",
               approvers=["Synthetic sponsor"], decision="Release")
BREACH = dict(scope_kind="archetype", scope="Solid wall", owner="Synthetic owner", evidence="e", containment="c", resident_impact="r",
              remediation="m", restart_authority="OD-35 demo")


class Gov:
    make = tf.Flows.make
    setUp = tf.Flows.setUp
    tearDown = tf.Flows.tearDown
    actions = tf.Flows.actions

    def approve_all(self, mde=10):
        s = self.store
        s.protocol_freeze(self.pm1, dict(PROTOCOL, synthetic=True))
        s.protocol_approve(self.pm2, dict(dpia_ref="DPIA-DEMO", lawful_basis_ref="LB-DEMO"))
        s.benefits_record(self.pm1, dict(BENEFITS, mde_cycle_time_pct=mde, mde_coordination_hours_pct=mde))
        s.benefits_approve(self.pm2, {})

    def test_capture_closed_until_protocol_dpia_and_register_approved(self):
        s = self.store
        self.assertEqual(len(s.capture_gate()), 2)
        with self.assertRaises(PermissionError):
            s.require_capture_open()
        s.protocol_freeze(self.pm1, PROTOCOL)
        with self.assertRaises(PermissionError):
            s.protocol_approve(self.pm1, dict(dpia_ref="d", lawful_basis_ref="l"))
        with self.assertRaises(ValueError):
            s.protocol_approve(self.pm2, dict(dpia_ref="d"))
        s.protocol_approve(self.pm2, dict(dpia_ref="d", lawful_basis_ref="l"))
        self.assertEqual(len(s.capture_gate()), 1)
        s.benefits_record(self.pm1, dict(BENEFITS, mde_cycle_time_pct=10, mde_coordination_hours_pct=10))
        s.benefits_approve(self.pm2, {})
        self.assertEqual(s.capture_gate(), [])
        s.require_capture_open()

    def test_changed_protocol_needs_reason_and_new_approval(self):
        self.approve_all()
        with self.assertRaises(ValueError):
            self.store.protocol_freeze(self.pm1, PROTOCOL)
        self.store.protocol_freeze(self.pm1, dict(PROTOCOL, reason="Cut-off moved"))
        self.assertEqual(len(self.store.capture_gate()), 1)
        self.assertEqual(self.store._gov()["protocol_versions"][0]["status"], "Approved")

    def test_incomplete_protocol_and_non_manager_refused(self):
        with self.assertRaises(ValueError):
            self.store.protocol_freeze(self.pm1, dict(PROTOCOL, mde=""))
        with self.assertRaises(PermissionError):
            self.store.protocol_freeze(tf.U["RLO-1"], PROTOCOL)
        with self.assertRaises(PermissionError):
            self.store.protocol_freeze(self.pm1, dict(PROTOCOL, ids=[1]))

    def test_bg011_never_pass_or_fail_when_mde_exceeds_target(self):
        self.assertEqual(self.store.benefit_verdicts()["cycle_time"]["verdict"], "Not assessable")
        self.approve_all(mde=26)
        v = self.store.benefit_verdicts(dict(cycle_time=30, coordination_hours=30))
        self.assertEqual(v["cycle_time"]["verdict"], "Interval estimate only")
        self.assertEqual(v["coordination_hours"]["verdict"], "Interval estimate only")
        self.store.benefits_record(self.pm1, dict(BENEFITS, mde_cycle_time_pct=15, mde_coordination_hours_pct=15))
        v = self.store.benefit_verdicts(dict(cycle_time=30, coordination_hours=10))
        self.assertEqual((v["cycle_time"]["verdict"], v["coordination_hours"]["verdict"]), ("Pass", "Fail"))

    def test_shadow_and_live_need_phase_0_released(self):
        s = self.store
        self.approve_all()
        shadow = dict(RELEASE, scope="Shadow testing", shadow_entry_evidence="Synthetic entry evidence")
        with self.assertRaises(PermissionError):
            s.release_record(self.pm1, shadow)
        with self.assertRaises(PermissionError):
            s.release_record(self.pm1, dict(RELEASE, scope="Live pilot"))
        s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture", decision="Withhold"))
        with self.assertRaises(PermissionError):
            s.release_record(self.pm1, shadow)
        s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        s.release_record(self.pm1, shadow)
        s.release_record(self.pm1, dict(RELEASE, scope="Live pilot"))
        s.release_record(self.pm1, dict(RELEASE, scope="Live pilot", decision="Withhold"))

    def test_pilot_case_events_need_open_capture_gate(self):
        d = copy.deepcopy(tf.test_mvp.DATA)
        d["staff"] = tf.STAFF
        d["cases"][0]["pilot"] = True
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        s = self.store = self.make(d, tmp.name)
        for call in (lambda: s.log_call(self.geo, "ZF-1", "Spoke", ""), lambda: s.set_decision(self.geo, "ZF-1", "Waiting"),
                     lambda: s.advance(self.geo, "ZF-1"), lambda: s.return_case(self.geo, "ZF-1", "Contacting resident", "r")):
            with self.assertRaisesRegex(PermissionError, "capture is closed"):
                call()
        self.approve_all()
        s.log_call(self.geo, "ZF-1", "Spoke", "")

    def test_paused_scope_blocks_case_workflows_but_not_hazards(self):
        s = self.store
        self.approve_all()
        s.breach_record(self.pm1, dict(BREACH, scope="Mid terrace"))
        with self.assertRaisesRegex(PermissionError, "paused"):
            s.log_call(self.geo, "ZF-1", "Spoke", "")
        with self.assertRaisesRegex(PermissionError, "paused"):
            s.set_decision(self.geo, "ZF-1", "Waiting")
        with self.assertRaisesRegex(PermissionError, "paused"):
            s.advance(self.geo, "ZF-1")
        s.raise_hazard(self.pm1, "ZF-1", "Damp and mould", "Emergency")

    def test_breach_record_needs_an_authorised_role(self):
        with self.assertRaises(PermissionError):
            self.store.breach_record(tf.U["RLO-1"], BREACH)
        self.assertEqual(self.store.breach_record(tf.U["BSL-1"], BREACH)["status"], "Paused")

    def test_phase_release_decisions_are_recorded_and_gated(self):
        s = self.store
        self.assertEqual(s.release_gaps(), list(g.PHASES))
        with self.assertRaises(PermissionError):
            s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        self.approve_all()
        s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        with self.assertRaises(ValueError):
            s.release_record(self.pm1, dict(RELEASE, scope="Shadow testing"))
        s.release_record(self.pm1, dict(RELEASE, scope="Shadow testing", shadow_entry_evidence="Synthetic entry evidence"))
        s.release_record(self.pm1, dict(RELEASE, scope_kind="tranche", scope="Tranche 1"))
        s.release_record(self.pm1, dict(RELEASE, scope="Live pilot", decision="Withhold"))
        self.assertTrue(s.is_released("Shadow testing"))
        self.assertFalse(s.is_released("Live pilot"))
        self.assertEqual(s.release_gaps(), [])
        with self.assertRaises(ValueError):
            s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture", approvers=[]))

    def test_breach_pauses_scope_until_authorised_restart(self):
        self.approve_all()
        s = self.store
        b = s.breach_record(tf.U["QI-1"], BREACH)
        self.assertTrue(s.is_paused("archetype", "Solid wall"))
        with self.assertRaises(PermissionError):
            s.require_not_paused("archetype", "Solid wall")
        self.assertFalse(s.is_paused("archetype", "Other"))
        with self.assertRaises(ValueError):
            s.breach_record(tf.U["QI-1"], dict(BREACH, evidence=""))
        with self.assertRaises(PermissionError):
            s.breach_restart(self.pm1, dict(id=b["id"], release_id="REL-9", authority_ref="a", remediation_evidence="r"))
        rel = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        with self.assertRaises(PermissionError):
            s.breach_restart(tf.U["QI-1"], dict(id=b["id"], release_id=rel["id"], authority_ref="a", remediation_evidence="r"))
        s.breach_restart(self.pm2, dict(id=b["id"], release_id=rel["id"], authority_ref="OD-35 demo", remediation_evidence="Synthetic remediation"))
        self.assertFalse(s.is_paused("archetype", "Solid wall"))
        self.assertIn("breach_restart", self.actions())
        self.assertTrue(s.verify_audit())

    def test_view_is_manager_only(self):
        with self.assertRaises(PermissionError):
            self.store.governance_view(tf.U["RLO-1"])
        self.assertFalse(self.store.governance_view(self.pm1)["capture_open"])


class JsonGov(Gov, unittest.TestCase):
    def make(self, data, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return Store(str(p))


class SqlGov(Gov, unittest.TestCase):
    def make(self, data, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))

    def test_survives_a_restart(self):
        self.approve_all()
        self.store.breach_record(tf.U["QI-1"], BREACH)
        again = SqlStore(str(Path(self.tmp.name) / "zavaforward.json"), os.path.join(self.tmp.name, "pw.sqlite"))
        self.assertEqual(again.capture_gate(), [])
        self.assertTrue(again.is_paused("archetype", "Solid wall"))


if __name__ == "__main__":
    unittest.main()
