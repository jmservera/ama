import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core import gates
from zava_forward.core.store import READY_STAGE, GateError, Store

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


class AdvanceBookingGateTests(unittest.TestCase):
    """Store.advance must call require_booking_gates and fail closed."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        self.user = data["staff"][0]
        path.write_text(json.dumps(data))
        self.store: Any = Store(str(path))  # type: ignore[no-untyped-call]
        for name in ("gate_reasons", "require_safety_clear", "require_resident_clear"):
            patcher = patch.object(
                self.store, name, return_value=[] if name == "gate_reasons" else None
            )
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch("zava_forward.core.store.buildings.blockers", return_value=[])
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch("zava_forward.core.store.resident_gate", return_value=[])
        patcher.start()
        self.addCleanup(patcher.stop)
        with self.store.lock:
            case = self.store._case("ZF-3")  # type: ignore[no-untyped-call]
            case["stage"] = READY_STAGE
            case["funding_ok"] = True
            case["hazards"] = []

    def mutate(self, **fields: Any) -> None:
        with self.store.lock:
            case = self.store._case("ZF-3")
            for key, value in fields.items():
                if value is KeyError:
                    case.pop(key, None)
                else:
                    case[key] = value

    def assert_blocked(self) -> None:
        with self.assertRaises(GateError) as ctx:
            self.store.advance(self.user, "ZF-3")
        reason = str(ctx.exception)
        self.assertIn("Owner:", reason)
        self.assertIn("Next action:", reason)
        self.assertEqual(self.store._case("ZF-3")["stage"], READY_STAGE)

    def test_funding_missing_none_or_non_bool_blocks(self) -> None:
        for value in (KeyError, None, "yes", 1, False):
            with self.subTest(funding=value):
                self.mutate(funding_ok=value)
                self.assert_blocked()

    def test_malformed_hazards_block(self) -> None:
        values: list[Any] = ["none", None, {}, KeyError, [{}], ["x"]]
        for value in values:
            with self.subTest(hazards=value):
                self.mutate(hazards=value)
                self.assert_blocked()

    def test_advance_without_booking_gate_call_is_detected(self) -> None:
        self.mutate(funding_ok=None)
        with patch.object(self.store, "require_booking_gates") as spy:
            try:
                self.store.advance(self.user, "ZF-3")
            except Exception:
                pass
        spy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
