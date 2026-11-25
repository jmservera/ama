"""Document content scanning, retention listing and legal hold (ADR 0002 decision 2, PRD DH-003, issue #117).

Scanning: an upload is checked before it can be read, downloaded or sent to the
document-reading assistant. A document is available only when its scan status
is "clean". Infected or type-mismatched content is deleted and never recorded.
A scanner that cannot answer yet (Defender for Storage is asynchronous) leaves
the document "pending", which is not available until a rescan returns clean.

* LocalSignatureScanner: development and tests only. It finds a labelled
  synthetic test marker and the standard EICAR test file, and checks that the bytes match the declared
  type. It is not an antivirus engine and gives no assurance about real malware.
* DefenderForStorageScanner: reads the blob index tag that Microsoft Defender
  for Storage on-upload malware scanning writes. Run only against a fake
  transport; nothing here has been run against a real storage account, and
  enabling Defender on the account is an open infrastructure item.

Retention: a job lists documents past their trigger. The periods below are
synthetic-demo placeholders, not an approved schedule (PR-003): the DPO and
Legal set the real periods. The job lists and never deletes. A named manager
approves each deletion; a legal hold on the case blocks it. The deletion is
audited by identifier, kind and approver, never by file name or content.

Choose the scanner with ZF_SCANNER=local (default) or defender.
"""
import logging
import os
import re
import urllib.parse
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from datetime import date, datetime, timedelta
from typing import Any

from . import controls
from .documents import AzureBlobDocumentStore, DocumentStoreError

SYNTHETIC = "synthetic-demo"
LOG = logging.getLogger(__name__)
TEST_MARKER = b"ZF-SYNTHETIC-MALWARE-TEST-MARKER"
EICAR_SIGNATURE = (b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$" + b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" + b"!$H+H*")
MANAGER_ROLES = ("Retrofit Programme Manager",)
MAGIC = {"pdf": (b"%PDF",), "png": (b"\x89PNG\r\n\x1a\n",), "jpg": (b"\xff\xd8\xff",), "jpeg": (b"\xff\xd8\xff",),
         "docx": (b"PK\x03\x04",), "xlsx": (b"PK\x03\x04",)}
DEFENDER_TAG = "Malware Scanning scan result"
DEFENDER_CLEAN = "No threats found"
DEFENDER_BAD = "Malicious"
VERDICTS = ("clean", "pending", "infected", "mismatch", "failed")
RETENTION_YEARS = {"EPC": 6, "Survey": 6, "Design": 6, "Consent": 3, "Funding evidence": 7, "Photo": 3, "Other": 1}
RETENTION_LABEL = (f"{SYNTHETIC} placeholder period from the trigger; not an approved retention schedule. "
                   "The DPO and Legal set the real periods (PR-003, OD-14).")
HOLD_REF = re.compile(r"^[A-Za-z0-9 ._:/-]{1,80}$")


class DocumentUnavailable(PermissionError):
    """The document has not passed the content scan."""


class Scanner:
    name = "none"

    def scan(self, case_id, doc_id, name, data, mime):
        """Return a two-string tuple (verdict, detail); verdict is clean, infected, mismatch or pending."""
        raise NotImplementedError


class LocalSignatureScanner(Scanner):
    name = f"local-signature ({SYNTHETIC})"

    def scan(self, case_id, doc_id, name, data, mime):
        if TEST_MARKER in data:
            return "infected", "synthetic malware test marker found"
        if EICAR_SIGNATURE in data:
            return "infected", "standard antivirus test file (EICAR) found"
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext in MAGIC and not any(data.startswith(m) for m in MAGIC[ext]):
            return "mismatch", f"content does not match the .{ext} type"
        if ext in ("csv", "txt") and b"\x00" in data:
            return "mismatch", f"content does not match the .{ext} type"
        return "clean", "no signature match"


class DefenderForStorageScanner(Scanner):
    name = "defender-for-storage"

    def __init__(self, store):
        if not isinstance(store, AzureBlobDocumentStore):
            raise ValueError("ZF_SCANNER=defender needs ZF_DOC_STORE=azure-blob.")
        self.store = store

    def scan(self, case_id, doc_id, name, data, mime):
        try:
            tags = self.store.tags(case_id, doc_id)
        except DocumentStoreError:
            return "pending", "scan result unavailable"
        result = tags.get(DEFENDER_TAG)
        if result == DEFENDER_CLEAN:
            return "clean", result
        if result == DEFENDER_BAD:
            return "infected", "Defender reported malicious content"
        return "pending", "scan result not yet written"


