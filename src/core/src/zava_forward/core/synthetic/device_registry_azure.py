"""Keyless Azure IoT Hub identity-registry adapter for the injected `Registry` protocol (#185).

Source only and default off: importing this module, building the adapter, a dry run or `close()`
never imports the SDK, acquires a token or opens a connection. Authentication is an injected
Microsoft Entra token credential (the SDK's `from_token_credential`); there is no connection
string, service key, ambient credential discovery or fallback. The adapter creates identities
DISABLED with an exact run marker and public X.509 thumbprints only. Issuing, storing, rotating
or activating a credential is out of scope and stays with the credential lifecycle (#185).

Every write is conditional. Create sends `If-None-Match: *`, so an existing identity conflicts and
is never adopted or overwritten. Delete sends the exact, non-wildcard ETag of an ownership
snapshot, so a recreated, modified or foreign identity is refused. Errors carry fixed codes only.
"""

import importlib
import re
import threading
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from types import ModuleType, TracebackType
from typing import Any, Protocol

from zava_forward.core.synthetic import device_identity

HUB_HOST = re.compile(r"[a-z0-9][a-z0-9-]{1,48}[a-z0-9]\.azure-devices\.net")
DEVICE_ID = re.compile("SYN-" + device_identity.SENSOR_ID.pattern)
THUMBPRINT = re.compile(r"[0-9A-F]{40}|[0-9A-F]{64}")
ETAG = re.compile(r"[A-Za-z0-9+/=_.:-]{1,64}")
MARKER_PREFIX = "zava-forward:sim-run:v1:"
NOT_RUN_OWNED = "(not-run-owned)"
MAX_LIST = 1000
_DENIED = (401, 403)
_ACCEPTED_CREATE = (200, 201)
_ACCEPTED_DELETE = (200, 204, 404)


