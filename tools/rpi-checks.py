#!/usr/bin/env python3
"""Run full or changed-path local checks and verify scoped exact-commit receipts."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import secrets
import shutil
import signal
import stat
import subprocess
import sys
import threading
import time
from collections.abc import Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.request import urlopen

PROJECTS = ("core", "agents", "api", "orchestrator", "importer")
IMAGES = ("api", "agents", "orchestrator", "importer")
SQL_SELECTORS = (
    "test_mssqlstore",
    "test_lawstore.MssqlStoreTests",
    "test_assistants.MssqlContractTests",
    "test_assistants.MssqlReviewTests",
    "test_assistants.MssqlDurabilityTests",
    "test_assistants.MssqlApiTests",
    "test_assistants.MssqlLedgerTests",
    "test_resident_aoai_sql.AccountingSqlTests",
)
RUFF_GROUPS = (
    ("infra/tests/test_bicep_policy.py", "infra/tests/test_deploy.py", "infra/scripts/deploy.py"),
    ("infra/scripts/pipeline.py", "infra/tests/test_pipeline.py"),
    (
        "infra/scripts/staff_azure.py",
        "infra/scripts/staff_blob.py",
        "infra/scripts/staff-azure-worker.py",
        "infra/scripts/credential_arm.py",
        "infra/tests/test_staff_azure.py",
    ),
    ("src/check-container.py", "infra/tests/test_container_contract.py"),
    ("tools/rpi-checks.py", "tools/test_rpi_checks.py"),
)
WORKFLOWS = ("src-ci.yml", "mvp-ci.yml", "mvp-validation.yml", "src-deploy.yml", "infra-plan.yml")
# Explicitly updated with the matrix whenever native workflow commands change.
WORKFLOW_HASHES = {
    "src-ci.yml": "09254836b5575acfe05efb8f77ced0989dda5c0ae8e63a8f1a3d33d3b1509379",
    "mvp-ci.yml": "92178fff316a4cd8b4e619c47e96c0238106c311cad928263b6e795797a3a54e",
    "mvp-validation.yml": "94feeb7e0c6807a94dc2624eaf7c5e76c807a234e1777b593b169fd801e511cc",
    "src-deploy.yml": "3c2f1ed59b1486fc1316a48207cc4ef7d6a830bbba1dcad4152acab4bd2f1bbc",
    "infra-plan.yml": "4240d803e33e68e63e03d201f241fa21101e2e260848c276b32817624cca6056",
}
AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
TOOLS = ("python3", "node", "docker", "az", "bicep", "actionlint", "shellcheck", "trivy")
HEAVY_LOCK_PATH = Path("/tmp/ama-rpi-heavy.lock")
# Linux sun_path[108] includes NUL; Chromium adds this mkdtemp/socket suffix to TMPDIR.
CHROMIUM_SOCKET_PATH_BYTES = 107
CHROMIUM_SOCKET_SUFFIX = "/org.chromium.Chromium.XXXXXX/SingletonSocket"
EXPECTED_SKIP_REASONS = {
    "needs a SQL Server (ZF_TEST_MSSQL=1)",
    "needs disposable SQL Server (ZF_TEST_MSSQL=1)",
    "needs task-owned SQL Server",
    "opt-in loopback SQL Server",
    "opt-in loopback MSSQL",
    "owned local MSSQL opt-in",
    "Opt-in task-owned MSSQL",
    "opt-in own local SQL",
    "opt-in task-owned loopback SQL",
    "opt-in local SQL Server",
    "opt-in isolated local SQL Server",
    "opt-in owned loopback SQL Server",
    "opt-in local Playwright",
    "opt-in Chromium journey",
    "opt-in local Chromium",
    "Chromium is installed by the later browser-check step",
    "opt-in local browser",
    "JSON-only separate-file audit ordering",
    "SQL writer dependency checks",
    "JSON file rollback only",
    "JSON does not have a SQL COMMIT acknowledgement boundary.",
    "Opt-in rendered check requires local Playwright browser.",
    "requires owned loopback SQL Server",
    "Explicit isolated synthetic Azure SQL database required",
}
CHAT_PANEL_BROWSER_SELECTOR = (
    "test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log"
)
CHAT_PANEL_DISCOVERY_SKIP = (
    f"{CHAT_PANEL_BROWSER_SELECTOR.rsplit('.', 1)[1]} ({CHAT_PANEL_BROWSER_SELECTOR})",
    "opt-in local Chromium",
)
EMPLOYEE_ACCEPTANCE_BROWSER_MODULE = "checks.employee_acceptance_check"
EMPLOYEE_ACCEPTANCE_BROWSER_PATHS = (
    ".:src:tests:../core/src:../agents/src:../core/tests:../agents/tests"
)
SQL_NOT_APPLICABLE = {
    (
        "test_json_postsave_audit_failure_reports_persisted_uncertainty "
        "(test_mssqlstore.MssqlHazardReferral."
        "test_json_postsave_audit_failure_reports_persisted_uncertainty)",
        "JSON-only separate-file audit ordering",
    )
}
TYPE_GROUPS = (
    ("--strict", "src/check-container.py"),
    ("--strict", "infra/scripts/pipeline.py"),
    ("--strict", "tools/rpi-checks.py", "tools/test_rpi_checks.py"),
    (
        "--follow-imports=silent",
        "--ignore-missing-imports",
        "infra/scripts/staff_azure.py",
        "infra/scripts/staff_blob.py",
        "infra/scripts/staff-azure-worker.py",
        "infra/scripts/credential_arm.py",
    ),
)
WORKFLOW_INVENTORY = (
    "import json,yaml,sys; from pathlib import Path; "
    "print(json.dumps({name:yaml.load(Path('.github/workflows',name).read_text(),"
    "Loader=yaml.BaseLoader)['jobs'] for name in sys.argv[1:]}))"
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
REGULATORY_ASSERT = (
    "from pathlib import Path; import json,sys; "
    "r=json.loads(Path(sys.argv[1]).read_text()); "
    "assert 'skipped' not in json.dumps(r)"
)
SQL_DRIVER = (
    "import ctypes; ctypes.CDLL('libltdl.so.7'); ctypes.CDLL('libkrb5.so.3'); import mssql_python"
)
SQL_QUERY = (
    "import os,time; from zava_forward.core.mssqlstore import _Conn,connection_string; "
    "db=_Conn(connection_string(dict(os.environ,ZF_SQL_DATABASE='master'))); "
    "assert db.execute('SELECT 1').fetchone()[0]==1; "
    "db.execute('CREATE DATABASE rpi_disposable'); db.close()"
)


class GateError(RuntimeError):
    """Required evidence is absent or invalid."""


def admit_browser_output(out: Path, groups: list[str]) -> None:
    if "browser" not in groups:
        return
    tmp = out / "tmp"
    tmp_bytes = len(os.fsencode(tmp))
    tmp_limit = CHROMIUM_SOCKET_PATH_BYTES - len(os.fsencode(CHROMIUM_SOCKET_SUFFIX))
    out_limit = tmp_limit - len(os.fsencode("/tmp"))
    if tmp_bytes > tmp_limit:
        raise GateError(
            f"Chromium singleton socket path would exceed {CHROMIUM_SOCKET_PATH_BYTES} bytes: "
            f"resolved --out is {len(os.fsencode(out))} bytes (maximum {out_limit}), "
            f"owned TMPDIR is {tmp_bytes} bytes (maximum {tmp_limit}). "
            "Use a shorter new external --out, for example /tmp/rpi-608-final; "
            "the runner sets TMPDIR to <output>/tmp, overriding caller TMPDIR."
        )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def clean_identity(root: Path, base: str) -> dict[str, str]:
    if any(line and not line.startswith("H ") for line in git(root, "ls-files", "-v").splitlines()):
        raise GateError("Candidate index hides inputs with assume-unchanged/skip-worktree flags")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise GateError("Candidate has tracked modifications or untracked inputs")
    if git(root, "ls-files", "--others", "--ignored", "--exclude-standard"):
        raise GateError("Candidate has ignored inputs; move all scratch outside the checkout")
    head = git(root, "rev-parse", "HEAD")
    resolved = git(root, "rev-parse", f"{base}^{{commit}}")
    if resolved != git(root, "rev-parse", "refs/remotes/origin/main"):
        raise GateError(
            "Reviewed base differs from current origin/main; reconcile before validation"
        )
    merge_base = git(root, "merge-base", head, resolved)
    if merge_base != resolved:
        raise GateError("Candidate does not descend from the reviewed main base")
    return {
        "head": head,
        "tree": git(root, "rev-parse", "HEAD^{tree}"),
        "base": resolved,
        "merge_base": merge_base,
        "matrix": digest(root / "tools/rpi-checks.py"),
        "helper": digest(root / "src/check-container.py"),
    }


def tool_identity() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for name in TOOLS:
        path = shutil.which(name)
        if not path:
            raise GateError(f"Missing required tool: {name}")
        result[name] = {"sha256": digest(Path(path).resolve())}
    result["docker-server"] = {
        "version": subprocess.check_output(
            ["docker", "version", "--format={{.Server.Version}}"], text=True
        ).strip()
    }
    return result


def environment_identity(out: Path, names: list[str] | None = None) -> dict[str, str]:
    """Hash bounded environment data without executing Python or loading startup code."""
    result: dict[str, str] = {}
    if names == []:
        return result
    venvs = out / "venvs"
    if venvs.is_symlink() or not venvs.is_dir():
        raise GateError("Missing or symlinked environment directory")
    for name in names if names is not None else (*PROJECTS, "namespace"):
        environment = venvs / name
        site = environment / "lib/python3.12/site-packages"
        entries = 0
        total = 0

        def children(directory: Path) -> list[Path]:
            nonlocal entries
            if directory.is_symlink() or not directory.is_dir():
                raise GateError("Missing or symlinked environment metadata directory")
            paths = []
            for child in directory.iterdir():
                entries += 1
                if entries > 4096:
                    raise GateError("Environment metadata entry limit exceeded")
                paths.append(child)
            return sorted(paths)

        def record(path: Path, *, interpreter: bool = False) -> dict[str, Any]:
            nonlocal total
            if interpreter and path.is_symlink():
                # Bind link text, never follow a receipt-controlled interpreter target.
                target = os.readlink(path)
                if len(target) > 4096:
                    raise GateError("Environment interpreter link limit exceeded")
                return {"link": target}
            if path.is_symlink():
                raise GateError("Symlinked package/startup metadata is not permitted")
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(stream.fileno())
                limit = 64 * 1024 * 1024 if interpreter else 8 * 1024 * 1024
                if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                    raise GateError("Environment metadata must be bounded regular files")
                content = stream.read(limit + 1)
                total += len(content)
                if len(content) > limit or total > 128 * 1024 * 1024:
                    raise GateError("Environment metadata byte limit exceeded")
            return {
                "mode": stat.S_IMODE(info.st_mode),
                "sha256": hashlib.sha256(content).hexdigest(),
            }

        def metadata(directory: Path, depth: int = 0) -> dict[str, Any]:
            if depth > 8:
                raise GateError("Environment metadata depth limit exceeded")
            records = {}
            for path in children(directory):
                if path.is_symlink():
                    raise GateError("Symlinked package/startup metadata is not permitted")
                if path.is_dir():
                    records[path.name] = metadata(path, depth + 1)
                else:
                    records[path.name] = record(path)
            return records

        for directory in (environment, environment / "lib", site.parent):
            if directory.is_symlink() or not directory.is_dir():
                raise GateError("Missing or symlinked environment directory")
        packages = {"pyvenv.cfg": record(environment / "pyvenv.cfg")}
        interpreters = [p for p in children(environment / "bin") if p.name.startswith("python")]
        if not any(p.name == "python" for p in interpreters):
            raise GateError("Environment interpreter identity is missing")
        for path in interpreters:
            packages[str(path.relative_to(environment))] = record(path, interpreter=True)
        startup = {}
        distributions = 0
        for path in children(site):
            if path.name.endswith(".dist-info"):
                distributions += 1
                records = metadata(path)
                if "METADATA" not in records:
                    raise GateError("Package distribution METADATA is missing")
                packages[str(path.relative_to(environment))] = records
            elif path.name.endswith((".pth", ".egg-link")) or path.name.startswith(
                ("sitecustomize.", "usercustomize.", "__editable__")
            ):
                startup[str(path.relative_to(environment))] = record(path)
            elif path.name == "__pycache__":
                for cached in children(path):
                    if cached.name.startswith(("sitecustomize.", "usercustomize.", "__editable__")):
                        startup[str(cached.relative_to(environment))] = record(cached)
        if not distributions:
            raise GateError("Environment package metadata is missing")
        for key, records in ((name, packages), (f"{name}-startup", startup)):
            result[key] = hashlib.sha256(
                json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
    return result


def image_build_argv(dockerfile: str, tag: str, context: str, *, fresh: bool) -> list[str]:
    # Scanned images skip the layer cache so apt-get upgrade always runs.
    return [
        "docker",
        "build",
        *(["--no-cache"] if fresh else []),
        "--memory=3g",
        "--cpu-quota=200000",
        "-f",
        dockerfile,
        "-t",
        tag,
        context,
    ]


def required_groups(extras: list[str]) -> list[str]:
    return [
        "preflight",
        *[f"project-{name}" for name in PROJECTS],
        "namespace",
        "static",
        "infra",
        "migration",
        "browser",
        "mssql",
        *[f"image-{name}" for name in IMAGES],
        "logo-0600",
        *[f"extra-{value}" for value in extras],
    ]


def dependencies(group: str) -> set[str]:
    if group in ("static", "tooling", "infra", "migration", "logo-0600") or group.startswith(
        "image-"
    ):
        return {"namespace"}
    if group in ("browser", "mssql"):
        return {"project-api"}
    if group.startswith("extra-"):
        return {f"project-{extra_selector(group.removeprefix('extra-'))[0]}"}
    return set()


def changed_groups(paths: list[str], extras: list[str]) -> list[str]:
    selected = {"preflight", "static"}
    for value in extras:
        selected.add(f"extra-{value}")
    for path in paths:
        parts = Path(path).parts
        if path.endswith(".md") or path.startswith(("docs/", ".copilot-tracking/", "support/")):
            continue
        if path in ("tools/rpi-checks.py", "tools/test_rpi_checks.py"):
            selected.add("tooling")
        elif path.startswith("infra/"):
            selected.add("infra")
        elif len(parts) > 2 and parts[0] == "src" and parts[1] in PROJECTS:
            project = parts[1]
            consumers = (
                PROJECTS
                if project == "core"
                else ("agents", "api")
                if project == "agents"
                else (project,)
            )
            selected.update(f"project-{name}" for name in consumers)
            runtime = parts[2] == "src" or any(
                item in path.lower() for item in ("dockerfile", "requirements", "pyproject.toml")
            )
            if runtime:
                selected.update(f"image-{name}" for name in consumers if name in IMAGES)
                if "api" in consumers:
                    selected.add("logo-0600")
            if project == "api" and ("/web/" in path or parts[2] == "checks"):
                selected.add("browser")
            if project in ("core", "api") and (
                "requirements" in path.lower() or parts[2] == "pyproject.toml"
            ):
                selected.add("mssql")
            if any(word in path.lower() for word in ("store", "schema", "sql", "assistants")):
                selected.add("mssql")
        else:
            return required_groups(extras)
    while True:
        closed = selected | set().union(*(dependencies(group) for group in selected))
        if closed == selected:
            break
        selected = closed
    order = [*required_groups(extras), "tooling"]
    return [group for group in order if group in selected]


def selection(root: Path, base: str, mode: str, extras: list[str]) -> dict[str, Any]:
    if mode not in ("all", "changed"):
        raise GateError("Invalid selection mode")
    paths = []
    if mode == "changed":
        paths = (
            subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(root),
                    "diff",
                    "--no-renames",
                    "--name-only",
                    "-z",
                    f"{base}...HEAD",
                ]
            )
            .decode()
            .rstrip("\0")
            .split("\0")
        )
        paths = [path for path in paths if path]
    groups = required_groups(extras) if mode == "all" else changed_groups(paths, extras)
    return {"mode": mode, "paths": paths, "groups": groups}


def selected_environments(groups: list[str]) -> list[str]:
    names = set()
    for group in groups:
        if group == "namespace":
            names.add("namespace")
        elif group.startswith(("project-", "setup-")):
            names.add(group.split("-", 1)[1])
        elif group in ("browser", "mssql"):
            names.add("api")
        elif group.startswith("extra-"):
            names.add(extra_selector(group.removeprefix("extra-"))[0])
        elif dependencies(group) == {"namespace"}:
            names.add("namespace")
    return sorted(names)


def cgroup_directories() -> list[Path]:
    membership = next(
        (
            line[3:]
            for line in Path("/proc/self/cgroup").read_text().splitlines()
            if line.startswith("0::")
        ),
        None,
    )
    if membership is None or not membership.startswith("/") or ".." in Path(membership).parts:
        raise GateError("Cannot resolve effective cgroup-v2 membership")
    current = Path(membership)
    mounts = []

    def unescape(value: str) -> str:
        return re.sub(r"\\([0-7]{3})", lambda match: chr(int(match[1], 8)), value)

    for line in Path("/proc/self/mountinfo").read_text().splitlines():
        before, separator, after = line.partition(" - ")
        if not separator or after.split()[0] != "cgroup2":
            continue
        fields = before.split()
        root, mount = Path(unescape(fields[3])), Path(unescape(fields[4]))
        if current.is_relative_to(root):
            mounts.append((len(root.parts), mount, mount / current.relative_to(root)))
    if not mounts:
        raise GateError("Cannot resolve effective cgroup-v2 mount")
    _, mount, directory = max(mounts, key=lambda value: value[0])
    if not directory.is_dir():
        raise GateError("Effective cgroup directory is unavailable")
    return [directory, *[parent for parent in directory.parents if parent.is_relative_to(mount)]]


def worker_limit(requested: int) -> int:
    if requested < 1:
        raise GateError("--jobs must be positive")
    cpus = float(len(os.sched_getaffinity(0)))
    memory = re.search(
        r"^MemAvailable:\s+(\d+)\s+kB$",
        Path("/proc/meminfo").read_text(),
        re.MULTILINE,
    )
    if memory is None:
        raise GateError("Host available-memory capacity is unavailable")
    available = int(memory[1]) * 1024
    for directory in cgroup_directories():
        quota = directory / "cpu.max"
        if quota.exists():
            amount, period = quota.read_text().split()
            if amount != "max":
                if int(period) <= 0 or int(amount) <= 0:
                    raise GateError("Invalid cgroup CPU capacity")
                cpus = min(cpus, int(amount) / int(period))
        maximum = directory / "memory.max"
        if maximum.exists() and maximum.read_text().strip() != "max":
            available = min(
                available,
                int(maximum.read_text()) - int((directory / "memory.current").read_text()),
            )
    limit = min(requested, int(cpus // 2), (available - 1024**3) // (4 * 1024**3))
    if limit < 1:
        raise GateError(
            "Insufficient capacity: each worker needs 2 CPUs and 4 GiB plus 1 GiB headroom"
        )
    return limit


def test_paths(project: str, own_tests: bool = False) -> str:
    paths = []
    if own_tests:
        paths.append(f"<checkout>/src/{project}/tests")
    if project in ("api", "agents", "orchestrator"):
        paths.append("<checkout>/src/core/tests")
    if project == "api":
        paths.append("<checkout>/src/agents/tests")
    return ":".join(paths)


def required_checks(root: Path, receipt: dict[str, Any]) -> list[dict[str, Any]]:
    """Trusted ordered command contracts, never commands loaded for execution."""
    token, sql = receipt["owner"], receipt["sql"]
    groups = receipt.get("executed_groups", required_groups(receipt["extras"]))
    if (
        not isinstance(token, str)
        or re.fullmatch("[0-9a-f]{24}", token) is None
        or (
            "mssql" in groups
            and (
                re.fullmatch("[0-9a-f]{64}", sql["container"]) is None
                or not sql["port"].isdigit()
                or not 0 < int(sql["port"]) <= 65535
                or re.fullmatch("sha256:[0-9a-f]{64}", receipt["images"]["mssql"]) is None
            )
        )
    ):
        raise GateError("Receipt owned resource identity is invalid")
    result: list[dict[str, Any]] = []
    group = "preflight"

    def py(name: str) -> str:
        return f"<output>/venvs/{name}/bin/python"

    def add(
        argv: list[str],
        cwd: str = ".",
        *,
        env: dict[str, str] | None = None,
        timeout: int = 900,
        suite: bool = False,
        integration: bool = False,
        probe: bool = False,
        attempts: int = 1,
    ) -> None:
        result.append(
            {
                "group": group,
                "argv": argv,
                "cwd": cwd,
                "env": env or {},
                "timeout_seconds": timeout,
                "suite": suite,
                "integration": integration,
                "probe": probe,
                "attempts": attempts,
            }
        )

    def install(name: str, packages: list[str], dev: bool = True) -> None:
        add(["python3", "-m", "venv", f"<output>/venvs/{name}"])
        add([py(name), "-m", "pip", "check"])
        add([py(name), "-c", "import zava_forward"], probe=True)
        args = [py(name), "-m", "pip", "install"]
        for project in packages:
            args += ["-e", f"src/{project}" + ("[dev]" if dev and project == name else "")]
        add(args, timeout=1200)
        add([py(name), "-m", "pip", "check"])

    def lint(python: str, files: tuple[str, ...], cwd: str = ".") -> None:
        add(
            [
                python,
                "-m",
                "ruff",
                "check",
                "--isolated",
                "--select",
                "E,F,I,B,UP",
                "--target-version",
                "py312",
                "--line-length",
                "100",
                *files,
            ],
            cwd,
        )
        add(
            [
                python,
                "-m",
                "ruff",
                "format",
                "--isolated",
                "--line-length",
                "100",
                "--check",
                *files,
            ],
            cwd,
        )

    for argv in (
        ["python3", "--version"],
        ["node", "--version"],
        ["docker", "version"],
        ["az", "bicep", "version"],
        ["actionlint", "-version"],
        ["shellcheck", "--version"],
        ["trivy", "--version"],
    ):
        add(argv, timeout=60)
    for project in PROJECTS:
        group = f"project-{project}"
        packages = [] if project == "core" else ["core"]
        if project == "api":
            packages.append("agents")
        install(project, [*packages, project])
        python, cwd = py(project), f"src/{project}"
        add(
            [python, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd,
            env={"PYTHONPATH": test_paths(project)},
            suite=True,
            timeout=1800,
        )
        add([python, "-m", "ruff", "check", "."], cwd)
        add([python, "-m", "ruff", "format", "--check", "."], cwd)
        add([python, "-m", "mypy"], cwd)
    group = "namespace"
    install("namespace", list(PROJECTS), dev=False)
    python = py("namespace")
    for project in ("core", "agents", "orchestrator", "importer"):
        add([python, "-m", f"zava_forward.{project}"])
    add([python, "-c", "from zava_forward.api.version import __version__; print(__version__)"])
    add(
        [
            python,
            "-c",
            "import zava_forward; assert zava_forward.__file__ is None; "
            "assert len(list(zava_forward.__path__)) == 5",
        ]
    )
    group = "static"
    add(
        [
            python,
            "-m",
            "compileall",
            "-q",
            *[f"src/{p}/src" for p in ("core", "agents", "api", "orchestrator")],
        ]
    )
    for name in ("app", "assistants"):
        add(["node", "--check", f"src/api/src/zava_forward/api/web/{name}.js"])
    add(["git", "ls-files", "--", "*/.assistant-test-*", "mvp/data", ":(glob)src/**/data/**"])
    add(
        [
            "actionlint",
            "-config-file",
            "infra/tests/actionlint.yaml",
            *[f".github/workflows/{name}" for name in WORKFLOWS],
        ]
    )
    add(
        [python, "-m", "unittest", "discover", "-s", "tools", "-p", "test_rpi_checks.py", "-v"],
        suite=True,
    )
    group = "infra"
    add([python, "-c", "import yaml, mssql_python"], probe=True)
    add([python, "-m", "pip", "install", "PyYAML==6.0.3", "ruff==0.17.1", "mypy==2.4.0"])
    add([python, "-m", "pip", "install", "--require-hashes", "-r", "src/api/requirements.txt"])
    add([python, "-c", WORKFLOW_INVENTORY, *WORKFLOWS])
    for file in sorted([*root.glob("infra/*.bicep"), *root.glob("infra/modules/*.bicep")]):
        relative = str(file.relative_to(root))
        add(["az", "bicep", "build", "--file", relative, "--stdout"])
        add(["az", "bicep", "lint", "--file", relative])
    add(
        [python, "-m", "unittest", "discover", "-s", "infra/tests", "-v"],
        env={"REQUIRE_AZ_BICEP": "1"},
        suite=True,
        integration=True,
        timeout=1800,
    )
    for files in RUFF_GROUPS:
        lint(python, files)
    for type_files in TYPE_GROUPS:
        add([python, "-m", "mypy", *type_files])
    group = "migration"
    add([python, "-c", "import pptx"], probe=True)
    add([python, "-m", "pip", "install", "-r", "tools/rename-zava-requirements.txt"])
    add([python, "tools/rename-zava-tests.py"])
    group = "browser"
    python = py("api")
    for name in (
        "design_system_browser_check",
        "regulatory_ux_check",
        "case_journey_browser_check",
    ):
        lint(python, (f"checks/{name}.py",), "src/api")
    add([python, "-m", "playwright", "install", "chromium"])
    add(
        [python, "-m", EMPLOYEE_ACCEPTANCE_BROWSER_MODULE],
        "src/api",
        env={"PYTHONPATH": EMPLOYEE_ACCEPTANCE_BROWSER_PATHS},
        suite=True,
        integration=True,
    )
    add(
        [python, "-m", "unittest", "-v", CHAT_PANEL_BROWSER_SELECTOR],
        "src/api",
        env={"PYTHONPATH": test_paths("api", True), "ZF_BROWSER_TESTS": "1"},
        suite=True,
        integration=True,
    )
    add(
        [python, "-c", BROWSER_ENTRY, "checks.design_system_browser_check"],
        "src/api",
        env={"PYTHONPATH": "<output>/safety"},
    )
    add(
        [
            python,
            "-c",
            BROWSER_ENTRY,
            "checks.case_journey_browser_check",
            "--axe",
            "<output>/axe-4.10.3.min.js",
            "--out",
            "<output>/case-journey",
        ],
        "src/api",
        env={"PYTHONPATH": "<output>/safety:" + test_paths("api", True)},
    )
    add(
        [
            python,
            "-m",
            "checks.regulatory_ux_check",
            "--axe",
            "<output>/axe-4.10.3.min.js",
            "--out",
            "<output>/regulatory-ux-results.json",
        ],
        "src/api",
        env={"PYTHONPATH": test_paths("api", True)},
    )
    add([python, "-c", REGULATORY_ASSERT, "<output>/regulatory-ux-results.json"])
    group = "mssql"
    sql = sql if "mssql" in groups else {"container": "", "port": ""}
    add([python, "-m", "pip", "install", "--require-hashes", "-r", "src/api/requirements.txt"])
    add([python, "-c", SQL_DRIVER])
    add(["docker", "pull", "mcr.microsoft.com/mssql/server:2022-latest"])
    add(
        [
            "docker",
            "run",
            "-d",
            "--label",
            f"ama.rpi.owner={token}",
            "--memory=3g",
            "--cpus=2",
            "--publish=127.0.0.1::1433",
            "--env=ACCEPT_EULA=Y",
            "--env=MSSQL_PID=Developer",
            "--env=MSSQL_MEMORY_LIMIT_MB=2048",
            "--env=MSSQL_SA_PASSWORD",
            "mcr.microsoft.com/mssql/server:2022-latest",
        ],
        env={"MSSQL_SA_PASSWORD": "<redacted>"},
    )
    add(["docker", "inspect", sql["container"]])
    sqlenv = {
        "PYTHONPATH": test_paths("api", True),
        "ZF_TEST_MSSQL": "1",
        "ZF_SQL_SERVER": "127.0.0.1",
        "ZF_SQL_PORT": sql["port"],
        "ZF_SQL_DATABASE": "rpi_disposable",
        "ZF_SQL_AUTH": "password",
        "ZF_SQL_USER": "sa",
        "ZF_SQL_PASSWORD": "<redacted>",
        "ZF_SQL_TRUST_CERT": "1",
    }
    add([python, "-c", SQL_QUERY], env=sqlenv, timeout=15, attempts=60)
    add(["docker", "inspect", sql["container"]])
    add(["docker", "image", "inspect", receipt["images"].get("mssql", "")])
    add(
        [python, "-m", "unittest", "-v", *SQL_SELECTORS],
        "src/api",
        env=sqlenv,
        suite=True,
        integration=True,
        timeout=1800,
    )
    add(["docker", "rm", "-f", sql["container"]])
    for name in (*[f"image-{p}" for p in IMAGES], "logo-0600"):
        if name not in groups:
            continue
        group = name
        project = "api" if name == "logo-0600" else name.removeprefix("image-")
        context = "<output>/logo-snapshot/src" if name == "logo-0600" else "<checkout>/src"
        image = receipt["images"][name]
        tag = f"zava-forward-{project}:rpi-{token}" + ("-logo0600" if name == "logo-0600" else "")
        if image["tag"] != tag or re.fullmatch("sha256:[0-9a-f]{64}", image["id"]) is None:
            raise GateError("Receipt image identity is invalid")
        add(
            image_build_argv(
                f"{context}/{project}/Dockerfile", tag, context, fresh=name != "logo-0600"
            ),
            timeout=1800,
        )
        add(["docker", "image", "inspect", tag])
        add([py("namespace"), "src/check-container.py", project, image["id"]], timeout=300)
        if name == "logo-0600":
            continue
        args = [
            "trivy",
            "image",
            "--cache-dir",
            "<output>/cache/trivy",
            "--config",
            "src/trivy.yaml",
            "--scanners",
            "vuln",
            "--severity",
            "HIGH,CRITICAL",
        ]
        add(
            [
                *args,
                "--ignore-unfixed",
                "--exit-code",
                "1",
                "--format",
                "json",
                "--output",
                f"<output>/{project}-gate.json",
                image["id"],
            ]
        )
        add(
            [
                *args,
                "--ignore-unfixed=false",
                "--exit-code",
                "0",
                "--format",
                "json",
                "--output",
                f"<output>/{project}-all.json",
                image["id"],
            ]
        )
        add(
            [
                *args,
                "--format",
                "spdx-json",
                "--output",
                f"<output>/{project}.spdx.json",
                image["id"],
            ]
        )
    for value in receipt["extras"]:
        project, selector = extra_selector(value)
        group = f"extra-{value}"
        module = f"src/{project}/tests/{selector.split('.')[0]}.py"
        if not git(root, "ls-files", "--", module):
            raise GateError("Extra selector is not a tracked test module")
        add(
            [py(project), "-m", "unittest", "-v", selector],
            f"src/{project}",
            env={"PYTHONPATH": test_paths(project, True)},
            suite=True,
            integration=True,
        )
    group = "tooling"
    python = py("namespace")
    add([python, "-m", "pip", "install", "ruff==0.17.1", "mypy==2.4.0"])
    lint(python, RUFF_GROUPS[-1])
    add([python, "-m", "mypy", *TYPE_GROUPS[2]])
    for name in (*PROJECTS, "namespace"):
        group = f"setup-{name}"
        if name == "namespace":
            install(name, list(PROJECTS), dev=False)
        else:
            packages = [] if name == "core" else ["core"]
            if name == "api":
                packages.append("agents")
            install(name, [*packages, name])
    return [check for check in result if check["group"] in groups]


def verify_commands(root: Path, out: Path, receipt: dict[str, Any]) -> None:
    checks = required_checks(root, receipt)
    order = list(dict.fromkeys(check["group"] for check in checks))
    commands = iter(
        sorted(
            receipt["commands"],
            key=lambda row: order.index(row["group"]) if row["group"] in order else len(order),
        )
    )
    logs: set[str] = set()
    for check in checks:
        for _attempt in range(check["attempts"]):
            row = next(commands, None)
            if row is None or any(
                row.get(key) != check[key]
                for key in (
                    "group",
                    "argv",
                    "cwd",
                    "env",
                    "timeout_seconds",
                    "suite",
                    "integration",
                )
            ):
                raise GateError(f"Required command identity missing/mismatched: {check['group']}")
            name = row["log"]
            if (
                not re.fullmatch(r"[0-9]{4}-[a-zA-Z0-9_.:-]+\.log", name)
                or name in logs
                or receipt["files"].get(name) != row["sha256"]
                or digest(out / name) != row["sha256"]
            ):
                raise GateError("Required command log evidence missing/mismatched")
            logs.add(name)
            output = (out / name).read_text()
            code = row["exit_code"]
            if row.get("interrupted") or code in (124, 127, 130) or code < 0:
                raise GateError("Required command interrupted/timed out/unavailable")
            if code:
                if not row.get("expected_probe_failure") or not (
                    check["probe"] or check["attempts"] > 1
                ):
                    raise GateError("Required command did not succeed")
                if check["attempts"] > 1:
                    continue
            elif row.get("expected_probe_failure"):
                raise GateError("Successful command mislabeled as a failed probe")
            if check["suite"]:
                counts = check_skips(
                    output,
                    integration=check["integration"],
                    group=check["group"],
                    expected_count=(
                        3 if EMPLOYEE_ACCEPTANCE_BROWSER_MODULE in check["argv"] else None
                    ),
                    expected_test=(
                        CHAT_PANEL_DISCOVERY_SKIP[0]
                        if CHAT_PANEL_BROWSER_SELECTOR in check["argv"]
                        else None
                    ),
                )
                if counts["executed"] <= 0 or any(row.get(k) != v for k, v in counts.items()):
                    raise GateError("Required suite result evidence missing/mismatched")
            if check["group"] == "static" and check["argv"][0] == "git" and output.strip():
                raise GateError("Tracked data guard evidence is not empty")
            break
        else:
            raise GateError("Required SQL readiness never succeeded")
    if next(commands, None) is not None:
        raise GateError("Receipt contains commands outside the trusted matrix")


def verify_results(out: Path, receipt: dict[str, Any]) -> None:
    groups = receipt.get("executed_groups", required_groups(receipt["extras"]))
    if (out / "snapshot-inputs.log").read_text().strip():
        raise GateError("Snapshot input evidence is not clean")
    if "browser" in groups:
        if digest(out / "axe-4.10.3.min.js") != AXE_SHA256:
            raise GateError("Pinned axe evidence identity mismatch")
        browser = json.loads((out / "regulatory-ux-results.json").read_text())
        if (
            browser["outcome"] != "passed"
            or browser["axe_status"] != "executed"
            or browser["axe_version"] != "4.10.3"
            or browser["axe_sha256"] != AXE_SHA256
            or not browser["scans"]
            or "skipped" in json.dumps(browser)
            or any(scan["violations"] for scan in browser["scans"])
        ):
            raise GateError("Required browser result evidence is incomplete/failed")
        journey = json.loads((out / "case-journey-results.json").read_text())
        if (
            not journey["browser"]
            or journey["axe_version"] != "4.10.3"
            or journey["page_errors"]
            or journey["zoom"] != "chrome.tabs.setZoom=2; innerWidth<=640"
            or len(journey["scans"]) != 87
            or any(
                item["impact"] in ("serious", "critical")
                for scan in journey["scans"]
                for item in scan["violations"]
            )
        ):
            raise GateError("Required case journey evidence is incomplete/failed")
    for project in IMAGES:
        if f"image-{project}" not in groups:
            continue
        image_id = receipt["images"][f"image-{project}"]["id"]
        for suffix in ("gate", "all"):
            report = json.loads((out / f"{project}-{suffix}.json").read_text())
            if (
                report["Trivy"]["Version"] != "0.76.0"
                or report["Metadata"]["ImageID"] != image_id
                or not report["Results"]
                or (suffix == "gate" and any(r.get("Vulnerabilities") for r in report["Results"]))
            ):
                raise GateError("Required scan result evidence is incomplete/failed")
        spdx = json.loads((out / f"{project}.spdx.json").read_text())
        if (
            spdx["spdxVersion"] != "SPDX-2.3"
            or spdx["name"] != image_id
            or not spdx["packages"]
            or "Tool: trivy-0.76.0" not in spdx["creationInfo"]["creators"]
        ):
            raise GateError("Required SPDX evidence is incomplete/mismatched")
    if "infra" in groups:
        inventory = next(
            row for row in receipt["commands"] if row["argv"][1:3] == ["-c", WORKFLOW_INVENTORY]
        )
        jobs = json.loads((out / inventory["log"]).read_text())
        coverage = json.loads((out / "workflow-coverage.json").read_text())
        if coverage["steps"] != Runner.coverage_rows(jobs):
            raise GateError("Workflow coverage evidence does not match the command inventory")


def extra_selector(value: str) -> tuple[str, str]:
    if not re.fullmatch(r"(core|agents|api|orchestrator|importer):test_[A-Za-z0-9_.]+", value):
        raise GateError(
            "Extra checks must be reviewed PROJECT:test_module[.Class.method] selectors"
        )
    project, selector = value.split(":", 1)
    return project, selector


def check_skips(
    text: str,
    *,
    integration: bool = False,
    group: str = "",
    expected_test: str | None = None,
    expected_count: int | None = None,
) -> dict[str, Any]:
    counts = re.findall(r"Ran (\d+) tests? in ", text)
    skips = [
        {"test": match[0], "reason": match[1]}
        for match in re.findall(r"(?m)^(.+?) \.\.\. skipped ['\"](.+?)['\"]$", text)
    ]
    if not counts or int(counts[-1]) == 0:
        raise GateError("Unittest command did not report an executed suite")
    if (
        integration and any((s["test"], s["reason"]) not in SQL_NOT_APPLICABLE for s in skips)
    ) or any(
        s["reason"] not in EXPECTED_SKIP_REASONS
        or (
            s["reason"] == CHAT_PANEL_DISCOVERY_SKIP[1]
            and (group != "project-api" or (s["test"], s["reason"]) != CHAT_PANEL_DISCOVERY_SKIP)
        )
        for s in skips
    ):
        raise GateError(f"Unexpected required integration/dependency skip: {skips}")
    summary = re.findall(r"(?m)^OK(?: \((.*?)\))?$", text)
    if not summary:
        raise GateError("Unittest success summary missing")
    declared = re.search(r"skipped=(\d+)", summary[-1])
    if (int(declared[1]) if declared else 0) != len(skips):
        raise GateError("Skip count does not match enumerated test/reason evidence")
    if expected_count is not None and (int(counts[-1]) != expected_count or skips):
        raise GateError(
            f"Required {expected_count}-test zero-skip execution evidence missing/mismatched"
        )
    if expected_test is not None and (
        int(counts[-1]) != 1
        or skips
        or re.findall(r"(?m)^(.+?) \.\.\. (.+)$", text) != [(expected_test, "ok")]
    ):
        raise GateError(
            f"Required exact test execution evidence missing/mismatched: {expected_test}"
        )
    return {"tests": int(counts[-1]), "executed": int(counts[-1]) - len(skips), "skips": skips}


def scan_database(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise GateError("Trivy database metadata unavailable")
    metadata = json.loads(path.read_text())
    now = datetime.now(UTC)
    updated = datetime.fromisoformat(metadata["UpdatedAt"].replace("Z", "+00:00"))
    next_update = datetime.fromisoformat(metadata["NextUpdate"].replace("Z", "+00:00"))
    if not updated <= now < next_update:
        raise GateError("Trivy database is stale or has a future update time")
    return {
        "sha256": digest(path),
        "updated_at": metadata["UpdatedAt"],
        "next_update": metadata["NextUpdate"],
    }


def owned_sql(metadata: dict[str, Any], container: str, token: str) -> str:
    bindings = metadata["NetworkSettings"]["Ports"].get("1433/tcp")
    if (
        metadata["Id"] != container
        or metadata["Config"].get("Labels", {}).get("ama.rpi.owner") != token
        or not metadata["State"]["Running"]
        or not bindings
        or len(bindings) != 1
        or bindings[0]["HostIp"] != "127.0.0.1"
        or not bindings[0]["HostPort"].isdigit()
    ):
        raise GateError("Refusing destructive SQL tests: endpoint is not provably runner-owned")
    port = bindings[0]["HostPort"]
    assert isinstance(port, str)
    return port


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(".pending")
    with temporary.open("w") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


class Runner:
    def __init__(
        self,
        root: Path,
        out: Path,
        base: str,
        extras: list[str],
        *,
        selected: dict[str, Any] | None = None,
        jobs: int = 1,
        resume: Path | None = None,
    ) -> None:
        self.root, self.out, self.base, self.extras = root, out, base, extras
        self.selection = selected or selection(root, base, "all", extras)
        admit_browser_output(out, self.selection["groups"])
        self.jobs, self.resume = jobs, resume
        self.reused: list[str] = []
        self.local = threading.local()
        self.row_lock = threading.Lock()
        self.install_lock = threading.Lock()
        self.docker_lock = threading.Lock()
        self.cancelled = threading.Event()
        self.active: dict[int, subprocess.Popen[str]] = {}
        self.token = secrets.token_hex(12)
        self.snapshot = out / "checkout"
        self.envs = out / "venvs"
        self.rows: list[dict[str, Any]] = []
        self.groups: list[str] = []
        self.failures: list[str] = []
        self.images: dict[str, Any] = {}
        self.secrets: list[str] = []
        self.process: subprocess.Popen[str] | None = None
        self.containers: set[str] = set()
        self.sql_identity: dict[str, str] = {}
        self.env = {
            "PATH": os.environ.get("PATH", os.defpath),
            "HOME": str(out / "home"),
            "TMPDIR": str(out / "tmp"),
            "XDG_CACHE_HOME": str(out / "cache"),
            "AZURE_CONFIG_DIR": str(out / "azure"),
            "AZURE_BICEP_USE_BINARY_FROM_PATH": "true",
            "AZURE_CORE_COLLECT_TELEMETRY": "false",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPYCACHEPREFIX": str(out / "bytecode"),
            "PYTHONNOUSERSITE": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_CACHE_DIR": str(out / "cache/pip"),
            "RUFF_CACHE_DIR": str(out / "cache/ruff"),
            "MYPY_CACHE_DIR": str(out / "cache/mypy"),
            "PLAYWRIGHT_BROWSERS_PATH": str(out / "chromium"),
            "ZF_DATA": str(out / "unused-data/zavaforward.json"),
            "ZF_STORE": "json",
            "LANG": "C.UTF-8",
        }
        for folder in ("home", "tmp", "cache", "azure", "unused-data"):
            (out / folder).mkdir(parents=True)
        safety = out / "safety"
        safety.mkdir()
        (safety / "sitecustomize.py").write_text(
            "import sys\n"
            "def local_only(event, args):\n"
            "    if event == 'socket.connect':\n"
            "        address = args[1]\n"
            "        if isinstance(address, tuple) and address[0] not in "
            "('127.0.0.1', 'localhost', '::1'):\n"
            "            raise RuntimeError('Local RPI test refused non-loopback connection')\n"
            "sys.addaudithook(local_only)\n"
        )
        self.safety = safety
        self.group = "preflight"

    @property
    def group(self) -> str:
        return str(getattr(self.local, "group", "preflight"))

    @group.setter
    def group(self, value: str) -> None:
        self.local.group = value

    @property
    def process(self) -> subprocess.Popen[str] | None:
        return getattr(self.local, "process", None)

    @process.setter
    def process(self, value: subprocess.Popen[str] | None) -> None:
        self.local.process = value
        with self.row_lock:
            if value is None:
                self.active.pop(threading.get_ident(), None)
            else:
                self.active[threading.get_ident()] = value

    def scrub(self, text: str) -> str:
        for value in self.secrets:
            text = text.replace(value, "<redacted>")
        for path, label in (
            (str(self.snapshot), "<checkout>"),
            (str(self.out), "<output>"),
            (str(self.root), "<candidate>"),
            (str(Path.home()), "<home>"),
        ):
            text = text.replace(path, label)
        return text

    def command(
        self,
        argv: list[str],
        cwd: str = ".",
        *,
        env: dict[str, str] | None = None,
        timeout: int = 900,
        suite: bool = False,
        integration: bool = False,
        retry: bool = False,
    ) -> str:
        if self.cancelled.is_set():
            raise GateError("Execution cancelled before command start")
        started = datetime.now(UTC).isoformat()
        entry: dict[str, Any] = {
            "group": self.group,
            "argv": [self.scrub(a) for a in argv],
            "cwd": cwd,
            "started": started,
            "timeout_seconds": timeout,
            "env": {key: self.scrub(value) for key, value in (env or {}).items()},
            "suite": suite,
            "integration": integration,
        }
        with self.row_lock:
            logfile = f"{len(self.rows):04d}-{self.group}.log"
            self.rows.append(entry)
        self.local.last_entry = entry
        entry["log"] = logfile
        child_env = {
            **self.env,
            "RUFF_CACHE_DIR": str(self.out / "cache/ruff" / self.group),
            "MYPY_CACHE_DIR": str(self.out / "cache/mypy" / self.group),
            **(env or {}),
        }
        if suite or (len(argv) > 2 and argv[1] == "-m" and argv[2].startswith("checks.")):
            child_env["PYTHONPATH"] = str(self.safety) + ":" + child_env.get("PYTHONPATH", "")
        print(f"{self.group}: {self.scrub(' '.join(argv))}", flush=True)
        cancellation = None
        try:
            self.process = subprocess.Popen(
                argv,
                cwd=self.snapshot / cwd,
                env=child_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
            )
            if self.cancelled.is_set():
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(self.process.pid, signal.SIGTERM)
            try:
                output, _ = self.process.communicate(timeout=timeout)
                code = self.process.returncode
            except subprocess.TimeoutExpired:
                output = self.stop_command()
                code = 124
                output += "\nRequired command interrupted: TimeoutExpired\n"
            except KeyboardInterrupt as error:
                cancellation = error
                entry["interrupted"] = True
                output = self.stop_command()
                code = 130
                output += "\nRequired command interrupted: KeyboardInterrupt\n"
        except FileNotFoundError as error:
            output, code = f"Missing tool/dependency: {error.filename}", 127
        finally:
            if self.process is not None and self.process.returncode is not None:
                self.process = None
        sanitized = self.scrub(output)
        (self.out / logfile).write_text(sanitized)
        print(sanitized, end="" if sanitized.endswith("\n") else "\n", flush=True)
        entry.update(
            exit_code=code,
            finished=datetime.now(UTC).isoformat(),
            sha256=digest(self.out / logfile),
        )
        if cancellation is not None:
            raise cancellation
        if code:
            if retry:
                entry["expected_probe_failure"] = True
                return output
            raise GateError(f"{self.group} failed ({code}); see {logfile}")
        if suite:
            entry.update(
                check_skips(
                    output,
                    integration=integration,
                    group=self.group,
                    expected_count=(3 if EMPLOYEE_ACCEPTANCE_BROWSER_MODULE in argv else None),
                    expected_test=(
                        CHAT_PANEL_DISCOVERY_SKIP[0]
                        if CHAT_PANEL_BROWSER_SELECTOR in argv
                        else None
                    ),
                )
            )
        return output

    def stop_command(self) -> str:
        assert self.process is not None
        # Signal only this command's new process group; allow helper finally cleanup.
        os.killpg(self.process.pid, signal.SIGINT)
        try:
            output, _ = self.process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            output, _ = self.process.communicate()
        return output

    def python(self, project: str) -> str:
        return str(self.envs / project / "bin/python")

    def metadata_cleanup(self) -> None:
        for project in PROJECTS:
            for path in (self.snapshot / "src" / project / "src").glob("*.egg-info"):
                if path.is_symlink() or not path.is_dir():
                    raise GateError("Unexpected editable-build metadata path")
                if git(self.snapshot, "ls-files", "--", str(path.relative_to(self.snapshot))):
                    raise GateError("Refusing to remove tracked build metadata")
                shutil.rmtree(path)

    def install(self, name: str, packages: list[str], dev: bool = True) -> None:
        with self.install_lock:
            self._install(name, packages, dev)

    def _install(self, name: str, packages: list[str], dev: bool = True) -> None:
        self.command(["python3", "-m", "venv", str(self.envs / name)])
        pip = [self.python(name), "-m", "pip"]
        self.command([*pip, "check"])
        # A fresh external venv cannot import these sibling distributions.
        self.command([self.python(name), "-c", "import zava_forward"], retry=True)
        args = [*pip, "install"]
        for project in packages:
            args += ["-e", f"src/{project}" + ("[dev]" if dev and project == name else "")]
        self.command(args, timeout=1200)
        self.metadata_cleanup()
        self.command([*pip, "check"])

    @contextlib.contextmanager
    def gate(self, name: str) -> Iterator[None]:
        self.group = name
        start = sum(row["group"] == name for row in self.rows)
        try:
            yield
            if sum(row["group"] == name for row in self.rows) == start:
                raise GateError(f"Required group {name} has no execution evidence")
        except GateError as error:
            self.failures.append(f"{name}: {error}")
            print(f"FAILED required group: {name}: {error}", flush=True)
        else:
            self.groups.append(name)
        finally:
            if name == "mssql":
                self.cleanup_containers()

    def tests_env(self, project: str, own_tests: bool = False) -> dict[str, str]:
        return {
            "PYTHONPATH": test_paths(project, own_tests).replace("<checkout>", str(self.snapshot))
        }

    def lint(self, python: str, files: tuple[str, ...], cwd: str = ".") -> None:
        self.command(
            [
                python,
                "-m",
                "ruff",
                "check",
                "--isolated",
                "--select",
                "E,F,I,B,UP",
                "--target-version",
                "py312",
                "--line-length",
                "100",
                *files,
            ],
            cwd,
        )
        self.command(
            [
                python,
                "-m",
                "ruff",
                "format",
                "--isolated",
                "--line-length",
                "100",
                "--check",
                *files,
            ],
            cwd,
        )

    def preflight(self) -> None:
        with self.gate("preflight"):
            tool_identity()
            for argv in (
                ["python3", "--version"],
                ["node", "--version"],
                ["docker", "version"],
                ["az", "bicep", "version"],
                ["actionlint", "-version"],
                ["shellcheck", "--version"],
                ["trivy", "--version"],
            ):
                text = self.command(argv, timeout=60)
                if argv[0] == "trivy" and "Version: 0.76.0" not in text:
                    raise GateError("Trivy must be exactly 0.76.0")
                if argv[0] == "python3" and not text.startswith("Python 3.12."):
                    raise GateError("Project environments require Python 3.12")
            for name in WORKFLOWS:
                if WORKFLOW_HASHES.get(name) != digest(self.snapshot / ".github/workflows" / name):
                    raise GateError(f"Workflow matrix drift: {name}")

    def projects(self, projects: tuple[str, ...] = PROJECTS, *, install: bool = True) -> None:
        for project in projects:
            with self.gate(f"project-{project}"):
                packages = [] if project == "core" else ["core"]
                if project == "api":
                    packages.append("agents")
                if install:
                    self.install(project, [*packages, project])
                py, cwd = self.python(project), f"src/{project}"
                self.command(
                    [py, "-m", "unittest", "discover", "-s", "tests", "-v"],
                    cwd,
                    env=self.tests_env(project),
                    suite=True,
                    timeout=1800,
                )
                self.command([py, "-m", "ruff", "check", "."], cwd)
                self.command([py, "-m", "ruff", "format", "--check", "."], cwd)
                self.command([py, "-m", "mypy"], cwd)

    def namespace_static_infra(self, only: str | None = None) -> None:
        py = self.python("namespace")
        if only in (None, "namespace"):
            self.namespace()
        if only in (None, "static"):
            self.static()
        if only in (None, "infra"):
            self.infra()
        if only in (None, "migration"):
            self.migration()
        if only == "tooling":
            with self.gate("tooling"):
                self.command([py, "-m", "pip", "install", "ruff==0.17.1", "mypy==2.4.0"])
                self.lint(py, RUFF_GROUPS[-1])
                self.command([py, "-m", "mypy", *TYPE_GROUPS[2]])

    def namespace(self) -> None:
        with self.gate("namespace"):
            self.install("namespace", list(PROJECTS), dev=False)
            py = self.python("namespace")
            for project in ("core", "agents", "orchestrator", "importer"):
                self.command([py, "-m", f"zava_forward.{project}"])
            self.command(
                [py, "-c", "from zava_forward.api.version import __version__; print(__version__)"]
            )
            self.command(
                [
                    py,
                    "-c",
                    "import zava_forward; assert zava_forward.__file__ is None; "
                    "assert len(list(zava_forward.__path__)) == 5",
                ]
            )

    def static(self) -> None:
        py = self.python("namespace")
        with self.gate("static"):
            self.command(
                [
                    py,
                    "-m",
                    "compileall",
                    "-q",
                    *[f"src/{p}/src" for p in ("core", "agents", "api", "orchestrator")],
                ]
            )
            for name in ("app", "assistants"):
                self.command(["node", "--check", f"src/api/src/zava_forward/api/web/{name}.js"])
            tracked = self.command(
                [
                    "git",
                    "ls-files",
                    "--",
                    "*/.assistant-test-*",
                    "mvp/data",
                    ":(glob)src/**/data/**",
                ]
            )
            if tracked.strip():
                raise GateError("Tracked sandbox/working data guard failed")
            self.command(
                [
                    "actionlint",
                    "-config-file",
                    "infra/tests/actionlint.yaml",
                    *[f".github/workflows/{name}" for name in WORKFLOWS],
                ]
            )
            self.command(
                [py, "-m", "unittest", "discover", "-s", "tools", "-p", "test_rpi_checks.py", "-v"],
                suite=True,
            )

    def infra(self) -> None:
        py = self.python("namespace")
        with self.gate("infra"):
            self.command([py, "-c", "import yaml, mssql_python"], retry=True)
            self.command(
                [py, "-m", "pip", "install", "PyYAML==6.0.3", "ruff==0.17.1", "mypy==2.4.0"]
            )
            self.command(
                [py, "-m", "pip", "install", "--require-hashes", "-r", "src/api/requirements.txt"]
            )
            self.workflow_coverage(py)
            for file in sorted(
                [*self.snapshot.glob("infra/*.bicep"), *self.snapshot.glob("infra/modules/*.bicep")]
            ):
                relative = str(file.relative_to(self.snapshot))
                self.command(["az", "bicep", "build", "--file", relative, "--stdout"])
                self.command(["az", "bicep", "lint", "--file", relative])
            self.command(
                [py, "-m", "unittest", "discover", "-s", "infra/tests", "-v"],
                env={"REQUIRE_AZ_BICEP": "1"},
                suite=True,
                integration=True,
                timeout=1800,
            )
            for files in RUFF_GROUPS:
                self.lint(py, files)
            for type_files in TYPE_GROUPS:
                self.command([py, "-m", "mypy", *type_files])

    def migration(self) -> None:
        py = self.python("namespace")
        with self.gate("migration"):
            self.command([py, "-c", "import pptx"], retry=True)
            self.command([py, "-m", "pip", "install", "-r", "tools/rename-zava-requirements.txt"])
            self.command([py, "tools/rename-zava-tests.py"], timeout=900)

    def workflow_coverage(self, python: str) -> None:
        inventory = self.command(
            [
                python,
                "-c",
                WORKFLOW_INVENTORY,
                *WORKFLOWS,
            ]
        )
        jobs = json.loads(inventory)
        atomic_json(self.out / "workflow-coverage.json", {"steps": self.coverage_rows(jobs)})

    @staticmethod
    def coverage_rows(jobs: dict[str, Any]) -> list[dict[str, Any]]:
        equivalents = {
            ("src-ci.yml", "project"): "project-*; browser; image-*; logo-0600",
            ("src-ci.yml", "namespace"): "namespace; static; infra; migration",
            ("src-ci.yml", "no-working-data"): "static",
            ("src-ci.yml", "mssql"): "mssql",
            ("mvp-ci.yml", "test"): "project-api; project-orchestrator; static",
            ("mvp-ci.yml", "image"): "image-api; logo-0600",
            ("mvp-ci.yml", "mssql"): "mssql",
            ("mvp-validation.yml", "validate"): "project-api; static; infra; migration",
        }
        rows = []
        for workflow, document in jobs.items():
            for job, metadata in document.items():
                for index, step in enumerate(metadata["steps"]):
                    boundary = equivalents.get((workflow, job))
                    action = step.get("uses", "")
                    if workflow in ("src-deploy.yml", "infra-plan.yml"):
                        boundary = (
                            "hosted-only authenticated/approval/release; infra fake contracts only"
                        )
                    elif job == "image-paths":
                        boundary = (
                            "hosted-only PR path context; infra local changed-images contracts"
                        )
                    elif action.startswith("actions/upload-artifact@"):
                        boundary = (
                            "hosted-only artifact publication; equivalent external local files"
                        )
                    elif action.startswith("actions/checkout@"):
                        boundary = "local exact-HEAD detached checkout; not GitHub event identity"
                    elif action.startswith("actions/setup-python@"):
                        boundary = "local Python 3.12 isolated bootstrap; not hosted provisioning"
                    if boundary is None:
                        raise GateError(
                            f"Workflow step has no coverage classification: {workflow}/{job}"
                        )
                    rows.append(
                        {
                            "workflow": workflow,
                            "job": job,
                            "step": index,
                            "name": step.get("name", step.get("id", action)),
                            "coverage": boundary,
                            "workflow_sha256": WORKFLOW_HASHES[workflow],
                        }
                    )
        return rows

    def browser(self) -> None:
        with self.gate("browser"):
            py = self.python("api")
            for name in (
                "design_system_browser_check",
                "regulatory_ux_check",
                "case_journey_browser_check",
            ):
                self.lint(py, (f"checks/{name}.py",), "src/api")
            self.command([py, "-m", "playwright", "install", "chromium"], timeout=900)
            self.command(
                [py, "-m", EMPLOYEE_ACCEPTANCE_BROWSER_MODULE],
                "src/api",
                env={"PYTHONPATH": EMPLOYEE_ACCEPTANCE_BROWSER_PATHS},
                suite=True,
                integration=True,
            )
            self.command(
                [py, "-m", "unittest", "-v", CHAT_PANEL_BROWSER_SELECTOR],
                "src/api",
                env={**self.tests_env("api", True), "ZF_BROWSER_TESTS": "1"},
                suite=True,
                integration=True,
            )
            axe = self.out / "axe-4.10.3.min.js"
            with urlopen(
                "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js", timeout=60
            ) as response:
                axe.write_bytes(response.read())
            if digest(axe) != AXE_SHA256:
                raise GateError("Pinned axe integrity check failed")
            # The unchanged harness scrubs its server environment, including bytecode settings.
            bytecode_policy = "import sys; sys.dont_write_bytecode = True\n"
            (self.out / "browser-bytecode-policy.pth").write_text(bytecode_policy)
            (self.envs / "api/lib/python3.12/site-packages/00-rpi-bytecode.pth").write_text(
                bytecode_policy
            )
            try:
                self.command(
                    [py, "-c", BROWSER_ENTRY, "checks.design_system_browser_check"],
                    "src/api",
                    timeout=900,
                    env={"PYTHONPATH": str(self.safety)},
                )
                self.command(
                    [
                        py,
                        "-c",
                        BROWSER_ENTRY,
                        "checks.case_journey_browser_check",
                        "--axe",
                        str(axe),
                        "--out",
                        str(self.out / "case-journey"),
                    ],
                    "src/api",
                    timeout=900,
                    env={
                        "PYTHONPATH": str(self.safety)
                        + ":"
                        + self.tests_env("api", True)["PYTHONPATH"]
                    },
                )
                shutil.copyfile(
                    self.out / "case-journey/results.json",
                    self.out / "case-journey-results.json",
                )
            finally:
                marker = self.snapshot / ".venv"
                if marker.exists():
                    marker.rmdir()
            self.command(
                [
                    py,
                    "-m",
                    "checks.regulatory_ux_check",
                    "--axe",
                    str(axe),
                    "--out",
                    str(self.out / "regulatory-ux-results.json"),
                ],
                "src/api",
                env=self.tests_env("api", True),
                timeout=900,
            )
            self.command(
                [
                    py,
                    "-c",
                    REGULATORY_ASSERT,
                    str(self.out / "regulatory-ux-results.json"),
                ]
            )

    def sql(self) -> None:
        with self.gate("mssql"):
            py = self.python("api")
            self.command(
                [py, "-m", "pip", "install", "--require-hashes", "-r", "src/api/requirements.txt"]
            )
            self.command(
                [
                    py,
                    "-c",
                    SQL_DRIVER,
                ]
            )
            password = "Aa1!" + secrets.token_hex(24)
            self.secrets.append(password)
            self.command(
                ["docker", "pull", "mcr.microsoft.com/mssql/server:2022-latest"], timeout=900
            )
            container = self.command(
                [
                    "docker",
                    "run",
                    "-d",
                    "--label",
                    f"ama.rpi.owner={self.token}",
                    "--memory=3g",
                    "--cpus=2",
                    "--publish=127.0.0.1::1433",
                    "--env=ACCEPT_EULA=Y",
                    "--env=MSSQL_PID=Developer",
                    "--env=MSSQL_MEMORY_LIMIT_MB=2048",
                    "--env=MSSQL_SA_PASSWORD",
                    "mcr.microsoft.com/mssql/server:2022-latest",
                ],
                env={"MSSQL_SA_PASSWORD": password},
            ).strip()
            if not re.fullmatch("[0-9a-f]{64}", container):
                raise GateError("Invalid SQL container identity")
            self.containers.add(container)
            metadata = json.loads(self.command(["docker", "inspect", container]))[0]
            port = owned_sql(metadata, container, self.token)
            self.sql_identity = {"container": container, "port": port}
            sqlenv = {
                **self.tests_env("api", True),
                "ZF_TEST_MSSQL": "1",
                "ZF_SQL_SERVER": "127.0.0.1",
                "ZF_SQL_PORT": port,
                "ZF_SQL_DATABASE": "rpi_disposable",
                "ZF_SQL_AUTH": "password",
                "ZF_SQL_USER": "sa",
                "ZF_SQL_PASSWORD": password,
                "ZF_SQL_TRUST_CERT": "1",
            }
            for _attempt in range(60):
                self.command([py, "-c", SQL_QUERY], env=sqlenv, timeout=15, retry=True)
                if self.local.last_entry["exit_code"] == 0:
                    break
                time.sleep(2)
            else:
                raise GateError("Owned SQL query readiness timeout")
            metadata = json.loads(self.command(["docker", "inspect", container]))[0]
            if owned_sql(metadata, container, self.token) != port:
                raise GateError("Owned SQL endpoint changed")
            self.images["mssql"] = json.loads(
                self.command(["docker", "image", "inspect", metadata["Image"]])
            )[0]["Id"]
            self.command(
                [py, "-m", "unittest", "-v", *SQL_SELECTORS],
                "src/api",
                env=sqlenv,
                suite=True,
                integration=True,
                timeout=1800,
            )
            self.command(["docker", "rm", "-f", container])
            self.containers.remove(container)

    def image(self, project: str, *, stress: bool = False) -> None:
        name = "logo-0600" if stress else f"image-{project}"
        with self.gate(name):
            context = self.snapshot / "src"
            if stress:
                context = self.out / "logo-snapshot/src"
                shutil.copytree(self.snapshot / "src", context)
                (context / "api/src/zava_forward/api/web/zava-logo.png").chmod(0o600)
            tag = f"zava-forward-{project}:rpi-{self.token}" + ("-logo0600" if stress else "")
            self.command(
                image_build_argv(
                    str(context / project / "Dockerfile"), tag, str(context), fresh=not stress
                ),
                timeout=1800,
            )
            metadata = json.loads(self.command(["docker", "image", "inspect", tag]))[0]
            image_id = metadata["Id"]
            self.images[name] = {"id": image_id, "digests": metadata["RepoDigests"], "tag": tag}
            self.command(
                [self.python("namespace"), "src/check-container.py", project, image_id], timeout=300
            )
            if stress:
                return
            args = [
                "trivy",
                "image",
                "--cache-dir",
                str(self.out / "cache/trivy"),
                "--config",
                "src/trivy.yaml",
                "--scanners",
                "vuln",
                "--severity",
                "HIGH,CRITICAL",
            ]
            self.command(
                [
                    *args,
                    "--ignore-unfixed",
                    "--exit-code",
                    "1",
                    "--format",
                    "json",
                    "--output",
                    str(self.out / f"{project}-gate.json"),
                    image_id,
                ],
                timeout=900,
                retry=True,
            )
            gate_row = self.local.last_entry
            gate_row.pop("expected_probe_failure", None)
            self.command(
                [
                    *args,
                    "--ignore-unfixed=false",
                    "--exit-code",
                    "0",
                    "--format",
                    "json",
                    "--output",
                    str(self.out / f"{project}-all.json"),
                    image_id,
                ],
                timeout=900,
            )
            self.command(
                [
                    *args,
                    "--format",
                    "spdx-json",
                    "--output",
                    str(self.out / f"{project}.spdx.json"),
                    image_id,
                ],
                timeout=900,
            )
            for suffix in ("gate.json", "all.json", "spdx.json"):
                report = json.loads(
                    (
                        self.out / f"{project}-{suffix}"
                        if suffix != "spdx.json"
                        else self.out / f"{project}.spdx.json"
                    ).read_text()
                )
                if not isinstance(report, dict) or (
                    suffix == "spdx.json" and "spdxVersion" not in report
                ):
                    raise GateError("Scanner report/SBOM is invalid")
            scan_database(self.out / "cache/trivy/db/metadata.json")
            if gate_row["exit_code"]:
                raise GateError("Fixable HIGH/CRITICAL scan failed; full report and SPDX retained")

    def cleanup_containers(self) -> None:
        for container in list(self.containers):
            result = subprocess.run(
                ["docker", "inspect", container], capture_output=True, text=True, env=self.env
            )
            if result.returncode == 0:
                metadata = json.loads(result.stdout)[0]
                if (
                    metadata["Id"] != container
                    or metadata["Config"]["Labels"].get("ama.rpi.owner") != self.token
                ):
                    raise GateError("Cleanup ownership mismatch")
                subprocess.run(
                    ["docker", "rm", "-f", container], check=True, capture_output=True, env=self.env
                )
            self.containers.remove(container)

    def cleanup(self) -> None:
        if self.process is not None:
            os.killpg(self.process.pid, signal.SIGTERM)
            self.process.wait(timeout=30)
            self.process = None
        self.cleanup_containers()
        if self.snapshot.exists():
            if git(self.snapshot, "status", "--porcelain", "--untracked-files=all") or git(
                self.snapshot, "ls-files", "--others", "--ignored", "--exclude-standard"
            ):
                raise GateError("Dirty owned snapshot retained for diagnosis; never force removed")
            subprocess.run(
                ["git", "-C", str(self.root), "worktree", "remove", str(self.snapshot)],
                check=True,
                capture_output=True,
            )

    def dispatch(self, group: str) -> None:
        if group.startswith("project-"):
            self.projects((group.removeprefix("project-"),), install=False)
        elif group in ("static", "infra", "migration", "tooling"):
            self.namespace_static_infra(group)
        elif group == "browser":
            self.browser()
        elif group == "mssql" or group.startswith("image-") or group == "logo-0600":
            with self.docker_lock:
                if group == "mssql":
                    self.sql()
                else:
                    self.image(
                        "api" if group == "logo-0600" else group.removeprefix("image-"),
                        stress=group == "logo-0600",
                    )
        elif group.startswith("extra-"):
            value = group.removeprefix("extra-")
            project, selector = extra_selector(value)
            with self.gate(group):
                module = f"src/{project}/tests/{selector.split('.')[0]}.py"
                if not git(self.snapshot, "ls-files", "--", module):
                    raise GateError("Extra selector is not a tracked test module")
                self.command(
                    [self.python(project), "-m", "unittest", "-v", selector],
                    f"src/{project}",
                    env=self.tests_env(project, True),
                    suite=True,
                    integration=True,
                )
        else:
            raise GateError(f"Unknown execution group: {group}")

    def schedule(self, groups: list[str]) -> None:
        pending = set(groups)
        completed = set(self.groups) | set(self.reused)
        failed: set[str] = set()
        running: dict[Future[None], str] = {}
        prerequisites = {group: dependencies(group) & (pending | completed) for group in pending}
        shared_namespace = [g for g in ("static", "infra", "migration", "tooling") if g in pending]
        shared_api = [
            g
            for g in (
                "project-api",
                "browser",
                "mssql",
                *[name for name in groups if name.startswith("extra-api:")],
            )
            if g in pending
        ]
        for chain in (shared_namespace, shared_api):
            for before, after in zip(chain, chain[1:], strict=False):
                prerequisites[after].add(before)
        # Infra/migration install into namespace; builds must see no generated metadata.
        writers = set(shared_namespace) & {"infra", "migration", "tooling"}
        for group in pending:
            if group.startswith("image-") or group == "logo-0600":
                prerequisites[group].update(writers)
        with ThreadPoolExecutor(max_workers=self.jobs) as pool:
            try:
                while pending or running:
                    for group in groups:
                        if group not in pending:
                            continue
                        if prerequisites[group] & failed:
                            pending.remove(group)
                            failed.add(group)
                            self.failures.append(f"{group}: blocked by failed prerequisite")
                        elif prerequisites[group] <= completed and len(running) < self.jobs:
                            pending.remove(group)
                            running[pool.submit(self.dispatch, group)] = group
                    if not running:
                        if pending:
                            raise GateError("Group dependency graph cannot make progress")
                        break
                    done, _ = wait(running, return_when=FIRST_COMPLETED)
                    for future in done:
                        group = running.pop(future)
                        future.result()
                        if group in self.groups:
                            completed.add(group)
                        else:
                            failed.add(group)
            except BaseException:
                self.cancelled.set()
                for future in running:
                    future.cancel()
                with self.row_lock:
                    processes = list(self.active.values())
                for process in processes:
                    if process.poll() is None:
                        with contextlib.suppress(ProcessLookupError):
                            os.killpg(process.pid, signal.SIGTERM)
                for process in processes:
                    try:
                        process.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        with contextlib.suppress(ProcessLookupError):
                            os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=30)
                raise

    def run(self) -> Path:
        identity = clean_identity(self.root, self.base)
        tools = tool_identity()
        parent = None
        if self.resume:
            parent = validate_receipt(self.root, self.resume, self.base, passing=False)
            if parent["status"] != "failed" or parent["selection"] != self.selection:
                raise GateError("Resume requires a failed receipt with the same selection")
            self.reused = parent["groups"]
        selected = self.selection["groups"]
        remaining = [group for group in selected if group not in self.reused]
        failure = None
        try:
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.root),
                    "worktree",
                    "add",
                    "--detach",
                    str(self.snapshot),
                    identity["head"],
                ],
                check=True,
                capture_output=True,
            )
            if clean_identity(self.snapshot, self.base) != identity:
                raise GateError("Snapshot differs from exact candidate")
            if "preflight" in remaining:
                self.preflight()
            if self.failures:
                raise GateError("; ".join(self.failures))
            needed = set(selected_environments(remaining))
            for name in (*PROJECTS, "namespace"):
                if name not in needed:
                    continue
                group = "namespace" if name == "namespace" else f"project-{name}"
                if group == "namespace" and group in remaining:
                    self.namespace()
                    continue
                self.group = group if group in remaining else f"setup-{name}"
                packages = [] if name == "core" else ["core"]
                if name == "api":
                    packages.append("agents")
                self.install(
                    name,
                    list(PROJECTS) if name == "namespace" else [*packages, name],
                    dev=name != "namespace",
                )
                if group not in remaining:
                    self.groups.append(f"setup-{name}")
            if self.failures:
                raise GateError("; ".join(self.failures))
            self.schedule([g for g in remaining if g not in ("preflight", "namespace")])
            if self.failures:
                raise GateError("; ".join(self.failures))
            if not set(selected) <= set(self.groups) | set(self.reused):
                raise GateError("Required matrix group coverage is incomplete")
            (self.out / "snapshot-inputs.log").write_text(
                git(self.snapshot, "status", "--porcelain", "--untracked-files=all")
                + git(self.snapshot, "ls-files", "--others", "--ignored", "--exclude-standard")
            )
            if (
                clean_identity(self.snapshot, self.base) != identity
                or clean_identity(self.root, self.base) != identity
            ):
                raise GateError("Source changed during execution")
            if tool_identity() != tools:
                raise GateError("Tool identity changed during execution")
        except (
            GateError,
            OSError,
            subprocess.SubprocessError,
            ValueError,
            KeyError,
            KeyboardInterrupt,
        ) as error:
            failure = self.scrub(str(error)) or type(error).__name__
        finally:
            if self.snapshot.exists():
                (self.out / "snapshot-inputs.log").write_text(
                    git(self.snapshot, "status", "--porcelain", "--untracked-files=all")
                    + git(self.snapshot, "ls-files", "--others", "--ignored", "--exclude-standard")
                )
            try:
                self.cleanup()
            except (GateError, OSError, subprocess.SubprocessError) as error:
                cleanup_failure = self.scrub(str(error))
                failure = f"{failure or ''}; cleanup failed: {cleanup_failure}"
        receipt: dict[str, Any] = {
            "schema": 4,
            "scope": "full" if selected == required_groups(self.extras) else "partial",
            "selection": self.selection,
            "status": "failed" if failure else "passed",
            "failure": failure,
            "resume_eligible": bool(failure)
            and not any(
                marker in (failure or "")
                for marker in (
                    "cleanup failed",
                    "Source changed",
                    "Tool identity changed",
                    "Snapshot differs",
                    "snapshot retained",
                )
            ),
            "identity": identity,
            "tools": tools,
            "groups": [g for g in selected if g in self.groups or g in self.reused],
            "executed_groups": [
                g
                for g in [
                    *required_groups(self.extras),
                    "tooling",
                    *[f"setup-{name}" for name in (*PROJECTS, "namespace")],
                ]
                if g in self.groups
            ],
            "resume": (
                {"path": str(self.resume), "sha256": digest(self.resume)} if self.resume else None
            ),
            "jobs": self.jobs,
            "extras": self.extras,
            "commands": self.rows,
            "images": self.images,
            "owner": self.token,
            "sql": self.sql_identity,
            "sealed": datetime.now(UTC).isoformat(),
            "hosted_only": [
                "GitHub approvals/protection/checks",
                "OIDC/Azure what-if",
                "manual release/deployment",
                "real AI acceptance",
            ],
        }
        try:
            receipt["environments"] = environment_identity(
                self.out, selected_environments(receipt["executed_groups"])
            )
            if any(g.startswith("image-") for g in receipt["executed_groups"]):
                receipt["trivy_database"] = scan_database(self.out / "cache/trivy/db/metadata.json")
        except (GateError, OSError, subprocess.SubprocessError, ValueError) as error:
            failure = self.scrub(str(error))
            receipt.update(status="failed", failure=failure)
        receipt["files"] = {
            path.name: digest(path)
            for path in self.out.iterdir()
            if path.is_file() and path.name not in ("receipt.json", "receipt.sha256")
        }
        if not failure:
            try:
                verify_commands(self.root, self.out, receipt)
                verify_results(self.out, receipt)
            except (GateError, OSError, ValueError, KeyError) as error:
                failure = self.scrub(str(error))
                receipt.update(status="failed", failure=failure)
        path = self.out / "receipt.json"
        atomic_json(path, receipt)
        (self.out / "receipt.sha256").write_text(digest(path) + "\n")
        if failure:
            raise GateError(f"{failure}; failed receipt retained at {path}")
        return path


def validate_receipt(
    root: Path,
    path: Path,
    base: str,
    *,
    passing: bool = True,
    depth: int = 0,
    new_output: Path | None = None,
) -> dict[str, Any]:
    if depth > 16:
        raise GateError("Resume provenance depth exceeded")
    path = path.resolve()
    if path.is_relative_to(root):
        raise GateError("Authoritative receipt must be outside the repository")
    if digest(path) != path.with_name("receipt.sha256").read_text().strip():
        raise GateError("Receipt integrity mismatch")
    receipt: dict[str, Any] = json.loads(path.read_text())
    if receipt["schema"] != 4 or receipt["status"] not in (
        ("passed",) if passing else ("passed", "failed")
    ):
        raise GateError("Receipt does not establish an eligible run")
    if not passing and receipt["status"] == "failed" and not receipt["resume_eligible"]:
        raise GateError("Failed receipt lacks a safe resume checkpoint")
    selected = selection(root, base, receipt["selection"]["mode"], receipt["extras"])
    scope = "full" if selected["groups"] == required_groups(receipt["extras"]) else "partial"
    if receipt["scope"] != scope or receipt["selection"] != selected:
        raise GateError("Receipt scope/selection mismatch")
    if receipt["identity"] != clean_identity(root, base):
        raise GateError("Receipt source/base/matrix/helper identity mismatch")
    if new_output is not None:
        admit_browser_output(new_output, selected["groups"])
    if receipt["tools"] != tool_identity():
        raise GateError("Receipt tool identity mismatch")
    executed = receipt["executed_groups"]
    allowed = {*selected["groups"], *[f"setup-{name}" for name in (*PROJECTS, "namespace")]}
    if len(executed) != len(set(executed)) or not set(executed) <= allowed:
        raise GateError("Receipt executed group selection mismatch")
    if receipt["environments"] != environment_identity(
        path.parent, selected_environments(executed)
    ):
        raise GateError("Receipt package/environment identity mismatch")
    extras = receipt["extras"]
    for value in extras:
        extra_selector(value)
    inherited: list[str] = []
    if receipt["resume"]:
        prior = Path(receipt["resume"]["path"])
        if digest(prior) != receipt["resume"]["sha256"]:
            raise GateError("Resume parent receipt identity mismatch")
        parent = validate_receipt(root, prior, base, passing=False, depth=depth + 1)
        if parent["status"] != "failed" or parent["selection"] != selected:
            raise GateError("Resume parent is not a failed matching selection")
        inherited = parent["groups"]
        if set(inherited) & set(executed):
            raise GateError("Resume reran a successful group")
    covered = [g for g in selected["groups"] if g in executed or g in inherited]
    if receipt["groups"] != covered or (passing and covered != selected["groups"]):
        raise GateError("Receipt omits required matrix coverage")
    for name, expected in receipt["files"].items():
        if Path(name).name != name or digest(path.parent / name) != expected:
            raise GateError("Receipt evidence file hash mismatch")
    evidence = dict(
        receipt, commands=[row for row in receipt["commands"] if row["group"] in executed]
    )
    if passing and len(evidence["commands"]) != len(receipt["commands"]):
        raise GateError("Passing receipt contains failed or unselected commands")
    verify_commands(root, path.parent, evidence)
    if any(g.startswith("image-") for g in executed) and receipt["trivy_database"] != scan_database(
        path.parent / "cache/trivy/db/metadata.json"
    ):
        raise GateError("Trivy database changed since receipt")
    expected_images = {g for g in executed if g in ("mssql", "logo-0600") or g.startswith("image-")}
    if not expected_images <= set(receipt["images"]) or (
        passing and set(receipt["images"]) != expected_images
    ):
        raise GateError("Receipt image coverage is incomplete")
    required_files = {
        "snapshot-inputs.log",
    }
    if "browser" in executed:
        required_files.update(
            (
                "axe-4.10.3.min.js",
                "regulatory-ux-results.json",
                "case-journey-results.json",
                "browser-bytecode-policy.pth",
            )
        )
    if "infra" in executed:
        required_files.add("workflow-coverage.json")
    for project in IMAGES:
        if f"image-{project}" in executed:
            required_files.update(
                (f"{project}-gate.json", f"{project}-all.json", f"{project}.spdx.json")
            )
    if not required_files <= set(receipt["files"]):
        raise GateError("Required scan/browser/SBOM evidence is incomplete")
    verify_results(path.parent, evidence)
    for name, image in receipt["images"].items():
        if name not in expected_images:
            continue
        image_id = image if name == "mssql" else image["id"]
        reference = (
            "mcr.microsoft.com/mssql/server:2022-latest" if name == "mssql" else image["tag"]
        )
        current = subprocess.check_output(
            ["docker", "image", "inspect", "--format={{.Id}}", reference], text=True
        ).strip()
        if current != image_id:
            raise GateError("Receipt image identity mismatch")
    return receipt


def verify(root: Path, path: Path, base: str, *, required_scope: str = "full") -> None:
    if required_scope not in ("full", "partial"):
        raise GateError("Invalid required receipt scope")
    # Reject partial evidence before invoking any live resource/environment probes.
    receipt = json.loads(path.read_text())
    if receipt.get("scope") not in ("full", "partial") or (
        required_scope == "full" and receipt["scope"] != "full"
    ):
        raise GateError("Receipt scope does not satisfy required full coverage")
    receipt = validate_receipt(root, path, base)
    print(
        f"VERIFIED {receipt['scope']} local gate: {receipt['identity']['head']} "
        f"base {receipt['identity']['base']}"
    )


@contextlib.contextmanager
def heavy_lock(timeout: int, inherited_fd: int | None = None) -> Iterator[None]:
    if inherited_fd is not None:
        if inherited_fd < 0:
            raise GateError("Inherited heavy-resource lock descriptor must be nonnegative")
        fd = os.dup(inherited_fd)
    else:
        fd = os.open(HEAVY_LOCK_PATH, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as stream:
        if inherited_fd is not None:
            actual = os.fstat(stream.fileno())
            expected = HEAVY_LOCK_PATH.stat(follow_symlinks=False)
            if (
                not stat.S_ISREG(actual.st_mode)
                or not stat.S_ISREG(expected.st_mode)
                or (actual.st_dev, actual.st_ino) != (expected.st_dev, expected.st_ino)
            ):
                raise GateError("Inherited descriptor is not the shared heavy-resource lock")
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if inherited_fd is not None:
                    raise GateError(
                        "Inherited heavy-resource lock is held by another owner"
                    ) from None
                if time.monotonic() >= deadline:
                    raise GateError("Global heavy-resource lock timeout") from None
                time.sleep(1)
        yield


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true")
    mode.add_argument("--changed", action="store_true")
    mode.add_argument("--resume", type=Path, metavar="FAILED_RECEIPT")
    mode.add_argument("--verify-receipt", type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--extra-test", action="append", default=[])
    parser.add_argument("--lock-timeout", type=int, default=600)
    parser.add_argument(
        "--heavy-lock-fd",
        type=int,
        help="Borrow the shared lock's inherited descriptor without releasing caller ownership",
    )
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--required-scope", choices=("full", "partial"), default="full")
    args = parser.parse_args()
    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel")).resolve()
    try:
        if args.verify_receipt:
            verify(
                root,
                args.verify_receipt.resolve(),
                args.base,
                required_scope=args.required_scope,
            )
        else:
            for value in args.extra_test:
                extra_selector(value)
            if args.out is None:
                raise GateError("--out is required and must be a new external directory")
            out = args.out.resolve()
            if out.is_relative_to(root) or out.exists():
                raise GateError(
                    "--out must be a new external directory; prior receipts are immutable"
                )
            clean_identity(root, args.base)
            if args.jobs < 1:
                raise GateError("--jobs must be positive")
            resume = args.resume.resolve() if args.resume else None
            if resume:
                parent = validate_receipt(root, resume, args.base, passing=False, new_output=out)
                if parent["status"] != "failed" or args.extra_test:
                    raise GateError("--resume needs a failed receipt and no --extra-test override")
                extras = parent["extras"]
                selected = parent["selection"]
            else:
                extras = args.extra_test
                selected = selection(root, args.base, "changed" if args.changed else "all", extras)
            admit_browser_output(out, selected["groups"])
            tool_identity()
            out.mkdir(mode=0o700, parents=True)

            def interrupted(signum: int, frame: Any) -> None:
                raise KeyboardInterrupt(f"Interrupted by signal {signum}")

            signal.signal(signal.SIGTERM, interrupted)
            signal.signal(signal.SIGINT, interrupted)
            queued = datetime.now(UTC).isoformat()
            with heavy_lock(args.lock_timeout, args.heavy_lock_fd):
                jobs = worker_limit(args.jobs)
                print(
                    f"Lock queued {queued}; acquired {datetime.now(UTC).isoformat()}; "
                    f"jobs={jobs}; groups={','.join(selected['groups'])}",
                    flush=True,
                )
                receipt = Runner(
                    root, out, args.base, extras, selected=selected, jobs=jobs, resume=resume
                ).run()
                verify(
                    root,
                    receipt,
                    args.base,
                    required_scope=(
                        "full" if selected["groups"] == required_groups(extras) else "partial"
                    ),
                )
            print(f"Receipt: {receipt}")
        return 0
    except (GateError, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
