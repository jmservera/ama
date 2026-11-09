"""Azure Blob JSON persistence for the ranking publication archive (owner decision, issue 1258).

A thin adapter over the REST pattern and authentication of AzureBlobDocumentStore. It can only
create a record (conditional, create-only), read one back with its metadata and list names. There
is no overwrite, delete or caller-chosen location: the account and container come from the
deployment configuration and every name must match the ranking record pattern.

Errors carry a short reason and an HTTP status only. They never name the account, container, URL,
credential or token. A write whose outcome is not known after the request was sent is reported as
BlobArchiveUncertain and is neither a success nor a rollback.
"""

import hashlib
import os
import re
import urllib.parse
import xml.etree.ElementTree as ET
from collections.abc import Callable, Mapping
from typing import Any

from .documents import AzureBlobDocumentStore

SELECTOR = "ZF_RANKING_ARCHIVE"
CONTAINER_VAR = "ZF_RANKING_BLOB_CONTAINER"
_NAME = re.compile(r"^ranking-[A-Za-z0-9._-]+-\d{4}-\d{2}-\d{2}-[0-9a-f]{12}\.json$")
_MAX_PAGES = 1000
Transport = Callable[..., tuple[int, Mapping[str, str], bytes]]


class BlobArchiveError(OSError):
    """The archive refused or could not complete a request. Nothing is claimed as stored."""


class BlobArchiveUncertain(OSError):
    """A create request was sent and its outcome is unknown; the record may or may not exist."""


def metadata_for(snap: Mapping[str, Any], published_on: str, raw: bytes) -> dict[str, str]:
    return {
        "policy_version": str(snap["policy_version"]),
        "as_of": str(snap["as_of"]),
        "published_on": published_on,
        "snapshot_hash": str(snap["snapshot_hash"]),
        "record_sha256": hashlib.sha256(raw).hexdigest(),
    }


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def _parse_listing(body: bytes) -> tuple[list[str], str]:
    """Names and next marker of one List Blobs page; any other structure is unreadable."""
    unreadable = "ranking archive listing was unreadable"
    bad = False
    try:
        root = ET.fromstring(body)
    except (ET.ParseError, LookupError, ValueError):
        bad = True
    if bad or root.tag != "EnumerationResults":
        raise BlobArchiveError(unreadable)
    blobs = root.findall("Blobs")
    if len(blobs) != 1:
        raise BlobArchiveError(unreadable)
    names: list[str] = []
    for blob in blobs[0]:
        entry = blob.findall("Name") if blob.tag == "Blob" else []
        if len(entry) != 1 or len(entry[0]) or not (entry[0].text or "").strip():
            raise BlobArchiveError(unreadable)
        name = entry[0].text or ""
        if name.startswith("ranking-") and name.endswith(".json"):
            names.append(name)
    return names, (root.findtext("NextMarker") or "").strip()


