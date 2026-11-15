"""Procurement, contractor and quality screens: text state meaning and keyboard (Refs #228).

Rendered through the real role-screens.js in Node. These are engineering checks, not
WCAG 2.2 conformance acceptance (#151).
"""

import json
import subprocess
import unittest
from datetime import date, timedelta
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
CSS = (WEB / "style.css").read_text(encoding="utf-8")

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const input = JSON.parse(process.argv[2]);
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  api: async (path) => path.startsWith("/api/packages") ? input.packages : input.orders,
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + `;globalThis.__s = roleScreens.get(${JSON.stringify(input.id)});`, context);
(async () => {
  const s = context.__s;
  const extra = await s.load?.(input.c);
  console.log(JSON.stringify(await s.render(input.c, extra)));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""


def render(screen: str, case: dict[str, Any], packages: Any = (), orders: Any = ()) -> Any:
    payload = {"id": screen, "c": case, "packages": packages, "orders": orders}
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(payload)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def walk(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


def text(node: Any) -> str:
    return json.dumps(node)


def package(**cap: Any) -> dict[str, Any]:
    row = {"contractor": "Test Ltd", "offered": 10, "committed": 5, "in_use": 1, "headroom": 5}
    return {
        "id": "PKG-1",
        "name": "North",
        "capacity": [row | cap],
        "scope": "Loft",
        "scope_version": 1,
    }


def packages_screen(**cap: Any) -> Any:
    return render("procurement-packages", {"id": "C-1"}, [package(**cap)], [])


def quality_case(state: str, **extra: Any) -> dict[str, Any]:
    record = {"measure": "Loft", "state": state, "items": [], "submitted_by": "Ann"} | extra
    return {"id": "C-1", "measures": ["Loft"], "quality": [record], "quality_handover_blockers": []}


class LotCapacityState(unittest.TestCase):
    def test_headroom_has_text_prefix(self) -> None:
        expected = {
            5: "Offered capacity remaining: 5",
            0: "Fully committed: 0",
            -2: "Over-committed: -2",
            None: "Unknown: headroom not supplied",
        }
        for headroom, prefix in expected.items():
            with self.subTest(headroom=headroom):
                self.assertIn(prefix, text(packages_screen(headroom=headroom)))


class ExpiryState(unittest.TestCase):
    def state(self, offset: int | None) -> str:
        value = None if offset is None else (date.today() + timedelta(days=offset)).isoformat()
        return text(packages_screen(insurance_expiry=value, certification_expiry=value))

    def test_expiry_prefixes(self) -> None:
        self.assertIn("Expired: ", self.state(-3))
        self.assertIn("Expires within 30 days: ", self.state(10))
        self.assertIn("In date until: ", self.state(200))
        self.assertIn("Unknown: expiry date not supplied", self.state(None))

    def test_expiry_does_not_claim_validity(self) -> None:
        self.assertIn("does not confirm that cover or certification is valid", self.state(200))


class QualityStates(unittest.TestCase):
    def test_defect_and_handover_states(self) -> None:
        cases = {
            "Returned": ("Open: awaiting a fix", "Not ready: handover sign-off"),
            "Fixed, awaiting reinspection": (
                "Fixed: awaiting independent reinspection",
                "Not ready",
            ),
            "Accepted": ("Closed: reinspection passed", "Awaiting sign-off: accepted"),
            "Handed over": ("Closed: reinspection passed", "Signed off: handover recorded"),
        }
        for state, expected in cases.items():
            with self.subTest(state=state):
                out = text(render("quality-queue", quality_case(state)))
                for fragment in expected:
                    self.assertIn(fragment, out)


class KeyboardReach(unittest.TestCase):
    def test_tables_are_named_focusable_regions_without_pointer_only_controls(self) -> None:
        tree = packages_screen()
        regions = [n for n in walk(tree) if (n.get("attrs") or {}).get("class") == "table-scroll"]
        self.assertTrue(regions)
        for region in regions:
            attrs = region["attrs"]
            self.assertEqual(attrs["tabindex"], 0)
            self.assertEqual(attrs["role"], "region")
            self.assertTrue(attrs["aria-label"])
        for node in walk(tree) + walk(render("quality-queue", quality_case("Accepted"))):
            attrs = node.get("attrs") or {}
            self.assertNotIn("onclick", attrs)
            self.assertNotIn("aria-invalid", attrs)

    def test_focus_indicator_is_never_removed(self) -> None:
        self.assertIn(":focus-visible{outline:", CSS)
        self.assertNotRegex(CSS, r"\.table-scroll[^{]*\{[^}]*outline:\s*(none|0)")

    def test_single_status_per_state_message(self) -> None:
        out = packages_screen()
        statuses = [n for n in walk(out) if (n.get("attrs") or {}).get("role") == "status"]
        self.assertTrue(all("regulatory-alerts" not in text(n) for n in statuses))


if __name__ == "__main__":
    unittest.main()
