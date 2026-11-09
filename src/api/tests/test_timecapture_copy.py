"""Staff-time refusal and error guidance (issue 153): reason, owner and next action.

The Node cases run the real timecapture.js helpers. The opt-in browser cases serve the real app on
loopback with synthetic data and explicitly constructed responses. Neither is human, DPO or
assistive-technology acceptance.
"""

import json
import os
import re
import subprocess
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from zava_forward.core.store import Store

import test_mvp
from zava_forward.api.server import App, make_handler
from zava_forward.api.timecapture import NOTICE_VERSION, TimeCapture

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
READY = dict(
    ZF_TIME_CAPTURE="on",
    DPIA_APPROVED="D1",
    ZF_TIME_CONSULTATION="C1",
    ZF_TIME_NOTICE_APPROVED="N1",
    ZF_TIME_NOTICE_VERSION=NOTICE_VERSION,
)
SAM = test_mvp.DATA["staff"][0]
PAM = test_mvp.DATA["staff"][1]
SUPPORT = dict(code="SUP", email="support-officer@example.test", role="Programme Support Officer")
UNSAFE = 'Traceback: sqlite3.OperationalError at /srv/x.py <img src=x onerror="alert(1)">'
BANNED = re.compile(r"\b(gate|hold|provenance|trace)\b", re.I)

NODE = r"""
const fs = require("node:fs"), vm = require("node:vm");
const ctx = vm.createContext({});
vm.runInContext(fs.readFileSync(process.argv[1] + "/timecapture.js", "utf8"), ctx);
const on = {flag_on: true, dpia_recorded: true, consultation_recorded: true, notice_approved: true,
  requested: true, activated: true, enabled: true, requested_role: "Programme Support Officer"};
const blocked = (change, manager) =>
  ctx.timeBlockedText({...on, enabled: false, ...change}, manager);
const act = (status, message, kind, outcome) =>
  ctx.timeActionFailureText({status, message, outcome}, kind || "record");
const out = {
  off: blocked({flag_on: false}), dpia: blocked({dpia_recorded: false}),
  consultation: blocked({consultation_recorded: false}), notice: blocked({notice_approved: false}),
  requestManager: blocked({requested: false, activated: false}, true),
  requestStaff: blocked({requested: false, activated: false}, false),
  enableManager: blocked({activated: false}, true), enableStaff: blocked({activated: false}, false),
  unexplained: blocked({}),
  minutesWhole: act(400, "Minutes must be a whole number."),
  minutesRange: act(400, "Minutes must be between 1 and 600."),
  activity: act(400, "Choose an activity from the list."),
  validationOther: act(400, UNSAFE),
  unknownCase: act(404, "Case not found."),
  notice403: act(403, "Read and acknowledge the staff notice before recording time."),
  manager403: act(403, "Only a manager can take the enabling action.", "enabling"),
  noRequest403: act(403, "Enabling needs a request first, made by a manager.", "enabling"),
  sameRole403: act(403, "The enabling request was made by Programme Support Officer.", "enabling"),
  off403: act(403, "Time capture is switched off."),
  audit403: act(403, UNSAFE),
  pending: act(409, "This action is still pending. Wait for its result."),
  noStatus: act(undefined, "Failed to fetch"),
  server500: act(500, UNSAFE),
  committed: act(200, UNSAFE, "record", "committed"),
  otherKind: act(undefined, "Failed to fetch", "enabling"),
  other4xx: act(418, UNSAFE),
  loadNetwork: ctx.timeLoadFailureText({message: "Failed to fetch"}),
  load500: ctx.timeLoadFailureText({status: 500, message: UNSAFE}),
  loadNotice: ctx.timeLoadFailureText(
    {status: 403, message: "Read and acknowledge the staff notice."}),
  load403: ctx.timeLoadFailureText({status: 403, message: UNSAFE}),
};
console.log(JSON.stringify(out));
""".replace("UNSAFE", json.dumps(UNSAFE))


