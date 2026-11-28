import copy
import json
import os
import re
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
BENEFITS.update(
    ai_denominator="per accepted handover",
    ai_quality_floor="Synthetic floor: no critical misses",
    ai_cost_components="Synthetic platform, review and assurance effort",
)
CLAIM = dict(
    claim="Synthetic coordinator time released",
    capacity_kind="capacity gain",
    baseline="Synthetic baseline",
    synthetic=True,
)
RELEASE = dict(
    scope_kind="phase",
    requirements="RULE-020",
    evidence="Synthetic evidence",
    unresolved="None",
    envelope_ref="ENV-DEMO",
    economics_report_ref="Synthetic AI economics report",
    economics_limit_breach="None",
    approvers=["Synthetic sponsor"],
    decision="Release",
)
BREACH = dict(
    scope_kind="archetype",
    scope="Solid wall",
    owner="Synthetic owner",
    evidence="e",
    containment="c",
    resident_impact="r",
    remediation="m",
    restart_authority="OD-35 demo",
)


class Gov:
    make = tf.Flows.make
    setUp = tf.Flows.setUp
    tearDown = tf.Flows.tearDown
    actions = tf.Flows.actions

    def approve_all(self, mde=10):
        s = self.store
        s.protocol_freeze(self.pm1, dict(PROTOCOL, synthetic=True))
        s.protocol_approve(self.pm2, dict(dpia_ref="DPIA-DEMO", lawful_basis_ref="LB-DEMO"))
        s.benefits_record(
            self.pm1, dict(BENEFITS, mde_cycle_time_pct=mde, mde_coordination_hours_pct=mde)
        )
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
        s.benefits_record(
            self.pm1, dict(BENEFITS, mde_cycle_time_pct=10, mde_coordination_hours_pct=10)
        )
        s.benefits_approve(self.pm2, {})
        self.assertEqual(s.capture_gate(), [])
        s.require_capture_open()

    def test_ai_running_cost_line_is_required_before_capture(self):
        s = self.store
        s.protocol_freeze(self.pm1, PROTOCOL)
        s.protocol_approve(self.pm2, dict(dpia_ref="d", lawful_basis_ref="l"))
        base = dict(BENEFITS, mde_cycle_time_pct=10, mde_coordination_hours_pct=10)
        for missing in ("ai_denominator", "ai_quality_floor", "ai_cost_components"):
            with self.assertRaises(ValueError):
                s.benefits_record(self.pm1, {k: v for k, v in base.items() if k != missing})
        with self.assertRaises(ValueError):
            s.benefits_record(self.pm1, dict(base, ai_denominator="per token"))
        entry = s.benefits_record(self.pm1, base)
        self.assertTrue(entry["ai_running_cost"]["cost_status"].startswith("Unknown"))
        s.benefits_approve(self.pm2, {})
        s.require_capture_open()
        del s._gov()["benefits"]["BG-011"]["ai_running_cost"]
        self.assertIn("AI running-cost line", " ".join(s.capture_gate()))
        priced = s.benefits_record(
            self.pm1, dict(base, ai_price_source="Synthetic price list 2026-11-01")
        )
        self.assertEqual(priced["ai_running_cost"]["cost_status"], "Priced from the named source")

    def test_ai_running_cost_is_unknown_not_zero_without_price_or_outcomes(self):
        s = self.store
        base = dict(BENEFITS, mde_cycle_time_pct=10, mde_coordination_hours_pct=10)
        line = s.benefits_record(self.pm1, base)["ai_running_cost"]
        self.assertEqual(line["named_denominator"], "per accepted handover")
        self.assertEqual(
            (
                line["total_cost_of_ai"],
                line["cost_per_accepted_outcome"],
                line["accepted_outcome_count"],
            ),
            ("Unknown",) * 3,
        )
        price = "Synthetic price list 2026-11-01"
        for extra in (
            dict(ai_total_cost="12.50"),
            dict(ai_price_source=price, ai_total_cost="12.50", ai_accepted_outcomes=0),
            dict(ai_price_source=price, ai_accepted_outcomes=5),
            dict(ai_total_cost="12.50", ai_accepted_outcomes=5),
        ):
            line = s.benefits_record(self.pm1, dict(base, **extra))["ai_running_cost"]
            self.assertEqual(line["cost_per_accepted_outcome"], "Unknown", extra)
        line = s.benefits_record(
            self.pm1,
            dict(base, ai_price_source=price, ai_total_cost="12.50", ai_accepted_outcomes=5),
        )["ai_running_cost"]
        self.assertEqual(
            (line["total_cost_of_ai"], line["cost_per_accepted_outcome"]), ("12.50", "2.5000")
        )
        for zero in ("0", 0, "0.00"):
            line = s.benefits_record(
                self.pm1,
                dict(base, ai_price_source=price, ai_total_cost=zero, ai_accepted_outcomes=5),
            )["ai_running_cost"]
            self.assertEqual(
                (line["total_cost_of_ai"], line["cost_per_accepted_outcome"]),
                ("Unknown", "Unknown"),
                zero,
            )
        line = s.benefits_record(
            self.pm1, dict(base, ai_total_cost="   ", ai_accepted_outcomes="  ")
        )["ai_running_cost"]
        self.assertEqual(line["total_cost_of_ai"], "Unknown")
        for bad in (
            dict(ai_total_cost="-1"),
            dict(ai_total_cost="abc"),
            dict(ai_accepted_outcomes="-2"),
            dict(ai_accepted_outcomes="\u00b2"),
            dict(ai_total_cost="1e9999999"),
            dict(ai_total_cost=True),
        ):
            with self.assertRaises(ValueError):
                s.benefits_record(self.pm1, dict(base, **bad))

    def test_release_decision_carries_ai_running_cost_line(self):
        s = self.store
        rec = s.release_record(
            self.pm1, dict(RELEASE, scope="Phase 0 capture", decision="Withhold")
        )
        self.assertEqual(rec["ai_running_cost"]["cost_per_accepted_outcome"], "Unknown")
        s.benefits_record(
            self.pm1,
            dict(
                BENEFITS,
                mde_cycle_time_pct=10,
                mde_coordination_hours_pct=10,
                ai_price_source="Synthetic price list",
                ai_total_cost="9",
                ai_accepted_outcomes=3,
            ),
        )
        rec = s.release_record(
            self.pm1, dict(RELEASE, scope_kind="tranche", scope="Synthetic tranche 1")
        )
        self.assertEqual(rec["ai_running_cost"]["cost_per_accepted_outcome"], "3.0000")
        self.assertEqual(rec["economics_report_ref"], "Synthetic AI economics report")

    def test_value_claim_is_capacity_until_destination_confirmed(self):
        s = self.store
        with self.assertRaises(PermissionError):
            s.value_claim_record(tf.U["RLO-1"], CLAIM)
        with self.assertRaises(ValueError):
            s.value_claim_record(self.pm1, dict(CLAIM, capacity_kind="cash"))
        claim = s.value_claim_record(self.pm1, CLAIM)
        self.assertEqual(
            (claim["status"], claim["destination"]), ("Capacity only, not booked", None)
        )
        confirm = dict(
            id=claim["id"], destination="spend avoided", budget_owner_ref="Synthetic owner ref"
        )
        with self.assertRaises(PermissionError):
            s.value_claim_confirm(self.pm1, confirm)
        with self.assertRaises(ValueError):
            s.value_claim_confirm(self.pm2, dict(confirm, destination="time saved"))
        with self.assertRaises(ValueError):
            s.value_claim_confirm(self.pm2, dict(confirm, budget_owner_ref=""))
        self.assertEqual(s.value_claim_confirm(self.pm2, confirm)["status"], "Booked")
        booked = dict(s._gov()["value_claims"][0])
        with self.assertRaisesRegex(ValueError, "already Booked"):
            s.value_claim_confirm(
                self.pm2, dict(confirm, destination="capital freed", budget_owner_ref="Other ref")
            )
        self.assertEqual(s._gov()["value_claims"][0], booked)
        self.assertEqual(
            s.governance_view(self.pm1)["value_claims"][0]["destination"], "spend avoided"
        )

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
        self.store.benefits_record(
            self.pm1, dict(BENEFITS, mde_cycle_time_pct=15, mde_coordination_hours_pct=15)
        )
        v = self.store.benefit_verdicts(dict(cycle_time=30, coordination_hours=10))
        self.assertEqual(
            (v["cycle_time"]["verdict"], v["coordination_hours"]["verdict"]), ("Pass", "Fail")
        )

    def test_shadow_and_live_need_phase_0_released(self):
        s = self.store
        self.approve_all()
        shadow = dict(
            RELEASE, scope="Shadow testing", shadow_entry_evidence="Synthetic entry evidence"
        )
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
        for call in (
            lambda: s.log_call(self.geo, "ZF-1", "Spoke", ""),
            lambda: s.set_decision(self.geo, "ZF-1", "Waiting"),
            lambda: s.advance(self.geo, "ZF-1"),
            lambda: s.return_case(self.geo, "ZF-1", "Contacting resident", "r"),
        ):
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
        s.raise_hazard(
            self.pm1,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            metadata=dict(source="Synthetic report", aware_at="2026-01-01T10:00:00Z"),
        )

    def test_work_package_breach_pauses_only_cases_with_active_orders_in_it(self):
        s = self.store
        self.approve_all()
        s.data.setdefault("procurement", dict(packages=[], work_orders=[]))["work_orders"].append(
            dict(id="WO-1", case_id="ZF-1", package="PKG-1", state="Appointed")
        )
        b = s.breach_record(self.pm1, dict(BREACH, scope_kind="work package", scope="PKG-1"))
        with self.assertRaisesRegex(PermissionError, "paused"):
            s.log_call(self.geo, "ZF-1", "Spoke", "")
        s.log_call(self.geo, "ZF-2", "Spoke", "")
        rel = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        s.breach_restart(
            self.pm2,
            dict(
                id=b["id"],
                release_id=rel["id"],
                authority_ref="OD-35 demo",
                remediation_evidence="Synthetic remediation",
            ),
        )
        s.log_call(self.geo, "ZF-1", "Spoke", "")

    def test_breach_record_needs_an_authorised_role(self):
        with self.assertRaises(PermissionError):
            self.store.breach_record(tf.U["RLO-1"], BREACH)
        self.assertEqual(self.store.breach_record(tf.U["BSL-1"], BREACH)["status"], "Paused")

    def test_release_decision_needs_economics_report_and_breach_handling(self) -> None:
        s = self.store
        self.approve_all()
        for missing in ("economics_report_ref", "economics_limit_breach"):
            with self.assertRaises(ValueError):
                s.release_record(
                    self.pm1,
                    {k: v for k, v in RELEASE.items() if k != missing}
                    | dict(scope="Phase 0 capture"),
                )
        breached = dict(
            RELEASE,
            scope="Phase 0 capture",
            economics_limit_breach="Synthetic spend limit exceeded",
        )
        with self.assertRaises(ValueError):
            s.release_record(self.pm1, breached)
        self.assertEqual(s.release_gaps(), list(g.PHASES))
        withheld = s.release_record(self.pm1, dict(breached, decision="Withhold"))
        self.assertNotIn("economics_breach_decision", withheld)
        decided = dict(
            breached, economics_breach_decision="Synthetic: limit raised by the budget owner"
        )
        for bad in (None, "Someone else", self.pm1["email"]):
            with self.assertRaises(ValueError):
                s.release_record(
                    self.pm1, dict(decided, economics_breach_approver=bad) if bad else decided
                )
        rec = s.release_record(
            self.pm1, dict(decided, economics_breach_approver="Synthetic sponsor")
        )
        self.assertEqual(rec["economics_breach_approver"], "Synthetic sponsor")
        with self.assertRaises(ValueError):
            s.release_record(
                self.pm1, dict(RELEASE, scope="Phase 0 capture", economics_report_ref="Unknown")
            )
        self.assertEqual(
            s.release_record(
                self.pm1,
                dict(
                    RELEASE,
                    scope="Phase 0 capture",
                    economics_report_ref="Unknown",
                    decision="Withhold",
                ),
            )["decision"],
            "Withhold",
        )
        proposer_listed = dict(
            decided,
            approvers=["Synthetic sponsor", self.pm1["email"]],
            economics_breach_approver=self.pm1["email"],
        )
        with self.assertRaises(ValueError):
            s.release_record(self.pm1, proposer_listed)
        self.assertEqual(rec["economics_limit_breach"], "Synthetic spend limit exceeded")
        self.assertEqual(rec["economics_report_ref"], "Synthetic AI economics report")
        self.assertIn("economics_breach_decision", rec)
        clean = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        self.assertEqual(clean["economics_limit_breach"], "None")
        self.assertNotIn("economics_breach_decision", clean)

    def test_phase_release_decisions_are_recorded_and_gated(self):
        s = self.store
        self.assertEqual(s.release_gaps(), list(g.PHASES))
        with self.assertRaises(PermissionError):
            s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        self.approve_all()
        s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        with self.assertRaises(ValueError):
            s.release_record(self.pm1, dict(RELEASE, scope="Shadow testing"))
        s.release_record(
            self.pm1,
            dict(RELEASE, scope="Shadow testing", shadow_entry_evidence="Synthetic entry evidence"),
        )
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
            s.breach_restart(
                self.pm1,
                dict(id=b["id"], release_id="REL-9", authority_ref="a", remediation_evidence="r"),
            )
        rel = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        with self.assertRaises(PermissionError):
            s.breach_restart(
                tf.U["QI-1"],
                dict(id=b["id"], release_id=rel["id"], authority_ref="a", remediation_evidence="r"),
            )
        s.breach_restart(
            self.pm2,
            dict(
                id=b["id"],
                release_id=rel["id"],
                authority_ref="OD-35 demo",
                remediation_evidence="Synthetic remediation",
            ),
        )
        self.assertFalse(s.is_paused("archetype", "Solid wall"))
        self.assertIn("breach_restart", self.actions())
        self.assertTrue(s.verify_audit())

    def test_breach_names_restart_authority_and_blocks_automatic_restart(self):
        self.approve_all()
        s = self.store
        b = s.breach_record(tf.U["QI-1"], BREACH)
        self.assertEqual(
            (b["restart_authority"], b["restart_rule"], b["automatic_restart"]),
            ("OD-35 demo", "RULE-024", False),
        )
        for bad_authority in (
            "",
            "TBD",
            "none",
            "automatic",
            "Unavailable: OD-35 authority unappointed",
            "CM-0123456789abcdef",
        ):
            with self.assertRaises(ValueError):
                s.breach_record(tf.U["QI-1"], dict(BREACH, restart_authority=bad_authority))
        with self.assertRaises(PermissionError):
            s.breach_record(tf.U["QI-1"], dict(BREACH, restart_authority=tf.U["QI-1"]["email"]))
        rel = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        ok = dict(
            id=b["id"], release_id=rel["id"], authority_ref="OD-35 demo", remediation_evidence="r"
        )
        with self.assertRaises(PermissionError):
            s.breach_restart(self.pm2, dict(ok, automatic=True))
        with self.assertRaises(PermissionError):
            s.breach_restart(self.pm2, dict(ok, authority_ref="Someone else"))
        with self.assertRaises(PermissionError):
            s.breach_restart(self.pm1, ok)
        self.assertTrue(s.is_paused("archetype", "Solid wall"))

    def test_protocol_approval_refusals(self):
        s = self.store
        approval = dict(dpia_ref="DPIA-DEMO", lawful_basis_ref="LB-DEMO")
        with self.assertRaisesRegex(ValueError, "Freeze a protocol version first"):
            s.protocol_approve(self.pm2, approval)
        s.protocol_freeze(self.pm1, PROTOCOL)
        with self.assertRaisesRegex(ValueError, "latest protocol version"):
            s.protocol_approve(self.pm2, dict(approval, version=7))
        s.protocol_approve(self.pm2, approval)
        with self.assertRaisesRegex(ValueError, "already approved"):
            s.protocol_approve(self.pm2, approval)

    def test_release_input_refusals_and_latest_decision_governs(self):
        s = self.store
        self.approve_all()
        phase0 = dict(RELEASE, scope="Phase 0 capture")
        for bad in (
            dict(scope_kind="programme"),
            dict(decision="Maybe"),
            dict(scope="Phase 9"),
            dict(approvers=[]),
            dict(approvers=["  ", 7, None]),
        ):
            with self.assertRaises(ValueError):
                s.release_record(self.pm1, dict(phase0, **bad))
        self.assertEqual(s.release_gaps(), list(g.PHASES))
        self.assertEqual(
            s.release_record(self.pm1, dict(RELEASE, scope_kind="tranche", scope="Any tranche"))[
                "scope"
            ],
            "Any tranche",
        )
        s.release_record(self.pm1, phase0)
        shadow = dict(
            RELEASE, scope="Shadow testing", shadow_entry_evidence="Synthetic entry evidence"
        )
        s.release_record(self.pm1, shadow)
        self.assertTrue(s.is_released("Shadow testing"))
        s.release_record(self.pm1, dict(phase0, decision="Withhold"))
        self.assertFalse(s.is_released("Phase 0 capture"))
        with self.assertRaises(PermissionError):
            s.release_record(self.pm1, dict(RELEASE, scope="Live pilot"))

    def test_breach_restart_refusals(self):
        s = self.store
        self.approve_all()
        with self.assertRaises(ValueError):
            s.breach_record(self.pm1, dict(BREACH, scope_kind="street"))
        # recorded_at has minute resolution, so pin the earlier time instead of racing the clock
        with patch("zava_forward.core.controls.now", return_value="1970-01-01T00:00"):
            early = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        b = s.breach_record(tf.U["QI-1"], BREACH)
        restart = dict(
            id=b["id"],
            release_id=early["id"],
            authority_ref="OD-35 demo",
            remediation_evidence="Synthetic remediation",
        )
        with self.assertRaisesRegex(ValueError, "Choose one of the breaches"):
            s.breach_restart(self.pm2, dict(restart, id="BRE-99"))
        with self.assertRaisesRegex(PermissionError, "after the breach"):
            s.breach_restart(self.pm2, restart)
        withheld = s.release_record(
            self.pm1, dict(RELEASE, scope="Phase 0 capture", decision="Withhold")
        )
        with self.assertRaisesRegex(PermissionError, "Release decision"):
            s.breach_restart(self.pm2, dict(restart, release_id=withheld["id"]))
        self.assertTrue(s.is_paused("archetype", "Solid wall"))
        later = s.release_record(self.pm1, dict(RELEASE, scope="Phase 0 capture"))
        s.breach_restart(self.pm2, dict(restart, release_id=later["id"]))
        self.assertFalse(s.is_paused("archetype", "Solid wall"))
        with self.assertRaisesRegex(ValueError, "not paused"):
            s.breach_restart(self.pm2, dict(restart, release_id=later["id"]))

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
        again = SqlStore(
            str(Path(self.tmp.name) / "zavaforward.json"), os.path.join(self.tmp.name, "pw.sqlite")
        )
        self.assertEqual(again.capture_gate(), [])
        self.assertTrue(again.is_paused("archetype", "Solid wall"))


