"""Issue 80 criterion 2: every workbench list offers a read-only CSV copy or says why not."""

import copy
import csv
import io
import json
import re
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from dataset import DATA
from zava_forward.core.lawstore import LawStore
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api import server
from zava_forward.api.server import App, make_handler
from zava_forward.api.timecapture import ACTIVITIES, NOTICE_VERSION, TimeCapture

WEB = Path(server.__file__).parent / "web"

# Every list the workbench reads: its JSON endpoint, the CSV copy and the screen that links it.
EXPORTED = {
    "/api/cases": ("/api/cases.csv", "app.js"),
    "/api/closed-cases": ("/api/closed-cases.csv", "progress.js"),
    "/api/handoffs": ("/api/handoffs.csv", "app.js"),
    "/api/handoffs/unaccepted": ("/api/handoffs/unaccepted.csv", "app.js"),
    "/api/visits": ("/api/visits.csv", "app.js"),
    "/api/funding": ("/api/funding.csv", "app.js"),
    "/api/packages": ("/api/packages.csv", "ops.js"),
    "/api/workorders": ("/api/workorders.csv", "ops.js"),
    "/api/checklists": ("/api/checklists.csv", "ops.js"),
    "/api/finance": ("/api/finance.csv", "panels.js"),
    "/api/asset/stock-queue": ("/api/asset/stock-queue.csv", "role-screens.js"),
    "/api/resident/choice-queue": ("/api/resident/choice-queue.csv", "role-screens.js"),
    "/api/form-schemas": ("/api/form-schemas.csv", "role-screens.js"),
    "/api/time/mine": ("/api/time/mine.csv", "timecapture.js"),
    "/api/time/report": ("/api/time/report.csv", "timecapture.js"),
    "/api/law/sources": ("/api/law/sources.csv", "law.js"),
    "/api/assistants/proposals": ("/api/assistants/proposals.csv", "assistants.js"),
    "/api/aftercare/concerns": ("/api/aftercare/concerns.csv", "aftercare.js"),
}
# The exception register builds its summary file in the browser from the rows it shows.
BROWSER_EXPORT = {"/api/exceptions": ("exception-register-visible-summary.csv", "role-screens.js")}
# Endpoints the screens read that are not row lists, or that must not leave the application.
EXEMPT = {
    "/api/ai/priority": "One recommendation waiting for a human decision, not a list of records.",
    "/api/facets": "Filter choices for the case queue; the queue itself exports.",
    "/api/stats": "Totals only; the case queue exports its rows.",
    "/api/coordinator": "A map and totals over the case queue, which exports its rows.",
    "/api/ai/report": "Totals about assistant use, no rows.",
    "/api/finance/exposure": "Totals over the finance queue, which exports its items.",
    "/api/assistants": "The list of assistants a role may use, not case records.",
    "/api/assistants/simulation/quality": "Quality totals for the practice run.",
    "/api/chat/status": "Chat availability only.",
    "/api/chat/skills": "Chat helper names only.",
    "/api/chat/threads": "Conversation content is never exported (RULE-026).",
    "/api/chat/unstored-ask": "Conversation content is never exported (RULE-026).",
    "/api/chat/regulatory/inbox": "Conversation content is never exported (RULE-026).",
    "/api/chat/regulatory/status": "Chat availability only.",
    "/api/chat/regulatory/threads": "Conversation content is never exported (RULE-026).",
    "/api/chat/regulatory/usage": "Usage totals only.",
    "/api/law/alerts": "Rule alerts for one open case, shown inside the case chat.",
    "/api/time/status": "A checklist of settings, not a list of records.",
    "/api/briefing": "A written daily summary, not a list of records.",
    "/api/law/search": "Results for a question the person typed; the sources list exports.",
    "/api/aftercare/evaluator": "Totals with their denominators; the concerns list exports.",
    "/api/aftercare/form": "Form choices, not records.",
    "/api/ai/priority/": "Decision on one recommendation.",
    "/api/ai/review/": "Decision on one recommendation.",
    "/api/assistants/": "One assistant action.",
    "/api/assistants/proposals/": "One proposal and its review; the proposals list exports.",
    "/api/assistants/simulation/quality/": "Quality totals for the practice run.",
    "/api/buildings/": "One building view.",
    "/api/cases/": "One case; the case queue exports its rows.",
    "/api/chat/regulatory/threads/": "Conversation content is never exported (RULE-026).",
    "/api/chat/threads/": "Conversation content is never exported (RULE-026).",
    "/api/law/provisions/": "The text of one provision, read on screen.",
    "/api/law/sources/": "The provisions of one source; the sources list exports.",
    "/api/packages/": "One package action; the packages list exports.",
    "/api/workorders/": "One work order action; the work orders list exports.",
    "/api/me": "The signed-in person.",
    "/api/login": "Sign in.",
    "/api/logout": "Sign out.",
    "/api/import-check": "Preview of a file the person chose; it changes nothing.",
}
NEW = (
    "/api/time/mine",
    "/api/time/report",
    "/api/law/sources",
    "/api/assistants/proposals",
    "/api/aftercare/concerns",
)
READ_ONLY_NOTE = "read-only copy"
ENDPOINT = re.compile(r"""\b(?:api|get|fetch)\(\s*[`"'](/api/[A-Za-z0-9/_.\-]*)""")
AFTERCARE_PATH = re.compile(r"""AFTERCARE_API\}/([a-z]+)|\bread\("([a-z]+)"\)""")


