"""Versioned rule cards with an approval lifecycle (ADR 0005, architecture 3, phase 2; AC-104).

A card version is immutable and append-only; lifecycle changes are append-only events, so
prior versions, approvers and dates are always retained. The lifecycle is draft, approved,
active, held, retired. Only a version approved by the card's named owner (a different person
from its author, holding the separate owner role) can become active. A detected source
change is recorded as a review item and never alters an approved card. The two seed cards are
labelled exercise fixtures: their approvals are simulated and are not law or real approval.
"""
import json
import sqlite3
from datetime import date

AUTHOR, OWNER = "rule_author", "rule_owner"


def _canon(name):
    return " ".join(str(name).split()).casefold()
STATES = ("draft", "approved", "active", "held", "retired")
EXERCISE_LABEL = "EXERCISE CARD: synthetic fixture, not approved by a named owner. Not law and not a real approval (ADR 0005 owner decision, 2026-10-15)."
APPEND_ONLY = ("rule_card_version", "rule_card_event", "rule_card_review")
FIELDS = ("title", "trigger", "applicability", "provisions", "clock", "safe_default", "escalation_role", "approver", "effective", "retirement")

SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS rule_card_version (card_id TEXT NOT NULL, version INTEGER NOT NULL, title TEXT NOT NULL, trigger_text TEXT NOT NULL, applicability TEXT NOT NULL, provisions TEXT NOT NULL, clock TEXT NOT NULL, safe_default TEXT NOT NULL, escalation_role TEXT NOT NULL, approver TEXT NOT NULL, author TEXT NOT NULL, effective TEXT, retirement TEXT, exercise INTEGER NOT NULL, created TEXT NOT NULL, PRIMARY KEY (card_id, version))",
    "CREATE TABLE IF NOT EXISTS rule_card_event (id INTEGER PRIMARY KEY AUTOINCREMENT, card_id TEXT NOT NULL, version INTEGER NOT NULL, state TEXT NOT NULL, actor TEXT NOT NULL, role TEXT NOT NULL, at TEXT NOT NULL, simulated INTEGER NOT NULL, note TEXT)",
    "CREATE TABLE IF NOT EXISTS rule_card_review (id INTEGER PRIMARY KEY AUTOINCREMENT, card_id TEXT NOT NULL, source_id TEXT NOT NULL, source_version INTEGER NOT NULL, detected TEXT NOT NULL, status TEXT NOT NULL, note TEXT)",
)
MSSQL_DDL = (
    "CREATE TABLE rule_card_version (card_id VARCHAR(100) NOT NULL, version INT NOT NULL, title NVARCHAR(200) NOT NULL, trigger_text NVARCHAR(600) NOT NULL, applicability NVARCHAR(600) NOT NULL, provisions NVARCHAR(MAX) NOT NULL, clock NVARCHAR(400) NOT NULL, safe_default NVARCHAR(600) NOT NULL, escalation_role NVARCHAR(200) NOT NULL, approver NVARCHAR(200) NOT NULL, author NVARCHAR(200) NOT NULL, effective VARCHAR(10) NULL, retirement VARCHAR(10) NULL, exercise BIT NOT NULL, created VARCHAR(10) NOT NULL, PRIMARY KEY (card_id, version))",
    "CREATE TABLE rule_card_event (id INT IDENTITY PRIMARY KEY, card_id VARCHAR(100) NOT NULL, version INT NOT NULL, state VARCHAR(20) NOT NULL, actor NVARCHAR(200) NOT NULL, role VARCHAR(40) NOT NULL, at VARCHAR(10) NOT NULL, simulated BIT NOT NULL, note NVARCHAR(400) NULL)",
    "CREATE TABLE rule_card_review (id INT IDENTITY PRIMARY KEY, card_id VARCHAR(100) NOT NULL, source_id VARCHAR(100) NOT NULL, source_version INT NOT NULL, detected VARCHAR(10) NOT NULL, status VARCHAR(20) NOT NULL, note NVARCHAR(400) NULL)",
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
    def __init__(self, db):
        """db is a sqlite3 connection, which may be the law store's own."""
        self.db = db
        db.row_factory = sqlite3.Row
        for ddl in SQLITE_DDL:
            db.execute(ddl)
        for t in APPEND_ONLY:
            for op in ("UPDATE", "DELETE"):
                db.execute(f"CREATE TRIGGER IF NOT EXISTS {t}_no_{op.lower()} BEFORE {op} ON {t} BEGIN SELECT RAISE(ABORT, '{t} is append-only'); END")
        db.commit()

    def _event(self, card_id, version, state, actor, role, at, simulated, note=None):
        self.db.execute("INSERT INTO rule_card_event (card_id, version, state, actor, role, at, simulated, note) VALUES (?,?,?,?,?,?,?,?)",
                        (card_id, version, state, actor, role, at, int(simulated), note))
        self.db.commit()

    def propose(self, card_id, author, role, today=None, exercise=True, **f):
        """Create the next immutable draft version. Needs the author role. Never touches earlier versions.

        Only labelled exercise cards are allowed until a named owner and the #116 role binding exist (ADR 0005).
        """
        if not exercise:
            raise RuleError("only labelled exercise cards are allowed until real approvers and #116 roles exist")
        if role != AUTHOR:
            raise RuleError("only the rule author role can draft a card")
        missing = [k for k in FIELDS if k not in ("retirement",) and not f.get(k)]
        if missing:
            raise RuleError("missing fields: " + ", ".join(missing))
        today = today or date.today().isoformat()
        v = (self.db.execute("SELECT MAX(version) v FROM rule_card_version WHERE card_id=?", (card_id,)).fetchone()[0] or 0) + 1
        self.db.execute("INSERT INTO rule_card_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            card_id, v, f["title"], f["trigger"], f["applicability"], json.dumps(f["provisions"]), f["clock"], f["safe_default"],
            f["escalation_role"], f["approver"], author, f["effective"], f.get("retirement"), int(exercise), today))
        self._event(card_id, v, "draft", author, role, today, exercise)
        return v

    def _version(self, card_id, version):
        r = self.db.execute("SELECT * FROM rule_card_version WHERE card_id=? AND version=?", (card_id, version)).fetchone()
        if not r:
            raise RuleError("unknown card version")
        return r

    def state(self, card_id, version):
        r = self.db.execute("SELECT state FROM rule_card_event WHERE card_id=? AND version=? ORDER BY id DESC LIMIT 1", (card_id, version)).fetchone()
        return r[0] if r else None

    def _owner_only(self, card_id, version, actor, role):
        c = self._version(card_id, version)
        if role != OWNER or _canon(actor) != _canon(c["approver"]):
            raise RuleError("only the named owner role of this card can do this")
        return c

    def approve(self, card_id, version, actor, role, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if _canon(actor) == _canon(c["author"]):
            raise RuleError("an author cannot approve their own card")
        if self.state(card_id, version) != "draft":
            raise RuleError("only a draft can be approved")
        self._event(card_id, version, "approved", actor, role, today or date.today().isoformat(), c["exercise"], "simulated approval, exercise only" if c["exercise"] else None)

    def activate(self, card_id, version, actor, role, today=None):
        """Make an approved version active, retiring nothing silently: any other active version is superseded by a retire event."""
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) != "approved":
            raise RuleError("only an approved version can be activated")
        today = today or date.today().isoformat()
        for (v,) in self.db.execute("SELECT DISTINCT version FROM rule_card_version WHERE card_id=? AND version<>?", (card_id, version)).fetchall():
            if self.state(card_id, v) in ("active", "held"):
                self._event(card_id, v, "retired", actor, role, today, c["exercise"], f"superseded by v{version}")
        self._event(card_id, version, "active", actor, role, today, c["exercise"])

    def hold(self, card_id, version, actor, role, note, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) != "active":
            raise RuleError("only an active card can be held")
        self._event(card_id, version, "held", actor, role, today or date.today().isoformat(), c["exercise"], note)

    def release(self, card_id, version, actor, role, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) != "held":
            raise RuleError("only a held card can be released")
        self._event(card_id, version, "active", actor, role, today or date.today().isoformat(), c["exercise"], "hold released")

    def retire(self, card_id, version, actor, role, today=None):
        c = self._owner_only(card_id, version, actor, role)
        if self.state(card_id, version) not in ("approved", "active", "held"):
            raise RuleError("only an approved, active or held card can be retired")
        self._event(card_id, version, "retired", actor, role, today or date.today().isoformat(), c["exercise"])

    def is_active(self, card_id, on=None):
        """The version that may fire on a date: state active, inside its effective and retirement dates. Else None."""
        on = on or date.today().isoformat()
        for (v,) in self.db.execute("SELECT version FROM rule_card_version WHERE card_id=? ORDER BY version DESC", (card_id,)).fetchall():
            c = self._version(card_id, v)
            if self.state(card_id, v) == "active" and c["effective"] <= on and (not c["retirement"] or on < c["retirement"]):
                return v
        return None

    def history(self, card_id):
        out = []
        for r in self.db.execute("SELECT * FROM rule_card_version WHERE card_id=? ORDER BY version", (card_id,)):
            d = dict(r)
            d["provisions"] = json.loads(d["provisions"])
            d["state"] = self.state(card_id, r["version"])
            d["label"] = EXERCISE_LABEL if r["exercise"] else None
            d["events"] = [dict(e) for e in self.db.execute("SELECT state, actor, role, at, simulated, note FROM rule_card_event WHERE card_id=? AND version=? ORDER BY id", (card_id, r["version"]))]
            approved = [e for e in d["events"] if e["state"] == "approved"]
            d["approved_by"] = approved[0]["actor"] if approved else None
            d["approved_on"] = approved[0]["at"] if approved else None
            out.append(d)
        return out

    def source_changed(self, source_id, source_version, today=None):
        """Record a review item for each card citing the source. Approved cards are never modified."""
        today = today or date.today().isoformat()
        hit = []
        for (cid,) in self.db.execute("SELECT DISTINCT card_id FROM rule_card_version WHERE provisions LIKE ?", (f"%{source_id}%",)).fetchall():
            self.db.execute("INSERT INTO rule_card_review (card_id, source_id, source_version, detected, status, note) VALUES (?,?,?,?,?,?)",
                            (cid, source_id, source_version, today, "open", "Source changed. Owner to review and, if needed, draft a new card version."))
            hit.append(cid)
        self.db.commit()
        return hit

    def reviews(self, card_id=None):
        q, a = "SELECT * FROM rule_card_review", ()
        if card_id:
            q, a = q + " WHERE card_id=?", (card_id,)
        return [dict(r) for r in self.db.execute(q + " ORDER BY id", a)]

    def seed(self, today="2026-10-15"):
        """Load the two exercise cards as drafts. Idempotent. They stay draft until a named owner approves."""
        added = []
        for card in SEED_CARDS:
            if not self.db.execute("SELECT 1 FROM rule_card_version WHERE card_id=?", (card["card_id"],)).fetchone():
                c = dict(card)
                cid = c.pop("card_id")
                self.propose(cid, "Exercise author (synthetic)", AUTHOR, today=today, exercise=True, **c)
                added.append(cid)
        return added
