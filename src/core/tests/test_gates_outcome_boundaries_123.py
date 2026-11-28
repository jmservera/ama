"""Boundary cases for the deterministic gates (epic #123 phase gates; FR-008, RULE-001)."""

import unittest
from collections.abc import Callable, Iterator

from zava_forward.core import gates

PAST = "2099-01-01"
NOW = "2026-11-28"
FUTURE_RULE = "2099-12-31"


def _result(outcome: str) -> gates.GateResult:
    return gates.GateResult("safety", outcome, "A reason.", "Owner", "Fix it.")


class TransitionTests(unittest.TestCase):
    def test_empty_set_never_allows_a_transition(self) -> None:
        self.assertFalse(gates.transition_allowed([]))

    def test_one_non_pass_blocks_the_transition(self) -> None:
        results = [_result(gates.PASS), _result(gates.UNKNOWN), _result(gates.PASS)]
        self.assertFalse(gates.transition_allowed(results))

    def test_all_pass_allows_a_generator_input(self) -> None:
        def passing() -> Iterator[gates.GateResult]:
            yield _result(gates.PASS)
            yield _result(gates.PASS)

        self.assertTrue(gates.transition_allowed(passing()))

    def test_unmet_keeps_input_order_and_drops_passes(self) -> None:
        first, second = _result(gates.FAIL), _result(gates.UNKNOWN)
        self.assertEqual(gates.unmet([first, _result(gates.PASS), second]), [first, second])


class OutcomeGateEffectiveDateTests(unittest.TestCase):
    def gate_calls(self) -> list[Callable[[bool | None, str, str | None], gates.GateResult]]:
        return [
            gates.capacity_gate,
            lambda state, reason, on: gates.eligibility_gate(state, reason, "Grants", on),
            gates.authority_gate,
            gates.finance_gate,
        ]

    def test_true_before_the_rule_is_in_effect_is_unknown(self) -> None:
        for call in self.gate_calls():
            with self.subTest(call=call):
                result = call(True, "ignored", "2000-01-01")
                self.assertEqual(result.outcome, gates.UNKNOWN)
                self.assertFalse(result.passed)
                self.assertIn("not yet in effect", result.reason)

    def test_true_once_the_rule_is_in_effect_passes(self) -> None:
        for call in self.gate_calls():
            with self.subTest(call=call):
                self.assertTrue(call(True, "ignored", PAST).passed)

    def test_false_fails_and_none_is_unknown_whatever_the_date(self) -> None:
        for call in self.gate_calls():
            with self.subTest(call=call):
                self.assertEqual(call(False, "Over limit.", PAST).outcome, gates.FAIL)
                self.assertEqual(call(None, "Unreadable.", PAST).outcome, gates.UNKNOWN)

    def test_blank_reason_falls_back_to_plain_text(self) -> None:
        for call in self.gate_calls():
            with self.subTest(call=call):
                self.assertTrue(call(False, "   ", PAST).reason.strip())

    def test_supplied_reason_is_kept(self) -> None:
        self.assertEqual(
            gates.finance_gate(False, "Budget exhausted.", PAST).reason, "Budget exhausted."
        )


class RecordShapeTests(unittest.TestCase):
    def test_gate_rule_rejects_a_non_iso_effective_date(self) -> None:
        with self.assertRaises(ValueError):
            gates.GateRule("g", "source", "2026-1-3", "1", "reviewer")

    def test_gate_rule_rejects_a_blank_source(self) -> None:
        with self.assertRaises(ValueError):
            gates.GateRule("g", "  ", "2026-11-03", "1", "reviewer")

    def test_gate_result_rejects_an_unknown_outcome_and_blank_reason(self) -> None:
        with self.assertRaises(ValueError):
            gates.GateResult("g", "maybe", "Reason.", "Owner", "Fix.")
        with self.assertRaises(ValueError):
            gates.GateResult("g", gates.PASS, " ", "Owner", "Fix.")

    def test_result_record_embeds_the_rule_record(self) -> None:
        record = gates.finance_gate(True, "x", PAST).as_record()
        self.assertEqual(record["outcome"], gates.PASS)
        self.assertEqual(record["rule"], gates.FINANCE_RULE.as_record())

    def test_result_without_a_rule_records_none(self) -> None:
        self.assertIsNone(_result(gates.PASS).as_record()["rule"])


class RefusalErrorTests(unittest.TestCase):
    def test_refusals_keep_text_and_expose_the_gate_result(self) -> None:
        capacity = gates.CapacityGateError("No capacity.", False)
        authority = gates.AuthorityGateError("No designation.", None, PAST)
        finance = gates.FinanceGateError("No budget.", False, PAST)
        self.assertEqual(str(capacity), "No capacity.")
        self.assertEqual(capacity.result.outcome, gates.FAIL)
        self.assertEqual(authority.result.outcome, gates.UNKNOWN)
        self.assertEqual(finance.result.reason, "No budget.")

    def test_result_errors_carry_rule_and_record(self) -> None:
        result = gates.finance_gate(False, "No budget.", PAST)
        for error in (
            gates.GateResultError("Refused.", result),
            gates.GateResultPermissionError("Refused.", result),
        ):
            with self.subTest(error=type(error).__name__):
                self.assertIs(error.result, result)
                self.assertEqual(error.rule, gates.FINANCE_RULE)
                self.assertEqual(error.record, result.as_record())


if __name__ == "__main__":
    unittest.main()
