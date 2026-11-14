"""Issue #225 finance and grants WCAG 2.2 jump-link delegation and conformance checks."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from test_finance_grants_screens import CASE, QUEUE, REVIEW, WEB, run, walk
    from test_finance_screen_wcag import JUMP_IDS, FinanceScreenWcagTests
else:
    _tests_dir = str(Path(__file__).resolve().parent)
    if _tests_dir not in sys.path:
        sys.path.insert(0, _tests_dir)
    _grants = importlib.import_module("test_finance_grants_screens")
    CASE = _grants.CASE
    QUEUE = _grants.QUEUE
    REVIEW = _grants.REVIEW
    WEB = _grants.WEB
    run = _grants.run
    walk = _grants.walk
    _wcag = importlib.import_module("test_finance_screen_wcag")
    JUMP_IDS = _wcag.JUMP_IDS
    FinanceScreenWcagTests = _wcag.FinanceScreenWcagTests

__all__ = ["FinanceScreenJumpDelegationTests", "FinanceScreenWcagTests"]

DELEGATED_CLICK_SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const data = JSON.parse(process.argv[2]);
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
  routeController: new AbortController(), me: {user: {role: "Grants and Evidence Officer"}},
  api: async (path) => {
    if (path === "/api/finance") return data.queue;
    if (path.startsWith("/api/ai/report")) throw new Error("403");
    if (path.endsWith("/proposal-freshness")) return {};
    if (path.endsWith("/form-review")) return data.review;
    return {};
  },
  h: (tag, attrs, ...kids) => ({tag, attrs: attrs || {}, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
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
    ? {getAttribute: (name) => Object.prototype.hasOwnProperty.call(linkNode.attrs, name)
        ? String(linkNode.attrs[name]) : null}
    : null;
  const event = {
    preventDefault() { prevented += 1; },
    target: {closest: (selector) => (selector === "a[data-jump]" ? linkElement : null)},
  };
  for (const listener of clickListeners) listener(event);
};

vm.runInContext(host + "\n;globalThis.__s = roleScreens;", context);
(async () => {
  for (const id of ["finance-invoices", "finance-funding"]) {
    const screen = context.__s.get(id);
    const extra = await screen.load(data.case);
    const tree = await screen.render(data.case, extra);
    activeTargets = new Map(
      collect(tree, (n) => n.tag === "div" && n.attrs.id && n.attrs.tabindex === "-1")
        .map((n) => [n.attrs.id, {focus() { focused.push([id, n.attrs.id]); }}])
    );
    const links = collect(tree, (n) => n.tag === "a" && n.attrs["data-jump"]);
    for (const link of links) dispatchClick(link);
    if (id === "finance-invoices") {
      activeTargets.delete("finance-queue");
      dispatchClick(links[0]);
      dispatchClick(null);
    }
  }
  console.log(JSON.stringify({listeners: clickListeners.length, prevented, focused}));
})().catch((err) => { console.error(err); process.exitCode = 1; });
"""


class FinanceScreenJumpDelegationTests(unittest.TestCase):
    def test_jump_links_delegate_via_data_jump_without_inline_onclick(self) -> None:
        rendered = run()
        for screen, expected_ids in JUMP_IDS.items():
            links = [
                n for n in walk(rendered[screen]["tree"]) if (n.get("attrs") or {}).get("data-jump")
            ]
            self.assertEqual({n["attrs"]["data-jump"] for n in links}, expected_ids, screen)
            for link in links:
                attrs: dict[str, Any] = link["attrs"]
                self.assertEqual(attrs["data-jump"], attrs["data-jump-target"])
                self.assertNotIn("onclick", attrs)

    def test_delegated_click_prevents_default_focuses_targets_and_tolerates_missing_node(
        self,
    ) -> None:
        payload = json.dumps({"case": CASE, "review": REVIEW, "queue": QUEUE})
        result = subprocess.run(
            ["node", "-e", DELEGATED_CLICK_SCRIPT, str(WEB), payload],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(observed["listeners"], 1)
        self.assertEqual(observed["prevented"], 7)
        self.assertEqual(
            observed["focused"],
            [
                ["finance-invoices", "finance-queue"],
                ["finance-invoices", "finance-lines"],
                ["finance-invoices", "finance-economics"],
                ["finance-funding", "grant-pack"],
                ["finance-funding", "funding-summary"],
                ["finance-funding", "finance-economics"],
            ],
        )


if __name__ == "__main__":
    unittest.main()
