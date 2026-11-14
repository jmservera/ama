"""Epic #104 criteria 3 and 5: AI never decides, and no capability runs without owned limits.

Cross-capability guard over every registered AI task. It adds no behaviour: it fails when a
registered capability, assistant, chat, concern pack or held-out adapter stops being bounded.
Everything is offline and synthetic; nothing here is an approval, a price or a paid call.
"""

from __future__ import annotations

import ast
import copy
import json
import math
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.core import aftercare, ai_registry, assistants, ranking
from zava_forward.core.ai_consumption import (
    CallContext,
    Consumption,
    DispatchHeld,
    reference,
)
from zava_forward.core.ai_consumption_demo import END, MODEL, START, DemoPort
from zava_forward.core.store import Store

import zava_forward.agents.chat as chat_module
import zava_forward.agents.dispatch as dispatch_module
from heldout_freeze_fixture import manifest
from test_dispatch import good_text, limits, make_task, message, returned
from test_heldout_batch import Spy, auth, run
from zava_forward.agents import ai_eval, chat_eval
from zava_forward.agents.chat import ChatModel
from zava_forward.agents.dispatch import AgentWorker

ASSISTANTS = (
    "stock-prioritisation",
    "assessment-preparation",
    "funding-evidence",
    "works-resident-coordination",
    "quality-evidence",
)
RETAINED = ("briefing", "message", "summary", "priority", "funding_draft", "read_document")
EXPECTED = set(ASSISTANTS) | set(RETAINED) | {"chat-case-conversation", "aftercare-concern-pack"}
harness: Any = ai_eval  # the offline harness is untyped


class RegistryGuard(unittest.TestCase):
    def test_every_registered_capability_is_known_to_this_suite(self) -> None:
        self.assertEqual(set(ai_registry.tasks()), EXPECTED)
        self.assertEqual(set(assistants.REGISTRY), set(ASSISTANTS))

    def test_no_capability_is_approved_live_or_allowed_to_act(self) -> None:
        for task_id, entry in ai_registry.tasks().items():
            with self.subTest(task=task_id):
                self.assertEqual(entry["approval_state"], "unapproved")
                self.assertFalse(ai_registry.authorizes_live(task_id, {}))
                text = json.dumps(entry).lower()
                self.assertIn("no write, send, approve or rank", text)

    def test_only_the_exact_demo_switch_honours_chat_and_nothing_else(self) -> None:
        env = {
            ai_registry.DEMO_SWITCH: "approved-2026-11-03",
            ai_registry.DEMO_PROFILE: ai_registry.DEMO_PROFILE_VALUE,
        }
        live = {t for t in ai_registry.tasks() if ai_registry.authorizes_live(t, env)}
        self.assertEqual(live, {"chat-case-conversation"})
        for bad in (
            {ai_registry.DEMO_SWITCH: "approved-2026-11-03"},
            {ai_registry.DEMO_PROFILE: "demo"},
            {**env, ai_registry.DEMO_SWITCH: "yes"},
            {**env, ai_registry.DEMO_PROFILE: "production"},
        ):
            self.assertFalse(ai_registry.authorizes_live("chat-case-conversation", bad), bad)

    def test_chat_and_concern_pack_are_registered_disabled(self) -> None:
        for task_id in ("chat-case-conversation", "aftercare-concern-pack"):
            entry = ai_registry.tasks()[task_id]
            self.assertEqual((entry["enabled"], entry["state"]), (False, "disabled"))


