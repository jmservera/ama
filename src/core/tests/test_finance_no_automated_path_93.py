"""Issue #93 end-to-end invariant suite: RULE-010 / AC-035.

Proves that no automated, agent, worker, orchestrator, system, unauthenticated,
non-human, or AI proposal-apply path can:
1. submit a bid (`submit_bid`),
2. approve match funding (`approve_match_funding`),
3. certify a claim (`certify_claim`), or
4. record cash (`record_cash`),
across both `Store` and `SqlStore`, `Assistants`, `form_review`, and AST-verified
`src/agents` and `src/orchestrator` package boundaries, while legitimate
designated independent humans continue to succeed.
"""

from __future__ import annotations

import ast
import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset
import release_support
from test_finance_signoffs import STAFF
from test_form_staging import schema as staging_schema
from test_grant_lifecycle_controls import designate
from zava_forward.core import ai_registry as _untyped_registry
from zava_forward.core import assistants as _untyped_assistants
from zava_forward.core import bounded_ai, finance, form_review, forms
from zava_forward.core.finance import (
    PROTECTED_FINANCE_OPERATIONS,
    AutomatedFinanceAuthorityRefusedError,
    classify_finance_operation,
    guard_no_automated_finance_authority,
    verify_no_automated_finance_authority,
)
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

AI_REGISTRY: Any = _untyped_registry
ASSISTANTS_MOD: Any = _untyped_assistants
DATASET_MOD: Any = dataset
RELEASE_SUPPORT: Any = release_support
STORE_CLS: Any = Store
SQL_STORE_CLS: Any = SqlStore

REPO_SRC = Path(__file__).resolve().parents[2]
ASSIST_ENV: dict[str, str] = {
    "ZF_ASSIST_AUTHORITY": "Synthetic Programme Sponsor",
    "ZF_ASSIST_CALL_ALLOWANCE": "25",
    "ZF_ASSIST_TOKEN_ALLOWANCE": "500000",
    "ZF_ASSIST_EXPIRES": "2999-01-01T00:00:00Z",
}


def _person(code: str, role: str, **kw: Any) -> dict[str, Any]:
    return {
        "code": code,
        "name": f"{role} {code}",
        "email": f"{code.lower()}@example.test",
        "role": role,
        **kw,
    }


def _lines(
    qty: int = 10,
    amount: int = 1000,
    ms: str = "MS-1",
    measure: str = "Loft insulation",
) -> list[dict[str, Any]]:
    return [{"measure": measure, "quantity": qty, "amount": amount, "milestone_ref": ms}]


def _automated_actors(human_template: dict[str, Any]) -> list[tuple[str, object]]:
    return [
        ("none_unauthenticated", None),
        ("string_worker", "background-grant-worker"),
        ("empty_dict_unauthenticated", {}),
        ("blank_identity_dict", {"name": "Anonymous Caller", "role": "Retrofit Programme Manager"}),
        (
            "agent_actor_type",
            {**human_template, "actor_type": "agent"},
        ),
        (
            "orchestrator_actor_type",
            {**human_template, "actor_type": "orchestrator"},
        ),
        (
            "worker_flag",
            {**human_template, "is_worker": True},
        ),
        (
            "system_flag",
            {**human_template, "is_system": True},
        ),
        (
            "service_principal_flag",
            {**human_template, "service_principal": True},
        ),
        (
            "managed_identity_source",
            {**human_template, "identity_source": "managed_identity"},
        ),
        (
            "explicit_non_human",
            {**human_template, "human": False},
        ),
        (
            "authority_non_human",
            {
                **human_template,
                "financial_authority": {
                    **copy.deepcopy(human_template["financial_authority"]),
                    "human": False,
                },
            },
        ),
        (
            "agent_email_prefix",
            {**human_template, "email": "agent@zava.example"},
        ),
        (
            "bot_code_prefix",
            {**human_template, "code": "BOT-PM-93"},
        ),
        (
            "automated_role",
            {**human_template, "role": "orchestrator"},
        ),
        (
            "caller_with_proposal_id",
            {**human_template, "proposal_id": "PROP-CALLER-93"},
        ),
    ]


