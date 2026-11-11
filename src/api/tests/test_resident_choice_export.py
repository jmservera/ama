"""Resident-choice queue CSV: truthful page summary, fail-closed text, JSON errors (synthetic)."""

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
from unittest.mock import patch

from dataset import DATA
from zava_forward.core.store import Store

from zava_forward.api import resident_choice_export as export
from zava_forward.api.server import App, make_handler

HEADER = [
    "Home reference",
    "Measure choices (latest recorded version)",
    "Paused, withdrawn or retained human review",
    "Update commitment status",
    "Homes skipped before this page",
    "Page size limit",
    "Homes in this file",
    "Open homes in total",
]
ALLOWED = ("sam", "pam", "rex", "pso")
DENIED = ("bea", "quinn", "gina", "kim", "adm", "unk")
ROLES = {
    "rex": "Retrofit Coordinator",
    "pso": "Programme Support Officer",
    "bea": "Building Safety Liaison",
    "quinn": "Quality Inspector",
    "gina": "Grants and Evidence Officer",
    "adm": "Application Administrator",
    "unk": "Mystery Role",
}


def version(
    number: Any, status: Any, revision: Any = 2, design: Any = 3, **extra: Any
) -> dict[str, Any]:
    return dict(
        version=number, status=status, context_revision=revision, design_version=design, **extra
    )


def measure(name: Any, status: Any, versions: Any, review: Any = None) -> dict[str, Any]:
    return dict(measure=name, status=status, versions=versions, review=review, context=None)


def page(*items: Any, total: Any = None, limit: Any = 50, offset: Any = 0) -> dict[str, Any]:
    return dict(
        items=list(items), total=len(items) if total is None else total, limit=limit, offset=offset
    )


def home(cid: str, measures: Any, update: Any = None) -> dict[str, Any]:
    return dict(
        id=cid,
        address="9 Canary Lane",
        town="Canarytown",
        measure_decisions=measures,
        resident_update=update,
    )


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


