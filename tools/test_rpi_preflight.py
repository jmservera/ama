"""Focused tests for the non-receipt preflight helper (issue #1830)."""

from __future__ import annotations

import fcntl
import importlib.util
import io
import json
import os
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

PASSWORD = "Aa1!test-only-secret"
IMAGE_ID = "sha256:" + "e" * 64
REGISTRY_DIGEST = "mcr.microsoft.com/mssql/server@sha256:" + "f" * 64
NOW = datetime(2026, 11, 16, 11, 0, tzinfo=UTC)
HERE = Path(__file__).resolve().parent


def load(name: str, filename: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pre = load("rpi_preflight", "rpi-preflight.py")
GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "PATH": os.environ["PATH"],
}
PASSING = (
    "import unittest\n"
    "class T(unittest.TestCase):\n"
    "    def test_one(self): self.assertTrue(True)\n"
    "    def test_two(self): self.assertTrue(True)\n"
)
SKIPPING = (
    "import unittest\n"
    "class T(unittest.TestCase):\n"
    "    @unittest.skip('opt-in')\n"
    "    def test_one(self): pass\n"
)
FAILING = "import unittest\nclass T(unittest.TestCase):\n    def test_one(self): self.fail('x')\n"
MUTATING = (
    "import unittest, pathlib\n"
    "class T(unittest.TestCase):\n"
    "    def test_one(self):\n"
    "        root = pathlib.Path(__file__).resolve().parents[3]\n"
    "        (root / 'cache').mkdir(exist_ok=True)\n"
    "        (root / 'cache' / 'x').write_text('changed')\n"
)
IMPORT_MUTATING = (
    "import pathlib\n"
    "root = pathlib.Path(__file__).resolve().parents[3]\n"
    "(root / 'cache' / 'x').write_text('changed at import')\n"
    "raise ImportError('boom')\n"
)
LEAKING = (
    "import os, unittest\n"
    "class T(unittest.TestCase):\n"
    "    def test_one(self):\n"
    "        self.assertNotIn('LEAK_ME', os.environ)\n"
    "        self.assertNotIn('ZF_SQL_PASSWORD', os.environ)\n"
)


def run_main(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = pre.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class Base(unittest.TestCase):
    admission_open = True

    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.base = Path(self.dir.name).resolve()
        self.repo = self.base / "repo"
        self.out = self.base / "out"
        self.repo.mkdir()
        self.git("init", "-q")
        (self.repo / ".gitignore").write_text("cache/\n")
        (self.repo / "cache").mkdir()
        (self.repo / "cache" / "x").write_text("original")
        for project in pre.PROJECTS:
            (self.repo / "src" / project / "tests").mkdir(parents=True)
        self.write("src/core/tests/test_ok.py", PASSING)
        self.write("src/core/tests/test_skip.py", SKIPPING)
        self.write("src/core/tests/test_fail.py", FAILING)
        self.write("src/core/tests/test_mut.py", MUTATING)
        self.write("src/core/tests/test_env.py", LEAKING)
        self.write("src/core/src/thing.py", "x = 1\n")
        self.write("src/api/tests/test_api.py", PASSING)
        self.write("tools/new-thing.py", "")
        self.write("docs/a.md", "")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        patcher = patch.object(pre, "check_interpreter", lambda python, repo: None)
        patcher.start()
        self.addCleanup(patcher.stop)
        if self.admission_open:
            # Fixtures only: the command line cannot reach the retained mechanics.
            gate = patch.object(pre, "refuse_selected_code_execution", lambda *_: None)
            gate.start()
            self.addCleanup(gate.stop)

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            capture_output=True,
            text=True,
            check=True,
            env=GIT_ENV,
        ).stdout

    def write(self, name: str, text: str) -> None:
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run_pre(self, *argv: str) -> tuple[int, str, str]:
        return run_main("--python", sys.executable, "--repo", str(self.repo), *argv)


