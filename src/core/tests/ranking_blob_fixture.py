"""In-memory Azure Blob REST stand-in for the ranking archive tests (Refs #1258).

This is a mock transport, not an emulator and not a storage account. It models only what the
archive adapter relies on: create-only Put Blob (If-None-Match), x-ms-meta-* round trip, Get Blob,
a paginated container listing, and injected faults. It has no delete and no overwrite.
"""

import json
import threading
import urllib.parse
from collections.abc import Callable, Mapping

from zava_forward.core.documents import DocumentStoreError

URL = "https://acct.blob.core.windows.net"
SAS = "sv=2022&sig=SENTINEL-SAS-SECRET"


Response = tuple[int, dict[str, str], bytes]
Call = tuple[str, str, Mapping[str, str], bytes | None]


class FakeBlobContainer:
    def __init__(self, page_size: int = 100, mixed_case: bool = False) -> None:
        self.blobs: dict[str, bytes] = {}
        self.meta: dict[str, dict[str, str]] = {}
        self.calls: list[Call] = []
        self.put_faults: list[int | str | tuple[int, str]] = []
        self.get_faults: dict[str, int] = {}
        self.list_status = 200
        self.list_body: bytes | None = None
        self.page_size = page_size
        self.mixed_case = mixed_case
        self.lock = threading.Lock()
        self.put_gate: Callable[[], object] | None = None

    def __call__(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: int = 20,
    ) -> Response:
        with self.lock:
            self.calls.append((method, url, dict(headers), body))
        if "oauth2/token" in url or "msi/token" in url or "identity.local" in url:
            return (
                200,
                {},
                json.dumps(dict(access_token="SENTINEL-TOKEN", expires_on="9999999999")).encode(),
            )
        u = urllib.parse.urlparse(url)
        name = urllib.parse.unquote(u.path.split("/", 2)[2]) if u.path.count("/") >= 2 else ""
        if method == "PUT":
            return self._put(name, headers, body)
        if method == "GET" and "comp=list" in u.query:
            return self._list(urllib.parse.parse_qs(u.query))
        if method == "GET":
            return self._get(name)
        return 405, {}, b""

    def _put(self, name: str, headers: Mapping[str, str], body: bytes | None) -> Response:
        if self.put_gate:
            self.put_gate()
        with self.lock:
            fault = self.put_faults.pop(0) if self.put_faults else None
        if fault == "unreachable":
            raise DocumentStoreError(
                "storage unreachable: https://acct.blob.core.windows.net/ranking?sig=SENTINEL-SAS-SECRET"
            )
        if isinstance(fault, int):
            return fault, {}, b""
        if isinstance(fault, tuple):
            return fault[0], {"x-ms-error-code": fault[1]}, b""
        with self.lock:
            if (
                headers.get("If-None-Match") != "*"
                or "x-ms-blob-type" not in headers
                or body is None
            ):
                return 400, {}, b""
            if name in self.blobs:
                return 409, {"x-ms-error-code": "BlobAlreadyExists"}, b""
            self.blobs[name] = body
            self.meta[name] = {
                k[len("x-ms-meta-") :].lower(): v
                for k, v in headers.items()
                if k.lower().startswith("x-ms-meta-")
            }
        if fault == "lost":
            raise DocumentStoreError("storage unreachable: response lost")
        return 201, {}, b""

    def _get(self, name: str) -> Response:
        if name in self.get_faults:
            return self.get_faults[name], {}, b""
        with self.lock:
            if name not in self.blobs:
                return 404, {}, b""
            meta = {
                ("X-Ms-Meta-" + k.title() if self.mixed_case else "x-ms-meta-" + k): v
                for k, v in self.meta[name].items()
            }
            return 200, meta, self.blobs[name]

    def _list(self, q: dict[str, list[str]]) -> Response:
        if self.list_status != 200:
            return self.list_status, {}, b""
        if self.list_body is not None:
            return 200, {}, self.list_body
        prefix, marker = q.get("prefix", [""])[0], q.get("marker", [""])[0]
        with self.lock:
            names = sorted(n for n in self.blobs if n.startswith(prefix))
        start = names.index(marker) if marker in names else 0
        page = names[start : start + self.page_size]
        nxt = names[start + self.page_size] if start + self.page_size < len(names) else ""
        xml = (
            "<EnumerationResults><Blobs>"
            + "".join(f"<Blob><Name>{n}</Name></Blob>" for n in page)
            + f"</Blobs><NextMarker>{nxt}</NextMarker></EnumerationResults>"
        )
        return 200, {}, xml.encode()

    def requests(self, method: str) -> list[Call]:
        return [c for c in self.calls if c[0] == method and "oauth2" not in c[1]]
