"""Issue 691: the employee server must queue bursts of parallel proxy connections."""

import select
import socket
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from zava_forward.api import server
from zava_forward.api.resident_demo import app as demo
from zava_forward.api.resident_preview import app as preview


def _queued(cls: type[HTTPServer], burst: int = 30) -> int:
    httpd = cls(("127.0.0.1", 0), BaseHTTPRequestHandler)
    socks: list[socket.socket] = []
    try:
        for _ in range(burst):
            c = socket.socket()
            c.setblocking(False)
            try:
                c.connect(httpd.server_address)
            except BlockingIOError:
                pass
            socks.append(c)
        time.sleep(0.5)
        return sum(
            1
            for c in socks
            if c.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0
            and select.select([], [c], [], 0)[1]
        )
    finally:
        for c in socks:
            c.close()
        httpd.server_close()


class ListenBacklogTests(unittest.TestCase):
    def test_servers_declare_large_backlog(self) -> None:
        for cls in (server._Server, demo._Server, preview._Server):
            self.assertGreaterEqual(cls.request_queue_size, 128)
            self.assertTrue(cls.daemon_threads)

    def test_employee_server_queues_burst(self) -> None:
        self.assertEqual(_queued(server._Server), 30)


if __name__ == "__main__":
    unittest.main()
