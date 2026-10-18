"""Actual local HTTP exercise of constructed governance claims, never live acceptance."""

import copy
import importlib
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from zava_forward.core.governance import GovernanceCommittedError

from zava_forward.api.server import App, make_handler

fixtures = importlib.import_module("test_governance")


class GovernanceEvidenceApi(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture: Any = fixtures.SqlEvidenceRegister()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store: Any = self.fixture.store
        self.app: Any = App(self.store, "constructed-126-only")
        self.http = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.http.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.http.shutdown()
        self.http.server_close()
        self.thread.join(timeout=5)

    def call(self, path: str, actor: str = "pm-1", body: object = None) -> tuple[int, Any]:
        if actor and actor not in self.cookies:
            req = Request(
                self.base + "/api/login",
                json.dumps(
                    {"email": f"{actor}@example.test", "password": "constructed-126-only"}
                ).encode(),
            )
            with urlopen(req, timeout=10) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies.get(actor, ""), "Content-Type": "application/json"},
        )
        try:
            with urlopen(req, timeout=10) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_http_inventory_append_exact_context_and_replay(self) -> None:
        self.assertEqual(self.call("/api/governance", "")[0], 401)
        status, view = self.call("/api/governance")
        self.assertEqual(status, 200)
        self.assertEqual(len(view["rai_evidence"]["findings"]), 22)
        self.assertIsNone(view["rai_evidence"]["current_assessment"])
        status, record = self.call("/api/governance/evidence-record", body=fixtures.claim())
        self.assertEqual(status, 200, record)
        self.assertEqual(record["recorded_by"]["email"], "pm-1@example.test")
        query = urlencode({"assessment": json.dumps(fixtures.ASSESSMENT)})
        status, view = self.call("/api/governance?" + query)
        self.assertEqual(status, 200)
        self.assertEqual(view["rai_evidence"]["current_disposition_count"], 1)
        self.assertEqual(view["rai_evidence"]["findings"][2]["claims"], [record])
        self.assertEqual(
            self.call("/api/governance/evidence-record", body=fixtures.claim())[1], record
        )
        changed = dict(fixtures.ASSESSMENT, source_commit="f" * 40)
        query = urlencode({"assessment": json.dumps(changed)})
        self.assertEqual(
            self.call("/api/governance?" + query)[1]["rai_evidence"]["current_disposition_count"],
            0,
        )
        self.assertEqual(
            self.call(
                "/api/governance/evidence-record",
                body=fixtures.claim(event_ref="different", expected_revision=0),
            )[0],
            409,
        )
        for path in ("/api/governance/accept", "/api/governance/close"):
            self.assertEqual(self.call(path, body={})[0], 404)

    def test_http_role_denial_and_current_demotion(self) -> None:
        for actor in ("rlo-1", "con-1"):
            self.assertEqual(self.call("/api/governance", actor)[0], 403)
            self.assertEqual(
                self.call("/api/governance/evidence-record", actor, fixtures.claim())[0], 403
            )
        self.assertEqual(self.call("/api/governance")[0], 200)
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?",
            (
                json.dumps(dict(self.fixture.pm, role="Resident Liaison Officer")),
                self.fixture.pm["email"],
            ),
        )
        self.assertEqual(self.call("/api/governance")[0], 403)
        self.assertEqual(
            self.call("/api/governance/evidence-record", body=fixtures.claim())[0], 403
        )

    def test_http_closed_schema_and_no_write_get(self) -> None:
        before = copy.deepcopy(self.store.data)
        audit = list(self.store.audit_entries())
        for query in (
            "unknown=x",
            "assessment=null",
            "assessment=%7B",
            "assessment=1",
            "assessment=%7B%7D&assessment=%7B%7D",
        ):
            self.assertEqual(self.call("/api/governance?" + query)[0], 400)
        extras: list[dict[str, Any]] = [
            {"actor": {}},
            {"recorded_at": "yesterday"},
            {"status": "Closed"},
            {"approval": True},
            {"expected_revision": True},
            {"references": [{}]},
        ]
        for extra in extras:
            self.assertEqual(
                self.call("/api/governance/evidence-record", body=fixtures.claim(**extra))[0],
                400,
            )
        self.assertEqual(before, self.store.data)
        # Ordinary access audit may exist; no claim success audit may exist.
        self.assertEqual(
            [e for e in self.store.audit_entries() if e["action"] == "rai_evidence_record"],
            [e for e in audit if e["action"] == "rai_evidence_record"],
        )

    def test_http_committed_reload_response(self) -> None:
        original = self.store.save

        def fail_ack() -> None:
            original()
            raise RuntimeError("constructed acknowledgement failure")

        with patch.object(self.store, "save", side_effect=fail_ack):
            status, result = self.call("/api/governance/evidence-record", body=fixtures.claim())
        self.assertEqual((status, result["outcome"]), (409, "committed"))
        self.assertEqual(self.call("/api/governance")[1]["rai_evidence"]["history_record_count"], 1)
        self.assertEqual(
            self.call("/api/governance/evidence-record", body=fixtures.claim())[0], 200
        )
        with patch.object(
            self.store, "rai_evidence_record", side_effect=GovernanceCommittedError("Reload")
        ):
            self.assertEqual(
                self.call("/api/governance/evidence-record", body=fixtures.claim())[0], 409
            )

    def test_http_response_encoding_failure_is_committed(self) -> None:
        original = self.store.rai_evidence_record

        def unencodable(user: Any, body: Any) -> Any:
            result = original(user, body)
            result["constructed_transport_failure"] = object()
            return result

        with patch.object(self.store, "rai_evidence_record", side_effect=unencodable):
            status, result = self.call("/api/governance/evidence-record", body=fixtures.claim())
        self.assertEqual((status, result["outcome"]), (409, "committed"))
        self.assertEqual(self.call("/api/governance")[1]["rai_evidence"]["history_record_count"], 1)


class JsonGovernanceEvidenceApi(GovernanceEvidenceApi):
    def setUp(self) -> None:
        self.fixture = fixtures.EvidenceRegister()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store = self.fixture.store
        self.app = App(self.store, "constructed-126-only")
        self.http = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.http.server_address[1]}"
        self.cookies = {}

    def test_http_role_denial_and_current_demotion(self) -> None:
        for actor in ("rlo-1", "con-1"):
            self.assertEqual(self.call("/api/governance", actor)[0], 403)
            self.assertEqual(
                self.call("/api/governance/evidence-record", actor, fixtures.claim())[0], 403
            )
        self.assertEqual(self.call("/api/governance")[0], 200)
        del self.store.staff[self.fixture.pm["email"]]
        self.assertEqual(self.call("/api/governance")[0], 401)
        self.assertEqual(
            self.call("/api/governance/evidence-record", body=fixtures.claim())[0], 401
        )

    def test_http_committed_reload_response(self) -> None:
        # JSON has no SQL commit witness; exercise the explicit core outcome instead.
        with patch.object(
            self.store, "rai_evidence_record", side_effect=GovernanceCommittedError("Reload")
        ):
            self.assertEqual(
                self.call("/api/governance/evidence-record", body=fixtures.claim())[0], 409
            )
