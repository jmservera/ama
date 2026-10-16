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
import os
import re
import struct

from .chatthreads import MSSQL_DDL as CHAT_DDL, MSSQL_INDEX as CHAT_INDEX, MSSQL_MIGRATE as CHAT_MIGRATE
from .sqlstore import INDEXES, SqlStore

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
  queue_new INT NOT NULL DEFAULT 0, queue_priority INT NOT NULL DEFAULT 0,
  queue_stale INT NOT NULL DEFAULT 0, queue_blocked INT NOT NULL DEFAULT 0,
  queue_overdue INT NOT NULL DEFAULT 0, queue_unowned INT NOT NULL DEFAULT 0)""",
    "recommendations": f"CREATE TABLE recommendations (id {_t(64)} PRIMARY KEY, rowversion BIGINT NOT NULL DEFAULT 1, seq BIGINT NOT NULL, "
                       f"[user] {_t(200)}, body NVARCHAR(MAX) NOT NULL)",
    "audit": f"""CREATE TABLE audit (
  seq BIGINT IDENTITY(1,1) PRIMARY KEY, at {_t(40)}, who {_t(200)}, action {_t(200)}, case_id {_t(64)},
  detail NVARCHAR(MAX) NOT NULL, prev {_t(100)}, hash {_t(100)} UNIQUE)""",
    "audit_head": f"CREATE TABLE audit_head (id INT PRIMARY KEY CHECK (id = 1), count BIGINT NOT NULL, hash {_t(100)})",
    "chat_thread": CHAT_DDL[0],
    "chat_message": CHAT_DDL[1],
    "chat_memory": CHAT_DDL[2],
    "chat_memory_control": CHAT_DDL[3],
}

APPEND_ONLY = ("IF OBJECT_ID(N'audit_append_only', N'TR') IS NULL EXEC(N'CREATE TRIGGER audit_append_only ON audit "
               "INSTEAD OF UPDATE, DELETE AS THROW 50001, ''audit ledger is append-only'', 1')")

BEGIN = ("BEGIN TRAN; DECLARE @r INT; EXEC @r = sp_getapplock @Resource = N'zavaforward_write', @LockMode = N'Exclusive', "
         "@LockOwner = N'Transaction', @LockTimeout = 15000; IF @r < 0 THROW 50002, 'could not take the write lock', 1;")

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
    def __init__(self, cur):
        self.cur = cur

    @property
    def rowcount(self):
        return self.cur.rowcount

    def fetchone(self):
        r = self.cur.fetchone()
        return None if r is None else tuple(r)

    def fetchall(self):
        return [tuple(r) for r in self.cur.fetchall()]


class _Conn:
    """The few sqlite3 calls SqlStore makes, over one mssql-python connection. Reconnects when the link was dropped between requests."""

    def __init__(self, conn_str, token=None):
        import mssql_python
        self.driver, self.conn_str, self.raw, self.in_tran = mssql_python, conn_str, None, False
        self.attrs = {}
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
        for attempt in (0, 1):
            try:
                if self.raw is None:
                    self._connect()
                cur = self.raw.cursor()
                (cur.executemany if many else cur.execute)(sql, args)
                return cur
            except self.driver.Error as e:
                dead = bool(_PROGRESS.search(str(e)))
                if dead:
                    self.raw = None
                if attempt or not dead or self.in_tran:
                    raise

    def execute(self, sql, args=()):
        key = sql.strip().upper()
        if key == "BEGIN IMMEDIATE":
            self._run(BEGIN, ())
            self.in_tran = True
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
        return _Cursor(self._run(self._rewrite(sql), tuple(args)))

    def executemany(self, sql, rows):
        return _Cursor(self._run(self._rewrite(sql), list(rows), many=True))

    def close(self):
        if self.raw is not None:
            self.raw.close()


class MssqlStore(SqlStore):
    def __init__(self, data_path, env=None, state_dir=None, **kw):
        self._env = os.environ if env is None else env
        super().__init__(data_path, os.path.join(state_dir or self._env.get("ZF_STATE") or ".", "mssql"), **kw)

    @property
    def dberror(self):
        import mssql_python
        return mssql_python.Error

    def _open(self, db_path):
        self.db = _Conn(connection_string(self._env), self._env.get("ZF_SQL_TOKEN"))

    _epoch_sql = "SELECT DATEDIFF_BIG(MILLISECOND, CONVERT(datetime2,'1970-01-01'), SYSUTCDATETIME()) / 1000.0"

    def assistant_connection(self):
        return _Conn(connection_string(self._env), self._env.get("ZF_SQL_TOKEN"))

    def _create_schema(self):
        with self.dblock:
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

    def _create_indexes(self):
        with self.dblock:
            for stmt in list(CHAT_MIGRATE) + _indexes() + [CHAT_INDEX]:
                self.db.execute(stmt)

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
