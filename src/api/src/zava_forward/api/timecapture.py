"""Staff time capture (PR-004). Built, but off.

It records nothing unless all of these hold:

* ZF_TIME_CAPTURE=on (the feature flag, off by default);
* DPIA_APPROVED=<reference of the approved DPIA> (bare yes, true, on and 1 are
  refused, ignoring case and surrounding whitespace; the trimmed reference is
  stored with every entry). This checks reference presence, not authenticity
  or legal approval;
* ZF_TIME_CONSULTATION=<reference of the completed staff consultation>, also
  stored with every entry;
* ZF_TIME_NOTICE_APPROVED=<reference of the approval of the staff notice
  wording>, stored with the enabling record;
* a manager has requested enabling (request_enable) and a manager in a different
  role has taken the audited enabling action (activate); the record stores the
  three references, who asked, who enabled and both roles;
* the person has acknowledged the current staff notice (NOTICE_VERSION). The
  acknowledgement is stored with the time and is audited by the server.

The enabling record, the entries and the notice acknowledgements live in the
shared SQL store (SQLite or Azure SQL, in their own tables, apart from case
data), so they share its backup, access control and retention. Only the JSON demo
store, which has no database, falls back to a local SQLite file (ZF_TIME_DB). A person sees only
their own entries. Reports are totals by activity for process measurement,
suppressed when fewer than ZF_TIME_MIN_GROUP different people (default 5)
contributed. There is no per-person report and no export of individual rows.
Using the data to rate a person needs a separate decision (PR-004). The notice
wording below is a draft for the DPIA and consultation owners to replace; the
paired-measurement definitions (OD-18) are not built here.
"""
import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime

ACTIVITIES = ("Calling the resident", "Case notes and updates", "Booking visits", "Funding and evidence", "Checking safety issues",
              "Handover and coordination", "Other")
MAX_MINUTES = 600
NOTICE_VERSION = "draft-1"
NOTICE_TEXT = ("Time capture records the minutes you choose to enter against a case and an activity. Only you can see your own entries. "
               "Managers see totals by activity, never by person, and groups of fewer than the minimum number of people are hidden. "
               "The entries are used to measure the process, not to rate you. Entering time is your choice to switch on case by case "
               "once you have read this notice.")


SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS time_entry (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, user_code TEXT NOT NULL, case_id TEXT NOT NULL, "
    "minutes INTEGER NOT NULL, activity TEXT NOT NULL, dpia_ref TEXT NOT NULL, consultation_ref TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS time_request (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, by_user TEXT NOT NULL, by_role TEXT NOT NULL, "
    "dpia_ref TEXT NOT NULL, consultation_ref TEXT NOT NULL, notice_ref TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS time_enabled (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, by_user TEXT NOT NULL, by_role TEXT NOT NULL, "
    "requested_by TEXT NOT NULL, requested_role TEXT NOT NULL, dpia_ref TEXT NOT NULL, consultation_ref TEXT NOT NULL, notice_ref TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS notice_ack (user_code TEXT NOT NULL, version TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (user_code, version))",
    "CREATE INDEX IF NOT EXISTS ix_time_user ON time_entry (user_code, id)",
)
MSSQL_DDL = (
    "CREATE TABLE time_entry (id BIGINT IDENTITY(1,1) PRIMARY KEY, at NVARCHAR(40) NOT NULL, user_code NVARCHAR(50) NOT NULL, case_id NVARCHAR(64) NOT NULL, "
    "minutes INT NOT NULL, activity NVARCHAR(100) NOT NULL, dpia_ref NVARCHAR(200) NOT NULL, consultation_ref NVARCHAR(200) NOT NULL)",
    "CREATE TABLE time_request (id BIGINT IDENTITY(1,1) PRIMARY KEY, at NVARCHAR(40) NOT NULL, by_user NVARCHAR(200) NOT NULL, by_role NVARCHAR(100) NOT NULL, "
    "dpia_ref NVARCHAR(200) NOT NULL, consultation_ref NVARCHAR(200) NOT NULL, notice_ref NVARCHAR(200) NOT NULL)",
    "CREATE TABLE time_enabled (id BIGINT IDENTITY(1,1) PRIMARY KEY, at NVARCHAR(40) NOT NULL, by_user NVARCHAR(200) NOT NULL, by_role NVARCHAR(100) NOT NULL, "
    "requested_by NVARCHAR(200) NOT NULL, requested_role NVARCHAR(100) NOT NULL, dpia_ref NVARCHAR(200) NOT NULL, consultation_ref NVARCHAR(200) NOT NULL, "
    "notice_ref NVARCHAR(200) NOT NULL)",
    "CREATE TABLE notice_ack (user_code NVARCHAR(50) NOT NULL, version NVARCHAR(50) NOT NULL, at NVARCHAR(40) NOT NULL, PRIMARY KEY (user_code, version))",
)
MSSQL_INDEX = ("IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'ix_time_user' AND object_id = OBJECT_ID(N'time_entry')) "
               "CREATE INDEX ix_time_user ON time_entry (user_code, id)")
