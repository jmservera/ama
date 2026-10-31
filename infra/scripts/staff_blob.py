"""Private Blob result transport for the in-VNet SQL staff job.

The worker writes AES-GCM protected pages to a private container with its managed identity.
The controller reads them with Entra credentials from a host that can reach the private
endpoint. Every ambiguity is an explicit refusal: there is no tag, console or public fallback.
"""

from __future__ import annotations

import base64
import json
import os
import re
import threading
import time
from typing import Any

CONTAINER = "staff-results"
SCHEMA = "zava-forward-staff-result-1"
VERSION = 2
PAGE_BYTES = 48 * 1024
MAX_PAGES = 64
MAX_BLOB = 128 * 1024
TTL = 900
SKEW = 60
ACCOUNT_URL = re.compile(r"https://[a-z0-9]{3,24}\.blob\.core\.windows\.net")
PAGED = "candidates"
HEADER = {
    "v",
    "run",
    "op",
    "digest",
    "image",
    "schema",
    "index",
    "count",
    "items",
    "bytes",
    "created",
    "not_after",
    "paged",
}


PREFLIGHT_BUDGET = 45.0
READ_BUDGET = 45.0
LIST_TIMEOUT = 20
BLOB_TIMEOUT = 20


class StaffJobError(Exception):
    """Sanitized job failure, including uncertain SQL or cleanup outcomes."""


def _bounded(call: Any, deadline: float, message: str) -> Any:
    """Enforce an overall deadline on a blocking SDK call.

    The synchronous SDK cannot be interrupted, so the call runs in a daemon thread that is
    abandoned on expiry. Only read-only calls are run this way and their late result is discarded.
    """
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise StaffJobError(message)
    box: dict[str, Any] = {}

    def run() -> None:
        try:
            box["value"] = call()
        except BaseException as error:  # noqa: BLE001 - re-raised in the caller below
            box["error"] = error

    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    worker.join(remaining)
    if worker.is_alive():
        raise StaffJobError(message)
    if "error" in box:
        raise box["error"]
    return box["value"]


def account_url(value: Any) -> str:
    if not isinstance(value, str) or not ACCOUNT_URL.fullmatch(value.rstrip("/")):
        raise StaffJobError("Private result Blob account URL is not an exact public-cloud account.")
    return value.rstrip("/")


def blob_name(run: str, index: int) -> str:
    return f"{run}/page-{index:03d}.json"


def _aad(header: dict[str, Any]) -> bytes:
    return json.dumps(header, sort_keys=True, separators=(",", ":")).encode()


