"""Simulated IoT device identity provisioning, secret-redacted logging, and SIM-* teardown (#185).

Records the chosen device identity approach (`per-device symmetric SAS / DPS enrollment group`)
and named credential owner role (`Platform Engineering / IoT Operations Owner`). Ephemeral
per-device symmetric SAS credentials are derived at runtime inside `SymmetricSasCredentialStore`
and addressed exclusively by immutable opaque `secretref://` URIs so raw symmetric keys,
connection strings, and SAS tokens never appear in source, summaries, audit records, or logs.
"""

import base64
import contextlib
import hashlib
import hmac
import logging
import re
import secrets
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import privacy, sensor_identity, sensor_stock

VERSION = "simulated-live-provisioning-v1"
DEVICE_IDENTITY_APPROACH = di.DEVICE_IDENTITY_APPROACH
CREDENTIAL_OWNER_ROLE = di.CREDENTIAL_OWNER_ROLE
DEFAULT_CREDENTIAL_OWNER = CREDENTIAL_OWNER_ROLE
CREDENTIAL_ROTATION_POLICY = "ephemeral-per-run-issue-before-revoke"
SIMULATED_DEVICE_PREFIX = "SIM-"
REDACTED = "<redacted>"
TeardownReceipt = di.TeardownReceipt

_OWNER_PLACEHOLDERS = frozenset(
    {"tbc", "tbd", "todo", "n/a", "na", "none", "unknown", "unassigned"}
)
_SAFE_URI_RE = re.compile(r"\b(?:secretref|kv)://[A-Za-z0-9._/-]+")
_PEM_PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z0-9 ]*PRIVATE KEY-----"
)
_CONNECTION_STRING_RE = re.compile(
    r"(?i)(?:HostName|Endpoint|IdScope)\s*=\s*[^;\s'\"<>]+"
    r"(?:\s*;\s*[^;\s'\"<>]+)*"
    r"\s*;\s*(?:SharedAccessKey|SharedAccessSignature|AccountKey|DeviceKey|SymmetricKey)"
    r"\s*=\s*[^;\s'\"<>]+"
    r"(?:\s*;\s*[^;\s'\"<>]+)*"
)
_SAS_TOKEN_RE = re.compile(
    r"(?i)\bSharedAccessSignature\s+sr=[^\s'\",;<>]+(?:\s+[^\s'\",;<>]+=[^\s'\",;<>]+)*"
)
_SAS_SIG_PARAM_RE = re.compile(r"(?i)(?<=[?&;\s])sig=[A-Za-z0-9%/+=_-]{8,}")
_NAMED_SECRET_ASSIGN_RE = re.compile(
    r"(?i)\b(?:SharedAccessKey|PrimaryKey|SecondaryKey|AccountKey|SymmetricKey|"
    r"DeviceKey|MasterKey|EnrollmentGroupKey|sas_token|connection_string)"
    r"\s*[:=]\s*[^\s,;'\"}]+"
)
_B64_CANDIDATE_RE = re.compile(r"(?<![A-Za-z0-9/_:-])[A-Za-z0-9+/]{32,}={0,2}(?![A-Za-z0-9/_:-])")
_URLSAFE_B64_CANDIDATE_RE = re.compile(r"(?<![A-Za-z0-9/_:-])[A-Za-z0-9_-]{40,}(?![A-Za-z0-9/_:-])")
_HEX64_RE = re.compile(r"[0-9a-fA-F]{64}")

_STANDARD_LOG_ATTRS = frozenset(
    {
        *logging.LogRecord("x", 0, "", 0, "", (), None).__dict__.keys(),
        "message",
        "asctime",
    }
)

_SIM_LOCKS: dict[str, threading.RLock] = {}
_SIM_LOCKS_GUARD = threading.Lock()


def _sim_run_lock(run_id: str) -> threading.RLock:
    with _SIM_LOCKS_GUARD:
        return _SIM_LOCKS.setdefault(run_id, threading.RLock())


def _looks_like_standalone_key(token: str) -> bool:
    if _HEX64_RE.fullmatch(token) is not None:
        return False
    has_lower = any(ch.islower() for ch in token)
    has_upper = any(ch.isupper() for ch in token)
    has_digit = any(ch.isdigit() for ch in token)
    if token.endswith("=") or "+" in token or "/" in token:
        return has_digit or (has_lower and has_upper)
    if "_" in token or "-" in token:
        if "--" in token or "__" in token:
            return False
        return has_lower and has_upper and has_digit
    return has_lower and has_upper and has_digit


def _scrub_string(text: str) -> str:
    if not text:
        return text
    protected: list[str] = []

    def _stash_uri(match: re.Match[str]) -> str:
        idx = len(protected)
        protected.append(match.group(0))
        return f"\x00URI{idx}\x00"

    scrubbed = _SAFE_URI_RE.sub(_stash_uri, text)
    scrubbed = _PEM_PRIVATE_KEY_RE.sub(REDACTED, scrubbed)
    scrubbed = _CONNECTION_STRING_RE.sub(REDACTED, scrubbed)
    scrubbed = _SAS_TOKEN_RE.sub(REDACTED, scrubbed)
    scrubbed = _SAS_SIG_PARAM_RE.sub(f"sig={REDACTED}", scrubbed)
    scrubbed = _NAMED_SECRET_ASSIGN_RE.sub(REDACTED, scrubbed)
    scrubbed = _B64_CANDIDATE_RE.sub(
        lambda m: REDACTED if _looks_like_standalone_key(m.group(0)) else m.group(0),
        scrubbed,
    )
    scrubbed = _URLSAFE_B64_CANDIDATE_RE.sub(
        lambda m: REDACTED if _looks_like_standalone_key(m.group(0)) else m.group(0),
        scrubbed,
    )
    for idx, uri in enumerate(protected):
        scrubbed = scrubbed.replace(f"\x00URI{idx}\x00", uri)
    return scrubbed


