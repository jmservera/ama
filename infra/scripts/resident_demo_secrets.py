#!/usr/bin/env python3
"""Owner-local helper: store the resident demo verifier and session key in the private vault.

Dry run by default: it validates your inputs locally and reads only vault metadata; no secret value
leaves this process. `--apply` writes exactly two fixed secrets, resident-demo-password-verifier
and resident-demo-session-key, in ONE secure ARM deployment to kv-cutovertest-rzsrg after a
what-if proves two new secrets there, both expiring no later than 2026-10-26T12:00:00Z.

The verifier comes from a hidden prompt or an owner-only (mode 0600) file outside the repository;
make it with resident_demo_verifier.py. The session key is generated here at apply time and is
never printed. Nothing is accepted on the command line or in the environment.

Running --apply is not an authority. It still needs a separate exact write approval, cleared
budget and a proven private write path; Azure role assignments are the enforcing control. If a
write fails part way, nothing is cleaned up automatically: reconcile under a separate approval.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import importlib.util
import os
import re
import secrets
import stat
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import credential_arm  # noqa: E402

_spec = importlib.util.spec_from_file_location("setup_entra", HERE / "setup-entra.py")
assert _spec and _spec.loader
setup = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("setup_entra", setup)
_spec.loader.exec_module(setup)

from zava_forward.core.resident_showcase import PasswordVerifier, ShowcaseConfigError  # noqa: E402

MAX_EXPIRY = datetime(2026, 10, 26, 12, 0, tzinfo=UTC)
MAX_FILE_BYTES = 1024
GUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


class HelperError(ValueError):
    """Sanitized refusal; messages never carry secret material."""


def parse_expiry(value: str, now: datetime) -> str:
    if not value.endswith("Z"):
        raise HelperError("Expiry must be an ISO UTC time ending in Z.")
    try:
        moment = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        raise HelperError("Expiry is not a valid ISO UTC time.") from None
    if moment <= now:
        raise HelperError("Expiry is not in the future.")
    if moment > MAX_EXPIRY:
        raise HelperError("Expiry is later than the authority limit 2026-10-26T12:00:00Z.")
    return value


def read_private_file(path: Path) -> str:
    """Open once without following links, then check and read that same descriptor."""
    resolved = path.parent.resolve() / path.name
    if setup.REPO == resolved or setup.REPO in resolved.parents:
        raise HelperError("Keep the verifier file outside the repository.")
    try:
        descriptor = os.open(resolved, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except OSError:
        raise HelperError("The verifier file cannot be opened (missing or a link).") from None
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.geteuid()
            or stat.S_IMODE(info.st_mode) != 0o600
            or info.st_size > MAX_FILE_BYTES
        ):
            raise HelperError("The verifier file must be your own regular 0600 file, up to 1 KiB.")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            raw = stream.read(MAX_FILE_BYTES + 1)
    finally:
        os.close(descriptor)
    try:
        return raw.decode("ascii").strip()
    except UnicodeDecodeError:
        raise HelperError("The verifier file is not plain text.") from None


def confirmation(subscription: str, expires: str) -> str:
    return (
        f"WRITE {subscription} {credential_arm.RESIDENT_VAULT} "
        f"{credential_arm.RESIDENT_VERIFIER} {credential_arm.RESIDENT_SESSION_KEY} {expires}"
    )


class QuietParser(argparse.ArgumentParser):
    def error(self, message: str) -> Any:
        # Never echo argument text: a mistaken secret on the command line must not be printed.
        self.exit(2, "Invalid arguments; see --help. Secrets are never accepted as arguments.\n")


def main(
    argv: list[str],
    interactive: bool,
    stdout: TextIO,
    stderr: TextIO,
    prompt: Callable[[str], str] = getpass.getpass,
    ask: Callable[[str], str] = input,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
    make_cli: Callable[[Path], Any] | None = None,
) -> int:
    parser = QuietParser(description=__doc__, prog="resident_demo_secrets.py")
    parser.add_argument("--subscription", required=True, help="Azure subscription id")
    parser.add_argument("--expires", required=True, help="secret expiry, ISO UTC ending in Z")
    parser.add_argument("--tenant-profile", type=Path, default=setup.PROFILE)
    parser.add_argument("--verifier-file", type=Path, help="owner-only 0600 file with the verifier")
    parser.add_argument(
        "--apply", action="store_true", help="write the two secrets (default: dry run)"
    )
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit as stop:
        return int(stop.code or 0)
    try:
        if not GUID.fullmatch(args.subscription):
            raise HelperError("Subscription must be a GUID.")
        if not interactive:
            raise HelperError("Run this in an interactive terminal; piped input is refused.")
        expires = parse_expiry(args.expires, now())
        spec = (
            read_private_file(args.verifier_file)
            if args.verifier_file
            else prompt("Verifier from resident_demo_verifier.py (hidden): ")
        )
        try:
            PasswordVerifier(spec.strip())
        except ShowcaseConfigError:
            raise HelperError(
                "That is not a well formed scrypt verifier; nothing was sent."
            ) from None
        spec = spec.strip()
        profile = setup.private_path(args.tenant_profile, directory=True)
        cli = (make_cli or (lambda path: setup.Azure(path, body_directory=path)))(profile)
        cli.subscription = args.subscription
        app = {
            "id": f"/subscriptions/{args.subscription}/resourceGroups/ama"
            "/providers/Microsoft.Resources/resident-demo"
        }
        credential_arm.preflight(cli, app, credential_arm.RESIDENT_VAULT)
        if not args.apply:
            print(
                "Dry run complete: inputs valid, vault metadata checked, nothing written.",
                file=stdout,
            )
            return 0
        phrase = confirmation(args.subscription, expires)
        print("To write, type exactly:\n" + phrase, file=stderr)
        if ask("Confirm: ").strip() != phrase:
            raise HelperError("Confirmation did not match; nothing was written.")
        expires = parse_expiry(args.expires, now())
        key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
        references = credential_arm.store_resident_demo(cli, app, spec, key, expires)
    except HelperError as error:
        print(f"Refused: {error}", file=stderr)
        return 1
    except (credential_arm.CredentialError, setup.SetupError) as error:
        print(f"Failed: {error}", file=stderr)
        return 1
    except setup.AzureError as error:
        print(f"Failed: Azure request error ({error.kind}); no value was printed.", file=stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Cancelled.", file=stderr)
        return 1
    except Exception:  # noqa: BLE001 - privacy boundary: no traceback may carry a secret
        print("Failed: unexpected error; no value was printed.", file=stderr)
        return 1
    for name, uri in references.items():
        print(f"stored {name} -> {uri} (expires {expires})", file=stdout)
    return 0


if __name__ == "__main__":
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, ValueError, OSError):
        pass
    sys.exit(main(sys.argv, sys.stdin.isatty(), sys.stdout, sys.stderr))
