"""Data protection register, dispatch gate and rights clock stay reference-only."""

from __future__ import annotations

import importlib
import json
import os
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest import mock

from zava_forward.core.data_protection import (
    BY_ID,
    CONSTRUCTED_DERIVATIVE,
    DATA_CLASSES,
    HOSTING_REGION_VS_INFERENCE_RESIDENCY,
    MANUAL_PATH,
    MODE_ENV,
    SUBJECT_POPULATIONS,
    TASKS,
    WHOLE_SYSTEM_SURFACES,
    RightsRequestLedger,
    answer_rights_request,
    dispatch_attachment_to_model,
    dispatch_hold,
    due_date,
    log_rights_action,
    model_dispatch,
    record_rights_request,
    register_report,
    required_gates,
    rights_status,
    validate_necessity_exception,
    validate_task_payload,
)
from zava_forward.core.data_protection import (
    _valid_redaction_review as valid_redaction_review,
)
from zava_forward.core.data_protection import (
    _valid_scoped_necessity_ref as valid_scoped_necessity_ref,
)

# Legacy modules exempt from strict typing are reached dynamically.
ai_module: Any = importlib.import_module("zava_forward.core.ai")
store_module: Any = importlib.import_module("zava_forward.core.store")
sqlstore_module: Any = importlib.import_module("zava_forward.core.sqlstore")


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


