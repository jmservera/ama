"""The demo is constructed evidence: it must stay synthetic and Unknown without billing."""

from __future__ import annotations

import json
import unittest

from zava_forward.core.ai_consumption_demo import run


class DemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.out = run()

    def test_unknown_price_or_authority_holds_dispatch(self) -> None:
        held = self.out["without_price_or_authority"]
        self.assertEqual(held["dispatch_held"], "authority-unknown")
        self.assertEqual(held["path"], "workflow-only")

    def test_looping_request_stops_at_call_limit(self) -> None:
        loop = self.out["looping_request"]
        self.assertEqual(loop["model_calls_allowed"], 2)
        self.assertEqual(loop["stopped_with"], "request-call-limit")

    def test_cost_is_unknown_without_billing(self) -> None:
        report = self.out["report_without_billing"]
        self.assertEqual(report["cost_per_accepted_proposal"], "Unknown")
        self.assertEqual(report["total_cost_of_ai"], "Unknown")
        self.assertIsNone(report["financial_source"])

    def test_billing_report_is_synthetic_and_separates_quality(self) -> None:
        report = self.out["report_with_synthetic_billing"]
        self.assertEqual(report["evidence_label"], "synthetic")
        self.assertEqual(report["reconciliation"], "reconciled")
        self.assertEqual(report["total_cost_of_ai"], "Unknown")
        self.assertEqual(report["quality_status"], "Unknown")
        self.assertEqual(report["quality_qualified_cost"], "Unknown")
        self.assertIn("synthetic", self.out["evidence_label"])

    def test_no_raw_content_in_output(self) -> None:
        text = json.dumps(self.out)
        for word in ("prompt_text", "completion_text", "demo-template-v1"):
            self.assertNotIn(word, text)


if __name__ == "__main__":
    unittest.main()
