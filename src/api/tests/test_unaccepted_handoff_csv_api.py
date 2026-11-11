"""Issue 1419: the CSV copy of unaccepted handoffs equals its JSON route (synthetic data)."""

import copy
import csv
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest import mock

from tests.test_mvp import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import EXPORT_KINDS, LIST_EXPORTS, App, make_handler

JSON_PATH = "/api/handoffs/unaccepted"
CSV_PATH = "/api/handoffs/unaccepted.csv"
AS_OF = "2026-10-01T12:00+00:00"
FIELDS = [
    "case_id",
    "status",
    "age_hours",
    "due_at",
    "chase_owner",
    "chase_owner_code",
    "proposed_receiver",
    "escalated",
    "needs_escalation",
    "reasons",
    "approved_limit_hours",
    "limit_note",
    "as_of",
]
NOT_SET = "Approved escalation time not set (OD-09)"
PRIVATE = (
    "PRIVATE-RESIDENT",
    "PRIVATE-ADDRESS",
    "PRIVATE-NOTE",
    "PRIVATE-NEXT",
    "PRIVATE-EVIDENCE",
)
ACTORS = (
    ("sam", "Sam Example", "RLO-01", "Resident Liaison Officer"),
    ("rae", "Rae Other", "RLO-02", "Resident Liaison Officer"),
    ("pam", "Pam Lead", "PM-01", "Retrofit Programme Manager"),
    ("pso", "Pia Support", "PSO-01", "Programme Support Officer"),
    ("rex", "Rex Coordinator", "RC-01", "Retrofit Coordinator"),
    ("kim", "Kim Builder", "CON-01", "Contractor"),
    ("adm", "Ada Admin", "ADM-01", "Application Administrator"),
    ("unk", "Una Unknown", "UNK-01", "Unrecognised Role"),
)