def node_outputs() -> dict[str, str]:
    done = subprocess.run(
        ["node", "-e", NODE, str(WEB)], capture_output=True, text=True, timeout=60, check=False
    )
    if done.returncode:
        raise AssertionError(done.stderr)
    outputs: dict[str, str] = json.loads(done.stdout)
    return outputs


class StaffTimeGuidanceText(unittest.TestCase):
    out: dict[str, str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = node_outputs()

    def has(self, name: str, *parts: str) -> None:
        for part in parts:
            self.assertIn(part, self.out[name], name)

    def test_every_message_states_reason_owner_and_next_action_in_plain_words(self) -> None:
        for name, text in self.out.items():
            with self.subTest(name=name):
                self.assertRegex(text, r"\. Owner: .+\. Next action: .+")
                self.assertIsNone(BANNED.search(text), text)
                self.assertTrue(text.isascii(), text)
                self.assertNotIn("DPIA_APPROVED", text)
                self.assertNotIn("Traceback", text)
                self.assertNotIn("<img", text)
                self.assertNotIn("/srv", text)
                self.assertNotIn("Failed to fetch", text)

    def test_blocked_states_name_the_existing_route_and_never_a_person(self) -> None:
        self.has("off", "switched off", "Owner: application support")
        self.has("dpia", "DPIA", "Owner: application support", "service settings")
        self.has("consultation", "staff consultation", "Owner: application support")
        self.has("notice", "current staff notice wording", "approval reference")
        self.has(
            "requestManager", "Owner: a manager (Retrofit Programme Manager", "Request enabling"
        )
        self.has("requestStaff", "ask a manager to request enabling")
        self.has("enableManager", "different role", "Enable time capture (audited)")
        self.has("enableStaff", "Programme Support Officer", "ask that manager to enable it")
        self.has("unexplained", "reason is not shown", "Owner: application support")
        for text in self.out.values():
            self.assertNotRegex(text, r"\b(Pam|Sam|Dr|Mr|Ms)\b")
            self.assertNotIn("approved by", text)

    def test_validation_refusals_name_the_input_and_say_nothing_was_saved(self) -> None:
        self.has("minutesWhole", "whole number", "Nothing was saved", "Owner: you")
        self.has("minutesRange", "1 to 600", "Nothing was saved")
        self.has("activity", "activity from the list", "Nothing was saved")
        self.has("validationOther", "Some details were not accepted", "Nothing was saved")
        self.has("unknownCase", "case reference was not found", "nothing was saved")

    def test_known_refusals_before_a_write_say_nothing_changed(self) -> None:
        self.has("notice403", "Nothing was saved", "read the staff notice")
        self.has("manager403", "Nothing was changed", "this step is for a manager")
        self.has("noRequest403", "needs a request first", "ask a manager to request enabling")
        self.has("sameRole403", "different role must enable", "ask that manager to enable it")
        self.has("off403", "Nothing was saved", "not available yet")

    def test_unknown_outcomes_check_records_before_retrying_and_claim_nothing(self) -> None:
        for name in ("audit403", "noStatus", "server500", "committed"):
            with self.subTest(name=name):
                self.has(name, "We cannot tell whether this entry was saved", "check My entries")
                self.has(name, "before you save again", "latest 200 entries")
        self.has("pending", "still in progress", "wait for it to finish", "check My entries")
        self.has("otherKind", "We cannot tell whether this change was saved", "read the checklist")
        self.has("other4xx", "reason is not shown here")
        for name in ("noStatus", "server500", "committed", "audit403", "pending", "otherKind"):
            lowered = self.out[name].lower()
            for claim in (
                "was saved successfully",
                "not saved",
                "nothing was",
                "retry automatically",
            ):
                self.assertNotIn(claim, lowered, name)
            self.assertNotIn("safe to", lowered)

    def test_load_failures_stay_distinct_from_blocked_and_unsaved_states(self) -> None:
        for name in ("loadNetwork", "load500"):
            self.has(name, "Staff time capture could not load", "Owner: application support")
        self.has("loadNotice", "read the staff notice", "refresh this page")
        self.has("load403", "not available to you right now", "contact application support")
        for name in ("loadNetwork", "load500", "loadNotice", "load403"):
            self.assertNotIn("Nothing was", self.out[name])
            self.assertNotIn("switched off", self.out[name])

    def test_source_keeps_text_rendering_and_default_disabled_semantics(self) -> None:
        source = (WEB / "timecapture.js").read_text()
        self.assertNotIn("innerHTML", source)
        self.assertNotIn("\u2014", source)
        self.assertIn('role: "alert"', source)
        self.assertIn("st.enabled", source)


class Served:
    """Isolated loopback app with synthetic staff and a time-capture store."""

    def __init__(
        self, env: dict[str, str], ready: bool = False, acknowledged: bool = False
    ) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(test_mvp.DATA))
        self.store = Store(str(path))
        self.time = TimeCapture(self.store, env, os.path.join(self.tmp.name, "time.sqlite"))
        if ready:
            self.time.request_enable(SUPPORT)
            self.time.activate(PAM)
        if acknowledged:
            self.time.acknowledge(SAM)
        app = App(self.store, "zf-test", self.time)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()


