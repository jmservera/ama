"""Tension callouts and the same-home stage walk on role screens (Refs #233)."""

import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
SCREENS = (WEB / "role-screens.js").read_text()

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const role = process.argv[2];
const home = process.argv[3];
const context = vm.createContext({
  location: {hash: "#/screens"}, URLSearchParams, Intl, AbortController,
  routeController: new AbortController(), me: {user: {role}}, workspaceStatus: {},
  api: async () => [],
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host, context);
const text = (n) => !n || typeof n !== "object" ? String(n) : (n.kids || []).map(text).join(" ");
const links = (n, out = []) => {
  if (n && typeof n === "object") {
    if (n.tag === "a") out.push({href: n.attrs.href, text: text(n)});
    (n.kids || []).forEach((k) => links(k, out));
  }
  return out;
};
const headings = (n, out = []) => {
  if (n && typeof n === "object") {
    if (n.tag === "h2") out.push(text(n));
    (n.kids || []).forEach((k) => headings(k, out));
  }
  return out;
};
const out = {};
for (const id of ["programme-queue", "resident-choice", "procurement-packages"]) {
  const s = vm.runInContext(`roleScreens.get("${id}")`, context);
  if (!s.roles.includes(role)) continue;
  const tree = s.render({id: home, measure_decisions: []}, {packages: [], orders: []});
  out[id] = {
    titles: headings(tree),
    text: text(tree), links: links(tree)
  };
}
console.log(JSON.stringify(out));
"""


def run(role: str = "Retrofit Programme Manager", home: str = "ZF-233") -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), role, home],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    out: dict[str, Any] = json.loads(result.stdout)
    return out


CONTINUITY = "Tension: continuity versus disclosure"
CHOICE = "Tension: utilisation versus choice"


class TensionCallouts(unittest.TestCase):
    def test_each_tension_is_stated_where_its_design_resolves_it(self) -> None:
        out = run()
        expected = {
            "programme-queue": [CONTINUITY],
            "resident-choice": [CHOICE, CONTINUITY],
            "procurement-packages": [CHOICE],
        }
        for screen, titles in expected.items():
            for title in titles:
                self.assertIn(title, out[screen]["titles"], screen)
        self.assertNotIn(CHOICE, out["programme-queue"]["titles"])
        self.assertNotIn(CONTINUITY, out["procurement-packages"]["titles"])

    def test_callouts_are_labelled_hypotheses_with_a_text_status(self) -> None:
        for screen, data in run().items():
            text = data["text"]
            self.assertIn("Status: proposed design rule.", text, screen)
            self.assertIn("pending validation in #155", text, screen)
            self.assertIn("not observed behaviour", text, screen)

    def test_resident_choice_comes_before_capacity_wording_and_disclosure_list(self) -> None:
        titles = run("Resident Liaison Officer")["resident-choice"]["titles"]
        self.assertLess(titles.index("Choice comes before offered capacity"), titles.index(CHOICE))
        self.assertLess(titles.index(CONTINUITY), titles.index("Not shown for this role"))

    def test_callouts_add_no_colour_icon_invalid_or_simulator_markup(self) -> None:
        start = SCREENS.index("const screenTensionText")
        block = SCREENS[start : SCREENS.index("function screenTable(", start)]
        for banned in ("aria-invalid", "style", "icon", "<svg", "simulat", "impersonat"):
            self.assertNotIn(banned, block.lower(), banned)
        self.assertEqual(len(re.findall(r"screenTension\(", SCREENS)), 5)


class SameHomeWalk(unittest.TestCase):
    def test_every_stage_link_carries_the_one_selected_home(self) -> None:
        stages = [
            link
            for link in run()["programme-queue"]["links"]
            if link["text"].startswith(tuple(f"{n}. " for n in range(1, 9)))
        ]
        # Stage 1 is a deferral and uninstalled screens render as text, so not all eight link.
        self.assertGreaterEqual(len(stages), 5)
        for link in stages:
            self.assertRegex(link["href"], r"[?&]case=ZF-233(&|$)", link["text"])
        screens = {re.search(r"screen=([a-z-]+)", s["href"]).group(1) for s in stages}  # type: ignore[union-attr]
        self.assertGreaterEqual(len(screens), 5)

    def test_walk_states_separate_examples_are_not_stages_of_the_home(self) -> None:
        text = run()["programme-queue"]["text"]
        self.assertIn("Separate example homes are never shown as stages of this home.", text)
        self.assertIn("Every link carries this one home's case reference.", text)
        self.assertIn("no screen yet (recorded deferral)", text)
        self.assertIn("design hypothesis, not observed behaviour", text)

    def test_stage_screens_are_registered_and_home_scoped(self) -> None:
        start = SCREENS.index("const journeyStages")
        block = SCREENS[start : SCREENS.index("];", start)]
        ids = re.findall(r'"([a-z]+(?:-[a-z]+)+)"', block)
        registered = set(re.findall(r'^\s*id: "([a-z-]+)",', SCREENS, re.MULTILINE))
        self.assertTrue(set(ids) <= registered, set(ids) - registered)
        self.assertNotRegex(block, r"EX-HOME-\d+")


if __name__ == "__main__":
    unittest.main()
