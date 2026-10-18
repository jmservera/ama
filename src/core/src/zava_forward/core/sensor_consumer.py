"""Finite constructed sensor admission. No transport or operational authority."""

import hashlib
import json
import math
import re
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Protocol, cast

from .mssqlstore import MssqlStore
from .sqlstore import SqlStore
from .synthetic.sensor_faults import READING_FIELDS, SCHEMA_VERSION

IDENTITY = re.compile(r"[A-Z0-9][A-Z0-9_-]*\Z")
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]{0,2})(?:\.[0-9]{1,2})?\Z")
STAMP = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\Z")
READING_COLUMNS = (
    "sensor_id",
    "reading_id",
    "home_id",
    "observed_at",
    "temperature_c",
    "humidity_pct",
    "source_type",
    "scenario",
    "seed",
    "schema_version",
    "injected_fault",
)
Primitive = str | int | float | bool | None
Observation = dict[str, Primitive]
REJECTIONS = frozenset(
    {
        "SCHEMA",
        "IDENTITY",
        "PROVENANCE",
        "UTC_TIME",
        "NUMBER",
        "CALIBRATION",
        "UNMAPPED",
        "HOME_MISMATCH",
        "HOME_UNAVAILABLE",
        "MAPPING_INTERVAL",
        "CONSENT",
        "WINDOW",
        "CLOCK_SKEW",
        "UNIT",
        "RANGE",
        "OUT_OF_ORDER",
        "IDENTITY_CONFLICT",
    }
)


class Cursor(Protocol):
    def fetchone(self) -> Sequence[object] | None: ...
    def fetchall(self) -> Sequence[Sequence[object]]: ...


class Connection(Protocol):
    def execute(self, sql: str, args: Sequence[object] = ()) -> Cursor: ...
    def close(self) -> None: ...


class ConsumerError(RuntimeError):
    def __init__(self, code: str, reference: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.reference = reference


def utc(value: str) -> datetime:
    if not isinstance(value, str) or not STAMP.fullmatch(value):
        raise ValueError("UTC_SECONDS_REQUIRED")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _text(value: object, limit: int) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= limit
        and value.isascii()
        and value.isprintable()
    )


def _identity(value: object, limit: int) -> bool:
    return _text(value, limit) and isinstance(value, str) and bool(IDENTITY.fullmatch(value))


@dataclass(frozen=True)
class ExercisePolicy:
    window_start: str
    window_end: str
    max_past_seconds: int
    max_future_seconds: int
    temperature_min: float
    temperature_max: float
    humidity_min: float
    humidity_max: float
    accountable_role: str
    manual_route: str
    reviewer: str | None

    def validate(self) -> None:
        if utc(self.window_start) >= utc(self.window_end):
            raise ValueError("INVALID_EXERCISE_WINDOW")
        for n in (self.max_past_seconds, self.max_future_seconds):
            if type(n) is not int or not 0 <= n <= 86400 * 31:
                raise ValueError("INVALID_EXERCISE_CLOCK")
        for low, high in (
            (self.temperature_min, self.temperature_max),
            (self.humidity_min, self.humidity_max),
        ):
            if any(type(v) not in (float, int) or not math.isfinite(v) for v in (low, high)):
                raise ValueError("INVALID_EXERCISE_RANGE")
            if not -999.99 <= low <= high <= 999.99:
                raise ValueError("INVALID_EXERCISE_RANGE")
        if not 0 <= self.humidity_min <= self.humidity_max <= 100:
            raise ValueError("INVALID_EXERCISE_RANGE")
        if not all(_text(v, 80) and v.strip() for v in (self.accountable_role, self.manual_route)):
            raise ValueError("MANUAL_ROUTE_REQUIRED")
        if self.reviewer is not None and not (_text(self.reviewer, 80) and self.reviewer.strip()):
            raise ValueError("INVALID_REVIEWER")