class AssistantNonMutation(unittest.TestCase):
    def task(self, capability: str) -> dict[str, Any]:
        task = make_task()
        task["capability"] = capability
        return task

    def handle(self, capability: str, text: str | None) -> tuple[Any, list[Any]]:
        calls: list[Any] = []

        def provider(*args: Any) -> dict[str, Any]:
            calls.append(args)
            return returned(text)

        task = self.task(capability)
        before = copy.deepcopy(task["snapshot"])
        result = AgentWorker(provider).handle(message(task), limits())
        assert result is not None
        self.assertEqual(task["snapshot"], before)
        return result, calls

    def test_valid_output_is_a_single_unapproved_proposal_for_each_assistant(self) -> None:
        for capability in ASSISTANTS:
            with self.subTest(capability=capability):
                result, calls = self.handle(capability, good_text())
                self.assertIsNone(result.failure)
                self.assertEqual(len(calls), 1)
                self.assertIs(result.envelope["approved"], False)
                self.assertEqual(set(result.output or {}), {"summary", "findings", "unknowns"})

    def test_hostile_outputs_never_become_a_decision_or_ranking(self) -> None:
        cited = [dict(text="t", citations=["home.epc"])]
        hostile = {
            "approved": dict(summary="s", findings=cited, unknowns=[], approved=True),
            "rank": dict(summary="s", findings=cited, unknowns=[], rank=1),
            "transition": dict(summary="s", findings=cited, unknowns=[], next_stage="Complete"),
            "uncited": dict(summary="s", findings=[dict(text="t", citations=["x"])], unknowns=[]),
        }
        for capability in ASSISTANTS:
            for name, body in hostile.items():
                with self.subTest(capability=capability, hostile=name):
                    result, _ = self.handle(capability, json.dumps(body))
                    self.assertIsNone(result.output)
                    self.assertTrue(result.failure)
                    self.assertIs(result.envelope["approved"], False)

    def test_worker_and_chat_adapters_import_no_store_or_controlled_record_module(self) -> None:
        allowed_core = {"assistants", "ai_registry", "ai", "ai_consumption", "chat_panel"}
        for module in (dispatch_module, chat_module):
            tree = ast.parse(Path(str(module.__file__)).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.ImportFrom):
                    self.assertEqual(node.level, 0, "no relative imports in the worker")
                    names = [f"{node.module or ''}.{a.name}" for a in node.names]
                elif isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                for name in names:
                    self.assertNotRegex(name, r"\b(store|sqlstore|aftercare|grants?|consent)\b")
                    if name.startswith("zava_forward.core."):
                        self.assertIn(name.split(".")[2], allowed_core, name)


