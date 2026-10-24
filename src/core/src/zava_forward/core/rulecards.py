"""Versioned rule cards with an approval lifecycle (ADR 0005, architecture 3, phase 2; AC-104).

A card version is immutable and append-only; lifecycle changes are append-only events, so
prior versions, approvers and dates are always retained. The lifecycle is draft, approved,
active, held, retired. Only a version approved by the card's named owner (a different person
from its author, holding the separate owner role) can become active. A detected source
change is recorded as a review item and never alters an approved card. The two seed cards are
labelled exercise fixtures: their approvals are simulated and are not law or real approval.
"""
import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import date
from functools import wraps

from zava_forward.core import lawstore

AUTHOR, OWNER = "rule_author", "rule_owner"


def _canon(name):
    return " ".join(str(name).split()).casefold()


def _locked(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        with self.sql.lock:
            return method(self, *args, **kwargs)
    return call


def _mutation(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        with self.transaction():
            return method(self, *args, **kwargs)
    return call


def _day(value):
    if not isinstance(value, str):
        raise RuleError("dates must be ISO YYYY-MM-DD strings")
    try:
        if date.fromisoformat(value).isoformat() == value:
            return value
    except ValueError:
        pass
    raise RuleError("dates must be ISO YYYY-MM-DD strings")


def _text(value, name, limit=None):
    if not isinstance(value, str) or not value.strip():
        raise RuleError(f"{name} must be nonempty text")
    if limit is not None and len(value.strip()) > limit:
        raise RuleError(f"{name} must be at most {limit} characters")
    return value.strip()
STATES = ("draft", "approved", "active", "held", "retired")
EXERCISE_LABEL = "EXERCISE CARD: synthetic fixture. Any recorded approval is simulated only, not legal or operational approval (ADR 0005 owner decision, 2026-10-15)."
APPEND_ONLY = ("rule_card_version", "rule_card_event", "rule_card_review", "rule_card_review_event", "rule_card_check")
REVIEW_STATES = ("open", "assessed")
TRACE = {
    "hazard-awareness-clock": dict(requirements=["CON-001", "FR-003", "RULE-003"], tests=["src/core/tests/test_rulecards.py", "src/api/tests/test_lawstore.py"]),
    "automated-decision-safeguard": dict(requirements=["FR-034", "RULE-021"], tests=["src/core/tests/test_rulecards.py", "src/agents/tests/test_ai_eval.py"]),
}
FIELDS = ("title", "trigger", "applicability", "provisions", "clock", "safe_default", "escalation_role", "approver", "effective", "retirement", "check")

SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS rule_card_version (card_id TEXT NOT NULL, version INTEGER NOT NULL, title TEXT NOT NULL, trigger_text TEXT NOT NULL, applicability TEXT NOT NULL, provisions TEXT NOT NULL, clock TEXT NOT NULL, safe_default TEXT NOT NULL, escalation_role TEXT NOT NULL, approver TEXT NOT NULL, author TEXT NOT NULL, effective TEXT, retirement TEXT, exercise INTEGER NOT NULL, created TEXT NOT NULL, PRIMARY KEY (card_id, version))",
    "CREATE TABLE IF NOT EXISTS rule_card_event (id INTEGER PRIMARY KEY, card_id TEXT NOT NULL, version INTEGER NOT NULL, state TEXT NOT NULL, actor TEXT NOT NULL, role TEXT NOT NULL, at TEXT NOT NULL, simulated INTEGER NOT NULL, note TEXT)",
    "CREATE TABLE IF NOT EXISTS rule_card_review (id INTEGER PRIMARY KEY, card_id TEXT NOT NULL, source_id TEXT NOT NULL, source_version INTEGER NOT NULL, detected TEXT NOT NULL, status TEXT NOT NULL, note TEXT, affected TEXT, prior_version INTEGER, source_effective TEXT)",
    "CREATE TABLE IF NOT EXISTS rule_card_review_event (id INTEGER PRIMARY KEY, review_id INTEGER NOT NULL, state TEXT NOT NULL, actor TEXT NOT NULL, role TEXT NOT NULL, at TEXT NOT NULL, record TEXT)",
    "CREATE TABLE IF NOT EXISTS rule_card_check (card_id TEXT NOT NULL, version INTEGER NOT NULL, specification TEXT NOT NULL, PRIMARY KEY (card_id, version))",
)
MSSQL_DDL = (
    "CREATE TABLE rule_card_version (card_id VARCHAR(100) NOT NULL, version INT NOT NULL, title NVARCHAR(200) NOT NULL, trigger_text NVARCHAR(600) NOT NULL, applicability NVARCHAR(600) NOT NULL, provisions NVARCHAR(MAX) NOT NULL, clock NVARCHAR(400) NOT NULL, safe_default NVARCHAR(600) NOT NULL, escalation_role NVARCHAR(200) NOT NULL, approver NVARCHAR(200) NOT NULL, author NVARCHAR(200) NOT NULL, effective VARCHAR(10) NULL, retirement VARCHAR(10) NULL, exercise BIT NOT NULL, created VARCHAR(10) NOT NULL, PRIMARY KEY (card_id, version))",
    "CREATE TABLE rule_card_event (id INT PRIMARY KEY, card_id VARCHAR(100) NOT NULL, version INT NOT NULL, state VARCHAR(20) NOT NULL, actor NVARCHAR(200) NOT NULL, role VARCHAR(40) NOT NULL, at VARCHAR(10) NOT NULL, simulated BIT NOT NULL, note NVARCHAR(400) NULL)",
    "CREATE TABLE rule_card_review (id INT PRIMARY KEY, card_id VARCHAR(100) NOT NULL, source_id VARCHAR(100) NOT NULL, source_version INT NOT NULL, detected VARCHAR(10) NOT NULL, status VARCHAR(20) NOT NULL, note NVARCHAR(400) NULL, affected NVARCHAR(MAX) NULL, prior_version INT NULL, source_effective VARCHAR(10) NULL)",
    "CREATE TABLE rule_card_review_event (id INT PRIMARY KEY, review_id INT NOT NULL, state VARCHAR(20) NOT NULL, actor NVARCHAR(200) NOT NULL, role VARCHAR(40) NOT NULL, at VARCHAR(10) NOT NULL, record NVARCHAR(MAX) NULL)",
    "CREATE TABLE rule_card_check (card_id VARCHAR(100) NOT NULL, version INT NOT NULL, specification NVARCHAR(MAX) NOT NULL, PRIMARY KEY (card_id, version))",
)
LEDGER_SUFFIX = " WITH (LEDGER = ON (APPEND_ONLY = ON))"

SEED_CARDS = (
    dict(
        card_id="hazard-awareness-clock",
        title="Hazard awareness clock",
        trigger="Case record contains a damp, mould or emergency hazard report",
        applicability="Zava North Homes tenanted homes and communal areas (synthetic stock)",
        provisions=["awaabs-law-regulations-2025 (illustrative citation, to be confirmed by the owner)"],
        clock="Per the approved card, starting from the recorded awareness time; no duration is set by this exercise card",
        safe_default="Use the human emergency or hazard route now; open an investigation task",
        escalation_role="Repairs and hazard owner, then Building Safety lead",
        approver="Named compliance owner (unassigned)",
        effective="2025-10-27",
    ),
    dict(
        card_id="automated-decision-safeguard",
        title="Automated decision safeguard",
        trigger="An agent output would decide or materially shape an outcome for a resident",
        applicability="Any workflow where software proposes a decision about a resident",
        provisions=["uk-gdpr-current-text, Article 22 (illustrative citation, to be confirmed by the owner)"],
        clock="No clock; applies at the point of decision",
        safe_default="Route to a named human reviewer; the agent only proposes and the resident can seek review",
        escalation_role="Data Protection Officer, then Compliance lead",
        approver="Named DPO (unassigned)",
        effective="2026-10-15",
    ),
)


class RuleError(Exception):
    pass


class RuleCardStore:
    canonical = None  # optional resolver mapping a recorded alias to one canonical person key
    distinct = None  # optional (actor, author) -> bool; when set, only a demonstrably distinct actor may approve

    def _who(self, name):
        return self.canonical(name) if self.canonical else _canon(name)

    def __init__(self, db):
        """Accept an existing law SQL adapter or a legacy local SQLite connection."""
        self.sql = lawstore.SqliteDb(connection=db) if isinstance(db, sqlite3.Connection) else db
        self.db = self.sql.db
        with self.transaction():
            if self.sql.dialect == "mssql":
                for t, ddl in zip(APPEND_ONLY, MSSQL_DDL):
                    suffix = LEDGER_SUFFIX if self.sql.ledger else ""
                    self.sql.run(f"IF OBJECT_ID(N'{t}', N'U') IS NULL {ddl}{suffix}")
                    if self.sql.ledger:
                        kind = self.sql.all("SELECT ledger_type_desc FROM sys.tables WHERE name=?", (t,))[0]["ledger_type_desc"]
                        if kind != "APPEND_ONLY_LEDGER_TABLE":
                            raise RuleError(f"{t} must be an append-only ledger table")
                    else:
                        self.sql.run(f"IF OBJECT_ID(N'{t}_append_only', N'TR') IS NULL EXEC(N'CREATE TRIGGER {t}_append_only ON {t} INSTEAD OF UPDATE, DELETE AS THROW 50001, ''{t} is append-only'', 1')")
            else:
                for ddl in SQLITE_DDL:
                    self.sql.run(ddl)
                for t in APPEND_ONLY:
                    for op in ("UPDATE", "DELETE"):
                        self.sql.run(f"CREATE TRIGGER IF NOT EXISTS {t}_no_{op.lower()} BEFORE {op} ON {t} BEGIN SELECT RAISE(ABORT, '{t} is append-only'); END")

    @contextmanager
    def transaction(self):
        with self.sql.lock:
            self.sql.begin()
            try:
                yield
                self.sql.commit()
            except self.sql.integrity_error as exc:
                self.sql.rollback()
                raise RuleError("conflicting rule-card write; reload and retry") from exc
            except BaseException:
                self.sql.rollback()
                raise

    def _next_id(self, table):
        return (self.sql.all(f"SELECT MAX(id) v FROM {table}")[0]["v"] or 0) + 1

    def _event(self, card_id, version, state, actor, role, at, simulated, note=None):
        if note is not None:
            note = _text(note, "note", 400)
        self.sql.run("INSERT INTO rule_card_event (id, card_id, version, state, actor, role, at, simulated, note) VALUES (?,?,?,?,?,?,?,?,?)",
                     (self._next_id("rule_card_event"), card_id, version, state, _text(actor, "actor", 200), role, _day(at), int(simulated), note))

    @_mutation
    def propose(self, card_id, author, role, today=None, exercise=True, **f):
        return self._propose(card_id, author, role, today, exercise, **f)

    def _propose(self, card_id, author, role, today=None, exercise=True, **f):
        """Create the next immutable draft version. Needs the author role. Never touches earlier versions.

        Only labelled exercise cards are allowed; identity binding is not operational approval.
        """
        if not exercise:
            raise RuleError("only labelled exercise cards are allowed; operational approval remains open")
        if role != AUTHOR:
            raise RuleError("only the rule author role can draft a card")
        card_id, author = _text(card_id, "card_id"), _text(author, "author", 200)
        if len(card_id) > 100 or "/" in card_id or card_id == "reviews":
            raise RuleError("card_id must be at most 100 characters, contain no slash and not be reviews")
        if set(f) - set(FIELDS):
            raise RuleError("unknown card fields")
        missing = [k for k in FIELDS if k not in ("retirement", "check") and not f.get(k)]
        if missing:
            raise RuleError("missing fields: " + ", ".join(missing))
        limits = dict(title=200, trigger=600, applicability=600, clock=400, safe_default=600, escalation_role=200, approver=200)
        for k in FIELDS:
            if k not in ("provisions", "effective", "retirement", "check"):
                f[k] = _text(f[k], k, limits[k])
        if f.get("check") is not None:
            from zava_forward.core.rule_engine import validate_spec
            try:
                f["check"] = validate_spec(f["check"])
            except ValueError as exc:
                raise RuleError(str(exc)) from exc
        if not isinstance(f["provisions"], list) or not f["provisions"]:
            raise RuleError("provisions must be a nonempty list of citations")
        f["provisions"] = [_text(p, "provision") for p in f["provisions"]]
        f["effective"] = _day(f["effective"])
        if f.get("retirement") is not None:
            f["retirement"] = _day(f["retirement"])
            if f["retirement"] <= f["effective"]:
                raise RuleError("retirement must be after effective date")
        today = _day(today or date.today().isoformat())
        v = (self.sql.all("SELECT MAX(version) v FROM rule_card_version WHERE card_id=?", (card_id,))[0]["v"] or 0) + 1
        self.sql.run("INSERT INTO rule_card_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            card_id, v, f["title"], f["trigger"], f["applicability"], json.dumps(f["provisions"]), f["clock"], f["safe_default"],
            f["escalation_role"], f["approver"], author, f["effective"], f.get("retirement"), int(exercise), today))
        if f.get("check") is not None:
            self.sql.run("INSERT INTO rule_card_check (card_id, version, specification) VALUES (?,?,?)",
                         (card_id, v, json.dumps(f["check"], sort_keys=True)))
        self._event(card_id, v, "draft", author, role, today, exercise)
        return v

    def _version(self, card_id, version):
        rows = self.sql.all("SELECT * FROM rule_card_version WHERE card_id=? AND version=?", (card_id, version))
        r = rows[0] if rows else None
        if not r:
            raise RuleError("unknown card version")
        return r

    @_locked
    def state(self, card_id, version):
        rows = self.sql.all("SELECT state FROM rule_card_event WHERE card_id=? AND version=? ORDER BY id DESC", (card_id, version))
        return rows[0]["state"] if rows else None

    def _owner_only(self, card_id, version, actor, role):
        c = self._version(card_id, version)
        if role != OWNER or self._who(actor) != self._who(c["approver"]):
            raise RuleError("only the named owner role of this card can do this")
        return c

    @_mutation
    def approve(self, card_id, version, actor, role, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.distinct is not None and not self.distinct(actor, c["author"]):
            raise RuleError("an author cannot approve their own card, or the author identity cannot be resolved")
        if self._who(actor) == self._who(c["author"]):
            raise RuleError("an author cannot approve their own card")
        if self.state(card_id, version) != "draft":
            raise RuleError("only a draft can be approved")
        self._event(card_id, version, "approved", actor, role, today or date.today().isoformat(), c["exercise"], "simulated approval, exercise only" if c["exercise"] else None)

    @_mutation
    def activate(self, card_id, version, actor, role, today=None):
        """Make an approved version active, retiring nothing silently: any other active version is superseded by a retire event."""
        from zava_forward.core.source_monitor import activation_guard
        activation_guard(self, card_id)
        self._activate(card_id, version, actor, role, today)

    def _activate(self, card_id, version, actor, role, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) != "approved":
            raise RuleError("only an approved version can be activated")
        today = _day(today or date.today().isoformat())
        if today < c["effective"] or (c["retirement"] and today >= c["retirement"]):
            raise RuleError("activation must be within the card's effective dates")
        for row in self.sql.all("SELECT version FROM rule_card_version WHERE card_id=? AND version<>?", (card_id, version)):
            v = row["version"]
            if self.state(card_id, v) in ("active", "held"):
                self._event(card_id, v, "retired", actor, role, today, c["exercise"], f"superseded by v{version}")
        self._event(card_id, version, "active", actor, role, today, c["exercise"])

    @_mutation
    def hold(self, card_id, version, actor, role, note, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) != "active":
            raise RuleError("only an active card can be held")
        self._event(card_id, version, "held", actor, role, today or date.today().isoformat(), c["exercise"], _text(note, "hold reason"))

    @_mutation
    def release(self, card_id, version, actor, role, today=None):
        from zava_forward.core.source_monitor import activation_guard
        activation_guard(self, card_id)
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) != "held":
            raise RuleError("only a held card can be released")
        self._event(card_id, version, "active", actor, role, today or date.today().isoformat(), c["exercise"], "hold released")

    @_mutation
    def retire(self, card_id, version, actor, role, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) not in ("approved", "active", "held"):
            raise RuleError("only an approved, active or held card can be retired")
        self._event(card_id, version, "retired", actor, role, today or date.today().isoformat(), c["exercise"])

    @_locked
    def is_active(self, card_id, on=None):
        """The version that may fire on a date: state active, inside its effective and retirement dates. Else None."""
        on = _day(on or date.today().isoformat())
        for row in self.sql.all("SELECT version FROM rule_card_version WHERE card_id=? ORDER BY version DESC", (card_id,)):
            v = row["version"]
            c = self._version(card_id, v)
            if self.state(card_id, v) == "active" and c["effective"] <= on and (not c["retirement"] or on < c["retirement"]):
                return v
        return None

    @_locked
    def history(self, card_id):
        out = []
        for r in self.sql.all("SELECT * FROM rule_card_version WHERE card_id=? ORDER BY version", (card_id,)):
            d = dict(r)
            d["provisions"] = json.loads(d["provisions"])
            specs = self.sql.all("SELECT specification FROM rule_card_check WHERE card_id=? AND version=?", (card_id, r["version"]))
            d["check"] = json.loads(specs[0]["specification"]) if specs else None
            d["state"] = self.state(card_id, r["version"])
            d["label"] = EXERCISE_LABEL if r["exercise"] else None
            d["events"] = self.sql.all("SELECT state, actor, role, at, simulated, note FROM rule_card_event WHERE card_id=? AND version=? ORDER BY id", (card_id, r["version"]))
            approved = [e for e in d["events"] if e["state"] == "approved"]
            d["approved_by"] = approved[0]["actor"] if approved else None
            d["approved_on"] = approved[0]["at"] if approved else None
            out.append(d)
        return out

    @_locked
    def cards(self):
        return [self.history(r["card_id"])[-1] for r in self.sql.all("SELECT DISTINCT card_id FROM rule_card_version ORDER BY card_id")]

    @_mutation
    def source_changed(self, source_id, source_version, today=None, source_effective=None, prior_version=None):
        return self._source_changed(source_id, source_version, today, source_effective, prior_version)

    def _source_cards(self, source_id):
        found = set()
        for row in self.sql.all("SELECT card_id, provisions FROM rule_card_version"):
            for citation in json.loads(row["provisions"]):
                if re.split(r"[@,\s(]", citation, maxsplit=1)[0] == source_id:
                    found.add(row["card_id"])
        return sorted(found)

    def _source_changed(self, source_id, source_version, today=None, source_effective=None, prior_version=None, context=None):
        """Record a review item for each card citing the source. Approved cards are never modified.

        Each item names the affected rule card, its active version, the requirements and tests the card traces to,
        and the source versions and effective date, so a human owner can assess it. It stays open until the
        card's named owner records an assessment; it never activates, changes or retires anything.
        """
        today = today or date.today().isoformat()
        prior_version = source_version - 1 if prior_version is None and source_version > 1 else prior_version
        hit = []
        for cid in self._source_cards(source_id):
            t = TRACE.get(cid, {})
            affected = dict(rules=[cid], active_version=self.is_active(cid, today), requirements=t.get("requirements", []), tests=t.get("tests", []),
                            journeys=[], communications=[], unmapped=not t)
            if context:
                affected.update(context)
            self.sql.run("INSERT INTO rule_card_review (id, card_id, source_id, source_version, detected, status, note, affected, prior_version, source_effective) VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (self._next_id("rule_card_review"), cid, source_id, source_version, today, "open", "Source changed. Owner to review and, if needed, draft a new card version.",
                             json.dumps(affected), prior_version, source_effective))
            hit.append(cid)
        return hit

    @_mutation
    def assess_review(self, review_id, actor, role, today=None, *, interpretation, outcome, tests, effective, notification, rollback, hold=None):
        return self._assess_review(review_id, actor, role, today, interpretation=interpretation, outcome=outcome,
                                   tests=tests, effective=effective, notification=notification, rollback=rollback, hold=hold)

    def _assess_review(self, review_id, actor, role, today=None, *, interpretation, outcome, tests, effective, notification, rollback, hold=None):
        """Record the named owner's assessment of a review item (RULE-021, AC-068). Only the owner of the card can do this.

        outcome is no_change or new_version_required. A new version still needs propose, approve and activate.
        If hold is given, the card's active version is held at once; the assessment itself never activates a rule.
        """
        rows = self.sql.all("SELECT * FROM rule_card_review WHERE id=?", (review_id,))
        r = rows[0] if rows else None
        if not r:
            raise RuleError("unknown review item")
        latest = self.sql.all("SELECT MAX(version) v FROM rule_card_version WHERE card_id=?", (r["card_id"],))[0]["v"]
        c = self._owner_only(r["card_id"], latest, actor, role)
        if self._review_state(review_id) != "open":
            raise RuleError("review item is already assessed")
        if outcome not in ("no_change", "new_version_required"):
            raise RuleError("outcome must be no_change or new_version_required")
        rec = dict(interpretation=interpretation, outcome=outcome, tests=tests, effective=effective, notification=notification, rollback=rollback, hold=hold)
        rec.update(simulated=bool(c["exercise"]), label=EXERCISE_LABEL if c["exercise"] else None)
        missing = [k for k in ("interpretation", "tests", "effective", "notification", "rollback") if not rec[k]]
        if missing:
            raise RuleError("missing assessment fields: " + ", ".join(missing))
        today = today or date.today().isoformat()
        if hold:
            for row in self.sql.all("SELECT version FROM rule_card_version WHERE card_id=?", (r["card_id"],)):
                v = row["version"]
                if self.state(r["card_id"], v) == "active":
                    self._owner_only(r["card_id"], v, actor, role)
                    self._event(r["card_id"], v, "held", actor, role, today, c["exercise"], f"review {review_id}: {hold}")
        self.sql.run("INSERT INTO rule_card_review_event (id, review_id, state, actor, role, at, record) VALUES (?,?,?,?,?,?,?)",
                        (self._next_id("rule_card_review_event"), review_id, "assessed", actor, role, today, json.dumps(rec)))

    def _review_state(self, review_id):
        rows = self.sql.all("SELECT state FROM rule_card_review_event WHERE review_id=? ORDER BY id DESC", (review_id,))
        return rows[0]["state"] if rows else "open"

    @_locked
    def reviews(self, card_id=None):
        q, a = "SELECT * FROM rule_card_review", ()
        if card_id:
            q, a = q + " WHERE card_id=?", (card_id,)
        out = []
        for r in self.sql.all(q + " ORDER BY id", a):
            d = dict(r)
            d["affected"] = json.loads(d["affected"]) if d["affected"] else None
            d["status"] = self._review_state(d["id"])
            events = self.sql.all("SELECT actor, role, at, record FROM rule_card_review_event WHERE review_id=? ORDER BY id DESC", (d["id"],))
            ev = events[0] if events else None
            d["assessment"] = dict(actor=ev["actor"], at=ev["at"], **json.loads(ev["record"])) if ev else None
            out.append(d)
        return out

    @_mutation
    def seed(self, today="2026-10-15"):
        """Load the two exercise cards as drafts. Idempotent. They stay draft until a named owner approves."""
        added = []
        for card in SEED_CARDS:
            if not self.sql.all("SELECT 1 x FROM rule_card_version WHERE card_id=?", (card["card_id"],)):
                c = dict(card)
                cid = c.pop("card_id")
                self._propose(cid, "Exercise author (synthetic)", AUTHOR, today=today, exercise=True, **c)
                added.append(cid)
        return added
