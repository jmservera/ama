"""Public synthetic simulation lane for the Quality sensor assistant (issue 1288, CANDIDATE design).

The whole model input is composed here, from the bundled public fixture case below and from the
readings persisted in a dedicated simulation store (its own SQLite file, schema and HMAC key file).
No working-store case, document, reading or free text can enter: the composer takes none. The
composer seals the exact serialized provider body bytes; the real Ai client verifies that seal
against the bytes it serialized, before any data hold, meter, token or socket. The private and real
captured-data route stays off: a captured request without a valid seal is refused as before.

Disclosed limits: a withdrawal between the last check and the socket send is not made atomic here
(the lane carries only public synthetic data); in-process hostile code that reads the key file or
replaces the client's verifier is outside this boundary.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import stat
import tempfile
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol

from . import ai_consumption, assistants, sensor_view
from .sensor_consumer import ExercisePolicy, Observation, SensorConsumer, SensorControl
from .sqlstore import SqlStore
from .synthetic.live_readings import Reading

NAMESPACE = "zf-public-simulation-quality-v1"
CAPABILITY = "quality-evidence"
HOME_ID = "SIM-PUBLIC-1"
SENSOR_ID = "SENS-SYN-PUB1"
DEVICE_ID = "SYN-SENS-PUB1"
STORE_ENV, KEY_ENV = "ZF_SIM_STORE", "ZF_SIM_KEY_FILE"
SEAL_SECONDS = 120
KEY_BYTES = 32
SLOTS = 12
LABEL = "Public synthetic simulation. Not a real home, resident or device."
MANUAL = "Use the ordinary quality check and the manual route; nothing was sent to a model."
PROPOSAL_STATE = "unapproved-proposal"
MAX_OUTPUT_CHARS = 4000
WINDOW = ("2026-01-01T00:00:00Z", "2036-01-01T00:00:00Z")

FIXTURE: dict[str, Any] = {
    "id": HOME_ID,
    "stage": "Quality check",
    "wave": 0,
    "owner_code": "SIM",
    "closed": False,
    "days_in_stage": 0,
    "hazards": [],
    "appointments": [],
    "contacts": [],
    "documents": [],
    "contractor": {"name": "Fixture Installer Ltd"},
    "resident": {"name": "Fixture Resident"},
    "funding": {"status": "Not started"},
    "home": {
        "address": "1 Fixture Row",
        "area": "Fixtureville",
        "town": "Exampletown",
        "postcode": "ZZ1 1ZZ",
        "type": "Terraced",
        "built": "1950s",
        "epc": "D",
        "tenure": "Social rent",
    },
    "measures": ["Loft insulation"],
    "quality": [
        {
            "measure": "Loft insulation",
            "state": "Submitted",
            "checklist_version": "QC-LOFT v1",
            "evidence_version": 1,
            "recorded_at": "2026-01-05T10:00:00Z",
            "items": [
                {"label": "Depth measured and photo taken", "evidence": "Fixture photo 1"},
                {"label": "Ventilation at the eaves kept clear", "evidence": "Fixture photo 2"},
            ],
        }
    ],
}

POLICY = ExercisePolicy(
    window_start=WINDOW[0],
    window_end=WINDOW[1],
    max_past_seconds=86400,
    max_future_seconds=0,
    temperature_min=-10,
    temperature_max=45,
    humidity_min=0,
    humidity_max=100,
    accountable_role="public-simulation",
    manual_route="manual-sensor-review",
    reviewer="Public fixture",
)
CONTROL = SensorControl(
    sensor_id=SENSOR_ID,
    home_id=HOME_ID,
    mapping_start=WINDOW[0],
    mapping_end=WINDOW[1],
    consent="granted",
    calibration_start=WINDOW[0],
    calibration_end=WINDOW[1],
    calibration_confirmed=True,
    temperature_unit="degC",
    humidity_unit="percent",
)

DDL = (
    "CREATE TABLE IF NOT EXISTS sim_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS sim_seals (nonce TEXT PRIMARY KEY, digest TEXT NOT NULL,"
    " expires REAL NOT NULL, state TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS sim_proposals (id INTEGER PRIMARY KEY AUTOINCREMENT,"
    " digest TEXT NOT NULL, state TEXT NOT NULL, body TEXT NOT NULL, created REAL NOT NULL)",
)


class Ticket(Protocol):
    """One admitted call: a refusal reason, or an obligation to end it with the envelope."""

    reason: str | None

    def end(self, envelope: Mapping[str, Any]) -> None: ...

    def send_fence(self) -> None: ...


@dataclass(frozen=True)
class Admission:
    """The operator authority the lane runs under: late hold check, bounds and call admission."""

    hold: Callable[[], str | None]
    bounds: Callable[[], tuple[int, int]]
    begin: Callable[[int, str], Ticket]


class Unavailable(RuntimeError):
    """The lane is not configured or its store or key is unsafe; callers show the manual route."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "ascii"
    )


