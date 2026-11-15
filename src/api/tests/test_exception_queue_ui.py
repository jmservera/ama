"""Interactive #/exceptions employee workbench view and controlled recovery tests (#135).

Executes shipped `mutationKey` and `exceptionsView` from `web/app.js` in Node's `vm`
against synthetic `/api/exceptions` and `/api/exceptions/recovery` contracts.
"""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

APP_JS = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/app.js"

NODE_HARNESS = r"""
const fs = require("node:fs");
const vm = require("node:vm");

const src = fs.readFileSync(process.argv[1], "utf8");
const headStart = src.indexOf("const SUPPORT_OWNER =");
const headEnd = src.indexOf("async function api(");
const excStart = src.indexOf("const EXCEPTIONS_READ_ERROR =");
const excEnd = src.indexOf("async function signOut(");
if (headStart < 0 || headEnd < 0 || excStart < 0 || excEnd < 0) {
  throw new Error("Could not slice mutationKey / ownedNotice / exceptionsView from app.js");
}
const slice = [
  src.slice(headStart, headEnd),
  src.slice(excStart, excEnd),
].join("\n");

function makeNode(tag, attrs = {}, kids = []) {
  const listeners = {};
  const cleanAttrs = {};
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k.startsWith("on") && typeof v === "function") {
      const evType = k.slice(2);
      listeners[evType] = listeners[evType] || [];
      listeners[evType].push(v);
    } else if (v !== false && v !== null && v !== undefined) {
      cleanAttrs[k] = v;
    }
  }
  const node = {
    tag,
    attrs: cleanAttrs,
    dataset: {},
    hidden: Boolean(attrs && attrs.hidden),
    value: attrs && attrs.value !== undefined ? String(attrs.value) : "",
    disabled: Boolean(attrs && attrs.disabled),
    focused: false,
    parent: null,
    kids: [],
    listeners,
    get textContent() {
      return this.kids.map((k) => (typeof k === "string" ? k : k.textContent)).join("");
    },
    set textContent(v) {
      this.kids = v === null || v === undefined || v === "" ? [] : [String(v)];
    },
    addEventListener(type, fn) {
      listeners[type] = listeners[type] || [];
      listeners[type].push(fn);
    },
    setAttribute(k, v) {
      this.attrs[k] = String(v);
      if (k === "disabled") this.disabled = true;
    },
    removeAttribute(k) {
      delete this.attrs[k];
      if (k === "disabled") this.disabled = false;
    },
    focus() {
      this.focused = true;
    },
    async dispatch(type) {
      let prevented = false;
      const ev = {
        type,
        preventDefault() {
          prevented = true;
        },
      };
      for (const fn of listeners[type] || []) {
        await fn(ev);
      }
      return prevented;
    },
  };
  for (const raw of kids.flat(Infinity)) {
    if (raw === false || raw === null || raw === undefined) continue;
    if (typeof raw === "object" && raw.tag) {
      raw.parent = node;
      node.kids.push(raw);
    } else {
      node.kids.push(String(raw));
    }
  }
  if (tag === "select" && !node.value) {
    const firstOpt = node.kids.find((k) => typeof k === "object" && k.tag === "option");
    if (firstOpt) node.value = String(firstOpt.attrs.value || "");
  }
  return node;
}

function serialize(node) {
  if (typeof node === "string") return node;
  return {
    tag: node.tag,
    attrs: node.attrs,
    hidden: node.hidden,
    value: node.value,
    disabled: node.disabled,
    focused: node.focused,
    kids: node.kids.map(serialize),
  };
}

function findAll(node, pred, out = []) {
  if (!node || typeof node === "string") return out;
  if (pred(node)) out.push(node);
  for (const k of node.kids) findAll(k, pred, out);
  return out;
}

const conflictItem = {
  id: "EX-001",
  kind: "source_conflict",
  recovery_key: "source_conflict:ZF-1:SQ-1",
  status: "open",
  owner: "steward@example.test",
  owner_role: "data_steward",
  resolution_owner: "steward@example.test",
  correlation_id: "ZF-1:SQ-1",
  summary: "Stock epc differs between sources for case ZF-1.",
  values: [
    { value: "D", source: "S-A", date: "2026-01-01", version: "1" },
    { value: "C", source: "S-B", date: "2026-02-01", version: "2" },
  ],
  eligibility: "Unknown",
  unresolved_eligibility: true,
  original_source: { case_id: "ZF-1", query_id: "SQ-1", field: "epc" },
  recovery_policy: {
    allowed_actions: ["hold", "resolve_by_owner"],
    automatic_replay: false,
    automatic_release: false,
    note: "Recovery is a recorded human request; nothing is replayed or sent automatically.",
  },
  recovery_context: {
    correlation_id: "ZF-1:SQ-1",
    ref: "ZF-1:SQ-1",
    owner: "steward@example.test",
    owner_role: "data_steward",
    allowed_actions: ["hold", "resolve_by_owner"],
    runbook: "Compare both recorded values with their source owners.",
    automatic_replay: false,
    automatic_release: false,
  },
  runbook: "Compare both recorded values with their source owners.",
  recovery: null,
  audit_trail: [],
};

const failedImportItem = {
  id: "EX-002",
  kind: "failed_import",
  failure_category: "failed_import",
  recovery_key: "failed_import:BATCH-9",
  ref: "BATCH-9",
  status: "open",
  owner: "steward@example.test",
  owner_role: "data_steward",
  correlation_id: "CORR-BATCH-9",
  summary: "Import batch BATCH-9 failed and needs human triage.",
  error: "Missing UPRN column <script>alert(1)</script>",
  eligibility: "Unknown",
  unresolved_eligibility: true,
  original_source: { batch_id: "BATCH-9", source_name: "stock.xlsx" },
  recovery_policy: {
    allowed_actions: ["hold", "request_rerun"],
    automatic_replay: false,
    automatic_release: false,
    note: "Recovery is a recorded human request; nothing is replayed or sent automatically.",
  },
  recovery_context: {
    correlation_id: "CORR-BATCH-9",
    ref: "BATCH-9",
    owner: "steward@example.test",
    owner_role: "data_steward",
    allowed_actions: ["hold", "request_rerun"],
    runbook: "Keep the unimported rows aside; fix the source extract with the data steward.",
    automatic_replay: false,
    automatic_release: false,
  },
  runbook: "Keep the unimported rows aside; fix the source extract with the data steward.",
  recovery: null,
  audit_trail: [],
};

const failedAiItem = {
  id: "EX-003",
  kind: "failed_ai_run",
  failure_category: "failed_ai_run",
  recovery_key: "failed_ai_run:R-AI-1",
  ref: "R-AI-1",
  status: "open",
  owner: "operator@example.test",
  owner_role: "digital_operator",
  correlation_id: "CORR-AI-1",
  summary: "AI task summary did not deliver a model result.",
  error: "Model timeout",
  eligibility: "Unknown",
  unresolved_eligibility: true,
  original_source: { record_id: "R-AI-1", task: "summary", case_ids: ["ZF-1"] },
  recovery_policy: {
    allowed_actions: ["hold", "request_rerun"],
    automatic_replay: false,
    automatic_release: false,
    note: "Recovery is a recorded human request; nothing is replayed or sent automatically.",
  },
  recovery_context: {
    correlation_id: "CORR-AI-1",
    ref: "R-AI-1",
    owner: "operator@example.test",
    owner_role: "digital_operator",
    allowed_actions: ["hold", "request_rerun"],
    runbook: "Continue with the manual path; check service health first.",
    automatic_replay: false,
    automatic_release: false,
  },
  runbook: "Continue with the manual path; check service health first.",
  recovery: null,
  audit_trail: [],
};

const strandedItem = {
  id: "EX-004",
  kind: "stranded_task",
  failure_category: "stranded_task",
  recovery_key: "stranded_task:case:ZF-1/hazards/0",
  ref: "case:ZF-1/hazards/0",
  status: "open",
  owner: "operator@example.test",
  owner_role: "digital_operator",
  correlation_id: "case:ZF-1/hazards/0",
  summary: "Task External safety service response has no accountable owner or missed its handoff.",
  error: "due 2020-01-01T00:00:00Z, completion Not evidenced",
  eligibility: "Unknown",
  unresolved_eligibility: true,
  original_source: { case_id: "ZF-1", source: "case:ZF-1/hazards/0" },
  recovery_policy: {
    allowed_actions: ["hold", "request_rerun"],
    automatic_replay: false,
    automatic_release: false,
    note: "Recovery is a recorded human request; nothing is replayed or sent automatically.",
  },
  recovery_context: {
    correlation_id: "case:ZF-1/hazards/0",
    ref: "case:ZF-1/hazards/0",
    owner: "operator@example.test",
    owner_role: "digital_operator",
    allowed_actions: ["hold", "request_rerun"],
    runbook: "Name a current staff owner on the case before moving the task forward.",
    automatic_replay: false,
    automatic_release: false,
  },
  runbook: "Name a current staff owner on the case before moving the task forward.",
  recovery: null,
  audit_trail: [],
};

const outagePayload = {
  state: "ok",
  items: [conflictItem, failedImportItem, failedAiItem, strandedItem],
  unrouted: ["Case ZF-9: stock query could not be read, so its conflicts are not routed."],
  sources: [
    "Stock reconciliation queries on open cases.",
    "Service outage status includes recorded AI continuity state; no live probe runs here.",
  ],
  banner: {
    state: "outage",
    text: "Service outage affecting ai_continuity:all_ai_work. Use the manual path.",
    last_checked: "2026-11-14T10:00:00Z",
    components: {
      "ai_continuity:all_ai_work": {
        since: "2026-11-14T09:55:00Z",
        note: "Provider quota exhausted (incident owner: Pam Lead)",
        recovered: false,
      },
    },
    next_steps: [
      "Continue urgent casework using manual records and direct staff handoffs.",
      "Do not retry failed model calls or imports until the digital operator confirms recovery.",
    ],
  },
  access: {
    roles: { "steward@example.test": ["data_steward", "digital_operator"] },
    viewer_roles: ["data_steward", "digital_operator"],
    allowed_kinds: ["source_conflict", "failed_import", "failed_ai_run", "stranded_task"],
    scope: {
      source_conflict: "data_steward",
      failed_import: "data_steward",
      failed_ai_run: "digital_operator",
      stranded_task: "digital_operator",
    },
  },
  note: "Recovery is a recorded human request; nothing is replayed or sent automatically.",
};

function createHarness(apiHandler) {
  let rendered = [];
  const calls = [];
  const ctx = vm.createContext({
    URLSearchParams,
    Intl,
    Date,
    AbortController,
    location: { hash: "#/exceptions" },
    routeController: new AbortController(),
    me: { user: { email: "steward@example.test", role: "Retrofit Programme Manager" } },
    h: (tag, attrs, ...kids) => makeNode(tag, attrs || {}, kids),
    show: (...nodes) => {
      const root = makeNode("main", {}, nodes);
      rendered = root.kids;
    },
    api: async (path, body, signal) => {
      calls.push({ path, body: body === undefined ? null : body, hasSignal: Boolean(signal) });
      return await apiHandler(path, body);
    },
  });
  vm.runInContext(
    slice + "\n;globalThis.__run = { exceptionsView, mutationKey };",
    ctx
  );
  return {
    ctx,
    calls,
    getRoot: () => makeNode("main", {}, rendered),
  };
}

(async () => {
  // Scenario 1: full outage + conflict + 3 failure kinds + controlled recovery submit -> closed
  const livePayload = JSON.parse(JSON.stringify(outagePayload));
  const full = createHarness(async (path, body) => {
    if (path === "/api/exceptions") return JSON.parse(JSON.stringify(livePayload));
    if (path === "/api/exceptions/recovery") {
      const target = livePayload.items.find((it) => it.recovery_key === body.key);
      target.status = body.action === "resolve_by_owner" ? "closed" : "held";
      target.recovery = {
        action: body.action,
        reason: body.reason,
        requested_by: "steward@example.test",
        at: "2026-11-14T10:05:00Z",
        automatic_replay: false,
        automatic_release: false,
      };
      target.audit_trail.push({
        action: body.action,
        reason: body.reason,
        by: "steward@example.test",
        at: "2026-11-14T10:05:00Z",
        replayed: false,
        released: false,
      });
      return JSON.parse(JSON.stringify(target));
    }
    throw new Error("Unexpected path " + path);
  });
  await full.ctx.__run.exceptionsView();
  const initialTree = serialize(full.getRoot());

  // Blank reason validation on EX-001 form
  const rootLive = full.getRoot();
  const isSafetyForm = (n) => n.tag === "form" && n.attrs.class === "safety-step";
  const firstForm = findAll(rootLive, isSafetyForm)[0];
  const firstTextarea = findAll(firstForm, (n) => n.tag === "textarea")[0];
  firstTextarea.value = "   ";
  await firstForm.dispatch("submit");
  const afterBlankSubmit = {
    callsCount: full.calls.length,
    ariaInvalid: firstTextarea.attrs["aria-invalid"],
    focused: firstTextarea.focused,
    tree: serialize(firstForm),
  };

  // Valid step 1 (hold) then step 2 (resolve_by_owner -> closed hides form)
  firstTextarea.value = "Checking certificate.";
  await firstForm.dispatch("submit");
  const rootAfterHold = full.getRoot();
  const updatedConflictForm = findAll(rootAfterHold, isSafetyForm)[0];
  const select2 = findAll(updatedConflictForm, (n) => n.tag === "select")[0];
  const textarea2 = findAll(updatedConflictForm, (n) => n.tag === "textarea")[0];
  select2.value = "resolve_by_owner";
  textarea2.value = "Verified S-B manually with stock team.";
  await updatedConflictForm.dispatch("submit");
  const afterCloseTree = serialize(full.getRoot());

  // Scenario 2: roles_not_named + unknown banner
  const unnamed = createHarness(async () => ({
    ...outagePayload,
    state: "roles_not_named",
    items: [],
    unrouted: ["No data steward or digital operator is named yet."],
    banner: {
      state: "unknown",
      text: "Service state has not been checked recently. Do not assume it is healthy.",
      last_checked: null,
      components: {},
      next_steps: [
        "Treat service and model health as unverified until an operator records a check.",
      ],
    },
    access: { roles: {}, viewer_roles: [], allowed_kinds: [], scope: {} },
  }));
  await unnamed.ctx.__run.exceptionsView();

  // Scenario 3: 403 denied
  const denied = createHarness(async () => {
    const err = new Error("Forbidden");
    err.status = 403;
    throw err;
  });
  await denied.ctx.__run.exceptionsView();

  // Scenario 4: network/server error
  const failedRead = createHarness(async () => {
    const err = new Error("Gateway down");
    err.status = 502;
    throw err;
  });
  await failedRead.ctx.__run.exceptionsView();

  // Scenario 5: mutationKey distinguishes distinct exception keys
  const mk1 = full.ctx.__run.mutationKey("/api/exceptions/recovery", {
    key: "source_conflict:ZF-1:SQ-1",
    action: "hold",
  });
  const mk2 = full.ctx.__run.mutationKey("/api/exceptions/recovery", {
    key: "failed_ai_run:R-AI-1",
    action: "hold",
  });

  process.stdout.write(
    JSON.stringify({
      initialTree,
      afterBlankSubmit,
      afterCloseTree,
      calls: full.calls,
      unnamedTree: serialize(unnamed.getRoot()),
      deniedTree: serialize(denied.getRoot()),
      failedReadTree: serialize(failedRead.getRoot()),
      mutationKeys: [mk1, mk2],
    })
  );
})();
"""