def open_scanner(docstore, env=None):
    env = os.environ if env is None else env
    kind = (env.get("ZF_SCANNER") or "local").lower()
    if kind == "local":
        if isinstance(docstore, AzureBlobDocumentStore):
            LOG.warning("Synthetic local scanner is guarding an Azure Blob store; it gives no malware assurance. "
                        "Enable Defender for Storage and set ZF_SCANNER=defender (issue #117).")
        return LocalSignatureScanner()
    if kind == "defender":
        return DefenderForStorageScanner(docstore)
    raise ValueError(f"Unknown ZF_SCANNER {kind!r}. Use local or defender.")


def blob_tags(store, case_id, doc_id):
    """Index tags of one blob, as {key: value}."""
    url = store._url(case_id, doc_id)
    url += ("&" if "?" in url else "?") + urllib.parse.urlencode({"comp": "tags"})
    status, _, body = store.transport("GET", url, store._headers(), None)
    if status != 200:
        raise DocumentStoreError(f"storage refused the tag read (HTTP {status})")
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        raise DocumentStoreError("unreadable blob tags")
    return {t.findtext("Key"): t.findtext("Value") for t in root.iter("Tag")}


AzureBlobDocumentStore.tags = blob_tags


def _day(text):
    return datetime.strptime(str(text)[:10], "%Y-%m-%d").date()


def _scan_result(result):
    if (type(result) is not tuple or len(result) != 2
            or type(result[0]) is not str or type(result[1]) is not str):
        raise RuntimeError("The scanner returned a malformed result; the document remains unavailable.")
    if result[0] not in VERDICTS:
        raise RuntimeError("The scanner returned an unsupported verdict; the document remains unavailable.")
    return result


def _valid_verdict(value: Any) -> str | None:
    return value if type(value) is str and value in VERDICTS else None


def scan_status(doc: Any) -> str | None:
    """Fail-closed malware scan status across nested scan and top-level scan_status."""
    if not isinstance(doc, Mapping):
        return None
    has_scan = "scan" in doc
    has_top = "scan_status" in doc
    if not has_scan and not has_top:
        return None
    nested: str | None = None
    if has_scan:
        raw_scan = doc["scan"]
        if not isinstance(raw_scan, Mapping):
            return None
        nested = _valid_verdict(raw_scan.get("status"))
        if nested is None:
            return None
    top: str | None = None
    if has_top:
        top = _valid_verdict(doc["scan_status"])
        if top is None:
            return None
    if has_scan and has_top and nested != top:
        if nested == "clean":
            return top
        if top == "clean":
            return nested
        return None
    return nested if has_scan else top


def is_clean_document(doc: Any) -> bool:
    return isinstance(doc, Mapping) and (doc.get("generated") is True or scan_status(doc) == "clean")


def is_clean_upload(doc: Any) -> bool:
    return isinstance(doc, Mapping) and not doc.get("generated") and scan_status(doc) == "clean"


def is_available_case_document(doc: Any) -> bool:
    if not isinstance(doc, Mapping):
        return False
    if doc.get("generated") is True:
        return True
    if doc.get("generated") is False or "scan" in doc or "scan_status" in doc:
        return scan_status(doc) == "clean"
    return True


def is_rescan_pending(doc: Any) -> bool:
    if not isinstance(doc, Mapping) or bool(doc.get("generated")):
        return False
    if "scan" not in doc and "scan_status" not in doc:
        return True
    return scan_status(doc) == "pending"


