"""Aftercare concern route and evaluator view on constructed records (FR-049, AC-063, #133)."""

import json
import unittest
from collections.abc import Callable
from copy import deepcopy
from typing import Any

from zava_forward.core import aftercare as af
from zava_forward.core.aftercare import AftercareRegister

OWNER = "Aftercare Lead"


def raised(reg: AftercareRegister, home: str = "H1", **kw: object) -> str:
    args: dict[str, object] = dict(
        route="digital",
        raised_by="household",
        home_ref=home,
        kind="discomfort",
        statement="The living room stays cold in the evening.",
        owner=OWNER,
        next_update="2026-12-01",
    )
    args.update(kw)
    return str(reg.raise_concern(**args)["id"])  # type: ignore[arg-type]


class RouteTests(unittest.TestCase):
    def test_non_digital_route_needs_staff_and_channel(self) -> None:
        reg = AftercareRegister()
        with self.assertRaises(ValueError):
            raised(reg, route="staff_recorded", recorded_by="Sam", channel="email")
        with self.assertRaises(ValueError):
            raised(reg, route="staff_recorded", channel="phone")
        rec = reg.concerns[raised(reg, route="staff_recorded", recorded_by="Sam", channel="paper")]
        self.assertEqual(rec["channel"], "paper")
        self.assertEqual(rec["accessible_route"], af.ACCESSIBLE_ROUTE)

    def test_representative_needs_a_stated_basis_and_kinds_are_checked(self) -> None:
        reg = AftercareRegister()
        with self.assertRaises(ValueError):
            raised(reg, raised_by="representative")
        cid = raised(
            reg, raised_by="representative", representative_basis="Written consent on file"
        )
        self.assertEqual(reg.concerns[cid]["representative_basis"], "Written consent on file")
        with self.assertRaises(ValueError):
            raised(reg, kind="complaint")
        for kind in ("higher_bill", "control_use"):
            raised(reg, kind=kind)

    def test_owner_is_required_and_only_owner_acts(self) -> None:
        reg = AftercareRegister()
        with self.assertRaises(ValueError):
            raised(reg, owner=" ")
        cid = raised(reg)
        with self.assertRaises(PermissionError):
            reg.start_investigation(cid, "Someone Else", "2026-12-05")


class ResidentReportTests(unittest.TestCase):
    def test_normal_sensor_never_dismisses_and_is_not_a_basis(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg, sensor_context={"signal": "normal"})
        rec = reg.concerns[cid]
        self.assertFalse(rec["dismissed_by_sensor"])
        self.assertEqual(rec["investigation"], "received")
        self.assertIn(cid, [r["id"] for r in reg.unresolved()])
        with self.assertRaises(ValueError):
            reg.record_outcome(cid, OWNER, "no_remedy_needed", "sensor_reading", "Reading normal")
        self.assertNotIn("sensor_context", reg.view(cid))
        self.assertEqual(
            reg.concerns[cid]["statement"], "The living room stays cold in the evening."
        )