@dataclass(frozen=True)
class SensorControl:
    sensor_id: str
    home_id: str
    mapping_start: str
    mapping_end: str
    consent: str
    calibration_start: str
    calibration_end: str
    calibration_confirmed: bool
    temperature_unit: str
    humidity_unit: str

    def validate(self) -> None:
        if not _identity(self.sensor_id, 20) or not _identity(self.home_id, 64):
            raise ValueError("INVALID_CONTROL_IDENTITY")
        if self.consent not in ("granted", "unknown", "declined"):
            raise ValueError("INVALID_CONTROL_CONSENT")
        if type(self.calibration_confirmed) is not bool:
            raise ValueError("INVALID_CONTROL_CALIBRATION")
        for start, end in (
            (self.mapping_start, self.mapping_end),
            (self.calibration_start, self.calibration_end),
        ):
            if utc(start) >= utc(end):
                raise ValueError("INVALID_CONTROL_INTERVAL")
        if (self.temperature_unit, self.humidity_unit) != ("degC", "percent"):
            raise ValueError("UNSUPPORTED_CONTROL_UNITS")


@dataclass(frozen=True)
class Receipt:
    reference: str
    status: str
    reason: str
    replay: bool = False


def preflight(batch: object) -> list[Observation]:
    """Bound the envelope first; closed-schema faults are durable per-row DQ."""
    if not isinstance(batch, (list, tuple)) or not 1 <= len(batch) <= 100:
        raise ConsumerError("INVALID_BATCH")
    result: list[Observation] = []
    for row in batch:
        if not isinstance(row, dict) or len(row) > 20:
            raise ConsumerError("INVALID_BATCH")
        copied: Observation = {}
        for key, value in row.items():
            if (
                not isinstance(key, str)
                or len(key) > 80
                or type(value) not in (str, int, float, bool, type(None))
            ):
                raise ConsumerError("INVALID_BATCH")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                if isinstance(value, int) and abs(value) > 2**63 - 1:
                    raise ConsumerError("INVALID_BATCH")
            copied[key] = value
        if len(json.dumps(copied, ensure_ascii=True).encode()) > 4096:
            raise ConsumerError("INVALID_BATCH")
        result.append(copied)
    return result


