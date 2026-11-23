"""Ordering of the employee chat late-success settle wait (issue 2190, flake 2)."""

from __future__ import annotations

import unittest
from typing import Any

from checks.employee_chat_browser_check import settle_route


class RecordingPage:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def wait_for_function(self, expression: str) -> None:
        self.calls.append(("function", expression))

    def wait_for_load_state(self, state: str) -> None:
        self.calls.append(("load", state))


class SettleRouteTests(unittest.TestCase):
    def test_list_route_waits_for_its_status_before_network_idle(self) -> None:
        page: Any = RecordingPage()
        settle_route(page, "#/")
        self.assertEqual([kind for kind, _ in page.calls], ["function", "load"])
        self.assertIn("workspace-status", page.calls[0][1])
        self.assertIn("'Perspective:'", page.calls[0][1])
        self.assertEqual(page.calls[1], ("load", "networkidle"))

    def test_other_transitions_only_wait_for_network_idle(self) -> None:
        for destination in ("#/progress", None):
            with self.subTest(destination=destination):
                page: Any = RecordingPage()
                settle_route(page, destination)
                self.assertEqual(page.calls, [("load", "networkidle")])


if __name__ == "__main__":
    unittest.main()