class Serializer(unittest.TestCase):
    def one(self, item: Any) -> dict[str, str]:
        return rows(export.choice_queue_csv(page(item)))[0]

    def test_empty_page_is_the_exact_stable_header_only(self) -> None:
        text = export.choice_queue_csv(page(total=7, offset=500))
        self.assertEqual(text, ",".join(f'"{h}"' if "," in h else h for h in HEADER) + "\r\n")
        self.assertEqual(list(export.FIELDS), HEADER)

    def test_page_context_is_repeated_on_every_row(self) -> None:
        got = rows(
            export.choice_queue_csv(page(home("A", []), home("B", []), total=9, limit=2, offset=4))
        )
        for row in got:
            self.assertEqual([row[h] for h in HEADER[4:]], ["4", "2", "2", "9"])
        self.assertEqual([r["Home reference"] for r in got], ["A", "B"])

    def test_current_status_and_latest_version_stay_distinct_with_binding(self) -> None:
        row = self.one(
            home("A", [measure("Loft insulation", "Not recorded", [version(1, "Accepted", 1, 1)])])
        )
        self.assertEqual(
            row["Measure choices (latest recorded version)"],
            "Loft insulation: current Not recorded; "
            "latest recorded v1 Accepted (revision 1, design 1)",
        )
        self.assertEqual(row["Paused, withdrawn or retained human review"], "None recorded")

    def test_no_measures_and_no_commitment_are_explicit_absence_labels(self) -> None:
        row = self.one(home("A", []))
        self.assertEqual(
            row["Measure choices (latest recorded version)"], "No measure choices recorded"
        )
        self.assertEqual(row["Update commitment status"], "No commitment recorded")

    def test_paused_and_withdrawn_with_review_keep_version_and_review_meaning(self) -> None:
        review = dict(status="Needs human review", decision_version=1)
        paused = measure(
            "Heat pump", "Waiting", [version(1, "Paused"), version(2, "Waiting")], review
        )
        withdrawn = measure("Wall insulation", "Withdrawn", [version(1, "Withdrawn")], review)
        row = self.one(home("A", [paused, withdrawn]))
        self.assertEqual(
            row["Paused, withdrawn or retained human review"],
            "Heat pump: Paused (current answer Waiting) (v1, revision 2, design 3), "
            "needs human review before any restart; "
            "Wall insulation: Withdrawn (v1, revision 2, design 3), "
            "needs human review before any restart",
        )

    def test_current_stop_without_review_is_still_listed(self) -> None:
        row = self.one(home("A", [measure("Heat pump", "Paused", [version(1, "Paused")])]))
        self.assertEqual(
            row["Paused, withdrawn or retained human review"],
            "Heat pump: Paused (v1, revision 2, design 3)",
        )

    def test_declined_review_is_retained_after_a_later_waiting(self) -> None:
        review = dict(status="Needs human review", decision_version=1)
        row = self.one(
            home(
                "A",
                [
                    measure(
                        "Solar panels",
                        "Waiting",
                        [version(1, "Declined"), version(2, "Waiting")],
                        review,
                    )
                ],
            )
        )
        self.assertEqual(
            row["Paused, withdrawn or retained human review"],
            "Solar panels: Declined (current answer Waiting) (v1, revision 2, design 3), "
            "human review retained after a Declined answer",
        )

    def test_declined_without_review_is_not_listed_as_a_stop(self) -> None:
        row = self.one(home("A", [measure("Solar panels", "Declined", [version(1, "Declined")])]))
        self.assertEqual(row["Paused, withdrawn or retained human review"], "None recorded")

    def test_unrecognised_measure_names_are_withheld_never_echoed_or_renamed(self) -> None:
        for name in (
            "Cavity wall",
            "loft insulation",
            "Loft insulation ",
            "Heat pump (J. Smith)",
            None,
            7,
        ):
            row = self.one(home("A", [measure(name, "Accepted", [version(1, "Accepted")])]))
            text = " ".join(row.values())
            self.assertIn("Measure name withheld: current Accepted", text)
            for leaked in ("Cavity", "loft", "Smith", "Loft insulation "):
                self.assertNotIn(leaked, text)
        for name in ("Loft insulation", "Wall insulation", "Heat pump", "Solar panels", "General"):
            self.assertTrue(
                self.one(home("A", [measure(name, "Waiting", [])]))[
                    "Measure choices (latest recorded version)"
                ].startswith(name)
            )

    def test_missing_or_invalid_evidence_is_unknown_never_absence_or_not_recorded(self) -> None:
        bad = [
            measure("Heat pump", "Mystery", [version(1, "Accepted")]),
            measure("Heat pump", None, [version(1, "Accepted")]),
            measure("Heat pump", "Accepted", [version(1, "Mystery")]),
            measure("Heat pump", "Accepted", None),
            measure("Heat pump", "Accepted", ["x"]),
            measure("Heat pump", "Accepted", [version(1, "Accepted")], "review"),
            measure("Heat pump", "Accepted", [version(1, "Accepted")], dict(decision_version=1)),
        ]
        for m in bad:
            row = self.one(home("A", [m]))
            text = (
                row["Measure choices (latest recorded version)"]
                + " | "
                + row["Paused, withdrawn or retained human review"]
            )
            self.assertIn("Unknown", text, m)
            self.assertNotIn("Not recorded", text, m)
            self.assertNotEqual(
                row["Paused, withdrawn or retained human review"], "None recorded", m
            )
        broken_homes: tuple[Any, ...] = (None, "x", ["x"], {})
        for broken in broken_homes:
            row = self.one(home("A", broken))
            self.assertEqual(
                row["Measure choices (latest recorded version)"], "Unknown (evidence unavailable)"
            )
            self.assertEqual(
                row["Paused, withdrawn or retained human review"], "Unknown (evidence unavailable)"
            )
        row = self.one(
            home("A", [measure("Heat pump", "Accepted", [version("1", "Accepted", "2", None)])])
        )
        self.assertEqual(
            row["Measure choices (latest recorded version)"],
            "Heat pump: current Accepted; latest recorded version Unknown Accepted "
            "(revision Unknown, design Unknown)",
        )
        row = self.one(dict(id="A"))
        self.assertEqual(row["Update commitment status"], "Unknown")

    def test_review_pointing_at_a_missing_version_keeps_the_review_but_not_a_stop_claim(
        self,
    ) -> None:
        review = dict(status="Needs human review", decision_version=9)
        row = self.one(
            home("A", [measure("Heat pump", "Waiting", [version(1, "Waiting")], review)])
        )
        self.assertEqual(
            row["Paused, withdrawn or retained human review"],
            "Heat pump: Unknown (evidence unavailable), needs human review",
        )

    def test_unrecognised_review_status_is_unknown_never_none_recorded(self) -> None:
        for status in ("", "garbled", "needs human review", "Needs human review "):
            review = dict(status=status, decision_version=1)
            versions = [version(1, "Declined"), version(2, "Waiting")]
            row = self.one(home("A", [measure("Solar panels", "Waiting", versions, review)]))
            self.assertEqual(
                row["Paused, withdrawn or retained human review"],
                "Solar panels: Unknown (evidence unavailable)",
                status,
            )

    def test_known_review_states_and_explicit_none_keep_their_meaning(self) -> None:
        versions = [version(1, "Declined"), version(2, "Waiting")]
        label = "Paused, withdrawn or retained human review"
        row = self.one(home("A", [measure("Solar panels", "Waiting", versions, None)]))
        self.assertEqual(row[label], "None recorded")
        accepted = dict(status="Reviewed with supplied acceptance", decision_version=1)
        row = self.one(home("A", [measure("Solar panels", "Waiting", versions, accepted)]))
        self.assertEqual(row[label], "None recorded")
        retained = dict(status="Needs human review", decision_version=1)
        row = self.one(home("A", [measure("Solar panels", "Waiting", versions, retained)]))
        self.assertIn("human review retained after a Declined answer", row[label])

    def test_update_status_is_closed_vocabulary_and_detail_never_enters(self) -> None:
        update = dict(
            status="Proposed",
            purpose="CANARY-PURPOSE",
            owner="CANARY-OWNER",
            due_at="2031-01-01",
            safe_contact_ref="CANARY-ROUTE",
        )
        row = self.one(home("A", [], update))
        self.assertEqual(row["Update commitment status"], "Proposed")
        self.assertNotIn("CANARY", " ".join(row.values()))
        self.assertEqual(
            self.one(home("A", [], dict(status="=1+1")))["Update commitment status"], "Unknown"
        )
        self.assertEqual(self.one(home("A", [], "text"))["Update commitment status"], "Unknown")
        self.assertEqual(self.one(home("A", [], {}))["Update commitment status"], "Unknown")

    def test_cells_are_neutralised_and_quoted(self) -> None:
        for raw, expected in (
            ("=1+1", "'=1+1"),
            ("+SUM(A1)", "'+SUM(A1)"),
            ("-2", "'-2"),
            ("@cmd", "'@cmd"),
            ("\tTab", "'\tTab"),
            ('Zo\u00eb "q", c\nl2', 'Zo\u00eb "q", c\nl2'),
        ):
            got = rows(export.choice_queue_csv(page(home(raw, []))))
            self.assertEqual(got[0]["Home reference"], expected)
        self.assertEqual(self.one(dict(id=""))["Home reference"], "Unknown")
        self.assertEqual(self.one(dict(id=None))["Home reference"], "Unknown")

    def test_strict_fields_exclude_every_canary_value(self) -> None:
        canary = {
            key: f"CANARY-{key}"
            for key in (
                "note",
                "answered_by",
                "source",
                "representative_ref",
                "recorder_identity",
                "scope",
                "adjustment",
                "evidence",
                "retention",
                "household",
                "address",
                "phone",
            )
        }
        v = version(1, "Accepted", **canary)
        m = measure("Heat pump", "Accepted", [v], dict(status="Resolved", note="CANARY-review"))
        m["context"] = dict(scope="CANARY-context", revision=2, design_version=3)
        item = home(
            "A",
            [m],
            dict(
                status="Outstanding",
                purpose="CANARY-purpose",
                owner="CANARY-owner",
                owner_identity={"email": "CANARY-mail"},
                due_at="CANARY-due",
                safe_contact_ref="CANARY-safe",
                history=["CANARY-history"],
            ),
        )
        item["address"] = "CANARY-address"
        item["town"] = "CANARY-town"
        text = export.choice_queue_csv(page(item))
        self.assertNotIn("CANARY", text)
        self.assertEqual(rows(text)[0].keys(), set(HEADER) | set())
        self.assertNotIn("{", text)

    def test_malformed_page_raises_instead_of_writing_a_false_file(self) -> None:
        for bad in (
            dict(items=None, total=0, limit=1, offset=0),
            dict(items=["x"], total=1, limit=1, offset=0),
            page(home("A", []), total="1"),
            page(home("A", []), limit=True),
            page(home("A", []), offset=None),
        ):
            with self.assertRaises(TypeError):
                export.choice_queue_csv(bad)


