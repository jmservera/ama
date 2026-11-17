"""Issue #98 deterministic approved-rule validation, versioned packs, and stale propagation."""

import copy
import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

_SRC = str(Path(__file__).resolve().parents[1] / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import dataset  # noqa: E402
import test_form_review  # noqa: E402
from dataset import change_metadata  # noqa: E402
from test_form_staging import batch  # noqa: E402
from zava_forward.core import form_review, form_validation, forms  # noqa: E402


def rich_schema(
    *,
    version: int = 1,
    form_type: str = "funding",
    funding_status: str = "Evidenced",
    include_human_only: bool = False,
) -> dict[str, Any]:
    funding: dict[str, Any] = (
        dict(
            status="Evidenced",
            scheme_id="SYN-SCHEME",
            route="claim",
            evidence_ref="SYN-FUND-ROUTE",
        )
        if form_type == "funding" and funding_status == "Evidenced"
        else dict(status="Unknown", scheme_id=None, route=None, evidence_ref=None)
        if form_type == "funding"
        else dict(status="Not applicable", scheme_id=None, route=None, evidence_ref=None)
    )
    fields: list[dict[str, Any]] = [
        dict(
            id="epc",
            section_id="home",
            type="enum",
            unit=None,
            options=list("ABCDEFG"),
            required=True,
            required_when=[],
            source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
            evidence_required=["certificate"],
            calculation_ref=None,
            category="value",
        ),
        dict(
            id="ground_area",
            section_id="home",
            type="number",
            unit="m2",
            options=[],
            required=True,
            required_when=[],
            source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
            evidence_required=["survey"],
            calculation_ref=None,
            category="value",
        ),
        dict(
            id="upper_area",
            section_id="home",
            type="number",
            unit="m2",
            options=[],
            required=True,
            required_when=[],
            source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
            evidence_required=["survey"],
            calculation_ref=None,
            category="value",
        ),
        dict(
            id="area",
            section_id="home",
            type="number",
            unit="m2",
            options=[],
            required=True,
            required_when=[],
            source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
            evidence_required=["survey"],
            calculation_ref=dict(id="SYN-CALC", version="1", evidence_ref="SYN-FORMULA"),
            category="value",
        ),
        dict(
            id="notes",
            section_id="home",
            type="string",
            unit=None,
            options=[],
            required=False,
            required_when=[dict(field_id="epc", equals="D")],
            source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
            evidence_required=["record"],
            calculation_ref=None,
            category="value",
        ),
    ]
    if include_human_only:
        fields.append(
            dict(
                id="signoff",
                section_id="governance",
                type="string",
                unit=None,
                options=[],
                required=False,
                required_when=[],
                source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
                evidence_required=["record"],
                calculation_ref=None,
                category="approval",
            )
        )
    return dict(
        id="SYN-TECH",
        version=version,
        form_type=form_type,
        template=dict(id="SYN-TEMPLATE", version="1", evidence_ref="SYN-TMPL-REF"),
        reviewer="pam@example.test",
        funding=funding,
        rule_refs=[dict(id="SYN-RULE", version="1", evidence_ref="SYN-RULE-SOURCE")],
        fields=fields,
    )


def make_rules(
    draft: dict[str, Any],
    *,
    rule_set_id: str = "SYN-RULE",
    rule_set_version: str = "1",
    approved: bool = True,
    include_sum: bool = True,
    ground_min: int | float = 10,
    epc_options: list[str] | None = None,
) -> dict[str, Any]:
    rules: list[dict[str, Any]] = [
        dict(
            rule_id="R-EPC",
            field_id="epc",
            kind="one_of",
            param=epc_options if epc_options is not None else ["C", "D", "E"],
            message="EPC band must be C, D, or E.",
        ),
        dict(
            rule_id="R-GROUND-MIN",
            field_id="ground_area",
            kind="min",
            param=ground_min,
            message="Ground area is below minimum threshold.",
        ),
        dict(
            rule_id="R-UPPER-MAX",
            field_id="upper_area",
            kind="max",
            param=200,
            message="Upper area exceeds maximum threshold.",
        ),
        dict(
            rule_id="R-NOTES-LEN",
            field_id="notes",
            kind="max_length",
            param=20,
            message="Notes exceed 20 characters.",
        ),
        dict(
            rule_id="R-NOTES-PAT",
            field_id="notes",
            kind="pattern",
            param=r"[a-z0-9 -]+",
            message="Notes contain disallowed characters.",
        ),
    ]
    if include_sum:
        rules.append(
            dict(
                rule_id="R-AREA-SUM",
                field_id="area",
                kind="sum",
                param=dict(
                    calc_id="SYN-CALC",
                    calc_version="1",
                    addends=["ground_area", "upper_area"],
                ),
                message="Total area must equal ground_area plus upper_area.",
            )
        )
    approval: dict[str, Any] = (
        dict(status="Approved", approver="fin-lead@example.test", evidence_ref="SYN-RULE-APP-1")
        if approved
        else dict(status="Unapproved", approver=None, evidence_ref=None)
    )
    return dict(
        id=rule_set_id,
        version=rule_set_version,
        approval=approval,
        bound=dict(
            schema_id=draft["schema_id"],
            schema_version=draft["schema_version"],
            schema_digest=draft["schema_digest"],
            template_id=draft["template"]["id"],
            template_version=draft["template"]["version"],
        ),
        rules=rules,
    )


class Issue98FieldValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = test_form_review.FormReview()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.stores = self.base.stores
        self.actor = self.base.actor

    def approve_registered_schema(
        self,
        store: Any,
        *,
        schema_id: str = "SYN-TECH",
        version: int = 1,
        schema_approved: bool = True,
        policy_approved: bool = True,
    ) -> None:
        """Test-only fixture mutation simulating external Finance/template-owner sign-off."""
        with store.lock:
            for row in store.data["form_schemas"]:
                if row["definition"]["id"] == schema_id and row["definition"]["version"] == version:
                    row["approval"] = "Approved" if schema_approved else "Unapproved"
                    row["approval_evidence"] = "SYN-SCHEMA-APP-1" if schema_approved else None
                    row["source_policy_status"] = "Approved" if policy_approved else "Unapproved"
            store.save()

    def stage_doc(
        self, store: Any, pairs: list[tuple[str, str]], filename: str = "survey.txt"
    ) -> tuple[Any, Any]:
        lines = [f"{fid}={raw}" for fid, raw in pairs]
        text = "\n".join(lines)
        doc = store.add_document(
            self.actor,
            "ZF-1",
            filename,
            "EPC",
            text.encode(),
            metadata=change_metadata(store, "ZF-1"),
        )
        req = batch(doc["id"])
        candidates = []
        offset = 0
        for fid, raw in pairs:
            prefix = f"{fid}="
            start = offset + len(prefix)
            end = start + len(raw)
            candidates.append(dict(field_id=fid, raw_value=raw, locator=dict(start=start, end=end)))
            offset = end + 1
        req["candidates"] = candidates
        staged = forms.stage_candidates(store, self.actor, "ZF-1", req)
        return doc, staged

    def setup_rich_draft(
        self,
        store: Any,
        *,
        definition: dict[str, Any] | None = None,
        approve_schema: bool = True,
    ) -> tuple[Any, Any, Any, Any, Any]:
        forms.register_schema(store, self.actor, definition or rich_schema())
        if approve_schema:
            self.approve_registered_schema(store)
        doc1, staged1 = self.stage_doc(
            store,
            [("epc", "D"), ("ground_area", "12.1"), ("notes", "loft ok")],
            filename="epc-cert.txt",
        )
        doc2, staged2 = self.stage_doc(
            store,
            [("upper_area", "17.2"), ("area", "29.3")],
            filename="floor-plan.txt",
        )
        draft = form_review.action(
            store,
            self.actor,
            "ZF-1",
            dict(action="open", schema_id="SYN-TECH", schema_version=1),
        )
        return draft, doc1, staged1, doc2, staged2

    def accept_candidate(
        self,
        store: Any,
        draft: Any,
        staged: Any,
        field_id: str,
        value: Any,
        *,
        decision: str = "correct",
    ) -> Any:
        cand = next(c for c in staged["candidates"] if c["field_id"] == field_id)
        payload: dict[str, Any] = dict(
            action="review",
            draft_id=draft["draft_id"],
            expected_version=draft["input_version"],
            field_id=field_id,
            decision=decision,
            batch_id=staged["id"],
            candidate_id=cand["id"],
            value=value if decision == "correct" else None,
            reason="SYN explicit reviewer note",
        )
        return form_review.action(store, self.actor, "ZF-1", payload)

    def confirm_all_rich(self, store: Any, draft: Any, staged1: Any, staged2: Any) -> Any:
        draft = self.accept_candidate(store, draft, staged1, "epc", "D", decision="accept")
        draft = self.accept_candidate(store, draft, staged1, "ground_area", 12.1)
        draft = self.accept_candidate(store, draft, staged1, "notes", "loft ok", decision="accept")
        draft = self.accept_candidate(store, draft, staged2, "upper_area", 17.2)
        draft = self.accept_candidate(store, draft, staged2, "area", 29.3)
        return draft

    def test_unapproved_or_unbound_authorities_return_not_evaluated_and_held_pack(self) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, _d1, s1, _d2, s2 = self.setup_rich_draft(store, approve_schema=False)
                draft = self.confirm_all_rich(store, draft, s1, s2)
                rules = make_rules(draft)

                res = form_validation.validate(store, self.actor, "ZF-1", draft["draft_id"], rules)
                self.assertEqual(res["status"], "Not evaluated")
                self.assertEqual(res["results"], [])
                self.assertIsNone(res["rule_set"])

                pack = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(pack["pack_status"], "Held")
                self.assertFalse(pack["pack_ready_for_review"])
                self.assertFalse(pack["reviewed"])
                self.assertEqual(pack["submission"], "Not submitted")
                self.assertEqual(pack["eligibility"], "Not assessed")

                # Schema approved, source policy still unapproved -> Not evaluated
                self.approve_registered_schema(store, schema_approved=True, policy_approved=False)
                self.assertEqual(
                    form_validation.validate(store, self.actor, "ZF-1", draft["draft_id"], rules)[
                        "status"
                    ],
                    "Not evaluated",
                )

                # Both approved, but rule set unapproved (with None approver) -> Not evaluated
                self.approve_registered_schema(store, schema_approved=True, policy_approved=True)
                unapproved_rules = make_rules(draft, approved=False)
                self.assertEqual(
                    form_validation.validate(
                        store, self.actor, "ZF-1", draft["draft_id"], unapproved_rules
                    )["status"],
                    "Not evaluated",
                )

                # Rule set (id, version) missing from schema rule_refs -> Not evaluated
                undeclared = make_rules(draft, rule_set_version="99")
                out_undeclared = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], undeclared
                )
                self.assertEqual(out_undeclared["status"], "Not evaluated")
                self.assertTrue(any("rule_refs" in reason for reason in out_undeclared["reasons"]))

                # Mismatched template_version in bound -> Not evaluated
                wrong_bound = make_rules(draft)
                wrong_bound["bound"]["template_version"] = "2"
                self.assertEqual(
                    form_validation.validate(
                        store, self.actor, "ZF-1", draft["draft_id"], wrong_bound
                    )["status"],
                    "Not evaluated",
                )

        # Funding form with Unknown funding route remains Not evaluated even if approved
        for store in self.stores:
            unknown_def = rich_schema(funding_status="Unknown")
            unknown_def["id"] = "SYN-FUND-UNK"
            forms.register_schema(store, self.actor, unknown_def)
            self.approve_registered_schema(store, schema_id="SYN-FUND-UNK")
            draft_u = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(action="open", schema_id="SYN-FUND-UNK", schema_version=1),
            )
            rules_u = make_rules(draft_u)
            res_u = form_validation.validate(
                store, self.actor, "ZF-1", draft_u["draft_id"], rules_u
            )
            self.assertEqual(res_u["status"], "Not evaluated")
            self.assertTrue(any("funding route" in r for r in res_u["reasons"]))

    def test_malformed_rule_sets_and_human_only_targets_raise_value_error(self) -> None:
        store = self.stores[0]
        draft, *_ = self.setup_rich_draft(
            store, definition=rich_schema(include_human_only=True), approve_schema=True
        )
        valid_base = make_rules(draft)

        bad_cases: list[Any] = [
            None,
            {},
        ]
        # Duplicate rule_id
        dup = copy.deepcopy(valid_base)
        dup["rules"][1]["rule_id"] = dup["rules"][0]["rule_id"]
        bad_cases.append(dup)

        # Unknown field_id
        unk = copy.deepcopy(valid_base)
        unk["rules"][0]["field_id"] = "missing_field"
        bad_cases.append(unk)

        # HUMAN_ONLY target field
        human = copy.deepcopy(valid_base)
        human["rules"].append(
            dict(
                rule_id="R-HUM",
                field_id="signoff",
                kind="max_length",
                param=10,
                message="Cannot validate human sign-off.",
            )
        )
        bad_cases.append(human)

        # Boolean param for numeric min
        bool_min = copy.deepcopy(valid_base)
        bool_min["rules"][1]["param"] = True
        bad_cases.append(bool_min)

        # Invalid regex
        bad_re = copy.deepcopy(valid_base)
        bad_re["rules"][4]["param"] = "[unclosed"
        bad_cases.append(bad_re)

        # Sum rule with mismatched calc_version
        bad_calc = copy.deepcopy(valid_base)
        bad_calc["rules"][5]["param"]["calc_version"] = "999"
        bad_cases.append(bad_calc)

        # Sum rule referencing non-numeric addend
        bad_addend = copy.deepcopy(valid_base)
        bad_addend["rules"][5]["param"]["addends"] = ["ground_area", "notes"]
        bad_cases.append(bad_addend)

        # Duplicate sum rule on same field
        dup_sum = copy.deepcopy(valid_base)
        dup_sum["rules"].append(dict(dup_sum["rules"][5], rule_id="R-AREA-SUM-2"))
        bad_cases.append(dup_sum)

        for bad in bad_cases:
            with self.assertRaises(ValueError):
                form_validation.validate(store, self.actor, "ZF-1", draft["draft_id"], bad)

    def test_validation_evaluates_reviewer_confirmed_inputs_only(self) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                forms.register_schema(store, self.actor, rich_schema())
                self.approve_registered_schema(store)
                # Stage values that would FAIL rules if unconfirmed candidates were evaluated
                _doc, staged = self.stage_doc(
                    store,
                    [
                        ("epc", "G"),
                        ("ground_area", "1"),
                        ("upper_area", "999"),
                        ("area", "5"),
                        ("notes", "INVALID UPPERCASE WITH MORE THAN TWENTY CHARS"),
                    ],
                )
                draft = form_review.action(
                    store,
                    self.actor,
                    "ZF-1",
                    dict(action="open", schema_id="SYN-TECH", schema_version=1),
                )
                rules = make_rules(draft)

                unreviewed = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(unreviewed["confirmed_fields"], [])
                self.assertEqual({r["status"] for r in unreviewed["results"]}, {"Unknown"})
                self.assertEqual(unreviewed["status"], "Unknown")

                # Rejecting a candidate still leaves it unconfirmed (Unknown, never Fail)
                draft = form_review.action(
                    store,
                    self.actor,
                    "ZF-1",
                    dict(
                        action="review",
                        draft_id=draft["draft_id"],
                        expected_version=draft["input_version"],
                        field_id="epc",
                        decision="reject",
                        batch_id=None,
                        candidate_id=None,
                        value=None,
                        reason="SYN explicit reviewer note",
                    ),
                )
                after_reject = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual({r["status"] for r in after_reject["results"]}, {"Unknown"})

                # Blank string correction remains Unknown, never Fail
                draft = self.accept_candidate(store, draft, staged, "epc", "D")
                draft = self.accept_candidate(store, draft, staged, "notes", "   ")
                after_blank = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(after_blank["confirmed_fields"], ["epc"])
                self.assertNotIn("Fail", {i["status"] for i in after_blank["open_issues"]})
                notes_statuses = {
                    r["status"] for r in after_blank["results"] if r["field_id"] == "notes"
                }
                self.assertEqual(notes_statuses, {"Unknown"})

    def test_tampered_or_unregistered_reviewer_history_is_blocked_as_fail(self) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, _d1, s1, _d2, s2 = self.setup_rich_draft(store)
                draft = self.confirm_all_rich(store, draft, s1, s2)
                rules = make_rules(draft)

                # Mutate reviewer on epc's audit event to an unregistered email
                with store.lock:
                    stored = next(
                        d
                        for d in store._case("ZF-1")["form_reviews"]
                        if d["id"] == draft["draft_id"]
                    )
                    epc_event = next(e for e in stored["history"] if e["field_id"] == "epc")
                    epc_event["reviewer"] = "unregistered-reviewer@example.test"
                    store.save()

                tampered = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(tampered["status"], "Fail")
                self.assertNotIn("epc", tampered["confirmed_fields"])
                epc_rule = next(r for r in tampered["results"] if r["rule_id"] == "R-EPC")
                self.assertEqual(epc_rule["status"], "Unknown")
                self.assertIn(
                    ("epc", "Fail", "Value lacks reviewer confirmation."),
                    {(i["field_id"], i["status"], i["reason"]) for i in tampered["open_issues"]},
                )

    def test_approved_scalar_and_decimal_sum_rules_across_all_types(self) -> None:
        scalar_def = rich_schema(form_type="technical")
        scalar_def["fields"].extend(
            [
                dict(
                    id="floors",
                    section_id="home",
                    type="integer",
                    unit=None,
                    options=[],
                    required=True,
                    required_when=[],
                    source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
                    evidence_required=["survey"],
                    calculation_ref=None,
                    category="value",
                ),
                dict(
                    id="consented",
                    section_id="home",
                    type="boolean",
                    unit=None,
                    options=[],
                    required=True,
                    required_when=[],
                    source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
                    evidence_required=["record"],
                    calculation_ref=None,
                    category="value",
                ),
                dict(
                    id="survey_date",
                    section_id="home",
                    type="date",
                    unit=None,
                    options=[],
                    required=True,
                    required_when=[],
                    source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
                    evidence_required=["survey"],
                    calculation_ref=None,
                    category="value",
                ),
            ]
        )
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                forms.register_schema(store, self.actor, scalar_def)
                self.approve_registered_schema(store)
                _doc, staged = self.stage_doc(
                    store,
                    [
                        ("epc", "D"),
                        ("ground_area", "0.1"),
                        ("upper_area", "0.2"),
                        ("area", "0.3"),
                        ("notes", "loft ok"),
                        ("floors", "2"),
                        ("consented", "true"),
                        ("survey_date", "2026-05-01"),
                    ],
                )
                draft = form_review.action(
                    store,
                    self.actor,
                    "ZF-1",
                    dict(action="open", schema_id="SYN-TECH", schema_version=1),
                )
                draft = self.accept_candidate(store, draft, staged, "epc", "D", decision="accept")
                draft = self.accept_candidate(store, draft, staged, "ground_area", 0.1)
                draft = self.accept_candidate(store, draft, staged, "upper_area", 0.2)
                draft = self.accept_candidate(store, draft, staged, "area", 0.3)
                draft = self.accept_candidate(
                    store, draft, staged, "notes", "loft ok", decision="accept"
                )
                draft = self.accept_candidate(store, draft, staged, "floors", 2)
                draft = self.accept_candidate(store, draft, staged, "consented", True)
                draft = self.accept_candidate(
                    store, draft, staged, "survey_date", "2026-05-01", decision="accept"
                )

                rules = make_rules(draft, ground_min=0.05)
                rules["rules"].extend(
                    [
                        dict(
                            rule_id="R-NUMBER-EQ",
                            field_id="upper_area",
                            kind="equals",
                            param=0.2,
                            message="Upper area must equal 0.2.",
                        ),
                        dict(
                            rule_id="R-FLOORS",
                            field_id="floors",
                            kind="min",
                            param=1,
                            message="At least 1 floor required.",
                        ),
                        dict(
                            rule_id="R-CONSENT",
                            field_id="consented",
                            kind="equals",
                            param=True,
                            message="Consent flag must be True.",
                        ),
                        dict(
                            rule_id="R-DATE",
                            field_id="survey_date",
                            kind="equals",
                            param="2026-05-01",
                            message="Survey date must match 2026-05-01.",
                        ),
                    ]
                )
                # Verify Decimal equality on number fields (100 vs 100.0) and exact 0.1 + 0.2 == 0.3
                passed = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(passed["status"], "Pass")
                self.assertEqual(passed["open_issues"], [])

                pack = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(pack["pack_status"], "Ready for Finance review")
                self.assertTrue(pack["pack_ready_for_review"])
                self.assertFalse(pack["reviewed"])

                # Without the sum rule, calculation_ref keeps open_issues Unknown -> pack Held
                no_sum_rules = make_rules(draft, include_sum=False, ground_min=0.05)
                no_sum = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], no_sum_rules
                )
                self.assertEqual(no_sum["status"], "Unknown")
                self.assertTrue(
                    any(
                        i["reason"] == "Approved calculation is unavailable."
                        for i in no_sum["open_issues"]
                    )
                )

                # Mismatched sum produces Fail
                draft = self.accept_candidate(store, draft, staged, "area", 100.0)
                rules["rules"].append(
                    dict(
                        rule_id="R-AREA-INT-FLOAT",
                        field_id="area",
                        kind="one_of",
                        param=[100],
                        message="Area must match integer 100 numerically.",
                    )
                )
                failed = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(failed["status"], "Fail")
                int_float_rule = next(
                    r for r in failed["results"] if r["rule_id"] == "R-AREA-INT-FLOAT"
                )
                self.assertEqual(int_float_rule["status"], "Pass")
                sum_rule = next(r for r in failed["results"] if r["rule_id"] == "R-AREA-SUM")
                self.assertEqual(sum_rule["status"], "Fail")

    def test_overall_status_precedence_fail_over_conflict_over_unknown_over_pass(self) -> None:
        store = self.stores[0]
        draft, _d1, s1, _d2, s2 = self.setup_rich_draft(store)
        # Stage conflicting alternative for notes while notes remains unreviewed
        self.stage_doc(store, [("notes", "conflicting alternative")], filename="alt.txt")
        draft = self.accept_candidate(store, draft, s1, "epc", "D", decision="accept")
        draft = self.accept_candidate(store, draft, s1, "ground_area", 12.1)
        draft = self.accept_candidate(store, draft, s2, "upper_area", 17.2)
        draft = self.accept_candidate(store, draft, s2, "area", 29.3)

        rules = make_rules(draft)
        conflict_out = form_validation.validate(store, self.actor, "ZF-1", draft["draft_id"], rules)
        # Rules on notes are Unknown, open_issues has Conflict -> Conflict beats Unknown
        self.assertEqual(conflict_out["status"], "Conflict")

        # Now make ground_area fail its min rule -> Fail beats Conflict and Unknown
        strict_rules = make_rules(draft, ground_min=50)
        fail_out = form_validation.validate(
            store, self.actor, "ZF-1", draft["draft_id"], strict_rules
        )
        self.assertEqual(fail_out["status"], "Fail")

    def test_review_pack_links_fields_evidence_attachments_and_single_pass_hashing(self) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, doc1, s1, doc2, s2 = self.setup_rich_draft(store)
                # Review epc (v1) and ground_area (v2) on doc1; notes stays optional on epc="C"
                draft = self.accept_candidate(store, draft, s1, "epc", "C")
                draft = self.accept_candidate(store, draft, s1, "ground_area", 12.1)
                # Review upper_area (v3) and area (v4) on doc2
                draft = self.accept_candidate(store, draft, s2, "upper_area", 17.2)
                draft = self.accept_candidate(store, draft, s2, "area", 29.3)

                rules_with_unconfirmed_notes = make_rules(draft)
                held_pack = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules_with_unconfirmed_notes
                )
                self.assertEqual(held_pack["pack_status"], "Held")

                rules = make_rules(draft)
                rules["rules"] = [r for r in rules["rules"] if r["field_id"] != "notes"]
                before_audit = list(store.audit_entries())
                with (
                    patch.object(store.docstore, "get", wraps=store.docstore.get) as read,
                    patch.object(store, "save", side_effect=AssertionError("No save")),
                ):
                    pack = form_validation.review_pack(
                        store, self.actor, "ZF-1", draft["draft_id"], rules
                    )

                # Each distinct document hashed at most once per review_pack call
                read_ids = [call.args[1] for call in read.call_args_list]
                self.assertEqual(read_ids.count(doc1["id"]), 1)
                self.assertEqual(read_ids.count(doc2["id"]), 1)
                self.assertEqual(list(store.audit_entries()), before_audit)

                self.assertEqual(pack["pack_status"], "Ready for Finance review")
                self.assertEqual(pack["template_version"], "1")
                self.assertEqual(pack["input_version"], 5)
                self.assertEqual(len(pack["history"]), 4)

                by_fid = {f["field_id"]: f for f in pack["fields"]}
                self.assertEqual(by_fid["epc"]["input_version"], 2)
                self.assertEqual(by_fid["ground_area"]["input_version"], 3)
                self.assertEqual(by_fid["upper_area"]["input_version"], 4)
                self.assertEqual(by_fid["area"]["input_version"], 5)
                self.assertEqual(by_fid["notes"]["input_version"], 0)
                for item in [*pack["fields"], *pack["evidence"], *pack["attachments"]]:
                    self.assertEqual(item["template_version"], "1")

                # Evidence deduplicates per (source_id, source_version) with max input_version
                self.assertEqual(len(pack["evidence"]), 2)
                ev_by_src = {e["source_id"]: e for e in pack["evidence"]}
                att_ids = {a["attachment_id"] for a in pack["attachments"]}
                self.assertEqual(ev_by_src[doc1["id"]]["field_ids"], ["epc", "ground_area"])
                self.assertEqual(ev_by_src[doc1["id"]]["input_version"], 3)
                self.assertIn(ev_by_src[doc1["id"]]["attachment_id"], att_ids)
                self.assertEqual(ev_by_src[doc2["id"]]["field_ids"], ["upper_area", "area"])
                self.assertEqual(ev_by_src[doc2["id"]]["input_version"], 5)
                self.assertIn(ev_by_src[doc2["id"]]["attachment_id"], att_ids)

                # Persistence across reopen yields identical content_sha256
                reopened = self.base.reopen(store)
                reopened_pack = form_validation.review_pack(
                    reopened, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(pack["content_sha256"], reopened_pack["content_sha256"])

    def test_pack_freshness_rejects_tampered_and_cross_case_packs_as_invalid(self) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, _d1, s1, _d2, s2 = self.setup_rich_draft(store)
                draft = self.confirm_all_rich(store, draft, s1, s2)
                rules = make_rules(draft)
                pack = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )

                tampered = copy.deepcopy(pack)
                tampered["fields"][0]["value"] = "A"
                self.assertEqual(
                    form_validation.pack_freshness(store, self.actor, "ZF-1", tampered, rules)[
                        "status"
                    ],
                    "Invalid",
                )

                missing_key = copy.deepcopy(pack)
                del missing_key["evidence"]
                self.assertEqual(
                    form_validation.pack_freshness(store, self.actor, "ZF-1", missing_key, rules)[
                        "status"
                    ],
                    "Invalid",
                )

                other_case = str(dataset.DATA["cases"][1]["id"])
                self.assertEqual(
                    form_validation.pack_freshness(store, self.actor, other_case, pack, rules)[
                        "status"
                    ],
                    "Invalid",
                )

    def test_unavailable_evidence_and_missing_draft_block_disclosure(self) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, doc1, s1, _d2, s2 = self.setup_rich_draft(store)
                draft = self.confirm_all_rich(store, draft, s1, s2)
                rules = make_rules(draft)
                saved = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )

                # Quarantine doc1 on the case
                with store.lock:
                    target_doc = next(
                        d for d in store._case("ZF-1")["documents"] if d["id"] == doc1["id"]
                    )
                    target_doc["scan"]["status"] = "infected"
                    store.save()

                v_out = form_validation.validate(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                p_out = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                f_out = form_validation.pack_freshness(store, self.actor, "ZF-1", saved, rules)
                self.assertEqual(v_out["status"], "Unavailable")
                self.assertEqual(p_out["status"], "Unavailable")
                self.assertEqual(p_out["pack_status"], "Held")
                self.assertNotIn("fields", p_out)
                self.assertEqual(f_out["status"], "Unavailable")

                # Restore scan status, then delete draft to test missing working review
                with store.lock:
                    target_doc["scan"]["status"] = "clean"
                    store._case("ZF-1")["form_reviews"].clear()
                    store.save()
                missing_draft = form_validation.pack_freshness(
                    store, self.actor, "ZF-1", saved, rules
                )
                self.assertEqual(missing_draft["status"], "Unavailable")

    def test_pack_freshness_propagates_exact_staleness_on_source_input_and_schema_changes(
        self,
    ) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, _doc1, s1, doc2, s2 = self.setup_rich_draft(store)
                draft = self.confirm_all_rich(store, draft, s1, s2)
                rules = make_rules(draft)
                saved = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )

                cur = form_validation.pack_freshness(store, self.actor, "ZF-1", saved, rules)
                self.assertEqual(cur["status"], "Current")
                self.assertEqual(cur["stale_fields"], [])
                self.assertEqual(
                    cur["unaffected_fields"],
                    ["area", "epc", "ground_area", "notes", "upper_area"],
                )

                # 1. Reviewer updates epc -> epc and conditional dependent notes become stale
                draft = self.accept_candidate(store, draft, s1, "epc", "C")
                after_epc = form_validation.pack_freshness(store, self.actor, "ZF-1", saved, rules)
                self.assertEqual(after_epc["status"], "Stale")
                self.assertEqual(after_epc["stale_fields"], ["epc", "notes"])
                self.assertEqual(
                    after_epc["unaffected_fields"], ["area", "ground_area", "upper_area"]
                )
                self.assertTrue(after_epc["reasons"])

                # 2. Update doc2 version -> upper_area and sum dependent area become stale
                saved_v2 = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                with store.lock:
                    doc2_rec = next(
                        d for d in store._case("ZF-1")["documents"] if d["id"] == doc2["id"]
                    )
                    doc2_rec["version"] = 2
                    store.save()
                after_doc2 = form_validation.pack_freshness(
                    store, self.actor, "ZF-1", saved_v2, rules
                )
                self.assertEqual(after_doc2["status"], "Stale")
                self.assertEqual(after_doc2["stale_fields"], ["area", "upper_area"])
                self.assertEqual(after_doc2["unaffected_fields"], ["epc", "ground_area", "notes"])

                # 3. Register schema v2 changing ground_area -> ground_area and area become stale
                with store.lock:
                    doc2_rec["version"] = 1
                    store.save()
                schema_v2 = rich_schema(version=2)
                schema_v2["fields"][1]["unit"] = "sqft"
                forms.register_schema(store, self.actor, schema_v2)
                after_schema = form_validation.pack_freshness(
                    store, self.actor, "ZF-1", saved_v2, rules
                )
                self.assertEqual(after_schema["status"], "Stale")
                self.assertEqual(after_schema["stale_fields"], ["area", "ground_area"])
                self.assertEqual(after_schema["unaffected_fields"], ["epc", "notes", "upper_area"])

    def test_pack_freshness_propagates_pass_preserving_rule_changes_to_dependents_only(
        self,
    ) -> None:
        for store in self.stores:
            with self.subTest(store=type(store).__name__):
                draft, _d1, s1, _d2, s2 = self.setup_rich_draft(store)
                draft = self.confirm_all_rich(store, draft, s1, s2)
                rules = make_rules(draft, ground_min=5)
                saved = form_validation.review_pack(
                    store, self.actor, "ZF-1", draft["draft_id"], rules
                )
                self.assertEqual(saved["pack_status"], "Ready for Finance review")

                # Tighten ground_area min (12.1 still passes): ground_area and sum target area stale
                tighter_ground = make_rules(draft, ground_min=10)
                ground_diff = form_validation.pack_freshness(
                    store, self.actor, "ZF-1", saved, tighter_ground
                )
                self.assertEqual(ground_diff["status"], "Stale")
                self.assertEqual(ground_diff["stale_fields"], ["area", "ground_area"])
                self.assertEqual(ground_diff["unaffected_fields"], ["epc", "notes", "upper_area"])
                self.assertTrue(ground_diff["reasons"])

                # Tighten epc options ("D" still passes): epc and conditional notes become stale
                tighter_epc = make_rules(draft, ground_min=5, epc_options=["C", "D"])
                epc_diff = form_validation.pack_freshness(
                    store, self.actor, "ZF-1", saved, tighter_epc
                )
                self.assertEqual(epc_diff["status"], "Stale")
                self.assertEqual(epc_diff["stale_fields"], ["epc", "notes"])
                self.assertEqual(
                    epc_diff["unaffected_fields"], ["area", "ground_area", "upper_area"]
                )

    def test_authorization_rejects_resident_missing_and_out_of_scope_callers(self) -> None:
        store = self.stores[0]
        draft, _d1, s1, _d2, s2 = self.setup_rich_draft(store)
        draft = self.confirm_all_rich(store, draft, s1, s2)
        rules = make_rules(draft)
        pack = form_validation.review_pack(store, self.actor, "ZF-1", draft["draft_id"], rules)

        unauthorized_callers = [
            dict(email="nobody@example.test", role="Officer"),
            dict(email="resident@example.test", role="Resident"),
        ]
        for bad_actor in unauthorized_callers:
            with self.assertRaises(PermissionError):
                form_validation.validate(store, bad_actor, "ZF-1", draft["draft_id"], rules)
            with self.assertRaises(PermissionError):
                form_validation.review_pack(store, bad_actor, "ZF-1", draft["draft_id"], rules)
            with self.assertRaises(PermissionError):
                form_validation.pack_freshness(store, bad_actor, "ZF-1", pack, rules)


if __name__ == "__main__":
    unittest.main()