def _collect_text(node: Any) -> str:
    if isinstance(node, str):
        return node
    return " ".join(_collect_text(k) for k in node.get("kids", []))


def _collect_tags(node: Any, out: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    if out is None:
        out = []
    if isinstance(node, dict) and "tag" in node:
        out.append(node)
        for k in node.get("kids", []):
            _collect_tags(k, out)
    return out


class ExceptionQueueUiTests(unittest.TestCase):
    data: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        proc = subprocess.run(
            ["node", "-e", NODE_HARNESS, str(APP_JS)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.data = json.loads(proc.stdout)

    def test_renders_conflict_dual_values_resolution_owner_and_owned_failures(self) -> None:
        text = _collect_text(self.data["initialTree"])
        for expected in (
            "Data steward and digital operator exception queue",
            "Resolution owner",
            "steward@example.test",
            "no winning source is selected automatically",
            "S-A",
            "S-B",
            "failed_import",
            "CORR-BATCH-9",
            "failed_ai_run",
            "CORR-AI-1",
            "stranded_task",
            "case:ZF-1/hazards/0",
            "Unknown (unresolved eligibility preserved without silent overwrite)",
            "batch BATCH-9",
        ):
            self.assertIn(expected, text)
        # Untrusted markup in error text remains plain text, never parsed into a <script> tag.
        tags = {n["tag"] for n in _collect_tags(self.data["initialTree"])}
        self.assertNotIn("script", tags)
        self.assertIn("<script>alert(1)</script>", text)

    def test_surfaces_scoped_access_and_honest_outage_states_with_next_steps(self) -> None:
        outage_text = _collect_text(self.data["initialTree"])
        self.assertIn("Outage detected:", outage_text)
        self.assertIn("ai_continuity:all_ai_work", outage_text)
        self.assertIn("Pam Lead", outage_text)
        self.assertIn(
            "Continue urgent casework using manual records and direct staff handoffs.",
            outage_text,
        )
        self.assertIn(
            "Data steward (source conflicts, identity conflicts and failed imports)", outage_text
        )
        self.assertIn(
            "Digital operator (failed model calls, failed integrations and stranded tasks)",
            outage_text,
        )
        self.assertIn("source_conflict: data_steward", outage_text)
        unnamed_text = _collect_text(self.data["unnamedTree"])
        self.assertIn("Service health unverified:", unnamed_text)
        self.assertIn("No data steward or digital operator is named yet", unnamed_text)

    def test_controlled_recovery_validates_reason_posts_audit_trail_and_closes_without_replay(
        self,
    ) -> None:
        blank = self.data["afterBlankSubmit"]
        self.assertEqual(blank["callsCount"], 1)  # Only initial GET /api/exceptions ran.
        self.assertEqual(blank["ariaInvalid"], "true")
        self.assertTrue(blank["focused"])
        self.assertIn(
            "Enter the audit reason before recording a recovery decision",
            _collect_text(blank["tree"]),
        )

        post_calls = [c for c in self.data["calls"] if c["path"] == "/api/exceptions/recovery"]
        self.assertEqual(
            post_calls,
            [
                {
                    "path": "/api/exceptions/recovery",
                    "body": {
                        "key": "source_conflict:ZF-1:SQ-1",
                        "action": "hold",
                        "reason": "Checking certificate.",
                    },
                    "hasSignal": False,
                },
                {
                    "path": "/api/exceptions/recovery",
                    "body": {
                        "key": "source_conflict:ZF-1:SQ-1",
                        "action": "resolve_by_owner",
                        "reason": "Verified S-B manually with stock team.",
                    },
                    "hasSignal": False,
                },
            ],
        )
        after_text = _collect_text(self.data["afterCloseTree"])
        self.assertIn("Closed by named owner", after_text)
        self.assertIn("Verified S-B manually with stock team.", after_text)
        self.assertIn("Replayed: No. Released: No.", after_text)
        self.assertIn("Closed by the named owner. No further recovery action", after_text)
        # 4 items originally had 4 recovery forms; closing EX-001 leaves 3 open recovery forms.
        open_forms = [
            n
            for n in _collect_tags(self.data["afterCloseTree"])
            if n["tag"] == "form" and n.get("attrs", {}).get("class") == "safety-step"
        ]
        self.assertEqual(len(open_forms), 3)

    def test_mutation_key_deduplicates_per_exception_key_and_error_states_name_owners(self) -> None:
        mk1, mk2 = self.data["mutationKeys"]
        self.assertNotEqual(mk1, mk2)
        self.assertIn("source_conflict:ZF-1:SQ-1", mk1)
        denied_text = _collect_text(self.data["deniedTree"])
        self.assertIn("Owner: the programme owner.", denied_text)
        failed_text = _collect_text(self.data["failedReadTree"])
        self.assertIn("Owner: application support.", failed_text)
        self.assertIn("Check again", failed_text)

    def test_heading_hierarchy_and_table_semantics_hold_across_every_view_state(self) -> None:
        for state_name in ("initialTree", "unnamedTree", "deniedTree", "failedReadTree"):
            nodes = _collect_tags(self.data[state_name])
            headings = [int(n["tag"][1]) for n in nodes if n["tag"] in {"h1", "h2", "h3", "h4"}]
            self.assertGreaterEqual(len(headings), 1, state_name)
            self.assertEqual(headings[0], 1, state_name)
            self.assertEqual(headings.count(1), 1, state_name)
            for prev, curr in zip(headings, headings[1:], strict=False):
                self.assertLessEqual(curr, prev + 1, f"{state_name}: {headings}")
        tables = [n for n in _collect_tags(self.data["initialTree"]) if n["tag"] == "table"]
        self.assertGreaterEqual(len(tables), 1)
        for tbl in tables:
            captions = [k for k in tbl["kids"] if isinstance(k, dict) and k.get("tag") == "caption"]
            self.assertEqual(len(captions), 1)
            col_headers = [
                n
                for n in _collect_tags(tbl)
                if n["tag"] == "th" and n.get("attrs", {}).get("scope") == "col"
            ]
            self.assertGreaterEqual(len(col_headers), 2)


if __name__ == "__main__":
    unittest.main()
