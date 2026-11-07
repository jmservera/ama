"""Azure Storage Queue adapter for the `TaskQueue` port, using only the standard library.

The agents identity installs no third-party packages (ADR 0001, ADR 0006), so this
speaks the Queue service REST API with a bearer token supplied by the caller. The
HTTP transport and token source are injected, which keeps the adapter testable
without network access. It never decides anything about a case: it leases a
message, hands the validated inert task to the worker and acknowledges only after
the API post-back succeeded. Malformed or repeatedly failing messages move to the
poison queue instead of blocking the queue.
"""

from __future__ import annotations

import base64
import binascii
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable
from typing import Any

from zava_forward.agents.dispatch import MAX_MESSAGE_CHARS, TaskMessage

API_VERSION = "2023-11-03"
MAX_DELIVERIES = 5
LEASE_SECONDS = 60
HTTP_TIMEOUT_SECONDS = 10
MAX_RESPONSE_BYTES = 256 * 1024

Transport = Callable[[str, str, dict[str, str], bytes | None], tuple[int, bytes]]
"""(method, url, headers, body) -> (status, response body)."""

TokenSource = Callable[[], str]
"""Returns a current bearer token for https://storage.azure.com/."""


class QueueError(RuntimeError):
    """A queue service call failed; the worker loop retries after a pause."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def urllib_transport(
    method: str, url: str, headers: dict[str, str], body: bytes | None
) -> tuple[int, bytes]:
    """Default transport. Redirects are refused so a bearer token is never forwarded."""
    request = urllib.request.Request(url, data=body, headers=headers, method=method)  # noqa: S310
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            return response.status, response.read(MAX_RESPONSE_BYTES)
    except urllib.error.HTTPError as error:
        return error.code, error.read(MAX_RESPONSE_BYTES)
    except OSError as error:
        raise QueueError("Queue service unreachable.") from error


def checked_endpoint(endpoint: str) -> str:
    """Accept only an https storage queue endpoint so tokens never travel in clear text."""
    parts = urllib.parse.urlsplit(endpoint)
    if parts.scheme != "https" or not parts.hostname or parts.path not in ("", "/"):
        raise ValueError("Queue endpoint must be an https origin.")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("Queue endpoint must not carry credentials or a query.")
    return f"https://{parts.netloc}"


def decode_text(text: str) -> str:
    """Queue text is base64 when written by some SDKs and plain JSON when written by others."""
    try:
        return base64.b64decode(text, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return text


class AzureTaskQueue:
    """`TaskQueue` over the Queue service REST API."""

    def __init__(
        self,
        endpoint: str,
        queue: str,
        poison_queue: str,
        token: TokenSource,
        transport: Transport = urllib_transport,
        lease: int = LEASE_SECONDS,
        max_deliveries: int = MAX_DELIVERIES,
    ) -> None:
        self.endpoint = checked_endpoint(endpoint)
        for name in (queue, poison_queue):
            if not name or not name.replace("-", "").isalnum() or name != name.lower():
                raise ValueError("Queue names must be lower-case letters, digits and hyphens.")
        self.queue = queue
        self.poison_queue = poison_queue
        self.token = token
        self.transport = transport
        self.lease = lease
        self.max_deliveries = max_deliveries

    def _call(
        self, method: str, path: str, query: dict[str, str], body: bytes | None = None
    ) -> tuple[int, bytes]:
        url = f"{self.endpoint}/{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        headers = {
            "Authorization": f"Bearer {self.token()}",
            "x-ms-version": API_VERSION,
            "Content-Type": "application/xml",
        }
        return self.transport(method, url, headers, body)

    def _messages(self, queue: str) -> str:
        return f"{queue}/messages"

    def receive(self) -> tuple[str, TaskMessage] | None:
        status, body = self._call(
            "GET",
            self._messages(self.queue),
            {"numofmessages": "1", "visibilitytimeout": str(self.lease)},
        )
        if status != 200:
            raise QueueError(f"Queue receive failed with status {status}.")
        try:
            entries = ET.fromstring(body).findall("QueueMessage")  # noqa: S314
        except ET.ParseError as error:
            raise QueueError("Queue receive returned malformed XML.") from error
        if not entries:
            return None
        entry = entries[0]
        message_id = entry.findtext("MessageId") or ""
        pop_receipt = entry.findtext("PopReceipt") or ""
        text = entry.findtext("MessageText") or ""
        try:
            deliveries = int(entry.findtext("DequeueCount") or "1")
        except ValueError as error:
            raise QueueError("Queue message has an invalid DequeueCount.") from error
        if not message_id or not pop_receipt:
            raise QueueError("Queue message is missing its identity.")
        receipt = f"{message_id}\n{pop_receipt}"
        if deliveries > self.max_deliveries or len(text) > MAX_MESSAGE_CHARS * 2:
            self._poison(receipt, text)
            return None
        try:
            message = TaskMessage.from_json(decode_text(text))
        except (ValueError, KeyError, TypeError):
            self._poison(receipt, text)
            return None
        return receipt, message

    def _poison(self, receipt: str, text: str) -> None:
        """Move an unusable message aside. Delete only after the poison copy is stored."""
        # The raw text is kept for diagnosis; it contains only the inert task snapshot.
        envelope = "<QueueMessage><MessageText>{}</MessageText></QueueMessage>".format(
            base64.b64encode(text[: MAX_MESSAGE_CHARS * 2].encode("utf-8")).decode("ascii")
        )
        status, _ = self._call(
            "POST", self._messages(self.poison_queue), {}, envelope.encode("ascii")
        )
        if status != 201:
            raise QueueError(f"Poison queue write failed with status {status}.")
        self.ack(receipt)

    @staticmethod
    def _split(receipt: str) -> tuple[str, str]:
        message_id, _, pop_receipt = receipt.partition("\n")
        if not message_id or not pop_receipt:
            raise ValueError("Receipt is malformed.")
        return message_id, pop_receipt

    def ack(self, receipt: str) -> None:
        message_id, pop_receipt = self._split(receipt)
        status, _ = self._call(
            "DELETE",
            f"{self._messages(self.queue)}/{urllib.parse.quote(message_id, safe='')}",
            {"popreceipt": pop_receipt},
        )
        if status not in (204, 404):
            raise QueueError(f"Queue delete failed with status {status}.")

    def release(self, receipt: str) -> None:
        """Make the message visible again at once; a lost lease expires on its own."""
        message_id, pop_receipt = self._split(receipt)
        status, _ = self._call(
            "PUT",
            f"{self._messages(self.queue)}/{urllib.parse.quote(message_id, safe='')}",
            {"popreceipt": pop_receipt, "visibilitytimeout": "0"},
        )
        if status not in (204, 404):
            raise QueueError(f"Queue release failed with status {status}.")


__all__ = [
    "AzureTaskQueue",
    "QueueError",
    "Transport",
    "TokenSource",
    "checked_endpoint",
    "urllib_transport",
]
