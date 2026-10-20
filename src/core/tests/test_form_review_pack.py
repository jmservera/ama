"""Review-pack data integrity for the fictional form template; no approval or runtime behaviour."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from zava_forward.core import forms
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.synthetic import privacy

ROOT = Path(__file__).resolve().parents[3]
PACK = json.loads((ROOT / "src/core/evals/fictional_form_review_pack.json").read_text())
UNRESOLVED = "Unresolved - Finance to supply"


class FictionalFormReviewPack(unittest.TestCase):
    def stores(self) -> list[Any]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        result: list[Any] = []
        for kind in ("json", "sql"):
            folder = Path(tmp.name) / kind
            folder.mkdir()
            seed = folder / "synthetic.json"
            seed.write_text(json.dumps(copy.deepcopy(dataset.DATA)))
            store: Any = (
                Store(str(seed))  # type: ignore[no-untyped-call]
                if kind == "json"
                else SqlStore(str(seed), str(folder / "s.sqlite"))  # type: ignore[no-untyped-call]
            )
            if kind == "sql":
                self.addCleanup(store.db.close)
            result.append(store)
        return result

    def test_schema_registers_only_with_substituted_reviewer_and_stays_unapproved(self) -> None:
        actor = dict(dataset.DATA["staff"][1])
        request = copy.deepcopy(PACK["schema"])
        request["reviewer"] = actor["email"]
        differing = {k for k in request if request[k] != PACK["schema"][k]}
        self.assertEqual(differing, {"reviewer"})
        for store in self.stores():
            with self.assertRaises(ValueError):
                forms.register_schema(store, actor, copy.deepcopy(PACK["schema"]))
            row = forms.register_schema(store, actor, request)
            self.assertEqual(row["definition"], request)
            self.assertEqual(row["approval"], "Unapproved")
            self.assertIsNone(row["approval_evidence"])
            self.assertEqual(row["definition"]["funding"]["status"], "Unknown")

    def test_review_table_and_declared_references_match_schema(self) -> None:
        fields = {f["id"]: f for f in PACK["schema"]["fields"]}
        review = [r["field_id"] for r in PACK["field_review"]]
        self.assertEqual(sorted(review), sorted(fields))
        self.assertEqual({f["type"] for f in fields.values()}, set(forms.TYPES))
        self.assertTrue({"GBP", "m2", "kWh/m2/year"} <= {f["unit"] for f in fields.values()})
        self.assertTrue(any(f["required_when"] for f in fields.values()))
        for row in PACK["field_review"]:
            field = fields[row["field_id"]]
            human = field["category"] in forms.HUMAN_ONLY
            self.assertEqual(row["freshness"]["max_source_age_days"] is None, human)
        calcs = {c["id"]: c for c in PACK["calculations"]}
        refs = {f["calculation_ref"]["id"] for f in fields.values() if f["calculation_ref"]}
        self.assertEqual(refs, set(calcs))
        for calc in calcs.values():
            self.assertLessEqual(set(calc["inputs"]), set(fields))
            self.assertTrue(calc["status"].startswith("Unresolved"))
        self.assertEqual(PACK["schema"]["template"]["id"], PACK["template"]["id"])
        self.assertEqual(PACK["schema"]["template"]["version"], PACK["template"]["version"])
        humans = [f for f in fields.values() if f["category"] in forms.HUMAN_ONLY]
        self.assertEqual({f["category"] for f in humans}, {"declaration", "signature", "approval"})

    def test_stale_map_is_exhaustive_disjoint_and_calculation_consistent(self) -> None:
        fields = {f["id"] for f in PACK["schema"]["fields"]}
        calcs = {c["id"]: set(c["inputs"]) for c in PACK["calculations"]}
        for trigger in PACK["stale_propagation"]["triggers"]:
            affected = set(trigger["affected_fields"])
            unaffected = set(trigger["unaffected_fields"])
            self.assertEqual(affected | unaffected, fields, trigger["id"])
            self.assertFalse(affected & unaffected, trigger["id"])
            self.assertEqual(
                {cid for cid, inputs in calcs.items() if inputs & affected},
                set(trigger["affected_calculations"]),
                trigger["id"],
            )
        self.assertIn("Proposed control", PACK["stale_propagation"]["status"])

    def test_every_field_stale_trigger_maps_to_a_trigger_listing_it(self) -> None:
        triggers = {t["id"]: t for t in PACK["stale_propagation"]["triggers"]}
        for row in PACK["field_review"]:
            fid = row["field_id"]
            expected = {tid for tid, t in triggers.items() if fid in t["affected_fields"]}
            self.assertEqual(set(row["freshness"]["stale_triggers"]), expected, fid)
        aged = {
            r["field_id"] for r in PACK["field_review"] if r["freshness"]["max_source_age_days"]
        }
        self.assertEqual(set(triggers["ST-SOURCE-AGE-EXPIRY"]["affected_fields"]), aged)

    def test_lineage_and_human_only_refusal_match_the_staging_contract(self) -> None:
        actor = dict(dataset.DATA["staff"][1])
        request = copy.deepcopy(PACK["schema"])
        request["reviewer"] = actor["email"]
        processing = dict(
            kind="text",
            parser="SYN-importer",
            parser_version="test-1",
            model_version=None,
            route_evidence=None,
            error_record=None,
        )
        for store in self.stores():
            forms.register_schema(store, actor, copy.deepcopy(request))
            doc = store.add_document(
                actor, "ZF-1", "synthetic.txt", "EPC", b"EPC band D\n",
                metadata=dataset.change_metadata(store, "ZF-1"),
            )  # fmt: skip
            base = dict(
                schema_id=request["id"],
                schema_version=request["version"],
                document_id=doc["id"],
                processing=processing,
            )
            for human in ("applicant_declaration", "authorised_signature", "finance_approval"):
                refused = dict(
                    base,
                    candidates=[dict(field_id=human, raw_value="x", locator=dict(start=0, end=1))],
                )
                with self.assertRaises(PermissionError):
                    forms.stage_candidates(store, actor, "ZF-1", refused)
            ok = dict(
                base,
                candidates=[
                    dict(field_id="epc_band", raw_value="D", locator=dict(start=9, end=10))
                ],
            )
            saved = forms.stage_candidates(store, actor, "ZF-1", ok)
            self.assertEqual(set(saved["processing"]), set(processing) | {"assertion_status"})
            lineage = PACK["lineage_expectations"]
            self.assertEqual(saved["processing"]["assertion_status"], lineage["assertion_status"])
            for key in ("parser", "parser_version", "route_evidence", "error_record"):
                self.assertIn(key, lineage["recorded"])
            self.assertEqual(saved["verification"]["status"], "Exact source match")

    def test_authority_and_binding_decisions_are_unresolved_and_unsigned(self) -> None:
        decisions = PACK["finance_decisions"]
        names = {d["field"] for d in decisions}
        self.assertTrue(
            {
                "authority_holder",
                "scheme_and_route",
                "signature",
                "approval_date",
                "binding_statement",
                "approver_decision",
            }
            <= names
        )
        for decision in decisions:
            self.assertIsNone(decision["value"], decision["id"])
            self.assertEqual(decision["status"], UNRESOLVED)
            self.assertEqual(
                set(decision),
                {"id", "value", "status", "field", "question", "owner_role", "evidence_needed"},
            )
        self.assertEqual(PACK["finance_decision_status"], UNRESOLVED)
        self.assertEqual(PACK["status"].split(" - ")[0], "NOT APPROVED")
        self.assertTrue(PACK["template"]["approval_status"].startswith("NOT APPROVED"))
        self.assertIsNone(PACK["template"]["effective_from"])
        self.assertEqual(
            PACK["schema"]["funding"],
            dict(status="Unknown", scheme_id=None, route=None, evidence_ref=None),
        )
        text = " ".join(PACK["statements"])
        for phrase in (
            "not a real",
            "Unapproved",
            "No Finance",
            "criterion 1 remains unmet",
            "no payment",
            "Nothing here is submitted",
            "fictional proposals pending Finance decisions FD-07 and FD-09",
        ):
            self.assertIn(phrase, text)
        for phrase in ("NOT an approved template", "No submission", "no payment"):
            self.assertIn(phrase, PACK["label"])
        self.assertIn("Unresolved", PACK["roles"]["approver"]["status"])
        self.assertIn("criterion 1", PACK["unmet_authority"])

    def test_roles_are_separate_and_separation_is_proposed(self) -> None:
        roles = PACK["roles"]
        self.assertEqual(len({roles[r]["role"] for r in ("preparer", "reviewer", "approver")}), 3)
        self.assertIn("review own preparation", roles["preparer"]["may_not"])
        self.assertIn("Not enforced", roles["separation_rule"])

    def test_public_payload_is_registered_and_passes_privacy_checks(self) -> None:
        self.assertEqual(privacy.public_issues(ROOT), [])
        register = json.loads((ROOT / privacy.PACK / "provenance-register.json").read_text())
        entry = next(d for d in register["datasets"] if d["id"] == "DS-FICT-FORM-REVIEW-PACK")
        self.assertEqual(entry["visibility"], "public")
        self.assertEqual(entry["location"], "src/core/evals/fictional_form_review_pack.json")


if __name__ == "__main__":
    unittest.main()