def redact_provisioning_secrets(value: object) -> object:
    """Recursively scrub symmetric keys, connection strings, SAS tokens, and PEM keys."""
    if isinstance(value, str):
        return _scrub_string(value)
    if isinstance(value, dict):
        return {
            redact_provisioning_secrets(key): redact_provisioning_secrets(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_provisioning_secrets(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_provisioning_secrets(item) for item in value)
    return value


def contains_raw_secret(text: str) -> bool:
    """Return True when `text` contains raw symmetric key, connection string, or SAS material."""
    return bool(text) and _scrub_string(text) != text


class SecretRedactingFilter(logging.Filter):
    """Logging filter that formats and scrubs messages, extras, and exception payloads."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            rendered = record.getMessage()
        except Exception:
            rendered = f"{record.msg} {record.args}" if record.args else str(record.msg)
        record.msg = _scrub_string(rendered)
        record.args = None
        if record.exc_info:
            exc = record.exc_info[1]
            if exc is not None:
                record.exc_text = _scrub_string(f"{type(exc).__name__}: {exc}")
            record.exc_info = None
        elif isinstance(record.exc_text, str):
            record.exc_text = _scrub_string(record.exc_text)
        if isinstance(record.stack_info, str):
            record.stack_info = _scrub_string(record.stack_info)
        for key, val in list(record.__dict__.items()):
            if key not in _STANDARD_LOG_ATTRS:
                record.__dict__[key] = redact_provisioning_secrets(val)
        return True


def install_provisioning_log_redaction(logger: logging.Logger) -> SecretRedactingFilter:
    """Ensure `SecretRedactingFilter` is attached once to `logger`."""
    for existing in logger.filters:
        if isinstance(existing, SecretRedactingFilter):
            return existing
    redactor = SecretRedactingFilter()
    logger.addFilter(redactor)
    return redactor


LOG = logging.getLogger(__name__)
install_provisioning_log_redaction(LOG)


class LiveProvisioningError(RuntimeError):
    """Fixed-code provisioning error that suppresses chained secret-bearing tracebacks."""

    def __init__(
        self,
        code: str,
        new_manifest: "ProvisioningManifest | None" = None,
    ) -> None:
        safe_code = _scrub_string(code)
        super().__init__(safe_code)
        self.__suppress_context__ = True
        self.new_manifest = new_manifest


def validate_credential_owner(credential_owner: str) -> str:
    """Validate that `credential_owner` names a real role without secrets or personal data."""
    if contains_raw_secret(credential_owner):
        raise LiveProvisioningError("CREDENTIAL_OWNER_SECRET_MATERIAL")
    if privacy.pattern_issues(credential_owner):
        raise LiveProvisioningError("CREDENTIAL_OWNER_PERSONAL_DATA")
    cleaned = credential_owner.strip()
    if not cleaned or cleaned.lower() in _OWNER_PLACEHOLDERS or cleaned.startswith("<"):
        raise LiveProvisioningError("CREDENTIAL_OWNER_NOT_NAMED")
    return cleaned


@dataclass(frozen=True)
class SimulatedDeviceIdentity:
    """Per-home `SIM-*` simulated device identity carrying only a non-secret credential URI."""

    device_id: str
    sensor_id: str
    home_id: str
    credential_ref: str = field(default="", repr=False)

    def validate(self) -> None:
        if (
            not di.SENSOR_ID.fullmatch(self.sensor_id)
            or self.device_id != SIMULATED_DEVICE_PREFIX + self.sensor_id
            or not sensor_identity.home_key(self.home_id)
            or self.sensor_id != sensor_identity.sensor_key(self.home_id)
            or contains_raw_secret(self.credential_ref)
        ):
            raise LiveProvisioningError("INVALID_DEVICE_IDENTITY")


@dataclass(frozen=True)
class ProvisioningManifest:
    """Provisioning manifest recording approach, credential owner role, and `SIM-*` mapping."""

    run_id: str
    identities: tuple[SimulatedDeviceIdentity, ...]
    approach: str = DEVICE_IDENTITY_APPROACH
    credential_owner: str = CREDENTIAL_OWNER_ROLE
    rotation_policy: str = CREDENTIAL_ROTATION_POLICY

    @property
    def identity_approach(self) -> str:
        return self.approach

    def validate(self) -> None:
        if not di.RUN_ID.fullmatch(self.run_id):
            raise LiveProvisioningError("INVALID_MANIFEST")
        if self.approach != DEVICE_IDENTITY_APPROACH:
            raise LiveProvisioningError("UNSUPPORTED_PROVISIONING_APPROACH")
        validate_credential_owner(self.credential_owner)
        if not self.rotation_policy.strip() or contains_raw_secret(self.rotation_policy):
            raise LiveProvisioningError("INVALID_ROTATION_POLICY")
        if not 1 <= len(self.identities) <= di.MAX_DEVICES:
            raise LiveProvisioningError("INVALID_DEVICE_COUNT")
        for identity in self.identities:
            identity.validate()
        for values in (
            [i.device_id for i in self.identities],
            [i.home_id for i in self.identities],
        ):
            if len(set(values)) != len(values):
                raise LiveProvisioningError("DEVICE_HOME_NOT_ONE_TO_ONE")

    def as_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "source_type": "SYNTHETIC",
            "contains_real_data": False,
            "version": VERSION,
            "run_id": self.run_id,
            "approach": self.approach,
            "identity_approach": self.approach,
            "enrollment_mode": "dps_enrollment_group",
            "credential_type": "per_device_symmetric_sas",
            "credential_owner": self.credential_owner,
            "rotation_policy": self.rotation_policy,
            "device_count": len(self.identities),
            "devices": [
                {
                    "device_id": i.device_id,
                    "sensor_id": i.sensor_id,
                    "home_id": i.home_id,
                    "credential_ref": i.credential_ref,
                }
                for i in self.identities
            ],
        }
        return cast(dict[str, object], redact_provisioning_secrets(payload))


ProvisioningPlan = ProvisioningManifest


def plan_simulated_provisioning(
    run_id: str,
    homes: Sequence[str | Mapping[str, object]] = (),
    *,
    credential_owner: str = CREDENTIAL_OWNER_ROLE,
    approach: str = DEVICE_IDENTITY_APPROACH,
    rotation_policy: str = CREDENTIAL_ROTATION_POLICY,
) -> ProvisioningManifest:
    """Build a validated `SIM-*` provisioning manifest for consenting synthetic stock homes."""
    failure: LiveProvisioningError | None = None
    manifest: ProvisioningManifest | None = None
    try:
        built: list[SimulatedDeviceIdentity] = []
        for entry in homes:
            if isinstance(entry, str):
                if not sensor_identity.home_key(entry):
                    raise LiveProvisioningError("INVALID_DEVICE_IDENTITY")
                sid = sensor_identity.sensor_key(entry)
                built.append(SimulatedDeviceIdentity(f"{SIMULATED_DEVICE_PREFIX}{sid}", sid, entry))
            elif isinstance(entry, Mapping):
                raw_sid = entry.get("sensor_id")
                raw_hid = entry.get("home_id")
                if not isinstance(raw_sid, str) or not isinstance(raw_hid, str):
                    raise LiveProvisioningError("INVALID_DEVICE_IDENTITY")
                built.append(
                    SimulatedDeviceIdentity(
                        f"{SIMULATED_DEVICE_PREFIX}{raw_sid}",
                        raw_sid,
                        raw_hid,
                    )
                )
            else:
                raise LiveProvisioningError("INVALID_DEVICE_IDENTITY")
        manifest = ProvisioningManifest(
            run_id=run_id,
            identities=tuple(built),
            approach=approach,
            credential_owner=credential_owner,
            rotation_policy=rotation_policy,
        )
        manifest.validate()
    except LiveProvisioningError as error:
        failure = error
    except Exception:
        failure = LiveProvisioningError("INVALID_MANIFEST")
    if failure is not None:
        raise LiveProvisioningError(str(failure)) from None
    assert manifest is not None
    return manifest


def plan_simulated_register(
    register_path: Path,
    homes: int,
    run_id: str,
    *,
    credential_owner: str = CREDENTIAL_OWNER_ROLE,
    approach: str = DEVICE_IDENTITY_APPROACH,
    seed: int = 7,
) -> ProvisioningManifest:
    """Select consenting synthetic homes from `register_path` and plan `SIM-*` identities."""
    selection = sensor_stock.read_register(register_path, homes)
    sensors = selection.sensors(seed)
    if not sensors:
        raise LiveProvisioningError("NO_MONITORED_HOMES")
    return plan_simulated_provisioning(
        run_id,
        sensors,
        credential_owner=credential_owner,
        approach=approach,
    )


@dataclass(frozen=True)
class _VaultEntry:
    run_id: str
    device_id: str
    derived_key_b64: str = field(repr=False)


class SymmetricSasCredentialStore:
    """In-memory DPS enrollment-group symmetric SAS vault returning opaque URIs only."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._enrollment_group_key: bytes = secrets.token_bytes(32)
        self._seq = 0
        self._vault: dict[str, _VaultEntry] = {}

    def __repr__(self) -> str:
        with self._lock:
            count = len(self._vault)
        return f"SymmetricSasCredentialStore(active_references={count})"

    def issue(self, device_id: str, run_id: str) -> str:
        if not device_id or not di.RUN_ID.fullmatch(run_id):
            raise LiveProvisioningError("CREDENTIAL_ISSUE_INVALID_INPUT")
        with self._lock:
            self._seq += 1
            seq = self._seq
            digest = hmac.new(
                self._enrollment_group_key,
                f"{run_id}:{device_id}:{seq}".encode(),
                hashlib.sha256,
            ).digest()
            derived_b64 = base64.b64encode(digest).decode("ascii")
            safe_dev = re.sub(r"[^a-z0-9._-]", "-", device_id.lower())
            reference = f"secretref://dps-sas/{run_id}/{safe_dev}/{seq}"
            self._vault[reference] = _VaultEntry(
                run_id=run_id,
                device_id=device_id,
                derived_key_b64=derived_b64,
            )
            return reference

    def revoke(self, reference: str) -> None:
        with self._lock:
            self._vault.pop(reference, None)

    def run_references(self, run_id: str) -> Sequence[str]:
        with self._lock:
            return tuple(ref for ref, entry in self._vault.items() if entry.run_id == run_id)

    def all_simulated_references(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(
                ref
                for ref, entry in self._vault.items()
                if entry.device_id.startswith(SIMULATED_DEVICE_PREFIX)
            )

    def has_reference(self, reference: str) -> bool:
        with self._lock:
            return reference in self._vault

    def active_count(self) -> int:
        with self._lock:
            return len(self._vault)


class SimulatedDeviceRegistry:
    """Deterministic thread-safe simulated device registry isolating `SIM-*` identities."""

    def __init__(self, initial_devices: Mapping[str, str] | None = None) -> None:
        self._lock = threading.Lock()
        self._devices: dict[str, str] = dict(initial_devices or {})

    def __repr__(self) -> str:
        with self._lock:
            sim_count = sum(1 for dev in self._devices if dev.startswith(SIMULATED_DEVICE_PREFIX))
            total = len(self._devices)
        return f"SimulatedDeviceRegistry(simulated={sim_count}, total={total})"

    def seed_non_simulated(self, device_id: str, owner_tag: str = "non-simulated") -> None:
        if device_id.startswith(SIMULATED_DEVICE_PREFIX):
            raise LiveProvisioningError("EXPECTED_NON_SIMULATED_DEVICE_ID")
        with self._lock:
            self._devices[device_id] = owner_tag

    def create(self, device_id: str, run_id: str) -> None:
        if not device_id.startswith(SIMULATED_DEVICE_PREFIX):
            raise LiveProvisioningError("NON_SIMULATED_DEVICE_ID")
        with self._lock:
            if device_id in self._devices:
                raise LiveProvisioningError("IDENTITY_CONFLICT")
            self._devices[device_id] = run_id

    def run_of(self, device_id: str) -> str | None:
        with self._lock:
            return self._devices.get(device_id)

    def delete(self, device_id: str, run_id: str) -> None:
        with self._lock:
            if self._devices.get(device_id) == run_id:
                del self._devices[device_id]

    def list_run(self, run_id: str) -> Sequence[str]:
        with self._lock:
            return tuple(sorted(dev for dev, tag in self._devices.items() if tag == run_id))

    def simulated_runs(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(
                sorted(
                    {
                        tag
                        for dev, tag in self._devices.items()
                        if dev.startswith(SIMULATED_DEVICE_PREFIX)
                    }
                )
            )

    def list_simulated(self, run_id: str | None = None) -> tuple[str, ...]:
        with self._lock:
            return tuple(
                sorted(
                    dev
                    for dev, tag in self._devices.items()
                    if dev.startswith(SIMULATED_DEVICE_PREFIX) and (run_id is None or tag == run_id)
                )
            )

    def list_all(self) -> dict[str, str]:
        with self._lock:
            return dict(self._devices)


@dataclass(frozen=True)
class ProvisioningAuditRecord:
    """Secret-redacted audit record for simulated device provisioning, rotation, or teardown."""

    action: str
    outcome: str
    run_id: str | None
    approach: str
    credential_owner: str
    device_ids: tuple[str, ...]
    credential_refs: tuple[str, ...]
    detail: str = ""

    @classmethod
    def sanitized(
        cls,
        *,
        action: str,
        outcome: str,
        run_id: str | None,
        approach: str,
        credential_owner: str,
        device_ids: Sequence[str],
        credential_refs: Sequence[str] = (),
        detail: str = "",
    ) -> "ProvisioningAuditRecord":
        return cls(
            action=_scrub_string(action),
            outcome=_scrub_string(outcome),
            run_id=_scrub_string(run_id) if run_id is not None else None,
            approach=_scrub_string(approach),
            credential_owner=_scrub_string(credential_owner),
            device_ids=tuple(_scrub_string(d) for d in device_ids),
            credential_refs=tuple(_scrub_string(r) for r in credential_refs),
            detail=_scrub_string(detail),
        )

    def as_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "source_type": "SYNTHETIC",
            "contains_real_data": False,
            "action": self.action,
            "outcome": self.outcome,
            "run_id": self.run_id,
            "approach": self.approach,
            "credential_owner": self.credential_owner,
            "device_ids": list(self.device_ids),
            "credential_refs": list(self.credential_refs),
            "detail": self.detail,
        }
        return cast(dict[str, object], redact_provisioning_secrets(payload))


@dataclass(frozen=True)
class ProvisioningSummary:
    """Secret-free provisioning or rotation result carrying manifest and audit record."""

    manifest: ProvisioningManifest
    registry: SimulatedDeviceRegistry | di.Registry
    credential_store: SymmetricSasCredentialStore | di.CredentialStore
    audit_record: ProvisioningAuditRecord

    def as_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "source_type": "SYNTHETIC",
            "contains_real_data": False,
            "version": VERSION,
            "run_id": self.manifest.run_id,
            "approach": self.manifest.approach,
            "identity_approach": self.manifest.approach,
            "enrollment_mode": "dps_enrollment_group",
            "credential_type": "per_device_symmetric_sas",
            "credential_owner": self.manifest.credential_owner,
            "rotation_policy": self.manifest.rotation_policy,
            "device_count": len(self.manifest.identities),
            "devices": [
                {
                    "device_id": i.device_id,
                    "sensor_id": i.sensor_id,
                    "home_id": i.home_id,
                    "credential_ref": i.credential_ref,
                }
                for i in self.manifest.identities
            ],
            "credentials": "stored in runtime vault; opaque references only",
            "audit": self.audit_record.as_dict(),
        }
        return cast(dict[str, object], redact_provisioning_secrets(payload))


def _record_audit(
    audit_log: list[ProvisioningAuditRecord] | None,
    record: ProvisioningAuditRecord,
) -> ProvisioningAuditRecord:
    if audit_log is not None:
        audit_log.append(record)
    return record


def provision_simulated_devices(
    manifest: ProvisioningManifest,
    registry: di.Registry | SimulatedDeviceRegistry | None = None,
    store: di.CredentialStore | SymmetricSasCredentialStore | None = None,
    *,
    note: str = "",
    audit_log: list[ProvisioningAuditRecord] | None = None,
) -> ProvisioningSummary:
    """Provision `SIM-*` identities and per-device symmetric SAS credentials atomically."""
    failure: LiveProvisioningError | None = None
    summary: ProvisioningSummary | None = None
    active_registry = registry if registry is not None else SimulatedDeviceRegistry()
    active_store = store if store is not None else SymmetricSasCredentialStore()
    try:
        manifest.validate()
        with _sim_run_lock(manifest.run_id):
            summary = _provision_simulated_locked(
                manifest,
                active_registry,
                active_store,
                note=note,
                audit_log=audit_log,
            )
    except LiveProvisioningError as error:
        failure = error
    if failure is not None:
        raise LiveProvisioningError(str(failure), failure.new_manifest) from None
    assert summary is not None
    return summary


def _provision_simulated_locked(
    manifest: ProvisioningManifest,
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore,
    *,
    note: str,
    audit_log: list[ProvisioningAuditRecord] | None,
) -> ProvisioningSummary:
    try:
        already_active = bool(
            registry.list_run(manifest.run_id) or store.run_references(manifest.run_id)
        )
        check_failed = False
    except Exception:
        already_active, check_failed = False, True
    if check_failed:
        _record_audit(
            audit_log,
            ProvisioningAuditRecord.sanitized(
                action="provision",
                outcome="failed",
                run_id=manifest.run_id,
                approach=manifest.approach,
                credential_owner=manifest.credential_owner,
                device_ids=[i.device_id for i in manifest.identities],
                detail=note or "ACTIVE_RUN_CHECK_FAILED",
            ),
        )
        LOG.warning("Simulated provisioning precheck failed for run_id=%s", manifest.run_id)
        raise LiveProvisioningError("ACTIVE_RUN_CHECK_FAILED") from None
    if already_active:
        _record_audit(
            audit_log,
            ProvisioningAuditRecord.sanitized(
                action="provision",
                outcome="refused",
                run_id=manifest.run_id,
                approach=manifest.approach,
                credential_owner=manifest.credential_owner,
                device_ids=[i.device_id for i in manifest.identities],
                detail=note or "RUN_ALREADY_ACTIVE",
            ),
        )
        LOG.warning("Simulated provisioning refused; run_id=%s already active", manifest.run_id)
        raise LiveProvisioningError("RUN_ALREADY_ACTIVE")

    created: list[SimulatedDeviceIdentity] = []
    attempted: SimulatedDeviceIdentity | None = None
    issued: list[SimulatedDeviceIdentity] = []
    failed_detail = ""
    failed = False
    try:
        for identity in manifest.identities:
            attempted = identity
            registry.create(identity.device_id, manifest.run_id)
            attempted = None
            created.append(identity)
            ref = store.issue(identity.device_id, manifest.run_id)
            if contains_raw_secret(ref):
                raise LiveProvisioningError("CREDENTIAL_REFERENCE_CONTAINS_SECRET")
            issued.append(
                SimulatedDeviceIdentity(
                    identity.device_id,
                    identity.sensor_id,
                    identity.home_id,
                    ref,
                )
            )
    except Exception as exc:
        failed = True
        failed_detail = _scrub_string(f"{type(exc).__name__}: {exc}")

    if failed:
        owner_tag = _safe_run_of(registry, attempted.device_id) if attempted is not None else None
        if attempted is not None and owner_tag == manifest.run_id:
            created.append(attempted)
        rollback_errors = _rollback_partial_provision(
            manifest.run_id,
            created,
            [i.credential_ref for i in issued],
            registry,
            store,
        )
        code = (
            "PROVISION_ROLLBACK_INCOMPLETE"
            if rollback_errors or owner_tag is _UNKNOWN_OWNER
            else "PROVISION_FAILED_ROLLED_BACK"
        )
        _record_audit(
            audit_log,
            ProvisioningAuditRecord.sanitized(
                action="provision",
                outcome="rolled_back" if code == "PROVISION_FAILED_ROLLED_BACK" else "failed",
                run_id=manifest.run_id,
                approach=manifest.approach,
                credential_owner=manifest.credential_owner,
                device_ids=[i.device_id for i in created],
                detail=f"{code}; {note}; {failed_detail}".strip("; "),
            ),
        )
        LOG.warning(
            "Simulated provisioning aborted for run_id=%s code=%s detail=%s",
            manifest.run_id,
            code,
            failed_detail,
        )
        raise LiveProvisioningError(code) from None

    provisioned = ProvisioningManifest(
        run_id=manifest.run_id,
        identities=tuple(issued),
        approach=manifest.approach,
        credential_owner=manifest.credential_owner,
        rotation_policy=manifest.rotation_policy,
    )
    audit = _record_audit(
        audit_log,
        ProvisioningAuditRecord.sanitized(
            action="provision",
            outcome="applied",
            run_id=provisioned.run_id,
            approach=provisioned.approach,
            credential_owner=provisioned.credential_owner,
            device_ids=[i.device_id for i in provisioned.identities],
            credential_refs=[i.credential_ref for i in provisioned.identities],
            detail=note or "provisioned per-device symmetric SAS credentials",
        ),
    )
    LOG.info(
        "Provisioned %d simulated devices for run_id=%s approach=%s owner=%s note=%s",
        len(provisioned.identities),
        provisioned.run_id,
        provisioned.approach,
        provisioned.credential_owner,
        note,
    )
    return ProvisioningSummary(
        manifest=provisioned,
        registry=registry,
        credential_store=store,
        audit_record=audit,
    )


_UNKNOWN_OWNER = object()


def _safe_run_of(
    registry: di.Registry | SimulatedDeviceRegistry,
    device_id: str,
) -> object:
    try:
        return registry.run_of(device_id)
    except Exception:
        return _UNKNOWN_OWNER


def _rollback_partial_provision(
    run_id: str,
    created: Sequence[SimulatedDeviceIdentity],
    issued_refs: Sequence[str],
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore,
) -> int:
    errors = 0
    for identity in sorted(created, key=lambda item: item.device_id):
        try:
            registry.delete(identity.device_id, run_id)
        except Exception:
            errors += 1
    refs: list[str] = list(dict.fromkeys(r for r in issued_refs if r))
    try:
        for discovered in store.run_references(run_id):
            if discovered not in refs:
                refs.append(discovered)
    except Exception:
        errors += 1
    for ref in refs:
        try:
            store.revoke(ref)
        except Exception:
            errors += 1
    try:
        still_present = [
            i.device_id for i in created if i.device_id in set(registry.list_run(run_id))
        ]
        still_refs = list(store.run_references(run_id))
        if still_present or still_refs:
            errors += 1
    except Exception:
        errors += 1
    return errors


def rotate_simulated_credentials(
    manifest: ProvisioningManifest,
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore,
    *,
    note: str = "",
    audit_log: list[ProvisioningAuditRecord] | None = None,
) -> ProvisioningSummary:
    """Issue fresh per-device symmetric SAS credentials before revoking prior references."""
    failure: LiveProvisioningError | None = None
    summary: ProvisioningSummary | None = None
    try:
        manifest.validate()
        with _sim_run_lock(manifest.run_id):
            summary = _rotate_simulated_locked(
                manifest,
                registry,
                store,
                note=note,
                audit_log=audit_log,
            )
    except LiveProvisioningError as error:
        failure = error
    if failure is not None:
        raise LiveProvisioningError(str(failure), failure.new_manifest) from None
    assert summary is not None
    return summary


def _rotate_simulated_locked(
    manifest: ProvisioningManifest,
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore,
    *,
    note: str,
    audit_log: list[ProvisioningAuditRecord] | None,
) -> ProvisioningSummary:
    run_id = manifest.run_id
    old_refs = [i.credential_ref for i in manifest.identities]
    if not all(old_refs) or len(set(old_refs)) != len(old_refs):
        raise LiveProvisioningError("ROTATION_REFERENCES_MISSING")
    try:
        owned = {i.device_id for i in manifest.identities}
        listed_sim = {d for d in registry.list_run(run_id) if d.startswith(SIMULATED_DEVICE_PREFIX)}
        precheck = (
            listed_sim == owned
            and all(registry.run_of(d) == run_id for d in owned)
            and set(old_refs) == set(store.run_references(run_id))
        )
    except Exception:
        raise LiveProvisioningError("ROTATION_CHECK_FAILED") from None
    if not precheck:
        raise LiveProvisioningError("ROTATION_STATE_MISMATCH")

    issued: list[SimulatedDeviceIdentity] = []
    issue_failed = False
    try:
        for identity in manifest.identities:
            new_ref = store.issue(identity.device_id, run_id)
            if contains_raw_secret(new_ref):
                raise LiveProvisioningError("CREDENTIAL_REFERENCE_CONTAINS_SECRET")
            issued.append(
                SimulatedDeviceIdentity(
                    identity.device_id,
                    identity.sensor_id,
                    identity.home_id,
                    new_ref,
                )
            )
    except Exception:
        issue_failed = True

    if issue_failed:
        undo_errors = 0
        try:
            extras = [r for r in store.run_references(run_id) if r not in set(old_refs)]
        except Exception:
            extras = []
            undo_errors += 1
        for ref in extras:
            try:
                store.revoke(ref)
            except Exception:
                undo_errors += 1
        code = "ROTATION_ROLLBACK_INCOMPLETE" if undo_errors else "ROTATION_FAILED_OLD_KEPT"
        _record_audit(
            audit_log,
            ProvisioningAuditRecord.sanitized(
                action="rotate",
                outcome="failed",
                run_id=run_id,
                approach=manifest.approach,
                credential_owner=manifest.credential_owner,
                device_ids=[i.device_id for i in manifest.identities],
                detail=f"{code}; {note}".strip("; "),
            ),
        )
        raise LiveProvisioningError(code) from None

    revoke_errors = 0
    for old_ref in old_refs:
        try:
            store.revoke(old_ref)
        except Exception:
            revoke_errors += 1
    rotated = ProvisioningManifest(
        run_id=run_id,
        identities=tuple(issued),
        approach=manifest.approach,
        credential_owner=manifest.credential_owner,
        rotation_policy=manifest.rotation_policy,
    )
    try:
        leftover = set(store.run_references(run_id)) != {
            i.credential_ref for i in rotated.identities
        }
    except Exception:
        revoke_errors += 1
        leftover = False
    if revoke_errors:
        raise LiveProvisioningError(f"ROTATION_REVOKE_FAILED:{revoke_errors}", rotated)
    if leftover:
        raise LiveProvisioningError("ROTATION_INCOMPLETE", rotated)

    audit = _record_audit(
        audit_log,
        ProvisioningAuditRecord.sanitized(
            action="rotate",
            outcome="applied",
            run_id=run_id,
            approach=rotated.approach,
            credential_owner=rotated.credential_owner,
            device_ids=[i.device_id for i in rotated.identities],
            credential_refs=[i.credential_ref for i in rotated.identities],
            detail=note or "rotated per-device symmetric SAS credentials",
        ),
    )
    LOG.info(
        "Rotated credentials for %d simulated devices in run_id=%s",
        len(rotated.identities),
        run_id,
    )
    return ProvisioningSummary(
        manifest=rotated,
        registry=registry,
        credential_store=store,
        audit_record=audit,
    )


def teardown_simulated_identities(
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore | None = None,
    *,
    manifest: ProvisioningManifest | None = None,
    run_id: str | None = None,
    credential_owner: str = CREDENTIAL_OWNER_ROLE,
    approach: str = DEVICE_IDENTITY_APPROACH,
    note: str = "",
    audit_log: list[ProvisioningAuditRecord] | None = None,
) -> TeardownReceipt:
    """Deterministically remove targeted `SIM-*` simulated identities and verify zero residual."""
    failure: LiveProvisioningError | None = None
    receipt: TeardownReceipt | None = None
    try:
        if manifest is not None:
            manifest.validate()
            if run_id is not None and run_id != manifest.run_id:
                raise LiveProvisioningError("TEARDOWN_RUN_MISMATCH")
            target_run: str | None = manifest.run_id
            effective_owner = manifest.credential_owner
            effective_approach = manifest.approach
        else:
            if approach != DEVICE_IDENTITY_APPROACH:
                raise LiveProvisioningError("UNSUPPORTED_PROVISIONING_APPROACH")
            effective_owner = validate_credential_owner(credential_owner)
            effective_approach = approach
            if run_id is not None and not di.RUN_ID.fullmatch(run_id):
                raise LiveProvisioningError("INVALID_MANIFEST")
            target_run = run_id

        if target_run is not None:
            with _sim_run_lock(target_run):
                receipt = _teardown_scoped_run(
                    target_run=target_run,
                    manifest=manifest,
                    registry=registry,
                    store=store,
                    approach=effective_approach,
                    credential_owner=effective_owner,
                    note=note,
                    audit_log=audit_log,
                )
        else:
            receipt = _teardown_all_simulated(
                registry=registry,
                store=store,
                approach=effective_approach,
                credential_owner=effective_owner,
                note=note,
                audit_log=audit_log,
            )
    except LiveProvisioningError as error:
        failure = error
    if failure is not None:
        raise LiveProvisioningError(str(failure)) from None
    assert receipt is not None
    return receipt


def _teardown_scoped_run(
    *,
    target_run: str,
    manifest: ProvisioningManifest | None,
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore | None,
    approach: str,
    credential_owner: str,
    note: str,
    audit_log: list[ProvisioningAuditRecord] | None,
) -> TeardownReceipt:
    try:
        run_listed = [
            d for d in registry.list_run(target_run) if d.startswith(SIMULATED_DEVICE_PREFIX)
        ]
    except Exception:
        raise LiveProvisioningError("TEARDOWN_FAILED") from None

    if manifest is not None:
        owned = {i.device_id for i in manifest.identities}
        try:
            foreign = any(registry.run_of(d) not in (None, target_run) for d in sorted(owned))
        except Exception:
            raise LiveProvisioningError("TEARDOWN_FAILED") from None
        if foreign:
            raise LiveProvisioningError("TEARDOWN_OWNERSHIP_MISMATCH")
        uncovered = set(run_listed) - owned
        if uncovered:
            raise LiveProvisioningError(f"TEARDOWN_MANIFEST_INCOMPLETE:{len(uncovered)}")
        candidates = sorted(owned)
    else:
        candidates = sorted(set(run_listed))

    present_before: list[str] = []
    errors = 0
    for device_id in candidates:
        try:
            if registry.run_of(device_id) == target_run:
                present_before.append(device_id)
            registry.delete(device_id, target_run)
        except Exception:
            errors += 1

    revoked_refs = _revoke_run_credentials(store, target_run, manifest)
    if revoked_refs is None:
        errors += 1
        revoked_count = 0
    else:
        revoked_count = len(revoked_refs)

    try:
        residual_sim = tuple(
            sorted(
                d for d in registry.list_run(target_run) if d.startswith(SIMULATED_DEVICE_PREFIX)
            )
        )
        residual_creds = len(list(store.run_references(target_run))) if store is not None else 0
    except Exception:
        errors += 1
        residual_sim = ()
        residual_creds = 0

    return _finalize_teardown_verification(
        run_id=target_run,
        approach=approach,
        credential_owner=credential_owner,
        removed_device_ids=tuple(present_before),
        revoked_credential_count=revoked_count,
        residual_simulated=residual_sim,
        residual_creds=residual_creds,
        errors=errors,
        note=note,
        audit_log=audit_log,
    )


def _revoke_run_credentials(
    store: di.CredentialStore | SymmetricSasCredentialStore | None,
    run_id: str,
    manifest: ProvisioningManifest | None,
) -> list[str] | None:
    if store is None:
        return []
    try:
        discovered = list(store.run_references(run_id))
    except Exception:
        return None
    explicit = (
        [i.credential_ref for i in manifest.identities if i.credential_ref]
        if manifest is not None
        else []
    )
    ordered = list(dict.fromkeys(r for r in explicit if r in set(discovered)))
    ordered += [r for r in discovered if r not in ordered]
    failed = False
    for ref in ordered:
        try:
            store.revoke(ref)
        except Exception:
            failed = True
    return None if failed else ordered


def _teardown_all_simulated(
    *,
    registry: di.Registry | SimulatedDeviceRegistry,
    store: di.CredentialStore | SymmetricSasCredentialStore | None,
    approach: str,
    credential_owner: str,
    note: str,
    audit_log: list[ProvisioningAuditRecord] | None,
) -> TeardownReceipt:
    if not isinstance(registry, SimulatedDeviceRegistry):
        raise LiveProvisioningError("RUN_SCOPE_REQUIRED")
    runs = registry.simulated_runs()
    with contextlib.ExitStack() as stack:
        for active_run in sorted(runs):
            stack.enter_context(_sim_run_lock(active_run))

        targets: list[tuple[str, str]] = []
        for active_run in sorted(registry.simulated_runs()):
            for device_id in registry.list_simulated(active_run):
                targets.append((device_id, active_run))
        targets.sort(key=lambda pair: (pair[0], pair[1]))

        removed: list[str] = []
        errors = 0
        for device_id, owner_run in targets:
            try:
                if registry.run_of(device_id) == owner_run:
                    removed.append(device_id)
                registry.delete(device_id, owner_run)
            except Exception:
                errors += 1

        revoked_refs: list[str] = []
        if store is not None:
            candidate_refs: list[str] = []
            try:
                for active_run in sorted(runs):
                    for ref in store.run_references(active_run):
                        if ref not in candidate_refs:
                            candidate_refs.append(ref)
                if isinstance(store, SymmetricSasCredentialStore):
                    for ref in store.all_simulated_references():
                        if ref not in candidate_refs:
                            candidate_refs.append(ref)
            except Exception:
                errors += 1
            for ref in candidate_refs:
                try:
                    store.revoke(ref)
                    revoked_refs.append(ref)
                except Exception:
                    errors += 1

        try:
            residual_sim = registry.list_simulated()
            if store is None:
                residual_creds = 0
            elif isinstance(store, SymmetricSasCredentialStore):
                residual_creds = len(store.all_simulated_references())
            else:
                residual_creds = sum(
                    len(list(store.run_references(active_run))) for active_run in runs
                )
        except Exception:
            errors += 1
            residual_sim = ()
            residual_creds = 0

        return _finalize_teardown_verification(
            run_id=None,
            approach=approach,
            credential_owner=credential_owner,
            removed_device_ids=tuple(removed),
            revoked_credential_count=len(revoked_refs),
            residual_simulated=residual_sim,
            residual_creds=residual_creds,
            errors=errors,
            note=note,
            audit_log=audit_log,
        )


def _finalize_teardown_verification(
    *,
    run_id: str | None,
    approach: str,
    credential_owner: str,
    removed_device_ids: tuple[str, ...],
    revoked_credential_count: int,
    residual_simulated: tuple[str, ...],
    residual_creds: int,
    errors: int,
    note: str,
    audit_log: list[ProvisioningAuditRecord] | None,
) -> TeardownReceipt:
    if errors or residual_simulated or residual_creds:
        if errors:
            code = f"TEARDOWN_FAILED:{errors}"
        elif residual_simulated:
            code = f"TEARDOWN_RESIDUAL_SIMULATED_IDENTITIES:{len(residual_simulated)}"
        else:
            code = "TEARDOWN_CREDENTIALS_REMAIN"
        _record_audit(
            audit_log,
            ProvisioningAuditRecord.sanitized(
                action="teardown",
                outcome="failed",
                run_id=run_id,
                approach=approach,
                credential_owner=credential_owner,
                device_ids=removed_device_ids,
                detail=f"{code}; {note}".strip("; "),
            ),
        )
        LOG.error(
            "Simulated teardown failed verification run_id=%s code=%s",
            run_id,
            code,
        )
        raise LiveProvisioningError(code)

    receipt = TeardownReceipt.verified(
        run_id=run_id,
        approach=approach,
        credential_owner=credential_owner,
        removed_device_ids=removed_device_ids,
        revoked_credential_count=revoked_credential_count,
    )
    _record_audit(
        audit_log,
        ProvisioningAuditRecord.sanitized(
            action="teardown",
            outcome="verified_zero_residual",
            run_id=run_id,
            approach=approach,
            credential_owner=credential_owner,
            device_ids=removed_device_ids,
            detail=(
                note
                or f"verified zero residual simulated identities ({receipt.verification_sha256})"
            ),
        ),
    )
    LOG.info(
        "Tore down %d simulated identities run_id=%s verified_zero_residual=%s note=%s",
        receipt.removed_count,
        run_id,
        receipt.verified_zero_residual,
        note,
    )
    return receipt


deprovision_simulated_devices = teardown_simulated_identities
