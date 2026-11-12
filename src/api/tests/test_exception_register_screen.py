"""Employee exception register view: renders the returned contract, read-only (#135).

All data below is constructed synthetic text. Nothing reads ZF_DATA or calls a service.
"""

import csv
import io
import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.list_export import safe_cell

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
    h: (tag, attrs, ...kids) => ({tag, attrs, addEventListener() {},
      kids: kids.flat(Infinity).filter(
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
        self.assertNotIn("failed imports are not connected", text(self.out["full"]["out"]))
        self.assertNotIn("failed imports are not connected", body)
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


CSV_SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const marker = {owner: "marker.owner@example.test", summary: "MARK-SUMMARY", error: "MARK-ERROR",
  runbook: "MARK-RUNBOOK", eligibility: "MARK-ELIGIBILITY", ref: "MARK-REF",
  original_source: {record_id: "MARK-RECORD", batch_id: "MARK-BATCH", case_id: "MARK-CASE",
    query_id: "MARK-QUERY", source: "MARK-SOURCE", status: "MARK-STATUS"}};
const item = (extra) => ({id: "EX-001", kind: "source_conflict", status: "open",
  owner_role: "data_steward", ...marker, ...extra});
const clean = [item({values: [{value: "MARK-VALUE-A"}, {value: "MARK-VALUE-B"}]}),
  item({id: "EX-002", kind: "failed_ai_run", owner_role: "digital_operator"}),
  item({id: "EX-010", kind: "stranded_task"})];
const base = (items, extra = {}) => ({state: "ok", items, unrouted: [], sources: [],
  banner: {state: "unknown", text: "x"}, access: {roles: {}, scope: {}}, note: "n", ...extra});
const odd = [
  item({id: "EX-001", kind: "constructor", status: "closed", owner_role: "a@b.test"}),
  item({id: "EX-002", kind: "future_kind", status: 5, owner_role: {}}),
  item({id: "EX-003", kind: "__proto__", status: null, owner_role: null}),
  item({id: "EX-004", kind: "identity_conflict", status: "open", owner_role: "data_steward"})];

async function scenario(name, data, opts = {}) {
  const calls = [], made = [], revoked = [], clicks = [], timers = [];
  let removed = 0, appended = 0;
  const listeners = {};
  const controller = new AbortController();
  const context = vm.createContext({
    URLSearchParams, Intl, AbortController, Date,
    location: {hash: "#/screens?screen=data-operator&exceptions=1"},
    routeController: controller, me: {user: {role: "Retrofit Programme Manager"}},
    api: async (path, body) => { calls.push({path, write: body !== undefined}); return data; },
    Blob: class {
      constructor(parts, o) {
        if (opts.blobFails) throw new Error("no blob");
        this.text = parts.join("");
        this.type = o.type;
      }
    },
    URL: {createObjectURL: (b) => {
        made.push({text: b.text, type: b.type});
        return "blob:synthetic-" + made.length;
      },
      revokeObjectURL: (u) => revoked.push(u)},
    document: {createElement: () => ({
        click() {
          if (opts.clickFails) throw new Error("blocked");
          clicks.push(this.download + "|" + this.href);
        },
        remove() { removed += 1; }}),
      body: {append() { appended += 1; }}},
    setTimeout: (fn) => timers.push(fn),
    h: (tag, attrs, ...kids) => {
      const node = {tag, attrs, kids: kids.flat(Infinity).filter(
        kid => kid !== false && kid !== null && kid !== undefined)};
      Object.defineProperty(node, "addEventListener",
        {value: (type, fn) => { listeners[type] = fn; }});
      return node;
    }
  });
  vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
  const out = await context.__s.overview(controller.signal, [], null);
  const find = (n, tag, found = []) => {
    if (n && typeof n === "object") {
      if (n.tag === tag) found.push(n);
      (n.kids || []).forEach(k => find(k, tag, found));
    }
    return found;
  };
  const buttons = find(out, "button");
  const statusNode = find(out, "p").find(p => p.attrs && p.attrs.id === "exception-summary-status");
  const beforeCalls = calls.length;
  if (buttons.length && listeners.click) listeners.click();
  const afterClick = {calls: calls.length - beforeCalls, made: made.length,
    revoked: revoked.length};
  timers.forEach(fn => fn());
  return {name, buttons: buttons.length, button: buttons[0] && buttons[0].attrs,
    status: statusNode ? (statusNode.textContent ?? "") : null,
    made, clicks, removed, appended, revoked, afterClick,
    statusAttrs: statusNode && statusNode.attrs, host: context};
}
(async () => {
  const results = await Promise.all([
    scenario("clean", base(clean)),
    scenario("odd", base(odd)),
    scenario("empty", base([])),
    scenario("roles", base(clean, {state: "roles_not_named"})),
    scenario("unreadable", base([...clean, 7])),
    scenario("badid1", base([item({id: "EX-1"})])),
    scenario("badid2", base([item({id: "=EX-001"})])),
    scenario("badid3", base([item({id: "EX-001\n"})])),
    scenario("blobfail", base(clean), {blobFails: true}),
    scenario("clickfail", base(clean), {clickFails: true}),
  ]);
  const ctx = vm.createContext({h: () => ({}), Date});
  vm.runInContext(host, ctx);
  const strings = JSON.parse(process.argv[2]);
  const cells = strings.map((s) => vm.runInContext("exceptionSummaryCell", ctx)(s));
  console.log(JSON.stringify({results: results.map(({host, ...r}) => r), cells}));
})();
"""


HOST_SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const register = {state: "ok", items: [{id: "EX-900", kind: "source_conflict", status: "open",
    owner: "synthetic.steward@example.test", owner_role: "data_steward", eligibility: "Unknown",
    runbook: "Synthetic", values: [{value: "D", source: "S-A", date: "2026-01-01", version: "1"},
      {value: "C", source: "S-B", date: "2026-01-02", version: "2"}]}],
  unrouted: [], sources: [], banner: {state: "unknown", text: "Synthetic banner."},
  access: {roles: {}, scope: {}}, note: "Synthetic note."};
const rows = [{id: "C-1", address: "1 Synthetic Road", status: "open"}];
async function scenario(name, role, hash, exceptions) {
  const calls = [];
  const shown = [];
  const controller = new AbortController();
  const context = vm.createContext({
    URLSearchParams, Intl, AbortController, Date, Promise,
    location: {hash}, routeController: controller, me: {user: {role}},
    workspaceStatus: {textContent: ""},
    show: (...kids) => shown.push(kids),
    api: async (path, body, signal) => {
      calls.push({path, write: body !== undefined});
      if (path.startsWith("/api/exceptions")) return exceptions(controller, signal);
      if (path.startsWith("/api/cases?")) return {items: rows, total: 1};
      return {id: "C-1", stock_reconciliation_events: [], stock_queries: []};
    },
    h: (tag, attrs, ...kids) => ({tag, attrs, addEventListener() {},
      kids: kids.flat(Infinity).filter(
        kid => kid !== false && kid !== null && kid !== undefined)})
  });
  vm.runInContext(host + "\n;globalThis.__view = roleScreensView;", context);
  let error = null;
  try { await context.__view(); } catch (e) { error = e.name || String(e); }
  return {name, calls, shown, error};
}
const manager = "Retrofit Programme Manager";
const link = "#/screens?screen=data-operator";
const denied = () => {
  const e = new Error("Only a named data steward or digital operator can see this.");
  e.status = 403;
  throw e;
};
(async () => {
  const results = await Promise.all([
    scenario("loaded", manager, link + "&exceptions=1", async () => register),
    scenario("default", manager, link, async () => { throw new Error("must not load"); }),
    scenario("other_role", "Retrofit Coordinator", link + "&exceptions=1", async () => register),
    scenario("stale", manager, link + "&exceptions=1", async (controller) => {
      controller.abort();
      return register;
    }),
    scenario("denied", manager, link + "&exceptions=1", denied)
  ]);
  console.log(JSON.stringify(results));
})();
"""


def run_host() -> dict[str, dict[str, Any]]:
    result = subprocess.run(
        ["node", "-e", HOST_SCRIPT, str(WEB)], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    return {r["name"]: r for r in json.loads(result.stdout)}


class HostIntegration(unittest.TestCase):
    """The existing role-screen host reaches the register only for managers and on request."""

    out: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = run_host()

    def test_manager_request_reaches_the_endpoint_once_with_the_page_summary(self) -> None:
        result = self.out["loaded"]
        paths = [call["path"] for call in result["calls"]]
        self.assertEqual(paths.count("/api/exceptions"), 1)
        self.assertIn("/api/cases/C-1", paths)
        self.assertFalse(any(call["write"] for call in result["calls"]))
        page = text(result["shown"][-1])
        for phrase in (
            "EX-900",
            "Source conflicts with every returned value",
            "No winning source is selected",
            "Choose a home",
        ):
            self.assertIn(phrase, page)

    def test_register_is_not_requested_without_the_explicit_link(self) -> None:
        result = self.out["default"]
        self.assertNotIn("/api/exceptions", [call["path"] for call in result["calls"]])
        self.assertIn("Open the exception register", text(result["shown"][-1]))

    def test_other_roles_never_reach_the_screen_or_the_endpoint(self) -> None:
        result = self.out["other_role"]
        self.assertEqual(result["calls"], [])
        self.assertIn("not installed for your signed-in role", text(result["shown"]))

    def test_superseded_navigation_never_renders_the_register(self) -> None:
        result = self.out["stale"]
        self.assertEqual(result["error"], "AbortError")
        self.assertNotIn("EX-900", text(result["shown"]))
        self.assertEqual(len(result["shown"]), 1)

    def test_denial_shows_no_rows_inside_the_page(self) -> None:
        page = text(self.out["denied"]["shown"][-1])
        self.assertIn("Access denied. Only a named data steward", page)
        self.assertNotIn("EX-900", page)


CSV_STRINGS = [
    "=1+1",
    "+1",
    "-1",
    "@x",
    "\tx",
    "\rx",
    "a,b",
    'say "hi"',
    "line\nbreak",
    "a\r\nb",
    "plain",
    "'=already",
    " lead",
    "EX-001",
    "Source conflict",
]
FILE = "exception-register-visible-summary.csv"
CLEAN_CSV = (
    "Reference in this view,Kind,State,Configured owner role\r\n"
    "EX-001,Source conflict,open,data_steward\r\n"
    "EX-002,Requested AI help did not deliver a model result,open,digital_operator\r\n"
    "EX-010,Stranded work,open,data_steward\r\n"
)
ODD_CSV = (
    "Reference in this view,Kind,State,Configured owner role\r\n"
    "EX-001,Unknown,Unknown,Unknown\r\n"
    "EX-002,Unknown,Unknown,Unknown\r\n"
    "EX-003,Unknown,Unknown,Unknown\r\n"
    "EX-004,Identity conflict,open,data_steward\r\n"
)


def run_csv() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", CSV_SCRIPT, str(WEB), json.dumps(CSV_STRINGS)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


class ExceptionSummaryCsv(unittest.TestCase):
    """Browser-built four-column summary: exact bytes, fail-closed offers, no request (#80)."""

    scenarios: dict[str, dict[str, Any]]
    cells: list[str]

    @classmethod
    def setUpClass(cls) -> None:
        parsed = run_csv()
        cls.scenarios = {r["name"]: r for r in parsed["results"]}
        cls.cells = parsed["cells"]

    def test_clean_list_offers_one_native_button_and_exact_bytes(self) -> None:
        clean = self.scenarios["clean"]
        self.assertEqual(clean["buttons"], 1)
        self.assertEqual(clean["button"]["type"], "button")
        self.assertEqual(clean["button"]["aria-describedby"], "exception-summary-note")
        self.assertEqual(clean["statusAttrs"]["role"], "status")
        self.assertEqual(len(clean["made"]), 1)
        self.assertEqual(clean["made"][0], {"text": CLEAN_CSV, "type": "text/csv;charset=utf-8"})
        self.assertFalse(clean["made"][0]["text"].startswith("\ufeff"))
        self.assertEqual(clean["status"], f"Download started: 3 rows, {FILE}")

    def test_no_excluded_field_reaches_the_file(self) -> None:
        body = self.scenarios["clean"]["made"][0]["text"]
        self.assertNotIn("MARK", body)
        self.assertNotIn("example.test", body)

    def test_activation_makes_no_request_and_cleans_up(self) -> None:
        clean = self.scenarios["clean"]
        self.assertEqual(clean["afterClick"], {"calls": 0, "made": 1, "revoked": 0})
        self.assertEqual(clean["clicks"], [f"{FILE}|blob:synthetic-1"])
        self.assertEqual((clean["appended"], clean["removed"]), (1, 1))
        self.assertEqual(clean["revoked"], ["blob:synthetic-1"])

    def test_values_outside_the_allowlists_export_as_unknown(self) -> None:
        self.assertEqual(self.scenarios["odd"]["made"][0]["text"], ODD_CSV)

    def test_unsafe_or_incomplete_views_offer_no_file(self) -> None:
        for name in ("empty", "roles", "unreadable", "badid1", "badid2", "badid3"):
            result = self.scenarios[name]
            self.assertEqual((result["buttons"], result["made"]), (0, []), name)

    def test_failure_reports_no_file_and_releases_everything(self) -> None:
        for name in ("blobfail", "clickfail"):
            result = self.scenarios[name]
            self.assertTrue(
                result["status"].startswith("No file was created or the download"), name
            )
            self.assertIn("Nothing was changed.", result["status"], name)
            self.assertEqual(result["removed"], result["appended"], name)
        self.assertEqual(self.scenarios["clickfail"]["revoked"], ["blob:synthetic-1"])

    def test_cell_escaping_matches_the_repository_helper(self) -> None:
        for value, got in zip(CSV_STRINGS, self.cells, strict=True):
            buf = io.StringIO()
            csv.writer(buf).writerow([safe_cell(value), "x"])
            self.assertEqual(got, buf.getvalue()[: -len(",x\r\n")], repr(value))


if __name__ == "__main__":
    unittest.main()
