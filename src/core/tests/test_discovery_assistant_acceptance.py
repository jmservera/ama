"""Acceptance status and no-write attestation for the discovery assistant (Refs #125)."""

import itertools
import unittest

from zava_forward.core import discovery_assistant_acceptance as daa
from zava_forward.core import discovery_assistant_boundary as dab
from zava_forward.core import discovery_assistant_evaluation as dae


def ready() -> dab.ReadinessReport:
    return dab.assess_readiness(
        [dab.ReadinessEvidence(k, f"EX-REF-{n}", "Owner") for n, k in enumerate(dab.ITEM_KEYS)]
    )


def no_write(keys: tuple[str, ...] = daa.NO_WRITE_KEYS) -> daa.NoWriteReport:
    return daa.assess_no_write(
        [daa.NoWriteEvidence(k, f"EX-OBS-{n}", "Security owner") for n, k in enumerate(keys)]
    )


def compared() -> dae.ComparisonReport:
    return dae.compare_methods(
        [
            dae.MeasureResult(m, x, f"EX-RES-{i}", "Evaluation owner")
            for i, (m, x) in enumerate(itertools.product(dae.MEASURE_KEYS, dae.METHODS))
        ]
    )


class NoWriteTests(unittest.TestCase):
    def test_each_missing_item_blocks(self) -> None:
        for key in daa.NO_WRITE_KEYS:
            rest = tuple(k for k in daa.NO_WRITE_KEYS if k != key)
            self.assertEqual(no_write(rest).missing, (key,))

    def test_complete_never_establishes_criterion(self) -> None:
        report = no_write()
        self.assertEqual(report.missing, ())
        self.assertFalse(report.no_write_access_established)

    def test_invalid_entries_rejected(self) -> None:
        report = daa.assess_no_write(
            [
                daa.NoWriteEvidence("credential-scope", "TBD", "Owner"),
                daa.NoWriteEvidence("write-attempt-denied", "EX-OBS-1", "Owner"),
                daa.NoWriteEvidence("write-attempt-denied", "EX-OBS-2", "Owner"),
                daa.NoWriteEvidence("bogus", "EX-OBS-3", "Owner"),
            ]
        )
        self.assertEqual(len(report.invalid), 3)


class AcceptanceTests(unittest.TestCase):
    def test_empty_inputs_list_every_blocker(self) -> None:
        status = daa.assess_acceptance(
            dab.assess_readiness([]), daa.assess_no_write([]), dae.compare_methods([])
        )
        self.assertEqual(len(status.blockers), 3)
        self.assertFalse(any(status.criteria_met.values()))

    def test_complete_evidence_still_leaves_criteria_unmet_and_unapproved(self) -> None:
        status = daa.assess_acceptance(ready(), no_write(), compared())
        self.assertEqual(status.blockers, ())
        self.assertFalse(any(status.criteria_met.values()))
        self.assertFalse(status.connection_to_company_data_permitted)
        self.assertFalse(status.approved_solution)

    def test_single_gap_is_named(self) -> None:
        status = daa.assess_acceptance(ready(), no_write(("credential-scope",)), compared())
        self.assertEqual(status.blockers, ("no-write-evidence-incomplete",))


if __name__ == "__main__":
    unittest.main()
