"""Stage map and tension callouts stay announceable and keyboard-safe (Refs #233)."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any, ClassVar

from tests.test_role_screens_connected_journey import ROLES, SKIP, WEB

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const roles = JSON.parse(process.argv[2]);
const skip = new Set(JSON.parse(process.argv[3]));
const h = (tag, attrs, ...kids) => ({tag, attrs: attrs || {}, kids: kids.flat(Infinity).filter(
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
      ? {items: [{id: "ZF-233"}], total: 1}
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
      await vm.runInContext("roleScreensView()",
        make(role, `#/screens?screen=${id}&case=ZF-233`, shown));
      const row = {role, id, lists: [], current: [], mapTabindex: 0, tensions: []};
      shown.forEach((n) => walk(n, (m) => {
        if (m.tag === "section" && (m.kids[0] || {}).tag === "h2") {
          const title = text(m.kids[0]);
          if (title.startsWith("Tension:")) row.tensions.push({title, body: text(m)});
          if (title.startsWith("Journey stages for")) {
            walk(m, (a) => {
              const nested = /^h[1-6]$/.test(a.tag) && a !== m.kids[0];
              if (a.attrs.tabindex !== undefined || nested) row.mapTabindex++;
              if (a.tag === "ol") row.lists.push(a.attrs["aria-label"]);
              if (a.tag === "li" && a.attrs["aria-current"]) row.current.push(
                {value: a.attrs["aria-current"], text: text(a)});
            });
          }
        }
      }));
      out.push(row);
    }
  }
  console.log(JSON.stringify(out));
})();
"""


def run() -> list[dict[str, Any]]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(Path(WEB)), json.dumps(ROLES), json.dumps(sorted(SKIP))],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    out: list[dict[str, Any]] = json.loads(result.stdout)
    return out


class StageMapAnnouncements(unittest.TestCase):
    rows: ClassVar[list[dict[str, Any]]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = run()

    def test_stage_list_is_named_after_the_selected_home(self) -> None:
        self.assertGreaterEqual(len(self.rows), 20)
        for row in self.rows:
            self.assertEqual(
                row["lists"], ["Eight journey stages for ZF-233"], (row["role"], row["id"])
            )

    def test_current_stage_is_announced_once_and_also_written_as_text(self) -> None:
        stage_screens = {
            "technical-queue",
            "resident-choice",
            "procurement-packages",
            "contractor-job-pack",
            "quality-queue",
            "finance-invoices",
        }
        for row in self.rows:
            if row["id"] in stage_screens:
                self.assertEqual(len(row["current"]), 1, (row["role"], row["id"]))
                self.assertEqual(row["current"][0]["value"], "step")
                self.assertIn("You are on this screen", row["current"][0]["text"])
            else:
                self.assertEqual(row["current"], [], (row["role"], row["id"]))

    def test_stage_map_adds_no_tab_stops_and_no_nested_headings(self) -> None:
        for row in self.rows:
            self.assertEqual(row["mapTabindex"], 0, (row["role"], row["id"]))


class TensionCalloutsKeepPlainStatus(unittest.TestCase):
    def test_tension_callouts_carry_a_text_status_line(self) -> None:
        tensions = [t for row in run() for t in row["tensions"]]
        self.assertTrue(tensions)
        for tension in tensions:
            self.assertIn("Status: proposed design rule.", tension["body"], tension["title"])
            self.assertIn("pending validation in #155", tension["body"], tension["title"])


if __name__ == "__main__":
    unittest.main()
