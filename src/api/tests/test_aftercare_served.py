"""Issue 133: the synthetic assisted aftercare journey through the real authenticated routes."""

import copy
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

import dataset
from test_quality_procurement import STAFF
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler

PW = "SYN-aftercare-test"
BODY: dict[str, Any] = dict(
    request_id="req-served-0001",
    raised_by="household",
    kind="discomfort",
    statement="Synthetic: the new loft hatch is cold to touch.",
    channel="phone",
    next_update="2026-11-20",
)


class Served(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        data["staff"] = copy.deepcopy(STAFF)
        self.path = Path(self.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(data))
        self.cookies: dict[str, str] = {}
        self.start()

    def start(self) -> None:
        self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.app = App(self.store, PW)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.cookies = {}

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(
        self, who: str | None, path: str, body: dict[str, Any] | None = None
    ) -> tuple[int, Any]:
        if who and who not in self.cookies:
            login = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(dict(email=f"{who}@example.test", password=PW)).encode(),
            )
            with urllib.request.urlopen(login) as r:
                self.cookies[who] = r.headers["Set-Cookie"].split(";")[0]
        headers = {"Cookie": self.cookies[who]} if who else {}
        request = urllib.request.Request(
            self.base + path, None if body is None else json.dumps(body).encode(), headers=headers
        )
        try:
            with urllib.request.urlopen(request) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def home(self) -> str:
        return str(self.call("sam", "/api/aftercare/form")[1]["homes"][0])

    def body(self, **extra: Any) -> dict[str, Any]:
        return dict(BODY, home_ref=self.home(), **extra)


class AftercareServed(Served):
    def test_form_is_bounded_to_the_constructed_allowlist(self) -> None:
        code, form = self.call("sam", "/api/aftercare/form")
        self.assertEqual(code, 200)
        self.assertIsInstance(form["homes"], list)
        self.assertTrue(form["homes"])
        self.assertIn("synthetic", form["synthetic_notice"].lower())
        self.assertEqual(self.app.aftercare.homes, set(form["homes"]))

    def test_unlisted_home_is_refused_and_nothing_is_stored(self) -> None:
        code, out = self.call(
            "sam", "/api/aftercare/concerns", dict(BODY, home_ref="REAL-HOUSEHOLD-1")
        )
        self.assertEqual(code, 400)
        self.assertIn("errors", out)
        self.assertEqual(self.call("sam", "/api/aftercare/concerns")[1]["count"], 0)

    def test_roles_and_session_actor(self) -> None:
        self.assertEqual(self.call(None, "/api/aftercare/form")[0], 401)
        for who in ("kim", "quin"):
            self.assertEqual(self.call(who, "/api/aftercare/concerns", self.body())[0], 403, who)
            self.assertEqual(self.call(who, "/api/aftercare/form")[0], 403, who)
        code, out = self.call(
            "sam", "/api/aftercare/concerns", self.body(recorded_by="Someone Else", actor="x")
        )
        self.assertEqual(code, 201, out)
        self.assertNotIn("Someone Else", json.dumps(out))
        actions = self.store.data["aftercare"]["actions"]
        self.assertEqual({a["actor"] for a in actions}, {"Sam Example"})

    def test_replay_conflict_and_restart_readback(self) -> None:
        body = self.body()
        first = self.call("sam", "/api/aftercare/concerns", body)
        self.assertEqual(first[0], 201)
        again = self.call("sam", "/api/aftercare/concerns", body)
        self.assertEqual(again[0], 200)
        self.assertEqual(self.call("sam", "/api/aftercare/concerns")[1]["count"], 1)
        changed = self.call(
            "sam",
            "/api/aftercare/concerns",
            dict(body, statement="Synthetic: a different statement."),
        )
        self.assertEqual(changed[0], 409)
        self.stop()
        self.store.db.close()
        self.start()
        code, listing = self.call("sam", "/api/aftercare/concerns")
        self.assertEqual(code, 200)
        self.assertEqual(listing["count"], 1)
        self.assertEqual(self.call("sam", "/api/aftercare/concerns", body)[0], 200)
        self.assertEqual(self.call("sam", "/api/aftercare/concerns")[1]["count"], 1)

    def test_evaluator_readback_has_unknown_denominator_and_no_closure(self) -> None:
        self.call("sam", "/api/aftercare/concerns", self.body())
        code, view = self.call("pam", "/api/aftercare/evaluator")
        self.assertEqual(code, 200)
        text = json.dumps(view)
        self.assertIn("nknown", text)
        self.assertNotIn("closed_automatically", text)
        self.assertEqual(self.call("kim", "/api/aftercare/evaluator")[0], 403)

    def test_quality_note_route_is_not_a_concern_intake(self) -> None:
        code, _ = self.call(
            "sam", "/api/cases/ZF-1/quality-aftercare", dict(index=0, note="Synthetic concern")
        )
        self.assertNotEqual(code, 200)
        self.assertEqual(self.call("sam", "/api/aftercare/concerns")[1]["count"], 0)

    def test_unconfirmed_write_is_503_and_same_id_reconciles(self) -> None:
        from zava_forward.core.aftercare_store import DocumentStateStore, UnconfirmedWriteError

        body = self.body()
        real = DocumentStateStore.update

        def committed_then_lost(store: DocumentStateStore, mutator: Any) -> Any:
            real(store, mutator)
            raise UnconfirmedWriteError(
                "Saved state could not be confirmed. Send again with the same request reference."
            )

        with patch.object(DocumentStateStore, "update", committed_then_lost):
            code, out = self.call("sam", "/api/aftercare/concerns", body)
        self.assertEqual(code, 503, out)
        again = self.call("sam", "/api/aftercare/concerns", body)
        self.assertEqual(again[0], 200)
        self.assertEqual(self.call("sam", "/api/aftercare/concerns")[1]["count"], 1)

    def test_malformed_and_unknown_paths(self) -> None:
        self.assertIn(self.call("sam", "/api/aftercare/concerns", dict(BODY))[0], (400,))
        self.assertEqual(self.call("sam", "/api/aftercare/nothing")[0], 404)


if __name__ == "__main__":
    unittest.main()
