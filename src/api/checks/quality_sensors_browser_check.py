"""Nonbillable Chromium check of retained readings against the Quality model snapshot (#1288, E1/AC7).

Constructed isolated fixture with a local MOCK model provider, not the retained dataset and not a
real model. It correlates the readings a person sees with the readings the authorised Quality
request carried, then exercises unavailable, stale, withheld, attributed-unapproved and denied
states. It is an engineering check: not native-assistive-technology, human or real-AI acceptance.

Run from src/api: PYTHONPATH=tests:../core/tests:../agents/tests python3 -m checks.quality_sensors_browser_check
[--axe axe-4.10.3.min.js] [--out results.json]
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import threading
import time
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from playwright.sync_api import expect, sync_playwright

import release_support
import test_assistants as ta
import test_mvp
import test_quality_sensors as qs
from checks.regulatory_ux_check import AXE_SHA256
from zava_forward.api.server import App, make_handler
from zava_forward.core import projection, simulation_lane
from zava_forward.core.assistants import Assistants
from zava_forward.core.sqlstore import SqlStore

PASSWORD = "browser-test-only"


class Fixture(qs.Seed):
    """Reuses the retained-reading seeding helpers outside a unittest case."""

    def __init__(self, root: Path):
        self.root = root
        self.people = {}
        for i, role in enumerate(projection.STAFF_ROLES + ("Contractor", "Unknown")):
            self.people[role] = dict(
                code=f"ROLE-{i}", name=f"Human {i}", email=f"human{i}@example.test", role=role
            )
        data = json.loads(json.dumps(test_mvp.DATA))
        data["staff"] = list(self.people.values())
        for c in data["cases"]:
            c["handoff"] = dict(state="Offered", to_code="ROLE-0", note="Constructed handoff note")
        (root / "seed.json").write_text(json.dumps(data))
        self.pm = self.people["Retrofit Programme Manager"]
        self.store = SqlStore(str(root / "seed.json"), str(root / "state.sqlite"))
        self.provider = self.store.ai = qs.CapturingProvider()
        self.service = Assistants(self.store, ta.config())
        self.controls = {}
        with self.service.transaction() as db:
            for table in (
                "sensor_reading",
                "sensor_consumer_control",
                "sensor_consumer_control_home",
                "sensor_consumer_index_state",
                "sensor_consumer_policy",
            ):
                db.execute(f"DROP TABLE IF EXISTS {table}")
        release_support.install(self.store)


def main(axe_path: Path | None = None, out: Path | None = None):
    axe = None
    if axe_path:
        raw = axe_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != AXE_SHA256:
            raise ValueError("Unexpected axe 4.10.3 bytes")
        axe = raw.decode()
    root = Path.cwd() / f".q{uuid.uuid4().hex[:6]}"
    root.mkdir()
    os.environ["TMPDIR"] = str(root)
    fx = Fixture(root)
    inspector = fx.people["Quality Inspector"]
    liaison = fx.people["Resident Liaison Officer"]
    lane_store, lane_key = str(root / "sim.sqlite"), str(root / "sim.key")
    simulation_lane.provision(lane_store, lane_key)
    os.environ[simulation_lane.STORE_ENV] = lane_store
    os.environ[simulation_lane.KEY_ENV] = lane_key
    app = App(fx.store, PASSWORD)
    app.assistants = fx.service
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    passed, scans = [], []

    def check(name, condition):
        assert condition, name
        passed.append(name)
        print(f"PASS {name}")

    def scan(page, state):
        if axe is None:
            return
        page.evaluate(axe)
        result = page.evaluate("""async () => await axe.run(document.querySelector('main'), {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})""")
        scans.append(
            {"state": state, "violations": result["violations"], "incomplete": result["incomplete"]}
        )
        check(
            f"axe no serious/critical: {state}",
            not any(item["impact"] in ("serious", "critical") for item in result["violations"]),
        )

    def login(page, user):
        page.goto(base + "/app")
        page.fill("#email", user["email"])
        page.fill("#pw", PASSWORD)
        page.click("button[type=submit]")
        page.wait_for_selector("nav:not([hidden])")

    def open_quality(page, tag):
        page.goto(base + f"/app?{tag}#/case/ZF-1?tab=quality")
        expect(page.locator("#sensors")).to_be_visible()
        expect(page.locator("#sensors [role=status]").first).not_to_contain_text("Loading")
        return page.locator("#sensors")

    def open_flag(page, tag):
        page.goto(base + f"/app?{tag}#/case/ZF-1?tab=ai")
        card = page.locator("article").filter(has=page.locator("h3", has_text="Quality evidence"))
        expect(card).to_have_count(1)
        summary = page.get_by_text("Reviewed or stale suggestions", exact=True)
        if summary.count() and not card.is_visible():
            summary.click()
        expect(card).to_be_visible()
        return card

    try:
        with sync_playwright() as pw:
            chrome = os.environ.get("CHECK_BROWSER_EXECUTABLE") or shutil.which("google-chrome")
            browser = pw.chromium.launch(
                env=dict(os.environ, HOME=str(root)),
                **({"executable_path": chrome} if chrome else {}),
            )
            page = browser.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.route(
                "**/*",
                lambda route: (
                    route.continue_() if route.request.url.startswith(base) else route.abort()
                ),
            )

            fx.put(4)
            fx.add_live(10)
            fx.quality_ready()
            fx.service.scan()
            (tid,) = fx.quality_task()
            check("authorised Quality request reaches the mock provider", fx.service.execute(tid))
            sent = fx.provider.prompts[-1]["evidence"]
            captured = {
                (r["reading_id"], r["temperature_c"], r["humidity_pct"])
                for r in sent["sources"]["sensors"]["readings"]
            }
            check("captured model snapshot holds retained readings", len(captured) >= 4)

            login(page, inspector)
            panel = open_quality(page, "ok")
            newest = panel.locator("table").first
            shown = {
                (
                    row.locator("th").inner_text(),
                    row.locator("td").nth(2).inner_text(),
                    row.locator("td").nth(3).inner_text(),
                )
                for row in newest.locator("tbody tr").all()
            }
            check(
                "displayed reading IDs and values equal the captured model snapshot",
                shown == captured,
            )
            scan(page, "retained readings")

            proposal = open_flag(page, "flag")
            flag = proposal.get_by_role("group", name="Review flag status")
            expect(flag).to_contain_text("Review suggested by the model")
            expect(flag).to_contain_text("Not approved.")
            expect(flag).to_contain_text("local-test-double test test-model")
            cited = {
                m.split("reading ")[1]
                for m in re.findall(r"sensor [^,]+, reading [^;.]+", flag.inner_text())
            }
            check(
                "attributed unapproved flag cites readings the model was given",
                bool(cited) and cited <= {i for i, _, _ in captured},
            )
            expect(flag).to_contain_text(
                "still holds the readings this finding cited, with the same values"
            )
            check("flag offers no approval control", flag.get_by_role("button").count() == 0)
            scan(page, "unapproved flag")

            fx.set_consent("declined")
            panel = open_quality(page, "withheld")
            expect(panel).to_contain_text("Use the manual route")
            check("withheld consent shows no readings table", panel.locator("table").count() == 0)
            proposal = open_flag(page, "withheld-flag")
            expect(proposal.get_by_role("group", name="Review flag status")).to_contain_text(
                "Withheld: monitoring consent is not granted now"
            )
            check(
                "withheld current capture is not reported as missing readings",
                "no longer retained" not in proposal.inner_text()
                and "deleted" not in proposal.inner_text(),
            )
            scan(page, "withheld")

            fx.set_consent("granted")
            with fx.clock(7 * 3600):
                panel = open_quality(page, "stale")
                expect(panel).to_contain_text("stale")
                check(
                    "stale readings are labelled stale, not live",
                    "Freshness: stale" in panel.inner_text(),
                )
                scan(page, "stale")

            with fx.service.transaction() as db:
                db.execute("DROP TABLE sensor_reading")
            panel = open_quality(page, "unavailable")
            expect(panel).to_contain_text("Use the manual route")
            check(
                "unavailable readings are explicit, not an empty normal state",
                panel.locator("table").count() == 0 and "manual" in panel.inner_text().lower(),
            )
            proposal = open_flag(page, "unavailable-flag")
            expect(proposal.get_by_role("group", name="Review flag status")).to_contain_text(
                "Whether the cited readings have changed since capture is unknown."
            )
            check(
                "unavailable current capture is unknown, not missing",
                "no longer retained" not in proposal.inner_text()
                and "deleted" not in proposal.inner_text(),
            )
            scan(page, "unavailable")

            page = browser.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.route(
                "**/*",
                lambda route: (
                    route.continue_() if route.request.url.startswith(base) else route.abort()
                ),
            )
            login(page, inspector)
            page.goto(base + "/app?sim#/case/ZF-1?tab=ai")
            sim = page.locator("#simulation")
            expect(sim).to_be_visible()
            expect(sim).to_contain_text("Public synthetic simulation (not this home)")
            expect(sim).to_contain_text("Not a real home")
            check("simulation panel is labelled synthetic", "Not a real home" in sim.inner_text())
            page.get_by_role("button", name="Add Simulated Readings").click()
            expect(sim.locator("tbody tr")).not_to_have_count(0)
            shown = {
                (r.locator("th").inner_text(), *r.locator("td").all_inner_texts()[2:4])
                for r in sim.locator("tbody tr").all()
            }
            stored = {
                (r["reading_id"], r["temperature_c"], r["humidity_pct"])
                for r in app.simulation.view()["readings"]
            }
            check(
                "simulation UI readings equal the stored simulation readings",
                {(a, b, c) for a, b, c in shown} == stored,
            )
            page.get_by_role("button", name="Request Simulation Proposal").click()
            expect(page.locator("#simulation [role=status]").last).to_contain_text(
                "Proposal stored as unapproved"
            )
            expect(sim).to_contain_text("Status: unapproved proposal")
            check("proposal shown as unapproved", "Status: unapproved proposal" in sim.inner_text())
            check(
                "no accept control in the simulation",
                sim.get_by_role("button", name=re.compile("accept", re.I)).count() == 0,
            )
            scan(page, "simulation panel")

            def seed(findings, name):
                supplied = app.simulation.compose()["readings"]
                body = dict(
                    output=dict(summary="Seeded.", findings=findings, unknowns=[]),
                    model="seed",
                    request_digest=name * 16,
                    readings=supplied,
                )
                with app.simulation._connect() as db:
                    db.execute(
                        "INSERT INTO sim_proposals (digest,state,body,created) VALUES (?,?,?,?)",
                        (name * 16, simulation_lane.PROPOSAL_STATE, json.dumps(body), time.time()),
                    )
                return supplied

            loads = iter(range(100))

            def fresh_panel():
                page.goto(base + f"/app?sim{next(loads)}#/case/ZF-1?tab=ai")
                expect(sim).to_contain_text("Status: unapproved proposal")
                return sim.inner_text()

            first_cited = fresh_panel()
            check(
                "the stored proposal says how many readings it was given and how many it cited",
                "It was given 12 stored readings." in first_cited
                and re.search(r"It cited [12] of them", first_cited) is not None,
            )
            supplied = seed([dict(text="Only the home.", citations=["source:home"])], "a")
            text = fresh_panel()
            check(
                "a proposal citing only the home reports zero cited sensor readings",
                "It was given 12 stored readings. It cited no sensor readings." in text,
            )
            seed([], "b")
            text = fresh_panel()
            check(
                "an empty finding list is stated, not shown as an empty list",
                "The model gave no findings." in text and "It cited no sensor readings." in text,
            )
            one = f"sensor:{simulation_lane.SENSOR_ID}:{supplied[3][0]}"
            seed([dict(text="One of twelve.", citations=[one])], "c")
            text = fresh_panel()
            check(
                "one cited reading of twelve is reported as one of twelve",
                "It was given 12 stored readings. It cited 1 of them: " + supplied[3][0] in text,
            )
            sim.locator("details summary").click()
            expect(sim.locator("details li")).to_have_count(12)
            before = sim.inner_text()
            app.simulation.clock = lambda: time.time() + 3600
            app.simulation.observe()
            app.simulation.clock = time.time
            rotated = fresh_panel()
            check(
                "the historic request keeps its supplied and cited readings after rotation",
                "It was given 12 stored readings. It cited 1 of them: " + supplied[3][0] in rotated
                and before.count(supplied[3][0]) >= 1,
            )
            scan(page, "simulation panel with supplied and cited readings")
            page = browser.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.route(
                "**/*",
                lambda route: (
                    route.continue_() if route.request.url.startswith(base) else route.abort()
                ),
            )
            login(page, liaison)
            page.goto(base + "/app?denied#/case/ZF-1?tab=quality")
            denied = page.locator("#sensors")
            expect(denied).to_contain_text("Your role does not include indoor readings")
            check("denied role sees no readings", denied.locator("table").count() == 0)
            page.goto(base + "/app")
            status = None
            cookies = page.context.cookies()
            request = Request(
                base + "/api/cases/ZF-1/sensors",
                headers={"Cookie": "; ".join(f"{c['name']}={c['value']}" for c in cookies)},
            )
            try:
                urlopen(request)
            except HTTPError as error:
                status = error.code
            check("sensor API denies the same role", status in (401, 403))
            check("no page errors", not errors)
            browser.close()
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
        fx.service.stop()
        fx.store.db.close()
        shutil.rmtree(root, ignore_errors=True)
    if out:
        out.write_text(json.dumps({"passed": passed, "axe": scans}, indent=2))
    print(f"{len(passed)} checks passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    main(args.axe, args.out)