class WholeSystemInventoryAndNecessityTests(unittest.TestCase):
    def test_subject_populations_separate_staff_tenant_review_fixtures_and_future_residents(
        self,
    ) -> None:
        rep = register_report({})
        self.assertEqual(BY_ID["fixture_resident"].kind, "constructed")
        self.assertEqual(
            BY_ID["fixture_resident"].subject_population, "constructed_resident_fixture"
        )
        expected_actual_populations = {
            "staff_identity": "current_staff_identity",
            "tenant_identity": "current_tenant_identity",
            "review_record": "current_review_record",
            "future_real_resident": "future_real_resident",
        }
        for cid, pop in expected_actual_populations.items():
            self.assertEqual(BY_ID[cid].kind, "actual")
            self.assertEqual(BY_ID[cid].subject_population, pop)
            self.assertIn(cid, rep["subject_populations"][pop]["class_ids"])
        self.assertEqual(
            rep["subject_populations"]["constructed_resident_fixture"]["class_ids"],
            ["fixture_resident"],
        )
        for pop_id in SUBJECT_POPULATIONS:
            if pop_id != "constructed_resident_fixture":
                self.assertNotIn(
                    "fixture_resident", rep["subject_populations"][pop_id]["class_ids"]
                )
        self.assertTrue(
            HOSTING_REGION_VS_INFERENCE_RESIDENCY[
                "uk_hosting_does_not_prove_uk_inference_residency"
            ]
        )
        self.assertTrue(
            rep["hosting_region_vs_inference_residency"][
                "uk_hosting_does_not_prove_uk_inference_residency"
            ]
        )
        self.assertTrue(
            rep["hosting_region_vs_inference_residency"][
                "synthetic_resident_does_not_exempt_actual_staff"
            ]
        )
        self.assertFalse(
            rep["hosting_region_vs_inference_residency"]["inference_residency_verified"]
        )

    def test_whole_system_inventory_covers_all_nine_actual_classes_and_surfaces(self) -> None:
        actual_ids = {c.id for c in DATA_CLASSES if c.kind == "actual"}
        self.assertEqual(
            actual_ids,
            {
                "staff_identity",
                "tenant_identity",
                "review_record",
                "future_real_resident",
                "raw_document",
                "prompt_output",
                "audit_ledger",
                "telemetry",
                "provider_retained_copy",
            },
        )
        for cid in actual_ids:
            self.assertTrue(BY_ID[cid].processing_surfaces, cid)
        rep = register_report({})
        coverage = rep["whole_system_coverage"]
        self.assertEqual(set(coverage), set(WHOLE_SYSTEM_SURFACES))
        for surface in WHOLE_SYSTEM_SURFACES:
            self.assertTrue(coverage[surface], surface)
        self.assertEqual(
            required_gates(BY_ID["provider_retained_copy"]),
            ("LAWFUL_BASIS", "RETENTION", "ERASURE", "TRANSFER"),
        )

    def test_whole_system_task_manifests_cover_all_seven_plus_legacy_tasks(self) -> None:
        required_tasks = {
            "rule_lookup",
            "check_explain",
            "alert_triage",
            "agent_chat",
            "look_at_attachment",
            "intake_summary",
            "case_brief",
            "read_document",
        }
        self.assertTrue(required_tasks <= set(TASKS))
        for name, spec in TASKS.items():
            for key in (
                "purpose",
                "audience",
                "necessity",
                "prohibited",
                "permitted_fields",
                "fields",
            ):
                self.assertTrue(spec[key], f"{name}:{key}")
            self.assertEqual(spec["permitted_fields"], spec["fields"], name)
            for fname, rule in spec["permitted_fields"].items():
                field_type, bound = rule
                self.assertIn(field_type, (str, int), f"{name}:{fname}")
                self.assertGreater(bound, 0, f"{name}:{fname}")

    def test_user_permission_never_establishes_task_necessity_or_bypasses_bounds(self) -> None:
        sample_valid: dict[str, dict[str, Any]] = {
            "rule_lookup": {"card_id": "RC-2035", "provision_id": "PAS2035-8.2"},
            "check_explain": {"card_id": "C-1", "as_of": "2026-11-15"},
            "alert_triage": {"alert_id": "ALT-1", "status": "open"},
            "agent_chat": {"case_id": "ZF-1", "role": "Retrofit Coordinator"},
            "look_at_attachment": {"doc_id": "D-1", "derivative": "reviewed_redacted"},
            "intake_summary": {"case_id": "ZF-1", "stage": "Intake", "priority_band": "routine"},
            "case_brief": {"case_id": "ZF-1", "stage": "Survey", "waiting_days": 5},
        }
        for task_name, valid_body in sample_valid.items():
            empty_res = validate_task_payload(task_name, {}, user_permission_granted=True)
            self.assertFalse(empty_res["permitted"], task_name)
            self.assertFalse(empty_res["user_permission_establishes_necessity"], task_name)

            perm_only = validate_task_payload(
                task_name,
                {"user_permission_granted": True, "resident_name": "Jane Doe", "health": "COPD"},
                user_permission_granted=True,
            )
            self.assertFalse(perm_only["permitted"], task_name)
            self.assertIn("health", perm_only["special_category_dropped"])
            self.assertNotIn("COPD", str(perm_only))

            mixed = validate_task_payload(
                task_name,
                {
                    **valid_body,
                    "medical": "oxygen",
                    "undeclared_extra": "drop-me",
                },
                user_permission_granted=True,
            )
            self.assertTrue(mixed["permitted"], task_name)
            self.assertFalse(mixed["user_permission_establishes_necessity"], task_name)
            self.assertNotIn("undeclared_extra", mixed["fields"])
            self.assertIn("medical", mixed["special_category_dropped"])
            self.assertNotIn("oxygen", str(mixed))

        bool_int = validate_task_payload(
            "case_brief", {"waiting_days": True}, user_permission_granted=True
        )
        self.assertFalse(bool_int["permitted"])
        self.assertEqual(bool_int["rejected"], ["waiting_days"])

        unknown_task_constructed = model_dispatch(
            "fixture_resident",
            {},
            task="unapproved_freeform",
            payload={"prompt": "hi"},
            user_permission_granted=True,
        )
        self.assertFalse(unknown_task_constructed["permitted"])
        self.assertFalse(unknown_task_constructed["user_permission_establishes_necessity"])

        bad_payload_actual = model_dispatch(
            "prompt_output",
            refs("prompt_output"),
            task="agent_chat",
            payload={"resident_name": "Disallowed"},
            user_permission_granted=True,
        )
        self.assertFalse(bad_payload_actual["permitted"])
        self.assertFalse(bad_payload_actual["user_permission_establishes_necessity"])


