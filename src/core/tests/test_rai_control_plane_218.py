"""Focused unit tests for Epic #218 RAI control plane, OQ-017 gating, and readiness."""

from __future__ import annotations

import copy
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset as _dataset
import release_support as _release_support
from zava_forward.core import (
    ai_registry as _ai_registry,
)
from zava_forward.core import (
    assistants as _assistants,
)
from zava_forward.core import (
    rai_control_plane,
)
from zava_forward.core import (
    rai_release as _rai_release,
)
from zava_forward.core.ai import Ai as _Ai
from zava_forward.core.sqlstore import SqlStore as _SqlStore
from zava_forward.core.store import Store as _Store

dataset_mod: Any = _dataset
ai_registry: Any = _ai_registry
assistants_mod: Any = _assistants
rai_release: Any = _rai_release
Ai: Any = _Ai
SqlStore: Any = _SqlStore
Store: Any = _Store
release_support: Any = _release_support

EXPECTED_REQUIREMENT_IDS = frozenset(
    {
        "FR-051",
        "FR-052",
        "FR-053",
        "FR-054",
        "NFR-014",
        "AC-069",
        "AC-070",
        "AC-071",
        "AC-072",
        "AC-073",
        "OQ-017",
        "OQ-018",
        "OQ-019",
        "RULE-024",
        "RULE-020",
    }
)


def _pm_actor(store: Any) -> dict[str, Any]:
    staff_rows: list[dict[str, Any]] = list(store.data["staff"])
    for member in staff_rows:
        if member.get("role") == "Retrofit Programme Manager":
            return dict(member)
    return {
        "name": "Priya Nair",
        "email": "pm@zavanorth.example",
        "role": "Retrofit Programme Manager",
    }


def _make_json_store(tmp_dir: str, name: str = "json") -> Any:
    sub = Path(tmp_dir) / name
    sub.mkdir(parents=True, exist_ok=True)
    seed_path = sub / "seed.json"
    seed_path.write_text(json.dumps(copy.deepcopy(dataset_mod.DATA)), encoding="utf-8")
    return Store(str(seed_path))


def _make_sql_store(test_case: unittest.TestCase, tmp_dir: str, name: str = "sql") -> Any:
    sub = Path(tmp_dir) / name
    sub.mkdir(parents=True, exist_ok=True)
    seed_path = sub / "seed.json"
    seed_path.write_text(json.dumps(copy.deepcopy(dataset_mod.DATA)), encoding="utf-8")
    store = SqlStore(str(seed_path), str(sub / "store.sqlite3"))
    test_case.addCleanup(store.db.close)
    return store


