"""Versioned law store seeded from the dated local regulatory snapshots (ADR 0005, phase 1).

Sources, versions and provisions are append-only: a newer retrieval becomes a new
version and existing rows and snapshot files are never changed. sqlite3 is the
development and test driver; MSSQL_DDL maps the same tables onto Azure SQL ledger
tables. Snapshots are written once, content addressed, to a blob folder (an
immutable Blob container in Azure). The keyword retrieval index is derived and is
rebuilt from the provision table. Reading needs no AI. Missing sources are gaps and
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

REGISTER = Path(__file__).resolve().parent.parent / "law" / "law-source-register.json"
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


class LawStore:
    def __init__(self, db_path, blob_dir):
        self.blobs = Path(blob_dir)
        self.blobs.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        for ddl in SQLITE_DDL:
            self.db.execute(ddl)
        for t in APPEND_ONLY:
            for op in ("UPDATE", "DELETE"):
                self.db.execute(f"CREATE TRIGGER IF NOT EXISTS {t}_no_{op.lower()} BEFORE {op} ON {t} BEGIN SELECT RAISE(ABORT, '{t} is append-only'); END")
        self.db.commit()

    def close(self):
        self.db.close()

    def seed(self, regulatory_dir, register_path=REGISTER, today=None):
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
            row = self.db.execute("SELECT MAX(version) v FROM reg_version WHERE source_id=?", (s["id"],)).fetchone()
            last = row["v"] or 0
            if last and self.db.execute("SELECT 1 FROM reg_version WHERE source_id=? AND version=? AND content_hash=?", (s["id"], last, digest)).fetchone():
                report["unchanged"].append(s["id"])
                continue
            text = raw.decode("utf-8")
            m = URL.search(text)
            if not self.db.execute("SELECT 1 FROM reg_source WHERE id=?", (s["id"],)).fetchone():
                self.db.execute("INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)", (
                    s["id"], s["title"], m.group(1) if m else None, s["authority_type"], "UK", reg["owner"],
                    s["change_likelihood"], s["cadence"], s["file"]))
            v = last + 1
            blob = self._write_blob(s["id"], v, digest, raw)
            provisions = split_provisions(text)
            self.db.execute("INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                s["id"], v, s["status"], s.get("effective"), reg["retrieved"], None, "not_reviewed", digest, blob,
                "ok" if provisions else "empty", s["completeness"], s.get("completeness_note")))
            for i, (path, body) in enumerate(provisions, 1):
                self.db.execute("INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)", (
                    f"{s['id']}@v{v}#{i:04d}", s["id"], v, i, path, body, sha256(body.encode())))
            report["added"].append(f"{s['id']}@v{v}")
        for g in reg["gaps"]:
            self.db.execute("INSERT OR IGNORE INTO reg_gap VALUES (?,?,?,?,?)", (g["id"], g["topic"], json.dumps(g["keywords"]), g["reason"], today))
        self.db.commit()
        self.rebuild_index()
        return report

    def _write_blob(self, source_id, version, digest, raw):
        rel = f"{source_id}/v{version}-{digest[:16]}.md"
        p = self.blobs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "xb") as fh:
            fh.write(raw)
        p.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        return rel

    def verify_snapshot(self, source_id, version):
        v = self.db.execute("SELECT content_hash, blob_path FROM reg_version WHERE source_id=? AND version=?", (source_id, version)).fetchone()
        if not v:
            raise KeyError(source_id)
        return sha256((self.blobs / v["blob_path"]).read_bytes()) == v["content_hash"]

    def rebuild_index(self):
        """Derive the retrieval index from SQL only. Current versions only; older ones stay readable but are not retrieved."""
        self.db.execute("DELETE FROM reg_index")
        rows = self.db.execute("SELECT p.id, p.heading_path, p.text FROM reg_provision p JOIN (SELECT source_id, MAX(version) v FROM reg_version GROUP BY source_id) c ON c.source_id=p.source_id AND c.v=p.version").fetchall()
        for r in rows:
            counts = {}
            for t in terms(r["heading_path"] + " " + r["text"]):
                counts[t] = counts.get(t, 0) + 1
            self.db.executemany("INSERT INTO reg_index VALUES (?,?,?)", [(t, r["id"], n) for t, n in counts.items()])
        self.db.commit()
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
        rows = self.db.execute("SELECT s.*, v.version, v.status, v.effective, v.retrieved, v.reviewed, v.review_status, v.content_hash, v.completeness, v.completeness_note FROM reg_source s JOIN reg_version v ON v.source_id=s.id AND v.version=(SELECT MAX(version) FROM reg_version WHERE source_id=s.id) ORDER BY s.id").fetchall()
        return dict(sources=[self._source(r) for r in rows], gaps=self.gaps())

    def gaps(self):
        return [dict(id=r["id"], topic=r["topic"], keywords=json.loads(r["keywords"]), reason=r["reason"], recorded=r["recorded"], answer=NO_SOURCE)
                for r in self.db.execute("SELECT * FROM reg_gap ORDER BY id")]

    def source(self, source_id):
        s = self.db.execute("SELECT * FROM reg_source WHERE id=?", (source_id,)).fetchone()
        if not s:
            raise KeyError(source_id)
        versions = [self._source(dict(r, **{"title": s["title"]})) for r in self.db.execute("SELECT * FROM reg_version WHERE source_id=? ORDER BY version DESC", (source_id,))]
        provisions = [dict(r) for r in self.db.execute("SELECT id, version, ordinal, heading_path, hash FROM reg_provision WHERE source_id=? AND version=? ORDER BY ordinal", (source_id, versions[0]["version"]))]
        return dict(source=dict(s), versions=versions, provisions=provisions)

    def provision(self, pid):
        r = self.db.execute("SELECT p.*, v.status, v.effective, v.retrieved, v.review_status, v.completeness, v.completeness_note, s.title, s.official_url, s.authority_type FROM reg_provision p JOIN reg_version v ON v.source_id=p.source_id AND v.version=p.version JOIN reg_source s ON s.id=p.source_id WHERE p.id=?", (pid,)).fetchone()
        if not r:
            raise KeyError(pid)
        return self._source(r)

    def search(self, query, limit=10):
        """Keyword retrieval with caveats. Gap topics are answered as no source held, never guessed."""
        q = query.lower()
        no_source = [g for g in self.gaps() if any(k in q for k in g["keywords"])]
        words = sorted(set(terms(q)))
        results = []
        if words:
            marks = ",".join("?" * len(words))
            for r in self.db.execute(f"SELECT provision_id, SUM(hits) score FROM reg_index WHERE term IN ({marks}) GROUP BY provision_id ORDER BY score DESC, provision_id LIMIT ?", (*words, limit)).fetchall():
                p = self.provision(r["provision_id"])
                p["text"] = p["text"][:400]
                p["score"] = r["score"]
                results.append(p)
        caveats = sorted({c for r in results for c in r["caveats"]})
        return dict(query=query, results=results, caveats=caveats, no_source_held=no_source,
                    answer=None if results else NO_SOURCE)


def main(argv=None):
    a = argv or sys.argv[1:]
    if len(a) != 3:
        sys.exit("usage: python -m zavaforward_mvp.lawstore REGULATORY_DIR DB_FILE BLOB_DIR")
    store = LawStore(a[1], a[2])
    print(json.dumps(store.seed(a[0]), indent=2))


if __name__ == "__main__":
    main()
