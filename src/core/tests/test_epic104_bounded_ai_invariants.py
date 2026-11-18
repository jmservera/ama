"""Epic #104 cross-capability bounded-AI invariant enforcement and audit tests (`src/core`).

Covers all 13 registered capabilities across `Store` and `SqlStore`:
1. AI never approves, executes, ranks, or mutates controlled records.
2. No registered AI capability is enabled beyond the exercise without finite
   call, token, and budget limits approved by a named human (and an owned alert).
"""

from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset
import release_support
from zava_forward.core import aftercare as _untyped_aftercare
from zava_forward.core import ai as _untyped_ai
from zava_forward.core import ai_consumption, bounded_ai, rai_release
from zava_forward.core import ai_consumption_demo as _untyped_demo
from zava_forward.core import ai_registry as _untyped_registry
from zava_forward.core import assistants as _untyped_assistants
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

AFTERCARE_MOD: Any = _untyped_aftercare
AI_MOD: Any = _untyped_ai
AI_REGISTRY: Any = _untyped_registry
ASSISTANTS_MOD: Any = _untyped_assistants
DATASET_MOD: Any = dataset
DEMO_MOD: Any = _untyped_demo
RELEASE_SUPPORT: Any = release_support
STORE_CLS: Any = Store
SQL_STORE_CLS: Any = SqlStore
CHAT_ISO_CLS: Any = ChatIsolation

ASSIST_ENV: dict[str, str] = {
    "ZF_ASSIST_AUTHORITY": "Synthetic Programme Sponsor",
    "ZF_ASSIST_CALL_ALLOWANCE": "25",
    "ZF_ASSIST_TOKEN_ALLOWANCE": "500000",
    "ZF_ASSIST_EXPIRES": "2999-01-01T00:00:00Z",
}
CHAT_ENV: dict[str, str] = {
    "CHAT_DPIA_REF": "SYN-DPIA-104",
    "CHAT_LAWFUL_BASIS_REF": "SYN-BASIS-104",
    "CHAT_NOTICE_REF": "SYN-NOTICE-104",
    "ZF_CHAT_DEMO_ACTIVATION": "approved-2026-11-03",
    "ZF_DEPLOYMENT_PROFILE": "demo",
}


def _human_task_entry(task_id: str) -> dict[str, Any]:
    entry: dict[str, Any] = copy.deepcopy(dict(AI_REGISTRY.get(task_id)))
    entry.update(
        enabled=True,
        state="bounded-approved",
        approval_state="approved-2026-11-15",
        accountable_individual="Named Programme Director",
        delegation="Delegation Register DR-104",
        authority={role: f"Named Holder ({role})" for role in rai_release.AUTHORITY_ROLES},
    )
    return entry


