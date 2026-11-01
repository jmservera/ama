"""Monitoring coverage register, indicator and diagnostic-sanitiser checks (issue 146)."""

import unittest
from pathlib import Path

from zava_forward.core import monitoring_coverage as mc

INFRA = Path(__file__).resolve().parents[3] / "infra"
CONSTRUCTED: dict[str, float | bool | str] = {"limit": 0.1, "min_sample": 20, "constructed": True}
APPROVED: dict[str, float | bool | str] = {
    "limit": 0.1,
    "min_sample": 20,
    "approved_by": "Named Assurance Lead",
}


def _evaluate(
    events: object = 1,
    denominator: object = 50,
    complete: bool = True,
    threshold: dict[str, float | bool | str] | None = CONSTRUCTED,
    owner: str | None = "Safety and Assurance appointee",
) -> dict[str, object]:
    return mc.evaluate_indicator(
        events=events,
        denominator=denominator,
        window_complete=complete,
        threshold=threshold,
        incident_owner=owner,
    )


class RegisterTests(unittest.TestCase):
    def test_register_matches_runbook_and_bicep(self) -> None:
        sources = {
            p.relative_to(INFRA).as_posix(): p.read_text(encoding="utf-8")
            for p in INFRA.rglob("*.bicep")
        }
        runbook = (INFRA / "monitoring-runbooks.md").read_text(encoding="utf-8")
        self.assertEqual(mc.coverage_gaps(runbook, sources), [])

    def test_detects_missing_runbook_source_and_owner(self) -> None:
        bad = (
            mc.AlertEntry("x-alert", mc.INSTALLED, "", "jobs", "main.bicep", "nope"),
            mc.AlertEntry("y-gap", mc.GAP, "Owner", "poison", "main.bicep", "m"),
        )
        problems = mc.coverage_gaps("### Other", {"main.bicep": ""}, bad)
        self.assertIn("x-alert: no owner role", problems)
        self.assertIn("x-alert: no runbook heading", problems)
        self.assertIn("x-alert: not found in main.bicep", problems)
        self.assertIn("y-gap: gap must not claim a source", problems)
        self.assertIn("criterion ledger: no register entry", problems)

    def test_poison_and_ai_limits_stay_explicit_gaps(self) -> None:
        gaps = {e.anchor for e in mc.ALERTS if e.status == mc.GAP}
        self.assertTrue(
            {"agent-tasks-poison", "import-jobs-poison", "ai-limits", "rai-harm"} <= gaps
        )


class IndicatorTests(unittest.TestCase):
    def test_missing_threshold_or_approval_is_blocked_not_green(self) -> None:
        self.assertEqual(_evaluate(threshold=None)["status"], mc.BLOCKED)
        self.assertEqual(_evaluate(threshold={"limit": 0.1, "min_sample": 5})["status"], mc.BLOCKED)
        self.assertEqual(_evaluate(threshold={"limit": 2, "min_sample": 5})["status"], mc.BLOCKED)

    def test_blocked_threshold_keeps_constructed_provenance_and_huge_limit_is_blocked(self) -> None:
        result = _evaluate(threshold={"constructed": True, "limit": 0.1})
        self.assertEqual(result["status"], mc.BLOCKED)
        self.assertTrue(result["offline_only"])
        huge = {"constructed": True, "limit": 10**400, "min_sample": 5}
        self.assertEqual(_evaluate(threshold=huge)["status"], mc.BLOCKED)

    def test_insufficient_samples_and_window(self) -> None:
        self.assertEqual(_evaluate(events=0, denominator=0)["status"], mc.INSUFFICIENT)
        self.assertEqual(_evaluate(denominator=5)["status"], mc.INSUFFICIENT)
        self.assertEqual(_evaluate(complete=False)["status"], mc.INSUFFICIENT)

    def test_invalid_counts_blocked(self) -> None:
        for events, denominator in ((-1, 50), (60, 50), (True, 50), ("1", 50), (1, None)):
            with self.subTest(events=events, denominator=denominator):
                self.assertEqual(
                    _evaluate(events=events, denominator=denominator)["status"], mc.BLOCKED
                )

    def test_within_threshold_is_not_safety_proof_and_constructed_is_offline(self) -> None:
        result = _evaluate()
        self.assertEqual(result["status"], mc.WITHIN)
        self.assertTrue(result["offline_only"])
        self.assertNotIn("green", str(result).lower())
        self.assertFalse(_evaluate(threshold=APPROVED)["offline_only"])

    def test_breach_requires_owned_incident(self) -> None:
        result = _evaluate(events=10, threshold=APPROVED)
        self.assertEqual(result["status"], mc.BREACH)
        self.assertTrue(result["incident_required"])
        self.assertEqual(result["incident_owner"], "Safety and Assurance appointee")
        ownerless = _evaluate(events=10, owner="unknown")
        self.assertIsNone(ownerless["incident_owner"])
        self.assertEqual(ownerless["reason"], "breach without owner")


class SanitiserTests(unittest.TestCase):
    def test_only_allowlisted_aggregate_fields_survive(self) -> None:
        event = {
            "alert": "job-ledger",
            "count": 3,
            "prompt": "raw resident text",
            "chat": "hello",
            "reading": 21.5,
            "resident_id": "r-1",
            "status": "breach",
            "task": {"nested": "x"},
        }
        self.assertEqual(
            mc.sanitize_diagnostic(event), {"alert": "job-ledger", "count": 3, "status": "breach"}
        )

    def test_allowlisted_fields_still_drop_identities_tokens_and_long_text(self) -> None:
        event = {
            "task": "a.b@example.org",
            "release": "Bearer abc123",
            "status": "10.1.2.3",
            "owner_role": "x" * 500,
            "alert": "eyJhbGciOiJIUzI1.payload.sig",
            "severity": "2",
        }
        self.assertEqual(mc.sanitize_diagnostic(event), {"severity": "2"})

    def test_values_must_match_field_schemas(self) -> None:
        event = {
            "alert": "some free text",
            "status": "customer said the boiler broke",
            "owner_role": "Jane Smith",
            "release": "two words",
            "window_start": "yesterday",
            "window_end": "2026-11-01T07:00:00Z",
            "count": 10**12,
            "denominator": 5,
            "task": "triage-1",
            "severity": "high",
        }
        self.assertEqual(
            mc.sanitize_diagnostic(event),
            {
                "window_end": "2026-11-01T07:00:00Z",
                "denominator": 5,
                "task": "triage-1",
                "severity": "high",
            },
        )


if __name__ == "__main__":
    unittest.main()
