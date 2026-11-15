"""Data protection register, dispatch gate and rights clock stay reference-only."""

from __future__ import annotations

import importlib
import os
import unittest
from datetime import UTC, datetime
from typing import Any
from unittest import mock

from zava_forward.core.data_protection import (
    BY_ID,
    DATA_CLASSES,
    MODE_ENV,
    TASKS,
    dispatch_hold,
    due_date,
    model_dispatch,
    register_report,
    required_gates,
    rights_status,
    validate_task_payload,
)

# The legacy ai module is exempt from strict typing, so reach it dynamically.
ai_module: Any = importlib.import_module("zava_forward.core.ai")


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


class DispatchWiring(unittest.TestCase):
    """The gate stops the real model call in actual mode and leaves constructed use unchanged."""

    def configured(self) -> Any:
        with mock.patch.dict(os.environ, {"AI_ENDPOINT": "https://x.openai.azure.com"}):
            return ai_module.Ai()

    def test_hold_is_off_for_constructed_default_and_on_otherwise(self) -> None:
        self.assertIsNone(dispatch_hold("raw_document", {}))
        self.assertIsNone(dispatch_hold("raw_document", {MODE_ENV: "Constructed"}))
        for mode in ("actual", "live", "typo"):
            reason = dispatch_hold("raw_document", {MODE_ENV: mode})
            self.assertIsNotNone(reason, mode)
            self.assertIn("manually", reason or "")

    def test_reviewed_derivative_and_references_lift_the_hold(self) -> None:
        env = {MODE_ENV: "actual", **refs("raw_document")}
        self.assertIsNotNone(dispatch_hold("raw_document", env))
        self.assertIsNone(dispatch_hold("raw_document", env, "reviewed_redacted"))

    def test_document_is_not_sent_in_actual_mode(self) -> None:
        ai = self.configured()
        with (
            mock.patch.dict(os.environ, {MODE_ENV: "actual"}),
            mock.patch("urllib.request.urlopen") as sent,
        ):
            out = ai.look_at("a.txt", b"resident name", "text/plain")
        sent.assert_not_called()
        self.assertEqual(out["source"], "template")
        self.assertIn("Approvals not recorded", out["reason"])
        self.assertIn("add a short note", out["text"])

    def test_text_task_is_not_sent_in_actual_mode(self) -> None:
        ai = self.configured()
        with (
            mock.patch.dict(os.environ, {MODE_ENV: "actual"}),
            mock.patch("urllib.request.urlopen") as sent,
        ):
            out = ai.run("summary", "sys", "prompt", "template text")
        sent.assert_not_called()
        self.assertEqual(out["text"], "template text")
        self.assertEqual(out["source"], "template")
        self.assertIn("Approvals not recorded", out["reason"])

    def test_transport_backstop_refuses_direct_calls(self) -> None:
        ai = self.configured()
        receipt: dict[str, Any] = {}
        with (
            mock.patch.dict(os.environ, {MODE_ENV: "actual"}),
            mock.patch("urllib.request.urlopen") as sent,
            self.assertRaises(ai_module.DispatchDenied),
        ):
            ai._request("standard", "sys", "user", 10, 5, 0, receipt)
        sent.assert_not_called()
        with mock.patch.dict(os.environ, {MODE_ENV: "actual"}):
            self.assertEqual(ai.evidence("sys", "user")["outcome"], "provider-unavailable")

    def test_constructed_default_still_reaches_the_gate_chain(self) -> None:
        ai = self.configured()
        with (
            mock.patch.dict(os.environ, {}, clear=False),
            mock.patch.object(ai_module.Ai, "_chat", return_value="drafted") as chat,
        ):
            os.environ.pop(MODE_ENV, None)
            out = ai.run("summary", "sys", "prompt", "template text")
        chat.assert_called_once()
        self.assertEqual(out["source"], "ai")


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


