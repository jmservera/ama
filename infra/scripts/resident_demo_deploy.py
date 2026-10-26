#!/usr/bin/env python3
"""Deploy ONLY the resident demo (identity, app, three scoped role assignments) in group ama.

Dry run by default: it runs an ARM what-if of infra/resident-demo.bicep and refuses unless every
actionable change is one of the six resident-owned resources below (the five resources and the
exact nested guard deployment resident-demo-scope; no other deployment is allowed). `--apply`
repeats that proof, then deploys. It never uses main.bicep or deploy.py, so it cannot restore the
API minimum of two replicas, the cron schedules or the event job, and it never touches the SQL
database, the environment, the registry or the vault beyond the two secret-scoped role assignments.

Needs: the two owner-written secrets already in the private vault, the resident SQL principal and
view already created, and a separate exact execution approval with a cleared budget check. Running
--apply is not an authority. Expiry is a UTC instant no later than 2026-11-01T00:00:00Z. Rollback is
a rerun with --no-ingress; stop conditions are in infra/README.md. No secret value is handled here.
"""

from __future__ import annotations

import argparse
import re
import sys
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import resident_demo_secrets as secrets_helper  # noqa: E402

setup = secrets_helper.setup
TEMPLATE = HERE.parent / "resident-demo.bicep"
APP = "ca-resident-demo"
GUARD = "resident-demo-scope"
IDENTITY = "id-resident-demo"
VAULT = "kv-cutovertest-rzsrg"
REGISTRY = "crcutovertestrzsrg"
SECRETS = ("resident-demo-password-verifier", "resident-demo-session-key")
IMAGE = re.compile(r"crcutovertestrzsrg\.azurecr\.io/[a-z0-9][a-z0-9._/-]*@sha256:[0-9a-f]{64}")
HOST = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]*\.database\.windows\.net")
DATABASE = re.compile(r"[A-Za-z0-9_-]{1,64}")
ACTIONABLE = {"Create", "Modify", "Deploy"}


class DeployError(ValueError):
    """Sanitized refusal."""


def allowed_ids(subscription: str) -> dict[str, str]:
    root = f"/subscriptions/{subscription.lower()}/resourcegroups/ama/providers/"
    return {
        "identity": root + "microsoft.managedidentity/userassignedidentities/" + IDENTITY.lower(),
        "app": root + "microsoft.app/containerapps/" + APP,
        "vault": root + "microsoft.keyvault/vaults/" + VAULT + "/secrets/",
        "registry": root + "microsoft.containerregistry/registries/" + REGISTRY,
        "guard": root + "microsoft.resources/deployments/" + GUARD,
    }


def check_changes(plan: Any, subscription: str) -> int:
    """Return the number of actionable changes, or raise unless all are resident-owned."""
    changes = plan.get("changes", plan.get("properties", {}).get("changes"))
    if plan.get("status") != "Succeeded" or not isinstance(changes, list):
        raise DeployError("What-if did not succeed; nothing was deployed.")
    ids = allowed_ids(subscription)
    marker = "/providers/microsoft.authorization/roleassignments/"
    actionable = 0
    for change in changes:
        kind = change.get("changeType")
        if kind in ("Ignore", "NoChange"):
            continue
        resource = str(change.get("resourceId", "")).lower()
        owned = resource in (ids["identity"], ids["app"], ids["guard"])
        if marker in resource:
            scope = resource.split(marker)[0]
            owned = scope == ids["registry"] or (
                scope.startswith(ids["vault"]) and scope[len(ids["vault"]) :] in SECRETS
            )
        if kind not in ACTIONABLE or not owned:
            raise DeployError(
                "What-if shows a change outside the resident-owned resources; nothing was deployed."
            )
        actionable += 1
    return actionable


def confirmation(subscription: str, expires: str, image: str, ingress: bool) -> str:
    digest = image.rsplit("sha256:", 1)[1][:12]
    return f"DEPLOY {subscription} {APP} {expires} {digest} ingress={'on' if ingress else 'off'}"


class QuietParser(argparse.ArgumentParser):
    def error(self, message: str) -> Any:
        self.exit(2, "Invalid arguments; see --help.\n")


