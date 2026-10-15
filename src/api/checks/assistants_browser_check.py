"""Nonbillable Chromium exercise on an isolated fixture, not the retained dataset.

Run: PYTHONPATH=src/api/tests:src/core/tests python3 src/api/checks/assistants_browser_check.py.
"""
import json
import os
import re
import shutil
import threading
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from test_assistants import Provider, config
from test_mvp import DATA
from zava_forward.core.assistants import Assistants, REGISTRY, canonical
from zava_forward.api.server import App, make_handler
from zava_forward.core.sqlstore import SqlStore


def main():
    root = Path.cwd() / f".b{uuid.uuid4().hex[:6]}"
    root.mkdir()
    # Playwright/Chromium scratch state is confined to the project as well.
    os.environ["TMPDIR"] = str(root)
    seed = root / "seed.json"
    data = json.loads(json.dumps(DATA))
    data["cases"][0]["appointments"] = [
        dict(date=day, slot="Morning", type="Assessment", who="Test Surveyors",
             person="Kim Test", outcome="Booked")
        for day in ("2026-10-14", "2026-10-15")
    ]
    seed.write_text(json.dumps(data))
    store = SqlStore(str(seed), str(root / "state.sqlite"))
    store.ai = Provider()
    app = App(store, "browser-test-only")
    app.assistants = Assistants(store, config())
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    passed = []

    def check(name, condition):
        assert condition, name
        passed.append(name)
        print(f"PASS {name}")

    try:
        with sync_playwright() as pw:
            chrome = os.environ.get("CHECK_BROWSER_EXECUTABLE") or shutil.which("google-chrome")
            browser = pw.chromium.launch(env=dict(os.environ, HOME=str(root)),
                                         **({"executable_path": chrome} if chrome else {}))
            page = browser.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            # No external calls, including background map tiles, are needed.
            page.route("**/*", lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
            page.goto(base + "/app")
            page.fill("#email", "pam@example.test")
            page.fill("#pw", "browser-test-only")
            page.click("button[type=submit]")
            page.wait_for_selector("nav:not([hidden])")
            page.goto(base + "/app#/case/ZF-1")
            expect(page.get_by_role("button", name="Request Stock facts and prioritisation", exact=True)).to_be_visible()
            check("five distinct case-card controls", page.locator("button:has-text('Request ')").count() == 5)
            names = ("Stock facts and prioritisation", "Assessment preparation", "Funding evidence",
                     "Works and resident coordination", "Quality evidence")
            pm = DATA["staff"][1]
            before = store.assistant_connection()
            domain = before.execute("SELECT id,body FROM cases ORDER BY id").fetchall()
            before.close()
            for cap, name in zip(REGISTRY, names):
                page.get_by_role("button", name=f"Request {name}", exact=True).click()
                page.wait_for_selector(f"article h3:has-text('{name}')")
                p = next(p for p in app.assistants.listing(pm)["proposals"] if p["capability"] == cap)
                check(f"{cap} provider path", app.assistants.execute(p["id"]))
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            expect(page.locator("article p[role=status]").filter(has_text=re.compile(r"^ready\."))).to_have_count(5)
            check("all five rendered ready", page.locator("article").count() == 5)
            check("shared role-owned queue link", page.get_by_role("link", name="Shared role-owned review queue").count() == 1)
            card = page.locator("article").filter(has=page.locator("h3", has_text="Stock facts and prioritisation"))
            card.get_by_label("Source verification or review note").fill("Checked each cited source and retained unknowns.")
            card.get_by_label("I checked the cited sources", exact=False).check()
            card.get_by_role("button", name="Record human source verification").click()
            try:
                page.wait_for_selector("button:has-text('Accept proposal only')", timeout=5000)
            except Exception as e:
                raise AssertionError(card.inner_text()) from e
            card.get_by_label("Source verification or review note").fill("Accept this proposal, not the case.")
            card.get_by_role("button", name="Accept proposal only", exact=True).click()
            page.wait_for_selector("article >> text=accepted.")
            check("explicit separate human verification and accept", True)
            db = store.assistant_connection()
            check("assistant actions preserve every case", domain == db.execute("SELECT id,body FROM cases ORDER BY id").fetchall())
            db.close()
            with app.assistants.transaction() as db:
                c = json.loads(db.execute("SELECT body FROM cases WHERE id='ZF-1'").fetchone()[0])
                c["home"]["epc"] = "F"
                db.execute("UPDATE cases SET body=? WHERE id='ZF-1'", (canonical(c),))
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.wait_for_selector("article >> text=stale.")
            check("material change visibly stale with no accept", page.locator("button:has-text('Accept proposal only')").count() == 0)
            store.ai.bad = "citation"
            page.get_by_role("button", name="Request Stock facts and prioritisation", exact=True).click()
            page.wait_for_timeout(100)
            p = next(p for p in app.assistants.listing(pm)["proposals"] if not p["stale"] and p["capability"] == "stock-prioritisation")
            app.assistants.execute(p["id"])
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.wait_for_selector("article >> text=failed.")
            check("malformed citation shows failed and manual route", "human/manual work required" in page.locator("#app").inner_text())
            app.assistants = Assistants(store, {})
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.wait_for_selector("text=Operator authority, finite allowance and expiry are required.")
            check("disabled configuration does not block manual case access", page.locator("h1").count() == 1)
            page.get_by_role("link", name="Shared role-owned review queue").click()
            page.wait_for_selector("h1:has-text('Role-owned assistant proposals')")
            check("shared queue retains stale failure and history", page.locator("article").count() == 6)

            held = []
            def hold(route):
                held.append(route)

            page.route("**/api/assistants", hold)
            page.goto(base + "/app#/case/ZF-1")
            expect(page.get_by_role("heading", name="Log a call", exact=True)).to_be_visible(timeout=2000)
            expect(page.get_by_role("button", name="Save answer", exact=True)).to_be_enabled()
            check("pending assistance does not block manual controls", bool(held))
            page.fill("#outcome", "Manual call while assistance is pending")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator(".tl")).to_contain_text("Manual call while assistance is pending")
            check("manual write succeeds while assistance stays pending", True)
            expect(page.get_by_role("status").filter(
                has_text="Assistance unavailable: Assistance request timed out")).to_be_visible(timeout=12000)
            check("assistance deadline exposes manual fallback", True)
            for route in held:
                route.abort()
            page.unroute("**/api/assistants", hold)
            page.goto(base + "/app#/case/ZF-2")
            expect(page.get_by_role("button", name="Refresh proposals", exact=True)).to_be_visible()

            stale = []
            def hold_first(route):
                if not stale:
                    stale.append(route)
                else:
                    route.continue_()

            page.route("**/api/assistants", hold_first)
            page.goto(base + "/app#/case/ZF-1")
            expect(page.locator("#app")).to_contain_text("Reference ZF-1")
            expect(page.get_by_role("status").filter(has_text="Loading assistance.")).to_be_visible()
            page.goto(base + "/app#/case/ZF-2")
            expect(page.locator("#app")).to_contain_text("Reference ZF-2")
            expect(page.get_by_role("button", name="Refresh proposals", exact=True)).to_be_visible()
            late = app.assistants.registry(pm)
            late["disabled"] = "STALE-ASSISTANT-PANEL"
            stale[0].fulfill(status=200, content_type="application/json", body=json.dumps(late))
            page.wait_for_timeout(100)
            check("late assistance cannot populate a different case",
                  "STALE-ASSISTANT-PANEL" not in page.locator("#app").inner_text())
            page.unroute("**/api/assistants", hold_first)
            page.goto(base + "/app#/visits")
            expect(page.get_by_role("heading", name="Visits coming up", exact=True)).to_be_visible()
            expect(page.locator("#app ul.list > li")).to_have_count(2)
            check("booked visit day groups render as elements", page.locator("#app section.card").count() == 2)
            page.locator("#app ul.list > li a").first.click()
            expect(page.locator("#app")).to_contain_text("Reference ZF-1")
            check("rendered visit opens its case", True)
            check("no page errors", not errors)
            browser.close()
        print(f"{len(passed)} browser checks passed; no billable provider or retained dataset access.")
    finally:
        app.assistants.stop()
        server.shutdown()
        server.server_close()
        thread.join()
        store.db.close()
        shutil.rmtree(root)


if __name__ == "__main__":
    main()
