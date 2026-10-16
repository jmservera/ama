"""Synthetic retention-review boundaries; no asserted DPO schedule or disposal."""

from __future__ import annotations

import copy
import json
import unittest
from datetime import UTC, datetime, timedelta
from typing import Any

from zava_forward.core.regulatory_privacy import retention_report

NOW = datetime(2026, 10, 16, 12, tzinfo=UTC)


class RetentionReview(unittest.TestCase):
    def setUp(self) -> None:
        self.threads: list[dict[str, Any]] = [
            dict(
                id="SYN-THREAD",
                created_at=(NOW - timedelta(days=2)).isoformat(),
                message_count=2,
                content="PRIVATE-CONTENT-CANARY",
                owner="PRIVATE-OWNER-CANARY",
            )
        ]

    def test_unknown_periods_do_not_imply_approval_or_disposal(self) -> None:
        before = copy.deepcopy(self.threads)
        result = retention_report(self.threads, {}, NOW)
        self.assertEqual(result["chat"]["status"], "unknown")
        self.assertIsNone(result["chat"]["days"])
        self.assertIsNone(result["chat"]["records"][0]["due_for_review"])
        self.assertFalse(result["dpo_reviewed"])
        self.assertFalse(result["deletion_enabled"])
        self.assertTrue(all(c["days"] is None for c in result["other_classes"]))
        self.assertNotIn("PRIVATE-", json.dumps(result))
        self.assertEqual(self.threads, before)

    def test_exact_due_boundary_is_simulated_review_not_deletion(self) -> None:
        env = dict(CHAT_RETENTION_REF="SYNTH-RETENTION", CHAT_RETENTION_DAYS="2")
        self.assertFalse(
            retention_report(self.threads, env, NOW - timedelta(microseconds=1))["chat"]["records"][
                0
            ]["due_for_review"]
        )
        result = retention_report(self.threads, env, NOW)
        self.assertTrue(result["chat"]["records"][0]["due_for_review"])
        self.assertEqual(result["chat"]["status"], "simulated")
        self.assertEqual(result["chat"]["records"][0]["review_due"], NOW.isoformat())
        self.assertFalse(result["dpo_reviewed"])
        self.assertFalse(result["deletion_enabled"])

    def test_malformed_or_non_synthetic_configuration_is_explicitly_rejected(self) -> None:
        for ref, days in (
            ("", "2"),
            ("SYNTH-RETENTION", ""),
            ("UNVERIFIED-REAL-APPROVAL", "2"),
            ("SYNTH-RETENTION", "0"),
            ("SYNTH-RETENTION", "-1"),
            ("SYNTH-RETENTION", "2.5"),
            ("SYNTH-RETENTION", "36501"),
            ("SYNTH-RETENTION", "\u00b2"),
        ):
            with self.subTest(ref=ref, days=days), self.assertRaises(ValueError):
                retention_report(
                    self.threads, dict(CHAT_RETENTION_REF=ref, CHAT_RETENTION_DAYS=days), NOW
                )
        with self.assertRaises(ValueError):
            retention_report(self.threads, {}, NOW.replace(tzinfo=None))


if __name__ == "__main__":
    unittest.main()
