"""Management view AI consumption economics and Unknown-not-zero invariants (Issue #100)."""

from __future__ import annotations

import copy
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dataset import DATA
from test_progress_reports import AS_OF, disposition
from zava_forward.core import ai_tasks, coordinator, insights, progress, tokenomics
from zava_forward.core.ai_consumption import (
    COMPONENTS,
    CallContext,
    Consumption,
    reference,
)
from zava_forward.core.assistants import Assistants
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

COST_KEYS = (
    "token_cost",
    "total_cost_of_ai",
    "token_cost_per_accepted_outcome",
    "cost_per_accepted_outcome",
    "quality_qualified_cost_per_accepted_outcome",
    "booked_value",
)
UNIT_COST_KEYS = (
    "token_cost_per_accepted_outcome",
    "cost_per_accepted_outcome",
    "quality_qualified_cost_per_accepted_outcome",
)
START = "2026-10-01T00:00:00Z"
END = "2026-10-10T00:00:00Z"
MODEL = "test-mgmt-model"


def _make_fixture() -> dict[str, Any]:
    data: dict[str, Any] = copy.deepcopy(DATA)
    data["staff"].append(
        dict(
            code="RC-100",
            name="Synthetic Coordinator",
            email="rc100@example.test",
            role="Retrofit Coordinator",
        )
    )
    data["cases"][0].update(
        stage="Contacting resident",
        building_id="SYN-B100",
        returns=[
            disposition(1, "2026-10-02T12:00:00Z", "Survey booked", "Contact paused"),
            disposition(2, "2026-10-04T12:00:00Z", "Contact paused", "Contacting resident"),
        ],
    )
    return data


def _coordinator_actor(store: Any) -> dict[str, Any]:
    for member in store.data["staff"]:
        if member.get("role") == "Retrofit Coordinator":
            return dict(member)
    raise AssertionError("Expected Retrofit Coordinator in fixture staff")


def _configure_priced_ledger(
    ledger: Consumption,
    *,
    config_ref: str,
    billed_amount: str = "0.000135",
    synthetic: bool = True,
) -> str:
    budget_id = reference(f"mgmt-period-{config_ref}")
    price_id = ledger.price(
        source="https://prices.azure.com/api/retail/prices",
        source_hash=reference("mgmt-price-hash-100"),
        retrieved=START,
        version="mgmt-v1",
        model=MODEL,
        currency="GBP",
        start=START,
        end=END,
        input_rate="1",
        output_rate="2",
        cached_rate="0.5",
        synthetic=synthetic,
    )
    ledger.authorize(
        authority="mgmt-spend-authority-100",
        owner="mgmt-alert-owner-100",
        evidence="mgmt-synthetic-spend-evidence",
        price=price_id,
        capability="assessment",
        configuration=config_ref,
        start=START,
        end=END,
        max_calls=5,
        max_depth=2,
        budgets=[dict(id=budget_id, calls=100, tokens=100000, amount="50")],
    )
    ledger.billing(
        source="synthetic-bill-100",
        allocation="exact-tag-100",
        budget=budget_id,
        start=START,
        end=END,
        currency="GBP",
        billed=billed_amount,
        tolerance="0.01",
        complete=True,
        synthetic=synthetic,
    )
    return config_ref


def _run_metered_call(
    ledger: Consumption,
    *,
    root_name: str,
    output_id: str,
    config_ref: str,
    accept: bool,
) -> str:
    root = reference(root_name)
    ctx = CallContext(
        root=root,
        attempt=reference(f"{root_name}-attempt-1"),
        capability="assessment",
        case_type="retrofit-case",
        configuration=config_ref,
        prompt=reference("mgmt-prompt-v1"),
    )
    ticket = ledger.reserve(ctx, MODEL, 1000, 100)
    ledger.complete(
        ticket,
        dict(prompt_tokens=100, completion_tokens=20, total_tokens=120, cached_tokens=10),
        MODEL,
        "returned",
    )
    ledger.output(root, output_id, eligible=True)
    if accept:
        ledger.review(output_id, "accept")
    return root


