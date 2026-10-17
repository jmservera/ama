"""Offline synthetic browser check for upload and recipient acceptance provenance."""

import copy
import json
import tempfile
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from dataset import DATA
from playwright.sync_api import sync_playwright
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        seed = Path(temporary) / "seed.json"
        seed.write_text(json.dumps(copy.deepcopy(DATA)))
        store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "browser-test")))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            with urllib.request.urlopen(base + "/healthz") as response:
                assert response.status == 200
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                context = browser.new_context(viewport={"width": 1280, "height": 900},
                                              reduced_motion="reduce")
                context.route("**/*", lambda route: route.continue_()
                              if route.request.url.startswith(base + "/") else route.abort())
                page = context.new_page()
                page.on("dialog", lambda dialog: dialog.accept())
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))

                def login(actor: str) -> None:
                    page.goto(base + "/app")
                    page.locator("#email").fill(f"{actor}@example.test")
                    page.locator("#pw").fill("browser-test")
                    page.locator("button[type=submit]").click()
                    page.locator("a.item").first.wait_for()
                    page.goto(base + "/app#/case/ZF-1")
                    page.get_by_role("heading", name="Documents", exact=True).wait_for()

                def source(prefix: str) -> None:
                    page.locator(f"#{prefix}-source").fill("SYN browser supplied register")
                    page.locator(f"#{prefix}-source_version").fill("browser-source-7")
                    page.locator(f"#{prefix}-reason").fill("Synthetic browser recorded change")

                login("sam")
                upload = page.locator("form").filter(has=page.locator("#doc-upload-source"))
                upload.get_by_label("Choose a file", exact=True).set_input_files(
                    {"name": "supplied.txt", "mimeType": "text/plain", "buffer": b"synthetic browser"})
                upload.get_by_role("button", name="Add document", exact=True).click()
                assert page.locator("#doc-upload-source").evaluate(
                    "(el) => el === document.activeElement")
                assert store.cases["ZF-1"]["documents"] == []
                source("doc-upload")
                page.locator("#doc-upload-reason").press("Enter")
                page.get_by_role("link", name="supplied.txt", exact=True).wait_for()
                assert store.cases["ZF-1"]["document_history"][-1]["source_version"] == "browser-source-7"

                source("ho-offer")
                page.locator("#ho-offer-reason").press("Enter")
                page.get_by_text("Waiting for an answer.", exact=False).wait_for()
                assert store.cases["ZF-1"]["owner_code"] == "RLO-01"

                context.clear_cookies()
                login("pam")
                source("ho-accept")
                # A concurrent receipt changes the expected handoff version.
                store.receive_handoff(DATA["staff"][1], "ZF-1")
                page.locator("#ho-accept-reason").press("Enter")
                status = page.locator("#ho-accept-status")
                status.get_by_text("Reload", exact=False).wait_for()
                assert status.evaluate("(el) => el === document.activeElement")
                assert page.locator("#ho-accept-source").input_value() == "SYN browser supplied register"
                assert store.cases["ZF-1"]["owner_code"] == "RLO-01"

                page.reload()
                source("ho-accept")
                page.locator("#ho-accept-reason").press("Enter")
                page.get_by_role("button", name="Complete handoff", exact=True).wait_for()
                assert store.cases["ZF-1"]["owner_code"] == "PM-01"
                assert store.cases["ZF-1"]["handoff_history"][-1]["source_version"] == "browser-source-7"
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                assert not errors, errors
                browser.close()
            reopened = SqlStore("seed-not-read", store.db_path)
            try:
                case = reopened.cases["ZF-1"]
                for history, action in (("document_history", "upload_document"),
                                        ("handoff_history", "handoff_accepted")):
                    event = case[history][-1]
                    assert event["source_version"] == "browser-source-7"
                    audit = next(e for e in reopened.audit_entries() if e["action"] == action)
                    assert json.loads(audit["detail"]) == event
                assert reopened.verify_audit()
            finally:
                reopened.db.close()
            print("PASS: required input/focus, keyboard upload/offer/accept, stale inline refusal, "
                  "recipient ownership, 390px/reduced motion, SQL reopen/event-audit equality; "
                  "no page errors or external requests.")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            store.db.close()


if __name__ == "__main__":
    main()
