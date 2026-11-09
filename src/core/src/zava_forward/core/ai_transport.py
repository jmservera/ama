"""A fenced single-shot HTTP transport for the real Ai client.

The admitting authority hands the client a send fence (see
`ai_consumption.send_fence`). This transport owns the socket, so it can run
that fence at the physical boundary: before the connection is opened and again
immediately before the first request byte, after the connection and TLS
handshake exist. The fence restamps the admission for a bounded send window;
a total deadline then shuts the socket, so a slow send cannot outlive the
window that another caller's slot reuse relies on.

The opener has no proxy, redirect or retry handling, so one request is one
connection and one fence pair. What user space cannot exclude is an operating
system suspension between the last fence return and the kernel write, or one
that outlasts the restamped window; see `Assistants.fence_send`.
"""

from __future__ import annotations

import functools
import http.client
import socket
import ssl
import threading
import time
import urllib.request
from collections.abc import Callable
from typing import Any

from . import ai_consumption

# The fence call itself may not take longer than this, or its restamped window is stale.
FENCE_MARGIN = 2.0


class Window:
    """The fence calls and the absolute deadline of one connection.

    The deadline owns the connected socket handle captured at the first request byte, so it
    keeps a live shutdown handle across headers and body regardless of what the HTTP layers do
    to their own `sock` attribute. It is cancelled only by `finish`, when the whole response
    completes or fails.
    """

    def __init__(self, fence: Callable[[], None], deadline: float) -> None:
        self.fence, self.deadline = fence, deadline
        self.sent = False
        self.adopted = False
        self.done = False
        self.expired = False
        self.sock: socket.socket | None = None
        self.timer: threading.Timer | None = None
        self.lock = threading.Lock()

    def first_byte(self, sock: socket.socket | None) -> None:
        if self.sent:
            return
        self.sent = True
        started = time.monotonic()
        self.fence()
        if time.monotonic() - started > FENCE_MARGIN:
            raise ai_consumption.DispatchWithdrawn("fence-stalled")
        with self.lock:
            self.sock = sock
            timer = threading.Timer(self.deadline, self.expire)
            timer.daemon = True
            self.timer = timer
            timer.start()

    def expire(self) -> None:
        with self.lock:
            if self.done:
                return
            self.expired = True
            sock = self.sock
        _shutdown(sock)

    def finish(self) -> None:
        with self.lock:
            self.done = True
            timer = self.timer
        if timer is not None:
            timer.cancel()


def _shutdown(sock: socket.socket | None) -> None:
    if sock is not None:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass


class OwnedResponse(http.client.HTTPResponse):
    """A response whose lifetime is the window: it ends only when the body is done or closed."""

    window: Window  # bound per connection by `owned`

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.window.adopted = True

    def _check(self) -> None:
        if self.window.expired:
            raise TimeoutError("absolute provider deadline reached")

    def read(self, amt: int | None = None) -> bytes:
        self._check()
        try:
            data = super().read(amt)
        except OSError:
            self._check()
            raise
        self._check()  # a shutdown can look like a clean end of stream
        if self.isclosed():
            self.window.finish()  # the whole body was read: the response is complete
        return data

    def close(self) -> None:
        super().close()
        self.window.finish()


def owned(window: Window) -> type[OwnedResponse]:
    return type("OwnedResponse", (OwnedResponse,), {"window": window})


class FencedHTTPConnection(http.client.HTTPConnection):
    def __init__(
        self, *args: Any, fence: Callable[[], None], deadline: float, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.window = Window(fence, deadline)
        self.response_class = owned(self.window)

    def connect(self) -> None:
        self.window.fence()
        super().connect()

    def send(self, data: Any) -> None:
        if self.sock is None:
            self.connect()  # connect first, so the fence below runs on the live connection
        self.window.first_byte(self.sock)
        super().send(data)

    def close(self) -> None:
        if not self.window.adopted:
            self.window.finish()
        super().close()


class FencedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(
        self, *args: Any, fence: Callable[[], None], deadline: float, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.window = Window(fence, deadline)
        self.response_class = owned(self.window)

    def connect(self) -> None:
        self.window.fence()
        super().connect()

    def send(self, data: Any) -> None:
        if self.sock is None:
            self.connect()  # connect first, so the fence below runs on the live connection
        self.window.first_byte(self.sock)
        super().send(data)

    def close(self) -> None:
        if not self.window.adopted:
            self.window.finish()
        super().close()


class _HTTP(urllib.request.HTTPHandler):
    def __init__(self, fence: Callable[[], None], deadline: float) -> None:
        super().__init__()
        self.fence, self.deadline = fence, deadline

    def http_open(self, req: urllib.request.Request) -> http.client.HTTPResponse:
        connection = functools.partial(
            FencedHTTPConnection, fence=self.fence, deadline=self.deadline
        )
        return self.do_open(connection, req)


class _HTTPS(urllib.request.HTTPSHandler):
    def __init__(self, fence: Callable[[], None], deadline: float) -> None:
        super().__init__()
        self.fence, self.deadline = fence, deadline
        self.context = ssl.create_default_context()

    def https_open(self, req: urllib.request.Request) -> http.client.HTTPResponse:
        connection = functools.partial(
            FencedHTTPSConnection, fence=self.fence, deadline=self.deadline, context=self.context
        )
        return self.do_open(connection, req)


def opener(fence: Callable[[], None], deadline: float) -> urllib.request.OpenerDirector:
    director = urllib.request.OpenerDirector()
    for handler in (
        _HTTP(fence, deadline),
        _HTTPS(fence, deadline),
        urllib.request.HTTPDefaultErrorHandler(),
        urllib.request.HTTPErrorProcessor(),
        urllib.request.UnknownHandler(),
    ):
        director.add_handler(handler)
    return director
