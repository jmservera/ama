"""E7 regressions for issue 1288: the fenced transport's absolute deadline owns the whole response.

A real loopback TLS server with public synthetic bodies, the real fenced opener and the production
read call. The deadline must stop a response whose headers arrive at once and whose body trickles
past the deadline, for a closing and for a persistent connection, without leaving a live timer or an
open socket. Shutting the local socket ends the local read only; it does not stop remote work."""

import http.client
import os
import socket
import ssl
import threading
import time
import unittest
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

from zava_forward.core import ai_consumption, ai_transport

import test_quality_sensors_e2 as e2

DEADLINE = 1.0
JSON = b'{"model":"m","choices":[{"message":{"content":"{}"}}],"usage":{}}'


class Peer:
    """Accepts TLS connections, reads one request, then runs the scripted reply."""

    def __init__(self, script: Callable[[Any], None]) -> None:
        directory = e2.certificate()
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(f"{directory}/cert.pem", f"{directory}/key.pem")
        self.cert = f"{directory}/cert.pem"
        self.script, self.accepts = script, 0
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(4)
        self.sock.settimeout(0.2)
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.serve, daemon=True)
        self.thread.start()

    @property
    def endpoint(self) -> str:
        return f"https://127.0.0.1:{self.sock.getsockname()[1]}"

    def serve(self) -> None:
        while not self.stop.is_set():
            try:
                raw, _ = self.sock.accept()
            except (TimeoutError, OSError):
                continue
            self.accepts += 1
            threading.Thread(target=self.handle, args=(raw,), daemon=True).start()

    def handle(self, raw: Any) -> None:
        try:
            conn = self.context.wrap_socket(raw, server_side=True)
            conn.settimeout(10)
            data = b""
            while b"\r\n\r\n" not in data:
                data += conn.recv(1024)
            head, _, body = data.partition(b"\r\n\r\n")
            size = int(
                [h for h in head.split(b"\r\n") if h.lower().startswith(b"content-length")][
                    0
                ].split(b":")[1]
            )
            while len(body) < size:
                body += conn.recv(1024)
            self.script(conn)
        except OSError:
            pass

    def close(self) -> None:
        self.stop.set()
        self.thread.join(5)
        self.sock.close()


def trickle(conn: Any, seconds: float, filler: bytes = b" ") -> None:
    end = time.monotonic() + seconds
    try:
        while time.monotonic() < end:
            conn.sendall(filler)
            time.sleep(0.1)
    except OSError:
        pass


def closing_trickle(conn: Any) -> None:
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n")
    trickle(conn, 5)
    conn.close()


def persistent_trickle(conn: Any) -> None:
    conn.sendall(
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 100000\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    trickle(conn, 5)
    conn.close()


def json_prefix_then_trickle(conn: Any) -> None:
    conn.sendall(
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 100000\r\n"
        b"Connection: keep-alive\r\n\r\n" + JSON
    )
    trickle(conn, 5)
    conn.close()


def quick(conn: Any) -> None:
    conn.sendall(
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: "
        + str(len(JSON)).encode()
        + b"\r\nConnection: close\r\n\r\n"
        + JSON
    )
    conn.close()


def server_error(conn: Any) -> None:
    body = b'{"error":"synthetic"}'
    conn.sendall(
        b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: "
        + str(len(body)).encode()
        + b"\r\nConnection: close\r\n\r\n"
        + body
    )
    conn.close()


def malformed(conn: Any) -> None:
    conn.sendall(b"NOT-HTTP garbage\r\n\r\n")
    conn.close()


class DeadlineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.windows: list[Any] = []
        outer = self

        real = ai_transport.Window

        def recording(*args: Any, **kwargs: Any) -> Any:
            window = real(*args, **kwargs)
            outer.windows.append(window)
            return window

        patcher = patch.object(ai_transport, "Window", recording)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.fenced = 0

    def peer(self, script: Callable[[Any], None]) -> Peer:
        peer = Peer(script)
        self.addCleanup(peer.close)
        patcher = patch.dict(os.environ, {"SSL_CERT_FILE": peer.cert})
        patcher.start()
        self.addCleanup(patcher.stop)
        return peer

    def fence(self) -> None:
        self.fenced += 1

    def request(self, peer: Peer) -> Any:
        opener = ai_transport.opener(self.fence, DEADLINE)
        req = urllib.request.Request(f"{peer.endpoint}/x", data=b'{"public":"synthetic"}')
        return opener.open(req, timeout=5)

    def assertReleased(self) -> None:
        self.assertEqual(len(self.windows), 1)
        window = self.windows[0]
        self.assertTrue(window.done, "the deadline operation was never finished")
        if window.sock is not None:
            self.assertEqual(window.sock.fileno(), -1, "the socket is still open")
        end = time.monotonic() + 2
        while time.monotonic() < end:
            live = [t for t in threading.enumerate() if isinstance(t, threading.Timer)]
            if not live:
                return
            time.sleep(0.05)
        self.fail("a deadline timer thread is still alive")

    def outlasts(self, script: Callable[[Any], None]) -> None:
        peer = self.peer(script)
        started = time.monotonic()
        with self.assertRaises(TimeoutError):
            with self.request(peer) as response:
                response.read(256001)
        self.assertLess(time.monotonic() - started, 4, "the read outlived the absolute deadline")
        self.assertReleased()

    def test_a_closing_response_that_trickles_past_the_deadline_is_stopped(self) -> None:
        self.outlasts(closing_trickle)

    def test_a_persistent_response_that_trickles_past_the_deadline_is_stopped(self) -> None:
        self.outlasts(persistent_trickle)

    def test_a_valid_json_prefix_followed_by_a_trickle_is_not_accepted_as_complete(self) -> None:
        self.outlasts(json_prefix_then_trickle)

    def test_a_prompt_response_completes_and_releases_everything(self) -> None:
        peer = self.peer(quick)
        with self.request(peer) as response:
            self.assertEqual(response.read(256001), JSON)
        self.assertEqual(self.fenced, 2)  # pre-connect and pre-first-byte
        self.assertReleased()

    def test_an_http_error_releases_the_operation_when_it_is_closed(self) -> None:
        peer = self.peer(server_error)
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.request(peer)
        caught.exception.close()
        self.assertReleased()

    def test_a_malformed_status_line_releases_the_operation(self) -> None:
        peer = self.peer(malformed)
        with self.assertRaises((http.client.HTTPException, urllib.error.URLError)):
            self.request(peer)
        self.assertReleased()

    def test_a_refused_send_fence_opens_no_socket_and_leaves_nothing_live(self) -> None:
        peer = self.peer(quick)

        def refuse() -> None:
            raise ai_consumption.DispatchWithdrawn("refused")

        opener = ai_transport.opener(refuse, DEADLINE)
        with self.assertRaises(ai_consumption.DispatchWithdrawn):
            opener.open(urllib.request.Request(f"{peer.endpoint}/x", data=b"{}"), timeout=5)
        self.assertEqual(peer.accepts, 0)
        end = time.monotonic() + 2
        while [t for t in threading.enumerate() if isinstance(t, threading.Timer)]:
            self.assertLess(time.monotonic(), end, "a timer thread is still alive")
            time.sleep(0.05)


if __name__ == "__main__":
    unittest.main()
