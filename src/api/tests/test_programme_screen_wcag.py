"""Programme connected view states start with a word and sections are keyboard reachable."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const focused = [];
const doc = {getElementById: (id) => ({focus: () => focused.push(id)})};
const context = vm.createContext({
  location: {hash: "#/screens?screen=programme-queue"}, URLSearchParams, Intl, Date,
  document: doc, routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  api: async () => ({}),
  h: (tag, attrs, ...kids) => ({tag, attrs: attrs || {},
    kids: kids.flat(Infinity).filter(k => k !== false && k !== null && k !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('programme-queue');", context);
const bound = {measure: "Loft", context_revision: 2};
const clear = {id: "C-8", work: {blockers: []}, technical: {}, measures: "Loft",
  measure_decisions: [{measure: "Loft", context: {revision: 2}}],
  quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}],
  finance: {budget: {status: "Approved"}}};
const orders = [{id: "WO-1", state: "Appointed", appointment_control: {status: "Committed", missing: []},
  versions: [{resident_bindings: [bound]}]}];
const s = context.__s;
const blocked = s.render({id: "C-9", work: {blockers: []}}, {orders: null});
const ok = s.render(clear, {orders});
const link = ok.kids[0].kids.find(k => k.tag === "div" && k.attrs.role === "group").kids[0];
link.attrs.onclick({});
console.log(JSON.stringify({blocked, ok, focused}));
"""  # noqa: E501


def run() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def walk(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


def text(node: object) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        return "".join(text(kid) for kid in node.get("kids", []))
    return ""


def summary_lines(node: object) -> list[str]:
    for item in walk(node):
        if item["tag"] == "ul" and item["kids"] and "step." in text(item["kids"][0]):
            return [text(li) for li in item["kids"]]
    return []


class ProgrammeScreenWcag(unittest.TestCase):
    def setUp(self) -> None:
        self.out = run()

    def test_blocked_steps_start_with_action_needed(self) -> None:
        lines = summary_lines(self.out["blocked"])
        self.assertEqual(len(lines), 5)
        resident = next(line for line in lines if "Resident step" in line)
        self.assertTrue(resident.startswith("Warning: No recorded blocker"), resident)
        for line in (line for line in lines if line is not resident):
            self.assertTrue(line.startswith("Action needed: Blocked"), line)
            self.assertIn("Owner:", line)
            self.assertIn("Next action:", line)

    def test_clear_steps_are_a_warning_never_a_pass(self) -> None:
        lines = summary_lines(self.out["ok"])
        quality = next(line for line in lines if "Quality step" in line)
        self.assertTrue(quality.startswith("Warning: No recorded blocker"), quality)
        self.assertIn("not a pass", quality)
        self.assertFalse(any(line.startswith("Pass") for line in lines))

    def test_existing_state_cells_are_unchanged(self) -> None:
        cells = [text(td) for td in walk(self.out["blocked"]) if td["tag"] == "td"]
        self.assertIn("Blocked: evidence missing", cells)
        self.assertNotIn("Action needed: Blocked", cells)

    def test_section_links_use_documented_classes_and_move_focus(self) -> None:
        group = next(n for n in walk(self.out["ok"]) if n["attrs"].get("role") == "group")
        self.assertEqual(group["attrs"]["class"], "row")
        links = group["kids"]
        self.assertEqual(len(links), 4)
        for link in links:
            self.assertEqual((link["tag"], link["attrs"]["class"]), ("button", "btn alt"))
            self.assertEqual(link["attrs"]["type"], "button")
        ids = {n["attrs"].get("id") for n in walk(self.out["ok"])}
        self.assertEqual(
            ids & {"programme-summary", "programme-steps"}, {"programme-summary", "programme-steps"}
        )
        self.assertEqual(self.out["focused"], ["programme-summary"])

    def test_no_nav_element_or_other_controls(self) -> None:
        tags = {n["tag"] for n in walk(self.out["ok"])}
        self.assertFalse(tags & {"nav", "form", "input", "select"})


if __name__ == "__main__":
    unittest.main()
