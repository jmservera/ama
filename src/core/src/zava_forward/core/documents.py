"""Document storage behind one small interface (ADR 0002 decision 2).

The store keeps document metadata on the case; the bytes live behind a
DocumentStore. Two implementations:

* LocalDocumentStore: files under a folder (development, tests).
* AzureBlobDocumentStore: Azure Blob Storage over its REST API with urllib.
  Authentication is a SAS token (ZF_BLOB_SAS) or, when none is set, a managed
  identity token (Container Apps IDENTITY_ENDPOINT, else the VM metadata
  endpoint). No new dependency. The HTTP call goes through a transport
  callable so tests use a fake; nothing here has been run against a real
  storage account.

Choose with ZF_DOC_STORE=local (default) or azure-blob, plus
ZF_BLOB_ACCOUNT_URL, ZF_BLOB_CONTAINER, ZF_BLOB_SAS or ZF_BLOB_CLIENT_ID.
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

MAX_BYTES = 5 * 1024 * 1024
ACCEPTED = {"pdf": "application/pdf", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "csv": "text/csv", "txt": "text/plain"}
ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


class DocumentStoreError(Exception):
    """The storage back end failed. The caller reports a clean error and writes no metadata."""


def check_ids(case_id, doc_id):
    if not ID.match(str(case_id)) or not ID.match(str(doc_id)) or ".." in str(case_id) + str(doc_id):
        raise KeyError(doc_id)


class DocumentStore:
    def put(self, case_id, doc_id, data, mime):
        raise NotImplementedError

    def get(self, case_id, doc_id):
        raise NotImplementedError

    def delete(self, case_id, doc_id):
        raise NotImplementedError

    def list_ids(self, case_id):
        raise NotImplementedError


class LocalDocumentStore(DocumentStore):
    def __init__(self, root):
        self.root = root

    def _path(self, case_id, doc_id):
        check_ids(case_id, doc_id)
        return os.path.join(self.root, str(case_id), str(doc_id))

    def put(self, case_id, doc_id, data, mime):
        path = self._path(case_id, doc_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, "wb") as f:
                f.write(data)
        except OSError as e:
            raise DocumentStoreError(str(e))

    def get(self, case_id, doc_id):
        try:
            with open(self._path(case_id, doc_id), "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise KeyError(doc_id)
        except OSError as e:
            raise DocumentStoreError(str(e))

    def delete(self, case_id, doc_id):
        try:
            os.remove(self._path(case_id, doc_id))
        except FileNotFoundError:
            pass

    def list_ids(self, case_id):
        check_ids(case_id, "x")
        try:
            return sorted(os.listdir(os.path.join(self.root, str(case_id))))
        except FileNotFoundError:
            return []
        except OSError as e:
            raise DocumentStoreError(str(e))


def urllib_transport(method, url, headers, body, timeout=20):
    """Default transport: returns (status, headers, body) and never raises on an HTTP status."""
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read()
    except (urllib.error.URLError, OSError) as e:
        raise DocumentStoreError(f"storage unreachable: {e}")


class AzureBlobDocumentStore(DocumentStore):
    API_VERSION = "2021-08-06"
    RESOURCE = "https://storage.azure.com/"

    def __init__(self, account_url, container, sas=None, client_id=None, transport=None, env=None, clock=time.time):
        parts = urllib.parse.urlparse(account_url or "")
        if parts.scheme != "https" or not parts.netloc:
            raise ValueError("ZF_BLOB_ACCOUNT_URL must be an https URL such as https://account.blob.core.windows.net")
        if not re.match(r"^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])$", container or ""):
            raise ValueError("ZF_BLOB_CONTAINER must be a valid container name")
        self.base = f"https://{parts.netloc}/{container}"
        self.sas = (sas or "").lstrip("?") or None
        self.client_id = client_id
        self.transport = transport or urllib_transport
        self.env = os.environ if env is None else env
        self.clock = clock
        self._token = None

    def _url(self, case_id, doc_id):
        check_ids(case_id, doc_id)
        url = f"{self.base}/{urllib.parse.quote(str(case_id))}/{urllib.parse.quote(str(doc_id))}"
        return f"{url}?{self.sas}" if self.sas else url

    def _bearer(self):
        if self._token and self._token[1] - 60 > self.clock():
            return self._token[0]
        ep, hdr = self.env.get("IDENTITY_ENDPOINT"), self.env.get("IDENTITY_HEADER")
        query = {"resource": self.RESOURCE}
        if self.client_id:
            query["client_id"] = self.client_id
        if ep:
            url, headers = f"{ep}?{urllib.parse.urlencode({**query, 'api-version': '2019-08-01'})}", {"X-IDENTITY-HEADER": hdr or ""}
        else:
            url, headers = f"http://169.254.169.254/metadata/identity/oauth2/token?{urllib.parse.urlencode({**query, 'api-version': '2018-02-01'})}", {"Metadata": "true"}
        status, _, body = self.transport("GET", url, headers, None)
        if status != 200:
            raise DocumentStoreError("could not get a managed identity token")
        try:
            tok = json.loads(body)
            self._token = (tok["access_token"], float(tok.get("expires_on") or self.clock() + 3000))
        except (ValueError, KeyError, TypeError):
            raise DocumentStoreError("unreadable managed identity token")
        return self._token[0]

    def _headers(self, extra=None):
        h = {"x-ms-version": self.API_VERSION, **(extra or {})}
        if not self.sas:
            h["Authorization"] = f"Bearer {self._bearer()}"
        return h

    def put(self, case_id, doc_id, data, mime):
        h = self._headers({"x-ms-blob-type": "BlockBlob", "Content-Type": mime, "Content-Length": str(len(data)),
                           "If-None-Match": "*"})
        status, _, _ = self.transport("PUT", self._url(case_id, doc_id), h, data)
        if status not in (200, 201):
            raise DocumentStoreError(f"storage refused the upload (HTTP {status})")

    def get(self, case_id, doc_id):
        status, _, body = self.transport("GET", self._url(case_id, doc_id), self._headers(), None)
        if status == 404:
            raise KeyError(doc_id)
        if status != 200:
            raise DocumentStoreError(f"storage refused the download (HTTP {status})")
        return body

    def delete(self, case_id, doc_id):
        status, _, _ = self.transport("DELETE", self._url(case_id, doc_id), self._headers(), None)
        if status not in (200, 202, 404):
            raise DocumentStoreError(f"storage refused the delete (HTTP {status})")

    def list_ids(self, case_id):
        check_ids(case_id, "x")
        prefix, names, marker = f"{urllib.parse.quote(str(case_id))}/", [], None
        while True:
            q = {"restype": "container", "comp": "list", "prefix": prefix}
            if marker:
                q["marker"] = marker
            url = f"{self.base}?{urllib.parse.urlencode(q)}" + (f"&{self.sas}" if self.sas else "")
            status, _, body = self.transport("GET", url, self._headers(), None)
            if status != 200:
                raise DocumentStoreError(f"storage refused the listing (HTTP {status})")
            try:
                root = ET.fromstring(body)
            except ET.ParseError:
                raise DocumentStoreError("unreadable storage listing")
            names += [n.text[len(prefix):] for n in root.iter("Name") if n.text and n.text.startswith(prefix)]
            marker = (root.findtext("NextMarker") or "").strip()
            if not marker:
                return sorted(names)


def open_document_store(default_root, env=None, transport=None):
    env = os.environ if env is None else env
    kind = (env.get("ZF_DOC_STORE") or "local").lower()
    if kind == "local":
        return LocalDocumentStore(env.get("ZF_DOC_DIR") or default_root)
    if kind == "azure-blob":
        return AzureBlobDocumentStore(env.get("ZF_BLOB_ACCOUNT_URL"), env.get("ZF_BLOB_CONTAINER"), env.get("ZF_BLOB_SAS"),
                                      env.get("ZF_BLOB_CLIENT_ID"), transport, env)
    raise ValueError(f"Unknown ZF_DOC_STORE {kind!r}. Use local or azure-blob.")
