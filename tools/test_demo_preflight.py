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
    def __init__(self, revisions=None, executions=None) -> None:
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
