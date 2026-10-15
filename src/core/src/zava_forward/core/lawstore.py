"""Versioned law store seeded from the dated local regulatory snapshots (ADR 0005, phase 1).

Sources, versions and provisions are append-only: a newer retrieval becomes a new
version and existing rows and snapshot files are never changed. The deployed backend
is Azure SQL (MssqlDb, append-only ledger tables) with snapshots in an immutable Azure
Blob container (AzureBlobSnapshots). sqlite3 (SqliteDb) and a local folder
(LocalSnapshots) are the local test doubles only. Snapshots are written once and
content addressed. The keyword retrieval index is derived and is rebuilt from the
provision table. Reading needs no AI. Missing sources are gaps and
are answered as "no source held". Nothing here is legal advice or approval.
"""
import hashlib
import json
import os
import re
import sqlite3
import stat
import sys
from datetime import date
from pathlib import Path

REGISTER = Path(__file__).resolve().parent / "law" / "law-source-register.json"
NO_SOURCE = "No source is held for this topic. Do not rely on this system; ask the named owner."
PARTIAL = "This source is held only in part, so the answer may be incomplete."
NOT_REVIEWED = "Not yet reviewed by a named owner. This is a reference copy, not legal advice."
STATUSES = ("in_force", "guidance", "consultation", "historical")
COMPLETENESS = ("full", "partial")

APPEND_ONLY = ("reg_source", "reg_version", "reg_provision", "reg_gap")
SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS reg_source (id TEXT PRIMARY KEY, title TEXT NOT NULL, official_url TEXT, authority_type TEXT NOT NULL, jurisdiction TEXT NOT NULL, owner TEXT NOT NULL, change_likelihood TEXT NOT NULL, cadence TEXT NOT NULL, local_file TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_version (source_id TEXT NOT NULL, version INTEGER NOT NULL, status TEXT NOT NULL, effective TEXT, retrieved TEXT NOT NULL, reviewed TEXT, review_status TEXT NOT NULL, content_hash TEXT NOT NULL, blob_path TEXT NOT NULL, parse_result TEXT NOT NULL, completeness TEXT NOT NULL, completeness_note TEXT, PRIMARY KEY (source_id, version))",
    "CREATE TABLE IF NOT EXISTS reg_provision (id TEXT PRIMARY KEY, source_id TEXT NOT NULL, version INTEGER NOT NULL, ordinal INTEGER NOT NULL, heading_path TEXT NOT NULL, text TEXT NOT NULL, hash TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_gap (id TEXT PRIMARY KEY, topic TEXT NOT NULL, keywords TEXT NOT NULL, reason TEXT NOT NULL, recorded TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_index (term TEXT NOT NULL, provision_id TEXT NOT NULL, hits INTEGER NOT NULL, PRIMARY KEY (term, provision_id))",
)
MSSQL_DDL = (
    "CREATE TABLE reg_source (id VARCHAR(100) PRIMARY KEY, title NVARCHAR(400) NOT NULL, official_url NVARCHAR(1000) NULL, authority_type VARCHAR(40) NOT NULL, jurisdiction VARCHAR(40) NOT NULL, owner NVARCHAR(200) NOT NULL, change_likelihood NVARCHAR(100) NOT NULL, cadence NVARCHAR(200) NOT NULL, local_file NVARCHAR(300) NOT NULL)",
    "CREATE TABLE reg_version (source_id VARCHAR(100) NOT NULL, version INT NOT NULL, status VARCHAR(20) NOT NULL, effective VARCHAR(10) NULL, retrieved VARCHAR(10) NOT NULL, reviewed VARCHAR(10) NULL, review_status VARCHAR(40) NOT NULL, content_hash CHAR(64) NOT NULL, blob_path NVARCHAR(400) NOT NULL, parse_result VARCHAR(40) NOT NULL, completeness VARCHAR(10) NOT NULL, completeness_note NVARCHAR(400) NULL, PRIMARY KEY (source_id, version))",
    "CREATE TABLE reg_provision (id VARCHAR(140) PRIMARY KEY, source_id VARCHAR(100) NOT NULL, version INT NOT NULL, ordinal INT NOT NULL, heading_path NVARCHAR(600) NOT NULL, text NVARCHAR(MAX) NOT NULL, hash CHAR(64) NOT NULL)",
    "CREATE TABLE reg_gap (id VARCHAR(100) PRIMARY KEY, topic NVARCHAR(200) NOT NULL, keywords NVARCHAR(400) NOT NULL, reason NVARCHAR(400) NOT NULL, recorded VARCHAR(10) NOT NULL)",
    "CREATE TABLE reg_index (term VARCHAR(100) NOT NULL, provision_id VARCHAR(140) NOT NULL, hits INT NOT NULL, PRIMARY KEY (term, provision_id))",
)
LEDGER_SUFFIX = " WITH (LEDGER = ON (APPEND_ONLY = ON))"

