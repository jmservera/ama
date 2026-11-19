#!/usr/bin/env python3
"""Non-receipt, change-specific preflight for the local RPI gate (issue #1830).

Runs only reviewed unit selectors and tracked browser checks that the caller names,
labels every result as development feedback and never produces a gate receipt.
It does not install, provision, clean up or edit anything.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import hmac
import json
import os
import re
import shutil
import signal
import socket
import stat
import struct
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Any, Self
from urllib.parse import urlsplit

LABEL = "NON-RECEIPT DEVELOPMENT FEEDBACK. Does not satisfy the full tier, review or hosted CI."
HEAVY_LOCK_PATH = Path("/tmp/ama-rpi-heavy.lock")
PROC = Path("/proc")
AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
PROJECTS = ("core", "agents", "api", "orchestrator", "importer")
SELECTOR = re.compile(r"(core|agents|api|orchestrator|importer):test_[A-Za-z0-9_.]+")
CHECK = re.compile(r"[a-z][a-z0-9_]*_check")
CONTAINER = re.compile(r"[0-9a-f]{64}")
INERT_PREFIXES = ("docs/", ".copilot-tracking/", "support/")
SQL_WORDS = ("store", "schema", "sql", "assistants")
SECRET_WORDS = ("PASSWORD", "SECRET", "TOKEN", "KEY")
OUT_BYTES = 58
EXIT_PASS, EXIT_FAIL, EXIT_INPUT, EXIT_UNCOVERED, EXIT_MUTATION, EXIT_PREREQ = (
    0,
    1,
    2,
    3,
    4,
    5,
)
EXIT_NOT_RUN = 6
DOCKER_REMOTE_ENV = (
    "DOCKER_HOST",
    "DOCKER_CONTEXT",
    "DOCKER_TLS_VERIFY",
    "DOCKER_CERT_PATH",
)
MSSQL_IMAGE = "mcr.microsoft.com/mssql/server:"
MSSQL_DIGEST = "mcr.microsoft.com/mssql/server@sha256:"
IMAGE_ID = re.compile(r"sha256:[0-9a-f]{64}")
MAX_CONTAINER_AGE = timedelta(hours=6)
CLOCK_SKEW = timedelta(seconds=60)
OWNER = re.compile(r"[A-Za-z0-9_.-]{8,64}")
GATE_ONLY = "fresh images, scanners, hosted CI and the full receipt are gate-only and not covered"
LIST_SNIPPET = (
    "import json,sys,unittest\n"
    "loader=unittest.TestLoader(); out={}\n"
    "def walk(s):\n"
    "    for t in s:\n"
    "        if isinstance(t,unittest.TestSuite): yield from walk(t)\n"
    "        else: yield t\n"
    "for name in sys.argv[1:]:\n"
    "    ids=[]\n"
    "    for t in walk(loader.loadTestsFromName(name)):\n"
    "        ids.append(t.id())\n"
    "    out[name]=ids\n"
    "print(json.dumps(out))\n"
)
BROWSER_ENTRY = (
    "import runpy,tempfile,os,sys\n"
    "from unittest.mock import patch\n"
    "original=tempfile.TemporaryDirectory\n"
    "def external_scratch(*args,**kwargs):\n"
    "    kwargs['dir']=os.environ['TMPDIR']\n"
    "    return original(*args,**kwargs)\n"
    "with patch('tempfile.TemporaryDirectory',external_scratch):\n"
    "    runpy.run_module(sys.argv.pop(1),run_name='__main__')\n"
)
ORIGIN_PROBE = (
    "import importlib,json,sys\n"
    "out={}\n"
    "for project in sys.argv[1:]:\n"
    "    try:\n"
    "        module=importlib.import_module('zava_forward.'+project)\n"
    "        out[project]=[str(p) for p in module.__path__]\n"
    "    except Exception:\n"
    "        pass\n"
    "print(json.dumps(out))\n"
)
CHROMIUM_PROBE = (
    "import sys\n"
    "from playwright.sync_api import sync_playwright\n"
    "p=sync_playwright().start()\n"
    "print(p.chromium.executable_path)\n"
    "p.stop()\n"
)


class PreflightError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        stdin=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise PreflightError(EXIT_INPUT, f"git {args[0]} failed: {result.stderr.decode()[:200]}")
    return result.stdout


def tracked_or_intended(repo: Path) -> set[str]:
    raw = git(repo, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    return {item.decode() for item in raw.split(b"\0") if item}


def repo_relative(repo: Path, value: str, known: set[str]) -> str:
    pure = PurePosixPath(value)
    if (
        not value
        or value.startswith("-")
        or pure.is_absolute()
        or ".." in pure.parts
        or "\0" in value
    ):
        raise PreflightError(EXIT_INPUT, f"Invalid repository path: {value!r}")
    normal = pure.as_posix()
    full = repo / normal
    resolved = full.resolve()
    if not resolved.is_relative_to(repo) or not resolved.exists():
        raise PreflightError(EXIT_INPUT, f"Path does not exist inside the repository: {value}")
    if normal not in known:
        raise PreflightError(EXIT_INPUT, f"Path is neither tracked nor intended: {value}")
    return normal


def parse_selector(repo: Path, value: str, known: set[str]) -> tuple[str, str]:
    if not SELECTOR.fullmatch(value):
        raise PreflightError(
            EXIT_INPUT,
            f"Selector must be PROJECT:test_module[.Class[.method]]: {value!r}",
        )
    project, selector = value.split(":", 1)
    module = selector.split(".", 1)[0]
    repo_relative(repo, f"src/{project}/tests/{module}.py", known)
    return project, selector


def required_needs(path: str) -> tuple[set[str], str | None]:
    """Reviewed required-area table: needs a path demands, or the reason it is uncovered."""
    parts = PurePosixPath(path).parts
    lowered = path.lower()
    if path.startswith(INERT_PREFIXES) or path.endswith(".md"):
        return set(), None
    if len(parts) > 2 and parts[0] == "src" and parts[1] in PROJECTS:
        project = parts[1]
        if any(word in lowered for word in ("dockerfile", "requirements", "pyproject.toml")):
            return (
                set(),
                "dependency or image input: image and scanner groups are gate-only",
            )
        consumers = (
            PROJECTS
            if project == "core"
            else ("agents", "api")
            if project == "agents"
            else (project,)
        )
        needs = {f"unit:{name}" for name in consumers}
        if project == "api" and ("/web/" in path or parts[2] == "checks"):
            needs.add("browser")
        name = parts[-1].lower()
        if any(word in name for word in SQL_WORDS) or (project == "core" and "sensor" in name):
            needs.add("sql")
        return needs, None
    return set(), "no reviewed preflight mapping for this path; gate-only"


def parse_covers(values: list[str], files: set[str], targets: set[str]) -> dict[str, set[str]]:
    covers: dict[str, set[str]] = {}
    for value in values:
        path, separator, target = value.partition("=")
        if not separator or path not in files or target not in targets:
            raise PreflightError(
                EXIT_INPUT,
                f"--covers must be FILE=TARGET naming a --file and a target: {value!r}",
            )
        covers.setdefault(path, set()).add(target)
    return covers


def assess_coverage(
    files: list[str],
    covers: dict[str, set[str]],
    unit_projects: dict[str, str],
    browser_targets: set[str],
    sql_targets: set[str],
) -> list[dict[str, Any]]:
    uncovered = []
    for path in files:
        needs, reason = required_needs(path)
        if reason is not None:
            uncovered.append({"path": path, "reason": reason})
            continue
        if not needs:
            continue
        declared = covers.get(path, set())
        if not declared:
            uncovered.append({"path": path, "reason": "no --covers declaration"})
            continue
        missing = []
        for need in sorted(needs):
            if need.startswith("unit:"):
                satisfied = any(unit_projects.get(target) == need[5:] for target in declared)
            elif need == "browser":
                satisfied = bool(declared & browser_targets)
            else:
                satisfied = bool(declared & sql_targets)
            if not satisfied:
                missing.append(need)
        if missing:
            uncovered.append(
                {
                    "path": path,
                    "reason": "missing declared coverage: " + ", ".join(missing),
                }
            )
    return uncovered


def test_environment(repo: Path, project_tests: list[str]) -> dict[str, str]:
    return {
        "PYTHONPATH": ":".join(str(repo / item) for item in project_tests),
        "PYTHONDONTWRITEBYTECODE": "1",
    }


def tests_dirs(project: str, own: bool = True) -> list[str]:
    paths = [f"src/{project}/tests"] if own else []
    if project in ("api", "agents", "orchestrator"):
        paths.append("src/core/tests")
    if project == "api":
        paths.append("src/agents/tests")
    return paths


def scrubbed_env(tmp: Path, extra: dict[str, str]) -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if key in ("PATH", "HOME", "LANG", "PLAYWRIGHT_BROWSERS_PATH") or key.startswith("LC_")
    }
    env["TMPDIR"] = str(tmp)
    env.update(extra)
    return env


def mask(text: str, env: dict[str, str]) -> str:
    for key, value in env.items():
        if value and any(word in key.upper() for word in SECRET_WORDS):
            text = text.replace(value, "<redacted>")
    return text


def run(
    argv: list[str], cwd: Path, env: dict[str, str], timeout: int
) -> tuple[int, str, float, bool]:
    started = time.monotonic()
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate()
        timed_out = True
    return (
        process.returncode,
        mask(output or "", env),
        time.monotonic() - started,
        timed_out,
    )


def check_interpreter(python: Path, repo: Path) -> None:
    if not python.is_file() or not os.access(python, os.X_OK):
        raise PreflightError(EXIT_PREREQ, f"--python is not an executable file: {python}")
    result = subprocess.run(
        [str(python), "-c", ORIGIN_PROBE, *PROJECTS],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env={"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
    )
    try:
        origins = json.loads(result.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        origins = {}
    for project in PROJECTS:
        root = (repo / "src" / project / "src").resolve()
        paths = origins.get(project) if isinstance(origins, dict) else None
        if (
            result.returncode != 0
            or not paths
            or not all(Path(item).resolve().is_relative_to(root) for item in paths)
        ):
            raise PreflightError(
                EXIT_PREREQ,
                f"--python must import zava_forward.{project} from this checkout; pip install "
                "every src/<project> distribution in editable mode first (the preflight never "
                "installs)",
            )


def list_tests(
    python: Path, repo: Path, project: str, selectors: list[str], env: dict[str, str]
) -> dict[str, list[str]]:
    code, output, _, _ = run(
        [str(python), "-c", LIST_SNIPPET, *selectors], repo / "src" / project, env, 120
    )
    try:
        listed = json.loads(output.strip().splitlines()[-1])
    except (ValueError, IndexError):
        raise PreflightError(
            EXIT_INPUT, f"Could not load selectors {selectors}: {output[-300:]}"
        ) from None
    if code != 0:
        raise PreflightError(EXIT_INPUT, f"Could not load selectors: {output[-300:]}")
    for name, ids in listed.items():
        if not ids or any(".ModuleImportFailure." in item or "_FailedTest" in item for item in ids):
            raise PreflightError(
                EXIT_INPUT, f"Selector loads zero tests or fails to import: {name}"
            )
    return {name: list(ids) for name, ids in listed.items()}


def judge_unittest(output: str, expected: int, code: int) -> str | None:
    match = re.search(r"^Ran (\d+) tests? in ", output, re.MULTILINE)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if code != 0 or match is None or not lines or lines[-1] != "OK":
        return "tests did not finish with a plain OK (failure, error or skip)"
    if int(match.group(1)) != expected or expected == 0:
        return f"ran {match.group(1)} tests, listed {expected}"
    return None


def docker_query(*args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env={"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")},
        check=False,
    )
    return result.returncode, result.stdout


def refuse(reason: str) -> PreflightError:
    return PreflightError(EXIT_PREREQ, f"Refusing SQL tests: {reason}")


def refuse_sql_execution() -> PreflightError:
    """SQL admission is closed: no trusted, lifetime-bound target mechanism exists (issue #1830).

    The helpers below correlate daemon-reported metadata with kernel process and listener
    tables. That is necessary but not sufficient: it does not authenticate the process that
    accepts on the Docker socket (a root-created socket can be handed to an unprivileged
    acceptor) and it does not pin the listener across discovery and every later connection
    (a released port can be rebound before or between connections). A post-run recheck is
    too late. Admission stays closed until a trusted host-side broker binds both.
    """
    return refuse(
        "SQL execution is disabled: the Docker acceptor is not authenticated and the SQL "
        "listener is not pinned through discovery and every connection, so no endpoint can "
        "be trusted. Use a disposable container through the full gate; the live SQL "
        "criterion of issue #1830 is not met"
    )


def refuse_selected_code_execution(*selections: list[str]) -> None:
    """Refuse every request that would import or run repository-controlled code (issue #1830).

    Unit and browser-test selectors, browser checks and SQL selectors all import selected
    modules, `load_tests` hooks, package initializers or `__main__` code, in discovery as well
    as in a run, and a selector may name any zero-argument callable. No positive dependency or
    capability proof exists for Python, and no runtime isolation is available without
    privileges (unprivileged namespaces are not guaranteed and no sandbox is installed).
    Textual denylists, environment scrubbing and rechecks do not bound that code, so this
    runs before the first subprocess, including git, and covers --dry-run.
    """
    if any(selections):
        raise PreflightError(
            EXIT_PREREQ,
            "Refusing to run: selected tests, browser wrappers and browser checks execute "
            "repository-controlled code on import, discovery and run, and neither a verified "
            "capability policy nor runtime isolation exists to bound it. Nothing was imported "
            "or run. Change-specific unit, browser and SQL preflight feedback of issue #1830 "
            "is not delivered; use the full gate",
        )


def socket_peer(path: str) -> int:
    """Uid of the process that created the listening socket; sends no request.

    This is the creator, not the acceptor: a root-created socket can be handed to an
    unprivileged service, so it cannot authenticate who answers requests.
    """
    with socket.socket(socket.AF_UNIX) as probe:
        probe.settimeout(5)
        probe.connect(path)
        _, uid, _ = struct.unpack(
            "3i",
            probe.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i")),
        )
    return uid


def trusted_socket(path: str) -> str:
    """Resolve the Docker socket and require root ownership of it and of every parent.

    Necessary but insufficient: it does not identify the process accepting connections.
    """
    if not os.path.isabs(path):
        raise refuse("Docker socket path is not absolute")
    real = Path(os.path.realpath(path))
    try:
        found = real.lstat()
        parents = [item.lstat() for item in real.parents]
    except OSError:
        raise refuse("Docker socket is not readable") from None
    if not stat.S_ISSOCK(found.st_mode) or found.st_uid != 0 or found.st_mode & 0o002:
        raise refuse("Docker socket is not a root-owned socket")
    if any(item.st_uid != 0 or item.st_mode & 0o022 for item in parents):
        raise refuse("Docker socket directory is writable by a non-root user")
    try:
        if socket_peer(str(real)) != 0:
            raise refuse("Docker socket was not created by root (possible proxy)")
    except OSError:
        raise refuse("Docker socket is not connectable") from None
    return str(real)


def local_docker_daemon() -> str:
    """Return the pinned unix endpoint after refusing remote, user-owned or proxied sockets."""
    if any(os.environ.get(name) for name in DOCKER_REMOTE_ENV):
        raise refuse("Docker host or context variables set")
    try:
        if Path(PROC / "self/uid_map").read_text().split() != ["0", "0", "4294967295"]:
            raise refuse("not in the initial user namespace, so uids cannot be trusted")
    except OSError:
        raise refuse("user namespace mapping is unreadable") from None
    code, output = docker_query("context", "inspect")
    try:
        host = json.loads(output)[0]["Endpoints"]["docker"]["Host"]
        parts = urlsplit(host)
    except (ValueError, KeyError, IndexError, TypeError):
        parts = None
    if (
        code != 0
        or parts is None
        or parts.scheme != "unix"
        or parts.netloc
        or parts.query
        or parts.fragment
    ):
        raise refuse("Docker is not a local unix socket")
    return "unix://" + trusted_socket(parts.path)


def owner_uid(path: Path) -> int:
    return path.stat().st_uid


def process_facts(proc: Path, pid: str) -> tuple[Any, ...] | None:
    """Stable identity of a process, or None when it vanished or cannot be read."""
    comm = ""
    try:
        raw = (proc / pid / "stat").read_text()
        comm = raw[raw.index("(") + 1 : raw.rindex(")")]
        rest = raw[raw.rindex(")") + 2 :].split()
        uid = owner_uid(proc / pid)
        if comm not in ("dockerd", "docker-proxy"):
            return None
        argv = tuple((proc / pid / "cmdline").read_bytes().decode(errors="replace").split("\0"))
    except (OSError, ValueError, IndexError):
        # A vanished or unreadable unrelated process is skipped; a Docker one never is.
        if comm in ("dockerd", "docker-proxy"):
            raise refuse("a Docker process could not be read") from None
        return None
    return (pid, comm, int(rest[1]), rest[19], uid, argv)


def candidates(proc: Path) -> list[tuple[Any, ...]]:
    found = [
        facts
        for entry in proc.iterdir()
        if entry.name.isdigit() and (facts := process_facts(proc, entry.name))
    ]
    return sorted(found, key=lambda item: int(item[0]))


def tcp_listeners(proc: Path, port: int) -> list[tuple[str, int, int]]:
    result = []
    for name in ("tcp", "tcp6"):
        try:
            lines = (proc / "net" / name).read_text().splitlines()[1:]
        except FileNotFoundError:
            continue
        except OSError:
            raise refuse("TCP listener table is unreadable") from None
        for line in lines:
            fields = line.split()
            if len(fields) > 9 and fields[3] == "0A":
                address, _, wanted = fields[1].rpartition(":")
                if int(wanted, 16) == port:
                    result.append((address, int(fields[7]), int(fields[9])))
    return result


def proxy_options(argv: tuple[str, ...]) -> dict[str, str]:
    result: dict[str, str] = {}
    for index, token in enumerate(argv[1:-1], start=1):
        following = argv[index + 1]
        if token.startswith("-") and not following.startswith("-"):
            result[token] = following
    return result


def verify_local_target(port: int, addresses: set[str], proc: Path | None = None) -> None:
    """Refuse unless the loopback listener looks like a root docker-proxy of the local dockerd.

    Evidence is read from the kernel, never from the Docker endpoint, because a proxied
    endpoint can return consistent fabricated metadata. It correlates process names, argv and
    addresses only: it does not prove the listener inode, network namespace or executable
    belong to the inspected container, and it holds nothing across later connections.
    """
    proc = PROC if proc is None else proc
    before = candidates(proc)
    daemons = [item for item in before if item[1] == "dockerd"]
    proxies = [item for item in before if item[1] == "docker-proxy"]
    if len(daemons) != 1 or daemons[0][4] != 0 or Path(daemons[0][5][0]).name != "dockerd":
        raise refuse("there is not exactly one root dockerd on this host")
    listeners = tcp_listeners(proc, port)
    if len(listeners) != 1 or listeners[0][0] != "0100007F" or listeners[0][1] != 0:
        raise refuse("the SQL port has no single root-owned 127.0.0.1 listener")
    if not listeners[0][2]:
        raise refuse("the SQL listener has no socket inode")
    matching = [
        item
        for item in proxies
        if (options := proxy_options(item[5])).get("-proto") == "tcp"
        and options.get("-host-ip") == "127.0.0.1"
        and options.get("-host-port") == str(port)
    ]
    if len(matching) != 1:
        raise refuse("the SQL port is not held by exactly one docker-proxy")
    proxy = matching[0]
    options = proxy_options(proxy[5])
    if (
        proxy[4] != 0
        or Path(proxy[5][0]).name != "docker-proxy"
        or proxy[2] != int(daemons[0][0])
        or options.get("-container-port") != "1433"
        or options.get("-container-ip") not in addresses
    ):
        raise refuse("the listener is not the local dockerd proxy of the inspected container")
    if candidates(proc) != before:
        raise refuse("Docker processes changed while they were inspected")


def utc_now() -> datetime:
    return datetime.now(UTC)


def docker_time(value: object) -> datetime:
    moment = datetime.fromisoformat(re.sub(r"(\.\d{6})\d+", r"\1", str(value)))
    if moment.tzinfo is None:
        raise ValueError("timestamp without a zone")
    return moment


def fresh_disposable(metadata: dict[str, Any], image: dict[str, Any]) -> bool:
    """True only for a recently created container with no mounts and a registry image."""
    host = metadata["HostConfig"]
    created = docker_time(metadata["Created"])
    started = docker_time(metadata["State"]["StartedAt"])
    now = utc_now()
    digests = image["RepoDigests"]
    return (
        metadata["Mounts"] == []
        and not host["Binds"]
        and not host.get("Mounts")
        and not host.get("VolumesFrom")
        and host["RestartPolicy"]["Name"] in ("", "no")
        and now - MAX_CONTAINER_AGE <= created <= started <= now + CLOCK_SKEW
        and IMAGE_ID.fullmatch(metadata["Image"]) is not None
        and image["Id"] == metadata["Image"]
        and isinstance(digests, list)
        and bool(digests)
        and all(str(item).startswith(MSSQL_DIGEST) for item in digests)
    )


def owned_container(container: str, owner: str) -> None:
    """Metadata and listener correlation for a future trusted mechanism; not reachable today.

    A pass is not proof of ownership or of a stable endpoint (see refuse_sql_execution).
    """
    env = os.environ
    for name in (
        "ZF_TEST_MSSQL",
        "ZF_SQL_SERVER",
        "ZF_SQL_PORT",
        "ZF_SQL_DATABASE",
        "ZF_SQL_AUTH",
        "ZF_SQL_USER",
        "ZF_SQL_PASSWORD",
    ):
        if not env.get(name):
            raise PreflightError(EXIT_PREREQ, f"SQL selectors need {name} set by the caller")
    if (
        env["ZF_TEST_MSSQL"] != "1"
        or env["ZF_SQL_SERVER"] != "127.0.0.1"
        or env["ZF_SQL_AUTH"] != "password"
        or env["ZF_SQL_USER"] != "sa"
        or not env["ZF_SQL_DATABASE"].startswith("rpi_")
        or not env["ZF_SQL_PORT"].isdigit()
    ):
        raise PreflightError(
            EXIT_PREREQ,
            "SQL selectors need ZF_TEST_MSSQL=1, server 127.0.0.1, password auth as sa, "
            "a database named rpi_* and a numeric port",
        )
    if not OWNER.fullmatch(owner):
        raise PreflightError(EXIT_INPUT, "--sql-owner must be the owner token of your container")
    if not CONTAINER.fullmatch(container):
        raise PreflightError(EXIT_INPUT, "--sql-container must be a 64 character container id")
    host = local_docker_daemon()
    code, output = docker_query("--host", host, "inspect", container)
    try:
        metadata = json.loads(output)[0]
        image_code, image_output = (
            docker_query("--host", host, "image", "inspect", metadata["Image"])
            if IMAGE_ID.fullmatch(str(metadata["Image"]))
            else (1, "")
        )
        code = code or image_code
        image = json.loads(image_output)[0]
        bindings = metadata["NetworkSettings"]["Ports"].get("1433/tcp")
        labels = metadata["Config"].get("Labels") or {}
        secrets = [
            item.partition("=")[2]
            for item in metadata["Config"].get("Env") or []
            if item.startswith("MSSQL_SA_PASSWORD=")
        ]
        owned = (
            metadata["Id"] == container
            and metadata["State"]["Running"]
            and labels.get("ama.rpi.owner") == owner
            and str(metadata["Config"]["Image"]).startswith(MSSQL_IMAGE)
            and fresh_disposable(metadata, image)
            and len(secrets) == 1
            and hmac.compare_digest(secrets[0].encode(), env["ZF_SQL_PASSWORD"].encode())
            and bindings
            and len(bindings) == 1
            and bindings[0]["HostIp"] == "127.0.0.1"
            and bindings[0]["HostPort"] == env["ZF_SQL_PORT"]
        )
        network = metadata["NetworkSettings"]
        addresses = {
            str(item["IPAddress"])
            for item in [network, *(network.get("Networks") or {}).values()]
            if item.get("IPAddress")
        }
    except (ValueError, KeyError, IndexError, TypeError, AttributeError):
        owned = False
        addresses = set()
    if code != 0 or not owned or not addresses:
        raise PreflightError(
            EXIT_PREREQ,
            "Refusing destructive SQL tests: container is not a running, labelled, local, "
            "loopback-only, recently created mssql container with no mounts and a registry "
            "image, bound to ZF_SQL_PORT and ZF_SQL_PASSWORD",
        )
    verify_local_target(int(env["ZF_SQL_PORT"]), addresses)


class heavy_lock:
    def __init__(self, timeout: int) -> None:
        self.timeout = timeout
        self.stream: Any = None

    def __enter__(self) -> Self:
        fd = os.open(HEAVY_LOCK_PATH, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        self.stream = os.fdopen(fd, "w")
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                fcntl.flock(self.stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    self.stream.close()
                    raise PreflightError(
                        EXIT_PREREQ,
                        "Heavy-resource lock is held by another owner; not queued",
                    ) from None
                time.sleep(0.5)

    def __exit__(self, *_: object) -> None:
        self.stream.close()


def digest_tree(repo: Path, skip: list[Path]) -> dict[str, str]:
    listed: set[str] = set()
    for args in (
        ("ls-files", "--cached", "--others", "--exclude-standard", "-z"),
        ("ls-files", "--others", "--ignored", "--exclude-standard", "-z"),
    ):
        listed.update(item.decode() for item in git(repo, *args).split(b"\0") if item)
    result = {}
    for name in sorted(listed):
        path = repo / name
        if any(path.is_relative_to(item) for item in skip):
            continue
        if path.is_symlink():
            result[name] = "link:" + os.readlink(path)
        elif path.is_file():
            hasher = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1 << 20), b""):
                    hasher.update(block)
            result[name] = hasher.hexdigest()
    result[".git-status"] = hashlib.sha256(
        git(repo, "status", "--porcelain=v1", "-z", "--ignored")
    ).hexdigest()
    return result


def mutated(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(
        name for name in before.keys() | after.keys() if before.get(name) != after.get(name)
    )


def check_out_dir(repo: Path, out: Path) -> Path:
    resolved = out.resolve()
    if resolved.is_relative_to(repo) or repo.is_relative_to(resolved):
        raise PreflightError(EXIT_INPUT, "--out must be outside the repository")
    if len(str(resolved).encode()) > OUT_BYTES:
        raise PreflightError(EXIT_INPUT, f"--out must be at most {OUT_BYTES} bytes")
    if (resolved / "receipt.json").exists():
        raise PreflightError(EXIT_INPUT, "--out must not contain a receipt.json")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def browser_check_args(
    repo: Path, name: str, known: set[str], axe: Path | None, out: Path | None
) -> list[str]:
    if not CHECK.fullmatch(name):
        raise PreflightError(EXIT_INPUT, f"Invalid browser check name: {name!r}")
    relative = repo_relative(repo, f"src/api/checks/{name}.py", known)
    source = (repo / relative).read_text()
    extra: list[str] = []
    if '"--axe"' in source:
        if axe is None or not axe.is_file():
            raise PreflightError(EXIT_INPUT, f"{name} needs --axe pointing at the pinned axe file")
        if hashlib.sha256(axe.read_bytes()).hexdigest() != AXE_SHA256:
            raise PreflightError(EXIT_INPUT, "--axe does not match the pinned axe 4.10.3 digest")
        extra += ["--axe", str(axe.resolve())]
    if '"--out"' in source:
        if out is None:
            raise PreflightError(EXIT_INPUT, f"{name} needs --out")
        target = out / name
        target.mkdir(exist_ok=True)
        extra += ["--out", str(target)]
    return extra


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--file", action="append", default=[], dest="files")
    parser.add_argument("--covers", action="append", default=[])
    parser.add_argument("--test", action="append", default=[])
    parser.add_argument("--browser-test", action="append", default=[])
    parser.add_argument("--sql-test", action="append", default=[])
    parser.add_argument("--sql-container")
    parser.add_argument("--sql-owner")
    parser.add_argument("--browser-check", action="append", default=[])
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--allow-uncovered", action="store_true")
    parser.add_argument("--lock-timeout", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def execute(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    if not (args.test or args.browser_test or args.sql_test or args.browser_check):
        raise PreflightError(EXIT_INPUT, "Name at least one selector or browser check")
    refuse_selected_code_execution(args.test, args.browser_test, args.sql_test, args.browser_check)
    repo = args.repo.resolve()
    if repo != Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve():
        raise PreflightError(EXIT_INPUT, "--repo must be a repository root")
    known = tracked_or_intended(repo)
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    unit, browser_units, sql_units = args.test, args.browser_test, args.sql_test
    selectors = {
        value: parse_selector(repo, value, known) for value in unit + browser_units + sql_units
    }
    files = [repo_relative(repo, value, known) for value in args.files]
    browser_names = list(args.browser_check)
    targets = set(selectors) | set(browser_names)
    covers = parse_covers(args.covers, set(files), targets)
    uncovered = assess_coverage(
        files,
        covers,
        {value: project for value, (project, _) in selectors.items()},
        set(browser_units) | set(browser_names),
        set(sql_units),
    )
    result: dict[str, Any] = {
        "kind": "rpi-preflight",
        "receipt": False,
        "label": LABEL,
        "head": head,
        "files": files,
        "targets": sorted(targets),
        "uncovered": uncovered,
        "coverage_note": "declared coverage, relevance not verified; " + GATE_ONLY,
        "full_gate_required": True,
        "commands": [],
        "dry_run": args.dry_run,
    }
    if uncovered and not args.allow_uncovered:
        return EXIT_UNCOVERED, result
    needs_lock = bool(browser_units or browser_names)
    if sql_units:
        raise refuse_sql_execution()
    check_interpreter(args.python, repo)
    out = check_out_dir(repo, args.out) if args.out else None
    temporary = None if out else Path(tempfile.mkdtemp(prefix="rpi-preflight-"))
    scratch = out or temporary
    assert scratch is not None
    skip = [scratch]
    try:
        groups = [
            ("unit", unit, {}),
            ("browser-test", browser_units, {"ZF_BROWSER_TESTS": "1"}),
        ]
        extra_args = [
            browser_check_args(repo, name, known, args.axe, out) for name in browser_names
        ]
        if browser_names or browser_units:
            probe = subprocess.run(
                [str(args.python), "-c", CHROMIUM_PROBE],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
                env=scrubbed_env(scratch, {}),
                check=False,
            )
            if probe.returncode != 0 or not Path(probe.stdout.strip()).exists():
                raise PreflightError(EXIT_PREREQ, "Chromium is not installed for --python")
        before = digest_tree(repo, skip)
        failed = False
        refusal: PreflightError | None = None
        try:
            lock = heavy_lock(args.lock_timeout) if needs_lock and not args.dry_run else None
            if lock:
                lock.__enter__()
            try:
                for kind, values, extra in groups:
                    for project in PROJECTS:
                        names = [selectors[v][1] for v in values if selectors[v][0] == project]
                        if not names:
                            continue
                        env = scrubbed_env(
                            scratch, test_environment(repo, tests_dirs(project)) | extra
                        )
                        listed = list_tests(args.python, repo, project, names, env)
                        count = sum(len(ids) for ids in listed.values())
                        entry: dict[str, Any] = {
                            "kind": kind,
                            "project": project,
                            "selectors": names,
                            "tests_listed": count,
                        }
                        if not args.dry_run:
                            argv = [str(args.python), "-m", "unittest", "-v", *names]
                            code, output, seconds, timed_out = run(
                                argv, repo / "src" / project, env, args.timeout
                            )
                            reason = (
                                "timed out" if timed_out else judge_unittest(output, count, code)
                            )
                            entry |= {
                                "argv": argv,
                                "exit": code,
                                "seconds": round(seconds, 1),
                            }
                            entry["failure"] = reason
                            entry["tail"] = output[-1500:] if reason else ""
                            failed |= reason is not None
                        result["commands"].append(entry)
                for name, extra_argv in zip(browser_names, extra_args, strict=True):
                    env = scrubbed_env(
                        scratch,
                        {
                            "ZF_BROWSER_TESTS": "1",
                            "PYTHONDONTWRITEBYTECODE": "1",
                            "PYTHONPATH": ":".join(
                                str(repo / "src/api" / item)
                                for item in (
                                    "tests",
                                    "../core/tests",
                                    "../agents/tests",
                                )
                            ),
                        },
                    )
                    argv = [
                        str(args.python),
                        "-c",
                        BROWSER_ENTRY,
                        f"checks.{name}",
                        *extra_argv,
                    ]
                    entry = {"kind": "browser-check", "check": name, "argv": argv}
                    if not args.dry_run:
                        code, output, seconds, timed_out = run(
                            argv, repo / "src" / "api", env, args.timeout
                        )
                        reason = (
                            "timed out" if timed_out else (None if code == 0 else "check failed")
                        )
                        entry |= {
                            "exit": code,
                            "seconds": round(seconds, 1),
                            "failure": reason,
                        }
                        entry["tail"] = output[-1500:] if reason else output[-400:]
                        failed |= reason is not None
                    result["commands"].append(entry)
            finally:
                if lock:
                    lock.__exit__()
        except PreflightError as error:
            refusal = error
        changed = mutated(before, digest_tree(repo, skip))
        result["source_mutations"] = changed
        if refusal is not None:
            result["refusal"] = str(refusal)
        if changed:
            return EXIT_MUTATION, result
        if refusal is not None:
            raise refusal
        if failed:
            return EXIT_FAIL, result
        if args.dry_run:
            return EXIT_NOT_RUN, result
        return (EXIT_UNCOVERED if uncovered else EXIT_PASS), result
    finally:
        if temporary is not None:
            shutil.rmtree(temporary, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        code, result = execute(args)
    except PreflightError as error:
        print(f"{LABEL}\nREFUSED ({error.code}): {error}", file=sys.stderr)
        return error.code
    partial = bool(result["uncovered"])
    result["status"] = (
        "pass" if code == EXIT_PASS and not partial and not args.dry_run else "not-pass"
    )
    result["exit"] = code
    print(LABEL)
    for entry in result["commands"]:
        print(
            f"  {entry['kind']}: {entry.get('project') or entry.get('check')} "
            f"listed={entry.get('tests_listed', '-')} exit={entry.get('exit', 'dry-run')}"
            + (f" FAILURE: {entry['failure']}" if entry.get("failure") else "")
        )
    for name in result.get("source_mutations", []):
        print(f"  SOURCE MUTATED: {name}")
    if "refusal" in result:
        print(f"  REFUSED ({result['refusal']})")
    for item in result["uncovered"]:
        print(f"  UNCOVERED {item['path']}: {item['reason']}")
    if partial and args.allow_uncovered:
        print("  WARNING: uncovered paths allowed; this is not a pass.")
    print(f"  {result['coverage_note']}")
    print(f"  result: {result['status']} (exit {code}); the full gate is still required")
    if args.out:
        (args.out.resolve() / "preflight-result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n"
        )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
