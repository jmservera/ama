import copy
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

import test_finance_signoffs as tf
from zava_forward.core import governance as g
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

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
        d = copy.deepcopy(tf.dataset.DATA)
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
        s.raise_hazard(self.pm1, "ZF-1", "Damp and mould", "Emergency",
                       metadata=dict(source="Synthetic report", aware_at="2026-01-01T10:00:00Z"))

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


FINDINGS = (
    "GOVERN-AUDIT-01", "GOVERN-AUDIT-02", "MAP-01", "MAP-02", "MAP-04",
    "MEASURE-01", "MN-3.2", "MN-4.1", "MN-4.3", "T-RAI-001", "T-RAI-002",
    "GOVERN-AUDIT-04", "GOVERN-AUDIT-05", "MAP-05", "MEASURE-02", "MEASURE-03",
    "MEASURE-04", "MN-2.3", "T-RAI-005", "EU-COND-01", "EU-COND-02", "EU-COND-04",
)
BASELINE = "1cb398c7b90bec05a5700008a97d0cfac494144a"
ASSESSMENT = dict(source_commit="ab0613f3336109ff9b96560a16758ee842232715",
                  task_id=None, task_version=None, release_version=None,
                  nonapplicability_reason="Constructed whole-system source inspection, not a task release")


def claim(**changes):
    body = dict(finding_id="MAP-01", baseline_commit=BASELINE, assessment=copy.deepcopy(ASSESSMENT),
                evidence_tier="implemented/source-tested", result="Constructed source test only",
                references=["src/core/tests/test_governance.py::test_inventory"],
                limitations="No qualified human or live evidence", decision_maker_status="Unappointed",
                decision_maker_ref=None, event_ref="SYN-126-1", expected_revision=0)
    return dict(body, **changes)


