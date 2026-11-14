"""Role screens keep one explicit home identity across a cross-role walk (Refs #233)."""

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
const h = (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
  kid => kid !== false && kid !== null && kid !== undefined)});
const text = (n) => !n || typeof n !== "object" ? String(n) : (n.kids || []).map(text).join(" ");
const walk = (n, f) => {
  if (n && typeof n === "object") { f(n); (n.kids || []).forEach((k) => walk(k, f)); }
};
const render = async (role, hash, returnedId) => {
  const shown = [];
  const context = vm.createContext({
    location: {hash}, URLSearchParams, Intl, AbortController,
    routeController: new AbortController(), me: {user: {role}}, workspaceStatus: {}, h,
    api: async (u) => u.startsWith("/api/cases?")
      ? {items: [{id: "ZF-233"}, {id: "ZF-234"}], total: 2}
      : u.startsWith("/api/cases/")
        ? {id: returnedId || decodeURIComponent(u.split("/").pop()), measure_decisions: []} : [],
    show: (...nodes) => shown.push(...nodes)
  });
  vm.runInContext(host, context);
  await vm.runInContext("roleScreensView()", context);
  const badges = [], alerts = [], hrefs = [], maps = [];
  shown.forEach((n) => walk(n, (m) => {
    if (m.attrs && m.attrs["data-same-home"]) badges.push(text(m));
    if (m.attrs && m.attrs.role === "alert") alerts.push(text(m));
    const isMap = m.tag === "section"
      && text((m.kids || [])[0]).startsWith("Journey stages for");
    const carries = isMap
      || (m.tag === "nav" && m.attrs["aria-label"] === "Specialist screens");
    if (isMap) maps.push(1);
    if (carries) walk(m, (a) => { if (a.tag === "a") hrefs.push(a.attrs.href); });
  }));
  return {badges, alerts, hrefs, maps: maps.length};
};
(async () => {
  const walkRoles = [
    ["Retrofit Programme Manager", "technical-queue"],
    ["Retrofit Coordinator", "resident-choice"],
    ["Quality Inspector", "quality-queue"],
    ["Building Safety Liaison", "technical-queue"],
    ["Grants and Evidence Officer", "finance-invoices"],
  ];
  const walked = [];
  for (const [role, id] of walkRoles) {
    walked.push({role, id, ...(await render(role, `#/screens?screen=${id}&case=ZF-233`))});
  }
  const mismatch = await render("Quality Inspector",
    "#/screens?screen=quality-queue&case=ZF-233", "ZF-234");
  console.log(JSON.stringify({walked, mismatch}));
})();
"""


def run() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    out: dict[str, Any] = json.loads(result.stdout)
    return out


class SameHomeIdentity(unittest.TestCase):
    data: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = run()

    def test_each_role_screen_names_the_same_case_once(self) -> None:
        for row in self.data["walked"]:
            self.assertEqual(len(row["badges"]), 1, (row["role"], row["id"]))
            self.assertIn("Same home: case ZF-233", row["badges"][0])
            self.assertIn("never shown here as another stage", row["badges"][0])

    def test_cross_role_deep_links_keep_that_case_only(self) -> None:
        for row in self.data["walked"]:
            self.assertEqual(row["maps"], 1, (row["role"], row["id"]))
            screen_links = [h for h in row["hrefs"] if h.startswith("#/screens?screen=")]
            self.assertTrue(screen_links)
            for href in screen_links:
                self.assertIn("case=ZF-233", href)
                self.assertNotIn("ZF-234", href)

    def test_mismatched_record_is_withheld_not_relabelled(self) -> None:
        row = self.data["mismatch"]
        self.assertEqual(row["badges"], [])
        self.assertEqual(row["maps"], 0)
        self.assertEqual(len(row["alerts"]), 1)
        self.assertIn("does not match the requested home ZF-233", row["alerts"][0])
        self.assertIn("Next action:", row["alerts"][0])


if __name__ == "__main__":
    unittest.main()
