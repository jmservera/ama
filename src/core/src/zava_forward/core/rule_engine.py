"""Bounded, SQL-backed exercise checks. No model, messaging or hold mutation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any

from zava_forward.core.regulatory_usage import offline_usage

KINDS = ("hazard-awareness-clock", "automated-decision-safeguard")
AUDIENCES = {
    KINDS[0]: ("Building Safety Liaison", "Resident Liaison Officer", "Retrofit Programme Manager"),
    KINDS[1]: ("Retrofit Coordinator", "Retrofit Programme Manager"),
}
SAFE_ROUTE = "Use the existing human emergency or hazard service now; do not wait for checks."
TABLES = ("reg_check", "reg_alert", "reg_alert_event", "reg_checkpoint")
ENGINE_VERSION = 2
SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS reg_check (id TEXT PRIMARY KEY, case_id TEXT NOT NULL, "
    "at TEXT NOT NULL, check_seq INTEGER NOT NULL, body TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_alert (id TEXT PRIMARY KEY, episode TEXT NOT NULL, "
    "throttle TEXT NOT NULL, "
    "case_id TEXT NOT NULL, created TEXT NOT NULL, body TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_alert_event (id TEXT PRIMARY KEY, alert_id TEXT NOT NULL, "
    "action TEXT NOT NULL, actor TEXT NOT NULL, at TEXT NOT NULL, note TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_checkpoint (id TEXT PRIMARY KEY, body TEXT NOT NULL)",
)
MSSQL_DDL = (
    "CREATE TABLE reg_check (id CHAR(64) PRIMARY KEY, case_id VARCHAR(100) NOT NULL, "
    "at VARCHAR(32) NOT NULL, check_seq BIGINT NOT NULL, body NVARCHAR(MAX) NOT NULL)",
    "CREATE TABLE reg_alert (id CHAR(64) PRIMARY KEY, episode CHAR(64) NOT NULL, "
    "throttle CHAR(64) NOT NULL, "
    "case_id VARCHAR(100) NOT NULL, created VARCHAR(32) NOT NULL, body NVARCHAR(MAX) NOT NULL)",
    "CREATE TABLE reg_alert_event (id CHAR(64) PRIMARY KEY, alert_id CHAR(64) NOT NULL, "
    "action VARCHAR(30) NOT NULL, actor NVARCHAR(200) NOT NULL, at VARCHAR(32) NOT NULL, "
    "note NVARCHAR(600) NOT NULL)",
    "CREATE TABLE reg_checkpoint (id CHAR(64) PRIMARY KEY, body NVARCHAR(MAX) NOT NULL)",
)


def validate_spec(value: object) -> dict[str, object]:
    """Accept only the versioned, bounded code contract, never expressions or fact paths."""
    if not isinstance(value, dict) or value.get("kind") not in KINDS:
        raise ValueError("check.kind must name a supported deterministic check")
    if set(value) - {"kind", "hours", "attention_hours"}:
        raise ValueError("unsupported check fields; clocks and evidence paths are code-owned")
    if value["kind"] == KINDS[1] and set(value) != {"kind"}:
        raise ValueError("the decision safeguard has no clock")
    hours = value.get("hours")
    attention = value.get("attention_hours", 0)
    if hours is not None and (type(hours) is not int or not 1 <= hours <= 8760):
        raise ValueError("check.hours must be an approved integer from 1 to 8760")
    if type(attention) is not int or not 0 <= attention <= (hours or 0):
        raise ValueError("attention_hours must be between zero and check.hours")
    return dict(value)


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(value: object) -> str:
    return hashlib.sha256(_json(value).encode()).hexdigest()


def _home_key(facts: dict[str, Any], case_id: str) -> tuple[str, str]:
    """Return a home grouping key; an address key is derived, not a registered home identifier."""
    if facts.get("home_id"):
        return str(facts["home_id"]), "recorded_home"
    home = facts.get("home")
    if isinstance(home, dict):
        postcode = re.sub(r"[^a-z0-9]+", "", str(home.get("postcode") or "").lower())
        address = re.sub(r"[^a-z0-9]+", " ", str(home.get("address") or "").lower()).strip()
        parts = [postcode, address]
        if all(parts):
            return "home-" + _hash(parts)[:16], "address_key"
    return case_id, "case_only"


def _time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(UTC) if parsed.tzinfo else None


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def evaluate(
    kind: str, spec: dict[str, Any], facts: dict[str, Any], now: datetime
) -> list[dict[str, Any]]:
    """Evaluate explicit evidence only; timestamps are observations, never model proposals."""
    key = "hazards" if kind == KINDS[0] else "automated_decisions"
    items = facts.get(key)
    if not isinstance(items, list):
        return [dict(item=key, result="unknown", noticed=f"Missing {key} evidence", harm=0)]
    if not items:
        return [dict(item=key, result="not applicable", noticed=f"No recorded {key}", harm=0)]
    out = []
    for index, item in enumerate(items):
        r: dict[str, Any] = dict(
            item=f"{key}/{index}", result="unknown", noticed="Incomplete evidence", harm=0
        )
        out.append(r)
        if not isinstance(item, dict):
            continue
        if kind == KINDS[1]:
            significant = item.get("significant")
            if significant is False:
                r.update(result="not applicable", noticed="Explicitly non-significant decision")
            elif significant is True:
                r["harm"] = 1
                at = _time(item.get("decided_at"))
                if (
                    _text(item.get("decision_owner"))
                    and item.get("state") == "recorded"
                    and _text(item.get("source"))
                    and _text(item.get("evidence"))
                    and _text(item.get("reasons"))
                    and at is not None
                    and at <= now
                ):
                    r.update(result="clear", noticed="Named human decision evidence recorded")
                elif (
                    item.get("state") == "pending"
                    and _text(item.get("decision_owner"))
                    and _text(item.get("source"))
                    and not item.get("decided_at")
                    and not item.get("evidence")
                ):
                    r.update(result="attention", noticed="Named human decision evidence needed")
            continue
        priority = item.get("priority")
        r["harm"] = 2 if priority == "Emergency" else 1
        aware = _time(item.get("aware_at"))
        if (
            aware is None
            or aware > now
            or not _text(item.get("source"))
            or priority not in ("Emergency", "Significant", "Routine")
            or type(item.get("released")) is not bool
        ):
            continue
        hold = item.get("hold")
        if not isinstance(hold, dict):
            continue
        if item["released"]:
            decision = hold.get("decision")
            actor = decision.get("actor") if isinstance(decision, dict) else None
            released = _time(item.get("released_at"))
            accepted = _time(item.get("accepted_at"))
            decided = _time(decision.get("at")) if isinstance(decision, dict) else None
            if (
                hold.get("status") == "Released"
                and isinstance(decision, dict)
                and _text(decision.get("evidence"))
                and isinstance(actor, dict)
                and _text(actor.get("email"))
                and _text(item.get("raised_by_email"))
                and _text(item.get("repaired_by_email"))
                and actor["email"]
                not in (item.get("raised_by_email"), item.get("repaired_by_email"))
                and accepted is not None
                and decided is not None
                and _text(item.get("repair_evidence"))
                and released is not None
                and aware <= accepted <= released <= now
                and aware <= decided <= now
            ):
                r.update(result="clear", noticed="Independent human hold release recorded")
            continue
        if hold.get("status") != "Active" or hold.get("decision") is not None:
            continue
        hours = spec.get("hours")
        if hours is None:
            r["noticed"] = "No approved executable duration; use the human safety route"
            continue
        due = aware + timedelta(hours=hours)
        r["due_at"] = due.isoformat()
        if now >= due:
            r.update(result="breach risk", noticed="Approved elapsed-hour check is due")
        elif now >= due - timedelta(hours=spec.get("attention_hours", 0)):
            r.update(result="attention", noticed="Approved elapsed-hour check is approaching")
        else:
            r.update(result="clear", noticed="Not yet due under this bounded check")
    return out


def citation_eligibility(
    law: Any, card: dict[str, Any], day: str
) -> tuple[list[dict[str, Any]], str]:
    """Shared runtime/release eligibility; discovery candidates are not provisions."""
    citations = []
    state = "active"
    for pid in card["provisions"]:
        try:
            p = law.provision(pid)
        except KeyError:
            citations.append(dict(id=pid, status="missing"))
            state = "unknown"
            continue
        latest = law.source(p["source_id"])["versions"][0]
        citations.append(
            {
                k: p[k]
                for k in (
                    "id",
                    "source_id",
                    "version",
                    "status",
                    "effective",
                    "retrieved",
                    "review_status",
                    "completeness",
                    "hash",
                )
            }
        )
        if p["status"] in ("consultation", "historical") or p["effective"] and p["effective"] > day:
            if state != "unknown":
                state = "not applicable"
        elif (
            p["status"] not in ("in_force", "guidance")
            or p["version"] != latest["version"]
            or p["completeness"] != "full"
            or p["review_status"] != "reviewed"
            or p["retrieved"] > day
        ):
            state = "unknown"
    return citations, state


class RuleEngine:
    """Adapt legacy SQL/card interfaces; all output is exercise evidence, not legal approval."""

    def __init__(self, law: Any) -> None:
        self.law = law
        self.sql = law.sql
        with law.rules.transaction():
            for table, sqlite, mssql in zip(TABLES, SQLITE_DDL, MSSQL_DDL, strict=True):
                if self.sql.dialect == "mssql":
                    suffix = " WITH (LEDGER = ON (APPEND_ONLY = ON))" if self.sql.ledger else ""
                    self.sql.run(f"IF OBJECT_ID(N'{table}', N'U') IS NULL {mssql}{suffix}")
                    if self.sql.ledger:
                        rows = self.sql.all(
                            "SELECT ledger_type_desc FROM sys.tables WHERE name=?", (table,)
                        )
                        if rows[0]["ledger_type_desc"] != "APPEND_ONLY_LEDGER_TABLE":
                            raise ValueError(f"{table} must be append-only ledger")
                    else:
                        self.sql.run(
                            f"IF OBJECT_ID(N'{table}_append_only', N'TR') IS NULL "
                            f"EXEC(N'CREATE TRIGGER {table}_append_only ON {table} "
                            "INSTEAD OF UPDATE, DELETE AS THROW 50001, "
                            f"''{table} is append-only'', 1')"
                        )
                else:
                    self.sql.run(sqlite)
                    for op in ("UPDATE", "DELETE"):
                        self.sql.run(
                            f"CREATE TRIGGER IF NOT EXISTS {table}_no_{op.lower()} "
                            f"BEFORE {op} ON {table} BEGIN "
                            f"SELECT RAISE(ABORT, '{table} is append-only'); END"
                        )

    def _citations(self, card: dict[str, Any], day: str) -> tuple[list[dict[str, Any]], str]:
        return citation_eligibility(self.law, card, day)

    def run(
        self,
        store: Any,
        case_id: str,
        trigger: str = "data_change",
        *,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Read a SQL snapshot and atomically checkpoint checks and alert publications.

        ``now`` is a code/test clock injection, never an HTTP or model input.
        Scheduled minutes revisit homes, recovering failed post-commit dispatch.
        """
        if trigger not in ("data_change", "step_transition", "schedule"):
            raise ValueError("unsupported engine trigger")
        now = now or datetime.now(UTC)
        if now.tzinfo is None:
            raise ValueError("engine clock must be timezone-aware")
        now = now.astimezone(UTC)
        if not hasattr(store, "db"):
            raise ValueError("deterministic checks require a SQL case store")
        with store.lock:
            row = store.db.execute(
                "SELECT rowversion, body FROM cases WHERE id=?", (case_id,)
            ).fetchone()
            if row is None:
                raise KeyError(case_id)
            revision, body = row
            facts = json.loads(body)
            with self.law.rules.transaction():
                cards = self.law.rules.cards()
                for i, card in enumerate(cards):
                    active = self.law.rules.is_active(card["card_id"], now.date().isoformat())
                    if active is not None:
                        cards[i] = next(
                            c
                            for c in self.law.rules.history(card["card_id"])
                            if c["version"] == active
                        )
                contract = [(c, *self._citations(c, now.date().isoformat())) for c in cards]
                key = _hash(
                    [
                        ENGINE_VERSION,
                        case_id,
                        revision,
                        trigger,
                        contract,
                        now.isoformat(timespec="minutes") if trigger == "schedule" else None,
                    ]
                )
                prior = self.sql.all("SELECT body FROM reg_checkpoint WHERE id=?", (key,))
                if prior:
                    checkpoint: dict[str, Any] = json.loads(prior[0]["body"])
                    return checkpoint
                sequence = (self.sql.all("SELECT MAX(check_seq) n FROM reg_check")[0]["n"] or 0) + 1
                checks = []
                home_id, home_scope = _home_key(facts, case_id)
                for card, citations, source_state in contract:
                    spec = card["check"]
                    eligible = (
                        card["state"] == "active"
                        and card["approved_by"] is not None
                        and card["approved_on"] <= now.date().isoformat()
                        and card["events"][-1]["at"] <= now.date().isoformat()
                        and card["effective"] <= now.date().isoformat()
                        and (not card["retirement"] or now.date().isoformat() < card["retirement"])
                    )
                    result = source_state
                    if not eligible or spec is None:
                        result = "unknown"
                    rows: list[dict[str, Any]] = (
                        evaluate(spec["kind"], spec, facts, now)
                        if eligible and spec is not None and result == "active"
                        else [
                            dict(
                                item="card",
                                result=result,
                                harm=0,
                                noticed="Card or source is not executable as an active control",
                            )
                        ]
                    )
                    for r in rows:
                        check = dict(
                            **r,
                            id=_hash([key, card["card_id"], r["item"]]),
                            case_id=case_id,
                            home_id=home_id,
                            home_scope=home_scope,
                            step=facts["stage"],
                            card_id=card["card_id"],
                            card_version=card["version"],
                            card_status=card["state"],
                            citations=citations,
                            at=now.isoformat(),
                            trigger=trigger,
                            inputs_hash=_hash([revision, body]),
                            evidence_ids=[f"case/{case_id}@{revision}/{r['item']}"],
                            revision=revision,
                            sequence=sequence,
                            safe_action=card["safe_default"],
                            decision_owner=card["approver"],
                            escalation_role=card["escalation_role"],
                            clock=card["clock"],
                            exercise=bool(card["exercise"]),
                            label=card["label"],
                            audience=list(
                                AUDIENCES.get(spec["kind"] if spec else card["card_id"], ())
                            ),
                            usage=offline_usage(
                                "regulatory-check",
                                str(ENGINE_VERSION),
                                r["result"],
                                now.isoformat(),
                            ),
                        )
                        self.sql.run(
                            "INSERT INTO reg_check (id, case_id, at, check_seq, body) "
                            "VALUES (?,?,?,?,?)",
                            (check["id"], case_id, now.isoformat(), sequence, _json(check)),
                        )
                        checks.append(check)
                        if (
                            eligible
                            and spec is not None
                            and source_state == "active"
                            and check["result"] in ("attention", "breach risk", "unknown")
                        ):
                            self._publish(check, now)
                checkpoint = dict(
                    id=key, case_id=case_id, revision=revision, at=now.isoformat(), checks=checks
                )
                self.sql.run(
                    "INSERT INTO reg_checkpoint (id, body) VALUES (?,?)", (key, _json(checkpoint))
                )
                return checkpoint

    def _events(self, alert_id: str) -> list[dict[str, Any]]:
        return list(
            self.sql.all(
                "SELECT action, actor, at, note FROM reg_alert_event "
                "WHERE alert_id=? ORDER BY at, id",
                (alert_id,),
            )
        )

    def _publish(self, check: dict[str, Any], now: datetime) -> None:
        throttle = _hash([check["home_id"], check["card_id"], check["step"], check["item"]])
        if check["result"] == "attention":
            for row in self.sql.all(
                "SELECT created, body FROM reg_alert WHERE throttle=?", (throttle,)
            ):
                if json.loads(row["body"])["result"] == "attention" and now < (
                    datetime.fromisoformat(row["created"]) + timedelta(hours=24)
                ):
                    return
        episode = _hash(
            [
                check["case_id"],
                check["card_id"],
                check["card_version"],
                check["step"],
                check["item"],
                check.get("due_at"),
            ]
        )
        rows = self.sql.all(
            "SELECT id, created, body FROM reg_alert WHERE episode=? ORDER BY created DESC, id",
            (episode,),
        )
        if rows:
            latest = json.loads(rows[0]["body"])
            events = self._events(latest["id"])
            if latest["result"] == check["result"]:
                if check["result"] == "attention":
                    if now < datetime.fromisoformat(rows[0]["created"]) + timedelta(hours=24):
                        return
                elif not any(e["action"] == "outcome" for e in events):
                    return
        alert = dict(check, episode=episode)
        self.sql.run(
            "INSERT INTO reg_alert (id, episode, throttle, case_id, created, body) "
            "VALUES (?,?,?,?,?,?)",
            (alert["id"], episode, throttle, check["case_id"], now.isoformat(), _json(alert)),
        )

    def alerts(self, user: dict[str, Any], case_id: str | None = None) -> dict[str, Any]:
        """Return authorized home groups, with unresolved risks retained and fatigue counts."""
        from zava_forward.core.projection import NOTE_HELD, STAFF_ROLES, can_see_reason

        if user.get("role") not in STAFF_ROLES:
            raise PermissionError("Only scoped staff can read alerts")
        with self.sql.lock:
            query = "SELECT body FROM reg_alert"
            rows = self.sql.all(
                query + " WHERE case_id=?" if case_id else query, (case_id,) if case_id else ()
            )
            visible = []
            current: dict[tuple[str, str, str], dict[str, Any]] = {}
            snapshots: dict[tuple[str, str], list[dict[str, Any]]] = {}
            checks_query = "SELECT body FROM reg_check"
            for row in self.sql.all(
                checks_query + " WHERE case_id=?" if case_id else checks_query,
                (case_id,) if case_id else (),
            ):
                check = json.loads(row["body"])
                identity = (check["case_id"], check["card_id"])
                prior_checks = snapshots.get(identity, [])
                if not prior_checks or check["sequence"] > prior_checks[0]["sequence"]:
                    snapshots[identity] = [check]
                elif check["sequence"] == prior_checks[0]["sequence"]:
                    prior_checks.append(check)
            for snapshot in snapshots.values():
                for check in snapshot:
                    current[(check["case_id"], check["card_id"], check["item"])] = check
            for row in rows:
                a = json.loads(row["body"])
                if user["role"] not in a["audience"] and user["email"] != a["decision_owner"]:
                    continue
                a["events"] = self._events(a["id"])
                active = self.law.rules.is_active(a["card_id"])
                _, source_state = self._citations(
                    {"provisions": [c["id"] for c in a["citations"]]},
                    datetime.now(UTC).date().isoformat(),
                )
                a["active_control"] = active == a["card_version"] and source_state == "active"
                check = current.get((a["case_id"], a["card_id"], a["item"]))
                a["latest_result"] = check["result"] if check else "unknown"
                a["latest_evaluated_at"] = check["at"] if check else None
                if not can_see_reason(user):
                    for event in a["events"]:
                        event["note"] = NOTE_HELD
                a["requires_acknowledgement"] = a["result"] == "breach risk" and not any(
                    e["action"] == "acknowledge" for e in a["events"]
                )
                a["requires_outcome"] = a["result"] == "breach risk" and not any(
                    e["action"] == "outcome" for e in a["events"]
                )
                visible.append(a)
            classified = [
                a
                for a in visible
                if any(e["action"] in ("false_positive", "confirmed") for e in a["events"])
            ]
            false = sum(
                any(e["action"] == "false_positive" for e in a["events"]) for a in classified
            )
            groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
            selected: dict[str, dict[str, Any]] = {}
            for a in sorted(visible, key=lambda a: (a["at"], a["id"]), reverse=True):
                if any(e["action"] == "outcome" for e in a["events"]):
                    continue
                if a["result"] == "breach risk":
                    groups[a["home_id"]].append(a)
                elif (
                    a["active_control"]
                    and a["latest_result"] == a["result"]
                    and a["episode"] not in selected
                ):
                    selected[a["episode"]] = a
                    groups[a["home_id"]].append(a)
            for alerts in groups.values():
                alerts.sort(
                    key=lambda a: (a.get("due_at", "9999"), -a["harm"], a["case_id"], a["id"])
                )
            permitted_checks = [
                c
                for c in current.values()
                if user["role"] in c["audience"] or user["email"] == c["decision_owner"]
            ]
            return dict(
                coverage_status="unknown"
                if not permitted_checks or any(c["result"] == "unknown" for c in permitted_checks)
                else "evaluated",
                homes=[
                    dict(home_id=h, alerts=a)
                    for h, a in sorted(
                        groups.items(),
                        key=lambda pair: (
                            pair[1][0].get("due_at", "9999"),
                            -pair[1][0]["harm"],
                            pair[0],
                        ),
                    )
                ],
                precision=dict(
                    total=len(visible),
                    classified=len(classified),
                    false_positives=false,
                    unclassified=len(visible) - len(classified),
                    false_positive_rate=false / len(classified) if classified else None,
                ),
            )

    def disposition(
        self,
        user: dict[str, Any],
        alert_id: str,
        action: str,
        note: str,
        *,
        now: datetime | None = None,
    ) -> None:
        """Append a named-owner acknowledgement, outcome or classification; never suppress."""
        from zava_forward.core.projection import STAFF_ROLES

        if user.get("role") not in STAFF_ROLES or "rule_owner" not in user.get("rule_roles", []):
            raise PermissionError("A trusted named owner capability is required")
        if action not in ("acknowledge", "outcome", "false_positive", "confirmed"):
            raise ValueError("unsupported alert disposition")
        if not _text(note) or len(note) > 600:
            raise ValueError("disposition needs evidence/outcome text of at most 600 characters")
        with self.law.rules.transaction():
            rows = self.sql.all("SELECT body FROM reg_alert WHERE id=?", (alert_id,))
            if not rows:
                raise PermissionError("Alert is not in your decision scope")
            a = json.loads(rows[0]["body"])
            if user["email"].strip().lower() != a["decision_owner"].strip().lower():
                raise PermissionError("Only this alert's named decision owner may act")
            events = self._events(alert_id)
            if (
                action == "outcome"
                and a["result"] == "breach risk"
                and not any(e["action"] == "acknowledge" for e in events)
            ):
                raise ValueError("Breach risk needs owner acknowledgement before an outcome")
            prior = [e for e in events if e["action"] == action]
            if prior:
                if prior[0]["note"] == note:
                    return
                raise ValueError("Disposition already recorded; history cannot be overwritten")
            if action in ("false_positive", "confirmed") and any(
                e["action"] in ("false_positive", "confirmed") for e in events
            ):
                raise ValueError("An alert classification is already recorded")
            self.sql.run(
                "INSERT INTO reg_alert_event (id, alert_id, action, actor, at, note) "
                "VALUES (?,?,?,?,?,?)",
                (
                    _hash([alert_id, action]),
                    alert_id,
                    action,
                    user["email"],
                    (now or datetime.now(UTC)).isoformat(),
                    note,
                ),
            )


def main() -> None:
    """Run a bounded scheduled page; repeat pages and minutes to recover missed checks."""
    from zava_forward.core import lawstore
    from zava_forward.core.factory import open_store

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--after", default="")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    store = open_store()
    law = lawstore.LawStore.from_env()
    if law is None:
        if hasattr(store, "db"):
            store.db.close()
        raise SystemExit("The law store is not configured; checks are unknown. " + SAFE_ROUTE)
    try:
        engine = RuleEngine(law)
        if not hasattr(store, "db"):
            raise ValueError("scheduled checks require a SQL case store")
        with store.lock:
            tail, params = store._limit(args.limit, 0)
            rows = store.db.execute(
                "SELECT id FROM cases WHERE id>? ORDER BY id" + tail,
                [args.after, *params],
            ).fetchall()
        now = datetime.now(UTC)
        for (cid,) in rows:
            engine.run(store, cid, "schedule", now=now)
        print(_json(dict(processed=len(rows), next_after=rows[-1][0] if rows else None)))
    finally:
        law.close()
        if hasattr(store, "db"):
            store.db.close()


if __name__ == "__main__":
    main()
