"""Constructed thresholds are offline-only; live needs named-human approval (issue 146)."""

from __future__ import annotations

import copy
import unittest
from typing import Any

from cohort_eval_fixture import clean_observed, manifest
from zava_forward.core import cohort_eval, monitoring_coverage, rai_release

NOW = 1_000.0
HUMAN = {
    "cohorts_owner": "Priya Shah, Data Lead",
    "lawful_fields_owner": "Tom Reed, DPO",
    "thresholds_owner": "Amina Okafor, RAI Owner",
    "expires": NOW + 3600,
}


def live_manifest(
    approval: dict[str, Any] | None = None, synthetic: bool = False
) -> dict[str, Any]:
    m = copy.deepcopy(manifest())
    m["synthetic"] = synthetic
    m.pop("approval", None)
    return cohort_eval.approve(m, approval if approval is not None else HUMAN)


def codes(m: dict[str, Any], **kw: Any) -> set[str]:
    rec = cohort_eval.evaluate(m, clean_observed(m), live=True, now=NOW, **kw)
    return {b["code"] for b in rec["blockers"]}


class OfflineUse(unittest.TestCase):
    def test_constructed_thresholds_still_work_offline(self) -> None:
        m = manifest()
        rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertTrue(rec["activation_allowed"])
        self.assertFalse(rec["fairness_evidence"])


class LiveCohortThresholds(unittest.TestCase):
    def test_valid_named_human_approval_is_accepted(self) -> None:
        m = live_manifest()
        rec = cohort_eval.evaluate(m, clean_observed(m), live=True, now=NOW)
        self.assertEqual(rec["blockers"], [])
        self.assertTrue(rec["activation_allowed"])

    def test_constructed_manifest_is_rejected_even_with_named_approval(self) -> None:
        m = live_manifest(synthetic=True)
        self.assertIn("constructed_thresholds_live", codes(m))
        rec = cohort_eval.evaluate(m, clean_observed(m), live=True, now=NOW)
        self.assertFalse(rec["activation_allowed"])

    def test_human_disposition_cannot_clear_constructed_or_approval_gaps(self) -> None:
        disposition = {"by": "RAI owner", "decision": "accept", "rationale": "reviewed"}
        for m in (
            live_manifest(synthetic=True),
            live_manifest(dict(HUMAN, thresholds_owner="agent")),
        ):
            rec = cohort_eval.evaluate(m, clean_observed(m), disposition, live=True, now=NOW)
            self.assertFalse(rec["activation_allowed"])

    def test_missing_blank_or_unapproved_owner_is_rejected(self) -> None:
        for value in ("", "  ", "unapproved", "unknown", None):
            m = live_manifest(dict(HUMAN, thresholds_owner=value))
            found = codes(m)
            self.assertTrue(
                {"unapproved_thresholds", "live_approval_not_named_human"} <= found, value
            )

    def test_system_or_agent_attributed_owner_is_rejected(self) -> None:
        for value in ("system", "Copilot Agent", "release-bot", "AI assistant", "automation"):
            m = live_manifest(dict(HUMAN, cohorts_owner=value))
            self.assertIn("live_approval_not_named_human", codes(m), value)

    def test_expired_or_unverifiable_approval_is_rejected(self) -> None:
        for expires in (NOW, NOW - 1, None, True, float("nan")):
            m = live_manifest(dict(HUMAN, expires=expires))
            self.assertIn("live_approval_expired", codes(m), expires)
        m = live_manifest()
        rec = cohort_eval.evaluate(m, clean_observed(m), live=True)
        self.assertIn("live_approval_expired", {b["code"] for b in rec["blockers"]})

    def test_threshold_edit_after_approval_voids_live_approval(self) -> None:
        m = live_manifest()
        m["thresholds"]["max_error_rate"] = 0.9
        self.assertIn("unapproved_thresholds", codes(m))

    def test_fictional_or_placeholder_owner_is_rejected_for_live_use(self) -> None:
        for value in ("Data lead (fictional)", "DPO placeholder", "Mock RAI Owner", "TBD"):
            m = live_manifest(dict(HUMAN, lawful_fields_owner=value))
            rec = cohort_eval.evaluate(m, clean_observed(m), live=True, now=NOW)
            self.assertIn("live_approval_not_named_human", {b["code"] for b in rec["blockers"]})
            self.assertNotEqual(rec["owner_approval_status"], "approved")
            self.assertFalse(rec["lawful_analysis_fields_approved"])
            self.assertFalse(rec["live_activation_allowed"])
            self.assertFalse(rec["fairness_evidence"])

    def test_undated_or_malformed_approval_date_blocks_live_use(self) -> None:
        undated_owners = {k: v for k, v in HUMAN.items() if k != "expires"}
        m_undated = live_manifest(undated_owners)
        rec_undated = cohort_eval.evaluate(m_undated, clean_observed(m_undated), live=True, now=NOW)
        self.assertIn("live_approval_undated", {b["code"] for b in rec_undated["blockers"]})
        self.assertEqual(rec_undated["owner_approval_status"], "pending_owner_approval")
        self.assertFalse(rec_undated["lawful_analysis_fields_approved"])
        self.assertFalse(rec_undated["activation_allowed"])
        self.assertFalse(rec_undated["fairness_evidence"])

        for bad_date in ("", "not-a-date", "20261114", NOW + 10):
            m_bad = live_manifest(dict(HUMAN, approved_at=bad_date))
            rec_bad = cohort_eval.evaluate(m_bad, clean_observed(m_bad), live=True, now=NOW)
            self.assertIn("live_approval_undated", {b["code"] for b in rec_bad["blockers"]})
            self.assertEqual(rec_bad["owner_approval_status"], "unapproved")
            self.assertFalse(rec_bad["lawful_analysis_fields_approved"])
            self.assertFalse(rec_bad["activation_allowed"])


