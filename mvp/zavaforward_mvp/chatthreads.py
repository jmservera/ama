"""Per-user chat thread storage (issue #160, ADR 0004 decision 3).

Threads and messages are stored apart from the tamper-evident audit ledger. The ledger only receives event metadata
(thread id, case, counts, role): never message text, so deleting a thread leaves the hash chain intact.

One service (ChatMixin, mixed into Store) holds the rules; two small repositories supply storage, so the in-memory
Store and the SQL stores (SQLite for tests, Azure SQL in deployment) behave identically. Every query filters on the
owner key, so another user's thread is indistinguishable from a missing one. Each thread carries a row version and a
write fails closed with ConflictError when the caller's expected version no longer matches.
"""
import json
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

MAX_CONTENT = 8000
MAX_EVIDENCE = 20
ROLES = ("user", "assistant")
ACTIVE, ARCHIVED = "active", "archived"

SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS chat_thread (id TEXT PRIMARY KEY, owner TEXT NOT NULL, owner_role TEXT NOT NULL, case_id TEXT NOT NULL, "
    "title TEXT NOT NULL, task TEXT NOT NULL, task_version TEXT NOT NULL, model TEXT NOT NULL, status TEXT NOT NULL, "
    "rowversion INTEGER NOT NULL, message_count INTEGER NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS chat_message (thread_id TEXT NOT NULL, seq INTEGER NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, "
    "model TEXT NOT NULL, task_version TEXT NOT NULL, evidence TEXT NOT NULL, created_at TEXT NOT NULL, PRIMARY KEY (thread_id, seq))",
    "CREATE TABLE IF NOT EXISTS chat_memory (id TEXT PRIMARY KEY, owner TEXT NOT NULL, owner_role TEXT NOT NULL, content TEXT NOT NULL, "
    "redactions TEXT NOT NULL, item_class TEXT NOT NULL, source TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, "
    "expires_at TEXT NULL)",
    "CREATE TABLE IF NOT EXISTS chat_memory_control (scope TEXT NOT NULL, ref TEXT NOT NULL, enabled INTEGER NOT NULL, actor TEXT NOT NULL, "
    "note TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (scope, ref))",
    "CREATE INDEX IF NOT EXISTS ix_chat_thread_owner ON chat_thread (owner, status, updated_at)",
)
MSSQL_DDL = (
    "CREATE TABLE chat_thread (id NVARCHAR(40) COLLATE Latin1_General_100_BIN2 NOT NULL PRIMARY KEY, owner NVARCHAR(200) COLLATE Latin1_General_100_BIN2 NOT NULL, "
    "owner_role NVARCHAR(100) NOT NULL, case_id NVARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL, title NVARCHAR(200) NOT NULL, "
    "task NVARCHAR(64) NOT NULL, task_version NVARCHAR(40) NOT NULL, model NVARCHAR(100) NOT NULL, status NVARCHAR(20) COLLATE Latin1_General_100_BIN2 NOT NULL, "
    "rowversion BIGINT NOT NULL, message_count INT NOT NULL, created_at NVARCHAR(40) NOT NULL, updated_at NVARCHAR(40) COLLATE Latin1_General_100_BIN2 NOT NULL)",
    "CREATE TABLE chat_message (thread_id NVARCHAR(40) COLLATE Latin1_General_100_BIN2 NOT NULL, seq INT NOT NULL, role NVARCHAR(20) NOT NULL, "
    "content NVARCHAR(MAX) NOT NULL, model NVARCHAR(100) NOT NULL, task_version NVARCHAR(40) NOT NULL, evidence NVARCHAR(MAX) NOT NULL, "
    "created_at NVARCHAR(40) NOT NULL, PRIMARY KEY (thread_id, seq))",
    "CREATE TABLE chat_memory (id NVARCHAR(40) COLLATE Latin1_General_100_BIN2 NOT NULL PRIMARY KEY, owner NVARCHAR(200) COLLATE Latin1_General_100_BIN2 NOT NULL, "
    "owner_role NVARCHAR(100) NOT NULL, content NVARCHAR(MAX) NOT NULL, redactions NVARCHAR(200) NOT NULL, item_class NVARCHAR(40) NOT NULL, source NVARCHAR(200) NOT NULL, "
    "created_at NVARCHAR(40) NOT NULL, updated_at NVARCHAR(40) NOT NULL, expires_at NVARCHAR(40) COLLATE Latin1_General_100_BIN2 NULL)",
    "CREATE TABLE chat_memory_control (scope NVARCHAR(20) COLLATE Latin1_General_100_BIN2 NOT NULL, ref NVARCHAR(200) COLLATE Latin1_General_100_BIN2 NOT NULL, "
    "enabled INT NOT NULL, actor NVARCHAR(200) NOT NULL, note NVARCHAR(200) NOT NULL, at NVARCHAR(40) NOT NULL, PRIMARY KEY (scope, ref))",
)
MSSQL_INDEX = ("IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'ix_chat_thread_owner' AND object_id = OBJECT_ID(N'chat_thread')) "
               "CREATE INDEX ix_chat_thread_owner ON chat_thread (owner, status, updated_at)")
