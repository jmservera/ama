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
import sys
import urllib.parse
import xml.etree.ElementTree as ET

from zava_forward.core import ledger
from zava_forward.core.documents import AzureBlobDocumentStore, DocumentStoreError

ALERT_MARKER = "LEDGER_DIGEST_ALERT"
OK_MARKER = "LEDGER_DIGEST_OK"


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
            names += [n.text for n in root.iter("Name") if n.text and n.text.endswith(".json")]
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
            raise DocumentStoreError(f"digest {name} is not valid JSON")


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
    heads = [blob.read_digest(n) for n in names if n.startswith("digest-")]
    years = [blob.read_digest(n) for n in names if n.startswith("year-")]
    entries = list(store.audit_entries())
    rep = ledger.verify_entries(entries, heads)
    yrep = ledger.verify_years(entries, years) if entries else dict(intact=not years, years={}, missing_years=[d["year"] for d in years])
    problems = []
    if not rep["intact"]:
        problems.append(dict(check="chain", problem=rep["problem"], digest_mismatches=rep["digest_mismatches"]))
    if not yrep["intact"]:
        problems.append(dict(check="years", missing_years=yrep["missing_years"],
                             broken={y: v["problems"] for y, v in yrep["years"].items() if not v["intact"]}))
    if not heads and not years:
        problems.append(dict(check="digests", problem="the container holds no recognized head or year digest anchors to verify against"))
    return dict(intact=not problems, digests=len(heads), year_digests=len(years), entries=rep["entries"], problems=problems)


def main(argv=None, env=None, store=None, blob=None, out=print):
    """python -m zava_forward.orchestrator.digest_blob [--publish] : publish then verify; exit 1 and alert on mismatch."""
    argv = sys.argv[1:] if argv is None else argv
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