class SelectorTests(Base):
    def test_passing_selector_exits_zero_and_records_a_non_receipt(self) -> None:
        code, out, _ = self.run_pre("--test", "core:test_ok", "--out", str(self.out))
        self.assertEqual(code, 0, out)
        result = json.loads((self.out / "preflight-result.json").read_text())
        self.assertIs(result["receipt"], False)
        self.assertEqual(result["kind"], "rpi-preflight")
        self.assertEqual(result["commands"][0]["tests_listed"], 2)
        for key in ("schema", "sealed", "owner", "groups", "identity"):
            self.assertNotIn(key, result)
        self.assertIn("NON-RECEIPT", out)

    def test_invalid_selectors_and_paths_exit_two(self) -> None:
        for value in (
            "core:../x",
            "-core:test_ok",
            "web:test_ok",
            "core:test_ok;rm",
            "core:test_missing_module",
        ):
            self.assertEqual(self.run_pre(f"--test={value}")[0], 2, value)
        self.write("src/core/tests/test_new.py", PASSING)
        self.assertEqual(self.run_pre("--test", "core:test_new")[0], 0)

    def test_zero_tests_and_import_failures_exit_two_without_running(self) -> None:
        self.assertEqual(self.run_pre("--test", "core:test_ok.Nope.method")[0], 2)
        self.assertEqual(self.run_pre("--test", "core:test_ok.T.test_absent")[0], 2)
        self.write("src/core/tests/test_broken.py", "import does_not_exist\n")
        self.git("add", "-A")
        self.assertEqual(self.run_pre("--test", "core:test_broken")[0], 2)

    def test_a_skipped_test_a_failure_and_dry_run_are_not_passes(self) -> None:
        self.assertEqual(self.run_pre("--test", "core:test_skip")[0], 1)
        self.assertEqual(self.run_pre("--test", "core:test_fail")[0], 1)
        code, out, _ = self.run_pre("--test", "core:test_ok", "--dry-run")
        self.assertEqual(code, 6)
        self.assertIn("result: not-pass", out)

    def test_environment_is_scrubbed(self) -> None:
        with patch.dict(os.environ, {"LEAK_ME": "1", "ZF_SQL_PASSWORD": "secret"}):
            self.assertEqual(self.run_pre("--test", "core:test_env")[0], 0)

    def test_judge_requires_a_plain_ok_and_the_listed_count(self) -> None:
        self.assertIsNone(pre.judge_unittest("Ran 2 tests in 0.1s\n\nOK\n", 2, 0))
        self.assertIsNotNone(pre.judge_unittest("Ran 1 test in 0.1s\n\nOK\n", 2, 0))
        self.assertIsNotNone(pre.judge_unittest("Ran 0 tests in 0.0s\n\nOK\n", 0, 0))
        self.assertIsNotNone(pre.judge_unittest("Ran 2 tests in 0.1s\n\nOK (skipped=1)\n", 2, 0))


class OutputAndMutationTests(Base):
    def test_out_must_be_external_short_and_free_of_a_receipt(self) -> None:
        self.assertEqual(
            self.run_pre("--test", "core:test_ok", "--out", str(self.repo / "o"))[0], 2
        )
        (self.out).mkdir()
        (self.out / "receipt.json").write_text("{}")
        self.assertEqual(self.run_pre("--test", "core:test_ok", "--out", str(self.out))[0], 2)
        long = self.base / ("x" * 60)
        self.assertEqual(self.run_pre("--test", "core:test_ok", "--out", str(long))[0], 2)

    def test_a_change_to_an_already_ignored_file_is_detected(self) -> None:
        code, out, _ = self.run_pre("--test", "core:test_mut")
        self.assertEqual(code, 4, out)
        self.assertEqual((self.repo / "cache" / "x").read_text(), "changed")

    def test_an_import_time_mutation_followed_by_an_import_error_is_reported(
        self,
    ) -> None:
        self.write("src/core/tests/test_importmut.py", IMPORT_MUTATING)
        self.git("add", "-A")
        code, out, err = self.run_pre("--test", "core:test_importmut", "--out", str(self.out))
        self.assertEqual(code, 4, out + err)
        result = json.loads((self.out / "preflight-result.json").read_text())
        self.assertEqual(result["source_mutations"], ["cache/x"])
        self.assertIn("fails to import", result["refusal"])
        self.assertIn("cache/x", out)

    def test_the_verifier_rejects_the_preflight_json(self) -> None:
        self.run_pre("--test", "core:test_ok", "--out", str(self.out))
        runner = load("rpi_checks_readonly", "rpi-checks.py")
        with self.assertRaises(runner.GateError):
            runner.verify(self.repo, self.out / "preflight-result.json", "0" * 40)


class CoverageTests(Base):
    def cover(self, path: str, *targets: str, extra: tuple[str, ...] = ()) -> tuple[int, str, str]:
        pairs: list[str] = []
        for target in targets:
            pairs += ["--covers", f"{path}={target}"]
        return self.run_pre("--file", path, *pairs, *extra)

    def test_declared_unit_coverage_passes_and_missing_declaration_is_uncovered(
        self,
    ) -> None:
        api_only = ("--test", "api:test_api")
        self.write("src/api/src/mod.py", "")
        self.git("add", "-A")
        self.assertEqual(self.cover("src/api/src/mod.py", "api:test_api", extra=api_only)[0], 0)
        self.assertEqual(self.run_pre("--file", "src/api/src/mod.py", *api_only)[0], 3)

    def test_core_requires_every_consumer_project(self) -> None:
        code, out, _ = self.cover(
            "src/core/src/thing.py", "core:test_ok", extra=("--test", "core:test_ok")
        )
        self.assertEqual(code, 3)
        self.assertIn("unit:api", out)

    def test_api_web_needs_a_browser_target_and_store_needs_sql(self) -> None:
        self.write("src/api/src/web/page.js", "")
        self.write("src/api/src/store_x.py", "")
        self.git("add", "-A")
        unit = ("--test", "api:test_api")
        code, out, _ = self.cover("src/api/src/web/page.js", "api:test_api", extra=unit)
        self.assertEqual((code, "browser" in out), (3, True))
        code, out, _ = self.cover("src/api/src/store_x.py", "api:test_api", extra=unit)
        self.assertEqual((code, "sql" in out), (3, True))

    def test_unknown_tools_path_is_uncovered_docs_are_inert_and_allow_warns(
        self,
    ) -> None:
        unit = ("--test", "core:test_ok")
        self.assertEqual(self.run_pre("--file", "tools/new-thing.py", *unit)[0], 3)
        self.assertEqual(self.run_pre("--file", "docs/a.md", *unit)[0], 0)
        code, out, _ = self.run_pre("--file", "tools/new-thing.py", "--allow-uncovered", *unit)
        self.assertEqual(code, 3)
        self.assertIn("WARNING", out)
        self.assertIn("result: not-pass", out)

    def test_covers_must_name_a_file_and_a_target(self) -> None:
        self.assertEqual(
            self.run_pre(
                "--test",
                "core:test_ok",
                "--file",
                "docs/a.md",
                "--covers",
                "docs/a.md=zzz",
            )[0],
            2,
        )

    def test_file_paths_reject_escapes_and_symlinks(self) -> None:
        (self.base / "outside.txt").write_text("x")
        os.symlink(self.base / "outside.txt", self.repo / "link.txt")
        self.git("add", "-A")
        for value in ("../outside.txt", "/etc/passwd", "link.txt", "-x"):
            self.assertEqual(self.run_pre("--test", "core:test_ok", f"--file={value}")[0], 2, value)