# Columns added to chat_memory after the #163 table; CREATE TABLE IF NOT EXISTS would not add them to an existing table.
MEMORY_ADDED = (("item_class", "working_preference"), ("source", ""), ("updated_at", ""))
MSSQL_MIGRATE = tuple(
    f"IF COL_LENGTH(N'chat_memory', N'{c}') IS NULL ALTER TABLE chat_memory ADD {c} NVARCHAR({40 if c != 'source' else 200}) NOT NULL "
    f"CONSTRAINT df_chat_memory_{c} DEFAULT N'{d}'" for c, d in MEMORY_ADDED)


TABLE_NAMES = ("chat_memory_control", "chat_memory", "chat_message", "chat_thread")

THREAD_COLS = ("id", "owner", "owner_role", "case_id", "title", "task", "task_version", "model", "status", "rowversion",
               "message_count", "created_at", "updated_at")
MEMORY_COLS = ("id", "owner", "owner_role", "content", "redactions", "item_class", "source", "created_at", "updated_at", "expires_at")
CONTROL_COLS = ("scope", "ref", "enabled", "actor", "note", "at")
MEMORY_ID_PREFIX = "CM-"
MESSAGE_COLS = ("thread_id", "seq", "role", "content", "model", "task_version", "evidence", "created_at")


class ChatNotFound(LookupError):
    """No such thread for this user (a thread owned by someone else is reported the same way)."""


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def user_key(user):
    key = str((user or {}).get("email") or "").strip().lower()
    if not key:
        raise ValueError("A chat thread needs an authenticated user.")
    return key


