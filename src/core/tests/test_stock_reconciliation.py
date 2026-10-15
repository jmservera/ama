"""Synthetic comparison, human sign-off and incomplete support contracts."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from zava_forward.core import ai_tasks, insights, ranking, stock
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import GateError, Store


def query() -> dict[str, Any]:
    """Construct two fictional competing EPC records."""
    return dict(
        field="epc",
        left=dict(
            value="D",
            source_id="SYN-STOCK",
            date="2026-01-01",
            version="1",
            validation_state="Unvalidated",
        ),
        right=dict(
            value="E",
            source_id="SYN-SURVEY",
            date="2026-02-01",
            version="2",
            validation_state="Disputed",
        ),
        query_owner="sam@example.test",
    )


class StockReconciliation(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = copy.deepcopy(dataset.DATA)
        for code, role in (
            ("rc1", "Retrofit Coordinator"),
            ("rc2", "Retrofit Coordinator"),
            ("qi", "Quality Inspector"),
            ("bs", "Building Safety Liaison"),
        ):
            self.data["staff"].append(
                dict(code=code, name=f"Synthetic {code}", email=f"{code}@example.test", role=role)
            )
        self.users = {p["email"].split("@")[0]: p for p in self.data["staff"]}

    def stores(self) -> list[Any]:
        result = []
        for backend in ("json", "sql"):
            folder = Path(self.tmp.name) / backend
            folder.mkdir()
            path = folder / "synthetic.json"
            path.write_text(json.dumps(self.data))
            store = (
                Store(str(path))
                if backend == "json"
                else SqlStore(str(path), str(folder / "state.sqlite"))
            )
            if isinstance(store, SqlStore):
                self.addCleanup(store.db.close)
            result.append(store)
        return result

    def tech(self, store: Any, actor: str, action: str, **body: object) -> None:
        store.technical_action(self.users[actor], "ZF-3", dict(action=action, **body))

    def signed(self, store: Any) -> None:
        self.tech(store, "rc1", "design_submit", note="Synthetic loft design")
        for kind in store.EVIDENCE:
            store.add_document(self.users["sam"], "ZF-3", f"{kind}.pdf", kind, b"%PDF-SYN")
        for actor, kind in (
            ("qi", "assessment"),
            ("rc2", "design"),
            ("bs", "building"),
            ("pam", "coordination"),
        ):
            self.tech(store, actor, "signoff_give", type=kind)

    def test_comparisons_retain_both_sources_owner_history_and_persist(self) -> None:
        for store in self.stores():
            before = store.detail("ZF-3")
            store.stock_reconcile(self.users["sam"], "ZF-3", query())
            store.stock_reconcile(self.users["pam"], "ZF-3", query())
            detail = store.detail("ZF-3")
            rows = detail["stock_reconciliation"]
            self.assertEqual([r["version"] for r in rows], [1, 2])
            self.assertEqual(rows[0]["left"], query()["left"])
            self.assertEqual(rows[0]["right"], query()["right"])
            self.assertEqual(rows[0]["query_owner"]["email"], "sam@example.test")
            for key in ("authority", "resolution", "eligibility"):
                self.assertEqual(rows[0][key], "Unknown")
            for key in ("home", "decision", "owner_code", "stage", "hazards"):
                self.assertEqual(detail[key], before[key])
            reopened = (
                Store(store.live_path)
                if type(store) is Store
                else SqlStore(str(Path(self.tmp.name) / "sql/synthetic.json"), store.db_path)
            )
            if isinstance(reopened, SqlStore):
                self.addCleanup(reopened.db.close)
            self.assertEqual(reopened.detail("ZF-3")["stock_reconciliation"], rows)
            self.assertTrue(reopened.verify_audit())

    def test_invalid_comparisons_are_atomic_and_cannot_bind_forged_identity(self) -> None:
        mutations: list[dict[str, Any]] = [
            {"field": "priority_support"},
            {"query_owner": "missing@example.test"},
            {"left": {"value": "D"}},
            {"right": dict(query()["right"], value="D")},
            {"right": dict(query()["right"], date="2099-01-01")},
            {"right": dict(query()["right"], validation_state="Approved by AI")},
            {"recorded_by": "forged"},
            {"field": ["epc"]},
        ]
        for store in self.stores():
            before = store.detail("ZF-3")
            for mutation in mutations:
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    store.stock_reconcile(self.users["sam"], "ZF-3", dict(query(), **mutation))
                self.assertEqual(store.detail("ZF-3"), before)
            with self.assertRaises(PermissionError):
                store.stock_reconcile(dict(self.users["sam"], role="Contractor"), "ZF-3", query())
            with self.assertRaises(PermissionError):
                store.stock_reconcile(dict(self.users["sam"], name="Forged"), "ZF-3", query())
            self.assertFalse(list(store.audit_entries()))

    def test_conflict_holds_without_design_but_never_blocks_hazard_intake(self) -> None:
        for store in self.stores():
            store.stock_reconcile(self.users["sam"], "ZF-3", query())
            self.assertIn("Sam Example", " ".join(store.detail("ZF-3")["gate"]))
            with self.assertRaises(GateError):
                store.advance(self.users["pam"], "ZF-3")
            store.raise_hazard(
                self.users["sam"],
                "ZF-3",
                "Electrical",
                "Emergency",
                "Synthetic report",
                metadata=dict(source="SYN-REPORT", aware_at="2026-01-01T10:00:00Z"),
            )
            self.assertEqual(len(store.detail("ZF-3")["hazards"]), 1)
            self.assertEqual(store.detail("ZF-2")["stock_reconciliation"], [])

    def test_later_conflict_preserves_signed_history_but_blocks_further_approval(self) -> None:
        for store in self.stores():
            self.signed(store)
            before = store.detail("ZF-3")["technical"]
            store.stock_reconcile(self.users["sam"], "ZF-3", query())
            with self.assertRaises(GateError):
                self.tech(store, "bs", "signoff_give", type="building")
            with self.assertRaises(GateError):
                store.advance(self.users["pam"], "ZF-3")
            self.assertEqual(store.detail("ZF-3")["technical"], before)

    def test_four_human_signoffs_and_only_affected_reassessment(self) -> None:
        for store in self.stores():
            self.signed(store)
            before = store.detail("ZF-3")["technical"]
            self.assertEqual(len({s["by_email"] for s in before["signoffs"].values()}), 4)
            self.tech(
                store,
                "rc1",
                "design_change",
                note="Synthetic wall change",
                affects=["design", "building"],
            )
            changed = store.detail("ZF-3")["technical"]
            for key in ("assessment", "coordination"):
                self.assertEqual(changed["signoffs"][key], before["signoffs"][key])
            for key in ("design", "building"):
                self.assertEqual(changed["signoffs"][key]["status"], "Needs reassessment")
                self.assertEqual(changed["signoffs"][key]["history"][-1]["version"], 2)
            self.tech(store, "rc2", "signoff_give", type="design")
            signed = store.detail("ZF-3")["technical"]["signoffs"]["design"]
            self.assertEqual(signed["version"], 2)
            self.assertEqual(signed["history"][-1]["by_email"], "rc2@example.test")

    def test_bad_technical_input_and_agent_identity_never_mutate(self) -> None:
        for store in self.stores():
            self.tech(store, "rc1", "design_submit", note="SYN")
            before = store.detail("ZF-3")
            invalid_affects: list[object] = [
                [],
                None,
                "design",
                ["design", "design"],
                ["assessment"],
                [{}],
            ]
            for affects in invalid_affects:
                with self.subTest(affects=affects), self.assertRaises(ValueError):
                    self.tech(store, "rc1", "design_change", note="SYN", affects=affects)
                self.assertEqual(store.detail("ZF-3"), before)
            with self.assertRaises(ValueError):
                self.tech(store, "qi", "signoff_give", type="assessment", note=["bad"])
            for actor in (
                dict(self.users["qi"], email="agent@example.test"),
                dict(self.users["qi"], name="Forged professional"),
                dict(self.users["qi"], role="Retrofit Coordinator"),
            ):
                with self.assertRaises(PermissionError):
                    store.technical_action(
                        actor, "ZF-3", dict(action="signoff_give", type="assessment")
                    )
            self.assertEqual(store.detail("ZF-3"), before)

    def test_building_and_hazard_checks_are_reused(self) -> None:
        for store in self.stores():
            self.tech(store, "rc1", "design_submit", note="SYN")
            with store.lock:
                store._case("ZF-3")["building_id"] = "SYN-MISSING-BUILDING"
                store.save()
            with self.assertRaises(GateError):
                self.tech(store, "bs", "signoff_give", type="building")
            store.technical_action(
                self.users["rc1"], "ZF-4", dict(action="design_submit", note="SYN")
            )
            with self.assertRaises(GateError):
                store.technical_action(
                    self.users["bs"], "ZF-4", dict(action="signoff_give", type="building")
                )

    def test_support_truth_table_and_coverage(self) -> None:
        for resident, status, coverage in (
            ({}, "Unknown", "Unknown"),
            ({"priority_support": None}, "Unknown", "Unknown"),
            ({"priority_support": False}, "Unknown", "Unknown"),
            ({"adjustment": "None"}, "Unknown", "Unknown"),
            ({"priority_support": False, "adjustment": None}, "Unknown", "Unknown"),
            ({"priority_support": False, "adjustment": "None"}, "No", "Recorded"),
            ({"priority_support": True}, "Yes", "Unknown"),
            ({"priority_support": None, "adjustment": "Phone only"}, "Yes", "Unknown"),
            ({"priority_support": True, "adjustment": "None"}, "Yes", "Recorded"),
            ({"priority_support": "Unknown", "adjustment": "Unknown"}, "Unknown", "Unknown"),
        ):
            with self.subTest(resident=resident):
                self.assertEqual(stock.support_status(resident), status)
                self.assertEqual(stock.support_coverage(resident), coverage)

    def test_missing_support_keeps_homes_in_ranking_views_and_ai_facts(self) -> None:
        self.data["cases"][0]["resident"].pop("priority_support")
        self.data["cases"][0]["resident"]["adjustment"] = None
        for store in self.stores():
            case = store.detail("ZF-1")
            self.assertEqual(case["support_status"], "Unknown")
            self.assertEqual(case["support_coverage"], "Unknown")
            row = next(r for r in store.list_cases(self.users["pam"], "all") if r["id"] == "ZF-1")
            self.assertEqual(row["support_status"], "Unknown")
            self.assertIs(row["support"], False)
            self.assertIn("Support flags unknown; human review needed", row["reasons"])
            self.assertEqual(store.stats()["kpis"]["support_unknown"], 1)
            self.assertIn("Extra support: Unknown", ai_tasks.source_labels(case))
            self.assertNotIn("Extra support: needed", ai_tasks.source_labels(case))
            self.assertIn("Resident adjustments: Unknown", store._facts(case))
            self.assertEqual(insights.matches(case, {"flag": "support"}), False)
            self.assertEqual(
                store.detail("ZF-1", self.users["rc1"])["resident"]["adjustment"], "Unknown"
            )
        known = copy.deepcopy(self.data["cases"])
        missing = known[0]
        missing["days_in_stage"] = 100
        entries = ranking.rank(known)
        self.assertEqual(entries[0]["id"], "ZF-4")  # independent safety factor
        self.assertEqual(entries[1]["id"], "ZF-1")  # independent waiting factor
        self.assertEqual(
            [e["id"] for e in entries], [c["id"] for c in sorted(known, key=ranking.sql_key)]
        )

    def test_existing_sql_encoding_refresh_is_idempotent_and_preserves_history(self) -> None:
        self.data["cases"][0]["resident"]["adjustment"] = None
        json_store, sql = self.stores()
        json_store.stock_reconcile(self.users["sam"], "ZF-3", query())
        sql.stock_reconcile(self.users["sam"], "ZF-3", query())
        before = list(sql.audit_entries())
        sql.db.execute("DELETE FROM meta WHERE key='support_encoding'")
        sql.db.execute("UPDATE cases SET support=1, rkey='OLD' WHERE id='ZF-1'")
        for _ in range(2):
            reopened = SqlStore(str(Path(self.tmp.name) / "sql/synthetic.json"), sql.db_path)
            self.addCleanup(reopened.db.close)
            row = reopened.db.execute("SELECT support, rkey FROM cases WHERE id='ZF-1'").fetchone()
            self.assertEqual(tuple(row), (0, ranking.sql_key(self.data["cases"][0])))
            self.assertEqual(list(reopened.audit_entries()), before)
            self.assertEqual(
                reopened.db.execute(
                    "SELECT value FROM meta WHERE key='support_encoding'"
                ).fetchone()[0],
                "1",
            )
            self.assertEqual(len(reopened.detail("ZF-3")["stock_reconciliation"]), 1)
            self.assertEqual(
                reopened.list_cases(self.users["pam"], "all"),
                json_store.list_cases(self.users["pam"], "all"),
            )
            first = json_store.page_cases(self.users["pam"], "all", limit=2)
            self.assertEqual(reopened.page_cases(self.users["pam"], "all", limit=2), first)
            self.assertEqual(
                reopened.page_cases(self.users["pam"], "all", limit=2, after=first["next_cursor"]),
                json_store.page_cases(
                    self.users["pam"], "all", limit=2, after=first["next_cursor"]
                ),
            )
            self.assertNotIn(
                "ZF-1",
                [
                    r["id"]
                    for r in reopened.list_cases(
                        self.users["pam"], "all", filters={"flag": "support"}
                    )
                ],
            )
