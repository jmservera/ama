"""Azure SQL / SQL Server store behind the Store interface (ADR 0002 decision 1).

SqlStore holds the logic; this class only supplies the T-SQL dialect and the connection:

* a small connection adapter that speaks the sqlite3 calls SqlStore makes. BEGIN IMMEDIATE becomes a transaction holding
  an exclusive application lock, so writers are serialised across every replica exactly as SQLite's write lock does;
* binary collation on every compared or sorted text column, so ordering, the ranking key and equality match SQLite;
* an append-only ledger table for the audit ledger when the database is ledger enabled (Azure SQL ledger: the engine
  itself refuses UPDATE and DELETE and keeps a verifiable digest). Otherwise an INSTEAD OF trigger does the same.

Authentication is Microsoft Entra. ZF_SQL_AUTH=msi uses the app's managed identity (no password anywhere);
default uses the developer's Azure login; token takes a bearer token for one-off operator tasks such as the first seed; password is for the CI SQL Server container only.
The driver is mssql-python (pinned in requirements.txt); it is imported only when this store is chosen.
"""
import contextlib
import json
import os
import re
import struct
import logging
import threading
import time

from .chatthreads import MEMORY_ADDED as CHAT_MEMORY_ADDED, MSSQL_DDL as CHAT_DDL, MSSQL_INDEX as CHAT_INDEX
from . import continuity, ranking, stock
from .sqlstore import CASE_COLS, INDEXES, QUEUE_COLS, SqlStore

COLLATE = "COLLATE Latin1_General_100_BIN2"


def _t(n, col="NVARCHAR"):
    return f"{col}({n}) {COLLATE} NOT NULL"


TABLES = {
    "meta": f"CREATE TABLE meta ([key] {_t(64)} PRIMARY KEY, value NVARCHAR(MAX) NOT NULL)",
    "staff": f"CREATE TABLE staff (email {_t(200)} PRIMARY KEY, body NVARCHAR(MAX) NOT NULL)",
    "cases": f"""CREATE TABLE cases (
  id {_t(64)} PRIMARY KEY, rowversion BIGINT NOT NULL DEFAULT 1, seq BIGINT NOT NULL,
  stage {_t(100)}, area {_t(100)}, wave {_t(50)}, owner_code {_t(50)},
  closed INT NOT NULL, hazard INT NOT NULL, postcode {_t(20)}, address {_t(400)},
  body NVARCHAR(MAX) NOT NULL, support INT NOT NULL DEFAULT 0, days INT NOT NULL DEFAULT 0, rkey {_t(200)} DEFAULT '',
  contractor {_t(200)} DEFAULT '', search NVARCHAR(MAX) {COLLATE} NOT NULL DEFAULT '', search_c NVARCHAR(MAX) {COLLATE} NOT NULL DEFAULT '',
  surname {_t(200)} DEFAULT '', last_contact {_t(40)} DEFAULT '0000', next_visit {_t(40)} DEFAULT '9999',
  decision {_t(40)} DEFAULT '', fstatus {_t(40)} DEFAULT '',
  priority_correction INT NOT NULL DEFAULT 0,
  queue_new INT NOT NULL DEFAULT 0, queue_priority INT NOT NULL DEFAULT 0,
  queue_stale INT NOT NULL DEFAULT 0, queue_blocked INT NOT NULL DEFAULT 0,
  queue_overdue INT NOT NULL DEFAULT 0, queue_unowned INT NOT NULL DEFAULT 0)""",
    "recommendations": f"CREATE TABLE recommendations (id {_t(64)} PRIMARY KEY, rowversion BIGINT NOT NULL DEFAULT 1, seq BIGINT NOT NULL, "
                       f"[user] {_t(200)}, body NVARCHAR(MAX) NOT NULL, created_ord BIGINT NOT NULL DEFAULT 0)",
    "audit": f"""CREATE TABLE audit (
  seq BIGINT IDENTITY(1,1) PRIMARY KEY, at {_t(40)}, who {_t(200)}, action {_t(200)}, case_id {_t(64)},
  detail NVARCHAR(MAX) NOT NULL, prev {_t(100)}, hash {_t(100)} UNIQUE)""",
    "audit_head": f"CREATE TABLE audit_head (id INT PRIMARY KEY CHECK (id = 1), count BIGINT NOT NULL, hash {_t(100)})",
    "continuity_gate_state": f"CREATE TABLE continuity_gate_state (id INT PRIMARY KEY CHECK (id = 1), gate_version VARCHAR(64) {COLLATE} NOT NULL, epoch BIGINT NOT NULL DEFAULT 0)",
    "continuity_open_holds": f"CREATE TABLE continuity_open_holds (scope VARCHAR(64) {COLLATE} PRIMARY KEY, incident_id VARCHAR(64) {COLLATE} NOT NULL, epoch BIGINT NOT NULL)",
    "chat_thread": CHAT_DDL[0],
    "chat_message": CHAT_DDL[1],
    "chat_memory": CHAT_DDL[2],
    "chat_memory_control": CHAT_DDL[3],
}

