"""Execute a retained OLDER API image against a task-owned disposable SQL Server (issue #107).

Test-only and diagnostic. Not part of unit discovery, `tools/rpi-checks.py` or any gate. Run from
`src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests` and this worktree's distributions
installed (never a historical image's distributions). The older image is addressed ONLY by its
immutable ID; its Git provenance is unknown unless an OCI label says otherwise and is never inferred.

Actual mode creates its own labelled SQL container and a run-labelled INTERNAL private Docker
network, runs a fixed worker inside the older image once per named step (a fresh container each
time, so a restart) attached only to that network, and mutates and reads release and allowance
state through a separate current-source SQL connection published on loopback only. Outcomes:

* ACCEPTED: the positive control passed, every named case held and cleanup is verified (exit 0).
* VIOLATED: an older process dispatched after revocation or mismatch, restored an approval or
  replenished the allowance (exit 2). An observed violation is kept even when a later step failed.
* INSUFFICIENT: unsupported protocol, setup or schema error, timeout, missing or malformed
  observation, failed positive control, unproved precondition or unresolved cleanup (exit 3). This is
  never a pass.
* REFUSED: non-disposable target, wrong image, non-local engine or unsafe output path (exit 4).

`--self-test` runs the same worker, scenario and judge as plain subprocesses of the CURRENT source over
SQLite. It is a lower-fidelity check of this probe's own logic and is never old-image evidence.
"""

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any, Protocol, cast

from checks.old_image_worker import PACKAGED, VERSIONS
from zava_forward.core.mssqlstore import _Conn, connection_string

PINNED_IMAGE = "sha256:ad99bbb99df321f8d874b0df52ead4b3e24f4fb02c21a2245b278ea1a1e2cf78"
OWNER_LABEL = "ama.rpi.owner=issue-107-old-image-sql"
SQL_IMAGE = "mcr.microsoft.com/mssql/server:2022-latest"
TASK_LABEL = "zf.task=1292-sql-disposable"
ROOT = Path(__file__).resolve().parents[3]
WORKER = ROOT / "src/api/checks/old_image_worker.py"
FIXTURES = ROOT / "src/core/tests/release_support.py"

GOOD, REVOKED, MISMATCHED = "stock-prioritisation", "assessment-preparation", "funding-evidence"
CASES = ("ZF-1", "ZF-2", "ZF-3")
CALLS = 2
MUTATED = "mismatch-by-independent-connection"
OUTCOMES = {"ACCEPTED": 0, "VIOLATED": 2, "INSUFFICIENT": 3, "REFUSED": 4}

WORKER_TIMEOUT = 300
TOTAL_DEADLINE = 1800
HOST_OP_TIMEOUT = 60
READY_TIMEOUT = 240
DOCKER_TIMEOUT = 60
CLEANUP_TRIES = 3
SETTLE_SECONDS = 3
OUTPUT_LIMIT = 65536
HEX64 = re.compile(r"[0-9a-f]{64}")

PLAN = [(GOOD, c) for c in CASES] + [(REVOKED, "ZF-1"), (MISMATCHED, "ZF-1")]
TASK_KEYS = ("good1", "good2", "good3", "revoked", "mismatched")
# step -> (task key the step executes, capability/case pairs it re-invokes)
PROTOCOL: dict[str, tuple[str, list[list[str]]]] = {
    "provision": ("good1", []),
    "restart_after_revocation": ("revoked", [[REVOKED, "ZF-1"]]),
    "restart_after_mismatch": ("mismatched", [[MISMATCHED, "ZF-1"]]),
    "restart_remaining_allowance": ("good2", []),
    "restart_larger_allowance": ("good3", []),
}
SNAPSHOTS = (
    "after_provision",
    "after_revocation",
    "after_revoked_restart",
    "after_mutation",
    "after_mismatched_restart",
    "after_remaining",
    "after_larger",
)
LIMITS = (
    "Fresh-process proof is the distinct container id plus a hostname equal to its short id; "
    "sampled @@SPID values are reported only and are not required to be unique or to identify "
    "the session that performed an operation.",
    "Host SQL operations run on abandonable threads: a driver call blocked in native code cannot "
    "be killed, so the owned SQL container is removed and the process exits after reporting.",
    "Network isolation is the run-labelled internal network; the SQL container is also on the "
    "default bridge only to publish its port on loopback for the host connection.",
)

# Abandoned host calls cannot be killed; the entry point exits the process after reporting.
ABANDONED: list[str] = []


class Refused(RuntimeError):
    """A guard failed before any container was created or any state was touched."""


class DeadlineExceeded(RuntimeError):
    """A bounded host operation or the whole diagnostic ran out of time."""


class CreateFailed(RuntimeError):
    """A Docker object could not be created or reconciled to a verified identity."""


def redact(text: str, secrets_: Sequence[str]) -> str:
    for secret in secrets_:
        if secret:
            text = text.replace(secret, "***")
    return text


