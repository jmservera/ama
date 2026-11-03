"""Coverage for the assistive-technology record completeness check (#215)."""

from __future__ import annotations

import unittest
from typing import Any

from checks.regulatory_at_record_check import ROLES, check


def full_set() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for role in ROLES:
        for mode in ("keyboard-only", "screen-reader"):
            records.append(
                {
                    "session": f"{role}-{mode}",
                    "role": role,
                    "mode": mode,
                    "tool": "NVDA 2025.1 with Firefox" if mode == "screen-reader" else "",
                    "chat_available": False,
                    "result": "pass",
                }
            )
    return records


class AtRecordCheckTests(unittest.TestCase):
    def test_complete_set_is_complete_but_not_acceptance(self) -> None:
        result = check(full_set())
        self.assertTrue(result["records_complete"])
        self.assertIn("not acceptance", result["note"])

    def test_empty_set_reports_every_gap(self) -> None:
        result = check([])
        self.assertFalse(result["records_complete"])
        self.assertIn("repairs/keyboard-only", result["problems"][0])

    def test_failure_without_barrier_is_rejected(self) -> None:
        records = full_set()
        records[0]["result"] = "fail"
        result = check(records)
        self.assertFalse(result["records_complete"])
        self.assertTrue(any("barrier" in p for p in result["problems"]))

    def test_failure_with_barrier_is_routed_and_still_complete(self) -> None:
        records = full_set()
        records[1].update(result="fail", barrier="Status read without words", workaround="Card")
        result = check(records)
        self.assertTrue(result["records_complete"])
        self.assertEqual(result["findings_to_route"][0]["workaround"], "Card")

    def test_screen_reader_needs_tool_version(self) -> None:
        records = full_set()
        records[1]["tool"] = " "
        self.assertFalse(check(records)["records_complete"])

    def test_chat_unavailable_run_required_except_suppliers(self) -> None:
        records = full_set()
        for record in records:
            record["chat_available"] = True
        problems = " ".join(check(records)["problems"])
        self.assertIn("repairs", problems)
        self.assertNotIn("suppliers", problems)

    def test_unknown_role_is_unusable(self) -> None:
        records = full_set()
        records[0]["role"] = "board"
        self.assertFalse(check(records)["records_complete"])


if __name__ == "__main__":
    unittest.main()
