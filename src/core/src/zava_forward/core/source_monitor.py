"""Offline discovery and simulated human-controlled rule releases, never legal approval."""

from __future__ import annotations

import difflib
import json
from datetime import date, timedelta
from typing import Any

from zava_forward.core import lawstore, rule_engine, rulecards

EXERCISE_OWNER = "Juan Manuel Servera"
LABEL = "EXERCISE ONLY: approvals and regression evidence are simulated, not legal approval."
TABLES = (
    "reg_monitor_config",
    "reg_monitor_observation",
    "reg_monitor_change",
    "reg_monitor_event",
)
SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS reg_monitor_config "
    "(id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, body TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_monitor_observation "
    "(id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, at TEXT NOT NULL, body TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_monitor_change "
    "(id TEXT PRIMARY KEY, source_id TEXT NOT NULL, body TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS reg_monitor_event "
    "(id INTEGER PRIMARY KEY, change_id TEXT NOT NULL, action TEXT NOT NULL, body TEXT NOT NULL)",
)
MSSQL_DDL = (
    "CREATE TABLE reg_monitor_config "
    "(id INT PRIMARY KEY, source_id VARCHAR(100) NOT NULL, body NVARCHAR(MAX) NOT NULL)",
    "CREATE TABLE reg_monitor_observation "
    "(id INT PRIMARY KEY, source_id VARCHAR(100) NOT NULL, at VARCHAR(10) NOT NULL, "
    "body NVARCHAR(MAX) NOT NULL)",
    "CREATE TABLE reg_monitor_change "
    "(id CHAR(64) PRIMARY KEY, source_id VARCHAR(100) NOT NULL, body NVARCHAR(MAX) NOT NULL)",
    "CREATE TABLE reg_monitor_event "
    "(id INT PRIMARY KEY, change_id CHAR(64) NOT NULL, action VARCHAR(30) NOT NULL, "
    "body NVARCHAR(MAX) NOT NULL)",
)
IMPACT_FIELDS = ("requirements", "journeys", "tests", "communications")


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(value: object) -> str:
    return lawstore.sha256(_json(value).encode())  # type: ignore[no-any-return]


def _day(value: str) -> str:
    return rulecards._day(value)  # type: ignore[no-any-return]


def _text(value: object, name: str) -> str:
    return rulecards._text(value, name)  # type: ignore[no-any-return]


def _owner(actor: str, role: str) -> None:
    if role != rulecards.OWNER or rulecards._canon(actor) != rulecards._canon(EXERCISE_OWNER):
        raise rulecards.RuleError(
            "only Juan Manuel Servera with rule_owner may approve this exercise"
        )


def activation_guard(rules: Any, card_id: str) -> None:
    """Existing lifecycle entry points must not bypass a monitored source review."""
    exists = (
        rules.sql.all(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", ("reg_monitor_change",)
        )
        if rules.sql.dialect == "sqlite"
        else rules.sql.all("SELECT name FROM sys.tables WHERE name=?", ("reg_monitor_change",))
    )
    if not exists:
        return
    for row in rules.sql.all("SELECT body FROM reg_monitor_change"):
        change = json.loads(row["body"])
        if card_id in change["affected"]["cards"] or card_id in rules._source_cards(
            change["source_id"]
        ):
            raise rulecards.RuleError(
                "monitored cards require source-monitor regression and owner activation; "
                "direct activation or hold release is blocked"
            )


