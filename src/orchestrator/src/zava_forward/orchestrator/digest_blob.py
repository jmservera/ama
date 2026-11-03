"""Ledger digests in an immutable Azure Blob container, and the scheduled verification of the ledger against them.

The container (`ledger-digests`) has a locked time-based retention policy, so a digest cannot be
overwritten or deleted by the application or an administrator before retention ends. Publishing
uploads every local digest that is not yet in the container (create-only, If-None-Match: *).
Verification reads the digests back from the container, not from local files, and checks the
ledger against them. A mismatch prints one LEDGER_DIGEST_ALERT line (picked up by a log alert in
Azure) and exits non-zero so the job run shows as failed.

Configure with ZF_DIGEST_ACCOUNT_URL, ZF_DIGEST_CONTAINER (default ledger-digests) and
ZF_DIGEST_CLIENT_ID (managed identity). ZF_DIGEST_SAS is for local tests only.
"""
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

from zava_forward.core import ledger
from zava_forward.core.documents import AzureBlobDocumentStore, DocumentStoreError

ALERT_MARKER = "LEDGER_DIGEST_ALERT"
OK_MARKER = "LEDGER_DIGEST_OK"
RECONCILE_OK_MARKER = "LEDGER_DIGEST_RECONCILE_OK"
RECONCILE_ALERT_MARKER = "LEDGER_DIGEST_RECONCILE_ALERT"


class InvalidDigestError(DocumentStoreError):
    """Remote digest bytes cannot supply anchor evidence."""


def _valid_anchor_name(name):
    return re.fullmatch(
        r"(?:digest-(?:[0-9]{10}|[1-9][0-9]{10,})|year-(?!0000)[0-9]{4})\.json", name
    ) is not None


def _valid_anchor(name, digest):
    if not isinstance(digest, dict):
        return False
    count = digest.get("count")
    head = digest.get("head")
    if (digest.get("chain") != "main" or digest.get("algorithm") != "sha256"
            or type(count) is not int or count < 0
            or not isinstance(head, str) or re.fullmatch(r"[0-9a-f]{64}", head) is None):
        return False
    if name.startswith("digest-"):
        return name == f"digest-{count:010d}.json" and (count != 0 or head == ledger.GENESIS)
    year = digest.get("year")
    first_prev = digest.get("first_prev")
    return (isinstance(year, str) and re.fullmatch(r"[0-9]{4}", year) is not None
            and year != "0000" and name == f"year-{year}.json" and count > 0
            and isinstance(first_prev, str) and re.fullmatch(r"[0-9a-f]{64}", first_prev) is not None)


class BlobDigestStore(AzureBlobDocumentStore):
    """Create-only digest blobs named digest-NNNNNNNNNN.json and year-YYYY.json at the container root."""

    def _blob_url(self, name):
        url = f"{self.base}/{urllib.parse.quote(name)}"
        return f"{url}?{self.sas}" if self.sas else url

    def put_digest(self, name, digest):
        """Upload once. Returns True when written, False when the blob already exists."""
        data = json.dumps(digest, sort_keys=True).encode()
        h = self._headers({"x-ms-blob-type": "BlockBlob", "Content-Type": "application/json",
                           "Content-Length": str(len(data)), "If-None-Match": "*"})
        status, _, _ = self.transport("PUT", self._blob_url(name), h, data)
        if status in (200, 201):
            return True
        if status in (409, 412):
            return False
        raise DocumentStoreError(f"digest container refused the upload (HTTP {status})")

    def list_digests(self):
        names, marker = [], None
        while True:
            q = {"restype": "container", "comp": "list"}
            if marker:
                q["marker"] = marker
            url = f"{self.base}?{urllib.parse.urlencode(q)}" + (f"&{self.sas}" if self.sas else "")
            status, _, body = self.transport("GET", url, self._headers(), None)
            if status != 200:
                raise DocumentStoreError(f"digest container refused the listing (HTTP {status})")
            try:
                root = ET.fromstring(body)
            except ET.ParseError:
                raise DocumentStoreError("unreadable digest listing")
            names += [n.text for n in root.iter("Name") if n.text and (
                n.text.endswith(".json") or n.text.startswith(("digest-", "year-")))]
            marker = (root.findtext("NextMarker") or "").strip()
            if not marker:
                return sorted(names)

    def read_digest(self, name):
        status, _, body = self.transport("GET", self._blob_url(name), self._headers(), None)
        if status != 200:
            raise DocumentStoreError(f"digest container refused the download (HTTP {status})")
        try:
            return json.loads(body)
        except ValueError:
            raise InvalidDigestError("invalid remote digest anchor") from None


def open_digest_store(env=None, transport=None):
    env = os.environ if env is None else env
    url = env.get("ZF_DIGEST_ACCOUNT_URL")
    if not url:
        return None
    return BlobDigestStore(url, env.get("ZF_DIGEST_CONTAINER") or "ledger-digests", env.get("ZF_DIGEST_SAS"),
                           env.get("ZF_DIGEST_CLIENT_ID"), transport, env)


