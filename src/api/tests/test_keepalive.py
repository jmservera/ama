"""Issue 810: the API answers HTTP/1.1 and keeps connections alive for the Easy Auth sidecar."""

import http.client
import threading
import unittest

from test_auth import ENV, Base
from zava_forward.api import auth
from zava_forward.api.server import App, _Server, make_handler


class KeepAliveTests(Base):
    def setUp(self) -> None:
        super().setUp()  # type: ignore[no-untyped-call]
        self.app = App(  # type: ignore[no-untyped-call]
            self.store,
            provider=auth.TrustedProxyProvider(self.store, ENV),  # type: ignore[no-untyped-call]
        )
        self.httpd = _Server(("127.0.0.1", 0), make_handler(self.app))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.conn = http.client.HTTPConnection("127.0.0.1", self.httpd.server_address[1], timeout=10)

    def tearDown(self) -> None:
        self.conn.close()
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()  # type: ignore[no-untyped-call]

    def test_connection_is_reused_across_requests(self) -> None:
        for _ in range(3):
            self.conn.request("GET", "/healthz")
            r = self.conn.getresponse()
            self.assertEqual((r.version, r.status), (11, 200))
            self.assertEqual(r.read(), b"ok")
            self.assertFalse(r.will_close)

    def test_unread_body_closes_the_connection(self) -> None:
        self.conn.request("POST", "/api/me", headers={"Content-Length": "9000000"})
        r = self.conn.getresponse()
        self.assertEqual(r.status, 400)
        r.read()
        self.assertTrue(r.will_close)


if __name__ == "__main__":
    unittest.main()