class RankingImmutability(unittest.TestCase):
    def test_ai_recommendation_is_proposed_and_never_changes_the_ranking_or_cases(self) -> None:
        specs = [dict(id=f"ZF-{n}", days=n * 10) for n in range(1, 6)]
        reversed_ids = [s["id"] for s in reversed(specs)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eval.json"
            cases = [harness.build_case(s) for s in specs]
            path.write_text(json.dumps(dict(staff=[harness.OWNER, harness.OTHER], cases=cases)))
            store = Store(str(path), str(Path(tmp) / "live.json"), str(Path(tmp) / "audit.jsonl"))
            output = json.dumps(
                [
                    dict(case_id=i, reason="Waiting.", cites=[f"Days in stage: {s['days']}"])
                    for i, s in zip(reversed_ids, specs, strict=True)
                ]
            )
            harness._scripted(store, [output])
            before_rank = copy.deepcopy(store._ranking())
            before_cases = copy.deepcopy(store.cases)
            deterministic = ranking.canonical(before_rank)
            rec = store.ai_priority(harness.OWNER, 5)
            proposed = [i["case_id"] for i in rec["items"]]
            by_rank = sorted(before_rank, key=lambda i: before_rank[i]["rank"])
            self.assertNotEqual(proposed, by_rank)
            self.assertEqual(rec["status"], "Proposed")
            self.assertEqual(rec["source"], "ai")
            self.assertEqual(ranking.canonical(store._ranking()), deterministic)
            self.assertEqual(store.cases, before_cases)
            with self.assertRaises(PermissionError):
                store.resolve_priority(harness.OTHER, rec["id"], "accept")
            self.assertEqual(store.cases, before_cases)
            self.assertEqual(ranking.canonical(store._ranking()), deterministic)
            done = store.resolve_priority(harness.OWNER, rec["id"], "reject", "Not needed.")
            self.assertEqual(done["status"], "Rejected")
            self.assertEqual(ranking.canonical(store._ranking()), deterministic)
            self.assertEqual(store.cases, before_cases)


class ChatBoundaries(unittest.TestCase):
    def test_golden_chat_run_refuses_actions_and_never_enables(self) -> None:
        report = chat_eval.run_eval()
        self.assertTrue(report["passed"], report["failures"])
        enablement = report["enablement"]
        self.assertEqual((enablement["outcome"], enablement["state"]), ("insufficient", "disabled"))
        self.assertEqual(enablement["actual_calls"], "blocked")
        self.assertFalse(ai_registry.authorizes_live(chat_eval.TASK, {}))

    def test_chat_model_without_admission_is_denied_before_any_call(self) -> None:
        calls: list[Any] = []

        def provider(*args: Any) -> dict[str, Any]:
            calls.append(args)
            return returned(good_text())

        for admission in (None, lambda: "not approved"):
            model = ChatModel(AgentWorker(provider), admission=admission)
            with self.assertRaises(Exception) as caught:
                model("system", "prompt")
            self.assertEqual(calls, [])
            self.assertIn("activation-not-approved", str(caught.exception))


class ConcernPack(unittest.TestCase):
    def test_pack_is_unreviewed_owner_only_and_leaves_the_concern_unchanged(self) -> None:
        reg = aftercare.AftercareRegister()
        cid = str(
            reg.raise_concern(
                route="digital",
                raised_by="household",
                home_ref="H1",
                kind="discomfort",
                statement="The living room stays cold in the evening.",
                owner="Aftercare Lead",
                next_update="2026-12-01",
            )["id"]
        )
        before = copy.deepcopy(reg.concerns)
        pack = reg.propose_pack(cid, "Household reports a cold living room in the evening.")
        self.assertEqual((pack["approved"], pack["approval"]), (False, aftercare.PACK_NOT_REVIEWED))
        with self.assertRaises(ValueError):
            reg.propose_pack(cid, "The higher use was caused by the household.")
        self.assertEqual(reg.concerns, before)
        with self.assertRaises(PermissionError):
            reg.review_pack(str(pack["id"]), "Someone Else", "accept", "Fine")
        self.assertEqual(reg.concerns, before)
        done = reg.review_pack(str(pack["id"]), "Aftercare Lead", "accept", "Reviewed")
        self.assertNotEqual(done["approval"], aftercare.PACK_NOT_REVIEWED)
        self.assertEqual(reg.concerns, before)


def context(capability: str, config: str, attempt: str, depth: int = 1) -> CallContext:
    return CallContext(
        root=reference("root-" + capability),
        attempt=reference(attempt),
        capability=capability.replace("_", "-"),
        case_type="retrofit-case",
        configuration=config,
        prompt=reference("prompt-v1"),
        depth=depth,
    )


class Nfr012Limits(unittest.TestCase):
    """BRD NFR-012 / AC-100 for every registered capability, through the real ledger."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = Consumption(DemoPort(Path(self.tmp.name) / "l.sqlite"))
        self.config = reference("config-v1")

    def price(self, **over: Any) -> str:
        fields: dict[str, Any] = dict(
            source="https://prices.azure.com/api/retail/prices",
            source_hash=reference("price"),
            retrieved=START,
            version="v1",
            model=MODEL,
            currency="USD",
            start=START,
            end=END,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=False,
        )
        fields.update(over)
        return str(self.ledger.price(**fields))

    def authorize(self, capability: str, **over: Any) -> None:
        fields: dict[str, Any] = dict(
            authority="authority-1",
            owner="alert-owner",
            evidence="owner-approved",
            price=self.price(),
            capability=capability.replace("_", "-"),
            configuration=self.config,
            start=START,
            end=END,
            max_calls=2,
            max_depth=1,
            budgets=[dict(id=reference("period"), calls=2, tokens=5000, amount="1")],
        )
        fields.update(over)
        self.ledger.authorize(**fields)

    def alerts(self) -> list[dict[str, Any]]:
        import sqlite3

        db = sqlite3.connect(Path(self.tmp.name) / "l.sqlite")
        try:
            rows = db.execute("SELECT body FROM assistant_events").fetchall()
        finally:
            db.close()
        return [b for (raw,) in rows if (b := json.loads(raw)).get("kind") == "alert"]

    def held(self, ctx: CallContext, reason: str, **kw: Any) -> None:
        seen = len(self.alerts())
        with self.assertRaises(DispatchHeld) as caught:
            self.ledger.reserve(ctx, MODEL, kw.get("tokens", 1000), 100)
        self.assertEqual(str(caught.exception), reason)
        alerts = self.alerts()
        self.assertEqual(len(alerts), seen + 1)
        alert = alerts[-1]
        if kw.get("owner"):
            self.assertEqual(alert["owner"], kw["owner"])
        self.assertEqual(alert["route"], "workflow-only")
        self.assertEqual(alert["reason"], reason)
        self.assertTrue(alert["owner"])

    def test_no_authority_holds_every_capability_on_the_workflow_path(self) -> None:
        for capability in sorted(EXPECTED):
            with self.subTest(capability=capability):
                self.held(
                    context(capability, self.config, "a-" + capability),
                    "authority-unknown",
                    owner=reference("unassigned-owner-OD-51"),
                )

    def test_authorised_capability_is_admitted_within_limits_then_held_at_each_limit(self) -> None:
        for capability in sorted(EXPECTED):
            with self.subTest(capability=capability):
                config = reference("cfg-" + capability)
                self.authorize(
                    capability,
                    configuration=config,
                    authority="a-" + capability,
                    budgets=[
                        dict(id=reference("b-" + capability), calls=2, tokens=1200, amount="1")
                    ],
                )
                first = self.ledger.reserve(
                    context(capability, config, capability + "1"), MODEL, 1000, 100
                )
                self.assertTrue(first)
                self.ledger.complete(
                    first,
                    dict(prompt_tokens=10, completion_tokens=5, total_tokens=15, cached_tokens=0),
                    MODEL,
                    "returned",
                )
                self.held(
                    context(capability, config, capability + "d", depth=2),
                    "request-depth-limit",
                    owner=reference("alert-owner"),
                )
                self.held(
                    context(capability, config, capability + "big"),
                    "token-budget-limit",
                    tokens=1100,
                    owner=reference("alert-owner"),
                )
                self.ledger.reserve(context(capability, config, capability + "2"), MODEL, 1000, 100)
                self.held(
                    context(capability, config, capability + "3"),
                    "request-call-limit",
                    owner=reference("alert-owner"),
                )

    def test_unmeasured_usage_holds_the_budget_instead_of_assuming_zero(self) -> None:
        self.authorize("briefing", configuration=self.config)
        first = self.ledger.reserve(context("briefing", self.config, "u1"), MODEL, 1000, 100)
        usage = dict(prompt_tokens=1, completion_tokens=1, total_tokens=2, cached_tokens=None)
        self.ledger.complete(first, usage, MODEL, "returned")
        self.held(
            context("briefing", self.config, "u2"),
            "liability-unknown",
            owner=reference("alert-owner"),
        )

    def test_synthetic_price_blocks_a_live_call_and_money_limit_holds(self) -> None:
        synthetic = self.price(synthetic=True)
        self.authorize("assessment-preparation", price=synthetic, configuration=self.config)
        ctx = context("assessment-preparation", self.config, "x")
        with self.assertRaises(DispatchHeld) as caught:
            self.ledger.reserve(ctx, MODEL, 1000, 100, live=True)
        self.assertEqual(str(caught.exception), "price-unknown")
        other = reference("cfg-money")
        self.authorize(
            "funding-evidence",
            configuration=other,
            authority="a-money",
            budgets=[dict(id=reference("p2"), calls=5, tokens=10**9, amount="0.0000001")],
        )
        self.held(
            context("funding-evidence", other, "m"),
            "money-budget-limit",
            owner=reference("alert-owner"),
        )

    def test_authority_expires_to_the_workflow_path(self) -> None:
        self.authorize("quality-evidence", configuration=self.config)
        port: Any = self.ledger.port
        port.clock += 10**7
        self.held(
            context("quality-evidence", self.config, "late"),
            "authority-expired",
            owner=reference("alert-owner"),
        )

    def test_authority_needs_finite_positive_limits_and_a_named_owner(self) -> None:
        bad: list[dict[str, Any]] = [
            dict(budgets=[]),
            dict(max_calls=0),
            dict(max_depth=0),
            dict(max_calls=math.inf),
            dict(budgets=[dict(id=reference("p"), calls=1, tokens=1, amount="inf")]),
            dict(budgets=[dict(id=reference("p"), calls=1, tokens=1, amount="nan")]),
            dict(budgets=[dict(id=reference("p"), calls=1, tokens=1, amount="-1")]),
            dict(owner=""),
            dict(start=END, end=START),
        ]
        for over in bad:
            with self.subTest(over=over), self.assertRaises((ValueError, TypeError)):
                self.authorize("assessment-preparation", **over)

    def test_assistant_work_is_invalid_without_each_finite_setting(self) -> None:
        good = dict(
            ZF_ASSIST_AUTHORITY="op",
            ZF_ASSIST_CALL_ALLOWANCE="10",
            ZF_ASSIST_TOKEN_ALLOWANCE="1000000",
            ZF_ASSIST_EXPIRES="2999-01-01T00:00:00Z",
        )
        self.assertTrue(assistants.Limits(good).valid)
        for key in good:
            values = ("", "0", "-1", "inf", "nan", "x") if key != "ZF_ASSIST_AUTHORITY" else ("",)
            for value in (None, *values):
                env = dict(good)
                if value is None:
                    del env[key]
                else:
                    env[key] = value
                with self.subTest(key=key, value=value):
                    limit = assistants.Limits(env)
                    self.assertFalse(limit.valid)
                    self.assertTrue(limit.error)
        self.assertFalse(
            assistants.Limits({**good, "ZF_ASSIST_EXPIRES": "2999-01-01T00:00:00"}).valid
        )


class HeldOutAdapters(unittest.TestCase):
    def test_live_batch_runs_only_inside_a_complete_authorisation(self) -> None:
        spy = Spy()
        report = run(spy)
        self.assertGreater(len(spy.calls), 0)
        self.assertEqual(report["approved_by"], "owner")
        for key in (
            "approved_by",
            "authority_ref",
            "expires_utc",
            "max_calls",
            "max_total_tokens",
            "max_budget_usd",
            "currency",
            "model",
            "input_usd_per_1m",
            "output_usd_per_1m",
            "max_prompt_tokens",
            "max_completion_tokens",
        ):
            text = key in ("approved_by", "authority_ref", "model", "currency")
            for value in (None, "", " ") if text else (None, "", 0, -1, "inf", "nan", True):
                a = auth()
                if value is None:
                    del a[key]
                else:
                    a[key] = value
                with self.subTest(key=key, value=value):
                    blocked = Spy()
                    refused = run(blocked, a)
                    self.assertEqual(refused["outcome"], "refused")
                    self.assertEqual(blocked.calls, [])

    def test_expired_authorisation_makes_no_call(self) -> None:
        spy = Spy()
        report = run(spy, auth(expires_utc=datetime(2026, 11, 13, 11, tzinfo=UTC).isoformat()))
        self.assertEqual(report["outcome"], "refused")
        self.assertEqual(spy.calls, [])

    def test_chat_model_authorisation_blocks_each_missing_limit(self) -> None:
        ok = dict(
            authorised_by="owner",
            max_calls=10,
            max_tokens=1000,
            max_budget=5,
            budget_currency="GBP",
            expires_at="2026-12-01T00:00:00+00:00",
        )
        now = "2026-11-04T00:00:00Z"
        self.assertEqual(chat_eval.call_authorization(ok, 1, 1, now=now)["outcome"], "within-limit")
        for key in ok:
            broken = {k: v for k, v in ok.items() if k != key}
            with self.subTest(missing=key):
                self.assertEqual(
                    chat_eval.call_authorization(broken, 1, 1, now=now)["outcome"], "blocked"
                )
        self.assertEqual(chat_eval.call_authorization(None, 1, 1, now=now)["outcome"], "blocked")

    def test_manifest_fixture_is_not_mutated_by_a_refused_batch(self) -> None:
        m = manifest()
        before = copy.deepcopy(m)
        run(Spy(), auth(max_calls=0), m=m)
        self.assertEqual(m, before)


if __name__ == "__main__":
    unittest.main()
