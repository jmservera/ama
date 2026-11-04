"""Issue 810: the API answers HTTP/1.1 and keeps connections alive for the Easy Auth sidecar."""

import http.client
import socket
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
        port = self.httpd.server_address[1]
        self.conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)

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

    def _pipelined(self, first: bytes) -> bytes:
        second = b"GET /healthz HTTP/1.1\r\nHost: x\r\n\r\n"
        with socket.create_connection(("127.0.0.1", self.httpd.server_address[1]), timeout=10) as s:
            s.sendall(first + second)
            data = b""
            while chunk := s.recv(65536):
                data += chunk
        return data

    def test_non_post_body_closes_without_second_response(self) -> None:
        body = b"GET /healthz HTTP/1.1\r\nHost: x\r\n\r\n"  # smuggled request inside the body
        for method in ("GET", "HEAD", "PUT", "DELETE", "OPTIONS"):
            with self.subTest(method=method):
                line = f"{method} /healthz HTTP/1.1\r\nHost: x\r\n"
                head = f"{line}Content-Length: {len(body)}\r\n\r\n".encode()
                data = self._pipelined(head + body)
                self.assertEqual(data.count(b"HTTP/1.1 "), 1, data)
                self.assertIn(b"Connection: close", data)

    def test_transfer_encoding_closes_without_second_response(self) -> None:
        head = b"GET /healthz HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n"
        data = self._pipelined(head)
        self.assertEqual(data.count(b"HTTP/1.1 "), 1, data)
        self.assertIn(b"Connection: close", data)


if __name__ == "__main__":
    unittest.main()
