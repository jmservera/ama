"""Regression checks and executable enforcement tests for resident and representative UX (#154).

Preserves the design-document regression checks (`J1`-`J6`, `R1`) and verifies positive-allowlist
task-limited representative view projection and request/session-time authority expiry (`FR-045`,
`FR-046`, `NFR-008`, `NFR-009`).
"""

import copy
import json
import re
import tempfile
import unittest
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core import controls
from zava_forward.core import resident_decisions as rd
from zava_forward.core import resident_journey_design as rjd
from zava_forward.core import resident_showcase as rs
from zava_forward.core.resident_documents import DocumentFacts, DocumentRequest
from zava_forward.core.store import Store

DOC = (
    Path(__file__).resolve().parents[3]
    / "docs/reference/research/ux/customer-journeys/residents.md"
)
JOURNEYS = {
    "J1": "Choose each proposed measure",
    "J2": "Pause, withdraw or ask for more time",
    "J3": "Compare appointment offers and confirmations",
    "J4": "Know who will update you and when",
    "J5": "Handover, practise controls and get aftercare",
    "J6": "Challenge, complain and follow a remedy",
    "R1": "Task-limited representative briefing and actions",
}


def section(code: str) -> str:
    text = DOC.read_text(encoding="utf-8")
    heading = f"### {code}: {JOURNEYS[code]}"
    start = text.index(heading)
    match = re.search(r"^#{2,3} ", text[start + len(heading) :], re.MULTILINE)
    end = start + len(heading) + match.start() if match else len(text)
    return " ".join(text[start:end].split())


