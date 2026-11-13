import copy
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from typing import Any

from dataset import DATA, supplied_resident_fixture
from test_quality_procurement import EVIDENCE, QUIL, QUIN, SAM, STAFF
from zava_forward.core import gates
from zava_forward.core.finance import _fin
from zava_forward.core.grants import require_authority
from zava_forward.core.quality import CHECKLISTS, evidence_gaps, handover_blockers
from zava_forward.core.store import GateError, Store

RULE = gates.GateRule("resident", "BRD RULE-002", "2026-01-01", "1", "Reviewer A")


def run(state: Any, **kw: Any) -> gates.GateResult:
    return gates.check(
        RULE,
        state,
        owner="Resident Liaison Officer",
        correction="Record the decision.",
        label="Resident decision",
        on="2026-11-03",
        **kw,
    )


def full_labels() -> list[str]:
    return list(CHECKLISTS["Loft insulation"]["items"])


class GateTests(unittest.TestCase):
    def test_outcomes_have_reasons(self) -> None:
        self.assertEqual(run(True).outcome, gates.PASS)
        self.assertEqual(run(False).outcome, gates.FAIL)
        for r in (run(True), run(False), run(None)):
            self.assertTrue(r.reason)
            self.assertEqual(r.rule, RULE)

    def test_unknown_never_passes(self) -> None:
        states: tuple[Any, ...] = (None, "yes", 1, [], {})
        for state in states:
            self.assertEqual(run(state).outcome, gates.UNKNOWN)
        self.assertFalse(gates.transition_allowed([run(True), run(None)]))
        self.assertFalse(gates.transition_allowed([]))
        self.assertTrue(gates.transition_allowed([run(True)]))

    def test_rule_not_yet_effective_is_unknown(self) -> None:
        future = gates.GateRule("funding", "src", "2027-01-01", "1", "R")
        r = gates.check(future, True, owner="o", correction="c", label="Funding", on="2026-11-03")
        self.assertEqual(r.outcome, gates.UNKNOWN)

    def test_rule_metadata_required(self) -> None:
        with self.assertRaises(ValueError):
            gates.GateRule("g", "", "2026-01-01", "1", "R")
        with self.assertRaises(ValueError):
            gates.GateRule("g", "s", "01/01/2026", "1", "R")
        self.assertEqual(
            set(run(True).as_record()["rule"]),
            {"gate", "source", "effective_date", "version", "reviewer"},
        )

    def test_safety_release(self) -> None:
        hold = {"accountable_role": "Building Safety Liaison"}
        ok = {"role": "Building Safety Liaison", "email": "b@x.test"}
        self.assertEqual(
            gates.safety_release_gate(hold, ok, ["a@x.test"], on="2026-11-03").outcome, gates.PASS
        )
        wrong = dict(ok, role="Retrofit Programme Manager")
        self.assertEqual(gates.safety_release_gate(hold, wrong, []).outcome, gates.FAIL)
        self.assertEqual(gates.safety_release_gate(hold, ok, ["B@X.test"]).outcome, gates.FAIL)
        self.assertEqual(gates.safety_release_gate({}, ok, []).outcome, gates.UNKNOWN)
        self.assertEqual(
            gates.safety_release_gate(hold, {"role": hold["accountable_role"]}, []).outcome,
            gates.UNKNOWN,
        )

    def test_booking_gates(self) -> None:
        good = {"funding_ok": True, "hazards": [{"released": True}], "owner": "Sam"}
        by = {r.gate: r for r in gates.booking_gates(good, [], on="2026-11-04")}
        self.assertEqual({r.outcome for r in by.values()}, {gates.PASS})
        self.assertTrue(gates.transition_allowed(by.values()))
        for r in by.values():
            self.assertIsNotNone(r.rule)

    def test_booking_gates_fail_and_unknown(self) -> None:
        def out(case: dict[str, Any], reasons: list[str] | None) -> dict[str, str]:
            return {r.gate: r.outcome for r in gates.booking_gates(case, reasons, on="2026-11-04")}

        open_hold = {"funding_ok": False, "hazards": [{"released": False}]}
        self.assertEqual(
            out(open_hold, ["x"]), {"funding": "fail", "safety": "fail", "resident": "fail"}
        )
        missing = out({"funding_ok": "yes"}, None)
        self.assertEqual(set(missing.values()), {gates.UNKNOWN})
        results = gates.booking_gates({}, None, on="2026-11-04")
        self.assertFalse(gates.transition_allowed(results))
        self.assertEqual(len(gates.unmet(results)), 3)
        malformed = out({"funding_ok": True, "hazards": [{}]}, [])
        self.assertEqual(malformed["safety"], gates.FAIL)

    def test_evidence_gate(self) -> None:
        ok = gates.evidence_gate([], "Grants Officer", on="2026-11-04")
        self.assertEqual(ok.outcome, gates.PASS)
        bad = gates.evidence_gate(["EPC", "Survey"], "Grants Officer", on="2026-11-04")
        self.assertEqual(bad.outcome, gates.FAIL)
        self.assertIn("EPC, Survey", bad.reason)
        unknown = gates.evidence_gate(None, "Grants Officer", on="2026-11-04")
        self.assertEqual(unknown.outcome, gates.UNKNOWN)
        self.assertFalse(gates.transition_allowed([ok, unknown]))
        self.assertIsNotNone(bad.rule)

    def test_store_evidence_missing_is_unknown_when_malformed(self) -> None:
        self.assertIsNone(Store._evidence_missing({}))
        self.assertEqual(
            Store._evidence_missing({"documents": [{"kind": "EPC"}]}),
            ["Survey", "Design", "Consent"],
        )

    def test_booking_refused_when_evidence_missing_or_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "zavaforward.json"
            path.write_text(json.dumps(DATA))
            store: Any = Store(str(path))  # type: ignore[no-untyped-call]
            for documents, expected in (
                ([], "EPC, Survey, Design, Consent"),
                ([{"kind": "EPC"}], "Survey, Design, Consent"),
                ([{}], None),
            ):
                case = copy.deepcopy(store._case("ZF-3"))
                case["documents"] = documents
                with self.assertRaises(GateError) as ctx:
                    store.require_booking_gates(case)
                reasons = str(ctx.exception)
                self.assertIn("Grants and Evidence Officer", reasons)
                if expected:
                    self.assertIn(expected, reasons)


