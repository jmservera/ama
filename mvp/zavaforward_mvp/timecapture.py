"""Staff time capture (PR-004). Built, but off.

It records nothing unless all of these hold:

* ZF_TIME_CAPTURE=on (the feature flag, off by default);
* DPIA_APPROVED=<reference of the approved DPIA> (it cannot be a bare yes: the
  reference is stored with every entry);
* ZF_TIME_CONSULTATION=<reference of the completed staff consultation>, also
  stored with every entry;
* the person has acknowledged the current staff notice (NOTICE_VERSION). The
  acknowledgement is stored with the time and is audited by the server.

Entries live in their own database, apart from case data. A person sees only
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
from datetime import datetime

ACTIVITIES = ("Calling the resident", "Case notes and updates", "Booking visits", "Funding and evidence", "Checking safety issues",
              "Handover and coordination", "Other")
MAX_MINUTES = 600
NOTICE_VERSION = "draft-1"
NOTICE_TEXT = ("Time capture records the minutes you choose to enter against a case and an activity. Only you can see your own entries. "
               "Managers see totals by activity, never by person, and groups of fewer than the minimum number of people are hidden. "
               "The entries are used to measure the process, not to rate you. Entering time is your choice to switch on case by case "
               "once you have read this notice.")


class TimeCaptureOff(PermissionError):
    pass


class NoticeNotAcknowledged(PermissionError):
    pass


class TimeCapture:
    def __init__(self, db_path=None, env=None):
        self.env = os.environ if env is None else env
        self.db_path = db_path or self.env.get("ZF_TIME_DB") or os.path.join(self.env.get("ZF_STATE") or ".", "time.sqlite")
        self.lock = threading.Lock()
        self.db = None

    def status(self, user=None):
        flag = (self.env.get("ZF_TIME_CAPTURE") or "").strip().lower() in ("1", "on", "true", "yes")
        dpia = (self.env.get("DPIA_APPROVED") or "").strip()
        consult = (self.env.get("ZF_TIME_CONSULTATION") or "").strip()
        if not flag:
            why = "Time capture is switched off."
        elif not dpia:
            why = "Time capture cannot be switched on until a DPIA reference is recorded (DPIA_APPROVED)."
        elif not consult:
            why = "Time capture cannot be switched on until the staff consultation is recorded (ZF_TIME_CONSULTATION)."
        else:
            why = ""
        out = dict(enabled=flag and bool(dpia) and bool(consult), flag_on=flag, dpia_recorded=bool(dpia), consultation_recorded=bool(consult),
                   reason=why, activities=list(ACTIVITIES), min_group=self.min_group(), notice_version=NOTICE_VERSION)
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

    def _require(self):
        st = self.status()
        if not st["enabled"]:
            raise TimeCaptureOff(st["reason"])
        return (self.env.get("DPIA_APPROVED") or "").strip(), (self.env.get("ZF_TIME_CONSULTATION") or "").strip()

    def _db(self):
        if self.db is None:
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
            self.db = sqlite3.connect(self.db_path, check_same_thread=False)
            self.db.execute("CREATE TABLE IF NOT EXISTS time_entry (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, "
                            "user_code TEXT NOT NULL, case_id TEXT NOT NULL, minutes INTEGER NOT NULL, activity TEXT NOT NULL, dpia_ref TEXT NOT NULL, consultation_ref TEXT NOT NULL DEFAULT '')")
            if "consultation_ref" not in [r[1] for r in self.db.execute("PRAGMA table_info(time_entry)")]:
                self.db.execute("ALTER TABLE time_entry ADD COLUMN consultation_ref TEXT NOT NULL DEFAULT ''")
            self.db.execute("CREATE INDEX IF NOT EXISTS ix_time_user ON time_entry (user_code, id)")
            self.db.execute("CREATE TABLE IF NOT EXISTS notice_ack (user_code TEXT NOT NULL, version TEXT NOT NULL, at TEXT NOT NULL, "
                            "PRIMARY KEY (user_code, version))")
        return self.db

    def acknowledged(self, user):
        if not os.path.exists(self.db_path) and self.db is None:
            return False
        with self.lock:
            return self._db().execute("SELECT 1 FROM notice_ack WHERE user_code=? AND version=?", (user["code"], NOTICE_VERSION)).fetchone() is not None

    def acknowledge(self, user):
        """Record that this person has read the current notice. Idempotent. Refused while capture is not enabled."""
        self._require()
        with self.lock:
            db = self._db()
            db.execute("INSERT OR IGNORE INTO notice_ack (user_code, version, at) VALUES (?,?,?)",
                       (user["code"], NOTICE_VERSION, datetime.now().isoformat(timespec="minutes")))
            db.commit()
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
        with self.lock:
            db = self._db()
            db.execute("INSERT INTO time_entry (at, user_code, case_id, minutes, activity, dpia_ref, consultation_ref) VALUES (?,?,?,?,?,?,?)",
                       (datetime.now().isoformat(timespec="minutes"), user["code"], str(case_id)[:40], minutes, activity, dpia, consult))
            db.commit()

    def mine(self, user):
        self._require()
        self._require_ack(user)
        with self.lock:
            rows = self._db().execute("SELECT at, case_id, minutes, activity FROM time_entry WHERE user_code=? ORDER BY id DESC LIMIT 200",
                                      (user["code"],)).fetchall()
        return [dict(at=a, case_id=c, minutes=m, activity=t) for a, c, m, t in rows]

    def report(self):
        """Totals by activity, with groups of too few people suppressed. Never lists a person."""
        self._require()
        k = self.min_group()
        with self.lock:
            rows = self._db().execute("SELECT activity, COUNT(*), SUM(minutes), COUNT(DISTINCT user_code) FROM time_entry GROUP BY activity").fetchall()
        out = [dict(activity=a, entries=n, minutes=m) for a, n, m, people in rows if people >= k]
        hidden = sum(1 for _, _, _, people in rows if people < k)
        return dict(by_activity=out, suppressed_activities=hidden, min_group=k,
                    note="Totals for process measurement. Groups with fewer than the minimum number of people are hidden. No individual rows.")
