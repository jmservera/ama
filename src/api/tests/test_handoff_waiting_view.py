"""Issue 83: read-only on-screen waiting times for unaccepted handoffs (#/handoff-waiting).

The Node cases run the real handoffWaitingView source with stubbed rendering helpers. The opt-in
browser cases serve the real app on loopback with synthetic data; responses the real backend
cannot produce (an old handoff with no due time, an escalated one, an empty queue beside a
non-empty personal list, malformed bodies) are explicitly constructed by page routing and are
labelled as such. Neither is human, assistive-technology or live acceptance, and neither
establishes an approved waiting time (OD-09).
"""

import copy
import json
import os
import subprocess
import unittest
from pathlib import Path
from typing import Any

from dataset import change_metadata

from test_handoff_read_guidance import SAM, Served
from test_unaccepted_handoff_download_ui import heavy_lock_or_none

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
START = "const WAITING_READ_ERROR"
END = "async function listView"
POLICY = "No approved waiting-time limit is set for the whole queue"

NODE = r"""
const fs = require("node:fs"), vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const start = src.indexOf(process.argv[2]), end = src.indexOf(process.argv[3]);
if (start < 0 || end < start) throw new Error("handoffWaitingView source markers not found");
const slice = src.slice(start, end);
const el = (tag, attrs, kids) => ({tag, attrs, kids,
  text() { return this.kids.map(k => typeof k === "string" ? k : k.text()).join(" "); },
  all() { return [this].concat(this.kids.flatMap(k => typeof k === "string" ? [] : k.all())); }});
const h = (tag, attrs, ...kids) =>
  el(tag, attrs || {}, kids.flat().filter(k => k != null && k !== false));
const row = (over) => Object.assign({case_id: "ZF-1", status: "Sent", age_hours: 5.25,
  due_at: null, chase_owner: "Sam Example", chase_owner_code: "RLO-01",
  proposed_receiver: "Pam Lead", escalated: false, needs_escalation: false, reasons: [],
  approved_limit_hours: null, limit_note: "Approved escalation time not set (OD-09)",
  as_of: "2026-11-11T09:00:00+00:00"}, over);
const err = (message, extra) => Object.assign(new Error(message), extra);
const scenarios = {
  mixed: [row({age_hours: 400}),
    row({case_id: "ZF-2", age_hours: 1, due_at: "2026-11-10T09:00:00+00:00", needs_escalation: true,
      reasons: ["Handoff due time has passed"]}),
    row({case_id: "ZF-4", age_hours: -0.01}),
    row({case_id: "ZF/3", status: "Escalated", escalated: true, chase_owner: null,
      proposed_receiver: null})],
  empty: [],
  forbidden: err("authorised staff can view handoffs RAWSERVERTEXT", {status: 403}),
  server: err("RAWSERVERTEXT /srv/x.py", {status: 500}),
  transport: new TypeError("Failed to fetch RAWSERVERTEXT"),
  notArray: {},
  badRow: [row({age_hours: "5"})],
  nullRow: [null],
  badFlag: [row({escalated: "no"})],
  limit: [row({approved_limit_hours: 24})],
  abort: err("aborted", {name: "AbortError"}),
  session: err("Your session has ended. Sign in again.", {status: 401}),
};
const out = {};
(async () => {
  for (const [name, result] of Object.entries(scenarios)) {
    const calls = [], shown = [];
    const api = (...a) => { calls.push(a); return result instanceof Error
      ? Promise.reject(result) : Promise.resolve(result); };
    const show = (...nodes) => { shown.push(nodes.flat()); };
    const ctx = vm.createContext({h, api, show, queueHref: () => "#/", encodeURIComponent});
    vm.runInContext(slice + "\nthis.view = handoffWaitingView;", ctx);
    await ctx.view();
    const last = shown.length ? shown[shown.length - 1] : [];
    const nodes = last.flatMap(n => n.all());
    out[name] = {calls, shows: shown.length, text: last.map(n => n.text()).join(" "),
      roles: nodes.filter(n => n.attrs.role).map(n => n.attrs.role),
      tables: nodes.filter(n => n.tag === "table").length,
      anchors: nodes.filter(n => n.tag === "a").map(n => n.attrs.href),
      buttons: nodes.filter(n => n.tag === "button").map(n => [n.attrs.type, n.text()]),
      rowsText: nodes.filter(n => n.tag === "tr").map(n => n.text())};
  }
  console.log(JSON.stringify(out));
})();
"""


