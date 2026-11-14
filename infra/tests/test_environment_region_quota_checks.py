"""Region and quota parameter-set contract and preflight checks (issue 137)."""

import importlib.util
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_bicep_policy import compile_bicep, evaluate

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "region_quota_preflight", ROOT / "scripts" / "region_quota_preflight.py"
)
assert SPEC and SPEC.loader
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)

SETS = {
    "dev": "main.bicepparam",
    "test": "main.test.bicepparam",
    "pilot": "main.pilot.example.bicepparam",
}
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")


def params(name: str) -> dict:
    return PREFLIGHT.read_params((ROOT / SETS[name]).read_text(encoding="utf-8"))


def statuses(results: list[dict]) -> dict[str, str]:
    return {r["check"]: r["status"] for r in results}


class ParameterSetContractTests(unittest.TestCase):
    def test_every_set_declares_region_and_quota_parameters(self) -> None:
        for env in SETS:
            with self.subTest(env=env):
                p = params(env)
                for name in PREFLIGHT.REQUIRED_PARAMS:
                    self.assertIn(name, p)
                self.assertEqual(p["environmentName"], env)
                self.assertIn("aiModelFallbackLocation", p)

    def test_template_parameters_are_not_hardcoded(self) -> None:
        for name in ("aiModelLocation", "aiModelFallbackLocation", "modelCapacityBudget"):
            self.assertRegex(MAIN, rf"(?m)^param {name} ")
        self.assertRegex(MAIN, r"projectName: 'zava-forward-agents'\n\s+location: aiModelLocation")
        self.assertNotRegex(MAIN, r"aiModelLocation: '")

    def test_committed_sets_never_claim_a_recorded_check(self) -> None:
        for env in SETS:
            with self.subTest(env=env):
                self.assertEqual(params(env)["regionCheckReference"], "")
                self.assertEqual(params(env)["quotaCheckReference"], "")

    def test_pilot_region_is_an_unresolved_placeholder(self) -> None:
        self.assertEqual(params("pilot")["aiModelLocation"], "")
        self.assertEqual(params("dev")["aiModelLocation"], "uksouth")


class PreflightTests(unittest.TestCase):
    record = {
        "checked_on": "2026-11-14",
        "regions": ["uksouth"],
        "quotas": [
            {
                "name": "model-gpt-4.1-nano",
                "region": "uksouth",
                "limit": 50,
                "used": 2,
                "requested": 1,
            }
        ],
    }

    def test_committed_sets_block_without_a_record(self) -> None:
        for env in SETS:
            with self.subTest(env=env):
                s = statuses(PREFLIGHT.evaluate(params(env)))
                self.assertEqual(s["parameters-explicit"], "pass")
                self.assertEqual(s["check-record"], "blocked")
                self.assertEqual(s["regionCheckReference-recorded"], "blocked")
        self.assertEqual(
            statuses(PREFLIGHT.evaluate(params("pilot")))["location-selected"], "blocked"
        )

    def test_complete_set_with_record_passes(self) -> None:
        p = params("test") | {"regionCheckReference": "r", "quotaCheckReference": "q"}
        results = PREFLIGHT.evaluate(p, self.record)
        self.assertTrue(all(r["status"] == "pass" for r in results), results)

    def test_quota_shortfall_unrecorded_region_and_budget_fail(self) -> None:
        p = params("dev") | {"regionCheckReference": "r", "quotaCheckReference": "q"}
        short = {**self.record, "regions": ["northeurope"]}
        short["quotas"] = [
            {"name": "model-x", "region": "uksouth", "limit": 5, "used": 4, "requested": 31}
        ]
        s = statuses(PREFLIGHT.evaluate(p, short))
        self.assertEqual(s["regions-covered"], "fail")
        self.assertEqual(s["quota-model-x"], "fail")
        self.assertEqual(s["model-budget"], "fail")

    def test_fallback_equal_to_primary_fails_and_output_is_deterministic(self) -> None:
        p = params("dev") | {"aiModelFallbackLocation": "uksouth"}
        self.assertEqual(statuses(PREFLIGHT.evaluate(p))["fallback-differs"], "fail")
        self.assertEqual(PREFLIGHT.evaluate(p), PREFLIGHT.evaluate(p))


class GuardTests(unittest.TestCase):
    def test_guard_names_new_checks(self) -> None:
        guard = (ROOT / "modules" / "guard.bicep").read_text(encoding="utf-8")
        for name in ("aiFallbackLocationMustDiffer", "modelCapacityMustFitBudget"):
            self.assertRegex(guard, rf"param {name} string")
            self.assertIn(name, MAIN)
        self.assertRegex(MAIN, r"chatModelCapacity <= modelCapacityBudget")
        self.assertIsNotNone(re.search(r"aiModelLocation", MAIN))
        self.assertTrue(callable(compile_bicep) and callable(evaluate))


if __name__ == "__main__":
    unittest.main()
