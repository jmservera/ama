#!/usr/bin/env python3
"""Offline helper: turn the owner's chosen demo password into a scrypt verifier.

Run it yourself, on a machine you control, in an interactive terminal. It reads the password with
a hidden prompt (twice), prints ONLY the verifier on standard output and keeps no file. It takes no
arguments and refuses piped input, so the password cannot arrive in a command line, environment
variable, history or pipe. It does not claim memory or swap safety: the plaintext exists briefly
in this process. Keep the verifier in a password manager or an owner-only local file, never in
chat or git. Nothing here generates a password or contacts Azure.
"""

import getpass
import sys
from collections.abc import Callable
from typing import TextIO

from zava_forward.core.resident_showcase_verifier import build_verifier

GUIDE = (
    "The verifier is derived from your password. Treat it as sensitive: keep it in a "
    "password manager or an owner-only local file. Do not paste it into chat or commit it."
)


def main(
    argv: list[str],
    interactive: bool,
    stdout: TextIO,
    stderr: TextIO,
    prompt: Callable[[str], str] = getpass.getpass,
) -> int:
    if len(argv) > 1:
        print("This tool takes no arguments.", file=stderr)
        return 2
    if not interactive:
        print(
            "Run this in an interactive terminal; piped input is refused.", file=stderr
        )
        return 2
    try:
        first = prompt("Demo password (hidden): ")
        if prompt("Repeat it (hidden): ") != first:
            print("The two entries differ.", file=stderr)
            return 1
        verifier = build_verifier(first)
    except ValueError as error:
        print(f"Rejected: {error}", file=stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Cancelled.", file=stderr)
        return 1
    except Exception:  # noqa: BLE001 - privacy boundary: no traceback may carry the password
        print("Could not build the verifier.", file=stderr)
        return 1
    print(verifier, file=stdout)
    print(GUIDE, file=stderr)
    return 0


if __name__ == "__main__":
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, ValueError, OSError):
        pass
    sys.exit(main(sys.argv, sys.stdin.isatty(), sys.stdout, sys.stderr))
