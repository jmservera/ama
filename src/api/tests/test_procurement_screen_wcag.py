"""WCAG 2.2 (#228, #151): supplier, contractor and procurement screens use text cues and jump links.

Engineering checks only, not conformance acceptance.
"""

import json
import subprocess
import unittest
from typing import Any

from test_procurement_screens import ORDER, PACKAGE, SCRIPT, WEB


def render(screen: str, case: dict[str, Any], packages: Any, orders: Any) -> Any:
    payload = {"id": screen, "c": case, "packages": packages, "orders": orders}
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(payload)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["tree"]


def walk(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


CASE = {"id": "C-1", "needs_notice": False, "named_contact": "Ann"}
SCREENS = ("procurement-packages", "contractor-job-pack")


class JumpLinks(unittest.TestCase):
    def test_sections_are_links_to_focusable_headings_not_buttons(self) -> None:
        for screen in SCREENS:
            with self.subTest(screen=screen):
                tree = render(screen, CASE, [PACKAGE], [ORDER])
                nodes = walk(tree)
                nav = next(n for n in nodes if n.get("tag") == "nav")
                self.assertTrue(nav["attrs"]["aria-label"])
                links = [n for n in walk(nav) if n.get("tag") == "a"]
                self.assertGreaterEqual(len(links), 4)
                headings = {
                    n["attrs"]["id"]: n
                    for n in nodes
                    if n.get("tag") == "h2" and "id" in n.get("attrs", {})
                }
                for link in links:
                    target: Any = headings.get(link["attrs"]["data-jump"])
                    self.assertIsNotNone(target, link["attrs"]["href"])
                    self.assertEqual(target["attrs"]["tabindex"], -1)
                    self.assertTrue(link["attrs"]["href"].startswith("#"))
                self.assertNotIn("button", [n.get("tag") for n in nodes])

    def test_finance_screens_are_left_to_their_own_slice(self) -> None:
        source = (WEB / "role-screens.js").read_text(encoding="utf-8")
        for anchor in ("finance-invoices", "finance-economics", "finance-queue"):
            self.assertNotIn(f'{{ anchor: "{anchor}" }}', source)

    def test_draft_anchor_ids_are_sanitised_and_unique(self) -> None:
        odd = [PACKAGE | {"id": "PKG 1/x"}, PACKAGE | {"id": "PKG 1/x"}]
        tree = render("procurement-packages", CASE, odd, [ORDER])
        ids = [
            n["attrs"]["id"]
            for n in walk(tree)
            if n.get("tag") == "h2" and n.get("attrs", {}).get("id", "").startswith("package-draft")
        ]
        self.assertEqual(len(ids), 2)
        self.assertEqual(len(set(ids)), 2)
        self.assertTrue(all(" " not in i and "/" not in i for i in ids))


class TextualState(unittest.TestCase):
    def test_work_order_state_leads_with_words(self) -> None:
        done = ORDER | {"state": "Completed"}
        for screen in SCREENS:
            with self.subTest(screen=screen):
                out = json.dumps(render(screen, CASE, [PACKAGE], [done]))
                self.assertIn("Completed on record, not accepted: Completed", out)

    def test_appointed_work_order_is_open(self) -> None:
        out = json.dumps(render("contractor-job-pack", CASE, [], [ORDER | {"state": "Appointed"}]))
        self.assertIn("Open: Appointed", out)

    def test_unrecognised_state_is_action_needed_not_blank(self) -> None:
        odd = ORDER | {"state": "Strange"}
        out = json.dumps(render("contractor-job-pack", CASE, [], [odd]))
        self.assertIn("Action needed: Strange", out)

    def test_checklist_states_have_prefix(self) -> None:
        out = json.dumps(render("contractor-job-pack", CASE, [], [ORDER]))
        self.assertIn("Unknown: Not assessed on this screen", out)


if __name__ == "__main__":
    unittest.main()
