"""Run-owned simulated IoT Hub device identities: provision, store credentials, tear down.

Individual enrolment with per-device X.509 (ADR 0003 decision 6). Credential material only ever
crosses the CredentialStore boundary; manifests, reprs and errors carry references, never secrets.
"""

import re
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from zava_forward.core.synthetic import sensor_identity

VERSION = "simulated-device-identity-v1"
RUN_ID = re.compile(r"[a-z0-9][a-z0-9-]{2,31}")
SENSOR_ID = re.compile(r"[A-Z0-9][A-Z0-9_-]{0,19}")
MAX_DEVICES = 100
_LOCKS: dict[str, threading.RLock] = {}
_LOCKS_GUARD = threading.Lock()


def _run_lock(run_id: str) -> threading.RLock:
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(run_id, threading.RLock())


class DeviceIdentityError(RuntimeError):
    pass


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


@dataclass(frozen=True)
class Manifest:
    run_id: str
    credential_owner: str
    identities: tuple[DeviceIdentity, ...]

    def validate(self) -> None:
        if not RUN_ID.fullmatch(self.run_id) or not self.credential_owner.strip():
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


def plan(run_id: str, credential_owner: str, sensors: Sequence[Mapping[str, object]]) -> Manifest:
    """Map `Selection.sensors()` output to one identity per stock home; no credentials yet."""
    identities = tuple(
        DeviceIdentity("SYN-" + str(s["sensor_id"]), str(s["sensor_id"]), str(s["home_id"]))
        for s in sensors
    )
    manifest = Manifest(run_id, credential_owner, identities)
    manifest.validate()
    return manifest


def provision(manifest: Manifest, registry: Registry, store: CredentialStore) -> Manifest:
    manifest.validate()
    # Serialise attempts per run so an overlapping attempt cannot roll back another's devices.
    with _run_lock(manifest.run_id):
        return _provision_locked(manifest, registry, store)


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
        rollback = Manifest(manifest.run_id, manifest.credential_owner, tuple(created))
        try:
            teardown(rollback, registry, store, refs=[i.credential_ref for i in issued])
            teardown_error = None
        except DeviceIdentityError as error:
            teardown_error = error
        if teardown_error is not None:
            raise DeviceIdentityError(str(teardown_error)) from None
        if owner is _UNKNOWN:
            raise DeviceIdentityError("PROVISION_ROLLBACK_INCOMPLETE") from None
        raise DeviceIdentityError("PROVISION_FAILED_ROLLED_BACK")
    return Manifest(manifest.run_id, manifest.credential_owner, tuple(issued))


def teardown(
    manifest: Manifest,
    registry: Registry,
    store: CredentialStore,
    refs: Sequence[str] | None = None,
) -> None:
    """Delete exactly the run's identities and credentials under the run lock (see below)."""
    with _run_lock(manifest.run_id):
        _teardown_locked(manifest, registry, store, refs)


def _teardown_locked(
    manifest: Manifest,
    registry: Registry,
    store: CredentialStore,
    refs: Sequence[str] | None,
) -> None:
    """Delete exactly the run's identities and credentials, then verify none remain.

    Adapter exceptions may carry secrets, so they are replaced by fixed error codes and the
    remaining cleanup still runs.
    """
    owned = {i.device_id for i in manifest.identities}
    explicit = [r for r in (refs if refs is not None else _refs(manifest)) if r]
    full_run = refs is None
    run_id = manifest.run_id
    try:
        foreign = any(registry.run_of(d) not in (None, run_id) for d in sorted(owned))
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
        remaining = sorted(owned.intersection(registry.list_run(run_id)))
        leftover = sorted(set(references).intersection(store.run_references(run_id)))
    except Exception:
        errors += 1
    if errors:
        raise DeviceIdentityError(f"TEARDOWN_FAILED:{errors}")
    if remaining:
        raise DeviceIdentityError(f"TEARDOWN_INCOMPLETE:{len(remaining)}")
    if leftover:
        raise DeviceIdentityError("TEARDOWN_CREDENTIALS_REMAIN")


_UNKNOWN = object()


def _owner_of(registry: Registry, device_id: str) -> object:
    try:
        return registry.run_of(device_id)
    except Exception:
        return _UNKNOWN


def _refs(manifest: Manifest) -> list[str]:
    return [i.credential_ref for i in manifest.identities]
