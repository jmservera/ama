"""Dry-run-by-default tooling that plans per-home SYN- device identities (#185).

The default action only maps each consenting stock home to one `SYN-` device ID and prints
non-secret references. A live run needs a named credential owner and a Registry and
CredentialStore: trusted code may inject them, or `--apply --hub-host` builds the keyless Hub
adapters (SAS enrolment, Hub-generated keys discarded, in-memory references). The `cycle` action
provisions then tears down in one process and reports the residual count. The report never
prints credential material.
"""

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import device_registry_azure as dra
from zava_forward.core.synthetic import live_provisioning as lp
from zava_forward.core.synthetic import privacy, sensor_stock

VERSION = "simulated-device-provision-v1"
DEVICE_IDENTITY_APPROACH = di.DEVICE_IDENTITY_APPROACH
CREDENTIAL_OWNER_ROLE = di.CREDENTIAL_OWNER_ROLE
DEFAULT_CREDENTIAL_OWNER = CREDENTIAL_OWNER_ROLE
teardown_simulated_identities = lp.teardown_simulated_identities
deprovision_simulated_devices = lp.deprovision_simulated_devices
_PLACEHOLDERS = frozenset({"tbc", "tbd", "todo", "n/a", "na", "none", "unknown", "unassigned"})
ACTIONS = ("provision", "teardown", "cycle")
_CREDENTIALS = {
    ("dry-run", "provision"): "none created or stored; dry run only",
    ("dry-run", "teardown"): "none revoked; dry run only",
    ("dry-run", "cycle"): "none created, stored or revoked; dry run only",
    ("applied", "provision"): "stored by the injected credential store; references only",
    ("applied", "teardown"): "revoked by the injected credential store; none remain",
    ("applied", "cycle"): "Hub-generated keys discarded on issue; references revoked; none remain",
}


class ProvisionError(RuntimeError):
    """Fixed-code refusal; never carries adapter or credential detail."""


def owner_named(owner: str) -> bool:
    value = owner.strip()
    return bool(value) and value.lower() not in _PLACEHOLDERS and not value.startswith("<")


def build_manifest(register: Path, homes: int, run_id: str, owner: str, seed: int) -> di.Manifest:
    selection = sensor_stock.read_register(register, homes)
    sensors = selection.sensors(seed)
    if not sensors:
        raise ProvisionError("NO_MONITORED_HOMES")
    return di.plan(run_id, owner, sensors)


def report(
    manifest: di.Manifest,
    action: str,
    mode: str,
    *,
    teardown_receipt: di.TeardownReceipt | None = None,
) -> dict[str, object]:
    if lp.contains_raw_secret(manifest.credential_owner):
        raise ProvisionError("CREDENTIAL_OWNER_SECRET_MATERIAL")
    if privacy.pattern_issues(manifest.credential_owner):
        raise ProvisionError("CREDENTIAL_OWNER_PERSONAL_DATA")
    body: dict[str, object] = {
        "source_type": "SYNTHETIC",
        "contains_real_data": False,
        "version": VERSION,
        "mode": mode,
        "action": action,
        "run_id": manifest.run_id,
        "approach": manifest.approach,
        "credential_owner": manifest.credential_owner,
        "owner_named": owner_named(manifest.credential_owner),
        "device_count": len(manifest.identities),
        "devices": [{"device_id": i.device_id, "home_id": i.home_id} for i in manifest.identities],
        "credentials": _CREDENTIALS[(mode, action)],
    }
    if teardown_receipt is not None:
        body["teardown_receipt"] = teardown_receipt.as_dict()
    return body


def run(
    manifest: di.Manifest,
    action: str,
    apply: bool,
    registry: di.Registry | None = None,
    store: di.CredentialStore | None = None,
) -> dict[str, object]:
    """Dry-run unless `apply` is set; a live run also needs a named owner and both adapters."""
    if action not in ACTIONS:
        raise ProvisionError("INVALID_ACTION")
    if not apply:
        return report(manifest, action, "dry-run")
    if not owner_named(manifest.credential_owner):
        raise ProvisionError("CREDENTIAL_OWNER_NOT_NAMED")
    if registry is None or store is None:
        raise ProvisionError("LIVE_ADAPTERS_NOT_CONFIGURED")
    if action == "provision":
        result = di.provision(manifest, registry, store)
        return report(result, action, "applied")
    if action == "cycle":
        di.provision(manifest, registry, store)
    receipt = di.teardown(manifest, registry, store)
    return report(manifest, action, "applied", teardown_receipt=receipt)


def hub_adapters(
    manifest: di.Manifest, hostname: str
) -> tuple[di.Registry, di.CredentialStore, Callable[[], None]]:
    """Keyless Hub registry (SAS enrolment, Hub keys discarded) plus an in-memory reference vault.

    Needs `azure-identity` and the `iothub` extra installed; neither is declared by this project.
    """
    try:
        from azure.identity import DefaultAzureCredential
    except ImportError:
        raise ProvisionError("ADAPTER_UNAVAILABLE") from None
    spec = dra.EnrollmentSpec(
        manifest.run_id,
        tuple(dra.SasEnrollment(i.device_id) for i in manifest.identities),
    )
    try:
        registry = dra.AzureIotHubRegistry(hostname, spec, credential=DefaultAzureCredential())
    except dra.RegistryError as error:
        raise ProvisionError(str(error)) from None
    return registry, lp.SymmetricSasCredentialStore(), registry.close


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan per-home SYN- device identities (dry run)")
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--homes", type=int, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--owner", default="unassigned")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--action", choices=ACTIONS, default="provision")
    parser.add_argument("--apply", action="store_true", help="live run; refused without adapters")
    parser.add_argument("--hub-host", help="IoT Hub host name; with --apply uses the Hub registry")
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.register, args.homes, args.run_id, args.owner, args.seed)
        if args.apply and args.hub_host:
            registry, store, close = hub_adapters(manifest, args.hub_host)
            try:
                body = run(manifest, args.action, True, registry, store)
                body["residual_in_hub"] = len(registry.list_run(manifest.run_id))
            finally:
                close()
        else:
            body = run(manifest, args.action, args.apply)
    except (
        ProvisionError,
        di.DeviceIdentityError,
        dra.RegistryError,
        ValueError,
        OSError,
    ) as error:
        code = (
            str(error)
            if isinstance(error, (ProvisionError, di.DeviceIdentityError, dra.RegistryError))
            else "INVALID_INPUT"
        )
        print(f"refused: {code}", file=sys.stderr)
        return 2
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