def screen_endpoints() -> set[str]:
    found: set[str] = set()
    for js in WEB.glob("*.js"):
        text = js.read_text()
        found.update(ENDPOINT.findall(text))
        found.update("/api/aftercare/" + (m[0] or m[1]) for m in AFTERCARE_PATH.findall(text))
    return found


class InventoryIsComplete(unittest.TestCase):
    def test_every_list_the_screens_read_is_exported_or_explained(self) -> None:
        known = set(EXPORTED) | set(BROWSER_EXPORT) | set(EXEMPT)
        self.assertEqual(sorted(screen_endpoints() - known), [])

    def test_every_exempt_entry_gives_a_plain_reason(self) -> None:
        for path, reason in EXEMPT.items():
            self.assertTrue(reason.endswith("."), path)
            self.assertNotRegex(reason, r"\b(gate|hold|provenance|trace|snapshot|envelope)s?\b")

    def test_every_csv_copy_is_a_get_route_and_has_a_download_link_on_its_screen(self) -> None:
        source = Path(server.__file__).read_text()
        for csv_path, screen in EXPORTED.values():
            with self.subTest(path=csv_path):
                self.assertIn(csv_path.removesuffix(".csv").rsplit("/", 1)[-1], source)
                js = (WEB / screen).read_text()
                stem = csv_path.rsplit("/", 1)[-1]
                self.assertIn(stem, js)
        for _, (name, screen) in BROWSER_EXPORT.items():
            self.assertIn(name, (WEB / screen).read_text())

    def test_new_download_links_say_the_file_is_a_read_only_copy(self) -> None:
        for csv_path, screen in (EXPORTED[p] for p in EXPORTED if p in NEW):
            js = (WEB / screen).read_text()
            link = js[js.index(csv_path.rsplit("/", 1)[-1]) :][:600]
            self.assertIn(READ_ONLY_NOTE, link, csv_path)

    def test_no_download_link_offers_a_write_back_route(self) -> None:
        write_back = re.compile(r"(?i)\bmethod\b|upload|\bPOST\b")
        self.assertTrue(write_back.search('href: "/api/x.csv", method: "POST"'))
        links = 0
        for js in WEB.glob("*.js"):
            for line in js.read_text().splitlines():
                if ".csv" in line and "href" in line and "/api/" in line:
                    links += 1
                    self.assertIsNone(write_back.search(line), f"{js.name}: {line.strip()}")
        self.assertGreaterEqual(links, len(NEW))