FINDINGS = (
    "GOVERN-AUDIT-01",
    "GOVERN-AUDIT-02",
    "MAP-01",
    "MAP-02",
    "MAP-04",
    "MEASURE-01",
    "MN-3.2",
    "MN-4.1",
    "MN-4.3",
    "T-RAI-001",
    "T-RAI-002",
    "GOVERN-AUDIT-04",
    "GOVERN-AUDIT-05",
    "MAP-05",
    "MEASURE-02",
    "MEASURE-03",
    "MEASURE-04",
    "MN-2.3",
    "T-RAI-005",
    "EU-COND-01",
    "EU-COND-02",
    "EU-COND-04",
)
BASELINE = "1cb398c7b90bec05a5700008a97d0cfac494144a"
ASSESSMENT = dict(
    source_commit="ab0613f3336109ff9b96560a16758ee842232715",
    task_id=None,
    task_version=None,
    release_version=None,
    nonapplicability_reason="Constructed whole-system source inspection, not a task release",
)


def claim(**changes):
    body = dict(
        finding_id="MAP-01",
        baseline_commit=BASELINE,
        assessment=copy.deepcopy(ASSESSMENT),
        evidence_tier="implemented/source-tested",
        result="Constructed source test only",
        references=["src/core/tests/test_governance.py::test_inventory"],
        limitations="No qualified human or live evidence",
        decision_maker_status="Unappointed",
        decision_maker_ref=None,
        event_ref="SYN-126-1",
        expected_revision=0,
    )
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
        self.admin.execute(
            f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
        )
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
            self.assertEqual(
                (row["closure"], row["acceptance"], row["disposition"]),
                ("Open", "Unknown", "insufficient"),
            )
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
        task = dict(
            source_commit=ASSESSMENT["source_commit"],
            task_id="task",
            task_version="1",
            release_version="r1",
            nonapplicability_reason=None,
        )
        self.store.rai_evidence_record(
            self.pm, claim(assessment=task, expected_revision=1, event_ref="SYN-TASK")
        )
        for key in ("source_commit", "task_id", "task_version", "release_version"):
            altered = dict(task, **{key: "e" * 40 if key == "source_commit" else "changed"})
            self.assertEqual(self.view(altered)["current_disposition_count"], 0)
        historical = dict(ASSESSMENT, source_commit=BASELINE)
        self.store.rai_evidence_record(
            self.pm, claim(assessment=historical, expected_revision=2, event_ref="SYN-BASE")
        )
        self.assertEqual(self.view(historical)["current_disposition_count"], 0)

    def test_complete_is_not_accepted_or_closed(self):
        for i, fid in enumerate(FINDINGS):
            self.store.rai_evidence_record(
                self.pm,
                claim(
                    finding_id=fid,
                    expected_revision=i,
                    event_ref=f"SYN-{i}",
                    evidence_tier="insufficient",
                ),
            )
        v = self.view()
        self.assertEqual(v["current_disposition_count"], 22)
        self.assertTrue(v["dispositions_complete"])
        self.assertEqual(v["open_count"], 22)
        self.assertTrue(all(r["acceptance"] == "Unknown" for r in v["findings"]))

    def test_prd_review_and_owner_acceptance_stay_separate_from_report_and_claims(self):
        pm2 = tf.U["PM-2"]
        gov0 = self.store.governance_view(self.pm, ASSESSMENT)
        self.assertEqual(gov0["prd_quality_review"], g.PRD_QUALITY_REVIEW)
        self.assertEqual(gov0["prd_owner_acceptance"], g.PRD_OWNER_ACCEPTANCE)
        self.assertEqual(gov0["rai_evidence"]["prd_quality_review"], g.PRD_QUALITY_REVIEW)
        self.assertEqual(gov0["rai_evidence"]["prd_owner_acceptance"], g.PRD_OWNER_ACCEPTANCE)
        self.assertFalse(gov0["prd_quality_review"]["satisfied"])
        self.assertFalse(gov0["prd_quality_review"]["accepted"])
        self.assertFalse(gov0["prd_owner_acceptance"]["accepted"])
        self.assertTrue(gov0["prd_quality_review"]["separate_from_report_acceptance"])
        self.assertTrue(gov0["prd_quality_review"]["separate_from_remediation_completion"])
        self.assertTrue(gov0["prd_owner_acceptance"]["separate_from_report_acceptance"])
        self.assertTrue(gov0["prd_owner_acceptance"]["separate_from_remediation_completion"])
        self.assertEqual(
            gov0["rai_evidence"]["baseline"]["acceptance_scope"],
            "baseline-assessment-and-remediation-planning only",
        )
        for forbidden in (
            {"prd_quality_review": {"satisfied": True, "accepted": True}},
            {"prd_owner_acceptance": {"accepted": True}},
            {"affected_dispatch": "ENABLED"},
            {"conditional_eu_assurance": "Satisfied"},
            {"live_use": "APPROVED"},
        ):
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(ValueError):
                    self.store.rai_evidence_record(self.pm, claim(**forbidden))
        for i, fid in enumerate(FINDINGS):
            self.store.rai_evidence_record(
                self.pm,
                claim(
                    finding_id=fid,
                    expected_revision=i,
                    event_ref=f"SYN-SEP-{i}",
                    evidence_tier="independent-acceptance",
                    decision_maker_status="Unverified reference",
                    decision_maker_ref="Synthetic exercise reviewer",
                ),
            )
        self.store.protocol_freeze(self.pm, dict(PROTOCOL, synthetic=True))
        self.store.protocol_approve(pm2, dict(dpia_ref="DPIA-DEMO", lawful_basis_ref="LB-DEMO"))
        self.store.benefits_record(
            self.pm, dict(BENEFITS, mde_cycle_time_pct=10, mde_coordination_hours_pct=10)
        )
        self.store.benefits_approve(pm2, {})
        self.store.release_record(self.pm, dict(RELEASE, scope="Phase 0 capture"))
        with self.store.lock:
            self.store.data["governance"]["prd_quality_review"] = {
                "satisfied": True,
                "accepted": True,
            }
            self.store.data["governance"]["prd_owner_acceptance"] = {"accepted": True}
            self.store.data["governance"]["affected_dispatch"] = "ENABLED"
            self.store.data["governance"]["conditional_eu_assurance"] = "Applied"
            self.store.save()
        self.store = self.reopen()
        gov = self.store.governance_view(self.pm, ASSESSMENT)
        rai = gov["rai_evidence"]
        self.assertTrue(rai["dispositions_complete"])
        self.assertEqual(rai["current_disposition_count"], 22)
        self.assertEqual(gov["prd_quality_review"], g.PRD_QUALITY_REVIEW)
        self.assertEqual(gov["prd_owner_acceptance"], g.PRD_OWNER_ACCEPTANCE)
        self.assertEqual(rai["prd_quality_review"], g.PRD_QUALITY_REVIEW)
        self.assertEqual(rai["prd_owner_acceptance"], g.PRD_OWNER_ACCEPTANCE)
        gov["prd_quality_review"]["accepted"] = True
        rai["prd_owner_acceptance"]["accepted"] = True
        fresh = self.store.governance_view(self.pm, ASSESSMENT)
        self.assertFalse(fresh["prd_quality_review"]["accepted"])
        self.assertFalse(fresh["rai_evidence"]["prd_owner_acceptance"]["accepted"])

    def test_live_use_blocked_dispatch_disabled_and_conditional_eu_guards(self):
        self.assertEqual(g.RAI_EU_CONDITIONAL, ("EU-COND-01", "EU-COND-02", "EU-COND-04"))
        v0 = self.view()
        self.assertEqual(
            v0["live_use"], "BLOCKED pending separate qualified evidence and approvals"
        )
        self.assertEqual(
            v0["affected_dispatch"],
            "DISABLED until appropriate evidence and qualified approvals exist",
        )
        self.assertEqual(
            v0["conditional_eu_assurance"],
            "Applies only after qualified applicability review",
        )
        by_id = {row["finding_id"]: row for row in v0["findings"]}
        for fid, row in by_id.items():
            is_eu = fid in g.RAI_EU_CONDITIONAL
            self.assertEqual(row["conditional_eu"], is_eu)
            self.assertEqual(
                row["applicability_review"],
                "Required before conditional EU assurance applies"
                if is_eu
                else "Not conditional EU check",
            )
        for i, fid in enumerate(g.RAI_EU_CONDITIONAL):
            self.store.rai_evidence_record(
                self.pm,
                claim(
                    finding_id=fid,
                    expected_revision=i,
                    event_ref=f"SYN-EU-{i}",
                    evidence_tier="independent-acceptance",
                    decision_maker_status="Unverified reference",
                    decision_maker_ref="Synthetic legal note (not qualified review)",
                ),
            )
        self.store = self.reopen()
        v1 = self.view()
        self.assertEqual(
            v1["live_use"], "BLOCKED pending separate qualified evidence and approvals"
        )
        self.assertEqual(
            v1["affected_dispatch"],
            "DISABLED until appropriate evidence and qualified approvals exist",
        )
        self.assertEqual(
            v1["conditional_eu_assurance"],
            "Applies only after qualified applicability review",
        )
        eu_rows = {row["finding_id"]: row for row in v1["findings"] if row["conditional_eu"]}
        self.assertEqual(set(eu_rows), set(g.RAI_EU_CONDITIONAL))
        for row in eu_rows.values():
            self.assertEqual(row["baseline_status"], "NOT_ASSESSED")
            self.assertEqual(row["baseline_verdict"], "UNCHANGED")
            self.assertEqual(
                row["applicability_review"],
                "Required before conditional EU assurance applies",
            )
            self.assertEqual(row["closure"], "Open")
            self.assertEqual(row["acceptance"], "Unknown")
            self.assertEqual(row["evidence_adequacy"], "Not independently established")

    def test_invalid_promotions_and_primitives_leave_no_success(self):
        bad = [
            {"actor": self.pm},
            {"recorded_at": "yesterday"},
            {"approval": True},
            {"closure": "Closed"},
            {"evidence_tier": "accepted"},
            {"finding_id": "UNKNOWN"},
            {"baseline_commit": "a" * 40},
            {"expected_revision": True},
            {"expected_revision": -1},
            {"result": {}},
            {"result": "x" * 2001},
            {"references": []},
            {"references": ["x"] * 21},
            {"references": [{}]},
            {"references": ["x" * 501]},
            {"limitations": ""},
            {"decision_maker_ref": "self appointed"},
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
        self.assertFalse(
            [a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]
        )

    def test_inert_limits_and_independent_acceptance_is_only_claim(self):
        body = claim(
            result="x" * 2000,
            limitations="x" * 2000,
            references=["https://127.0.0.1/no-fetch"] + ["x" * 500] * 19,
            event_ref="x" * 200,
            decision_maker_status="Unverified reference",
            decision_maker_ref="x" * 500,
            evidence_tier="independent-acceptance",
        )
        with patch("urllib.request.urlopen", side_effect=AssertionError("must not fetch")):
            self.store.rai_evidence_record(self.pm, body)
        row = self.view()["findings"][2]
        self.assertEqual((row["closure"], row["acceptance"]), ("Open", "Unknown"))

    def test_all_tiers_and_explicit_owner_unknown_are_claims(self):
        for i, tier in enumerate(g.RAI_TIERS):
            self.store.rai_evidence_record(
                self.pm,
                claim(
                    evidence_tier=tier,
                    expected_revision=i,
                    event_ref=f"TIER-{i}",
                    decision_maker_status="Unknown",
                ),
            )
        row = self.view()["findings"][2]
        self.assertEqual([r["evidence_tier"] for r in row["claims"]], list(g.RAI_TIERS))
        self.assertEqual((row["closure"], row["acceptance"]), ("Open", "Unknown"))

    def test_schema_boundaries_and_legacy_insufficiency(self):
        for changes in (
            {"limitations": "x" * 2001},
            {"event_ref": "x" * 201},
            {"decision_maker_status": "Unverified reference", "decision_maker_ref": "x" * 501},
            {"assessment": dict(ASSESSMENT, nonapplicability_reason="x" * 601)},
            {"assessment": dict(ASSESSMENT, source_commit="A" * 40)},
            {"assessment": dict(ASSESSMENT, task_id="task", task_version="v", release_version="r")},
            {"references": "not a list"},
            {"expected_revision": 1.0},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    self.store.rai_evidence_record(self.pm, claim(**changes))
        binding = dict(
            source_commit="f" * 40,
            task_id="t" * 200,
            task_version="v" * 200,
            release_version="r" * 200,
            nonapplicability_reason=None,
        )
        for key in ("task_id", "task_version", "release_version"):
            with self.assertRaises(ValueError):
                self.store.rai_evidence_record(
                    self.pm, claim(assessment=dict(binding, **{key: "x" * 201}))
                )
        self.store.rai_evidence_record(self.pm, claim(assessment=binding))
        self.assertEqual(self.view(binding)["current_disposition_count"], 1)
        self.store.rai_evidence_record(
            self.pm,
            claim(
                assessment=dict(ASSESSMENT, nonapplicability_reason="x" * 600),
                expected_revision=1,
                event_ref="MAX-REASON",
            ),
        )
        # Legacy unproven history must not be credited or silently repaired.
        with self.store.lock:
            self.store.data["governance"]["rai_claims"].append(
                {"finding_id": "MAP-01", "status": "accepted"}
            )
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
        self.assertFalse(
            [a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]
        )

    def test_current_roles_forgery_removal_and_demotion(self):
        for user in (
            tf.U["RLO-1"],
            tf.U["CON-1"],
            dict(self.pm, name="forged"),
            dict(self.pm, email="unknown@example.test"),
            dict(tf.U["CON-1"], role=self.pm["role"]),
        ):
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
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(user), self.pm["email"])
            )
            original()

        with patch.object(self.store, "save", side_effect=demote):
            with self.assertRaises(PermissionError):
                self.store.rai_evidence_record(self.pm, claim())
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(self.pm), self.pm["email"])
        )
        append = self.store._append_audit

        def failure(entries):
            append(entries)
            raise RuntimeError("constructed precommit failure")

        with patch.object(self.store, "_append_audit", side_effect=failure):
            with self.assertRaisesRegex(RuntimeError, "precommit"):
                self.store.rai_evidence_record(self.pm, claim())
        self.assertEqual(self.view()["history_record_count"], 0)
        self.assertFalse(
            [a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]
        )

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
        self.assertEqual(
            len([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]), 1
        )

    def test_immediate_postcommit_hook_failure_has_witness(self):
        with patch(
            "zava_forward.core.appointments.mark_committed",
            side_effect=RuntimeError("after COMMIT"),
        ):
            with self.assertRaises(g.GovernanceCommittedError):
                self.store.rai_evidence_record(self.pm, claim())
        self.store = self.reopen()
        self.assertEqual(self.view()["history_record_count"], 1)
        self.assertEqual(
            len([a for a in self.store.audit_entries() if a["action"] == "rai_evidence_record"]), 1
        )

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
            with (
                patch.object(
                    self.store, "_proc_sync", side_effect=RuntimeError("recovery unavailable")
                ),
                patch.object(
                    self.store, "_append_audit", side_effect=RuntimeError("precommit unavailable")
                ),
            ):
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


REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
DOC_FENCE_RE = re.compile(r"```.*?```", re.S)
DOC_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
TRACKING_SEGMENT = "." + "-".join(("copilot", "tracking"))


def _github_slugs(markdown_text):
    cleaned = DOC_FENCE_RE.sub("", markdown_text)
    slugs = set()
    counts = {}
    for match in DOC_HEADING_RE.finditer(cleaned):
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", match.group(2))
        heading = heading.replace("`", "").strip().lower()
        base = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        seen = counts.get(base, 0)
        counts[base] = seen + 1
        slugs.add(base if seen == 0 else f"{base}-{seen}")
    return slugs


def _section_text(markdown_text, heading_line):
    idx = markdown_text.index(heading_line)
    level = len(heading_line.split(" ", 1)[0])
    rest = markdown_text[idx + len(heading_line) :]
    next_heading = re.search(rf"^#{{1,{level}}}\s+", rest, re.M)
    end = idx + len(heading_line) + next_heading.start() if next_heading else len(markdown_text)
    return markdown_text[idx:end]


class GovernanceDocumentationContractTests(unittest.TestCase):
    def setUp(self):
        if not (REPO_ROOT / "docs").is_dir():
            self.skipTest("repository docs are not in this image")

    def test_addendum_prd_adr_and_core_guide_record_separation_and_preserve_history(self):
        docs = {
            "addendum": REPO_ROOT / "docs/case_study_48_addendum.md",
            "prd": REPO_ROOT / "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
            "adr": REPO_ROOT / "docs/adrs/0002-pilot-readiness-architecture.md",
            "core_readme": REPO_ROOT / "src/core/README.md",
        }
        normalized = {
            name: " ".join(path.read_text(encoding="utf-8").split()) for name, path in docs.items()
        }
        shared_tokens = (
            "prd_quality_review",
            "prd_owner_acceptance",
            "baseline-assessment-and-remediation-planning only",
            "DISABLED until appropriate evidence and qualified approvals exist",
            "Applies only after qualified applicability review",
            "EU-COND-01",
            "EU-COND-02",
            "EU-COND-04",
        )
        for name, text in normalized.items():
            for token in shared_tokens:
                self.assertIn(token, text, f"{name} missing {token!r}")
        expected_history = {
            "addendum": (
                "0.12.0",
                "0.14.0",
                "0.16.0",
                "0.21.0",
                g.RAI_BASELINE,
                "FAIL",
                "Validate BLOCKED",
                "Finalize NOT_EVALUATED",
                "PARTIAL",
                "NOT_ASSESSED",
                "DOWNGRADED",
                "INVALID_PAYLOAD",
            ),
            "prd": (
                'version: "0.21.0"',
                'status: "in-review"',
                'historical_exercise_accepted_version: "0.12.0"',
                "0.14.0",
                g.RAI_BASELINE,
                "FAIL",
                "Validate BLOCKED",
                "Finalize NOT_EVALUATED",
                "PARTIAL",
                "NOT_ASSESSED",
                "DOWNGRADED",
            ),
            "adr": (
                "Proposed.",
                "PARTIAL",
                "NOT_ASSESSED",
                "DOWNGRADED",
                "CONFIRMED",
                "UNCHANGED",
                "Open",
                "Unknown",
            ),
            "core_readme": (
                "0.14.0",
                g.RAI_BASELINE,
                "DOWNGRADED",
                "NOT_ASSESSED",
                "UNCHANGED",
                "Open",
                "Unknown",
            ),
        }
        for name, tokens in expected_history.items():
            for token in tokens:
                self.assertIn(token, normalized[name], f"{name} lost historical token {token!r}")

    def test_knowledge_index_and_append_only_log_record_issue_126_evidence(self):
        index_raw = (REPO_ROOT / "docs/reference/README.md").read_text(encoding="utf-8")
        index_norm = " ".join(index_raw.split())
        for token in (
            "#constructed-rai-evidence-claims-2026-10-18-126",
            "#constructed-rai-evidence-register-engineering-2026-10-18",
            "#constructed-finding-evidence-engineering-2026-10-18-126",
            "#finding-evidence-register-engineering-2026-10-18-126",
            "0.21.0",
            "0.14.0",
            "affected_dispatch",
            "conditional_eu_assurance",
            "EU-COND-01",
            "EU-COND-02",
            "EU-COND-04",
            "OD-36",
        ):
            self.assertIn(token, index_norm)
        log_raw = (REPO_ROOT / "docs/reference/log.md").read_text(encoding="utf-8")
        prior_heading = "## 2026-11-14 provenance register hardening (#159)"
        entry_heading = "## [2026-11-15] update | Governance PRD separation and conditional EU assurance boundaries (Refs #126)"
        self.assertIn(prior_heading, log_raw)
        self.assertIn(entry_heading, log_raw)
        self.assertLess(log_raw.index(prior_heading), log_raw.index(entry_heading))
        entry_norm = " ".join(_section_text(log_raw, entry_heading).split())
        for token in (
            "prd_quality_review",
            "prd_owner_acceptance",
            "affected_dispatch",
            "conditional_eu_assurance",
            "0.12.0",
            "0.14.0",
            "0.16.0",
            "0.21.0",
            g.RAI_BASELINE,
            "FAIL / Validate BLOCKED / Finalize NOT_EVALUATED",
            "PARTIAL",
            "NOT_ASSESSED",
            "DOWNGRADED",
            "INVALID_PAYLOAD",
            "OD-36",
        ):
            self.assertIn(token, entry_norm)

    def test_links_anchors_and_no_tracking_leaks_across_governance_surfaces(self):
        full_zero_tracking = (
            REPO_ROOT / "src/core/src/zava_forward/core/governance.py",
            REPO_ROOT / "src/core/README.md",
            REPO_ROOT / "docs/adrs/0002-pilot-readiness-architecture.md",
        )
        for path in full_zero_tracking:
            self.assertNotIn(TRACKING_SEGMENT, path.read_text(encoding="utf-8"), path.as_posix())
        addendum_path = REPO_ROOT / "docs/case_study_48_addendum.md"
        prd_path = REPO_ROOT / "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
        adr_path = REPO_ROOT / "docs/adrs/0002-pilot-readiness-architecture.md"
        core_readme_path = REPO_ROOT / "src/core/README.md"
        index_path = REPO_ROOT / "docs/reference/README.md"
        log_path = REPO_ROOT / "docs/reference/log.md"

        addendum_sec = _section_text(
            addendum_path.read_text(encoding="utf-8"),
            "### Constructed RAI Evidence Register Engineering (2026-10-18)",
        )
        prd_sec = _section_text(
            prd_path.read_text(encoding="utf-8"),
            "#### Constructed Finding-Evidence Engineering (2026-10-18, #126)",
        )
        index_raw = index_path.read_text(encoding="utf-8")
        index_126_match = re.search(r"For issue #126,.*?(?:\n\n|\Z)", index_raw, re.S)
        self.assertIsNotNone(index_126_match)
        index_126_sec = index_126_match.group(0)
        index_proj_docs = _section_text(index_raw, "### Project Documents")
        log_sec = _section_text(
            log_path.read_text(encoding="utf-8"),
            "## [2026-11-15] update | Governance PRD separation and conditional EU assurance boundaries (Refs #126)",
        )
        for label, snippet in (
            ("addendum #126", addendum_sec),
            ("prd #126", prd_sec),
            ("index #126", index_126_sec),
            ("log 2026-11-15 #126", log_sec),
        ):
            self.assertNotIn(TRACKING_SEGMENT, snippet, label)

        slug_cache = {}

        def assert_links_resolve(source_path, markdown_snippet, check_fragments=True):
            cleaned = DOC_FENCE_RE.sub("", markdown_snippet)
            for match in DOC_LINK_RE.finditer(cleaned):
                target = match.group(1)
                if (
                    target.startswith(("http://", "https://", "mailto:"))
                    or "{" in target
                    or "<" in target
                ):
                    continue
                if TRACKING_SEGMENT in target:
                    continue
                rel_part, sep, frag = target.partition("#")
                target_file = (source_path.parent / rel_part).resolve() if rel_part else source_path
                self.assertTrue(
                    target_file.exists(),
                    f"{source_path.relative_to(REPO_ROOT)} -> missing {target}",
                )
                if check_fragments and sep and frag and target_file.is_file():
                    if target_file not in slug_cache:
                        slug_cache[target_file] = _github_slugs(
                            target_file.read_text(encoding="utf-8")
                        )
                    self.assertIn(
                        frag,
                        slug_cache[target_file],
                        f"{source_path.relative_to(REPO_ROOT)} -> missing anchor #{frag} in {target_file.relative_to(REPO_ROOT)}",
                    )

        for full_doc in (addendum_path, prd_path, adr_path, core_readme_path):
            assert_links_resolve(
                full_doc, full_doc.read_text(encoding="utf-8"), check_fragments=True
            )
        assert_links_resolve(index_path, index_raw, check_fragments=False)
        assert_links_resolve(index_path, index_126_sec, check_fragments=True)
        assert_links_resolve(index_path, index_proj_docs, check_fragments=True)
        assert_links_resolve(log_path, log_sec, check_fragments=True)


if __name__ == "__main__":
    unittest.main()