class FundingReadinessTests(unittest.TestCase):
    """Missing or non-boolean funding is denied with a funding reason, not a lookup error."""

    def make(self, funding: Any, *, absent: bool = False) -> Any:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"] = STAFF
        for c in data["cases"]:
            if c["id"] == "ZF-3":
                supplied_resident_fixture(c)
                if absent:
                    del c["funding_ok"]
                else:
                    c["funding_ok"] = funding
        path = Path(tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(data))
        return Store(str(path))  # type: ignore[no-untyped-call]

    def funding_reasons(self, store: Any) -> list[str]:
        reasons = Store.gate_reasons(store.cases["ZF-3"])  # type: ignore[no-untyped-call]
        return [r for r in reasons if "Funding" in r]

    def test_only_explicit_true_reads_as_ready(self) -> None:
        store = self.make(True)
        self.assertEqual(self.funding_reasons(store), [])
        self.assertEqual(
            Store.status_line(store.cases["ZF-3"]),  # type: ignore[no-untyped-call]
            "Ready",
        )

    def test_unconfirmed_funding_reads_as_denied_with_reason(self) -> None:
        for funding, absent in (
            (None, False),
            (False, False),
            ("yes", False),
            (1, False),
            (None, True),
        ):
            with self.subTest(funding=funding, absent=absent):
                store = self.make(funding, absent=absent)
                case = store.cases["ZF-3"]
                self.assertEqual(len(self.funding_reasons(store)), 1)
                self.assertNotEqual(
                    Store.status_line(case),  # type: ignore[no-untyped-call]
                    "Ready",
                )
                self.assertEqual(
                    [r for r in store.detail("ZF-3")["gate"] if "Funding" in r],
                    self.funding_reasons(store),
                )
                with self.assertRaises(GateError) as ctx:
                    store.advance(STAFF[0], "ZF-3")
                self.assertIn("Funding", str(ctx.exception))
                self.assertEqual(store.cases["ZF-3"]["stage"], "Final checks before ordering")