class MemoryRepo:
    """Threads held in the Store's own document, so the in-memory Store persists them with its live file."""

    def __init__(self, store):
        self.store = store

    @property
    def doc(self):
        return self.store.data.setdefault("chat_threads", {})

    @contextmanager
    def txn(self):
        with self.store.lock:
            yield

    def insert_thread(self, t):
        self.doc[t["id"]] = dict(t, messages=[])

    def get(self, tid, owner):
        t = self.doc.get(tid)
        return None if t is None or t["owner"] != owner else {k: t[k] for k in THREAD_COLS}

    def list(self, owner, status):
        rows = [{k: t[k] for k in THREAD_COLS} for t in self.doc.values() if t["owner"] == owner and (status is None or t["status"] == status)]
        return sorted(rows, key=lambda t: (t["updated_at"], t["id"]), reverse=True)

    def update(self, tid, owner, expected, **fields):
        t = self.doc.get(tid)
        if t is None or t["owner"] != owner or t["rowversion"] != expected:
            return False
        t.update(fields, rowversion=expected + 1)
        return True

    def add_message(self, m):
        self.doc[m["thread_id"]]["messages"].append(dict(m))

    def messages(self, tid):
        return [dict(m) for m in self.doc[tid]["messages"]]

    def delete(self, tid):
        self.doc.pop(tid, None)

    @property
    def memory_doc(self):
        return self.store.data.setdefault("chat_memory", [])

    def insert_memory(self, m):
        self.memory_doc.append(dict(m))

    def memories(self, owner):
        return [dict(m) for m in self.memory_doc if m["owner"] == owner]

    def delete_memories(self, owner):
        keep = [m for m in self.memory_doc if m["owner"] != owner]
        n = len(self.memory_doc) - len(keep)
        self.memory_doc[:] = keep
        return n

    def update_memory(self, owner, mid, **fields):
        for m in self.memory_doc:
            if m["id"] == mid and m["owner"] == owner:
                m.update(fields)
                return True
        return False

    def delete_memory(self, owner, mid):
        keep = [m for m in self.memory_doc if not (m["id"] == mid and m["owner"] == owner)]
        n = len(self.memory_doc) - len(keep)
        self.memory_doc[:] = keep
        return n == 1

    @property
    def control_doc(self):
        return self.store.data.setdefault("chat_memory_control", {})

    def get_control(self, scope, ref):
        c = self.control_doc.get(f"{scope}:{ref}")
        return dict(c) if c else None

    def set_control(self, scope, ref, enabled, actor, note, at):
        self.control_doc[f"{scope}:{ref}"] = dict(scope=scope, ref=ref, enabled=int(enabled), actor=actor, note=note, at=at)

    def purge_memory(self, now):
        keep = [m for m in self.memory_doc if not (m["expires_at"] and m["expires_at"] < now)]
        n = len(self.memory_doc) - len(keep)
        self.memory_doc[:] = keep
        return n

    def commit(self):
        self.store.save()