class PrerequisiteTests(Base):
    def test_busy_heavy_lock_is_not_queued(self) -> None:
        lock = self.base / "heavy.lock"
        with patch.object(pre, "HEAVY_LOCK_PATH", lock), lock.open("w") as held:
            fcntl.flock(held, fcntl.LOCK_EX)
            with self.assertRaises(pre.PreflightError) as caught:
                pre.heavy_lock(0).__enter__()
        self.assertEqual(caught.exception.code, 5)

    def test_browser_check_name_axe_digest_and_out_are_validated(self) -> None:
        self.write(
            "src/api/checks/demo_check.py",
            "import argparse\np=argparse.ArgumentParser()\n"
            'p.add_argument("--axe")\np.add_argument("--out")\n',
        )
        self.git("add", "-A")
        known = pre.tracked_or_intended(self.repo)
        with self.assertRaises(pre.PreflightError):
            pre.browser_check_args(self.repo, "../demo_check", known, None, None)
        with self.assertRaises(pre.PreflightError):
            pre.browser_check_args(self.repo, "demo_check", known, None, self.out)
        axe = self.base / "axe.js"
        axe.write_text("not pinned")
        with self.assertRaises(pre.PreflightError) as caught:
            pre.browser_check_args(self.repo, "demo_check", known, axe, self.out)
        self.assertIn("pinned", str(caught.exception))

    def sql_env(self, **change: str) -> dict[str, str]:
        return {
            "ZF_TEST_MSSQL": "1",
            "ZF_SQL_SERVER": "127.0.0.1",
            "ZF_SQL_PORT": "32000",
            "ZF_SQL_DATABASE": "rpi_disposable",
            "ZF_SQL_AUTH": "password",
            "ZF_SQL_USER": "sa",
            "ZF_SQL_PASSWORD": PASSWORD,
        } | change

    def inspect(self, **change: object) -> list[dict[str, object]]:
        metadata: dict[str, object] = {
            "Id": "a" * 64,
            "Created": "2026-11-16T10:00:00.123456789Z",
            "Image": IMAGE_ID,
            "HostConfig": {
                "Binds": None,
                "VolumesFrom": None,
                "RestartPolicy": {"Name": "no"},
            },
            "State": {"Running": True, "StartedAt": "2026-11-16T10:00:01.5Z"},
            "Config": {
                "Labels": {"ama.rpi.owner": "owner-token-1"},
                "Image": "mcr.microsoft.com/mssql/server:2022-latest",
                "Env": ["ACCEPT_EULA=Y", f"MSSQL_SA_PASSWORD={PASSWORD}"],
            },
            "Mounts": [],
            "NetworkSettings": {
                "IPAddress": "172.17.0.2",
                "Ports": {"1433/tcp": [{"HostIp": "127.0.0.1", "HostPort": "32000"}]},
            },
        }
        return [metadata | change]

    def docker(
        self,
        inspect: object = None,
        host: str = "unix:///var/run/docker.sock",
        listening: bool = True,
        image: object = None,
    ) -> ExitStack:
        data = self.inspect() if inspect is None else inspect
        image_data = (
            [{"Id": IMAGE_ID, "RepoDigests": [REGISTRY_DIGEST]}] if image is None else image
        )

        def query(*args: str) -> tuple[int, str]:
            if args[:2] == ("context", "inspect"):
                return 0, json.dumps([{"Endpoints": {"docker": {"Host": host}}}])
            self.assertEqual(args[0], "--host", "every daemon call must pin the verified socket")
            if args[2:4] == ("image", "inspect"):
                return 0, json.dumps(image_data)
            return 0, json.dumps(data)

        def verify(port: int, addresses: set[str], proc: Path | None = None) -> None:
            if not listening:
                raise pre.PreflightError(5, "no verified local listener")

        stack = ExitStack()
        proc = Path(stack.enter_context(tempfile.TemporaryDirectory()))
        (proc / "self").mkdir()
        (proc / "self/uid_map").write_text("         0          0 4294967295\n")
        stack.enter_context(patch.object(pre, "PROC", proc))
        stack.enter_context(patch.object(pre, "trusted_socket", lambda path: path))
        stack.enter_context(patch.object(pre, "verify_local_target", verify))
        stack.enter_context(patch.object(pre, "utc_now", lambda: NOW))
        stack.enter_context(patch.object(pre, "docker_query", query))
        return stack

    def refused(self, env: dict[str, str], stack: ExitStack, label: str) -> None:
        with (
            stack,
            patch.dict(os.environ, env),
            self.assertRaises(pre.PreflightError, msg=label),
        ):
            pre.owned_container("a" * 64, "owner-token-1")

    def test_sql_requires_an_owned_loopback_container(self) -> None:
        with self.docker(), patch.dict(os.environ, self.sql_env()):
            pre.owned_container("a" * 64, "owner-token-1")
        config = self.inspect()[0]["Config"]
        assert isinstance(config, dict)
        cases = {
            "unlabelled": self.inspect(Config=config | {"Labels": {}}),
            "foreign owner": self.inspect(
                Config=config | {"Labels": {"ama.rpi.owner": "someone-else-1"}}
            ),
            "stopped": self.inspect(State={"Running": False}),
            "public": self.inspect(
                NetworkSettings={
                    "IPAddress": "172.17.0.2",
                    "Ports": {"1433/tcp": [{"HostIp": "0.0.0.0", "HostPort": "32000"}]},
                }
            ),
            "port": self.inspect(
                NetworkSettings={
                    "IPAddress": "172.17.0.2",
                    "Ports": {"1433/tcp": [{"HostIp": "127.0.0.1", "HostPort": "1"}]},
                }
            ),
            "other image": self.inspect(Config=config | {"Image": "postgres:16"}),
        }
        for name, metadata in cases.items():
            with (
                self.docker(metadata),
                patch.dict(os.environ, self.sql_env()),
                self.assertRaises(pre.PreflightError, msg=name) as caught,
            ):
                pre.owned_container("a" * 64, "owner-token-1")
            self.assertEqual(caught.exception.code, 5, name)

    def test_sql_refuses_persistent_mounts_and_unproven_provenance(self) -> None:
        host = {"Binds": None, "VolumesFrom": None, "RestartPolicy": {"Name": "no"}}
        state = {"Running": True, "StartedAt": "2026-11-16T10:00:01Z"}
        volume = {
            "Type": "volume",
            "Name": "mssql-data",
            "Destination": "/var/opt/mssql",
        }
        cases = {
            "named volume": self.inspect(Mounts=[volume]),
            "anonymous volume": self.inspect(Mounts=[volume | {"Name": "f" * 64}]),
            "bind mount": self.inspect(Mounts=[{"Type": "bind", "Source": "/data"}]),
            "tmpfs": self.inspect(Mounts=[{"Type": "tmpfs", "Destination": "/x"}]),
            "mounts missing": self.inspect(Mounts=None),
            "binds in host config": self.inspect(HostConfig=host | {"Binds": ["v:/var/opt/mssql"]}),
            "volumes from": self.inspect(HostConfig=host | {"VolumesFrom": ["other"]}),
            "mount in host config": self.inspect(HostConfig=host | {"Mounts": [volume]}),
            "restart policy": self.inspect(HostConfig=host | {"RestartPolicy": {"Name": "always"}}),
            "host config missing": [
                {k: v for k, v in self.inspect()[0].items() if k != "HostConfig"}
            ],
            "stale creation": self.inspect(Created="2026-11-16T04:59:59Z"),
            "future creation": self.inspect(
                Created="2026-11-16T11:05:00Z",
                State=state | {"StartedAt": "2026-11-16T11:06:00Z"},
            ),
            "started before created": self.inspect(
                State=state | {"StartedAt": "2026-11-16T09:00:00Z"}
            ),
            "never started": self.inspect(State=state | {"StartedAt": "0001-01-01T00:00:00Z"}),
            "unparseable creation": self.inspect(Created="yesterday"),
            "naive creation": self.inspect(Created="2026-11-16T10:00:00"),
            "missing creation": [{k: v for k, v in self.inspect()[0].items() if k != "Created"}],
            "image id is not a digest": self.inspect(Image="mcr.microsoft.com/mssql/server:x"),
        }
        for name, metadata in cases.items():
            self.refused(self.sql_env(), self.docker(metadata), name)
        images = {
            "locally built image": [{"Id": IMAGE_ID, "RepoDigests": []}],
            "retagged foreign image": [
                {"Id": IMAGE_ID, "RepoDigests": ["evil/mssql@sha256:" + "f" * 64]}
            ],
            "mixed digests": [{"Id": IMAGE_ID, "RepoDigests": [REGISTRY_DIGEST, "evil@sha256:1"]}],
            "image id mismatch": [{"Id": "sha256:" + "1" * 64, "RepoDigests": [REGISTRY_DIGEST]}],
            "image unavailable": [],
            "digests missing": [{"Id": IMAGE_ID}],
        }
        for name, image in images.items():
            self.refused(self.sql_env(), self.docker(image=image), name)

    def test_sql_refuses_a_remote_docker_daemon_or_context(self) -> None:
        self.refused(self.sql_env(), self.docker(host="tcp://203.0.113.5:2376"), "remote host")
        self.refused(self.sql_env(), self.docker(host="ssh://user@remote"), "ssh host")
        for name in ("DOCKER_HOST", "DOCKER_CONTEXT"):
            self.refused(self.sql_env() | {name: "remote"}, self.docker(), name)

    def test_sql_binds_the_connection_to_the_inspected_container(self) -> None:
        self.refused(self.sql_env(ZF_SQL_PASSWORD="another"), self.docker(), "password mismatch")
        self.refused(self.sql_env(ZF_SQL_PASSWORD=""), self.docker(), "empty password")
        self.refused(self.sql_env(ZF_SQL_AUTH="integrated"), self.docker(), "auth")
        self.refused(self.sql_env(ZF_SQL_USER="other"), self.docker(), "user")
        self.refused(self.sql_env(ZF_SQL_DATABASE="production"), self.docker(), "database")
        self.refused(self.sql_env(ZF_SQL_SERVER="localhost"), self.docker(), "name not address")
        self.refused(self.sql_env(), self.docker(listening=False), "no local listener")
        config = self.inspect()[0]["Config"]
        assert isinstance(config, dict)
        no_secret = self.inspect(Config=config | {"Env": ["ACCEPT_EULA=Y"]})
        self.refused(self.sql_env(), self.docker(no_secret), "container lacks bound secret")

    def sql_argv(self) -> tuple[str, ...]:
        self.write("src/api/tests/test_sqlish.py", PASSING)
        self.git("add", "-A")
        return (
            "--sql-test",
            "api:test_sqlish",
            "--sql-container",
            "a" * 64,
            "--sql-owner",
            "o" * 8,
        )

    def contact_guards(self, stack: ExitStack, skip: tuple[str, ...] = ()) -> dict[str, MagicMock]:
        """Fail any Docker, socket, process-table, lock, discovery or test contact."""
        guards = {}
        for name in (
            "docker_query",
            "socket_peer",
            "local_docker_daemon",
            "owned_container",
            "verify_local_target",
            "candidates",
            "list_tests",
            "run",
            "heavy_lock",
            "check_interpreter",
        ):
            if name in skip:
                continue
            guards[name] = stack.enter_context(
                patch.object(pre, name, side_effect=AssertionError(f"{name} was contacted"))
            )
        return guards

    def test_sql_admission_is_closed_even_when_every_legacy_check_would_pass(self) -> None:
        argv = self.sql_argv()
        for dry in ((), ("--dry-run",)):
            with ExitStack() as stack:
                guards = self.contact_guards(stack)
                stack.enter_context(patch.dict(os.environ, self.sql_env()))
                code, _, err = self.run_pre(*argv, *dry)
            self.assertEqual(code, 5, dry)
            self.assertIn("not met", err)
            for guard in guards.values():
                guard.assert_not_called()

    def test_a_root_created_socket_with_an_unprivileged_acceptor_is_never_contacted(
        self,
    ) -> None:
        argv = self.sql_argv()
        path = self.base / "delegated.sock"
        accepted: list[bytes] = []
        listener = socket.socket(socket.AF_UNIX)
        listener.bind(str(path))
        listener.listen(4)
        listener.settimeout(0.3)

        def accept() -> None:
            try:
                connection, _ = listener.accept()
            except OSError:
                return
            with connection:
                accepted.append(connection.recv(64))

        thread = threading.Thread(target=accept)
        thread.start()
        self.addCleanup(listener.close)
        with ExitStack() as stack:
            guards = self.contact_guards(stack)
            stack.enter_context(patch.dict(os.environ, self.sql_env(DOCKER_HOST=f"unix://{path}")))
            stack.enter_context(
                patch.object(pre, "trusted_socket", side_effect=AssertionError("contacted"))
            )
            code, _, _ = self.run_pre(*argv)
        thread.join()
        self.assertEqual(code, 5)
        self.assertEqual(accepted, [])
        guards["socket_peer"].assert_not_called()
        guards["docker_query"].assert_not_called()

    def test_a_substituted_listener_is_never_reached_before_or_between_connections(
        self,
    ) -> None:
        argv = self.sql_argv()
        substitute = socket.socket()
        substitute.bind(("127.0.0.1", 0))
        substitute.listen(8)
        substitute.setblocking(False)
        self.addCleanup(substitute.close)
        port = str(substitute.getsockname()[1])
        for outcome in (None, pre.PreflightError(5, "replaced between connections")):
            with ExitStack() as stack:
                guards = self.contact_guards(stack)
                stack.enter_context(patch.dict(os.environ, self.sql_env(ZF_SQL_PORT=port)))
                guards["owned_container"].side_effect = outcome
                code, _, _ = self.run_pre(*argv)
            self.assertEqual(code, 5, outcome)
            for guard in guards.values():
                guard.assert_not_called()
        with self.assertRaises(BlockingIOError):
            substitute.accept()

    def test_sql_refuses_missing_container_flag_and_non_loopback_server(self) -> None:
        self.write("src/api/tests/test_sqlish.py", PASSING)
        self.git("add", "-A")
        self.assertEqual(self.run_pre("--sql-test", "api:test_sqlish")[0], 5)
        code = self.run_pre("--sql-test", "api:test_sqlish", "--sql-container", "a" * 64)[0]
        self.assertEqual(code, 5)
        self.refused(self.sql_env(ZF_SQL_SERVER="db.example.invalid"), self.docker(), "server")
        self.refused(self.sql_env(ZF_TEST_MSSQL=""), self.docker(), "opt-in")

    def fake_python(self, origins: dict[str, list[str]]) -> Path:
        script = self.base / "python"
        script.write_text(f"#!/bin/sh\ncat <<'EOF'\n{json.dumps(origins)}\nEOF\n")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        return script

    def test_interpreter_must_import_every_project_from_this_checkout(self) -> None:
        real = load("rpi_preflight_real", "rpi-preflight.py")
        mine = {p: [str(self.repo / "src" / p / "src" / "zava_forward" / p)] for p in real.PROJECTS}
        real.check_interpreter(self.fake_python(mine), self.repo)
        other = self.base / "other" / "src" / "api" / "src" / "zava_forward" / "api"
        for label, origins in {
            "api from another checkout": mine | {"api": [str(other)]},
            "one of two path entries": mine | {"agents": [*mine["agents"], str(other)]},
            "project not installed": {k: v for k, v in mine.items() if k != "importer"},
            "no path": mine | {"core": []},
        }.items():
            with self.assertRaises(real.PreflightError, msg=label) as caught:
                real.check_interpreter(self.fake_python(origins), self.repo)
            self.assertEqual(caught.exception.code, 5, label)
        with self.assertRaises(real.PreflightError) as caught:
            real.check_interpreter(Path(sys.executable), self.repo)
        self.assertEqual(caught.exception.code, 5)


