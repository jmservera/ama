import unittest

from zava_forward.core import gates

RULE = gates.GateRule("resident", "BRD RULE-002", "2026-01-01", "1", "Reviewer A")


def run(state, **kw):
    return gates.check(
        RULE,
        state,
        owner="Resident Liaison Officer",
        correction="Record the decision.",
        label="Resident decision",
        on="2026-11-03",
        **kw,
    )


class GateTests(unittest.TestCase):
    def test_outcomes_have_reasons(self):
        self.assertEqual(run(True).outcome, gates.PASS)
        self.assertEqual(run(False).outcome, gates.FAIL)
        for r in (run(True), run(False), run(None)):
            self.assertTrue(r.reason)
            self.assertEqual(r.rule, RULE)

    def test_unknown_never_passes(self):
        for state in (None, "yes", 1, [], {}):
            self.assertEqual(run(state).outcome, gates.UNKNOWN)
        self.assertFalse(gates.transition_allowed([run(True), run(None)]))
        self.assertFalse(gates.transition_allowed([]))
        self.assertTrue(gates.transition_allowed([run(True)]))

    def test_rule_not_yet_effective_is_unknown(self):
        future = gates.GateRule("funding", "src", "2027-01-01", "1", "R")
        r = gates.check(future, True, owner="o", correction="c", label="Funding", on="2026-11-03")
        self.assertEqual(r.outcome, gates.UNKNOWN)

    def test_rule_metadata_required(self):
        with self.assertRaises(ValueError):
            gates.GateRule("g", "", "2026-01-01", "1", "R")
        with self.assertRaises(ValueError):
            gates.GateRule("g", "s", "01/01/2026", "1", "R")
        self.assertEqual(
            set(run(True).as_record()["rule"]),
            {"gate", "source", "effective_date", "version", "reviewer"},
        )

    def test_safety_release(self):
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


if __name__ == "__main__":
    unittest.main()
