"""Issue 920: /api/me reports which optional services are off so denials are not requested."""

import json
import threading
import unittest
import urllib.error
import urllib.request
from typing import Any

from test_auth import ENV, OID_SAM, Base, principal
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
        req = urllib.request.Request(self.base + path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_me_reports_stores_off_and_denials_stay_expected(self) -> None:
        code, me = self.get("/api/me")
        self.assertEqual(code, 200)
        self.assertEqual(me["services"], {"photo": False, "law_alerts": False})
        self.assertEqual(self.get("/api/account/photo")[0], 503)
        self.assertEqual(self.get("/api/law/alerts")[0], 503)
        self.assertEqual(self.get("/api/chat/regulatory/status")[0], 403)

    def test_me_reports_photo_token_present(self) -> None:
        _, me = self.get("/api/me", **{"X-MS-TOKEN-AAD-ACCESS-TOKEN": "synthetic"})
        self.assertTrue(me["services"]["photo"])


if __name__ == "__main__":
    unittest.main()