HARNESS = (
    "import pathlib\n"
    "def main(argv=None):\n"
    "    pathlib.Path(__file__).resolve().parents[4].joinpath('harness-ran').write_text('x')\n"
    "    return 0\n"
)
WRAPPERS = {
    "browser check": (
        "--browser-check",
        "wrapper_check",
        "src/api/checks/wrapper_check.py",
        "from checks.sensor_sql_check import main\nif __name__ == '__main__':\n    main()\n",
    ),
    "test wrapper method": (
        "--test",
        "api:test_wrapper",
        "src/api/tests/test_wrapper.py",
        (
            "import unittest\nfrom checks.sensor_sql_check import main\n"
            "class T(unittest.TestCase):\n    def test_one(self):\n        main([])\n"
        ),
    ),
    "import-time call": (
        "--test",
        "api:test_wrapper",
        "src/api/tests/test_wrapper.py",
        "from checks.sensor_sql_check import main\nmain([])\n",
    ),
    "load_tests hook": (
        "--browser-test",
        "api:test_wrapper",
        "src/api/tests/test_wrapper.py",
        (
            "from checks.sensor_sql_check import main\n"
            "def load_tests(loader, tests, pattern):\n    main([])\n    return tests\n"
        ),
    ),
    "arbitrary callable": (
        "--test",
        "api:test_wrapper.wipe",
        "src/api/tests/test_wrapper.py",
        "from checks.sensor_sql_check import main\ndef wipe():\n    main([])\n",
    ),
    "sql selector": (
        "--sql-test",
        "api:test_wrapper",
        "src/api/tests/test_wrapper.py",
        "from checks.sensor_sql_check import main\nmain([])\n",
    ),
}


