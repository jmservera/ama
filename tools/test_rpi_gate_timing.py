"""Focused tests for the read-only gate timing analyzer (issue #1830)."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from collections.abc import Sequence
from contextlib import redirect_stderr, redirect_stdout
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

SPEC = importlib.util.spec_from_file_location(
    "rpi_gate_timing", Path(__file__).with_name("rpi-gate-timing.py")
)
assert SPEC and SPEC.loader
timing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(timing)

ORIGIN = datetime(2026, 11, 16, 10, 0, tzinfo=UTC)


def stamp(offset: float) -> str:
    return (ORIGIN + timedelta(seconds=offset)).isoformat()


def write_receipt(
    folder: Path,
    commands: Sequence[tuple[str, float, float]],
    *,
    jobs: int = 2,
    head: str = "a" * 40,
    **overrides: Any,
) -> Path:
    receipt: dict[str, Any] = {
        "schema": 4,
        "scope": "full",
        "status": "passed",
        "jobs": jobs,
        "image_cache": "fresh",
        "selection": {"mode": "all"},
        "tools": {"python3": "3.12"},
        "images": {},
        "sealed": stamp(max(end for _, _, end in commands) + 1),
        "identity": {"head": head},
        "commands": [
            {
                "group": group,
                "argv": ["python3", "-m", "unittest"],
                "started": stamp(start),
                "finished": stamp(end),
            }
            for group, start, end in commands
        ],
    }
    receipt.update(overrides)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "receipt.json"
    path.write_text(json.dumps(receipt))
    (folder / "receipt.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest() + "\n")
    return path


CHAIN = [("setup", 0, 10), ("a", 10, 40), ("b", 10, 20), ("c", 50, 90)]


def run(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = timing.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class ReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)

    def test_digest_mismatch_and_non_full_receipts_are_refused(self) -> None:
        path = write_receipt(self.root / "a", CHAIN)
        (path.parent / "receipt.sha256").write_text("0" * 64)
        self.assertEqual(run("report", str(path))[0], 2)
        partial = write_receipt(self.root / "b", CHAIN, scope="partial")
        self.assertEqual(run("report", str(partial))[0], 2)
        failed = write_receipt(self.root / "c", CHAIN, status="failed")
        self.assertEqual(run("report", str(failed))[0], 2)

    def test_span_group_wall_gap_and_chain_account_for_every_second(self) -> None:
        path = write_receipt(self.root / "a", CHAIN)
        code, out, _ = run("report", str(path))
        report = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(report["span_seconds"], 90.0)
        self.assertEqual(report["summed_command_seconds"], 10 + 30 + 10 + 40)
        self.assertEqual(report["groups"]["a"]["wall"], 30.0)
        self.assertEqual(report["chain_seconds"], report["span_seconds"])
        waits = [s for s in report["critical_chain"] if s["kind"] == "wait"]
        self.assertEqual([w["seconds"] for w in waits], [10.0])
        self.assertEqual(report["concurrency_seconds"]["2"], 10.0)

    def test_idle_gap_inside_a_group_and_queue_wait_from_the_log(self) -> None:
        commands = [("g", 0, 10), ("g", 30, 40)]
        path = write_receipt(self.root / "a", commands)
        log = self.root / "run.log"
        log.write_text(f"Lock queued {stamp(-5)}; acquired {stamp(-2)}; jobs=2\nrest\n")
        report = json.loads(run("report", str(path), "--log", str(log))[1])
        self.assertEqual(report["groups"]["g"]["idle_gaps"], [20.0])
        self.assertEqual(report["queue_wait_seconds"], 3.0)
        self.assertEqual(report["lock_to_seal_seconds"], 43.0)

    def test_repeated_identical_commands_are_listed_across_groups(self) -> None:
        path = write_receipt(self.root / "a", [("a", 0, 10), ("b", 10, 40), ("c", 40, 45)])
        receipt = json.loads(path.read_text())
        receipt["commands"][2]["argv"] = ["python3", "-m", "ruff"]
        path.write_text(json.dumps(receipt))
        (path.parent / "receipt.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest())
        report = json.loads(run("report", str(path))[1])
        self.assertEqual(len(report["repeated_commands"]), 1)
        row = report["repeated_commands"][0]
        self.assertEqual((row["runs"], row["seconds"], row["groups"]), (2, 40.0, ["a", "b"]))
        self.assertFalse(row["setup"])

    def test_missing_or_empty_log_is_refused_not_a_traceback(self) -> None:
        path = write_receipt(self.root / "a", [("g", 0, 10)])
        empty = self.root / "empty.log"
        empty.write_text("")
        for log in (self.root / "absent.log", empty):
            code, _out, err = run("report", str(path), "--log", str(log))
            self.assertEqual(code, 2)
            self.assertIn("REFUSED", err)

    def test_log_without_a_lock_line_reports_queue_wait_as_unmeasured(self) -> None:
        path = write_receipt(self.root / "a", [("g", 0, 10)])
        log = self.root / "run.log"
        log.write_text("jobs=2\n")
        report = json.loads(run("report", str(path), "--log", str(log))[1])
        self.assertIsNone(report["queue_wait_seconds"])
        self.assertIn("queue_wait_unavailable", report)
        self.assertNotIn("lock_to_seal_seconds", report)

    def test_malformed_or_negative_lock_line_is_refused(self) -> None:
        path = write_receipt(self.root / "a", [("g", 0, 10)])
        log = self.root / "run.log"
        for line in (
            "Lock queued not-a-time; acquired also-not; jobs=2",
            f"Lock queued {stamp(-2)}; acquired {stamp(-5)}; jobs=2",
        ):
            log.write_text(line + "\n")
            code, _out, err = run("report", str(path), "--log", str(log))
            self.assertEqual(code, 2)
            self.assertIn("REFUSED", err)

    def test_malformed_receipt_bodies_are_refused_not_a_traceback(self) -> None:
        good = {"group": "g", "argv": ["python3"], "started": stamp(0), "finished": stamp(5)}
        bodies = {
            "missing argv": [{"group": "g", "started": stamp(0), "finished": stamp(5)}],
            "bad time": [{**good, "started": "nope"}],
            "naive time": [{**good, "started": "2026-11-16T10:00:00"}],
            "reversed": [{**good, "started": stamp(5), "finished": stamp(0)}],
            "not a list": "nope",
        }
        for name, commands in bodies.items():
            with self.subTest(name):
                path = write_receipt(self.root / name.replace(" ", "-"), [("g", 0, 5)])
                receipt = json.loads(path.read_text())
                receipt["commands"] = commands
                path.write_text(json.dumps(receipt))
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                (path.parent / "receipt.sha256").write_text(digest + "\n")
                code, _out, err = run("report", str(path))
                self.assertEqual(code, 2)
                self.assertIn("REFUSED", err)

    def test_hash_valid_receipt_missing_header_fields_is_refused(self) -> None:
        fields = {
            "jobs": None,
            "image_cache": None,
            "sealed": None,
            "naive sealed": "2026-11-16T10:00:00",
            "zero jobs": 0,
        }
        for name, value in fields.items():
            with self.subTest(name):
                path = write_receipt(self.root / name.replace(" ", "-"), [("g", 0, 5)])
                receipt = json.loads(path.read_text())
                key = {"naive sealed": "sealed", "zero jobs": "jobs"}.get(name, name)
                if value is None:
                    del receipt[key]
                else:
                    receipt[key] = value
                path.write_text(json.dumps(receipt))
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                (path.parent / "receipt.sha256").write_text(digest + "\n")
                code, _out, err = run("report", str(path))
                self.assertEqual(code, 2)
                self.assertIn("REFUSED", err)

    def test_receipt_that_is_not_json_is_refused(self) -> None:
        path = write_receipt(self.root / "a", [("g", 0, 5)])
        path.write_text("{bad")
        (path.parent / "receipt.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest())
        code, _out, err = run("report", str(path))
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", err)

    def test_setup_commands_are_separated_by_exact_tokens(self) -> None:
        self.assertTrue(timing.is_setup(["python", "-m", "pip", "install"]))
        self.assertTrue(timing.is_setup(["docker", "build", "x"]))
        self.assertFalse(timing.is_setup(["python", "-m", "unittest", "pipeline"]))


class CompareTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        self.host = {
            "cpu_model": "x",
            "vcpus": 4,
            "memory_kib": 1,
            "docker_server": "27",
        }

    def arm(
        self,
        name: str,
        spans: list[int],
        groups: tuple[str, ...] = ("g",),
        **overrides: Any,
    ) -> tuple[list[str], Path, Path]:
        paths = [
            write_receipt(
                self.root / f"{name}{i}",
                [(group, 0, span) for group in groups],
                **overrides,
            )
            for i, span in enumerate(spans)
        ]
        manifest = self.root / f"{name}-host.json"
        manifest.write_text(json.dumps(self.host))
        records = self.root / f"{name}-verify.json"
        records.write_text(
            json.dumps(
                [
                    {
                        "receipt": str(p),
                        "command": "rpi-checks.py --verify-receipt",
                        "exit": 0,
                        "checkout": "/x",
                    }
                    for p in paths
                ]
            )
        )
        return [str(p) for p in paths], manifest, records

    def compare(self, before: Any, after: Any, *extra: str) -> tuple[int, dict[str, Any]]:
        code, out, _ = run(
            "compare",
            "--before", *before[0],
            "--after", *after[0],
            "--host-manifest-before", str(before[1]),
            "--host-manifest-after", str(after[1]),
            "--verification-before", str(before[2]),
            "--verification-after", str(after[2]),
            *extra,
        )  # fmt: skip
        return code, json.loads(out)

    def test_abba_arms_report_medians(self) -> None:
        code, report = self.compare(self.arm("b", [100, 120]), self.arm("a", [80, 90, 70]))
        self.assertEqual(code, 0)
        self.assertEqual(report["before"]["span_median"], 110)
        self.assertEqual(report["after"]["span_median"], 80)
        self.assertEqual(report["span_median_delta"], -30)

    def test_retried_shards_are_visible_in_report_and_compare(self) -> None:
        retry = {"group": "api-shard-2", "log": "l", "sha256": "0" * 64, "exit_code": 1, "argv": []}
        clean = write_receipt(self.root / "clean", CHAIN)
        self.assertEqual(json.loads(run("report", str(clean))[1])["retries"], 0)
        retried = write_receipt(self.root / "retried", CHAIN, retries=[retry, retry])
        report = json.loads(run("report", str(retried))[1])
        self.assertEqual((report["retries"], report["retried_groups"]), (2, ["api-shard-2"]))
        code, compared = self.compare(
            self.arm("b2", [100, 120], retries=[retry]), self.arm("a2", [80, 90])
        )
        self.assertEqual(code, 0)
        self.assertEqual((compared["before"]["retries"], compared["after"]["retries"]), (2, 0))

    def test_markdown_renders_a_table_or_the_refusal_reasons(self) -> None:
        def markdown(before: Any, after: Any) -> tuple[int, str]:
            code, out, _ = run(
                "compare",
                "--before", *before[0],
                "--after", *after[0],
                "--host-manifest-before", str(before[1]),
                "--host-manifest-after", str(after[1]),
                "--verification-before", str(before[2]),
                "--verification-after", str(after[2]),
                "--markdown",
            )  # fmt: skip
            return code, out

        code, out = markdown(self.arm("b", [100, 120]), self.arm("a", [80, 90]))
        self.assertEqual(code, 0)
        self.assertIn("| before | 2 | 110.0 | 100.0 | 120.0 | 0 |", out)
        self.assertIn("| after | 2 | 85.0 | 80.0 | 90.0 | 0 |", out)
        self.assertIn("delta (after minus before): -25.0 s", out)
        code, out = markdown(self.arm("b", [100]), self.arm("a", [80, 90]))
        self.assertEqual(code, 3)
        self.assertIn("Verdict: NONCOMPARABLE", out)
        self.assertIn("* before: at least two distinct receipts per arm are required", out)

    def test_single_receipt_arm_unlike_jobs_hosts_and_missing_records_are_refused(
        self,
    ) -> None:
        code, report = self.compare(self.arm("b", [100]), self.arm("a", [90, 80]))
        self.assertEqual(code, 3)
        self.assertIn("at least two", report["reasons"][0])
        code, report = self.compare(self.arm("b", [100, 101]), self.arm("a", [90, 80], jobs=3))
        self.assertIn("jobs differs", report["reasons"])
        before, after = self.arm("b", [100, 101]), self.arm("a", [90, 80])
        after[1].write_text(json.dumps(self.host | {"vcpus": 8}))
        self.assertIn("host vcpus differs", self.compare(before, after)[1]["reasons"])
        after[2].write_text("[]")
        self.assertEqual(self.compare(before, after)[0], 3)

    def test_duplicates_mixed_arms_and_empty_manifests_are_refused(self) -> None:
        before = self.arm("b", [100, 120])
        duplicate = ([before[0][0], before[0][0]], before[1], before[2])
        code, report = self.compare(duplicate, self.arm("a", [80, 90]))
        self.assertIn("distinct", report["reasons"][0])
        self.assertEqual(code, 3)
        shared = ([before[0][0], before[0][1]], before[1], before[2])
        self.assertIn("both arms", self.compare(before, shared)[1]["reasons"][0])
        mixed = self.arm("m", [100, 120])
        write_receipt(self.root / "m1", [("g", 0, 120)], jobs=9)
        self.assertIn("jobs differs", self.compare(mixed, self.arm("a", [80, 90]))[1]["reasons"])
        after = self.arm("e", [80, 90])
        after[1].write_text("{}")
        self.assertIn(
            "host manifest lacks",
            self.compare(self.arm("f", [1, 2]), after)[1]["reasons"][0],
        )

    def test_blank_or_zero_host_manifests_are_not_complete(self) -> None:
        blank = {"cpu_model": "", "vcpus": 0, "memory_kib": 0, "docker_server": ""}
        for placeholder in (
            blank,
            self.host | {"vcpus": True},
            self.host | {"cpu_model": " "},
        ):
            before, after = self.arm("b", [100, 120]), self.arm("a", [80, 90])
            for arm in (before, after):
                arm[1].write_text(json.dumps(placeholder))
            code, report = self.compare(before, after)
            self.assertEqual(code, 3, placeholder)
            self.assertEqual(report["verdict"], "NONCOMPARABLE")
            self.assertIn("host manifest lacks", report["reasons"][0])

    def test_executed_groups_and_command_contracts_must_match(self) -> None:
        both = ("g", "h")
        before = self.arm("b", [100, 120], both)
        code, report = self.compare(before, self.arm("a", [80, 90], ("g",)))
        self.assertEqual(code, 3)
        self.assertTrue(any("group set differs" in r for r in report["reasons"]), report)
        weak = self.arm("w", [80, 90], both)
        for name in weak[0]:
            data = json.loads(Path(name).read_text())
            data["commands"][1]["argv"] = ["python3", "-c", "pass"]
            Path(name).write_text(json.dumps(data))
            Path(name).with_name("receipt.sha256").write_text(
                hashlib.sha256(Path(name).read_bytes()).hexdigest() + "\n"
            )
        code, report = self.compare(before, weak)
        self.assertEqual(code, 3)
        self.assertTrue(any("command contract differs" in r for r in report["reasons"]), report)
        self.assertEqual(self.compare(before, self.arm("s", [80, 90], both))[0], 0)

    def mutate(
        self, made: tuple[list[str], Path, Path], change: Any
    ) -> tuple[list[str], Path, Path]:
        for item in made[0]:
            data = json.loads(Path(item).read_text())
            change(data["commands"])
            Path(item).write_text(json.dumps(data))
            Path(item).with_name("receipt.sha256").write_text(
                hashlib.sha256(Path(item).read_bytes()).hexdigest() + "\n"
            )
        return made

    def docker_arm(self, name: str, token: str, ident: str, image: str) -> Any:
        def change(commands: list[dict[str, Any]]) -> None:
            commands[0]["argv"] = [
                "docker",
                "run",
                "--label",
                f"ama.rpi.owner={token}",
                "x",
            ]
            commands[0]["env"] = {"ZF_SQL_PORT": ident[:5], "A": "1"}
            commands.append(commands[0] | {"argv": ["docker", "inspect", ident], "env": {}})
            commands.append(commands[0] | {"argv": ["docker", "rm", "-f", ident], "env": {}})
            commands.append(
                commands[0] | {"argv": ["docker", "image", "inspect", f"sha256:{image}"], "env": {}}
            )

        return self.mutate(self.arm(name, [100, 120]), change)

    def test_per_run_container_ids_and_owner_tokens_do_not_break_comparability(
        self,
    ) -> None:
        before = self.docker_arm("b", "a" * 24, "1" * 64, "c" * 64)
        after = self.docker_arm("a", "b" * 24, "2" * 64, "c" * 64)
        code, report = self.compare(before, after)
        self.assertEqual(code, 0, report)

    def test_image_id_drift_is_not_masked(self) -> None:
        before = self.docker_arm("b", "a" * 24, "1" * 64, "c" * 64)
        after = self.docker_arm("a", "b" * 24, "2" * 64, "d" * 64)
        code, report = self.compare(before, after)
        self.assertEqual(code, 3)
        self.assertIn("per-group command contract differs", report["reasons"])

    def test_cwd_env_and_execution_flag_drift_is_refused(self) -> None:
        drifts = {
            "cwd": lambda c: c[0].update(cwd="src/other"),
            "env value": lambda c: c[0].update(env={"ZF_TEST_MSSQL": "0"}),
            "env key": lambda c: c[0].update(env={"EXTRA": "1"}),
            "timeout": lambda c: c[0].update(timeout_seconds=1),
            "suite": lambda c: c[0].update(suite=True),
            "integration": lambda c: c[0].update(integration=True),
            "attempts": lambda c: c[0].update(attempts=3),
        }
        for name, drift in drifts.items():
            before = self.arm("b", [100, 120])
            code, report = self.compare(before, self.mutate(self.arm("a", [80, 90]), drift))
            self.assertEqual(code, 3, name)
            self.assertIn("per-group command contract differs", report["reasons"], name)

    def test_unlike_image_mode_and_tool_digest_are_refused(self) -> None:
        code, report = self.compare(
            self.arm("b", [1, 2]),
            self.arm("a", [1, 2], image_cache="warm", tools={"python3": "9"}),
        )
        self.assertEqual(code, 3)
        self.assertIn("image_cache differs", report["reasons"])
        self.assertIn("tools differs", report["reasons"])

    def test_receipt_image_identity_must_exist_and_the_pulled_base_must_match(
        self,
    ) -> None:
        groups = ("mssql", "image-api")

        def images(base: str, built: str, extra: bool = False) -> dict[str, Any]:
            result: dict[str, Any] = {
                "mssql": "sha256:" + base * 64,
                "image-api": {
                    "id": "sha256:" + built * 64,
                    "digests": [],
                    "tag": "t" + built,
                },
            }
            if extra:
                result["image-core"] = {"id": "sha256:" + built * 64}
            return result

        before = self.arm("b", [100, 120], groups, images=images("a", "b"))
        rebuilt = self.arm("r", [80, 90], groups, images=images("a", "c"))
        self.assertEqual(self.compare(before, rebuilt)[0], 0)
        cases = {
            "mssql base image identity differs": images("d", "b"),
            "receipt image sets differ": images("a", "b", extra=True),
            "receipt image identity is malformed": images("a", "b") | {"mssql": "latest"},
            "receipt images lack an identity for an executed image group": {},
        }
        for reason, drift in cases.items():
            code, report = self.compare(before, self.arm("x", [80, 90], groups, images=drift))
            self.assertEqual(code, 3, reason)
            self.assertIn(reason, report["reasons"])
        missing = self.arm("m", [80, 90], groups, images=None)
        self.assertEqual(self.compare(before, missing)[0], 3)

    def test_tree_delta_is_limited_to_the_runner_and_its_test(self) -> None:
        repo = self.root / "repo"
        repo.mkdir()

        def git(*args: str) -> str:
            env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
                   "GIT_COMMITTER_EMAIL": "t@x", "PATH": "/usr/bin:/bin"}  # fmt: skip
            return subprocess.run(
                ["git", "-C", str(repo), *args],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            ).stdout.strip()

        git("init", "-q")
        (repo / "tools").mkdir()
        (repo / "tools/rpi-checks.py").write_text("1")
        git("add", "-A")
        git("commit", "-qm", "one")
        first = git("rev-parse", "HEAD")
        (repo / "tools/rpi-checks.py").write_text("2")
        git("commit", "-qam", "two")
        runner_only = git("rev-parse", "HEAD")
        (repo / "other.txt").write_text("x")
        git("add", "-A")
        git("commit", "-qm", "three")
        wider = git("rev-parse", "HEAD")
        flags = ("--allow-tree-delta", "RUNNER_ONLY", "--repo", str(repo))
        before = self.arm("b", [100, 101], head=first)
        code, report = self.compare(before, self.arm("a", [90, 80], head=runner_only), *flags)
        self.assertEqual(code, 0, report)
        self.assertEqual(self.compare(before, self.arm("c", [90, 80], head=runner_only))[0], 3)
        code, report = self.compare(before, self.arm("d", [90, 80], head=wider), *flags)
        self.assertEqual(code, 3)
        self.assertIn("other.txt", report["reasons"][0])


if __name__ == "__main__":
    unittest.main()