def publish(store, blob):
    """Write the current head digest and sealed year digests locally, then upload any not yet in the container."""
    if not ledger.verify_entries(store.audit_entries())["intact"]:
        return []  # never anchor a chain that is already broken
    store.write_digest()
    store.write_year_digests()
    uploaded = []
    for d in ledger.read_digests(store.digest_dir):
        name = f"digest-{d['count']:010d}.json"
        if blob.put_digest(name, d):
            uploaded.append(name)
    for d in ledger.read_year_digests(store.digest_dir):
        name = f"year-{d['year']}.json"
        if blob.put_digest(name, d):
            uploaded.append(name)
    return uploaded


def verify(store, blob):
    """Verify the ledger against the digests held in the immutable container only."""
    names = blob.list_digests()
    heads, years, problems = [], [], []
    for name in names:
        if not name.startswith(("digest-", "year-")):
            continue
        if not _valid_anchor_name(name):
            problems.append(dict(check="digests", problem="invalid remote digest anchor"))
            continue
        try:
            digest = blob.read_digest(name)
        except InvalidDigestError:
            problems.append(dict(check="digests", problem="invalid remote digest anchor"))
            continue
        if not _valid_anchor(name, digest):
            problems.append(dict(check="digests", problem="invalid remote digest anchor"))
            continue
        (heads if name.startswith("digest-") else years).append(digest)
    entries = list(store.audit_entries())
    rep = ledger.verify_entries(entries, heads)
    yrep = ledger.verify_years(entries, years) if entries else dict(intact=not years, years={}, missing_years=[d["year"] for d in years])
    if not rep["intact"]:
        problems.append(dict(check="chain", problem=rep["problem"], digest_mismatches=rep["digest_mismatches"]))
    if not yrep["intact"]:
        problems.append(dict(check="years", missing_years=yrep["missing_years"],
                             broken={y: v["problems"] for y, v in yrep["years"].items() if not v["intact"]}))
    if not heads and not years:
        problems.append(dict(check="digests", problem="the container holds no recognized head or year digest anchors to verify against"))
    return dict(intact=not problems, digests=len(heads), year_digests=len(years), entries=rep["entries"], problems=problems)


def reconcile(blob, record):
    """Compare the remote anchors with an independent record: a JSON object of anchor blob name to head SHA-256.

    Read-only. This is the second-person check of an initial publication; it does not replace that
    person's judgement about where the record came from.
    """
    if (not isinstance(record, dict) or not record
            or any(not _valid_anchor_name(k) or not isinstance(v, str) or re.fullmatch(r"[0-9a-f]{64}", v) is None
                   for k, v in record.items())):
        raise InvalidDigestError("the independent record must map canonical anchor names to SHA-256 heads")
    remote, problems = {}, []
    for name in blob.list_digests():
        if not name.startswith(("digest-", "year-")):
            continue
        try:
            digest = blob.read_digest(name) if _valid_anchor_name(name) else None
        except InvalidDigestError:
            digest = None
        if digest is None or not _valid_anchor(name, digest):
            problems.append(dict(check="remote", problem="invalid remote digest anchor"))
        else:
            remote[name] = digest["head"]
    for name in sorted(set(record) - set(remote)):
        problems.append(dict(check="record", name=name, problem="recorded anchor is absent from the container"))
    for name in sorted(set(remote) - set(record)):
        problems.append(dict(check="remote", name=name, problem="remote anchor is not in the independent record"))
    for name in sorted(set(record) & set(remote)):
        if record[name] != remote[name]:
            problems.append(dict(check="head", name=name, problem="remote head differs from the independent record"))
    return dict(intact=not problems, compared=len(set(record) & set(remote)), problems=problems)


def _reconcile_main(path, env, blob, out):
    blob = blob or open_digest_store(env)
    if blob is None:
        out("ZF_DIGEST_ACCOUNT_URL is not set")
        return 2
    try:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        rep = reconcile(blob, record)
    except (OSError, ValueError, DocumentStoreError) as e:
        out(f"{RECONCILE_ALERT_MARKER} cannot reconcile: {type(e).__name__}")
        return 1
    out(json.dumps(rep, indent=2))
    if not rep["intact"]:
        out(f"{RECONCILE_ALERT_MARKER} remote anchors do not match the independent record")
        return 1
    out(f"{RECONCILE_OK_MARKER} remote anchors match the independent record")
    return 0


def main(argv=None, env=None, store=None, blob=None, out=print):
    """python -m zava_forward.orchestrator.digest_blob [--publish | --reconcile RECORD.json]

Publish then verify, or (read-only) reconcile remote anchors with a second person's independent
record. Exit 1 and alert on mismatch."""
    argv = sys.argv[1:] if argv is None else argv
    if "--reconcile" in argv:
        i = argv.index("--reconcile")
        if i + 1 >= len(argv):
            out("--reconcile needs the path of the independent record")
            return 2
        return _reconcile_main(argv[i + 1], env, blob, out)
    if store is None:
        from zava_forward.core.factory import open_store
        store = open_store(env)
    blob = blob or open_digest_store(env)
    if blob is None:
        out("ZF_DIGEST_ACCOUNT_URL is not set")
        return 2
    try:
        if "--publish" in argv:
            out("published: " + json.dumps(publish(store, blob)))
        rep = verify(store, blob)
    except DocumentStoreError as e:
        out(f"{ALERT_MARKER} digest container unavailable: {e}")
        return 1
    out(json.dumps(rep, indent=2))
    if not rep["intact"]:
        out(f"{ALERT_MARKER} ledger does not match the immutable digests")
        return 1
    out(f"{OK_MARKER} ledger matches the immutable digests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