TABLES = ("time_entry", "time_request", "time_enabled", "notice_ack")


class TimeCaptureOff(PermissionError):
    pass


class NoticeNotAcknowledged(PermissionError):
    pass


class SeparationOfDuties(PermissionError):
    pass


class TimeCapture:
    def __init__(self, store=None, env=None, db_path=None):
        self.env = os.environ if env is None else env
        self.store = store if hasattr(store, "assistant_connection") else None
        self.mssql = self.store is not None and hasattr(self.store, "_env")
        self.db_path = db_path or self.env.get("ZF_TIME_DB") or os.path.join(self.env.get("ZF_STATE") or ".", "time.sqlite")
        self.lock = threading.Lock()
        self.ready = False

    @property
    def where(self):
        return "the shared SQL store" if self.store is not None else f"a local SQLite file ({self.db_path}; JSON demo store only)"

    @contextmanager
    def _conn(self):
        """One connection per operation, to the shared SQL store when there is one."""
        if self.store is not None:
            db = self.store.assistant_connection()
        else:
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
            if self.mssql:
                for ddl in MSSQL_DDL:
                    db.execute(f"IF OBJECT_ID(N'{ddl.split()[2]}', N'U') IS NULL {ddl}")
                db.execute(MSSQL_INDEX)
            else:
                for ddl in SQLITE_DDL:
                    db.execute(ddl)
            self.ready = True

    def _top(self, n):
        return self.store._limit(n, 0) if self.store is not None else (" LIMIT ? OFFSET ?", [n, 0])

    def _exists(self):
        """Reading before anything was ever written must not create tables in a database that never used the feature."""
        return self.ready or self.store is not None or os.path.exists(self.db_path)

    @staticmethod
    def _now():
        return datetime.now().isoformat(timespec="minutes")

    def status(self, user=None):
        flag = (self.env.get("ZF_TIME_CAPTURE") or "").strip().lower() in ("1", "on", "true", "yes")
        dpia = (self.env.get("DPIA_APPROVED") or "").strip()
        dpia_recorded = bool(dpia) and dpia.casefold() not in ("yes", "true", "on", "1")
        consult = (self.env.get("ZF_TIME_CONSULTATION") or "").strip()
        notice = (self.env.get("ZF_TIME_NOTICE_APPROVED") or "").strip()
        req = self.request()
        act = self.activation()
        if not flag:
            why = "Time capture is switched off."
        elif not dpia_recorded:
            why = "Time capture cannot be switched on until a DPIA reference is recorded (DPIA_APPROVED), not a boolean flag such as yes, true, on or 1."
        elif not consult:
            why = "Time capture cannot be switched on until the staff consultation is recorded (ZF_TIME_CONSULTATION)."
        elif not notice:
            why = "Time capture cannot be switched on until the staff notice is approved (ZF_TIME_NOTICE_APPROVED)."
        elif not req:
            why = "Time capture is ready but needs an enabling request from a manager, then enabling by a manager in a different role."
        elif not act:
            why = f"Time capture is requested by {req['role']}; it needs enabling by a manager in a different role."
        else:
            why = ""
        out = dict(enabled=not why, flag_on=flag, dpia_recorded=dpia_recorded, consultation_recorded=bool(consult),
                   notice_approved=bool(notice), requested=bool(req), requested_by=req and req["by"], requested_role=req and req["role"],
                   activated=bool(act), activated_by=act and act["by"], activated_at=act and act["at"], activated_role=act and act["role"],
                   reason=why, activities=list(ACTIVITIES), min_group=self.min_group(), notice_version=NOTICE_VERSION, storage=self.where)
        if out["enabled"]:
            out["notice"] = NOTICE_TEXT
            if user is not None:
                out["acknowledged"] = self.acknowledged(user)
        return out

    def min_group(self):
        try:
            return max(2, int(self.env.get("ZF_TIME_MIN_GROUP", "5")))
        except ValueError:
            return 5

    def _refs(self):
        return tuple((self.env.get(k) or "").strip() for k in ("DPIA_APPROVED", "ZF_TIME_CONSULTATION", "ZF_TIME_NOTICE_APPROVED"))

    def _latest(self, sql):
        if not self._exists():
            return None
        lim, args = self._top(1)
        with self._conn() as db:
            return db.execute(sql + lim, args).fetchone()

    def request(self):
        """The enabling request, if it was made against the references currently configured."""
        r = self._latest("SELECT at, by_user, by_role, dpia_ref, consultation_ref, notice_ref FROM time_request ORDER BY id DESC")
        if not r or tuple(r[3:]) != self._refs():
            return None
        return dict(at=r[0], by=r[1], role=r[2])

    def activation(self):
        """The enabling record, if it was taken against the references currently configured."""
        r = self._latest("SELECT at, by_user, by_role, dpia_ref, consultation_ref, notice_ref FROM time_enabled ORDER BY id DESC")
        if not r or tuple(r[3:]) != self._refs():
            return None
        return dict(at=r[0], by=r[1], role=r[2])

    def _ready_to_enable(self):
        st = self.status()
        if not (st["flag_on"] and st["dpia_recorded"] and st["consultation_recorded"] and st["notice_approved"]):
            raise TimeCaptureOff(st["reason"])

    def request_enable(self, user):
        """A manager asks for capture to be enabled against the configured references. It enables nothing by itself. The caller audits it."""
        self._ready_to_enable()
        dpia, consult, notice = self._refs()
        with self._conn() as db:
            db.execute("INSERT INTO time_request (at, by_user, by_role, dpia_ref, consultation_ref, notice_ref) VALUES (?,?,?,?,?,?)",
                       (self._now(), user["email"], user["role"], dpia, consult, notice))
        return dict(dpia_ref=dpia, consultation_ref=consult, notice_ref=notice)

    def activate(self, user):
        """The enabling action. Needs the flag, the three references and a request by a manager in a different role: the
        person who asked cannot also enable, so no single role both proposes and switches on staff monitoring. The caller audits it."""
        self._ready_to_enable()
        req = self.request()
        if not req:
            raise SeparationOfDuties("Enabling needs a request first, made by a manager in a different role from the one who enables.")
        if req["by"] == user["email"] or req["role"] == user["role"]:
            raise SeparationOfDuties(f"The enabling request was made by {req['role']}. A manager in a different role must enable it.")
        dpia, consult, notice = self._refs()
        with self._conn() as db:
            db.execute("INSERT INTO time_enabled (at, by_user, by_role, requested_by, requested_role, dpia_ref, consultation_ref, notice_ref) "
                       "VALUES (?,?,?,?,?,?,?,?)", (self._now(), user["email"], user["role"], req["by"], req["role"], dpia, consult, notice))
        return dict(dpia_ref=dpia, consultation_ref=consult, notice_ref=notice, requested_by=req["by"], requested_role=req["role"])

    def _require(self):
        st = self.status()
        if not st["enabled"]:
            raise TimeCaptureOff(st["reason"])
        return (self.env.get("DPIA_APPROVED") or "").strip(), (self.env.get("ZF_TIME_CONSULTATION") or "").strip()

    def acknowledged(self, user):
        if not self._exists():
            return False
        with self._conn() as db:
            return db.execute("SELECT 1 FROM notice_ack WHERE user_code=? AND version=?", (user["code"], NOTICE_VERSION)).fetchone() is not None

    def acknowledge(self, user):
        """Record that this person has read the current notice. Idempotent. Refused while capture is not enabled."""
        self._require()
        with self._conn() as db:
            db.execute("INSERT INTO notice_ack (user_code, version, at) SELECT ?, ?, ? WHERE NOT EXISTS "
                       "(SELECT 1 FROM notice_ack WHERE user_code=? AND version=?)",
                       (user["code"], NOTICE_VERSION, self._now(), user["code"], NOTICE_VERSION))
        return NOTICE_VERSION

    def _require_ack(self, user):
        if not self.acknowledged(user):
            raise NoticeNotAcknowledged("Read and acknowledge the staff notice before recording time.")

    def record(self, user, case_id, minutes, activity):
        dpia, consult = self._require()
        self._require_ack(user)
        try:
            minutes = int(minutes)
        except (TypeError, ValueError):
            raise ValueError("Minutes must be a whole number.")
        if not 1 <= minutes <= MAX_MINUTES:
            raise ValueError(f"Minutes must be between 1 and {MAX_MINUTES}.")
        if activity not in ACTIVITIES:
            raise ValueError("Choose an activity from the list.")
        with self._conn() as db:
            db.execute("INSERT INTO time_entry (at, user_code, case_id, minutes, activity, dpia_ref, consultation_ref) VALUES (?,?,?,?,?,?,?)",
                       (self._now(), user["code"], str(case_id)[:40], minutes, activity, dpia, consult))

    def mine(self, user):
        self._require()
        self._require_ack(user)
        lim, args = self._top(200)
        with self._conn() as db:
            rows = db.execute("SELECT at, case_id, minutes, activity FROM time_entry WHERE user_code=? ORDER BY id DESC" + lim,
                              (user["code"], *args)).fetchall()
        return [dict(at=a, case_id=c, minutes=m, activity=t) for a, c, m, t in rows]

    def report(self):
        """Totals by activity, with groups of too few people suppressed. Never lists a person."""
        self._require()
        k = self.min_group()
        with self._conn() as db:
            rows = db.execute("SELECT activity, COUNT(*), SUM(minutes), COUNT(DISTINCT user_code) FROM time_entry GROUP BY activity").fetchall()
        out = [dict(activity=a, entries=n, minutes=m) for a, n, m, people in rows if people >= k]
        hidden = sum(1 for _, _, _, people in rows if people < k)
        return dict(by_activity=out, suppressed_activities=hidden, min_group=k,
                    note="Totals for process measurement. Groups with fewer than the minimum number of people are hidden. No individual rows.")
