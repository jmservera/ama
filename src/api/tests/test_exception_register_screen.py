"""Employee exception register view: renders the returned contract, read-only (#135).

All data below is constructed synthetic text. Nothing reads ZF_DATA or calls a service.
"""

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
const side = (value, id, version) => ({value, source: id, date: "2026-01-01", version});
const item = (extra) => ({id: "EX-001", status: "open", owner: "synthetic.operator@example.test",
  owner_role: "digital_operator", eligibility: "Unknown", recovery: null,
  runbook: "Synthetic runbook text", ...extra});
const failedAi = item({id: "EX-001", kind: "failed_ai_run", ref: "REC-9",
  summary: "AI task briefing did not deliver a model result.", error: "Model timed out",
  original_source: {record_id: "REC-9", task: "briefing", case_ids: ["C-1"],
    status: "Not reviewed"}});
const quarantined = item({id: "EX-002", kind: "failed_ai_run", ref: "REC-10",
  summary: "AI task draft did not deliver a model result.", error: "Real quarantine reason",
  original_source: {record_id: "REC-10", status: "Quarantined"}});
const legacyQuarantined = item({id: "EX-005", kind: "failed_ai_run", ref: "REC-11",
  error: "Legacy quarantine reason",
  original_source: {record_id: "REC-11", status: "quarantined"}});
const noReason = item({id: "EX-006", kind: "failed_ai_run", ref: "REC-12",
  original_source: {record_id: "REC-12", status: "Not reviewed"}});
const conflict = item({id: "EX-003", kind: "source_conflict",
  owner: "synthetic.steward@example.test",
  owner_role: "data_steward", summary: "Stock epc differs between sources for case C-1.",
  values: [side("D", "S-A", "1"), side("C", "S-B", "2")],
  original_source: {case_id: "C-1", query_id: "SQ-1", field: "epc", query_owner: "Query Owner"}});
const html = item({id: "EX-004", kind: "stranded_task", summary: "<img src=x onerror=alert(1)>",
  error: "<b>bold</b>", original_source: {source: "TASK-1"}});
const banner = {state: "unknown", last_checked: null, components: {},
  text: "Service state has not been checked recently. Do not assume it is healthy."};
const base = {state: "ok", items: [failedAi, quarantined, legacyQuarantined, noReason, conflict,
    html, 7],
  unrouted: [
    "Case C-9: stock query could not be read, so its conflicts are not routed. Open the case."],
  sources: ["Failed imports are not connected to this register yet.",
    "No service health check feeds this register, so service state is Unknown."],
  banner, access: {roles: {"synthetic.operator@example.test": ["digital_operator"]},
    scope: {failed_ai_run: "digital_operator", source_conflict: "data_steward"}},
  note: "Read-only. Recovery is a recorded human request made elsewhere; nothing is replayed."};
const empty = {...base, state: "roles_not_named", items: [],
  unrouted: ["No data steward or digital operator is named yet."],
  access: {roles: {}, scope: {}}};
const hidden = (value) => ({tag: "x", kids: [value]});