class QualityGateTests(unittest.TestCase):
    def test_quality_gate_outcomes_and_rule(self) -> None:
        ok = gates.quality_gate([], "Quality Inspector", on="2026-11-05")
        self.assertEqual(ok.outcome, gates.PASS)
        bad = gates.quality_gate(
            ["Guarantee issued", "Photos"], "Quality Inspector", on="2026-11-05"
        )
        self.assertEqual(bad.outcome, gates.FAIL)
        self.assertIn("Guarantee issued; Photos", bad.reason)
        unknown = gates.quality_gate(None, "Quality Inspector", on="2026-11-05")
        self.assertEqual(unknown.outcome, gates.UNKNOWN)
        early = gates.quality_gate([], "Quality Inspector", on="2026-11-04")
        self.assertEqual(early.outcome, gates.UNKNOWN)
        self.assertFalse(gates.transition_allowed([ok, unknown]))
        record = bad.as_record()["rule"]
        self.assertEqual(record["gate"], "quality")
        self.assertEqual(record["effective_date"], "2026-11-05")
        self.assertIn("Unreviewed", record["reviewer"])
        self.assertIn(
            "docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-008", record["source"]
        )
        self.assertNotIn("brd.md FR-008", record["source"])

    def test_evidence_gaps_unreadable_is_none(self) -> None:
        full = [dict(label=x, evidence="seen") for x in CHECKLISTS["Loft insulation"]["items"]]
        base: dict[str, Any] = dict(measure="Loft insulation", checklist="Loft insulation")
        self.assertEqual(evidence_gaps(dict(base, items=full)), [])  # type: ignore[no-untyped-call]
        self.assertEqual(evidence_gaps(dict(base, items=full[:3])), full_labels()[3:])  # type: ignore[no-untyped-call]
        for items in (None, "text", [None], [dict(label="x")] + ["y"]):
            self.assertIsNone(evidence_gaps(dict(base, items=items)))  # type: ignore[no-untyped-call]
        blank = [dict(full[0], evidence="  ")] + full[1:]
        self.assertEqual(evidence_gaps(dict(base, items=blank)), full_labels()[:1])  # type: ignore[no-untyped-call]
        non_text = [dict(full[0], evidence=7)] + full[1:]
        self.assertEqual(evidence_gaps(dict(base, items=non_text)), full_labels()[:1])  # type: ignore[no-untyped-call]

    def make(self) -> Any:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"] = STAFF
        for c in data["cases"][:2]:
            supplied_resident_fixture(c)
        path = Path(tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(data))
        return Store(str(path))  # type: ignore[no-untyped-call]

    def submit(self, store: Any) -> dict[str, Any]:
        store.submit_quality(
            SAM,
            "ZF-1",
            "Loft insulation",
            "Install Team",
            "Installer",
            EVIDENCE,
            context_revision=1,
        )
        rec: dict[str, Any] = store.cases["ZF-1"]["quality"][0]
        return rec

    def test_accept_refused_for_missing_or_unreadable_evidence(self) -> None:
        for damage in (
            lambda r: r["items"][0].update(evidence=""),
            lambda r: r["items"].pop(),
            lambda r: r.update(items=[]),
            lambda r: r.update(items=None),
            lambda r: r.update(items="unreadable"),
            lambda r: r["items"][1].update(evidence=7),
        ):
            store = self.make()
            rec = self.submit(store)
            damage(rec)  # type: ignore[no-untyped-call]
            before = copy.deepcopy(rec)
            with self.assertRaises(GateError) as ctx:
                store.accept_quality(QUIL, "ZF-1", 0)
            self.assertIn("Quality Inspector", str(ctx.exception))
            self.assertEqual(store.cases["ZF-1"]["quality"][0], before)
            self.assertEqual(before["state"], "Submitted")

    def test_handover_refused_when_accepted_evidence_is_missing(self) -> None:
        store = self.make()
        rec = self.submit(store)
        store.accept_quality(QUIL, "ZF-1", 0)
        rec["items"][0]["evidence"] = ""
        with self.assertRaises(GateError):
            store.hand_over_quality(SAM, "ZF-1", 0, "Guarantee given", True)
        rec = store.cases["ZF-1"]["quality"][0]
        self.assertEqual(rec["state"], "Accepted")
        rec["items"][0]["evidence"] = "seen again"
        store.hand_over_quality(SAM, "ZF-1", 0, "Guarantee given", True)
        self.assertEqual(store.cases["ZF-1"]["quality"][0]["state"], "Handed over")

    def test_accepted_record_with_missing_evidence_recovers_by_supersession(self) -> None:
        store = self.make()
        self.submit(store)
        store.accept_quality(QUIL, "ZF-1", 0)
        store.cases["ZF-1"]["quality"][0]["items"][0]["evidence"] = ""
        with self.assertRaises(GateError):
            store.hand_over_quality(SAM, "ZF-1", 0, "Guarantee given", True)
        self.submit(store)
        states = [q["state"] for q in store.cases["ZF-1"]["quality"]]
        self.assertEqual(states, ["Superseded", "Submitted"])
        store.accept_quality(QUIN, "ZF-1", 1)

    def corrupted(self, state: str) -> tuple[Any, dict[str, Any]]:
        store = self.make()
        rec = self.submit(store)
        if state != "Submitted":
            store.return_quality(QUIN, "ZF-1", 0, "Gap", "Missing check", "Test Ltd")
        if state == "Fixed, awaiting reinspection":
            store.record_fix(QUIN, "ZF-1", 0, "Install Team", "Corrected, ref 1")
        rec["items"][0]["evidence"] = ""
        return store, rec

    def replace(self, store: Any, user: Any = QUIN, items: Any = EVIDENCE) -> None:
        store.submit_quality(
            user, "ZF-1", "Loft insulation", "Install Team", "Installer", items, context_revision=1
        )

    def test_corrupted_in_progress_record_is_replaced_with_originals_kept(self) -> None:
        for state in ("Submitted", "Returned", "Fixed, awaiting reinspection"):
            store, rec = self.corrupted(state)
            original = copy.deepcopy(store.cases["ZF-1"]["quality"][0])
            if state != "Returned":
                with self.assertRaises(GateError):
                    store.accept_quality(QUIL, "ZF-1", 0)
            self.replace(store)
            rows = store.cases["ZF-1"]["quality"]
            self.assertEqual([r["state"] for r in rows], ["Superseded", "Submitted"], state)
            self.assertEqual(rows[0]["items"], original["items"])
            self.assertEqual(rows[0]["defects"], original["defects"])
            self.assertEqual(rows[1]["supersedes"], [0])
            self.assertEqual(rows[0]["history"][-1]["to_state"], "Superseded")
            self.assertEqual(rows[0]["history"][: len(original["history"])], original["history"])
            self.assertNotIn("accepted_by", rows[1])
            with self.assertRaises(PermissionError):
                store.accept_quality(QUIN, "ZF-1", 1)
            store.accept_quality(QUIL, "ZF-1", 1)
            self.assertEqual(store.cases["ZF-1"]["quality"][1]["state"], "Accepted")

    def test_unreadable_in_progress_items_are_replaceable(self) -> None:
        store, rec = self.corrupted("Submitted")
        rec["items"] = "unreadable"
        self.replace(store)
        self.assertEqual(store.cases["ZF-1"]["quality"][0]["items"], "unreadable")
        self.assertEqual(store.cases["ZF-1"]["quality"][1]["state"], "Submitted")

    def test_replacement_boundaries_hold(self) -> None:
        store, _ = self.corrupted("Submitted")
        with self.assertRaises(PermissionError):
            self.replace(store, user=SAM)
        partial = dict(EVIDENCE)
        partial.pop(next(iter(partial)))
        with self.assertRaises(ValueError):
            self.replace(store, items=partial)
        self.assertEqual(len(store.cases["ZF-1"]["quality"]), 1)
        self.assertEqual(store.cases["ZF-1"]["quality"][0]["state"], "Submitted")
        valid = self.make()
        self.submit(valid)
        with self.assertRaises(ValueError):
            self.replace(valid)
        self.assertEqual(len(valid.cases["ZF-1"]["quality"]), 1)

    def test_complete_evidence_still_accepts_and_wrong_state_error_is_unchanged(self) -> None:
        store = self.make()
        rec = self.submit(store)
        rec["items"][0]["evidence"] = ""
        store.return_quality(QUIN, "ZF-1", 0, "Gap", "Missing check", "Test Ltd")
        with self.assertRaises(ValueError):
            store.accept_quality(QUIL, "ZF-1", 0)
        with self.assertRaises(ValueError):
            store.hand_over_quality(SAM, "ZF-1", 0, "x", True)
        clean = self.make()
        self.submit(clean)
        clean.accept_quality(QUIL, "ZF-1", 0)
        self.assertEqual(clean.cases["ZF-1"]["quality"][0]["state"], "Accepted")

    def test_handover_blockers_agree_with_the_gate(self) -> None:
        store = self.make()
        rec = self.submit(store)
        store.accept_quality(QUIL, "ZF-1", 0)
        rec["items"] = None
        reasons = [b["reason"] for b in handover_blockers(store.cases["ZF-1"])]  # type: ignore[no-untyped-call]
        self.assertTrue(any("no evidence recorded" in r for r in reasons), reasons)


