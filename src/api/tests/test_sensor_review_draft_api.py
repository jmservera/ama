"""Loopback HTTP checks for the default-off sensor review draft routes (Refs #111).

Constructed approvals are SYNTHETIC TEST ONLY and never an actual signoff or approved task.
"""

import copy
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import timedelta
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest import mock

from tests.test_mvp import DATA
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_review_draft as srd
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic import sensor_scenarios as ss

from zava_forward.api.server import App, make_handler

PASSWORD = "synthetic-test-password"
CID = DATA["cases"][0]["id"]
OTHER = DATA["cases"][1]["id"]
APPROVED = sa.AnalysisPolicy(
    approval=sa.RuleApproval(
        sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"
    )
)
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))


def staff(code: str, role: str, **extra: Any) -> dict[str, Any]:
    return dict(
        code=code, name=f"Person {code}", email=f"{code.lower()}@example.test", role=role, **extra
    )


class DraftApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patch = mock.patch.dict(os.environ, {srd.FLAG: "1"})
        patch.start()
        self.addCleanup(patch.stop)
        data = copy.deepcopy(DATA)
        data["staff"] = [
            staff("qi", "Quality Inspector"),
            staff("scoped", "Quality Inspector", case_ids=[OTHER]),
            staff("rlo", "Resident Liaison Officer"),
            staff("con", "Contractor", contractor="Test Ltd"),
        ]
        path = Path(self.tmp.name) / "seed.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, PASSWORD)))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.addCleanup(self.httpd.server_close)
        self.addCleanup(self.httpd.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def call(self, actor: str, path: str, body: object = None) -> tuple[int, Any]:
        if actor not in self.cookies:
            login = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(dict(email=f"{actor}@example.test", password=PASSWORD)).encode(),
            )
            with urllib.request.urlopen(login) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            None if body is None else json.dumps(body).encode(),
            headers={"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def seed_draft(self) -> dict[str, Any]:
        rows = [
            dict(r, home_id=CID, sensor_id="SENS-SYN-1")
            for r in next(
                c for c in ss.generate() if c.truth.label == "sustained_high_humidity"
            ).rows
        ]
        signal = sa.derive_signal(CID, rows, WINDOW, WINDOW.end, "granted", APPROVED)
        user = self.store.staff["qi@example.test"]
        made: dict[str, Any] = srd._record_draft_synthetic(self.store, user, CID, signal, APPROVED)
        return made

    def test_flag_off_reports_disabled_and_refuses_writes(self) -> None:
        with mock.patch.dict(os.environ, {srd.FLAG: ""}):
            self.assertEqual(
                self.call("qi", f"/api/cases/{CID}/sensor-drafts"), (200, {"state": "disabled"})
            )
            status, _ = self.call("qi", f"/api/cases/{CID}/sensor-draft", {})
            self.assertEqual(status, 403)
        self.assertNotIn(srd.CASE_KEY, self.store.cases[CID])

    def test_roles_and_scope_are_denied_without_leaking_case_detail(self) -> None:
        paths = (
            f"/api/cases/{CID}/sensor-drafts",
            f"/api/cases/{OTHER}/sensor-drafts",
            "/api/cases/NOPE/sensor-drafts",
        )
        for actor in ("rlo", "con"):
            for path in paths:
                status, body = self.call(actor, path)
                self.assertEqual(status, 403, (actor, path))
                self.assertNotIn("stage", json.dumps(body))
        existing = self.call("scoped", f"/api/cases/{CID}/sensor-drafts")
        missing = self.call("scoped", "/api/cases/NOPE/sensor-drafts")
        self.assertEqual(existing, missing)
        self.assertEqual(existing[0], 403)
        self.assertEqual(self.call("qi", "/api/cases/NOPE/sensor-drafts")[0], 404)

    def test_post_denies_by_default_and_validates_the_window_after_authorization(self) -> None:
        good = {"window_start": "2024-01-01T00:00:00Z", "window_end": "2024-01-29T00:00:00Z"}
        self.assertEqual(self.call("con", f"/api/cases/{CID}/sensor-draft", good)[0], 403)
        self.assertEqual(self.call("rlo", f"/api/cases/{CID}/sensor-draft", good)[0], 403)
        self.assertEqual(
            self.call("qi", f"/api/cases/{CID}/sensor-draft", {"window_start": "x"})[0], 400
        )
        self.assertEqual(
            self.call("qi", f"/api/cases/{CID}/sensor-draft", dict(good, extra=1))[0], 400
        )
        status, body = self.call("qi", f"/api/cases/{CID}/sensor-draft", good)
        self.assertEqual(status, 200)
        self.assertFalse(body["created"])
        self.assertNotIn(srd.CASE_KEY, self.store.cases[CID])

    def test_seeded_draft_is_read_by_the_inspector_and_never_by_generic_case_detail(self) -> None:
        self.assertTrue(self.seed_draft()["created"])
        with mock.patch.object(srd, "SensorConsumer") as consumer:
            consumer.return_value.home_consent.return_value = "granted"
            status, body = self.call("qi", f"/api/cases/{CID}/sensor-drafts")
        self.assertEqual((status, body["state"], len(body["drafts"])), (200, "ok", 1))
        text = json.dumps(body)
        self.assertNotIn("draft_digest", text)
        for actor in ("qi", "rlo", "con"):
            status, detail = self.call(actor, f"/api/cases/{CID}")
            self.assertNotIn(srd.CASE_KEY, json.dumps(detail))
            self.assertNotIn("SYNTHETIC-TEST-SENTINEL", json.dumps(detail))
        self.assertIn(srd.CASE_KEY, self.store.detail(CID))

    def test_consent_not_granted_withholds_the_read(self) -> None:
        self.seed_draft()
        status, body = self.call("qi", f"/api/cases/{CID}/sensor-drafts")
        self.assertEqual((status, body["state"], body["drafts"]), (200, "consent-withheld", []))

    def test_existing_sensor_routes_still_deny_unauthorised_roles(self) -> None:
        self.assertIn(self.call("con", "/api/sensors")[0], (403, 404))


if __name__ == "__main__":
    unittest.main()
