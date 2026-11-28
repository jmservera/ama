"""Issue #220 non-retaliation guard test selector and facade parity suite.

Provides the ``test_no_retaliation_guard_220`` unittest module selector covering all canonical
Issue #220 core non-retaliation suites when invoked directly, while deduplicating full-suite
``unittest discover`` runs so each heavy Store/SQLite lifecycle test executes once.
"""

from __future__ import annotations

import copy
import unittest
from typing import Any

from test_challenge_no_retaliation_220 import (
    AssistantsProposalChallengeNoRetaliationTests,
    ChallengeRegisterNoRetaliationTests,
    StoreAndSqlStoreNoRetaliationLifecycleTests,
)
from zava_forward.core import challenges, no_retaliation_guard, resident_decisions

__all__ = [
    "AssistantsProposalChallengeNoRetaliationTests",
    "ChallengeRegisterNoRetaliationTests",
    "NoRetaliationGuardFacadeTests",
    "StoreAndSqlStoreNoRetaliationLifecycleTests",
]

_EXPECTED_PUBLIC_EXPORTS = frozenset(
    {
        "ACCESSIBLE_ROUTE",
        "FORBIDDEN_ADVERSE_FIELDS",
        "NON_DIGITAL_CHANNELS",
        "NOT_INFERRED",
        "PROTECTION",
        "RESOLVED",
        "ROUTES",
        "SAFEGUARDS",
        "STATUSES",
        "SUBJECT_KINDS",
        "SUBMITTER_KINDS",
        "ChallengeRegister",
        "ChallengeSafeguardError",
        "Node",
        "Record",
        "assert_no_adverse_challenge_effects",
        "build_non_retaliation_assurance",
        "reject_adverse_mapping",
    }
)