class ControlledRuleRegistryTests(unittest.TestCase):
    def test_every_gate_kind_has_a_rule_with_full_metadata(self) -> None:
        self.assertEqual({r.gate for r in gates.CONTROLLED_RULES}, set(gates.GATE_KINDS))
        for rule in gates.CONTROLLED_RULES:
            record = rule.as_record()
            with self.subTest(gate=rule.gate, source=rule.source):
                self.assertTrue(all(isinstance(v, str) and v.strip() for v in record.values()))
                self.assertEqual(
                    date.fromisoformat(rule.effective_date).isoformat(), rule.effective_date
                )

    def test_unreviewed_rules_are_reported_until_a_reviewer_is_named(self) -> None:
        self.assertEqual(set(gates.unreviewed_rules()), set(gates.CONTROLLED_RULES))

    def test_new_gates_never_pass_without_explicit_evidence(self) -> None:
        results = [
            gates.eligibility_gate(None, "No eligibility check is recorded.", "Grants Officer"),
            gates.authority_gate(None, "Designation unreadable."),
            gates.finance_gate(None, "Budget unreadable."),
        ]
        self.assertTrue(all(r.outcome == gates.UNKNOWN and r.reason for r in results))
        self.assertFalse(gates.transition_allowed(results))
        self.assertEqual(gates.finance_gate(False, "Over budget.").outcome, gates.FAIL)
        for gate in (
            gates.eligibility_gate(True, "x", "Grants Officer"),
            gates.authority_gate(True, "x"),
            gates.finance_gate(True, "x"),
        ):
            self.assertEqual(gate.outcome, gates.PASS)
        early = gates.finance_gate(True, "x", on="2026-11-12")
        self.assertEqual(early.outcome, gates.UNKNOWN)