def _same(a: str, b: str) -> bool:
    try:
        return os.path.samefile(a, b)
    except OSError:
        return os.path.realpath(a) == os.path.realpath(b)


def _read_key(path: str) -> bytes:
    try:
        info = os.lstat(path)
    except OSError as error:
        raise Unavailable("key-unavailable") from error
    if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or info.st_size != KEY_BYTES:
        raise Unavailable("key-unsafe")
    try:
        with open(path, "rb") as handle:
            key = handle.read(KEY_BYTES + 1)
    except OSError as error:
        raise Unavailable("key-unreadable") from error
    if len(key) != KEY_BYTES:
        raise Unavailable("key-unsafe")
    return key


def provision(store_path: str, key_path: str, working: tuple[str, ...] = ()) -> None:
    """Trusted one-time setup of the dedicated store and its own credential."""
    if _same_path(store_path, key_path) or any(_same_path(store_path, w) for w in working if w):
        raise Unavailable("store-not-separate")
    if os.path.exists(store_path) or os.path.exists(key_path):
        raise Unavailable("already-provisioned")
    key = secrets.token_bytes(KEY_BYTES)
    descriptor = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(key)
    with tempfile.TemporaryDirectory() as scratch:
        seed = os.path.join(scratch, "fixture.json")
        with open(seed, "w", encoding="utf-8") as handle:
            json.dump({"cases": [FIXTURE], "staff": []}, handle)
        store = SqlStore(
            seed,
            store_path,
            docs_dir=os.path.join(scratch, "docs"),
            digest_dir=os.path.join(scratch, "digests"),
        )
        try:
            SensorConsumer(store).configure(POLICY, [CONTROL])
            for statement in DDL:
                store.db.execute(statement)
            store.db.execute("INSERT INTO sim_meta VALUES ('namespace', ?)", (NAMESPACE,))
            store.db.execute(
                "INSERT INTO sim_meta VALUES ('store_id', ?)", (secrets.token_hex(16),)
            )
        finally:
            store.db.close()
    os.chmod(store_path, 0o600)


def _same_path(a: str, b: str) -> bool:
    return os.path.realpath(a) == os.path.realpath(b) or (
        os.path.exists(a) and os.path.exists(b) and _same(a, b)
    )


