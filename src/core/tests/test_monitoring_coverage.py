"""Monitoring coverage register, indicator and diagnostic-sanitiser checks (issue 146)."""

import unittest
from pathlib import Path
from typing import Any

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

    def test_unknown_status_is_a_problem(self) -> None:
        bad = (mc.AlertEntry("ai-limits", "installled", "Owner", "ai-limits"),)
        problems = mc.coverage_gaps("### ai-limits", {}, bad)
        self.assertTrue(any("unknown status" in p for p in problems))

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
        huge: dict[str, float | bool | str] = {
            "constructed": True,
            "limit": 10**400,
            "min_sample": 5,
        }
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


LIMITS = {"calls": 100, "tokens": 5000, "cost": 2000}
USAGE = {"calls": 10, "tokens": 400, "cost": 50}
AS_OF = "2026-11-04T00:00:00Z"
EXPIRY = "2026-12-01T00:00:00Z"


def _ai(**over: object) -> dict[str, Any]:
    args: dict[str, Any] = {
        "usage": USAGE,
        "limits": LIMITS,
        "expires_at": EXPIRY,
        "as_of": AS_OF,
        "constructed": True,
        "price_source": "constructed-price-list",
        "owner": "Competent task owner",
    }
    args.update(over)
    return mc.evaluate_ai_limits(**args)


class AiLimitTests(unittest.TestCase):
    def test_within_is_offline_and_not_green(self) -> None:
        result = _ai()
        self.assertEqual(result["status"], mc.WITHIN)
        self.assertTrue(result["offline_only"])
        self.assertEqual(result["runbook"], "ai-limits")

    def test_live_limits_need_named_approval(self) -> None:
        self.assertEqual(_ai(constructed=False)["status"], mc.BLOCKED)
        self.assertEqual(_ai(constructed=False, approved_by="unknown")["status"], mc.BLOCKED)
        live = _ai(constructed=False, approved_by="Finance budget owner")
        self.assertEqual(live["status"], mc.WITHIN)
        self.assertFalse(live["offline_only"])

    def test_each_dimension_breach_names_owner_and_runbook(self) -> None:
        for dim, used in (("calls", 101), ("tokens", 5001), ("cost", 2001)):
            result = _ai(usage={**USAGE, dim: used})
            self.assertEqual(result["status"], mc.BREACH, dim)
            self.assertEqual(result["dimensions"][dim], mc.BREACH)
            self.assertTrue(result["incident_required"])
            self.assertEqual(result["owner"], "Competent task owner")
            self.assertEqual(result["runbook"], "ai-limits")
        self.assertEqual(_ai(usage={**USAGE, "calls": 100})["status"], mc.WITHIN)

    def test_expiry_breach_and_ownerless_breach(self) -> None:
        result = _ai(as_of=EXPIRY)
        self.assertEqual(result["dimensions"]["expiry"], mc.BREACH)
        self.assertEqual(result["status"], mc.BREACH)
        ownerless = _ai(as_of=EXPIRY, owner=None)
        self.assertIsNone(ownerless["owner"])
        self.assertEqual(ownerless["reason"], "breach without owner")

    def test_missing_price_or_usage_is_never_zero_or_green(self) -> None:
        no_price = _ai(price_source=None)
        self.assertEqual(no_price["status"], mc.INSUFFICIENT)
        self.assertEqual(no_price["dimensions"]["cost"], mc.UNKNOWN)
        no_usage = _ai(usage={"calls": 1})
        self.assertEqual(no_usage["status"], mc.INSUFFICIENT)
        self.assertEqual(_ai(usage={})["status"], mc.INSUFFICIENT)

    def test_missing_or_invalid_limits_and_time_are_blocked(self) -> None:
        self.assertEqual(_ai(limits=None)["status"], mc.BLOCKED)
        self.assertEqual(_ai(limits={**LIMITS, "tokens": 0})["status"], mc.BLOCKED)
        self.assertEqual(_ai(limits={"calls": 100})["status"], mc.BLOCKED)
        self.assertEqual(_ai(expires_at=None)["status"], mc.BLOCKED)
        self.assertEqual(_ai(as_of="2026-11-04T00:00:00")["status"], mc.BLOCKED)
        self.assertEqual(_ai(usage={**USAGE, "calls": True})["status"], mc.INSUFFICIENT)


class ReconcileTests(unittest.TestCase):
    START, END = "2026-11-04T00:00:00Z", "2026-11-04T01:00:00Z"

    def _run(self, events: list[dict[str, str]]) -> dict[str, Any]:
        return mc.reconcile_events(events, window_start=self.START, window_end=self.END)

    def test_replayed_events_after_restart_count_once(self) -> None:
        event = {"event_id": "e1", "observed_at": "2026-11-04T00:10:00Z"}
        result = self._run([event, dict(event), {"event_id": "e2", "observed_at": self.START}])
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["duplicates"], 1)
        self.assertEqual(result["status"], mc.COUNTED)

    def test_window_is_half_open(self) -> None:
        result = self._run([{"event_id": "e1", "observed_at": self.END}])
        self.assertEqual(result["outside_window"], 1)
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["status"], mc.INSUFFICIENT)

    def test_invalid_events_and_window_are_blocked(self) -> None:
        bad = self._run([{"event_id": "a b", "observed_at": self.START}, {"event_id": "x"}])
        self.assertEqual(bad["invalid"], 2)
        self.assertEqual(bad["status"], mc.BLOCKED)
        swapped = mc.reconcile_events([], window_start=self.END, window_end=self.START)
        self.assertIsNone(swapped["count"])
        self.assertEqual(swapped["status"], mc.BLOCKED)


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

    def test_invalid_timestamps_and_oversized_strings_are_dropped(self) -> None:
        event = {
            "window_start": "2026-02-30T07:00:00Z",
            "window_end": "2026-11-01T99:99:99Z",
            "task": "x" * 4000,
            "release": "r1",
        }
        self.assertEqual(mc.sanitize_diagnostic(event), {"release": "r1"})
        self.assertEqual(
            mc.sanitize_diagnostic({"window_end": "2026-11-01T07:00:00Z"}),
            {"window_end": "2026-11-01T07:00:00Z"},
        )

    def test_evaluated_result_keeps_offline_provenance(self) -> None:
        result = mc.evaluate_indicator(
            events=1,
            denominator=10,
            window_complete=True,
            threshold={"limit": 0.5, "min_sample": 5, "constructed": True},
            incident_owner=None,
        )
        clean = mc.sanitize_diagnostic(result)
        self.assertIs(clean["offline_only"], True)
        self.assertEqual(clean["status"], mc.WITHIN)
        self.assertNotIn("offline_only", mc.sanitize_diagnostic({"offline_only": "yes"}))


if __name__ == "__main__":
    unittest.main()