class Http(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data: dict[str, Any] = copy.deepcopy(DATA)
        for code, role in ROLES.items():
            data["staff"].append(
                dict(
                    code=code.upper(),
                    name=f"Synthetic {code}",
                    email=f"{code}@example.test",
                    role=role,
                )
            )
        data["staff"].append(
            dict(
                code="CON-1",
                name="Kim",
                email="kim@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
        )
        path = Path(tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store: Any = Store(str(path))
        app = App(self.store, "synthetic-check")  # type: ignore[no-untyped-call]
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        self.base = f"http://127.0.0.1:{httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def fetch(self, path: str, who: str | None = None) -> tuple[int, Any, bytes]:
        headers = {}
        if who:
            if who not in self.cookies:
                body = json.dumps(
                    dict(email=f"{who}@example.test", password="synthetic-check")
                ).encode()
                with urllib.request.urlopen(
                    urllib.request.Request(self.base + "/api/login", body)
                ) as r:
                    self.cookies[who] = r.headers["Set-Cookie"].split(";")[0]
            headers["Cookie"] = self.cookies[who]
        try:
            with urllib.request.urlopen(
                urllib.request.Request(self.base + path, headers=headers)
            ) as r:
                return r.status, r.headers, r.read()
        except urllib.error.HTTPError as error:
            return error.code, error.headers, error.read()

    def ids(self, query: str = "") -> list[str]:
        return [
            r["Home reference"]
            for r in rows(self.fetch("/api/resident/choice-queue.csv" + query, "sam")[2].decode())
        ]

    def test_allowed_roles_get_identical_attachment_bodies_equal_to_the_serializer(self) -> None:
        expected = export.choice_queue_csv(
            self.store.resident_choice_queue(self.store.staff["sam@example.test"], 50, 0)
        )
        for who in ALLOWED:
            code, headers, body = self.fetch("/api/resident/choice-queue.csv", who)
            self.assertEqual(code, 200, who)
            self.assertEqual(headers["Content-Type"], "text/csv; charset=utf-8")
            self.assertEqual(
                headers["Content-Disposition"],
                'attachment; filename="resident-choice-queue-page.csv"',
            )
            self.assertEqual(body.decode(), expected, who)

    def test_denied_and_signed_out_get_json_without_attachment_or_csv(self) -> None:
        cases = [(None, 401)] + [(who, None) for who in DENIED]
        for who, want in cases:
            code, headers, body = self.fetch("/api/resident/choice-queue.csv", who)
            self.assertIn(code, (want,) if want else (403, 404), who)
            self.assertIsNone(headers["Content-Disposition"], who)
            self.assertEqual(headers["Content-Type"], "application/json", who)
            self.assertIn("error", json.loads(body))
            self.assertNotIn(b"ZF-", body)
            json_code = self.fetch("/api/resident/choice-queue", who)[0]
            self.assertEqual(code, json_code, who)

    def test_query_semantics_match_the_json_route_exactly(self) -> None:
        for query in (
            "",
            "?limit=2",
            "?limit=2&offset=1",
            "?limit=0",
            "?limit=1000",
            "?offset=-5",
            "?offset=99",
            "?limit=&limit=3",
            "?limit=2&limit=4",
            "?offset=&offset=2",
            "?unknown=x&limit=1",
        ):
            with self.subTest(query=query):
                body = json.loads(self.fetch("/api/resident/choice-queue" + query, "pam")[2])
                got = rows(self.fetch("/api/resident/choice-queue.csv" + query, "pam")[2].decode())
                self.assertEqual(
                    [r["Home reference"] for r in got], [i["id"] for i in body["items"]]
                )
                for r in got:
                    self.assertEqual(
                        [r[h] for h in HEADER[4:]],
                        [
                            str(body["offset"]),
                            str(body["limit"]),
                            str(len(body["items"])),
                            str(body["total"]),
                        ],
                    )
        for query in ("?limit=abc", "?offset=1.5", "?limit=%20", "?offset=x&offset=1"):
            with self.subTest(query=query):
                code, headers, body = self.fetch("/api/resident/choice-queue.csv" + query, "pam")
                self.assertEqual(code, 400)
                self.assertEqual(code, self.fetch("/api/resident/choice-queue" + query, "pam")[0])
                self.assertIsNone(headers["Content-Disposition"])
                self.assertEqual(headers["Content-Type"], "application/json")

    def test_order_offsets_defaults_and_closed_exclusion(self) -> None:
        self.assertEqual(self.ids(), ["ZF-1", "ZF-2", "ZF-3", "ZF-4", "ZF-5"])
        self.assertEqual(self.ids("?limit=2&offset=1"), ["ZF-2", "ZF-3"])
        self.assertEqual(self.ids("?offset=9"), [])
        self.store.cases["ZF-1"]["closed"] = True
        self.assertEqual(self.ids("?limit=2"), ["ZF-2", "ZF-3"])
        self.assertEqual(
            rows(self.fetch("/api/resident/choice-queue.csv?limit=2", "sam")[2].decode())[0][
                "Open homes in total"
            ],
            "4",
        )

    def test_empty_page_is_header_only_and_does_not_claim_no_open_homes(self) -> None:
        code, _, body = self.fetch("/api/resident/choice-queue.csv?offset=99", "sam")
        self.assertEqual(code, 200)
        self.assertEqual(rows(body.decode()), [])
        self.assertEqual(next(csv.reader(io.StringIO(body.decode()))), HEADER)
        self.assertEqual(len(body.decode().splitlines()), 1)

    def test_omitted_detail_leaves_files_count_below_the_page_size_while_total_counts_all(
        self,
    ) -> None:
        real = self.store.detail
        with patch.object(
            self.store,
            "detail",
            side_effect=lambda cid, user: None if cid == "ZF-2" else real(cid, user),
        ):
            got = rows(self.fetch("/api/resident/choice-queue.csv?limit=3", "sam")[2].decode())
        self.assertEqual([r["Home reference"] for r in got], ["ZF-1", "ZF-3"])
        self.assertEqual(
            {
                (r["Page size limit"], r["Homes in this file"], r["Open homes in total"])
                for r in got
            },
            {("3", "2", "5")},
        )

    def test_real_recorded_choice_is_summarised_with_its_binding(self) -> None:
        text = self.fetch("/api/resident/choice-queue.csv", "sam")[2].decode()
        self.assertIn("latest recorded v1 Accepted (revision 1, design 1)", text)

    def test_canary_values_in_the_projection_never_reach_the_file(self) -> None:
        real = self.store.detail

        def seeded(cid: str, user: Any) -> Any:
            d = real(cid, user)
            if d is not None:
                d["measure_decisions"] = [
                    measure(
                        "Heat pump",
                        "Accepted",
                        [
                            version(
                                1,
                                "Accepted",
                                note="CANARY-note",
                                answered_by="CANARY-by",
                                recorder_identity="CANARY-rec",
                                representative_ref="CANARY-rep",
                                scope="CANARY-scope",
                            )
                        ],
                        None,
                    )
                ]
                d["resident_update"] = dict(
                    status="Outstanding",
                    purpose="CANARY-purpose",
                    owner="CANARY-owner",
                    due_at="CANARY-due",
                    safe_contact_ref="CANARY-safe",
                )
            return d

        with patch.object(self.store, "detail", side_effect=seeded):
            code, _, body = self.fetch("/api/resident/choice-queue.csv", "sam")
        self.assertEqual(code, 200)
        text = body.decode()
        self.assertNotIn("CANARY", text)
        self.assertNotIn("Test Road", text)
        self.assertEqual(rows(text)[0]["Update commitment status"], "Outstanding")

    def test_unrecognised_review_status_in_the_projection_downloads_as_unknown(self) -> None:
        real = self.store.detail

        def seeded(cid: str, user: Any) -> Any:
            d = real(cid, user)
            if d is not None:
                versions = [version(1, "Declined"), version(2, "Waiting")]
                d["measure_decisions"] = [
                    measure(
                        "Solar panels",
                        "Waiting",
                        versions,
                        dict(status=status, decision_version=1),
                    )
                    for status in ("", "garbled")
                ]
            return d

        with patch.object(self.store, "detail", side_effect=seeded):
            code, _, body = self.fetch("/api/resident/choice-queue.csv", "sam")
        self.assertEqual(code, 200)
        label = "Paused, withdrawn or retained human review"
        for row in rows(body.decode()):
            self.assertEqual(
                row[label],
                "Solar panels: Unknown (evidence unavailable); "
                "Solar panels: Unknown (evidence unavailable)",
            )

    def test_loader_failure_is_json_without_attachment_or_header_only_success(self) -> None:
        with (
            patch.object(self.store, "resident_choice_queue", side_effect=OSError("SYN loader")),
            self.assertLogs("zava_forward.api.server", level="ERROR"),
        ):
            code, headers, body = self.fetch("/api/resident/choice-queue.csv", "sam")
        self.assertEqual(code, 500)
        self.assertIsNone(headers["Content-Disposition"])
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertNotIn(b"Home reference", body)

    def test_unexpected_page_shape_is_a_500_json_not_a_partial_csv(self) -> None:
        with (
            patch.object(
                self.store,
                "resident_choice_queue",
                return_value=dict(items=[], total="x", limit=1, offset=0),
            ),
            self.assertLogs("zava_forward.api.server", level="ERROR"),
        ):
            code, headers, body = self.fetch("/api/resident/choice-queue.csv", "sam")
        self.assertEqual(code, 500)
        self.assertIsNone(headers["Content-Disposition"])
        self.assertNotIn(b"Home reference", body)

    def test_download_changes_no_case_choice_update_or_audit_state(self) -> None:
        with self.store.lock:
            before = json.dumps(self.store.cases, sort_keys=True, default=str)
            audit = list(self.store.audit_entries())
        for who in ("sam", "pam", "quinn"):
            self.fetch("/api/resident/choice-queue.csv?limit=2", who)
        with self.store.lock:
            self.assertEqual(json.dumps(self.store.cases, sort_keys=True, default=str), before)
            self.assertEqual(list(self.store.audit_entries()), audit)

    def test_csv_route_is_not_in_the_shared_list_export_registry(self) -> None:
        from zava_forward.api.server import LIST_EXPORTS

        self.assertNotIn("/api/resident/choice-queue.csv", LIST_EXPORTS)


if __name__ == "__main__":
    unittest.main()
