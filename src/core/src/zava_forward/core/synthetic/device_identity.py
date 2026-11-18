"""Run-owned simulated IoT Hub device identities: provision, store credentials, tear down.

Individual enrolment with per-device X.509 (ADR 0003 decision 6). Credential material only ever
crosses the CredentialStore boundary; manifests, reprs and errors carry references, never secrets.
"""

import hashlib
import json
import re
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from zava_forward.core.synthetic import live_readings, sensor_identity

VERSION = "simulated-device-identity-v1"
DEVICE_IDENTITY_APPROACH = "per-device symmetric SAS / DPS enrollment group"
CREDENTIAL_OWNER_ROLE = "Platform Engineering / IoT Operations Owner"
RUN_ID = re.compile(r"[a-z0-9][a-z0-9-]{2,31}")
SENSOR_ID = re.compile(r"[A-Z0-9][A-Z0-9_-]{0,19}")
CANONICAL_SLOT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
MAX_DEVICES = 100
_LOCKS: dict[str, threading.RLock] = {}
_LOCKS_GUARD = threading.Lock()


def _run_lock(run_id: str) -> threading.RLock:
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(run_id, threading.RLock())


class DeviceIdentityError(RuntimeError):
    """Fixed-code error; `new_manifest` carries non-secret references after a partial rotation.

    After ROTATION_REVOKE_FAILED or ROTATION_INCOMPLETE the supported recovery is
    `teardown(error.new_manifest, ...)`. Retrying `rotate` is unsupported.
    """

    def __init__(self, message: str, new_manifest: "Manifest | None" = None) -> None:
        super().__init__(message)
        self.new_manifest = new_manifest


class Registry(Protocol):
    def create(self, device_id: str, run_id: str) -> None: ...

    def run_of(self, device_id: str) -> str | None:
        """Return the run tag of an existing identity, or None when absent."""
        ...

    def delete(self, device_id: str, run_id: str) -> None:
        """Atomically remove the identity only if tagged `run_id`; otherwise a no-op."""
        ...

    def list_run(self, run_id: str) -> Sequence[str]: ...


class CredentialStore(Protocol):
    def issue(self, device_id: str, run_id: str) -> str:
        """Store a credential under a new immutable per-issuance reference owned by `run_id`.

        Return only the non-secret reference; a later issuance never reuses it.
        """
        ...

    def revoke(self, reference: str) -> None: ...

    def run_references(self, run_id: str) -> Sequence[str]:
        """Return every reference stored for `run_id`, including after an uncertain write."""
        ...


@dataclass(frozen=True)
class DeviceIdentity:
    device_id: str
    sensor_id: str
    home_id: str
    credential_ref: str = field(default="", repr=False)

    def validate(self) -> None:
        if (
            not SENSOR_ID.fullmatch(self.sensor_id)
            or self.device_id != "SYN-" + self.sensor_id
            or not sensor_identity.home_key(self.home_id)
            or self.sensor_id != sensor_identity.sensor_key(self.home_id)
        ):
            raise DeviceIdentityError("INVALID_DEVICE_IDENTITY")