URL = re.compile(r"Converted from the \[[^\]]*\]\((https?://[^)\s]+)\)")
HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*$")
TOKEN = re.compile(r"[a-z0-9]{3,}")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def split_provisions(text):
    """Split Markdown into (heading_path, text) provisions at headings, skipping the frontmatter."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]
    stack, out, buf, path = [], [], [], "Introduction"
    def flush():
        body = "\n".join(buf).strip()
        if body:
            out.append((path, body))
    for line in lines:
        m = HEADING.match(line)
        if m:
            flush()
            buf.clear()
            level = len(m.group(1))
            stack[:] = [(lv, t) for lv, t in stack if lv < level] + [(level, m.group(2))]
            path = " > ".join(t for _, t in stack)
        else:
            buf.append(line)
    flush()
    return out


def terms(text):
    return TOKEN.findall(text.lower())


class LocalSnapshots:
    """Test double for the snapshot store: write-once files in a folder. Not for deployment."""

    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, rel, raw):
        """Write a snapshot once. Identical bytes are a no-op; different bytes under the same name raise FileExistsError."""
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(p, "xb") as fh:
                fh.write(raw)
        except FileExistsError:
            if p.read_bytes() != raw:
                raise
            return
        p.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    def get(self, rel):
        return (self.root / rel).read_bytes()


class AzureBlobSnapshots:
    """Snapshots in an Azure Blob container. Writes never overwrite; the container should also carry an
    immutability (WORM) policy, which is infrastructure and is not proven by this code."""

    def __init__(self, container):
        self.container = container

    @classmethod
    def from_env(cls, env=None):
        env = os.environ if env is None else env
        url, name = env.get("ZF_LAW_BLOB_ACCOUNT_URL"), env.get("ZF_LAW_BLOB_CONTAINER")
        if not url or not name:
            raise SystemExit("ZF_LAW_STORE=mssql needs ZF_LAW_BLOB_ACCOUNT_URL and ZF_LAW_BLOB_CONTAINER.")
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient
        return cls(BlobServiceClient(url, credential=DefaultAzureCredential()).get_container_client(name))

    def put(self, rel, raw):
        from azure.core.exceptions import ResourceExistsError
        try:
            self.container.upload_blob(rel, raw, overwrite=False)
        except ResourceExistsError:
            if self.get(rel) != raw:
                raise FileExistsError(rel)

    def get(self, rel):
        return self.container.download_blob(rel).readall()


class SqliteDb:
    """Local test double for the SQL backend."""
    ledger = False
    dberror = sqlite3.DatabaseError

    def __init__(self, path):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        for ddl in SQLITE_DDL:
            self.db.execute(ddl)
        for t in APPEND_ONLY:
            for op in ("UPDATE", "DELETE"):
                self.db.execute(f"CREATE TRIGGER IF NOT EXISTS {t}_no_{op.lower()} BEFORE {op} ON {t} BEGIN SELECT RAISE(ABORT, '{t} is append-only'); END")
        self.db.commit()

    def all(self, sql, args=()):
        return [dict(r) for r in self.db.execute(sql, args).fetchall()]

    def run(self, sql, args=()):
        self.db.execute(sql, args)

    def many(self, sql, rows):
        self.db.executemany(sql, rows)

    def insert_ignore(self, table, key, sql, args):
        self.db.execute(sql.replace("INSERT", "INSERT OR IGNORE", 1), args)

    def limited(self, sql):
        return sql + " LIMIT ?"

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()


class MssqlDb:
    """Azure SQL (or SQL Server in CI) backend reusing the store's connection settings (ZF_SQL_*)."""

    def __init__(self, env=None):
        from zava_forward.core.mssqlstore import _Conn, connection_string
        env = os.environ if env is None else env
        self.db = _Conn(connection_string(env), env.get("ZF_SQL_TOKEN"))
        self.ledger = bool(self.db.execute("SELECT is_ledger_on FROM sys.databases WHERE name = DB_NAME()").fetchone()[0])
        self.db.execute("BEGIN IMMEDIATE")
        try:
            for t, ddl in zip(APPEND_ONLY + ("reg_index",), MSSQL_DDL):
                ddl = ddl + LEDGER_SUFFIX if self.ledger and t in APPEND_ONLY else ddl
                self.db.execute(f"IF OBJECT_ID(N'{t}', N'U') IS NULL {ddl}")
            if self.ledger:
                for t in APPEND_ONLY:
                    kind = self.db.execute(f"SELECT ledger_type_desc FROM sys.tables WHERE name = N'{t}'").fetchone()[0]
                    if kind != "APPEND_ONLY_LEDGER_TABLE":
                        raise SystemExit(f"{t} is a {kind}, not an append-only ledger table; drop and recreate it before starting.")
            else:
                for t in APPEND_ONLY:
                    self.db.execute(f"IF OBJECT_ID(N'{t}_append_only', N'TR') IS NULL EXEC(N'CREATE TRIGGER {t}_append_only ON {t} "
                                    f"INSTEAD OF UPDATE, DELETE AS THROW 50001, ''{t} is append-only'', 1')")
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        self.in_tran = False

    @property
    def dberror(self):
        import mssql_python
        return mssql_python.Error

    def all(self, sql, args=()):
        cur = self.db.execute(sql, args)
        names = [d[0] for d in cur.cur.description]
        return [dict(zip(names, r)) for r in cur.fetchall()]

    def run(self, sql, args=()):
        self._begin()
        self.db.execute(sql, args)

    def many(self, sql, rows):
        self._begin()
        self.db.executemany(sql, rows)

    def _begin(self):
        if not self.in_tran:
            self.db.execute("BEGIN IMMEDIATE")
            self.in_tran = True

    def insert_ignore(self, table, key, sql, args):
        self.run(f"IF NOT EXISTS (SELECT 1 FROM {table} WHERE {key} = ?) {sql}", (args[0],) + tuple(args))

    def limited(self, sql):
        return sql + " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"

    def commit(self):
        if self.in_tran:
            self.db.execute("COMMIT")
            self.in_tran = False

    def rollback(self):
        if self.in_tran:
            self.db.execute("ROLLBACK")
            self.in_tran = False

    def close(self):
        self.db.close()