def cell(value: Any) -> str:
    """Independent expectation of the existing serializer rules for these 13 fields."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    text = str(value)
    return "'" + text if text[:1] in "=+-@\t\r" else text


class UnacceptedHandoffCsv(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"] = [
            dict(code=code, name=name, email=f"{key}@example.test", role=role)
            for key, name, code, role in ACTORS
        ]
        data["staff"][5]["contractor"] = "Test Ltd"
        path = Path(tmp.name) / "seed.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        clock = mock.patch("zava_forward.core.workflows._now", return_value=AS_OF)
        clock.start()
        self.addCleanup(clock.stop)
        self.set_handoff(
            "ZF-1", "Offered", "2026-10-01T06:00+00:00", "2026-10-01T10:00+00:00", "sam", "rae"
        )
        self.set_handoff("ZF-2", "Received", "2026-09-30T12:00+00:00", None, "sam", "rae")
        self.set_handoff(
            "ZF-3", "Escalated", "2026-10-01T10:30+00:00", "2026-10-01T09:00+00:00", "sam", "pam"
        )
        case = self.store.cases["ZF-1"]
        case["resident"]["name"] = "PRIVATE-RESIDENT"
        case["home"]["address"] = "PRIVATE-ADDRESS"
        case["handoff"].update(
            note="PRIVATE-NOTE", next_action="PRIVATE-NEXT", evidence="PRIVATE-EVIDENCE"
        )
        app = App(self.store, "synthetic-test-password")  # type: ignore[no-untyped-call]
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        self.base = f"http://127.0.0.1:{httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def set_handoff(
        self, case_id: str, state: str, offered: str, due: str | None, frm: str, to: str
    ) -> None:
        names = {key: (name, code, role) for key, name, code, role in ACTORS}
        self.store.cases[case_id]["handoff"] = dict(
            state=state,
            offered_at=offered,
            due_at=due,
            from_name=names[frm][0],
            from_code=names[frm][1],
            to_name=names[to][0],
            to_code=names[to][1],
            to_role=names[to][2],
        )

    def request(
        self, actor: str | None, path: str, method: str | None = None, body: bytes | None = None
    ) -> tuple[int, str, Any]:
        headers = {}
        if actor:
            if actor not in self.cookies:
                login = urllib.request.Request(
                    self.base + "/api/login",
                    json.dumps(
                        dict(email=f"{actor}@example.test", password="synthetic-test-password")
                    ).encode(),
                )
                with urllib.request.urlopen(login) as response:
                    self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
            headers["Cookie"] = self.cookies[actor]
        request = urllib.request.Request(self.base + path, body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read().decode(), response.headers
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode(), error.headers

    def both(
        self, actor: str | None, query: str = ""
    ) -> tuple[tuple[int, str, Any], tuple[int, str, Any]]:
        return self.request(actor, JSON_PATH + query), self.request(actor, CSV_PATH + query)

    def assert_parity(self, actor: str, query: str = "") -> list[list[str]]:
        (jcode, jtext, _), (ccode, ctext, headers) = self.both(actor, query)
        self.assertEqual((jcode, ccode), (200, 200), (query, jtext, ctext))
        rows = json.loads(jtext)
        decoded = list(csv.reader(io.StringIO(ctext, newline="")))
        self.assertEqual(decoded[0], FIELDS)
        self.assertEqual(decoded[1:], [[cell(r[k]) for k in FIELDS] for r in rows])
        self.assertEqual([list(r) for r in rows], [FIELDS] * len(rows))
        self.assertEqual(headers["Content-Type"], "text/csv; charset=utf-8")
        self.assertEqual(
            headers["Content-Disposition"], 'attachment; filename="unaccepted-handoffs.csv"'
        )
        return decoded[1:]

    def test_route_uses_shared_branch_not_the_generic_registry(self) -> None:
        self.assertEqual(EXPORT_KINDS[CSV_PATH], "handoffs")
        self.assertNotIn(CSV_PATH, LIST_EXPORTS)

    def test_literal_rows_order_and_null_limit_semantics(self) -> None:
        rows = self.assert_parity("sam")
        self.assertEqual([r[0] for r in rows], ["ZF-2", "ZF-1", "ZF-3"])
        self.assertEqual(
            rows[1],
            ["ZF-1", "Sent", "6.0", "2026-10-01T10:00+00:00", "Sam Example", "RLO-01", "Rae Other"]
            + ["No", "Yes", '["Handoff due time has passed"]', "", NOT_SET, AS_OF],
        )
        self.assertEqual(
            rows[0][3:],
            ["", "Sam Example", "RLO-01", "Rae Other", "No", "No", "[]", "", NOT_SET, AS_OF],
        )
        self.assertEqual(rows[2][1], "Escalated")
        self.assertEqual(rows[2][7:9], ["Yes", "No"])

    def test_due_age_and_both_reasons_with_a_supplied_limit(self) -> None:
        rows = {r[0]: r for r in self.assert_parity("sam", "?max_age_hours=5")}
        self.assertEqual(
            rows["ZF-1"][9],
            '["Handoff due time has passed","Unaccepted for more than the approved 5.0 hours"]',
        )
        self.assertEqual(rows["ZF-2"][9], '["Unaccepted for more than the approved 5.0 hours"]')
        self.assertEqual(rows["ZF-3"][9], '["Handoff due time has passed"]')
        self.assertEqual(rows["ZF-2"][10], "5.0")

    def test_only_unaccepted_states_are_listed(self) -> None:
        for state in ("Accepted", "Completed", "Declined", "Withdrawn"):
            with self.subTest(state=state):
                self.set_handoff("ZF-4", state, "2026-10-01T01:00+00:00", None, "sam", "rae")
                self.assertEqual(
                    sorted(r[0] for r in self.assert_parity("sam")), ["ZF-1", "ZF-2", "ZF-3"]
                )
        self.store.cases["ZF-4"].pop("handoff")
        self.assertEqual(self.request("sam", CSV_PATH)[1].count("\r\n"), 4)

    def test_visibility_follows_json_for_each_allowed_role(self) -> None:
        expected = {
            "sam": ["ZF-1", "ZF-2", "ZF-3"],
            "rae": ["ZF-1", "ZF-2"],
            "pam": ["ZF-1", "ZF-2", "ZF-3"],
            "pso": ["ZF-1", "ZF-2", "ZF-3"],
            "rex": [],
        }
        for actor, ids in expected.items():
            with self.subTest(actor=actor):
                if ids:
                    self.assertEqual(sorted(r[0] for r in self.assert_parity(actor)), ids)
                else:
                    self.assertEqual(self.request(actor, JSON_PATH)[:2], (200, "[]"))
                    self.assertEqual(self.request(actor, CSV_PATH)[:2], (200, "\r\n"))

    def test_empty_result_keeps_the_serializer_blank_record_without_column_names(self) -> None:
        for case in self.store.cases.values():
            case.pop("handoff", None)
        code, text, headers = self.request("sam", CSV_PATH)
        self.assertEqual((code, text), (200, "\r\n"))
        self.assertEqual(headers["Content-Type"], "text/csv; charset=utf-8")
        self.assertEqual(self.request("sam", JSON_PATH)[:2], (200, "[]"))

    def test_query_matrix_matches_json_status_and_error_body(self) -> None:
        ok = [
            "",
            "?max_age_hours=",
            "?max_age_hours=&max_age_hours=5",
            "?max_age_hours=5&max_age_hours=abc",
            "?max_age_hours=0.5",
            "?max_age_hours=999999",
            "?other=1",
            "?as_of=2000-01-01T00:00%2B00:00",
        ]
        for query in ok:
            with self.subTest(query=query):
                self.assert_parity("sam", query)
        blank_first = self.assert_parity("sam", "?max_age_hours=&max_age_hours=5")
        self.assertEqual(blank_first, self.assert_parity("sam"))
        self.assertEqual(self.assert_parity("sam", "?as_of=2000-01-01T00:00%2B00:00")[0][-1], AS_OF)
        bad = [
            "abc",
            "0",
            "-3",
            "nan",
            "NaN",
            "inf",
            "-inf",
            "Infinity",
            "1000000",
            "1e6",
            "5x",
            "%20",
        ]
        for value in bad:
            with self.subTest(value=value):
                (jcode, jtext, _), (ccode, ctext, _) = self.both("sam", f"?max_age_hours={value}")
                self.assertEqual((jcode, ccode), (400, 400))
                self.assertEqual(json.loads(ctext), json.loads(jtext))
                self.assertEqual(
                    json.loads(ctext),
                    {"error": "max_age_hours must be a positive number of hours."},
                )
        (jcode, _, _), (ccode, _, _) = self.both("sam", "?max_age_hours=nan&max_age_hours=5")
        self.assertEqual((jcode, ccode), (400, 400))

    def test_denied_and_signed_out_before_query_parse(self) -> None:
        for query in ("", "?max_age_hours=abc"):
            (jcode, _, _), (ccode, ctext, _) = self.both(None, query)
            self.assertEqual((jcode, ccode), (401, 401), query)
            for actor in ("kim", "adm", "unk"):
                with self.subTest(actor=actor, query=query):
                    (jcode, _, _), (ccode, ctext, _) = self.both(actor, query)
                    self.assertEqual((jcode, ccode), (403, 403))
                    self.assertEqual(
                        json.loads(ctext), {"error": "Your role does not include this."}
                    )

    def test_method_behaviour_and_near_miss_paths_are_unchanged(self) -> None:
        for method, body in (("POST", b"{}"), ("HEAD", None), ("PUT", b"{}"), ("DELETE", None)):
            with self.subTest(method=method):
                j = self.request("sam", JSON_PATH, method, body)
                c = self.request("sam", CSV_PATH, method, body)
                self.assertEqual(c[0], j[0])
        self.assertEqual(self.request("sam", CSV_PATH, "HEAD")[0], 200)
        self.assertEqual(self.request("sam", CSV_PATH, "POST", b"{}")[0], 404)
        for path in (CSV_PATH + "/", CSV_PATH.upper(), CSV_PATH + "x", JSON_PATH + ".json"):
            with self.subTest(path=path):
                code, _, headers = self.request("sam", path)
                self.assertIn(code, (403, 404))
                self.assertNotEqual(headers["Content-Type"], "text/csv; charset=utf-8")

    def test_pending_list_and_its_download_are_unchanged(self) -> None:
        code, text, headers = self.request("sam", "/api/handoffs.csv")
        self.assertEqual(code, 200)
        self.assertEqual(headers["Content-Disposition"], 'attachment; filename="handoffs.csv"')
        self.assertNotEqual(next(csv.reader(io.StringIO(text))), FIELDS)
        self.assertIn("resident", text.splitlines()[0])
        self.assertEqual(self.request("sam", "/api/handoffs")[0], 200)

    def test_only_the_thirteen_fields_and_no_private_values(self) -> None:
        text = self.request("sam", CSV_PATH)[1]
        for marker in PRIVATE:
            self.assertNotIn(marker, text)
        self.assertEqual(next(csv.reader(io.StringIO(text))), FIELDS)
        for row in csv.reader(io.StringIO(text, newline="")):
            self.assertEqual(len(row), 13)

    def test_formula_quote_comma_and_newline_cells_round_trip(self) -> None:
        self.store.cases["ZF-3"]["handoff"].update(
            from_name='=HYPERLINK("x")', to_name='Ann, "Q"\nline'
        )
        rows = {r[0]: r for r in self.assert_parity("sam")}
        self.assertEqual(rows["ZF-3"][4], '\'=HYPERLINK("x")')
        self.assertEqual(rows["ZF-3"][6], 'Ann, "Q"\nline')

    def test_reads_never_change_stored_state(self) -> None:
        before = copy.deepcopy(self.store.cases)
        for actor, query in (
            ("sam", ""),
            ("rae", "?max_age_hours=5"),
            ("kim", ""),
            ("sam", "?max_age_hours=abc"),
            (None, ""),
        ):
            self.both(actor, query)
        self.request("sam", CSV_PATH, "HEAD")
        self.request("sam", CSV_PATH, "POST", b"{}")
        self.assertEqual(self.store.cases, before)


if __name__ == "__main__":
    unittest.main()