class NoRetaliationGuardFacadeTests(unittest.TestCase):
    """Verify ``zava_forward.core.no_retaliation_guard`` matches canonical ``challenges``."""

    def test_public_contract_and_fail_closed_guard_parity(self) -> None:
        self.assertEqual(frozenset(no_retaliation_guard.__all__), _EXPECTED_PUBLIC_EXPORTS)
        for symbol in _EXPECTED_PUBLIC_EXPORTS:
            self.assertIs(
                getattr(no_retaliation_guard, symbol),
                getattr(challenges, symbol),
                f"Expected {symbol} on no_retaliation_guard to alias challenges.{symbol}",
            )

        assurance = no_retaliation_guard.build_non_retaliation_assurance(
            hazard_concern=True,
            independent_hazard_routed=True,
        )
        self.assertTrue(assurance["priority_preserved"])
        self.assertTrue(assurance["hazard_clock_preserved"])
        self.assertTrue(assurance["independent_hazard_intake_routed"])
        self.assertFalse(assurance["waits_for_challenge_review"])

        with self.assertRaises(no_retaliation_guard.ChallengeSafeguardError):
            no_retaliation_guard.reject_adverse_mapping({"retaliation_flag": True})

        baseline = {
            "id": "CASE-220-GUARD",
            "score": 88,
            "priority": "High",
            "urgent": True,
            "hazards": [
                {
                    "id": "HZ-1",
                    "released": False,
                    "aware_at": "2026-11-15T08:00:00Z",
                    "hold": {"status": "Active"},
                }
            ],
            "affected_challenges": [],
        }
        updated = copy.deepcopy(baseline)
        updated["affected_challenges"] = [{"id": "CH-0001", "status": "received"}]
        no_retaliation_guard.assert_no_adverse_challenge_effects(baseline, updated)

        lowered = copy.deepcopy(updated)
        lowered["score"] = 70
        with self.assertRaises(no_retaliation_guard.ChallengeSafeguardError):
            no_retaliation_guard.assert_no_adverse_challenge_effects(baseline, lowered)

    def test_independent_hazard_routing_keeps_existing_hazard_clocks(self) -> None:
        active = {
            "id": "HZ-1",
            "released": False,
            "aware_at": "2026-11-15T08:00:00Z",
            "hold": {"status": "Active"},
        }
        new_ok = {
            "id": "HZ-2",
            "released": False,
            "aware_at": "2026-11-16T09:00:00Z",
            "hold": {"status": "Active"},
        }
        before: dict[str, Any] = {"id": "CASE-220-HZ", "hazards": [active]}
        guard = no_retaliation_guard.assert_no_adverse_challenge_effects

        after = copy.deepcopy(before)
        after["hazards"].append(new_ok)
        guard(before, after, allow_new_independent_hazard=True)
        with self.assertRaises(no_retaliation_guard.ChallengeSafeguardError):
            guard(before, after)

        def delayed(case: dict[str, Any]) -> None:
            case["hazards"][0]["aware_at"] = "2026-11-20T08:00:00Z"

        def removed(case: dict[str, Any]) -> None:
            case["hazards"] = []

        def released_new(case: dict[str, Any]) -> None:
            case["hazards"][1]["released"] = True

        def held_new(case: dict[str, Any]) -> None:
            case["hazards"][1]["hold"] = {"status": "Released"}

        def unstamped_new(case: dict[str, Any]) -> None:
            case["hazards"][1]["aware_at"] = " "

        for name, mutate in (
            ("delayed_clock", delayed),
            ("removed_hazard", removed),
            ("released_new", released_new),
            ("inactive_hold_new", held_new),
            ("unstamped_new", unstamped_new),
        ):
            with self.subTest(name):
                bad = copy.deepcopy(after)
                mutate(bad)
                with self.assertRaises(no_retaliation_guard.ChallengeSafeguardError):
                    guard(before, bad, allow_new_independent_hazard=True)

    def test_held_form_review_drafts_remain_isolated_from_challenge_catalog(self) -> None:
        rd: Any = resident_decisions
        case: dict[str, Any] = {
            "id": "ZF-1",
            "form_staging": [
                {
                    "id": "BATCH-HELD-1",
                    "case_id": "ZF-1",
                    "schema_id": "SYN-TECH",
                    "schema_version": 1,
                    "schema_digest": "sha256:syn-held",
                    "source": {"id": "DOC-1", "version": 1, "content_sha256": "abc"},
                    "processing": {"kind": "text", "parser": "SYN-importer"},
                    "candidates": [{"id": "C-1", "field_id": "epc", "raw_value": "D"}],
                }
            ],
            "form_reviews": [
                {
                    "id": "DRAFT-HELD-1",
                    "fields": {
                        "epc": {
                            "value": "D",
                            "state": "Accepted",
                            "evidence": {"batch_id": "BATCH-HELD-1", "candidate_id": "C-1"},
                        }
                    },
                    "recorded_by": "pam@example.test",
                    "recorded_at": "2026-11-15T09:00:00Z",
                }
            ],
            "finance_decision_holds": [
                {
                    "decision_id": "template-rules",
                    "draft_id": "DRAFT-HELD-1",
                    "status": "Held",
                }
            ],
        }
        self.assertEqual(rd._form_staging_records(case, catalog_only=True), [])
        direct = rd._form_staging_records(case, catalog_only=False)
        self.assertEqual(len(direct), 1)
        self.assertEqual(direct[0]["human_decision"]["status"], "Proposed")
        self.assertIsNone(direct[0]["resolved_by"])

        unheld = copy.deepcopy(case)
        unheld["finance_decision_holds"] = []
        linked = rd._form_staging_records(unheld, catalog_only=True)
        self.assertEqual(len(linked), 1)
        self.assertEqual(linked[0]["id"], "form:BATCH-HELD-1")
        self.assertEqual(linked[0]["human_decision"]["status"], "Accepted")


def load_tests(
    loader: unittest.TestLoader,
    standard_tests: unittest.TestSuite,
    pattern: str | None,
) -> unittest.TestSuite:
    """Avoid double-running heavy Store/SQLite suites during default ``unittest discover``."""
    if pattern == "test*.py":
        return loader.loadTestsFromTestCase(NoRetaliationGuardFacadeTests)
    return standard_tests


if __name__ == "__main__":
    unittest.main()
