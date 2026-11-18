"""In-process container runtime hardening guard for deployed Container Apps and Jobs.

Azure Container Apps ARM schemas (`2025-07-01`) omit Kubernetes `securityContext` fields and its
hypervisor guest neither sets `ST_RDONLY` on `/` nor clears `CapBnd`. When `ZF_CONTAINER_HARDENING`
is `"enforced"` in deployed workloads, this pure-stdlib guard enforces:
1. Non-root execution (`UID == EUID == 10001` and `GID == EGID == 10001`, never `0`).
2. Restrictive process file creation mask (`umask 0o077`) and Python bytecode write suppression.
3. Linux `prctl(PR_SET_NO_NEW_PRIVS, 1)` plus `/proc/self/status` verification that
   `NoNewPrivs == 1` and `CapInh == CapPrm == CapEff == CapAmb == 0`.
4. Read-only / DAC-immutable root (`/`) and application (`/app`) paths rejecting file creation.
5. Bounded ephemeral scratch directories (`TMPDIR`/`/tmp` and `ZF_STATE` when configured) accepting
   file creation and deletion with safe directory permissions.
"""

from __future__ import annotations

import ctypes
import errno
import os
import secrets
import stat
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

HARDENING_ENV = "ZF_CONTAINER_HARDENING"
HARDENING_OFF = "off"
HARDENING_ENFORCED = "enforced"
EXPECTED_UID = 10001
EXPECTED_GID = 10001
PR_SET_NO_NEW_PRIVS = 38
DEFAULT_IMMUTABLE_PATHS: tuple[Path, ...] = (Path("/"), Path("/app"))
_ZERO_CAPABILITY_KEYS: tuple[str, ...] = ("CapInh", "CapPrm", "CapEff", "CapAmb")


class ContainerHardeningError(RuntimeError):
    """Raised when a deployed container process violates a required hardening invariant."""


@dataclass(frozen=True)
class HardeningReport:
    """Structured result of container runtime hardening verification."""

    enforced: bool
    uid: int
    euid: int
    gid: int
    egid: int
    no_new_privs: int | None
    immutable_paths: tuple[str, ...]
    writable_paths: tuple[str, ...]


def _parse_proc_status(status_text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw_line in status_text.splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _set_linux_no_new_privs() -> int:
    for soname in ("libc.so.6", None):
        try:
            libc = ctypes.CDLL(soname, use_errno=True)
        except OSError:
            continue
        prctl = getattr(libc, "prctl", None)
        if prctl is None:
            continue
        prctl.argtypes = [
            ctypes.c_int,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.c_ulong,
        ]
        prctl.restype = ctypes.c_int
        result: int = prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)
        return result
    raise ContainerHardeningError("Unable to locate libc prctl for PR_SET_NO_NEW_PRIVS.")


