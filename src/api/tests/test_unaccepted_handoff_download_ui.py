"""Issue 1419: the pending-handoff panel offers one distinct download of unaccepted handoffs.

The Node cases run the real pendingHandoffs source with stubbed rendering helpers. The opt-in
browser cases serve the real app on loopback with synthetic data. Neither is human,
assistive-technology or live acceptance.
"""

import copy
import csv
import fcntl
import io
import json
import os
import subprocess
import unittest
from pathlib import Path
from typing import Any

from test_handoff_read_guidance import END, START, Served

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
LABEL = "Download handoff waiting times for Excel"
HEAVY_LOCK = "/tmp/ama-rpi-heavy.lock"

NODE = r"""
const fs = require("node:fs"), vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const fn = src.indexOf(process.argv[2]), end = src.indexOf(process.argv[3]);
const constant = src.indexOf("const HANDOFF_READ_ERROR");
const start = constant >= 0 && constant < fn ? constant : fn;
if (fn < 0 || end < fn) throw new Error("pendingHandoffs source markers not found");
const slice = src.slice(start, end);
const element = (tag, attrs, kids) => ({tag, attrs, kids, hidden: false,
  replaceChildren(...next) { this.kids = next; },
  text() { return this.kids.map(k => typeof k === "string" ? k : k.text()).join(" "); },
  anchors() { return this.kids.flatMap(k => typeof k === "string" ? [] : k.anchors())
    .concat(tag === "a" ? [{href: attrs.href, download: attrs.download,
      text: this.text()}] : []); }});
const h = (tag, attrs, ...kids) => element(tag, attrs || {}, kids.flat().filter(k => k != null));
const tick = () => new Promise(resolve => setTimeout(resolve, 0));
const row = {case_id: "ZF-1", resident: "Pat Test", address: "1 Test Road", status: "Sent",
  accountable_owner: "Sam Example", to_code: "PM-01"};
const out = {};
(async () => {
  const scenarios = {
    transport: new TypeError("Failed to fetch"),
    http: Object.assign(new Error("Handoff service said no"), {status: 500}),
    rows: [row],
    empty: [],
  };
  for (const [name, result] of Object.entries(scenarios)) {
    const calls = [];
    const api = (...args) => { calls.push(args); return result instanceof Error
      ? Promise.reject(result) : Promise.resolve(result); };
    const ctx = vm.createContext({h, api, me: {user: {code: "RLO-01"}}, encodeURIComponent});
    vm.runInContext(slice + "\nthis.pendingHandoffs = pendingHandoffs;", ctx);
    const box = ctx.pendingHandoffs();
    const loading = box.anchors();
    await tick();
    out[name] = {loading, hidden: box.hidden, anchors: box.anchors(), text: box.text(), calls};
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


class UnacceptedDownloadText(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = node_outputs()

    def test_success_has_both_links_and_the_existing_one_is_unchanged(self) -> None:
        anchors = self.out["rows"]["anchors"]
        self.assertEqual(
            [(a["href"], a.get("download"), a["text"]) for a in anchors[:3]],
            [
                ("/api/handoffs.csv", "handoffs.csv", "Download for Excel"),
                ("/api/handoffs/unaccepted.csv", "unaccepted-handoffs.csv", LABEL),
                ("#/case/ZF-1", None, "Pat Test, 1 Test Road"),
            ],
        )
        self.assertEqual(len(anchors), 3)
        self.assertNotIn("?", anchors[1]["href"])

    def test_helper_text_is_truthful_plain_and_ascii(self) -> None:
        text = self.out["rows"]["text"]
        for phrase in (
            "not the list on this card",
            "every handoff you can see that has not been accepted yet",
            "no resident contact details",
            "read-only copy; changes in it are not imported back",
            "No waiting-time limit is set for the whole queue",
            "only when its own due time has passed",
            "An empty file has no column names",
        ):
            self.assertIn(phrase, text)
        self.assertTrue(text.isascii())
        self.assertNotIn("approved limit", text)

    def test_no_new_link_while_loading_on_error_or_when_empty(self) -> None:
        for name in ("rows", "transport", "http", "empty"):
            self.assertEqual(self.out[name]["loading"], [], name)
        for name in ("transport", "http", "empty"):
            self.assertEqual(self.out[name]["anchors"], [], name)
        self.assertTrue(self.out["empty"]["hidden"])

    def test_still_one_read_only_pending_request(self) -> None:
        for name, case in self.out.items():
            self.assertEqual(case["calls"], [["/api/handoffs"]], name)


def heavy_lock_or_none() -> Any:
    stream = open(HEAVY_LOCK, "a+")  # noqa: SIM115 - held for the whole browser class
    try:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        stream.close()
        return None
    return stream


@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")
class UnacceptedDownloadBrowser(unittest.TestCase):
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

    def open(self, offer: bool) -> tuple[Any, Any, list[Any]]:
        served = Served(offer)
        self.addCleanup(served.close)
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
        page.goto(served.base + "/app#/")
        page.get_by_role("heading", name="My cases today").wait_for()
        return served, page, requests

    def test_link_downloads_the_unaccepted_rows_by_mouse_and_keyboard_without_mutation(
        self,
    ) -> None:
        from playwright.sync_api import expect

        served, page, requests = self.open(True)
        before = copy.deepcopy(served.store.cases)
        card = page.locator('section[aria-label="Handoffs waiting for you"]')
        link = card.get_by_role("link", name=LABEL, exact=True)
        expect(link).to_have_count(1)
        expect(link).to_have_attribute("href", "/api/handoffs/unaccepted.csv")
        expect(link).to_have_attribute("download", "unaccepted-handoffs.csv")
        expect(card.get_by_role("link", name="Download for Excel", exact=True)).to_have_attribute(
            "href", "/api/handoffs.csv"
        )
        expect(card).to_contain_text("This file is not the list on this card.")
        for activate in (
            lambda: link.click(),
            lambda: (link.focus(), page.keyboard.press("Enter")),
        ):
            with page.expect_download() as info:
                activate()
            download = info.value
            self.assertEqual(download.suggested_filename, "unaccepted-handoffs.csv")
            rows = list(csv.reader(io.StringIO(Path(download.path()).read_text(), newline="")))
            self.assertEqual(rows[0][:3], ["case_id", "status", "age_hours"])
            self.assertEqual(len(rows[0]), 13)
            self.assertEqual([r[0] for r in rows[1:]], ["ZF-1"])
            self.assertEqual(rows[1][1], "Sent")
        self.assertEqual(served.store.cases, before)
        self.assertEqual([r for r in requests if r.method == "POST" and "login" not in r.url], [])

    def test_no_download_is_offered_when_nothing_is_pending(self) -> None:
        from playwright.sync_api import expect

        _, page, _ = self.open(False)
        card = page.locator('section[aria-label="Handoffs waiting for you"]')
        expect(card).to_be_hidden()
        self.assertEqual(page.get_by_role("link", name=LABEL).count(), 0)


if __name__ == "__main__":
    unittest.main()