async function scenario(name, reply, opts = {}) {
  const calls = [];
  const controller = new AbortController();
  const context = vm.createContext({
    URLSearchParams, Intl, AbortController, Date,
    location: {hash: opts.hash || "#/screens?screen=data-operator&exceptions=1"},
    routeController: controller, me: {user: {role: "Retrofit Programme Manager"}},
    api: async (path, body, signal) => {
      calls.push({path, write: body !== undefined});
      return reply(controller, signal);
    },
    h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
      kid => kid !== false && kid !== null && kid !== undefined)})
  });
  vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
  let out, error = null;
  try { out = await context.__s.overview(controller.signal, [], null); }
  catch (e) { error = e.name || String(e); }
  return {name, out, error, calls};
}
const status = (code, message) => () => { const e = new Error(message); e.status = code; throw e; };
(async () => {
  const results = await Promise.all([
    scenario("full", async () => base),
    scenario("empty", async () => empty),
    scenario("entry", async () => { throw new Error("must not load"); },
      {hash: "#/screens?screen=data-operator"}),
    scenario("denied", status(403,
      "Only a named data steward or digital operator can see this.")),
    scenario("network", () => { throw new TypeError("Failed to fetch"); }),
    scenario("server", status(500, "boom with <i>markup</i>")),
    scenario("malformed", async () => ({state: "ok", items: "nope"})),
    scenario("null", async () => null),
    scenario("aborted", async (controller) => { controller.abort(); return base; }),
    scenario("signedout", status(401, "Your session has ended. Sign in again."))
  ]);
  console.log(JSON.stringify(results));
})();
"""


def run() -> dict[str, dict[str, Any]]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    return {r["name"]: r for r in json.loads(result.stdout)}


def walk(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


QUARANTINED = "Quarantined. Requested AI help did not deliver a model result."


def text(node: object) -> str:
    return json.dumps(node)


class ExceptionRegisterScreen(unittest.TestCase):
    out: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = run()

    def test_reads_only_the_existing_endpoint_with_no_write(self) -> None:
        for name, result in self.out.items():
            for call in result["calls"]:
                self.assertEqual(call, {"path": "/api/exceptions", "write": False}, name)
        self.assertEqual(self.out["entry"]["calls"], [])
        self.assertEqual(len(self.out["full"]["calls"]), 1)

    def test_failed_ai_quarantine_and_workflow_only_distinction(self) -> None:
        body = text(self.out["full"]["out"])
        for phrase in (
            "Fell back to rules or template. Requested AI help did not deliver a model result.",
            "Reason: Model timed out",
            f"{QUARANTINED} Reason: Real quarantine reason",
            f"{QUARANTINED} Reason: Legacy quarantine reason",
            "Requested AI help did not deliver a model result. How it failed is Unknown.",
            "REC-9",
            "synthetic.operator@example.test",
            "from configuration, not an appointment",
            "Placeholder guidance, not an approved runbook: Synthetic runbook text",
            "Deliberate rules-and-template processing (workflow-only) is not a failure",
            "is not a model result",
        ):
            self.assertIn(phrase, body)

    def test_conflict_shows_both_values_source_eligibility_and_no_winner(self) -> None:
        body = text(self.out["full"]["out"])
        for phrase in (
            "D; source S-A v1; dated 2026-01-01",
            "C; source S-B v2; dated 2026-01-01",
            "synthetic.steward@example.test",
            "Unknown. No winning source is selected.",
        ):
            self.assertIn(phrase, body)

    def test_returned_banner_sources_unrouted_access_and_note_are_kept(self) -> None:
        body = text(self.out["full"]["out"])
        for phrase in (
            "Service state Unknown. Service state has not been checked recently",
            "Failed imports are not connected to this register yet.",
            "service state is Unknown",
            "Case C-9: stock query could not be read",
            "digital_operator",
            "Read-only. Recovery is a recorded human request made elsewhere",
            "1 returned entries could not be read",
        ):
            self.assertIn(phrase, body)

    def test_empty_or_roles_not_named_is_not_an_all_clear(self) -> None:
        body = text(self.out["empty"]["out"])
        for phrase in (
            "roles_not_named",
            "No data steward or digital operator is named yet.",
            "This is not an all clear",
            "No role named for you",
            "No source conflicts were returned",
        ):
            self.assertIn(phrase, body)
        self.assertNotIn("table", [n["tag"] for n in walk(self.out["empty"]["out"])])

    def test_returned_markup_is_text_not_elements(self) -> None:
        tags = {n["tag"] for n in walk(self.out["full"]["out"])}
        self.assertNotIn("img", tags)
        self.assertNotIn("b", tags)
        self.assertIn("<img src=x onerror=alert(1)>", text(self.out["full"]["out"]))
        self.assertNotIn("<i>markup</i>", text(self.out["server"]["out"]))

    def test_denied_unavailable_and_malformed_show_no_rows(self) -> None:
        for name in ("denied", "network", "server", "malformed", "null"):
            out = self.out[name]["out"]
            self.assertNotIn("table", [n["tag"] for n in walk(out)], name)
            self.assertNotIn("EX-001", text(out), name)
        self.assertIn("Access denied. Only a named data steward", text(self.out["denied"]["out"]))
        self.assertIn("Your access has not changed", text(self.out["denied"]["out"]))
        for name in ("network", "server", "malformed", "null"):
            self.assertIn("Do not read this as all clear", text(self.out[name]["out"]), name)

    def test_aborted_load_renders_nothing_and_sign_out_is_not_masked(self) -> None:
        self.assertIsNone(self.out["aborted"].get("out"))
        self.assertEqual(self.out["aborted"]["error"], "AbortError")
        self.assertIsNone(self.out["signedout"].get("out"))
        self.assertEqual(self.out["signedout"]["error"], "Error")

    def test_no_controls_and_entry_is_a_plain_link(self) -> None:
        for name in ("full", "empty", "denied", "entry"):
            tags = [n["tag"] for n in walk(self.out[name]["out"])]
            for control in ("button", "form", "input", "select", "textarea"):
                self.assertNotIn(control, tags, name)
        links = [n for n in walk(self.out["entry"]["out"]) if n["tag"] == "a"]
        self.assertEqual(len(links), 1)
        self.assertTrue(links[0]["attrs"]["href"].endswith("screen=data-operator&exceptions=1"))

    def test_tables_use_shared_labelled_pattern(self) -> None:
        nodes = walk(self.out["full"]["out"])
        tables = [n for n in nodes if n["tag"] == "table"]
        self.assertEqual(len(tables), 2)
        for table in tables:
            self.assertEqual(table["kids"][0]["tag"], "caption")
            for th in (n for n in walk(table) if n["tag"] == "th"):
                self.assertEqual(th["attrs"]["scope"], "col")
        for region in (n for n in nodes if (n.get("attrs") or {}).get("role") == "region"):
            self.assertEqual(region["attrs"]["tabindex"], 0)


if __name__ == "__main__":
    unittest.main()
