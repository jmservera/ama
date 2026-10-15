"""Privacy controls for per-user chat and memory (ADR 0004, GitHub #163). Built, but inactive.

No chat feature exists yet. This module holds what the DPIA needs to be testable
before any real use, and nothing in it decides a legal question:

* DATA_MAP: every place chat and memory content can land (messages, memory
  items, prompts sent to the model, logs) with its retention status.
* Decision record: lawful basis, staff notice and DPIA are references recorded
  by the DPO and Legal (CHAT_DPIA_REF, CHAT_LAWFUL_BASIS_REF, CHAT_NOTICE_REF).
  A bare yes is not a reference. Until all three exist, storing is refused.
* Retention: no period is set until CHAT_RETENTION_REF and CHAT_RETENTION_DAYS
  are both present. Without them nothing expires and the value is Unknown.
* Rights: locate, export and erase a user's threads, messages and memory by
  server-derived user key. The erase counts are returned for the audit ledger,
  which holds metadata only.
* Redaction: free text is masked for obvious identifiers and special-category
  cues before storage. It is best effort, not a guarantee, so the warning stays.
* Logging: diagnostic output may carry counts and ids, never content.

Tests use labelled synthetic values only. Open items stay with the DPO and Legal
in docs/reference/research/chat-memory-dpia.md.
"""
import os
import re
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta

WARNING = ("Do not type health, disability, safeguarding, religion, ethnicity, sexual orientation, trade union, criminal, "
           "financial hardship or other special-category details, and do not paste resident contact details. Use the case record "
           "instead. Matching text is masked before it is saved, but masking can miss things.")
REDACTION_VERSION = "draft-1"