Store_any: Any = Store
fin_any: Any = _fin
require_authority_any: Any = require_authority


class FinanceAuthorityWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        from test_grant_lifecycle_controls import designate

        self.tmp = tempfile.TemporaryDirectory()
        data = copy.deepcopy(DATA)
        data["staff"] = [
            designate(
                dict(
                    code="GEO-1",
                    name="G",
                    email="geo@example.test",
                    role="Grants and Evidence Officer",
                )
            ),
            dict(code="PM-1", name="P", email="pm@example.test", role="Retrofit Programme Manager"),
        ]
        path = Path(self.tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(data))
        self.store: Any = Store_any(str(path))
        self.geo, self.pm = data["staff"]
        self.raise_args = dict(
            action="commit_raise",
            supplier="S",
            contract="C",
            work_order="W",
            measure="Loft insulation",
            amount=100,
            quantity=1,
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def raise_commit(self) -> None:
        self.store.finance_action(self.geo, "ZF-1", self.raise_args)

    def budget(self, status: Any, amount: Any = 1000) -> None:
        with self.store.lock:
            fin_any(self.store.cases["ZF-1"])["budget"] = (
                status if not isinstance(status, str) else dict(amount=amount, status=status)
            )

    def test_commitment_gate_distinguishes_fail_from_unknown_and_never_mutates(self) -> None:
        cases = [
            (None, gates.FAIL, "A commitment needs an approved budget first."),
            ("Proposed", gates.FAIL, "A commitment needs an approved budget first."),
            ("Approved", gates.FAIL, "That is more than the budget left"),
            (["unreadable"], gates.UNKNOWN, "cannot be read"),
        ]
        for budget, outcome, text in cases:
            amount = 50 if text.startswith("That") else 1000
            with self.subTest(budget=budget, text=text):
                self.budget(budget, amount)
                with self.assertRaises(gates.FinanceGateError) as caught:
                    self.raise_commit()
                self.assertEqual(caught.exception.result.outcome, outcome)
                self.assertIn(text, str(caught.exception))
                self.assertEqual(fin_any(self.store.cases["ZF-1"])["commitments"], [])
        self.budget("Approved", "not a number")
        with self.assertRaises(gates.FinanceGateError) as caught:
            self.raise_commit()
        self.assertEqual(caught.exception.result.outcome, gates.UNKNOWN)

    def test_commitment_within_an_approved_budget_still_passes(self) -> None:
        self.budget("Approved")
        self.raise_commit()
        self.assertEqual(len(fin_any(self.store.cases["ZF-1"])["commitments"]), 1)

    def test_authority_refusals_are_gate_results(self) -> None:
        args = (self.store, self.geo, "grant:Opportunity", "ZF-1", "SYN-95")
        self.assertEqual(require_authority_any(*args)["status"], "Active")
        for field, value, outcome in (
            ("status", "Revoked", gates.FAIL),
            ("expires_at", "not-a-date", gates.UNKNOWN),
            ("permissions", [], gates.UNKNOWN),
        ):
            user = copy.deepcopy(self.geo)
            user["financial_authority"][field] = value
            self.store.staff[user["email"]] = user
            with self.subTest(field=field), self.assertRaises(gates.AuthorityGateError) as caught:
                require_authority_any(self.store, user, "grant:Opportunity", "ZF-1", "SYN-95")
            self.assertEqual(caught.exception.result.outcome, outcome)
            self.assertIn("Current scoped human financial designation", str(caught.exception))
        self.store.staff[self.pm["email"]] = self.pm
        with self.assertRaises(gates.AuthorityGateError) as caught:
            require_authority_any(self.store, self.pm, "grant:Opportunity", "ZF-1", "SYN-95")
        self.assertEqual(caught.exception.result.outcome, gates.UNKNOWN)


class GateBoundaryTests(unittest.TestCase):
    def assertSafe(self, result: gates.GateResult, outcomes: tuple[str, ...]) -> None:
        self.assertIn(result.outcome, outcomes)
        self.assertTrue(isinstance(result.reason, str) and result.reason.strip())

    def test_non_string_or_non_iterable_items_are_unknown(self) -> None:
        shapes: list[Any] = [[None], [1], ["ok", 2], 5, "text", [""]]
        for bad in shapes:
            with self.subTest(bad=bad):
                self.assertSafe(gates.evidence_gate(bad, "Owner"), (gates.UNKNOWN,))
                self.assertSafe(gates.quality_gate(bad, "Owner"), (gates.UNKNOWN,))
                self.assertSafe(gates.booking_gates({}, bad)[2], (gates.UNKNOWN,))
        self.assertSafe(gates.evidence_gate(["loft"], "Owner"), (gates.FAIL,))
        self.assertTrue(gates.evidence_gate([], "Owner", on="2026-12-01").passed)

    def test_blank_or_non_string_reasons_never_raise(self) -> None:
        for bad in ("", "  ", None, 5, ["x"]):
            for state in (None, False):
                with self.subTest(bad=bad, state=state):
                    for result in (
                        gates.eligibility_gate(state, bad, "Owner"),  # type: ignore[arg-type]
                        gates.authority_gate(state, bad),  # type: ignore[arg-type]
                        gates.finance_gate(state, bad),  # type: ignore[arg-type]
                        gates.capacity_gate(state, bad),  # type: ignore[arg-type]
                    ):
                        self.assertSafe(result, (gates.UNKNOWN, gates.FAIL))
        for err in (gates.FinanceGateError("", None), gates.AuthorityGateError(" ", False)):
            self.assertTrue(err.result.reason.strip())

    def test_safety_release_malformed_inputs_are_unknown(self) -> None:
        hold = {"accountable_role": "Building Safety Liaison"}
        actor = {"role": "Building Safety Liaison", "email": "a@x.test", "code": "A", "oid": "o"}
        shapes: list[Any] = [None, 5, "a@x.test", [3], [["x"]]]
        for bad in shapes:
            with self.subTest(recorders=bad):
                self.assertSafe(gates.safety_release_gate(hold, actor, bad), (gates.UNKNOWN,))
        for who in ({**actor, "oid": 0}, {**actor, "code": []}, {**actor, "email": 7}):
            with self.subTest(actor=who):
                self.assertSafe(
                    gates.safety_release_gate(hold, who, ["b@x.test"]), (gates.UNKNOWN,)
                )
        self.assertSafe(gates.safety_release_gate(hold, actor, ["b@x.test"]), (gates.PASS,))


if __name__ == "__main__":
    unittest.main()
