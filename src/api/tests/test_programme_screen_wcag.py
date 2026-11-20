"""Programme queue and connected view meet WCAG 2.2 keyboard jump and textual state rules."""

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
const listeners = {};
let activeElement = null;
const targets = new Map();
const doc = {
  get activeElement() { return activeElement; },
  addEventListener: (type, fn) => { (listeners[type] ||= []).push(fn); },
  querySelectorAll: () => [],
  getElementById: (id) => targets.get(id) || null
};
const loc = {hash: "#/screens?screen=programme-queue"};
const returned = {id: "C-1", address: "1 Test Street", work: {owner: "Owen Owner", queues: [],
  returned: {reason: "Missing survey", sender: "Quinn Sender"}, handoff: null}};
const pending = {id: "C-2", address: "2 Test Street", work: {owner: "Owen Owner", queues: ["unowned"],
  resident_update_owner: "Una Updater", returned: null,
  handoff: {state: "Offered", sender: "Sam Sender", proposed_receiver: "Rae Receiver",
    chase_owner: "Sam Sender", resident_update_owner: "Una Updater"}}};
const plain = {id: "C-3", address: "3 Test Street", work: {owner: "Owen Owner", queues: [], returned: null, handoff: null}};
const makeRow = (n) => ({id: "C-" + n, address: n + " Test Street", work: {owner: "Owen", queues: [],
  returned: {reason: "Reason " + n, sender: "Sender"}, handoff: null}});