class LiveReleaseApprover(unittest.TestCase):
    def gaps(self, approver: Any) -> list[str]:
        record = {
            "approver": approver,
            "serving_model": "m1",
            "expires": NOW + 10,
            "evidence_class": "actual",
        }
        return rai_release.missing_binding(record, {"model_version": "m1"}, [], NOW, True)

    def test_named_human_approver_passes_live(self) -> None:
        self.assertEqual(self.gaps({"name": "Amina Okafor", "email": "amina@zava.example"}), [])

    def test_blank_missing_or_system_approver_fails_live(self) -> None:
        bad: tuple[Any, ...] = (
            None,
            {},
            {"email": " "},
            {"email": "system@zava.example"},
            {"name": "Release Agent", "email": "amina@zava.example"},
        )
        for approver in bad:
            self.assertIn("named human release approver", self.gaps(approver), approver)

    def test_constructed_fixture_class_fails_live_but_not_offline(self) -> None:
        record = {
            "approver": {"email": "amina@zava.example"},
            "serving_model": "m1",
            "expires": NOW + 10,
            "evidence_class": "constructed-fixture",
        }
        binding = {"model_version": "m1"}
        self.assertTrue(rai_release.missing_binding(record, binding, [], NOW, True))
        self.assertEqual(rai_release.missing_binding(record, binding, [], NOW, False), [])

    def test_expired_release_fails(self) -> None:
        record = {
            "approver": {"email": "amina@zava.example"},
            "serving_model": "m1",
            "expires": NOW - 1,
            "evidence_class": "actual",
        }
        self.assertIn(
            "unexpired release",
            rai_release.missing_binding(record, {"model_version": "m1"}, [], NOW, True),
        )

    def test_live_release_rejects_constructed_or_non_human_monitoring_thresholds(self) -> None:
        constructed_decl = monitoring_coverage.task_declaration("stock-prioritisation")
        spec = {"monitoring_declaration": copy.deepcopy(constructed_decl)}
        record = {
            "approver": {"name": "Amina Okafor", "email": "amina@zava.example"},
            "serving_model": "m1",
            "expires": NOW + 10,
            "evidence_class": "actual",
            "monitoring_declaration": constructed_decl,
        }
        binding = {"model_version": "m1"}
        self.assertEqual(rai_release.missing_binding(record, binding, [], NOW, False), [])
        self.assertIn(
            "named-human approved live monitoring thresholds",
            rai_release.missing_binding(record, binding, [], NOW, True),
        )
        for bad in ("Copilot Agent", "Data lead (fictional)", "TBD"):
            bad_decl = copy.deepcopy(constructed_decl)
            for item in bad_decl["indicators"].values():
                item["threshold"] = {"limit": 0.05, "min_sample": 20, "approved_by": bad}
            self.assertIn(
                "named-human approved live monitoring thresholds",
                rai_release.missing_binding(
                    dict(record, monitoring_declaration=bad_decl), binding, [], NOW, True
                ),
            )
        approved_decl = copy.deepcopy(constructed_decl)
        for item in approved_decl["indicators"].values():
            item["threshold"] = {
                "limit": 0.05,
                "min_sample": 20,
                "approved_by": "Amina Okafor, RAI Assurance Lead",
            }
        self.assertTrue(rai_release.valid_monitoring_declaration(approved_decl, spec))
        self.assertEqual(
            rai_release.missing_binding(
                dict(record, monitoring_declaration=approved_decl), binding, [], NOW, True
            ),
            [],
        )
        weakened = copy.deepcopy(approved_decl)
        weakened["indicators"]["cohort_errors"] = {"applicable": False, "reason": "skip"}
        self.assertFalse(rai_release.valid_monitoring_declaration(weakened, spec))


if __name__ == "__main__":
    unittest.main()
