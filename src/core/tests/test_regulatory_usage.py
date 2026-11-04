"""Metadata-only accounting boundaries; all inputs are constructed synthetic events."""

from __future__ import annotations

import json
import unittest
from typing import Any
from unittest import mock

from zava_forward.core import regulatory_usage
from zava_forward.core.regulatory_usage import economics, offline_usage, summarize, usage_metering

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

    def test_usage_projects_to_closed_content_free_metering_record(self) -> None:
        for task, version, outcome, surface in (
            ("regulatory-home-chat", "regulatory-chat-v1", "answer", "chat"),
            ("regulatory-check", "rule-engine-v1", "clear", "check"),
        ):
            row = usage_metering(offline_usage(task, version, outcome, AT), "evt-1")
            self.assertEqual(row["surface"], surface)
            self.assertEqual(row["retention_class"], "usage")
            self.assertEqual(row["input_tokens"], 0)
            self.assertNotIn("outcome", row)
        with self.assertRaises(ValueError):
            usage_metering(offline_usage("regulatory-check", "free text", "clear", AT), "evt-1")

    def test_summary_rejects_usage_that_leaves_the_metering_schema(self) -> None:
        bad = offline_usage("regulatory-home-chat", "regulatory-chat-v1", "answer", AT)
        bad["task_version"] = "regulatory chat v1"
        with self.assertRaises(ValueError) as ctx:
            summarize([json.dumps(dict(role=ROLE, usage=bad))], ROLE, "2026-10-16", truncated=False)
        message = str(ctx.exception)
        self.assertEqual(message, "Stored regulatory usage is invalid; audit review required.")
        self.assertNotIn("task_version", message)

    def test_summary_wraps_metering_schema_errors_in_plain_language(self) -> None:
        good = offline_usage("regulatory-home-chat", "regulatory-chat-v1", "answer", AT)
        internal = ValueError("prompt_version: not in closed schema")
        with mock.patch.object(regulatory_usage, "usage_metering", side_effect=internal):
            with self.assertRaises(ValueError) as ctx:
                summarize(
                    [json.dumps(dict(role=ROLE, usage=good))], ROLE, "2026-10-16", truncated=False
                )
        self.assertEqual(
            str(ctx.exception), "Stored regulatory usage is invalid; audit review required."
        )
        self.assertNotIn("prompt_version", str(ctx.exception))
        self.assertIsNone(ctx.exception.__cause__)
        self.assertTrue(ctx.exception.__suppress_context__)

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