class IntactAttachmentDispatchControlTests(unittest.TestCase):
    def test_storage_permission_never_approves_intact_attachment_dispatch(self) -> None:
        env = refs("raw_document")
        for deriv in (None, "", "intact", "raw", "unreviewed_ocr"):
            decision = dispatch_attachment_to_model(
                env,
                derivative=deriv,
                storage_permission_granted=True,
                user_permission_granted=True,
                case_id="ZF-1",
                doc_id="D-1",
            )
            self.assertFalse(decision["permitted"], str(deriv))
            self.assertFalse(decision["storage_approves_ai_dispatch"])
            self.assertFalse(decision["user_permission_establishes_necessity"])
            self.assertIn("manual", decision["manual_path"].lower())

        no_rescue = dispatch_attachment_to_model(
            env,
            derivative=CONSTRUCTED_DERIVATIVE,
            scoped_necessity_ref="NEC-2026-99",
            storage_permission_granted=True,
            user_permission_granted=True,
        )
        self.assertFalse(no_rescue["permitted"])

    def test_reviewed_redacted_derivative_and_scoped_necessity_ref_boundaries(self) -> None:
        env = refs("raw_document")
        missing_reviewer = dispatch_attachment_to_model(
            env,
            derivative="reviewed_redacted",
            storage_permission_granted=True,
        )
        self.assertFalse(missing_reviewer["permitted"])

        bad_reviewer_not_rescued = dispatch_attachment_to_model(
            env,
            derivative="reviewed_redacted",
            redaction_reviewer_id="synth-reviewer-1",
            redaction_review_id="RED-1",
            scoped_necessity_ref="NEC-2026-10",
            storage_permission_granted=True,
        )
        self.assertFalse(bad_reviewer_not_rescued["permitted"])

        approved_derivative = dispatch_attachment_to_model(
            env,
            derivative="reviewed_redacted",
            redaction_reviewer_id="rlo@zava.example",
            redaction_review_id="RED-2026-10",
            payload={"doc_id": "D-1", "derivative": "reviewed_redacted"},
        )
        self.assertTrue(approved_derivative["permitted"])
        self.assertEqual(approved_derivative["approval_basis"], "reviewed_redacted")
        self.assertFalse(approved_derivative["storage_approves_ai_dispatch"])

        approved_scoped = dispatch_attachment_to_model(
            env,
            derivative="intact",
            scoped_necessity_ref="NEC-2026-22",
            storage_permission_granted=True,
        )
        self.assertTrue(approved_scoped["permitted"])
        self.assertEqual(approved_scoped["approval_basis"], "scoped_necessity_ref")

        for synth_ref in ("SYNTH-NEC-1", "synth-nec-lower"):
            denied_synth = dispatch_attachment_to_model(
                env,
                derivative="intact",
                scoped_necessity_ref=synth_ref,
                storage_permission_granted=True,
            )
            self.assertFalse(denied_synth["permitted"], synth_ref)

        bad_exc_not_rescued = dispatch_attachment_to_model(
            env,
            derivative="intact",
            necessity_exception={"reference": "SYNTH-1"},
            scoped_necessity_ref="NEC-2026-22",
            case_id="ZF-1",
            doc_id="D-1",
        )
        self.assertFalse(bad_exc_not_rescued["permitted"])

        active_env = {MODE_ENV: "actual", **env}
        self.assertIsNotNone(
            dispatch_hold(
                "raw_document",
                active_env,
                storage_permission_granted=True,
                user_permission_granted=True,
            )
        )
        self.assertIsNone(
            dispatch_hold(
                "raw_document",
                active_env,
                scoped_necessity_ref="NEC-2026-22",
            )
        )