@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")
class StaffTimeGuidanceBrowser(unittest.TestCase):
    pw: Any
    browser: Any

    @classmethod
    def setUpClass(cls) -> None:
        from playwright.sync_api import sync_playwright

        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.pw.stop()

    def open(self, served: Served, user: dict[str, Any], fragment: str = "#/time") -> Any:
        page = self.browser.new_page()
        self.addCleanup(page.close)
        page.route(
            "**/*",
            lambda route: (
                route.continue_() if route.request.url.startswith(served.base) else route.abort()
            ),
        )
        page.goto(served.base + "/")
        status = page.evaluate(
            """async (email) => (await fetch('/api/login', {method: 'POST',
              headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'},
              body: JSON.stringify({email, password: 'zf-test'})})).status""",
            user["email"],
        )
        self.assertEqual(status, 200)
        page.goto(served.base + "/app" + fragment)
        return page

    def served(self, *args: Any, **kwargs: Any) -> Served:
        served = Served(*args, **kwargs)
        self.addCleanup(served.close)
        return served

    def entries(self, served: Served) -> int:
        return len(served.time.mine(SAM))

    def test_disabled_and_missing_prerequisite_explain_owner_and_next_action(self) -> None:
        from playwright.sync_api import expect

        for env, expected, missing in (
            ({}, "Time capture is switched off", "Missing: feature switched on"),
            (
                dict(READY, DPIA_APPROVED=""),
                "DPIA) reference is recorded",
                "Missing: DPIA reference recorded",
            ),
        ):
            with self.subTest(expected=expected):
                page = self.open(self.served(env), PAM)
                banner = page.get_by_role("status").filter(has_text=expected)
                expect(banner).to_contain_text("Owner: application support. Next action:")
                expect(page.get_by_text(missing)).to_be_visible()
                self.assertEqual(page.get_by_role("button", name="Save").count(), 0)
                self.assertNotIn("DPIA_APPROVED", page.locator("main").inner_text())

    def test_invalid_minutes_unknown_case_and_unrecognised_refusal(self) -> None:
        from playwright.sync_api import expect

        served = self.served(READY, ready=True, acknowledged=True)
        page = self.open(served, SAM)
        page.get_by_label("Case reference").fill("ZF-1")
        page.get_by_label("Minutes").fill("0")
        save = page.get_by_role("button", name="Save")
        save.click()
        expect(page.get_by_text("Minutes must be from 1 to 600.")).to_contain_text(
            "Nothing was saved"
        )
        page.get_by_label("Minutes").fill("10")
        page.get_by_label("Case reference").fill("NOPE")
        save.click()
        expect(page.get_by_text("case reference was not found")).to_contain_text("Owner: you")
        self.assertEqual(self.entries(served), 0)

    def test_read_failure_is_a_load_failure_not_a_blocked_state(self) -> None:
        from playwright.sync_api import expect

        served = self.served(READY, ready=True)
        page = self.open(served, SAM, "#/")
        page.route("**/api/time/status", lambda route: route.abort())
        page.goto(served.base + "/app#/time")
        alert = page.get_by_role("alert").filter(has_text="could not load")
        expect(alert).to_contain_text("Owner: application support. Next action: refresh")
        expect(page.get_by_text("switched off")).to_have_count(0)
        page.unroute("**/api/time/status")
        page.route(
            "**/api/time/status",
            lambda route: route.fulfill(
                status=500, content_type="application/json", body=json.dumps({"error": UNSAFE})
            ),
        )
        page.reload()
        expect(page.get_by_role("alert").filter(has_text="could not load")).to_be_visible()
        self.assertNotIn("Traceback", page.locator("main").inner_text())
        self.assertEqual(page.locator("img[src='x']").count(), 0)

    def test_ambiguous_save_claims_nothing_whether_or_not_it_committed(self) -> None:
        from playwright.sync_api import expect

        served = self.served(READY, ready=True, acknowledged=True)
        page = self.open(served, SAM)
        page.get_by_label("Case reference").fill("ZF-1")
        page.get_by_label("Minutes").fill("15")

        def lost_before(route: Any) -> None:
            route.abort() if route.request.method == "POST" else route.continue_()

        def lost_after(route: Any) -> None:
            if route.request.method == "POST":
                route.fetch()
                route.abort()
            else:
                route.continue_()

        for handler, rows in ((lost_before, 0), (lost_after, 1)):
            with self.subTest(handler=handler.__name__):
                page.route("**/api/time", handler)
                page.get_by_role("button", name="Save").click()
                note = page.get_by_text("We cannot tell whether this entry was saved")
                expect(note).to_contain_text("check My entries")
                expect(note).to_contain_text("before you save again")
                page.unroute("**/api/time", handler)
                self.assertEqual(self.entries(served), rows)
                self.assertEqual(page.get_by_label("Minutes").input_value(), "15")
        page.reload()
        expect(page.get_by_text("ZF-1 15 min")).to_have_count(1)

    def test_server_error_detail_is_not_rendered_and_refusals_are_specific(self) -> None:
        from playwright.sync_api import expect

        served = self.served(READY, ready=True, acknowledged=True)
        page = self.open(served, SAM)
        page.route(
            "**/api/time",
            lambda route: (
                route.fulfill(
                    status=500, content_type="application/json", body=json.dumps({"error": UNSAFE})
                )
                if route.request.method == "POST"
                else route.continue_()
            ),
        )
        page.get_by_label("Case reference").fill("ZF-1")
        page.get_by_label("Minutes").fill("5")
        page.get_by_role("button", name="Save").click()
        expect(page.get_by_text("We cannot tell whether this entry was saved")).to_be_visible()
        self.assertNotIn("Traceback", page.locator("main").inner_text())
        self.assertEqual(page.locator("img[src='x']").count(), 0)
        page.unroute("**/api/time")
        page.route(
            "**/api/time",
            lambda route: (
                route.fulfill(
                    status=403,
                    content_type="application/json",
                    body=json.dumps(
                        {"error": "Read and acknowledge the staff notice before recording time."}
                    ),
                )
                if route.request.method == "POST"
                else route.continue_()
            ),
        )
        page.get_by_role("button", name="Save").click()
        expect(page.get_by_text("you read the staff notice")).to_contain_text("Owner: you")


if __name__ == "__main__":
    unittest.main()
