from __future__ import annotations

import csv
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .domain import (
    ACTOR_LABELS,
    CLOSURE_REASONS,
    DEFAULT_THRESHOLD,
    EVENT_OUTCOMES,
    escalation_status,
    normalize_scenario_stage,
    validate_threshold,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, database_path: Path, source_dir: Path):
        self.database_path = database_path
        self.source_dir = source_dir
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def connection(self):
        connection = self.connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connection() as db:
            db.execute("PRAGMA journal_mode = WAL")
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    candidate_id TEXT PRIMARY KEY,
                    property_ref TEXT NOT NULL,
                    current_status TEXT NOT NULL,
                    scenario_stage TEXT NOT NULL,
                    owner TEXT NOT NULL DEFAULT '',
                    locality TEXT NOT NULL DEFAULT '',
                    archetype_id TEXT NOT NULL DEFAULT '',
                    lead_supplier TEXT NOT NULL DEFAULT '',
                    rag_status TEXT NOT NULL DEFAULT '',
                    safety_hold_active INTEGER NOT NULL DEFAULT 0,
                    is_synthetic INTEGER NOT NULL CHECK (is_synthetic = 1),
                    source_file TEXT NOT NULL,
                    source_row INTEGER NOT NULL,
                    imported_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS appointment_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT NOT NULL REFERENCES cases(candidate_id),
                    outcome TEXT NOT NULL,
                    appointment_confirmed INTEGER NOT NULL,
                    actor_label TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    source_file TEXT NOT NULL DEFAULT 'Local synthetic scenario'
                );
                CREATE TABLE IF NOT EXISTS gate_controls (
                    candidate_id TEXT NOT NULL REFERENCES cases(candidate_id),
                    gate_key TEXT NOT NULL,
                    enabled INTEGER NOT NULL CHECK (enabled IN (0, 1)),
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (candidate_id, gate_key)
                );
                CREATE TABLE IF NOT EXISTS audit_log (
                    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT,
                    event_type TEXT NOT NULL,
                    actor_label TEXT NOT NULL,
                    details_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS imports (
                    import_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_file TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    accepted_count INTEGER NOT NULL,
                    rejected_count INTEGER NOT NULL,
                    actor_label TEXT NOT NULL,
                    imported_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS agent_runs (
                    run_id TEXT PRIMARY KEY,
                    candidate_id TEXT NOT NULL REFERENCES cases(candidate_id),
                    record_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            db.execute(
                "INSERT OR IGNORE INTO settings(key, value, version, updated_at) VALUES(?, ?, 1, ?)",
                ("threshold", str(DEFAULT_THRESHOLD), utc_now()),
            )
            if db.execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 0:
                self._seed_synthetic_cases(db)

    def _seed_synthetic_cases(self, db: sqlite3.Connection) -> None:
        lifecycle_path = self.source_dir / "candidate-lifecycle.csv"
        holds_path = self.source_dir / "safety-holds.csv"
        if not lifecycle_path.is_file():
            raise FileNotFoundError(
                f"Required synthetic source data was not found: {lifecycle_path}"
            )
        if not holds_path.is_file():
            raise FileNotFoundError(
                f"Required synthetic safety-hold data was not found: {holds_path}"
            )

        open_holds: set[str] = set()
        with holds_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required_hold_columns = {
                "candidate_id",
                "is_synthetic",
                "hold_status_in_tracker",
            }
            if not required_hold_columns.issubset(reader.fieldnames or []):
                raise ValueError(
                    "Synthetic safety-hold source is missing required columns: "
                    + ", ".join(sorted(required_hold_columns - set(reader.fieldnames or [])))
                )
            for row in reader:
                if (
                    row.get("is_synthetic", "").casefold() == "true"
                    and row.get("hold_status_in_tracker", "").casefold() == "open"
                    and row.get("candidate_id")
                ):
                    open_holds.add(row["candidate_id"])

        seeded = 0
        with lifecycle_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required_case_columns = {
                "candidate_id",
                "property_ref",
                "current_status",
                "is_synthetic",
            }
            if not required_case_columns.issubset(reader.fieldnames or []):
                raise ValueError(
                    "Synthetic candidate source is missing required columns: "
                    + ", ".join(sorted(required_case_columns - set(reader.fieldnames or [])))
                )
            for row_number, row in enumerate(reader, start=2):
                candidate_id = row.get("candidate_id", "").strip()
                if (
                    row.get("is_synthetic", "").casefold() != "true"
                    or not candidate_id.startswith("CAND-")
                    or not row.get("property_ref", "").strip().startswith(("SYN-PROP-", "HA-", "HB/"))
                ):
                    continue
                source_row = row_number
                if row.get("source_row"):
                    try:
                        source_row = int(row["source_row"])
                    except ValueError as exc:
                        raise ValueError("Synthetic candidate source_row must be a positive row number.") from exc
                    if source_row < 2:
                        raise ValueError("Synthetic candidate source_row must be a positive row number.")
                db.execute(
                    """
                    INSERT OR IGNORE INTO cases(
                        candidate_id, property_ref, current_status, scenario_stage, owner,
                        locality, archetype_id, lead_supplier, rag_status, safety_hold_active,
                        is_synthetic, source_file, source_row, imported_at
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
                    """,
                    (
                        candidate_id,
                        row["property_ref"].strip(),
                        row.get("current_status", "").strip() or "Unknown",
                        normalize_scenario_stage(row.get("current_status", "").strip())
                        or row.get("current_status", "").strip()
                        or "Unknown",
                        row.get("owner", "").strip(),
                        row.get("locality", "").strip(),
                        row.get("archetype_id", "").strip(),
                        row.get("lead_supplier", "").strip(),
                        row.get("rag_status", "").strip(),
                        int(candidate_id in open_holds),
                        "docs/reference/research/retrofit-synthetic-data/candidate-lifecycle.csv",
                        source_row,
                        utc_now(),
                    ),
                )
                seeded += db.execute("SELECT changes()").fetchone()[0]
        if not seeded:
            raise ValueError("No rows marked is_synthetic=true were found in the source dataset.")
        db.execute(
            """
            INSERT INTO audit_log(candidate_id, event_type, actor_label, details_json, created_at)
            VALUES(NULL, 'synthetic_dataset_loaded', 'System', ?, ?)
            """,
            (
                json.dumps(
                    {
                        "row_count": seeded,
                        "source_file": "candidate-lifecycle.csv",
                        "is_synthetic": True,
                        "real_address_overlay_used": False,
                    }
                ),
                utc_now(),
            ),
        )

    def threshold(self, db: sqlite3.Connection | None = None) -> tuple[int, int]:
        own = db is None
        db = db or self.connect()
        try:
            row = db.execute(
                "SELECT value, version FROM settings WHERE key = 'threshold'"
            ).fetchone()
            if row is None:
                return DEFAULT_THRESHOLD, 1
            return validate_threshold(row["value"]), int(row["version"])
        finally:
            if own:
                db.close()

    def get_case(self, candidate_id: str) -> dict[str, Any] | None:
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM cases WHERE candidate_id = ?", (candidate_id,)
            ).fetchone()
            if row is None:
                return None
            case = dict(row)
            case["is_synthetic"] = bool(case["is_synthetic"])
            case["safety_hold_active"] = bool(case["safety_hold_active"])
            events = [
                dict(event)
                for event in db.execute(
                    "SELECT * FROM appointment_events WHERE candidate_id = ? ORDER BY event_id",
                    (candidate_id,),
                )
            ]
            case["appointment_events"] = events
            threshold, version = self.threshold(db)
            active = self._is_case_active(db, candidate_id)
            status = escalation_status(events, threshold, active=active)
            case["eligible_count"] = status.eligible_count
            case["threshold"] = threshold
            case["threshold_version"] = version
            case["review_required"] = self._investigation_pending(
                db, candidate_id, status.required, status.eligible_count, version
            )
            case["escalation_active"] = status.required
            case["escalation_message"] = status.message
            case["controls"] = {
                row["gate_key"]: bool(row["enabled"])
                for row in db.execute(
                    "SELECT gate_key, enabled FROM gate_controls WHERE candidate_id = ?",
                    (candidate_id,),
                )
            }
            case["active"] = active
            if not active:
                case["eligible_count"] = 0
                case["review_required"] = False
            case["audit"] = [
                {
                    **dict(audit),
                    "details": json.loads(audit["details_json"]),
                }
                for audit in db.execute(
                    "SELECT * FROM audit_log WHERE candidate_id = ? ORDER BY audit_id DESC LIMIT 30",
                    (candidate_id,),
                )
            ]
            case["agent_runs"] = self.agent_runs(candidate_id, db)
            return case

    def agent_runs(self, candidate_id: str, db: sqlite3.Connection) -> list[dict[str, Any]]:
        return [
            json.loads(row["record_json"])
            for row in db.execute(
                "SELECT record_json FROM agent_runs WHERE candidate_id = ? ORDER BY created_at DESC, rowid DESC LIMIT 20",
                (candidate_id,),
            )
        ]

    def save_agent_run(self, run: dict[str, Any], actor: str) -> dict[str, Any]:
        actor = clean_actor(actor)
        run = {**run, "created_at": utc_now(), "requested_by": actor}
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute(
                "SELECT record_json FROM agent_runs WHERE run_id = ?", (run["run_id"],),
            ).fetchone()
            if existing:
                previous = json.loads(existing["record_json"])
                if (previous["state"] != "running" or run["state"] not in {"awaiting_review", "failed"}
                        or previous["candidate_id"] != run["candidate_id"]):
                    raise ValueError("Only an active run can be completed once.")
                run.update(created_at=previous["created_at"], requested_by=previous["requested_by"])
                db.execute("UPDATE agent_runs SET record_json = ? WHERE run_id = ?", (json.dumps(run), run["run_id"]))
            else:
                db.execute(
                    "INSERT INTO agent_runs(run_id, candidate_id, record_json, created_at) VALUES(?, ?, ?, ?)",
                    (run["run_id"], run["candidate_id"], json.dumps(run), run["created_at"]),
                )
            event = "agent_run_started" if run["state"] == "running" else "agent_proposal_recorded"
            self._audit(db, run["candidate_id"], event, actor, {
                "run_id": run["run_id"], "state": run["state"], "model": run["model"],
                "prompt_version": run["prompt_version"], "no_domain_state_changed": True,
            })
        return run

    def review_agent_run(self, candidate_id: str, run_id: str, decision: str, actor: str) -> dict[str, Any]:
        from .agents import safe_snapshot, snapshot_digest
        actor = clean_actor(actor)
        if decision not in {"accepted", "rejected"}:
            raise ValueError("Choose accepted or rejected for the proposal review.")
        with self.connection() as db:
            # Prevent another writer from changing the source while this review is reconciled.
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT record_json FROM agent_runs WHERE run_id = ? AND candidate_id = ?",
                (run_id, candidate_id),
            ).fetchone()
            if row is None:
                raise KeyError("Agent run was not found for this case.")
            run = json.loads(row["record_json"])
            if run["state"] != "awaiting_review":
                raise ValueError("Only an unreviewed validated proposal can be reviewed.")
            case = self.get_case(candidate_id)
            if case is None:
                raise KeyError("Synthetic case was not found.")
            if decision == "accepted" and snapshot_digest(safe_snapshot(case)) != run["snapshot_digest"]:
                raise ValueError("Proposal is stale. Run the agent again against current case evidence.")
            run.update(state=decision, reviewed_by=actor, reviewed_at=utc_now())
            db.execute("UPDATE agent_runs SET record_json = ? WHERE run_id = ?", (json.dumps(run), run_id))
            self._audit(db, candidate_id, "agent_proposal_reviewed", actor, {
                "run_id": run_id, "decision": decision, "no_domain_state_changed": True,
            })
        return run

    @staticmethod
    def _is_case_active(db: sqlite3.Connection, candidate_id: str) -> bool:
        case = db.execute(
            "SELECT current_status FROM cases WHERE candidate_id = ?",
            (candidate_id,),
        ).fetchone()
        if case is None:
            return False
        last = db.execute(
            "SELECT outcome FROM appointment_events WHERE candidate_id = ? ORDER BY event_id DESC LIMIT 1",
            (candidate_id,),
        ).fetchone()
        if last is not None:
            return last["outcome"] != "case_closed"
        source_status = case["current_status"].casefold().strip()
        return not (
            "closed" in source_status
            or source_status in {"withdrawn", "excluded"}
        )

    def _investigation_pending(
        self,
        db: sqlite3.Connection,
        candidate_id: str,
        escalation_active: bool,
        eligible_count: int,
        threshold_version: int,
    ) -> bool:
        if not escalation_active:
            return False
        last_close = db.execute(
            "SELECT COALESCE(MAX(audit_id), 0) FROM audit_log WHERE candidate_id = ? AND event_type = 'case_closed'",
            (candidate_id,),
        ).fetchone()[0]
        trigger = db.execute(
            """SELECT audit_id FROM audit_log
               WHERE candidate_id = ? AND event_type = 'human_review_required' AND audit_id > ?
               ORDER BY audit_id DESC LIMIT 1""",
            (candidate_id, last_close),
        ).fetchone()
        if trigger is None:
            return True
        review = db.execute(
            """SELECT audit_id, details_json FROM audit_log
               WHERE candidate_id = ? AND event_type = 'human_investigation_recorded'
                 AND audit_id > ?
               ORDER BY audit_id DESC LIMIT 1""",
            (candidate_id, trigger["audit_id"]),
        ).fetchone()
        if review is None:
            return True
        details = json.loads(review["details_json"])
        return (
            int(details.get("eligible_count", -1)) < eligible_count
            or int(details.get("threshold_version", -1)) != threshold_version
        )

    def list_cases(self, query: str = "", status: str = "", limit: int = 1000) -> list[dict[str, Any]]:
        predicates = ["is_synthetic = 1"]
        args: list[Any] = []
        if query:
            predicates.append(
                "(candidate_id LIKE ? OR property_ref LIKE ? OR owner LIKE ? OR locality LIKE ?)"
            )
            args.extend([f"%{query}%"] * 4)
        with self.connection() as db:
            sql = f"SELECT * FROM cases WHERE {' AND '.join(predicates)} ORDER BY candidate_id LIMIT ?"
            args.append(1000)
            rows = db.execute(sql, args).fetchall()
            threshold, version = self.threshold(db)
            pending_proposals = {
                row["candidate_id"]: row["count"]
                for row in db.execute(
                    """SELECT candidate_id, COUNT(*) AS count FROM agent_runs
                       WHERE json_extract(record_json, '$.state') = 'awaiting_review'
                       GROUP BY candidate_id"""
                )
            }
            selected: list[dict[str, Any]] = []
            for row in rows:
                case = dict(row)
                active = self._is_case_active(db, case["candidate_id"])
                events = [
                    dict(event)
                    for event in db.execute(
                        "SELECT outcome, appointment_confirmed FROM appointment_events WHERE candidate_id = ? ORDER BY event_id",
                        (case["candidate_id"],),
                    )
                ]
                escalation = escalation_status(events, threshold, active)
                review_required = self._investigation_pending(
                    db, case["candidate_id"], escalation.required, escalation.eligible_count, version,
                )
                if status == "active" and not active:
                    continue
                if status == "held" and not case["safety_hold_active"]:
                    continue
                if status == "escalated" and not review_required:
                    continue
                case.update(
                    {
                        "active": active,
                        "eligible_count": escalation.eligible_count,
                        "review_required": review_required,
                        "pending_agent_reviews": pending_proposals.get(case["candidate_id"], 0),
                    }
                )
                selected.append(case)
            return selected[: max(1, min(limit, 1000))]

    def overview(self) -> dict[str, Any]:
        with self.connection() as db:
            rows = db.execute(
                "SELECT candidate_id, safety_hold_active FROM cases WHERE is_synthetic = 1"
            ).fetchall()
            threshold, version = self.threshold(db)
            active_count = held_count = escalated = 0
            for row in rows:
                active = self._is_case_active(db, row["candidate_id"])
                active_count += int(active)
                held_count += int(row["safety_hold_active"])
                events = [
                    dict(event)
                    for event in db.execute(
                        "SELECT outcome, appointment_confirmed FROM appointment_events WHERE candidate_id = ? ORDER BY event_id",
                        (row["candidate_id"],),
                    )
                ]
                if escalation_status(events, threshold, active).required:
                    escalated += 1
            return {
                "total_cases": len(rows),
                "active_cases": active_count,
                "active_safety_holds": held_count,
                "escalated_cases": escalated,
                "threshold": threshold,
                "threshold_version": version,
                "source_label": "Synthetic evidence pack v2.0.0",
                "all_synthetic": True,
            }

    def update_threshold(self, value: Any, actor: str) -> dict[str, Any]:
        threshold = validate_threshold(value)
        actor = clean_actor(actor)
        with self.connection() as db:
            current, version = self.threshold(db)
            next_version = version + 1
            db.execute(
                "UPDATE settings SET value = ?, version = ?, updated_at = ? WHERE key = 'threshold'",
                (str(threshold), next_version, utc_now()),
            )
            self._audit(
                db,
                None,
                "threshold_configuration_changed",
                actor,
                {"previous": current, "current": threshold, "version": next_version, "synthetic_only": True},
            )
            for row in db.execute(
                "SELECT candidate_id FROM cases WHERE is_synthetic = 1"
            ).fetchall():
                candidate_id = row["candidate_id"]
                if not self._is_case_active(db, candidate_id):
                    continue
                events = [
                    dict(event)
                    for event in db.execute(
                        """SELECT outcome, appointment_confirmed FROM appointment_events
                           WHERE candidate_id = ? ORDER BY event_id""",
                        (candidate_id,),
                    )
                ]
                status = escalation_status(events, threshold)
                if status.required and self._investigation_pending(
                    db, candidate_id, True, status.eligible_count, next_version
                ):
                    self._audit(
                        db,
                        candidate_id,
                        "human_review_required",
                        "Workflow",
                        {
                            "eligible_count": status.eligible_count,
                            "threshold": threshold,
                            "threshold_version": next_version,
                            "reason": "threshold_configuration_changed",
                            "no_refusal_inference": True,
                        },
                    )
        return {"threshold": threshold, "version": next_version}

    def record_appointment(
        self,
        candidate_id: str,
        outcome: str,
        appointment_confirmed: bool,
        actor: str,
    ) -> dict[str, Any]:
        if outcome not in EVENT_OUTCOMES:
            raise ValueError("Unsupported appointment outcome.")
        if not isinstance(appointment_confirmed, bool):
            raise ValueError("appointment_confirmed must be a boolean.")
        actor = clean_actor(actor)
        with self.connection() as db:
            case = db.execute(
                "SELECT candidate_id FROM cases WHERE candidate_id = ? AND is_synthetic = 1",
                (candidate_id,),
            ).fetchone()
            if case is None:
                raise KeyError("Synthetic case was not found.")
            if not self._is_case_active(db, candidate_id):
                raise ValueError("Case is closed. Reopen it before recording new scenario events.")
            db.execute(
                """
                INSERT INTO appointment_events(candidate_id, outcome, appointment_confirmed, actor_label, occurred_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (candidate_id, outcome, int(appointment_confirmed), actor, utc_now()),
            )
            events = [
                dict(row)
                for row in db.execute(
                    "SELECT outcome, appointment_confirmed FROM appointment_events WHERE candidate_id = ? ORDER BY event_id",
                    (candidate_id,),
                )
            ]
            threshold, version = self.threshold(db)
            status = escalation_status(events, threshold)
            self._audit(
                db,
                candidate_id,
                "appointment_outcome_recorded",
                actor,
                {
                    "outcome": outcome,
                    "appointment_confirmed": appointment_confirmed,
                    "eligible_count": status.eligible_count,
                    "threshold": threshold,
                    "threshold_version": version,
                    "synthetic_only": True,
                },
            )
            if status.required and self._investigation_pending(
                db, candidate_id, True, status.eligible_count, version
            ):
                self._audit(
                    db,
                    candidate_id,
                    "human_review_required",
                    "Workflow",
                    {
                        "eligible_count": status.eligible_count,
                        "threshold": threshold,
                        "threshold_version": version,
                        "reason": "eligible_count_greater_than_threshold",
                        "no_refusal_inference": True,
                    },
                )
            return {
                "eligible_count": status.eligible_count,
                "threshold": threshold,
                "review_required": status.required,
                "message": status.message,
            }

    def close_case(self, candidate_id: str, actor: str, reason: str) -> None:
        actor = clean_actor(actor)
        if reason not in CLOSURE_REASONS:
            raise ValueError("Choose a supported synthetic closure reason.")
        with self.connection() as db:
            if db.execute(
                "SELECT 1 FROM cases WHERE candidate_id = ? AND is_synthetic = 1",
                (candidate_id,),
            ).fetchone() is None:
                raise KeyError("Synthetic case was not found.")
            if not self._is_case_active(db, candidate_id):
                raise ValueError("Case is already closed.")
            events = [
                dict(event)
                for event in db.execute(
                    "SELECT outcome, appointment_confirmed FROM appointment_events WHERE candidate_id = ? ORDER BY event_id",
                    (candidate_id,),
                )
            ]
            threshold, version = self.threshold(db)
            status = escalation_status(events, threshold)
            if self._investigation_pending(
                db, candidate_id, status.required, status.eligible_count, version
            ):
                raise ValueError("Record the required human investigation before closing this case.")
            db.execute(
                """
                INSERT INTO appointment_events(candidate_id, outcome, appointment_confirmed, actor_label, occurred_at)
                VALUES(?, 'case_closed', 0, ?, ?)
                """,
                (candidate_id, actor, utc_now()),
            )
            self._audit(db, candidate_id, "case_closed", actor, {"reason": reason, "counter_reset": True})

    def reopen_case(self, candidate_id: str, actor: str) -> None:
        actor = clean_actor(actor)
        with self.connection() as db:
            if db.execute(
                "SELECT 1 FROM cases WHERE candidate_id = ? AND is_synthetic = 1",
                (candidate_id,),
            ).fetchone() is None:
                raise KeyError("Synthetic case was not found.")
            if self._is_case_active(db, candidate_id):
                raise ValueError("Case is already active.")
            db.execute(
                """
                INSERT INTO appointment_events(candidate_id, outcome, appointment_confirmed, actor_label, occurred_at)
                VALUES(?, 'case_reopened', 0, ?, ?)
                """,
                (candidate_id, actor, utc_now()),
            )
            self._audit(db, candidate_id, "case_reopened", actor, {"counter_starts_new_active_episode": True})

    def update_controls(self, candidate_id: str, controls: dict[str, Any], actor: str) -> None:
        from .domain import GATE_LABELS

        actor = clean_actor(actor)
        unknown = set(controls) - set(GATE_LABELS)
        if unknown or any(not isinstance(value, bool) for value in controls.values()):
            raise ValueError("Scenario controls contain an unsupported gate or non-boolean value.")
        with self.connection() as db:
            if db.execute("SELECT 1 FROM cases WHERE candidate_id = ?", (candidate_id,)).fetchone() is None:
                raise KeyError("Synthetic case was not found.")
            for key, enabled in controls.items():
                db.execute(
                    """
                    INSERT INTO gate_controls(candidate_id, gate_key, enabled, updated_at)
                    VALUES(?, ?, ?, ?)
                    ON CONFLICT(candidate_id, gate_key) DO UPDATE SET enabled=excluded.enabled, updated_at=excluded.updated_at
                    """,
                    (candidate_id, key, int(enabled), utc_now()),
                )
            self._audit(db, candidate_id, "synthetic_gate_controls_updated", actor, controls)

    def advance_case(self, candidate_id: str, actor: str) -> dict[str, Any]:
        from .domain import check_transition

        actor = clean_actor(actor)
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM cases WHERE candidate_id = ? AND is_synthetic = 1",
                (candidate_id,),
            ).fetchone()
            if row is None:
                raise KeyError("Synthetic case was not found.")
            if not self._is_case_active(db, candidate_id):
                raise ValueError("Closed cases cannot advance.")
            controls = {
                control["gate_key"]: bool(control["enabled"])
                for control in db.execute(
                    "SELECT gate_key, enabled FROM gate_controls WHERE candidate_id = ?",
                    (candidate_id,),
                )
            }
            stage, missing = check_transition(
                row["scenario_stage"], controls, bool(row["safety_hold_active"])
            )
            if missing:
                return {"advanced": False, "missing": missing, "stage": row["scenario_stage"]}
            db.execute(
                "UPDATE cases SET scenario_stage = ? WHERE candidate_id = ?",
                (stage, candidate_id),
            )
            self._audit(db, candidate_id, "scenario_stage_advanced", actor, {"stage": stage, "synthetic_only": True})
            return {"advanced": True, "stage": stage, "missing": []}

    def record_review(self, candidate_id: str, actor: str) -> None:
        actor = clean_actor(actor)
        with self.connection() as db:
            if db.execute(
                "SELECT 1 FROM cases WHERE candidate_id = ? AND is_synthetic = 1",
                (candidate_id,),
            ).fetchone() is None:
                raise KeyError("Synthetic case was not found.")
            events = [
                dict(row)
                for row in db.execute(
                    "SELECT outcome, appointment_confirmed FROM appointment_events WHERE candidate_id = ? ORDER BY event_id",
                    (candidate_id,),
                )
            ]
            threshold, version = self.threshold(db)
            status = escalation_status(
                events, threshold, self._is_case_active(db, candidate_id)
            )
            if not self._investigation_pending(
                db, candidate_id, status.required, status.eligible_count, version
            ):
                raise ValueError("Human investigation is not currently required for this case.")
            self._audit(
                db,
                candidate_id,
                "human_investigation_recorded",
                actor,
                {
                    "outcome": "investigated",
                    "eligible_count": status.eligible_count,
                    "threshold": threshold,
                    "threshold_version": version,
                    "does_not_classify_refusal": True,
                },
            )

    def import_cases(
        self,
        rows: list[dict[str, Any]],
        source_file: str,
        digest: str,
        rejected_count: int,
        actor: str,
    ) -> int:
        actor = clean_actor(actor)
        imported_at = utc_now()
        inserted = 0
        with self.connection() as db:
            for record in rows:
                cursor = db.execute(
                    """
                    INSERT OR IGNORE INTO cases(
                        candidate_id, property_ref, current_status, scenario_stage, owner, locality,
                        archetype_id, lead_supplier, rag_status, safety_hold_active, is_synthetic,
                        source_file, source_row, imported_at
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1, ?, ?, ?)
                    """,
                    (
                        record["candidate_id"],
                        record["property_ref"],
                        record["current_status"],
                        normalize_scenario_stage(record["current_status"])
                        or record["current_status"],
                        record["owner"],
                        record["locality"],
                        record["archetype_id"],
                        record["lead_supplier"],
                        record["rag_status"],
                        source_file,
                        record["source_row"],
                        imported_at,
                    ),
                )
                if cursor.rowcount != 1:
                    raise ValueError(
                        f"Case {record['candidate_id']} now exists; nothing was imported. Re-preview the workbook."
                    )
                inserted += 1
            db.execute(
                """
                INSERT INTO imports(source_file, sha256, accepted_count, rejected_count, actor_label, imported_at)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (source_file, digest, inserted, rejected_count, actor, imported_at),
            )
            self._audit(
                db,
                None,
                "synthetic_workbook_imported",
                actor,
                {
                    "source_file": source_file,
                    "sha256": digest,
                    "accepted_rows": inserted,
                    "rejected_rows": rejected_count,
                    "synthetic_only": True,
                },
            )
        return inserted

    def export_bundle(self) -> dict[str, Any]:
        with self.connection() as db:
            cases = [
                dict(row)
                for row in db.execute(
                    "SELECT candidate_id, property_ref, current_status, scenario_stage, owner, locality, archetype_id, lead_supplier, rag_status, safety_hold_active, is_synthetic, source_file, source_row FROM cases ORDER BY candidate_id"
                )
            ]
            for case in cases:
                case["safety_hold_active"] = bool(case["safety_hold_active"])
                case["is_synthetic"] = bool(case["is_synthetic"])
            events = [
                dict(row)
                for row in db.execute(
                    "SELECT candidate_id, outcome, appointment_confirmed, actor_label, occurred_at, source_file FROM appointment_events ORDER BY event_id"
                )
            ]
            for event in events:
                event["appointment_confirmed"] = bool(event["appointment_confirmed"])
            audit = []
            for row in db.execute(
                    "SELECT candidate_id, event_type, actor_label, details_json, created_at FROM audit_log ORDER BY audit_id"
            ):
                entry = dict(row)
                entry["details"] = json.loads(entry.pop("details_json"))
                audit.append(entry)
            threshold, version = self.threshold(db)
            return {
                "export_version": "1.0",
                "generated_at": utc_now(),
                "scope": "Local synthetic viability prototype; not operational evidence.",
                "is_synthetic": True,
                "configuration": {"threshold": threshold, "version": version},
                "cases": cases,
                "appointment_events": events,
                "audit_log": audit,
                "agent_runs": [
                    json.loads(row["record_json"])
                    for row in db.execute("SELECT record_json FROM agent_runs ORDER BY created_at, rowid")
                ],
                "m365": {"enabled": False, "reason": "Not configured; no tenant credentials used."},
            }

    @staticmethod
    def _audit(
        db: sqlite3.Connection,
        candidate_id: str | None,
        event_type: str,
        actor: str,
        details: dict[str, Any],
    ) -> None:
        db.execute(
            """
            INSERT INTO audit_log(candidate_id, event_type, actor_label, details_json, created_at)
            VALUES(?, ?, ?, ?, ?)
            """,
            (candidate_id, event_type, actor, json.dumps(details, ensure_ascii=False), utc_now()),
        )


def clean_actor(value: Any) -> str:
    actor = str(value or "").strip()
    if actor not in ACTOR_LABELS:
        raise ValueError("Choose a supported synthetic reviewer label.")
    return actor
