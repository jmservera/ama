"""Light deterministic tests of the issue #107 older-image SQL probe's own control logic.

Fidelity: these tests never start Docker, an older image or SQL Server. Docker is a small in-memory
fake behind `probe.sh`; the scenario test runs the fixed worker as plain subprocesses of the CURRENT
source over SQLite and is labelled as a self-test; it proves the probe, worker and judge fit
together, not that any older image is safe. The actual-image continuation is
`checks/old_image_sql_probe.py` and is never run by discovery.
"""

import copy
import importlib
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from checks import old_image_sql_probe as probe
from checks import old_image_worker as worker

STEPS = tuple(probe.PROTOCOL)
TASKS = dict(zip(probe.TASK_KEYS, ("t1", "t2", "t3", "t4", "t5"), strict=True))
FIRST = next(iter(worker.PACKAGED))


def release(status: str = "active", version: str = "v") -> dict[str, Any]:
    return dict(id="r", status=status, prompt_version=version)


def snap(tasks: dict[str, str], pool: list[int], revoked: str = "revoked") -> dict[str, Any]:
    return dict(
        releases={
            probe.GOOD: [release()],
            probe.REVOKED: [release(revoked)],
            probe.MISMATCHED: [release(revoked, probe.MUTATED)],
        },
        tasks=tasks,
        pool=[pool],
    )


def identity(cid: str) -> dict[str, Any]:
    return dict(
        modules={
            m: dict(path=f"/usr/local/lib/python3.12/site-packages/{i}.py", sha256="a" * 64)
            for i, m in enumerate(worker.PACKAGED)
        },
        missing=[],
        versions=dict.fromkeys(worker.VERSIONS, "1"),
        hostname=cid[:12],
    )


def good() -> dict[str, Any]:
    """Hand-built complete observations of an older process that behaves; mutated by the cases."""
    steps: dict[str, Any] = {}
    for i, name in enumerate(STEPS):
        key, again = probe.PROTOCOL[name]
        cid = str(i + 1) * 64
        steps[name] = dict(
            status="ok",
            action="provision" if name == "provision" else "execute",
            returncode=0,
            container_id=cid,
            spid=100,
            identity=identity(cid),
            provider_calls=0,
            tasks=[],
            executed=[dict(id=TASKS[key], before="pending", result=False, after="disabled")],
            reinvoked=[dict(capability=c, case=k, state="disabled") for c, k in again],
        )
    steps["provision"].update(
        provider_calls=1,
        executed=[dict(id="t1", before="pending", result=True, after="ready")],
        tasks=[
            dict(id=TASKS[k], capability=c, case=case, state="pending")
            for k, (c, case) in zip(probe.TASK_KEYS, probe.PLAN, strict=True)
        ],
    )
    steps["restart_remaining_allowance"].update(
        provider_calls=1, executed=[dict(id="t2", before="pending", result=True, after="ready")]
    )
    pending = dict(
        good1="ready", good2="pending", good3="pending", revoked="pending", mismatched="pending"
    )
    first = [probe.CALLS, 2000000, 1, 130]
    second = [probe.CALLS, 2000000, 2, 260]
    after_provision = snap(pending, first, "active")
    after_provision["releases"][probe.MISMATCHED] = [release("active")]
    pre_worker = snap(pending, first)
    pre_worker["releases"][probe.MISMATCHED] = [release("active", probe.MUTATED)]
    host = dict(
        session=100,
        tasks=dict(TASKS),
        after_provision=after_provision,
        after_revocation=snap(pending, first),
        after_revoked_restart=snap(dict(pending, revoked="disabled"), first),
        after_mutation=pre_worker,
        after_mismatched_restart=snap(
            dict(pending, revoked="disabled", mismatched="disabled"), first
        ),
        after_remaining=snap(dict(pending, good2="ready"), second),
        after_larger=snap(dict(pending, good2="ready", good3="disabled"), second),
    )
    return dict(steps=steps, host=host)