def main(
    argv: list[str],
    interactive: bool,
    stdout: TextIO,
    stderr: TextIO,
    ask: Callable[[str], str] = input,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
    make_cli: Callable[[Path], Any] | None = None,
) -> int:
    parser = QuietParser(description=__doc__, prog="resident_demo_deploy.py")
    parser.add_argument("--subscription", required=True)
    parser.add_argument("--expires", required=True, help="ISO UTC ending in Z")
    parser.add_argument("--image", required=True, help="registry image by sha256 digest")
    parser.add_argument("--sql-server", required=True, help="existing SQL server FQDN")
    parser.add_argument("--sql-database", required=True)
    parser.add_argument("--no-ingress", action="store_true", help="rollback: remove ingress")
    parser.add_argument("--tenant-profile", type=Path, default=setup.PROFILE)
    parser.add_argument("--apply", action="store_true", help="deploy (default: what-if only)")
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit as stop:
        return int(stop.code or 0)
    try:
        if not secrets_helper.GUID.fullmatch(args.subscription):
            raise DeployError("Subscription must be a GUID.")
        if not (
            IMAGE.fullmatch(args.image)
            and HOST.fullmatch(args.sql_server)
            and DATABASE.fullmatch(args.sql_database)
        ):
            raise DeployError(
                "Image must be a digest in the fixed registry; SQL server/database are malformed."
            )
        if not interactive:
            raise DeployError("Run this in an interactive terminal; piped input is refused.")
        try:
            # Closing ingress is always safe, so rollback accepts an expired window; opening needs a live one.
            expires = secrets_helper.parse_expiry(
                args.expires, now(), require_future=not args.no_ingress
            )
        except secrets_helper.HelperError as error:
            raise DeployError(str(error)) from None
        cli = (make_cli or (lambda path: setup.Azure(path, body_directory=path)))(
            setup.private_path(args.tenant_profile, directory=True)
        )
        cli.subscription = args.subscription
        parameters = [
            f"image={args.image}",
            f"sqlServerFqdn={args.sql_server}",
            f"sqlDatabaseName={args.sql_database}",
            f"expiresAt={expires}",
            f"externalIngress={'false' if args.no_ingress else 'true'}",
        ]
        base = ["--template-file", str(TEMPLATE), "--parameters", *parameters]
        name = "resident-demo-" + uuid.uuid4().hex[:12]
        plan = cli.call(
            [
                "deployment",
                "group",
                "what-if",
                "-g",
                "ama",
                "--name",
                name,
                *base,
                "--no-pretty-print",
            ]
        )
        count = check_changes(plan, args.subscription)
        if not args.apply:
            print(
                f"Dry run complete: {count} resident-owned change(s), none elsewhere; "
                "nothing was deployed.",
                file=stdout,
            )
            return 0
        phrase = confirmation(args.subscription, expires, args.image, not args.no_ingress)
        print("To deploy, type exactly:\n" + phrase, file=stderr)
        if ask("Confirm: ").strip() != phrase:
            raise DeployError("Confirmation did not match; nothing was deployed.")
        secrets_helper.parse_expiry(args.expires, now(), require_future=not args.no_ingress)
        cli.call(["deployment", "group", "create", "-g", "ama", "--name", name, *base])
        app = cli.call(["containerapp", "show", "-g", "ama", "-n", APP])
        scale = app["properties"]["template"]["scale"]
        if scale.get("minReplicas") != 0 or scale.get("maxReplicas") != 1:
            raise DeployError("Deployed scale is not min 0 / max 1; stop and investigate.")
    except DeployError as error:
        print(f"Refused: {error}", file=stderr)
        return 1
    except setup.SetupError as error:
        print(f"Failed: {error}", file=stderr)
        return 1
    except setup.AzureError as error:
        print(f"Failed: Azure request error ({error.kind}).", file=stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Cancelled.", file=stderr)
        return 1
    except Exception:  # noqa: BLE001 - keep tracebacks out of operator logs
        print("Failed: unexpected error.", file=stderr)
        return 1
    print(f"Deployed {APP} (min 0, max 1, expires {expires}).", file=stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv, sys.stdin.isatty(), sys.stdout, sys.stderr))
