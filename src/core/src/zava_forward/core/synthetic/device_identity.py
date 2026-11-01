"""Run-owned simulated IoT Hub device identities: provision, store credentials, tear down.

Individual enrolment with per-device X.509 (ADR 0003 decision 6). Credential material only ever
crosses the CredentialStore boundary; manifests, reprs and errors carry references, never secrets.
"""

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from zava_forward.core.synthetic import sensor_identity

VERSION = "simulated-device-identity-v1"
RUN_ID = re.compile(r"[a-z0-9][a-z0-9-]{2,31}")
SENSOR_ID = re.compile(r"[A-Z0-9][A-Z0-9_-]{0,19}")
MAX_DEVICES = 100


class DeviceIdentityError(RuntimeError):
    pass


class Registry(Protocol):
    def create(self, device_id: str, run_id: str) -> None: ...

    def delete(self, device_id: str) -> None:
        """Remove the identity; an absent identity is a no-op."""
        ...

    def list_run(self, run_id: str) -> Sequence[str]: ...


class CredentialStore(Protocol):
    def issue(self, device_id: str) -> str:
        """Issue and store a credential; return only its non-secret reference."""
        ...

    def revoke(self, reference: str) -> None: ...

    def references(self) -> Sequence[str]: ...


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
    issued: list[DeviceIdentity] = []
    try:
        for identity in manifest.identities:
            registry.create(identity.device_id, manifest.run_id)
            reference = store.issue(identity.device_id)
            issued.append(
                DeviceIdentity(identity.device_id, identity.sensor_id, identity.home_id, reference)
            )
    except Exception:
        rollback = Manifest(manifest.run_id, manifest.credential_owner, manifest.identities)
        teardown(rollback, registry, store, refs=[i.credential_ref for i in issued])
        raise DeviceIdentityError("PROVISION_FAILED_ROLLED_BACK") from None
    return Manifest(manifest.run_id, manifest.credential_owner, tuple(issued))


def teardown(
    manifest: Manifest,
    registry: Registry,
    store: CredentialStore,
    refs: Sequence[str] | None = None,
) -> None:
    """Delete exactly the manifest's identities and credentials, then verify none remain."""
    owned = {i.device_id for i in manifest.identities}
    for device_id in sorted(owned):
        registry.delete(device_id)
    for reference in refs if refs is not None else [i.credential_ref for i in manifest.identities]:
        if reference:
            store.revoke(reference)
    remaining = sorted(owned.intersection(registry.list_run(manifest.run_id)))
    if remaining:
        raise DeviceIdentityError(f"TEARDOWN_INCOMPLETE:{len(remaining)}")
    if any(
        reference in set(store.references())
        for reference in (i.credential_ref for i in manifest.identities)
        if reference
    ):
        raise DeviceIdentityError("TEARDOWN_CREDENTIALS_REMAIN")
