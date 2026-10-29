"""Metadata-only accounting boundaries; all inputs are constructed synthetic events."""

from __future__ import annotations

import json
import unittest
from typing import Any

from zava_forward.core.regulatory_usage import economics, offline_usage, summarize

AT = "2026-10-16T12:00:00+00:00"
ROLE = "Resident Liaison Officer"


def record(kind: str = "answer", **overrides: Any) -> str:
    return json.dumps(
        dict(
            role=ROLE,
            usage=offline_usage("regulatory-home-chat", "regulatory-chat-v1", kind, AT),
        )
        | overrides
    )


class RegulatoryUsage(unittest.TestCase):
    def test_closed_model_free_contract_and_unknown_cost(self) -> None:
        usage = offline_usage("regulatory-home-chat", "regulatory-chat-v1", "answer", AT)
        self.assertEqual(usage["model_calls"], 0)
        self.assertEqual(usage["model_call_limit_per_role_period"], 0)
        self.assertNotIn("question", usage)
        self.assertNotIn("case_id", usage)
        self.assertNotIn("sources", usage)
        report = economics()
        self.assertEqual(report["ai_cost_per_accepted_check"], "Unknown")
        self.assertEqual(len(report["missing_inputs"]), 4)
        self.assertEqual(report["execution"]["paid_authority"], "none")
        self.assertEqual(report["execution"]["paid_budget_limit"], 0)

    def test_role_day_outcomes_legacy_and_partial_are_explicit(self) -> None:
        data = [
            record(),
            record("refused"),
            record("conflict"),
            record(role="Quality Inspector"),
            record(usage=None),
            record(
                usage=offline_usage(
                    "regulatory-home-chat",
                    "regulatory-chat-v1",
                    "answer",
                    "2026-10-15T12:00:00+00:00",
                )
            ),
        ]
        result = summarize(data, ROLE, "2026-10-16", truncated=True)
        self.assertEqual(result["outcomes"], dict(answer=1, refused=1, conflict=1))
        self.assertEqual(result["recorded_turns"], 3)
        self.assertEqual(result["unmetered_events_in_window"], 1)
        self.assertEqual(result["coverage"], "bounded_partial")
        self.assertEqual(
            summarize([], ROLE, "2026-10-16", truncated=False)["coverage"],
            "recorded_audit_only",
        )

    def test_invalid_or_content_bearing_usage_is_not_silently_counted(self) -> None:
        for field, value in (("model_calls", 1), ("question", "PRIVATE-CANARY")):
            usage = offline_usage("regulatory-home-chat", "regulatory-chat-v1", "answer", AT)
            usage[field] = value
            with self.assertRaisesRegex(ValueError, "audit review"):
                summarize([record(usage=usage)], ROLE, "2026-10-16", truncated=False)
        for args in (
            ("unknown", "v1", "answer", AT),
            ("regulatory-home-chat", "v1", "approve", AT),
            ("regulatory-home-chat", "v1", "answer", "2026-10-16"),
        ):
            with self.assertRaises(ValueError):
                offline_usage(*args)


if __name__ == "__main__":
    unittest.main()