PATTERNS = (
    ("email", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("phone", re.compile(r"(?<!\w)(?:\+44\s?|0)\d(?:[\s-]?\d){8,10}(?!\w)")),
    ("ni_number", re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b", re.I)),
    ("postcode", re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b", re.I)),
    ("special_category", re.compile(r"\b(?:diagnos\w*|disabilit\w*|dementia|cancer|asthma|copd|mental health|depress\w*|safeguard\w*|"
                                    r"vulnerab\w*|pregnan\w*|religio\w*|muslim|christian|jewish|hindu|sikh|ethnic\w*|sexual orientation|"
                                    r"trade union|criminal\w*|convict\w*|benefits claimant)\b", re.I)),
)

DATA_MAP = (
    dict(id="message", data="Chat messages typed by staff and assistant replies", subjects="Staff; residents named in case text",
         location="Azure SQL chat_message, uksouth, owner-filtered", sensitivity="Personal data; may hold resident data typed in free text",
         retention="Unknown until DPO approval", rights="Locate, export, erase by user key"),
    dict(id="thread", data="Thread header: user key, case, task, time", subjects="Staff", location="Azure SQL chat_thread, uksouth",
         sensitivity="Personal data", retention="Unknown until DPO approval", rights="Locate, export, erase by user key"),
    dict(id="memory", data="Opt-in memory items (off by default)", subjects="Staff", location="Azure SQL chat_memory, uksouth, owner-filtered",
         sensitivity="Personal data; never special-category or consent data", retention="Unknown until DPO approval; expiry required",
         rights="Locate, export, edit, erase by user key"),
    dict(id="prompt", data="Prompt assembled per turn: own thread, own memory, projected case data", subjects="Staff; residents in case text",
         location="Sent to the Azure OpenAI deployment in uksouth; not stored by Zava", sensitivity="Personal data in transit",
         retention="Not stored by Zava. Provider abuse-monitoring and retention terms Unknown, to be recorded by the DPO",
         rights="Nothing held by Zava to erase; provider terms are an open item"),
    dict(id="diagnostic_log", data="Application diagnostics", subjects="Staff", location="Process output and Azure Monitor",
         sensitivity="Must hold no chat or memory content", retention="Per platform log policy", rights="Not applicable: no content held"),
    dict(id="audit_ledger", data="Event metadata: who, what, when, counts", subjects="Staff", location="Append-only audit ledger",
         sensitivity="Metadata only, no content, so erasure does not break tamper evidence", retention="Per ledger policy",
         rights="Metadata retained; DPO to confirm"),
)

MODEL_PROVIDER_POSITION = dict(
    provider="Azure OpenAI through the existing Foundry deployments (ADR 0001 to ADR 0003)", region="uksouth (owner decision 2026-10-15)",
    zava_stores_prompts=False, foundry_agent_memory=False,
    open_items=("Provider data processing terms, abuse-monitoring retention and any opt-out must be retrieved and recorded by the DPO "
                "from current Microsoft terms; not verified here.",
                "International transfer position, if any, stays Unknown until the DPO records it."))

DIAGNOSTIC_FIELDS = frozenset({"thread_id", "user_key", "case_id", "task", "role", "count", "status", "at", "event", "latency_ms"})
SQL_TYPES = {"sqlite": "TEXT", "mssql": "NVARCHAR(MAX)"}
_DDL = (
    "CREATE TABLE chat_thread (id {k} PRIMARY KEY, user_key {k} NOT NULL, role {k} NOT NULL, case_id {k} NOT NULL, task {k} NOT NULL, at {k} NOT NULL)",
    "CREATE TABLE chat_message (id {k} PRIMARY KEY, thread_id {k} NOT NULL, user_key {k} NOT NULL, author {k} NOT NULL, content {t} NOT NULL, "
    "redactions {k} NOT NULL, at {k} NOT NULL)",
    "CREATE TABLE chat_memory (id {k} PRIMARY KEY, user_key {k} NOT NULL, role {k} NOT NULL, content {t} NOT NULL, redactions {k} NOT NULL, "
    "at {k} NOT NULL, expires_at {k} NULL)",
)
TABLES = ("chat_thread", "chat_message", "chat_memory")


def redact(text):
    """Return (masked text, sorted kinds found). Masking is best effort."""
    kinds = set()
    for kind, rx in PATTERNS:
        text, n = rx.subn(f"[{kind} removed]", text)
        if n:
            kinds.add(kind)
    return text, sorted(kinds)


def diagnostic_safe(fields):
    """Drop everything except ids, counts and status from a diagnostic record. Content is never logged."""
    return {k: v for k, v in fields.items() if k in DIAGNOSTIC_FIELDS}


class ChatNotApproved(PermissionError):
    pass


class ChatPrivacy:
    def __init__(self, store=None, env=None, db_path=None):
        self.env = os.environ if env is None else env
        self.store = store if hasattr(store, "assistant_connection") else None
        self.mssql = self.store is not None and hasattr(self.store, "_env")
        self.db_path = db_path or self.env.get("ZF_CHAT_DB") or os.path.join(self.env.get("ZF_STATE") or ".", "chat.sqlite")
        self.lock = threading.Lock()
        self.ready = False

    @contextmanager
    def _conn(self):
        if self.store is not None:
            db = self.store.assistant_connection()
        else:
            import sqlite3
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
            db = sqlite3.connect(self.db_path, isolation_level=None)
        try:
            self._ensure(db)
            yield db
        finally:
            db.close()

    def _ensure(self, db):
        if self.ready:
            return
        with self.lock:
            kind = SQL_TYPES["mssql" if self.mssql else "sqlite"]
            for ddl in _DDL:
                ddl = ddl.format(k="NVARCHAR(200)" if self.mssql else "TEXT", t=kind)
                db.execute(f"IF OBJECT_ID(N'{ddl.split()[2]}', N'U') IS NULL {ddl}" if self.mssql else ddl.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1))
            self.ready = True

    def _ref(self, key):
        return (self.env.get(key) or "").strip()

    def decision(self):
        """The recorded DPO and Legal decision. Storage stays refused until all three references exist."""
        refs = dict(dpia_ref=self._ref("CHAT_DPIA_REF"), lawful_basis_ref=self._ref("CHAT_LAWFUL_BASIS_REF"), notice_ref=self._ref("CHAT_NOTICE_REF"))
        missing = [k for k, v in refs.items() if not v]
        days = self._ref("CHAT_RETENTION_DAYS")
        retention_set = bool(self._ref("CHAT_RETENTION_REF")) and days.isdigit() and int(days) > 0
        return dict(refs=refs, approved=not missing, missing=missing, retention_days=int(days) if retention_set else None,
                    retention="Unknown: no period set until CHAT_RETENTION_REF and CHAT_RETENTION_DAYS are recorded" if not retention_set else f"{int(days)} days",
                    owner="Juan Manuel Servera (DPO, Legal and Compliance, 2026-10-15)",
                    performance_use="Prohibited: chat and memory content is excluded from performance measurement without a separate decision (RULE-026)")

    def _require(self):
        d = self.decision()
        if not d["approved"]:
            raise ChatNotApproved("Chat and memory storage is refused until the DPIA, lawful basis and staff notice references are recorded: "
                                  + ", ".join(d["missing"]))
        return d

    @staticmethod
    def _now():
        return datetime.now().isoformat(timespec="seconds")

    def _expiry(self, d):
        return (datetime.now() + timedelta(days=d["retention_days"])).isoformat(timespec="seconds") if d["retention_days"] else None

    def start_thread(self, user_key, role, case_id, task):
        self._require()
        tid = uuid.uuid4().hex
        with self._conn() as db:
            db.execute("INSERT INTO chat_thread (id, user_key, role, case_id, task, at) VALUES (?,?,?,?,?,?)",
                       (tid, user_key, role, str(case_id)[:40], str(task)[:100], self._now()))
        return tid

    def add_message(self, user_key, thread_id, author, content):
        """Store a redacted message in the caller's own thread. Returns the redaction kinds found, for the warning."""
        self._require()
        text, kinds = redact(str(content)[:4000])
        with self._conn() as db:
            if db.execute("SELECT 1 FROM chat_thread WHERE id=? AND user_key=?", (thread_id, user_key)).fetchone() is None:
                raise PermissionError("Thread not found for this user.")
            db.execute("INSERT INTO chat_message (id, thread_id, user_key, author, content, redactions, at) VALUES (?,?,?,?,?,?,?)",
                       (uuid.uuid4().hex, thread_id, user_key, author, text, ",".join(kinds), self._now()))
        return kinds

    def add_memory(self, user_key, role, content):
        """Opt-in memory. Refused outright if the text looks special-category, rather than stored masked."""
        d = self._require()
        text, kinds = redact(str(content)[:1000])
        if "special_category" in kinds:
            raise ValueError("Memory must not hold special-category data. " + WARNING)
        with self._conn() as db:
            mid = uuid.uuid4().hex
            db.execute("INSERT INTO chat_memory (id, user_key, role, content, redactions, at, expires_at) VALUES (?,?,?,?,?,?,?)",
                       (mid, user_key, role, text, ",".join(kinds), self._now(), self._expiry(d)))
        return mid

    def locate(self, user_key):
        """Rights request: counts and ids of everything held for this user key. Reads need no approval."""
        with self._conn() as db:
            threads = [r[0] for r in db.execute("SELECT id FROM chat_thread WHERE user_key=?", (user_key,)).fetchall()]
            memory = [r[0] for r in db.execute("SELECT id FROM chat_memory WHERE user_key=?", (user_key,)).fetchall()]
            n = db.execute("SELECT COUNT(*) FROM chat_message WHERE user_key=?", (user_key,)).fetchone()[0]
        return dict(threads=threads, messages=n, memory=memory)

    def export(self, user_key):
        """Rights request (access): the user's own content, nobody else's."""
        with self._conn() as db:
            msgs = db.execute("SELECT thread_id, author, content, at FROM chat_message WHERE user_key=? ORDER BY at", (user_key,)).fetchall()
            mem = db.execute("SELECT id, content, at, expires_at FROM chat_memory WHERE user_key=? ORDER BY at", (user_key,)).fetchall()
        return dict(messages=[dict(thread_id=t, author=a, content=c, at=at) for t, a, c, at in msgs],
                    memory=[dict(id=i, content=c, at=at, expires_at=e) for i, c, at, e in mem])

    def erase(self, user_key):
        """Rights request (erasure): delete the user's threads, messages and memory. Returns counts for a metadata-only audit event."""
        with self._conn() as db:
            before = self.locate_in(db, user_key)
            for t in ("chat_message", "chat_thread", "chat_memory"):
                db.execute(f"DELETE FROM {t} WHERE user_key=?", (user_key,))
        return dict(threads=len(before["threads"]), messages=before["messages"], memory=len(before["memory"]))

    @staticmethod
    def locate_in(db, user_key):
        return dict(threads=db.execute("SELECT id FROM chat_thread WHERE user_key=?", (user_key,)).fetchall(),
                    messages=db.execute("SELECT COUNT(*) FROM chat_message WHERE user_key=?", (user_key,)).fetchone()[0],
                    memory=db.execute("SELECT id FROM chat_memory WHERE user_key=?", (user_key,)).fetchall())

    def purge_expired(self):
        """Delete memory past its expiry. Nothing expires while no retention period is approved."""
        with self._conn() as db:
            n = db.execute("SELECT COUNT(*) FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?", (self._now(),)).fetchone()[0]
            db.execute("DELETE FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?", (self._now(),))
        return n