class SourceMonitor:
    """Trusted in-process exercise service. It exposes no HTTP identity or agent approval path."""

    def __init__(self, law: Any) -> None:
        self.law = law
        self.rules = law.rules
        self.sql = law.sql
        with self.rules.transaction():
            for table, sqlite, mssql in zip(TABLES, SQLITE_DDL, MSSQL_DDL, strict=True):
                if self.sql.dialect == "mssql":
                    suffix = rulecards.LEDGER_SUFFIX if self.sql.ledger else ""
                    self.sql.run(f"IF OBJECT_ID(N'{table}', N'U') IS NULL {mssql}{suffix}")
                    if self.sql.ledger:
                        rows = self.sql.all(
                            "SELECT ledger_type_desc FROM sys.tables WHERE name=?", (table,)
                        )
                        if rows[0]["ledger_type_desc"] != "APPEND_ONLY_LEDGER_TABLE":
                            raise rulecards.RuleError(f"{table} must be append-only ledger")
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

    def _id(self, table: str) -> int:
        return int(self.sql.all(f"SELECT MAX(id) n FROM {table}")[0]["n"] or 0) + 1

    def _event(self, cid: str, action: str, body: dict[str, Any]) -> int:
        eid = self._id("reg_monitor_event")
        self.sql.run(
            "INSERT INTO reg_monitor_event VALUES (?,?,?,?)",
            (eid, cid, action, _json(dict(body, simulated=True, label=LABEL))),
        )
        return eid

    def events(self, cid: str) -> list[dict[str, Any]]:
        return [
            dict(id=r["id"], action=r["action"], **json.loads(r["body"]))
            for r in self.sql.all(
                "SELECT * FROM reg_monitor_event WHERE change_id=? ORDER BY id", (cid,)
            )
        ]

    def changes(self) -> list[dict[str, Any]]:
        with self.sql.lock:
            return [
                dict(id=r["id"], **json.loads(r["body"]), events=self.events(r["id"]))
                for r in self.sql.all("SELECT * FROM reg_monitor_change ORDER BY id")
            ]

    def _change(self, cid: str) -> dict[str, Any]:
        rows = self.sql.all("SELECT body FROM reg_monitor_change WHERE id=?", (cid,))
        if not rows:
            raise rulecards.RuleError("unknown source change")
        return dict(id=cid, **json.loads(rows[0]["body"]))

    def config(self, source_id: str) -> dict[str, Any]:
        rows = self.sql.all(
            "SELECT * FROM reg_monitor_config WHERE source_id=? ORDER BY id DESC", (source_id,)
        )
        if not rows:
            raise rulecards.RuleError("source monitoring is not configured")
        return dict(id=rows[0]["id"], **json.loads(rows[0]["body"]))

    def configure(
        self,
        source_id: str,
        *,
        cadence_days: int,
        likelihood: str,
        rationale: str,
        impact: dict[str, list[str]],
        actor: str,
        role: str,
    ) -> int:
        _owner(actor, role)
        if type(cadence_days) is not int or not 1 <= cadence_days <= 366:
            raise rulecards.RuleError("cadence_days must be an integer from 1 to 366")
        if likelihood not in ("High", "Medium", "Low"):
            raise rulecards.RuleError("likelihood must be High, Medium or Low")
        if set(impact) != set(IMPACT_FIELDS):
            raise rulecards.RuleError(
                "impact needs requirements, journeys, tests and communications"
            )
        for field, values in impact.items():
            if not isinstance(values, list) or any(
                not isinstance(v, str) or not v.strip() for v in values
            ):
                raise rulecards.RuleError(f"impact.{field} must be a list of nonempty identifiers")
        body = dict(
            source_id=source_id,
            cadence_days=cadence_days,
            likelihood=likelihood,
            rationale=_text(rationale, "register rationale"),
            impact=impact,
            owner=EXERCISE_OWNER,
            simulated=True,
            label=LABEL,
        )
        with self.rules.transaction():
            self.law.source(source_id)
            existing = self.sql.all(
                "SELECT body FROM reg_monitor_config WHERE source_id=? ORDER BY id DESC",
                (source_id,),
            )
            if existing and existing[0]["body"] == _json(body):
                return int(self.config(source_id)["id"])
            revision = self._id("reg_monitor_config")
            self.sql.run(
                "INSERT INTO reg_monitor_config VALUES (?,?,?)", (revision, source_id, _json(body))
            )
            return revision

    def due(self, source_id: str, today: str) -> bool:
        today = _day(today)
        with self.sql.lock:
            config = self.config(source_id)
            rows = self.sql.all(
                "SELECT at, body FROM reg_monitor_observation WHERE source_id=? ORDER BY id DESC",
                (source_id,),
            )
            if not rows:
                return True
            current = date.fromisoformat(today)
            if date.fromisoformat(rows[0]["at"]) > current:
                raise rulecards.RuleError("monitor clock precedes the last observation")
            for row in rows:
                if not json.loads(row["body"])["error"]:
                    last = date.fromisoformat(row["at"])
                    return current >= last + timedelta(days=config["cadence_days"])
            return True

    def _heads(self, cards: list[str]) -> dict[str, Any]:
        return {cid: self.rules.history(cid) for cid in cards}

    def observe(
        self,
        source_id: str,
        *,
        today: str,
        content: bytes | None,
        metadata: dict[str, Any],
        provenance: str,
        method: str = "metadata",
        error: str | None = None,
    ) -> str | None:
        """Compare a local observation; caller retrieval success never establishes verification."""
        today = _day(today)
        if not isinstance(metadata, dict):
            raise rulecards.RuleError("publication metadata must be an object")
        if method not in ("metadata", "feed", "legislation", "scraping", "local-fixture"):
            raise rulecards.RuleError("unknown discovery method")
        if set(metadata) - {"published", "effective", "status", "official_url", "complete"}:
            raise rulecards.RuleError("unknown publication metadata")
        for key in ("published", "effective"):
            if metadata.get(key) is not None:
                _day(metadata[key])
        if metadata.get("status") is not None and metadata["status"] not in lawstore.STATUSES:
            raise rulecards.RuleError("unknown source status")
        if "complete" in metadata and type(metadata["complete"]) is not bool:
            raise rulecards.RuleError("complete must be a boolean, not an authority signal")
        provenance = _text(provenance, "provenance")
        if content is None and not error:
            raise rulecards.RuleError("missing content needs an explicit retrieval error")
        if content is not None and error:
            raise rulecards.RuleError("a failed observation cannot include candidate content")
        if content is not None:
            content.decode("utf-8")
        with self.rules.transaction():
            config = self.config(source_id)
            source = self.law.source(source_id)
            baseline = source["versions"][0]
            attempts = self.sql.all(
                "SELECT * FROM reg_monitor_observation WHERE source_id=? ORDER BY id DESC",
                (source_id,),
            )
            if attempts and attempts[0]["at"] > today:
                raise rulecards.RuleError("monitor clock precedes the last observation")
            digest = lawstore.sha256(content) if content is not None else None
            comparison = dict(metadata)
            comparison.setdefault("effective", baseline["effective"])
            comparison.setdefault("status", baseline["status"])
            comparison.setdefault("official_url", source["source"]["official_url"])
            comparison.setdefault(
                "complete",
                baseline["completeness"] == "full" and digest == baseline["content_hash"],
            )
            categories = []
            if error:
                categories.append("retrieval_failure")
            else:
                if digest != baseline["content_hash"]:
                    categories.append("content")
                if any(
                    comparison[k] != v
                    for k, v in dict(
                        effective=baseline["effective"],
                        status=baseline["status"],
                        official_url=source["source"]["official_url"],
                        complete=baseline["completeness"] == "full",
                    ).items()
                ) or comparison.get("published"):
                    categories.append("metadata")
            identity = dict(
                source_id=source_id,
                baseline_version=baseline["version"],
                baseline_hash=baseline["content_hash"],
                content_hash=digest,
                metadata=comparison,
                error=error,
                config_id=config["id"],
                card_ids=self.rules._source_cards(source_id),
            )
            cid = _hash(identity) if categories else None
            body = dict(
                identity,
                candidate_id=cid,
                method=method,
                provenance=provenance,
                verified=False,
                error=error,
                label=LABEL,
            )
            self.sql.run(
                "INSERT INTO reg_monitor_observation VALUES (?,?,?,?)",
                (self._id("reg_monitor_observation"), source_id, today, _json(body)),
            )
            if cid and not self.sql.all("SELECT id FROM reg_monitor_change WHERE id=?", (cid,)):
                blob = f"candidates/{source_id}/{cid}.md" if content is not None else None
                if blob:
                    self.law.blobs.put(blob, content)
                baseline_raw = self.law.blobs.get(baseline["blob_path"])
                if lawstore.sha256(baseline_raw) != baseline["content_hash"]:
                    raise rulecards.RuleError("baseline snapshot is corrupt")
                diff = (
                    list(
                        difflib.unified_diff(
                            baseline_raw.decode("utf-8").splitlines(),
                            content.decode("utf-8").splitlines() if content is not None else [],
                            fromfile=f"{source_id}@v{baseline['version']}",
                            tofile="unverified candidate",
                            lineterm="",
                        )
                    )
                    if content is not None
                    else []
                )
                cards = self.rules._source_cards(source_id)
                affected = dict(
                    config["impact"],
                    cards=self._heads(cards),
                    unmapped=not cards or any(not config["impact"][f] for f in IMPACT_FIELDS),
                )
                change = dict(
                    identity,
                    detected=today,
                    categories=categories,
                    method=method,
                    provenance=provenance,
                    verified=False,
                    candidate_blob=blob,
                    affected=affected,
                    owner=EXERCISE_OWNER,
                    label=LABEL,
                    simulated=True,
                    difference=dict(
                        content_diff=diff[:200],
                        truncated=len(diff) > 200,
                        metadata_before=dict(
                            effective=baseline["effective"],
                            status=baseline["status"],
                            official_url=source["source"]["official_url"],
                            complete=baseline["completeness"] == "full",
                        ),
                        metadata_after=comparison,
                    ),
                )
                self.sql.run(
                    "INSERT INTO reg_monitor_change VALUES (?,?,?)", (cid, source_id, _json(change))
                )
                self.rules._source_changed(
                    source_id,
                    baseline["version"],
                    today,
                    comparison.get("effective"),
                    baseline["version"],
                    context=dict(candidate_id=cid, config_id=config["id"], **config["impact"]),
                )
            return cid

    def _fresh(self, change: dict[str, Any]) -> None:
        source_id = change["source_id"]
        baseline = self.law.source(source_id)["versions"][0]
        if (baseline["version"], baseline["content_hash"]) != (
            change["baseline_version"],
            change["baseline_hash"],
        ):
            raise rulecards.RuleError("source baseline changed; new review required")
        if self.config(source_id)["id"] != change["config_id"]:
            raise rulecards.RuleError("source configuration changed; new review required")
        rows = self.sql.all(
            "SELECT body FROM reg_monitor_observation WHERE source_id=? ORDER BY id DESC",
            (source_id,),
        )
        if not rows or json.loads(rows[0]["body"])["candidate_id"] != change["id"]:
            raise rulecards.RuleError("latest source observation differs; new review required")
        if self.rules._source_cards(source_id) != sorted(change["affected"]["cards"]):
            raise rulecards.RuleError("affected card inventory changed; new review required")
        if (
            change["candidate_blob"] is None
            or lawstore.sha256(self.law.blobs.get(change["candidate_blob"]))
            != change["content_hash"]
        ):
            raise rulecards.RuleError("candidate snapshot missing or corrupt")

    def _eligible(self, card: dict[str, Any], today: str) -> None:
        if (
            not card.get("check")
            or card["effective"] > today
            or (card["retirement"] and card["retirement"] <= today)
        ):
            raise rulecards.RuleError("card is not executable on the release date")
        _, state = rule_engine.citation_eligibility(self.law, card, today)
        if state != "active":
            raise rulecards.RuleError("card citations are not current, reviewed and complete")

    def approve(
        self,
        cid: str,
        *,
        actor: str,
        role: str,
        today: str,
        provenance_review: str,
        completeness_review: str,
        interpretation: str,
        notification: str,
        rollback: str,
        targets: dict[str, int],
        effective: str,
        cases: list[dict[str, Any]],
    ) -> int:
        """Record simulated owner review of the frozen impact, targets and regression plan."""
        _owner(actor, role)
        today, effective = _day(today), _day(effective)
        if effective < today:
            raise rulecards.RuleError("release effective date cannot precede approval")
        evidence = {
            k: _text(v, k)
            for k, v in dict(
                provenance_review=provenance_review,
                completeness_review=completeness_review,
                interpretation=interpretation,
                notification=notification,
                rollback=rollback,
            ).items()
        }
        with self.rules.transaction():
            change = self._change(cid)
            self._fresh(change)
            if change["error"] or not change["metadata"]["complete"]:
                raise rulecards.RuleError("failed or incomplete retrieval cannot be approved")
            if change["metadata"].get("effective") and effective < change["metadata"]["effective"]:
                raise rulecards.RuleError("release cannot precede the candidate effective date")
            if any(e["action"] == "activated" for e in self.events(cid)):
                raise rulecards.RuleError("a previously activated change needs a new review")
            if not targets or set(targets) != set(change["affected"]["cards"]):
                raise rulecards.RuleError("targets must cover every affected card")
            if any(not change["affected"][f] for f in IMPACT_FIELDS):
                raise rulecards.RuleError("complete the bounded impact inventory before approval")
            dispositions = {}
            for card_id, version in targets.items():
                if type(version) is not int:
                    raise rulecards.RuleError("target versions must be integers")
                card = self.rules._owner_only(card_id, version, actor, role)
                state = self.rules.state(card_id, version)
                if state not in ("approved", "active", "held"):
                    raise rulecards.RuleError("each target needs separate card-owner approval")
                dispositions[card_id] = (
                    "new_version_required" if state == "approved" else "no_change"
                )
                if state == "approved":
                    if self.rules.history(card_id)[-1]["version"] != version:
                        raise rulecards.RuleError("the target must be the latest card version")
                    if card["effective"] != effective:
                        raise rulecards.RuleError("target and release effective dates must match")
                card = next(c for c in self.rules.history(card_id) if c["version"] == version)
                if not card["exercise"]:
                    raise rulecards.RuleError("only exercise cards can enter a simulated release")
                self._eligible(card, effective)
            required = set(change["affected"]["tests"])
            found: set[str] = set()
            covered: set[str] = set()
            for case in cases:
                if set(case) != {"test_id", "card_id", "facts", "expected"}:
                    raise rulecards.RuleError(
                        "regression needs test_id, card_id, facts and expected"
                    )
                if case["card_id"] not in targets or not isinstance(case["facts"], dict):
                    raise rulecards.RuleError("regression case must reference an approved target")
                if (
                    not isinstance(case["expected"], list)
                    or not case["expected"]
                    or any(
                        r not in ("clear", "attention", "breach risk", "unknown", "not applicable")
                        for r in case["expected"]
                    )
                ):
                    raise rulecards.RuleError("expected must list deterministic result states")
                test_id = _text(case["test_id"], "test_id")
                if test_id in found:
                    raise rulecards.RuleError("regression test IDs must be unique")
                found.add(test_id)
                covered.add(case["card_id"])
            if not required <= found or covered != set(targets):
                raise rulecards.RuleError("regressions must cover all impacted tests and targets")
            plan = dict(
                candidate_id=cid,
                actor=EXERCISE_OWNER,
                at=today,
                effective=effective,
                targets=targets,
                dispositions=dispositions,
                heads=self._heads(sorted(targets)),
                cases=cases,
                engine_version=rule_engine.ENGINE_VERSION,
                evaluation_clock=effective + "T12:00:00Z",
                config_id=change["config_id"],
                evidence=evidence,
                verified=True,
                observation_head=self.sql.all(
                    "SELECT MAX(id) n FROM reg_monitor_observation WHERE source_id=?",
                    (change["source_id"],),
                )[0]["n"],
            )
            plan["digest"] = _hash(plan)
            for review in self.rules.reviews():
                if (
                    review["affected"]
                    and review["affected"].get("candidate_id") == cid
                    and review["status"] == "open"
                ):
                    self.rules._assess_review(
                        review["id"],
                        actor,
                        role,
                        today,
                        interpretation=interpretation,
                        outcome=dispositions[review["card_id"]],
                        tests=sorted(required),
                        effective=effective,
                        notification=notification,
                        rollback=rollback,
                    )
            return self._event(cid, "approved", plan)

    def _approval(self, cid: str) -> dict[str, Any]:
        approvals = [e for e in self.events(cid) if e["action"] == "approved"]
        if not approvals:
            raise rulecards.RuleError("named owner approval is required before regression")
        approval = approvals[-1]
        change = self._change(cid)
        self._fresh(change)
        observations = self.sql.all(
            "SELECT body FROM reg_monitor_observation WHERE source_id=? AND id>?",
            (change["source_id"], approval["observation_head"]),
        )
        if any(json.loads(row["body"])["candidate_id"] != cid for row in observations):
            raise rulecards.RuleError("intervening source observation invalidated this approval")
        if approval["engine_version"] != rule_engine.ENGINE_VERSION:
            raise rulecards.RuleError("regression evaluator changed; new approval required")
        if approval["heads"] != self._heads(sorted(approval["targets"])):
            raise rulecards.RuleError(
                "card lifecycle changed; new approval and regression required"
            )
        return approval

    def regress(self, cid: str, *, today: str) -> dict[str, Any]:
        today = _day(today)
        with self.rules.transaction():
            approval = self._approval(cid)
            if today < approval["at"]:
                raise rulecards.RuleError("regression cannot precede approval")
            now = rule_engine._time(approval["evaluation_clock"])
            assert now is not None
            results = []
            for case in approval["cases"]:
                card = next(
                    c
                    for c in approval["heads"][case["card_id"]]
                    if c["version"] == approval["targets"][case["card_id"]]
                )
                observed = [
                    r["result"]
                    for r in rule_engine.evaluate(
                        card["check"]["kind"], card["check"], case["facts"], now
                    )
                ]
                results.append(
                    dict(
                        test_id=case["test_id"],
                        observed=observed,
                        expected=case["expected"],
                        passed=observed == case["expected"],
                    )
                )
            result = dict(
                approval_id=approval["id"],
                digest=approval["digest"],
                at=today,
                engine_version=rule_engine.ENGINE_VERSION,
                results=results,
                passed=all(r["passed"] for r in results),
                simulated=True,
                label=LABEL,
            )
            self._event(cid, "regression", result)
            return result

    def activate(self, cid: str, *, actor: str, role: str, today: str) -> None:
        _owner(actor, role)
        today = _day(today)
        with self.rules.transaction():
            approval = self._approval(cid)
            runs = [e for e in self.events(cid) if e["action"] == "regression"]
            if (
                not runs
                or not runs[-1]["passed"]
                or (runs[-1]["approval_id"], runs[-1]["digest"])
                != (approval["id"], approval["digest"])
            ):
                raise rulecards.RuleError("latest regression for this approval must pass")
            if today < approval["effective"] or today < runs[-1]["at"]:
                raise rulecards.RuleError("activation cannot precede effective date or regression")
            prior: dict[str, int | None] = {}
            prior_states: dict[str, str] = {}
            change = self._change(cid)
            for other in self.sql.all(
                "SELECT body FROM reg_monitor_change WHERE source_id<>?", (change["source_id"],)
            ):
                other_source = json.loads(other["body"])["source_id"]
                if set(approval["targets"]) & set(self.rules._source_cards(other_source)):
                    raise rulecards.RuleError(
                        "overlapping changed sources require coordinated owner release; "
                        "not supported by this offline slice"
                    )
            for card_id, version in approval["targets"].items():
                card = next(c for c in self.rules.history(card_id) if c["version"] == version)
                self._eligible(card, today)
                held = [c["version"] for c in self.rules.history(card_id) if c["state"] == "held"]
                if held and (approval["dispositions"][card_id] != "no_change" or held != [version]):
                    raise rulecards.RuleError("owner hold cannot be superseded by a source release")
                prior[card_id] = self.rules.is_active(card_id, today)
                prior_states[card_id] = card["state"]
            for card_id, version in approval["targets"].items():
                if approval["dispositions"][card_id] == "new_version_required":
                    self.rules._activate(card_id, version, actor, role, today)
                elif prior_states[card_id] == "held":
                    self.rules._event(
                        card_id,
                        version,
                        "active",
                        actor,
                        role,
                        today,
                        True,
                        "simulated source no-change review: owner released hold after regression",
                    )
            self._event(
                cid,
                "activated",
                dict(
                    actor=EXERCISE_OWNER,
                    at=today,
                    approval_id=approval["id"],
                    prior=prior,
                    targets=approval["targets"],
                    dispositions=approval["dispositions"],
                    prior_states=prior_states,
                    heads=self._heads(sorted(prior)),
                    regression_id=runs[-1]["id"],
                ),
            )

    def rollback(self, cid: str, *, actor: str, role: str, today: str, reason: str) -> None:
        _owner(actor, role)
        today, reason = _day(today), _text(reason, "rollback reason")
        with self.rules.transaction():
            events = self.events(cid)
            activated = [e for e in events if e["action"] == "activated"]
            if not activated or any(e["action"] == "rolled_back" for e in events):
                raise rulecards.RuleError("no unchanged activation is available for rollback")
            release = activated[-1]
            if today < release["at"] or release["heads"] != self._heads(sorted(release["targets"])):
                raise rulecards.RuleError("intervening lifecycle change prevents rollback")
            for card_id, version in release["prior"].items():
                if version is not None:
                    card = next(c for c in self.rules.history(card_id) if c["version"] == version)
                    self.rules._owner_only(card_id, version, actor, role)
                    self._eligible(card, today)
            for card_id, version in release["targets"].items():
                if release["dispositions"][card_id] == "no_change":
                    if release["prior_states"][card_id] == "held":
                        self.rules._event(
                            card_id,
                            version,
                            "held",
                            actor,
                            role,
                            today,
                            True,
                            f"source rollback restoring owner hold: {reason}"[:400],
                        )
                    continue
                self.rules._event(
                    card_id,
                    version,
                    "retired",
                    actor,
                    role,
                    today,
                    True,
                    f"source rollback: {reason}"[:400],
                )
                if release["prior"][card_id] is not None:
                    self.rules._event(
                        card_id,
                        release["prior"][card_id],
                        "active",
                        actor,
                        role,
                        today,
                        True,
                        f"source rollback: {reason}"[:400],
                    )
            self._event(
                cid,
                "rolled_back",
                dict(actor=EXERCISE_OWNER, at=today, reason=reason, activation_id=release["id"]),
            )
