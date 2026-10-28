"""Nonbillable Chromium exercise on an isolated fixture, not the retained dataset.

Run: PYTHONPATH=src/api/tests:src/core/tests python3 src/api/checks/assistants_browser_check.py.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import threading
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

import release_support
from checks.regulatory_ux_check import AXE_SHA256
from test_assistants import Provider, config
from test_mvp import DATA
from zava_forward.core.assistants import Assistants, REGISTRY, canonical
from zava_forward.api.server import App, make_handler
from zava_forward.core.sqlstore import SqlStore


def main(axe_path: Path | None = None, out: Path | None = None):
    axe = None
    scans = []
    if axe_path:
        raw = axe_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
            raise ValueError("Unexpected axe 4.10.3 bytes")
        axe = raw.decode()
    if out:
        out.mkdir(parents=True, exist_ok=False)
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
    release_support.install(store, legacy=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    passed = []

    def check(name, condition):
        assert condition, name
        passed.append(name)
        print(f"PASS {name}")

    def scan(page, state):
        if axe is None:
            return
        page.evaluate(axe)
        result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a',
            'wcag21aa', 'wcag22aa']}})""")
        scans.append({"state": state, "violations": result["violations"],
                      "incomplete": result["incomplete"]})
        check(f"axe no serious/critical: {state}", not any(
            item["impact"] in ("serious", "critical") for item in result["violations"]
        ))

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
            page.goto(base + "/app#/case/ZF-1?tab=ai")
            expect(page.get_by_role("button", name="Request Stock facts and prioritisation", exact=True)).to_be_visible()
            check("five distinct case-card controls", page.locator(
                "#case-panel-ai > section.card button:has-text('Request ')"
            ).count() == 5)
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
            card.get_by_label("Reason", exact=True).fill(
                "Checked each cited source and retained unknowns."
            )
            card.get_by_label("I checked the cited sources", exact=False).check()
            card.get_by_role("button", name="Record human source verification").click()
            expect(card.get_by_role("button", name="Accept", exact=True)).to_be_enabled()
            card.get_by_role("button", name="Edit", exact=True).click()
            editing = card.get_by_label("Edited evidence proposal JSON", exact=True)
            pending_output = json.loads(editing.input_value())
            pending_output["summary"] = "Unsubmitted synthetic review wording"
            editing.fill(json.dumps(pending_output))
            card.get_by_label("Reason", exact=True).fill("Pending source review reason")
            card.get_by_label("I checked the cited sources", exact=False).check()
            previous = editing.element_handle()
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.wait_for_function("old => !old.isConnected", arg=previous)
            expect(editing).to_have_value(json.dumps(pending_output))
            expect(card.get_by_label("Reason", exact=True)).to_have_value(
                "Pending source review reason"
            )
            expect(card.get_by_label(
                "I checked the cited sources", exact=False
            )).to_be_checked()
            check("async proposal reload preserves current-revision edits", True)
            overrides = [
                {"stale": True},
                {"state": "queued"},
                {"state": "accepted"},
                {"state": "failed"},
                {"actionable": False},
                {"release_denial": {"reason": "Synthetic release denial"}},
                {"epoch_current": False},
                {"verification": None},
                {"verification": {"by": "other@example.test", "note": "Other reviewer"}},
            ]
            review_requests = []

            def reviews(request):
                if request.method == "POST" and request.url.endswith("/review"):
                    review_requests.append(request.url)

            page.on("request", reviews)
            for override in overrides:
                def unavailable(route, _request, changes=override):
                    response = route.fetch()
                    body = response.json()
                    for item in body["proposals"]:
                        if item["capability"] == "stock-prioritisation":
                            item.update(changes)
                    route.fulfill(response=response, json=body)

                page.route("**/api/assistants/proposals?**", unavailable)
                previous = editing.element_handle()
                page.get_by_role("button", name="Refresh proposals", exact=True).click()
                page.wait_for_function("old => !old.isConnected", arg=previous)
                expect(editing).to_have_value(json.dumps(pending_output))
                expect(editing).to_be_visible()
                for label in ("Accept", "Edit", "Save edited proposal"):
                    expect(card.get_by_role("button", name=label, exact=True)).to_be_disabled()
                before = len(review_requests)
                card.get_by_role("button", name="Save edited proposal", exact=True).evaluate(
                    "el => el.click()"
                )
                page.evaluate("() => new Promise(resolve => setTimeout(resolve, 0))")
                check(f"restored unavailable editor cannot submit/{override}",
                      len(review_requests) == before)
                check(f"restored unavailable text remains selectable/{override}",
                      editing.evaluate("""el => {
                        el.focus(); el.select();
                        return !el.disabled && el.selectionEnd === el.value.length;
                      }"""))
                scan(page, f"restored-editor/{override}")
                page.unroute("**/api/assistants/proposals?**", unavailable)
            page.remove_listener("request", reviews)
            previous = editing.element_handle()
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.wait_for_function("old => !old.isConnected", arg=previous)
            expect(editing).to_have_value(json.dumps(pending_output))
            expect(card.get_by_role("button", name="Save edited proposal")).to_be_enabled()
            scan(page, "restored-editor/ready-own-verification")
            page.get_by_role("tab", name="Resident", exact=True).click()
            page.locator("#outcome").fill("Unrelated call with pending proposal review")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator("#outcome")).to_have_value("")
            page.get_by_role("tab", name="AI assistance", exact=False).click()
            expect(editing).to_have_value(json.dumps(pending_output))
            expect(card.get_by_label("Reason", exact=True)).to_have_value(
                "Pending source review reason"
            )
            check("unrelated successful action preserves async review edits", True)
            pending_loads = []
            page.route("**/api/assistants/proposals?**", lambda route: pending_loads.append(route))
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            expect(page.get_by_text(
                "Loading assistance. Ordinary case controls remain available.", exact=True
            )).to_have_count(1)
            page.get_by_role("tab", name="Resident", exact=True).click()
            page.locator("#outcome").fill("Second refresh while proposal loader is pending")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator("#outcome")).to_have_value("")
            page.get_by_role("tab", name="AI assistance", exact=False).click()
            expect(page.get_by_text(
                "Loading assistance. Ordinary case controls remain available.", exact=True
            )).to_be_visible()
            check("two independent proposal loads are pending", len(pending_loads) == 2)
            for pending in pending_loads:
                pending.fulfill(response=pending.fetch())
            page.unroute("**/api/assistants/proposals?**")
            expect(editing).to_have_value(json.dumps(pending_output))
            expect(card.get_by_label("Reason", exact=True)).to_have_value(
                "Pending source review reason"
            )
            check("overlapping refreshes preserve unresolved proposal snapshots", True)
            db = store.assistant_connection()
            domain = db.execute("SELECT id,body FROM cases ORDER BY id").fetchall()
            db.close()
            current_proposal = next(
                item for item in app.assistants.listing(pm)["proposals"]
                if item["capability"] == "stock-prioritisation"
            )
            revised = page.request.post(
                base + f"/api/assistants/proposals/{current_proposal['id']}/review",
                headers={"X-ZF-CSRF": "1"},
                data={"action": "verify", "revision": current_proposal["revision"],
                      "source_verified": True, "note": "Concurrent synthetic source review"},
            )
            check("concurrent revision fixture records source review", revised.status == 200)
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            expect(card.get_by_role("button", name="Accept", exact=True)).to_be_enabled()
            expect(card.get_by_label("Reason", exact=True)).to_have_value("")
            check(
                "different revision never inherits pending review edits",
                json.loads(editing.input_value())["summary"]
                != "Unsubmitted synthetic review wording",
            )
            recovery = page.locator("details").filter(has=page.get_by_text(
                "Unsubmitted review edits from earlier evidence", exact=True
            ))
            recovery.locator("summary").click()
            expect(recovery.get_by_label("Earlier Reason", exact=True)).to_have_value(
                "Pending source review reason"
            )
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            expect(recovery.get_by_label("Earlier Reason", exact=True)).to_have_value(
                "Pending source review reason"
            )
            check("old-revision edits remain available to copy across refresh", True)
            recovery.locator("summary").click()
            recovery.get_by_role("button", name="Discard earlier review edits").click()
            card.get_by_role("button", name="Edit", exact=True).click()
            own_pending = json.loads(editing.input_value())
            own_pending["summary"] = "Unsent JSON during own source verification"
            editing.fill(json.dumps(own_pending))
            card.get_by_label("Reason", exact=True).fill("Rechecked the supplied sources")
            card.get_by_label("I checked the cited sources", exact=False).check()
            card.get_by_role("button", name="Record human source verification").click()
            expect(recovery.get_by_label(
                "Earlier Edited evidence proposal JSON", exact=True
            )).to_have_value(json.dumps(own_pending))
            check(
                "source verification retains unsent JSON against its earlier revision",
                json.loads(editing.input_value())["summary"]
                != "Unsent JSON during own source verification",
            )
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            expect(recovery.get_by_label(
                "Earlier Edited evidence proposal JSON", exact=True
            )).to_have_value(json.dumps(own_pending))
            recovery.locator("summary").click()
            recovery.get_by_role("button", name="Discard earlier review edits").click()
            card.get_by_label("Reason", exact=True).fill("Accept this proposal, not the case.")
            with page.expect_response("**/api/assistants/proposals/*/review") as accepted:
                card.get_by_role("button", name="Accept", exact=True).click()
            if accepted.value.status != 200:
                raise AssertionError(f"Accept failed: {accepted.value.text()}")
            check("accept records current revision", True)
            page.wait_for_selector("article >> text=accepted.", state="attached")
            check("explicit separate human verification and accept", True)
            db = store.assistant_connection()
            check("assistant actions preserve every case", domain == db.execute("SELECT id,body FROM cases ORDER BY id").fetchall())
            db.close()
            with app.assistants.transaction() as db:
                c = json.loads(db.execute("SELECT body FROM cases WHERE id='ZF-1'").fetchone()[0])
                c["home"]["epc"] = "F"
                db.execute("UPDATE cases SET body=? WHERE id='ZF-1'", (canonical(c),))
            page.get_by_role("button", name="Refresh proposals", exact=True).click()
            page.get_by_text("Reviewed or stale suggestions", exact=True).click()
            page.wait_for_selector("article >> text=stale.")
            check("material change visibly stale with disabled accept", all(
                button.is_disabled()
                for button in page.get_by_role("button", name="Accept", exact=True).all()
            ))
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
            page.goto(base + "/app#/case/ZF-1?tab=resident")
            expect(page.get_by_role("heading", name="Log a call", exact=True)).to_be_visible(timeout=2000)
            expect(page.get_by_text("Read-only resident decisions.", exact=False)).to_be_visible()
            expect(page.get_by_role("button", name="Save", exact=True)).to_be_enabled()
            check("pending assistance does not block manual controls", bool(held))
            page.fill("#outcome", "Manual call while assistance is pending")
            page.get_by_role("button", name="Save", exact=True).click()
            expect(page.locator(".tl")).to_contain_text("Manual call while assistance is pending")
            check("manual write succeeds while assistance stays pending", True)
            page.get_by_role("tab", name="AI assistance", exact=False).click()
            expect(page.get_by_role("status").filter(
                has_text="Assistance unavailable: Assistance request timed out")).to_be_visible(timeout=12000)
            check("assistance deadline exposes manual fallback", True)
            for route in held:
                route.abort()
            page.unroute("**/api/assistants", hold)
            page.goto(base + "/app#/case/ZF-2?tab=ai")
            expect(page.get_by_role("button", name="Refresh proposals", exact=True)).to_be_visible()

            stale = []
            def hold_first(route):
                if not stale:
                    stale.append(route)
                else:
                    route.continue_()

            page.route("**/api/assistants", hold_first)
            page.goto(base + "/app#/case/ZF-1?tab=ai")
            expect(page.locator("#app")).to_contain_text("Reference ZF-1")
            expect(page.get_by_role("status").filter(has_text="Loading assistance.")).to_be_visible()
            page.goto(base + "/app#/case/ZF-2?tab=ai")
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
            if out:
                (out / "results.json").write_text(json.dumps({
                    "browser": browser.version, "axe_version": "4.10.3" if axe else None,
                    "axe_sha256": AXE_SHA256 if axe else None,
                    "scans": scans, "checks": passed, "page_errors": errors,
                }, indent=2) + "\n")
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    main(args.axe, args.out)
