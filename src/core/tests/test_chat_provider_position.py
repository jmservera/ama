"""Deterministic unit tests for the #163 model provider data-handling and region contract."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

import dataset
from zava_forward.core import regulatory_privacy
from zava_forward.core.chat_privacy import MODEL_PROVIDER_POSITION, ChatNotApproved, ChatPrivacy
from zava_forward.core.chat_provider_position import (
    APPROVED_DEPLOYMENT_TYPES,
    DPO_LEGAL_APPROVED,
    EU_DATA_ZONE_REGIONS,
    MODEL_PROVIDER_CONTRACT,
    PRIMARY_REGION,
    ProviderPositionError,
    evaluate_provider_position,
    is_demo_or_synthetic_ref,
    is_valid_governance_ref,
    require_provider_position,
)
from zava_forward.core.store import Store

STAFF_USER: dict[str, Any] = dict(dataset.DATA["staff"][0])
TASK = "stock-prioritisation"
SYNTH_CHAT_REFS: dict[str, str] = {
    "CHAT_DPIA_REF": "SYNTH-DPIA-1",
    "CHAT_LAWFUL_BASIS_REF": "SYNTH-LB-1",
    "CHAT_NOTICE_REF": "SYNTH-NOTICE-1",
}
REAL_REG_REFS: dict[str, str] = {
    name: f"GOV-REF-{idx}" for idx, (name, _) in enumerate(regulatory_privacy.GATE_REFS, start=1)
}


class ChatProviderPositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data_file = Path(self.tmp.name) / "zavaforward.json"
        data_file.write_text(json.dumps(dataset.DATA), encoding="utf-8")
        self.store = cast(Callable[[str], Any], Store)(str(data_file))

    def test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted(self) -> None:
        pos = evaluate_provider_position({})
        self.assertTrue(pos["valid"])
        self.assertEqual(pos["region"], PRIMARY_REGION)
        self.assertEqual(pos["residency_zone"], "uk_south")
        self.assertEqual(pos["deployment_type"], "Standard")
        self.assertFalse(pos["deployment_attested"])
        self.assertTrue(
            evaluate_provider_position(
                {"CHAT_PROVIDER_REGION": "uksouth", "CHAT_DEPLOYMENT_TYPE": "Standard"}
            )["deployment_attested"]
        )
        self.assertFalse(MODEL_PROVIDER_CONTRACT["deployment_attested"])
        self.assertFalse(MODEL_PROVIDER_POSITION["deployment_attested"])
        self.assertTrue(pos["zero_model_training"])
        self.assertFalse(pos["customer_data_training"])
        self.assertFalse(pos["zava_stores_prompts"])
        self.assertFalse(pos["foundry_agent_memory"])
        self.assertFalse(pos["cross_border_transfer"])
        self.assertFalse(pos["transfer_signoff_required"])
        self.assertFalse(DPO_LEGAL_APPROVED)
        self.assertFalse(pos["dpo_legal_approved"])
        self.assertFalse(pos["documented_terms"]["dpo_accepted"])
        self.assertEqual(
            pos["documented_terms"]["status"],
            "vendor_documentation_not_dpo_accepted",
        )
        self.assertEqual(pos["violations"], [])
        self.assertEqual(MODEL_PROVIDER_POSITION["primary_region"], "uksouth")
        self.assertEqual(
            MODEL_PROVIDER_POSITION["approved_deployment_types"], APPROVED_DEPLOYMENT_TYPES
        )

    def test_uksouth_rejects_datazone_standard_because_uk_outside_eu_data_zone(self) -> None:
        pos = evaluate_provider_position(
            {"CHAT_PROVIDER_REGION": "uksouth", "CHAT_DEPLOYMENT_TYPE": "DataZoneStandard"}
        )
        self.assertFalse(pos["valid"])
        self.assertFalse(pos["deployment_attested"])
        self.assertEqual(pos["residency_zone"], "uk_south")
        self.assertIn("unapproved_deployment_residency", pos["violations"])
        with self.assertRaises(ProviderPositionError) as ctx:
            require_provider_position(
                {"CHAT_PROVIDER_REGION": "uksouth", "CHAT_DEPLOYMENT_TYPE": "DataZoneStandard"}
            )
        self.assertIn("unapproved_deployment_residency", ctx.exception.violations)

    def test_eu_data_zone_regions_require_recorded_transfer_signoff(self) -> None:
        for eu_region in EU_DATA_ZONE_REGIONS:
            with self.subTest(region=eu_region):
                blocked = evaluate_provider_position(
                    {"CHAT_PROVIDER_REGION": eu_region, "CHAT_DEPLOYMENT_TYPE": "DataZoneStandard"}
                )
                self.assertFalse(blocked["valid"])
                self.assertEqual(blocked["residency_zone"], "eu_data_zone")
                self.assertTrue(blocked["cross_border_transfer"])
                self.assertEqual(blocked["violations"], ["cross_border_transfer_unapproved"])

                allowed = require_provider_position(
                    {
                        "CHAT_PROVIDER_REGION": eu_region,
                        "CHAT_DEPLOYMENT_TYPE": "DataZoneStandard",
                        "CHAT_TRANSFER_REF": "SYNTH-TRA-EU-1",
                    }
                )
                self.assertTrue(allowed["valid"])
                self.assertEqual(allowed["region"], eu_region)
                self.assertEqual(allowed["deployment_type"], "DataZoneStandard")
                self.assertTrue(allowed["transfer_ref_recorded"])
                self.assertFalse(allowed["dpo_legal_approved"])

    def test_unapproved_regions_and_blank_region_fail_closed_without_echoing_value(self) -> None:
        for bad_region in (
            "eastus",
            "westus2",
            "australiaeast",
            "global",
            "PRIVATE-REGION-CANARY",
            "",
            "   ",
        ):
            with self.subTest(region=bad_region):
                pos = evaluate_provider_position({"CHAT_PROVIDER_REGION": bad_region})
                self.assertFalse(pos["valid"])
                self.assertEqual(pos["region"], "unapproved")
                self.assertEqual(pos["residency_zone"], "unapproved")
                self.assertIn("unapproved_region", pos["violations"])
        canary_pos = evaluate_provider_position({"CHAT_PROVIDER_REGION": "PRIVATE-REGION-CANARY"})
        self.assertNotIn("PRIVATE-REGION-CANARY", json.dumps(canary_pos).upper())

    def test_global_and_unapproved_deployment_types_fail_closed_without_echoing_value(self) -> None:
        for bad_sku in (
            "GlobalStandard",
            "GlobalBatch",
            "GlobalProvisionedManaged",
            "ProvisionedManaged",
            "PRIVATE-SKU-CANARY",
            "",
        ):
            with self.subTest(sku=bad_sku):
                pos = evaluate_provider_position({"CHAT_DEPLOYMENT_TYPE": bad_sku})
                self.assertFalse(pos["valid"])
                self.assertEqual(pos["deployment_type"], "unapproved")
                self.assertIn("unapproved_deployment_residency", pos["violations"])
        canary_pos = evaluate_provider_position({"CHAT_DEPLOYMENT_TYPE": "PRIVATE-SKU-CANARY"})
        self.assertNotIn("PRIVATE-SKU-CANARY", json.dumps(canary_pos).upper())

    def test_provider_training_flags_fail_closed(self) -> None:
        for bad_flag in ("true", "1", "yes", "on", "enabled", "opt-in", "custom"):
            with self.subTest(flag=bad_flag):
                pos = evaluate_provider_position({"CHAT_PROVIDER_TRAINING": bad_flag})
                self.assertFalse(pos["valid"])
                self.assertFalse(pos["zero_model_training"])
                self.assertTrue(pos["customer_data_training"])
                self.assertEqual(pos["violations"], ["provider_training_prohibited"])
        kw_pos = evaluate_provider_position({}, customer_data_training=True)
        self.assertFalse(kw_pos["valid"])
        self.assertIn("provider_training_prohibited", kw_pos["violations"])

    def test_content_filtering_and_abuse_monitoring_disclosures_are_distinct(self) -> None:
        pos = evaluate_provider_position({})
        cf = pos["content_filtering"]
        am = pos["abuse_monitoring"]
        self.assertEqual(cf["service"], "Azure AI Content Safety")
        self.assertEqual(cf["mode"], "synchronous_stateless_harm_filtering")
        self.assertFalse(cf["stores_prompts"])
        self.assertFalse(cf["trains_models"])
        self.assertEqual(am["mode"], "platform_default_unverified")
        self.assertFalse(am["modified_abuse_monitoring_recorded"])
        self.assertFalse(am["modified_abuse_monitoring_verified"])
        self.assertEqual(am["default_sample_retention_days"], 30)
        self.assertTrue(am["human_review_possible"])
        self.assertTrue(am["eea_reviewer_residency_documented"])
        self.assertFalse(am["uk_reviewer_residency_verified"])

    def test_modified_abuse_monitoring_reference_validation_and_actual_mode_rejection(self) -> None:
        modified = evaluate_provider_position(
            {"CHAT_ABUSE_MONITORING_MODIFIED_REF": "SYNTH-MSFT-MOD-ABUSE-1"}
        )
        self.assertTrue(modified["valid"])
        self.assertEqual(modified["abuse_monitoring"]["mode"], "modified_recorded_unverified")
        self.assertTrue(modified["abuse_monitoring"]["modified_abuse_monitoring_recorded"])
        self.assertFalse(modified["abuse_monitoring"]["modified_abuse_monitoring_verified"])
        self.assertEqual(modified["abuse_monitoring"]["default_sample_retention_days"], 30)
        self.assertTrue(modified["abuse_monitoring"]["human_review_possible"])
        self.assertNotIn("SYNTH-MSFT-MOD-ABUSE-1", json.dumps(modified))

        placeholder = evaluate_provider_position({"CHAT_ABUSE_MONITORING_MODIFIED_REF": "yes"})
        self.assertFalse(placeholder["valid"])
        self.assertIn("invalid_abuse_monitoring_ref", placeholder["violations"])

        actual_synth = evaluate_provider_position(
            {
                "ZF_DATA_PROCESSING": "actual",
                "CHAT_ABUSE_MONITORING_MODIFIED_REF": "SYNTH-MSFT-MOD-ABUSE-1",
            }
        )
        self.assertFalse(actual_synth["valid"])
        self.assertIn(
            "synthetic_or_demo_abuse_monitoring_ref_in_actual_mode",
            actual_synth["violations"],
        )

    def test_placeholder_governance_references_rejected_across_controls(self) -> None:
        for tok in ("yes", "true", "1", "approved", "ok", "none", "tbd", ""):
            self.assertFalse(is_valid_governance_ref(tok, actual=False), tok)
        privacy = ChatPrivacy(
            self.store,
            env={
                "CHAT_DPIA_REF": "yes",
                "CHAT_LAWFUL_BASIS_REF": "approved",
                "CHAT_NOTICE_REF": "true",
            },
        )
        decision = privacy.decision()
        self.assertFalse(decision["approved"])
        self.assertEqual(decision["missing"], ["dpia_ref", "lawful_basis_ref", "notice_ref"])

    def test_actual_data_mode_rejects_synthetic_and_demo_references(self) -> None:
        for sample in (
            "SYNTH-DPIA-1",
            "SYN-DPIA",
            "SYNTHETIC-CHAT-TEST",
            "docs/reference/research/chat-demo-storage-approval-2026-11-01.md#dpia",
            "docs/reference/research/chat-memory-dpia.md",
        ):
            self.assertTrue(is_demo_or_synthetic_ref(sample), sample)
            self.assertTrue(is_valid_governance_ref(sample, actual=False), sample)
            self.assertFalse(is_valid_governance_ref(sample, actual=True), sample)

        privacy = ChatPrivacy(
            self.store,
            env={
                **SYNTH_CHAT_REFS,
                "ZF_DATA_PROCESSING": "actual",
                "CHAT_RETENTION_REF": "SYNTH-RET-30",
                "CHAT_RETENTION_DAYS": "30",
            },
        )
        decision = privacy.decision()
        self.assertFalse(decision["approved"])
        self.assertEqual(
            decision["synthetic_refs_in_actual_mode"],
            ["dpia_ref", "lawful_basis_ref", "notice_ref"],
        )
        self.assertIsNone(decision["retention_days"])
        with self.assertRaises(ChatNotApproved):
            privacy.start_thread(STAFF_USER, "ZF-1", TASK)

        non_synthetic_actual = ChatPrivacy(
            self.store,
            env={
                "ZF_DATA_PROCESSING": "actual",
                "CHAT_DPIA_REF": "DPIA-2026-99",
                "CHAT_LAWFUL_BASIS_REF": "LB-2026-99",
                "CHAT_NOTICE_REF": "NOTICE-2026-99",
                "CHAT_RETENTION_REF": "RET-2026-99",
                "CHAT_RETENTION_DAYS": "30",
            },
        )
        non_synthetic_decision = non_synthetic_actual.decision()
        self.assertFalse(non_synthetic_decision["approved"])
        self.assertEqual(non_synthetic_decision["synthetic_refs_in_actual_mode"], [])
        self.assertTrue(non_synthetic_decision["actual_mode_unapproved"])
        self.assertFalse(non_synthetic_decision["dpo_legal_approved"])
        self.assertIsNone(non_synthetic_decision["retention_days"])
        with self.assertRaises(ChatNotApproved) as exc_ctx:
            non_synthetic_actual.start_thread(STAFF_USER, "ZF-1", TASK)
        self.assertIn("DPO and Legal", str(exc_ctx.exception))
        with self.assertRaises(ChatNotApproved):
            non_synthetic_actual.opt_in(STAFF_USER, True)

        unattested_actual = evaluate_provider_position({"ZF_DATA_PROCESSING": "actual"})
        self.assertFalse(unattested_actual["valid"])
        self.assertFalse(unattested_actual["deployment_attested"])
        self.assertEqual(
            unattested_actual["violations"],
            [
                "unattested_region_in_actual_mode",
                "unattested_deployment_in_actual_mode",
                "actual_mode_dpo_legal_unapproved",
            ],
        )

        attested_actual = evaluate_provider_position(
            {
                "ZF_DATA_PROCESSING": "actual",
                "CHAT_PROVIDER_REGION": "uksouth",
                "CHAT_DEPLOYMENT_TYPE": "Standard",
            }
        )
        self.assertFalse(attested_actual["valid"])
        self.assertTrue(attested_actual["deployment_attested"])
        self.assertEqual(attested_actual["violations"], ["actual_mode_dpo_legal_unapproved"])

        for actual_provider_env in (
            {"ZF_DATA_PROCESSING": "actual"},
            {
                "ZF_DATA_PROCESSING": "actual",
                "CHAT_PROVIDER_REGION": "westeurope",
                "CHAT_DEPLOYMENT_TYPE": "DataZoneStandard",
                "CHAT_TRANSFER_REF": "TRA-2026-99",
            },
        ):
            evaluated_actual = evaluate_provider_position(actual_provider_env)
            self.assertFalse(evaluated_actual["valid"])
            self.assertFalse(evaluated_actual["transfer_ref_recorded"])
            self.assertIn(
                "actual_mode_dpo_legal_unapproved",
                evaluated_actual["violations"],
            )
            with self.assertRaises(ProviderPositionError):
                require_provider_position(actual_provider_env)

    def test_retention_stays_inactive_before_approval_or_when_provider_invalid(self) -> None:
        unapproved = ChatPrivacy(
            self.store,
            env={"CHAT_RETENTION_REF": "SYNTH-RET-1", "CHAT_RETENTION_DAYS": "30"},
        )
        self.assertFalse(unapproved.decision()["approved"])
        self.assertIsNone(unapproved.decision()["retention_days"])
        self.assertEqual(
            unapproved.purge_retention("9999-01-01T00:00:00+00:00"),
            {"threads": 0, "messages": 0, "memory": 0, "applied": False},
        )

        bad_provider = ChatPrivacy(
            self.store,
            env={
                **SYNTH_CHAT_REFS,
                "CHAT_RETENTION_REF": "SYNTH-RET-1",
                "CHAT_RETENTION_DAYS": "30",
                "CHAT_DEPLOYMENT_TYPE": "GlobalStandard",
            },
        )
        self.assertFalse(bad_provider.decision()["approved"])
        self.assertIsNone(bad_provider.decision()["retention_days"])

        for invalid_days in ("\u00b2", "\u0663\u0660", "0", "-5", "36501", "thirty", "9" * 5000):
            with self.subTest(days=invalid_days):
                bad_days = ChatPrivacy(
                    self.store,
                    env={
                        **SYNTH_CHAT_REFS,
                        "CHAT_RETENTION_REF": "SYNTH-RET-1",
                        "CHAT_RETENTION_DAYS": invalid_days,
                    },
                )
                self.assertTrue(bad_days.decision()["approved"])
                self.assertIsNone(bad_days.decision()["retention_days"])
                self.assertEqual(
                    bad_days.purge_retention("9999-01-01T00:00:00+00:00")["applied"],
                    False,
                )

    def test_chat_privacy_entrypoints_fail_closed_on_provider_violations(self) -> None:
        valid_privacy = ChatPrivacy(self.store, env=SYNTH_CHAT_REFS)
        thread_id = valid_privacy.start_thread(STAFF_USER, "ZF-1", TASK)

        for bad_env in (
            {**SYNTH_CHAT_REFS, "CHAT_PROVIDER_REGION": "eastus"},
            {**SYNTH_CHAT_REFS, "CHAT_DEPLOYMENT_TYPE": "GlobalStandard"},
            {**SYNTH_CHAT_REFS, "CHAT_PROVIDER_TRAINING": "true"},
            {**SYNTH_CHAT_REFS, "CHAT_CROSS_BORDER_TRANSFER": "true"},
            {**SYNTH_CHAT_REFS, "CHAT_CROSS_BORDER_TRANSFER": "maybe"},
        ):
            blocked = ChatPrivacy(self.store, env=bad_env)
            with self.assertRaises(ChatNotApproved):
                blocked.start_thread(STAFF_USER, "ZF-1", TASK)
            with self.assertRaises(ChatNotApproved):
                blocked.add_message(STAFF_USER, thread_id, "user", "hello")
            with self.assertRaises(ChatNotApproved):
                blocked.opt_in(STAFF_USER, True)
            with self.assertRaises(ChatNotApproved):
                blocked.add_memory(STAFF_USER, "prefers concise notes", task=TASK)

    def test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo(
        self,
    ) -> None:
        env_ok = {**REAL_REG_REFS, "OTHER": "PRIVATE-CANARY"}
        ok_report = regulatory_privacy.readiness_report(env_ok)
        self.assertTrue(ok_report["live_data_permitted"])
        self.assertFalse(ok_report["dpo_reviewed"])
        self.assertEqual(len(ok_report["criteria"]), 8)
        self.assertTrue(ok_report["provider_position"]["valid"])
        dumped_ok = json.dumps(ok_report)
        self.assertNotIn("PRIVATE-CANARY", dumped_ok)
        self.assertNotIn("GOV-REF-1", dumped_ok)

        env_bad = {
            **REAL_REG_REFS,
            "CHAT_PROVIDER_REGION": "PRIVATE-REGION-CANARY",
            "CHAT_TRANSFER_REF": "PRIVATE-TRANSFER-CANARY",
        }
        bad_report = regulatory_privacy.readiness_report(env_bad)
        self.assertFalse(bad_report["live_data_permitted"])
        self.assertFalse(bad_report["provider_position"]["valid"])
        dumped_bad = json.dumps(bad_report)
        self.assertNotIn("PRIVATE-REGION-CANARY", dumped_bad)
        self.assertNotIn("PRIVATE-TRANSFER-CANARY", dumped_bad)

        query_blocked = regulatory_privacy.build_foundry_query(
            "rule_lookup",
            {"card_id": "RC-1", "source_id": "SRC-1"},
            question="What rule applies?",
            env={"CHAT_PROVIDER_TRAINING": "true"},
        )
        self.assertFalse(query_blocked["permitted"])
        self.assertEqual(query_blocked["fields"], {})
        self.assertEqual(query_blocked["provider_violations"], ["provider_training_prohibited"])

        with patch.dict(
            os.environ,
            {**REAL_REG_REFS, "CHAT_PROVIDER_REGION": "eastus"},
            clear=False,
        ):
            ambient_report = regulatory_privacy.readiness_report()
            self.assertFalse(ambient_report["live_data_permitted"])
            self.assertIn(
                "unapproved_region",
                ambient_report["provider_position"]["violations"],
            )
            ambient_query = regulatory_privacy.build_foundry_query(
                "rule_lookup",
                {"card_id": "RC-1", "source_id": "SRC-1"},
                question="What rule applies?",
            )
            self.assertFalse(ambient_query["permitted"])
            self.assertIn("unapproved_region", ambient_query["provider_violations"])

        malformed_report = regulatory_privacy.readiness_report("PRIVATE-MALFORMED-ENV-CANARY")
        self.assertFalse(malformed_report["live_data_permitted"])
        self.assertFalse(malformed_report["provider_position"]["valid"])
        self.assertIn(
            "unapproved_region",
            malformed_report["provider_position"]["violations"],
        )
        self.assertNotIn("PRIVATE-MALFORMED-ENV-CANARY", json.dumps(malformed_report))

        malformed_query = regulatory_privacy.build_foundry_query(
            "rule_lookup",
            {"card_id": "RC-1", "source_id": "SRC-1"},
            question="What rule applies?",
            env="PRIVATE-MALFORMED-ENV-CANARY",
        )
        self.assertFalse(malformed_query["permitted"])
        self.assertIn("unapproved_region", malformed_query["provider_violations"])
        self.assertNotIn("PRIVATE-MALFORMED-ENV-CANARY", json.dumps(malformed_query))

        actual_eu_env = {
            **REAL_REG_REFS,
            "ZF_DATA_PROCESSING": "actual",
            "CHAT_PROVIDER_REGION": "westeurope",
            "CHAT_TRANSFER_REF": "TRA-2026-99",
        }
        actual_eu_report = regulatory_privacy.readiness_report(actual_eu_env)
        self.assertFalse(actual_eu_report["live_data_permitted"])
        self.assertFalse(actual_eu_report["provider_position"]["valid"])
        self.assertFalse(actual_eu_report["provider_position"]["deployment_attested"])
        self.assertIn(
            "unattested_deployment_in_actual_mode",
            actual_eu_report["provider_position"]["violations"],
        )
        self.assertIn(
            "actual_mode_dpo_legal_unapproved",
            actual_eu_report["provider_position"]["violations"],
        )
        actual_eu_query = regulatory_privacy.build_foundry_query(
            "rule_lookup",
            {"card_id": "RC-1", "source_id": "SRC-1"},
            question="What rule applies?",
            env=actual_eu_env,
        )
        self.assertFalse(actual_eu_query["permitted"])
        self.assertEqual(actual_eu_query["fields"], {})
        self.assertIn(
            "unattested_deployment_in_actual_mode",
            actual_eu_query["provider_violations"],
        )
        self.assertIn(
            "actual_mode_dpo_legal_unapproved",
            actual_eu_query["provider_violations"],
        )


if __name__ == "__main__":
    unittest.main()