def _plain(n):
    return f"NVARCHAR({n}) {COLLATE}"


# Column types for migrations on a ledger table, equal to the fresh-create DDL above (the legacy path keeps the caller's type).
LEDGER_TYPES = {
    ("cases", "stage"): _plain(100), ("cases", "area"): _plain(100), ("cases", "wave"): _plain(50), ("cases", "owner_code"): _plain(50),
    ("cases", "postcode"): _plain(20), ("cases", "address"): _plain(400), ("cases", "rkey"): _plain(200),
    ("cases", "contractor"): _plain(200), ("cases", "surname"): _plain(200), ("cases", "last_contact"): _plain(40),
    ("cases", "next_visit"): _plain(40), ("cases", "decision"): _plain(40), ("cases", "fstatus"): _plain(40),
    ("cases", "body"): _plain("MAX"), ("cases", "search"): _plain("MAX"), ("cases", "search_c"): _plain("MAX"),
}

APPEND_ONLY = ("IF OBJECT_ID(N'audit_append_only', N'TR') IS NULL EXEC(N'CREATE TRIGGER audit_append_only ON audit "
               "INSTEAD OF UPDATE, DELETE AS THROW 50001, ''audit ledger is append-only'', 1')")

GATE_TRIGGERS = (
    "IF OBJECT_ID(N'continuity_gate_no_delete', N'TR') IS NULL EXEC(N'CREATE TRIGGER continuity_gate_no_delete ON continuity_gate_state "
    "INSTEAD OF DELETE AS IF EXISTS (SELECT 1 FROM deleted) THROW 50004, ''continuity gate state cannot be deleted'', 1')",
    "IF OBJECT_ID(N'continuity_gate_monotonic', N'TR') IS NULL EXEC(N'CREATE TRIGGER continuity_gate_monotonic ON continuity_gate_state "
    "AFTER UPDATE AS IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE i.epoch < d.epoch) "
    "THROW 50004, ''continuity gate epoch is monotonic'', 1')",
)

BEGIN = ("BEGIN TRAN; DECLARE @r INT; EXEC @r = sp_getapplock @Resource = N'zavaforward_write', @LockMode = N'Exclusive', "
         "@LockOwner = N'Transaction', @LockTimeout = 15000; IF @r < 0 THROW 50002, 'could not take the write lock', 1;")

LOCK_WAIT_MS = 15000
LOCK_FAILED = "could not take the write lock"
_DRIVER_MODULES = ("mssql_python", "pyodbc")
_DRIVER_ERRORS = ("ProgrammingError", "DatabaseError")


def is_write_lock_busy(exc: BaseException | None) -> bool:
    """True when exc, or an exception it chains from, is the driver error for a timed-out write lock (SQL error 50002).

    The driver is recognised by class and module name so this needs no optional import."""
    seen: set[int] = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        kind = type(exc)
        if kind.__module__.split(".")[0] in _DRIVER_MODULES and kind.__name__ in _DRIVER_ERRORS and LOCK_FAILED in str(exc):
            return True
        exc = exc.__cause__ or exc.__context__
    return False


