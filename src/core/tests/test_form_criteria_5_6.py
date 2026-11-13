"""Issue 96 criteria 5 and 6 end to end on synthetic data: a reviewed export never
submits or implies eligibility, and a source, schema or rule change marks only the
dependent proposals and approvals stale. No approval is created or implied."""

import copy
import json
import unittest
from typing import Any

import test_form_dependencies as deps
from zava_forward.core import form_export, form_review, forms

CLAIMS = ("submitted", "eligible", "approved", "award", "payment", "reviewed_ready")


class Criteria(unittest.TestCase):
    def setUp(self) -> None:
        self.base = deps.FormDependencies()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.stores = self.base.stores
        self.actor = self.base.actor

    def world(self, store: Any) -> str:
        with store.lock:
            return json.dumps(
                [store.data, store._case("ZF-1"), getattr(store, "audit_log", None)],
                sort_keys=True,
                default=str,
            )

    def approve(self, store: Any, draft: Any, **fields: str) -> None:
        with store.lock:
            ledger = store._case("ZF-1")["finance_decision_holds"]
            for name, field in fields.items():
                bound = dict(
                    schema_digest=draft["schema_digest"],
                    input_version=draft["input_version"],
                    field_ids=[field],
                )
                ledger.append(dict(self.base.hold(draft["draft_id"], bound), decision_id=name))
            store.save()

    def states(self, store: Any, draft: Any) -> dict[str, Any]:
        report = self.base.view(store)
        proposals = form_review.proposal_freshness(store, self.actor, "ZF-1", draft["draft_id"])
        saved = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])
        return dict(
            stale=report["stale_fields"],
            proposals={p["field_id"]: p["state"] for p in proposals["proposals"]},
            approvals={
                a["decision_id"]: (a["state"], a["fields"])
                for a in report["dependency_impact"]["approvals"]
                if a["decision_id"] != "template-rules"
            },
            export=saved,
        )

    def test_reviewed_export_never_submits_or_implies_eligibility(self) -> None:
        for store in self.stores:
            draft, _ = self.base.setup_reviewed(store)
            self.approve(store, draft, a="epc", b="area", c="notes")
            before = self.world(store)
            report = self.base.view(store)
            self.assertEqual(
                [report["fields"][f]["effective_state"] for f in ("epc", "area", "notes")],
                ["Accepted", "Corrected", "Accepted"],
            )
            out = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])
            saved = copy.deepcopy(out)
            form_export.export_freshness(store, self.actor, "ZF-1", saved)
            form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])
            with self.subTest(store=type(store).__name__):
                self.assertEqual(self.world(store), before)
                self.assertEqual(
                    (out["status"], out["reviewed"], out["submission"], out["eligibility"]),
                    ("Held", False, "Not submitted", "Not assessed"),
                )
                for claim in CLAIMS:
                    self.assertNotIn(claim, out)
                for words in ("not a reviewed", "does not submit", "eligibility"):
                    self.assertIn(words, out["notice"])
                self.assertFalse(report["reviewed_ready"])
                self.assertEqual(report["status"], "Held")
                self.assertEqual(out["content_sha256"], saved["content_sha256"])

    def test_source_change_marks_only_declared_dependents(self) -> None:
        for store in self.stores:
            draft, staged = self.base.setup_reviewed(store)
            self.approve(store, draft, a="epc", b="notes", c="area")
            before = self.states(store, draft)
            documents = copy.deepcopy(store._case("ZF-1")["documents"])
            saved = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])
            with store.lock:
                bound = staged["epc"]["source"]["id"]
                next(d for d in store._case("ZF-1")["documents"] if d["id"] == bound)[
                    "version"
                ] += 1
                store.save()
            now = self.states(store, draft)
            with self.subTest(store=type(store).__name__):
                self.assertEqual(before["stale"], [])
                self.assertEqual(before["approvals"]["a"], ("Current", []))
                self.assertEqual(before["approvals"]["b"], ("Current", []))
                self.assertEqual(now["stale"], ["epc"])
                self.assertEqual(
                    now["proposals"], {"epc": "Stale", "area": "Current", "notes": "Current"}
                )
                self.assertEqual(now["approvals"]["a"], ("Review required", ["epc"]))
                self.assertEqual(now["approvals"]["b"], ("Current", []))
                fresh = form_export.export_freshness(store, self.actor, "ZF-1", saved)
                self.assertEqual(now["approvals"]["c"], ("Review required", ["area"]))
                self.assertEqual(fresh["stale_fields"], ["area", "epc"])
                self.assertEqual(fresh["unaffected_fields"], ["notes"])
                self.assertEqual(self.base.view(store)["fields"]["notes"]["state"], "Accepted")
                others = [d for d in store._case("ZF-1")["documents"] if d["id"] != bound]
                self.assertEqual(others, [d for d in documents if d["id"] != bound])

    def test_rule_change_on_one_field_marks_only_that_field(self) -> None:
        for store in self.stores:
            draft, _ = self.base.setup_reviewed(store)
            self.approve(store, draft, a="epc", b="area", c="notes")
            before = self.states(store, draft)
            saved = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])

            def recalculate(definition: dict[str, Any]) -> None:
                definition["fields"][1]["calculation_ref"]["version"] = "2"

            forms.register_schema(store, self.actor, deps.successor(recalculate))
            now = self.states(store, draft)
            with self.subTest(store=type(store).__name__):
                self.assertEqual(before["stale"], [])
                self.assertEqual(before["approvals"]["a"], ("Current", []))
                self.assertEqual(before["approvals"]["c"], ("Current", []))
                self.assertEqual(now["stale"], ["area"])
                self.assertEqual(
                    now["proposals"], {"epc": "Current", "area": "Stale", "notes": "Current"}
                )
                self.assertEqual(now["approvals"]["a"], ("Current", []))
                self.assertEqual(now["approvals"]["b"], ("Review required", ["area"]))
                self.assertEqual(now["approvals"]["c"], ("Current", []))
                fresh = form_export.export_freshness(store, self.actor, "ZF-1", saved)
                self.assertEqual(fresh["stale_fields"], ["area"])
                self.assertEqual(fresh["unaffected_fields"], ["epc", "notes"])

    def test_schema_change_marks_only_dependents_of_the_changed_field(self) -> None:
        for store in self.stores:
            draft, _ = self.base.setup_reviewed(store)
            self.approve(store, draft, a="epc", b="area", c="notes")
            before = self.states(store, draft)
            forms.register_schema(
                store, self.actor, deps.successor(lambda d: d["fields"][2].update(unit="note"))
            )
            now = self.states(store, draft)
            impact = self.base.view(store)["dependency_impact"]["schema"]["causes"]
            with self.subTest(store=type(store).__name__):
                self.assertEqual(before["stale"], [])
                self.assertEqual(before["approvals"]["c"], ("Current", []))
                self.assertEqual(impact["notes"], ["field-definition-changed"])
                self.assertEqual(impact["area"], ["calculation-inputs-undeclared"])
                self.assertNotIn("epc", impact)
                self.assertEqual(now["stale"], ["area", "notes"])
                self.assertEqual(now["approvals"]["a"], ("Current", []))
                self.assertEqual(now["approvals"]["b"], ("Review required", ["area"]))
                self.assertEqual(now["approvals"]["c"], ("Review required", ["notes"]))