def sh(
    argv: Sequence[str], env: Mapping[str, str], timeout: float, limit: int = OUTPUT_LIMIT
) -> subprocess.CompletedProcess[str]:
    """Run one command with a wall-clock timeout; only the last `limit` bytes of each stream are kept."""
    proc = subprocess.Popen(
        list(argv),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=dict(env),
        start_new_session=True,
    )
    tails = (bytearray(), bytearray())

    def pump(stream: Any, tail: bytearray) -> None:
        for chunk in iter(lambda: stream.read1(8192), b""):
            tail += chunk
            if len(tail) > limit:
                del tail[: len(tail) - limit]

    readers = [
        threading.Thread(target=pump, args=(proc.stdout, tails[0]), daemon=True),
        threading.Thread(target=pump, args=(proc.stderr, tails[1]), daemon=True),
    ]
    for reader in readers:
        reader.start()
    try:
        proc.wait(timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(10)
        raise
    finally:
        for reader in readers:
            reader.join(10)
        for stream in (proc.stdout, proc.stderr):
            if stream:
                stream.close()
    return subprocess.CompletedProcess(
        list(argv),
        proc.returncode,
        tails[0].decode("utf-8", "replace"),
        tails[1].decode("utf-8", "replace"),
    )


class Deadline:
    """Wall-clock budget for the whole diagnostic and for each blocking host call."""

    def __init__(self, seconds: float) -> None:
        self.end = time.monotonic() + seconds
        self.abandoned: list[str] = []

    def remaining(self) -> float:
        return self.end - time.monotonic()

    def cap(self, seconds: float) -> float:
        left = self.remaining()
        if left <= 0:
            raise DeadlineExceeded("the diagnostic deadline has passed")
        return min(seconds, left)

    def call(self, label: str, seconds: float, fn: Callable[..., Any], *args: Any) -> Any:
        """Run `fn` on a daemon thread. A call that does not return is abandoned, never awaited."""
        if self.abandoned:
            raise DeadlineExceeded(f"{label}: an earlier host call is still blocked")
        limit = self.cap(seconds)
        box: dict[str, Any] = {}
        done = threading.Event()

        def target() -> None:
            try:
                box["value"] = fn(*args)
            except BaseException as error:
                box["error"] = error
            finally:
                done.set()

        threading.Thread(target=target, daemon=True).start()
        if not done.wait(limit):
            self.abandoned.append(label)
            ABANDONED.append(label)
            raise DeadlineExceeded(f"{label} did not return within {limit:.0f}s")
        if "error" in box:
            raise box["error"]
        return box.get("value")


def worker_create_args(
    name: str, run: str, network: str, probe: str, spec: str, env_keys: Sequence[str]
) -> list[str]:
    """Fixed reviewed argv for one older-image worker container; secrets travel as `-e KEY` only."""
    args = [
        "create",
        "--label",
        OWNER_LABEL,
        "--label",
        f"ama.rpi.run={run}",
        "--name",
        name,
        "--network",
        network,
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--tmpfs",
        "/tmp",
        "--tmpfs",
        "/state:uid=10001,gid=10001",
        "--memory",
        "1g",
        "--cpus",
        "1",
        "--pids-limit",
        "256",
        "--user",
        "10001:10001",
        "--entrypoint",
        "python",
        "-v",
        f"{probe}:/probe:ro",
    ]
    for key in env_keys:
        args += ["-e", key]
    return [*args, PINNED_IMAGE, "-I", "-B", "/probe/old_image_worker.py", f"/probe/{spec}"]


class Engine(Protocol):
    fidelity: str
    site_packages_only: bool

    def run(self, spec: dict[str, Any], label: str) -> dict[str, Any]: ...


class Db(Protocol):
    def query(self, sql: str, params: Sequence[Any] = ()) -> list[Any]: ...

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None: ...

    def session(self) -> int | None: ...


class SqliteDb:
    def __init__(self, path: str) -> None:
        self.conn = sqlite3.connect(path, timeout=30, isolation_level=None)

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[Any]:
        return self.conn.execute(sql, tuple(params)).fetchall()

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        self.conn.execute(sql, tuple(params))

    def session(self) -> int | None:
        return None


class MssqlDb:
    def __init__(self, env: Mapping[str, str]) -> None:
        self.conn = _Conn(connection_string(env))

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[Any]:
        return list(self.conn.execute(sql, tuple(params)).fetchall())

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        self.conn.execute(sql, tuple(params))

    def session(self) -> int | None:
        return int(self.conn.execute("SELECT @@SPID").fetchone()[0])


class BoundedDb:
    """Every host SQL call is bounded by the per-call and whole-diagnostic deadline."""

    def __init__(self, inner: Db, deadline: Deadline, seconds: float = HOST_OP_TIMEOUT) -> None:
        self.inner, self.deadline, self.seconds = inner, deadline, seconds

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[Any]:
        result: list[Any] = self.deadline.call(
            "host query", self.seconds, self.inner.query, sql, params
        )
        return result

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        self.deadline.call("host statement", self.seconds, self.inner.execute, sql, params)

    def session(self) -> int | None:
        result: int | None = self.deadline.call("host session", self.seconds, self.inner.session)
        return result


def snapshot(db: Db, tids: Mapping[str, str | None]) -> dict[str, Any]:
    """Independent read of release rows, task states and the allowance pool."""
    releases: dict[str, list[dict[str, Any]]] = {}
    for capability in (GOOD, REVOKED, MISMATCHED):
        rows = db.query(
            "SELECT id,status,body FROM assistant_releases WHERE capability=? ORDER BY id",
            (capability,),
        )
        releases[capability] = [
            dict(id=r[0], status=r[1], prompt_version=json.loads(r[2]).get("prompt_version"))
            for r in rows
        ]
    states = {}
    for key, tid in tids.items():
        row = db.query("SELECT state FROM assistant_tasks WHERE id=?", (tid,)) if tid else []
        states[key] = row[0][0] if row else None
    pool = db.query(
        "SELECT calls,tokens,used_calls,reserved_tokens FROM assistant_allowance ORDER BY id"
    )
    return dict(releases=releases, tasks=states, pool=[list(r) for r in pool])


def revoke(db: Db, rid: str) -> None:
    db.execute(
        "UPDATE assistant_releases SET status='revoked',revision=revision+1 "
        "WHERE id=? AND status='active'",
        (rid,),
    )


def mismatch(db: Db, rid: str) -> None:
    body = json.loads(db.query("SELECT body FROM assistant_releases WHERE id=?", (rid,))[0][0])
    body["prompt_version"] = MUTATED
    db.execute(
        "UPDATE assistant_releases SET body=?,revision=revision+1 WHERE id=? AND status='active'",
        (json.dumps(body, sort_keys=True, separators=(",", ":")), rid),
    )


def scenario(
    engine: Engine,
    db: Db,
    config: Mapping[str, str],
    principal: Mapping[str, Any],
    obs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the fixed steps in order into a caller-owned record, so no later error erases an earlier
    observation. The first step that does not finish `ok` is followed by its host snapshot and ends
    the scenario; judging is a separate pure step."""
    obs = obs if obs is not None else dict(steps={}, host={})
    steps: dict[str, Any] = obs["steps"]
    host: dict[str, Any] = obs["host"]
    base = dict(principal=dict(principal), action="execute")
    tids: dict[str, str | None] = dict.fromkeys(TASK_KEYS)

    def run(name: str, spec: dict[str, Any]) -> bool:
        try:
            steps[name] = engine.run(spec, name)
        except Exception as error:
            steps[name] = dict(status="error", error=f"{type(error).__name__}: {error}")
        return bool(steps[name].get("status") == "ok")

    def read(key: str) -> None:
        host[key] = snapshot(db, tids)

    def spec(name: str, **extra: Any) -> dict[str, Any]:
        key, again = PROTOCOL[name]
        return dict(
            base,
            config=dict(extra.pop("config", config)),
            execute=[tids[key]],
            reinvoke=[list(pair) for pair in again],
            **extra,
        )

    try:
        host["session"] = db.session()
        host["tasks"] = tids
        ok = run(
            "provision",
            dict(
                base,
                action="provision",
                config=dict(config),
                invoke=[list(pair) for pair in PLAN],
                execute_index=[0],
            ),
        )
        ids = {
            f"{t['capability']}/{t['case']}": t.get("id")
            for t in steps["provision"].get("tasks") or []
            if isinstance(t, Mapping) and "capability" in t
        }
        for key, (capability, case) in zip(TASK_KEYS, PLAN, strict=True):
            tids[key] = ids.get(f"{capability}/{case}")
        if not ok:
            return obs
        try:
            read("after_provision")
            active = host["after_provision"]["releases"]
            rid_revoked = next(r["id"] for r in active[REVOKED] if r["status"] == "active")
            rid_mismatched = next(r["id"] for r in active[MISMATCHED] if r["status"] == "active")
        except (StopIteration, KeyError):
            raise RuntimeError("precondition unreadable: no single active release") from None

        revoke(db, rid_revoked)
        read("after_revocation")
        ok = run("restart_after_revocation", spec("restart_after_revocation"))
        read("after_revoked_restart")
        if not ok:
            return obs

        mismatch(db, rid_mismatched)
        read("after_mutation")
        ok = run("restart_after_mismatch", spec("restart_after_mismatch"))
        read("after_mismatched_restart")
        if not ok:
            return obs

        ok = run("restart_remaining_allowance", spec("restart_remaining_allowance"))
        read("after_remaining")
        if not ok:
            return obs
        larger = dict(config, ZF_ASSIST_CALL_ALLOWANCE="5")
        run("restart_larger_allowance", spec("restart_larger_allowance", config=larger))
        read("after_larger")
    except Exception as error:
        host["error"] = f"{type(error).__name__}: {error}"
    return obs


def whole(value: Any) -> bool:
    return type(value) is int and value >= 0


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def pool_row(snap: Any) -> list[int] | None:
    """The one allowance row: calls, tokens, used_calls, reserved_tokens, all whole numbers."""
    rows = snap.get("pool") if isinstance(snap, Mapping) else None
    if isinstance(rows, list) and len(rows) == 1:
        row = rows[0]
        if isinstance(row, list) and len(row) == 4 and all(whole(v) for v in row):
            return row
    return None


def release_rows(snap: Any, capability: str) -> list[Mapping[str, Any]] | None:
    releases = snap.get("releases") if isinstance(snap, Mapping) else None
    rows = releases.get(capability) if isinstance(releases, Mapping) else None
    if isinstance(rows, list) and all(isinstance(r, Mapping) for r in rows):
        return rows
    return None


def task_state_of(snap: Any, key: str) -> Any:
    tasks = snap.get("tasks") if isinstance(snap, Mapping) else None
    return tasks.get(key) if isinstance(tasks, Mapping) else None


def release_state(snap: Any, capability: str, bound: set[str]) -> tuple[bool, bool]:
    """(any row active, required state missing or malformed) for the bound release IDs."""
    rows = release_rows(snap, capability)
    if rows is None:
        return False, True
    active = any(r.get("status") == "active" for r in rows)
    lost = not bound <= {r.get("id") for r in rows}
    return active, lost or any(not isinstance(r.get("status"), str) for r in rows)


def completed(name: str, step: Mapping[str, Any], tids: Mapping[str, Any]) -> bool:
    """The supported execute and re-invoke both ran to an observed result for the requested task."""
    return step.get("status") == "ok" and not execution_gaps(
        name, step, tids.get(PROTOCOL[name][0])
    )


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def dispatched(step: Mapping[str, Any]) -> bool:
    calls = step.get("provider_calls")
    return (isinstance(calls, int) and not isinstance(calls, bool) and calls > 0) or any(
        e.get("result") is True for e in entries(step, "executed")
    )


def entries(step: Mapping[str, Any], field: str) -> list[Mapping[str, Any]]:
    value = step.get(field)
    return [e for e in value if isinstance(e, Mapping)] if isinstance(value, list) else []


def execution_gaps(name: str, step: Mapping[str, Any], wanted: Any) -> list[str]:
    """Gaps in the one execution record and the re-invoke records of a step."""
    gaps: list[str] = []
    _, again = PROTOCOL[name]
    executed = step.get("executed")
    if not isinstance(executed, list) or len(executed) != 1 or not isinstance(executed[0], Mapping):
        gaps.append(f"{name}: exactly one execution record was not reported")
    else:
        entry = executed[0]
        if not text(wanted) or entry.get("id") != wanted:
            gaps.append(f"{name}: execution record is not for the requested task")
        if entry.get("before") != "pending":
            gaps.append(f"{name}: task was not pending before execution")
        if not isinstance(entry.get("result"), bool) or not text(entry.get("after")):
            gaps.append(f"{name}: execution result or after-state not reported")
        if "error" in entry:
            gaps.append(f"{name}: execute raised, outcome not observed")
    reinvoked = step.get("reinvoked")
    if not isinstance(reinvoked, list) or len(reinvoked) != len(again):
        gaps.append(f"{name}: re-invoke records were not reported")
    else:
        for want, got_entry in zip(again, reinvoked, strict=True):
            if not (
                isinstance(got_entry, Mapping)
                and [got_entry.get("capability"), got_entry.get("case")] == want
                and text(got_entry.get("state"))
            ):
                gaps.append(f"{name}: re-invoke of {want[0]} was not observed")
            elif "error" in got_entry:
                gaps.append(f"{name}: re-invoke raised, refusal not observed")
    return gaps


def check_step(name: str, step: Any, tids: Mapping[str, Any], strict: bool) -> list[str]:
    """Completeness of one step against the fixed protocol. Anything absent or malformed is a gap."""
    if not isinstance(step, Mapping):
        return [f"{name}: no observation"]
    if step.get("status") != "ok":
        return [f"{name}: status {step.get('status')!r} {step.get('error', '')}".strip()]
    gaps: list[str] = []
    if type(step.get("returncode")) is not int or step.get("returncode") != 0:
        gaps.append(f"{name}: process did not exit 0")
    if step.get("action") != ("provision" if name == "provision" else "execute"):
        gaps.append(f"{name}: unexpected action {step.get('action')!r}")
    cid = step.get("container_id")
    if not text(cid):
        gaps.append(f"{name}: no container identity")
    identity = step.get("identity")
    modules = identity.get("modules") if isinstance(identity, Mapping) else None
    if not isinstance(modules, Mapping) or set(modules) != set(PACKAGED):
        gaps.append(f"{name}: packaged module identity is not the complete expected set")
    else:
        for mod, info in modules.items():
            if not (
                isinstance(info, Mapping)
                and text(info.get("path"))
                and isinstance(info.get("sha256"), str)
                and HEX64.fullmatch(info["sha256"])
            ):
                gaps.append(f"{name}: {mod} has no path and hash")
    if not isinstance(identity, Mapping) or identity.get("missing") != []:
        gaps.append(f"{name}: protocol members missing or unreported")
    elif not isinstance(identity.get("versions"), Mapping) or set(identity["versions"]) != set(
        VERSIONS
    ):
        gaps.append(f"{name}: distribution versions not reported")
    if strict and text(cid) and isinstance(identity, Mapping):
        if identity.get("hostname") != str(cid)[:12]:
            gaps.append(f"{name}: worker hostname is not this container")
    if not whole(step.get("provider_calls")):
        gaps.append(f"{name}: provider call count not reported")

    key, again = PROTOCOL[name]
    tasks = step.get("tasks")
    if name == "provision":
        got = tasks if isinstance(tasks, list) else []
        ids = [t.get("id") if isinstance(t, Mapping) else None for t in got]
        if (
            len(got) != len(PLAN)
            or not all(isinstance(t, Mapping) for t in got)
            or [(t.get("capability"), t.get("case")) for t in got if isinstance(t, Mapping)] != PLAN
            or not all(text(i) for i in ids)
            or len(set(ids)) != len(ids)
        ):
            gaps.append(
                "provision: five distinct tasks for the requested capability/case were not reported"
            )
        elif any(t.get("state") != "pending" or "error" in t for t in got):
            gaps.append("not all five fixture tasks were created pending")
        wanted = ids[0] if ids else None
    else:
        wanted = tids.get(key)
        if tasks != []:
            gaps.append(f"{name}: unexpected task creation")
    gaps += execution_gaps(name, step, wanted)
    return gaps


def judge(obs: Mapping[str, Any], site_packages_only: bool) -> dict[str, Any]:
    """Pure classification. A violation proved by trustworthy partial evidence is kept whatever else
    failed; missing or malformed evidence is INSUFFICIENT, never a refusal and never a pass."""
    steps: Mapping[str, Any] = obs.get("steps") or {}
    host: Mapping[str, Any] = obs.get("host") or {}
    weak: list[str] = []
    bad: list[str] = []
    if "error" in host:
        weak.append(str(host["error"]))
    snaps = {k: host.get(k) for k in SNAPSHOTS}
    for key, value in snaps.items():
        if not isinstance(value, Mapping):
            weak.append(f"{key}: host snapshot missing")
    tids = mapping(host.get("tasks"))
    ids = [tids.get(k) for k in TASK_KEYS]
    if not all(text(i) for i in ids) or len(set(ids)) != len(ids):
        weak.append("five distinct task identities were not recorded")

    for name in PROTOCOL:
        weak += check_step(name, steps.get(name), tids, site_packages_only)
    ok_steps = [s for s in steps.values() if isinstance(s, Mapping) and s.get("status") == "ok"]
    mods = [m for m in (_modules(s) for s in ok_steps) if m is not None]
    shas = {json.dumps({k: v.get("sha256") for k, v in m.items()}, sort_keys=True) for m in mods}
    if len(shas) > 1:
        weak.append("packaged module hashes differ between steps")
    if site_packages_only and not all(
        "/site-packages/" in str(v.get("path")) for m in mods for v in m.values()
    ):
        weak.append("a module loaded from outside site-packages")
    cids = [s.get("container_id") for s in ok_steps]
    if any(not text(c) for c in cids) or len(set(cids)) != len(cids):
        weak.append("steps did not run as distinct processes or containers")

    provision = mapping(steps.get("provision"))
    done = entries(provision, "executed")
    pool1 = pool_row(snaps["after_provision"])
    if not (
        provision.get("status") == "ok"
        and done
        and done[0].get("result") is True
        and done[0].get("after") == "ready"
        and provision.get("provider_calls") == 1
        and pool1 is not None
        and pool1[0] == CALLS
        and pool1[2] == 1
    ):
        weak.append("positive control failed: older runtime did not dispatch exactly one call")

    bound: dict[str, set[str]] = {}
    for cap in (REVOKED, MISMATCHED):
        rows = release_rows(snaps["after_provision"], cap)
        if rows is None or sum(r.get("status") == "active" for r in rows) != 1:
            weak.append(f"{cap}: not exactly one active release before mutation")
        found = {r.get("id") for r in rows or []}
        bound[cap] = {i for i in found if isinstance(i, str) and i}
        if not bound[cap] or len(bound[cap]) != len(found):
            weak.append(f"{cap}: release identities were not recorded")
    revoked_read = bool(bound[REVOKED]) and release_state(
        snaps["after_revocation"], REVOKED, bound[REVOKED]
    ) == (False, False)
    if not revoked_read:
        weak.append("revocation was not read back")
    mut_rows = release_rows(snaps["after_mutation"], MISMATCHED)
    mutated_read = mut_rows is not None and any(
        r.get("prompt_version") == MUTATED and r.get("id") in bound[MISMATCHED] for r in mut_rows
    )
    if not mutated_read:
        weak.append("material mismatch was not read back")
    for key in ("revoked", "mismatched"):
        if task_state_of(snaps["after_provision"], key) != "pending":
            weak.append(f"{key} task was not pending before the restart")

    def audit(label: str, snap: Any, cap: str, trusted: bool) -> None:
        """After the supported worker the affected approval must not be active, whatever its version
        (the injected mutation proves the trigger, it is no exemption); lost state is a gap."""
        if not isinstance(snap, Mapping):
            return
        active, lost = release_state(snap, cap, bound[cap])
        if active and trusted:
            bad.append(f"{label}: an approval was restored or recorded for {cap}")
        if lost:
            weak.append(f"{label}: {cap} release state was missing or unreadable")

    mismatch_done = (
        completed("restart_after_mismatch", mapping(steps.get("restart_after_mismatch")), tids)
        and mutated_read
    )

    def refused(
        name: str, task: str, cap: str, snap: str, triggered: bool, audited: bool = True
    ) -> None:
        step = mapping(steps.get(name))
        after = snaps[snap]
        if not triggered:
            return
        if dispatched(step):
            bad.append(f"{name}: older process dispatched a provider call")
        if task_state_of(after, task) == "ready":
            bad.append(f"{name}: older process produced output")
        for entry in entries(step, "reinvoked"):
            state = entry.get("state")
            if isinstance(state, str) and state != "disabled":
                bad.append(f"{name}: new request not disabled ({state})")
        audit(name, after, cap, audited)
        before, now = pool_row(snaps["after_provision"]), pool_row(after)
        if before is not None and now is not None and before != now:
            bad.append(f"{name}: allowance changed")
        elif isinstance(after, Mapping) and (before is None or now is None):
            weak.append(f"{name}: allowance pool was not one well-formed row")
        executed = entries(step, "executed")
        if (
            executed
            and isinstance(after, Mapping)
            and executed[0].get("after") != task_state_of(after, task)
        ):
            weak.append(f"{name}: worker and host disagree on the task state")

    refused("restart_after_revocation", "revoked", REVOKED, "after_revoked_restart", revoked_read)
    refused(
        "restart_after_mismatch",
        "mismatched",
        MISMATCHED,
        "after_mismatched_restart",
        mutated_read,
        mismatch_done,
    )
    for later in ("after_mismatched_restart", "after_remaining", "after_larger"):
        audit(later, snaps[later], REVOKED, revoked_read)
    for later in ("after_remaining", "after_larger"):
        audit(later, snaps[later], MISMATCHED, mismatch_done)

    rest = mapping(steps.get("restart_remaining_allowance"))
    rest_done = entries(rest, "executed")
    pool2 = pool_row(snaps["after_remaining"])
    if not (
        rest.get("status") == "ok"
        and rest_done
        and rest_done[0].get("result") is True
        and rest.get("provider_calls") == 1
        and pool2 is not None
        and pool2[2] == 2
        and pool2[0] == CALLS
    ):
        weak.append("remaining-allowance control did not dispatch the last permitted call")
    if pool1 is not None and pool2 is not None and _replenished(pool1, pool2):
        bad.append("restart_remaining_allowance: allowance was replenished")

    big = mapping(steps.get("restart_larger_allowance"))
    pool3 = pool_row(snaps["after_larger"])
    exhausted = pool2 is not None and pool2[2] >= pool2[0]
    if exhausted:
        if dispatched(big):
            bad.append(
                "restart_larger_allowance: older process dispatched past the finite allowance"
            )
        larger = snaps["after_larger"]
        if isinstance(larger, Mapping):
            rows = larger.get("pool")
            if isinstance(rows, list) and len(rows) > 1:
                bad.append("restart_larger_allowance: a second allowance pool was created")
            elif pool3 is not None and pool2 is not None and _replenished(pool2, pool3):
                bad.append(
                    "restart_larger_allowance: allowance ceiling rose or consumption fell after the denied restart"
                )
            elif pool3 is None:
                weak.append("restart_larger_allowance: allowance pool was not one well-formed row")
    big_done = entries(big, "executed")
    if big.get("status") == "ok" and (
        not big_done or task_state_of(snaps["after_larger"], "good3") != "disabled"
    ):
        weak.append("restart_larger_allowance: refusal of the exhausted allowance was not observed")

    outcome = "VIOLATED" if bad else "INSUFFICIENT" if weak else "ACCEPTED"
    return dict(outcome=outcome, insufficient=weak, violations=bad)


def _modules(step: Mapping[str, Any]) -> Mapping[str, Any] | None:
    identity = step.get("identity")
    modules = identity.get("modules") if isinstance(identity, Mapping) else None
    if isinstance(modules, Mapping) and all(isinstance(v, Mapping) for v in modules.values()):
        return modules
    return None


def _replenished(before: Sequence[int], after: Sequence[int]) -> bool:
    """Either ceiling rose or either consumed quantity fell."""
    return (
        after[0] > before[0] or after[1] > before[1] or after[2] < before[2] or after[3] < before[3]
    )


def build_seed(path: Path) -> dict[str, Any]:
    """Same constructed principals and homes as `test_assistants.Base`; no private data."""
    import copy

    import test_mvp
    from zava_forward.core import projection

    data = copy.deepcopy(test_mvp.DATA)
    people = {}
    for i, role in enumerate(projection.STAFF_ROLES + ("Contractor", "Unknown")):
        people[role] = dict(
            code=f"ROLE-{i}", name=f"Human {i}", email=f"human{i}@example.test", role=role
        )
    data["staff"] = list(people.values())
    for c in data["cases"]:
        c["resident"]["adjustment"] = "PRIVATE-VULNERABILITY-REASON"
        c["finance"] = dict(
            budget=dict(amount=9183461, status="Approved"), commitments=[], invoices=[]
        )
        c["handoff"] = dict(state="Offered", to_code="ROLE-0", note="PRIVATE-HANDOFF-NOTE")
        c["documents"] = [
            dict(
                id="SURVEY-1",
                kind="Survey",
                name="PRIVATE-DOCUMENT-NAME",
                summary="PRIVATE-AI-SUMMARY",
                content_sha256="abc",
                version=1,
            )
        ]
    path.write_text(json.dumps(data))
    return dict(people["Retrofit Programme Manager"])


def stage(out: Path) -> tuple[Path, dict[str, Any]]:
    """Immutable inputs for the read-only /probe mount; hashes are recorded in the report."""
    probe = out / "probe"
    probe.mkdir(mode=0o755)
    shutil.copyfile(WORKER, probe / "old_image_worker.py")
    shutil.copyfile(FIXTURES, probe / "release_support.py")
    principal = build_seed(probe / "seed.json")
    for path in probe.iterdir():
        path.chmod(0o644)
    return probe, principal


def hashes(probe: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(probe.iterdir())}


def parse_worker(stdout: str) -> dict[str, Any]:
    for line in reversed(stdout.strip().splitlines()):
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if isinstance(value, dict):
            return value
    return dict(status="error", error="worker produced no JSON line")


# `-I` ignores PYTHONPATH and user site, so the self-test hands the parent's import path to the worker
# explicitly; the worker then runs isolated without needing a pip-installed checkout.
ISOLATED_LAUNCHER = (
    "import json, runpy, sys\n"
    "paths, worker, spec = json.loads(sys.argv[1]), sys.argv[2], sys.argv[3]\n"
    "sys.path[:0] = paths\n"
    "sys.argv = [worker, spec]\n"
    "runpy.run_path(worker, run_name='__main__')\n"
)


class SubprocessEngine:
    """Lower fidelity: the CURRENT source in a plain subprocess over SQLite. Never old-image evidence."""

    fidelity = "current-source-self-test"
    site_packages_only = False

    def __init__(self, probe: Path, db: Path, secrets_: Sequence[str] = ()) -> None:
        self.probe, self.db, self.counter, self.secrets = probe, db, 0, secrets_

    def run(self, spec: dict[str, Any], label: str) -> dict[str, Any]:
        self.counter += 1
        spec = dict(
            spec, seed=str(self.probe / "seed.json"), db=str(self.db), state_dir=str(self.probe)
        )
        spec_path = self.probe / f"spec-{self.counter}.json"
        spec_path.write_text(json.dumps(spec))
        env = dict(os.environ, ZF_PROBE_BACKEND="sqlite", ZF_PROBE_FIXTURES=str(self.probe))
        try:
            done = sh(
                [
                    sys.executable,
                    "-I",
                    "-B",
                    "-c",
                    ISOLATED_LAUNCHER,
                    json.dumps([p for p in sys.path if p]),
                    str(self.probe / "old_image_worker.py"),
                    str(spec_path),
                ],
                env,
                WORKER_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return dict(
                status="error", error="worker timed out", container_id=f"self-{self.counter}"
            )
        result = parse_worker(done.stdout)
        result.update(
            container_id=f"self-{self.counter}",
            returncode=done.returncode,
            raw_stderr=redact(done.stderr[-2000:], self.secrets),
        )
        return result


class Docker:
    """Every Docker object this run may own. Names are registered before create; an ambiguous create is
    reconciled by exact name plus the owner and run labels, and nothing is ever matched more broadly."""

    def __init__(
        self,
        run_id: str,
        env: Mapping[str, str],
        deadline: Deadline,
        secrets_: Sequence[str],
        pause: Callable[[float], None] = time.sleep,
    ) -> None:
        self.run_id, self.env, self.deadline, self.secrets = run_id, env, deadline, secrets_
        self.pause = pause
        self.resources: dict[str, dict[str, Any]] = {}

    def cmd(
        self,
        *args: str,
        timeout: float = DOCKER_TIMEOUT,
        env: Mapping[str, str] | None = None,
        capped: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        limit = self.deadline.cap(timeout) if capped else timeout
        return sh(["docker", *args], env if env is not None else self.env, limit)

    def labels(self) -> list[str]:
        return ["--label", OWNER_LABEL, "--label", f"ama.rpi.run={self.run_id}"]

    def fields(self, res: Mapping[str, Any], cid: str) -> tuple[str, ...] | None:
        """Full id, exact name, run label and owner label of one object, or None when unreadable."""
        if res["kind"] == "container":
            fmt = '{{.Id}}|{{.Name}}|{{index .Config.Labels "ama.rpi.run"}}|{{index .Config.Labels "ama.rpi.owner"}}'
            argv: tuple[str, ...] = ("inspect", "--format", fmt, cid)
        else:
            fmt = '{{.Id}}|{{.Name}}|{{index .Labels "ama.rpi.run"}}|{{index .Labels "ama.rpi.owner"}}|{{.Internal}}'
            argv = ("network", "inspect", "--format", fmt, cid)
        done = self.cmd(*argv, capped=False)
        if done.returncode != 0:
            return None
        return tuple(done.stdout.strip().split("|"))

    def match(self, res: Mapping[str, Any], found: tuple[str, ...] | None) -> bool:
        wanted_name = ("/" if res["kind"] == "container" else "") + str(res["name"])
        return (
            found is not None
            and len(found) >= 4
            and found[1] == wanted_name
            and found[2] == self.run_id
            and found[3] == OWNER_LABEL.split("=", 1)[1]
        )

    def find(self, res: dict[str, Any]) -> tuple[str, str | None]:
        """('found', id), ('none', None) after a successful empty listing, or ('error', None)."""
        name = str(res["name"])
        try:
            if res["kind"] == "container":
                listing = self.cmd(
                    "ps",
                    "-a",
                    "--no-trunc",
                    "--filter",
                    f"name=^/{name}$",
                    "--filter",
                    f"label={OWNER_LABEL}",
                    "--filter",
                    f"label=ama.rpi.run={self.run_id}",
                    "--format",
                    "{{.ID}}",
                    capped=False,
                )
            else:
                listing = self.cmd(
                    "network",
                    "ls",
                    "--no-trunc",
                    "--filter",
                    f"name={name}",
                    "--filter",
                    f"label={OWNER_LABEL}",
                    "--filter",
                    f"label=ama.rpi.run={self.run_id}",
                    "--format",
                    "{{.ID}}",
                    capped=False,
                )
        except (subprocess.TimeoutExpired, OSError) as error:
            res["errors"].append(f"list {type(error).__name__}")
            return "error", None
        if listing.returncode != 0:
            res["errors"].append(
                redact(f"list failed: {listing.stderr.strip()[:200]}", self.secrets)
            )
            return "error", None
        owned: list[str] = []
        for cid in [line.strip() for line in listing.stdout.splitlines() if line.strip()]:
            try:
                found = self.fields(res, cid)
            except (subprocess.TimeoutExpired, OSError) as error:
                res["errors"].append(f"inspect {type(error).__name__}")
                return "error", None
            if found is None:
                res["errors"].append("inspect failed")
                return "error", None
            if self.match(res, found) and HEX64.fullmatch(cid) and found[0] == cid:
                owned.append(cid)
        if not owned:
            return "none", None
        if len(owned) > 1 or (res["id"] and owned[0] != res["id"]):
            res["errors"].append("exact name and labels matched an unexpected identity")
            return "error", None
        return "found", owned[0]

    def create(
        self, kind: str, name: str, args: Sequence[str], env: Mapping[str, str] | None = None
    ) -> str:
        """Create one object and return its verified full id. Registered first, so a create that the
        daemon completed after the client gave up is still tracked."""
        res = self.resources.setdefault(
            name,
            dict(
                kind=kind,
                name=name,
                id=None,
                ambiguous=False,
                reconciled=False,
                absent=None,
                attempts=0,
                errors=[],
            ),
        )
        verb = ["create"] if kind == "container" else ["network", "create"]
        try:
            done = self.cmd(*verb, *args, env=env, timeout=600 if kind == "container" else 60)
        except (subprocess.TimeoutExpired, OSError) as error:
            res["ambiguous"] = True
            res["errors"].append(f"create {type(error).__name__}")
        else:
            cid = done.stdout.strip()
            if done.returncode == 0 and HEX64.fullmatch(cid):
                res["id"] = cid
                return cid
            res["errors"].append(
                redact(f"create failed: {done.stderr.strip()[:200]}", self.secrets)
            )
        state, cid_found = self.find(res)
        if state == "found" and cid_found:
            res["id"], res["ambiguous"], res["reconciled"] = cid_found, False, True
            return cid_found
        raise CreateFailed(f"{kind} {name} was not created or could not be verified")

    def attachments(self, cid: str) -> tuple[str, set[str]] | None:
        """Network mode and every network name the container is attached to, or None if unreadable."""
        done = self.cmd(
            "inspect",
            "--format",
            "{{.HostConfig.NetworkMode}}|{{json .NetworkSettings.Networks}}",
            cid,
            capped=False,
        )
        mode, _, nets = done.stdout.strip().partition("|")
        if done.returncode != 0:
            return None
        try:
            return mode, set(json.loads(nets)) if nets and nets != "null" else set()
        except ValueError:
            return None

    def remove(self, res: dict[str, Any]) -> None:
        """Bounded removal: re-list by exact name and labels until absent or the attempts are spent."""
        settled = not res["ambiguous"]
        while True:
            state, cid = self.find(res)
            if state == "none":
                if not settled:
                    settled = True
                    self.pause(SETTLE_SECONDS)
                    continue
                res["absent"] = True
                return
            if res["attempts"] >= CLEANUP_TRIES:
                res["absent"] = False
                return
            res["attempts"] += 1
            if state != "found" or cid is None:
                continue
            argv = ("rm", "--force", cid) if res["kind"] == "container" else ("network", "rm", cid)
            try:
                done = self.cmd(*argv, timeout=120, capped=False)
                if done.returncode != 0:
                    res["errors"].append(
                        redact(f"remove failed: {done.stderr.strip()[:200]}", self.secrets)
                    )
            except (subprocess.TimeoutExpired, OSError) as error:
                res["errors"].append(f"remove {type(error).__name__}")

    def cleanup(self) -> dict[str, Any]:
        """Remove what this run created, containers before the network. Never raises."""
        order = sorted(self.resources.values(), key=lambda r: r["kind"] != "container")
        for res in order:
            try:
                self.remove(res)
            except Exception as error:
                res["absent"] = False
                res["errors"].append(f"cleanup {type(error).__name__}: {error}")
        records = [
            dict(
                kind=r["kind"],
                name=r["name"],
                id=r["id"],
                ambiguous_create=r["ambiguous"],
                reconciled_after_ambiguous_create=r["reconciled"],
                absent=r["absent"] is True,
                removal_attempts=r["attempts"],
                errors=list(r["errors"]),
            )
            for r in order
        ]
        problems = [
            f"{r['kind']} {r['name']}: "
            + (
                "create ended without a verified answer; a late daemon-side create cannot be excluded"
                if r["ambiguous_create"]
                else "still present or absence unverified"
            )
            for r in records
            if not r["absent"] or r["ambiguous_create"]
        ]
        return dict(
            expected=[r["name"] for r in records],
            removed=[r["name"] for r in records if r["absent"] and r["id"]],
            remaining=[r["name"] for r in records if not r["absent"]],
            resources=records,
            problems=problems,
            ok=not problems,
        )


class DockerEngine:
    """Actual mode: one fresh container from the pinned older image per step, on the private network."""

    fidelity = "actual-older-image"
    site_packages_only = True

    def __init__(
        self,
        probe: Path,
        docker: Docker,
        network: str,
        env: Mapping[str, str],
        keys: Sequence[str],
    ) -> None:
        self.probe, self.docker, self.network, self.env, self.keys = (
            probe,
            docker,
            network,
            env,
            keys,
        )
        self.counter = 0

    def run(self, spec: dict[str, Any], label: str) -> dict[str, Any]:
        self.counter += 1
        spec = dict(spec, seed="/probe/seed.json", state_dir="/state")
        name = f"ama-107-old-{self.docker.run_id}-{self.counter}"
        spec_name = f"spec-{self.counter}.json"
        (self.probe / spec_name).write_text(json.dumps(spec))
        (self.probe / spec_name).chmod(0o644)
        try:
            cid = self.docker.create(
                "container",
                name,
                worker_create_args(
                    name, self.docker.run_id, self.network, str(self.probe), spec_name, self.keys
                )[1:],
                env=self.env,
            )
        except CreateFailed as error:
            return dict(status="error", error=redact(str(error), self.docker.secrets))
        found = self.docker.attachments(cid)
        if found is None or found[0] != self.network or not found[1] <= {self.network}:
            return dict(
                status="error",
                error="worker is not attached only to the private network",
                container_id=cid,
            )
        try:
            started = self.docker.cmd("start", "-a", cid, timeout=WORKER_TIMEOUT)
        except subprocess.TimeoutExpired:
            try:
                self.docker.cmd("kill", cid, capped=False)
            except (subprocess.TimeoutExpired, OSError):
                pass
            return dict(status="error", error="worker timed out", container_id=cid)
        result = parse_worker(started.stdout)
        result.update(
            container_id=cid,
            returncode=started.returncode,
            raw_stderr=redact(started.stderr[-2000:], self.docker.secrets),
        )
        return result


def preflight(env: Mapping[str, str]) -> dict[str, str]:
    """Refuse a non-local engine or an image other than the pinned ID before any container exists."""
    host = (env.get("DOCKER_HOST") or "").strip()
    if host and not host.startswith("unix://"):
        raise Refused("DOCKER_HOST must be unset or a local unix socket")
    if env.get("DOCKER_TLS_VERIFY") or env.get("DOCKER_CERT_PATH"):
        raise Refused("a TLS Docker endpoint is not a local engine")

    def docker(*args: str) -> str:
        done = sh(["docker", *args], env, DOCKER_TIMEOUT)
        if done.returncode != 0:
            raise Refused(f"docker {args[0]} failed: {done.stderr.strip()[:200]}")
        return done.stdout.strip()

    if docker("context", "show") != "default":
        raise Refused("the selected Docker context must be default")
    endpoint = docker("context", "inspect", "--format", "{{.Endpoints.docker.Host}}", "default")
    if not endpoint.startswith("unix://"):
        raise Refused("the default Docker context must be a local unix socket")
    if docker("image", "inspect", "--format", "{{.Id}}", PINNED_IMAGE) != PINNED_IMAGE:
        raise Refused("the image ID is not the pinned older image")
    return dict(image_inspect=docker("image", "inspect", PINNED_IMAGE), endpoint=endpoint)


def free_name() -> str:
    return uuid.uuid4().hex[:12]


def write_report(out: Path, report: Mapping[str, Any], secrets_: Sequence[str]) -> None:
    (out / "report.json").write_text(redact(json.dumps(report, indent=2, default=str), secrets_))


def new_output(path: str) -> Path:
    """Create the new output folder exclusively and return its canonical location. The parent is
    resolved through symlinks and `..`, must already exist and may not be inside the checkout."""
    out = Path(path)
    if not out.is_absolute() or out.name in ("", ".", ".."):
        raise Refused("--out must be a new absolute folder outside the repository")
    root = ROOT.resolve()
    try:
        parent = out.parent.resolve(strict=True)
    except (OSError, RuntimeError):
        raise Refused("the parent of --out must already exist") from None
    canonical = parent / out.name
    if root in (canonical, *canonical.parents):
        raise Refused("--out must be a new absolute folder outside the repository")
    try:
        canonical.mkdir(mode=0o700)
    except OSError:
        raise Refused("--out must not already exist") from None
    bound = canonical.resolve(strict=True)
    if bound != canonical or root in (bound, *bound.parents) or canonical.is_symlink():
        raise Refused("--out did not resolve to a new location outside the repository")
    return bound


def assistant_config(**overrides: Any) -> Any:
    """The untyped test-suite config helper, called through an explicit Any boundary."""
    from test_assistants import config

    return cast(Any, config)(**overrides)


def self_test(out: Path) -> int:
    probe, principal = stage(out)
    engine = SubprocessEngine(probe, out / "cases.sqlite")
    obs = scenario(
        engine,
        SqliteDb(str(out / "cases.sqlite")),
        assistant_config(call_allowance=CALLS),
        principal,
    )
    verdict = judge(obs, engine.site_packages_only)
    report = dict(
        fidelity=engine.fidelity,
        verdict=verdict,
        observations=obs,
        inputs=hashes(probe),
        note="Current-source SQLite self-test of the probe logic; not older-image evidence.",
    )
    write_report(out, report, ())
    print(f"SELF-TEST ({engine.fidelity}): {verdict['outcome']}; not old-image evidence.")
    return 0 if verdict["outcome"] == "ACCEPTED" else 1


def wait_ready(
    connect: Callable[[], Any],
    create: str,
    deadline: Deadline,
    seconds: float = READY_TIMEOUT,
    pause: Callable[[float], None] = time.sleep,
) -> None:
    """Bounded readiness: every login and statement is deadline-bound and a failed connection is closed."""
    end = time.monotonic() + seconds
    while True:
        conn: Any = None
        try:
            conn = deadline.call("readiness login", HOST_OP_TIMEOUT, connect)
            deadline.call("readiness create database", HOST_OP_TIMEOUT, conn.execute, create)
            return
        except DeadlineExceeded:
            raise
        except Exception:
            if time.monotonic() >= end:
                raise Refused("task-owned SQL Server did not become ready") from None
            pause(2)
        finally:
            if conn is not None:
                try:
                    deadline.call("readiness close", 10, conn.close)
                except Exception:
                    pass


def conclude(verdict: Mapping[str, Any], containment: Mapping[str, Any]) -> dict[str, Any]:
    """Cleanup can only make a result weaker: a behavioural violation is kept beside containment
    errors and an otherwise ACCEPTED run with unresolved cleanup is INSUFFICIENT."""
    result = dict(verdict)
    result["insufficient"] = list(verdict.get("insufficient", []))
    if not containment.get("ok"):
        result["containment_errors"] = list(containment.get("problems", []))
        if result["outcome"] == "ACCEPTED":
            result["outcome"] = "INSUFFICIENT"
            result["insufficient"].append(
                "cleanup is unresolved: " + "; ".join(containment["problems"])
            )
    return result


def actual(out: Path) -> int:
    import sqlguard

    env = dict(os.environ)
    run_id = free_name()
    sql_name, net_name, alias = f"ama-107-sql-{run_id}", f"ama-107-net-{run_id}", f"sql-{run_id}"
    password = "Aa1!" + secrets.token_urlsafe(24)
    sensitive = [password]
    deadline = Deadline(TOTAL_DEADLINE)
    docker = Docker(run_id, env, deadline, sensitive)
    obs: dict[str, Any] = dict(steps={}, host={})
    report: dict[str, Any] = dict(
        fidelity="actual-older-image",
        image=PINNED_IMAGE,
        run=run_id,
        output=str(out),
        provenance="UNKNOWN (no OCI revision label evidenced)",
        limits=list(LIMITS),
    )
    verdict: dict[str, Any] = dict(outcome="INSUFFICIENT", insufficient=["not run"], violations=[])
    try:
        report["preflight"] = preflight(env)
        probe, principal = stage(out)
        report["inputs"] = hashes(probe)
        db_name = f"zf_old_image_107_{run_id}"
        net_id = docker.create(
            "network", net_name, ["--driver", "bridge", "--internal", *docker.labels(), net_name]
        )
        net = docker.fields(docker.resources[net_name], net_id)
        if not docker.match(docker.resources[net_name], net) or not net or net[-1] != "true":
            raise Refused("the private network is not the owned internal network")
        report["network"] = dict(name=net_name, id=net_id, internal=True)
        sql_env = dict(env, ACCEPT_EULA="Y", MSSQL_SA_PASSWORD=password)
        sql_id = docker.create(
            "container",
            sql_name,
            [
                "--label",
                TASK_LABEL,
                *docker.labels(),
                "--name",
                sql_name,
                "--memory",
                "3g",
                "--cpus",
                "2",
                "-e",
                "ACCEPT_EULA",
                "-e",
                "MSSQL_SA_PASSWORD",
                "-p",
                "127.0.0.1::1433",
                SQL_IMAGE,
            ],
            env=sql_env,
        )
        for argv in (("network", "connect", "--alias", alias, net_name, sql_id), ("start", sql_id)):
            done = docker.cmd(*argv, timeout=120)
            if done.returncode != 0:
                raise Refused(f"docker {argv[0]} failed: {redact(done.stderr, sensitive)[:200]}")
        listed = docker.cmd("port", sql_id, "1433/tcp")
        if listed.returncode != 0 or ":" not in listed.stdout:
            raise Refused("the SQL port publication could not be read")
        port = listed.stdout.strip().splitlines()[0].rsplit(":", 1)[1]
        joined = docker.attachments(sql_id)
        if joined is None or joined[1] != {"bridge", net_name}:
            raise Refused(
                "the SQL container is not on exactly the default bridge and the private network"
            )
        manifest = out / "sql-manifest.json"
        sqlguard.write_manifest(str(manifest), "127.0.0.1", port, password, sql_id)
        sql = dict(
            ZF_SQL_SERVER="127.0.0.1",
            ZF_SQL_PORT=port,
            ZF_SQL_AUTH="password",
            ZF_SQL_USER="sa",
            ZF_SQL_PASSWORD=password,
            ZF_SQL_TRUST_CERT="1",
            ZF_SQL_TASK_MANIFEST=str(manifest),
        )
        sqlguard.require_task_owned_loopback(sql)
        master = dict(sql, ZF_SQL_DATABASE="master")
        wait_ready(
            lambda: _Conn(connection_string(master)), f"CREATE DATABASE [{db_name}]", deadline
        )
        worker_sql = dict(sql, ZF_SQL_SERVER=alias, ZF_SQL_PORT="1433", ZF_SQL_DATABASE=db_name)
        run_env = dict(env, **worker_sql, ZF_PROBE_BACKEND="mssql", ZF_PROBE_FIXTURES="/probe")
        keys = [
            "ZF_SQL_SERVER",
            "ZF_SQL_PORT",
            "ZF_SQL_DATABASE",
            "ZF_SQL_AUTH",
            "ZF_SQL_USER",
            "ZF_SQL_PASSWORD",
            "ZF_SQL_TRUST_CERT",
            "ZF_PROBE_BACKEND",
            "ZF_PROBE_FIXTURES",
        ]
        engine = DockerEngine(probe, docker, net_name, run_env, keys)
        host_env = dict(sql, ZF_SQL_DATABASE=db_name)
        inner = deadline.call("host login", HOST_OP_TIMEOUT, MssqlDb, host_env)
        scenario(
            engine,
            BoundedDb(inner, deadline),
            assistant_config(call_allowance=CALLS),
            principal,
            obs,
        )
        verdict = judge(obs, engine.site_packages_only)
    except Refused as error:
        verdict = dict(outcome="REFUSED", insufficient=[], violations=[str(error)])
    except Exception as error:
        verdict = judge(obs, True) if obs["steps"] else verdict
        verdict["insufficient"] = [*verdict["insufficient"], f"{type(error).__name__}: {error}"]
        if verdict["outcome"] == "ACCEPTED":
            verdict["outcome"] = "INSUFFICIENT"
    finally:
        containment = docker.cleanup()
        verdict = conclude(verdict, containment)
        report.update(verdict=verdict, observations=obs, containment=containment)
        write_report(out, report, sensitive)
    outcome = verdict["outcome"]
    print(f"OLD-IMAGE SQL PROBE {outcome} (image {PINNED_IMAGE}); report {out / 'report.json'}")
    return OUTCOMES[outcome]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="new absolute folder outside the repository")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="current-source SQLite self-test of the probe logic (not old-image evidence)",
    )
    args = parser.parse_args(argv)
    try:
        out = new_output(args.out)
    except Refused as error:
        print(f"REFUSED: {error}")
        return OUTCOMES["REFUSED"]
    return self_test(out) if args.self_test else actual(out)


if __name__ == "__main__":
    code = main()
    sys.stdout.flush()
    if ABANDONED:
        os._exit(code)
    raise SystemExit(code)