class RegistryAndAuditContractTest(unittest.TestCase):
    def test_capability_inventory_matches_all_thirteen_registered_capabilities(self) -> None:
        inventory = bounded_ai.capability_inventory()
        self.assertEqual(frozenset(inventory), bounded_ai.EXPECTED_CAPABILITIES)
        self.assertEqual(len(inventory), 13)
        drifted = {k: v for k, v in inventory.items() if k != "briefing"}
        with (
            patch.object(AI_REGISTRY, "tasks", return_value=drifted),
            self.assertRaises(bounded_ai.BoundedAiViolation),
        ):
            bounded_ai.capability_inventory()

    def test_audit_registered_capabilities_proves_default_propose_only_and_non_exercise_blocked(
        self,
    ) -> None:
        audit = bounded_ai.audit_registered_capabilities({})
        self.assertTrue(audit["ok"], audit["violations"])
        self.assertEqual(audit["count"], 13)
        for cap_id, row in audit["capabilities"].items():
            with self.subTest(capability=cap_id):
                self.assertTrue(row["propose_only"])
                self.assertFalse(row["non_exercise_enabled"])
                self.assertTrue(row["non_exercise_block_reasons"])

        demo_gate = bounded_ai.verify_non_exercise_enablement(
            "chat-case-conversation", env=CHAT_ENV
        )
        self.assertFalse(demo_gate["allowed"])
        self.assertIn("demo-activation-is-exercise-only", demo_gate["reasons"])

    def test_enforce_proposal_only_rejects_approved_controlled_status_forbidden_keys_and_claims(
        self,
    ) -> None:
        for cap_id in sorted(bounded_ai.EXPECTED_CAPABILITIES):
            env = AI_REGISTRY.envelope(
                cap_id,
                case_ids=["ZF-1"],
                source_versions={"ZF-1": "v1"},
                result={"source": "template", "text": "Draft summary for human review."},
            )
            bounded_ai.enforce_proposal_only(cap_id, env)

        bad_payloads: list[dict[str, Any]] = [
            {"approved": True, "approval": "Not reviewed"},
            {"approved": False, "approval": "Accepted"},
            {"approved": False, "approval": "Not reviewed", "status": "Approved"},
            {"approved": False, "approval": "Not reviewed", "stage_transition": "Complete"},
            {"approved": False, "approval": "Not reviewed", "rank_override": 1},
            {"approved": False, "approval": "Not reviewed", "payment_released": True},
            {
                "approved": False,
                "approval": "Not reviewed",
                "text": "The grant has been approved and works executed.",
            },
        ]
        for payload in bad_payloads:
            with self.subTest(payload=payload), self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.enforce_proposal_only("briefing", payload)

    def test_enforce_proposal_only_rejects_nested_forbidden_mutation_keys(self) -> None:
        clean_nested: dict[str, Any] = {
            "approved": False,
            "approval": "Not reviewed",
            "result": {
                "summary": "Draft note for review.",
                "findings": [{"text": "EPC band D recorded.", "citations": ["home.epc"]}],
            },
        }
        bounded_ai.enforce_proposal_only("briefing", clean_nested)

        nested_bad_payloads: list[dict[str, Any]] = [
            {
                "approved": False,
                "approval": "Not reviewed",
                "result": {"rank_override": 1},
            },
            {
                "approved": False,
                "approval": "Not reviewed",
                "output": {"meta": {"approved_by": "Named Officer"}},
            },
            {
                "approved": False,
                "approval": "Not reviewed",
                "findings": [{"text": "Draft item", "mutation": {"stage_transition": "Complete"}}],
            },
            {
                "approved": False,
                "approval": "Not reviewed",
                "steps": ({"consent_granted": True},),
            },
        ]
        for payload in nested_bad_payloads:
            with self.subTest(payload=payload), self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.enforce_proposal_only("briefing", payload)

    def test_partitioned_snapshot_enforces_workspace_slot_boundaries_and_catches_stealth_mutations(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            path.write_text(json.dumps(copy.deepcopy(DATASET_MOD.DATA)), encoding="utf-8")
            store = STORE_CLS(str(path))
            reg = AFTERCARE_MOD.AftercareRegister()
            cid = str(
                reg.raise_concern(
                    route="digital",
                    raised_by="household",
                    home_ref="H-104",
                    kind="discomfort",
                    statement="Evening hallway temperature drops.",
                    owner="Aftercare Lead",
                    next_update="2026-12-01",
                )["id"]
            )
            before = bounded_ai.snapshot_controlled_records(store, aftercare=reg)
            bounded_ai.assert_controlled_records_unchanged(before, copy.deepcopy(before))

            # Legitimate funding_draft workspace update passes only for capability="funding_draft".
            store.cases["ZF-1"]["funding"]["draft"] = "Unapproved draft wording"
            store.cases["ZF-1"]["funding"]["status"] = "Draft ready"
            after_draft = bounded_ai.snapshot_controlled_records(store, aftercare=reg)
            bounded_ai.assert_controlled_records_unchanged(
                before, after_draft, capability="funding_draft"
            )
            with self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.assert_controlled_records_unchanged(
                    before, after_draft, capability="briefing"
                )

            # Illegal funding approval/status promotion fails even for capability="funding_draft".
            store.cases["ZF-1"]["funding"]["status"] = "Approved"
            after_illegal_status = bounded_ai.snapshot_controlled_records(store, aftercare=reg)
            with self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.assert_controlled_records_unchanged(
                    before, after_illegal_status, capability="funding_draft"
                )
            store.cases["ZF-1"]["funding"]["status"] = "Draft ready"
            store.cases["ZF-1"]["funding"]["approved_by"] = "Named Officer"
            after_illegal_approver = bounded_ai.snapshot_controlled_records(store, aftercare=reg)
            with self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.assert_controlled_records_unchanged(
                    before, after_illegal_approver, capability="funding_draft"
                )

            # Controlled aftercare concern mutation fails.
            reg.concerns[cid]["statement"] = "Mutated statement"
            after_concern = bounded_ai.snapshot_controlled_records(store, aftercare=reg)
            with self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.assert_controlled_records_unchanged(after_draft, after_concern)

    def test_authorizes_live_rejects_non_human_accountable_individual_authority_or_no_delegation(
        self,
    ) -> None:
        valid = _human_task_entry("briefing")
        with patch.object(AI_REGISTRY, "get", return_value=valid):
            self.assertTrue(AI_REGISTRY.authorizes_live("briefing", {}))

        invalid_variants = [
            {**valid, "accountable_individual": "AI Assistant"},
            {**valid, "accountable_individual": "system"},
            {**valid, "accountable_individual": "unapproved"},
            {**valid, "delegation": None},
            {
                **valid,
                "authority": {**valid["authority"], "release": "copilot-bot"},
            },
        ]
        for broken in invalid_variants:
            with (
                self.subTest(broken=broken),
                patch.object(AI_REGISTRY, "get", return_value=broken),
            ):
                self.assertFalse(AI_REGISTRY.authorizes_live("briefing", {}))


class AiDispatchGateBypassRegressionTest(unittest.TestCase):
    def _configured_ai(self) -> Any:
        client = AI_MOD.Ai()
        client.endpoint = "https://synthetic-aoai.openai.azure.com"
        client.token = "synthetic-test-token"
        client.expires = 9999999999.0
        client.fast = "gpt-4.1-mini"
        client.strong = "gpt-4.1"
        client.model_version = "gpt-4.1-mini-2025-04-14"
        client.model_version_strong = "gpt-4.1-mini-2025-04-14"
        return client

    def test_ai_run_fails_closed_when_capability_disabled_in_registry(self) -> None:
        calls: list[Any] = []
        client = self._configured_ai()
        client.release = lambda task, dep=None: {
            "id": f"rel:{task}",
            "version": "v1",
            "digest": AI_REGISTRY.digest(AI_REGISTRY.legacy_binding(task, client, dep)),
        }
        disabled_entry = {
            **dict(AI_REGISTRY.get("briefing")),
            "enabled": False,
            "state": "disabled",
        }
        with (
            patch.object(AI_REGISTRY, "get", return_value=disabled_entry),
            patch.object(AI_MOD.urllib.request, "urlopen", side_effect=calls.append),
        ):
            result = client.run("briefing", "sys", "prompt", "Template fallback")
        self.assertEqual(result["source"], "template")
        self.assertEqual(result["text"], "Template fallback")
        self.assertEqual(calls, [])

    def test_ai_look_at_fails_closed_when_read_document_unregistered_or_disabled(self) -> None:
        calls: list[Any] = []
        client = self._configured_ai()
        client.release = lambda task, dep=None: {
            "id": f"rel:{task}",
            "version": "v1",
            "digest": AI_REGISTRY.digest(AI_REGISTRY.legacy_binding(task, client, dep)),
        }
        disabled_doc = {
            **dict(AI_REGISTRY.get("read_document")),
            "enabled": False,
            "state": "disabled",
        }
        for patched in (None, disabled_doc):
            with (
                self.subTest(entry=patched),
                patch.object(AI_REGISTRY, "get", return_value=patched),
                patch.object(AI_MOD.urllib.request, "urlopen", side_effect=calls.append),
            ):
                out = client.look_at(
                    "survey.txt",
                    b"Synthetic EPC band D note",
                    "text/plain",
                    derivative="synthetic_safe",
                )
                self.assertEqual(out["source"], "template")
                self.assertEqual(calls, [])

    def test_ai_run_and_look_at_bind_hyphenated_consumption_capability_ids(self) -> None:
        seen_capabilities: list[str] = []

        class RecordingMeter:
            def reserve(
                self,
                ctx: ai_consumption.CallContext,
                model: str,
                max_in: int,
                max_out: int,
                **kw: Any,
            ) -> str:
                seen_capabilities.append(ctx.capability)
                raise ai_consumption.DispatchHeld("authority-unknown")

            def complete(self, *args: Any, **kwargs: Any) -> None:
                return None

        calls: list[Any] = []
        client = self._configured_ai()
        client.consumption = RecordingMeter()
        client.release = lambda task, dep=None: {
            "id": f"rel:{task}",
            "version": "v1",
            "digest": AI_REGISTRY.digest(AI_REGISTRY.legacy_binding(task, client, dep)),
        }
        with patch.object(AI_MOD.urllib.request, "urlopen", side_effect=calls.append):
            r1 = client.run("funding_draft", "sys", "prompt", "Template funding draft")
            r2 = client.look_at(
                "survey.txt",
                b"Synthetic survey note",
                "text/plain",
                derivative="synthetic_safe",
            )
        self.assertEqual((r1["source"], r2["source"]), ("template", "template"))
        self.assertEqual(seen_capabilities, ["funding-draft", "read-document"])
        self.assertEqual(calls, [])


class NonExerciseConsumptionAndReleaseBoundsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.port = DEMO_MOD.DemoPort(Path(self.tmp.name) / "ledger.sqlite")
        self.ledger = ai_consumption.Consumption(self.port)
        self.config = ai_consumption.reference("cfg-104")

    def _price(
        self, *, synthetic: bool = False, ledger: ai_consumption.Consumption | None = None
    ) -> str:
        target = self.ledger if ledger is None else ledger
        return str(
            target.price(
                source="https://prices.azure.com/api/retail/prices",
                source_hash=ai_consumption.reference("price-hash"),
                retrieved=DEMO_MOD.START,
                version="v1",
                model=DEMO_MOD.MODEL,
                currency="USD",
                start=DEMO_MOD.START,
                end=DEMO_MOD.END,
                input_rate="1",
                output_rate="2",
                cached_rate="0.5",
                synthetic=synthetic,
            )
        )

    def _authorize(self, capability: str, price_id: str, **over: Any) -> str:
        fields: dict[str, Any] = {
            "authority": f"auth-{capability}",
            "owner": "Named Budget Holder",
            "evidence": "FIN-APPROVAL-104",
            "price": price_id,
            "capability": capability,
            "configuration": self.config,
            "start": DEMO_MOD.START,
            "end": DEMO_MOD.END,
            "max_calls": 5,
            "max_depth": 1,
            "budgets": [
                {
                    "id": ai_consumption.reference(f"period-{capability}"),
                    "calls": 5,
                    "tokens": 10000,
                    "amount": "2.50",
                }
            ],
            "alert": "alert-rule-ai-limits",
            "alert_owner": "Named Budget Holder",
        }
        fields.update(over)
        return str(self.ledger.authorize(**fields))

    def test_consumption_authorize_rejects_blank_and_non_human_owners_preserving_synthetic_omission(
        self,
    ) -> None:
        real_pid = self._price(synthetic=False)
        for bad_owner in ("", "   ", "AI", "system", "copilot-bot", "unapproved", "unknown"):
            with self.subTest(owner=bad_owner), self.assertRaises(ValueError):
                self._authorize("briefing", real_pid, owner=bad_owner)
            with self.subTest(alert_owner=bad_owner), self.assertRaises(ValueError):
                self._authorize("briefing", real_pid, alert_owner=bad_owner)
        for blank_key in ("authority", "evidence"):
            with self.subTest(blank=blank_key), self.assertRaises(ValueError):
                self._authorize("briefing", real_pid, **{blank_key: "   "})

        # Synthetic exercise authority with alert=None still succeeds and omits "alert".
        syn_pid = self._price(synthetic=True)
        aid = self._authorize(
            "stock-prioritisation",
            syn_pid,
            authority="syn-auth-1",
            owner="exercise-fixture",
            alert=None,
            alert_owner=None,
        )
        self.assertTrue(aid)
        # Supplying non-human alert_owner even on synthetic price fails closed.
        with self.assertRaises(ValueError):
            self._authorize(
                "stock-prioritisation",
                syn_pid,
                authority="syn-auth-2",
                owner="exercise-fixture",
                alert="alert-rule-ai-limits",
                alert_owner="AI-bot",
            )

    def test_consumption_price_swap_to_non_synthetic_rejects_unbounded_existing_authority(
        self,
    ) -> None:
        scratch = ai_consumption.Consumption(
            DEMO_MOD.DemoPort(Path(self.tmp.name) / "scratch.sqlite")
        )
        future_real_pid = self._price(synthetic=False, ledger=scratch)
        self._authorize(
            "briefing",
            future_real_pid,
            authority="pre-registered-without-alert",
            owner="Named Budget Holder",
            alert=None,
            alert_owner=None,
        )
        with self.assertRaises(ValueError):
            self._price(synthetic=False)

    def test_consumption_non_exercise_status_reports_unexpired_human_owned_budget_only(
        self,
    ) -> None:
        missing = self.ledger.non_exercise_status("briefing", configuration=self.config)
        self.assertFalse(missing["allowed"])
        self.assertIn("authority-unknown", missing["reasons"])

        syn_pid = self._price(synthetic=True)
        self._authorize(
            "briefing",
            syn_pid,
            authority="syn-only",
            owner="Named Budget Holder",
            alert=None,
            alert_owner=None,
        )
        syn_status = self.ledger.non_exercise_status("briefing", configuration=self.config)
        self.assertFalse(syn_status["allowed"])
        self.assertIn("non-synthetic-price-missing", syn_status["reasons"])

        real_pid = self._price(synthetic=False)
        self._authorize("funding-draft", real_pid, configuration=self.config)
        ok_status = self.ledger.non_exercise_status(
            "funding-draft", configuration=self.config, model=DEMO_MOD.MODEL
        )
        self.assertTrue(ok_status["allowed"], ok_status["reasons"])
        self.assertEqual(ok_status["reasons"], [])

        expired = self.ledger.non_exercise_status(
            "funding-draft",
            configuration=self.config,
            model=DEMO_MOD.MODEL,
            now=float(ai_consumption.timestamp(DEMO_MOD.END)),
        )
        self.assertFalse(expired["allowed"])

    def test_verify_non_exercise_enablement_requires_every_finite_human_approved_control(
        self,
    ) -> None:
        real_pid = self._price(synthetic=False)
        now = float(ai_consumption.timestamp(DEMO_MOD.START)) + 60.0
        end_ts = float(ai_consumption.timestamp(DEMO_MOD.END))
        binding = {
            "deployment": "gpt-4.1-mini",
            "model_version": DEMO_MOD.MODEL,
            "prompt_version": "2026-10-09.1",
            "policy_version": "v1",
        }

        for cap_id in sorted(bounded_ai.EXPECTED_CAPABILITIES):
            consumption_cap = str(AI_REGISTRY.consumption_capability(cap_id))
            self._authorize(consumption_cap, real_pid, authority=f"live-{consumption_cap}")
            entry = _human_task_entry(cap_id)
            rec = RELEASE_SUPPORT.fixture(
                cap_id,
                binding,
                model=DEMO_MOD.MODEL,
                cls="actual",
                expires=end_ts,
                accountable_owner="Named Programme Director",
            )
            allowed = bounded_ai.verify_non_exercise_enablement(
                cap_id,
                env={},
                task_entry=entry,
                release_record=rec,
                binding=binding,
                bound_keys=tuple(binding.keys()),
                now=now,
                ledger=self.ledger,
                configuration=self.config,
                model=DEMO_MOD.MODEL,
            )
            with self.subTest(capability=cap_id):
                self.assertTrue(allowed["allowed"], allowed["reasons"])

            # Removing finite consumption or using synthetic evidence_class immediately blocks.
            synthetic_rec = {
                **rec,
                "evidence_class": "constructed-fixture",
                "actual_authorisation": False,
            }
            blocked_syn = bounded_ai.verify_non_exercise_enablement(
                cap_id,
                env={},
                task_entry=entry,
                release_record=synthetic_rec,
                binding=binding,
                bound_keys=tuple(binding.keys()),
                now=now,
                ledger=self.ledger,
                configuration=self.config,
                model=DEMO_MOD.MODEL,
            )
            self.assertFalse(blocked_syn["allowed"])


class _CrossCapabilityStoreMixin:
    tmp: tempfile.TemporaryDirectory[str]
    store: Any

    def make_store(self, data: dict[str, Any], tmp_dir: str) -> Any:
        raise NotImplementedError

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        seed: dict[str, Any] = copy.deepcopy(DATASET_MOD.DATA)
        self.store = self.make_store(seed, self.tmp.name)
        RELEASE_SUPPORT.install(self.store)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _staff_for_roles(self, roles: tuple[str, ...] | list[str]) -> dict[str, Any]:
        for member in self.store.data["staff"]:
            if member.get("role") in roles:
                return dict(member)
        raise AssertionError(f"No staff fixture found for roles={roles!r}")

    def test_retained_capabilities_never_approve_execute_rank_or_mutate_controlled_records(
        self,
    ) -> None:
        test_self: Any = self
        manager = self._staff_for_roles(["Retrofit Programme Manager"])
        grants_officer = self._staff_for_roles(
            ["Grants and Evidence Officer", "Retrofit Programme Manager"]
        )
        case_id = "ZF-1"
        uploaded = self.store.add_document(
            manager,
            case_id,
            "epc-104.txt",
            "EPC",
            b"Synthetic EPC band D note for read-only verification.",
            metadata={
                "source": "SYN-DOC-104",
                "source_version": "v1",
                "reason": "Synthetic document fixture",
                "ai_derivative": "synthetic_safe",
            },
        )
        doc_id = str(uploaded["id"])

        operations: list[tuple[str, Any]] = [
            ("briefing", lambda: self.store.briefing(manager)),
            ("message", lambda: self.store.ai_run(manager, case_id, "message")),
            ("summary", lambda: self.store.ai_run(manager, case_id, "summary")),
            ("priority", lambda: self.store.ai_priority(manager, 3)),
            ("funding_draft", lambda: self.store.funding_draft(grants_officer, case_id)),
            ("read_document", lambda: self.store.read_document(manager, case_id, doc_id)),
        ]
        for cap_id, action in operations:
            with test_self.subTest(capability=cap_id):
                before = bounded_ai.snapshot_controlled_records(self.store)
                result = action()
                after = bounded_ai.snapshot_controlled_records(self.store)
                bounded_ai.assert_controlled_records_unchanged(before, after, capability=cap_id)
                envelope = result.get("envelope")
                if isinstance(envelope, dict):
                    bounded_ai.enforce_proposal_only(cap_id, envelope)
                test_self.assertFalse(self.store.cases[case_id].get("funding_ok"))
                test_self.assertIsNone(self.store.cases[case_id]["funding"].get("approved_by"))

    def test_assistants_chat_and_aftercare_never_approve_execute_rank_or_mutate_controlled_records(
        self,
    ) -> None:
        test_self: Any = self
        reg = AFTERCARE_MOD.AftercareRegister()
        concern_id = str(
            reg.raise_concern(
                route="digital",
                raised_by="household",
                home_ref="H-ZF-1",
                kind="discomfort",
                statement="Bedroom stays cool overnight.",
                owner="Aftercare Lead",
                next_update="2026-12-01",
            )["id"]
        )
        manager = self._staff_for_roles(["Retrofit Programme Manager"])
        before = bounded_ai.snapshot_controlled_records(self.store, aftercare=reg)

        # 1. aftercare-concern-pack
        pack = reg.propose_pack(concern_id, "Household reports cool bedroom overnight.")
        bounded_ai.enforce_proposal_only("aftercare-concern-pack", pack)

        # 2. chat-case-conversation (both action refusal and grounded question)
        panel = ChatPanel(
            CHAT_ISO_CLS(self.store, env=CHAT_ENV),
            lambda _s, _p: json.dumps(
                {"answer": "Recorded stage is shown on the case card.", "citations": ["ZF-1/stage"]}
            ),
        )
        tid = self.store.chat_create_thread(manager, case_id="ZF-1")["id"]
        refused = panel.ask(manager, tid, "Approve the grant and advance the stage now.")
        test_self.assertEqual(refused["kind"], "refused")
        answered = panel.ask(manager, tid, "What stage is this case in?")
        test_self.assertIn(answered["kind"], ("answer", "rules", "fallback"))

        # 3. 5 proposal-only assistants (SQL queue on SqlStore; fail-closed on Store)
        def assistant_provider(*_args: Any) -> dict[str, Any]:
            return {
                "text": json.dumps(
                    {
                        "summary": "Grounded proposal for staff review.",
                        "findings": [{"text": "EPC band recorded.", "citations": ["home.epc"]}],
                        "unknowns": [],
                    }
                ),
                "model": "test-model",
                "outcome": "returned",
                "source": "local-test-double",
                "usage": {
                    "prompt_tokens": 20,
                    "completion_tokens": 10,
                    "total_tokens": 30,
                    "cached_tokens": 0,
                },
            }

        if hasattr(self.store, "assistant_connection"):
            self.store.ai.endpoint = "https://synthetic-aoai.openai.azure.com"
        service = ASSISTANTS_MOD.Assistants(self.store, env=ASSIST_ENV, provider=assistant_provider)
        try:
            if hasattr(self.store, "assistant_connection"):
                RELEASE_SUPPORT.install(self.store)
            for cap_id in sorted(bounded_ai.ASSISTANT_CAPABILITIES):
                role_user = self._staff_for_roles(ASSISTANTS_MOD.REGISTRY[cap_id]["roles"])
                if hasattr(self.store, "assistant_connection"):
                    created = service.invoke(role_user, cap_id, "ZF-1")
                    service.execute(created["id"])
                    detail = service.detail(role_user, created["id"])
                    test_self.assertNotEqual(detail["state"], "accepted")
                    test_self.assertFalse(detail["relied_on"])
                    test_self.assertIsNone(detail["review"])
                    bounded_ai.enforce_proposal_only(cap_id, dict(detail.get("envelope") or {}))
                    bounded_ai.enforce_proposal_only(cap_id, dict(detail.get("output") or {}))
                else:
                    with test_self.assertRaises(ValueError):
                        service.invoke(role_user, cap_id, "ZF-1")
        finally:
            service.stop()

        after = bounded_ai.snapshot_controlled_records(self.store, aftercare=reg)
        bounded_ai.assert_controlled_records_unchanged(before, after)


class JsonCrossCapabilityImmutabilityTest(_CrossCapabilityStoreMixin, unittest.TestCase):
    def make_store(self, data: dict[str, Any], tmp_dir: str) -> Any:
        path = Path(tmp_dir) / "zavaforward.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return STORE_CLS(str(path))


class SqlCrossCapabilityImmutabilityTest(_CrossCapabilityStoreMixin, unittest.TestCase):
    def make_store(self, data: dict[str, Any], tmp_dir: str) -> Any:
        path = Path(tmp_dir) / "zavaforward.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return SQL_STORE_CLS(str(path), os.path.join(tmp_dir, "epic104.sqlite"))


if __name__ == "__main__":
    unittest.main()