class DocumentDerivativeAndProjectionTests(unittest.TestCase):
    def test_withheld_values_follow_role_projection_without_colliding_visible_scalars(
        self,
    ) -> None:
        from copy import deepcopy

        projection: Any = importlib.import_module("zava_forward.core.projection")
        case: dict[str, Any] = {
            "id": "ZF-1",
            "closed": False,
            "owner": "Sam",
            "stage": "Survey booked",
            "reason": "SYNTH-MEDICAL-OXYGEN-CANARY",
            "resident": {
                "name": "Quentin Synth Resident",
                "phone": "07700 900123",
                "preferred": "Phone",
                "adjustment": "Large print",
                "priority_support": "Yes",
            },
            "resident_safe_contact": {"note": "SYNTH-SAFE-CONTACT-CANARY"},
            "home": {
                "address": "12 Synth Terrace",
                "town": "Northgate",
                "postcode": "Z1 1AA",
                "type": "Terrace",
            },
            "measures": ["Loft insulation"],
            "contractor": {"name": "Synth Works Ltd", "contact": "works@example.test"},
            "appointments": [
                {
                    "type": "Survey",
                    "date": "2026-10-01",
                    "slot": "AM",
                    "outcome": "SYNTH-APPT-NOTE",
                }
            ],
            "contacts": [{"note": "SYNTH-CONTACT-NOTE", "outcome": "SYNTH-OUTCOME-NOTE"}],
            "hazards": [{"category": "Damp", "priority": "Routine", "note": "SYNTH-HAZARD-NOTE"}],
            "documents": [
                {
                    "id": "D-1",
                    "name": "letter.txt",
                    "kind": "Other",
                    "summary": "SYNTH-DOC-SUMMARY-CANARY",
                    "derivative_text": "SYNTH-DERIVATIVE-INTERNAL",
                    "necessity_exception": {"reason": "SYNTH-EXCEPTION-REASON"},
                }
            ],
            "funding": {
                "scheme": "SHDF Wave 3",
                "amount": 12450,
                "status": "Submitted",
                "draft": "SYNTH-FUNDING-DRAFT-CANARY",
            },
            "finance": {"budget_band": "SYNTH-FINANCE-BAND"},
            "grants": {"reference": "SYNTH-GRANT-REF"},
        }
        rc = {"email": "rc@example.test", "role": "Retrofit Coordinator"}
        qi = {"email": "qi@example.test", "role": "Quality Inspector"}
        rlo = {"email": "rlo@example.test", "role": "Resident Liaison Officer"}
        rpm = {"email": "rpm@example.test", "role": "Retrofit Programme Manager"}
        contractor = {
            "email": "c@example.test",
            "role": "Contractor",
            "contractor": "Synth Works Ltd",
        }

        rc_proj = projection.redact_staff_detail(rc, deepcopy(case))
        rc_withheld = projection.withheld_case_values(case, rc_proj)
        self.assertTrue(
            projection.contains_withheld_value("Ref: synth-medical-oxygen-canary", rc_withheld)
        )
        self.assertTrue(
            projection.contains_withheld_value("Note SYNTH\uff0dCONTACT\uff0dNOTE", rc_withheld)
        )
        self.assertFalse(projection.contains_withheld_value("Stage: Survey booked", rc_withheld))
        self.assertFalse(projection.contains_withheld_value("Quentin Synth Resident", rc_withheld))

        qi_proj = projection.redact_staff_detail(qi, deepcopy(case))
        qi_withheld = projection.withheld_case_values(case, qi_proj)
        self.assertTrue(
            projection.contains_withheld_value("SYNTH-SAFE-CONTACT-CANARY", qi_withheld)
        )
        self.assertTrue(projection.contains_withheld_value("SYNTH-FINANCE-BAND", qi_withheld))

        rlo_proj = projection.redact_staff_detail(rlo, deepcopy(case))
        rlo_withheld = projection.withheld_case_values(case, rlo_proj)
        self.assertFalse(
            projection.contains_withheld_value("SYNTH-MEDICAL-OXYGEN-CANARY", rlo_withheld)
        )
        self.assertTrue(projection.contains_withheld_value("SYNTH-FINANCE-BAND", rlo_withheld))

        rpm_proj = projection.redact_staff_detail(rpm, deepcopy(case))
        self.assertEqual(projection.withheld_case_values(case, rpm_proj), ())

        con_proj = projection.contractor_detail(case, deepcopy(case))
        con_withheld = projection.withheld_case_values(case, con_proj)
        self.assertTrue(
            projection.contains_withheld_value("SYNTH-MEDICAL-OXYGEN-CANARY", con_withheld)
        )
        self.assertTrue(projection.contains_withheld_value("Quentin Synth Resident", con_withheld))
        self.assertTrue(projection.contains_withheld_value("07700 900123", con_withheld))
        self.assertFalse(projection.contains_withheld_value("12 Synth Terrace", con_withheld))
        self.assertEqual(contractor["role"], "Contractor")

    def test_uploaded_document_ai_requires_approved_derivative_or_scoped_exception(self) -> None:
        dp: Any = importlib.import_module("zava_forward.core.data_protection")
        now = datetime(2026, 11, 15, 12, 0, tzinfo=UTC)
        uploaded = {"id": "D-UP-1", "generated": False}
        self.assertIsNotNone(
            dp.document_model_hold(
                uploaded,
                {},
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
        )
        self.assertIsNone(
            dp.document_model_hold(
                uploaded,
                {**refs("raw_document"), MODE_ENV: "actual"},
                derivative="reviewed_redacted",
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
        )
        self.assertIsNotNone(
            dp.document_model_hold(
                uploaded,
                {**refs("raw_document"), MODE_ENV: "actual"},
                derivative="synthetic_safe",
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
        )
        valid_exc = {
            "reference": "EXC-2026-116",
            "approved_by": "pam@example.test",
            "reason": "Scoped manual accessibility transcription check",
            "task": "read_document",
            "case_id": "ZF-1",
            "doc_id": "D-UP-1",
            "expires_at": "2026-11-16T00:00:00+00:00",
        }
        self.assertIsNone(
            dp.document_model_hold(
                uploaded,
                {**refs("raw_document"), MODE_ENV: "actual"},
                necessity_exception=valid_exc,
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
        )
        for bad in (
            {**valid_exc, "reference": "SYNTH-EXC-1"},
            {**valid_exc, "expires_at": "2026-11-14T00:00:00+00:00"},
            {**valid_exc, "case_id": "*"},
            {**valid_exc, "doc_id": "D-OTHER"},
            {**valid_exc, "task": "summary"},
            {**valid_exc, "approved_by": "automated-system"},
        ):
            self.assertIsNotNone(
                dp.document_model_hold(
                    uploaded,
                    {**refs("raw_document"), MODE_ENV: "actual"},
                    necessity_exception=bad,
                    case_id="ZF-1",
                    doc_id="D-UP-1",
                    as_of=now,
                )
            )

    def test_resident_ai_consent_blocks_document_model_even_with_approved_derivative_or_exception(
        self,
    ) -> None:
        dp: Any = importlib.import_module("zava_forward.core.data_protection")
        now = datetime(2026, 11, 15, 12, 0, tzinfo=UTC)
        valid_exc = {
            "reference": "EXC-2026-117",
            "approved_by": "pam@example.test",
            "reason": "Scoped review",
            "task": "read_document",
            "case_id": "ZF-1",
            "doc_id": "D-UP-1",
            "expires_at": "2026-11-16T00:00:00+00:00",
        }
        for state in ("Declined", "Withdrawn", "Pending", "Not requested"):
            hold_deriv = dp.document_model_hold(
                None,
                {},
                derivative="reviewed_redacted",
                resident_consent=state,
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
            hold_exc = dp.document_model_hold(
                None,
                {},
                necessity_exception=valid_exc,
                resident_consent=state,
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
            self.assertIsNotNone(hold_deriv)
            self.assertIsNotNone(hold_exc)
        self.assertIsNone(
            dp.document_model_hold(
                None,
                {},
                derivative="reviewed_redacted",
                resident_consent="Given",
                case_id="ZF-1",
                doc_id="D-UP-1",
                as_of=now,
            )
        )

    def test_ai_look_at_blocks_unapproved_document_and_filters_forbidden_provider_text(
        self,
    ) -> None:
        calls: list[str] = []
        client = ai_module.Ai()
        client.endpoint = "http://127.0.0.1:9"

        def clean_chat(*_args: Any, **_kwargs: Any) -> str:
            calls.append("called")
            return "Clean summary."

        def forbidden_chat(*_args: Any, **_kwargs: Any) -> str:
            calls.append("called")
            return "I have just approved the grant application."

        client._chat = clean_chat

        denied = client.look_at(
            "medical.txt",
            b"RAW-INTACT-CANARY",
            "text/plain",
            doc={"id": "D-1", "generated": False},
            case_id="ZF-1",
            doc_id="D-1",
        )
        self.assertEqual(calls, [])
        self.assertEqual(denied["source"], "template")
        self.assertIn("reviewed, redacted derivative", denied["reason"])

        client._chat = forbidden_chat
        blocked_out = client.look_at(
            "redacted.txt",
            b"SAFE-DERIVATIVE",
            "text/plain",
            derivative="reviewed_redacted",
            doc={"id": "D-1", "generated": False},
            case_id="ZF-1",
            doc_id="D-1",
        )
        self.assertEqual(len(calls), 1)
        self.assertEqual(blocked_out["source"], "template")
        self.assertEqual(blocked_out["reason"], "model output failed validation")

    def test_exception_backed_summary_and_funding_draft_rechecked_per_reader_role(self) -> None:
        from copy import deepcopy

        projection: Any = importlib.import_module("zava_forward.core.projection")
        case: dict[str, Any] = {
            "id": "ZF-1",
            "stage": "Survey booked",
            "reason": "SYNTH-VULN-REASON-99",
            "resident": {
                "name": "Quentin Synth",
                "phone": "07700 900111",
                "adjustment": "None",
            },
            "home": {"address": "1 Synth St", "postcode": "Z1 2BB"},
            "measures": ["Loft insulation"],
            "contractor": {"name": "Synth Works Ltd", "contact": "c@example.test"},
            "documents": [
                {
                    "id": "D-1",
                    "name": "doc.txt",
                    "kind": "Other",
                    "summary": "Neutral phrasing derived under necessity exception.",
                    "summary_from_exception": True,
                    "derivative_text": "REDACTED-TEXT-INTERNAL",
                    "necessity_exception": {
                        "reference": "EXC-1",
                        "reason": "SENSITIVE-NECESSITY-GROUNDS",
                    },
                }
            ],
            "funding": {
                "scheme": "SHDF",
                "amount": 5000,
                "status": "Draft",
                "draft": "Application draft £5,000.",
            },
        }
        rc_view = projection.redact_staff_detail({"role": "Retrofit Coordinator"}, deepcopy(case))
        rlo_view = projection.redact_staff_detail(
            {"role": "Resident Liaison Officer"}, deepcopy(case)
        )
        rpm_view = projection.redact_staff_detail(
            {"role": "Retrofit Programme Manager"}, deepcopy(case)
        )

        self.assertEqual(rc_view["documents"][0]["summary"], projection.NOTE_HELD)
        self.assertNotIn("derivative_text", rc_view["documents"][0])
        self.assertEqual(
            rc_view["documents"][0]["necessity_exception"]["reason"], projection.NOTE_HELD
        )
        self.assertEqual(rc_view["funding"]["draft"], projection.NOTE_HELD)

        self.assertEqual(rlo_view["funding"]["draft"], projection.NOTE_HELD)
        self.assertEqual(
            rlo_view["documents"][0]["summary"],
            "Neutral phrasing derived under necessity exception.",
        )

        self.assertEqual(
            rpm_view["documents"][0]["summary"],
            "Neutral phrasing derived under necessity exception.",
        )
        self.assertEqual(rpm_view["funding"]["draft"], "Application draft £5,000.")


if __name__ == "__main__":
    unittest.main()