def _probe_immutable_directory(path: Path) -> None:
    try:
        st = path.stat()
    except OSError as exc:
        raise ContainerHardeningError(
            f"Immutable container path {path} is unavailable (errno={exc.errno})."
        ) from None
    if not stat.S_ISDIR(st.st_mode):
        raise ContainerHardeningError(f"Immutable container path {path} is not a directory.")

    probe = path / f".zf-ro-probe-{secrets.token_hex(8)}"
    try:
        fd = os.open(probe, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError as exc:
        if exc.errno in (errno.EROFS, errno.EACCES, errno.EPERM):
            return
        raise ContainerHardeningError(
            f"Unexpected filesystem probe failure on {path} (errno={exc.errno})."
        ) from None

    try:
        os.close(fd)
    finally:
        try:
            os.unlink(probe)
        except OSError:
            pass
    raise ContainerHardeningError(
        f"Container path {path} accepted writes; read-only or root-owned immutability is required."
    )


def _probe_writable_directory(path: Path) -> None:
    try:
        st = path.stat()
    except OSError as exc:
        raise ContainerHardeningError(
            f"Scratch directory {path} is unavailable (errno={exc.errno})."
        ) from None
    if not stat.S_ISDIR(st.st_mode):
        raise ContainerHardeningError(f"Scratch directory {path} is not a directory.")

    mode = stat.S_IMODE(st.st_mode)
    if (mode & stat.S_IWOTH) and not (mode & stat.S_ISVTX):
        raise ContainerHardeningError(
            f"Scratch directory {path} is world-writable without sticky bit."
        )

    probe = path / f".zf-rw-probe-{secrets.token_hex(8)}"
    try:
        fd = os.open(probe, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            os.write(fd, b"ok")
        finally:
            os.close(fd)
        os.unlink(probe)
    except OSError as exc:
        raise ContainerHardeningError(
            f"Scratch directory {path} is not writable (errno={exc.errno})."
        ) from None


def enforce_container_hardening(
    *,
    expected_uid: int = EXPECTED_UID,
    expected_gid: int = EXPECTED_GID,
    uid_getter: Callable[[], int] = os.getuid,
    euid_getter: Callable[[], int] = os.geteuid,
    gid_getter: Callable[[], int] = os.getgid,
    egid_getter: Callable[[], int] = os.getegid,
    umask_fn: Callable[[int], int] = os.umask,
    dont_write_bytecode: bool | None = None,
    bytecode_env: str | None = None,
    platform: str | None = None,
    prctl_fn: Callable[[], int] | None = None,
    proc_status_text: str | None = None,
    proc_status_path: Path = Path("/proc/self/status"),
    immutable_paths: Sequence[Path] = DEFAULT_IMMUTABLE_PATHS,
    writable_paths: Sequence[Path] = (Path("/tmp"),),
) -> HardeningReport:
    """Enforce deployed container runtime hardening invariants, failing closed on any violation."""
    uid, euid = uid_getter(), euid_getter()
    gid, egid = gid_getter(), egid_getter()
    if 0 in (uid, euid, gid, egid):
        raise ContainerHardeningError("Container hardening requires non-root UID and GID.")
    if uid != expected_uid or euid != expected_uid or gid != expected_gid or egid != expected_gid:
        raise ContainerHardeningError(
            f"Container hardening requires UID:GID {expected_uid}:{expected_gid} "
            f"(got {uid}:{gid}, effective {euid}:{egid})."
        )

    umask_fn(0o077)

    bytecode_disabled = (
        sys.dont_write_bytecode if dont_write_bytecode is None else dont_write_bytecode
    )
    if not bytecode_disabled and bytecode_env != "1":
        raise ContainerHardeningError(
            "Container hardening requires Python bytecode writes to be disabled "
            "(PYTHONDONTWRITEBYTECODE=1 or -B)."
        )

    active_platform = sys.platform if platform is None else platform
    no_new_privs: int | None = None
    if active_platform.startswith("linux"):
        apply_prctl = _set_linux_no_new_privs if prctl_fn is None else prctl_fn
        if apply_prctl() != 0:
            raise ContainerHardeningError("Failed to set Linux PR_SET_NO_NEW_PRIVS.")
        if proc_status_text is None:
            try:
                raw_status = proc_status_path.read_text(encoding="utf-8")
            except OSError:
                raise ContainerHardeningError(
                    "Unable to read /proc/self/status for capability verification."
                ) from None
        else:
            raw_status = proc_status_text
        fields = _parse_proc_status(raw_status)
        try:
            nnp_value = int(fields.get("NoNewPrivs", ""))
        except ValueError:
            nnp_value = -1
        if nnp_value != 1:
            raise ContainerHardeningError("Linux NoNewPrivs is not active.")
        no_new_privs = nnp_value
        for cap_key in _ZERO_CAPABILITY_KEYS:
            raw_cap = fields.get(cap_key)
            if raw_cap is None:
                raise ContainerHardeningError(
                    f"Missing {cap_key} in /proc/self/status capability check."
                )
            try:
                cap_mask = int(raw_cap, 16)
            except ValueError:
                raise ContainerHardeningError(
                    f"Malformed {cap_key} mask in /proc/self/status."
                ) from None
            if cap_mask != 0:
                raise ContainerHardeningError(
                    f"Linux capability mask {cap_key} must be zero (dropped capabilities)."
                )

    if not immutable_paths:
        raise ContainerHardeningError("At least one immutable path must be verified.")
    for immutable in immutable_paths:
        _probe_immutable_directory(Path(immutable))

    if not writable_paths:
        raise ContainerHardeningError("At least one writable scratch path must be verified.")
    for writable in writable_paths:
        _probe_writable_directory(Path(writable))

    return HardeningReport(
        enforced=True,
        uid=uid,
        euid=euid,
        gid=gid,
        egid=egid,
        no_new_privs=no_new_privs,
        immutable_paths=tuple(str(p) for p in immutable_paths),
        writable_paths=tuple(str(p) for p in writable_paths),
    )


def enforce_from_env(env: Mapping[str, str] | None = None) -> HardeningReport:
    """Enforce container hardening when `ZF_CONTAINER_HARDENING=enforced`; no-op when unset/off."""
    active_env = os.environ if env is None else env
    mode = active_env.get(HARDENING_ENV, "").strip().lower()
    if mode in ("", HARDENING_OFF):
        return HardeningReport(
            enforced=False,
            uid=os.getuid(),
            euid=os.geteuid(),
            gid=os.getgid(),
            egid=os.getegid(),
            no_new_privs=None,
            immutable_paths=(),
            writable_paths=(),
        )
    if mode != HARDENING_ENFORCED:
        raise ContainerHardeningError(
            "Invalid ZF_CONTAINER_HARDENING mode; expected 'enforced' or 'off'."
        )

    tmp_dir = Path(active_env.get("TMPDIR", "").strip() or "/tmp")
    writable: list[Path] = [tmp_dir]
    state_raw = active_env.get("ZF_STATE", "").strip()
    if state_raw:
        state_path = Path(state_raw)
        if state_path not in writable:
            writable.append(state_path)

    return enforce_container_hardening(
        bytecode_env=active_env.get("PYTHONDONTWRITEBYTECODE"),
        writable_paths=tuple(writable),
    )
