"""Data protection register, dispatch gate and rights clock stay reference-only."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime

from zava_forward.core.data_protection import (
    BY_ID,
    DATA_CLASSES,
    TASKS,
    due_date,
    model_dispatch,
    register_report,
    required_gates,
    rights_status,
    validate_task_payload,
)


def refs(class_id: str, value: str = "REF-1") -> dict[str, str]:
    return {f"DP_{class_id.upper()}_{g}_REF": value for g in required_gates(BY_ID[class_id])}


class Register(unittest.TestCase):
    def test_nothing_is_approved_by_default(self) -> None:
        rep = register_report({})
        self.assertFalse(rep["dpo_reviewed"])
        actual = [c for c in rep["classes"] if c["kind"] == "actual"]
        self.assertTrue(actual)
        self.assertFalse(any(c["references_recorded"] for c in actual))
        self.assertTrue(all("Unknown" in c["retention"] for c in actual))

    def test_covers_required_classes_and_special_category_needs_art9(self) -> None:
        ids = {c.id for c in DATA_CLASSES}
        self.assertTrue(
            {
                "staff_identity",
                "review_record",
                "raw_document",
                "prompt_output",
                "audit_ledger",
                "telemetry",
            }
            <= ids
        )
        self.assertIn("ART9", required_gates(BY_ID["raw_document"]))
        self.assertNotIn("ART9", required_gates(BY_ID["staff_identity"]))

    def test_synthetic_refs_do_not_count_and_values_not_echoed(self) -> None:
        rep = register_report(refs("audit_ledger", "SYNTH-1"))
        row = next(c for c in rep["classes"] if c["id"] == "audit_ledger")
        self.assertFalse(row["references_recorded"])
        self.assertTrue(row["synthetic"])
        self.assertNotIn("SYNTH-1", str(rep))


class Dispatch(unittest.TestCase):
    def test_constructed_fixture_allowed_actual_denied(self) -> None:
        self.assertTrue(model_dispatch("fixture_resident", {})["permitted"])
        for cid in ("tenant_identity", "raw_document", "prompt_output"):
            self.assertFalse(model_dispatch(cid, {})["permitted"], cid)
        self.assertIn("manual", model_dispatch("tenant_identity", {})["manual_path"].lower())

    def test_missing_transfer_denies_even_with_other_refs(self) -> None:
        env = refs("prompt_output")
        del env["DP_PROMPT_OUTPUT_TRANSFER_REF"]
        d = model_dispatch("prompt_output", env)
        self.assertFalse(d["permitted"])
        self.assertIn("TRANSFER", d["reason"])

    def test_raw_document_needs_reviewed_derivative(self) -> None:
        env = refs("raw_document")
        self.assertFalse(model_dispatch("raw_document", env)["permitted"])
        self.assertFalse(model_dispatch("raw_document", env, "intact")["permitted"])
        self.assertTrue(model_dispatch("raw_document", env, "reviewed_redacted")["permitted"])

    def test_synthetic_refs_and_non_model_classes_deny(self) -> None:
        self.assertFalse(
            model_dispatch("prompt_output", refs("prompt_output", "SYNTH-9"))["permitted"]
        )
        self.assertFalse(model_dispatch("staff_identity", refs("staff_identity"))["permitted"])
        self.assertFalse(model_dispatch("nope", {})["permitted"])


class TaskPayload(unittest.TestCase):
    def test_declared_fields_only_with_type_and_length(self) -> None:
        out = validate_task_payload(
            "check_explain",
            dict(card_id="C1", as_of="2026-11-03", case_id="x" * 81, health="asthma", name="A"),
        )
        self.assertEqual(out["fields"], dict(card_id="C1", as_of="2026-11-03"))
        self.assertEqual(out["rejected"], ["case_id"])
        self.assertEqual(out["special_category_dropped"], ["health"])
        self.assertNotIn("asthma", str(out))

    def test_unknown_task_denied_with_manual_path(self) -> None:
        out = validate_task_payload("free_chat", dict(card_id="C1"))
        self.assertFalse(out["permitted"])
        self.assertTrue(out["manual_path"])

    def test_every_task_declares_purpose_necessity_prohibited(self) -> None:
        for spec in TASKS.values():
            for key in ("purpose", "audience", "necessity", "prohibited", "fields"):
                self.assertTrue(spec[key])


class RightsClock(unittest.TestCase):
    def test_one_month_with_clamping(self) -> None:
        self.assertEqual(
            due_date(datetime(2026, 1, 31, tzinfo=UTC)), datetime(2026, 2, 28, tzinfo=UTC)
        )
        self.assertEqual(
            due_date(datetime(2026, 12, 15, tzinfo=UTC)), datetime(2027, 1, 15, tzinfo=UTC)
        )
        with self.assertRaises(ValueError):
            due_date(datetime(2026, 1, 1))

    def test_states(self) -> None:
        now = datetime(2026, 11, 20, tzinfo=UTC)
        rows = [
            dict(id="A", kind="access", received_at="2026-11-01T00:00:00+00:00"),
            dict(id="B", kind="erasure", received_at="2026-10-01T00:00:00+00:00"),
            dict(
                id="C",
                kind="access",
                received_at="2026-09-01T00:00:00+00:00",
                answered_at="2026-10-05T00:00:00+00:00",
            ),
            dict(
                id="D",
                kind="access",
                received_at="2026-09-01T00:00:00+00:00",
                answered_at="2026-09-20T00:00:00+00:00",
            ),
        ]
        rep = rights_status(rows, now)
        self.assertEqual(
            {r["id"]: r["state"] for r in rep["requests"]},
            dict(A="open", B="overdue", C="answered_late", D="answered"),
        )
        self.assertEqual(rep["overdue"], ["B"])


if __name__ == "__main__":
    unittest.main()
