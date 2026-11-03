"""Readiness gate and read-only boundary for the discovery assistant (Refs #125)."""

import unittest

from zava_forward.core import discovery_assistant_boundary as dab


def evidence(items: tuple[str, ...] = dab.ITEM_KEYS) -> list[dab.ReadinessEvidence]:
    return [dab.ReadinessEvidence(i, f"EX-REF-{n}", "Discovery owner") for n, i in enumerate(items)]


class ReadinessTests(unittest.TestCase):
    def test_empty_is_not_ready_and_lists_every_item(self) -> None:
        report = dab.assess_readiness([])
        self.assertEqual(report.status, dab.NOT_READY)
        self.assertEqual(report.missing, dab.ITEM_KEYS)
        self.assertFalse(report.connection_to_company_data_permitted)

    def test_each_missing_item_blocks(self) -> None:
        for key in dab.ITEM_KEYS:
            with self.subTest(key=key):
                rest = tuple(k for k in dab.ITEM_KEYS if k != key)
                report = dab.assess_readiness(evidence(rest))
                self.assertEqual(report.status, dab.NOT_READY)
                self.assertEqual(report.missing, (key,))

    def test_complete_evidence_is_only_ready_for_owner_decision(self) -> None:
        report = dab.assess_readiness(evidence())
        self.assertEqual(report.status, dab.READY_FOR_OWNER_DECISION)
        self.assertFalse(report.connection_to_company_data_permitted)
        self.assertFalse(report.approved_solution)
        self.assertIn("Manual analysis", report.manual_path)

    def test_placeholder_unknown_and_duplicate_evidence_rejected(self) -> None:
        bad = [
            dab.ReadinessEvidence("accountable-owner", "TBC", "Owner"),
            dab.ReadinessEvidence("manual-path", "EX-REF-9", ""),
            dab.ReadinessEvidence("calculation-tests", "EX-REF-1", "Analyst"),
            dab.ReadinessEvidence("calculation-tests", "EX-REF-2", "Analyst"),
            dab.ReadinessEvidence("made-up", "EX-REF-3", "Analyst"),
        ]
        report = dab.assess_readiness(bad)
        self.assertEqual(report.status, dab.NOT_READY)
        self.assertIn("unusable-evidence:accountable-owner", report.invalid)
        self.assertIn("unusable-evidence:manual-path", report.invalid)
        self.assertIn("duplicate:calculation-tests", report.invalid)
        self.assertIn("unknown-item:made-up", report.invalid)

    def test_deterministic(self) -> None:
        self.assertEqual(dab.assess_readiness(evidence()), dab.assess_readiness(evidence()))


class ToolBoundaryTests(unittest.TestCase):
    def test_every_denied_area_is_refused(self) -> None:
        for name in dab.DENIED_AREAS:
            with self.subTest(name=name):
                decision = dab.authorise_tool(name)
                self.assertFalse(decision.allowed)
                self.assertEqual(decision.reason, "DENIED_BY_AUTHORITY_BOUNDARY")

    def test_unknown_tool_denied_by_default(self) -> None:
        self.assertEqual(dab.authorise_tool("anything_else").reason, "NOT_ON_READ_ONLY_ALLOWLIST")

    def test_allowlisted_tools_never_write_to_source_systems(self) -> None:
        for name in dab.ALLOWED_TOOLS:
            decision = dab.authorise_tool(name)
            self.assertTrue(decision.allowed)
            self.assertFalse(decision.writes_to_source_system)
        self.assertFalse(set(dab.ALLOWED_TOOLS) & set(dab.DENIED_AREAS))

    def test_toolbox_requires_readiness(self) -> None:
        with self.assertRaises(dab.ToolDenied):
            dab.ReadOnlyToolbox({}, dab.assess_readiness([]))

    def test_toolbox_rejects_registering_a_writer(self) -> None:
        ready = dab.assess_readiness(evidence())
        with self.assertRaises(dab.ToolDenied):
            dab.ReadOnlyToolbox({"write_source_system": lambda: None}, ready)

    def test_toolbox_runs_allowed_and_records_denials(self) -> None:
        ready = dab.assess_readiness(evidence())
        box = dab.ReadOnlyToolbox({"calculate_lifecycle_durations": lambda x: x + 1}, ready)
        self.assertEqual(box.call("calculate_lifecycle_durations", 1), 2)
        with self.assertRaises(dab.ToolDenied):
            box.call("contact_resident")
        with self.assertRaises(dab.ToolDenied):
            box.call("export_analysis_evidence")
        self.assertEqual([d.reason for d in box.denials][0], "DENIED_BY_AUTHORITY_BOUNDARY")
        self.assertEqual(len(box.denials), 2)


if __name__ == "__main__":
    unittest.main()
