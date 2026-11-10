"""Runtime StateStore for the aftercare service over the existing Store and SqlStore documents.

The receipt, register and request-id index live in one JSON document under one namespace of the
store's document mechanism, so they are replaced together in one save. SqlStore compares the
document with the snapshot it loaded inside the save transaction and refuses a stale write; the
JSON Store replaces its single live file under its process lock and does not protect against a
second Store instance on the same file. The mutator is called once and is never rerun.

A failed save is classified by re-reading the persisted document. Only a proven unchanged
document reports "nothing was saved". A matching, different or unreadable document reports an
unconfirmed write so the caller sends the same request reference again and the service replays it.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from typing import Any, TypeVar

from .aftercare_intake import ConflictError, PersistenceError
from .store import ConflictError as StoreConflict

T = TypeVar("T")

NAMESPACE = "aftercare"

UNCONFIRMED = (
    "We could not confirm whether this was saved. Check the concerns list, then send it again "
    "with the same request reference. It will not be recorded twice."
)


class UnconfirmedWriteError(PersistenceError):
    """The write may or may not have committed. Never report it as not saved."""


def _canon(value: Any) -> str | None:
    return None if value is None else json.dumps(value, sort_keys=True)


class DocumentStateStore:
    def __init__(self, store: Any, key: str = NAMESPACE) -> None:
        self.store = store
        self.key = key

    def read(self) -> str | None:
        with self.store.lock:
            return _canon(self.store.data.get(self.key))

    def _persisted(self) -> str | None:
        store = self.store
        if hasattr(store, "db"):
            with store.dblock:
                row = store.db.execute("SELECT value FROM meta WHERE key=?", (self.key,)).fetchone()
            return None if row is None else _canon(json.loads(row[0]))
        if not os.path.exists(store.live_path):
            return None
        with open(store.live_path, encoding="utf-8") as handle:
            return _canon(json.load(handle).get(self.key))

    def _restore(self, text: str | None) -> None:
        if text is None:
            self.store.data.pop(self.key, None)
        else:
            self.store.data[self.key] = json.loads(text)

    def update(self, mutator: Callable[[str | None], tuple[str, T]]) -> T:
        previous: str | None = None
        attempted: str | None = None
        result: T
        try:
            with self.store.lock:
                previous = _canon(self.store.data.get(self.key))
                text, result = mutator(previous)
                if _canon(json.loads(text)) == previous:
                    return result
                attempted = _canon(json.loads(text))
                self.store.data[self.key] = json.loads(text)
                self.store.save()
        except Exception as exc:
            if attempted is None:
                raise
            error = self._classify(exc, previous, attempted)
            raise error from (error.__cause__ or exc)
        return result

    def _classify(self, exc: Exception, previous: str | None, attempted: str | None) -> Exception:
        try:
            persisted = self._persisted()
        except Exception as reload_error:
            error = UnconfirmedWriteError(UNCONFIRMED)
            error.add_note(
                f"Reload failed ({type(reload_error).__name__}); "
                f"save failure was {type(exc).__name__}."
            )
            error.__cause__ = reload_error
            return error
        refresh: Exception | None = None
        try:
            with self.store.lock:
                self._restore(persisted)
        except Exception as restore_error:
            refresh = restore_error
        committed = persisted == attempted or bool(getattr(exc, "committed", False))
        if isinstance(exc, StoreConflict) and persisted != attempted:
            return ConflictError(
                "Another update was saved first, so nothing from this request was saved. "
                "Check the concerns list, then send it again."
            )
        if persisted == previous and not committed and refresh is None:
            return PersistenceError("The record could not be saved. Nothing was saved.")
        error = UnconfirmedWriteError(UNCONFIRMED)
        if refresh is not None:
            error.add_note(
                f"Refresh failed ({type(refresh).__name__}); "
                f"{type(exc).__name__} was raised by save."
            )
        return error