_SQLSTATE = re.compile(r"[0-9A-Z]{5}")


def driver_sqlstate(exc: BaseException | None) -> str:
    """The five-character SQLSTATE the driver reports for exc or its chain, or "" when none; never the message text."""
    seen: set[int] = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if type(exc).__module__.split(".")[0] in _DRIVER_MODULES and exc.args:
            code = exc.args[0]
            if isinstance(code, str) and _SQLSTATE.fullmatch(code):
                return code
        exc = exc.__cause__ or exc.__context__
    return ""


LOCK_RETRY_ATTEMPTS = 8
LOCK_RETRY_BASE = 1.0
LOCK_RETRY_CAP = 30.0
LINK_RETRY_ATTEMPTS = 4  # extra reconnects, with backoff, while the store starts
_sleep = time.sleep
_log = logging.getLogger(__name__)

_PROGRESS = re.compile(r"(?i)\bcommunication link\b|connection (?:is )?(?:dead|closed|reset)|08S01|08001|08003|08007|timeout expired|TCP Provider")


def _indexes():
    """The SQLite INDEXES script as idempotent T-SQL (filtered index for the partial one, brackets not needed)."""
    out = []
    for line in INDEXES.splitlines():
        m = re.match(r"CREATE INDEX IF NOT EXISTS (\w+) ON (\w+) \((.*?)\)(?: WHERE (.*))?;$", line)
        if m:
            name, table, cols, where = m.groups()
            stmt = f"CREATE INDEX {name} ON {table} ({cols})" + (f" WHERE {where}" if where else "")
            out.append(f"IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'{name}' AND object_id = OBJECT_ID(N'{table}')) {stmt}")
    return out


def connection_string(env=None):
    """Build the ODBC style connection string from ZF_SQL_* settings."""
    env = os.environ if env is None else env
    server, database = env.get("ZF_SQL_SERVER"), env.get("ZF_SQL_DATABASE")
    if not server or not database:
        raise SystemExit("ZF_STORE=mssql needs ZF_SQL_SERVER (for example myserver.database.windows.net) and ZF_SQL_DATABASE.")
    port = env.get("ZF_SQL_PORT") or "1433"
    parts = [f"Server=tcp:{server},{port}", f"Database={database}", "Encrypt=yes"]
    if env.get("ZF_SQL_TRUST_CERT") == "1":
        parts.append("TrustServerCertificate=yes")
    auth = (env.get("ZF_SQL_AUTH") or "msi").lower()
    if auth == "msi":
        parts.append("Authentication=ActiveDirectoryMSI")
        if env.get("ZF_SQL_CLIENT_ID"):
            parts.append(f"UID={env['ZF_SQL_CLIENT_ID']}")
    elif auth == "default":
        parts.append("Authentication=ActiveDirectoryDefault")
    elif auth == "token":
        if not env.get("ZF_SQL_TOKEN"):
            raise SystemExit("ZF_SQL_AUTH=token needs ZF_SQL_TOKEN (az account get-access-token --resource https://database.windows.net/), for one-off operator tasks.")
    elif auth == "password":
        if not env.get("ZF_SQL_USER") or not env.get("ZF_SQL_PASSWORD"):
            raise SystemExit("ZF_SQL_AUTH=password needs ZF_SQL_USER and ZF_SQL_PASSWORD (CI containers only, never Azure).")
        parts += [f"UID={env['ZF_SQL_USER']}", f"PWD={env['ZF_SQL_PASSWORD']}"]
    else:
        raise SystemExit(f"Unknown ZF_SQL_AUTH {auth!r}. Use msi, default, token or password.")
    return ";".join(parts) + ";"


