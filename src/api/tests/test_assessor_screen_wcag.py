"""PAS 2035 technical and quality screens state evidence in text, not colour alone (WCAG 1.4.1)."""

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
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Quality Inspector"}},
  api: async () => ({}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__roles = roleScreens;", context);
const signed = {status: "Signed off", by: "A Person", version: 2};
const c = {id: "C-1", technical: {design_version: 2, signoffs: {
  assessment: signed,
  design: {status: "Returned", reason: "Redo"},
  building: {status: "Needs reassessment"},
  coordination: {status: "constructor"}
}}, technical_missing: [], stock_reconciliation: [],
measures: "Loft", quality_handover_blockers: [], quality: [{measure: "Loft", state: "Submitted",
  items: [{label: "Depth", evidence: "Photo"}, {label: "Seal", evidence: ""}]}]};
const technical = context.__roles.get("technical-queue").render(c);
const quality = context.__roles.get("quality-queue").render(c);
const incomplete = context.__roles.get("technical-queue").render(
  {...c, technical: {signoffs: {assessment: {status: "Signed off"}}}});
console.log(JSON.stringify({technical, quality, incomplete}));
"""


def render() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def walk(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


def texts(node: Any) -> list[str]:
    return [kid for n in walk(node) for kid in n.get("kids", []) if isinstance(kid, str)]


class AssessorScreenWcag(unittest.TestCase):
    def test_signoff_states_carry_text_prefixes(self) -> None:
        found = texts(render()["technical"])
        self.assertIn("Verified: Signed off on design version 2", found)
        self.assertIn("Action needed: Returned", found)
        self.assertIn("Action needed: Needs reassessment", found)
        # A prototype-chain key must not be treated as a known state.
        self.assertIn("Pending review: constructor", found)

    def test_incomplete_signed_off_record_is_not_verified(self) -> None:
        found = texts(render()["incomplete"])
        self.assertFalse([t for t in found if t.startswith("Verified:")])
        self.assertTrue([t for t in found if t.startswith("Action needed: Signed off record")])

    def test_sections_have_jump_links_to_labelled_landmarks(self) -> None:
        tree = render()["technical"]
        nodes = walk(tree)
        nav = next(n for n in nodes if n["tag"] == "nav")
        self.assertEqual(nav["attrs"]["aria-label"], "Sections on this screen")
        targets = {n["attrs"]["href"][1:] for n in walk(nav) if n["tag"] == "a"}
        sections = {
            n["attrs"]["id"]: n for n in nodes if n["tag"] == "section" and "id" in n["attrs"]
        }
        self.assertEqual(targets, set(sections))
        for ident, section in sections.items():
            self.assertEqual(section["attrs"]["aria-labelledby"], f"{ident}-heading")
            heading = next(n for n in walk(section) if n["tag"] == "h2")
            self.assertEqual(heading["attrs"]["id"], f"{ident}-heading")

    def test_quality_check_states_use_text_prefixes(self) -> None:
        found = texts(render()["quality"])
        self.assertIn("Pending review: Evidence noted", found)
        self.assertIn("Action needed: No evidence", found)


if __name__ == "__main__":
    unittest.main()
