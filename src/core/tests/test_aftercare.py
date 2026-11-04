"""Aftercare concern route and evaluator view on constructed records (FR-049, AC-063, #133)."""

import unittest

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
        before = reg.view(cid) | {"history": before["history"]}
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
        self.assertEqual(after["investigation"], "received")
        self.assertIsNone(after["outcome"])
        self.assertEqual(after["remedy"], before["remedy"])
        self.assertIn(cid, [r["id"] for r in reg.unresolved()])

    def test_pack_is_a_registered_unapproved_task(self) -> None:
        from zava_forward.core import ai_registry

        task = ai_registry.get(af.PACK_TASK)  # type: ignore[no-untyped-call]
        assert task is not None
        self.assertEqual(task["approval_state"], ai_registry.UNAPPROVED)
        self.assertEqual(task["kind"], "proposal-pack")
        live = ai_registry.authorizes_live(af.PACK_TASK)  # type: ignore[no-untyped-call]
        self.assertFalse(live)
        self.assertIn("no model call", task["manual_route"])


if __name__ == "__main__":
    unittest.main()
