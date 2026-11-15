"""Focused API and web tests for Issue #76: hazard and safeguarding clock and named owner."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from dataset import DATA
from zava_forward.core import projection
from zava_forward.core.sqlstore import SqlStore

from test_case_journey import DOM, WEB, shipped_helpers
from zava_forward.api.server import App, make_handler


class HazardSafeguardingClockAndOwnerApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data: dict[str, Any] = copy.deepcopy(DATA)
        data["as_of"] = "2026-10-16"
        data["staff"].extend(
            [
                dict(
                    code="BS-1",
                    name="Bea Safe",
                    email="bea@example.test",
                    role="Building Safety Liaison",
                ),
                dict(
                    code="RC-1",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-1",
                    name="Kim Contractor",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        # ZF-1: standalone unallocated safeguarding item with missing timestamp (fail-closed)
        data["cases"][0]["hazards"] = []
        data["cases"][0]["safeguarding_items"] = [
            dict(
                id="SG-API-1",
                priority="Urgent",
                note="CONFIDENTIAL-SAFEGUARDING-NOTE",
                source="CONFIDENTIAL-SAFEGUARDING-SOURCE",
            )
        ]
        # ZF-2: emergency hazard + unallocated safeguarding item with awareness timestamp
        data["cases"][1]["hazards"] = [
            dict(
                category="Damp and mould",
                priority="Emergency",
                released=False,
                aware_at="2026-10-15T08:00:00Z",
                owner="Bea Safe",
                source="CONFIDENTIAL-HAZARD-SOURCE",
                job="RJ-76001",
            )
        ]
        data["cases"][1]["safeguarding_items"] = [
            dict(
                id="SG-API-2",
                priority="Significant",
                aware_at="2026-10-15T12:00:00Z",
                destination=dict(
                    code="BS-1",
                    name="Bea Safe",
                    email="bea@example.test",
                    role="Building Safety Liaison",
                ),
                received_at="2026-10-15T13:00:00Z",
                accepted_at=None,
            )
        ]
        seed_path = Path(self.tmp.name) / "seed.json"
        seed_path.write_text(json.dumps(data))
        sql_store_cls: Any = SqlStore
        app_cls: Any = App
        make_handler_fn: Any = make_handler
        self.store: Any = sql_store_cls(str(seed_path), str(seed_path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler_fn(app_cls(self.store, "synthetic-check"))
        )
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self._shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def _shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def _get(self, email_prefix: str, path: str) -> Any:
        if email_prefix not in self.cookies:
            req = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{email_prefix}@example.test", password="synthetic-check")
                ).encode(),
            )
            with urllib.request.urlopen(req) as resp:
                self.cookies[email_prefix] = resp.headers["Set-Cookie"].split(";")[0]
        req = urllib.request.Request(
            self.base + path,
            headers={"Cookie": self.cookies[email_prefix]},
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def test_queue_and_case_card_endpoints_expose_clock_owner_and_redaction_boundaries(
        self,
    ) -> None:
        blocked = self._get("bea", "/api/cases?view=all&queue=blocked")
        items_by_id = {row["id"]: row for row in blocked["items"]}
        self.assertIn("ZF-1", items_by_id)
        self.assertIn("ZF-2", items_by_id)

        zf1_clock = items_by_id["ZF-1"]["work"]["hazard_clocks"][0]
        self.assertEqual(zf1_clock["item_kind"], "safeguarding")
        self.assertEqual(zf1_clock["clock_status"], "fail_closed_missing_timestamp")
        self.assertIsNone(zf1_clock["clock_deadline_utc"])
        self.assertTrue(zf1_clock["unassigned"])
        self.assertTrue(zf1_clock["named_owner"])
        self.assertEqual(zf1_clock["named_owner"], zf1_clock["escalation_owner"])

        zf2_clocks = items_by_id["ZF-2"]["work"]["hazard_clocks"]
        self.assertEqual(len(zf2_clocks), 2)
        self.assertEqual(
            zf2_clocks[0]["clock_label"],
            "Awaab's Law 24h emergency action clock (recorded reference)",
        )
        self.assertEqual(zf2_clocks[0]["clock_status"], "running")
        self.assertEqual(zf2_clocks[0]["named_owner"], "Bea Safe")
        self.assertFalse(zf2_clocks[0]["unassigned"])
        self.assertEqual(zf2_clocks[1]["item_kind"], "safeguarding")
        self.assertTrue(zf2_clocks[1]["unassigned"])
        self.assertEqual(zf2_clocks[1]["escalation_owner"], "Bea Safe")

        # Non-reason staff receives clock + named owner on case card while private notes are held.
        rc_card = self._get("rex", "/api/cases/ZF-1")
        self.assertEqual(rc_card["safeguarding_items"][0]["note"], projection.NOTE_HELD)
        self.assertEqual(rc_card["safeguarding_items"][0]["source"], projection.NOTE_HELD)
        self.assertEqual(
            rc_card["safeguarding_items"][0]["clock_status"],
            "fail_closed_missing_timestamp",
        )
        self.assertTrue(rc_card["safeguarding_items"][0]["named_owner"])

        # Contractor receives no hazard, safeguarding, or staff work context (PR-002).
        con_list = self._get("kim", "/api/cases?view=all")
        for row in con_list["items"]:
            self.assertNotIn("work", row)
            self.assertNotIn("hazard", row)
            self.assertNotIn("safeguarding", row)

    def test_web_app_and_unmodified_role_screens_render_clock_and_named_owner(
        self,
    ) -> None:
        blocked = self._get("bea", "/api/cases?view=all&queue=blocked")
        zf1_detail = self._get("bea", "/api/cases/ZF-1")
        zf2_detail = self._get("bea", "/api/cases/ZF-2")
        me = self._get("bea", "/api/me")

        # 1. Verify unmodified role-screens.js + workSummary renders clock and owner cleanly.
        role_script = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const webDir = process.argv[1];
const payload = JSON.parse(process.argv[2]);
const app = fs.readFileSync(webDir + "/app.js", "utf8");
const host = fs.readFileSync(webDir + "/role-screens.js", "utf8");
let rendered;
const details = { "ZF-1": payload.zf1, "ZF-2": payload.zf2 };
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, navigator: { language: "en-GB" },
  location: { hash: "#/screens?screen=safety-lead" },
  me: payload.me,
  routeController: new AbortController(),
  workspaceStatus: {},
  api: async (url) => {
    if (url.startsWith("/api/cases/ZF-1")) return details["ZF-1"];
    if (url.startsWith("/api/cases/ZF-2")) return details["ZF-2"];
    return payload.blocked;
  },
  h: (tag, attrs, ...kids) => ({
    tag,
    attrs: attrs || {},
    kids: kids.flat(Infinity).filter((k) => k !== false && k !== null && k !== undefined),
  }),
  show: (...nodes) => { rendered = nodes; },
});
const slice = app.slice(app.indexOf("function workSummary("), app.indexOf("function workSteps("));
vm.runInContext(slice + "\n" + host, context);
function flatten(node) {
  if (!node) return "";
  if (typeof node !== "object") return String(node);
  return (node.kids || []).map(flatten).join(" ");
}
vm.runInContext("roleScreensView()", context).then(() => {
  const fullText = rendered.map(flatten).join("\n");
  assert.ok(!fullText.includes("Mismatch"), fullText);
  assert.ok(!fullText.includes("Owner: Unknown"), fullText);
  const sgFailClosed =
    "Safeguarding 24h emergency response clock (fail-closed: timestamp not recorded)";
  const hzEmergency = "Awaab's Law 24h emergency action clock (recorded reference)";
  const beaOwner = "Accountable owner: Bea Safe (Building Safety Liaison, ID BS-1)";
  assert.ok(fullText.includes(sgFailClosed), fullText);
  assert.ok(fullText.includes(hzEmergency), fullText);
  assert.ok(fullText.includes(beaOwner), fullText);
  assert.ok(fullText.includes("[Unassigned item; escalation owner:"), fullText);
}).catch((err) => { console.error(err); process.exitCode = 1; });
"""
        role_res = subprocess.run(
            [
                "node",
                "-e",
                role_script,
                str(WEB),
                json.dumps(dict(blocked=blocked, zf1=zf1_detail, zf2=zf2_detail, me=me)),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(role_res.returncode, 0, role_res.stderr)

        # 2. Verify safetyPanel renders .safety-clock-owner on hazard and safeguarding items.
        panel_script = (
            DOM
            + f"const WEB_APP = {str(WEB / 'app.js')!r};\n"
            + f"const PAYLOAD = {json.dumps(dict(zf1=zf1_detail, zf2=zf2_detail, me=me))};\n"
            + shipped_helpers()
            + r"""
Node.prototype.setCustomValidity = function (message) { this.message = message; };
Node.prototype.reportValidity = function () { return true; };
const source = require("node:fs").readFileSync(WEB_APP, "utf8");
const start = source.indexOf("const SAFETY_ROLES");
const mid = source.indexOf("const HAZ_PRIORITIES");
eval(source.slice(start, source.indexOf("\n", mid)).replaceAll("const ", "var "));
const fnStart = source.indexOf("function hazardState");
const fnEnd = source.indexOf("async function contractorListView");
eval(source.slice(fnStart, fnEnd).replace(/^function (\w+)/gm, "globalThis.$1 = function $1"));
let me = PAYLOAD.me;
globalThis.post = async () => {};
assert.ok(HAZ_CATEGORIES.includes("Safeguarding"));

const panel1 = safetyPanel(PAYLOAD.zf1, "ZF-1", async () => {});
const byClass = (el, cls) => el.querySelectorAll("li").filter((li) => li.className === cls);
const sgCards1 = byClass(panel1, "safeguarding-item");
assert.equal(sgCards1.length, 1);
assert.equal(byClass(panel1, "safety-item").length, 0);
const sgBanner1 = sgCards1[0].querySelector(".safety-clock-owner").textContent;
const expectedSg1 =
  "Safeguarding 24h emergency response clock: fail-closed (timestamp not recorded)";
assert.ok(sgBanner1.includes(expectedSg1), sgBanner1);
assert.ok(sgBanner1.includes("Unassigned item; escalation owner:"), sgBanner1);

const panel2 = safetyPanel(PAYLOAD.zf2, "ZF-2", async () => {});
const hzCards2 = byClass(panel2, "safety-item");
const sgCards2 = byClass(panel2, "safeguarding-item");
assert.equal(hzCards2.length, 1);
assert.equal(sgCards2.length, 1);
const hzBanner2 = hzCards2[0].querySelector(".safety-clock-owner").textContent;
const expectedHz2 = "Awaab's Law 24h emergency action clock (recorded reference): running";
const expectedBea = "Accountable owner: Bea Safe (Building Safety Liaison, ID BS-1)";
assert.ok(hzBanner2.includes(expectedHz2), hzBanner2);
assert.ok(hzBanner2.includes(expectedBea), hzBanner2);
assert.ok(!hzCards2[0].querySelector(".safety-facts").textContent.includes("Unknown"));
const sgBanner2 = sgCards2[0].querySelector(".safety-clock-owner").textContent;
assert.ok(sgBanner2.includes("Safeguarding 48h referral response clock: running"), sgBanner2);
assert.ok(
  sgBanner2.includes(expectedBea + " — Unassigned item; escalation owner: Bea Safe"),
  sgBanner2
);
"""
        )
        panel_res = subprocess.run(
            ["node", "-e", panel_script],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(panel_res.returncode, 0, panel_res.stderr)


if __name__ == "__main__":
    unittest.main()