class _NoAutomatedFinanceMatrixMixin:
    sql: bool = False
    tmp: tempfile.TemporaryDirectory[str]
    seed_path: Path
    store: Any
    geo: dict[str, Any]
    pm_a: dict[str, Any]
    pm_b: dict[str, Any]
    rc: dict[str, Any]
    inv_id: str
    claim_grant_id: str
    cash_grant_id: str

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        data: dict[str, Any] = copy.deepcopy(DATASET_MOD.DATA)
        staff_list: list[dict[str, Any]] = copy.deepcopy(STAFF)

        geo_raw = next(s for s in staff_list if s["code"] == "GEO-1")
        geo_designated = designate({**geo_raw, "oid": "syn-93-geo"})
        pm_a = designate(_person("PM-93-A", "Retrofit Programme Manager", oid="syn-93-pma"))
        pm_b = designate(_person("PM-93-B", "Retrofit Programme Manager", oid="syn-93-pmb"))
        rc = next(s for s in staff_list if s["code"] == "RC-1")

        # Extend synthetic fixture permissions to ZF-3 as well for funding_step probes
        for member in (geo_designated, pm_a, pm_b):
            perms = list(member["financial_authority"]["permissions"])
            extra = [
                {**p, "case_id": "ZF-3"} for p in perms if p["action"].startswith("application:")
            ]
            member["financial_authority"]["permissions"] = perms + extra

        staff_list = [s for s in staff_list if s["code"] != "GEO-1"] + [
            geo_designated,
            pm_a,
            pm_b,
        ]
        data["staff"] = staff_list
        for c in data["cases"]:
            c["funding_route"] = "SYN-95"
            c["measures"] = "Loft insulation"

        self.seed_path = Path(self.tmp.name) / "seed-93.json"
        self.seed_path.write_text(json.dumps(data), encoding="utf-8")
        self.geo = geo_designated
        self.pm_a = pm_a
        self.pm_b = pm_b
        self.rc = rc
        self.store = self._open_store()
        self._arm_ready_operations()

    def tearDown(self) -> None:
        if hasattr(self.store, "db"):
            self.store.db.close()
        self.tmp.cleanup()

    def _open_store(self) -> Any:
        if self.sql:
            return SQL_STORE_CLS(str(self.seed_path), str(self.seed_path.with_suffix(".sqlite")))
        return STORE_CLS(str(self.seed_path))

    def _arm_ready_operations(self) -> None:
        # 1. ZF-3 funding draft: Approved -> ready for submit_bid; ZF-1 ready for approve
        with self.store.lock:
            self.store._case("ZF-1")["funding"]["route"] = "SYN-95"
            self.store._case("ZF-3")["funding"]["route"] = "SYN-95"
            self.store._case("ZF-1")["decision"] = {
                "status": "Accepted",
                "by": "Pat Test",
                "at": "2026-01-01",
            }
            missing_zf3 = [
                str(x["kind"])
                for x in self.store.checklist(self.store.cases["ZF-3"])
                if not x["present"]
            ]
            missing_zf1 = [
                str(x["kind"])
                for x in self.store.checklist(self.store.cases["ZF-1"])
                if not x["present"]
            ]
            self.store.save()
        for kind in missing_zf3:
            self.store.add_document(
                self.pm_a,
                "ZF-3",
                f"{kind.lower().replace(' ', '-')}-93.txt",
                kind,
                f"Synthetic {kind} evidence".encode(),
                metadata={
                    "source": "SYN-93",
                    "source_version": "1",
                    "reason": "Synthetic fixture",
                },
            )
        for kind in missing_zf1:
            self.store.add_document(
                self.pm_a,
                "ZF-1",
                f"{kind.lower().replace(' ', '-')}-93-zf1.txt",
                kind,
                f"Synthetic {kind} evidence".encode(),
                metadata={
                    "source": "SYN-93",
                    "source_version": "1",
                    "reason": "Synthetic fixture",
                },
            )
        self.store.funding_draft(self.pm_a, "ZF-3")
        self.store.funding_step(self.pm_a, "ZF-3", "approve", "SYN-93 approved draft")
        self.store.funding_draft(self.pm_a, "ZF-1")

        # 2. ZF-1 finance: accepted invoice for payment_status + budget proposal for budget_approve
        self.store.finance_action(
            self.geo,
            "ZF-1",
            {"action": "budget_propose", "amount": 10000, "note": "SYN-93 initial budget"},
        )
        self.store.finance_action(self.pm_a, "ZF-1", {"action": "budget_approve"})
        self.store.finance_action(
            self.geo,
            "ZF-1",
            {
                "action": "commit_raise",
                "supplier": "Test Ltd",
                "contract": "C-1",
                "work_order": "WO-1",
                "measure": "Loft insulation",
                "amount": 5000,
                "quantity": 10,
            },
        )
        cmt_id = str(self.store.detail("ZF-1")["finance"]["commitments"][0]["id"])
        self.store.finance_action(self.pm_a, "ZF-1", {"action": "commit_approve", "id": cmt_id})
        self.store.finance_action(
            self.geo,
            "ZF-1",
            {
                "action": "invoice_receive",
                "kind": "Invoice",
                "supplier": "Test Ltd",
                "work_order": "WO-1",
                "ref": "INV-93",
                "lines": _lines(),
            },
        )
        self.inv_id = str(self.store.detail("ZF-1")["finance"]["invoices"][0]["id"])
        self.store.finance_action(self.geo, "ZF-1", {"action": "invoice_match", "id": self.inv_id})
        self.store.finance_action(
            self.pm_a,
            "ZF-1",
            {
                "action": "disposition",
                "id": self.inv_id,
                "decision": "Accept for payment",
                "note": "SYN-93 accepted for payment",
            },
        )
        self.store.finance_action(
            self.geo,
            "ZF-2",
            {"action": "budget_propose", "amount": 12000, "note": "SYN-93 ZF-2 match budget"},
        )

        # 3. ZF-1 grants: GR-1 pending Submitted; GR-2 pending Cash received
        self.store.grant_action(
            self.geo, "ZF-1", {"action": "grant_open", "scheme": "SYN-95", "source": "SYN-93 G1"}
        )
        self.store.grant_action(self.pm_a, "ZF-1", {"action": "grant_approve", "id": "GR-1"})
        for next_state in ("Award", "Claimable"):
            self.store.grant_action(
                self.geo,
                "ZF-1",
                {
                    "action": "grant_propose",
                    "id": "GR-1",
                    "to": next_state,
                    "source": f"SYN {next_state}",
                },
            )
            self.store.grant_action(self.pm_b, "ZF-1", {"action": "grant_approve", "id": "GR-1"})
        self.store.grant_action(
            self.geo,
            "ZF-1",
            {
                "action": "grant_eligibility",
                "id": "GR-1",
                "eligibility": "Eligible",
                "eligibility_source": "SYN-93 eligibility",
            },
        )
        self.store.grant_action(
            self.pm_a,
            "ZF-1",
            {"action": "grant_propose", "id": "GR-1", "to": "Submitted", "source": "SYN-93 claim"},
        )
        self.claim_grant_id = "GR-1"

        self.store.grant_action(
            self.geo, "ZF-1", {"action": "grant_open", "scheme": "SYN-95", "source": "SYN-93 G2"}
        )
        self.store.grant_action(self.pm_a, "ZF-1", {"action": "grant_approve", "id": "GR-2"})
        for next_state in ("Award", "Claimable", "Submitted", "Accepted"):
            if next_state == "Submitted":
                self.store.grant_action(
                    self.geo,
                    "ZF-1",
                    {
                        "action": "grant_eligibility",
                        "id": "GR-2",
                        "eligibility": "Eligible",
                        "eligibility_source": "SYN-93 eligibility 2",
                    },
                )
            proposer = self.pm_a if next_state == "Submitted" else self.geo
            self.store.grant_action(
                proposer,
                "ZF-1",
                {
                    "action": "grant_propose",
                    "id": "GR-2",
                    "to": next_state,
                    "source": f"SYN {next_state}",
                },
            )
            self.store.grant_action(self.pm_b, "ZF-1", {"action": "grant_approve", "id": "GR-2"})
        self.store.grant_action(
            self.geo,
            "ZF-1",
            {
                "action": "grant_propose",
                "id": "GR-2",
                "to": "Cash received",
                "source": "SYN-93 bank remittance",
                "amount": 1000,
            },
        )
        self.cash_grant_id = "GR-2"

        # 4. Register synthetic form schema for form_review probes
        forms.register_schema(
            self.store, self.pm_a, {**staging_schema(), "reviewer": self.pm_a["email"]}
        )

    def _snapshot(self) -> tuple[dict[str, Any], int]:
        with self.store.lock:
            if hasattr(self.store, "_sync"):
                self.store._sync()
            return copy.deepcopy(self.store.cases), len(list(self.store.audit_entries()))

    def test_all_four_operations_refuse_automated_actors_with_structured_error_and_zero_mutation(
        self,
    ) -> None:
        test_self: Any = self
        before_cases, before_audit = self._snapshot()

        for actor_label, actor in _automated_actors(self.pm_b):
            matrix: tuple[tuple[str, Any], ...] = (
                (
                    "submit_bid",
                    lambda a=actor: self.store.funding_step(a, "ZF-3", "submit", "REF-AUTO-93"),
                ),
                (
                    "submit_bid",
                    lambda a=actor: self.store.grant_action(
                        a, "ZF-1", {"action": "grant_open", "scheme": "SYN-95", "source": "SYN"}
                    ),
                ),
                (
                    "submit_bid",
                    lambda a=actor: form_review.action(
                        self.store, a, "ZF-1", {"action": "submit_bid"}
                    ),
                ),
                (
                    "approve_match_funding",
                    lambda a=actor: self.store.finance_action(
                        a, "ZF-2", {"action": "budget_approve"}
                    ),
                ),
                (
                    "approve_match_funding",
                    lambda a=actor: self.store.funding_step(a, "ZF-1", "approve", "SYN-AUTO"),
                ),
                (
                    "certify_claim",
                    lambda a=actor: self.store.grant_action(
                        a, "ZF-1", {"action": "grant_approve", "id": self.claim_grant_id}
                    ),
                ),
                (
                    "certify_claim",
                    lambda a=actor: form_review.action(
                        self.store,
                        a,
                        "ZF-1",
                        {"action": "open", "schema_id": "SYN-TECH", "schema_version": 1},
                    ),
                ),
                (
                    "record_cash",
                    lambda a=actor: self.store.grant_action(
                        a, "ZF-1", {"action": "grant_approve", "id": self.cash_grant_id}
                    ),
                ),
                (
                    "record_cash",
                    lambda a=actor: self.store.finance_action(
                        a,
                        "ZF-1",
                        {
                            "action": "payment_status",
                            "id": self.inv_id,
                            "status": "Paid outside this system",
                        },
                    ),
                ),
            )
            for expected_op, call in matrix:
                with test_self.subTest(actor=actor_label, operation=expected_op):
                    with test_self.assertRaises(AutomatedFinanceAuthorityRefusedError) as ctx:
                        call()
                    err = ctx.exception
                    test_self.assertIsInstance(err, ValueError)
                    test_self.assertEqual(err.operation, expected_op)
                    test_self.assertEqual(err.rule, "RULE-010")
                    rec = err.as_record()
                    test_self.assertEqual(rec["operation"], expected_op)
                    test_self.assertEqual(rec["code"], "automated_finance_authority_refused")

        after_cases, after_audit = self._snapshot()
        test_self.assertEqual(after_cases, before_cases)
        test_self.assertEqual(after_audit, before_audit)
        test_self.assertTrue(self.store.verify_audit())

    def test_ai_proposal_generation_and_acceptance_never_apply_to_four_operations(
        self,
    ) -> None:
        test_self: Any = self
        # 1. Generate and accept funding_draft AI proposal via Store.review_ai
        draft_out = self.store.funding_draft(self.pm_a, "ZF-1", mode="offline")
        rec_id = str(draft_out["record_id"])
        accepted_rec = self.store.review_ai(self.pm_a, rec_id, "accept")
        test_self.assertEqual(accepted_rec["status"], "Accepted")
        test_self.assertEqual(self.store.cases["ZF-1"]["funding"]["status"], "Draft ready")
        test_self.assertIsNone(self.store.cases["ZF-1"]["funding"].get("approved_by"))
        test_self.assertFalse(self.store.cases["ZF-1"].get("funding_ok"))

        # 2. On SqlStore, also generate, verify, and accept funding-evidence via Assistants
        assistant_tid = "AST-SYN-93"
        if hasattr(self.store, "assistant_connection"):
            self.store.ai.endpoint = "https://synthetic-aoai.openai.azure.com"

            def _provider(_system: str, _prompt: str, *_args: Any) -> dict[str, Any]:
                return {
                    "text": json.dumps(
                        {
                            "summary": "Synthetic grant evidence check only.",
                            "findings": [{"text": "EPC D present.", "citations": ["source:home"]}],
                            "unknowns": [],
                        }
                    ),
                    "model": "test-model",
                    "outcome": "returned",
                    "source": "ai",
                    "usage": {
                        "prompt_tokens": 12,
                        "completion_tokens": 8,
                        "total_tokens": 20,
                        "cached_tokens": 0,
                    },
                }

            svc = ASSISTANTS_MOD.Assistants(self.store, env=ASSIST_ENV, provider=_provider)
            try:
                RELEASE_SUPPORT.install(self.store, cls="actual")
                created = svc.invoke(self.geo, "funding-evidence", "ZF-1")
                assistant_tid = str(created["id"])
                svc.execute(assistant_tid)
                ready = svc.detail(self.geo, assistant_tid)
                verified = svc.review(
                    self.geo,
                    assistant_tid,
                    "verify",
                    ready["revision"],
                    note="SYN-93 verified source",
                    source_verified=True,
                )
                accepted_task = svc.review(
                    self.geo,
                    assistant_tid,
                    "accept",
                    verified["revision"],
                    note="SYN-93 accepted proposal notes",
                )
                test_self.assertEqual(accepted_task["state"], "accepted")
            finally:
                svc.stop()

        # 3. Applying accepted proposals or automated shortcut actions across all 4 ops fails closed
        before_cases, before_audit = self._snapshot()
        proposal_attempts: tuple[tuple[str, Any], ...] = (
            (
                "submit_bid",
                lambda: self.store.funding_step(
                    self.pm_b,
                    "ZF-3",
                    "submit",
                    "REF-PROP-93",
                    body={"recommendation_id": rec_id},
                ),
            ),
            (
                "submit_bid",
                lambda: self.store.grant_action(
                    self.geo,
                    "ZF-1",
                    {"action": "submit_bid", "scheme": "SYN-95", "source": "SYN"},
                ),
            ),
            (
                "approve_match_funding",
                lambda: self.store.finance_action(
                    self.pm_b,
                    "ZF-2",
                    {"action": "budget_approve", "assistant_task_id": assistant_tid},
                ),
            ),
            (
                "approve_match_funding",
                lambda: self.store.finance_action(
                    self.pm_b,
                    "ZF-2",
                    {"action": "approve_match_funding", "amount": 5000},
                ),
            ),
            (
                "certify_claim",
                lambda: self.store.grant_action(
                    self.pm_b,
                    "ZF-1",
                    {
                        "action": "grant_approve",
                        "id": self.claim_grant_id,
                        "proposal_id": rec_id,
                    },
                ),
            ),
            (
                "certify_claim",
                lambda: form_review.action(
                    self.store,
                    self.pm_a,
                    "ZF-1",
                    {
                        "action": "open",
                        "schema_id": "SYN-TECH",
                        "schema_version": 1,
                        "assistant_task_id": assistant_tid,
                    },
                ),
            ),
            (
                "record_cash",
                lambda: self.store.grant_action(
                    self.pm_b,
                    "ZF-1",
                    {
                        "action": "grant_approve",
                        "id": self.cash_grant_id,
                        "from_proposal": assistant_tid,
                    },
                ),
            ),
            (
                "record_cash",
                lambda: self.store.finance_action(
                    self.pm_b,
                    "ZF-1",
                    {
                        "action": "payment_status",
                        "id": self.inv_id,
                        "status": "Paid outside this system",
                        "auto_apply": True,
                    },
                ),
            ),
        )
        for expected_op, attempt in proposal_attempts:
            with test_self.subTest(operation=expected_op):
                with test_self.assertRaises(AutomatedFinanceAuthorityRefusedError) as ctx:
                    attempt()
                test_self.assertEqual(ctx.exception.operation, expected_op)

        after_cases, after_audit = self._snapshot()
        test_self.assertEqual(after_cases, before_cases)
        test_self.assertEqual(after_audit, before_audit)

        # 4. Designated independent human actors succeed cleanly on all 4 operations
        self.store.funding_step(self.pm_b, "ZF-3", "submit", "REF-HUMAN-93")
        self.store.finance_action(self.pm_b, "ZF-2", {"action": "budget_approve"})
        self.store.grant_action(
            self.pm_b, "ZF-1", {"action": "grant_approve", "id": self.claim_grant_id}
        )
        self.store.grant_action(
            self.pm_b, "ZF-1", {"action": "grant_approve", "id": self.cash_grant_id}
        )
        self.store.finance_action(
            self.pm_b,
            "ZF-1",
            {
                "action": "payment_status",
                "id": self.inv_id,
                "status": "Paid outside this system",
            },
        )
        test_self.assertEqual(self.store.cases["ZF-3"]["funding"]["status"], "Submitted")
        test_self.assertEqual(self.store.detail("ZF-2")["finance"]["budget"]["status"], "Approved")
        grants_by_id = {g["id"]: g for g in self.store.detail("ZF-1")["grants"]}
        test_self.assertEqual(grants_by_id[self.claim_grant_id]["state"], "Submitted")
        test_self.assertEqual(grants_by_id[self.cash_grant_id]["state"], "Cash received")

    def test_stored_non_human_staff_record_and_verifier_preserve_caller_store(
        self,
    ) -> None:
        test_self: Any = self
        before_cases, before_audit = self._snapshot()
        report = verify_no_automated_finance_authority(self.store)
        test_self.assertTrue(report["ok"])
        test_self.assertEqual(report["rule"], "RULE-010")
        test_self.assertEqual(tuple(report["operations"]), PROTECTED_FINANCE_OPERATIONS)
        for op_name in PROTECTED_FINANCE_OPERATIONS:
            test_self.assertGreater(report["refusal_counts"][op_name], 0)
        after_verify_cases, after_verify_audit = self._snapshot()
        test_self.assertEqual(after_verify_cases, before_cases)
        test_self.assertEqual(after_verify_audit, before_audit)

        # Mutate stored staff record for pm_b to human=False and verify finance_action rejects it
        email = self.pm_b["email"]
        with self.store.lock:
            mutated = copy.deepcopy(self.store.staff[email])
            mutated["financial_authority"]["human"] = False
            self.store.staff[email] = mutated
            if hasattr(self.store, "db"):
                with self.store.dblock:
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(mutated), email),
                    )
                    self.store.db.commit()
        with test_self.assertRaises(AutomatedFinanceAuthorityRefusedError) as ctx:
            self.store.finance_action(self.pm_b, "ZF-2", {"action": "budget_approve"})
        test_self.assertEqual(ctx.exception.operation, "approve_match_funding")
        test_self.assertEqual(ctx.exception.actor_kind, "non_human_staff")