class SensorContextTests(unittest.TestCase):
    def test_later_normal_signal_is_context_only(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        before = {k: reg.concerns[cid][k] for k in ("investigation", "outcome", "remedy")}
        rec = reg.add_sensor_context(cid, {"signal": "normal"})
        self.assertEqual(rec["sensor_context"], {"signal": "normal"})
        self.assertEqual({k: rec[k] for k in before}, before)
        self.assertFalse(rec["dismissed_by_sensor"])
        self.assertEqual(rec["history"][-1], {"event": "sensor_context_added"})
        self.assertIn(cid, [r["id"] for r in reg.unresolved()])
        self.assertNotIn("sensor_context", reg.view(cid))
        reg.start_investigation(cid, OWNER, "2026-12-08")
        reg.add_sensor_context(cid, {"signal": "normal"})
        self.assertEqual(reg.concerns[cid]["investigation"], "under_investigation")

    def test_context_text_is_guarded_and_typed(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        with self.assertRaises(ValueError):
            reg.add_sensor_context(cid, {"note": "Damp caused by the resident"})
        with self.assertRaises(ValueError):
            reg.add_sensor_context(cid, {})
        with self.assertRaises(ValueError):
            reg.add_sensor_context(cid, {"signal": 3})  # type: ignore[dict-item]
        with self.assertRaises(ValueError):
            raised(reg, sensor_context={"note": "Misuse of heating"})
        with self.assertRaises(KeyError):
            reg.add_sensor_context("AC-999", {"signal": "normal"})
        self.assertIsNone(reg.concerns[cid]["sensor_context"])


class ClosureTests(unittest.TestCase):
    def test_closure_cannot_erase_concern_or_remedy(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        reg.start_investigation(cid, OWNER, "2026-12-05")
        reg.record_outcome(cid, OWNER, "remedy_needed", "home_visit", "Visit 2026-11-20")
        self.assertEqual(reg.concerns[cid]["remedy"]["status"], "open")
        before = reg.view(cid)
        reg.record_closure("H1", "handover", "2026-11-25", "Closure Owner")
        reg.record_closure("H1", "financial", "2026-11-30", "Finance Owner")
        self.assertEqual(reg.view(cid), before)
        self.assertEqual([r["id"] for r in reg.unresolved("H1")], [cid])
        view = reg.evaluator_view(["H1"], ["H1"])
        self.assertEqual(view["unresolved_with_handover_or_financial_closure"], 1)
        with self.assertRaises(ValueError):
            reg.record_closure("H1", "package", "2026-11-30", "x")

    def test_closure_leaves_owner_outcome_remedy_and_history_whole_through_a_restart(self) -> None:
        reg = AftercareRegister()
        first = raised(reg)
        other = raised(reg, home="H2")
        reg.record_outcome(first, OWNER, "remedy_needed", "home_visit", "Visit found draughts")
        reg.set_remedy(first, OWNER, "in_progress")
        before = {cid: deepcopy(reg.concerns[cid]) for cid in (first, other)}
        for kind in af.CLOSURE_KINDS:
            reg.record_closure("H1", kind, "2026-12-10", "Closure Owner")
        restored = AftercareRegister.from_state(json.loads(json.dumps(reg.to_state())))
        for register in (reg, restored):
            self.assertEqual(register.concerns[first], before[first])
            self.assertEqual(register.concerns[other], before[other])
            self.assertEqual(register.concerns[first]["owner"], OWNER)
            self.assertEqual(register.concerns[first]["remedy"]["status"], "in_progress")
            self.assertEqual({r["id"] for r in register.unresolved()}, {first, other})

    def test_closure_before_a_concern_does_not_pre_close_it(self) -> None:
        reg = AftercareRegister()
        reg.record_closure("H1", "handover", "2026-11-01", "Closure Owner")
        reg.record_closure("H1", "financial", "2026-11-02", "Finance Owner")
        cid = raised(reg)
        rec = reg.concerns[cid]
        self.assertEqual(rec["investigation"], "received")
        self.assertEqual(rec["remedy"]["status"], "not_assessed")
        self.assertEqual([r["id"] for r in reg.unresolved("H1")], [cid])

    def test_owner_can_still_record_outcome_and_remedy_after_closure(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        reg.record_closure("H1", "financial", "2026-11-02", "Finance Owner")
        reg.record_outcome(cid, OWNER, "remedy_needed", "household_conversation", "Spoke to them")
        self.assertEqual(reg.concerns[cid]["remedy"]["status"], "open")
        reg.set_remedy(cid, OWNER, "completed", "Fitted and checked on 2026-11-20")
        self.assertEqual(reg.unresolved("H1"), [])
        self.assertEqual(reg.concerns[cid]["outcome"]["outcome"], "remedy_needed")

    def test_restore_refuses_a_closed_remedy_without_an_outcome_or_evidence(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        reg.record_outcome(cid, OWNER, "remedy_needed", "home_visit", "Visit")
        reg.set_remedy(cid, OWNER, "completed", "Checked")
        state = reg.to_state()
        edits: list[dict[str, object]] = [
            {"remedy": {"status": "completed", "evidence": None}},
            {"remedy": {"status": "completed", "evidence": " "}},
            {"investigation": "received", "outcome": None},
        ]
        for edit in edits:
            bad = deepcopy(state)
            bad["concerns"][cid].update(edit)
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                AftercareRegister.from_state(bad)

    def test_remedy_completion_needs_outcome_and_evidence(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        with self.assertRaises(ValueError):
            reg.set_remedy(cid, OWNER, "completed", "Fitted")
        reg.record_outcome(cid, OWNER, "remedy_needed", "home_visit", "Visit")
        with self.assertRaises(ValueError):
            reg.set_remedy(cid, OWNER, "completed")
        reg.set_remedy(cid, OWNER, "completed", "Fitted and household told")
        self.assertEqual(reg.unresolved(), [])

    def test_cannot_determine_stays_unresolved_and_overdue_lists_it(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        reg.record_outcome(cid, OWNER, "cannot_determine", "records_review", "Records incomplete")
        self.assertEqual([r["id"] for r in reg.overdue("2026-12-02")], [cid])
        self.assertEqual(reg.overdue("2026-12-01"), [])


class EvaluatorTests(unittest.TestCase):
    def test_denominators_unknowns_and_scope(self) -> None:
        reg = AftercareRegister()
        raised(reg, "H1")
        raised(reg, "H9")
        view = reg.evaluator_view(["H1", "H2", "H3"], ["H1", "H2", "H9"])
        self.assertEqual(view["homes_with_baseline"], {"count": 2, "denominator": 3})
        self.assertEqual(view["homes_baseline_unknown"], 1)
        self.assertEqual(view["households_raising_concern"], {"count": 1, "denominator": 3})
        self.assertEqual(view["concerns_outside_stated_scope"], 1)
        self.assertEqual(view["concerns_by_outcome"]["no_outcome_yet"], 1)
        self.assertIn("Households that did not raise", " ".join(view["unknowns"]))

    def test_unknown_baseline_is_stated_not_zero(self) -> None:
        view = AftercareRegister().evaluator_view(["H1"])
        self.assertIsNone(view["homes_with_baseline"])
        self.assertIn("Baseline coverage is unknown.", view["unknowns"])

    def test_templated_text_has_no_causation_blame_or_savings(self) -> None:
        for text in (af.ACCESSIBLE_ROUTE, af.PROTECTION, af.EVALUATOR_NOTICE):
            self.assertEqual(af.neutral_text(text), text)
        for bad in ("You will save money", "This was caused by heating use", "It is your fault"):
            with self.assertRaises(ValueError):
                af.neutral_text(bad)
        view = AftercareRegister().evaluator_view(["H1"], ["H1"])
        self.assertEqual(view["notice"], af.EVALUATOR_NOTICE)

    def test_paraphrased_savings_causation_and_blame_are_rejected(self) -> None:
        for bad in (
            "You'll save a lot",
            "You\u2019ll save a lot",
            "This will cut your bills",
            "Your bills will fall",
            "Expect savings of 20 percent",
            "The tenant caused the damp",
            "The resident caused it",
            "The resident is at fault",
            "It reflects the occupant's behaviour",
            "The resident misunderstood the controls",
            "Residents caused damp",
            "The tenant has caused damp",
            "The tenant was at fault",
            "Resident behaviour",
            "Unknown, but you'll save money",
            "No evidence of damp, the tenant caused it",
            "Unknown whether the tenant caused it and the tenant caused it",
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                af.neutral_text(bad)

    def test_further_savings_causation_and_household_blame_phrasings_are_rejected(self) -> None:
        for text in (
            "This reduces your bills.",
            "Lower bills are expected.",
            "This saves money.",
            "You could save money.",
            "Bills should fall.",
            "Saving money is likely.",
            "Higher use is due to the household.",
            "The tenant's fault.",
            "Overuse by the tenant.",
            "The household wastes energy.",
            "The result of the retrofit is lower use.",
            "The retrofit led to higher use.",
            "The insulation caused the change.",
            "The retrofit made the home colder.",
            "Your bills will be cheaper after the upgrade.",
            "No claim of savings, but you could save money.",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                af.neutral_text(text)
        for text in (
            "Cannot determine whether the retrofit caused it.",
            "The household reports a cold room.",
            "These figures are not a promise of savings.",
            "No claim of lower energy bills is made.",
        ):
            self.assertEqual(af.neutral_text(text), text)

    def test_neutral_factual_and_uncertain_statements_are_accepted(self) -> None:
        for good in (
            "Higher bills reported",
            "Resident reported cold room",
            "Cannot determine",
            "Cannot determine whether the resident caused it",
            "Unknown whether the tenant was at fault",
            "Unknown whether savings of any size were seen",
        ):
            self.assertEqual(af.neutral_text(good), good)

    def test_unicode_whitespace_and_soft_hyphen_obfuscation_are_rejected(self) -> None:
        for bad in (
            "\uff57\uff49\uff4c\uff4c \uff53\uff41\uff56\uff45 money",
            "\uff43\uff41\uff55\uff53\uff45\uff44 \uff42\uff59 damp",
            "will\u200bsave on heating",
            "your\u200dfault entirely",
            "guar\u00adanteed lower cost",
            "mis\u00aduse of the thermostat",
            "will   save next winter",
            "caused\nby condensation",
            "resident\u2019s lifestyle",
            "you\u2019ll save next quarter",
        ):
            with self.subTest(bad=bad):
                self.assertTrue(af.neutral_violations(bad))
                with self.assertRaises(ValueError):
                    af.neutral_text(bad)

    def test_multi_clause_uncertainty_and_negated_caveat_do_not_exempt_later_claims(self) -> None:
        for bad in (
            "Unknown whether flow dropped\nThe retrofit caused the cold room",
            "Unknown whether flow dropped; however, drying laundry indoors caused damp",
            "Unknown whether flow dropped, so bills will fall",
            "Cannot determine whether the valve stuck - resident lifestyle is at issue",
            "Not known if sensors drifted -- energy savings are expected",
            "Unknown whether humidity rose\u2014windows kept closed in winter",
            "Unknown whether flow changed while heating habits remain poor",
            "No claim of savings; however, the upgrade pays for itself",
            "They do not show a cause, and the heat pump caused the cold room",
        ):
            with self.subTest(bad=bad):
                self.assertTrue(af.neutral_violations(bad))
                with self.assertRaises(ValueError):
                    af.neutral_text(bad)
        for good in (
            af.EVALUATOR_NOTICE,
            af.PROTECTION,
            af.ACCESSIBLE_ROUTE,
            af.PACK_MANUAL_ROUTE,
            "Descriptive observed means only. They do not show a cause, assign fault or "
            "promise savings.",
            "Not known if the heating controls were reset during the power cut.",
        ):
            with self.subTest(good=good):
                self.assertEqual(af.neutral_violations(good), ())
                self.assertEqual(af.neutral_text(good), good)

    def test_lifestyle_blame_measure_causation_and_savings_promise_corpora_are_rejected(
        self,
    ) -> None:
        for bad in (
            "Condensation from drying laundry indoors.",
            "Damp from drying clothes on radiators.",
            "Mould from not opening windows.",
            "Humidity rose with windows kept shut.",
            "Cold room from lack of ventilation.",
            "High humidity reflects the occupant's lifestyle.",
            "Cold mornings reflect household heating habits.",
            "Improper use of the programmer.",
            "Thermostat setting was user error.",
            "Damage reflects carelessness.",
            "High consumption is the fault of the resident.",
            "Wall insulation is proven to cause the damp patch.",
            "The reading proves that the heat pump failed.",
            "Mould growth is attributable to the glazing.",
            "Airtightness caused the condensation.",
            "Ventilation is why your bedroom feels cold.",
            "The upgrade will save \u00a3150 a year.",
            "Households save up to 20% on heating.",
            "Expected five-year payback.",
            "The measure pays for itself.",
            "Slashes household heating bills.",
            "Promised energy savings after handover.",
            "The home is cheaper to run.",
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                af.neutral_text(bad)
        for good in (
            "Visited home; trickle vents observed closed and extract fan switched off at isolator.",
            "Household reported drying washing indoors because external line was removed.",
            "Observed 17.5 C mean evening living-room temperature over seven days.",
            "Checked programmer schedule with household and left printed quick guide.",
        ):
            with self.subTest(good=good):
                self.assertEqual(af.neutral_text(good), good)

    def test_register_writes_guard_staff_fields_while_keeping_household_statement_verbatim(
        self,
    ) -> None:
        reg = AftercareRegister()
        verbatim_statement = "I think the retrofit caused damp and you said I will save \u00a3200."
        verbatim_basis = "Carer letter saying higher bills are your fault."
        cid = raised(
            reg,
            raised_by="representative",
            representative_basis=verbatim_basis,
            statement=verbatim_statement,
        )
        self.assertEqual(reg.concerns[cid]["statement"], verbatim_statement)
        self.assertEqual(reg.concerns[cid]["representative_basis"], verbatim_basis)
        for bad_kw in (
            {"home": "H1 caused by damp"},
            {"owner": "Lead promising energy savings"},
            {"route": "staff_recorded", "channel": "phone", "recorded_by": "Sam blaming tenant"},
            {"sensor_context": {"caused by": "normal"}},
            {"sensor_context": {"note": "drying clothes"}},
        ):
            with self.subTest(bad_kw=bad_kw), self.assertRaises(ValueError):
                raised(reg, **bad_kw)
        self.assertEqual(len(reg.concerns), 1)
        with self.assertRaises(ValueError):
            reg.add_sensor_context(cid, {"blame": "reading"})
        with self.assertRaises(ValueError):
            reg.record_outcome(
                cid, OWNER, "advice_given", "home_visit", "Damp from not opening windows."
            )
        self.assertEqual(reg.concerns[cid]["investigation"], "received")
        with self.assertRaises(ValueError):
            reg.set_remedy(cid, OWNER, "open", "Upgrade pays for itself.")
        reg.record_outcome(cid, OWNER, "remedy_needed", "home_visit", "Checked vents on visit.")
        with self.assertRaises(ValueError):
            reg.set_remedy(cid, OWNER, "completed", "Fixed user error on thermostat.")
        self.assertEqual(reg.concerns[cid]["remedy"]["status"], "open")
        with self.assertRaises(ValueError):
            reg.record_closure("H1", "handover", "2026-12-10", "Owner promising payback")
        self.assertEqual(reg.closures, [])


class ConcernPackTests(unittest.TestCase):
    def test_pack_exists_without_ai_and_is_unreviewed(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg, sensor_context={"signal": "normal"})
        pack = reg.propose_pack(cid)
        self.assertEqual(pack["source"], "template")
        self.assertIsNone(pack["ai_summary"])
        self.assertEqual(pack["approval"], af.PACK_NOT_REVIEWED)
        self.assertFalse(pack["approved"])
        self.assertEqual(pack["household_statement"], reg.concerns[cid]["statement"])
        self.assertNotIn("normal", " ".join(pack["recorded_facts"]))
        for text in [*pack["recorded_facts"], *pack["questions_for_investigator"]]:
            af.neutral_text(text)

    def test_ai_summary_is_guarded_and_proposal_only(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        with self.assertRaises(ValueError):
            reg.propose_pack(cid, "The higher use was caused by the household.")
        with self.assertRaises(ValueError):
            reg.propose_pack(cid, "You will save money after the fix.")
        pack = reg.propose_pack(cid, "Household reports a cold living room in the evening.")
        self.assertEqual(pack["source"], "ai")
        self.assertFalse(pack["approved"])

    def test_review_by_named_owner_never_changes_the_concern(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        before = reg.view(cid)
        pid = str(reg.propose_pack(cid)["id"])
        self.assertEqual(reg.view(cid), before)
        with self.assertRaises(PermissionError):
            reg.review_pack(pid, "Someone Else", "accept", "Looks fine")
        with self.assertRaises(ValueError):
            reg.review_pack(pid, OWNER, "approve", "x")
        with self.assertRaises(ValueError):
            reg.review_pack(pid, OWNER, "accept", " ")
        done = reg.review_pack(pid, OWNER, "reject", "Not needed for this concern")
        self.assertEqual(done["approval"], "Rejected")
        self.assertFalse(done["approved"])
        with self.assertRaises(ValueError):
            reg.review_pack(pid, OWNER, "accept", "Changed mind")
        after = reg.view(cid)
        self.assertEqual(after, before)
        self.assertEqual(after["investigation"], "received")
        self.assertIsNone(after["outcome"])
        self.assertIn(cid, [r["id"] for r in reg.unresolved()])

    def test_proposing_a_pack_changes_nothing_on_the_record(self) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        before = deepcopy(reg.concerns)
        reg.propose_pack(cid, "Household reports a cold living room in the evening.")
        reg.propose_pack(cid)
        self.assertEqual(reg.concerns, before)
        self.assertEqual(len(reg.packs), 2)

    def test_pack_is_a_registered_unapproved_task(self) -> None:
        from zava_forward.core import ai_registry

        task = ai_registry.get(af.PACK_TASK)  # type: ignore[no-untyped-call]
        assert task is not None
        self.assertEqual(task["approval_state"], ai_registry.UNAPPROVED)
        self.assertEqual(task["kind"], "proposal-pack")
        live = ai_registry.authorizes_live(af.PACK_TASK)  # type: ignore[no-untyped-call]
        self.assertFalse(live)
        self.assertIn("no model call", task["manual_route"])

    def test_pack_review_reason_and_reviewer_are_guarded_without_mutating_pack_or_concern(
        self,
    ) -> None:
        reg = AftercareRegister()
        cid = raised(reg)
        pack = reg.propose_pack(cid)
        pid = str(pack["id"])
        for bad_reason in (
            "Rejected because damp is due to the resident.",
            "Accepted; heating bills will fall next month.",
            "Rejected; insulation caused the condensation.",
        ):
            with self.subTest(bad_reason=bad_reason), self.assertRaises(ValueError):
                reg.review_pack(pid, OWNER, "reject", bad_reason)
        self.assertIsNone(reg.packs[pid]["review"])
        self.assertEqual(reg.packs[pid]["approval"], af.PACK_NOT_REVIEWED)
        self.assertFalse(reg.packs[pid]["approved"])

    def test_all_templated_register_outputs_pass_neutral_guard(self) -> None:
        reg = AftercareRegister()
        cid = raised(
            reg,
            statement="Household said the retrofit caused damp and promised savings.",
        )
        texts: list[str] = []
        form = af.intake_form()
        texts.extend([form["title"], form["intro"], form["accessible_route"], form["protection"]])
        for field in form["fields"]:
            texts.append(field["label"])
            for opt in field.get("options", ()):
                texts.append(opt["label"])
        for opt in form["non_digital_channels"]:
            texts.append(opt["label"])
        texts.extend(af.intake_errors({"raised_by": "representative"}).values())
        shown = reg.view(cid)
        texts.extend([shown["accessible_route"], shown["protection"]])
        ev = reg.evaluator_view(["H1", "H2"], baseline_homes=["H1"])
        texts.append(ev["notice"])
        texts.extend(ev["unknowns"])
        pack = reg.propose_pack(cid)
        texts.extend(
            [
                pack["approval"],
                pack["manual_route"],
                pack["notice"],
                *pack["recorded_facts"],
                *pack["questions_for_investigator"],
            ]
        )
        for item in texts:
            with self.subTest(item=item):
                self.assertEqual(af.neutral_violations(item), ())


class IntakeFormTests(unittest.TestCase):
    def test_form_offers_non_digital_route_and_neutral_plain_text(self) -> None:
        form = af.intake_form()
        self.assertEqual(form["accessible_route"], af.ACCESSIBLE_ROUTE)
        self.assertEqual(
            [c["value"] for c in form["non_digital_channels"]], list(af.NON_DIGITAL_CHANNELS)
        )
        kinds = next(f for f in form["fields"] if f["name"] == "kind")["options"]
        self.assertEqual([k["value"] for k in kinds], list(af.CONCERN_KINDS))
        texts = [form["title"], form["intro"], form["protection"]]
        texts += [f["label"] for f in form["fields"]]
        for text in texts:
            self.assertEqual(af.neutral_text(text), text)
        self.assertNotIn("sensor", form["intro"].lower())

    def test_errors_are_plain_and_per_field(self) -> None:
        self.assertEqual(
            set(af.intake_errors({})),
            {"raised_by", "home_ref", "kind", "statement"},
        )
        ok = dict(raised_by="household", home_ref="H1", kind="other", statement="Too cold")
        self.assertEqual(af.intake_errors(ok), {})
        rep = dict(ok, raised_by="representative")
        self.assertEqual(set(af.intake_errors(rep)), {"representative_basis"})
        self.assertEqual(af.intake_errors(dict(rep, representative_basis="Power of attorney")), {})


class SnapshotTests(unittest.TestCase):
    def _populated(self) -> AftercareRegister:
        reg = AftercareRegister()
        cid = raised(reg, sensor_context={"signal": "normal"})
        reg.start_investigation(cid, OWNER, "2026-12-05")
        reg.record_outcome(cid, OWNER, "remedy_needed", "home_visit", "Visit found draughts")
        reg.record_closure("H1", "handover", "2026-12-10", "Handover Lead")
        reg.propose_pack(cid)
        return reg

    def test_round_trip_through_json_keeps_everything(self) -> None:
        reg = self._populated()
        restored = AftercareRegister.from_state(json.loads(json.dumps(reg.to_state())))
        self.assertEqual(restored.to_state(), reg.to_state())
        self.assertEqual([r["id"] for r in restored.unresolved()], ["AC-001"])
        self.assertEqual(restored.concerns["AC-001"]["remedy"]["status"], "open")
        self.assertEqual(raised(restored, home="H2"), "AC-002")

    def test_snapshot_is_a_copy(self) -> None:
        reg = self._populated()
        reg.to_state()["concerns"]["AC-001"]["owner"] = "Someone Else"
        self.assertEqual(reg.concerns["AC-001"]["owner"], OWNER)

    def test_restore_refuses_a_snapshot_that_weakens_a_concern(self) -> None:
        state = self._populated().to_state()
        bad = deepcopy(state)
        bad["concerns"]["AC-001"]["dismissed_by_sensor"] = True
        with self.assertRaises(ValueError):
            AftercareRegister.from_state(bad)
        bad = deepcopy(state)
        bad["concerns"]["AC-001"]["outcome"]["basis"] = "sensor_reading"
        with self.assertRaises(ValueError):
            AftercareRegister.from_state(bad)
        bad = deepcopy(state)
        bad["concerns"]["AC-001"]["outcome"] = None
        with self.assertRaises(ValueError):
            AftercareRegister.from_state(bad)
        bad = deepcopy(state)
        bad["packs"]["PK-001"]["concern_id"] = "AC-009"
        with self.assertRaises(ValueError):
            AftercareRegister.from_state(bad)

    def test_from_state_refuses_non_neutral_concern_closure_and_pack_fields(self) -> None:
        reg = self._populated()
        reg.set_remedy("AC-001", OWNER, "completed", "Draught strip fitted and checked.")
        reg.review_pack("PK-001", OWNER, "accept", "Useful factual checklist for home visit.")
        state = reg.to_state()
        mutations: list[Callable[[dict[str, Any]], object]] = [
            lambda s: s["concerns"]["AC-001"].__setitem__("owner", "Owner blaming resident"),
            lambda s: s["concerns"]["AC-001"].__setitem__(
                "accessible_route", "You will save money by calling."
            ),
            lambda s: s["concerns"]["AC-001"]["sensor_context"].__setitem__(
                "note", "caused by drying laundry"
            ),
            lambda s: s["concerns"]["AC-001"]["outcome"].__setitem__(
                "evidence", "Not opening windows caused mould."
            ),
            lambda s: s["concerns"]["AC-001"]["remedy"].__setitem__(
                "evidence", "Upgrade pays for itself."
            ),
            lambda s: s["closures"][0].__setitem__("owner", "Lead promising energy savings"),
            lambda s: s["packs"]["PK-001"].__setitem__(
                "ai_summary", "Higher bills are the resident's fault."
            ),
            lambda s: s["packs"]["PK-001"]["recorded_facts"].__setitem__(
                0, "The retrofit caused the damp."
            ),
            lambda s: s["packs"]["PK-001"]["review"].__setitem__(
                "reason", "Saves money next winter."
            ),
        ]
        for idx, mutate in enumerate(mutations):
            with self.subTest(mutation=idx):
                bad = deepcopy(state)
                mutate(bad)
                with self.assertRaises(ValueError):
                    AftercareRegister.from_state(bad)

    def _register_of(self, count: int) -> AftercareRegister:
        reg = AftercareRegister()
        for _ in range(count):
            raised(reg)
        return reg

    def test_restore_is_numeric_whatever_the_json_key_order(self) -> None:
        for count in (999, 1000, 1001):
            with self.subTest(count=count):
                state = self._register_of(count).to_state()
                text_sorted = json.loads(json.dumps(state, sort_keys=True))
                restored = AftercareRegister.from_state(text_sorted)
                self.assertEqual(
                    list(restored.concerns), [f"AC-{n:03d}" for n in range(1, count + 1)]
                )
                self.assertEqual(raised(restored), f"AC-{count + 1:03d}")
                reversed_state = deepcopy(state)
                reversed_state["concerns"] = dict(reversed(list(state["concerns"].items())))
                self.assertEqual(
                    list(AftercareRegister.from_state(reversed_state).concerns),
                    list(restored.concerns)[:count],
                )

    def test_restore_still_refuses_gaps_and_non_canonical_identifiers_past_999(self) -> None:
        state = self._register_of(1001).to_state()
        for label, drop, rename in (
            ("gap", "AC-500", None),
            ("unpadded", "AC-501", "AC-0501"),
            ("foreign", "AC-1001", "AC-X"),
        ):
            with self.subTest(label):
                bad = deepcopy(state)
                moved = bad["concerns"].pop(drop)
                if rename:
                    bad["concerns"][rename] = moved
                with self.assertRaises(ValueError):
                    AftercareRegister.from_state(bad)
        bad = deepcopy(state)
        bad["concerns"]["AC-1000"]["id"] = "AC-1001"
        with self.assertRaises(ValueError):
            AftercareRegister.from_state(bad)


if __name__ == "__main__":
    unittest.main()