class AdmissionTests(Base):
    """Issue #1830 correction 5: selected code is refused before anything imports or runs it."""

    admission_open = False

    def sinks(self, stack: ExitStack) -> dict[str, MagicMock]:
        names = (
            ("pre", "git"),
            ("pre", "check_interpreter"),
            ("pre", "list_tests"),
            ("pre", "run"),
            ("pre", "heavy_lock"),
            ("pre", "docker_query"),
            ("subprocess", "Popen"),
            ("subprocess", "run"),
            ("socket", "socket"),
        )
        return {
            f"{owner}.{name}": stack.enter_context(
                patch.object(pre if owner == "pre" else globals()[owner], name)
            )
            for owner, name in names
        }

    def test_every_selection_path_is_refused_before_any_code_or_process(self) -> None:
        self.write("src/api/checks/sensor_sql_check.py", HARNESS)
        for label, (flag, value, path, source) in WRAPPERS.items():
            self.write(path, source)
            self.git("add", "-A")
            for dry in ((), ("--dry-run",)):
                with ExitStack() as stack:
                    sinks = self.sinks(stack)
                    code, out, err = self.run_pre(flag, value, *dry)
                self.assertEqual(code, 5, (label, dry))
                self.assertIn("Nothing was imported or run", err)
                self.assertEqual(out, "")
                for sink in sinks.values():
                    sink.assert_not_called()
                self.assertFalse((self.base / "harness-ran").exists(), label)
                self.assertFalse((self.repo / "harness-ran").exists(), label)

    def test_a_repository_controlled_git_on_path_is_never_executed(self) -> None:
        shim = self.base / "bin"
        shim.mkdir()
        sentinel = self.base / "git-ran"
        git = shim / "git"
        git.write_text(f"#!/bin/sh\ntouch {sentinel}\n")
        git.chmod(0o755)
        self.write("src/api/tests/test_wrapper.py", PASSING)
        with patch.dict(os.environ, {"PATH": str(shim)}):
            code, _, _ = run_main(
                "--python", sys.executable, "--repo", str(self.repo), "--test", "api:test_wrapper"
            )
        self.assertEqual(code, 5)
        self.assertFalse(sentinel.exists())

    def test_an_empty_request_is_still_an_input_error_without_git(self) -> None:
        with patch.object(pre, "git") as git:
            code, _, _ = self.run_pre("--file", "docs/a.md")
        self.assertEqual(code, 2)
        git.assert_not_called()

    def test_the_admission_function_refuses_any_selection_and_only_a_selection(self) -> None:
        pre.refuse_selected_code_execution([], [], [], [])
        for position in range(4):
            selections: list[list[str]] = [[], [], [], []]
            selections[position] = ["x"]
            with self.assertRaises(pre.PreflightError) as caught:
                pre.refuse_selected_code_execution(*selections)
            self.assertEqual(caught.exception.code, 5)