class BlobRankingArchive:
    def __init__(
        self,
        account_url: str,
        container: str,
        sas: str | None = None,
        client_id: str | None = None,
        transport: Transport | None = None,
        env: Mapping[str, str] | None = None,
    ) -> None:
        try:
            self._store = AzureBlobDocumentStore(  # type: ignore[no-untyped-call]
                account_url, container, sas=sas, client_id=client_id, transport=transport, env=env
            )
        except ValueError:
            failed = True
        else:
            failed = False
        if failed:
            raise BlobArchiveError("ranking archive configuration is invalid")

    def _check(self, name: str) -> None:
        if not _NAME.fullmatch(name):
            raise ValueError("not a ranking record name")

    def _url(self, name: str) -> str:
        url = f"{self._store.base}/{urllib.parse.quote(name)}"
        return f"{url}?{self._store.sas}" if self._store.sas else url

    def _send(
        self, method: str, url: str, extra: dict[str, str], body: bytes | None, what: str
    ) -> tuple[int, Mapping[str, str], bytes]:
        """Send one request. A failure before dispatch is a refusal; after dispatch, uncertain."""
        refused = False
        try:
            headers = self._store._headers(extra)  # type: ignore[no-untyped-call]
        except Exception:
            refused = True
        if refused:
            raise BlobArchiveError(f"ranking archive {what} refused: authorization unavailable")
        dispatched = False
        try:
            result: tuple[int, Mapping[str, str], bytes] = self._store.transport(
                method, url, headers, body
            )
        except Exception:
            dispatched = True
        else:
            return result
        if dispatched and method == "PUT":
            raise BlobArchiveUncertain(f"ranking archive {what} outcome is unknown")
        raise BlobArchiveError(f"ranking archive {what} failed: storage unreachable")

    def create(self, name: str, data: bytes, meta: Mapping[str, str]) -> bool:
        """Create the record if it does not exist. True when created, False when it exists."""
        self._check(name)
        extra = {
            "x-ms-blob-type": "BlockBlob",
            "Content-Type": "application/json",
            "Content-Length": str(len(data)),
            "If-None-Match": "*",
        }
        extra.update({f"x-ms-meta-{k}": v for k, v in meta.items()})
        status, headers, _ = self._send("PUT", self._url(name), extra, data, "write")
        if status in (200, 201):
            return True
        if status == 412:
            return False
        if (
            status == 409
            and (_header(headers, "x-ms-error-code") or "BlobAlreadyExists") == "BlobAlreadyExists"
        ):
            return False
        if status == 408 or status >= 500:
            raise BlobArchiveUncertain(f"ranking archive write outcome is unknown (HTTP {status})")
        raise BlobArchiveError(f"ranking archive write refused (HTTP {status})")

    def read(self, name: str) -> tuple[bytes, dict[str, str]]:
        self._check(name)
        status, headers, body = self._send("GET", self._url(name), {}, None, "read")
        if status != 200:
            raise BlobArchiveError(f"ranking archive read refused (HTTP {status})")
        meta = {
            k.lower()[len("x-ms-meta-") :]: v
            for k, v in headers.items()
            if k.lower().startswith("x-ms-meta-")
        }
        return body, meta

    def names(self) -> list[str]:
        found: list[str] = []
        marker = ""
        for _ in range(_MAX_PAGES):
            query = {"restype": "container", "comp": "list", "prefix": "ranking-"}
            if marker:
                query["marker"] = marker
            url = f"{self._store.base}?{urllib.parse.urlencode(query)}"
            if self._store.sas:
                url = f"{url}&{self._store.sas}"
            status, _, body = self._send("GET", url, {}, None, "listing")
            if status != 200:
                raise BlobArchiveError(f"ranking archive listing refused (HTTP {status})")
            page, marker = _parse_listing(body)
            found += page
            if not marker:
                return sorted(found)
        raise BlobArchiveError("ranking archive listing did not finish")


def open_ranking_archive(
    env: Mapping[str, str], transport: Transport | None = None
) -> BlobRankingArchive | None:
    """The Blob archive selected by configuration, or None for the local folder adapter.

    Selecting Blob without a valid account URL and container refuses; it never falls back to a
    folder. Credentials follow the existing pattern: ZF_BLOB_SAS or the managed identity
    (ZF_BLOB_CLIENT_ID optional).
    """
    selected = (env.get(SELECTOR) or "").strip().lower()
    if selected in ("", "local"):
        return None
    if selected != "azure-blob":
        raise BlobArchiveError("ranking archive selection is not recognised")
    return BlobRankingArchive(
        env.get("ZF_BLOB_ACCOUNT_URL", ""),
        env.get(CONTAINER_VAR, ""),
        sas=env.get("ZF_BLOB_SAS"),
        client_id=env.get("ZF_BLOB_CLIENT_ID"),
        transport=transport,
        env=env,
    )


def from_environment(transport: Transport | None = None) -> BlobRankingArchive | None:
    """open_ranking_archive for the process environment."""
    return open_ranking_archive(os.environ, transport)