class _Cursor:
    """Rows are read inside the connection guard, so no cursor keeps a result open on the shared connection."""

    def __init__(self, cur, rows=None, rowcount=None):
        self.cur, self.rows = cur, rows
        self._rowcount = cur.rowcount if rowcount is None else rowcount

    @property
    def rowcount(self):
        return self._rowcount

    def fetchone(self):
        if self.rows is not None:
            return self.rows.pop(0) if self.rows else None
        r = self.cur.fetchone()
        return None if r is None else tuple(r)

    def fetchall(self):
        if self.rows is not None:
            rows, self.rows = self.rows, []
            return rows
        return [tuple(r) for r in self.cur.fetchall()]

    def __iter__(self):
        return iter(self.fetchall())


class _Conn:
    """The few sqlite3 calls SqlStore makes, over one mssql-python connection. Reconnects when the link was dropped between requests."""

    def __init__(self, conn_str, token=None):
        import mssql_python
        self.driver, self.conn_str, self.raw, self.in_tran = mssql_python, conn_str, None, False
        self.attrs = {}
        self.startup_retries = 0  # extra BEGIN attempts after a lock timeout; non-zero only while the store starts
        if token:
            raw = token.encode("utf-16-le")
            self.attrs = {1256: struct.pack("<I", len(raw)) + raw}  # SQL_COPT_SS_ACCESS_TOKEN
        self._connect()

    def _connect(self):
        self.raw = self.driver.connect(self.conn_str, autocommit=True, **({"attrs_before": self.attrs} if self.attrs else {}))

    @staticmethod
    def _rewrite(sql):
        # key and user are reserved words in T-SQL; the shared SQL uses them as plain column names.
        if re.search(r"\bmeta\b", sql):
            sql = re.sub(r"(?<![\[\w])(?<!PRIMARY )key\b(?!\])", "[key]", sql)
        if re.search(r"\brecommendations\b", sql):
            sql = re.sub(r"(?<![\[\w])user\b(?!\])", "[user]", sql)
        return sql

    def _run(self, sql, args, many=False):
        # mssql-python is thread-safety level 1: threads must not share a connection concurrently.
        # One statement runs and its rows are read at a time (issue #2195: live chat 500s).
        guard = self.__dict__.setdefault("guard", threading.RLock())
        with guard:
            starting = bool(getattr(self, "startup_retries", 0))
            attempts = 2 + (LINK_RETRY_ATTEMPTS if starting else 0)
            for attempt in range(attempts):
                try:
                    if self.raw is None:
                        self._connect()
                    cur = self.raw.cursor()
                    (cur.executemany if many else cur.execute)(sql, args)
                    rowcount = cur.rowcount
                    if getattr(cur, "description", None) is None:
                        return _Cursor(cur, None, rowcount)
                    return _Cursor(cur, [tuple(r) for r in cur.fetchall()], rowcount)
                except self.driver.Error as e:
                    dead = bool(_PROGRESS.search(str(e)))
                    if dead:
                        self.raw = None
                    if attempt == attempts - 1 or not dead or self.in_tran:
                        raise
                    if attempt and starting:
                        # A link that is still down right after a reconnect (a brief SQL outage) needs time, not another immediate try.
                        _sleep(min(LOCK_RETRY_CAP, LOCK_RETRY_BASE * 2 ** (attempt - 1)))

    def execute(self, sql, args=()):
        key = sql.strip().upper()
        if key == "BEGIN IMMEDIATE":
            self._begin()
            return None
        if key in ("COMMIT", "ROLLBACK"):
            try:
                if key == "COMMIT":
                    self._run("COMMIT TRAN", ())
                else:
                    self._run("IF @@TRANCOUNT > 0 ROLLBACK TRAN", ())
            except self.driver.Error:
                if key == "COMMIT":
                    raise
            finally:
                self.in_tran = False
            return None
        return self._run(self._rewrite(sql), tuple(args))

    def _begin_sql(self):
        wait = getattr(self.__dict__.get("_wait"), "ms", None)
        return BEGIN if wait is None else BEGIN.replace(f"@LockTimeout = {LOCK_WAIT_MS}", f"@LockTimeout = {int(wait)}")

    @contextlib.contextmanager
    def write_wait(self, ms):
        """Cap how long this thread waits for the write lock, for example for a GET that only records a comparison."""
        local = self.__dict__.setdefault("_wait", threading.local())
        before = getattr(local, "ms", None)
        local.ms = ms
        try:
            yield
        finally:
            local.ms = before

    def _begin(self):
        """Take the write lock. During start-up a lock timeout is retried with backoff, so a long writer delays the start
        instead of crash-looping the app (issue #2244). Any other failure, and the last timeout, propagate unchanged."""
        retries = self.startup_retries
        for attempt in range(retries + 1):
            try:
                self._run(self._begin_sql(), ())
                self.in_tran = True
                return
            except BaseException as e:
                self._abandon_partial_begin()
                if attempt >= retries or not isinstance(e, self.driver.Error) or LOCK_FAILED not in str(e):
                    raise
                delay = min(LOCK_RETRY_CAP, LOCK_RETRY_BASE * 2 ** attempt)
                _log.warning("SQL write lock busy at start-up; retry %d of %d in %.0f s", attempt + 1, retries, delay)
                _sleep(delay)

    def _abandon_partial_begin(self):
        """BEGIN TRAN may have run before the lock request failed; never leave that transaction open.

        If it cannot be rolled back, discard the connection, which ends it on the server. The original error is kept."""
        self.in_tran = False
        if self.raw is None:
            return
        try:
            self.raw.cursor().execute("IF @@TRANCOUNT > 0 ROLLBACK TRAN")
        except BaseException:
            try:
                self.raw.close()
            except BaseException:
                pass
            self.raw = None

    def executemany(self, sql, rows):
        return self._run(self._rewrite(sql), list(rows), many=True)

    def close(self):
        if self.raw is not None:
            self.raw.close()