def node_outputs() -> dict[str, Any]:
    done = subprocess.run(
        ["node", "-e", NODE, str(WEB), START, END],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if done.returncode:
        raise AssertionError(done.stderr)
    outputs: dict[str, Any] = json.loads(done.stdout)
    return outputs


class WaitingViewText(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = node_outputs()

    def test_one_read_only_unscoped_get_and_no_new_route_or_limit(self) -> None:
        for name, case in self.out.items():
            self.assertEqual(case["calls"], [["/api/handoffs/unaccepted"]], name)

    def test_rows_show_elapsed_as_of_owner_and_only_server_supplied_reasons(self) -> None:
        case = self.out["mixed"]
        old, due, fresh, escalated = case["rowsText"][1:]
        self.assertIn("400 hours", old)
        self.assertIn("No escalation reason recorded.", old)
        self.assertNotIn("late", old.lower())
        self.assertIn("1 hour ", due + " ")
        self.assertIn("Needs escalation. Reason: Handoff due time has passed.", due)
        self.assertIn("0 hours", fresh)
        self.assertNotIn("-0", fresh)
        self.assertIn("Already escalated.", escalated)
        self.assertIn("Unassigned", escalated)
        self.assertIn("Recorded as of 11 Nov 2026, 09:00 UTC", case["text"])
        self.assertIn("Sam Example", old)
        self.assertIn("#/case/ZF-1", case["anchors"])
        self.assertIn("#/case/ZF%2F3", case["anchors"])
        self.assertEqual(case["buttons"], [["button", "Check again"]])

    def test_scope_is_explicit_and_distinct_from_the_personal_list(self) -> None:
        text = self.out["mixed"]["text"]
        for phrase in (
            "every handoff that has not been accepted yet and that your role can see",
            "not the list called Handoffs waiting for you",
            POLICY,
            "A long wait alone does not mean a handoff is late",
            "nothing is escalated automatically",
            "read-only",
        ):
            self.assertIn(phrase, text)
        self.assertTrue(text.isascii())

    def test_empty_queue_is_stated_without_a_table_or_as_of(self) -> None:
        case = self.out["empty"]
        self.assertIn("No unaccepted handoffs are visible to your role.", case["text"])
        self.assertEqual((case["tables"], case["roles"].count("alert")), (0, 0))
        self.assertNotIn("Recorded as of", case["text"])

    def test_failures_and_malformed_payloads_are_a_visible_alert_without_table_or_raw_text(
        self,
    ) -> None:
        for name in (
            "forbidden",
            "server",
            "transport",
            "notArray",
            "badRow",
            "nullRow",
            "badFlag",
            "limit",
        ):
            case = self.out[name]
            self.assertEqual(case["roles"].count("alert"), 1, name)
            self.assertEqual(case["tables"], 0, name)
            self.assertNotIn("RAWSERVERTEXT", case["text"], name)
            self.assertNotIn("No unaccepted handoffs", case["text"], name)
            self.assertEqual(case["buttons"], [["button", "Check again"]], name)
        self.assertIn("cannot view handoff waiting times", self.out["forbidden"]["text"])
        self.assertIn("could not load", self.out["server"]["text"])

    def test_abort_and_ended_session_render_nothing_beyond_loading(self) -> None:
        for name in ("abort", "session"):
            self.assertEqual(self.out[name]["shows"], 1, name)
            self.assertNotIn("alert", self.out[name]["roles"], name)


@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")
class WaitingViewBrowser(unittest.TestCase):
    pw: Any
    browser: Any
    lock: Any

    @classmethod
    def setUpClass(cls) -> None:
        from playwright.sync_api import sync_playwright

        cls.lock = heavy_lock_or_none()
        if cls.lock is None:
            raise unittest.SkipTest("heavy browser lock is busy; no browser evidence was produced")
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.pw.stop()
        cls.lock.close()

    def open(self, offers: bool = True) -> tuple[Any, Any, list[Any]]:
        served = Served(False)
        self.addCleanup(served.close)
        if offers:
            for cid, due in (("ZF-1", "2020-01-01T00:00:00Z"), ("ZF-2", None)):
                meta = change_metadata(served.store, cid)
                if due:
                    meta = {**meta, "due_at": due}
                served.store.offer_handoff(
                    SAM, cid, "pam@example.test", "synthetic note", metadata=meta
                )
        page = self.browser.new_page()
        self.addCleanup(page.close)
        requests: list[Any] = []
        page.on("request", lambda request: requests.append(request))
        page.goto(served.base + "/")
        status = page.evaluate(
            """async () => (await fetch('/api/login', {method: 'POST',
              headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'},
              body: JSON.stringify({email: 'sam@example.test', password: 'zf-test'})})).status"""
        )
        self.assertEqual(status, 200)
        return served, page, requests

    def construct(self, page: Any, path: str, status: int, body: str) -> None:
        page.route(
            f"**{path}",
            lambda route: route.fulfill(status=status, content_type="application/json", body=body),
        )

    def screen(self, page: Any, base: str) -> Any:
        page.goto(base + "/app#/")
        page.get_by_role("heading", name="My cases today").wait_for()
        page.get_by_role("link", name="Handoff waiting times", exact=True).focus()
        page.keyboard.press("Enter")
        heading = page.get_by_role("heading", name="Handoff waiting times", exact=True)
        heading.wait_for()
        return heading

    def test_real_backend_rows_by_keyboard_without_mutation(self) -> None:
        from playwright.sync_api import expect

        served, page, requests = self.open()
        before = copy.deepcopy(served.store.cases)
        self.screen(page, served.base)
        expect(page).to_have_url(served.base + "/app#/handoff-waiting")
        table = page.get_by_role("table")
        expect(table.get_by_role("row")).to_have_count(3)
        due, fresh = table.get_by_role("row").nth(1), table.get_by_role("row").nth(2)
        ids = [r.get_by_role("rowheader").inner_text() for r in (due, fresh)]
        self.assertEqual(sorted(ids), ["ZF-1", "ZF-2"])
        by_id = {r.get_by_role("rowheader").inner_text(): r for r in (due, fresh)}
        expect(by_id["ZF-1"]).to_contain_text(
            "Needs escalation. Reason: Handoff due time has passed."
        )
        expect(by_id["ZF-2"]).to_contain_text("No escalation reason recorded.")
        expect(by_id["ZF-2"]).to_contain_text("Sam Example")
        expect(page.locator("main, #app")).to_contain_text("Recorded as of")
        expect(page.locator("#app")).to_contain_text(POLICY)
        link = by_id["ZF-2"].get_by_role("link", name="ZF-2")
        link.focus()
        page.keyboard.press("Enter")
        expect(page).to_have_url(served.base + "/app#/case/ZF-2")
        self.assertEqual(served.store.cases, before)
        stray = [r for r in requests if r.method != "GET" and "login" not in r.url]
        self.assertEqual(stray, [])
        waiting = [r.url for r in requests if "/api/handoffs/unaccepted" in r.url]
        self.assertTrue(waiting and all(u.endswith("/api/handoffs/unaccepted") for u in waiting))

    def test_reachable_when_personal_list_is_empty_or_its_load_fails_constructed(self) -> None:
        from playwright.sync_api import expect

        served, page, _ = self.open()
        self.construct(page, "/api/handoffs", 200, "[]")
        self.screen(page, served.base)
        expect(page.get_by_role("table").get_by_role("row")).to_have_count(3)
        expect(page.locator('section[aria-label="Handoffs waiting for you"]')).to_have_count(0)
        self.assertNotIn("Handoffs waiting for you", page.locator("h2").all_inner_texts())

        served, page, _ = self.open()
        self.construct(page, "/api/handoffs", 500, '{"error": "RAWSERVERTEXT"}')
        self.screen(page, served.base)
        expect(page.get_by_role("table").get_by_role("row")).to_have_count(3)

    def test_constructed_old_escalated_and_empty_queue(self) -> None:
        from playwright.sync_api import expect

        served, page, _ = self.open(False)
        rows = [
            dict(
                case_id="ZF-1",
                status="Escalated",
                age_hours=700.5,
                due_at=None,
                chase_owner="Sam Example",
                chase_owner_code="RLO-01",
                proposed_receiver="Pam Lead",
                escalated=True,
                needs_escalation=False,
                reasons=[],
                approved_limit_hours=None,
                limit_note="Approved escalation time not set (OD-09)",
                as_of="2026-11-11T09:00:00+00:00",
            ),
        ]
        self.construct(page, "/api/handoffs/unaccepted", 200, json.dumps(rows))
        self.screen(page, served.base)
        row = page.get_by_role("table").get_by_role("row").nth(1)
        expect(row).to_contain_text("700.5 hours")
        expect(row).to_contain_text("Already escalated.")
        expect(row).to_contain_text("Unknown")

        served, page, _ = self.open(False)
        self.screen(page, served.base)
        expect(page.get_by_role("status").filter(has_text="No unaccepted handoffs")).to_be_visible()
        expect(page.get_by_role("table")).to_have_count(0)

    def test_rejected_and_malformed_responses_are_visible_failures_and_recheck_works(self) -> None:
        from playwright.sync_api import expect

        for status, body in (
            (500, '{"error": "RAWSERVERTEXT /srv/x.py"}'),
            (403, '{"error": "RAWSERVERTEXT"}'),
            (200, "<html>RAWSERVERTEXT</html>"),
            (200, '[{"case_id": "ZF-1", "age_hours": "soon"}]'),
        ):
            served, page, requests = self.open(False)
            before = copy.deepcopy(served.store.cases)
            self.construct(page, "/api/handoffs/unaccepted", status, body)
            self.screen(page, served.base)
            alert = page.get_by_role("alert")
            expect(alert).to_be_visible()
            expect(page.locator("#app")).not_to_contain_text("RAWSERVERTEXT")
            expect(page.get_by_role("table")).to_have_count(0)
            expect(page.locator("#app")).not_to_contain_text("No unaccepted handoffs")
            page.unroute_all()
            page.get_by_role("button", name="Check again").focus()
            page.keyboard.press("Enter")
            expect(
                page.get_by_role("status").filter(has_text="No unaccepted handoffs")
            ).to_be_visible()
            self.assertEqual(served.store.cases, before)
            stray = [r for r in requests if r.method != "GET" and "login" not in r.url]
            self.assertEqual(stray, [])


if __name__ == "__main__":
    unittest.main()
