"""Refuse to start an application without its required Linux container controls."""

import os
import sys
from pathlib import Path


def verify_runtime() -> None:
    if os.getuid() != 10001 or os.getgid() != 10001:
        raise RuntimeError("UID and GID must both be 10001")
    if not os.statvfs("/").f_flag & os.ST_RDONLY:
        raise RuntimeError("root filesystem must be read-only (--read-only)")
    status = dict(line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines())
    for name in ("CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb"):
        if int(status[name].strip(), 16) != 0:
            raise RuntimeError(f"{name} must be zero (--cap-drop ALL)")
    if status["NoNewPrivs"].strip() != "1":
        raise RuntimeError("NoNewPrivs must be enabled (--security-opt no-new-privileges)")


def main() -> int:
    try:
        verify_runtime()
        if len(sys.argv) < 2:
            raise RuntimeError("application command is required")
        os.execvp(sys.argv[1], sys.argv[1:])
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"Container security contract failed: {error}", file=sys.stderr)
        return 78


if __name__ == "__main__":
    sys.exit(main())