class EvidenceRegister(unittest.TestCase):
    backend = "json"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "constructed.json"
        data = copy.deepcopy(tf.dataset.DATA)
        data["staff"] = copy.deepcopy(tf.STAFF)
        self.path.write_text(json.dumps(data))
        self.pm = data["staff"][1]
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import _Conn, connection_string
            if os.environ.get("ZF_SQL_SERVER") not in ("127.0.0.1", "localhost"):
                raise RuntimeError("Task-owned loopback SQL Server only.")
            env = patch.dict(os.environ, ZF_SQL_DATABASE="master")
            env.start()
            self.addCleanup(env.stop)
            self.admin = _Conn(connection_string())
            self.addCleanup(self.admin.close)
            self.database = "zf_rai126_" + uuid.uuid4().hex
            self.admin.execute(f"CREATE DATABASE [{self.database}]")
            self.addCleanup(self.drop_database)
            os.environ["ZF_SQL_DATABASE"] = self.database
        self.store = self.reopen()

    def drop_database(self):
        self.admin.execute(f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
        self.admin.execute(f"DROP DATABASE [{self.database}]")

    def reopen(self):
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore
            s = MssqlStore(str(self.path), state_dir=self.tmp.name)
        elif self.backend == "sqlite":
            s = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        else:
            return Store(str(self.path))
        self.addCleanup(s.db.close)
        return s

    def view(self, assessment=ASSESSMENT):
        return self.store.governance_view(self.pm, assessment)["rai_evidence"]

    def test_inventory(self):
        before, audit = copy.deepcopy(self.store.data), list(self.store.audit_entries())
        disk = self.path.read_bytes()
        v = self.view()
        self.assertEqual([r["finding_id"] for r in v["findings"]], list(FINDINGS))
        self.assertEqual(len(set(FINDINGS)), 22)
        self.assertEqual(v["current_disposition_count"], 0)
        self.assertEqual(v["baseline"]["commit"], BASELINE)
        for row in v["findings"]:
            self.assertEqual((row["closure"], row["acceptance"], row["disposition"]),
                             ("Open", "Unknown", "insufficient"))
        v["findings"][0]["claims"].append("mutated")
        self.assertEqual(self.view()["findings"][0]["claims"], [])
        self.assertEqual(before, self.store.data)
        self.assertEqual(audit, list(self.store.audit_entries()))
        self.assertEqual(disk, self.path.read_bytes())

    def test_append_reopen_reconcile_and_provenance(self):
        record = self.store.rai_evidence_record(self.pm, claim())
        self.assertEqual(record["recorded_by"]["email"], self.pm["email"])
        self.assertTrue(record["recorded_at"].endswith("+00:00"))
        self.assertEqual(record["revision"], 1)
        self.assertEqual(record["verification"], "unverified claim")
        self.assertEqual(record["evidence_class"], "constructed-fixture")
        audits = list(self.store.audit_entries())
        self.assertEqual(self.store.rai_evidence_record(self.pm, claim()), record)
        self.assertEqual(audits, list(self.store.audit_entries()))
        with self.assertRaises(Exception):
            self.store.rai_evidence_record(self.pm, claim(result="conflicting event"))
        self.store = self.reopen()
        self.assertEqual(self.view()["findings"][2]["claims"], [record])
        self.store.rai_evidence_record(self.pm, claim(event_ref="SYN-2", expected_revision=1))
        self.assertEqual(len(self.view()["findings"][2]["claims"]), 2)
        self.assertEqual(self.view()["current_disposition_count"], 1)

    def test_context_staleness_and_baseline_replay(self):
        self.store.rai_evidence_record(self.pm, claim())
        self.assertEqual(self.view()["current_disposition_count"], 1)
        self.assertIsNone(self.view(None)["current_disposition_count"])
        changed = dict(ASSESSMENT, source_commit="f" * 40)
        self.assertEqual(self.view(changed)["current_disposition_count"], 0)
        task = dict(source_commit=ASSESSMENT["source_commit"], task_id="task", task_version="1",
                    release_version="r1", nonapplicability_reason=None)
        self.store.rai_evidence_record(self.pm, claim(assessment=task, expected_revision=1, event_ref="SYN-TASK"))
        for key in ("source_commit", "task_id", "task_version", "release_version"):
            altered = dict(task, **{key: "e" * 40 if key == "source_commit" else "changed"})
            self.assertEqual(self.view(altered)["current_disposition_count"], 0)
        historical = dict(ASSESSMENT, source_commit=BASELINE)
        self.store.rai_evidence_record(self.pm, claim(assessment=historical, expected_revision=2, event_ref="SYN-BASE"))
        self.assertEqual(self.view(historical)["current_disposition_count"], 0)

    def test_complete_is_not_accepted_or_closed(self):
        for i, fid in enumerate(FINDINGS):
            self.store.rai_evidence_record(self.pm, claim(finding_id=fid, expected_revision=i, event_ref=f"SYN-{i}",
                                                        evidence_tier="insufficient"))
        v = self.view()
        self.assertEqual(v["current_disposition_count"], 22)
        self.assertTrue(v["dispositions_complete"])
        self.assertEqual(v["open_count"], 22)
        self.assertTrue(all(r["acceptance"] == "Unknown" for r in v["findings"]))

    def test_invalid_promotions_and_primitives_leave_no_success(self):
        bad = [
            {"actor": self.pm}, {"recorded_at": "yesterday"}, {"approval": True}, {"closure": "Closed"},
            {"evidence_tier": "accepted"}, {"finding_id": "UNKNOWN"}, {"baseline_commit": "a" * 40},
            {"expected_revision": True}, {"expected_revision": -1}, {"result": {}}, {"result": "x" * 2001},
            {"references": []}, {"references": ["x"] * 21}, {"references": [{}]}, {"references": ["x" * 501]},
            {"limitations": ""}, {"decision_maker_ref": "self appointed"},
            {"decision_maker_status": "Unverified reference"},
            {"assessment": dict(ASSESSMENT, source_commit="abc")},
            {"assessment": dict(ASSESSMENT, task_id="mixed")},
            {"assessment": dict(ASSESSMENT, extra="bad")},
        ]
        for changes in bad:
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    self.store.rai_evidence_record(self.pm, claim(**changes))
        self.assertEqual(self.view()["history_record_count"], 0)
        self.assertFalse([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"])

    def test_inert_limits_and_independent_acceptance_is_only_claim(self):
        body = claim(result="x" * 2000, limitations="x" * 2000, references=["https://127.0.0.1/no-fetch"] + ["x" * 500] * 19,
                     event_ref="x" * 200, decision_maker_status="Unverified reference",
                     decision_maker_ref="x" * 500, evidence_tier="independent-acceptance")
        with patch("urllib.request.urlopen", side_effect=AssertionError("must not fetch")):
            self.store.rai_evidence_record(self.pm, body)
        row = self.view()["findings"][2]
        self.assertEqual((row["closure"], row["acceptance"]), ("Open", "Unknown"))

    def test_all_tiers_and_explicit_owner_unknown_are_claims(self):
        for i, tier in enumerate(g.RAI_TIERS):
            self.store.rai_evidence_record(self.pm, claim(evidence_tier=tier, expected_revision=i,
                                                        event_ref=f"TIER-{i}", decision_maker_status="Unknown"))
        row = self.view()["findings"][2]
        self.assertEqual([r["evidence_tier"] for r in row["claims"]], list(g.RAI_TIERS))
        self.assertEqual((row["closure"], row["acceptance"]), ("Open", "Unknown"))

    def test_schema_boundaries_and_legacy_insufficiency(self):
        for changes in (
            {"limitations": "x" * 2001}, {"event_ref": "x" * 201},
            {"decision_maker_status": "Unverified reference", "decision_maker_ref": "x" * 501},
            {"assessment": dict(ASSESSMENT, nonapplicability_reason="x" * 601)},
            {"assessment": dict(ASSESSMENT, source_commit="A" * 40)},
            {"assessment": dict(ASSESSMENT, task_id="task", task_version="v", release_version="r")},
            {"references": "not a list"}, {"expected_revision": 1.0},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    self.store.rai_evidence_record(self.pm, claim(**changes))
        binding = dict(source_commit="f" * 40, task_id="t" * 200, task_version="v" * 200,
                       release_version="r" * 200, nonapplicability_reason=None)
        for key in ("task_id", "task_version", "release_version"):
            with self.assertRaises(ValueError):
                self.store.rai_evidence_record(self.pm, claim(assessment=dict(binding, **{key: "x" * 201})))
        self.store.rai_evidence_record(self.pm, claim(assessment=binding))
        self.assertEqual(self.view(binding)["current_disposition_count"], 1)
        self.store.rai_evidence_record(self.pm, claim(assessment=dict(ASSESSMENT, nonapplicability_reason="x" * 600),
                                                    expected_revision=1, event_ref="MAX-REASON"))
        # Legacy unproven history must not be credited or silently repaired.
        with self.store.lock:
            self.store.data["governance"]["rai_claims"].append({"finding_id": "MAP-01", "status": "accepted"})
            self.store.save()
        v = self.view()
        self.assertEqual(v["invalid_history_count"], 1)
        self.assertFalse(v["dispositions_complete"])
        self.assertEqual(v["findings"][2]["acceptance"], "Unknown")

    def test_in_process_save_failure_does_not_leave_claim(self):
        with patch.object(self.store, "save", side_effect=RuntimeError("constructed save failure")):
            with self.assertRaisesRegex(RuntimeError, "save failure"):
                self.store.rai_evidence_record(self.pm, claim())
        self.store = self.reopen()
        self.assertEqual(self.view()["history_record_count"], 0)
        self.assertFalse([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"])

    def test_current_roles_forgery_removal_and_demotion(self):
        for user in (tf.U["RLO-1"], tf.U["CON-1"], dict(self.pm, name="forged"),
                     dict(self.pm, email="unknown@example.test"), dict(tf.U["CON-1"], role=self.pm["role"])):
            with self.assertRaises(PermissionError):
                self.store.rai_evidence_record(user, claim())
            with self.assertRaises(PermissionError):
                self.store.governance_view(user)
        if hasattr(self.store, "db"):
            self.store.db.execute("DELETE FROM staff WHERE email=?", (self.pm["email"],))
        else:
            del self.store.staff[self.pm["email"]]
        with self.assertRaises(PermissionError):
            self.store.rai_evidence_record(self.pm, claim())


class SqlEvidenceRegister(EvidenceRegister):
    backend = "sqlite"

    def test_transaction_actor_recheck_and_audit_rollback(self):
        original = self.store.save
        def demote():
            user = dict(self.pm, role="Resident Liaison Officer")
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(user), self.pm["email"]))
            original()
        with patch.object(self.store, "save", side_effect=demote):
            with self.assertRaises(PermissionError):
                self.store.rai_evidence_record(self.pm, claim())
        self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(self.pm), self.pm["email"]))
        append = self.store._append_audit
        def failure(entries):
            append(entries)
            raise RuntimeError("constructed precommit failure")
        with patch.object(self.store, "_append_audit", side_effect=failure):
            with self.assertRaisesRegex(RuntimeError, "precommit"):
                self.store.rai_evidence_record(self.pm, claim())
        self.assertEqual(self.view()["history_record_count"], 0)
        self.assertFalse([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"])

    def test_competing_writer_and_stale_revision(self):
        from zava_forward.core.store import ConflictError
        other = self.reopen()
        original = self.store.save
        def compete():
            other.rai_evidence_record(self.pm, claim(event_ref="WINNER"))
            original()
        with patch.object(self.store, "save", side_effect=compete):
            with self.assertRaises(ConflictError):
                self.store.rai_evidence_record(self.pm, claim())
        self.assertEqual(self.view()["history_record_count"], 1)
        self.assertEqual(self.view()["findings"][2]["claims"][0]["event_ref"], "WINNER")
        with self.assertRaises(ConflictError):
            self.store.rai_evidence_record(self.pm, claim())

    def test_postcommit_failure_requires_reload_no_duplicate_audit(self):
        original = self.store.save
        def ack_failure():
            original()
            raise RuntimeError("constructed acknowledgement failure")
        with patch.object(self.store, "save", side_effect=ack_failure):
            with self.assertRaises(g.GovernanceCommittedError):
                self.store.rai_evidence_record(self.pm, claim())
        self.store = self.reopen()
        self.assertEqual(self.view()["history_record_count"], 1)
        self.store.rai_evidence_record(self.pm, claim())
        self.assertEqual(len([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]), 1)

    def test_immediate_postcommit_hook_failure_has_witness(self):
        with patch("zava_forward.core.appointments.mark_committed", side_effect=RuntimeError("after COMMIT")):
            with self.assertRaises(g.GovernanceCommittedError):
                self.store.rai_evidence_record(self.pm, claim())
        self.store = self.reopen()
        self.assertEqual(self.view()["history_record_count"], 1)
        self.assertEqual(len([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]), 1)

    def test_lock_exit_acknowledgement_failure_reports_committed(self):
        finish = self.store._finish
        def fail_exit():
            finish()
            raise RuntimeError("constructed lock exit failure")
        with patch.object(self.store, "_finish", side_effect=fail_exit):
            with self.assertRaises(g.GovernanceCommittedError):
                self.store.rai_evidence_record(self.pm, claim())
        self.store = self.reopen()
        self.assertEqual(self.view()["history_record_count"], 1)

    def test_failed_recovery_quarantines_success_and_preserves_pending_prefix(self):
        with self.store.lock:
            self.store.audit(self.pm["email"], "SYN_prior_pending", "-", "Constructed prefix")
            prior = list(self.store.local.pending)
            with patch.object(self.store, "_proc_sync", side_effect=RuntimeError("recovery unavailable")), \
                 patch.object(self.store, "_append_audit", side_effect=RuntimeError("precommit unavailable")):
                with self.assertRaisesRegex(RuntimeError, "precommit"):
                    self.store.rai_evidence_record(self.pm, claim())
            self.assertEqual(self.store.local.pending, prior)
        self.store = self.reopen()
        self.assertEqual(self.view()["history_record_count"], 0)
        actions = [a["action"] for a in self.store.audit_entries()]
        self.assertIn("SYN_prior_pending", actions)
        self.assertNotIn("rai_evidence_record", actions)


@unittest.skipUnless(os.environ.get("ZF_RAI126_MSSQL") == "1", "opt-in task-owned loopback SQL")
class MssqlEvidenceRegister(SqlEvidenceRegister):
    backend = "mssql"


if __name__ == "__main__":
    unittest.main()