def verify_envelope(device_id: str, row: Mapping[str, object]) -> None:
    """Bind a message to its own per-home Hub identity, schema version and stable reading ID."""
    sensor_id, home_id = row.get("sensor_id"), row.get("home_id")
    if (
        not isinstance(sensor_id, str)
        or not isinstance(home_id, str)
        or device_id != "SYN-" + sensor_id
        or not sensor_identity.home_key(home_id)
        or sensor_id != sensor_identity.sensor_key(home_id)
    ):
        raise DeviceIdentityError("DEVICE_ENVELOPE_MISMATCH")
    if row.get("schema_version") not in live_readings.LIVE_VERSIONS:
        raise DeviceIdentityError("SCHEMA_VERSION_REQUIRED")
    observed = row.get("observed_at")
    if not isinstance(observed, str) or not CANONICAL_SLOT.fullmatch(observed):
        raise DeviceIdentityError("READING_ID_MISMATCH")
    try:
        slot = datetime.strptime(observed, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise DeviceIdentityError("READING_ID_MISMATCH") from None
    grid = 5 if row.get("schema_version") == live_readings.SCHEMA_VERSION else 1
    if slot.second or slot.microsecond or slot.minute % grid:
        raise DeviceIdentityError("READING_ID_MISMATCH")
    if row.get("reading_id") != live_readings.reading_id_for(sensor_id, slot):
        raise DeviceIdentityError("READING_ID_MISMATCH")


@dataclass(frozen=True)
class Manifest:
    run_id: str
    credential_owner: str
    identities: tuple[DeviceIdentity, ...]
    approach: str = DEVICE_IDENTITY_APPROACH

    def validate(self) -> None:
        if (
            not RUN_ID.fullmatch(self.run_id)
            or not self.credential_owner.strip()
            or not self.approach.strip()
        ):
            raise DeviceIdentityError("INVALID_MANIFEST")
        if not 1 <= len(self.identities) <= MAX_DEVICES:
            raise DeviceIdentityError("INVALID_DEVICE_COUNT")
        for identity in self.identities:
            identity.validate()
        for values in (
            [i.device_id for i in self.identities],
            [i.home_id for i in self.identities],
        ):
            if len(set(values)) != len(values):
                raise DeviceIdentityError("DEVICE_HOME_NOT_ONE_TO_ONE")


def _teardown_digest(
    *,
    run_id: str | None,
    approach: str,
    credential_owner: str,
    removed_device_ids: tuple[str, ...],
    removed_count: int,
    revoked_credential_count: int,
    residual_simulated_identities: tuple[str, ...],
    residual_simulated_count: int,
    residual_credential_count: int,
    verified_zero_residual: bool,
) -> str:
    canonical = json.dumps(
        {
            "approach": approach,
            "credential_owner": credential_owner,
            "removed_count": removed_count,
            "removed_device_ids": list(removed_device_ids),
            "residual_credential_count": residual_credential_count,
            "residual_simulated_count": residual_simulated_count,
            "residual_simulated_identities": list(residual_simulated_identities),
            "revoked_credential_count": revoked_credential_count,
            "run_id": run_id,
            "verified_zero_residual": verified_zero_residual,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class TeardownReceipt:
    """Verifiable receipt proving deterministic simulated identity removal."""

    run_id: str | None
    approach: str
    credential_owner: str
    removed_device_ids: tuple[str, ...]
    removed_count: int
    revoked_credential_count: int
    residual_simulated_identities: tuple[str, ...]
    residual_simulated_count: int
    residual_credential_count: int
    verified_zero_residual: bool
    verification_sha256: str

    @classmethod
    def verified(
        cls,
        *,
        run_id: str | None,
        approach: str,
        credential_owner: str,
        removed_device_ids: tuple[str, ...],
        revoked_credential_count: int,
    ) -> "TeardownReceipt":
        removed = tuple(removed_device_ids)
        digest = _teardown_digest(
            run_id=run_id,
            approach=approach,
            credential_owner=credential_owner,
            removed_device_ids=removed,
            removed_count=len(removed),
            revoked_credential_count=revoked_credential_count,
            residual_simulated_identities=(),
            residual_simulated_count=0,
            residual_credential_count=0,
            verified_zero_residual=True,
        )
        return cls(
            run_id=run_id,
            approach=approach,
            credential_owner=credential_owner,
            removed_device_ids=removed,
            removed_count=len(removed),
            revoked_credential_count=revoked_credential_count,
            residual_simulated_identities=(),
            residual_simulated_count=0,
            residual_credential_count=0,
            verified_zero_residual=True,
            verification_sha256=digest,
        )

    def verify(self) -> bool:
        expected = _teardown_digest(
            run_id=self.run_id,
            approach=self.approach,
            credential_owner=self.credential_owner,
            removed_device_ids=self.removed_device_ids,
            removed_count=self.removed_count,
            revoked_credential_count=self.revoked_credential_count,
            residual_simulated_identities=self.residual_simulated_identities,
            residual_simulated_count=self.residual_simulated_count,
            residual_credential_count=self.residual_credential_count,
            verified_zero_residual=self.verified_zero_residual,
        )
        return (
            self.verified_zero_residual is True
            and self.residual_simulated_count == 0
            and self.residual_simulated_identities == ()
            and self.residual_credential_count == 0
            and self.removed_count == len(self.removed_device_ids)
            and self.verification_sha256 == expected
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "source_type": "SYNTHETIC",
            "contains_real_data": False,
            "run_id": self.run_id,
            "approach": self.approach,
            "identity_approach": self.approach,
            "credential_owner": self.credential_owner,
            "removed_device_ids": list(self.removed_device_ids),
            "removed_count": self.removed_count,
            "revoked_credential_count": self.revoked_credential_count,
            "residual_simulated_identities": list(self.residual_simulated_identities),
            "residual_simulated_count": self.residual_simulated_count,
            "residual_credential_count": self.residual_credential_count,
            "verified_zero_residual": self.verified_zero_residual,
            "verification_sha256": self.verification_sha256,
        }


def plan(
    run_id: str,
    credential_owner: str,
    sensors: Sequence[Mapping[str, object]],
    *,
    approach: str = DEVICE_IDENTITY_APPROACH,
) -> Manifest:
    """Map `Selection.sensors()` output to one identity per stock home; no credentials yet."""
    failure: DeviceIdentityError | None = None
    manifest: Manifest | None = None
    try:
        raw: list[DeviceIdentity] = []
        for s in sensors:
            sensor_id, home_id = s["sensor_id"], s["home_id"]
            if not isinstance(sensor_id, str) or not isinstance(home_id, str):
                raise DeviceIdentityError("INVALID_DEVICE_IDENTITY")
            raw.append(DeviceIdentity("SYN-" + sensor_id, sensor_id, home_id))
        identities = tuple(raw)
        manifest = Manifest(run_id, credential_owner, identities, approach=approach)
        manifest.validate()
    except DeviceIdentityError as error:
        failure = error
    except Exception:
        failure = DeviceIdentityError("INVALID_MANIFEST")
    if failure is not None:
        # Raised outside the handler so a caller's secret-bearing exception is never chained.
        raise DeviceIdentityError(str(failure)) from None
    assert manifest is not None
    return manifest


def provision(manifest: Manifest, registry: Registry, store: CredentialStore) -> Manifest:
    failure: DeviceIdentityError | None = None
    result: Manifest | None = None
    try:
        manifest.validate()
        # Serialise attempts per run so an overlapping attempt cannot roll back another's devices.
        with _run_lock(manifest.run_id):
            result = _provision_locked(manifest, registry, store)
    except DeviceIdentityError as error:
        failure = error
    if failure is not None:
        # Raised outside the handler so a caller's secret-bearing exception is never chained.
        raise DeviceIdentityError(str(failure)) from None
    if result is None:
        raise DeviceIdentityError("PROVISION_FAILED")
    return result


def _provision_locked(manifest: Manifest, registry: Registry, store: CredentialStore) -> Manifest:
    try:
        active = bool(registry.list_run(manifest.run_id) or store.run_references(manifest.run_id))
        failed = False
    except Exception:
        active, failed = False, True
    if failed:
        raise DeviceIdentityError("ACTIVE_RUN_CHECK_FAILED") from None
    if active:
        raise DeviceIdentityError("RUN_ALREADY_ACTIVE")
    created: list[DeviceIdentity] = []
    attempted: DeviceIdentity | None = None
    issued: list[DeviceIdentity] = []
    failed = False
    try:
        for identity in manifest.identities:
            attempted = identity
            registry.create(identity.device_id, manifest.run_id)
            attempted = None
            created.append(identity)
            reference = store.issue(identity.device_id, manifest.run_id)
            issued.append(
                DeviceIdentity(identity.device_id, identity.sensor_id, identity.home_id, reference)
            )
    except Exception:
        failed = True
    if failed:
        # Cleanup runs outside the handler so the original error is never chained.
        owner = _owner_of(registry, attempted.device_id) if attempted is not None else None
        if attempted is not None and owner == manifest.run_id:
            created.append(attempted)
        rollback = Manifest(
            manifest.run_id,
            manifest.credential_owner,
            tuple(created),
            approach=manifest.approach,
        )
        try:
            with _run_lock(rollback.run_id):
                _teardown_locked(
                    rollback,
                    registry,
                    store,
                    [i.credential_ref for i in issued],
                    full_run=False,
                )
            teardown_error = None
        except DeviceIdentityError as error:
            teardown_error = error
        if teardown_error is not None:
            raise DeviceIdentityError(str(teardown_error)) from None
        if owner is _UNKNOWN:
            raise DeviceIdentityError("PROVISION_ROLLBACK_INCOMPLETE") from None
        raise DeviceIdentityError("PROVISION_FAILED_ROLLED_BACK")
    return Manifest(
        manifest.run_id,
        manifest.credential_owner,
        tuple(issued),
        approach=manifest.approach,
    )


def rotate(manifest: Manifest, registry: Registry, store: CredentialStore) -> Manifest:
    """Issue a new credential per identity, then revoke the old ones (no downtime overlap).

    Old credentials stay valid until every new one is stored. Returns references only.

    Retry after ROTATION_REVOKE_FAILED or ROTATION_INCOMPLETE is unsupported: `rotate` on
    either manifest fails with ROTATION_STATE_MISMATCH. Recover by tearing down
    `DeviceIdentityError.new_manifest`.
    """
    failure: DeviceIdentityError | None = None
    result: Manifest | None = None
    try:
        manifest.validate()
        with _run_lock(manifest.run_id):
            result = _rotate_locked(manifest, registry, store)
    except DeviceIdentityError as error:
        failure = error
    if failure is not None:
        # Raised outside the handler so a caller's secret-bearing exception is never chained.
        raise DeviceIdentityError(str(failure), failure.new_manifest) from None
    if result is None:
        raise DeviceIdentityError("ROTATION_FAILED")
    return result


def _rotate_locked(manifest: Manifest, registry: Registry, store: CredentialStore) -> Manifest:
    run_id = manifest.run_id
    old = [i.credential_ref for i in manifest.identities]
    if not all(old) or len(set(old)) != len(old):
        raise DeviceIdentityError("ROTATION_REFERENCES_MISSING")
    try:
        owned = {i.device_id for i in manifest.identities}
        stored = set(store.run_references(run_id))
        precheck = (
            set(registry.list_run(run_id)) == owned
            and all(registry.run_of(d) == run_id for d in owned)
            and set(old) == stored
        )
    except Exception:
        raise DeviceIdentityError("ROTATION_CHECK_FAILED") from None
    if not precheck:
        raise DeviceIdentityError("ROTATION_STATE_MISMATCH")
    issued: list[DeviceIdentity] = []
    failed = False
    try:
        for identity in manifest.identities:
            reference = store.issue(identity.device_id, run_id)
            issued.append(
                DeviceIdentity(identity.device_id, identity.sensor_id, identity.home_id, reference)
            )
    except Exception:
        failed = True
    if failed:
        # Anything stored beyond the old set, including an uncertain write, is revoked.
        undo_errors = _revoke_all(store, run_id, keep=set(old))
        if undo_errors:
            raise DeviceIdentityError("ROTATION_ROLLBACK_INCOMPLETE") from None
        raise DeviceIdentityError("ROTATION_FAILED_OLD_KEPT") from None
    errors = 0
    for reference in old:
        try:
            store.revoke(reference)
        except Exception:
            errors += 1
    try:
        leftover = set(store.run_references(run_id)) != {i.credential_ref for i in issued}
    except Exception:
        errors += 1
        leftover = False
    new_manifest = Manifest(
        run_id,
        manifest.credential_owner,
        tuple(issued),
        approach=manifest.approach,
    )
    if errors:
        raise DeviceIdentityError(f"ROTATION_REVOKE_FAILED:{errors}", new_manifest)
    if leftover:
        raise DeviceIdentityError("ROTATION_INCOMPLETE", new_manifest)
    return new_manifest


def _revoke_all(store: CredentialStore, run_id: str, keep: set[str]) -> int:
    errors = 0
    try:
        extra = [r for r in store.run_references(run_id) if r not in keep]
    except Exception:
        return 1
    for reference in extra:
        try:
            store.revoke(reference)
        except Exception:
            errors += 1
    return errors


def teardown(
    manifest: Manifest,
    registry: Registry,
    store: CredentialStore,
    refs: Sequence[str] | None = None,
) -> TeardownReceipt:
    """Delete exactly the run's identities and credentials under the run lock (see below).

    Whole-run coverage is always enforced; partial cleanup is reserved for provisioning rollback.
    """
    failure: DeviceIdentityError | None = None
    receipt: TeardownReceipt | None = None
    try:
        manifest.validate()
        with _run_lock(manifest.run_id):
            receipt = _teardown_locked(manifest, registry, store, refs, full_run=True)
    except DeviceIdentityError as error:
        failure = error
    if failure is not None:
        # Raised outside the handler so a caller's secret-bearing exception is never chained.
        raise DeviceIdentityError(str(failure)) from None
    if receipt is None:
        raise DeviceIdentityError("TEARDOWN_FAILED")
    return receipt


def _teardown_locked(
    manifest: Manifest,
    registry: Registry,
    store: CredentialStore,
    refs: Sequence[str] | None,
    *,
    full_run: bool,
) -> TeardownReceipt:
    """Delete exactly the run's identities and credentials, then verify none remain.

    Adapter exceptions may carry secrets, so they are replaced by fixed error codes and the
    remaining cleanup still runs.
    """
    owned = {i.device_id for i in manifest.identities}
    explicit = [r for r in (refs if refs is not None else _refs(manifest)) if r]
    run_id = manifest.run_id
    present_owned: list[str] = []
    foreign: bool | None = False
    try:
        for device_id in sorted(owned):
            tag = registry.run_of(device_id)
            if tag not in (None, run_id):
                foreign = True
            elif tag == run_id:
                present_owned.append(device_id)
    except Exception:
        foreign = None
    if foreign is None:
        raise DeviceIdentityError("TEARDOWN_FAILED")
    if foreign:
        raise DeviceIdentityError("TEARDOWN_OWNERSHIP_MISMATCH")
    errors = 0
    try:
        discovered = list(store.run_references(run_id))
    except Exception:
        discovered = []
        errors += 1
    if full_run:
        try:
            uncovered = set(registry.list_run(run_id)) - owned
        except Exception:
            raise DeviceIdentityError("TEARDOWN_FAILED") from None
        if uncovered:
            raise DeviceIdentityError(f"TEARDOWN_MANIFEST_INCOMPLETE:{len(uncovered)}")
    # Only references the store attributes to this run are revoked; explicit ones cannot widen it.
    references = list(dict.fromkeys(r for r in explicit if r in set(discovered)))
    references += [r for r in discovered if r not in references]
    for device_id in sorted(owned):
        try:
            registry.delete(device_id, run_id)
        except Exception:
            errors += 1
    for reference in references:
        try:
            store.revoke(reference)
        except Exception:
            errors += 1
    remaining: list[str] = []
    leftover: list[str] = []
    try:
        listed = set(registry.list_run(run_id))
        remaining = sorted(listed if full_run else owned.intersection(listed))
        leftover = sorted(store.run_references(run_id))
    except Exception:
        errors += 1
    if errors:
        raise DeviceIdentityError(f"TEARDOWN_FAILED:{errors}")
    if remaining:
        raise DeviceIdentityError(f"TEARDOWN_INCOMPLETE:{len(remaining)}")
    if leftover:
        raise DeviceIdentityError("TEARDOWN_CREDENTIALS_REMAIN")
    return TeardownReceipt.verified(
        run_id=run_id,
        approach=manifest.approach,
        credential_owner=manifest.credential_owner,
        removed_device_ids=tuple(present_owned),
        revoked_credential_count=len(references),
    )


_UNKNOWN = object()


def _owner_of(registry: Registry, device_id: str) -> object:
    try:
        return registry.run_of(device_id)
    except Exception:
        return _UNKNOWN


def _refs(manifest: Manifest) -> list[str]:
    return [i.credential_ref for i in manifest.identities]