class MssqlStore(SqlStore):
    def _priority_correction_rows(self):
        rows = self.db.execute("""
            SELECT c.id, ch.id, ch.target
            FROM cases AS c
            CROSS APPLY OPENJSON(c.body, '$.affected_challenges')
            WITH (id NVARCHAR(64) '$.id',
                  target NVARCHAR(MAX) '$.target' AS JSON,
                  outcome NVARCHAR(64) '$.resolution.outcome',
                  preserved BIT '$.prior_correction_preserved') AS ch
            WHERE c.priority_correction = 1
              AND (ch.outcome COLLATE Latin1_General_100_BIN2 = 'Correction recorded'
                   OR ch.preserved = 1)
        """).fetchall()
        return [(cid, rid, json.loads(target)) for cid, rid, target in rows]

    def __init__(self, data_path, env=None, state_dir=None, **kw):
        self._env = os.environ if env is None else env
        super().__init__(data_path, os.path.join(state_dir or self._env.get("ZF_STATE") or ".", "mssql"), **kw)

    @property
    def dberror(self):
        import mssql_python
        return mssql_python.Error

    def _open(self, db_path):
        self.db = _Conn(connection_string(self._env), self._env.get("ZF_SQL_TOKEN"))
        self.db.startup_retries = LOCK_RETRY_ATTEMPTS - 1

    def write_wait(self, ms):
        return self.db.write_wait(ms)

    def _initialize(self, *args):
        try:
            super()._initialize(*args)
        finally:
            db = getattr(self, "db", None)
            if isinstance(db, _Conn):
                db.startup_retries = 0

    _epoch_sql = "SELECT DATEDIFF_BIG(MILLISECOND, CONVERT(datetime2,'1970-01-01'), SYSUTCDATETIME()) / 1000.0"

    def _is_ledger_table(self, table):
        row = self.db.execute("SELECT ledger_type FROM sys.tables WHERE object_id = OBJECT_ID(?)", (table,)).fetchone()
        return bool(row and row[0])

    def _add_column_default(self, table, col, sqltype, default, constraint=None):
        """A ledger table accepts only a nullable column with no default, so add it nullable, backfill the default, then
        enforce non-null with a CHECK and the default with a constraint. The caller's open transaction makes it all-or-nothing."""
        if not self._is_ledger_table(table):
            named = f" CONSTRAINT {constraint}" if constraint else ""
            self.db.execute(f"ALTER TABLE {table} ADD {col} {sqltype} NOT NULL{named} DEFAULT {default}")
            return
        sqltype = "INT" if sqltype == "INTEGER" else LEDGER_TYPES.get((table, col), sqltype)
        if sqltype == "TEXT":
            raise SystemExit(f"No ledger column type is defined for {table}.{col}.")
        self.db.execute(f"ALTER TABLE {table} ADD {col} {sqltype} NULL")
        self.db.execute(f"UPDATE {table} SET {col} = {default} WHERE {col} IS NULL")
        self.db.execute(f"ALTER TABLE {table} ADD CONSTRAINT ck_{table}_{col}_nn CHECK ({col} IS NOT NULL)")
        self.db.execute(f"ALTER TABLE {table} ADD CONSTRAINT {constraint or f'df_{table}_{col}'} DEFAULT {default} FOR {col}")

    def _chat_memory_current(self):
        """Read-only: every column the chat memory migration would add already exists (no write lock needed)."""
        cols = [("chat_memory", c) for c, _ in CHAT_MEMORY_ADDED] + [("chat_message", "actor_role")]
        return all(self.db.execute("SELECT COL_LENGTH(?, ?)", (t, c)).fetchone()[0] is not None for t, c in cols)

    def _migrate_current(self):
        """Read-only: derived columns, rank policy, identity columns and the continuity gate are already current (issue #2244).

        Anything unusual returns False and takes the locked path, which owns every repair."""
        have = self._columns()
        if not have >= set(CASE_COLS):
            return False
        row = self.db.execute("SELECT value FROM meta WHERE key='rank_policy'").fetchone()
        encoding = self.db.execute("SELECT value FROM meta WHERE key='support_encoding'").fetchone()
        if (row[0] if row else None) != ranking.CURRENT["version"] or (encoding[0] if encoding else None) != stock.SUPPORT_ENCODING:
            return False
        if next(self._identity_drift(), None) is not None:
            return False
        return continuity.gate_in_sync(self.db, mssql=hasattr(self, "_env"))

    def _migrate(self):
        with self.dblock:
            if self._migrate_current():
                return
            super()._migrate()

    def _migrate_queues(self):
        # Read-only fast path (issue #2244): nothing to add, so do not queue for the global write lock.
        if set(QUEUE_COLS) <= self._columns():
            return
        super()._migrate_queues()

    def _migrate_chat_memory(self):
        with self.dblock:
            if self._chat_memory_current():
                return
            self.db.execute("BEGIN IMMEDIATE")
            try:
                for col, default in CHAT_MEMORY_ADDED:
                    if self.db.execute("SELECT COL_LENGTH(N'chat_memory', ?)", (col,)).fetchone()[0] is None:
                        self._add_column_default("chat_memory", col, f"NVARCHAR({200 if col == 'source' else 40})", f"N'{default}'", f"df_chat_memory_{col}")
                if self.db.execute("SELECT COL_LENGTH(N'chat_message', N'actor_role')").fetchone()[0] is None:
                    self._add_column_default("chat_message", "actor_role", "NVARCHAR(100)", "N''", "df_chat_message_actor_role")
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    def assistant_connection(self):
        return _Conn(connection_string(self._env), self._env.get("ZF_SQL_TOKEN"))

    def _schema_current(self):
        """Read-only: every table exists and the append-only guard is in place, so start-up needs no write lock (issue #2244).

        Anything unusual returns False and takes the locked path, which also owns the explicit ledger error."""
        have = {r[0] for r in self.db.execute("SELECT name FROM sys.tables").fetchall()}
        if not set(TABLES) <= have:
            return False
        if self.db.execute("SELECT is_ledger_on FROM sys.databases WHERE name = DB_NAME()").fetchone()[0]:
            row = self.db.execute("SELECT ledger_type_desc FROM sys.tables WHERE name = N'audit'").fetchone()
            return bool(row) and row[0] == "APPEND_ONLY_LEDGER_TABLE"
        triggers = {r[0] for r in self.db.execute("SELECT name FROM sys.triggers").fetchall()}
        return {"audit_append_only", "continuity_gate_no_delete", "continuity_gate_monotonic"} <= triggers

    def _create_schema(self):
        with self.dblock:
            if self._schema_current():
                return
            self.db.execute("BEGIN IMMEDIATE")
            try:
                self._create_schema_serialized()
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    def _create_schema_serialized(self):
        with self.dblock:
            ledger = bool(self.db.execute("SELECT is_ledger_on FROM sys.databases WHERE name = DB_NAME()").fetchone()[0])
            for name, ddl in TABLES.items():
                if ledger and name == "audit":
                    ddl += " WITH (LEDGER = ON (APPEND_ONLY = ON))"
                self.db.execute(f"IF OBJECT_ID(N'{name}', N'U') IS NULL {ddl}")
            if ledger:
                kind = self.db.execute("SELECT ledger_type_desc FROM sys.tables WHERE name = N'audit'").fetchone()[0]
                if kind != "APPEND_ONLY_LEDGER_TABLE":
                    raise SystemExit(f"audit is a {kind}, not an append-only ledger table; drop and recreate it before starting.")
            else:
                self.db.execute(APPEND_ONLY)
                for trigger in GATE_TRIGGERS:
                    self.db.execute(trigger)

    def _has_rec_order(self):
        return self.db.execute("SELECT COL_LENGTH(N'recommendations', N'created_ord')").fetchone()[0] is not None

    def _rec_order_indexes_present(self):
        have = {r[0] for r in self.db.execute("SELECT name FROM sys.indexes WHERE name IS NOT NULL").fetchall()}
        return {"ix_recs_created_ord", "ix_recs_user_ord"} <= have

    def _create_rec_order_index(self):
        self.db.execute("IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'ix_recs_created_ord' AND object_id = OBJECT_ID(N'recommendations')) "
                        "CREATE INDEX ix_recs_created_ord ON recommendations (created_ord)")
        self.db.execute("IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'ix_recs_user_ord' AND object_id = OBJECT_ID(N'recommendations')) "
                        "CREATE INDEX ix_recs_user_ord ON recommendations ([user], created_ord)")

    def _indexes_current(self, statements):
        """Read-only: every index the script would create already exists."""
        have = {r[0] for r in self.db.execute("SELECT name FROM sys.indexes WHERE name IS NOT NULL").fetchall()}
        return all(m.group(1) in have for m in (re.search(r"CREATE INDEX (\w+)", st) for st in statements) if m)

    def _create_indexes(self):
        with self.dblock:
            self._migrate_chat_memory()
            statements = _indexes() + [CHAT_INDEX]
            if self._indexes_current(statements):
                return
            # check-then-create is not atomic across connections; the write lock serializes concurrent first opens
            self.db.execute("BEGIN IMMEDIATE")
            try:
                for stmt in statements:
                    self.db.execute(stmt)
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    def _columns(self):
        return {r[0] for r in self.db.execute("SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(N'cases')").fetchall()}

    def _meta_set(self, key, value):
        self.db.execute("MERGE meta AS t USING (SELECT ? AS k, ? AS v) AS s ON t.[key] = s.k "
                        "WHEN MATCHED THEN UPDATE SET value = s.v WHEN NOT MATCHED THEN INSERT ([key], value) VALUES (s.k, s.v);", (key, value))

    def _insert_ignore(self, table, cols, vals):
        names = ", ".join(f"[{c}]" for c in cols)
        self.db.execute(f"IF NOT EXISTS (SELECT 1 FROM {table} WHERE [{cols[0]}] = ?) INSERT INTO {table} ({names}) VALUES ({','.join('?' * len(cols))})",
                        (vals[0],) + tuple(vals))

    @staticmethod
    def _contains(col):
        return f"CHARINDEX(?, {col}) > 0"

    @staticmethod
    def _limit(limit, offset):
        return " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", [offset, limit]

    def explain(self, sql, args=()):
        raise NotImplementedError("Use SET SHOWPLAN_XML or Query Store on Azure SQL.")
