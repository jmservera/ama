"""Steward and operator state indicators are written and keyboard reachable (#229, WCAG 2.2)."""

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
const data = JSON.parse(process.argv[2]);
const h = (tag, attrs, ...kids) => ({tag, attrs: attrs || {}, addEventListener() {},
  kids: kids.flat(Infinity).filter(kid => kid !== false && kid !== null && kid !== undefined)});
const controller = new AbortController();
const context = vm.createContext({URLSearchParams, Intl, AbortController, Date,
  location: {hash: "#/screens?screen=data-operator&exceptions=1"}, routeController: controller,
  me: {user: {role: "Retrofit Programme Manager"}}, api: async () => data, h});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
context.__s.overview(controller.signal, [], null).then(out => console.log(JSON.stringify(out)));
"""

BASE: dict[str, Any] = {
    "state": "ok",
    "items": [
        {
            "id": "EX-001",
            "kind": "failed_import",
            "status": "open",
            "owner": "Sam",
            "owner_role": "data_steward",
            "summary": "Batch refused.",
            "original_source": {"status": "Quarantined", "batch_id": "B-1"},
        }
    ],
    "unrouted": [],
    "sources": [],
    "banner": {"state": "unknown", "text": "Unknown."},
    "access": {"roles": {}, "scope": {}},
    "note": "Synthetic.",
}

INDICATORS: dict[str, Any] = {
    "lineage": {"state": "stale", "as_of": "2026-11-01"},
    "sensor_feed": {"state": "degraded"},
    "ai_tasks": [{"task": "summary", "enabled": False}, {"task": "triage", "enabled": True}],
}


def render(contract: dict[str, Any]) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(contract)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    tree: dict[str, Any] = json.loads(result.stdout)
    return tree


def walk(node: Any) -> list[dict[str, Any]]:
    if not isinstance(node, dict):
        return []
    found = [node]
    for kid in node.get("kids", []):
        found += walk(kid)
    return found


def text(node: Any) -> str:
    if isinstance(node, str):
        return node
    return " ".join(text(kid) for kid in node.get("kids", []))


def glance(tree: dict[str, Any]) -> str:
    nodes = walk(tree)
    index = next(i for i, n in enumerate(nodes) if text(n) == "State at a glance")
    return " ".join(text(n) for n in nodes[index + 1 :] if n.get("tag") == "dl")[:2000]


class DataStewardScreenWcag(unittest.TestCase):
    def test_supplied_states_are_written_out(self) -> None:
        page = glance(render({**BASE, "indicators": INDICATORS}))
        for phrase in (
            "State: Stale",
            "State: Quarantined (1 item listed below)",
            "State: Degraded",
            "AI task: summary State: Disabled",
            "AI task: triage State: Enabled",
        ):
            self.assertIn(phrase, page)

    def test_missing_states_read_unknown_not_healthy(self) -> None:
        page = glance(render(BASE))
        self.assertIn("Lineage freshness State: Unknown", page)
        self.assertIn("Sensor feed health State: Unknown", page)
        self.assertIn("State: Unknown. No task settings were returned", page)
        self.assertNotIn("Fresh", page)
        self.assertNotIn("Healthy", page)
        self.assertNotIn("Enabled", page)

    def test_unrecognised_state_value_is_unknown(self) -> None:
        bad = {"lineage": {"state": "green"}, "sensor_feed": {"state": 3}}
        page = glance(render({**BASE, "indicators": bad}))
        self.assertIn("Lineage freshness State: Unknown", page)
        self.assertIn("Sensor feed health State: Unknown", page)

    def test_inherited_object_keys_are_unknown(self) -> None:
        bad = {"lineage": {"state": "constructor"}, "sensor_feed": {"state": "toString"}}
        page = glance(render({**BASE, "indicators": bad}))
        self.assertIn("Lineage freshness State: Unknown", page)
        self.assertIn("Sensor feed health State: Unknown", page)

    def test_section_jump_buttons_target_focusable_headings(self) -> None:
        nodes = walk(render(BASE))
        navs = [n for n in nodes if n.get("tag") == "nav"]
        self.assertEqual(len(navs), 1)
        self.assertEqual(navs[0]["attrs"]["aria-label"], "Data stewardship sections")
        buttons = [n for n in walk(navs[0]) if n.get("tag") == "button"]
        self.assertEqual(len(buttons), 4)
        headings = {
            n["attrs"].get("id"): n["attrs"].get("tabindex") for n in nodes if n.get("tag") == "h3"
        }
        for button in buttons:
            self.assertEqual(button["attrs"]["type"], "button")
            self.assertEqual(headings.get(button["attrs"]["data-jump-target"]), "-1")

    def test_no_quarantine_is_not_an_all_clear(self) -> None:
        page = glance(render({**BASE, "items": []}))
        self.assertIn("None returned, which is not an all clear", page)

    def test_indicators_are_read_only_and_add_no_status_or_invalid_markup(self) -> None:
        tree = render({**BASE, "indicators": INDICATORS})
        nodes = walk(tree)
        self.assertFalse([n for n in nodes if n.get("tag") in ("input", "select")])
        self.assertFalse([n for n in nodes if "aria-invalid" in n["attrs"]])
        statuses = [n for n in nodes if n["attrs"].get("role") == "status"]
        plain = [n for n in walk(render(BASE)) if n["attrs"].get("role") == "status"]
        self.assertEqual(len(statuses), len(plain))

    def test_tables_stay_keyboard_reachable_and_named(self) -> None:
        tree = render({**BASE, "indicators": INDICATORS})
        regions = [n for n in walk(tree) if n["attrs"].get("role") == "region"]
        self.assertTrue(regions)
        for region in regions:
            self.assertEqual(region["attrs"].get("tabindex"), 0)
            self.assertTrue(region["attrs"].get("aria-label"))
        self.assertTrue(all(n["kids"] for n in walk(tree) if n.get("tag") == "caption"))


if __name__ == "__main__":
    unittest.main()