class RaiControlPlane218Tests(unittest.TestCase):
    """Prove Epic #218 core acceptance criteria with deterministic unit checks."""

    def test_oq017_rejects_missing_blank_system_and_placeholder_approvals_with_audit(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_store = _make_json_store(tmp, "json-reject")
            actor = _pm_actor(json_store)
            invalid_cases: list[tuple[str, str, dict[str, Any] | None]] = [
                ("missing_dict", "funding-evidence", None),
                (
                    "blank_approver",
                    "funding-evidence",
                    {"approved_by": "   ", "named_approval_id": "OQ017-REL-2026-01"},
                ),
                (
                    "system_approver",
                    "funding-evidence",
                    {
                        "approved_by": "github-actions[bot]",
                        "named_approval_id": "OQ017-REL-2026-01",
                    },
                ),
                (
                    "placeholder_id",
                    "funding-evidence",
                    {
                        "approved_by": "Amina Okafor, RAI Assurance Lead",
                        "named_approval_id": "synthetic-approval-01",
                    },
                ),
                (
                    "disabled_task",
                    str(ai_registry.CONCERN_PACK_TASK),
                    {
                        "approved_by": "Amina Okafor, RAI Assurance Lead",
                        "named_approval_id": "OQ017-REL-2026-01",
                    },
                ),
                (
                    "unknown_task",
                    "unregistered-live-task",
                    {
                        "approved_by": "Amina Okafor, RAI Assurance Lead",
                        "named_approval_id": "OQ017-REL-2026-01",
                    },
                ),
            ]
            before_count = len(list(json_store.audit_entries()))
            for label, task_id, approval in invalid_cases:
                with self.subTest(store="json", case=label):
                    with self.assertRaises(rai_control_plane.LiveActivationApprovalError) as ctx:
                        json_store.activate_ai_task_live(actor, task_id, approval)
                    self.assertEqual(ctx.exception.code, "OQ-017")
                    self.assertIn("OQ-017", str(ctx.exception))
            json_entries = list(json_store.audit_entries())
            json_rejections = [
                entry
                for entry in json_entries[before_count:]
                if entry["action"] == rai_control_plane.AUDIT_ACTION_REJECTED
            ]
            self.assertEqual(len(json_rejections), len(invalid_cases))
            self.assertIs(json_store.verify_audit(), True)

            sql_store = _make_sql_store(self, tmp, "sql-reject")
            sql_store.ai.endpoint = "https://zava-live-openai.invalid"
            sql_actor = _pm_actor(sql_store)
            with patch.dict(
                os.environ,
                {"ZF_ASSIST_RELEASE_APPROVERS": str(sql_actor["email"])},
                clear=False,
            ):
                svc = assistants_mod.Assistants(sql_store)
                self.addCleanup(svc.stop)
                binding = assistants_mod.runtime_binding("funding-evidence", sql_store.ai)
                bad_release = release_support.fixture(
                    "funding-evidence",
                    binding,
                    cls="actual",
                    expires="2099-01-01T00:00:00Z",
                )
                bad_release["approved_by"] = ""
                with self.assertRaises(rai_control_plane.LiveActivationApprovalError) as sql_ctx:
                    svc.record_release(sql_actor, bad_release)
                self.assertIn("OQ-017", str(sql_ctx.exception))

                placeholder_release = release_support.fixture(
                    "funding-evidence",
                    binding,
                    cls="actual",
                    expires="2099-01-01T00:00:00Z",
                    named_approval_id="placeholder-live-id",
                )
                with self.assertRaises(rai_control_plane.LiveActivationApprovalError):
                    svc.record_release(sql_actor, placeholder_release)

            with patch.dict(
                os.environ,
                {"ZF_ASSIST_RELEASE_APPROVERS": "other-appointed@zavanorth.example"},
                clear=False,
            ):
                svc_unappointed = assistants_mod.Assistants(sql_store)
                self.addCleanup(svc_unappointed.stop)
                binding = assistants_mod.runtime_binding("funding-evidence", sql_store.ai)
                valid_body = release_support.fixture(
                    "funding-evidence",
                    binding,
                    cls="actual",
                    expires="2099-01-01T00:00:00Z",
                )
                with self.assertRaises(rai_control_plane.LiveActivationApprovalError) as unapp_ctx:
                    svc_unappointed.record_release(sql_actor, valid_body)
                self.assertIn("OQ-017", str(unapp_ctx.exception))

            sql_audits = [
                entry
                for entry in sql_store.audit_entries()
                if entry["action"] == rai_control_plane.AUDIT_ACTION_REJECTED
            ]
            self.assertEqual(len(sql_audits), 3)
            for entry in sql_audits:
                detail = json.loads(entry["detail"])
                self.assertEqual(detail["code"], "OQ-017")
                self.assertEqual(detail["decision"], "rejected")
            self.assertIs(sql_store.verify_audit(), True)

            conn = sql_store.assistant_connection()
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT COUNT(*) FROM assistant_events WHERE body LIKE ?",
                    (f"%{rai_control_plane.EVENT_KIND_REJECTED}%",),
                )
                row = cur.fetchone()
                self.assertEqual(int(row[0]), 3)
                cur.execute(
                    "SELECT body FROM assistant_releases WHERE id NOT LIKE 'fx-%'",
                )
                self.assertEqual(cur.fetchall(), [])
            finally:
                conn.close()

    def test_oq017_accepts_valid_named_human_live_activation_and_records_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sql_store = _make_sql_store(self, tmp, "sql-approved")
            sql_store.ai.endpoint = "https://zava-live-openai.invalid"
            actor = _pm_actor(sql_store)
            with patch.dict(
                os.environ,
                {"ZF_ASSIST_RELEASE_APPROVERS": str(actor["email"])},
                clear=False,
            ):
                svc = assistants_mod.Assistants(sql_store)
                self.addCleanup(svc.stop)
                binding = assistants_mod.runtime_binding("funding-evidence", sql_store.ai)
                valid_body = release_support.fixture(
                    "funding-evidence",
                    binding,
                    cls="actual",
                    expires="2099-01-01T00:00:00Z",
                )
                result = sql_store.activate_ai_task_live(
                    actor,
                    "funding-evidence",
                    valid_body,
                    assistants_service=svc,
                    release_body=valid_body,
                )
                self.assertEqual(result["status"], "active")
                self.assertEqual(result["code"], "OQ-017")
                self.assertEqual(result["approved_by"], "Amina Okafor, RAI Assurance Lead")
                self.assertEqual(result["named_approval_id"], "OQ017-APPROVAL-2026-01")
                self.assertIsNotNone(result["release_id"])

                recorded = [
                    entry
                    for entry in sql_store.audit_entries()
                    if entry["action"] == rai_control_plane.AUDIT_ACTION_RECORDED
                ]
                self.assertEqual(len(recorded), 1)
                self.assertIs(sql_store.verify_audit(), True)

        bound = ("prompt_version", "policy_version")
        bare_live = {
            "evidence_class": "actual",
            "actual_authorisation": True,
            "serving_model": "gpt-4o-2024-11-20",
            "expires": 4070908800.0,
            "prompt_version": "p1",
            "policy_version": "pol1",
            "approver": {
                "name": "Amina Okafor",
                "email": "amina@zavanorth.example",
            },
        }
        bare_binding = {
            "model_version": "gpt-4o-2024-11-20",
            "prompt_version": "p1",
            "policy_version": "pol1",
        }
        self.assertEqual(
            rai_release.missing_binding(
                bare_live,
                bare_binding,
                bound,
                1700000000.0,
                live=True,
            ),
            [],
        )
        with_bad_approver = dict(
            bare_live,
            approved_by="ci-pipeline",
            named_approval_id="placeholder-01",
        )
        missing = rai_release.missing_binding(
            with_bad_approver,
            bare_binding,
            bound,
            1700000000.0,
            live=True,
        )
        self.assertIn("named human approved_by (OQ-017)", missing)
        self.assertIn("named_approval_id (OQ-017)", missing)

        only_approver = dict(bare_live, approved_by="Amina Okafor, RAI Assurance Lead")
        self.assertIn(
            "named_approval_id (OQ-017)",
            rai_release.missing_binding(
                only_approver,
                bare_binding,
                bound,
                1700000000.0,
                live=True,
            ),
        )
        only_id = dict(bare_live, named_approval_id="OQ017-APPROVAL-2026-01")
        self.assertIn(
            "named human approved_by (OQ-017)",
            rai_release.missing_binding(
                only_id,
                bare_binding,
                bound,
                1700000000.0,
                live=True,
            ),
        )
        bool_expiry = dict(
            bare_live,
            expires=True,
            approved_by="Amina Okafor, RAI Assurance Lead",
            named_approval_id="OQ017-APPROVAL-2026-01",
        )
        self.assertIn(
            "unexpired release",
            rai_release.missing_binding(
                bool_expiry,
                bare_binding,
                bound,
                0.0,
                live=True,
            ),
        )

    def test_stored_sql_row_without_oq017_or_with_drifted_binding_is_denied_live(self) -> None:
        from zava_forward.core import assistant_release as _rel

        rel: Any = _rel
        with tempfile.TemporaryDirectory() as tmp:
            sql_store = _make_sql_store(self, tmp, "sql-stored-hardening")
            actor = _pm_actor(sql_store)
            live_ai = Ai()
            live_ai.endpoint = "https://zava-live-openai.invalid"
            live_ai.model_version = "gpt-4o-2024-11-20"
            sql_store.ai = live_ai
            with patch.dict(
                os.environ,
                {"ZF_AI": "openai", "ZF_ASSIST_RELEASE_APPROVERS": str(actor["email"])},
                clear=False,
            ):
                svc = assistants_mod.Assistants(sql_store)
                self.addCleanup(svc.stop)
                release_support.install(
                    sql_store,
                    live_ai,
                    model="gpt-4o-2024-11-20",
                    cls="actual",
                )
                cap = "funding-evidence"
                binding = assistants_mod.runtime_binding(cap, live_ai)
                legacy_row = release_support.fixture(
                    cap,
                    binding,
                    model="gpt-4o-2024-11-20",
                    cls="actual",
                )
                legacy_row.pop("approved_by", None)
                legacy_row.pop("named_approval_id", None)

                with svc.transaction() as db:
                    db.execute(
                        "UPDATE assistant_releases SET body=? WHERE id=?",
                        (rel.canonical(legacy_row), f"fx-{cap}"),
                    )
                    now_ts = svc.now(db)
                    selected, denied = rel.assessment(
                        db,
                        cap,
                        binding,
                        now_ts,
                        live=True,
                    )
                    self.assertIsNone(selected)
                    self.assertIsNotNone(denied)
                    self.assertIn("named human approved_by (OQ-017)", denied["missing"])
                    self.assertIn("named_approval_id (OQ-017)", denied["missing"])

                report_missing_oq017 = sql_store.ai_live_report(actor, assistants_service=svc)
                oq017_missing_check = report_missing_oq017["real_ai_delivery_gate"]["checks"][
                    "oq017_named_live_releases_recorded"
                ]
                self.assertIn(cap, oq017_missing_check["unapproved_live_tasks"])

                drifted_row = release_support.fixture(
                    cap,
                    dict(binding, prompt_version="drifted-prompt-v0"),
                    model="gpt-4o-2024-11-20",
                    cls="actual",
                )
                with svc.transaction() as db:
                    db.execute(
                        "UPDATE assistant_releases SET body=? WHERE id=?",
                        (rel.canonical(drifted_row), f"fx-{cap}"),
                    )

                report_drifted = sql_store.ai_live_report(actor, assistants_service=svc)
                oq017_drifted_check = report_drifted["real_ai_delivery_gate"]["checks"][
                    "oq017_named_live_releases_recorded"
                ]
                self.assertIn(cap, oq017_drifted_check["unapproved_live_tasks"])
                self.assertNotIn(cap, oq017_drifted_check["approved_live_tasks"])
                with svc.transaction() as db:
                    row_status = db.execute(
                        "SELECT status FROM assistant_releases WHERE id=?",
                        (f"fx-{cap}",),
                    ).fetchone()[0]
                self.assertEqual(row_status, "active")

    def test_requirement_traceability_covers_all_15_ids_and_resolves_ast_targets(self) -> None:
        rows = rai_control_plane.requirement_traceability()
        self.assertEqual(len(rows), 15)
        by_id = rai_control_plane.requirement_traceability_map()
        self.assertEqual(set(by_id), EXPECTED_REQUIREMENT_IDS)

        for req_id, entry in by_id.items():
            with self.subTest(requirement_id=req_id):
                self.assertIn(
                    entry["status"],
                    {"verified", "verified_with_live_deferral"},
                )
                self.assertTrue(entry["source_document"])
                self.assertTrue(entry["acceptance_checks"])
                if entry["status"] == "verified_with_live_deferral":
                    self.assertIsNotNone(entry["deferral"])
                    self.assertTrue(entry["deferral"]["owner"])
                    self.assertTrue(entry["deferral"]["reason"])

        for oq_id in ("OQ-017", "OQ-018", "OQ-019"):
            self.assertIsNotNone(by_id[oq_id]["deferral"])

        verification = rai_control_plane.verify_traceability_targets()
        self.assertEqual(verification["unresolved"], [])
        self.assertIs(verification["all_resolved"], True)

        summary = rai_control_plane.traceability_summary()
        self.assertEqual(summary["total_required"], 15)
        self.assertEqual(summary["covered_count"], 15)
        self.assertEqual(summary["missing_required_ids"], [])
        self.assertEqual(summary["unresolved_targets"], [])
        self.assertIs(summary["complete"], True)

    def test_verify_traceability_targets_fails_closed_when_target_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            test_dir = root / "src" / "core" / "tests"
            test_dir.mkdir(parents=True)
            (test_dir / "test_sample.py").write_text(
                "import unittest\n\n"
                "class BaseMixin:\n"
                "    def test_inherited(self) -> None:\n"
                "        pass\n\n"
                "class ConcreteTests(BaseMixin, unittest.TestCase):\n"
                "    pass\n",
                encoding="utf-8",
            )
            broken = rai_control_plane.verify_traceability_targets(repo_root=root)
            self.assertIs(broken["all_resolved"], False)
            self.assertGreaterEqual(len(broken["unresolved"]), 15)
            summary = rai_control_plane.traceability_summary(repo_root=root)
            self.assertEqual(summary["target_verification"], "unresolved")
            self.assertIs(summary["complete"], False)

    def test_traceability_is_complete_when_deployment_ships_no_test_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            summary = rai_control_plane.traceability_summary(repo_root=Path(tmp))
        self.assertEqual(summary["target_verification"], "test_tree_not_shipped")
        self.assertEqual(summary["missing_required_ids"], [])
        self.assertIs(summary["complete"], True)
        self.assertEqual(
            rai_control_plane.traceability_summary()["target_verification"], "verified"
        )

    def test_verify_traceability_targets_caches_default_root_immutably_under_one_ms(self) -> None:
        rai_control_plane._cached_default_traceability_targets.cache_clear()
        self.addCleanup(rai_control_plane._cached_default_traceability_targets.cache_clear)

        with patch.object(
            rai_control_plane,
            "_scan_traceability_targets",
            wraps=rai_control_plane._scan_traceability_targets,
        ) as scan_spy:
            first = rai_control_plane.verify_traceability_targets()
            self.assertIs(first["all_resolved"], True)
            self.assertEqual(first["unresolved"], [])
            self.assertEqual(scan_spy.call_count, 1)
            expected_count = first["verified_target_count"]

            first["all_resolved"] = False
            first["verified_target_count"] = 0
            first["unresolved"].append({"id": "FR-051", "target": "mutated", "reason": "mutated"})

            samples_ms: list[float] = []
            for _ in range(10):
                t0 = time.perf_counter()
                warm = rai_control_plane.verify_traceability_targets(None)
                samples_ms.append((time.perf_counter() - t0) * 1000.0)
                self.assertIs(warm["all_resolved"], True)
                self.assertEqual(warm["verified_target_count"], expected_count)
                self.assertEqual(warm["unresolved"], [])

            self.assertEqual(scan_spy.call_count, 1)
            self.assertLess(min(samples_ms), 1.0)
            self.assertLess(sum(samples_ms) / len(samples_ms), 1.0)

            with tempfile.TemporaryDirectory() as tmp:
                tmp_root = Path(tmp)
                explicit_broken = rai_control_plane.verify_traceability_targets(repo_root=tmp_root)
                self.assertIs(explicit_broken["all_resolved"], False)
                self.assertEqual(scan_spy.call_count, 2)

                still_cached = rai_control_plane.verify_traceability_targets(None)
                self.assertIs(still_cached["all_resolved"], True)
                self.assertEqual(scan_spy.call_count, 2)

                rai_control_plane._cached_default_traceability_targets.cache_clear()
                try:
                    with patch.object(
                        rai_control_plane,
                        "_default_repo_root",
                        return_value=tmp_root,
                    ):
                        broken_first = rai_control_plane.verify_traceability_targets(None)
                        self.assertIs(broken_first["all_resolved"], False)
                        self.assertTrue(broken_first["unresolved"])
                        original_reason = broken_first["unresolved"][0]["reason"]
                        self.assertEqual(scan_spy.call_count, 3)

                        broken_first["unresolved"][0]["reason"] = "mutated-reason"
                        broken_second = rai_control_plane.verify_traceability_targets(None)
                        self.assertEqual(scan_spy.call_count, 3)
                        self.assertEqual(
                            broken_second["unresolved"][0]["reason"],
                            original_reason,
                        )
                finally:
                    rai_control_plane._cached_default_traceability_targets.cache_clear()

    def test_rai_failure_does_not_change_real_ai_delivery_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = _make_json_store(tmp, "json-converse")
            actor = _pm_actor(store)
            baseline = store.rai_readiness_report(actor)
            self.assertEqual(baseline["rai_exercise_acceptance"]["status"], "passed")

            broken = copy.deepcopy(rai_control_plane.traceability_summary())
            broken["untraced_ids"] = ["FR-051"]
            broken["complete"] = False
            with patch.object(rai_control_plane, "traceability_summary", return_value=broken):
                degraded = store.rai_readiness_report(actor)

            self.assertEqual(degraded["rai_exercise_acceptance"]["status"], "failed")
            self.assertEqual(
                degraded["real_ai_delivery_gate"]["status"],
                baseline["real_ai_delivery_gate"]["status"],
            )
            self.assertEqual(
                {k: v["passed"] for k, v in degraded["real_ai_delivery_gate"]["checks"].items()},
                {k: v["passed"] for k, v in baseline["real_ai_delivery_gate"]["checks"].items()},
            )

    def test_exercise_acceptance_separates_rai_checks_from_real_ai_delivery_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_store = _make_json_store(tmp, "json-readiness")
            actor = _pm_actor(json_store)
            json_report = json_store.rai_readiness_report(actor)
            self.assertIn("rai_exercise_acceptance", json_report)
            self.assertIn("real_ai_delivery_gate", json_report)
            self.assertEqual(json_report["rai_exercise_acceptance"]["status"], "passed")
            self.assertEqual(json_report["real_ai_delivery_gate"]["status"], "blocked")
            self.assertIs(
                json_report["real_ai_delivery_gate"]["checks"]["provider_configured_and_enabled"][
                    "passed"
                ],
                False,
            )

            sql_store = _make_sql_store(self, tmp, "sql-readiness")
            sql_actor = _pm_actor(sql_store)
            offline_ai = Ai()
            offline_ai.endpoint = ""
            sql_store.ai = offline_ai
            with patch.dict(
                os.environ,
                {"ZF_AI": "off", "ZF_ASSIST_RELEASE_APPROVERS": str(sql_actor["email"])},
                clear=False,
            ):
                svc_off = assistants_mod.Assistants(sql_store)
                self.addCleanup(svc_off.stop)
                reg_off = svc_off.registry(sql_actor)
                self.assertEqual(reg_off["rai_exercise_acceptance"]["status"], "passed")
                self.assertEqual(reg_off["real_ai_delivery_gate"]["status"], "blocked")
                self.assertIs(
                    reg_off["real_ai_delivery_gate"]["checks"]["provider_configured_and_enabled"][
                        "workflow_only_forced"
                    ],
                    True,
                )

            live_ai = Ai()
            live_ai.endpoint = "https://zava-live-openai.invalid"
            live_ai.model_version = "gpt-4o-2024-11-20"
            sql_store.ai = live_ai
            with patch.dict(
                os.environ,
                {"ZF_AI": "openai", "ZF_ASSIST_RELEASE_APPROVERS": str(sql_actor["email"])},
                clear=False,
            ):
                svc_live = assistants_mod.Assistants(sql_store)
                self.addCleanup(svc_live.stop)
                release_support.install(sql_store, live_ai, cls="constructed-fixture")
                unapproved_gov = sql_store.governance_view(sql_actor, assistants_service=svc_live)
                self.assertEqual(
                    unapproved_gov["rai_exercise_acceptance"]["status"],
                    "passed",
                )
                self.assertEqual(
                    unapproved_gov["real_ai_delivery_gate"]["status"],
                    "blocked",
                )
                self.assertIs(
                    unapproved_gov["real_ai_delivery_gate"]["checks"][
                        "oq017_named_live_releases_recorded"
                    ]["passed"],
                    False,
                )

                release_support.install(sql_store, live_ai, cls="actual")
                approved_live_report = sql_store.ai_live_report(
                    sql_actor,
                    assistants_service=svc_live,
                )
                self.assertEqual(
                    approved_live_report["rai_exercise_acceptance"]["status"],
                    "passed",
                )
                self.assertIs(
                    approved_live_report["real_ai_delivery_gate"]["checks"][
                        "oq017_named_live_releases_recorded"
                    ]["passed"],
                    True,
                )
                self.assertEqual(
                    approved_live_report["real_ai_delivery_gate"]["status"],
                    "blocked",
                )
                self.assertEqual(
                    approved_live_report["real_ai_delivery_gate"]["deferred_open_questions"],
                    ["OQ-017", "OQ-018", "OQ-019"],
                )


if __name__ == "__main__":
    unittest.main()
