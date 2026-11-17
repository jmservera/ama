"""Resident screens: text state cues and keyboard section links (WCAG 2.2, #232, #151)."""

import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Resident Liaison Officer"}},
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__c = roleScreens.get('resident-choice');" +
  "globalThis.__s = roleScreens.get('resident-service-issues');", context);
const c = JSON.parse(process.argv[2]);
console.log(JSON.stringify({choice: context.__c.render(c), service: context.__s.render(c)}));
"""

CASE: dict[str, Any] = {
    "id": "C-1",
    "resident_update": {"status": "Proposed", "purpose": "Explain", "safe_contact_ref": "SC-1"},
    "measure_decisions": [{"measure": "Heat pump", "status": "Accepted", "versions": []}],
    "service_requests": [{"id": "SR-1", "route": "Repair", "status": "Open"}],
}


def render() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(CASE)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    out: dict[str, Any] = json.loads(result.stdout)
    return out


def walk(node: Any) -> list[dict[str, Any]]:
    if isinstance(node, dict) and "tag" in node:
        return [node] + [n for k in node["kids"] for n in walk(k)]
    return []


class ResidentScreenWcag(unittest.TestCase):
    def test_jump_links_are_anchors_targeting_focusable_headings(self) -> None:
        for key in ("choice", "service"):
            nodes = walk(render()[key])
            nav = next(n for n in nodes if n["tag"] == "nav")
            links = [k for k in nav["kids"] if k["tag"] == "a"]
            self.assertTrue(links)
            self.assertFalse([n for n in nav["kids"] if n["tag"] == "button"])
            headings = {n["attrs"].get("id"): n["attrs"] for n in nodes if n["tag"] == "h2"}
            for link in links:
                target = link["attrs"]["href"].removeprefix("#")
                self.assertEqual(link["attrs"]["data-jump"], target)
                self.assertEqual(headings[target].get("tabindex"), -1)

    def test_state_cues_are_text_and_noted_in_each_screen(self) -> None:
        out = {k: json.dumps(v) for k, v in render().items()}
        self.assertIn("Confirmed: Accepted", out["choice"])
        self.assertIn("Action needed: Proposed", out["choice"])
        self.assertIn("Action needed: Open", out["service"])
        for text in out.values():
            self.assertIn("Colour is never the only signal", text)

    def test_literal_panel_titles_are_kept_for_connected_home_check(self) -> None:
        source = (WEB / "role-screens.js").read_text()
        titles = (
            "Choice for each measure",
            "Paused or withdrawn by the resident",
            "Service issues",
        )
        for title in titles:
            self.assertTrue(re.search(rf'screenPanel\("{re.escape(title)}"', source), title)


if __name__ == "__main__":
    unittest.main()
