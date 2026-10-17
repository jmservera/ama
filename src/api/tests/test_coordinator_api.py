"""Authenticated fictional coordinator HTTP, browser and opt-in loopback SQL parity."""

import copy
import json
import os
import tempfile
import threading
import unittest
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from test_coordinator import fixture
from test_progress_reports import AS_OF
from zava_forward.core import insights
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api.server import App, make_handler


class CoordinatorApi(unittest.TestCase):
    backend = "sqlite"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(fixture()))
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore, _Conn, connection_string

            if os.environ.get("ZF_SQL_SERVER") not in ("localhost", "127.0.0.1"):
                raise RuntimeError("Coordinator SQL parity requires a task-owned loopback server.")
            environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
            environment.start()
            self.addCleanup(environment.stop)
            self.admin = _Conn(connection_string())
            self.addCleanup(self.admin.close)
            self.database = "zf_coordinator101_" + uuid.uuid4().hex
            self.admin.execute(f"CREATE DATABASE [{self.database}]")
            self.addCleanup(self.drop_database)
            os.environ["ZF_SQL_DATABASE"] = self.database
            self.store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        elif self.backend == "sqlite":
            self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        else:
            self.store = Store(str(self.path))
        if hasattr(self.store, "db"):
            self.addCleanup(self.store.db.close)
        self.app = App(self.store, "synthetic-coordinator-only")
        self.app.tiles = dict(url=None, attribution="", host=None)
        self.app.csp = "default-src 'self'; img-src 'self' data: blob:; frame-ancestors 'none'"
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def drop_database(self) -> None:
        self.admin.execute(
            f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
        )
        self.admin.execute(f"DROP DATABASE [{self.database}]")

    def call(self, path: str, actor: str = "pam") -> tuple[int, Any]:
        if actor and actor not in self.cookies:
            request = Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-coordinator-only")
                ).encode(),
            )
            with urlopen(request, timeout=10) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = Request(self.base + path, headers={"Cookie": self.cookies.get(actor, "")})
        try:
            with urlopen(request, timeout=10) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def query(self, **query: str) -> str:
        return "/api/coordinator?" + urlencode(dict(as_of=AS_OF, view="all", **query))

    def test_population_count_pagination_and_legacy_routes(self) -> None:
        for filters in (
            {},
            {"area": "Test"},
            {"flag": "hazard"},
            {"q": "ZF-2"},
            {"queue": "blocked"},
            {"flag": "fundingprog"},
        ):
            code, report = self.call(self.query(**filters))
            self.assertEqual(code, 200, report)
            code, page = self.call(
                "/api/cases?" + urlencode(dict(view="all", limit="2", **filters))
            )
            self.assertEqual(code, 200, page)
            self.assertEqual(report["cohort"]["selected_cases"], page["total"])
            self.assertEqual(report["records"]["total"], page["total"])
            self.assertEqual(report["map"]["total"], page["total"])
        code, page = self.call(self.query(limit="2", offset="2"))
        self.assertEqual(code, 200, page)
        self.assertEqual([x["id"] for x in page["records"]["items"]], ["ZF-3", "ZF-4"])
        self.assertIn("kpis", self.call("/api/stats")[1])

    def test_roles_scope_field_contract_and_authentication(self) -> None:
        self.assertEqual(self.call(self.query(), "")[0], 401)
        self.assertEqual(self.call(self.query(), "con")[0], 403)
        code, report = self.call(self.query(), "rex")
        self.assertEqual(code, 200, report)
        raw = json.dumps(report)
        for private in ("PRIVATE", "Pat Test", "01000", "adjustment", "source_version"):
            self.assertNotIn(private, raw)
        for actor, count in (("sam", 4), ("pam", 1), ("rex", 0)):
            code, report = self.call(
                "/api/coordinator?" + urlencode(dict(as_of=AS_OF, view="mine")), actor
            )
            self.assertEqual(code, 200, report)
            self.assertEqual(report["map"]["total"], count)
        with self.store.lock:
            current = self.store.staff["rex@example.test"]
            current["role"] = "Mystery"
            if hasattr(self.store, "db"):
                self.store.db.execute(
                    "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), current["email"])
                )
            self.store.save()
        self.assertEqual(self.call(self.query(), "rex")[0], 403)

    def test_invalid_queries_refuse_instead_of_silently_widening(self) -> None:
        for suffix in (
            "&area=",
            "&area=Test&area=Other",
            "&unknown=x",
            "&view=closed",
            "&metric=exclusions",
            "&metric_stage=wat",
            "&limit=0",
            "&bbox=nan,0,1,2",
        ):
            path = self.query() + suffix
            code, result = self.call(path)
            self.assertEqual(code, 400, result)
            self.assertIn("error", result)
        self.assertEqual(self.call("/api/coordinator?view=all")[0], 400)
        self.assertEqual(self.call(self.query(metric="priority"))[0], 400)

    def test_mixed_case_registered_email_authenticates_without_widening_access(self) -> None:
        with self.store.lock:
            registered = self.store.staff["pam@example.test"]
            registered["email"] = "Pam@Example.Test"
            if hasattr(self.store, "db"):
                self.store.db.execute(
                    "UPDATE staff SET body=? WHERE email=?",
                    (json.dumps(registered), "pam@example.test"),
                )
            self.store.save()
        self.assertEqual(self.call("/api/me")[1]["user"]["email"], "Pam@Example.Test")
        code, listing = self.call("/api/cases?view=all&limit=2")
        self.assertEqual(code, 200, listing)
        code, report = self.call(self.query())
        self.assertEqual(code, 200, report)
        self.assertEqual(report["records"]["total"], listing["total"])
        self.assertEqual(report["map"]["total"], listing["total"])
        self.assertEqual(self.call(self.query(), "")[0], 401)
        self.assertEqual(self.call(self.query(), "con")[0], 403)
        for role in ("Mystery", "", None):
            with self.subTest(role=role):
                with self.store.lock:
                    registered = self.store.staff["pam@example.test"]
                    registered["role"] = role
                    if hasattr(self.store, "db"):
                        self.store.db.execute(
                            "UPDATE staff SET body=? WHERE email=?",
                            (json.dumps(registered), "pam@example.test"),
                        )
                    self.store.save()
                self.assertEqual(self.call(self.query())[0], 403)
        with self.store.lock:
            del self.store.staff["pam@example.test"]
            if hasattr(self.store, "db"):
                self.store.db.execute("DELETE FROM staff WHERE email=?", ("pam@example.test",))
            self.store.save()
        self.assertEqual(self.call(self.query())[0], 401)

    def test_exit_drillthrough_unknowns_and_cluster_population(self) -> None:
        code, excluded = self.call(self.query(flag="support", metric="filtered_out"))
        self.assertEqual(code, 200, excluded)
        hazard = next(row for row in excluded["records"]["items"] if row["id"] == "ZF-4")
        self.assertTrue(hazard["stopped"])
        code, report = self.call(self.query(metric="exits", metric_stage="Contact paused"))
        self.assertEqual(code, 200, report)
        self.assertEqual([x["id"] for x in report["records"]["items"]], ["ZF-1"])
        self.assertEqual(report["map"]["total"], 1)
        with patch.object(insights, "MAP_CAP", 1):
            code, report = self.call(self.query(bbox="54,-2,55,-1"))
        self.assertEqual(code, 200, report)
        self.assertEqual(sum(x["count"] for x in report["map"]["items"]), 2)
        self.assertEqual(report["map"]["in_view"], 2)
        self.assertEqual(report["map"]["total"], 5)
        self.assertEqual(report["coverage"]["stage_history_unknown"], 3)
        self.assertIsNone(report["coverage"]["lifecycle_exclusions"])

    def test_reload_external_writer_and_no_aggregate_writes(self) -> None:
        before = copy.deepcopy(self.store.cases)
        audit = list(self.store.audit_entries())
        self.assertEqual(self.call(self.query())[0], 200)
        self.assertEqual(self.store.cases, before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        if self.backend == "sqlite":
            other = SqlStore("unused", self.store.db_path)
        elif self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore

            other = MssqlStore("unused", state_dir=self.tmp.name)
        else:
            other = self.store
        try:
            with other.lock:
                other._case("ZF-5")["home"]["area"] = "Test"
                other.save()
            report = self.call(self.query(area="Test"))[1]
            self.assertEqual(report["records"]["total"], 5)
            self.assertEqual(report["map"]["total"], 5)
            self.assertEqual(list(self.store.audit_entries()), audit)
            if hasattr(self.store, "db"):
                seq = self.store._db_seq()
                self.call(self.query())
                self.assertEqual(self.store._db_seq(), seq)
        finally:
            if other is not self.store:
                other.db.close()

    @unittest.skipUnless(os.environ.get("ZF_COORDINATOR_BROWSER") == "1", "opt-in Chromium journey")
    def test_actual_browser_keyboard_filters_drill_map_unknowns_and_denials(self) -> None:
        if self.backend != "sqlite":
            self.skipTest("Actual browser journey is owned by the SQLite application.")
        from playwright.sync_api import sync_playwright

        playwright = sync_playwright().start()
        self.addCleanup(playwright.stop)
        with patch.object(insights, "MAP_CAP", 1):
            browser = playwright.chromium.launch()
            self.addCleanup(browser.close)
            context = browser.new_context(reduced_motion="reduce")
            self.addCleanup(context.close)
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(self.base + "/app#/overview")
            page.get_by_label("Work email", exact=True).fill("pam@example.test")
            page.get_by_label("Password", exact=True).fill("synthetic-coordinator-only")
            page.get_by_role("button", name="Sign in", exact=True).click()
            page.get_by_role("link", name="Coordinator heatmap and lifecycle funnel").click()
            page.get_by_role("heading", name="Coordinator flow", exact=True).wait_for()
            page.wait_for_function(
                "() => document.querySelector('#co-as_of') || document.querySelector('main .err')"
            )
            self.assertEqual(
                page.locator("main .err").all_text_contents(),
                [""],
                page.locator("main").inner_text(),
            )
            page.get_by_label("Event cutoff (ISO date, time and timezone)").fill(AS_OF)
            page.get_by_role("button", name="Apply coordinator filters").focus()
            with page.expect_response(
                lambda response: (
                    "/api/coordinator?" in response.url and "as_of=2026-10-10" in response.url
                )
            ):
                page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.body.textContent.includes('5 current cases selected')"
            )
            page.wait_for_function(
                "() => document.body.textContent.includes('1 with unknown or invalid coordinates')"
            )
            self.assertIn("Approved priority is Unknown", page.locator("main").inner_text())
            self.assertIn("Lifecycle exclusions: Unknown", page.locator("main").inner_text())
            self.assertEqual(page.locator("#leaflet .map-cluster").count(), 1)
            cluster = page.locator("#leaflet .map-cluster").first
            cluster.focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(300)
            self.assertIn("selected records 5", page.locator("#workspace-status").inner_text())
            self.assertIn(
                "1 with unknown or invalid coordinates", page.locator("main").inner_text()
            )
            page.get_by_role("button", name="Show these as a list", exact=True).focus()
            page.keyboard.press("Enter")
            self.assertEqual(page.locator(":focus").get_attribute("id"), "coordinator-records")
            exit_link = page.get_by_role(
                "link", name="1 observed exits for Contact paused", exact=True
            )
            exit_link.focus()
            page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.body.textContent.includes("
                "'1 selected records; exits for Contact paused')"
            )
            self.assertIn("metric_stage=Contact%20paused", page.url)
            self.assertNotIn("&stage=", page.url)
            self.assertIn("Cohort denominator: 5", page.locator("main").inner_text())
            page.get_by_role("region", name="Selected records", exact=True).get_by_role(
                "link", name="ZF-1"
            ).focus()
            page.keyboard.press("Enter")
            page.get_by_role("heading", name="Pat Test", exact=True).wait_for()
            page.go_back()
            page.get_by_role("link", name="Show the full filtered population").click()
            page.wait_for_function(
                "() => document.body.textContent.includes('5 selected records; current.')"
            )
            page.get_by_label("Local authority", exact=True).select_option("Test")
            page.get_by_role("button", name="Apply coordinator filters").focus()
            page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.body.textContent.includes('4 current cases selected')"
            )
            report = page.evaluate(
                "async () => (await fetch('/api/coordinator?"
                "as_of=2026-10-10T12:00:00Z&view=all&area=Test')).json()"
            )
            listing = page.evaluate(
                "async () => (await fetch('/api/cases?view=all&area=Test')).json()"
            )
            self.assertEqual(report["map"]["total"], listing["total"])
            self.assertEqual(report["records"]["total"], 4)
            page.get_by_role("link", name="3 cases with unknown stage history", exact=True).click()
            page.wait_for_function(
                "() => document.body.textContent.includes('3 selected records; unknown history')"
            )
            for width in (320, 390, 1280):
                page.set_viewport_size(dict(width=width, height=900))
                self.assertFalse(
                    page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                )
            page.get_by_role("link", name="Show the full filtered population").click()
            page.wait_for_function(
                "() => document.body.textContent.includes('4 selected records; current.')"
            )
            page.get_by_label("Local authority", exact=True).select_option("Other")
            page.get_by_role("button", name="Apply coordinator filters").click()
            page.wait_for_function(
                "() => document.body.textContent.includes('1 current cases selected')"
            )
            page.get_by_label("Find by name, address, postcode or case ID").fill("NOT-A-CASE")
            page.get_by_role("button", name="Apply coordinator filters").click()
            page.wait_for_function(
                "() => document.body.textContent.includes('0 current cases selected')"
            )
            self.assertIn("No cases match this population", page.locator("main").inner_text())
            for actor in ("con", "rex"):
                denied = browser.new_context()
                try:
                    denied.request.post(
                        self.base + "/api/login",
                        data=dict(
                            email=f"{actor}@example.test", password="synthetic-coordinator-only"
                        ),
                    )
                    if actor == "rex":
                        with self.store.lock:
                            current = self.store.staff["rex@example.test"]
                            current["role"] = "Mystery"
                            self.store.db.execute(
                                "UPDATE staff SET body=? WHERE email=?",
                                (json.dumps(current), current["email"]),
                            )
                            self.store.save()
                    self.assertEqual(denied.request.get(self.base + self.query()).status, 403)
                finally:
                    denied.close()
            self.assertEqual(errors, [])


class JsonCoordinatorApi(CoordinatorApi):
    backend = "json"


@unittest.skipUnless(os.environ.get("ZF_COORDINATOR_MSSQL") == "1", "opt-in loopback MSSQL")
class MssqlCoordinatorApi(CoordinatorApi):
    backend = "mssql"
