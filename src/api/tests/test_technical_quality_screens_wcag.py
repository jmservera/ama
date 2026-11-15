"""Retrofit technical and quality screens WCAG 2.2 engineering checks (Refs #231, #151).

Executes the real role-screens.js inside Node vm and verifies keyboard jump
navigation, programmatic heading focus rings, explicit non-colour textual state
meaning, PAS 2035 acceptance-independence guards, row-header table semantics,
plain ASCII copy, and zero write or role-simulator controls. These automated
checks do not replace human assistive-technology validation (#151, #155).
"""

import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
CSS = (WEB / "style.css").read_text(encoding="utf-8")

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const payload = JSON.parse(process.argv[2]);
let clickHandler = null;
const elements = new Map();
const focused = [];
const scrolled = [];
const locationState = { hash: "#/screens?screen=technical-queue&case=C-1" };
const documentStub = {
  addEventListener(type, fn) {
    if (type === "click") clickHandler = fn;
  },
  getElementById(id) {
    return elements.get(id) || null;
  }
};
const context = vm.createContext({
  URLSearchParams,
  Intl,
  AbortController,
  Date,
  document: documentStub,
  location: locationState,
  routeController: new AbortController(),
  me: { user: { role: "Quality Inspector" } },
  api: async () => ({ total: 0, items: [] }),
  h: (tag, attrs, ...kids) => ({
    tag,
    attrs: attrs || {},
    kids: kids.flat(Infinity).filter((k) => k !== false && k !== null && k !== undefined)
  })
});
vm.runInContext(host + "\n;globalThis.__roles = roleScreens;", context);

function registerHeadings(node) {
  if (!node || typeof node !== "object") return;
  const id = node.attrs && node.attrs.id;
  if (id) {
    elements.set(id, {
      id,
      tag: node.tag,
      focus() { focused.push(id); },
      scrollIntoView(opts) { scrolled.push({ id, opts }); }
    });
  }
  for (const kid of node.kids || []) registerHeadings(kid);
}

const out = {};
for (const [name, spec] of Object.entries(payload.renders || {})) {
  const tree = context.__roles.get(spec.screen).render(spec.case);
  out[name] = tree;
  if (spec.register) registerHeadings(tree);
}

