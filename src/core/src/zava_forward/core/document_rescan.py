"""Bounded SQL rescan pages; worker results never delete bytes or release holds."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from .change_provenance import CommittedOutcomeError
from .documents import DocumentStoreError
from .store import ConflictError

WORKER = "system:document-rescan"
Record = dict[str, Any]
Key = tuple[str, str]


def mark_committed(store: Any) -> None:
    context = getattr(store.local, "document_rescan", None)
    if context is not None:
        context["committed"] = True


def _pending(doc: Record) -> bool:
    return (
        not doc.get("generated") and (doc.get("scan") or {}).get("status", "pending") == "pending"
    )


@contextmanager
def _attempt(store: Any) -> Iterator[None]:
    store._touched()
    prior = list(store.local.pending)
    previous = getattr(store.local, "document_rescan", None)
    context = {"committed": False}
    store.local.document_rescan = context
    try:
        yield
    except BaseException as error:
        if context["committed"]:
            store.local.pending.clear()
            store._touched().clear()
            store._seq = -1
            raise CommittedOutcomeError(
                "The rescan committed. Reload its scan and audit before retrying."
            ) from error
        try:
            with store.dblock:
                store._discard(prior)
        except Exception:
            error.add_note("Rescan recovery failed; reload persisted records before retrying.")
            logging.getLogger(__name__).error("Document rescan recovery failed")
        raise
    finally:
        store.local.document_rescan = previous


def run(store: Any, *, limit: int = 100, after: Key | None = None) -> Record:
    """Consume one keyset page, including skipped keys; start each new sweep without a cursor."""
    if not hasattr(store, "db"):
        raise ValueError("Document rescan jobs require a SQL case store.")
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("Document rescan limit must be from 1 to 100.")
    if after is not None and (
        not isinstance(after, tuple)
        or len(after) != 2
        or any(not isinstance(part, str) or not part.strip() for part in after)
    ):
        raise ValueError("Document rescan cursor requires case and document identifiers.")
    with store.lock:
        keys = sorted(
            (cid, doc["id"])
            for cid, case in store.cases.items()
            for doc in case["documents"]
            if _pending(doc) and (after is None or (cid, doc["id"]) > after)
        )
    page = keys[:limit]
    report: Record = dict(
        checked=0, clean=0, pending=0, blocked=0, skipped=0, failed=0, committed=0
    )
    report["next_after"] = list(page[-1]) if len(keys) > limit else None
    for cid, did in page:
        try:
            with store.lock, _attempt(store):
                case = store._case(cid)
                doc = next((d for d in case["documents"] if d["id"] == did), None)
                if doc is None or not _pending(doc):
                    report["skipped"] += 1
                    continue
                report["checked"] += 1
                result = store._scan_stored(cid, doc, WORKER, remove_bad=False)
                status = result["status"]
                report[status if status in ("clean", "pending") else "blocked"] += 1
        except CommittedOutcomeError:
            report["committed"] += 1
            logging.getLogger(__name__).error(
                "DOCUMENT_RESCAN_COMMITTED: reload scan and audit before retrying"
            )
        except (
            DocumentStoreError,
            OSError,
            ValueError,
            KeyError,
            RuntimeError,
            TypeError,
            ConflictError,
            store.dberror,
        ):
            report["failed"] += 1
            logging.getLogger(__name__).error(
                "DOCUMENT_RESCAN_FAILED: document unavailable; retry a new sweep"
            )
    return report