class SensorConsumer:
    def __init__(self, store: object) -> None:
        if not isinstance(store, SqlStore):
            raise ConsumerError("UNSUPPORTED_STORE_SQL_REQUIRED")
        self.store = store
        self.mssql = isinstance(store, MssqlStore)

    def _connect(self) -> Connection:
        try:
            return cast(Connection, self.store.assistant_connection())
        except self.store.dberror:
            raise ConsumerError("SENSOR_SQL_UNAVAILABLE") from None

    @contextmanager
    def _write(self, reference: str | None = None) -> Iterator[Connection]:
        db = self._connect()
        began = False
        committing = False
        try:
            db.execute("BEGIN IMMEDIATE")
            began = True
            yield db
            committing = True
            db.execute("COMMIT")
            began = False
        except self.store.dberror:
            raise ConsumerError(
                "SENSOR_COMMIT_UNCERTAIN" if committing else "SENSOR_SQL_UNAVAILABLE", reference
            ) from None
        finally:
            try:
                if began:
                    try:
                        db.execute("ROLLBACK")
                    except self.store.dberror:
                        raise ConsumerError(
                            "SENSOR_COMMIT_UNCERTAIN"
                            if committing
                            else "SENSOR_SQL_RECOVERY_FAILED",
                            reference,
                        ) from None
            finally:
                try:
                    db.close()
                except self.store.dberror:
                    raise ConsumerError(
                        "SENSOR_COMMIT_UNCERTAIN" if committing else "SENSOR_SQL_CLOSE_FAILED",
                        reference,
                    ) from None

    def configure(self, policy: ExercisePolicy, controls: Sequence[SensorControl]) -> None:
        """Trusted in-process exercise setup, never called with an observation."""
        policy.validate()
        if len(controls) > 100 or len({c.sensor_id for c in controls}) != len(controls):
            raise ValueError("INVALID_CONTROL_BATCH")
        for control in controls:
            control.validate()
        with self._write() as db:
            self._schema(db)
            db.execute("DELETE FROM sensor_consumer_policy")
            db.execute(
                "INSERT INTO sensor_consumer_policy (id, body) VALUES (1, ?)",
                (json.dumps(asdict(policy)),),
            )
            db.execute("DELETE FROM sensor_consumer_control")
            for control in controls:
                db.execute(
                    "INSERT INTO sensor_consumer_control (sensor_id, body) VALUES (?, ?)",
                    (control.sensor_id, json.dumps(asdict(control))),
                )

    def _schema(self, db: Connection) -> None:
        text = "NVARCHAR(MAX)" if self.mssql else "TEXT"
        key = "VARCHAR(64) COLLATE Latin1_General_100_BIN2" if self.mssql else "TEXT"
        tables = {
            "sensor_consumer_policy": f"(id INT NOT NULL PRIMARY KEY, body {text} NOT NULL)",
            "sensor_consumer_control": (
                f"(sensor_id {key} NOT NULL PRIMARY KEY, body {text} NOT NULL)"
            ),
            "sensor_delivery": (
                f"(reference {key} NOT NULL PRIMARY KEY, status VARCHAR(12) NOT NULL,"
                " reason VARCHAR(40) NOT NULL, received_at VARCHAR(20) NOT NULL,"
                f" observation_body {text} NULL)"
            ),
            "sensor_data_quality_exception": (
                f"(reference {key} NOT NULL PRIMARY KEY, reason VARCHAR(40) NOT NULL,"
                " status VARCHAR(12) NOT NULL, observed_at VARCHAR(20) NULL,"
                " received_at VARCHAR(20) NOT NULL, accountable_role VARCHAR(80) NOT NULL,"
                " manual_route VARCHAR(80) NOT NULL, reviewer VARCHAR(80) NOT NULL)"
            ),
        }
        if self.mssql:
            from .synthetic.sensor_backfill import STOCK_SQL_DDL

            reading = STOCK_SQL_DDL.split("CREATE TABLE sensor_reading", 1)[1]
            reading = reading.replace(
                "VARCHAR(12) NOT NULL,\n  injected_fault", "VARCHAR(32) NOT NULL,\n  injected_fault"
            )
            # Explicit case equality on fresh keys; legacy inputs use uppercase ASCII only.
            reading = reading.replace("VARCHAR(73)", f"VARCHAR(73) {self._collation}")
            reading = reading.replace("VARCHAR(96)", f"VARCHAR(96) {self._collation}")
            tables["sensor_reading"] = reading.rstrip(";")
        else:
            tables["sensor_reading"] = (
                "("
                + ", ".join(f"{c} TEXT" for c in READING_COLUMNS)
                + ", PRIMARY KEY (sensor_id, reading_id))"
            )
        for name, body in tables.items():
            ddl = f"CREATE TABLE {name} {body}"
            if self.mssql:
                db.execute(f"IF OBJECT_ID(N'{name}', N'U') IS NULL {ddl}")
            else:
                db.execute(ddl.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1))
        self._check_reading_schema(db)

    _collation = "COLLATE Latin1_General_100_BIN2"

    def _check_reading_schema(self, db: Connection) -> None:
        if self.mssql:
            rows = db.execute(
                "SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION,"
                " NUMERIC_SCALE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='sensor_reading'"
            ).fetchall()
            columns = {str(r[0]): r for r in rows}
            if set(columns) != set(READING_COLUMNS):
                raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")
            for name, minimum in (
                ("sensor_id", 20),
                ("reading_id", 40),
                ("home_id", 12),
                ("source_type", 12),
                ("scenario", 20),
                ("schema_version", 12),
            ):
                row = columns[name]
                if row[1] not in ("varchar", "nvarchar") or int(str(row[2])) < minimum:
                    raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")
            if any(
                columns[n][1] != "decimal" or columns[n][3:5] != (5, 2)
                for n in ("temperature_c", "humidity_pct")
            ):
                raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")
            if columns["observed_at"][1] != "datetime2" or columns["seed"][1] != "bigint":
                raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")
            keys = db.execute(
                "SELECT c.name FROM sys.indexes i JOIN sys.index_columns ic"
                " ON i.object_id=ic.object_id AND i.index_id=ic.index_id"
                " JOIN sys.columns c ON c.object_id=ic.object_id AND c.column_id=ic.column_id"
                " WHERE i.object_id=OBJECT_ID('sensor_reading') AND i.is_primary_key=1"
                " ORDER BY ic.key_ordinal"
            ).fetchall()
            if [r[0] for r in keys] != ["sensor_id", "reading_id"]:
                raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")
            if int(str(columns["schema_version"][2])) < len(SCHEMA_VERSION):
                db.execute(
                    "ALTER TABLE sensor_reading ALTER COLUMN schema_version VARCHAR(32) NOT NULL"
                )
        else:
            rows = db.execute("PRAGMA table_info(sensor_reading)").fetchall()
            if {r[1] for r in rows} != set(READING_COLUMNS) or [
                r[1] for r in sorted(rows, key=lambda r: int(str(r[5]))) if r[5]
            ] != ["sensor_id", "reading_id"]:
                raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")
            if any(str(r[2]).upper() != "TEXT" for r in rows):
                raise ConsumerError("SENSOR_SCHEMA_UNSUPPORTED")

    def _policy(self, db: Connection) -> ExercisePolicy:
        row = db.execute("SELECT body FROM sensor_consumer_policy WHERE id=1").fetchone()
        if row is None:
            raise ConsumerError("SENSOR_CONTROLS_UNAVAILABLE")
        try:
            policy = ExercisePolicy(**json.loads(str(row[0])))
            policy.validate()
        except (TypeError, ValueError, OverflowError):
            raise ConsumerError("SENSOR_CONTROLS_MALFORMED") from None
        return policy

    @staticmethod
    def _shape(row: Observation) -> str | None:
        if set(row) != set(READING_FIELDS) or any(type(v) is not str for v in row.values()):
            return "SCHEMA"
        if row["schema_version"] != SCHEMA_VERSION or row["source_type"] != "SYNTHETIC":
            return "SCHEMA"
        for name, length in (("sensor_id", 20), ("reading_id", 40), ("home_id", 12)):
            if not _identity(row[name], length):
                return "IDENTITY"
        if not _identity(row["scenario"], 20):
            return "PROVENANCE"
        seed = str(row["seed"])
        if not re.fullmatch(r"-?(?:0|[1-9][0-9]{0,18})", seed) or abs(int(seed)) > 2**63 - 1:
            return "PROVENANCE"
        try:
            utc(str(row["observed_at"]))
        except ValueError:
            return "UTC_TIME"
        for name in ("temperature_c", "humidity_pct"):
            if not NUMBER.fullmatch(str(row[name])) or abs(Decimal(str(row[name]))) > 999.99:
                return "NUMBER"
        if row["calibrated"] not in ("true", "false"):
            return "CALIBRATION"
        return None

    @staticmethod
    def _reference(row: Observation) -> str:
        return hashlib.sha256(
            json.dumps(row, sort_keys=True, ensure_ascii=True).encode()
        ).hexdigest()

    def _retained_reading(
        self, reading: Sequence[object], expected: Observation | None = None
    ) -> datetime:
        stored = dict(zip(READING_COLUMNS, reading, strict=True))
        value = stored["observed_at"]
        try:
            if isinstance(value, datetime):
                if value.tzinfo is not None or value.microsecond:
                    raise ValueError("INVALID_STORED_TIME")
                observed = value.replace(tzinfo=UTC)
            else:
                observed = utc(str(value))
            for name in ("temperature_c", "humidity_pct"):
                number = str(stored[name])
                if not NUMBER.fullmatch(number) or abs(Decimal(number)) > Decimal("999.99"):
                    raise ValueError("INVALID_STORED_NUMBER")
        except ValueError:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED") from None

        if expected is None:
            if stored["schema_version"] == "reading-v1":
                # Legacy generator rows predate consumer witnesses.
                return observed
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        if self._shape(expected) is not None:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        for name in READING_COLUMNS:
            if name == "observed_at":
                matches = observed == utc(str(expected[name]))
            elif name in ("temperature_c", "humidity_pct"):
                matches = Decimal(str(stored[name])) == Decimal(str(expected[name]))
            elif name == "seed":
                seed = str(stored[name])
                matches = (
                    re.fullmatch(r"-?(?:0|[1-9][0-9]{0,18})", seed) is not None
                    and abs(int(seed)) <= 2**63 - 1
                    and int(seed) == int(str(expected[name]))
                )
            elif name == "injected_fault":
                matches = stored[name] is None
            else:
                matches = stored[name] == expected[name]
            if not matches:
                raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        return observed

    def _accepted_witness(self, body: object, reference: str) -> Observation:
        if not isinstance(body, str) or len(body.encode()) > 4096:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        try:
            parsed = json.loads(body)
        except ValueError:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED") from None
        if not isinstance(parsed, dict) or self._shape(parsed) is not None:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        if self._reference(parsed) != reference:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        return cast(Observation, parsed)

    def _latest_observed(self, db: Connection, sensor_id: Primitive) -> datetime | None:
        extract = "JSON_VALUE" if self.mssql else "json_extract"
        valid = "ISJSON" if self.mssql else "json_valid"
        safe_body = f"CASE WHEN {valid}(observation_body)=1 THEN observation_body ELSE NULL END"
        retained = db.execute(
            "SELECT reference, observation_body FROM sensor_delivery"
            " WHERE status='accepted' AND reason='ACCEPTED'"
            f" AND {extract}({safe_body}, '$.sensor_id')=?",
            (sensor_id,),
        ).fetchall()
        witnesses: dict[str, Observation] = {}
        for reference, body in retained:
            witness = self._accepted_witness(body, str(reference))
            reading_id = str(witness["reading_id"])
            if witness["sensor_id"] != sensor_id or reading_id in witnesses:
                raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
            witnesses[reading_id] = witness
        readings = db.execute(
            f"SELECT {', '.join(READING_COLUMNS)} FROM sensor_reading WHERE sensor_id=?",
            (sensor_id,),
        ).fetchall()
        latest = None
        for reading in readings:
            observed = self._retained_reading(reading, witnesses.pop(str(reading[1]), None))
            latest = observed if latest is None else max(latest, observed)
        if witnesses:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        return latest

    def _quality(
        self, db: Connection, row: Observation, policy: ExercisePolicy, received: datetime
    ) -> str | None:
        observed = utc(str(row["observed_at"]))
        control_row = db.execute(
            "SELECT body FROM sensor_consumer_control WHERE sensor_id=?", (row["sensor_id"],)
        ).fetchone()
        if control_row is None:
            return "UNMAPPED"
        try:
            control = SensorControl(**json.loads(str(control_row[0])))
            control.validate()
        except (TypeError, ValueError, OverflowError):
            raise ConsumerError("SENSOR_CONTROLS_MALFORMED") from None
        if control.sensor_id != row["sensor_id"]:
            raise ConsumerError("SENSOR_CONTROLS_MALFORMED")
        if control.home_id != row["home_id"]:
            return "HOME_MISMATCH"
        if db.execute("SELECT id FROM cases WHERE id=?", (control.home_id,)).fetchone() is None:
            return "HOME_UNAVAILABLE"
        if not utc(control.mapping_start) <= observed < utc(control.mapping_end):
            return "MAPPING_INTERVAL"
        if control.consent != "granted":
            return "CONSENT"
        if not utc(policy.window_start) <= observed < utc(policy.window_end):
            return "WINDOW"
        age = (received - observed).total_seconds()
        if not -policy.max_future_seconds <= age <= policy.max_past_seconds:
            return "CLOCK_SKEW"
        if (row["temperature_unit"], row["humidity_unit"]) != (
            control.temperature_unit,
            control.humidity_unit,
        ):
            return "UNIT"
        if (
            row["calibrated"] != "true"
            or not control.calibration_confirmed
            or not utc(control.calibration_start) <= observed < utc(control.calibration_end)
        ):
            return "CALIBRATION"
        if not policy.temperature_min <= float(str(row["temperature_c"])) <= policy.temperature_max:
            return "RANGE"
        if not policy.humidity_min <= float(str(row["humidity_pct"])) <= policy.humidity_max:
            return "RANGE"
        latest = self._latest_observed(db, row["sensor_id"])
        if latest is not None and observed <= latest:
            return "OUT_OF_ORDER"
        return None

    def process(self, row: Observation, received_at: str) -> Receipt:
        row = preflight([row])[0]
        received = utc(received_at)
        reference = self._reference(row)
        with self._write(reference) as db:
            prior = db.execute(
                "SELECT status, reason, observation_body FROM sensor_delivery WHERE reference=?",
                (reference,),
            ).fetchone()
            if prior:
                prior_status, prior_reason = str(prior[0]), str(prior[1])
                if (
                    prior_status == "accepted"
                    and prior_reason == "ACCEPTED"
                    and self._shape(row) is None
                ):
                    witness = self._accepted_witness(prior[2], reference)
                    if witness != row:
                        raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                    reading = db.execute(
                        f"SELECT {', '.join(READING_COLUMNS)} FROM sensor_reading"
                        " WHERE sensor_id=? AND reading_id=?",
                        (row["sensor_id"], row["reading_id"]),
                    ).fetchone()
                    if reading is None:
                        raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                    self._retained_reading(reading, witness)
                elif prior_status == "rejected" and prior_reason in REJECTIONS:
                    quality = db.execute(
                        "SELECT reason, status FROM sensor_data_quality_exception"
                        " WHERE reference=?",
                        (reference,),
                    ).fetchone()
                    if quality is None or tuple(quality) != (prior_reason, "Open"):
                        raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                else:
                    raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                return Receipt(reference, str(prior[0]), str(prior[1]), replay=True)
            policy = self._policy(db)
            reason = self._shape(row)
            observation_body = json.dumps(row, sort_keys=True) if reason is None else None
            if reason is None:
                exists = db.execute(
                    "SELECT reading_id FROM sensor_reading WHERE sensor_id=? AND reading_id=?",
                    (row["sensor_id"], row["reading_id"]),
                ).fetchone()
                reason = "IDENTITY_CONFLICT" if exists else self._quality(db, row, policy, received)
            receipt = Receipt(reference, "rejected" if reason else "accepted", reason or "ACCEPTED")
            if not reason:
                values: list[object] = []
                values.extend(row[c] for c in READING_COLUMNS[:-1])
                values.append(None)
                if self.mssql:
                    values[3] = utc(str(row["observed_at"])).replace(tzinfo=None)
                db.execute(
                    f"INSERT INTO sensor_reading ({', '.join(READING_COLUMNS)})"
                    f" VALUES ({', '.join('?' for _ in READING_COLUMNS)})",
                    values,
                )
            db.execute(
                "INSERT INTO sensor_delivery"
                " (reference, status, reason, received_at, observation_body)"
                " VALUES (?, ?, ?, ?, ?)",
                (reference, receipt.status, receipt.reason, received_at, observation_body),
            )
            if reason:
                observed: str | None = None
                try:
                    utc(str(row.get("observed_at")))
                    observed = str(row["observed_at"])
                except ValueError:
                    pass
                db.execute(
                    "INSERT INTO sensor_data_quality_exception"
                    " (reference, reason, status, observed_at, received_at,"
                    " accountable_role, manual_route, reviewer) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        reference,
                        reason,
                        "Open",
                        observed,
                        received_at,
                        policy.accountable_role,
                        policy.manual_route,
                        policy.reviewer or "Unassigned",
                    ),
                )
        try:
            self.acknowledge(receipt)
        except Exception:
            raise ConsumerError("SENSOR_COMMIT_UNCERTAIN", reference) from None
        return receipt

    def acknowledge(self, receipt: Receipt) -> None:
        """Post-COMMIT seam: a caller must reconcile any lost acknowledgement."""

    def inspect_exception(self, reference: str) -> Mapping[str, object] | None:
        if not re.fullmatch(r"[a-f0-9]{64}", reference):
            raise ConsumerError("INVALID_REFERENCE")
        db = self._connect()
        try:
            columns = (
                "reference",
                "reason",
                "status",
                "observed_at",
                "received_at",
                "accountable_role",
                "manual_route",
                "reviewer",
            )
            row = db.execute(
                f"SELECT {', '.join(columns)} FROM sensor_data_quality_exception WHERE reference=?",
                (reference,),
            ).fetchone()
            return dict(zip(columns, row, strict=True)) if row else None
        except self.store.dberror:
            raise ConsumerError("SENSOR_SQL_UNAVAILABLE") from None
        finally:
            db.close()
