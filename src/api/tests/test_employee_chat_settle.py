"""Ordering of the employee chat late-success settle wait (issue 2190, flake 2)."""

from __future__ import annotations

import inspect
import unittest
from collections.abc import Callable
from typing import Any

from checks.employee_chat_browser_check import late_success, settle_route, wait_for_skills
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, sync_playwright


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


class LateSuccessOrderTests(unittest.TestCase):
    def test_snapshot_is_taken_only_after_the_route_settles(self) -> None:
        source = inspect.getsource(late_success)
        self.assertIn("settle_route(", source)
        self.assertLess(source.index("settle_route("), source.index("state.snapshot ="))


DELAYED_ROUTE = """
<p id="workspace-status"></p>
<script>
  window.addEventListener('hashchange', () => {
    const publish = () => {
      document.getElementById('workspace-status').textContent = 'Perspective: tester.';
    };
    // Longer than the 500 ms networkidle window, with no request in flight. Without the
    // timer the status is held back until the test releases it, so no clock decides the outcome.
    if (window.autoPublish) setTimeout(publish, 1200); else window.publish = publish;
  });
</script>
"""


class SettleRouteBrowserTests(unittest.TestCase):
    """Reproduce the gap between the facets read and the cases read with a real browser."""

    def run_route(self, wait: Callable[[Page], None], auto_publish: bool) -> str:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
            except PlaywrightError as error:
                self.skipTest(f"Chromium is not installed: {error}")
            try:
                page = browser.new_page()
                page.set_content(DELAYED_ROUTE)
                page.evaluate("auto => { window.autoPublish = auto; }", auto_publish)
                page.evaluate("() => { location.hash = '#/'; }")
                wait(page)
                return str(page.locator("#workspace-status").text_content())
            finally:
                browser.close()

    def test_network_idle_alone_returns_before_the_list_status(self) -> None:
        status = self.run_route(
            lambda page: page.wait_for_load_state("networkidle"), auto_publish=False
        )
        self.assertEqual(status, "")

    def test_settle_route_returns_after_the_list_status(self) -> None:
        status = self.run_route(lambda page: settle_route(page, "#/"), auto_publish=True)
        self.assertTrue(status.startswith("Perspective:"), status)


DELAYED_SKILLS = """
<div role="dialog"><textarea id="q" disabled></textarea><select id="s"></select></div>
<script>
  // The question enables and the options arrive only after the skills read ends.
  setTimeout(() => {
    document.getElementById('q').disabled = false;
    document.getElementById('s').innerHTML = '<option>a</option>'.repeat(6);
  }, 1200);
</script>
"""


class WaitForSkillsTests(unittest.TestCase):
    """The option count is read only after the delayed skills load (issue 2190, fourth race)."""

    def test_wait_for_skills_returns_after_the_options_load(self) -> None:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
            except PlaywrightError as error:
                self.skipTest(f"Chromium is not installed: {error}")
            try:
                page = browser.new_page()
                page.set_content(DELAYED_SKILLS)
                self.assertEqual(page.locator("select option").count(), 0)
                wait_for_skills(page.locator("[role=dialog]"), page.locator("#q"))
                self.assertEqual(page.locator("select option").count(), 6)
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