def _compact(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def split_pages(result: dict[str, Any]) -> tuple[list[dict[str, Any]], int, int]:
    """Return plaintext pages, item count and measured plaintext bytes; never truncate."""
    items = result.get(PAGED)
    head = {k: v for k, v in result.items() if k != PAGED}
    if items is not None and not isinstance(items, list):
        raise StaffJobError("Staff result paged field is not a list; no result was disclosed.")
    items = items or []
    pages: list[dict[str, Any]] = [{"head": head, "items": []}]
    size = len(_compact(pages[0]))
    if size > PAGE_BYTES:
        raise StaffJobError("Staff result head exceeds one page; no result was disclosed.")
    empty_size = len(_compact({"items": []}))
    for item in items:
        length = len(_compact(item))
        if empty_size + length > PAGE_BYTES:
            raise StaffJobError("Staff result item exceeds one page; no result was disclosed.")
        addition = length + bool(pages[-1]["items"])
        if size + addition > PAGE_BYTES:
            pages.append({"items": []})
            size = empty_size
            addition = length
        if len(pages) > MAX_PAGES:
            raise StaffJobError(
                "Staff result exceeds the bounded page set; no result was disclosed."
            )
        pages[-1]["items"].append(item)
        size += addition
    sizes = [len(_compact(page)) for page in pages]
    if any(size > PAGE_BYTES for size in sizes):
        raise StaffJobError("Staff result exceeds the bounded page set; no result was disclosed.")
    return pages, len(items), sum(sizes)


def encode_pages(
    request: dict[str, Any], result: dict[str, Any], now: float | None = None
) -> list[tuple[str, bytes]]:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    created = int(time.time() if now is None else now)
    pages, items, size = split_pages(result)
    key = base64.b64decode(request["key"], validate=True)
    out = []
    for index, page in enumerate(pages):
        header = {
            "v": VERSION,
            "run": request["run"],
            "op": request["operation"],
            "digest": request["digest"],
            "image": request["image"],
            "schema": SCHEMA,
            "index": index,
            "count": len(pages),
            "items": items,
            "bytes": size,
            "created": created,
            "not_after": created + TTL,
            "paged": PAGED if PAGED in result else None,
        }
        nonce = os.urandom(12)
        ciphertext = AESGCM(key).encrypt(nonce, _compact(page), _aad(header))
        body = _compact(
            {
                **header,
                "nonce": base64.b64encode(nonce).decode(),
                "ct": base64.b64encode(ciphertext).decode(),
            }
        )
        if len(body) > MAX_BLOB:
            raise StaffJobError(
                "Staff result page exceeds the Blob bound; no result was disclosed."
            )
        out.append((blob_name(request["run"], index), body))
    return out


def write_result(container: Any, request: dict[str, Any], result: dict[str, Any]) -> None:
    """Write every page without overwrite; a partial write is reported by the caller."""
    pages = encode_pages(request, result)
    for name, body in pages:
        container.upload_blob(name, body, overwrite=False, length=len(body))


def _list(container: Any, run: str) -> dict[int, int]:
    pattern = re.compile(re.escape(run) + r"/page-(\d{3})\.json")
    found: dict[int, int] = {}
    for blob in container.list_blobs(name_starts_with=run + "/", timeout=LIST_TIMEOUT):
        name = blob["name"] if isinstance(blob, dict) else blob.name
        size = blob["size"] if isinstance(blob, dict) else blob.size
        match = pattern.fullmatch(name)
        if not match or int(match[1]) in found or type(size) is not int:
            raise StaffJobError("Private result Blob names are ambiguous; result refused.")
        found[int(match[1])] = size
        if len(found) > MAX_PAGES:
            raise StaffJobError("Private result Blob page count exceeds the bound; result refused.")
    return found


def preflight(container: Any, request: dict[str, Any], deadline: float | None = None) -> None:
    """Prove the private route and an empty run prefix before any secret leaves the host."""
    limit = time.monotonic() + PREFLIGHT_BUDGET
    limit = limit if deadline is None else min(limit, deadline)
    try:
        existing = _bounded(
            lambda: _list(container, request["run"]),
            limit,
            "Private result Blob did not answer within the time budget. Use an authorized "
            "private-connected host; no job was created and no fallback exists.",
        )
    except StaffJobError:
        raise
    except Exception:
        raise StaffJobError(
            "Private result Blob is unreachable or unauthorized from this host. Use an "
            "authorized private-connected host; no job was created and no fallback exists."
        ) from None
    if existing:
        raise StaffJobError("Private result Blob prefix is not empty; no job was created.")


def read_result(
    container: Any,
    request: dict[str, Any],
    now: float | None = None,
    deadline: float | None = None,
) -> dict[str, Any] | None:
    """Return None only when no page exists; anything partial or inconsistent is refused."""
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    clock = time.time() if now is None else now
    limit = time.monotonic() + READ_BUDGET
    limit = limit if deadline is None else min(limit, deadline)
    expired = "Private result Blob read exceeded its time budget; outcome is unverified."
    try:
        found = _bounded(lambda: _list(container, request["run"]), limit, expired)
    except StaffJobError:
        raise
    except Exception:
        raise StaffJobError(
            "Private result Blob could not be read; outcome is unverified."
        ) from None
    if not found:
        return None
    count = len(found)
    if sorted(found) != list(range(count)) or any(not 0 < s <= MAX_BLOB for s in found.values()):
        raise StaffJobError("Private result Blob page set is incomplete or oversized; refused.")
    key = base64.b64decode(request["key"], validate=True)
    pages: list[dict[str, Any]] = []
    first: dict[str, Any] | None = None
    try:
        for index in range(count):
            name = blob_name(request["run"], index)
            raw = _bounded(
                lambda name=name: container.download_blob(
                    name, offset=0, length=MAX_BLOB + 1, timeout=BLOB_TIMEOUT
                ).read(MAX_BLOB + 1),
                limit,
                expired,
            )
            if len(raw) > MAX_BLOB or len(raw) != found[index]:
                raise ValueError
            record = json.loads(raw)
            if not isinstance(record, dict) or set(record) != HEADER | {"nonce", "ct"}:
                raise ValueError
            header = {k: record[k] for k in HEADER}
            first = first or header
            fixed = (
                *("v", "run", "op", "digest", "image", "schema", "count", "items", "bytes"),
                *("created", "not_after", "paged"),
            )
            expected = {
                "v": VERSION,
                "run": request["run"],
                "op": request["operation"],
                "digest": request["digest"],
                "image": request["image"],
                "schema": SCHEMA,
                "count": count,
            }
            if (
                any(header[k] != v for k, v in expected.items())
                or header["index"] != index
                or any(header[k] != first[k] for k in fixed)
                or any(type(header[k]) is not int for k in ("index", "count", "items", "bytes"))
                or type(header["created"]) is not int
                or type(header["not_after"]) is not int
                or header["not_after"] - header["created"] != TTL
                or header["created"] > clock + SKEW
                or header["paged"] not in (None, PAGED)
            ):
                raise ValueError
            plain = AESGCM(key).decrypt(
                base64.b64decode(record["nonce"], validate=True),
                base64.b64decode(record["ct"], validate=True),
                _aad(header),
            )
            page = json.loads(plain)
            if (
                not isinstance(page, dict)
                or set(page) - {"head", "items"}
                or not isinstance(page.get("items"), list)
                or ("head" in page) != (index == 0)
            ):
                raise ValueError
            pages.append(page)
    except StaffJobError:
        raise
    except (ValueError, KeyError, TypeError, InvalidTag):
        raise StaffJobError("Private result Blob could not be authenticated; refused.") from None
    except Exception:
        raise StaffJobError(
            "Private result Blob could not be read; outcome is unverified."
        ) from None
    assert first is not None
    if first["not_after"] < clock:
        raise StaffJobError("Private result Blob result expired; refused.")
    items = [item for page in pages for item in page["items"]]
    if (
        len(items) != first["items"]
        or sum(len(_compact(p)) for p in pages) != first["bytes"]
        or (first["paged"] is None and items)
    ):
        raise StaffJobError("Private result Blob totals do not match; result refused.")
    value = dict(pages[0]["head"])
    if first["paged"]:
        value[PAGED] = items
    if (
        type(value.get("version")) is not int
        or value["version"] != 1
        or value.get("run") != request["run"]
        or value.get("operation") != request["operation"]
    ):
        raise StaffJobError("Private result Blob schema is invalid; refused.")
    return value