const clicks = [];
for (const action of payload.clicks || []) {
  let prevented = false;
  const linkObj = action.jump
    ? { getAttribute: (attr) => (attr === "data-jump" ? action.jump : null) }
    : null;
  clickHandler({
    target: { closest: (sel) => (sel === "a[data-jump]" ? linkObj : null) },
    preventDefault() { prevented = true; }
  });
  clicks.push({
    name: action.name,
    prevented,
    hash: locationState.hash,
    focused: [...focused],
    scrolled: [...scrolled]
  });
}
console.log(JSON.stringify({ out, clicks, hasClickHandler: typeof clickHandler === "function" }));
"""


def run_vm(
    renders: dict[str, dict[str, Any]], clicks: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps({"renders": renders, "clicks": clicks or []})],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def walk(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict) and "tag" in node:
        found.append(node)
        for kid in node.get("kids", []):
            found.extend(walk(kid))
    return found


def node_text(node: Any) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        return " ".join(part for part in (node_text(k) for k in node.get("kids", [])) if part)
    return ""


def dl_pairs(node: Any) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for dl in (n for n in walk(node) if n["tag"] == "dl"):
        kids = [k for k in dl.get("kids", []) if isinstance(k, dict)]
        for idx in range(0, len(kids) - 1, 2):
            if kids[idx]["tag"] == "dt" and kids[idx + 1]["tag"] == "dd":
                pairs.append((node_text(kids[idx]), node_text(kids[idx + 1])))
    return pairs


def signed(version: int = 2, by: str = "Alex Assessor") -> dict[str, Any]:
    return {"status": "Signed off", "version": version, "by": by, "history": []}


def side() -> dict[str, Any]:
    return {
        "value": "D",
        "source_id": "SRC-1",
        "version": "1",
        "date": "2024-01-10",
        "validation_state": "Verified",
    }


def technical_ready_case() -> dict[str, Any]:
    return {
        "id": "C-1",
        "stock_reconciliation": [
            {
                "id": "SQ-1",
                "field": "epc",
                "left": side(),
                "right": side(),
                "query_owner": {"name": "Dana Steward"},
            },
            {
                "id": "SQ-2",
                "field": "wall_type",
                "left": side(),
                "right": side(),
                "query_owner": {"name": "Dana Steward"},
            },
        ],
        "stock_reconciliation_events": [
            {"query_id": "SQ-1", "status": "Reconciled"},
            {"query_id": "SQ-2", "status": "Withdrawn"},
        ],
        "technical": {
            "design_version": 2,
            "design_name": "Priya Designer",
            "design_at": "2026-03-01T10:00:00Z",
            "versions": [{"note": "Updated ventilation calc"}],
            "signoffs": {
                key: signed(2) for key in ("assessment", "design", "building", "coordination")
            },
        },
        "technical_missing": [],
    }


def quality_record(state: str, **overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "measure": "Loft insulation",
        "state": state,
        "checklist": "Loft checklist",
        "checklist_version": "v1",
        "evidence_version": 1,
        "source": "Site upload",
        "submitted_by": "North Installers",
        "accepted_by": "Sam Inspector" if state in ("Accepted", "Handed over") else None,
        "defect": None,
        "items": [{"label": "Depth check", "evidence": "270mm photo"}],
    }
    base.update(overrides)
    return base


class TechnicalAndQualityWcagTests(unittest.TestCase):
    def test_jump_navigation_anchors_headings_and_delegated_click_focus(self) -> None:
        dup_quality = {
            "id": "C-1",
            "measures": ["Loft insulation", "Loft insulation"],
            "quality_handover_blockers": [],
            "quality": [
                quality_record("Submitted"),
                quality_record("Accepted", accepted_by="Sam Inspector"),
            ],
        }
        empty_quality = {
            "id": "C-1",
            "measures": ["Loft insulation"],
            "quality_handover_blockers": [],
            "quality": [],
        }
        vm_out = run_vm(
            renders={
                "tech": {
                    "screen": "technical-queue",
                    "case": technical_ready_case(),
                    "register": True,
                },
                "qual_dup": {
                    "screen": "quality-queue",
                    "case": dup_quality,
                    "register": True,
                },
                "qual_empty": {
                    "screen": "quality-queue",
                    "case": empty_quality,
                    "register": False,
                },
            },
            clicks=[
                {"name": "tech_jump", "jump": "technical-signoffs-heading"},
                {
                    "name": "qual_second_dup",
                    "jump": "quality-measure-loft-insulation-2-heading",
                },
                {"name": "missing_target", "jump": "does-not-exist-heading"},
                {"name": "non_jump_anchor", "jump": None},
            ],
        )
        self.assertTrue(vm_out["hasClickHandler"])

        for key in ("tech", "qual_dup", "qual_empty"):
            with self.subTest(screen=key):
                tree = vm_out["out"][key]
                nodes = walk(tree)
                nav = next(n for n in nodes if n["tag"] == "nav")
                self.assertEqual(nav["attrs"].get("aria-label"), "Sections on this screen")
                self.assertEqual(nav["attrs"].get("class"), "screen-links")
                # Direct <a> children keep flex-wrap spacing and avoid button semantics.
                self.assertTrue(all(kid["tag"] == "a" for kid in nav["kids"]))
                links = nav["kids"]
                sections = {
                    n["attrs"]["id"]: n
                    for n in nodes
                    if n["tag"] == "section" and "id" in n["attrs"]
                }
                self.assertEqual({a["attrs"]["href"][1:] for a in links}, set(sections))
                self.assertEqual(len(links), len(sections))
                for link in links:
                    sec_id = link["attrs"]["href"].removeprefix("#")
                    heading_id = f"{sec_id}-heading"
                    self.assertEqual(link["attrs"].get("data-jump"), heading_id)
                    self.assertEqual(link["attrs"].get("data-jump-target"), heading_id)
                    sec = sections[sec_id]
                    self.assertEqual(sec["attrs"].get("aria-labelledby"), heading_id)
                    h2 = next(n for n in walk(sec) if n["tag"] == "h2")
                    self.assertEqual(h2["attrs"].get("id"), heading_id)
                    self.assertEqual(h2["attrs"].get("tabindex"), -1)

        clicks = {c["name"]: c for c in vm_out["clicks"]}
        self.assertTrue(clicks["tech_jump"]["prevented"])
        self.assertEqual(clicks["tech_jump"]["hash"], "#/screens?screen=technical-queue&case=C-1")
        self.assertEqual(
            clicks["qual_second_dup"]["focused"],
            [
                "technical-signoffs-heading",
                "quality-measure-loft-insulation-2-heading",
            ],
        )
        self.assertEqual(
            clicks["qual_second_dup"]["scrolled"][-1],
            {
                "id": "quality-measure-loft-insulation-2-heading",
                "opts": {"block": "start"},
            },
        )
        self.assertTrue(clicks["missing_target"]["prevented"])
        self.assertFalse(clicks["non_jump_anchor"]["prevented"])

    def test_focus_ring_and_screen_css_invariants(self) -> None:
        self.assertIn(":focus-visible{outline:", CSS)
        self.assertRegex(
            CSS,
            r'\.screen-record\s+h2\[tabindex="-1"\]:focus-visible\s*\{[^}]*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)',
        )
        self.assertRegex(
            CSS,
            r"\.screen-evidence\s+th,\s*\.screen-evidence\s+td\s*\{\s*font-variant-numeric:\s*tabular-nums;\s*\}",
        )
        for selector in (r"\.screen-links", r"\.screen-record", r"\.table-scroll"):
            self.assertNotRegex(CSS, rf"{selector}[^{{]*\{{[^}}]*outline:\s*(none|0)")
        for block in re.findall(r"^\.screen-[^{]*\{[^}]*\}", CSS, flags=re.M):
            self.assertNotIn("animation", block)
            self.assertNotIn("transition", block)

    def test_technical_queue_textual_state_cues_and_ready_banner(self) -> None:
        blocked = technical_ready_case()
        blocked["stock_reconciliation"].append(
            {
                "id": "SQ-3",
                "field": "heating",
                "left": side(),
                "right": side(),
                "query_owner": {"name": "Dana Steward"},
            }
        )
        blocked["stock_reconciliation_events"].append({"query_id": "SQ-3", "status": "constructor"})
        blocked["technical"]["design_name"] = " "
        blocked["technical"]["signoffs"]["design"] = {
            "status": "Returned",
            "reason": "Heat loss gap",
            "history": [{"status": "Returned", "by": "Lead Coord"}],
        }
        blocked["technical"]["signoffs"]["building"] = {
            "status": "Needs reassessment",
            "reason": "Flue route changed",
            "history": [],
        }
        blocked["technical_missing"] = [
            {"item": "PAS survey photo", "assigned_to": "Retrofit Coordinator"}
        ]

        out = run_vm(
            renders={
                "ready": {"screen": "technical-queue", "case": technical_ready_case()},
                "blocked": {"screen": "technical-queue", "case": blocked},
            }
        )["out"]

        ready_nodes = walk(out["ready"])
        statuses = [n for n in ready_nodes if n["attrs"].get("role") == "status"]
        self.assertEqual(len(statuses), 1)
        self.assertEqual(statuses[0]["attrs"].get("class"), "status-line ok")
        banner = node_text(statuses[0])
        self.assertTrue(banner.startswith("Ready on record:"))
        self.assertIn("Recorded evidence is complete", banner)
        self.assertIn("This screen does not approve the stage.", banner)

        ready_pairs = dict(dl_pairs(out["ready"]))
        self.assertEqual(
            ready_pairs["Design state"],
            "Recorded: Design version 2 on record (not stage approval)",
        )
        # Pinned <dd> values required by browser tension and connected-home checks.
        self.assertEqual(ready_pairs["Current design version"], "2")
        self.assertEqual(ready_pairs["Recorded by"], "Priya Designer")

        ready_dump = json.dumps(out["ready"])
        self.assertIn("colour is never the only signal", ready_dump)
        self.assertIn("Recorded: Reconciled (recorded by a named person)", ready_dump)
        self.assertIn("Withdrawn: Withdrawn (recorded by a named person)", ready_dump)

        blocked_pairs = dict(dl_pairs(out["blocked"]))
        self.assertEqual(
            blocked_pairs["Design state"], "Action needed: Design record is incomplete"
        )
        blocked_dump = json.dumps(out["blocked"])
        self.assertIn("Cannot confirm readiness", blocked_dump)
        self.assertIn("Action needed: Unresolved", blocked_dump)
        self.assertIn("Action needed: Missing on record", blocked_dump)
        self.assertIn("Action needed: Returned", blocked_dump)
        self.assertIn("Action needed: Needs reassessment", blocked_dump)

    def test_quality_queue_textual_states_independence_and_reinspection(self) -> None:
        defect_base = {
            "description": "Unsealed loft hatch",
            "reason": "Air leakage gap",
            "owner": "North Installers",
            "raised_by": "Sam Inspector",
        }
        ownerless_defect = {**defect_base, "owner": "  "}
        ready_case = {
            "id": "C-1",
            "measures": ["Loft insulation"],
            "quality_handover_blockers": [],
            "quality": [
                quality_record(
                    "Handed over",
                    accepted_by="Sam Inspector",
                    defect=defect_base,
                    handover={"by": "Programme Lead", "at": "2026-03-02T12:00:00Z"},
                )
            ],
        }
        mixed_case = {
            "id": "C-1",
            "measures": ["Loft insulation"],
            "quality_handover_blockers": [],
            "quality": [
                quality_record("Returned", defect=ownerless_defect),
                quality_record("Fixed, awaiting reinspection", defect=defect_base),
                quality_record(
                    "Accepted",
                    accepted_by="north installers",
                    defect=defect_base,
                ),
                quality_record("constructor", accepted_by=None),
            ],
        }

        out = run_vm(
            renders={
                "ready": {"screen": "quality-queue", "case": ready_case},
                "mixed": {"screen": "quality-queue", "case": mixed_case},
            }
        )["out"]

        ready_statuses = [n for n in walk(out["ready"]) if n["attrs"].get("role") == "status"]
        self.assertEqual(len(ready_statuses), 1)
        self.assertEqual(ready_statuses[0]["attrs"].get("class"), "status-line ok")
        self.assertIn(
            "Ready on record. Every measure has accepted evidence and no open defect.",
            node_text(ready_statuses[0]),
        )
        ready_pairs = dict(dl_pairs(out["ready"]))
        self.assertEqual(ready_pairs["Measure state"], "Verified: Handed over")
        self.assertEqual(ready_pairs["Reinspection"], "Passed")
        self.assertEqual(
            ready_pairs["Reinspection state"],
            "Verified: Independent reinspection passed",
        )
        self.assertIn("Verified: Evidence noted", json.dumps(out["ready"]))
        self.assertIn("colour is never the only signal", json.dumps(out["ready"]))

        sections = [
            n
            for n in walk(out["mixed"])
            if n["tag"] == "section"
            and str(n["attrs"].get("id", "")).startswith("quality-measure-")
        ]
        self.assertEqual(len(sections), 4)

        returned_pairs = dict(dl_pairs(sections[0]))
        self.assertEqual(returned_pairs["Measure state"], "Action needed: Returned")
        self.assertEqual(
            returned_pairs["Defect owner"],
            "Action needed: Unassigned (no defect owner named)",
        )
        self.assertEqual(returned_pairs["Reinspection"], "Not yet possible")
        self.assertEqual(
            returned_pairs["Reinspection state"],
            "Action needed: Not yet possible until fix is recorded",
        )

        fixed_pairs = dict(dl_pairs(sections[1]))
        self.assertEqual(
            fixed_pairs["Measure state"],
            "Pending review: Fixed, awaiting reinspection",
        )
        self.assertEqual(fixed_pairs["Defect owner"], "North Installers")
        self.assertEqual(
            fixed_pairs["Reinspection state"],
            "Pending review: Awaiting independent reinspection",
        )

        # Self-accepted work must never render Verified on measure, check, or reinspection.
        self_pairs = dict(dl_pairs(sections[2]))
        self.assertTrue(self_pairs["Measure state"].startswith("Action needed: Accepted ("))
        self.assertEqual(self_pairs["Reinspection"], "Passed")
        self.assertEqual(
            self_pairs["Reinspection state"],
            "Action needed: Reinspection lacks independent named inspector",
        )
        self_dump = json.dumps(sections[2])
        self.assertNotIn("Verified:", self_dump)
        self.assertIn("Action needed: Evidence noted (acceptance incomplete)", self_dump)

        proto_pairs = dict(dl_pairs(sections[3]))
        self.assertEqual(proto_pairs["Measure state"], "Action needed: constructor")

    def test_tables_row_headers_plain_ascii_and_no_controls_or_simulator(self) -> None:
        tech_case = technical_ready_case()
        tech_case["technical"]["signoffs"]["design"] = {
            "status": "Returned",
            "reason": "Check calc",
            "history": [{"status": "Returned", "by": "Coord"}],
        }
        tech_case["technical_missing"] = [
            {"item": "Ventilation commissioning sheet", "assigned_to": "Coordinator"}
        ]
        qual_case = {
            "id": "C-1",
            "measures": ["Loft insulation"],
            "quality_handover_blockers": [],
            "quality": [
                quality_record(
                    "Submitted",
                    items=[
                        {"label": "Depth", "evidence": "270mm"},
                        {"label": "Eaves", "evidence": ""},
                    ],
                )
            ],
        }
        out = run_vm(
            renders={
                "tech": {"screen": "technical-queue", "case": tech_case},
                "qual": {"screen": "quality-queue", "case": qual_case},
            }
        )["out"]

        expected_counts = {"tech": 4, "qual": 1}
        for key, count in expected_counts.items():
            with self.subTest(screen=key):
                tree = out[key]
                nodes = walk(tree)
                regions = [n for n in nodes if n["attrs"].get("class") == "table-scroll"]
                tables = [n for n in nodes if n["tag"] == "table"]
                self.assertEqual(len(regions), count)
                self.assertEqual(len(tables), count)
                for region in regions:
                    self.assertEqual(region["attrs"].get("role"), "region")
                    self.assertEqual(region["attrs"].get("tabindex"), 0)
                    self.assertTrue(region["attrs"].get("aria-label"))
                for table in tables:
                    captions = [k for k in table["kids"] if k["tag"] == "caption"]
                    self.assertEqual(len(captions), 1)
                    self.assertTrue(node_text(captions[0]))
                    thead = next(k for k in table["kids"] if k["tag"] == "thead")
                    col_headers = [n for n in walk(thead) if n["tag"] == "th"]
                    self.assertTrue(col_headers)
                    for th in col_headers:
                        self.assertEqual(th["attrs"].get("scope"), "col")
                    tbody = next(k for k in table["kids"] if k["tag"] == "tbody")
                    rows = [k for k in tbody["kids"] if k["tag"] == "tr"]
                    self.assertTrue(rows)
                    for row in rows:
                        cells = row["kids"]
                        self.assertEqual(cells[0]["tag"], "th")
                        self.assertEqual(cells[0]["attrs"].get("scope"), "row")
                        self.assertTrue(all(c["tag"] == "td" for c in cells[1:]))

                for node in nodes:
                    self.assertNotIn(node["tag"], ("button", "form", "input", "select", "textarea"))
                    self.assertNotIn("onclick", node["attrs"])
                    self.assertNotIn("aria-invalid", node["attrs"])

                dumped = json.dumps(tree)
                self.assertNotIn("\u2014", dumped)
                lowered = dumped.lower()
                for forbidden in (
                    "role simulator",
                    "simulate role",
                    "switch role",
                    "view as",
                ):
                    self.assertNotIn(forbidden, lowered)


if __name__ == "__main__":
    unittest.main()
