"""Exact dependency stale/review-required propagation; synthetic data, no approvals created."""

import copy
import unittest
from typing import Any

import test_form_review
from dataset import change_metadata
from test_form_staging import batch, schema
from zava_forward.core import form_export, form_review, forms


def three() -> dict[str, Any]:
    definition = schema()
    definition["fields"].append(
        dict(
            id="notes",
            section_id="home",
            type="string",
            unit=None,
            options=[],
            required=False,
            required_when=[],
            source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
            evidence_required=["note"],
            calculation_ref=None,
            category="value",
        )
    )
    return definition


def successor(change: Any) -> dict[str, Any]:
    definition = three()
    definition["version"] = 2
    change(definition)
    return definition


def widen_epc(definition: dict[str, Any]) -> None:
    definition["fields"][0]["options"].append("H")


class FormDependencies(unittest.TestCase):
    def setUp(self) -> None:
        self.base = test_form_review.FormReview()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.stores = self.base.stores
        self.actor = self.base.actor

    def setup_reviewed(self, store: Any) -> tuple[Any, dict[str, Any]]:
        draft, epc, area = self.base.prepare(store, three())
        doc = store.add_document(
            self.actor,
            "ZF-1",
            "synthetic.txt",
            "EPC",
            b"N1",
            metadata=change_metadata(store, "ZF-1"),
        )
        request = batch(doc["id"])
        request["candidates"] = [
            dict(field_id="notes", raw_value="N1", locator=dict(start=0, end=2))
        ]
        notes = forms.stage_candidates(store, self.actor, "ZF-1", request)
        draft = self.base.review(store, draft, epc)
        draft = self.base.review(store, draft, area, "area", "correct", 12)
        draft = self.base.review(store, draft, notes, "notes")
        return draft, dict(epc=epc, area=area, notes=notes)

    def view(self, store: Any) -> dict[str, Any]:
        out: dict[str, Any] = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
        return out

    def test_identical_successor_affects_nothing(self) -> None:
        for store in self.stores:
            draft, _ = self.setup_reviewed(store)
            saved = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])
            forms.register_schema(store, self.actor, successor(lambda d: None))
            report = self.view(store)
            self.assertEqual(report["stale_fields"], [])
            self.assertEqual(report["dependency_impact"]["schema"]["status"], "Superseded")
            self.assertFalse(report["dependency_impact"]["schema"]["affects_draft"])
            fresh = form_export.export_freshness(store, self.actor, "ZF-1", saved)
            self.assertEqual(fresh["status"], "Current")

    def test_changed_field_stales_only_it_and_declared_dependents(self) -> None:
        for store in self.stores:
            draft, _ = self.setup_reviewed(store)
            saved = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])
            history = copy.deepcopy(draft["history"])
            forms.register_schema(store, self.actor, successor(widen_epc))
            report = self.view(store)
            causes = report["dependency_impact"]["schema"]["causes"]
            self.assertEqual(
                causes,
                {
                    "area": ["calculation-inputs-undeclared", "condition-depends-on-changed-field"],
                    "epc": ["field-definition-changed"],
                },
            )
            self.assertEqual(report["stale_fields"], ["area", "epc"])
            self.assertEqual(report["fields"]["notes"]["effective_state"], "Accepted")
            self.assertEqual(report["history"], history)
            fresh = form_export.export_freshness(store, self.actor, "ZF-1", saved)
            self.assertEqual(fresh["status"], "Stale")
            self.assertEqual(fresh["stale_fields"], ["area", "epc"])
            self.assertEqual(fresh["unaffected_fields"], ["notes"])
            self.assertFalse(fresh["reviewed"])

    def test_form_wide_reference_change_stays_stale_for_every_field(self) -> None:
        for store in self.stores:
            self.setup_reviewed(store)

            def bump(definition: dict[str, Any]) -> None:
                definition["rule_refs"][0]["version"] = "2"

            forms.register_schema(store, self.actor, successor(bump))
            report = self.view(store)
            self.assertEqual(report["stale_fields"], ["area", "epc", "notes"])
            self.assertEqual(
                report["dependency_impact"]["schema"]["form_wide"], ["rule_refs-changed"]
            )
            self.assertEqual(report["approved_rule_validation"], "Not evaluated")
            self.assertFalse(report["reviewed_ready"])

    def test_malformed_or_missing_lineage_is_unknown_not_unaffected(self) -> None:
        for store in self.stores:
            self.setup_reviewed(store)
            forms.register_schema(store, self.actor, successor(lambda d: None))
            for damage in ("digest", "missing-row"):
                with store.lock:
                    original = copy.deepcopy(store.data["form_schemas"])
                    if damage == "digest":
                        store.data["form_schemas"][1]["digest"] = "0" * 64
                    else:
                        del store.data["form_schemas"][0]
                    store.save()
                report = self.view(store)
                with self.subTest(store=type(store).__name__, damage=damage):
                    self.assertEqual(report["dependency_impact"]["schema"]["status"], "Unknown")
                    self.assertEqual(report["stale_fields"], ["area", "epc", "notes"])
                with store.lock:
                    store.data["form_schemas"] = original
                    store.save()

    def test_proposals_go_stale_only_for_their_changed_source_or_field(self) -> None:
        for store in self.stores:
            draft, staged = self.setup_reviewed(store)
            did = draft["draft_id"]
            states = {
                p["field_id"]: p["state"]
                for p in form_review.proposal_freshness(store, self.actor, "ZF-1", did)["proposals"]
            }
            self.assertEqual(states, {"epc": "Current", "area": "Current", "notes": "Current"})
            with store.lock:
                case = store._case("ZF-1")
                bound = staged["epc"]["source"]["id"]
                next(d for d in case["documents"] if d["id"] == bound)["version"] += 1
                store.save()
            forms.register_schema(
                store, self.actor, successor(lambda d: d["fields"][2].update(unit="note"))
            )
            found = {
                p["field_id"]: p
                for p in form_review.proposal_freshness(store, self.actor, "ZF-1", did)["proposals"]
            }
            self.assertEqual(found["epc"]["causes"], ["source-changed"])
            self.assertEqual(found["notes"]["causes"], ["field-definition-changed"])
            self.assertEqual(found["area"]["causes"], ["calculation-inputs-undeclared"])

    def test_malformed_proposal_linkage_is_unknown(self) -> None:
        for store in self.stores:
            draft, staged = self.setup_reviewed(store)
            with store.lock:
                case = store._case("ZF-1")
                rows = case["form_staging"]
                rows[0]["candidates"].append(dict(id="x1", field_id="ghost", raw_value="G"))
                del rows[1]["source"]
                store.save()
            found = form_review.proposal_freshness(store, self.actor, "ZF-1", draft["draft_id"])
            by_state: dict[str, list[Any]] = {}
            for row in found["proposals"]:
                by_state.setdefault(row["state"], []).append(row)
            self.assertEqual(by_state["Unknown"][0]["causes"], ["field-not-in-schema"])
            self.assertEqual(by_state["Unknown"][1]["causes"], ["proposal-record-malformed"])
            self.assertEqual([r["field_id"] for r in by_state["Current"]], ["epc", "notes"])

    def test_attributable_batch_missing_digest_stays_visible_as_unknown(self) -> None:
        for store in self.stores:
            draft, staged = self.setup_reviewed(store)
            args = (store, self.actor, "ZF-1", draft["draft_id"])
            before = form_review.proposal_freshness(*args)
            with store.lock:
                rows = store._case("ZF-1")["form_staging"]
                del rows[0]["schema_digest"]
                rows[1]["schema_digest"] = "0" * 64
                rows[2]["schema_id"] = "OTHER"
                store.save()
                snapshot = copy.deepcopy(store._case("ZF-1"))
            found = form_review.proposal_freshness(*args)
            with store.lock:
                self.assertEqual(snapshot, store._case("ZF-1"))
            unknown = [r for r in found["proposals"] if r["state"] == "Unknown"]
            self.assertEqual(len(before["proposals"]), 3)
            self.assertEqual(len(found["proposals"]), 1)
            self.assertEqual(
                unknown,
                [
                    dict(
                        batch_id=snapshot["form_staging"][0]["id"],
                        candidate_id=None,
                        field_id=None,
                        state="Unknown",
                        causes=["proposal-record-malformed"],
                    )
                ],
            )

    def hold(self, draft_id: Any, bound: Any, **extra: Any) -> dict[str, Any]:
        return dict(
            decision_id="SYN-APPROVAL",
            draft_id=draft_id,
            status="Recorded",
            owner_role="Finance",
            next_action="None",
            approved_input="SYN",
            approval_evidence="SYN-EVIDENCE",
            bound=bound,
            **extra,
        )

    def test_approval_references_review_only_when_dependent(self) -> None:
        for store in self.stores:
            draft, staged = self.setup_reviewed(store)
            other = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(action="open", schema_id="SYN-TECH", schema_version=1),
            )
            version = draft["input_version"]
            digest = draft["schema_digest"]
            good = dict(schema_digest=digest, input_version=version, field_ids=["epc"])
            with store.lock:
                ledger = store._case("ZF-1")["finance_decision_holds"]
                ledger.append(self.hold(draft["draft_id"], good))
                ledger.append(self.hold(draft["draft_id"], dict(good, field_ids=[])))
                ledger.append(self.hold(draft["draft_id"], None))
                ledger.append(self.hold(other["draft_id"], good))
                ledger.append(None)
                store.save()

            def approvals(store: Any = store, draft: Any = draft) -> list[dict[str, Any]]:
                drafts = form_review.view(store, self.actor, "ZF-1")["drafts"]
                found = next(d for d in drafts if d["draft_id"] == draft["draft_id"])
                out: list[dict[str, Any]] = found["dependency_impact"]["approvals"]
                return out

            first = approvals()
            self.assertEqual(
                [(a["state"], a["causes"]) for a in first],
                [
                    ("Held", []),
                    ("Current", []),
                    ("Review required", ["approval-lineage-malformed"]),
                    ("Review required", ["approval-lineage-malformed"]),
                    ("Review required", ["approval-ledger-malformed"]),
                ],
            )
            reviewed = self.base.review(store, draft, staged["notes"], "notes", "reject")
            self.assertEqual(approvals()[1]["state"], "Current")
            self.base.review(
                store,
                dict(draft, input_version=reviewed["input_version"]),
                staged["epc"],
                "epc",
                "reject",
            )
            changed = approvals()[1]
            self.assertEqual(changed["state"], "Review required")
            self.assertEqual(
                changed["causes"], ["field-issue-open", "field-reviewed-after-approval"]
            )
            self.assertEqual(changed["fields"], ["epc"])
            self.assertEqual(self.view(store)["status"], "Held")

    def test_current_reference_to_a_field_with_an_open_issue_needs_review(self) -> None:
        for store in self.stores:
            draft, _ = self.setup_reviewed(store)
            other = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(action="open", schema_id="SYN-TECH", schema_version=1),
            )

            def ref(d: Any, ids: list[str], name: str, digest: str = draft["schema_digest"]) -> Any:
                bound = dict(schema_digest=digest, input_version=d["input_version"], field_ids=ids)
                return dict(self.hold(d["draft_id"], bound), decision_id=name)

            with store.lock:
                case = store._case("ZF-1")
                case["finance_decision_holds"].extend(
                    [
                        ref(draft, ["notes"], "R-NOTES"),
                        ref(draft, ["area"], "R-AREA"),
                        ref(other, ["epc"], "R-EPC"),
                    ]
                )
                form_reviews = {d["id"]: d for d in case["form_reviews"]}
                form_reviews[draft["draft_id"]]["fields"]["area"]["value"] = "twelve"
                store.save()
                snapshot = copy.deepcopy(store._case("ZF-1"))
            drafts = form_review.view(store, self.actor, "ZF-1")["drafts"]
            with store.lock:
                self.assertEqual(snapshot, store._case("ZF-1"))
            by_id = {
                a["decision_id"]: a for d in drafts for a in d["dependency_impact"]["approvals"]
            }
            self.assertEqual(
                (by_id["R-NOTES"]["state"], by_id["R-NOTES"]["causes"]), ("Current", [])
            )
            self.assertEqual(by_id["R-AREA"]["state"], "Review required")
            self.assertEqual(by_id["R-AREA"]["causes"], ["field-issue-open"])
            self.assertEqual(by_id["R-AREA"]["fields"], ["area"])
            self.assertEqual(by_id["R-EPC"]["state"], "Review required")
            self.assertEqual(by_id["R-EPC"]["causes"], ["field-issue-open"])
            self.assertTrue(
                any(
                    a["state"] == "Held"
                    for d in drafts
                    for a in d["dependency_impact"]["approvals"]
                )
            )

    def test_new_schema_field_needs_review_even_when_no_field_is_stale(self) -> None:
        for store in self.stores:
            draft, _ = self.setup_reviewed(store)
            saved = form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])

            def add(definition: dict[str, Any]) -> None:
                extra = copy.deepcopy(definition["fields"][2])
                extra["id"] = "extra"
                definition["fields"].append(extra)

            forms.register_schema(store, self.actor, successor(add))
            report = self.view(store)
            self.assertEqual(report["stale_fields"], [])
            self.assertEqual(report["dependency_impact"]["schema"]["new_fields"], ["extra"])
            self.assertIn("extra", [i["field_id"] for i in report["issues"]])
            fresh = form_export.export_freshness(store, self.actor, "ZF-1", saved)
            self.assertEqual(fresh["status"], "Stale")
            self.assertEqual(fresh["stale_fields"], [])
            self.assertEqual(fresh["reasons"], ["A newer schema version changes this form."])


if __name__ == "__main__":
    unittest.main()
