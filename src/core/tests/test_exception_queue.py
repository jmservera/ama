"""Exception queue for the data steward and digital operator (FR-012, FR-029, AC-040)."""

import unittest

from zava_forward.core.exception_queue import (
    NO_AUTOMATION,
    OPERATOR,
    STEWARD,
    ExceptionQueue,
)

STAFF = {"Sam Steward": [STEWARD], "Olive Operator": [OPERATOR], "Outsider": []}
VALUES = [
    {"value": "1962", "source": "stock.xlsx", "date": "2026-09-01", "version": "v2"},
    {"value": "1974", "source": "survey.pdf", "date": "2026-09-15", "version": "v1"},
]
ORIGINAL = {"workbook": "stock.xlsx", "row": 7}


def make() -> ExceptionQueue:
    return ExceptionQueue(STAFF, clock=lambda: "2026-11-01T00:00:00+00:00")


class ExceptionQueueTests(unittest.TestCase):
    def test_conflict_shows_both_values_and_owner(self) -> None:
        q = make()
        item = q.raise_conflict("source_conflict", "Sam Steward", "Build year", VALUES, ORIGINAL)
        view = q.conflict_view("Sam Steward", item["id"])
        self.assertEqual(view["values"], VALUES)
        self.assertEqual(view["resolution_owner"], "Sam Steward")
        self.assertEqual(view["eligibility"], "Unknown")

    def test_conflict_needs_two_different_values_and_full_provenance(self) -> None:
        q = make()
        with self.assertRaises(ValueError):
            q.raise_conflict(
                "source_conflict", "Sam Steward", "x", [VALUES[0], VALUES[0]], ORIGINAL
            )
        bad = [VALUES[0], {"value": "1974", "source": "s", "date": "", "version": "v1"}]
        with self.assertRaises(ValueError):
            q.raise_conflict("source_conflict", "Sam Steward", "x", bad, ORIGINAL)

    def test_owner_must_hold_routed_role(self) -> None:
        q = make()
        with self.assertRaises(ValueError):
            q.raise_failure("failed_ai_run", "Sam Steward", "x", ORIGINAL, "timeout")
        with self.assertRaises(ValueError):
            q.raise_failure("failed_import", "Outsider", "x", ORIGINAL, "bad rows")

    def test_failures_land_in_owned_scoped_queue(self) -> None:
        q = make()
        q.raise_failure("failed_import", "Sam Steward", "Import", ORIGINAL, "3 rows to fix")
        q.raise_failure("failed_ai_run", "Olive Operator", "Model call", {"run": "r1"}, "timeout")
        q.raise_failure("stranded_task", "Olive Operator", "Task", {"task": "t9"}, "no owner")
        self.assertEqual([i["kind"] for i in q.queue("Sam Steward")], ["failed_import"])
        self.assertEqual(len(q.queue("Olive Operator")), 2)
        with self.assertRaises(PermissionError):
            q.queue("Outsider")

    def test_out_of_scope_item_denied_and_logged(self) -> None:
        q = make()
        item = q.raise_failure("failed_integration", "Olive Operator", "x", ORIGINAL, "500")
        with self.assertRaises(PermissionError):
            q.request_recovery("Sam Steward", item["id"], "hold", "try")
        self.assertEqual(q.access_report("Olive Operator")["audit"][-1]["action"], "denied")

    def test_recovery_is_audited_and_never_replays_or_releases(self) -> None:
        q = make()
        item = q.raise_failure("failed_ai_run", "Olive Operator", "x", ORIGINAL, "timeout")
        with self.assertRaises(ValueError):
            q.request_recovery("Olive Operator", item["id"], "request_rerun", " ")
        out = q.request_recovery("Olive Operator", item["id"], "request_rerun", "Model back up")
        self.assertEqual(out["status"], "rerun_requested")
        self.assertFalse(out["recovery"]["replayed"])
        self.assertFalse(out["recovery"]["released"])
        self.assertEqual(out["recovery"]["note"], NO_AUTOMATION)
        last = q.access_report("Olive Operator")["audit"][-1]
        self.assertEqual((last["actor"], last["action"]), ("Olive Operator", "request_rerun"))

    def test_only_named_owner_resolves_and_original_is_preserved(self) -> None:
        q = make()
        q2 = ExceptionQueue({**STAFF, "Sue Steward": [STEWARD]})
        item = q.raise_conflict("identity_conflict", "Sam Steward", "Name", VALUES, ORIGINAL)
        other = q2.raise_conflict("identity_conflict", "Sam Steward", "Name", VALUES, ORIGINAL)
        with self.assertRaises(PermissionError):
            q2.request_recovery("Sue Steward", other["id"], "resolve_by_owner", "pick")
        out = q.request_recovery("Sam Steward", item["id"], "resolve_by_owner", "Survey wins")
        self.assertEqual(out["status"], "closed")
        self.assertEqual(out["original_source"], ORIGINAL)
        self.assertEqual(out["values"], VALUES)
        self.assertEqual(out["eligibility"], "Unknown")
        with self.assertRaises(ValueError):
            q.request_recovery("Sam Steward", item["id"], "hold", "again")

    def test_returned_records_are_copies(self) -> None:
        q = make()
        item = q.raise_failure("failed_import", "Sam Steward", "x", ORIGINAL, "e")
        item["original_source"]["row"] = 99
        self.assertEqual(q.queue("Sam Steward")[0]["original_source"], ORIGINAL)

    def test_outage_banner_is_honest(self) -> None:
        q = make()
        self.assertEqual(q.outage_banner()["state"], "unknown")
        self.assertEqual(q.outage_banner("2026-11-01T00:00:00+00:00")["state"], "no_known_outage")
        for bad in ("", "garbage", "2026-11-02T00:00:00+00:00", "2026-10-31T00:00:00+00:00"):
            self.assertEqual(q.outage_banner(bad)["state"], "unknown")
        q.set_outage("Olive Operator", "model-service", "Timeouts since 08:00")
        self.assertEqual(q.outage_banner("2026-11-01T00:00:00+00:00")["state"], "outage")
        with self.assertRaises(PermissionError):
            q.clear_outage("Sam Steward", "model-service", "ok")
        with self.assertRaises(PermissionError):
            q.set_outage("Sam Steward", "x", "y")
        q.clear_outage("Olive Operator", "model-service", "Health check passed")
        audit = q.access_report("Olive Operator")["audit"]
        self.assertEqual([e["action"] for e in audit].count("denied"), 2)
        self.assertIn("Timeouts since 08:00", str(audit))
        self.assertIn("Health check passed", str(audit))
        self.assertEqual(q.outage_banner("2026-11-01T00:00:00+00:00")["state"], "no_known_outage")

    def test_audit_is_scoped_to_actor_role(self) -> None:
        q = make()
        item = q.raise_conflict("source_conflict", "Sam Steward", "x", VALUES, ORIGINAL)
        q.request_recovery("Sam Steward", item["id"], "hold", "secret reason")
        self.assertIn("secret reason", str(q.access_report("Sam Steward")["audit"]))
        self.assertNotIn("secret reason", str(q.access_report("Olive Operator")["audit"]))
        with self.assertRaises(PermissionError):
            q.access_report("Outsider")

    def test_access_is_visible(self) -> None:
        report = make().access_report("Sam Steward")
        self.assertEqual(report["roles"]["Sam Steward"], [STEWARD])
        self.assertEqual(report["scope"]["failed_ai_run"], OPERATOR)

    def test_access_report_is_audited_and_returns_copies(self) -> None:
        q = make()
        q.access_report("Sam Steward")
        report = q.access_report("Sam Steward")
        self.assertEqual(report["audit"][-1]["action"], "viewed_access_report")
        report["audit"].clear()
        self.assertTrue(q.access_report("Sam Steward")["audit"])
        self.assertFalse(hasattr(q, "audit") or hasattr(q, "items") or hasattr(q, "outages"))

    def test_outage_component_is_normalised_on_clear(self) -> None:
        q = make()
        q.set_outage("Olive Operator", " model-service ", "down")
        q.clear_outage("Olive Operator", " model-service ", "ok")
        self.assertEqual(q.outage_banner()["state"], "unknown")
        self.assertEqual(q.outage_banner()["components"], {})


if __name__ == "__main__":
    unittest.main()
