"""Same-home stage walk is reachable from every role screen and keeps one home (Refs #233)."""

import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any, ClassVar

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
SCREENS = (WEB / "role-screens.js").read_text()

ROLES = (
    "Retrofit Programme Manager",
    "Retrofit Coordinator",
    "Quality Inspector",
    "Building Safety Liaison",
    "Resident Liaison Officer",
    "Grants and Evidence Officer",
    "Contractor",
)
# These two need richer fixtures than a bare case; programme-queue is covered by the tensions test.
SKIP = {"asset-board", "programme-queue"}

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const roles = JSON.parse(process.argv[2]);
const skip = new Set(JSON.parse(process.argv[3]));
const h = (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
  kid => kid !== false && kid !== null && kid !== undefined)});
const text = (n) => !n || typeof n !== "object" ? String(n) : (n.kids || []).map(text).join(" ");
const walk = (n, f) => {
  if (n && typeof n === "object") { f(n); (n.kids || []).forEach((k) => walk(k, f)); }
};
const make = (role, hash, shown) => {
  const context = vm.createContext({
    location: {hash}, URLSearchParams, Intl, AbortController,
    routeController: new AbortController(), me: {user: {role}}, workspaceStatus: {}, h,
    api: async (u) => u.startsWith("/api/cases?")
      ? {items: [{id: "ZF-233"}, {id: "ZF-234"}], total: 2}
      : u.startsWith("/api/cases/") ? {id: u.split("/").pop(), measure_decisions: []} : [],
    show: (...nodes) => shown.push(...nodes)
  });
  vm.runInContext(host, context);
  return context;
};
(async () => {
  const out = [];
  for (const role of roles) {
    const ids = vm.runInContext(
      `[...roleScreens.values()].filter(s => s.roles.includes(me.user.role)).map(s => s.id)`,
      make(role, "#/screens", []));
    for (const id of ids.filter((i) => !skip.has(i))) {
      const shown = [];
      const context = make(role, `#/screens?screen=${id}&case=ZF-233`, shown);
      await vm.runInContext("roleScreensView()", context);
      const panels = [];
      const stageLinks = [];
      const selected = [];
      shown.forEach((n) => walk(n, (m) => {
        const head = (m.kids || [])[0];
        if (m.tag === "section" && head && head.tag === "h2"
            && text(head).startsWith("Journey stages for")) {
          panels.push(text(m.kids[0]));
          walk(m, (a) => {
            if (a.tag === "a") stageLinks.push({href: a.attrs.href, text: text(a)});
          });
          selected.push(text(m));
        }
      }));
      out.push({role, id, panels, stageLinks, panelText: selected.join(" ")});
    }
  }
  console.log(JSON.stringify(out));
})();
"""


def run() -> list[dict[str, Any]]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(ROLES), json.dumps(sorted(SKIP))],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    out: list[dict[str, Any]] = json.loads(result.stdout)
    return out


class ConnectedJourneyAcrossRoles(unittest.TestCase):
    rows: ClassVar[list[dict[str, Any]]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = run()

    def test_every_role_screen_shows_exactly_one_stage_map_for_the_selected_home(self) -> None:
        self.assertGreaterEqual(len(self.rows), 20)
        for row in self.rows:
            self.assertEqual(row["panels"], ["Journey stages for ZF-233"], (row["role"], row["id"]))

    def test_every_stage_link_keeps_the_selected_home_and_no_other(self) -> None:
        for row in self.rows:
            for link in row["stageLinks"]:
                self.assertRegex(link["href"], r"[?&]case=ZF-233(&|$)", (row["role"], link["text"]))
                self.assertNotIn("ZF-234", link["href"])
                self.assertNotRegex(link["href"], r"EX-HOME")

    def test_current_screen_is_marked_and_not_linked_to_itself(self) -> None:
        for row in self.rows:
            if row["id"] in {
                "resident-choice",
                "technical-queue",
                "quality-queue",
                "contractor-job-pack",
            }:
                self.assertIn(
                    "You are on this screen, showing home ZF-233.", row["panelText"], row["id"]
                )
                self.assertFalse(
                    any(f"screen={row['id']}&" in link["href"] for link in row["stageLinks"]),
                    (row["role"], row["id"]),
                )

    def test_screens_outside_the_stages_say_so_and_still_show_the_home(self) -> None:
        stage_screens = {
            "technical-queue",
            "resident-choice",
            "procurement-packages",
            "contractor-job-pack",
            "quality-queue",
            "finance-invoices",
        }
        outside = [r for r in self.rows if r["id"] not in stage_screens]
        self.assertTrue(outside)
        for row in outside:
            self.assertIn(
                "This screen is not one of the eight stages. It shows the same home ZF-233.",
                row["panelText"],
                row["id"],
            )

    def test_uninstalled_stage_screens_stay_text_with_owner_and_next_action(self) -> None:
        contractor = [r for r in self.rows if r["role"] == "Contractor"]
        self.assertTrue(contractor)
        for row in contractor:
            self.assertIn(
                "is not installed for your role. Your access has not changed. Owner:",
                row["panelText"],
            )

    def test_programme_queue_keeps_its_own_single_map(self) -> None:
        self.assertEqual(
            len(re.findall(r"journeyStageMap\(", SCREENS)), 3
        )  # definition, programme call, shared call
        self.assertIn("ownsStageMap: true", SCREENS)


if __name__ == "__main__":
    unittest.main()
