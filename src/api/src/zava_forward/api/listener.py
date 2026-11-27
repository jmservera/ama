"""Listening-socket behaviour shared by the stdlib HTTP servers."""

from __future__ import annotations

from socket import socket as Socket
from typing import Any


class NonBlockingAcceptMixin:
    """Keep `serve_forever` responsive to `shutdown()`.

    A readiness event can outlive its connection (accept(2): removed by an asynchronous
    network error), and a blocking accept then sleeps until the next client, so shutdown
    waits forever. A non-blocking listener raises BlockingIOError, which the stdlib
    request loop treats as "no request" before it re-checks the shutdown flag.
    """

    socket: Socket

    def server_activate(self) -> None:
        super().server_activate()  # type: ignore[misc]
        self.socket.setblocking(False)

    def get_request(self) -> tuple[Socket, Any]:
        request, address = super().get_request()  # type: ignore[misc]
        request.setblocking(True)
        return request, address
