import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dataset import DATA, supplied_resident_fixture
from test_quality_procurement import EVIDENCE, QUIL, QUIN, SAM, STAFF
from zava_forward.core import gates
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


if __name__ == "__main__":
    unittest.main()