class SqlProvenanceTests(unittest.TestCase):
    """Kernel-side evidence for the Docker socket and the loopback listener (isolated fixtures)."""

    PROXY = (
        "/usr/bin/docker-proxy",
        "-proto",
        "tcp",
        "-host-ip",
        "127.0.0.1",
        "-host-port",
        "32000",
        "-container-ip",
        "172.17.0.2",
        "-container-port",
        "1433",
        "-use-listen-fd",
        "",
    )
    LISTEN = "   0: 0100007F:7D00 00000000:0000 0A 00000000:00000000 00:00000000 00000000 "

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.proc = Path(directory.name)
        self.uids: dict[str, int] = {}
        (self.proc / "net").mkdir()
        self.table("tcp", [(self.LISTEN, 0, 4242)])
        self.table("tcp6", [])
        self.process(100, "dockerd", 1, ("/usr/bin/dockerd", "-H", "fd://", ""))
        self.process(200, "docker-proxy", 100, self.PROXY)
        self.process(300, "bash", 1, None)
        patcher = patch.object(pre, "owner_uid", lambda path: self.uids[path.name])
        patcher.start()
        self.addCleanup(patcher.stop)

    def table(self, name: str, rows: list[tuple[str, int, int]]) -> None:
        header = "  sl  local_address rem_address   st\n"
        lines = [f"{line}{uid:8d}        0 {inode} 1\n" for line, uid, inode in rows]
        (self.proc / "net" / name).write_text(header + "".join(lines))

    def process(
        self,
        pid: int,
        comm: str,
        ppid: int,
        argv: tuple[str, ...] | None,
        uid: int = 0,
        start: int = 5000,
    ) -> None:
        folder = self.proc / str(pid)
        folder.mkdir(exist_ok=True)
        zeros = " ".join(["0"] * 17)
        (folder / "stat").write_text(f"{pid} ({comm}) S {ppid} {zeros} {start} 0\n")
        if argv is not None:
            (folder / "cmdline").write_bytes("\0".join(argv).encode())
        self.uids[str(pid)] = uid

    def verify(self, address: str = "172.17.0.2") -> None:
        pre.verify_local_target(32000, {address}, self.proc)

    def refused(self, label: str, *, address: str = "172.17.0.2") -> None:
        with self.assertRaises(pre.PreflightError, msg=label) as caught:
            self.verify(address)
        self.assertEqual(caught.exception.code, 5, label)

    def test_a_default_userland_proxy_container_is_accepted_despite_process_churn(
        self,
    ) -> None:
        self.verify()
        (self.proc / "400").mkdir()

        self.verify()

    def test_proxy_and_listener_substitution_is_refused(self) -> None:
        self.table("tcp", [(self.LISTEN, 1000, 4242)])
        self.refused("user-owned loopback listener")
        self.table("tcp", [(self.LISTEN.replace("0100007F", "00000000"), 0, 4242)])
        self.refused("wildcard listener")
        self.table("tcp", [(self.LISTEN, 0, 4242), (self.LISTEN, 1000, 4243)])
        self.refused("a second listener shadows the port")
        self.table("tcp", [(self.LISTEN, 0, 4242)])
        self.table("tcp6", [(self.LISTEN.replace("0100007F", "0" * 32), 1000, 1)])
        self.refused("ipv6 wildcard listener")
        self.table("tcp6", [])
        self.table("tcp", [])
        self.refused("no listener")
        self.table("tcp", [(self.LISTEN, 0, 0)])
        self.refused("no inode")
        self.table("tcp", [(self.LISTEN, 0, 4242)])
        self.verify()

    def test_a_fake_or_misplaced_docker_proxy_is_refused(self) -> None:
        self.process(200, "docker-proxy", 100, self.PROXY, uid=1000)
        self.refused("proxy process owned by a user")
        self.process(200, "docker-proxy", 1, self.PROXY)
        self.refused("proxy not a child of dockerd")
        self.process(
            200,
            "docker-proxy",
            100,
            self.PROXY[:5] + ("-host-port", "1") + self.PROXY[7:],
        )
        self.refused("proxy for another port")
        self.process(200, "docker-proxy", 100, self.PROXY[:10] + ("-container-port", "1434", ""))
        self.refused("proxy for another container port")
        self.process(200, "docker-proxy", 100, self.PROXY)
        self.refused("proxy for another container address", address="172.17.0.9")
        self.process(201, "docker-proxy", 100, self.PROXY)
        self.refused("two proxies hold the port")
        shutil.rmtree(self.proc / "201")
        shutil.rmtree(self.proc / "200")
        self.refused("no proxy at all")

    def test_the_daemon_must_be_exactly_one_root_dockerd(self) -> None:
        self.process(100, "dockerd", 1, ("/usr/bin/dockerd", ""), uid=1000)
        self.refused("dockerd owned by a user")
        self.process(100, "dockerd", 1, ("/tmp/socat", "TCP:remote:2375", ""))
        self.refused("daemon process is not dockerd")
        self.process(100, "dockerd", 1, ("/usr/bin/dockerd", ""))
        self.process(101, "dockerd", 1, ("/usr/bin/dockerd", ""), uid=1000)
        self.refused("a second dockerd")
        shutil.rmtree(self.proc / "101")
        shutil.rmtree(self.proc / "100")
        self.refused("no dockerd (remote daemon behind a proxy socket)")

    def test_unreadable_docker_evidence_and_identity_change_are_refused(self) -> None:
        (self.proc / "200" / "cmdline").unlink()
        self.refused("candidate command line unreadable")
        self.process(200, "docker-proxy", 100, self.PROXY)

        def swap(proc: Path, port: int) -> list[tuple[str, int, int]]:
            self.process(200, "docker-proxy", 100, self.PROXY, start=6000)
            return [("0100007F", 0, 4242)]

        with (
            patch.object(pre, "tcp_listeners", swap),
            self.assertRaises(pre.PreflightError) as caught,
        ):
            self.verify()
        self.assertIn("changed", str(caught.exception))

    @unittest.skipIf(os.getuid() == 0, "needs an unprivileged caller")
    def test_a_user_created_unix_socket_proxy_is_refused_without_a_request(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "docker.sock")
            seen: list[bytes] = []
            server = socket.socket(socket.AF_UNIX)
            server.bind(path)
            server.listen(1)
            self.addCleanup(server.close)

            def accept() -> None:
                connection, _ = server.accept()
                with connection:
                    connection.settimeout(0.5)
                    try:
                        seen.append(connection.recv(64))
                    except OSError:
                        pass

            thread = threading.Thread(target=accept)
            thread.start()
            self.assertEqual(pre.socket_peer(path), os.getuid())
            thread.join(5)
            self.assertEqual(seen, [b""])
            with self.assertRaises(pre.PreflightError) as caught:
                pre.trusted_socket(path)
            self.assertEqual(caught.exception.code, 5)

    def test_socket_ownership_peer_directory_and_namespace_checks(self) -> None:
        def entry(mode: int, uid: int = 0) -> os.stat_result:
            return os.stat_result((mode, 1, 1, 1, uid, 0, 0, 0, 0, 0))

        socket_mode, directory = stat.S_IFSOCK | 0o660, stat.S_IFDIR | 0o755

        def lstat(unsafe: str = "", peer_owner: int = 0) -> ExitStack:
            def fake(self: Path) -> os.stat_result:
                if str(self) == "/run/docker.sock":
                    return entry(socket_mode, peer_owner)
                return entry(directory | (0o002 if str(self) == unsafe else 0), 0)

            stack = ExitStack()
            stack.enter_context(patch.object(pre.Path, "lstat", fake))
            stack.enter_context(patch.object(pre.os.path, "realpath", lambda p: "/run/docker.sock"))
            return stack

        with lstat(), patch.object(pre, "socket_peer", lambda path: 0):
            self.assertEqual(pre.trusted_socket("/var/run/docker.sock"), "/run/docker.sock")
        cases = {
            "non-root peer (proxy)": (lstat, 1000),
            "socket owned by a user": (lambda: lstat(peer_owner=1000), 0),
            "world-writable directory": (lambda: lstat(unsafe="/run"), 0),
        }
        for label, (make, peer) in cases.items():
            with (
                make(),
                patch.object(pre, "socket_peer", lambda path, peer=peer: peer),
                self.assertRaises(pre.PreflightError, msg=label),
            ):
                pre.trusted_socket("/var/run/docker.sock")
        with self.assertRaises(pre.PreflightError):
            pre.trusted_socket("relative.sock")

    def test_a_non_initial_user_namespace_is_refused(self) -> None:
        for mapping in ("0 1000 1", "0 0 1", ""):
            self.proc.joinpath("self").mkdir(exist_ok=True)
            self.proc.joinpath("self/uid_map").write_text(mapping)
            with (
                patch.object(pre, "PROC", self.proc),
                patch.dict(os.environ, {}, clear=False),
                self.assertRaises(pre.PreflightError, msg=mapping),
            ):
                pre.local_docker_daemon()


if __name__ == "__main__":
    unittest.main()
