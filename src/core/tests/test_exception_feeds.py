"""Feeds from existing records into the exception queue (FR-029, AC-040)."""

import unittest

from zava_forward.core.exception_feeds import feed_failed_ai_runs, feed_stranded_tasks
from zava_forward.core.exception_queue import OPERATOR, STEWARD, ExceptionQueue

STAFF = {"Sam Steward": [STEWARD], "Olive Operator": [OPERATOR]}


def make() -> ExceptionQueue:
    return ExceptionQueue(STAFF, clock=lambda: "2026-11-03T00:00:00+00:00")


def rec(rid: str, **fields: object) -> dict[str, object]:
    base: dict[str, object] = {
        "id": rid,
        "kind": "ai_task",
        "task": "summary",
        "case_ids": ["C1"],
        "status": "Not reviewed",
        "mode": "ai",
        "source": "ai",
        "fallback_reason": None,
        "created": "2026-11-03T09:00:00",
        "shown_output": "personal text",
    }
    return {**base, **fields}


class ExceptionFeedTests(unittest.TestCase):
    def test_fallback_and_quarantine_are_raised_others_are_not(self) -> None:
        q = make()
        records: list[dict[str, object]] = [
            rec("ok"),
            rec("fell", source="template", fallback_reason="provider timeout"),
            rec("quar", status="Quarantined", fallback_reason="late result quarantined"),
            rec(
                "chosen",
                mode="workflow-only",
                source="template",
                fallback_reason="workflow-only mode selected",
            ),
            {"id": "x", "kind": "other"},
        ]
        raised = feed_failed_ai_runs(q, records, "Olive Operator")
        self.assertEqual([i["original_source"]["record_id"] for i in raised], ["fell", "quar"])
        self.assertEqual(len(q.queue("Olive Operator")), 2)

    def test_item_keeps_ids_not_text_and_is_owned_and_unreplayed(self) -> None:
        q = make()
        (item,) = feed_failed_ai_runs(
            q, [rec("fell", source="template", fallback_reason="timeout")], "Olive Operator"
        )
        self.assertNotIn("personal text", str(item))
        self.assertEqual(item["owner"], "Olive Operator")
        self.assertEqual(item["eligibility"], "Unknown")
        self.assertIsNone(item["recovery"])

    def test_repeated_feed_does_not_duplicate(self) -> None:
        q = make()
        records = [rec("fell", source="template", fallback_reason="timeout")]
        feed_failed_ai_runs(q, records, "Olive Operator")
        feed_failed_ai_runs(q, records, "Olive Operator")
        self.assertEqual(len(q.queue("Olive Operator")), 1)

    def test_owner_without_role_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            feed_failed_ai_runs(
                make(), [rec("f", source="template", fallback_reason="t")], "Sam Steward"
            )

    def test_only_overdue_tasks_without_named_owner_are_stranded(self) -> None:
        q = make()
        overdue = [
            {
                "task": "Hazard follow-up",
                "owner": "Unknown",
                "due_at": "2026-11-01",
                "completion": "Not evidenced",
                "case_id": "C1",
                "source": "case:C1/hazards/0",
                "as_of": "2026-11-03",
            },
            {
                "task": "Handoff",
                "owner": "Pat Coordinator",
                "due_at": "2026-11-01",
                "completion": "Not evidenced",
                "case_id": "C2",
                "source": "case:C2/handoff",
            },
        ]
        raised = feed_stranded_tasks(q, overdue, "Olive Operator")
        feed_stranded_tasks(q, overdue, "Olive Operator")
        self.assertEqual(len(raised), 1)
        self.assertEqual(raised[0]["kind"], "stranded_task")
        self.assertEqual(len(q.queue("Olive Operator")), 1)
