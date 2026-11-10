"""Durable projection of refused import files for the exception register (#135, FR-029).

The importer owns its refusal ledger. A reviewed local adapter hands this store a bounded copy of
each refused file: source name, content digest when one is known, reason and time. The register
reads that copy, so no request ever reads a file path, and nothing here retries, approves or
changes the refused file. A repeated transfer of the same refusal changes nothing.
"""

import re
from collections.abc import Iterable, Mapping
from typing import Any

KEY = "import_exceptions"
MAX_REFUSALS = 500
NAME_MAX = 400
REASON_MAX = 400
AT_MAX = 32
DIGEST = re.compile(r"[0-9a-f]{64}")


class PartiallyRecordedError(RuntimeError):
    """The refusals are durable but the success audit entry is not."""


def ref_of(refusal: Mapping[str, Any]) -> str:
    """The feed's own key for a refusal, so the register and the transfer agree on identity."""
    return f"file:{refusal['source_sha256'] or refusal['source_name']}"


def _bounded(value: Any, label: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"A refused import needs {label}.")
    if len(value) > limit:
        raise ValueError(f"A refused import's {label} is longer than {limit} characters.")
    return value


def normalise(raw: Mapping[str, Any]) -> dict[str, str]:
    """A clean copy of exactly the fields the register keeps. Anything else is dropped."""
    if not isinstance(raw, Mapping):
        raise ValueError("A refused import must be a record.")
    digest = raw.get("source_sha256") or ""
    if not isinstance(digest, str) or (digest and not DIGEST.fullmatch(digest)):
        raise ValueError("A refused import's content digest must be 64 lowercase hex characters.")
    return {
        "source_name": _bounded(raw.get("source_name"), "a source name", NAME_MAX),
        "source_sha256": digest,
        "reason": _bounded(raw.get("reason"), "a reason", REASON_MAX),
        "at": _bounded(raw.get("at"), "a refusal time", AT_MAX),
    }


def load(data: Mapping[str, Any]) -> list[dict[str, str]] | None:
    """Transferred refusals, None when nothing was ever transferred. A damaged document raises."""
    doc = data.get(KEY)
    if doc is None:
        return None
    if not isinstance(doc, Mapping) or not isinstance(doc.get("refusals"), list):
        raise ValueError("The transferred import refusals could not be read.")
    return [normalise(r) for r in doc["refusals"]]


class ImportRefusalsMixin:
    data: dict[str, Any]
    lock: Any

    def record_import_refusals(self, refusals: Iterable[Mapping[str, Any]]) -> dict[str, int]:
        """Keep each new refusal once. The first copy of a ref stays; nothing is overwritten."""
        clean = [normalise(r) for r in refusals]
        with self.lock:
            kept = load(self.data) or []
            known = {ref_of(r) for r in kept}
            added = 0
            for refusal in clean:
                ref = ref_of(refusal)
                if ref not in known:
                    known.add(ref)
                    kept.append(refusal)
                    added += 1
            if len(kept) > MAX_REFUSALS:
                raise ValueError(
                    f"At most {MAX_REFUSALS} refused imports are kept here; nothing was recorded."
                )
            if added:
                self._persist_import_refusals({"refusals": kept}, f"added={added}")
            return {"added": added, "already_present": len(clean) - added, "total": len(kept)}

    def _persist_import_refusals(self, document: dict[str, Any], detail: str) -> None:
        """Publish the document only once it is saved, then audit. SqlStore replaces this.

        A failed save restores the previous document and writes no success audit. The JSON
        store keeps its document and audit in two files, so a failed audit after a durable save
        is reported as a partial outcome, not as nothing recorded."""
        previous = self.data.get(KEY)
        self.data[KEY] = document
        try:
            self.save()  # type: ignore[attr-defined]
        except BaseException:
            if previous is None:
                self.data.pop(KEY, None)
            else:
                self.data[KEY] = previous
            raise
        try:
            self.audit("importer", "recorded_import_refusals", "-", detail)  # type: ignore[attr-defined]
        except Exception as error:
            raise PartiallyRecordedError(
                "The refused imports were saved, but their audit entry was not written."
            ) from error
