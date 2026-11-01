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

    def test_batch_spread_needs_recorded_authority(self) -> None:
        from zava_forward.core.ai_consumption import UNKNOWN, batch_spread

        self.assertEqual(batch_spread([1, 2], None)["standard_deviation"], UNKNOWN)
        good = dict(authority="a", evidence="e", held_out=True, max_proposals=4)
        out = batch_spread([100, 200, 300], good)
        self.assertEqual(out["median"], "200")
        self.assertTrue(out["standard_deviation"].startswith("81.6496"))
        self.assertEqual(out["spend_authority"]["max_proposals"], 4)
        for bad in (
            dict(good, max_proposals=2),
            dict(good, held_out=False),
            dict(good, max_proposals=True),
            {"authority": "a"},
            dict(good, authority=None),
            dict(good, evidence=None),
            dict(good, authority=""),
            dict(good, evidence=""),
        ):
            self.assertEqual(batch_spread([100, 200, 300], bad)["median"], UNKNOWN)
        self.assertEqual(batch_spread([100], dict(good, max_proposals=1), 2)["median"], UNKNOWN)
        self.assertEqual(batch_spread([100], dict(good, max_proposals=2), 2)["median"], "100")

    def test_report_label_stays_unauthorised_without_batch(self) -> None:
        label = self.out["report_without_billing"]["tokens_per_proposal"]["evidence_label"]
        self.assertIn("not an authorised", label)


if __name__ == "__main__":
    unittest.main()
