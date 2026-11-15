"""Issue #226 Asset Executive and Board views WCAG 2.2 keyboard jump delegation and state cues."""

from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from test_asset_board_screen import WEB, run, walk
    from test_asset_exec_screen_wcag import EXPECTED_JUMP_SECTIONS
else:
    _tests_dir = str(Path(__file__).resolve().parent)
    if _tests_dir not in sys.path:
        sys.path.insert(0, _tests_dir)
    _asset_board = importlib.import_module("test_asset_board_screen")
    WEB = _asset_board.WEB
    run = _asset_board.run
    walk = _asset_board.walk
    _asset_wcag = importlib.import_module("test_asset_exec_screen_wcag")
    EXPECTED_JUMP_SECTIONS = _asset_wcag.EXPECTED_JUMP_SECTIONS

__all__ = ["AssetExecutiveWcagScreenTests"]

ASSET_VM_SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const payload = JSON.parse(process.argv[2]);
const clickListeners = [];
let activeTargets = new Map();
const focused = [];
let prevented = 0;

const document = {
  addEventListener(type, listener) {
    if (type === "click") clickListeners.push(listener);
  },
  getElementById(id) {
    return activeTargets.get(id) || null;
  },
};

const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date, document,
  routeController: new AbortController(),
  me: {user: {role: "Retrofit Programme Manager"}},
  api: async (path) => {
    if (path.startsWith("/api/ai/report")) {
      if (payload.report === "fail") throw new Error("unavailable");
      return payload.report;
    }
    if (path.startsWith("/api/asset/stock-queue")) {
      if (payload.queue === "fail") throw new Error("unavailable");
      return payload.queue;
    }
    return {total: 7, items: []};
  },
  h: (tag, attrs, ...kids) => ({
    tag,
    attrs: attrs || {},
    kids: kids.flat(Infinity).filter((kid) => kid !== false && kid !== null && kid !== undefined),
  }),
});

const collect = (node, predicate, out = []) => {
  if (node && typeof node === "object") {
    if (predicate(node)) out.push(node);
    for (const kid of node.kids || []) collect(kid, predicate, out);
  }
  return out;
};

const dispatchClick = (linkNode) => {
  const linkElement = linkNode
    ? {
        getAttribute: (name) =>
          Object.prototype.hasOwnProperty.call(linkNode.attrs, name)
            ? String(linkNode.attrs[name])
            : null,
      }
    : null;
  const event = {
    preventDefault() { prevented += 1; },
    target: linkNode === "bare"
      ? {}
      : {closest: (selector) => (selector === "a[data-jump]" ? linkElement : null)},
  };
  for (const listener of clickListeners) listener(event);
};

vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('asset-board');", context);
(async () => {
  const screen = context.__s;
  const extra = await screen.load(payload.case);
  const tree = await screen.render(payload.case, extra);
  activeTargets = new Map(
    collect(tree, (n) => n.tag === "h2" && n.attrs.id && n.attrs.tabindex === -1)
      .map((n) => [n.attrs.id, {focus() { focused.push(n.attrs.id); }}])
  );
  const links = collect(tree, (n) => n.tag === "a" && n.attrs["data-jump"]);
  for (const link of links) dispatchClick(link);
  activeTargets.delete("asset-boundary-heading");
  if (links[0]) dispatchClick(links[0]);
  dispatchClick(null);
  dispatchClick("bare");
  console.log(JSON.stringify({listeners: clickListeners.length, prevented, focused, tree}));
})().catch((err) => { console.error(err); process.exitCode = 1; });
"""


def _side(value: str, source_id: str, date: str) -> dict[str, str]:
    return {
        "value": value,
        "source_id": source_id,
        "date": date,
        "version": "1",
        "validation_state": "Unvalidated",
    }


def _default_case(
    events: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    owner = {"name": "Query Owner", "role": "Retrofit Programme Manager"}
    return {
        "id": "C-1",
        "stock_reconciliation": [
            {
                "id": "SQ-1",
                "field": "epc",
                "query_owner": owner,
                "left": _side("D", "S-A", "2020-01-01"),
                "right": _side("C", "S-B", "2026-01-01"),
            }
        ],
        "stock_reconciliation_events": events or [],
    }


def _default_queue() -> dict[str, object]:
    return {
        "items": [
            {
                "id": "C-9",
                "address": "1 Test Rd",
                "town": "Testville",
                "open_queries": 2,
                "fields": ["epc", "built"],
                "oldest_source_date": "2020-01-01",
                "owners": ["Query Owner"],
            }
        ]
    }


def _run_vm(
    case_payload: dict[str, object] | None = None,
    report: dict[str, object] | str | None = None,
    queue: dict[str, object] | str | None = None,
) -> dict[str, Any]:
    payload = json.dumps(
        {
            "case": case_payload if case_payload is not None else _default_case(),
            "report": report if report is not None else {"consumption": {"quality_status": "Pass"}},
            "queue": queue if queue is not None else _default_queue(),
        }
    )
    result = subprocess.run(
        ["node", "-e", ASSET_VM_SCRIPT, str(WEB), payload],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def _dl_pairs(node: object) -> list[tuple[str, str]]:
    items = [n for n in walk(node) if n.get("tag") in ("dt", "dd")]
    return [
        (str(dt["kids"][0]), str(dd["kids"][0]))
        for dt, dd in zip(items[0::2], items[1::2], strict=False)
    ]


def _table_rows(tree: object, caption: str) -> list[list[str]]:
    table = next(
        n for n in walk(tree) if n.get("tag") == "table" and n["kids"][0]["kids"] == [caption]
    )
    rows = [n for n in walk(table) if n.get("tag") == "tr"][1:]
    return [[str(cell["kids"][0]) for cell in row["kids"]] for row in rows]


class AssetExecutiveWcagScreenTests(unittest.TestCase):
    def test_delegated_jump_clicks_focus_all_ten_headings_and_tolerate_missing_targets(
        self,
    ) -> None:
        observed = _run_vm()
        expected_ids = [f"{sec_id}-heading" for sec_id, _ in EXPECTED_JUMP_SECTIONS]
        self.assertEqual(observed["listeners"], 1)
        self.assertEqual(observed["prevented"], len(expected_ids) + 1)
        self.assertEqual(observed["focused"], expected_ids)

    def test_conflict_queue_and_eligibility_expose_non_colour_textual_states(self) -> None:
        owner = {"name": "Query Owner", "role": "Retrofit Programme Manager"}
        variants: tuple[tuple[list[dict[str, object]], str], ...] = (
            ([], "Action needed: Unresolved"),
            (
                [{"query_id": "SQ-1", "status": "Reconciled", "actor": owner}],
                "Recorded: Reconciled (recorded by a named person)",
            ),
            (
                [{"query_id": "SQ-1", "status": "Withdrawn", "actor": owner}],
                "Withdrawn: Withdrawn (recorded by a named person)",
            ),
        )
        for events, expected_status in variants:
            with self.subTest(expected_status=expected_status):
                tree = _run_vm(case_payload=_default_case(events))["tree"]
                comparison_rows = _table_rows(tree, "Stock source conflicts and source age")
                self.assertEqual(comparison_rows[0][4], expected_status)

        default_tree = _run_vm()["tree"]
        queue_rows = _table_rows(default_tree, "Open stock conflicts by home")
        self.assertEqual(queue_rows[0][5], "State: Unknown. See missing investment inputs.")

        eligibility_section = next(
            n
            for n in walk(default_tree)
            if n.get("tag") == "section" and n.get("attrs", {}).get("id") == "asset-eligibility"
        )
        eligibility_pairs = _dl_pairs(eligibility_section)
        self.assertEqual(
            eligibility_pairs[:3],
            [
                ("Eligibility state", "State: Unknown. This page cannot confirm eligibility."),
                ("Eligibility", "Unknown"),
                ("Resolution owner", "Query Owner"),
            ],
        )

    def test_ai_cohort_and_usage_panels_prefix_states_and_handle_prototype_keys(self) -> None:
        unloaded_pairs = dict(_dl_pairs(run(None)["tree"]))
        self.assertEqual(
            unloaded_pairs["AI report"],
            (
                "State: Unavailable. The AI report could not be loaded, "
                "so every AI figure below is Unknown."
            ),
        )
        self.assertEqual(
            unloaded_pairs["Overall AI cost per accepted outcome"],
            "State: Unknown. Other cost components are not complete and quality-qualified.",
        )
        self.assertEqual(
            unloaded_pairs["Quality floor"],
            "State: Unknown. The AI report could not be loaded",
        )
        self.assertEqual(
            unloaded_pairs["Value status"],
            "State: Unknown. No finance-defensible value is recorded.",
        )
        self.assertEqual(unloaded_pairs["Evidence class"], "Unknown")

        recorded_tree = run(
            {
                "consumption": {
                    "quality_status": "Pass",
                    "cash_value": "120 GBP",
                    "currency": "GBP",
                    "total_cost_of_ai": "14.00",
                    "reconciliation": "reconciled",
                }
            }
        )["tree"]
        recorded_pairs = dict(_dl_pairs(recorded_tree))
        self.assertEqual(recorded_pairs["AI report"], "Loaded")
        self.assertEqual(recorded_pairs["Quality floor"], "State: Pass. As reported for all homes")
        self.assertEqual(recorded_pairs["Value status"], "State: Recorded. 120 GBP")
        self.assertEqual(recorded_pairs["Reconciliation with the bill"], "Recorded: reconciled")
        self.assertEqual(recorded_pairs["Total Cost of AI"], "State: Recorded. 14.00 GBP")

        reconciliation_cases: tuple[tuple[dict[str, object], str], ...] = (
            ({}, "State: Unknown"),
            ({"reconciliation": "unreconciled"}, "Action needed: unreconciled"),
            ({"reconciliation": "constructor"}, "Action needed: constructor"),
            ({"reconciliation": "toString"}, "Action needed: toString"),
        )
        for consumption, expected in reconciliation_cases:
            with self.subTest(consumption=consumption):
                pairs = dict(_dl_pairs(run({"consumption": consumption})["tree"]))
                self.assertEqual(pairs["Reconciliation with the bill"], expected)
                self.assertEqual(
                    pairs["Total Cost of AI"],
                    "State: Unknown. Every component below must be recorded first.",
                )

        for node in walk(recorded_tree):
            self.assertNotIn("style", node.get("attrs") or {})

    def test_stylesheet_jump_link_targets_and_tokenized_scroll_margin(self) -> None:
        css = (WEB / "style.css").read_text(encoding="utf-8")
        link_match = re.search(r"\.screen-links a\s*\{([^}]*)\}", css)
        self.assertIsNotNone(link_match)
        assert link_match is not None
        self.assertIn("min-height: 2.5rem", link_match.group(1))
        self.assertIn("display: inline-flex", link_match.group(1))

        margin_match = re.search(
            r"\.screen-record\[id\],\s*\.screen-evidence h2\[tabindex=\"-1\"\]\s*\{([^}]*)\}",
            css,
        )
        self.assertIsNotNone(margin_match)
        assert margin_match is not None
        self.assertIn("scroll-margin-top: var(--sp-5)", margin_match.group(1))
        self.assertIn(":focus-visible", css)


if __name__ == "__main__":
    unittest.main()
