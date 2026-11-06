"""Dry-run-by-default tooling that plans per-home SYN- device identities (#185).

The default action only maps each consenting stock home to one `SYN-` device ID and prints
non-secret references. A live run needs a named credential owner and a Registry and
CredentialStore supplied by trusted code; this module ships none, so the command line cannot
touch Azure and creates nothing. Injected trusted adapters may store and revoke credentials;
the report then says so by outcome and never prints credential material.
"""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import sensor_stock

VERSION = "simulated-device-provision-v1"
_PLACEHOLDERS = frozenset({"tbc", "tbd", "todo", "n/a", "na", "none", "unknown", "unassigned"})
ACTIONS = ("provision", "teardown")
_CREDENTIALS = {
    ("dry-run", "provision"): "none created or stored; dry run only",
    ("dry-run", "teardown"): "none revoked; dry run only",
    ("applied", "provision"): "stored by the injected credential store; references only",
    ("applied", "teardown"): "revoked by the injected credential store; none remain",
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


def report(manifest: di.Manifest, action: str, mode: str) -> dict[str, object]:
    return {
        "version": VERSION,
        "mode": mode,
        "action": action,
        "run_id": manifest.run_id,
        "credential_owner": manifest.credential_owner,
        "owner_named": owner_named(manifest.credential_owner),
        "device_count": len(manifest.identities),
        "devices": [{"device_id": i.device_id, "home_id": i.home_id} for i in manifest.identities],
        "credentials": _CREDENTIALS[(mode, action)],
    }


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
    di.teardown(manifest, registry, store)
    return report(manifest, action, "applied")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan per-home SYN- device identities (dry run)")
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--homes", type=int, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--owner", default="unassigned")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--action", choices=ACTIONS, default="provision")
    parser.add_argument("--apply", action="store_true", help="live run; refused without adapters")
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.register, args.homes, args.run_id, args.owner, args.seed)
        body = run(manifest, args.action, args.apply)
    except (ProvisionError, di.DeviceIdentityError, ValueError, OSError) as error:
        code = (
            str(error)
            if isinstance(error, (ProvisionError, di.DeviceIdentityError))
            else "INVALID_INPUT"
        )
        print(f"refused: {code}", file=sys.stderr)
        return 2
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