class RightsRequestLedgerPersistenceTests(unittest.TestCase):
    def test_rights_ledger_persists_in_store_and_json_file_roundtrip(self) -> None:
        received = datetime(2026, 1, 31, 9, 30, tzinfo=UTC)
        as_of_open = datetime(2026, 2, 15, 12, 0, tzinfo=UTC)
        answered_on_time = datetime(2026, 2, 27, 16, 0, tzinfo=UTC)

        with tempfile.TemporaryDirectory() as tmp:
            seed_path = Path(tmp) / "seed.json"
            seed_path.write_text(
                json.dumps({"cases": [], "staff": [], "recommendations": [], "audit": []}),
                encoding="utf-8",
            )
            live_path = Path(tmp) / "live.json"
            json_ledger_path = Path(tmp) / "rights-ledger.json"
            store: Any = store_module.Store(str(seed_path), live_path=str(live_path))

            rec = record_rights_request(
                store,
                request_id="DSR-2026-001",
                kind="access",
                subject_population="current_staff_identity",
                subject_key="SUBJ-SECRET-STAFF-99",
                received_at=received,
                actor="dpo@zava.example",
                notes_ref="SAR-INTAKE-REF-001",
            )
            self.assertEqual(rec["id"], "DSR-2026-001")
            self.assertEqual(rec["request_id"], "DSR-2026-001")
            self.assertEqual(rec["due_at"], "2026-02-28T09:30:00+00:00")

            log_rights_action(
                store,
                "DSR-2026-001",
                action="locate",
                actor="dpo@zava.example",
                at=as_of_open,
                target_scope="staff_identity_and_reviews",
                record_count=3,
            )
            log_rights_action(
                store,
                "DSR-2026-001",
                action="export",
                actor="dpo@zava.example",
                at=as_of_open,
                target_scope="staff_identity_and_reviews",
                record_count=2,
            )
            open_status = rights_status(store, as_of_open)
            self.assertTrue(open_status["persisted"])
            self.assertEqual(open_status["requests"][0]["state"], "open")

            answer_rights_request(
                store,
                "DSR-2026-001",
                actor="dpo@zava.example",
                answered_at=answered_on_time,
                summary_ref="SAR-BUNDLE-001",
            )
            self.assertNotIn("SUBJ-SECRET-STAFF-99", json.dumps(store.data.get("audit", [])))

            reloaded_store: Any = store_module.Store(str(seed_path), live_path=str(live_path))
            reloaded_status = rights_status(reloaded_store, answered_on_time)
            self.assertEqual(reloaded_status["requests"][0]["state"], "answered")
            self.assertEqual(reloaded_status["requests"][0]["action_kinds"], ["locate", "export"])

            json_payload = RightsRequestLedger(reloaded_store).to_json()
            json_ledger_path.write_text(json_payload, encoding="utf-8")
            roundtrip_mem = RightsRequestLedger.from_json(json_payload)
            self.assertEqual(roundtrip_mem.get("DSR-2026-001")["summary_ref"], "SAR-BUNDLE-001")

            file_ledger = RightsRequestLedger(path=json_ledger_path)
            file_status = rights_status(file_ledger, answered_on_time)
            self.assertTrue(file_status["persisted"])
            self.assertEqual(file_status["requests"][0]["id"], "DSR-2026-001")
            self.assertEqual(file_status["requests"][0]["state"], "answered")

    def test_rights_ledger_persists_across_sqlite_sqlstore_reopen(self) -> None:
        received = datetime(2026, 10, 1, 10, 0, tzinfo=UTC)
        erased_at = datetime(2026, 10, 12, 11, 0, tzinfo=UTC)
        late_answer = datetime(2026, 11, 5, 15, 0, tzinfo=UTC)

        with tempfile.TemporaryDirectory() as tmp:
            seed_path = Path(tmp) / "seed.json"
            seed_path.write_text(
                json.dumps({"cases": [], "staff": [], "recommendations": [], "audit": []}),
                encoding="utf-8",
            )
            db_path = Path(tmp) / "zava.sqlite3"
            sql_store: Any = sqlstore_module.SqlStore(str(seed_path), str(db_path))
            try:
                record_rights_request(
                    sql_store,
                    request_id="DSR-SQL-01",
                    kind="erasure",
                    subject_population="current_tenant_identity",
                    subject_key="SUBJ-SECRET-TENANT-42",
                    received_at=received,
                    actor="dpo@zava.example",
                )
                log_rights_action(
                    sql_store,
                    "DSR-SQL-01",
                    action="erase",
                    actor="dpo@zava.example",
                    at=erased_at,
                    target_scope="tenant_session_and_prompt_cache",
                    record_count=4,
                    local_deleted=True,
                    audit_retained_reason="Article 17(3)(b) statutory audit integrity",
                )
                answer_rights_request(
                    sql_store,
                    "DSR-SQL-01",
                    actor="dpo@zava.example",
                    answered_at=late_answer,
                    summary_ref="ERASE-RESP-01",
                    local_deleted=True,
                )
            finally:
                sql_store.db.close()

            reopened: Any = sqlstore_module.SqlStore(str(seed_path), str(db_path))
            try:
                rep = rights_status(reopened, late_answer)
                self.assertTrue(rep["persisted"])
                self.assertEqual(len(rep["requests"]), 1)
                row = rep["requests"][0]
                self.assertEqual(row["id"], "DSR-SQL-01")
                self.assertEqual(row["state"], "answered_late")
                self.assertTrue(row["local_deleted"])
                self.assertFalse(row["provider_erasure_confirmed"])
                self.assertEqual(rep["local_deleted_not_provider_erased"], ["DSR-SQL-01"])
                self.assertNotIn(
                    "SUBJ-SECRET-TENANT-42", json.dumps(reopened.data.get("audit", []))
                )
            finally:
                reopened.db.close()

    def test_rights_ledger_never_represents_local_deletion_as_provider_erasure(self) -> None:
        ledger = RightsRequestLedger()
        received = datetime(2026, 11, 1, 8, 0, tzinfo=UTC)
        now = datetime(2026, 11, 10, 8, 0, tzinfo=UTC)

        rec = ledger.record_request(
            request_id="DSR-ERASE-1",
            kind="erasure",
            subject_population="current_staff_identity",
            subject_key="staff-ref-1",
            received_at=received,
            actor="dpo@zava.example",
        )
        self.assertFalse(rec["local_deleted"])
        self.assertFalse(rec["provider_erasure_confirmed"])

        after_erase = ledger.log_action(
            "DSR-ERASE-1",
            action="erase",
            actor="dpo@zava.example",
            at=now,
            target_scope="local_prompt_output",
            record_count=1,
            local_deleted=True,
        )
        self.assertTrue(after_erase["local_deleted"])
        self.assertFalse(after_erase["provider_erasure_confirmed"])
        self.assertEqual(
            after_erase["provider_erasure_status"],
            "local_deleted_only_provider_erasure_unconfirmed",
        )

        answered = ledger.answer_request(
            "DSR-ERASE-1",
            actor="dpo@zava.example",
            answered_at=now,
            summary_ref="ERASE-LOCAL-ONLY-1",
            local_deleted=True,
        )
        self.assertTrue(answered["local_deleted"])
        self.assertFalse(answered["provider_erasure_confirmed"])

        rep = rights_status(ledger, now)
        self.assertEqual(rep["local_deleted_not_provider_erased"], ["DSR-ERASE-1"])
        self.assertFalse(rep["requests"][0]["provider_erasure_confirmed"])

        with self.assertRaises(ValueError):
            ledger.log_action(
                "DSR-ERASE-1",
                action="erase",
                actor="dpo@zava.example",
                at=now,
                provider_erasure_confirmed=True,
            )
        with self.assertRaises(ValueError):
            rights_status(
                [
                    {
                        "id": "BAD-1",
                        "kind": "erasure",
                        "received_at": "2026-11-01T00:00:00+00:00",
                        "provider_erasure_confirmed": True,
                    }
                ],
                now,
            )
        with self.assertRaises(ValueError):
            RightsRequestLedger.from_json(
                json.dumps(
                    {
                        "schema": "zava.rights_requests.v1",
                        "requests": [
                            {
                                "id": "BAD-2",
                                "request_id": "BAD-2",
                                "kind": "erasure",
                                "subject_population": "current_staff_identity",
                                "subject_key": "k",
                                "received_at": "2026-11-01T00:00:00+00:00",
                                "due_at": "2026-12-01T00:00:00+00:00",
                                "recorded_by": "dpo@zava.example",
                                "provider_erasure_confirmed": True,
                            }
                        ],
                    }
                )
            )
        with self.assertRaises(ValueError):
            ledger.record_request(
                request_id="SYNTH-DSR-1",
                kind="access",
                subject_population="current_staff_identity",
                subject_key="k",
                received_at=received,
                actor="dpo@zava.example",
            )


