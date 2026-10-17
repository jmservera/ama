"""Document content scanning, retention listing and legal hold (ADR 0002 decision 2, PRD DH-003, issue #117).

Scanning: an upload is checked before it can be read, downloaded or sent to the
document-reading assistant. A document is available only when its scan status
is "clean". Infected or type-mismatched content is deleted and never recorded.
A scanner that cannot answer yet (Defender for Storage is asynchronous) leaves
the document "pending", which is not available until a rescan returns clean.

* LocalSignatureScanner: development and tests only. It finds a labelled
  synthetic test marker and checks that the bytes match the declared type. It is
  not an antivirus engine and gives no assurance about real malware.
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
import os
import re
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta

from .documents import AzureBlobDocumentStore, DocumentStoreError

SYNTHETIC = "synthetic-demo"
TEST_MARKER = b"ZF-SYNTHETIC-MALWARE-TEST-MARKER"
MANAGER_ROLES = ("Retrofit Programme Manager",)
MAGIC = {"pdf": (b"%PDF",), "png": (b"\x89PNG\r\n\x1a\n",), "jpg": (b"\xff\xd8\xff",), "jpeg": (b"\xff\xd8\xff",),
         "docx": (b"PK\x03\x04",), "xlsx": (b"PK\x03\x04",)}
DEFENDER_TAG = "Malware Scanning scan result"
DEFENDER_CLEAN = "No threats found"
DEFENDER_BAD = "Malicious"
RETENTION_YEARS = {"EPC": 6, "Survey": 6, "Design": 6, "Consent": 3, "Funding evidence": 7, "Photo": 3, "Other": 1}
RETENTION_LABEL = (f"{SYNTHETIC} placeholder period from the trigger; not an approved retention schedule. "
                   "The DPO and Legal set the real periods (PR-003, OD-14).")
HOLD_REF = re.compile(r"^[A-Za-z0-9 ._:/-]{1,80}$")


class DocumentUnavailable(PermissionError):
    """The document has not passed the content scan."""


class Scanner:
    name = "none"

    def scan(self, case_id, doc_id, name, data, mime):
        """Return (verdict, detail); verdict is clean, infected, mismatch or pending."""
        raise NotImplementedError


class LocalSignatureScanner(Scanner):
    name = f"local-signature ({SYNTHETIC})"

    def scan(self, case_id, doc_id, name, data, mime):
        if TEST_MARKER in data:
            return "infected", "synthetic malware test marker found"
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


class DocControlsMixin:
    """Mixed into Store. Needs self.docstore, self.scanner, self.audit, self.save, self.lock and self._case."""

    def _manager(self, user, what):
        if user is None or user.get("role") not in MANAGER_ROLES:
            raise PermissionError(f"Only a programme manager can {what}.")

    def scan_new_document(self, case_id, did, name, data, mime):
        """Scan a stored upload. Returns the scan record; deletes the blob and raises on a bad verdict."""
        verdict, detail = self.scanner.scan(case_id, did, name, data, mime)
        if verdict in ("infected", "mismatch"):
            self.docstore.delete(case_id, did)
            raise ValueError("That file failed the content check and was not kept." if verdict == "mismatch"
                             else "That file failed the malware scan and was not kept.")
        return dict(status=verdict, scanner=self.scanner.name, at=datetime.now().isoformat(timespec="seconds"), detail=detail)

    @staticmethod
    def require_clean(doc):
        scan = doc.get("scan") or {}
        if not doc.get("generated") and scan.get("status") != "clean":
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
        data = self.docstore.get(case_id, doc["id"])
        verdict, detail = self.scanner.scan(case_id, doc["id"], doc["name"], data, doc["mime"])
        if verdict not in ("clean", "pending", "infected", "mismatch"):
            raise RuntimeError("The scanner returned an unsupported verdict; the document remains unavailable.")
        if remove_bad and verdict in ("infected", "mismatch"):
            self._remove_document(case_id, doc, "document_quarantined_deleted", who, f"{doc['id']}: {doc['kind']}: {verdict}")
            raise ValueError("That file failed the content check and was removed.")
        doc["scan"] = dict(status=verdict, scanner=self.scanner.name, at=datetime.now().isoformat(timespec="seconds"), detail=detail)
        self.audit(who, "document_rescanned", case_id, f"{doc['id']}: {verdict}")
        self.save()
        return doc["scan"]

    def ensure_scanned(self, case_id, doc, who="system"):
        """Rescan on first use when the scan is missing (stored before scanning existed) or pending."""
        if doc.get("generated") or (doc.get("scan") or {}).get("status", "pending") != "pending":
            return
        self._scan_stored(case_id, doc, who)

    def rescan_pending(self, who="system"):
        """Job entry point: rescan every missing or pending document. Returns counts."""
        out = dict(checked=0, clean=0, pending=0, removed=0)
        with self.lock:
            for cid in list(self.cases):
                for d in list(self.cases[cid]["documents"]):
                    if d.get("generated") or (d.get("scan") or {}).get("status", "pending") != "pending":
                        continue
                    out["checked"] += 1
                    try:
                        st = self._scan_stored(cid, d, who)["status"]
                        out["clean" if st == "clean" else "pending"] += 1
                    except ValueError:
                        out["removed"] += 1
                    except DocumentStoreError:
                        out["pending"] += 1
        return out

    def rescan_document(self, user, case_id, doc_id):
        self._doc_role(user, "rescan")
        with self.lock:
            doc = next((d for d in self._case(case_id)["documents"] if d["id"] == doc_id and not d["generated"]), None)
            if not doc:
                raise KeyError(doc_id)
            return dict(self._scan_stored(case_id, doc, user["email"]))

    # ---- legal hold
    def place_legal_hold(self, user, case_id, reference):
        self._manager(user, "place a legal hold")
        ref = (reference or "").strip()
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
                    trig = self._trigger(c, d)
                    if trig is None:
                        continue
                    due = trig + timedelta(days=365 * RETENTION_YEARS.get(d["kind"], RETENTION_YEARS["Other"]))
                    if due > today:
                        continue
                    held = bool((c.get("legal_hold") or {}).get("active"))
                    rows.append(dict(case_id=c["id"], doc_id=d["id"], kind=d["kind"], trigger=trig.isoformat(), due=due.isoformat(),
                                     status="blocked: legal hold" if held else "awaiting owner approval"))
            self.audit(user["email"], "retention_job_listed", "-", f"{len(rows)} due, {sum(r['status'].startswith('blocked') for r in rows)} held")
        rows.sort(key=lambda r: (r["due"], r["case_id"], r["doc_id"]))
        return dict(label=RETENTION_LABEL, as_of=today.isoformat(), records=rows)

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
                raise PermissionError("A legal hold blocks deletion on this case.")
            doc = next((d for d in c["documents"] if d["id"] == doc_id and not d["generated"]), None)
            if not doc:
                raise KeyError(doc_id)
            trig = self._trigger(c, doc)
            if trig is None or trig + timedelta(days=365 * RETENTION_YEARS.get(doc["kind"], 1)) > today:
                raise ValueError("This document is not past its retention trigger.")
            self._remove_document(case_id, doc, "retention_deleted", user["email"], f"{doc_id}: {doc['kind']}: approved by {user['name']}")