class DocControlsMixin:
    """Mixed into Store. Needs self.docstore, self.scanner, self.audit, self.save, self.lock and self._case."""

    def _manager(self, user, what):
        if isinstance(user, dict) and (
            any(k in user for k in ("sensor_id", "reading_id", "sensor_signal", "sensor_review_draft"))
            or str(user.get("source_type") or "").upper() in ("SENSOR", "IOT_HUB", "TELEMETRY")
            or any(controls.is_sensor_reference(user.get(k)) for k in ("email", "name", "code"))
        ):
            raise PermissionError(controls.SENSOR_REFUSAL)
        if user is None or user.get("role") not in MANAGER_ROLES:
            raise PermissionError(f"Only a programme manager can {what}.")

    def scan_new_document(self, case_id, did, name, data, mime):
        """Scan a stored upload. Returns the scan record; deletes the blob and raises on a bad verdict."""
        if self.scanner is None:
            raise RuntimeError("No content scanner is configured; the document remains unavailable.")
        verdict, detail = _scan_result(self.scanner.scan(case_id, did, name, data, mime))
        if verdict in ("infected", "mismatch"):
            self.docstore.delete(case_id, did)
            raise ValueError("That file failed the content check and was not kept." if verdict == "mismatch"
                             else "That file failed the malware scan and was not kept.")
        return dict(status=verdict, scanner=self.scanner.name, at=datetime.now().isoformat(timespec="seconds"), detail=detail)

    @staticmethod
    def require_clean(doc):
        if not is_clean_document(doc):
            raise DocumentUnavailable("This document is not available until it has passed the content scan.")

    def _remove_document(self, case_id, doc, action, who, detail):
        """Drop the record and save first; delete the blob only once the save has succeeded."""
        docs = self._case(case_id)["documents"]
        idx = docs.index(doc)
        docs.remove(doc)
        try:
            self.audit(who, action, case_id, detail)
            self.save()
        except Exception:
            docs.insert(idx, doc)
            raise
        self.docstore.delete(case_id, doc["id"])

    def _scan_stored(self, case_id, doc, who, *, remove_bad=True):
        """Scan a stored document (caller holds the lock). A missing scan field counts as pending. Returns the scan record."""
        if self.scanner is None:
            raise RuntimeError("No content scanner is configured; the document remains unavailable.")
        data = self.docstore.get(case_id, doc["id"])
        verdict, detail = _scan_result(self.scanner.scan(case_id, doc["id"], doc["name"], data, doc["mime"]))
        if remove_bad and verdict in ("infected", "mismatch"):
            self._remove_document(case_id, doc, "document_quarantined_deleted", who, f"{doc['id']}: {doc['kind']}: {verdict}")
            raise ValueError("That file failed the content check and was removed.")
        if hasattr(self, "_touch"):
            self._touch(case_id)
        doc["scan"] = dict(status=verdict, scanner=self.scanner.name, at=datetime.now().isoformat(timespec="seconds"), detail=detail)
        if "scan_status" in doc:
            doc["scan_status"] = verdict
        self.audit(who, "document_rescanned", case_id, f"{doc['id']}: {verdict}")
        self.save()
        return doc["scan"]

    def ensure_scanned(self, case_id, doc, who="system"):
        """Rescan on first use when the scan is missing (stored before scanning existed) or pending."""
        if not is_rescan_pending(doc):
            return
        self._scan_stored(case_id, doc, who)

    def rescan_pending(self, who="system"):
        """Job entry point: rescan every missing or pending document. Returns counts."""
        out = dict(checked=0, clean=0, pending=0, blocked=0, removed=0)
        with self.lock:
            for cid in list(self.cases):
                for d in list(self.cases[cid]["documents"]):
                    if not is_rescan_pending(d):
                        continue
                    out["checked"] += 1
                    try:
                        st = self._scan_stored(cid, d, who)["status"]
                        out[st if st in ("clean", "pending") else "blocked"] += 1
                    except ValueError:
                        out["removed"] += 1
                    except DocumentStoreError:
                        out["pending"] += 1
        return out

    def rescan_document(self, user, case_id, doc_id):
        self._doc_role(user, "rescan")
        with self.lock:
            doc = next((d for d in self._case(case_id)["documents"] if d["id"] == doc_id and not d.get("generated")), None)
            if not doc:
                raise KeyError(doc_id)
            return dict(self._scan_stored(case_id, doc, user["email"]))

    # ---- legal hold
    def place_legal_hold(self, user, case_id, reference):
        self._manager(user, "place a legal hold")
        if not isinstance(reference, str) and reference is not None:
            raise ValueError(controls.SENSOR_REFUSAL)
        ref = (reference or "").strip()
        if controls.is_sensor_reference(ref):
            raise ValueError(controls.SENSOR_REFUSAL)
        if not HOLD_REF.match(ref):
            raise ValueError("Give a short reference (letters, numbers and simple punctuation), not case details.")
        with self.lock:
            c = self._case(case_id)
            c["legal_hold"] = dict(active=True, reference=ref, by=user["name"], at=date.today().isoformat(),
                                   label=f"{SYNTHETIC}: a real hold needs the Legal delegate's decision")
            self.audit(user["email"], "legal_hold_placed", case_id, ref)
            self.save()
            return dict(c["legal_hold"])

    def release_legal_hold(self, user, case_id):
        self._manager(user, "release a legal hold")
        with self.lock:
            c = self._case(case_id)
            if not (c.get("legal_hold") or {}).get("active"):
                raise ValueError("There is no legal hold on this case.")
            if controls.is_sensor_reference((c.get("legal_hold") or {}).get("reference")):
                raise ValueError(controls.SENSOR_REFUSAL)
            c["legal_hold"] = dict(c["legal_hold"], active=False, released_by=user["name"], released_at=date.today().isoformat())
            self.audit(user["email"], "legal_hold_released", case_id, c["legal_hold"]["reference"])
            self.save()

    # ---- retention
    @staticmethod
    def _trigger(c, doc):
        """Retention runs from the case closing (or an explicit trigger), not from upload."""
        t = c.get("retention_trigger") or (c.get("stage_since") if c.get("closed") else None)
        return _day(t) if t else None

    def retention_due(self, user, today=None):
        """List documents past their trigger. Lists only; nothing is deleted."""
        self._manager(user, "list retention records")
        today = today or date.today()
        rows = []
        with self.lock:
            for c in self.cases.values():
                from .resident_decisions import RESIDENT_FIELDS, RESIDENT_RETENTION_ID, retention_schedule
                schedule = retention_schedule(c, today.isoformat())
                if schedule["expired"] and (any(c.get(key) for key in RESIDENT_FIELDS)
                                             or (c.get("decision") or {}).get("at")):
                    rows.append(dict(case_id=c["id"], doc_id=RESIDENT_RETENTION_ID,
                                     kind="Resident decisions", trigger=schedule["first_contact"],
                                     due=schedule["due"], status="blocked: legal hold" if
                                     (c.get("legal_hold") or {}).get("active") else "awaiting owner approval"))
                trig = None
                for d in c["documents"]:
                    if d.get("generated"):
                        continue
                    held = bool((c.get("legal_hold") or {}).get("active"))
                    try:
                        trig = self._trigger(c, d)
                    except (ValueError, TypeError):
                        # One unreadable date must not hide every other due record; list it for a person to fix.
                        rows.append(dict(case_id=c["id"], doc_id=d["id"], kind=d["kind"], trigger=None, due=None,
                                         status="blocked: legal hold" if held else "needs review: trigger date unreadable"))
                        continue
                    if trig is None:
                        continue
                    due = trig + timedelta(days=365 * RETENTION_YEARS.get(d["kind"], RETENTION_YEARS["Other"]))
                    if due > today:
                        continue
                    rows.append(dict(case_id=c["id"], doc_id=d["id"], kind=d["kind"], trigger=trig.isoformat(), due=due.isoformat(),
                                     status="blocked: legal hold" if held else "awaiting owner approval"))
        rows.sort(key=lambda r: (r["due"] or "", r["case_id"], r["doc_id"]))
        out = dict(label=RETENTION_LABEL, as_of=today.isoformat(), records=rows)
        detail = f"{len(rows)} due, {sum(r['status'].startswith('blocked') for r in rows)} held"
        try:
            with self.write_wait(self.BRIEFING_WRITE_WAIT_MS), self.lock:
                self.audit(user["email"], "retention_job_listed", "-", detail)
        except Exception as exc:
            from .mssqlstore import is_write_lock_busy

            if not is_write_lock_busy(exc):
                raise
            # A listing must not fail because other clients hold the SQL write lock (issue #2237): show it, say it
            # was not recorded, and let the next request record it.
            out.update(recorded=False, note="The list is shown but this view was not saved to the record because the record is busy. Refresh in a moment.")
        return out

    def approve_retention_deletion(self, user, case_id, doc_id, today=None):
        """Owner approval for one due document. A legal hold blocks it. The log keeps no file name or content."""
        from .resident_decisions import RESIDENT_RETENTION_ID
        if doc_id == RESIDENT_RETENTION_ID:
            return self.delete_resident_records(user, case_id, (today or date.today()).isoformat())
        self._manager(user, "approve a retention deletion")
        today = today or date.today()
        with self.lock:
            c = self._case(case_id)
            if (c.get("legal_hold") or {}).get("active"):
                self.audit(user["email"], "retention_delete_blocked_legal_hold", case_id, doc_id)
                raise PermissionError("A legal hold is in place on this case (its documents must be kept for a legal reason), "
                                      "so nothing was deleted. Keep the documents. This system only records the hold; "
                                      "a real hold needs the Legal delegate's decision, and a programme manager can record "
                                      "its release once the hold has ended.")
            doc = next((d for d in c["documents"] if d["id"] == doc_id and not d["generated"]), None)
            if not doc:
                raise KeyError(doc_id)
            try:
                trig = self._trigger(c, doc)
            except (ValueError, TypeError):
                raise ValueError("The retention start date on this case cannot be read, so nothing was deleted. "
                                 "Keep the document and correct the case closing date or retention start date.")
            if trig is None or trig + timedelta(days=365 * RETENTION_YEARS.get(doc["kind"], 1)) > today:
                raise ValueError("This document is not due for deletion, so nothing was deleted. Its retention period "
                                 "(demonstration values, not an approved schedule) counts from the date the case closed "
                                 "or a recorded retention start date, and that date is missing or the period has not ended. "
                                 "Keep the document and check the case closing date or retention start date.")
            self._remove_document(case_id, doc, "retention_deleted", user["email"], f"{doc_id}: {doc['kind']}: approved by {user['name']}")