class SqlRepo:
    """Threads in the SQL store's connection; the same statements run on SQLite and Azure SQL."""

    def __init__(self, store):
        self.store = store

    @contextmanager
    def txn(self):
        db = self.store.db
        with self.store.dblock:
            db.execute("BEGIN IMMEDIATE")
            try:
                yield
                db.execute("COMMIT")
            except BaseException:
                db.execute("ROLLBACK")
                raise

    def _row(self, cols, row):
        return dict(zip(cols, row))

    def insert_thread(self, t):
        self.store.db.execute(f"INSERT INTO chat_thread ({', '.join(THREAD_COLS)}) VALUES ({','.join('?' * len(THREAD_COLS))})",
                              tuple(t[c] for c in THREAD_COLS))

    def get(self, tid, owner):
        with self.store.dblock:
            row = self.store.db.execute(f"SELECT {', '.join(THREAD_COLS)} FROM chat_thread WHERE id=? AND owner=?", (tid, owner)).fetchone()
        return self._row(THREAD_COLS, row) if row else None

    def list(self, owner, status):
        sql, args = f"SELECT {', '.join(THREAD_COLS)} FROM chat_thread WHERE owner=?", [owner]
        if status:
            sql, args = sql + " AND status=?", args + [status]
        with self.store.dblock:
            rows = self.store.db.execute(sql + " ORDER BY updated_at DESC, id DESC", args).fetchall()
        return [self._row(THREAD_COLS, r) for r in rows]

    def update(self, tid, owner, expected, **fields):
        sets = "".join(f", {k}=?" for k in fields)
        cur = self.store.db.execute(f"UPDATE chat_thread SET rowversion=rowversion+1{sets} WHERE id=? AND owner=? AND rowversion=?",
                                    tuple(fields.values()) + (tid, owner, expected))
        return cur.rowcount == 1

    def add_message(self, m):
        row = dict(m, evidence=json.dumps(m["evidence"]))
        self.store.db.execute(f"INSERT INTO chat_message ({', '.join(MESSAGE_COLS)}) VALUES ({','.join('?' * len(MESSAGE_COLS))})",
                              tuple(row[c] for c in MESSAGE_COLS))

    def messages(self, tid):
        with self.store.dblock:
            rows = self.store.db.execute(f"SELECT {', '.join(MESSAGE_COLS)} FROM chat_message WHERE thread_id=? ORDER BY seq", (tid,)).fetchall()
        return [dict(self._row(MESSAGE_COLS, r), evidence=json.loads(r[6])) for r in rows]

    def delete(self, tid):
        self.store.db.execute("DELETE FROM chat_message WHERE thread_id=?", (tid,))
        self.store.db.execute("DELETE FROM chat_thread WHERE id=?", (tid,))

    def insert_memory(self, m):
        self.store.db.execute(f"INSERT INTO chat_memory ({', '.join(MEMORY_COLS)}) VALUES ({','.join('?' * len(MEMORY_COLS))})",
                              tuple(m[c] for c in MEMORY_COLS))

    def memories(self, owner):
        with self.store.dblock:
            rows = self.store.db.execute(f"SELECT {', '.join(MEMORY_COLS)} FROM chat_memory WHERE owner=? ORDER BY created_at, id", (owner,)).fetchall()
        return [self._row(MEMORY_COLS, r) for r in rows]

    def delete_memories(self, owner):
        return self.store.db.execute("DELETE FROM chat_memory WHERE owner=?", (owner,)).rowcount

    def update_memory(self, owner, mid, **fields):
        sets = ", ".join(f"{k}=?" for k in fields)
        return self.store.db.execute(f"UPDATE chat_memory SET {sets} WHERE id=? AND owner=?", tuple(fields.values()) + (mid, owner)).rowcount == 1

    def delete_memory(self, owner, mid):
        return self.store.db.execute("DELETE FROM chat_memory WHERE id=? AND owner=?", (mid, owner)).rowcount == 1

    def get_control(self, scope, ref):
        with self.store.dblock:
            row = self.store.db.execute(f"SELECT {', '.join(CONTROL_COLS)} FROM chat_memory_control WHERE scope=? AND ref=?", (scope, ref)).fetchone()
        return self._row(CONTROL_COLS, row) if row else None

    def set_control(self, scope, ref, enabled, actor, note, at):
        cur = self.store.db.execute("UPDATE chat_memory_control SET enabled=?, actor=?, note=?, at=? WHERE scope=? AND ref=?",
                                    (int(enabled), actor, note, at, scope, ref))
        if cur.rowcount == 0:
            self.store.db.execute(f"INSERT INTO chat_memory_control ({', '.join(CONTROL_COLS)}) VALUES ({','.join('?' * len(CONTROL_COLS))})",
                                  (scope, ref, int(enabled), actor, note, at))

    def purge_memory(self, now):
        return self.store.db.execute("DELETE FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?", (now,)).rowcount

    def commit(self):
        """The surrounding transaction commits."""


def _clean_evidence(evidence):
    refs = [str(r).strip() for r in (evidence or ()) if str(r).strip()]
    if len(refs) > MAX_EVIDENCE or any(len(r) > 200 for r in refs):
        raise ValueError(f"At most {MAX_EVIDENCE} evidence references of 200 characters.")
    if any(r.upper().startswith(MEMORY_ID_PREFIX) for r in refs):
        raise ValueError("Memory is never evidence and cannot be cited.")
    return refs


