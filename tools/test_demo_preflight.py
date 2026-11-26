from __future__ import annotations

import json
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import demo_preflight as pf

SECRET = "tok-SECRET-123"


def rev(name: str, health: str = "Healthy", traffic: int = 100, active: bool = True) -> dict:
    return {
        "name": name,
        "properties": {
            "active": active,
            "healthState": health,
            "runningState": "Running",
            "trafficWeight": traffic,
        },
    }


class FakeAz:
    def __init__(self, revisions=None, executions=None, deployment=None) -> None:
        self.deployment = deployment or {
            "image": "reg.azurecr.io/zava@sha256:" + "ab" * 32,
            "hardening": "enforced",
        }
        self.calls: list[list[str]] = []
        self.revisions = revisions if revisions is not None else [rev("app--1")]
        self.executions = (
            executions
            if executions is not None
            else [{"properties": {"status": "Succeeded", "startTime": "2026-11-21T10:00:00+00:00"}}]
        )

    def __call__(self, argv: list[str]) -> str:
        self.calls.append(argv)
        if "revision" in argv:
            return json.dumps(self.revisions)
        if "execution" in argv:
            return json.dumps(self.executions)
        if "logs" in argv:
            return "build: commit=0123456789abcdef"
        if "show" in argv and any("ZF_CONTAINER_HARDENING" in part for part in argv):
            return json.dumps(self.deployment)
        if "show" in argv:
            return "app.example.io\n"
        return SECRET


def ok_get(url: str) -> tuple[int, str]:
    return 200, "ok"


def counts() -> list[dict[str, object]]:
    return [{"home_id": "H1", "consent": "granted"}, {"home_id": "H2", "consent": "declined"}]


class Preflight(unittest.TestCase):
    def test_all_pass_and_record_has_counts_and_no_secret(self) -> None:
        az = FakeAz()
        results = pf.collect(az, ok_get, counts, apps=["a"], jobs=["j"])
        text = pf.render(results, datetime(2026, 11, 21, tzinfo=UTC), "ama")
        self.assertEqual(0, pf.exit_code(results, True))
        self.assertIn("cohort homes 2; declined 1, granted 1", text)
        self.assertIn("2026-11-21T00:00:00Z", text)
        self.assertNotIn(SECRET, text)

    def test_unhealthy_revision_or_split_traffic_fails(self) -> None:
        self.assertEqual(
            "FAIL", pf.check_revisions(FakeAz([rev("a", "Unhealthy")]), "g", "a").status
        )
        split = FakeAz([rev("a", traffic=60), rev("b", traffic=30)])
        self.assertEqual("FAIL", pf.check_revisions(split, "g", "a").status)
        self.assertEqual(
            "FAIL", pf.check_revisions(FakeAz([rev("a", active=False)]), "g", "a").status
        )

    def test_failed_job_fails_and_no_executions_is_unavailable(self) -> None:
        bad = FakeAz(executions=[{"properties": {"status": "Failed", "startTime": "2026-11-21"}}])
        self.assertEqual("FAIL", pf.check_job(bad, "g", "j").status)
        self.assertEqual("UNAVAILABLE", pf.check_job(FakeAz(executions=[]), "g", "j").status)

    def test_health_non_200_and_exception_fail(self) -> None:
        self.assertEqual("FAIL", pf.check_health(FakeAz(), lambda u: (503, ""), "g", "a").status)

        def boom(url: str) -> tuple[int, str]:
            raise OSError(SECRET)

        result = pf.check_health(FakeAz(), boom, "g", "a")
        self.assertEqual("FAIL", result.status)
        self.assertNotIn(SECRET, result.detail)

    def test_health_cold_start_timeout_retries_once(self) -> None:
        calls: list[int] = []

        def slow(url: str, timeout: int = 15) -> tuple[int, str]:
            calls.append(timeout)
            if timeout == 15:
                raise TimeoutError
            return 200, ""

        result = pf.check_health(FakeAz(), slow, "g", "a")
        self.assertEqual(("PASS", [15, 90]), (result.status, calls))

        def dead(url: str, timeout: int = 15) -> tuple[int, str]:
            raise TimeoutError

        self.assertEqual("FAIL", pf.check_health(FakeAz(), dead, "g", "a").status)

    def test_counts_unreachable_is_unavailable_and_strict_fails(self) -> None:
        def down() -> list[dict[str, object]]:
            raise ConnectionError(SECRET)

        result = pf.check_counts(down)
        self.assertEqual("UNAVAILABLE", result.status)
        self.assertNotIn(SECRET, result.detail)
        self.assertEqual(0, pf.exit_code([result], False))
        self.assertEqual(1, pf.exit_code([result], True))

    def test_deployment_reports_digest_and_requires_enforced_hardening(self) -> None:
        good = pf.check_deployment(FakeAz(), "ama", "app", "a")
        self.assertEqual(
            ("PASS", "digest abababababab; ZF_CONTAINER_HARDENING=enforced"),
            (good.status, good.detail),
        )
        for body in (
            {"image": "reg/zava@sha256:" + "cd" * 32, "hardening": None},
            {"image": "reg/zava:latest", "hardening": "enforced"},
        ):
            self.assertEqual(
                "FAIL", pf.check_deployment(FakeAz(deployment=body), "ama", "job", "j").status
            )

    def test_deployment_query_selects_only_the_hardening_value(self) -> None:
        az = FakeAz()
        pf.check_deployment(az, "ama", "job", "j")
        self.assertEqual(["containerapp", "job", "show"], az.calls[0][:3])
        self.assertEqual(1, sum("env[?name==" in part for part in az.calls[0]))

    def test_default_run_covers_agents_app_and_jobs(self) -> None:
        az = FakeAz()
        names = [r.name for r in pf.collect(az, ok_get, None)]
        self.assertIn("deployment ca-cutover-test-demo-agents", names)
        self.assertIn("deployment job-live-receiver", names)

    def test_build_commit_reads_last_startup_line_and_checks_expectation(self) -> None:
        def logs(text: str):
            return lambda argv: text

        out = 'x build: commit=0123456789ab\n{"Log":"build: commit=abcdef1234567"}'
        good = pf.check_build_commit(logs(out), "ama", "a", "abcdef1")
        self.assertEqual(("PASS", "commit abcdef123456"), (good.status, good.detail))
        self.assertEqual("FAIL", pf.check_build_commit(logs(out), "ama", "a", "9999999").status)
        self.assertEqual(
            "FAIL", pf.check_build_commit(logs("build: commit=unknown"), "ama", "a").status
        )
        self.assertEqual("UNAVAILABLE", pf.check_build_commit(logs("noise"), "ama", "a").status)

        def boom(argv: list[str]) -> str:
            raise RuntimeError("az exit 1")

        self.assertEqual("UNAVAILABLE", pf.check_build_commit(boom, "ama", "a").status)

    def test_only_read_only_az_commands(self) -> None:
        az = FakeAz()
        pf.collect(az, ok_get, None, apps=["a"], jobs=["j"])
        banned = {"create", "update", "delete", "start", "restart", "exec", "set", "stop"}
        for call in az.calls:
            self.assertFalse(banned & set(call), call)
        with self.assertRaises(ValueError):
            pf.run_az(["containerapp", "delete", "-n", "x"])


if __name__ == "__main__":
    unittest.main()