let coordinatorUp = true;
let pagingMode = false;
const context = vm.createContext({
  location: loc, history: {replaceState: (a, b, url) => { loc.hash = url; }},
  URLSearchParams, Intl, AbortController, Date,
  document: doc, routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  api: async (path) => {
    if (path.startsWith("/api/coordinator")) {
      if (!coordinatorUp) throw new Error("down");
      return {as_of: "2026-10-01", audit_integrity: "Intact",
        funnel: [{stage: "Funding check", entries: 3, exits: 2, returns: 1, reopens: 0, denominator: 9}]};
    }
    if (pagingMode) {
      const offset = Number(new URL(path, "http://x").searchParams.get("offset"));
      const total = 70;
      const count = Math.min(50, total - offset);
      return {total, items: Array.from({length: count}, (_, i) => makeRow(offset + i + 1))};
    }
    return {total: 3, items: [returned, pending, plain]};
  },
  h: (tag, attrs, ...kids) => {
    const clean = attrs || {};
    const node = {
      tag,
      attrs: clean,
      kids: kids.flat(Infinity).filter(k => k !== false && k !== null && k !== undefined)
    };
    Object.defineProperty(node, "replaceChildren", {value: (...k) => { node.kids = k; }});
    Object.defineProperty(node, "textContent", {set: (v) => { node.kids = [v]; }});
    Object.defineProperty(node, "disabled", {
      get: () => Boolean(node.attrs.disabled),
      set: (v) => { node.attrs.disabled = Boolean(v); }
    });
    Object.defineProperty(node, "focus", {
      value: () => {
        activeElement = node;
        focused.push(node.attrs.id || tag);
      }
    });
    Object.defineProperty(node, "getAttribute", {
      value: (name) => Object.hasOwn(node.attrs, name) ? String(node.attrs[name]) : null
    });
    if (clean.id) targets.set(clean.id, node);
    return node;
  }
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('programme-queue');", context);
(async () => {
  const s = context.__s;
  const bound = {measure: "Loft", context_revision: 2};
  const clear = {id: "C-8", work: {blockers: []}, technical: {}, measures: "Loft",
    measure_decisions: [{measure: "Loft", context: {revision: 2}}],
    quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}],
    finance: {budget: {status: "Approved"}}};
  const orders = [{id: "WO-1", state: "Appointed", appointment_control: {status: "Committed", missing: []},
    versions: [{resident_bindings: [bound]}]}];
  const overview = await s.overview(new AbortController().signal);
  // Filter to "all" snapshot as well so all three row state prefixes (Returned, Handoff, Not returned) are captured.
  const find = (n, pred, out = []) => {
    if (n && typeof n === "object") {
      if (pred(n)) out.push(n);
      (n.kids || []).forEach(k => find(k, pred, out));
    }
    return out;
  };
  const overviewDefault = JSON.parse(JSON.stringify(overview));
  const form = find(overview, n => n.tag === "form")[0];
  const select = find(form, n => n.tag === "select")[0];
  select.value = "all";
  form.attrs.onsubmit({preventDefault() {}});
  const overviewAll = JSON.parse(JSON.stringify(overview));

  coordinatorUp = false;
  const overviewDown = await s.overview(new AbortController().signal);
  coordinatorUp = true;

  // Register current overview + connected-home targets in targets map for delegated click checks.
  targets.clear();
  const blocked = s.render({id: "C-9", work: {blockers: []}}, {orders: null});
  const ok = s.render(clear, {orders});
  for (const tree of [overview, ok]) {
    find(tree, n => Boolean(n.attrs && n.attrs.id)).forEach(n => targets.set(n.attrs.id, n));
  }
  const jumpLinks = [
    ...find(overview, n => n.tag === "a" && Boolean(n.attrs["data-jump"])),
    ...find(ok, n => n.tag === "a" && Boolean(n.attrs["data-jump"]))
  ];
  let prevented = 0;
  const hashBefore = loc.hash;
  for (const link of jumpLinks) {
    for (const fn of listeners.click || []) {
      fn({
        target: {closest: (sel) => sel === "a[data-jump]" ? link : null},
        preventDefault: () => { prevented += 1; }
      });
    }
  }
  // Clicking a non-jump link must be ignored by the jump listener.
  for (const fn of listeners.click || []) {
    fn({
      target: {closest: () => null},
      preventDefault: () => { prevented += 100; }
    });
  }

  const jumpFocused = [...focused];

  // Verify pager focus handoff when boundary button disables while focused.
  pagingMode = true;
  const paged = await s.overview(new AbortController().signal);
  const prevBtn = find(paged, n => n.attrs && n.attrs.id === "programme-prev")[0];
  const nextBtn = find(paged, n => n.attrs && n.attrs.id === "programme-next")[0];
  const pagerFocus = [];
  activeElement = nextBtn;
  nextBtn.attrs.onclick();
  await new Promise(r => setTimeout(r, 0));
  pagerFocus.push(activeElement && activeElement.attrs.id);
  prevBtn.attrs.onclick();
  await new Promise(r => setTimeout(r, 0));
  pagerFocus.push(activeElement && activeElement.attrs.id);

  console.log(JSON.stringify({
    overview: overviewDefault,
    overviewAll,
    overviewDown,
    blocked,
    ok,
    focused: jumpFocused,
    prevented,
    hashUnchanged: loc.hash === hashBefore,
    pagerFocus
  }));
})().catch(e => { console.error(e); process.exitCode = 1; });
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
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = run()

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
        paragraphs = [text(p) for p in walk(self.out["ok"]) if p["tag"] == "p"]
        self.assertIn(
            "State: Warning. No blocker is recorded, which does not confirm readiness.",
            paragraphs,
        )

    def test_existing_state_cells_are_unchanged(self) -> None:
        cells = [text(td) for td in walk(self.out["blocked"]) if td["tag"] == "td"]
        self.assertIn("Blocked: evidence missing", cells)
        self.assertNotIn("Action needed: Blocked", cells)

    def test_overview_jump_nav_links_target_focusable_sections_in_order(self) -> None:
        overview = self.out["overview"]
        navs = [n for n in walk(overview) if n["tag"] == "nav"]
        self.assertEqual(len(navs), 1)
        nav = navs[0]
        self.assertEqual(
            nav["attrs"],
            {
                "aria-label": "Jump to a section of the programme overview",
                "class": "screen-links",
            },
        )
        expected = [
            "programme-overview-boundary",
            "programme-shared-queue",
            "programme-funnel",
            "programme-overview-withheld",
        ]
        links = nav["kids"]
        self.assertEqual([a["attrs"].get("data-jump") for a in links], expected)
        for link, target_id in zip(links, expected, strict=True):
            self.assertEqual(link["tag"], "a")
            self.assertEqual(link["attrs"].get("href"), f"#{target_id}")
            self.assertFalse(any(k.startswith("on") for k in link["attrs"]))
            self.assertTrue(text(link).startswith("Go to "))
        targets = [n for n in walk(overview) if n["attrs"].get("id") in expected]
        self.assertEqual([t["attrs"]["id"] for t in targets], expected)
        for target in targets:
            self.assertEqual(str(target["attrs"].get("tabindex")), "-1")
            nested = [n for n in walk(target)[1:] if n["attrs"].get("id") in expected]
            self.assertEqual(nested, [])

    def test_connected_home_jump_nav_links_target_focusable_sections_without_buttons(self) -> None:
        ok = self.out["ok"]
        navs = [n for n in walk(ok) if n["tag"] == "nav"]
        self.assertEqual(len(navs), 1)
        nav = navs[0]
        self.assertEqual(
            nav["attrs"],
            {
                "aria-label": "Jump to a section of the connected home view",
                "class": "screen-links",
            },
        )
        expected = [
            "programme-summary",
            "programme-steps",
            "programme-journey",
            "programme-withheld",
        ]
        links = nav["kids"]
        self.assertEqual([a["attrs"].get("data-jump") for a in links], expected)
        for link, target_id in zip(links, expected, strict=True):
            self.assertEqual(link["tag"], "a")
            self.assertEqual(link["attrs"].get("href"), f"#{target_id}")
            self.assertFalse(any(k.startswith("on") for k in link["attrs"]))
        targets = [n for n in walk(ok) if n["attrs"].get("id") in expected]
        self.assertEqual([t["attrs"]["id"] for t in targets], expected)
        for target in targets:
            self.assertEqual(str(target["attrs"].get("tabindex")), "-1")
            nested = [n for n in walk(target)[1:] if n["attrs"].get("id") in expected]
            self.assertEqual(nested, [])
        # Connected view panel still encloses both #programme-summary and #programme-steps.
        connected_panel = next(
            n
            for n in walk(ok)
            if n["tag"] == "section"
            and n["kids"]
            and text(n["kids"][0]) == "Connected view for C-8"
        )
        panel_ids = {n["attrs"].get("id") for n in walk(connected_panel)}
        self.assertTrue({"programme-summary", "programme-steps"}.issubset(panel_ids))
        # Stage map section itself carries zero internal tabindex attributes.
        journey = next(n for n in targets if n["attrs"]["id"] == "programme-journey")
        stage_section = journey["kids"][0]
        self.assertFalse(
            any("tabindex" in n["attrs"] for n in walk(stage_section)),
        )
        # Connected view remains strictly read-only with zero form/button controls.
        tags = {n["tag"] for n in walk(ok)}
        self.assertFalse(tags & {"button", "form", "input", "select", "textarea"})

    def test_simultaneous_overview_and_connected_view_have_disjoint_ids_and_distinct_jump_labels(
        self,
    ) -> None:
        combined_nodes = walk(self.out["overview"]) + walk(self.out["ok"])
        ids = [str(n["attrs"]["id"]) for n in combined_nodes if n["attrs"].get("id")]
        self.assertEqual(len(ids), len(set(ids)), ids)
        jump_labels = [
            text(n) for n in combined_nodes if n["tag"] == "a" and n["attrs"].get("data-jump")
        ]
        self.assertEqual(len(jump_labels), 8)
        self.assertEqual(len(jump_labels), len(set(jump_labels)), jump_labels)

    def test_delegated_jump_click_prevents_route_change_and_moves_focus_for_every_link(
        self,
    ) -> None:
        self.assertEqual(self.out["prevented"], 8)
        self.assertTrue(self.out["hashUnchanged"])
        self.assertEqual(
            self.out["focused"],
            [
                "programme-overview-boundary",
                "programme-shared-queue",
                "programme-funnel",
                "programme-overview-withheld",
                "programme-summary",
                "programme-steps",
                "programme-journey",
                "programme-withheld",
            ],
        )

    def test_returned_handoff_and_funnel_states_have_explicit_non_colour_textual_prefixes(
        self,
    ) -> None:
        queue_cells = [text(td) for td in walk(self.out["overviewAll"]) if td["tag"] == "td"]
        self.assertIn("State: Returned. Missing survey", queue_cells)
        self.assertIn("State: Not returned. Handoff state: Offered.", queue_cells)
        self.assertIn("State: Not returned", queue_cells)
        up_paragraphs = [text(p) for p in walk(self.out["overview"]) if p["tag"] == "p"]
        self.assertTrue(
            any(
                p.startswith("State: Recorded stage history (not a pass).")
                and "Audit integrity state: Intact." in p
                and "Conversion state: Unknown;" in p
                for p in up_paragraphs
            ),
            up_paragraphs,
        )
        down_paragraphs = [text(p) for p in walk(self.out["overviewDown"]) if p["tag"] == "p"]
        self.assertIn(
            "State: Unknown. Lifecycle and funnel counts could not be read. Owner: application "
            "support. Next action: refresh to try again, then contact application support if it "
            "continues.",
            down_paragraphs,
        )

    def test_queue_controls_live_regions_tables_and_pager_focus_handoff_are_keyboard_accessible(
        self,
    ) -> None:
        overview = self.out["overview"]
        for status_id in ("programme-filter-status", "programme-page-status"):
            region = next(n for n in walk(overview) if n["attrs"].get("id") == status_id)
            self.assertEqual(region["attrs"].get("role"), "status")
            self.assertEqual(region["attrs"].get("aria-live"), "polite")
        labels = [n for n in walk(overview) if n["tag"] == "label"]
        self.assertEqual([n["attrs"].get("for") for n in labels], ["programme-scope"])
        selects = [n for n in walk(overview) if n["tag"] == "select"]
        self.assertEqual([n["attrs"].get("id") for n in selects], ["programme-scope"])
        scroll_regions = [
            n
            for n in walk(overview) + walk(self.out["ok"])
            if n["attrs"].get("class") == "table-scroll"
        ]
        self.assertEqual(len(scroll_regions), 3)
        for region in scroll_regions:
            self.assertEqual(str(region["attrs"].get("tabindex")), "0")
            self.assertEqual(region["attrs"].get("role"), "region")
            self.assertTrue(region["attrs"].get("aria-label"))
            table = next(n for n in walk(region) if n["tag"] == "table")
            captions = [text(n) for n in walk(table) if n["tag"] == "caption"]
            self.assertEqual(len(captions), 1)
            thead = next(n for n in walk(table) if n["tag"] == "thead")
            col_headers = [n for n in walk(thead) if n["tag"] == "th"]
            self.assertTrue(
                col_headers and all(h["attrs"].get("scope") == "col" for h in col_headers)
            )
            tbody = next(n for n in walk(table) if n["tag"] == "tbody")
            row_trs = [n for n in tbody["kids"] if isinstance(n, dict) and n["tag"] == "tr"]
            self.assertTrue(row_trs)
            for tr in row_trs:
                first_cell = next(c for c in tr["kids"] if isinstance(c, dict))
                self.assertEqual(first_cell["tag"], "th")
                self.assertEqual(first_cell["attrs"].get("scope"), "row")
        # Focused Next on last page transfers focus to Previous, and back to Next on page 1.
        self.assertEqual(self.out["pagerFocus"], ["programme-prev", "programme-next"])


if __name__ == "__main__":
    unittest.main()