class ResidentJourneyDesign(unittest.TestCase):
    def test_every_required_topic_has_a_journey(self) -> None:
        for code in JOURNEYS:
            self.assertTrue(section(code), code)

    def test_update_commitments_handover_and_aftercare_content_is_kept(self) -> None:
        j4, j5 = section("J4"), section("J5")
        for phrase in (
            "Named owner, due date/time and basis",
            "reassignment retains the prior promise/history",
        ):
            self.assertIn(phrase, j4)
        for phrase in (
            "Current approved instructions, guarantees and contact route",
            "Replacing accepted evidence reopens dependent acceptance/handover",
            "phone/visit aftercare request",
        ):
            self.assertIn(phrase, j5)

    def test_each_journey_has_a_non_digital_equivalent(self) -> None:
        phrases = {
            "J1": "No decision or silence becomes refusal or consent",
            "J2": "Lost confirmation remains",
            "J3": "Do not invent appointment slots or response deadlines",
            "J4": "Do not make a promised service time up",
            "J5": "Asking for help or declining practice never establishes or removes consent",
            "J6": "owner must confirm them before use",
            "R1": "A family relationship or possession of a letter is not authority",
        }
        for code in JOURNEYS:
            text = section(code)
            self.assertIn("Non-digital equivalent:", text, code)
            self.assertIn(phrases[code], text.split("Non-digital equivalent:", 1)[1], code)

    def test_shared_frame_forbids_incapacity_inference_and_covers_needs(self) -> None:
        text = " ".join(DOC.read_text(encoding="utf-8").split())
        for phrase in (
            "Do not infer incapacity",
            "language, format, channel, contact times and adjustments",
            "Easy Read",
            "interpreting",
            "without a portal or smartphone",
        ):
            self.assertIn(phrase, text)

    def test_offers_are_distinct_from_confirmed_commitments(self) -> None:
        j3 = section("J3")
        for status in ("Offered - not booked", "Waiting for confirmation", "Visit confirmed"):
            self.assertIn(status, j3)
        self.assertIn("only after current resident/authorised representative", j3)
        self.assertIn("Changed offer/capacity returns to waiting", j3)

    def test_choice_is_per_measure_and_withdrawal_is_scoped(self) -> None:
        self.assertIn("no bundle-wide acceptance", section("J1"))
        self.assertIn("Your other choices have not changed", section("J2"))

    def test_remedy_status_stays_separate_from_response(self) -> None:
        j6 = section("J6")
        self.assertIn("A completed response is not a completed remedy", j6)
        self.assertIn("open remedy stays visible", j6)

    def test_representative_authority_is_task_limited_and_expires(self) -> None:
        r1 = section("R1")
        for phrase in (
            "never agree to works",
            "never receive the union of each other's permissions",
            "unavailable from that date",
            "Check authority again at each access/action",
            "Missing, unclear, disputed, expired or revoked authority",
            "No case details in denied response",
        ):
            self.assertIn(phrase, r1)

    def test_no_live_contact_and_validation_pending(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        flat = " ".join(text.split())
        self.assertIn("Do not paste it into live letters", flat)
        self.assertIn("neither builds it nor sends messages", flat)
        scripts = text[text.index("### Validation handoff and issue acceptance") :]
        row = r"^\| (?:J\d|R1|All tasks)[^|]*\|[^|]*\| ([^|]*?) \|$"
        rows = re.findall(row, scripts, re.MULTILINE)
        self.assertEqual(len(rows), 7)
        for result in rows:
            self.assertTrue(result.strip())


HOUSEHOLD_NOTE_CANARY = "SENSITIVE-HOUSEHOLD-SAFEGUARDING-CANARY"
SIBLING_DECISION_CANARY = "SIBLING-CAVITY-DECISION-CANARY"
UNRELATED_COMPLAINT_CANARY = "UNRELATED-COMPLAINT-SUMMARY-CANARY"
OTHER_REP_CANARY = "OTHER-REP-REQUEST-CANARY"
HANDOVER_CANARY = "HANDOVER-PACK-INTERNAL-CANARY"
ADDRESS_CANARY = "99 Secret Canary Crescent"
PHONE_CANARY = "07700900999"
SAFE_CONTACT_CANARY = "SAFE-CONTACT-ROUTE-CANARY"


def _synthetic_case(
    *,
    expires_at: Any = "2026-11-15T14:00:00Z",
    tasks: list[str] | None = None,
) -> dict[str, Any]:
    chosen_tasks = tasks if tasks is not None else ["Receive information"]
    authority: dict[str, Any] = {
        "version": 1,
        "representative_ref": "REP-1",
        "status": "Confirmed",
        "tasks": list(chosen_tasks),
        "case_id": "ZF-REP-1",
        "measure": "Loft insulation",
        "scope": "Main roof 270mm mineral wool",
        "design_version": 2,
        "context_revision": 1,
        "authority_date": "2026-11-01",
        "review_date": "2026-11-20",
        "safe_contact_ref": SAFE_CONTACT_CANARY,
        "safe_contact_revision": 1,
        "source": "Signed consent note REF-AUTH-1",
        "resident_wishes": "Share loft timing updates only.",
    }
    if expires_at is not Ellipsis:
        authority["expires_at"] = expires_at
    return {
        "id": "ZF-REP-1",
        "stage": "Survey being booked",
        "owner": "Uma Officer",
        "owner_code": "HO-1",
        "first_resident_contact_at": "2026-11-01T09:00",
        "resident": {
            "name": "Pat Example",
            "phone": PHONE_CANARY,
            "email": "pat.resident@example.test",
            "vulnerability_note": HOUSEHOLD_NOTE_CANARY,
        },
        "home": {
            "address": ADDRESS_CANARY,
            "town": "Northborough",
            "postcode": "NB1 9ZZ",
            "tenure": "Tenant",
        },
        "measures": ["Loft insulation", "Cavity wall"],
        "technical": {"design_version": 2},
        "resident_safe_contact": SAFE_CONTACT_CANARY,
        "resident_contact_history": [
            {
                "reference": SAFE_CONTACT_CANARY,
                "source": "In-person check",
                "at": "2026-11-01T09:00",
            }
        ],
        "resident_scopes": {
            "Loft insulation": [
                {
                    "revision": 1,
                    "case_id": "ZF-REP-1",
                    "measure": "Loft insulation",
                    "scope": "Main roof 270mm mineral wool",
                    "design_version": 2,
                    "source": "Survey pack v2",
                }
            ],
            "Cavity wall": [
                {
                    "revision": 1,
                    "case_id": "ZF-REP-1",
                    "measure": "Cavity wall",
                    "scope": "External elevations bead fill",
                    "design_version": 2,
                    "source": "Survey pack v2",
                }
            ],
        },
        "measure_decisions": {
            "Loft insulation": [
                {
                    "version": 1,
                    "measure": "Loft insulation",
                    "context_revision": 1,
                    "status": "Waiting",
                    "answered_by": "The resident",
                    "note": HOUSEHOLD_NOTE_CANARY,
                    "recorded_by_email": "rlo@example.test",
                    "at": "2026-11-02T10:00",
                }
            ],
            "Cavity wall": [
                {
                    "version": 1,
                    "measure": "Cavity wall",
                    "context_revision": 1,
                    "status": "Paused",
                    "answered_by": "The resident",
                    "note": SIBLING_DECISION_CANARY,
                    "recorded_by_email": "rlo@example.test",
                    "at": "2026-11-02T11:00",
                }
            ],
        },
        "representative_authorities": {"REP-1": [authority]},
        "service_requests": [
            {
                "id": "SR-RES-ONLY",
                "route": "Complaint",
                "summary": UNRELATED_COMPLAINT_CANARY,
                "desired_outcome": HOUSEHOLD_NOTE_CANARY,
                "representative_ref": "Unknown",
                "status": "Open",
                "next_update": "2026-11-18",
            },
            {
                "id": "SR-OTHER-REP",
                "route": "Service request",
                "summary": OTHER_REP_CANARY,
                "desired_outcome": OTHER_REP_CANARY,
                "representative_ref": "REP-2",
                "status": "Open",
                "next_update": "2026-11-19",
            },
            {
                "id": "SR-REP-1",
                "route": "Service request",
                "summary": HOUSEHOLD_NOTE_CANARY,
                "desired_outcome": HOUSEHOLD_NOTE_CANARY,
                "representative_ref": "REP-1",
                "status": "In progress",
                "next_update": "2026-11-17",
            },
        ],
        "resident_update": {
            "status": "Outstanding",
            "due_at": "2026-11-17T16:00:00Z",
            "purpose": HOUSEHOLD_NOTE_CANARY,
            "safe_contact_ref": SAFE_CONTACT_CANARY,
        },
        "handover": {"pack_note": HANDOVER_CANARY},
        "contacts": [{"note": HOUSEHOLD_NOTE_CANARY}],
        "hazards": [{"category": "Damp", "note": HOUSEHOLD_NOTE_CANARY}],
    }


def _assert_no_canaries(test: unittest.TestCase, payload: dict[str, Any]) -> None:
    serialized = json.dumps(payload)
    for canary in (
        HOUSEHOLD_NOTE_CANARY,
        SIBLING_DECISION_CANARY,
        UNRELATED_COMPLAINT_CANARY,
        OTHER_REP_CANARY,
        HANDOVER_CANARY,
        ADDRESS_CANARY,
        PHONE_CANARY,
        SAFE_CONTACT_CANARY,
        "pat.resident@example.test",
        "Pat Example",
        "Cavity wall",
    ):
        test.assertNotIn(canary, serialized)


class RepresentativeTaskProjectionTests(unittest.TestCase):
    ACTIVE_NOW = datetime(2026, 11, 10, 12, 0, 0, tzinfo=UTC)

    def test_receive_information_projects_only_scoped_briefing_and_omits_canaries(self) -> None:
        case = _synthetic_case(tasks=["Receive information"])
        view = rjd.project_representative_view(case, "REP-1", now=self.ACTIVE_NOW)
        self.assertTrue(view["active"])
        self.assertEqual(view["state"], "active")
        self.assertEqual(view["expires_at"], "2026-11-15T14:00:00Z")
        self.assertEqual(view["journey_stages"], ["R1", "J4"])
        self.assertEqual(view["permitted_actions"], ["view_task_briefing"])
        self.assertEqual(len(view["measures"]), 1)
        measure = view["measures"][0]
        self.assertEqual(measure["measure"], "Loft insulation")
        self.assertIn("progress", measure)
        self.assertIn("next_step", measure)
        self.assertNotIn("decision", measure)
        self.assertNotIn("appointments", view)
        self.assertNotIn("communications", view)
        self.assertNotIn("home", view)
        _assert_no_canaries(self, view)

    def test_communicate_projects_only_rep_linked_requests_and_rejects_unknown_ref(self) -> None:
        case = _synthetic_case(tasks=["Communicate"])
        view = rjd.project_representative_view(case, "REP-1", now=self.ACTIVE_NOW)
        self.assertTrue(view["active"])
        self.assertEqual(view["journey_stages"], ["R1", "J4", "J6"])
        self.assertEqual(
            view["permitted_actions"],
            ["view_task_briefing", "send_scoped_message", "request_scoped_callback"],
        )
        reqs = view["communications"]["service_requests"]
        self.assertEqual([r["id"] for r in reqs], ["SR-REP-1"])
        self.assertEqual(set(reqs[0]), {"id", "route", "status", "next_update"})
        self.assertEqual(
            view["communications"]["update_commitment"],
            {"status": "Outstanding", "due_at": "2026-11-17T16:00:00Z"},
        )
        _assert_no_canaries(self, view)

        unknown_view = rjd.project_representative_view(case, "Unknown", now=self.ACTIVE_NOW)
        self.assertFalse(unknown_view["active"])
        self.assertEqual(unknown_view["state"], "held")
        self.assertEqual(unknown_view["reason"], "missing_authority")

    def test_attend_separates_offered_and_confirmed_visits_and_strips_home_binding(self) -> None:
        case = _synthetic_case(tasks=["Attend"])
        loft_binding = {
            "home": {"address": ADDRESS_CANARY, "postcode": "NB1 9ZZ"},
            "resident_bindings": [{"measure": "Loft insulation", "context_revision": 1}],
        }
        cavity_binding = {
            "home": {"address": ADDRESS_CANARY, "postcode": "NB1 9ZZ"},
            "resident_bindings": [{"measure": "Cavity wall", "context_revision": 1}],
        }
        orders: list[dict[str, Any]] = [
            {
                "id": "WO-OFFERED",
                "case_id": "ZF-REP-1",
                "state": "Issued",
                "appointment_offer": {
                    "id": "OFF-1",
                    "date": "2026-11-12",
                    "period": "Morning",
                    "options": ["09:00-11:00"],
                    "instructions": "Ring doorbell twice.",
                    "constraints": HOUSEHOLD_NOTE_CANARY,
                    "binding": loft_binding,
                    "confirmations": {"staff": {"offer": "OFF-1"}, "capacity": {"offer": "OFF-1"}},
                },
                "appointment_authorities": {
                    "REP-1": {
                        "revoked": False,
                        "task": "Appointment agreement",
                        "offer": "OFF-1",
                        "binding": loft_binding,
                        "valid_from": "2026-11-01",
                        "valid_to": "2026-11-14",
                    }
                },
            },
            {
                "id": "WO-CONFIRMED",
                "case_id": "ZF-REP-1",
                "state": "Appointed",
                "appointment_offer": {
                    "id": "OFF-2",
                    "date": "2026-11-13",
                    "period": "Afternoon",
                    "options": ["13:00-15:00"],
                    "instructions": "Side gate access.",
                    "binding": loft_binding,
                    "confirmations": {
                        "resident": {"offer": "OFF-2"},
                        "staff": {"offer": "OFF-2"},
                        "capacity": {"offer": "OFF-2"},
                    },
                },
            },
            {
                "id": "WO-OUT-OF-SCOPE",
                "case_id": "ZF-REP-1",
                "state": "Appointed",
                "appointment_offer": {
                    "id": "OFF-CAVITY",
                    "date": "2026-11-14",
                    "period": "Morning",
                    "binding": cavity_binding,
                    "confirmations": {
                        "resident": {"offer": "OFF-CAVITY"},
                        "staff": {"offer": "OFF-CAVITY"},
                        "capacity": {"offer": "OFF-CAVITY"},
                    },
                },
            },
        ]
        view = rjd.project_representative_view(
            case, "REP-1", now=self.ACTIVE_NOW, work_orders=orders
        )
        self.assertTrue(view["active"])
        self.assertEqual(view["journey_stages"], ["R1", "J3"])
        self.assertEqual(
            view["permitted_actions"], ["view_visit_arrangements", "confirm_appointment"]
        )
        self.assertNotIn("progress", view["measures"][0])
        self.assertEqual(len(view["appointments"]["offered"]), 1)
        self.assertEqual(len(view["appointments"]["confirmed"]), 1)
        self.assertEqual(
            view["appointments"]["offered"][0]["booking_status"], "Offered - not booked"
        )
        self.assertTrue(view["appointments"]["offered"][0]["can_confirm_appointment"])
        self.assertEqual(view["appointments"]["confirmed"][0]["booking_status"], "Visit confirmed")
        _assert_no_canaries(self, view)

        with self.assertRaises(rjd.RepresentativeScopeDeniedError):
            rjd.enforce_representative_action(
                case,
                "REP-1",
                "submit_measure_decision",
                measure="Loft insulation",
                now=self.ACTIVE_NOW,
                work_orders=orders,
            )

    def test_works_decision_scopes_to_authorized_measure_and_isolates_multiple_reps(self) -> None:
        case = _synthetic_case(tasks=["Works decision"])
        rep2 = copy.deepcopy(case["representative_authorities"]["REP-1"][0])
        rep2.update(representative_ref="REP-2", tasks=["Attend"])
        case["representative_authorities"]["REP-2"] = [rep2]

        view_rep1 = rjd.project_representative_view(case, "REP-1", now=self.ACTIVE_NOW)
        view_rep2 = rjd.project_representative_view(case, "REP-2", now=self.ACTIVE_NOW)
        self.assertEqual(view_rep1["journey_stages"], ["R1", "J1", "J2"])
        self.assertEqual(
            view_rep1["permitted_actions"],
            [
                "view_task_briefing",
                "submit_measure_decision",
                "pause_measure",
                "withdraw_measure",
            ],
        )
        self.assertEqual(view_rep1["measures"][0]["decision"]["status"], "Waiting")
        self.assertNotIn("note", view_rep1["measures"][0]["decision"])
        self.assertEqual(view_rep2["journey_stages"], ["R1", "J3"])
        self.assertEqual(view_rep2["permitted_actions"], ["view_visit_arrangements"])
        _assert_no_canaries(self, view_rep1)

        allowed = rjd.enforce_representative_action(
            case,
            "REP-1",
            "submit_measure_decision",
            measure="Loft insulation",
            assistant_topic="consents",
            now=self.ACTIVE_NOW,
        )
        self.assertTrue(allowed["allowed"])
        for bad_action, bad_measure, bad_topic in (
            ("submit_measure_decision", "Cavity wall", None),
            ("confirm_appointment", "Loft insulation", None),
            ("submit_measure_decision", "Loft insulation", "home"),
            ("submit_measure_decision", "Loft insulation", "documents"),
        ):
            with self.assertRaises(rjd.RepresentativeScopeDeniedError):
                rjd.enforce_representative_action(
                    case,
                    "REP-1",
                    bad_action,
                    measure=bad_measure,
                    assistant_topic=bad_topic,
                    now=self.ACTIVE_NOW,
                )


class RepresentativeExpiryAndSessionEnforcementTests(unittest.TestCase):
    def test_mid_session_expiry_transitions_immediately_blocks_actions_and_surfaces_renewal(
        self,
    ) -> None:
        case = _synthetic_case(
            expires_at="2026-11-15T14:00:00Z", tasks=["Receive information", "Works decision"]
        )
        sessions = rjd.RepresentativeSessionStore()
        before_expiry = datetime(2026, 11, 15, 13, 59, 59, tzinfo=UTC)
        session, initial_view = sessions.open_session(case, "REP-1", now=before_expiry)
        self.assertTrue(session.active)
        self.assertTrue(initial_view["active"])
        self.assertEqual(initial_view["expires_at"], "2026-11-15T14:00:00Z")
        checked = sessions.session_action(
            session.session_id,
            case,
            "submit_measure_decision",
            measure="Loft insulation",
            now=before_expiry,
        )
        self.assertTrue(checked["allowed"])

        # Exact recorded expiry moment expressed with a +02:00 offset (16:00+02:00 == 14:00Z).
        at_expiry = datetime(2026, 11, 15, 16, 0, 0, tzinfo=timezone(timedelta(hours=2)))
        expired_view = sessions.session_view(session.session_id, case, now=at_expiry)
        self.assertFalse(expired_view["active"])
        self.assertEqual(expired_view["state"], "expired")
        self.assertEqual(expired_view["reason"], "expired")
        self.assertEqual(expired_view["expires_at"], "2026-11-15T14:00:00Z")
        self.assertEqual(expired_view["journey_stages"], [])
        self.assertEqual(expired_view["permitted_actions"], [])
        self.assertNotIn("measures", expired_view)
        self.assertNotIn("case_id", expired_view)
        self.assertEqual(
            expired_view["renewal_route"]["recorded_expires_at"], "2026-11-15T14:00:00Z"
        )
        self.assertTrue(expired_view["renewal_route"]["non_digital_supported"])
        self.assertIn("Housing Officer", expired_view["renewal_route"]["staff_route"])
        self.assertIn("without a portal", expired_view["renewal_route"]["resident_route"])
        self.assertEqual(session.state, "expired")
        _assert_no_canaries(self, expired_view)

        with self.assertRaises(rjd.RepresentativeAccessBlockedError) as ctx:
            sessions.session_action(
                session.session_id,
                case,
                "submit_measure_decision",
                measure="Loft insulation",
                now=at_expiry,
            )
        err_payload = ctx.exception.to_payload()
        self.assertEqual(err_payload["state"], "expired")
        self.assertEqual(err_payload["expires_at"], "2026-11-15T14:00:00Z")
        self.assertEqual(
            err_payload["renewal_route"]["recorded_expires_at"], "2026-11-15T14:00:00Z"
        )

    def test_missing_malformed_revoked_disputed_unclear_and_changed_context_hold_session(
        self,
    ) -> None:
        now = datetime(2026, 11, 10, 12, 0, 0, tzinfo=UTC)
        for bad_exp in (None, "", "2026-11-15", "2026-11-15T14:00:00", "not-a-timestamp"):
            bad_case = _synthetic_case(expires_at=bad_exp)
            held = rjd.project_representative_view(bad_case, "REP-1", now=now)
            self.assertFalse(held["active"], bad_exp)
            self.assertEqual(held["state"], "held")
            self.assertEqual(held["reason"], "missing_expiry")
            self.assertIsNone(held["expires_at"])

        for status, expected_reason in (
            ("Revoked", "revoked"),
            ("Disputed", "disputed"),
            ("Unclear", "unclear"),
        ):
            case = _synthetic_case(tasks=["Works decision"])
            sessions = rjd.RepresentativeSessionStore()
            session, _ = sessions.open_session(case, "REP-1", now=now)
            self.assertTrue(session.active)
            v2 = copy.deepcopy(case["representative_authorities"]["REP-1"][-1])
            v2.update(version=2, status=status)
            case["representative_authorities"]["REP-1"].append(v2)
            transitioned = sessions.session_view(session.session_id, case, now=now)
            self.assertFalse(transitioned["active"])
            self.assertEqual(transitioned["state"], "held")
            self.assertEqual(transitioned["reason"], expected_reason)
            self.assertEqual(transitioned["expires_at"], "2026-11-15T14:00:00Z")
            self.assertEqual(
                transitioned["renewal_route"]["recorded_expires_at"], "2026-11-15T14:00:00Z"
            )
            with self.assertRaises(rjd.RepresentativeAccessBlockedError):
                sessions.session_action(session.session_id, case, "view_task_briefing", now=now)

        # Safe contact change and scope revision bump immediately invalidate active authority.
        contact_changed = _synthetic_case(tasks=["Receive information"])
        contact_changed["resident_safe_contact"] = "NEW-SAFE-CONTACT-REF"
        self.assertEqual(
            rjd.project_representative_view(contact_changed, "REP-1", now=now)["reason"],
            "safe_contact_changed",
        )

        scope_changed = _synthetic_case(tasks=["Receive information"])
        scope_changed["resident_scopes"]["Loft insulation"].append(
            {
                "revision": 2,
                "case_id": "ZF-REP-1",
                "measure": "Loft insulation",
                "scope": "Revised scope",
                "design_version": 3,
                "source": "Survey pack v3",
            }
        )
        self.assertEqual(
            rjd.project_representative_view(scope_changed, "REP-1", now=now)["reason"],
            "scope_changed",
        )

        # Wiping the authority record mid-session still preserves the session's recorded expires_at.
        wiped = _synthetic_case(tasks=["Receive information"])
        sessions = rjd.RepresentativeSessionStore()
        session, _ = sessions.open_session(wiped, "REP-1", now=now)
        wiped["representative_authorities"].pop("REP-1")
        wiped_view = sessions.session_view(session.session_id, wiped, now=now)
        self.assertEqual(wiped_view["state"], "held")
        self.assertEqual(wiped_view["reason"], "missing_authority")
        self.assertEqual(wiped_view["expires_at"], "2026-11-15T14:00:00Z")

    def test_store_representative_record_authority_for_and_showcase_grant_expiry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_path = Path(tmp) / "store.json"
            data_path.write_text(
                json.dumps(
                    {
                        "staff": [
                            {
                                "code": "RLO-1",
                                "name": "Ria Liaison",
                                "email": "ria@example.test",
                                "role": "Resident Liaison Officer",
                            }
                        ],
                        "cases": [
                            {
                                "id": "ZF-S1",
                                "stage": "Survey being booked",
                                "owner": "Ria Liaison",
                                "owner_code": "RLO-1",
                                "resident": {"name": "Sam Resident", "phone": PHONE_CANARY},
                                "home": {
                                    "address": ADDRESS_CANARY,
                                    "town": "Northborough",
                                    "postcode": "NB1 1AA",
                                    "tenure": "Tenant",
                                },
                                "measures": ["Loft insulation", "Cavity wall"],
                                "technical": {"design_version": 1},
                                "contacts": [],
                                "hazards": [],
                                "documents": [],
                            }
                        ],
                        "audit": [],
                    }
                ),
                encoding="utf-8",
            )
            store: Any = Store(str(data_path))
            rlo = store.staff["ria@example.test"]
            with patch.object(controls, "today", return_value="2026-11-10"):
                store.resident_action(
                    rlo,
                    "ZF-S1",
                    {
                        "action": "scope_record",
                        "measure": "Loft insulation",
                        "scope": "Main loft",
                        "design_version": 1,
                        "source": "SRC-1",
                    },
                )
                store.resident_action(
                    rlo,
                    "ZF-S1",
                    {
                        "action": "safe_contact_record",
                        "safe_contact_ref": "SAFE-1",
                        "source": "SRC-SAFE",
                    },
                )
                for invalid_body in (
                    {"representative_ref": "Unknown", "expires_at": "2026-11-12T15:00:00Z"},
                    {"representative_ref": "REP-STORE", "expires_at": "2026-11-12T15:00:00"},
                    {"representative_ref": "REP-STORE", "expires_at": "2026-11-25T15:00:00Z"},
                ):
                    with self.assertRaises(ValueError):
                        store.resident_action(
                            rlo,
                            "ZF-S1",
                            {
                                "action": "representative_record",
                                "measure": "Loft insulation",
                                "context_revision": 1,
                                "status": "Confirmed",
                                "tasks": ["Works decision"],
                                "authority_date": "2026-11-10",
                                "review_date": "2026-11-15",
                                "safe_contact_ref": "SAFE-1",
                                "source": "AUTH-SRC",
                                "resident_wishes": "Loft choice only",
                                **invalid_body,
                            },
                        )
                store.resident_action(
                    rlo,
                    "ZF-S1",
                    {
                        "action": "representative_record",
                        "measure": "Loft insulation",
                        "context_revision": 1,
                        "representative_ref": "REP-STORE",
                        "status": "Confirmed",
                        "tasks": ["Works decision"],
                        "authority_date": "2026-11-10",
                        "review_date": "2026-11-15",
                        "expires_at": "2026-11-12T15:00:00Z",
                        "safe_contact_ref": "SAFE-1",
                        "source": "AUTH-SRC",
                        "resident_wishes": "Loft choice only",
                    },
                )
                case_obj = store._case("ZF-S1")
                ctx = rd.current_context(case_obj, "Loft insulation")
                active_at = datetime(2026, 11, 12, 14, 59, 59, tzinfo=UTC)
                expired_at = datetime(2026, 11, 12, 15, 0, 0, tzinfo=UTC)
                rec = rd.authority_for(
                    case_obj,
                    "REP-STORE",
                    "Works decision",
                    "Loft insulation",
                    ctx,
                    now=active_at,
                )
                self.assertEqual(rec["expires_at"], "2026-11-12T15:00:00Z")
                with self.assertRaises(ValueError):
                    rd.authority_for(
                        case_obj,
                        "REP-STORE",
                        "Works decision",
                        "Loft insulation",
                        ctx,
                        now=expired_at,
                    )

                proj_ok = store.representative_view(
                    rlo, "ZF-S1", "REP-STORE", now=active_at, session_id="SID-1"
                )
                self.assertTrue(proj_ok["active"])
                self.assertEqual(proj_ok["measures"][0]["measure"], "Loft insulation")
                proj_exp = store.representative_view(
                    rlo, "ZF-S1", "REP-STORE", now=expired_at, session_id="SID-1"
                )
                self.assertFalse(proj_exp["active"])
                self.assertEqual(proj_exp["state"], "expired")
                self.assertEqual(proj_exp["expires_at"], "2026-11-12T15:00:00Z")

        # Showcase representative grant projection & expiry
        showcase_now = datetime(2026, 10, 25, 12, 0, 0, tzinfo=UTC)
        row = rs.ShowcaseRow(
            case_id="SYN-CASE-1",
            email="resident.one@example.com",
            email_count=1,
            provenance="owner-approved test fixture",
            valid_from=showcase_now - timedelta(days=1),
            valid_to=showcase_now + timedelta(days=2),
            revoked=False,
            address=ADDRESS_CANARY,
            town="Northborough",
            postcode="NB1 1AA",
            stage="Survey being booked",
            closed=False,
            measures=("Loft insulation", "Cavity wall"),
            documents=DocumentFacts(
                requests=(
                    DocumentRequest(
                        id="REQ-1",
                        kind="Lease",
                        how_to_provide=HOUSEHOLD_NOTE_CANARY,
                    ),
                )
            ),
        )
        grant = rs.RepresentativeShowcaseGrant(
            case_id="SYN-CASE-1",
            email="rep.one@example.com",
            representative_ref="REP-SHOW-1",
            measure="Loft insulation",
            tasks=("Receive information",),
            valid_from=showcase_now - timedelta(hours=2),
            expires_at=showcase_now + timedelta(minutes=30),
        )
        active_show = rs.representative_showcase_view(grant, row, showcase_now)
        self.assertTrue(active_show["active"])
        self.assertEqual([m["measure"] for m in active_show["measures"]], ["Loft insulation"])
        self.assertNotIn("home", active_show)
        self.assertNotIn("sensors", active_show)
        self.assertNotIn("case_id", active_show)
        _assert_no_canaries(self, active_show)

        expired_show = rs.representative_showcase_view(
            grant, row, showcase_now + timedelta(minutes=30)
        )
        self.assertFalse(expired_show["active"])
        self.assertEqual(expired_show["state"], "expired")
        self.assertEqual(
            expired_show["expires_at"],
            rjd.format_iso_utc(showcase_now + timedelta(minutes=30)),
        )


if __name__ == "__main__":
    unittest.main()