class ExportRowContracts(unittest.TestCase):
    def test_concern_row_keeps_tracking_fields_and_drops_the_residents_words(self) -> None:
        item = {
            "id": "C-1",
            "home_ref": "H-1",
            "kind": "damp",
            "raised_by": "resident",
            "route": "repairs",
            "channel": "phone",
            "recorded_by": "Sam",
            "next_update": "2026-12-01",
            "unresolved": True,
            "overdue": False,
            "owner": {"label": "Owner", "status": "x"},
            "statement": "CANARY-STATEMENT",
            "history": ["CANARY-HISTORY"],
            "sensor_context": {"x": "CANARY-SENSOR"},
        }
        row = server.concern_export_row(item)  # type: ignore[no-untyped-call]
        self.assertNotIn("CANARY", json.dumps(row))
        self.assertEqual(row["owner"], "Owner")
        self.assertEqual(
            list(row),
            [
                "id",
                "home_ref",
                "kind",
                "raised_by",
                "route",
                "channel",
                "recorded_by",
                "next_update",
                "unresolved",
                "overdue",
                "owner",
            ],
        )
        self.assertNotIn("statement", row)

    def test_proposal_export_follows_every_page_of_the_scope(self) -> None:
        pages = {"": ("a", "b"), "b": ("c",)}
        calls: list[str] = []

        def read_page(after: str) -> dict[str, object]:
            calls.append(after)
            ids = pages[after]
            return {
                "proposals": [{"id": i} for i in ids],
                "next_after": ids[-1] if after == "" else None,
            }

        rows = server.all_proposals(read_page)  # type: ignore[no-untyped-call]
        self.assertEqual([r["id"] for r in rows], ["a", "b", "c"])
        self.assertEqual(calls, ["", "b"])
        with self.assertRaises(ValueError):
            server.all_proposals(lambda after: {"proposals": [], "next_after": "x"}, max_pages=3)  # type: ignore[no-untyped-call]

    def test_law_rows_list_sources_then_topics_with_no_source(self) -> None:
        rows = server.law_source_rows(  # type: ignore[no-untyped-call]
            {
                "sources": [
                    {
                        "title": "Act",
                        "status": "current",
                        "completeness": "full",
                        "effective": "2025-01-01",
                        "retrieved": "2026-01-01",
                        "version": 1,
                        "caveats": [],
                        "review_status": "reviewed",
                        "reviewed": "2026-01-02",
                        "authority_type": "legislation",
                        "official_url": "https://www.legislation.gov.uk/x",
                    },
                    {
                        "title": "Old Act",
                        "status": "historical",
                        "completeness": "full",
                        "effective": "2020-01-01",
                        "retrieved": "2026-01-01",
                        "version": 2,
                        "caveats": ["Historical source."],
                        "review_status": "pending",
                    },
                ],
                "gaps": [{"topic": "Topic", "answer": "No source is held.", "reason": "Not yet."}],
            }
        )
        self.assertEqual(
            [r["kind"] for r in rows], ["Source held", "Source held", "No source held"]
        )
        self.assertEqual(
            [
                rows[0][k]
                for k in (
                    "review_status",
                    "reviewed",
                    "authority_type",
                    "official_url",
                    "supersession",
                )
            ],
            [
                "reviewed",
                "2026-01-02",
                "legislation",
                "https://www.legislation.gov.uk/x",
                "Not superseded",
            ],
        )
        self.assertEqual(
            rows[1]["supersession"], "Superseded or historical, not the current authority"
        )
        self.assertIsNone(rows[1]["official_url"])

    def test_proposal_row_carries_source_freshness_and_reviewer_decision_without_payloads(
        self,
    ) -> None:
        item = {
            "id": "P-1",
            "case_id": "ZF-1",
            "capability": "summary",
            "display_state": "stale",
            "state": "accepted",
            "stale": True,
            "epoch_current": True,
            "relied_on": False,
            "source_signature": "sig",
            "verification": {
                "by": "a@x",
                "signature": "sig",
                "note": "CANARY-NOTE",
                "at": "2026-02-01",
            },
            "review": {"action": "accept", "by": "a@x", "note": "CANARY-NOTE", "at": "2026-02-02"},
            "output": {"text": "CANARY-OUTPUT"},
            "snapshot": {"x": "CANARY-SNAPSHOT"},
        }
        row = server.proposal_export_row(item)  # type: ignore[no-untyped-call]
        self.assertNotIn("CANARY", json.dumps(row))
        self.assertNotIn("a@x", json.dumps(row))
        self.assertEqual(row["source_state"], "Source changed since drafted")
        self.assertTrue(row["source_verified"])
        self.assertEqual((row["review_decision"], row["reviewed_at"]), ("accept", "2026-02-02"))
        bare = server.proposal_export_row({"id": "P-2", "stale": False, "source_signature": "s"})  # type: ignore[no-untyped-call]
        self.assertFalse(bare["source_verified"])
        self.assertEqual(bare["source_state"], "Source unchanged")
        self.assertIsNone(bare["review_decision"])

    def test_every_download_link_on_a_screen_points_at_a_listed_copy(self) -> None:
        listed = {csv_path for csv_path, _ in EXPORTED.values()}
        href = re.compile(r"""href: [`"](/api/[a-z/\-]+\.csv)""")
        for js in WEB.glob("*.js"):
            for path in href.findall(js.read_text()):
                self.assertIn(path, listed, js.name)