class Lane:
    """The trusted composer, minter and verifier over one dedicated simulation store."""

    def __init__(self, store: SqlStore, key: bytes, clock: Callable[[], float] = time.time) -> None:
        self.store, self.key, self.clock = store, key, clock
        try:
            db = store.assistant_connection()
            try:
                meta = dict(db.execute("SELECT key,value FROM sim_meta").fetchall())
            finally:
                db.close()
        except sqlite3.Error as error:
            raise Unavailable("store-not-simulation") from error
        if meta.get("namespace") != NAMESPACE or not meta.get("store_id"):
            raise Unavailable("store-not-simulation")
        self.store_id: str = meta["store_id"]

    @classmethod
    def open(
        cls,
        env: Mapping[str, str],
        working: tuple[str, ...] = (),
        clock: Callable[[], float] = time.time,
    ) -> Lane:
        path, key_path = env.get(STORE_ENV), env.get(KEY_ENV)
        if not path or not key_path:
            raise Unavailable("not-configured")
        if not os.path.isfile(path):
            raise Unavailable("store-unavailable")
        if any(w and _same_path(path, w) for w in working) or _same_path(path, key_path):
            raise Unavailable("store-not-separate")
        key = _read_key(key_path)
        try:
            probe = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            try:
                ids = [r[0] for r in probe.execute("SELECT id FROM cases")]
                tables = {
                    r[0] for r in probe.execute("SELECT name FROM sqlite_master WHERE type='table'")
                }
            finally:
                probe.close()
        except sqlite3.Error as error:
            raise Unavailable("store-not-simulation") from error
        if ids != [HOME_ID] or not {"sim_meta", "sim_seals", "sim_proposals"} <= tables:
            raise Unavailable("store-not-simulation")
        try:
            store = SqlStore(
                path,
                path,
                docs_dir=os.path.join(os.path.dirname(path), "sim-docs"),
                digest_dir=os.path.join(os.path.dirname(path), "sim-digests"),
            )
        except (sqlite3.Error, OSError) as error:
            raise Unavailable("store-unavailable") from error
        try:
            return cls(store, key, clock)
        except Unavailable:
            store.db.close()
            raise

    def close(self) -> None:
        self.store.db.close()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        db: sqlite3.Connection = self.store.assistant_connection()
        try:
            yield db
        finally:
            db.close()

    def observe(self) -> int:
        """Persist the latest public 5-minute readings through the real consumer."""
        now = int(self.clock())
        latest = now // 300 * 300
        consumer = SensorConsumer(self.store)
        added = 0
        with self._connect() as db:
            row = db.execute(
                "SELECT MAX(observed_at) FROM sensor_reading WHERE home_id=?", (HOME_ID,)
            ).fetchone()
        newest = row[0] if row and row[0] else ""
        for index in range(SLOTS - 1, -1, -1):
            slot = datetime.fromtimestamp(latest - index * 300, UTC)
            if slot.strftime("%Y-%m-%dT%H:%M:%SZ") <= newest:
                continue
            step = (latest - index * 300) // 300 % 12
            reading = Reading(
                HOME_ID,
                SENSOR_ID,
                DEVICE_ID,
                slot,
                18.0 + step * 0.1,
                55.0 + step * 0.5,
                100.0 + step,
                1288,
            )
            observed: Observation = {**reading.row()}
            receipt = consumer.process(observed, slot.strftime("%Y-%m-%dT%H:%M:%SZ"))
            added += receipt.status == "accepted"
        return added

    def view(self) -> dict[str, Any]:
        with self._connect() as db:
            out: dict[str, Any] = sensor_view.view(
                db, HOME_ID, sensor_view.reference_for(FIXTURE["quality"]), int(self.clock())
            )
        return out

    def compose(self, max_tokens: int = 600) -> dict[str, Any]:
        from .ai import Ai

        with self._connect() as db:
            sensors = sensor_view.capture_source(
                db, HOME_ID, sensor_view.reference_for(FIXTURE["quality"]), int(self.clock())
            )
        snapshot = assistants.capture(CAPABILITY, FIXTURE, sensors=sensors)
        task = {"capability": CAPABILITY, "snapshot": snapshot, "dispatch": {}}
        system, prompt = assistants.build_request(task)
        body = Ai.provider_body(system, prompt, max_tokens, 0)
        readings = (
            sorted(
                (r["reading_id"], r.get("temperature_c"), r.get("humidity_pct"))
                for r in sensor_view.citations(sensors).values()
            )
            if sensor_view.citations(sensors)
            else []
        )
        return dict(
            system=system,
            prompt=prompt,
            body=body,
            snapshot=snapshot,
            readings=readings,
            digest=hashlib.sha256(body).hexdigest(),
            max_tokens=max_tokens,
        )

    def _mac(self, fields: Mapping[str, Any]) -> str:
        return hmac.new(self.key, canonical(fields), hashlib.sha256).hexdigest()

    def mint(self, body: bytes) -> dict[str, Any]:
        fields = dict(
            ns=NAMESPACE,
            store=self.store_id,
            nonce=secrets.token_hex(16),
            digest=hashlib.sha256(body).hexdigest(),
            exp=self.clock() + SEAL_SECONDS,
        )
        with self._connect() as db:
            db.execute(
                "INSERT INTO sim_seals VALUES (?,?,?,'minted')",
                (fields["nonce"], fields["digest"], fields["exp"]),
            )
        return dict(fields, mac=self._mac(fields))

    def verify(self, seal: Mapping[str, Any], body: bytes) -> None:
        """Raise SimulationRefused unless this lane minted the seal for exactly these bytes."""
        refuse = ai_consumption.SimulationRefused
        names = ("ns", "store", "nonce", "digest", "exp", "mac")
        if not isinstance(seal, Mapping) or set(seal) != set(names):
            raise refuse("malformed")
        if not all(
            isinstance(seal[k], str) for k in ("ns", "store", "nonce", "digest", "mac")
        ) or not isinstance(seal["exp"], int | float):
            raise refuse("malformed")
        fields = {k: seal[k] for k in names if k != "mac"}
        if not hmac.compare_digest(self._mac(fields), seal["mac"]):
            raise refuse("signature")
        if seal["ns"] != NAMESPACE:
            raise refuse("namespace")
        if seal["store"] != self.store_id:
            raise refuse("store")
        if not hmac.compare_digest(seal["digest"], hashlib.sha256(body).hexdigest()):
            raise refuse("payload-mismatch")
        if self.clock() >= seal["exp"]:
            raise refuse("expired")
        with self._connect() as db:
            known = db.execute("SELECT 1 FROM sim_seals WHERE nonce=?", (seal["nonce"],)).fetchone()
            if known is None:
                raise refuse("unknown-nonce")
            used = db.execute(
                "UPDATE sim_seals SET state='consumed'"
                " WHERE nonce=? AND state='minted' AND digest=?",
                (seal["nonce"], seal["digest"]),
            ).rowcount
        if used != 1:
            raise refuse("replayed")

    def last_proposal(self) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT digest,state,body,created FROM sim_proposals ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if not row:
            return None
        stored = json.loads(row[2])
        supplied = stored.get("readings") or []
        named = {
            c
            for f in (stored.get("output") or {}).get("findings", [])
            for c in f.get("citations", [])
            if isinstance(c, str)
        }
        cited = [r for r in supplied if f"sensor:{SENSOR_ID}:{r[0]}" in named]
        return dict(digest=row[0], state=row[1], created=row[3], cited=cited, **stored)

    def request(self, ai: Any, admission: Admission) -> dict[str, Any]:
        """One sealed request over the composed public payload; the result is unapproved.

        The call is admitted by the operator authority, durable allowance and active-call slots
        before a seal is minted, so a declined request reaches no meter, token or socket.
        """
        base: dict[str, Any] = dict(label=LABEL, manual_route=MANUAL, namespace=NAMESPACE)
        if not getattr(ai, "configured", False):
            return dict(base, status="unavailable", reason="model-not-configured")
        if not getattr(ai, "send_fence_supported", False):
            return dict(base, status="unavailable", reason="real-provider-route-unavailable")
        max_tokens, timeout = admission.bounds()
        composed = self.compose(max_tokens)
        if not composed["readings"]:
            return dict(base, status="unavailable", reason="no-simulation-readings")
        ticket = admission.begin(
            len(composed["system"]) + len(composed["prompt"]), secrets.token_hex(32)
        )
        if ticket.reason:
            return dict(base, status="held", reason=ticket.reason)
        envelope: dict[str, Any] = dict(outcome="suspended-before-dispatch", usage=None)
        try:
            seal = self.mint(composed["body"])
            nonce = seal["nonce"]
            context = ai_consumption.CallContext(
                ai_consumption.reference(nonce),
                ai_consumption.reference(f"{nonce}:1"),
                CAPABILITY,
                "retrofit-case",
                ai_consumption.reference(NAMESPACE),
                ai_consumption.reference(composed["system"]),
            )
            envelope = dict(outcome="provider-unavailable", usage=None)
            with (
                ai_consumption.call_context(context),
                ai_consumption.captured_readings(True),
                ai_consumption.sealed_simulation(seal),
                ai_consumption.send_fence(ticket.send_fence),
            ):
                envelope = ai.evidence(
                    composed["system"], composed["prompt"], composed["max_tokens"], timeout
                )
        finally:
            ticket.end(envelope)
        sent = dict(request_digest=composed["digest"], readings=composed["readings"])
        if envelope.get("outcome") != "returned":
            return dict(
                base,
                status="not-sent"
                if envelope.get("outcome")
                in ("simulation-refused", "suspended-before-dispatch", "financial-held", "disabled")
                else "model-failed",
                reason=envelope.get("reason") or envelope.get("outcome"),
                **sent,
            )
        if admission.hold():
            return dict(
                base, status="held", reason="Suspended after the request; output discarded.", **sent
            )
        try:
            output = assistants.validate_output(
                json.loads(envelope["text"]), composed["snapshot"], MAX_OUTPUT_CHARS
            )
        except (ValueError, TypeError):
            return dict(
                base,
                status="invalid-output",
                reason="The output failed the citation checks.",
                **sent,
            )
        stored = dict(output=output, model=envelope.get("model"), **sent)
        with self._connect() as db:
            db.execute(
                "INSERT INTO sim_proposals (digest,state,body,created) VALUES (?,?,?,?)",
                (composed["digest"], PROPOSAL_STATE, json.dumps(stored), self.clock()),
            )
        return dict(base, status="proposal", state=PROPOSAL_STATE, output=output, **sent)

    def state(self) -> dict[str, Any]:
        view = self.view()
        return dict(
            label=LABEL,
            manual_route=MANUAL,
            namespace=NAMESPACE,
            status="ready",
            home=FIXTURE["home"],
            view=view,
            proposal=self.last_proposal(),
            generated_at=(datetime.now(UTC) + timedelta(0)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )


def unavailable_state(code: str) -> dict[str, Any]:
    return dict(
        label=LABEL, manual_route=MANUAL, namespace=NAMESPACE, status="unavailable", reason=code
    )
