"""Issue 920: /api/me reports which optional services are off so denials are not requested."""

import json
import threading
import unittest
import urllib.error
import urllib.request
from typing import Any

from test_auth import ENV, OID_NEW, OID_SAM, Base, principal
from zava_forward.api import auth
from zava_forward.api.server import App, _Server, make_handler


class ExpectedDenialTests(Base):
    def setUp(self) -> None:
        super().setUp()
        self.app = App(
            self.store,
            provider=auth.TrustedProxyProvider(self.store, ENV),
        )
        self.httpd = _Server(("127.0.0.1", 0), make_handler(self.app))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def get(self, path: str, **headers: str) -> tuple[int, Any]:
        headers["X-MS-CLIENT-PRINCIPAL"] = principal(oid=OID_SAM)
        return self.fetch(path, headers)

    def get_as(self, path: str, roles: tuple[str, ...]) -> tuple[int, Any]:
        return self.fetch(path, {"X-MS-CLIENT-PRINCIPAL": principal(roles=roles, oid=OID_NEW)})

    def fetch(self, path: str, headers: dict[str, str]) -> tuple[int, Any]:
        req = urllib.request.Request(self.base + path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_me_reports_stores_off_and_denials_stay_expected(self) -> None:
        code, me = self.get("/api/me")
        self.assertEqual(code, 200)
        self.assertEqual(
            me["services"],
            {"photo": False, "law_alerts": False, "assistants": True, "cases": True},
        )
        self.assertEqual(self.get("/api/account/photo")[0], 503)
        self.assertEqual(self.get("/api/law/alerts")[0], 503)
        self.assertEqual(self.get("/api/chat/regulatory/status")[0], 403)

    def test_me_reports_assistants_off_for_admin_only_and_denial_stays_403(self) -> None:
        admin = ("ZavaForward.ApplicationAdmin",)
        _, me = self.get_as("/api/me", admin)
        self.assertFalse(me["services"]["assistants"])
        self.assertFalse(me["services"]["cases"])
        self.assertEqual(self.get_as("/api/facets", admin)[0], 403)
        self.assertEqual(self.get_as("/api/assistants", admin)[0], 403)

    def test_me_reports_photo_token_present(self) -> None:
        _, me = self.get("/api/me", **{"X-MS-TOKEN-AAD-ACCESS-TOKEN": "synthetic"})
        self.assertTrue(me["services"]["photo"])


if __name__ == "__main__":
    unittest.main()