class Judge(unittest.TestCase):
    def outcome(
        self, change: Callable[[dict[str, Any]], None], strict: bool = True
    ) -> dict[str, Any]:
        obs = good()
        change(obs)
        return probe.judge(obs, strict)

    def outcome_of(self, obs: dict[str, Any]) -> dict[str, Any]:
        return probe.judge(obs, True)

    def test_well_behaved_complete_observations_are_accepted(self) -> None:
        self.assertEqual(self.outcome(lambda o: None)["outcome"], "ACCEPTED")

    def test_unsupported_step_or_missing_positive_control_is_never_a_pass(self) -> None:
        unsupported = self.outcome(lambda o: o["steps"]["provision"].update(status="unsupported"))
        self.assertEqual(unsupported["outcome"], "INSUFFICIENT")
        silent = self.outcome(lambda o: o["steps"]["provision"].update(provider_calls=0))
        self.assertEqual(silent["outcome"], "INSUFFICIENT")
        self.assertTrue(any("positive control" in m for m in silent["insufficient"]))

    def test_unproved_preconditions_are_insufficient_not_denial_evidence(self) -> None:
        def not_pending(o: dict[str, Any]) -> None:
            o["host"]["after_provision"]["tasks"]["revoked"] = "failed"

        self.assertEqual(self.outcome(not_pending)["outcome"], "INSUFFICIENT")

        def unread(o: dict[str, Any]) -> None:
            o["host"]["after_revocation"]["releases"][probe.REVOKED] = [release("active")]

        self.assertEqual(self.outcome(unread)["outcome"], "INSUFFICIENT")

    def test_dispatch_after_revocation_or_mismatch_is_a_violation(self) -> None:
        for step in ("restart_after_revocation", "restart_after_mismatch"):
            with self.subTest(step=step):
                obs = good()
                obs["steps"][step].update(provider_calls=1)
                self.assertEqual(probe.judge(obs, True)["outcome"], "VIOLATED")

    def test_restored_approval_or_open_request_is_a_violation(self) -> None:
        def restored(o: dict[str, Any]) -> None:
            o["host"]["after_revoked_restart"]["releases"][probe.REVOKED] = [release("active")]

        self.assertEqual(self.outcome(restored)["outcome"], "VIOLATED")

        def open_again(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_mismatch"]["reinvoked"][0]["state"] = "pending"

        self.assertEqual(self.outcome(open_again)["outcome"], "VIOLATED")

    def test_active_mutated_row_after_the_mismatch_worker_is_a_violation(self) -> None:
        def active(o: dict[str, Any]) -> None:
            o["host"]["after_mismatched_restart"]["releases"][probe.MISMATCHED] = [
                release("active", probe.MUTATED)
            ]

        verdict = self.outcome(active)
        self.assertEqual(verdict["outcome"], "VIOLATED")
        self.assertTrue(any("approval" in v for v in verdict["violations"]))

    def test_approval_restored_only_by_a_later_restart_is_a_violation(self) -> None:
        for snapshot in ("after_remaining", "after_larger"):
            for cap, version in ((probe.REVOKED, "v"), (probe.MISMATCHED, probe.MUTATED)):
                with self.subTest(snapshot=snapshot, capability=cap):
                    obs = good()
                    obs["host"][snapshot]["releases"][cap] = [release("active", version)]
                    self.assertEqual(probe.judge(obs, True)["outcome"], "VIOLATED")

    def test_unproved_mismatch_completion_does_not_blame_the_row(self) -> None:
        for broken in (
            dict(executed=[dict(id="t5", before="pending", error="boom")]),
            dict(reinvoked=[dict(capability="c", case="k", state="disabled", error="boom")]),
            dict(status="error", error="timed out"),
        ):
            with self.subTest(broken=sorted(broken)):
                obs = good()
                obs["steps"]["restart_after_mismatch"].update(broken)
                obs["host"]["after_mismatched_restart"]["releases"][probe.MISMATCHED] = [
                    release("active", probe.MUTATED)
                ]
                self.assertEqual(probe.judge(obs, True)["outcome"], "INSUFFICIENT")

    def test_incomplete_mismatch_completion_with_an_active_mutated_row_is_insufficient(
        self,
    ) -> None:
        def no_result(e: dict[str, Any]) -> None:
            del e["executed"][0]["result"]

        def no_after(e: dict[str, Any]) -> None:
            del e["executed"][0]["after"]

        def result_not_bool(e: dict[str, Any]) -> None:
            e["executed"][0]["result"] = "false"

        def no_state(e: dict[str, Any]) -> None:
            del e["reinvoked"][0]["state"]

        def no_reinvoke(e: dict[str, Any]) -> None:
            del e["reinvoked"]

        def wrong_task(e: dict[str, Any]) -> None:
            e["executed"][0]["id"] = TASKS["good1"]

        for change in (no_result, no_after, result_not_bool, no_state, no_reinvoke, wrong_task):
            with self.subTest(change=change.__name__):
                obs = good()
                change(obs["steps"]["restart_after_mismatch"])
                obs["host"]["after_mismatched_restart"]["releases"][probe.MISMATCHED] = [
                    release("active", probe.MUTATED)
                ]
                verdict = self.outcome_of(obs)
                self.assertEqual(verdict["outcome"], "INSUFFICIENT")
                self.assertEqual(verdict["violations"], [])

    def test_lost_malformed_or_unbound_release_state_is_insufficient(self) -> None:
        for snapshot in ("after_mismatched_restart", "after_remaining", "after_larger"):
            for rows in ([], [dict(id="r")], [dict(id="other", status="revoked")]):
                with self.subTest(snapshot=snapshot, rows=rows):
                    obs = good()
                    obs["host"][snapshot]["releases"][probe.MISMATCHED] = rows
                    self.assertEqual(probe.judge(obs, True)["outcome"], "INSUFFICIENT")
            obs = good()
            del obs["host"][snapshot]["releases"]
            self.assertEqual(probe.judge(obs, True)["outcome"], "INSUFFICIENT")

    def test_proved_active_release_survives_a_lost_bound_row(self) -> None:
        obs = good()
        obs["host"]["after_larger"]["releases"][probe.REVOKED] = [release("active")]
        obs["host"]["after_remaining"]["releases"][probe.MISMATCHED] = [
            release("revoked") | dict(id="gone"),
            release("active", probe.MUTATED) | dict(id="new"),
        ]
        verdict = probe.judge(obs, True)
        self.assertEqual(verdict["outcome"], "VIOLATED")
        self.assertTrue(verdict["insufficient"])

    def test_unrelated_row_cannot_establish_a_trigger(self) -> None:
        obs = good()
        obs["host"]["after_revocation"]["releases"][probe.REVOKED] = [
            release("active"),
            release("revoked") | dict(id="other"),
        ]
        obs["steps"]["restart_after_revocation"].update(provider_calls=1)
        self.assertEqual(probe.judge(obs, True)["outcome"], "INSUFFICIENT")
        obs = good()
        obs["host"]["after_mutation"]["releases"][probe.MISMATCHED] = [
            release("active", "v"),
            release("revoked", probe.MUTATED) | dict(id="other"),
        ]
        obs["steps"]["restart_after_mismatch"].update(provider_calls=1)
        self.assertEqual(probe.judge(obs, True)["outcome"], "INSUFFICIENT")

    def test_replenished_or_second_pool_is_a_violation(self) -> None:
        def refilled(o: dict[str, Any]) -> None:
            o["host"]["after_larger"]["pool"] = [[5, 2000000, 0, 0]]

        self.assertEqual(self.outcome(refilled)["outcome"], "VIOLATED")

        def second(o: dict[str, Any]) -> None:
            o["host"]["after_larger"]["pool"].append([5, 1, 0, 0])

        self.assertEqual(self.outcome(second)["outcome"], "VIOLATED")

    def test_token_ceiling_or_reserved_consumption_changes_are_violations(self) -> None:
        for change in ([2, 2000001, 2, 260], [2, 2000000, 2, 0], [2, 2000000, 1, 260]):
            with self.subTest(pool=change):
                obs = good()
                obs["host"]["after_larger"]["pool"] = [change]
                self.assertEqual(probe.judge(obs, True)["outcome"], "VIOLATED")
        obs = good()
        obs["host"]["after_remaining"]["pool"] = [[probe.CALLS, 2000000, 2, 100]]
        self.assertEqual(probe.judge(obs, True)["outcome"], "VIOLATED")

    def test_malformed_pool_is_insufficient(self) -> None:
        for bad in ([[2, 2000000, 2]], [[2, 2000000, 2, "x"]], []):
            with self.subTest(pool=bad):
                obs = good()
                obs["host"]["after_larger"]["pool"] = bad
                self.assertEqual(probe.judge(obs, True)["outcome"], "INSUFFICIENT")

    def test_violation_is_kept_when_a_later_step_errors_times_out_or_is_missing(self) -> None:
        for later in (
            dict(status="error", error="boom"),
            dict(status="unsupported"),
            dict(status="error", error="worker timed out"),
        ):
            with self.subTest(later=later):
                obs = good()
                obs["steps"]["restart_after_revocation"].update(provider_calls=1)
                obs["steps"]["restart_after_mismatch"] = later
                self.assertEqual(probe.judge(obs, True)["outcome"], "VIOLATED")
        obs = good()
        obs["steps"]["restart_after_revocation"].update(provider_calls=1)
        for name in STEPS[2:]:
            del obs["steps"][name]
        for key in (
            "after_mismatched_restart",
            "after_remaining",
            "after_larger",
            "after_mutation",
        ):
            del obs["host"][key]
        obs["host"]["error"] = "RuntimeError: host operation raised"
        verdict = probe.judge(obs, True)
        self.assertEqual(verdict["outcome"], "VIOLATED")
        self.assertTrue(verdict["insufficient"])

    def test_dispatch_is_not_a_violation_without_its_trigger_readback(self) -> None:
        def unread(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_revocation"].update(provider_calls=1)
            o["host"]["after_revocation"]["releases"][probe.REVOKED] = [release("active")]

        self.assertEqual(self.outcome(unread)["outcome"], "INSUFFICIENT")

    def test_raised_errors_are_insufficient_not_proof_of_refusal_or_violation(self) -> None:
        def reinvoke_raised(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_revocation"]["reinvoked"] = [dict(error="OperationalError")]

        self.assertEqual(self.outcome(reinvoke_raised)["outcome"], "INSUFFICIENT")

        def larger_raised(o: dict[str, Any]) -> None:
            o["steps"]["restart_larger_allowance"]["executed"] = [dict(error="OperationalError")]

        self.assertEqual(self.outcome(larger_raised)["outcome"], "INSUFFICIENT")

        def larger_not_refused(o: dict[str, Any]) -> None:
            o["host"]["after_larger"]["tasks"]["good3"] = "pending"

        self.assertEqual(self.outcome(larger_not_refused)["outcome"], "INSUFFICIENT")

    def test_missing_or_malformed_protocol_evidence_is_insufficient_never_accepted(self) -> None:
        def no_executed(o: dict[str, Any]) -> None:
            for step in o["steps"].values():
                step["executed"] = []

        def no_modules(o: dict[str, Any]) -> None:
            for step in o["steps"].values():
                step["identity"]["modules"] = {}

        def partial_modules(o: dict[str, Any]) -> None:
            for step in o["steps"].values():
                step["identity"]["modules"].pop(FIRST)

        def nonzero_exit(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_mismatch"]["returncode"] = 1

        def duplicate_ids(o: dict[str, Any]) -> None:
            o["host"]["tasks"]["good2"] = "t1"

        def missing_id(o: dict[str, Any]) -> None:
            o["host"]["tasks"]["revoked"] = None

        def duplicate_provision_ids(o: dict[str, Any]) -> None:
            o["steps"]["provision"]["tasks"][1]["id"] = "t1"

        def wrong_task_executed(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_revocation"]["executed"][0]["id"] = "t2"

        def wrong_pair(o: dict[str, Any]) -> None:
            o["steps"]["provision"]["tasks"][3]["case"] = "ZF-2"

        def no_reinvoke(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_mismatch"]["reinvoked"] = []

        def no_before_state(o: dict[str, Any]) -> None:
            del o["steps"]["restart_after_revocation"]["executed"][0]["before"]

        def no_result(o: dict[str, Any]) -> None:
            del o["steps"]["restart_larger_allowance"]["executed"][0]["result"]

        def missing_step(o: dict[str, Any]) -> None:
            del o["steps"]["restart_larger_allowance"]

        def missing_versions(o: dict[str, Any]) -> None:
            o["steps"]["provision"]["identity"].pop("versions")

        for change in (
            no_executed,
            no_modules,
            partial_modules,
            nonzero_exit,
            duplicate_ids,
            missing_id,
            duplicate_provision_ids,
            wrong_task_executed,
            wrong_pair,
            no_reinvoke,
            no_before_state,
            no_result,
            missing_step,
            missing_versions,
        ):
            with self.subTest(case=change.__name__):
                self.assertEqual(self.outcome(change)["outcome"], "INSUFFICIENT")

    def test_identity_and_independence_are_required_for_actual_runs(self) -> None:
        def editable(o: dict[str, Any]) -> None:
            for step in o["steps"].values():
                step["identity"]["modules"][FIRST]["path"] = "/src/a.py"

        self.assertEqual(self.outcome(editable)["outcome"], "INSUFFICIENT")
        self.assertEqual(self.outcome(editable, strict=False)["outcome"], "ACCEPTED")

        def shared_container(o: dict[str, Any]) -> None:
            o["steps"]["restart_larger_allowance"]["container_id"] = "1" * 64

        self.assertEqual(self.outcome(shared_container)["outcome"], "INSUFFICIENT")

        def drift(o: dict[str, Any]) -> None:
            o["steps"]["restart_after_mismatch"]["identity"]["modules"][FIRST]["sha256"] = "b" * 64

        self.assertEqual(self.outcome(drift)["outcome"], "INSUFFICIENT")

        def wrong_host(o: dict[str, Any]) -> None:
            o["steps"]["provision"]["identity"]["hostname"] = "elsewhere"

        self.assertEqual(self.outcome(wrong_host)["outcome"], "INSUFFICIENT")

    def test_reused_sequential_sql_session_ids_are_not_a_failure(self) -> None:
        def reused(o: dict[str, Any]) -> None:
            o["host"]["session"] = 57
            for step in o["steps"].values():
                step["spid"] = 57

        self.assertEqual(self.outcome(reused)["outcome"], "ACCEPTED")


class Scenario(unittest.TestCase):
    """Partial observations survive any later failure; no database or older image is involved."""

    def engine(self, failing: str | None, how: str) -> Any:
        fake = good()["steps"]

        class Fake:
            fidelity = "fake"
            site_packages_only = True

            def run(self, spec: dict[str, Any], label: str) -> dict[str, Any]:
                if label == failing:
                    if how == "raise":
                        raise RuntimeError("daemon gone")
                    return dict(status="error", error="worker timed out")
                step: dict[str, Any] = fake[label]
                return step

        return Fake()

    def run_scenario(self, failing: str | None, how: str, snapshots: int = 99) -> dict[str, Any]:
        calls = {"n": 0}
        template = good()["host"]

        def fake_snapshot(db: Any, tids: dict[str, str | None]) -> dict[str, Any]:
            calls["n"] += 1
            if calls["n"] > snapshots:
                raise RuntimeError("host operation raised")
            return copy.deepcopy(template["after_provision"])

        with (
            patch.object(probe, "snapshot", fake_snapshot),
            patch.object(probe, "revoke"),
            patch.object(probe, "mismatch"),
        ):
            obs: dict[str, Any] = dict(steps={}, host={})
            db = MagicMock()
            db.session.return_value = 1
            probe.scenario(self.engine(failing, how), db, {}, {}, obs)
        return obs

    def test_a_raising_or_failing_later_step_keeps_the_earlier_record(self) -> None:
        for how in ("raise", "error"):
            with self.subTest(how=how):
                obs = self.run_scenario("restart_after_revocation", how)
                self.assertEqual(obs["steps"]["provision"]["provider_calls"], 1)
                self.assertEqual(obs["steps"]["restart_after_revocation"]["status"], "error")
                self.assertIn("after_revoked_restart", obs["host"])
                self.assertNotIn("restart_after_mismatch", obs["steps"])

    def test_a_host_operation_that_raises_keeps_every_earlier_observation(self) -> None:
        obs = self.run_scenario(None, "raise", snapshots=2)
        self.assertEqual(obs["steps"]["provision"]["provider_calls"], 1)
        self.assertIn("after_provision", obs["host"])
        self.assertIn("after_revocation", obs["host"])
        self.assertIn("restart_after_revocation", obs["steps"])
        self.assertIn("host operation raised", obs["host"]["error"])


class Bounds(unittest.TestCase):
    def test_a_never_returning_host_call_is_abandoned_within_its_deadline(self) -> None:
        never = threading.Event()
        marker: list[str] = []
        with patch.object(probe, "ABANDONED", marker):
            abandoned = marker
            deadline = probe.Deadline(30)
            with self.assertRaises(probe.DeadlineExceeded):
                deadline.call("blocked query", 0.2, never.wait)
            self.assertEqual(abandoned, ["blocked query"])
            with self.assertRaises(probe.DeadlineExceeded):
                deadline.call("next", 5, lambda: 1)
        never.set()

    def test_the_whole_diagnostic_deadline_stops_new_work(self) -> None:
        with self.assertRaises(probe.DeadlineExceeded):
            probe.Deadline(-1).call("late", 5, lambda: 1)

    def test_bounded_db_stops_blocked_queries_without_real_sql(self) -> None:
        never = threading.Event()

        class Blocked:
            def query(self, sql: str, params: Any = ()) -> list[Any]:
                never.wait()
                return []

            def execute(self, sql: str, params: Any = ()) -> None:
                never.wait()

            def session(self) -> int | None:
                return 1

        with patch.object(probe, "ABANDONED", []):
            db = probe.BoundedDb(Blocked(), probe.Deadline(30), 0.2)
            with self.assertRaises(probe.DeadlineExceeded):
                db.query("select 1")
        never.set()

    def test_failed_readiness_connections_are_closed_and_bounded(self) -> None:
        conn = MagicMock()
        conn.execute.side_effect = RuntimeError("not ready")
        with self.assertRaises(probe.Refused):
            probe.wait_ready(lambda: conn, "x", probe.Deadline(30), seconds=0, pause=lambda s: None)
        conn.close.assert_called_once()

    def test_command_output_is_capped_and_a_timeout_kills_the_command(self) -> None:
        done = probe.sh([sys.executable, "-c", "print('x' * 100000)"], {}, 20, limit=100)
        self.assertLessEqual(len(done.stdout), 100)
        self.assertEqual(done.returncode, 0)
        with self.assertRaises(subprocess.TimeoutExpired):
            probe.sh([sys.executable, "-c", "import time; time.sleep(60)"], {}, 0.5)


class Guards(unittest.TestCase):
    def test_worker_argv_is_fixed_hardened_private_and_carries_no_secret(self) -> None:
        args = probe.worker_create_args(
            "ama-107-old-x-1", "x", "ama-107-net-x", "/p", "spec-1.json", ["ZF_SQL_PASSWORD"]
        )
        self.assertEqual(args[0], "create")
        self.assertEqual(args[args.index("-e") + 1], "ZF_SQL_PASSWORD")
        self.assertEqual(
            args[-4:], ["-I", "-B", "/probe/old_image_worker.py", "/probe/spec-1.json"]
        )
        self.assertIn(probe.PINNED_IMAGE, args)
        self.assertIn("/p:/probe:ro", args)
        for flag in ("--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges"):
            self.assertIn(flag, args)
        self.assertEqual(args[args.index("--network") + 1], "ama-107-net-x")
        joined = " ".join(args)
        for forbidden in ("--network=host", "docker.sock", "host-gateway", "--privileged", "host"):
            self.assertNotIn(forbidden, joined)
        self.assertIn(probe.OWNER_LABEL, args)
        self.assertNotIn("sh", args)
        self.assertFalse(any("=" in a and "PASSWORD" in a for a in args))

    def test_remote_or_tls_engine_is_refused_before_any_docker_call(self) -> None:
        with patch.object(probe, "sh") as run:
            for env in ({"DOCKER_HOST": "tcp://203.0.113.1:2375"}, {"DOCKER_CERT_PATH": "/x"}):
                with self.assertRaises(probe.Refused):
                    probe.preflight(env)
            run.assert_not_called()

    def test_a_different_image_or_context_is_refused(self) -> None:
        def fake(argv: list[str], *_: Any, **__: Any) -> subprocess.CompletedProcess[str]:
            text = {"show": "remote", "inspect": "sha256:other"}.get(argv[2], "")
            return subprocess.CompletedProcess(argv, 0, text, "")

        with patch.object(probe, "sh", fake), self.assertRaisesRegex(probe.Refused, "context"):
            probe.preflight({})

        def wrong_image(argv: list[str], *_: Any, **__: Any) -> subprocess.CompletedProcess[str]:
            text = {"show": "default"}.get(argv[2], "unix:///var/run/docker.sock")
            return subprocess.CompletedProcess(
                argv, 0, "sha256:other" if argv[2] == "inspect" and argv[1] == "image" else text, ""
            )

        with (
            patch.object(probe, "sh", wrong_image),
            self.assertRaisesRegex(probe.Refused, "pinned"),
        ):
            probe.preflight({})

    def test_output_must_be_new_absolute_and_outside_the_repository_even_through_links(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp)
            link = existing / "link"
            link.symlink_to(probe.ROOT)
            traversal = f"{probe.ROOT}/../{probe.ROOT.name}/x107-traversal"
            inside = probe.ROOT / "x107-inside"
            for bad in (
                "relative",
                str(existing),
                str(probe.ROOT / "out-107"),
                str(link / "x107-linked"),
                traversal,
                str(existing / "missing-parent" / "new"),
            ):
                with self.subTest(path=bad), self.assertRaises(probe.Refused):
                    probe.new_output(bad)
            self.assertFalse(inside.exists())
            self.assertFalse((probe.ROOT / "x107-linked").exists())
            self.assertFalse((probe.ROOT / "x107-traversal").exists())
            made = probe.new_output(str(existing / "new"))
            self.assertTrue(made.is_dir())
            self.assertEqual(made, (existing / "new").resolve())
            with self.assertRaises(probe.Refused):
                probe.new_output(str(existing / "new"))


class FakeDaemon:
    """A tiny in-memory Docker: only what `probe.Docker` calls, with switchable failures."""

    def __init__(self, run: str) -> None:
        self.run = run
        self.objects: dict[str, dict[str, str]] = {}
        self.fail: set[str] = set()
        self.timeout: set[str] = set()
        self.calls: list[list[str]] = []

    def add(self, kind: str, name: str, run: str | None = None) -> str:
        cid = format(len(self.objects) + 1, "x").rjust(64, "0")
        self.objects[cid] = dict(
            kind=kind, name=name, run=run or self.run, owner="issue-107-old-image-sql"
        )
        return cid

    def __call__(
        self, argv: list[str], env: Any, timeout: float, limit: int = 0
    ) -> subprocess.CompletedProcess[str]:
        self.calls.append(argv)
        args = argv[1:]
        verb = "network " + args[1] if args[0] == "network" else args[0]
        if verb in self.timeout:
            raise subprocess.TimeoutExpired(argv, timeout)
        if verb in self.fail:
            return subprocess.CompletedProcess(argv, 1, "", "daemon error pw=Sup3rSecret")
        out = ""
        if verb == "create":
            self.add("container", args[args.index("--name") + 1])
            out = "ignored-by-timeout-test"
            if "create-lost" in self.fail:
                return subprocess.CompletedProcess(argv, 0, "not-an-id", "")
        elif verb == "network create":
            out = self.add("network", args[-1])
        elif verb in ("ps", "network ls"):
            flt = next(a for a in args if a.startswith("name="))
            kind = "container" if verb == "ps" else "network"
            name = flt[5:].strip("^/$") if kind == "container" else flt[5:]
            out = "\n".join(
                cid for cid, o in self.objects.items() if o["kind"] == kind and name in o["name"]
            )
        elif verb in ("inspect", "network inspect"):
            o = self.objects.get(args[-1])
            if o is None:
                return subprocess.CompletedProcess(argv, 1, "", "no such object")
            prefix = "/" if o["kind"] == "container" else ""
            out = f"{args[-1]}|{prefix}{o['name']}|{o['run']}|{o['owner']}|true"
        elif verb == "rm":
            self.objects.pop(args[-1], None)
        elif verb == "network rm":
            self.objects.pop(args[-1], None)
        return subprocess.CompletedProcess(argv, 0, out, "")


class Lifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.daemon = FakeDaemon("run1")
        patcher = patch.object(probe, "sh", self.daemon)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.docker = probe.Docker(
            "run1", {}, probe.Deadline(600), ["Sup3rSecret"], pause=lambda s: None
        )

    def make(self, kind: str, name: str) -> str:
        return self.docker.create(kind, name, ["--name", name] if kind == "container" else [name])

    def test_clean_run_removes_everything_and_verifies_absence(self) -> None:
        net = self.make("network", "ama-107-net-run1")
        self.make("container", "ama-107-sql-run1")
        report = self.docker.cleanup()
        self.assertTrue(report["ok"], report)
        self.assertEqual(self.daemon.objects, {})
        self.assertEqual(report["expected"], ["ama-107-sql-run1", "ama-107-net-run1"])
        self.assertEqual(report["remaining"], [])
        self.assertTrue(net)

    def test_a_create_that_timed_out_but_completed_daemon_side_is_reconciled_and_removed(
        self,
    ) -> None:
        self.daemon.timeout.add("create")
        real = self.daemon.__call__

        def create_then_time_out(
            argv: list[str], env: Any, timeout: float, limit: int = 0
        ) -> subprocess.CompletedProcess[str]:
            if argv[1] == "create":
                self.daemon.timeout.discard("create")
                real(argv, env, timeout)
                self.daemon.timeout.add("create")
                raise subprocess.TimeoutExpired(argv, timeout)
            return real(argv, env, timeout, limit)

        with patch.object(probe, "sh", create_then_time_out):
            cid = self.make("container", "ama-107-old-run1-1")
            self.assertRegex(cid, r"^[0-9a-f]{64}$")
            report = self.docker.cleanup()
        self.assertEqual(self.daemon.objects, {})
        self.assertTrue(report["ok"], report)
        self.assertTrue(report["resources"][0]["reconciled_after_ambiguous_create"])
        self.assertTrue(report["resources"][0]["absent"])

    def test_an_unreconcilable_create_is_still_tracked_and_reported(self) -> None:
        self.daemon.timeout.add("create")
        with self.assertRaises(probe.CreateFailed):
            self.make("container", "ama-107-old-run1-2")
        report = self.docker.cleanup()
        self.assertEqual(report["expected"], ["ama-107-old-run1-2"])
        self.assertFalse(report["ok"])

    def test_remove_failures_and_timeouts_are_bounded_reported_and_never_ok(self) -> None:
        self.make("container", "ama-107-sql-run1")
        for mode in (self.daemon.fail, self.daemon.timeout):
            mode.add("rm")
            report = self.docker.cleanup()
            mode.discard("rm")
            self.assertFalse(report["ok"])
            self.assertEqual(report["remaining"], ["ama-107-sql-run1"])
            self.assertLessEqual(report["resources"][0]["removal_attempts"], probe.CLEANUP_TRIES)
            self.assertNotIn("Sup3rSecret", json.dumps(report))
            self.docker.resources["ama-107-sql-run1"]["attempts"] = 0
        self.assertTrue(self.docker.cleanup()["ok"])
        self.assertEqual(self.daemon.objects, {})

    def test_inspect_failure_leaves_absence_unverified(self) -> None:
        self.make("container", "ama-107-sql-run1")
        self.daemon.fail.add("inspect")
        report = self.docker.cleanup()
        self.assertFalse(report["ok"])
        self.assertEqual(report["remaining"], ["ama-107-sql-run1"])

    def test_only_exact_name_and_run_labels_are_ever_removed(self) -> None:
        self.make("container", "ama-107-sql-run1")
        other_run = self.daemon.add("container", "ama-107-sql-run1", run="other-run")
        superstring = self.daemon.add("container", "ama-107-sql-run1-extra")
        report = self.docker.cleanup()
        self.assertTrue(report["ok"], report)
        self.assertIn(other_run, self.daemon.objects)
        self.assertIn(superstring, self.daemon.objects)
        self.assertEqual(len(self.daemon.objects), 2)

    def test_behavioural_violation_is_kept_beside_containment_errors(self) -> None:
        containment = dict(ok=False, problems=["container x: still present"])
        kept = probe.conclude(
            dict(outcome="VIOLATED", insufficient=[], violations=["v"]), containment
        )
        self.assertEqual(kept["outcome"], "VIOLATED")
        self.assertEqual(kept["violations"], ["v"])
        self.assertEqual(kept["containment_errors"], containment["problems"])
        weak = probe.conclude(dict(outcome="ACCEPTED", insufficient=[], violations=[]), containment)
        self.assertEqual(weak["outcome"], "INSUFFICIENT")
        clean = probe.conclude(
            dict(outcome="ACCEPTED", insufficient=[], violations=[]), dict(ok=True, problems=[])
        )
        self.assertEqual(clean["outcome"], "ACCEPTED")


class WorkerProtocol(unittest.TestCase):
    def test_missing_protocol_member_is_reported_as_unsupported(self) -> None:
        real = importlib.import_module

        def blocked(name: str, *args: Any) -> Any:
            if name == "release_support":
                raise ImportError(name)
            return real(name, *args)

        with (
            patch.dict("os.environ", {"ZF_PROBE_BACKEND": "sqlite"}),
            patch.object(importlib, "import_module", blocked),
        ):
            result = worker.run(dict(action="identify"))
        self.assertEqual(result["status"], "unsupported")
        self.assertIn("release_support: ImportError", result["identity"]["missing"])


class SelfTest(unittest.TestCase):
    def test_probe_worker_and_judge_agree_over_sqlite_and_stay_labelled_lower_fidelity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            code = probe.main(["--self-test", "--out", str(out)])
            report = json.loads((out / "report.json").read_text())
        self.assertEqual(code, 0, report["verdict"])
        self.assertEqual(report["fidelity"], "current-source-self-test")
        self.assertEqual(report["verdict"]["outcome"], "ACCEPTED")
        self.assertNotEqual(report["fidelity"], "actual-older-image")
        calls = [s["provider_calls"] for s in report["observations"]["steps"].values()]
        self.assertEqual(calls, [1, 0, 0, 1, 0])


if __name__ == "__main__":
    unittest.main()