class RegistryError(RuntimeError):
    """Fixed-code error. `readback` reports a safe reread after an uncertain write."""

    def __init__(self, code: str, readback: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.readback = readback


class TokenCredential(Protocol):
    def get_token(self, *scopes: str, **kwargs: Any) -> Any: ...


@dataclass(frozen=True)
class X509Enrollment:
    """Public thumbprints for one known device; certificate issuance is not implied."""

    device_id: str
    primary_thumbprint: str
    secondary_thumbprint: str | None = None

    def __post_init__(self) -> None:
        secondary = self.secondary_thumbprint
        valid = (
            isinstance(self.device_id, str)
            and DEVICE_ID.fullmatch(self.device_id) is not None
            and isinstance(self.primary_thumbprint, str)
            and THUMBPRINT.fullmatch(self.primary_thumbprint) is not None
            and (
                secondary is None
                or (
                    isinstance(secondary, str)
                    and THUMBPRINT.fullmatch(secondary) is not None
                    and secondary != self.primary_thumbprint
                )
            )
        )
        if not valid:
            raise RegistryError("INVALID_ENROLLMENT")


@dataclass(frozen=True)
class EnrollmentSpec:
    """Finite enrolment for exactly one run; anything outside it is refused before SDK use."""

    run_id: str
    enrollments: tuple[X509Enrollment, ...]
    _by_id: dict[str, X509Enrollment] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        items = self.enrollments
        valid = (
            isinstance(self.run_id, str)
            and device_identity.RUN_ID.fullmatch(self.run_id) is not None
            and isinstance(items, tuple)
            and 1 <= len(items) <= device_identity.MAX_DEVICES
            and all(isinstance(item, X509Enrollment) for item in items)
        )
        if valid:
            ids = [item.device_id for item in items]
            prints = [
                p
                for item in items
                for p in (item.primary_thumbprint, item.secondary_thumbprint)
                if p
            ]
            valid = len(set(ids)) == len(ids) and len(set(prints)) == len(prints)
        if not valid:
            raise RegistryError("INVALID_ENROLLMENT")
        object.__setattr__(self, "_by_id", {item.device_id: item for item in items})

    @property
    def marker(self) -> str:
        return MARKER_PREFIX + self.run_id

    def enrollment(self, device_id: str) -> X509Enrollment | None:
        return self._by_id.get(device_id)


@dataclass(frozen=True)
class _Outcome:
    value: Any = None
    failed: bool = False
    status: int | None = None


@dataclass(frozen=True)
class _Read:
    state: str
    device: Any = None


def _status(error: BaseException) -> int | None:
    status = getattr(getattr(error, "response", None), "status_code", None)
    return status if isinstance(status, int) and not isinstance(status, bool) else None


def _owner(reason: object) -> str:
    """Exact supported marker only; the SYN prefix or enrolment membership is not ownership."""
    if isinstance(reason, str) and reason.startswith(MARKER_PREFIX):
        run_id = reason[len(MARKER_PREFIX) :]
        if device_identity.RUN_ID.fullmatch(run_id):
            return run_id
    return NOT_RUN_OWNED


def _load(name: str) -> ModuleType | None:
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def _rejection(status: int | None) -> str | None:
    if status in _DENIED:
        return "ACCESS_DENIED"
    if status is not None and 400 <= status < 500 and status != 408:
        return "REJECTED"
    return None


class AzureIotHubRegistry:
    """`device_identity.Registry` over the Azure IoT Hub identity registry, one run per adapter.

    Exactly one of `credential` (a trusted token credential; the adapter builds and owns the SDK
    manager at first use) or `client` (a trusted pre-built `IoTHubRegistryManager`, never closed
    here) must be supplied. Run one process per run ID: `device_identity` serialises a run only
    inside its process.
    """

    def __init__(
        self,
        hostname: str,
        spec: EnrollmentSpec,
        *,
        credential: TokenCredential | None = None,
        client: Any = None,
        timeout: float = 30.0,
    ) -> None:
        valid = (
            isinstance(hostname, str)
            and HUB_HOST.fullmatch(hostname) is not None
            and isinstance(spec, EnrollmentSpec)
            and (credential is None) != (client is None)
            and (credential is None or callable(getattr(credential, "get_token", None)))
            and isinstance(timeout, (int, float))
            and not isinstance(timeout, bool)
            and 1 <= timeout <= 60
        )
        if not valid:
            raise RegistryError("INVALID_CONFIGURATION")
        self._hostname = hostname
        self._spec = spec
        self._credential = credential
        self._timeout = float(timeout)
        self._manager: Any = client
        self._owned = False
        self._bound = False
        self._closed = False
        self._lock = threading.Lock()

    def __repr__(self) -> str:
        return f"AzureIotHubRegistry({self._hostname!r}, run={self._spec.run_id!r})"

    def __enter__(self) -> "AzureIotHubRegistry":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """Close only a manager this adapter built; an injected client is left to its owner."""
        with self._lock:
            manager, owned, already = self._manager, self._owned, self._closed
            self._closed, self._manager, self._owned = True, None, False
        if already or not owned or manager is None:
            return
        amqp = getattr(manager, "amqp_svc_client", None)
        for close in (
            getattr(amqp, "disconnect_sync", None),
            getattr(manager.protocol, "close", None),
        ):
            try:
                if callable(close):
                    close()
            except Exception:
                pass

    def create(self, device_id: str, run_id: str) -> None:
        self._run(run_id)
        enrollment = self._device(device_id)
        models = self._models()
        thumbprint = models.X509Thumbprint(
            primary_thumbprint=enrollment.primary_thumbprint,
            secondary_thumbprint=enrollment.secondary_thumbprint,
        )
        identity = models.Device(
            device_id=device_id,
            status="disabled",
            status_reason=self._spec.marker,
            authentication=models.AuthenticationMechanism(
                type="selfSigned", x509_thumbprint=thumbprint
            ),
            capabilities=models.DeviceCapabilities(iot_edge=False),
        )
        outcome = self._invoke(
            lambda devices: devices.create_or_update_identity(
                device_id, identity, custom_headers={"If-None-Match": "*"}
            )
        )
        if not outcome.failed or outcome.status in _ACCEPTED_CREATE:
            return
        if outcome.status in (409, 412):
            raise RegistryError("IDENTITY_CONFLICT")
        code = _rejection(outcome.status)
        if code is not None:
            raise RegistryError(code)
        raise RegistryError("WRITE_OUTCOME_UNKNOWN", self._readback(device_id))

    def run_of(self, device_id: str) -> str | None:
        self._device(device_id)
        read = self._read(device_id)
        if read.state == "absent":
            return None
        if read.state == "present":
            return _owner(getattr(read.device, "status_reason", None))
        raise RegistryError("ACCESS_DENIED" if read.state == "denied" else "UNAVAILABLE")

    def delete(self, device_id: str, run_id: str) -> None:
        self._run(run_id)
        self._device(device_id)
        read = self._read(device_id)
        if read.state == "absent":
            return
        if read.state != "present":
            raise RegistryError("ACCESS_DENIED" if read.state == "denied" else "UNAVAILABLE")
        device = read.device
        if _owner(getattr(device, "status_reason", None)) != run_id:
            return
        etag = getattr(device, "etag", None)
        generation = getattr(device, "generation_id", None)
        exact = (
            isinstance(etag, str)
            and ETAG.fullmatch(etag) is not None
            and isinstance(generation, str)
            and generation != ""
        )
        if not exact:
            raise RegistryError("OWNERSHIP_UNCERTAIN")
        outcome = self._invoke(
            lambda devices: devices.delete_identity(device_id, if_match=f'"{etag}"')
        )
        if not outcome.failed or outcome.status in _ACCEPTED_DELETE:
            return
        if outcome.status == 412:
            raise RegistryError("PRECONDITION_FAILED")
        code = _rejection(outcome.status)
        if code is not None:
            raise RegistryError(code)
        readback = self._readback(device_id)
        if readback != "absent":
            raise RegistryError("DELETE_OUTCOME_UNKNOWN", readback)

    def list_run(self, run_id: str) -> Sequence[str]:
        """Every enrolled-or-listed identity carrying the run marker, or an explicit refusal."""
        self._run(run_id)
        outcome = self._invoke(lambda devices: devices.get_devices(top=MAX_LIST))
        if outcome.failed:
            raise RegistryError("ACCESS_DENIED" if outcome.status in _DENIED else "UNAVAILABLE")
        listed = outcome.value
        if not isinstance(listed, list):
            raise RegistryError("UNAVAILABLE")
        if len(listed) >= MAX_LIST:
            raise RegistryError("LIST_INCOMPLETE")
        found: set[str] = set()
        for item in listed:
            device_id = getattr(item, "device_id", None)
            reason = getattr(item, "status_reason", None)
            if not isinstance(device_id, str):
                raise RegistryError("UNAVAILABLE")
            if reason == self._spec.marker:
                found.add(device_id)
            elif not isinstance(reason, str) and self._spec.enrollment(device_id) is not None:
                # A payload that omits the marker cannot prove absence of ownership.
                read = self._read(device_id)
                if read.state == "present":
                    if _owner(getattr(read.device, "status_reason", None)) == run_id:
                        found.add(device_id)
                elif read.state != "absent":
                    raise RegistryError(
                        "ACCESS_DENIED" if read.state == "denied" else "UNAVAILABLE"
                    )
        return sorted(found)

    def _run(self, run_id: str) -> None:
        if run_id != self._spec.run_id:
            raise RegistryError("NOT_ENROLLED")

    def _device(self, device_id: str) -> X509Enrollment:
        enrollment = self._spec.enrollment(device_id) if isinstance(device_id, str) else None
        if enrollment is None:
            raise RegistryError("NOT_ENROLLED")
        return enrollment

    def _models(self) -> Any:
        models = _load("azure.iot.hub.protocol.models")
        if models is None:
            raise RegistryError("SDK_MISSING")
        return models

    def _devices(self) -> Any:
        with self._lock:
            failure = "CLOSED" if self._closed else (None if self._bound else self._prepare())
            manager = self._manager
        if failure is not None:
            raise RegistryError(failure)
        return manager.protocol.devices

    def _prepare(self) -> str | None:
        """Build (credential path) and bind the manager once; returns a failure code or None."""
        manager = self._manager
        owned = False
        if manager is None:
            sdk = _load("azure.iot.hub")
            if sdk is None:
                return "SDK_MISSING"
            try:
                manager = sdk.IoTHubRegistryManager.from_token_credential(
                    self._hostname, self._credential
                )
            except Exception:
                return "CREDENTIAL_UNAVAILABLE"
            owned = True
        try:
            config = manager.protocol.config
            config.retry_policy.retries = 0
            config.connection.timeout = self._timeout
        except Exception:
            return "SDK_INCOMPATIBLE"
        self._manager, self._owned, self._bound = manager, owned, True
        return None

    def _invoke(self, call: Callable[[Any], Any]) -> _Outcome:
        devices = self._devices()
        try:
            return _Outcome(value=call(devices))
        except Exception as error:
            return _Outcome(failed=True, status=_status(error))

    def _read(self, device_id: str) -> _Read:
        outcome = self._invoke(lambda devices: devices.get_identity(device_id))
        if not outcome.failed:
            if getattr(outcome.value, "device_id", None) == device_id:
                return _Read("present", outcome.value)
            return _Read("unreadable")
        if outcome.status == 404:
            return _Read("absent")
        return _Read("denied" if outcome.status in _DENIED else "unreadable")

    def _readback(self, device_id: str) -> str:
        """One safe reread; never raises and never writes."""
        try:
            read = self._read(device_id)
        except RegistryError:
            return "unreadable"
        if read.state == "absent":
            return "absent"
        if read.state == "present":
            owner = _owner(getattr(read.device, "status_reason", None))
            return "owned" if owner == self._spec.run_id else "foreign"
        return "unreadable"