class ExportsLeaveStateUnchanged(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        folder = Path(tmp.name)
        data = copy.deepcopy(DATA)
        data["staff"].append(
            dict(
                code="CON-1",
                name="Kim",
                email="kim@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
        )
        data["staff"].append(
            dict(
                code="MGR-1", name="Mo", email="mo@example.test", role="Retrofit Programme Manager"
            )
        )
        seed = folder / "seed.json"
        seed.write_text(json.dumps(data))
        self.store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        env = dict(
            ZF_TIME_CAPTURE="on",
            DPIA_APPROVED="D1",
            ZF_TIME_CONSULTATION="C1",
            ZF_TIME_NOTICE_APPROVED="N1",
            ZF_TIME_NOTICE_VERSION=NOTICE_VERSION,
        )
        timed: Any = TimeCapture(self.store, env, str(folder / "time.sqlite"))  # type: ignore[no-untyped-call]
        self.time = timed
        self.time.request_enable(
            dict(code="A", email="a@example.test", role="Retrofit Programme Manager")
        )
        self.time.activate(dict(code="B", email="b@example.test", role="Programme Support Officer"))
        sam = data["staff"][0]
        self.time.acknowledge(sam)
        self.time.record(sam, "=1+1", 5, ACTIVITIES[0])
        self.law = LawStore(str(folder / "law.sqlite"), folder / "blobs")
        self.addCleanup(self.law.sql.close) if hasattr(self.law.sql, "close") else None
        app = App(self.store, "synthetic-check", timecap=self.time, law=self.law)  # type: ignore[no-untyped-call]
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        self.base = f"http://127.0.0.1:{httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}
        self.sam = data["staff"][0]["email"].split("@")[0]

    def call(
        self, actor: str, path: str, body: dict[str, str] | None = None
    ) -> tuple[int, str, dict[str, str]]:
        if actor not in self.cookies:
            login = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-check")
                ).encode(),
            )
            with urllib.request.urlopen(login) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            {"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read().decode(), dict(response.headers)
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode(), dict(error.headers)

    def stored_state(self) -> tuple[list[str], list[object]]:
        law_rows = self.law.sql.all("SELECT * FROM reg_source")
        return list(self.store.db.iterdump()), [tuple(r) for r in law_rows]

    def test_each_list_copy_downloads_as_csv_and_changes_nothing(self) -> None:
        paths = [csv_path for csv_path, _ in EXPORTED.values()]
        before = self.stored_state()
        for path in paths:
            for actor in ("sam", "pam", "mo"):
                code, text, headers = self.call(actor, path)
                if code != 200:
                    continue
                with self.subTest(path=path, actor=actor):
                    self.assertTrue(headers["Content-Type"].startswith("text/csv"))
                    self.assertIn("attachment", headers["Content-Disposition"])
                    list(csv.reader(io.StringIO(text)))
        served = {p for p in paths if any(self.call(a, p)[0] == 200 for a in ("sam", "pam", "mo"))}
        self.assertEqual(sorted(set(paths) - served), [])
        self.assertEqual(self.stored_state(), before)

    def test_time_entries_neutralise_formula_text_and_report_has_no_people(self) -> None:
        code, text, _ = self.call(self.sam, "/api/time/mine.csv")
        self.assertEqual(code, 200)
        self.assertNotIn(",=1+1", text)
        self.assertIn("'=1+1", text)
        code, text, _ = self.call("mo", "/api/time/report.csv")
        self.assertEqual(code, 200)
        self.assertEqual(text.strip(), "")  # one person only: below the minimum group, so hidden
        self.assertNotIn("example.test", text)
        self.assertEqual(self.call(self.sam, "/api/time/report.csv")[0], 403)

    def test_contractors_and_signed_out_callers_get_no_copy_of_any_list(self) -> None:
        for csv_path, _ in EXPORTED.values():
            with self.subTest(path=csv_path):
                self.assertEqual(self.call("kim", csv_path)[0], 403)
                with self.assertRaises(urllib.error.HTTPError) as refused:
                    urllib.request.urlopen(self.base + csv_path)
                self.assertEqual(refused.exception.code, 401)

    def test_a_copy_sent_back_for_import_is_only_previewed(self) -> None:
        _, copy_of_cases, _ = self.call("sam", "/api/cases.csv?view=all")
        before = self.stored_state()
        code, body, _ = self.call("sam", "/api/import-check", {"text": copy_of_cases})
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(body)["message"], "Your file has not been changed.")
        self.assertEqual(self.stored_state(), before)

    def test_no_route_writes_when_a_copy_path_is_posted(self) -> None:
        before = self.stored_state()
        for csv_path, _ in EXPORTED.values():
            with self.subTest(path=csv_path):
                self.assertNotEqual(self.call("sam", csv_path, {"text": "x"})[0], 200)
        self.assertEqual(self.stored_state(), before)


if __name__ == "__main__":
    unittest.main()