class ManagementTokenomicsInvariantTests(unittest.TestCase):
    """Prove Issue #100 AI consumption economics denominators and Unknown-not-zero rules."""

    def _assert_all_views_satisfy_invariant(
        self,
        store: Any,
        *,
        expect_priced: bool,
        expected_accepted: int,
    ) -> dict[str, dict[str, Any]]:
        actor = _coordinator_actor(store)
        stats_view: dict[str, Any] = store.stats()
        progress_view: dict[str, Any] = store.progress_report(
            actor,
            as_of=AS_OF,
            start=START,
            view="all",
        )
        coord_view: dict[str, Any] = coordinator.read(
            store,
            actor,
            dict(start=START, as_of=AS_OF),
        )
        live_view: dict[str, Any] = store.ai_live_report(
            actor,
            start=START,
            end=END,
            as_of=AS_OF,
        )

        views = {
            "stats": stats_view,
            "progress_report": progress_view,
            "coordinator": coord_view,
            "ai_live_report": live_view,
        }
        for name, payload in views.items():
            with self.subTest(view=name):
                self.assertIn("ai_consumption_economics", payload)
                econ = payload["ai_consumption_economics"]
                tokenomics.assert_tokenomics_invariants(econ)
                self.assertEqual(econ["price_source_configured"], expect_priced)
                self.assertEqual(econ["accepted_outcome_count"], expected_accepted)
                self.assertEqual(
                    econ["denominators"]["accepted_outcome_count"],
                    expected_accepted,
                )
                if not expect_priced:
                    for cost_key in COST_KEYS:
                        self.assertEqual(econ[cost_key], "Unknown")
                        self.assertNotIn(econ[cost_key], (0, 0.0, "0", "0.0", "0.000000"))
                if expected_accepted == 0:
                    for unit_key in UNIT_COST_KEYS:
                        self.assertEqual(econ[unit_key], "Unknown")

        # Verify progress CSV export preserves ai_consumption_economics verbatim
        csv_text: str = progress.export_csv(progress_view)
        rows = {
            row["section"]: json.loads(row["value"])
            for row in csv.DictReader(io.StringIO(csv_text))
            if row["section"] == "ai_consumption_economics"
        }
        self.assertIn("ai_consumption_economics", rows)
        tokenomics.assert_tokenomics_invariants(rows["ai_consumption_economics"])
        return views

    def test_empty_json_store_reports_explicit_zero_denominators_and_unknown_costs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            data = _make_fixture()
            data["recommendations"] = []
            path.write_text(json.dumps(data), encoding="utf-8")
            store_cls: Any = Store
            store = store_cls(path)

            views = self._assert_all_views_satisfy_invariant(
                store,
                expect_priced=False,
                expected_accepted=0,
            )
            econ = views["stats"]["ai_consumption_economics"]
            self.assertEqual(econ["od_51_status"], "open")
            for key in tokenomics.DENOMINATOR_KEYS:
                self.assertEqual(econ[key], 0)
                self.assertEqual(econ["denominators"][key], 0)

    def test_unpriced_store_with_accepted_and_unreviewed_proposals_keeps_costs_unknown(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            data = _make_fixture()
            case_id = data["cases"][0]["id"]
            data["recommendations"] = [
                dict(
                    id="REC-100-A",
                    kind="ai_task",
                    task="briefing",
                    source="ai",
                    status="Accepted",
                    verified=True,
                    case_ids=[case_id],
                    created="2026-10-03T10:00:00Z",
                    resolved_at="2026-10-03T11:00:00Z",
                ),
                dict(
                    id="REC-100-B",
                    kind="ai_task",
                    task="message",
                    source="workflow",
                    fallback_reason="AI off",
                    status="Proposed",
                    verified=True,
                    case_ids=[case_id],
                    created="2026-10-04T10:00:00Z",
                ),
                dict(
                    id="REC-100-UNVERIFIED",
                    kind="ai_task",
                    task="briefing",
                    source="ai",
                    status="Accepted",
                    verified=False,
                    case_ids=[case_id],
                    created="2026-10-05T10:00:00Z",
                    resolved_at="2026-10-05T11:00:00Z",
                ),
            ]
            path.write_text(json.dumps(data), encoding="utf-8")
            store_cls: Any = Store
            store = store_cls(path)

            views = self._assert_all_views_satisfy_invariant(
                store,
                expect_priced=False,
                expected_accepted=1,
            )
            econ = views["stats"]["ai_consumption_economics"]
            self.assertEqual(econ["proposal_count"], 2)
            self.assertEqual(econ["denominators"]["workflow_only_excluded_count"], 1)
            self.assertEqual(econ["accepted_outcome_count"], 1)
            self.assertEqual(econ["metered_call_count"], 0)
            self.assertEqual(econ["unmetered_call_count"], 2)
            self.assertEqual(econ["metered_usage"]["total_tokens"], "Unknown")
            for key in COST_KEYS:
                self.assertEqual(econ[key], "Unknown")

    def test_priced_sql_ledger_with_zero_accepted_outcomes_reports_unknown_per_outcome(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "seed.json"
            db_path = Path(tmp) / "zf.sqlite"
            data = _make_fixture()
            data["recommendations"] = []
            seed.write_text(json.dumps(data), encoding="utf-8")

            sql_cls: Any = SqlStore
            assistants_cls: Any = Assistants
            store = sql_cls(str(seed), str(db_path))
            store.tokenomics_governance = dict(
                od_51_status="approved",
                quality_floor_status="Pass",
                components={k: "0.000010" for k in COMPONENTS},
            )
            assistants = assistants_cls(store)
            assistants.now = lambda _db=None: tokenomics.parse_record_timestamp(
                "2026-10-05T12:00:00Z"
            )
            ledger: Consumption = assistants.consumption

            cfg = _configure_priced_ledger(ledger, config_ref=reference("cfg-zero-accepted"))
            root = _run_metered_call(
                ledger,
                root_name="root-zero-accepted",
                output_id="REC-SQL-PENDING",
                config_ref=cfg,
                accept=False,
            )
            with store.lock:
                store.data["recommendations"].append(
                    dict(
                        id="REC-SQL-PENDING",
                        kind="ai_task",
                        task="briefing",
                        source="ai",
                        status="Not reviewed",
                        verified=True,
                        meter_root=root,
                        case_ids=[data["cases"][0]["id"]],
                        created="2026-10-05T12:00:00Z",
                    )
                )

            views = self._assert_all_views_satisfy_invariant(
                store,
                expect_priced=True,
                expected_accepted=0,
            )
            econ = views["progress_report"]["ai_consumption_economics"]
            self.assertEqual(econ["od_51_status"], "approved")
            self.assertEqual(econ["proposal_count"], 1)
            self.assertEqual(econ["accepted_outcome_count"], 0)
            self.assertEqual(econ["metered_call_count"], 1)
            self.assertEqual(econ["unmetered_call_count"], 0)
            self.assertEqual(econ["token_cost"], "0.000135")
            for unit_key in UNIT_COST_KEYS:
                self.assertEqual(econ[unit_key], "Unknown")

            # If OD-51 remains open despite ledger billing, all costs revert to Unknown
            store.tokenomics_governance = dict(od_51_status="open")
            self._assert_all_views_satisfy_invariant(
                store,
                expect_priced=False,
                expected_accepted=0,
            )

    def test_priced_sql_ledger_with_accepted_outcome_computes_exact_unit_economics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "seed.json"
            db_path = Path(tmp) / "zf.sqlite"
            data = _make_fixture()
            data["recommendations"] = []
            seed.write_text(json.dumps(data), encoding="utf-8")

            sql_cls: Any = SqlStore
            assistants_cls: Any = Assistants
            store = sql_cls(str(seed), str(db_path))
            other_comps = {k: "0.000010" for k in COMPONENTS}
            store.tokenomics_governance = dict(
                od_51_status="approved",
                quality_floor_status="Pass",
                components=other_comps,
            )
            assistants = assistants_cls(store)
            assistants.now = lambda _db=None: tokenomics.parse_record_timestamp(
                "2026-10-06T12:00:00Z"
            )
            ledger: Consumption = assistants.consumption

            cfg = _configure_priced_ledger(
                ledger,
                config_ref=reference("cfg-accepted"),
            )
            root = _run_metered_call(
                ledger,
                root_name="root-accepted",
                output_id="REC-SQL-ACCEPTED",
                config_ref=cfg,
                accept=True,
            )
            with store.lock:
                store.data["recommendations"].append(
                    dict(
                        id="REC-SQL-ACCEPTED",
                        kind="ai_task",
                        task="briefing",
                        source="ai",
                        status="Accepted",
                        verified=True,
                        meter_root=root,
                        case_ids=[data["cases"][0]["id"]],
                        created="2026-10-06T12:00:00Z",
                        resolved_at="2026-10-06T12:05:00Z",
                    )
                )

            views = self._assert_all_views_satisfy_invariant(
                store,
                expect_priced=True,
                expected_accepted=1,
            )
            econ = views["coordinator"]["ai_consumption_economics"]
            self.assertEqual(econ["currency"], "GBP")
            self.assertEqual(econ["proposal_count"], 1)
            self.assertEqual(econ["accepted_outcome_count"], 1)
            self.assertEqual(econ["metered_call_count"], 1)
            self.assertEqual(econ["unmetered_call_count"], 0)
            self.assertEqual(econ["token_cost"], "0.000135")
            self.assertEqual(econ["token_cost_per_accepted_outcome"], "0.000135")
            self.assertEqual(
                econ["quality_qualified_cost_per_accepted_outcome"],
                "0.000135",
            )
            self.assertNotEqual(econ["total_cost_of_ai"], "Unknown")
            self.assertEqual(econ["cost_per_accepted_outcome"], econ["total_cost_of_ai"])
            self.assertEqual(econ["metered_usage"]["total_tokens"], 120)
            self.assertNotIn("tokens_per_home", econ)
            per_home = tokenomics.store_ai_consumption_economics(
                store, start=START, as_of=AS_OF, home_count=4
            )
            self.assertEqual(per_home["tokens_per_home"], "30")
            self.assertEqual(per_home["token_cost_per_home"], "0.00003375")

    def test_mixed_metered_and_unmetered_ai_calls_fail_closed_to_unknown_unit_cost(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "seed.json"
            db_path = Path(tmp) / "zf.sqlite"
            data = _make_fixture()
            data["recommendations"] = []
            seed.write_text(json.dumps(data), encoding="utf-8")

            sql_cls: Any = SqlStore
            assistants_cls: Any = Assistants
            store = sql_cls(str(seed), str(db_path))
            store.tokenomics_governance = dict(
                od_51_status="approved",
                quality_floor_status="Pass",
            )
            assistants = assistants_cls(store)
            assistants.now = lambda _db=None: tokenomics.parse_record_timestamp(
                "2026-10-06T12:00:00Z"
            )
            ledger: Consumption = assistants.consumption

            cfg = _configure_priced_ledger(ledger, config_ref=reference("cfg-mixed"))
            root = _run_metered_call(
                ledger,
                root_name="root-metered-1",
                output_id="REC-METERED",
                config_ref=cfg,
                accept=True,
            )
            case_id = data["cases"][0]["id"]
            with store.lock:
                store.data["recommendations"].extend(
                    [
                        dict(
                            id="REC-METERED",
                            kind="ai_task",
                            task="briefing",
                            source="ai",
                            status="Accepted",
                            verified=True,
                            meter_root=root,
                            case_ids=[case_id],
                            created="2026-10-06T12:00:00Z",
                            resolved_at="2026-10-06T12:05:00Z",
                        ),
                        dict(
                            id="REC-UNMETERED",
                            kind="ai_task",
                            task="message",
                            source="ai",
                            status="Accepted",
                            verified=True,
                            case_ids=[case_id],
                            created="2026-10-06T13:00:00Z",
                            resolved_at="2026-10-06T13:05:00Z",
                        ),
                    ]
                )

            views = self._assert_all_views_satisfy_invariant(
                store,
                expect_priced=False,
                expected_accepted=2,
            )
            econ = views["ai_live_report"]["ai_consumption_economics"]
            self.assertEqual(econ["metered_call_count"], 1)
            self.assertEqual(econ["unmetered_call_count"], 1)
            for key in COST_KEYS:
                self.assertEqual(econ[key], "Unknown")
            self.assertEqual(econ["metered_usage"]["total_tokens"], "Unknown")

    def test_invariant_validator_rejects_numeric_zero_costs_and_direct_helpers_remain_pure(
        self,
    ) -> None:
        summary = tokenomics.summarize_ai_consumption_economics()
        tokenomics.assert_tokenomics_invariants(summary)

        bad_zero_float = copy.deepcopy(summary)
        bad_zero_float["cost_per_accepted_outcome"] = 0.0
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(bad_zero_float)

        bad_zero_str = copy.deepcopy(summary)
        bad_zero_str["token_cost"] = "0.000000"
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(bad_zero_str)

        bad_bool_denom = copy.deepcopy(summary)
        bad_bool_denom["proposal_count"] = True
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(bad_bool_denom)

        data = _make_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "s.json"
            p.write_text(json.dumps(data), encoding="utf-8")
            s_cls: Any = Store
            s = s_cls(p)
            stats_fn: Any = insights.stats
            direct_stats = stats_fn(list(s.cases.values()), s.data["staff"])
            tokenomics.assert_tokenomics_invariants(direct_stats["ai_consumption_economics"])
            direct_report = progress.report(
                list(s.cases.values())[:1],
                as_of=AS_OF,
                start=START,
                cohort=dict(definition_id="SYN-1", label="L", population="P", case_ids=["ZF-1"]),
                scenario=None,
                audit_intact=True,
            )
            tokenomics.assert_tokenomics_invariants(direct_report["ai_consumption_economics"])
            before_audit = len(s.data.get("audit", []))
            live_fn: Any = ai_tasks.live_report
            live = live_fn(s)
            tokenomics.assert_tokenomics_invariants(live["ai_consumption_economics"])
            self.assertEqual(len(s.data.get("audit", [])), before_audit)


if __name__ == "__main__":
    unittest.main()
