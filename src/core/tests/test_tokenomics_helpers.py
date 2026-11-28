"""Direct tests for the fail-closed and privacy helpers behind AI consumption economics."""

from __future__ import annotations

import unittest
from decimal import Decimal
from typing import Any

from zava_forward.core import tokenomics

UNKNOWN = tokenomics.UNKNOWN


class MoneyAndRatioTest(unittest.TestCase):
    def test_non_positive_money_and_ratio_report_unknown_never_zero(self) -> None:
        self.assertEqual(tokenomics._positive_money_str(Decimal("0")), UNKNOWN)
        self.assertEqual(tokenomics._positive_money_str(Decimal("-1")), UNKNOWN)
        self.assertEqual(tokenomics._ratio_str(Decimal("0"), 3), UNKNOWN)
        self.assertEqual(tokenomics._ratio_str(Decimal("1"), 0), UNKNOWN)
        self.assertEqual(tokenomics._ratio_str(Decimal("-1"), 2), UNKNOWN)

    def test_positive_values_use_plain_decimal_notation(self) -> None:
        self.assertEqual(tokenomics._positive_money_str(Decimal("1E-7")), "0.0000001")
        self.assertEqual(tokenomics._ratio_str(Decimal("1"), 4), "0.25")


class SanitiserTest(unittest.TestCase):
    def test_owner_never_leaks_email_or_whitespace(self) -> None:
        self.assertEqual(tokenomics._sanitize_owner("a.b@example.org"), "configured-owner")
        self.assertEqual(tokenomics._sanitize_owner("finance lead"), "configured-owner")
        self.assertEqual(tokenomics._sanitize_owner("   "), "unassigned")
        self.assertEqual(tokenomics._sanitize_owner(None), "unassigned")
        self.assertEqual(tokenomics._sanitize_owner(" finance-lead "), "finance-lead")

    def test_code_falls_back_for_unsafe_or_missing_values(self) -> None:
        self.assertEqual(tokenomics._sanitize_code("x@y", "audit-log"), "audit-log")
        self.assertEqual(tokenomics._sanitize_code("bad value", "audit-log"), "audit-log")
        self.assertEqual(tokenomics._sanitize_code(7, "audit-log"), "audit-log")
        self.assertEqual(tokenomics._sanitize_code("pager:ops", "audit-log"), "pager:ops")

    def test_capability_names_are_normalised_or_defaulted(self) -> None:
        self.assertEqual(tokenomics._capability_name(" Draft Letter "), "draft-letter")
        self.assertEqual(tokenomics._capability_name("../etc"), "unspecified")
        self.assertEqual(tokenomics._capability_name(None, default="priority"), "priority")


class TimestampTest(unittest.TestCase):
    def test_accepted_forms_normalise_to_the_same_utc_epoch(self) -> None:
        epoch = 1_700_000_000.0
        self.assertEqual(tokenomics.parse_record_timestamp(epoch), epoch)
        self.assertEqual(
            tokenomics.parse_record_timestamp("2023-11-14T22:13:20Z"),
            tokenomics.parse_record_timestamp("2023-11-14T22:13:20"),
        )
        self.assertEqual(tokenomics.parse_record_timestamp("2023-11-14T23:13:20+01:00"), epoch)
        self.assertEqual(tokenomics.parse_record_timestamp("2023-11-14"), 1_699_920_000.0)

    def test_invalid_values_return_none(self) -> None:
        for bad in (None, True, -1, "", "  ", "2023-13-45", "yesterday", ["2023-11-14"]):
            with self.subTest(bad=bad):
                self.assertIsNone(tokenomics.parse_record_timestamp(bad))

    def test_bound_timestamp_rejects_unsupported_types(self) -> None:
        self.assertIsNone(tokenomics._bound_timestamp(None, "start"))
        with self.assertRaises(ValueError):
            tokenomics._bound_timestamp(["x"], "start")


def _unpriced_summary() -> dict[str, Any]:
    zero = {key: 0 for key in tokenomics.DENOMINATOR_KEYS}
    money = {
        "token_cost": UNKNOWN,
        "total_cost_of_ai": UNKNOWN,
        "token_cost_per_accepted_outcome": UNKNOWN,
        "cost_per_accepted_outcome": UNKNOWN,
        "quality_qualified_cost_per_accepted_outcome": UNKNOWN,
        "booked_value": UNKNOWN,
    }
    return {
        **zero,
        **money,
        "denominators": dict(zero),
        "price_source_configured": False,
        "od_51_status": "open",
        "other_tca_components": {},
        "by_capability": {},
    }


class InvariantNegativeTest(unittest.TestCase):
    def test_unpriced_zero_state_passes(self) -> None:
        tokenomics.assert_tokenomics_invariants(_unpriced_summary())

    def test_zero_or_numeric_cost_is_rejected(self) -> None:
        for bad in ("0.00", 0, None, ""):
            summary = _unpriced_summary()
            summary["token_cost"] = bad
            with self.subTest(bad=bad), self.assertRaises(AssertionError):
                tokenomics.assert_tokenomics_invariants(summary)

    def test_priced_flag_with_open_decision_or_denominator_mismatch_is_rejected(self) -> None:
        summary = _unpriced_summary()
        summary["price_source_configured"] = True
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(summary)
        summary = _unpriced_summary()
        summary["denominators"]["proposal_count"] = 1
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(summary)

    def test_unpriced_known_cost_or_unit_cost_without_accepted_outcomes_is_rejected(self) -> None:
        summary = _unpriced_summary()
        summary["total_cost_of_ai"] = "1.5"
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(summary)
        summary = _unpriced_summary()
        summary["by_capability"] = {
            "draft": {
                **{key: 0 for key in tokenomics.DENOMINATOR_KEYS},
                "token_cost": UNKNOWN,
                "total_cost_of_ai": UNKNOWN,
                "token_cost_per_accepted_outcome": "2",
                "cost_per_accepted_outcome": UNKNOWN,
                "booked_value": UNKNOWN,
            }
        }
        with self.assertRaises(AssertionError):
            tokenomics.assert_tokenomics_invariants(summary)


if __name__ == "__main__":
    unittest.main()