class ChatMixin:
    @property
    def chat_repo(self):
        repo = self.__dict__.get("_chat_repo")
        if repo is None:
            repo = self.__dict__["_chat_repo"] = SqlRepo(self) if hasattr(self, "assistant_connection") else MemoryRepo(self)
        return repo

    def _chat_conflict(self, tid):
        from .store import ConflictError
        return ConflictError(f"chat thread {tid}")

    def _chat_event(self, user, action, thread, **meta):
        """Ledger entry with metadata only; never message content or the title."""
        detail = json.dumps(dict(thread=thread["id"], messages=thread["message_count"], status=thread["status"], **meta), sort_keys=True)
        self.audit(user_key(user), action, thread["case_id"], detail)

    def _chat_owned(self, user, tid):
        t = self.chat_repo.get(tid, user_key(user))
        if t is None:
            raise ChatNotFound(tid)
        return t

    def chat_create_thread(self, user, case_id="", title="", task="", task_version="", model=""):
        from .assistants import REGISTRY, VERSION
        owner = user_key(user)
        if case_id and case_id not in self.cases:
            raise ValueError("Unknown case.")
        if task and task not in REGISTRY:
            raise ValueError("Unknown assistant task.")
        now = _now()
        t = dict(id="CT-" + uuid.uuid4().hex[:16], owner=owner, owner_role=str(user.get("role") or ""), case_id=case_id or "",
                 title=str(title or "New chat")[:200], task=task or "", task_version=task_version or (VERSION if task else ""),
                 model=str(model or "")[:100], status=ACTIVE, rowversion=1, message_count=0, created_at=now, updated_at=now)
        repo = self.chat_repo
        with repo.txn():
            repo.insert_thread(t)
            repo.commit()
        self._chat_event(user, "chat.thread.created", t, task=t["task"], task_version=t["task_version"], model=t["model"])
        return t

    def chat_add_message(self, user, tid, role, content, evidence=(), model="", expected_version=None):
        from .store import ConflictError
        if role not in ROLES:
            raise ValueError("Role must be user or assistant.")
        content = str(content or "")
        if not content.strip() or len(content) > MAX_CONTENT:
            raise ValueError(f"A message needs 1 to {MAX_CONTENT} characters.")
        refs, owner, repo = _clean_evidence(evidence), user_key(user), self.chat_repo
        with repo.txn():
            t = repo.get(tid, owner)
            if t is None:
                raise ChatNotFound(tid)
            if t["status"] != ACTIVE:
                raise ValueError("An archived thread is read only; restore it by starting a new thread.")
            if expected_version is not None and expected_version != t["rowversion"]:
                raise ConflictError(f"chat thread {tid}")
            now, seq = _now(), t["message_count"] + 1
            m = dict(thread_id=tid, seq=seq, role=role, content=content, evidence=refs, created_at=now,
                     model=str(model or t["model"])[:100] if role == "assistant" else "", task_version=t["task_version"] if role == "assistant" else "")
            if not repo.update(tid, owner, t["rowversion"], message_count=seq, updated_at=now):
                raise ConflictError(f"chat thread {tid}")
            repo.add_message(m)
            repo.commit()
        t = repo.get(tid, owner)
        self._chat_event(user, "chat.message.added", t, role=role, seq=seq, evidence_refs=len(refs))
        return m

    def chat_list_threads(self, user, include_archived=False):
        return self.chat_repo.list(user_key(user), None if include_archived else ACTIVE)

    def chat_resume(self, user, tid):
        """The thread and its messages in order, for the owner only."""
        t = self._chat_owned(user, tid)
        return dict(t, messages=self.chat_repo.messages(tid))

    def chat_archive(self, user, tid, expected_version=None):
        from .store import ConflictError
        owner, repo = user_key(user), self.chat_repo
        with repo.txn():
            t = repo.get(tid, owner)
            if t is None:
                raise ChatNotFound(tid)
            if expected_version is not None and expected_version != t["rowversion"]:
                raise ConflictError(f"chat thread {tid}")
            if t["status"] == ARCHIVED:
                return t
            if not repo.update(tid, owner, t["rowversion"], status=ARCHIVED, updated_at=_now()):
                raise ConflictError(f"chat thread {tid}")
            repo.commit()
        t = repo.get(tid, owner)
        self._chat_event(user, "chat.thread.archived", t)
        return t

    def chat_delete(self, user, tid, expected_version=None):
        from .store import ConflictError
        owner, repo = user_key(user), self.chat_repo
        with repo.txn():
            t = repo.get(tid, owner)
            if t is None:
                raise ChatNotFound(tid)
            if expected_version is not None and expected_version != t["rowversion"]:
                raise ConflictError(f"chat thread {tid}")
            repo.delete(tid)
            repo.commit()
        self._chat_event(user, "chat.thread.deleted", dict(t, status="deleted"))