class RejectionBoundaries(unittest.TestCase):
    """Failure paths that keep intact or unreviewed material away from a model (#121)."""

    def test_redaction_review_needs_named_human_and_recorded_review(self) -> None:
        bad: list[tuple[Any, Any]] = [
            (None, "REV-1"),
            ("  ", "REV-1"),
            ("x" * 121, "REV-1"),
            ("SYNTH-reviewer", "REV-1"),
            ("ai", "REV-1"),
            ("review-bot", "REV-1"),
            ("jo.reviewer", None),
            ("jo.reviewer", " "),
            ("jo.reviewer", "x" * 121),
            ("jo.reviewer", "SYNTH-1"),
        ]
        for reviewer, review_id in bad:
            with self.subTest(reviewer=reviewer, review_id=review_id):
                ok, _reason = valid_redaction_review(reviewer, review_id)
                self.assertFalse(ok)
        ok, reason = valid_redaction_review(" jo.reviewer ", " REV-1 ")
        self.assertTrue(ok)
        self.assertIn("not verified", reason)

    def test_scoped_necessity_ref_rejects_wildcards_long_and_other_tasks(self) -> None:
        for ref in (None, "", "   ", "x" * 121, "*", "ALL", "any", "SYNTH-1", "demo"):
            with self.subTest(ref=ref):
                self.assertFalse(valid_scoped_necessity_ref(ref, "read_document")[0])
        self.assertFalse(valid_scoped_necessity_ref("NEC-1", "case_brief")[0])
        self.assertTrue(valid_scoped_necessity_ref("NEC-1", "look_at_attachment")[0])
        self.assertTrue(valid_scoped_necessity_ref("NEC-1", "read_document")[0])

    def test_necessity_exception_rejects_each_malformed_shape(self) -> None:
        good: dict[str, Any] = {
            "reference": "NEC-1",
            "approved_by": "jo.dpo",
            "reason": "Reviewer needs the redacted excerpt",
            "task": "read_document",
        }

        def check(**changes: Any) -> dict[str, Any]:
            doc = {**good, **changes}
            doc = {k: v for k, v in doc.items() if v is not None}
            return validate_necessity_exception(doc, task="read_document", as_of="2026-11-28")

        self.assertTrue(check()["permitted"])
        self.assertFalse(validate_necessity_exception("NEC-1")["permitted"])
        self.assertFalse(validate_necessity_exception(None)["permitted"])
        for changes in (
            {"reference": None},
            {"reference": "x" * 121},
            {"approved_by": None},
            {"approved_by": "model"},
            {"reason": None},
            {"reason": "r" * 301},
            {"task": None},
            {"task": "*"},
            {"task": "case_brief"},
            {"case_id": 5},
            {"doc_id": ""},
            {"expires_at": "tomorrow"},
            {"expires_at": "2026-13-45"},
            {"expires_at": "2026-11-27"},
        ):
            with self.subTest(changes=changes):
                result = check(**changes)
                self.assertFalse(result["permitted"])
                self.assertIsNone(result["exception"])

    def test_necessity_exception_binds_case_document_and_actual_references(self) -> None:
        doc = {
            "id": "NEC-2",
            "approved_by": "jo.dpo",
            "reason": "Needed",
            "scope": "look_at_attachment",
            "case_id": "C-1",
            "doc_id": "D-1",
        }
        kwargs: dict[str, Any] = {"task": "look_at_attachment", "case_id": "C-1", "doc_id": "D-1"}
        self.assertTrue(validate_necessity_exception(doc, **kwargs)["permitted"])
        self.assertFalse(
            validate_necessity_exception(doc, **{**kwargs, "case_id": "C-2"})["permitted"]
        )
        self.assertFalse(
            validate_necessity_exception(doc, **{**kwargs, "doc_id": "D-2"})["permitted"]
        )
        self.assertFalse(
            validate_necessity_exception({**doc, "id": "SYNTH-9"}, actual=True, **kwargs)[
                "permitted"
            ]
        )
        self.assertTrue(
            validate_necessity_exception(
                {**doc, "expires_at": "2026-11-28T00:00:00"}, as_of=datetime(2026, 11, 28), **kwargs
            )["permitted"]
        )

    def test_task_payload_rejects_wrong_types_oversize_and_special_fields(self) -> None:
        result = validate_task_payload(
            "case_brief",
            {"case_id": "C-1", "waiting_days": True, "open_actions": 501, "stage": "x" * 81},
        )
        self.assertEqual(result["fields"], {"case_id": "C-1"})
        self.assertEqual(result["rejected"], ["open_actions", "stage", "waiting_days"])
        empty = validate_task_payload(
            "case_brief", {"waiting_days": -1}, user_permission_granted=True
        )
        self.assertFalse(empty["permitted"])
        self.assertTrue(empty["user_permission_granted"])
        self.assertFalse(empty["user_permission_establishes_necessity"])
        self.assertEqual(empty["manual_path"], MANUAL_PATH)

    def test_due_date_needs_timezone_and_rolls_over_december(self) -> None:
        with self.assertRaises(ValueError):
            due_date(datetime(2026, 11, 1))
        self.assertEqual(
            due_date(datetime(2026, 12, 31, tzinfo=UTC)), datetime(2027, 1, 31, tzinfo=UTC)
        )

    def test_rights_ledger_rejects_malformed_rows_on_load(self) -> None:
        base: dict[str, Any] = {
            "request_id": "R-1",
            "kind": "access",
            "received_at": "2026-11-01T00:00:00+00:00",
        }

        def load(**changes: Any) -> None:
            row = {**base, **changes}
            RightsRequestLedger.from_json(json.dumps({"requests": [row]}))

        load()
        for changes in (
            {"request_id": " "},
            {"kind": "sell"},
            {"received_at": "2026-11-01T00:00:00"},
            {"answered_at": "2026-10-01T00:00:00+00:00"},
            {"actions": [["erase"]]},
            {"actions": [{"action": "shred", "at": "2026-11-02T00:00:00+00:00"}]},
            {
                "actions": [
                    {
                        "action": "erase",
                        "at": "2026-11-02T00:00:00+00:00",
                        "provider_erasure_confirmed": True,
                    }
                ]
            },
            {"actions": [{"action": "erase", "at": "2026-11-02T00:00:00"}]},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                load(**changes)

    def test_rights_status_accepts_raw_rows_and_rejects_bad_mapping(self) -> None:
        now = datetime(2026, 11, 28, tzinfo=UTC)
        row = {
            "request_id": "R-1",
            "kind": "access",
            "received_at": "2026-10-01T00:00:00+00:00",
        }
        for source in ([row], {"requests": [row]}, {"rights_requests": [row]}):
            with self.subTest(source=type(source).__name__):
                report = rights_status(source, now)
                self.assertEqual(report["overdue"], ["R-1"])
                self.assertFalse(report["provider_erasure_confirmed"])
        with self.assertRaises(ValueError):
            rights_status({"requests": "R-1"}, now)
        with self.assertRaises(ValueError):
            rights_status([row], datetime(2026, 11, 28))


if __name__ == "__main__":
    unittest.main()