class StoreNoAutomatedFinance93Test(_NoAutomatedFinanceMatrixMixin, unittest.TestCase):
    sql = False


class SqlStoreNoAutomatedFinance93Test(_NoAutomatedFinanceMatrixMixin, unittest.TestCase):
    sql = True


class VerifierAndModuleBoundary93Test(unittest.TestCase):
    def test_standalone_verifier_and_operation_classification_cover_all_four_operations(
        self,
    ) -> None:
        report = verify_no_automated_finance_authority()
        self.assertTrue(report["ok"])
        self.assertEqual(report["operations"], PROTECTED_FINANCE_OPERATIONS)
        self.assertEqual(report["ai_capabilities_checked"], ("funding-evidence", "funding_draft"))
        self.assertGreater(report["probes_executed"], 20)

        self.assertEqual(classify_finance_operation("funding_step", "submit"), "submit_bid")
        self.assertEqual(
            classify_finance_operation("funding_step", "approve"),
            "approve_match_funding",
        )
        self.assertEqual(classify_finance_operation("funding_step", "confirm"), "record_cash")
        self.assertEqual(
            classify_finance_operation(
                "grant_action", "grant_approve", {"id": "GR-1"}, pending_to="Submitted"
            ),
            "certify_claim",
        )
        self.assertEqual(
            classify_finance_operation(
                "grant_action", "grant_approve", {"id": "GR-2"}, pending_to="Cash received"
            ),
            "record_cash",
        )
        self.assertEqual(
            classify_finance_operation("finance_action", "payment_status"),
            "record_cash",
        )
        self.assertEqual(classify_finance_operation("form_review", "submit"), "submit_bid")

        # Valid Entra human staff dict passes guard_no_automated_finance_authority cleanly
        guard_no_automated_finance_authority(
            {
                "code": "PM-ENTRA",
                "name": "Human Entra Staff",
                "email": "human.entra@example.test",
                "role": "Retrofit Programme Manager",
                "identity_source": "entra",
                "auth_provider": "trusted-proxy",
            },
            operation="approve_match_funding",
        )

    def test_agents_and_orchestrator_packages_expose_no_automated_finance_or_grant_path(
        self,
    ) -> None:
        forbidden = {
            "finance_action",
            "grant_action",
            "funding_step",
            "_financial_authority",
            "submit_bid",
            "approve_match_funding",
            "certify_claim",
            "record_cash",
        }
        inspected = 0
        for pkg in ("agents", "orchestrator"):
            src_root = REPO_SRC / pkg / "src"
            self.assertTrue(src_root.is_dir(), f"Missing {src_root}")
            for py_file in sorted(src_root.rglob("*.py")):
                inspected += 1
                tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
                found = {
                    node.attr if isinstance(node, ast.Attribute) else node.id
                    for node in ast.walk(tree)
                    if isinstance(node, (ast.Attribute, ast.Name))
                }
                with self.subTest(file=str(py_file.relative_to(REPO_SRC))):
                    self.assertEqual(found & forbidden, set())
        self.assertGreaterEqual(inspected, 2)

    def test_verifier_fails_closed_when_capability_or_module_boundary_is_tampered(
        self,
    ) -> None:
        # 1. Tampered bounded_ai capability audit fails closed
        bad_audit: dict[str, Any] = {
            "ok": False,
            "violations": ["funding_draft executable"],
            "capabilities": {},
        }
        with (
            patch.object(bounded_ai, "audit_registered_capabilities", return_value=bad_audit),
            self.assertRaises(AutomatedFinanceAuthorityRefusedError) as cap_ctx,
        ):
            verify_no_automated_finance_authority()
        self.assertEqual(cap_ctx.exception.actor_kind, "capability_registry")

        # 2. Tampered ai_registry permitted_capability fails closed even if audit returns ok
        drifted_tasks: dict[str, Any] = copy.deepcopy(dict(AI_REGISTRY.tasks()))
        drifted_tasks["funding_draft"] = {
            **drifted_tasks["funding_draft"],
            "permitted_capability": "auto-submit and execute grant bids",
        }
        with (
            patch.object(AI_REGISTRY, "tasks", return_value=drifted_tasks),
            self.assertRaises(AutomatedFinanceAuthorityRefusedError) as mode_ctx,
        ):
            verify_no_automated_finance_authority()
        self.assertEqual(mode_ctx.exception.actor_kind, "capability_registry")

        # 3. Tampered automation module AST boundary fails closed
        with (
            patch.object(
                finance,
                "_scan_python_files_for_authority_calls",
                return_value=["orchestrator/server.py:42:grant_action"],
            ),
            self.assertRaises(AutomatedFinanceAuthorityRefusedError) as ast_ctx,
        ):
            verify_no_automated_finance_authority()
        self.assertEqual(ast_ctx.exception.actor_kind, "module_boundary")