class LawStore:
    def __init__(self, db_path=None, blob_dir=None, db=None, blobs=None):
        """Local test double by default (sqlite file and blob folder); pass db and blobs for Azure SQL and Azure Blob."""
        self.sql = db or SqliteDb(db_path)
        self.blobs = blobs or LocalSnapshots(blob_dir)

    @classmethod
    def from_env(cls, env=None):
        env = os.environ if env is None else env
        if (env.get("ZF_LAW_STORE") or "sqlite").lower() == "mssql":
            return cls(db=MssqlDb(env), blobs=AzureBlobSnapshots.from_env(env))
        if not env.get("ZF_LAW_DB"):
            return None
        return cls(env["ZF_LAW_DB"], env.get("ZF_LAW_BLOBS", "/state/law-blobs"))

    def close(self):
        self.sql.close()

    def seed(self, regulatory_dir, register_path=REGISTER, today=None):
        try:
            return self._seed(regulatory_dir, register_path, today)
        except BaseException:
            self.sql.rollback()
            raise

    def _seed(self, regulatory_dir, register_path, today):
        """Load the register and snapshots. Idempotent: an unchanged hash adds nothing; a changed one adds a version."""
        reg = json.loads(Path(register_path).read_text())
        root, report = Path(regulatory_dir), dict(added=[], unchanged=[], missing_files=[])
        today = today or date.today().isoformat()
        for s in reg["sources"]:
            f = root / s["file"]
            if not f.is_file():
                report["missing_files"].append(s["id"])
                continue
            raw = f.read_bytes()
            digest = sha256(raw)
            last = self.sql.all("SELECT MAX(version) v FROM reg_version WHERE source_id=?", (s["id"],))[0]["v"] or 0
            if last and self.sql.all("SELECT 1 x FROM reg_version WHERE source_id=? AND version=? AND content_hash=?", (s["id"], last, digest)):
                report["unchanged"].append(s["id"])
                continue
            text = raw.decode("utf-8")
            m = URL.search(text)
            if not self.sql.all("SELECT 1 x FROM reg_source WHERE id=?", (s["id"],)):
                self.sql.run("INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)", (
                    s["id"], s["title"], m.group(1) if m else None, s["authority_type"], "UK", reg["owner"],
                    s["change_likelihood"], s["cadence"], s["file"]))
            v = last + 1
            blob = self._write_blob(s["id"], v, digest, raw)
            provisions = split_provisions(text)
            self.sql.run("INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                s["id"], v, s["status"], s.get("effective"), reg["retrieved"], None, "not_reviewed", digest, blob,
                "ok" if provisions else "empty", s["completeness"], s.get("completeness_note")))
            for i, (path, body) in enumerate(provisions, 1):
                self.sql.run("INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)", (
                    f"{s['id']}@v{v}#{i:04d}", s["id"], v, i, path, body, sha256(body.encode())))
            report["added"].append(f"{s['id']}@v{v}")
        for g in reg["gaps"]:
            self.sql.insert_ignore("reg_gap", "id", "INSERT INTO reg_gap VALUES (?,?,?,?,?)", (g["id"], g["topic"], json.dumps(g["keywords"]), g["reason"], today))
        self.sql.commit()
        self.rebuild_index()
        return report

    def _write_blob(self, source_id, version, digest, raw):
        rel = f"{source_id}/v{version}-{digest[:16]}.md"
        self.blobs.put(rel, raw)
        return rel

    def verify_snapshot(self, source_id, version):
        rows = self.sql.all("SELECT content_hash, blob_path FROM reg_version WHERE source_id=? AND version=?", (source_id, version))
        if not rows:
            raise KeyError(source_id)
        return sha256(self.blobs.get(rows[0]["blob_path"])) == rows[0]["content_hash"]

    def rebuild_index(self):
        """Derive the retrieval index from SQL only. Current versions only; older ones stay readable but are not retrieved."""
        self.sql.run("DELETE FROM reg_index")
        rows = self.sql.all("SELECT p.id, p.heading_path, p.text FROM reg_provision p JOIN (SELECT source_id, MAX(version) v FROM reg_version GROUP BY source_id) c ON c.source_id=p.source_id AND c.v=p.version")
        for r in rows:
            counts = {}
            for t in terms(r["heading_path"] + " " + r["text"]):
                counts[t] = counts.get(t, 0) + 1
            self.sql.many("INSERT INTO reg_index VALUES (?,?,?)", [(t, r["id"], n) for t, n in counts.items()])
        self.sql.commit()
        return len(rows)

    def _source(self, row):
        d = dict(row)
        d["caveats"] = self._caveats(d)
        return d

    @staticmethod
    def _caveats(d):
        out = []
        if d.get("completeness") == "partial":
            out.append(PARTIAL + (" " + d["completeness_note"] if d.get("completeness_note") else ""))
        if d.get("status") == "historical":
            out.append("Historical source. Not the current operational authority.")
        if d.get("status") == "consultation":
            out.append("Consultation material, not a final rule.")
        if d.get("review_status") != "reviewed":
            out.append(NOT_REVIEWED)
        return out

    def sources(self):
        rows = self.sql.all("SELECT s.*, v.version, v.status, v.effective, v.retrieved, v.reviewed, v.review_status, v.content_hash, v.completeness, v.completeness_note FROM reg_source s JOIN reg_version v ON v.source_id=s.id AND v.version=(SELECT MAX(version) FROM reg_version WHERE source_id=s.id) ORDER BY s.id")
        return dict(sources=[self._source(r) for r in rows], gaps=self.gaps())

    def gaps(self):
        return [dict(id=r["id"], topic=r["topic"], keywords=json.loads(r["keywords"]), reason=r["reason"], recorded=r["recorded"], answer=NO_SOURCE)
                for r in self.sql.all("SELECT * FROM reg_gap ORDER BY id")]

    def source(self, source_id):
        found = self.sql.all("SELECT * FROM reg_source WHERE id=?", (source_id,))
        if not found:
            raise KeyError(source_id)
        s = found[0]
        versions = [self._source(dict(r, **{"title": s["title"]})) for r in self.sql.all("SELECT * FROM reg_version WHERE source_id=? ORDER BY version DESC", (source_id,))]
        provisions = self.sql.all("SELECT id, version, ordinal, heading_path, hash FROM reg_provision WHERE source_id=? AND version=? ORDER BY ordinal", (source_id, versions[0]["version"]))
        return dict(source=s, versions=versions, provisions=provisions)

    def provision(self, pid):
        found = self.sql.all("SELECT p.*, v.status, v.effective, v.retrieved, v.review_status, v.completeness, v.completeness_note, s.title, s.official_url, s.authority_type FROM reg_provision p JOIN reg_version v ON v.source_id=p.source_id AND v.version=p.version JOIN reg_source s ON s.id=p.source_id WHERE p.id=?", (pid,))
        if not found:
            raise KeyError(pid)
        return self._source(found[0])

    def search(self, query, limit=10):
        """Keyword retrieval with caveats. Gap topics are answered as no source held, never guessed."""
        q = query.lower()
        no_source = [g for g in self.gaps() if any(k in q for k in g["keywords"])]
        words = sorted(set(terms(q)))
        results = []
        if words:
            marks = ",".join("?" * len(words))
            for r in self.sql.all(self.sql.limited(f"SELECT provision_id, SUM(hits) score FROM reg_index WHERE term IN ({marks}) GROUP BY provision_id ORDER BY score DESC, provision_id"), (*words, limit)):
                p = self.provision(r["provision_id"])
                p["text"] = p["text"][:400]
                p["score"] = r["score"]
                results.append(p)
        caveats = sorted({c for r in results for c in r["caveats"]})
        return dict(query=query, results=results, caveats=caveats, no_source_held=no_source,
                    answer=None if results else NO_SOURCE)


def main(argv=None):
    a = argv or sys.argv[1:]
    if (os.environ.get("ZF_LAW_STORE") or "").lower() == "mssql":
        if len(a) != 1:
            sys.exit("usage: ZF_LAW_STORE=mssql python -m zava_forward.core.lawstore REGULATORY_DIR (Azure SQL and Blob settings from ZF_SQL_* and ZF_LAW_BLOB_*)")
        store = LawStore.from_env()
    elif len(a) != 3:
        sys.exit("usage: python -m zava_forward.core.lawstore REGULATORY_DIR DB_FILE BLOB_DIR")
    else:
        store = LawStore(a[1], a[2])
    print(json.dumps(store.seed(a[0]), indent=2))


if __name__ == "__main__":
    main()
