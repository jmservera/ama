"""Manifest default queues compared with the real API (partial AC-034/043 evidence)."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from checks import workbench_browser_check as workbench
from checks.workbench_browser_check import MANIFEST, synthetic_data
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, sync_playwright
from zava_forward.core.store import Store

from zava_forward.api.server import App, make_handler

PASSWORD = "synthetic-only"


class ManifestDefaultsMatchApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        seed = Path(self.tmp.name) / "zavaforward.json"
        seed.write_text(json.dumps(synthetic_data()), encoding="utf-8")
        app_type: Any = App
        handler: Any = make_handler
        self.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), handler(app_type(Store(str(seed)), PASSWORD))
        )
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def call(self, path: str, cookie: str = "", body: dict[str, Any] | None = None) -> Any:
        request = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Cookie": cookie, "X-ZF-CSRF": "1"},
        )
        with urlopen(request, timeout=5) as response:
            return json.loads(response.read()), response.headers.get("Set-Cookie", "")

    def login(self, email: str) -> str:
        _, cookie = self.call("/api/login", body={"email": email, "password": PASSWORD})
        return str(cookie).split(";")[0]

    def test_default_ids_count_and_order_match_the_real_own_queue(self) -> None:
        checked = 0
        for profile in MANIFEST["profiles"]:
            default = profile.get("default")
            if default is None:
                continue
            checked += 1
            with self.subTest(profile=profile["perspective"]):
                cookie = self.login(profile["identity"])
                page, _ = self.call(f"/api/cases?view=mine&sort={default['order']}", cookie)
                self.assertEqual([row["id"] for row in page["items"]], default["ids"])
                self.assertEqual(page["total"], default["count"])
        self.assertEqual(checked, 8)

    def test_all_cases_scope_is_the_declared_fixture_set_for_staff(self) -> None:
        cookie = self.login("pam@example.test")
        page, _ = self.call("/api/cases?view=all&sort=urgent", cookie)
        self.assertEqual({row["id"] for row in page["items"]}, set(MANIFEST["all_case_ids"]))

    def test_declared_endpoints_are_reachable_for_each_partial_profile(self) -> None:
        for profile in MANIFEST["profiles"]:
            endpoint = profile.get("endpoint", "")
            if not endpoint.startswith("#/case/"):
                continue
            with self.subTest(profile=profile["perspective"]):
                cookie = self.login(profile["identity"])
                case, _ = self.call("/api/cases/" + endpoint.removeprefix("#/case/"), cookie)
                self.assertEqual(case["id"], endpoint.removeprefix("#/case/"))


QUEUE_PAGE = """<p id="workspace-status"></p>
<select id="f-queue"><option value="">Any</option><option>new</option><option>stale</option>
<option>overdue</option><option>priority</option><option>unowned</option></select><ul></ul>
<script>
const rows = {new: ["ZF-1"], stale: ["ZF-1"], overdue: ["ZF-4"], priority: [], unowned: []};
function render(queue) {
  const ids = rows[queue];
  document.querySelector("#workspace-status").textContent =
    `My assigned cases. ${ids.length} ${ids.length === 1 ? "case" : "cases"}. ` +
    `Workflow stage: any. Work queue: ${queue}. Order: Urgent first.`;
  document.querySelector("ul").replaceChildren(...ids.map(id => {
    const link = document.createElement("a");
    link.className = "item";
    link.href = "#/case/" + id;
    return link;
  }));
}
// The response-to-render gap: the list keeps the previous queue until the timer renders.
document.querySelector("#f-queue").addEventListener("change", event =>
  setTimeout(() => render(event.target.value), 300));
render("stale");
</script>"""


class QueueResultSynchronization(unittest.TestCase):
    def setUp(self) -> None:
        self.playwright = sync_playwright().start()
        self.addCleanup(self.playwright.stop)
        try:
            browser = self.playwright.chromium.launch()
        except PlaywrightError as error:
            if "Executable doesn't exist" in str(error):
                self.skipTest("Chromium is installed by the later browser-check step")
            raise
        self.addCleanup(browser.close)
        self.page: Page = browser.new_page()
        self.page.set_content(QUEUE_PAGE)

    def status(self) -> str:
        return self.page.locator("#workspace-status").inner_text()

    def test_equal_count_stale_to_overdue_waits_for_the_new_identity(self) -> None:
        self.assertEqual(workbench.ids(self.page), ["ZF-1"])
        self.page.locator("#f-queue").select_option("overdue")
        workbench.wait_queue_result(self.page, "overdue", ["ZF-4"])
        self.assertEqual(workbench.ids(self.page), ["ZF-4"])
        self.assertIn("Work queue: overdue.", self.status())

    def test_equal_count_empty_transition_waits_for_the_new_queue(self) -> None:
        for queue in ("overdue", "priority", "unowned"):
            self.page.locator("#f-queue").select_option(queue)
            workbench.wait_queue_result(self.page, queue, ["ZF-4"] if queue == "overdue" else [])
            self.assertIn(f"Work queue: {queue}.", self.status())
        self.assertEqual(workbench.ids(self.page), [])

    def test_timeout_reports_expected_and_observed_result(self) -> None:
        with self.assertRaises(AssertionError) as raised:
            workbench.wait_queue_result(self.page, "overdue", ["ZF-4"], timeout_ms=100)
        message = str(raised.exception)
        for part in ("overdue queue", "['ZF-4']", "['ZF-1']", "Work queue: stale."):
            self.assertIn(part, message)

    def test_status_format_matches_the_application(self) -> None:
        web = Path(workbench.__file__).parents[1] / "src/zava_forward/api/web"
        source = (web / "app.js").read_text()
        for token in (
            '${total} ${total === 1 ? "case" : "cases"}. Workflow stage:',
            'Work queue: ${listState.queue || "any"}. Order:',
        ):
            self.assertIn(token, source)


if __name__ == "__main__":
    unittest.main()
