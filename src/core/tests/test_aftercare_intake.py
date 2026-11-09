"""Assisted aftercare intake, receipts and joined synthetic view (#133 Stage A).

Constructed records only. The state files live in a temporary directory.
"""

import json
import tempfile
import threading
import unittest
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from zava_forward.core import aftercare_intake as ai
from zava_forward.core import projection
from zava_forward.core.aftercare import BANNED_PHRASES
from zava_forward.core.synthetic import sensor_scenarios as ss

NOW = datetime(2026, 11, 9, 12, 0, tzinfo=UTC)
LIAISON = {"name": "Synthetic Liaison", "role": "Resident Liaison Officer"}
COORDINATOR = {"name": "Synthetic Coordinator", "role": "Retrofit Coordinator"}
MANAGER = {"name": "Synthetic Manager", "role": "Retrofit Programme Manager"}
SUPPORT = {"name": "Synthetic Support", "role": "Programme Support Officer"}
INSPECTOR = {"name": "Synthetic Inspector", "role": "Quality Inspector"}
CONTRACTOR = {"name": "Synthetic Contractor", "role": "Contractor"}
HOMES = [
    str(cast(list[dict[str, str]], s["rows"])[0]["home_id"])
    for s in ss.retrofit_exercise_scenarios()
]
HOME = HOMES[0]
Values = dict[str, Any]


def values(**kw: Any) -> Values:
    base: Values = {
        "request_id": "req-0000001",
        "raised_by": "household",
        "home_ref": HOME,
        "kind": "discomfort",
        "statement": "  The living room stays cold in the evening.  ",
        "channel": "phone",
        "next_update": "2026-11-20",
    }
    base.update(kw)
    return base


class Base(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "aftercare.json"
        self.svc = self.service()

    def service(self, store: ai.StateStore | None = None, **kw: Any) -> ai.AftercareService:
        return ai.AftercareService(
            store or ai.FileStateStore(self.path), homes=HOMES, now=lambda: NOW, **kw
        )

    def record(self, user: Values = LIAISON, **kw: Any) -> Values:
        receipt, _ = self.svc.record_concern(user, values(**kw))
        return receipt


class RoleTests(Base):
    def test_role_sets_reuse_existing_staff_roles_only(self) -> None:
        for role in (*ai.RECORD_ROLES, *ai.VIEW_ROLES, *ai.MANAGER):
            self.assertIn(role, projection.STAFF_ROLES)

    def test_only_existing_staff_roles_can_record_or_view(self) -> None:
        staff: list[Any] = [LIAISON, COORDINATOR]
        for user in staff:
            self.svc.record_concern(user, values(request_id=f"req-{user['name'][-5:]}000"))
        denied: list[Any] = [MANAGER, SUPPORT, INSPECTOR, CONTRACTOR, None, {"role": "Unknown"}]
        for user in denied:
            with self.subTest(user=user):
                with self.assertRaises(PermissionError):
                    self.svc.record_concern(user, values(request_id="req-denied-01"))
        no_view: list[Any] = [INSPECTOR, CONTRACTOR, None, {"role": "Application Administrator"}]
        for user in no_view:
            with self.subTest(view=user):
                with self.assertRaises(PermissionError):
                    self.svc.concerns(user)
                with self.assertRaises(PermissionError):
                    self.svc.evaluator_view(user)
        self.assertEqual(self.svc.concerns(MANAGER)["count"], 2)

    def test_named_staff_is_required_for_the_record(self) -> None:
        with self.assertRaises(PermissionError):
            self.svc.record_concern({"role": LIAISON["role"]}, values())


class IntakeTests(Base):
    def test_receipt_keeps_provenance_original_text_and_unknown_owner(self) -> None:
        receipt = self.record()
        self.assertEqual(receipt["receipt_id"], "RC-AC-001")
        self.assertEqual(receipt["route"], "staff_recorded")
        self.assertEqual(receipt["channel"], "phone")
        self.assertEqual(receipt["recorded_by"], LIAISON)
        self.assertEqual(receipt["original"]["statement"], values()["statement"])
        self.assertEqual(receipt["owner"], {"label": ai.UNKNOWN_OWNER, "status": "unknown"})
        self.assertIn("No owner is named yet", receipt["what_happens_next"])
        self.assertIn("2026-11-20", receipt["what_happens_next"])
        self.assertIn("does not close it", receipt["what_happens_next"])
        self.assertEqual(receipt["received_at"], "2026-11-09T12:00:00+00:00")
        self.assertIn("no digital access", receipt["accessible_route"].lower())

    def test_every_channel_is_accepted_and_digital_is_not(self) -> None:
        for n, channel in enumerate(("phone", "in_person", "paper", "assisted_visit")):
            self.record(request_id=f"req-chan-{n:03d}", channel=channel)
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(request_id="req-chan-bad", channel="email")
        self.assertIn("channel", ctx.exception.errors)

    def test_representative_basis_is_required_and_kept_verbatim(self) -> None:
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(raised_by="representative")
        self.assertIn("representative_basis", ctx.exception.errors)
        receipt = self.record(
            raised_by="representative", representative_basis=" Named in the household's note "
        )
        self.assertEqual(
            receipt["original"]["representative_basis"], " Named in the household's note "
        )
        shown = self.svc.concern(LIAISON, "AC-001")
        self.assertEqual(shown["representative_basis"], " Named in the household's note ")
        self.assertEqual(shown["raised_by"], "representative")

    def test_household_route_ignores_a_stray_basis(self) -> None:
        receipt = self.record(representative_basis="Not applicable text")
        self.assertIsNone(receipt["original"]["representative_basis"])

    def test_all_field_errors_are_returned_together_in_plain_language(self) -> None:
        with self.assertRaises(ai.ValidationError) as ctx:
            self.svc.record_concern(
                LIAISON,
                {"request_id": "x", "raised_by": "neighbour", "next_update": "soon", "kind": "?"},
            )
        errors = ctx.exception.errors
        for field in (
            "request_id",
            "raised_by",
            "home_ref",
            "kind",
            "statement",
            "channel",
            "next_update",
        ):
            self.assertIn(field, errors)
        self.assertEqual(self.svc.concerns(MANAGER)["count"], 0)

    def test_home_must_be_in_the_stated_synthetic_set_and_past_date_is_refused(self) -> None:
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(home_ref="HOME-NOT-IN-SET")
        self.assertIn("home_ref", ctx.exception.errors)
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(next_update="2026-11-08")
        self.assertIn("next_update", ctx.exception.errors)

    def test_personal_details_and_oversize_text_are_refused_in_every_free_text(self) -> None:
        for text in ("Call me on 07700 900123", "mail me@example.org", "SW1A 1AA is cold"):
            with self.subTest(text=text), self.assertRaises(ai.ValidationError) as ctx:
                self.record(statement=text)
            self.assertIn("statement", ctx.exception.errors)
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(statement="x" * (ai.STATEMENT_MAX + 1))
        self.assertIn("too long", ctx.exception.errors["statement"])
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(raised_by="representative", representative_basis="note me@example.org")
        self.assertIn("representative_basis", ctx.exception.errors)
        self.record(request_id="req-clean-001")
        self.svc.assign_owner(MANAGER, "AC-001", "Resident Liaison Officer")
        with self.assertRaises(ai.ValidationError):
            self.svc.record_outcome(
                LIAISON, "AC-001", "advice_given", "home_visit", "Rang 07700 900123"
            )
        with self.assertRaises(ai.ValidationError):
            self.svc.set_remedy(LIAISON, "AC-001", "open", "a.b@example.org")

    def test_intake_cannot_name_an_owner_so_a_new_concern_has_an_unknown_one(self) -> None:
        with self.assertRaises(ai.ValidationError) as ctx:
            self.record(owner_role="Resident Liaison Officer")
        self.assertIn("owner_role", ctx.exception.errors)
        self.assertEqual(self.svc.concerns(MANAGER)["count"], 0)

    def test_replay_returns_the_same_receipt_and_a_changed_payload_conflicts(self) -> None:
        first, replayed = self.svc.record_concern(LIAISON, values())
        again, replay = self.svc.record_concern(LIAISON, values())
        self.assertFalse(replayed)
        self.assertTrue(replay)
        self.assertEqual(first, again)
        self.assertEqual(self.svc.concerns(MANAGER)["count"], 1)
        with self.assertRaises(ai.ConflictError):
            self.svc.record_concern(LIAISON, values(statement="A different concern."))
        self.assertEqual(self.svc.concerns(MANAGER)["count"], 1)

    def test_concurrent_services_on_one_store_keep_every_receipt(self) -> None:
        errors: list[BaseException] = []

        def worker(n: int) -> None:
            try:
                svc = self.service()
                for i in range(5):
                    svc.record_concern(LIAISON, values(request_id=f"req-t{n}-{i:04d}"))
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(n,)) for n in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        shown = self.service().concerns(MANAGER)
        self.assertEqual(shown["count"], 20)
        self.assertEqual(len({c["id"] for c in shown["items"]}), 20)


class PersistenceTests(Base):
    def test_state_survives_a_new_service_and_keeps_original_whitespace(self) -> None:
        self.record()
        self.svc.assign_owner(MANAGER, "AC-001", "Resident Liaison Officer")
        self.svc.start_investigation(LIAISON, "AC-001", "2026-11-25")
        reopened = self.service()
        shown = reopened.concern(COORDINATOR, "AC-001")
        self.assertEqual(shown["statement"], values()["statement"])
        self.assertEqual(shown["investigation"], "under_investigation")
        self.assertEqual(shown["recorded_by"], LIAISON["name"])
        doc = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(doc["format"], ai.FORMAT)
        self.assertEqual(doc["version"], 3)
        self.assertEqual([a["action"] for a in doc["actions"]][0], "concern_recorded")

    def test_failed_write_saves_nothing_and_reports_plainly(self) -> None:
        class Failing:
            def __init__(self, inner: ai.FileStateStore) -> None:
                self.inner = inner

            def read(self) -> str | None:
                return self.inner.read()

            def update(self, mutator: Callable[[str | None], tuple[str, Any]]) -> Any:
                mutator(self.inner.read())
                raise ai.PersistenceError("The record could not be saved. Nothing was saved.")

        failing = self.service(Failing(ai.FileStateStore(self.path)))
        status, payload = failing.handle("POST", "/api/aftercare/concerns", LIAISON, values())
        self.assertEqual(status, 503)
        self.assertIn("Nothing was saved", payload["error"])
        self.assertFalse(self.path.exists())
        self.assertEqual(self.service().concerns(MANAGER)["count"], 0)

    def test_corrupt_or_inconsistent_state_is_refused_and_never_overwritten(self) -> None:
        self.record()
        good = self.path.read_text(encoding="utf-8")
        doc = json.loads(good)
        bad_docs: list[str] = [
            "{not json",
            json.dumps({**doc, "format": "other"}),
            json.dumps({**doc, "version": -1}),
            json.dumps({**doc, "receipts": {}}),
            json.dumps(
                {**doc, "requests": {"req-0000001": {"fingerprint": "x", "concern_id": "AC-001"}}}
            ),
        ]
        changed = json.loads(good)
        changed["receipts"]["AC-001"]["home_ref"] = HOMES[1]
        bad_docs.append(json.dumps(changed))
        changed = json.loads(good)
        changed["receipts"]["AC-001"]["original"]["statement"] = "A different statement"
        bad_docs.append(json.dumps(changed))
        changed = json.loads(good)
        changed["register"]["concerns"]["AC-001"]["dismissed_by_sensor"] = True
        bad_docs.append(json.dumps(changed))
        for text in bad_docs:
            with self.subTest(text=text[:40]):
                self.path.write_text(text, encoding="utf-8")
                svc = self.service()
                with self.assertRaises(ai.StateInvalid):
                    svc.concerns(MANAGER)
                status, payload = svc.handle("POST", "/api/aftercare/concerns", LIAISON, values())
                self.assertEqual(status, 503)
                self.assertIn("left unchanged", payload["error"])
                self.assertEqual(self.path.read_text(encoding="utf-8"), text)


class OwnerLifecycleTests(Base):
    def setUp(self) -> None:
        super().setUp()
        self.record()

    def test_unknown_owner_cannot_be_acted_for_and_is_listed_unresolved(self) -> None:
        calls: list[Callable[[], Any]] = [
            lambda: self.svc.start_investigation(LIAISON, "AC-001", "2026-11-25"),
            lambda: self.svc.record_outcome(
                LIAISON, "AC-001", "advice_given", "home_visit", "Visit"
            ),
            lambda: self.svc.set_remedy(LIAISON, "AC-001", "open"),
        ]
        for call in calls:
            with self.assertRaisesRegex(PermissionError, "No owner is named"):
                call()
        shown = self.svc.concern(MANAGER, "AC-001")
        self.assertTrue(shown["unresolved"])
        self.assertEqual(shown["owner"]["status"], "unknown")

    def test_assignment_is_manager_only_once_and_labelled_synthetic(self) -> None:
        with self.assertRaises(PermissionError):
            self.svc.assign_owner(LIAISON, "AC-001", "Resident Liaison Officer")
        with self.assertRaises(ai.ValidationError):
            self.svc.assign_owner(MANAGER, "AC-001", "Contractor")
        shown = self.svc.assign_owner(MANAGER, "AC-001", "Resident Liaison Officer")
        self.assertEqual(
            shown["owner"]["label"], "Resident Liaison Officer (synthetic scenario owner)"
        )
        self.assertEqual(shown["owner"]["status"], "synthetic_scenario_owner")
        with self.assertRaises(ai.ConflictError):
            self.svc.assign_owner(MANAGER, "AC-001", "Retrofit Coordinator")
        self.assertEqual(shown["history"][-1], {"event": "owner_assigned"})

    def test_only_the_owner_role_acts_and_remedy_needs_evidence(self) -> None:
        self.svc.assign_owner(MANAGER, "AC-001", "Resident Liaison Officer")
        with self.assertRaisesRegex(PermissionError, "named owner"):
            self.svc.start_investigation(COORDINATOR, "AC-001", "2026-11-25")
        with self.assertRaises(PermissionError):
            self.svc.start_investigation(INSPECTOR, "AC-001", "2026-11-25")
        shown = self.svc.start_investigation(LIAISON, "AC-001", "2026-11-25")
        self.assertEqual(shown["investigation"], "under_investigation")
        with self.assertRaises(ValueError):
            self.svc.record_outcome(LIAISON, "AC-001", "remedy_needed", "sensor_reading", "x")
        shown = self.svc.record_outcome(
            LIAISON, "AC-001", "remedy_needed", "home_visit", "Visited with the household."
        )
        self.assertEqual(shown["remedy"]["status"], "open")
        with self.assertRaises(ValueError):
            self.svc.set_remedy(LIAISON, "AC-001", "completed")
        self.assertEqual(self.svc.concern(MANAGER, "AC-001")["investigation"], "outcome_recorded")

    def test_closure_never_changes_the_concern_or_erases_the_remedy(self) -> None:
        self.svc.assign_owner(MANAGER, "AC-001", "Resident Liaison Officer")
        self.svc.record_outcome(LIAISON, "AC-001", "remedy_needed", "home_visit", "Visited.")
        before = self.svc.concern(MANAGER, "AC-001")
        with self.assertRaises(PermissionError):
            self.svc.record_closure(LIAISON, HOME, "handover", "2026-11-01")
        for kind in ("handover", "financial"):
            self.svc.record_closure(MANAGER, HOME, kind, "2026-11-01")
        after = self.svc.concern(MANAGER, "AC-001")
        self.assertEqual(after["remedy"], before["remedy"])
        self.assertEqual(after["investigation"], before["investigation"])
        self.assertTrue(after["unresolved"])
        self.assertEqual({c["kind"] for c in after["closures"]}, {"handover", "financial"})
        self.assertIn("do not change this concern", after["closures"][0]["note"])
        view = self.svc.evaluator_view(MANAGER)
        self.assertEqual(view["totals"]["unresolved_with_handover_or_financial_closure"], 1)

    def test_normal_sensor_context_never_dismisses_and_stays_staff_only(self) -> None:
        shown = self.svc.add_sensor_context(
            COORDINATOR, "AC-001", {"signal": "NO_EXERCISE_SIGNAL", "label": "Normal reading"}
        )
        self.assertFalse(shown["dismissed_by_sensor"])
        self.assertTrue(shown["unresolved"])
        self.assertEqual(shown["investigation"], "received")
        self.assertIn("does not close", shown["sensor_note"])
        view = self.svc.evaluator_view(MANAGER)
        row = next(r for r in view["rows"] if r["home_ref"] == HOME)
        self.assertEqual(row["unresolved_count"], 1)
        with self.assertRaises(ValueError):
            self.svc.add_sensor_context(COORDINATOR, "AC-001", {"signal": "this was caused by it"})
        with self.assertRaises(PermissionError):
            self.svc.add_sensor_context(INSPECTOR, "AC-001", {"signal": "x"})

    def test_overdue_is_flagged_against_the_service_date(self) -> None:
        late = ai.AftercareService(
            ai.FileStateStore(self.path),
            homes=HOMES,
            now=lambda: datetime(2026, 12, 1, tzinfo=UTC),
        )
        self.assertTrue(late.concern(MANAGER, "AC-001")["overdue"])
        self.assertFalse(self.svc.concern(MANAGER, "AC-001")["overdue"])


class JoinedViewTests(Base):
    def test_every_home_has_a_row_with_denominators_and_unknowns(self) -> None:
        view = self.svc.evaluator_view(MANAGER)
        self.assertEqual(len(view["rows"]), 4)
        totals = view["totals"]
        self.assertEqual(totals["homes_in_cohort"], 4)
        self.assertEqual(totals["homes_with_usable_comparison"], {"count": 4, "denominator": 4})
        self.assertEqual(totals["households_raising_concern"], {"count": 0, "denominator": 4})
        self.assertEqual(totals["concerns_unresolved"], {"count": 0, "denominator": 0})
        row = view["rows"][0]
        self.assertEqual(row["comparison"]["status"], "sufficient")
        self.assertIsNotNone(row["comparison"]["baseline"]["temperature_c"])
        self.assertIn(
            "Households that did not raise a concern may still have one.", view["unknowns"]
        )
        self.assertTrue(any("not approved" in u for u in view["unknowns"]))
        self.assertTrue(any("data protection" in u for u in view["unknowns"]))
        self.assertIn("not a promise of savings", view["notice"])

    def test_concern_is_listed_whatever_the_comparison_says(self) -> None:
        self.record(home_ref=HOMES[1])
        view = self.svc.evaluator_view(SUPPORT)
        row = next(r for r in view["rows"] if r["home_ref"] == HOMES[1])
        self.assertEqual(row["comparison"]["status"], "sufficient")
        self.assertEqual([c["id"] for c in row["concerns"]], ["AC-001"])
        self.assertTrue(row["concerns"][0]["unresolved"])
        self.assertEqual(
            view["totals"]["households_raising_concern"], {"count": 1, "denominator": 4}
        )
        self.assertEqual(view["totals"]["concerns_unresolved"], {"count": 1, "denominator": 1})

    def test_insufficient_or_missing_comparison_is_unknown_without_partial_means(self) -> None:
        scenarios = list(ss.retrofit_exercise_scenarios())
        short = dict(scenarios[0])
        short["rows"] = tuple(list(cast(Any, short["rows"]))[:6])
        svc = self.service(scenarios=[short, *scenarios[1:]], cohort=[*HOMES, "H-NO-SCENARIO"])
        view = svc.evaluator_view(MANAGER)
        by_home = {r["home_ref"]: r for r in view["rows"]}
        for home in (HOME, "H-NO-SCENARIO"):
            comparison = by_home[home]["comparison"]
            self.assertEqual(comparison["status"], "unknown", home)
            for key in ("baseline", "early", "late", "deltas"):
                self.assertIsNone(comparison[key])
        self.assertEqual(
            view["totals"]["homes_with_usable_comparison"], {"count": 3, "denominator": 5}
        )
        self.assertEqual(view["register_summary"]["homes_baseline_unknown"], 2)

    def test_concern_outside_the_cohort_is_counted_not_hidden(self) -> None:
        self.record(home_ref=HOMES[2])
        narrow = self.service(cohort=HOMES[:2])
        view = narrow.evaluator_view(MANAGER)
        self.assertEqual(view["totals"]["concerns_outside_stated_scope"], 1)
        self.assertEqual(view["totals"]["homes_in_cohort"], 2)


class NeutralTextTests(Base):
    def strings(self, value: Any, skip: tuple[str, ...]) -> list[str]:
        out: list[str] = []
        if isinstance(value, dict):
            for key, item in value.items():
                if key not in skip:
                    out += self.strings(item, skip)
        elif isinstance(value, list):
            for item in value:
                out += self.strings(item, skip)
        elif isinstance(value, str):
            out.append(value)
        return out

    def test_no_templated_text_states_causation_blame_or_savings(self) -> None:
        receipt = self.record(raised_by="representative", representative_basis="Written note")
        self.svc.assign_owner(MANAGER, "AC-001", "Resident Liaison Officer")
        self.svc.record_closure(MANAGER, HOME, "handover", "2026-11-01")
        payloads = [
            self.svc.form(LIAISON),
            receipt,
            self.svc.concern(MANAGER, "AC-001"),
            self.svc.evaluator_view(MANAGER),
        ]
        free_text = ("original", "statement", "representative_basis")
        for payload in payloads:
            for text in self.strings(payload, free_text):
                for phrase in BANNED_PHRASES:
                    self.assertNotIn(phrase, text.lower(), text)


class RouteTests(Base):
    def call(self, method: str, path: str, user: Any = LIAISON, body: Any = None) -> Any:
        return self.svc.handle(method, path, user, body)

    def test_form_record_list_show_and_evaluator(self) -> None:
        status, form = self.call("GET", "/api/aftercare/form")
        self.assertEqual((status, form["assisted"]), (200, True))
        self.assertEqual(sorted(form["homes"]), sorted(HOMES))
        status, payload = self.call("POST", "/api/aftercare/concerns", body=values())
        self.assertEqual(status, 201)
        self.assertFalse(payload["replayed"])
        status, payload = self.call("POST", "/api/aftercare/concerns", body=values())
        self.assertEqual((status, payload["replayed"]), (200, True))
        self.assertEqual(self.call("GET", "/api/aftercare/concerns", MANAGER)[1]["count"], 1)
        listed = self.svc.handle("GET", "/api/aftercare/concerns", MANAGER, None, {"home_ref": "X"})
        self.assertEqual(listed[1]["count"], 0)
        self.assertEqual(self.call("GET", "/api/aftercare/concerns/AC-001", MANAGER)[0], 200)
        self.assertEqual(self.call("GET", "/api/aftercare/evaluator", SUPPORT)[0], 200)

    def test_status_mapping(self) -> None:
        cases: list[tuple[tuple[Any, ...], int]] = [
            (("POST", "/api/aftercare/concerns", CONTRACTOR, values()), 403),
            (("GET", "/api/aftercare/evaluator", None), 403),
            (("POST", "/api/aftercare/concerns", LIAISON, {}), 400),
            (("POST", "/api/aftercare/concerns", LIAISON, [1]), 400),
            (("GET", "/api/aftercare/concerns/AC-999", MANAGER), 404),
            (("GET", "/api/aftercare/nothing", MANAGER), 404),
            (("GET", "/api/aftercarex", MANAGER), 404),
            (("DELETE", "/api/aftercare/concerns", MANAGER), 405),
            (("POST", "/api/aftercare/evaluator", MANAGER, {}), 405),
            (("GET", "/api/aftercare/pack", MANAGER), 404),
        ]
        for args, expected in cases:
            with self.subTest(args=args[:2]):
                self.assertEqual(self.svc.handle(*args)[0], expected)
        status, payload = self.call("POST", "/api/aftercare/concerns", body={"kind": "x"})
        self.assertIn("channel", payload["errors"])
        self.assertTrue(payload["error"])

    def test_lifecycle_routes_and_conflict(self) -> None:
        self.call("POST", "/api/aftercare/concerns", body=values())
        self.assertEqual(
            self.call(
                "POST",
                "/api/aftercare/concerns/AC-001/owner",
                MANAGER,
                {"owner_role": "Resident Liaison Officer"},
            )[0],
            200,
        )
        self.assertEqual(
            self.call(
                "POST",
                "/api/aftercare/concerns/AC-001/owner",
                MANAGER,
                {"owner_role": "Retrofit Coordinator"},
            )[0],
            409,
        )
        steps = [
            ("investigation", {"next_update": "2026-11-30"}),
            ("outcome", {"outcome": "remedy_needed", "basis": "home_visit", "evidence": "Visit."}),
            ("remedy", {"status": "in_progress"}),
            ("sensor-context", {"context": {"signal": "NO_EXERCISE_SIGNAL"}}),
        ]
        for action, body in steps:
            with self.subTest(action=action):
                status, _ = self.call(
                    "POST", f"/api/aftercare/concerns/AC-001/{action}", LIAISON, body
                )
                self.assertEqual(status, 200)
        self.assertEqual(
            self.call(
                "POST",
                "/api/aftercare/closures",
                MANAGER,
                {"home_ref": HOME, "kind": "financial", "closed_on": "2026-11-01"},
            )[0],
            201,
        )
        status, shown = self.call("GET", "/api/aftercare/concerns/AC-001", MANAGER)
        self.assertEqual(shown["remedy"]["status"], "in_progress")
        self.assertTrue(shown["unresolved"])


class ReplayAfterDateTests(Base):
    """C2 finding 3: an exact retry recovers the stored receipt after next_update has passed."""

    def later(self) -> ai.AftercareService:
        tomorrow = datetime(2026, 11, 21, 12, 0, tzinfo=UTC)
        return ai.AftercareService(ai.FileStateStore(self.path), homes=HOMES, now=lambda: tomorrow)

    def test_exact_retry_after_the_update_date_returns_the_original_receipt_unchanged(self) -> None:
        first = self.record(next_update="2026-11-20")
        before = self.path.read_bytes()
        receipt, replayed = self.later().record_concern(LIAISON, values(next_update="2026-11-20"))
        self.assertTrue(replayed)
        self.assertEqual(receipt, first)
        self.assertEqual(self.path.read_bytes(), before)

    def test_changed_payload_after_the_date_conflicts_and_a_new_past_date_is_refused(self) -> None:
        self.record(next_update="2026-11-20")
        before = self.path.read_bytes()
        with self.assertRaises(ai.ConflictError):
            self.later().record_concern(
                LIAISON, values(next_update="2026-11-20", statement="A different statement.")
            )
        with self.assertRaises(ai.ValidationError) as ctx:
            self.later().record_concern(LIAISON, values(request_id="req-0000002"))
        self.assertIn("next_update", ctx.exception.errors)
        self.assertEqual(self.path.read_bytes(), before)

    def test_concurrent_same_request_retries_make_one_concern(self) -> None:
        self.record(next_update="2026-11-20")
        svc = self.later()
        results: list[bool] = []

        def retry() -> None:
            results.append(svc.record_concern(LIAISON, values(next_update="2026-11-20"))[1])

        threads = [threading.Thread(target=retry) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(results, [True] * 6)
        self.assertEqual(self.svc.concerns(MANAGER)["count"], 1)

    def test_replay_over_the_route_after_the_date_is_200(self) -> None:
        self.record(next_update="2026-11-20")
        status, payload = self.later().handle(
            "POST", "/api/aftercare/concerns", LIAISON, values(next_update="2026-11-20")
        )
        self.assertEqual((status, payload["replayed"]), (200, True))


class SensorContextGuardTests(Base):
    """C2 finding 4: sensor context passes the synthetic free-text guard before persistence."""

    def setUp(self) -> None:
        super().setUp()
        self.record()

    def refused(self, context: Any) -> dict[str, str]:
        before = self.path.read_bytes()
        with self.assertRaises(ai.ValidationError) as ctx:
            self.svc.add_sensor_context(COORDINATOR, "AC-001", context)
        self.assertEqual(self.path.read_bytes(), before)
        return ctx.exception.errors

    def test_flagged_values_and_keys_are_refused_without_echo_or_change(self) -> None:
        cases: list[dict[str, str]] = [
            {"note": "call me on 07123456789"},
            {"note": "write to someone@example.com"},
            {"phone_07123456789": "x"},
            {"note": "07123\u200b456789"},
            {"mail": "someone\uff20example.com"},
        ]
        for context in cases:
            with self.subTest(context=context):
                errors = self.refused(context)
                self.assertIn("context", errors)
                self.assertNotIn("07123", json.dumps(errors))
                self.assertNotIn("example", json.dumps(errors))

    def test_shape_and_length_limits(self) -> None:
        for context in (
            {},
            [("a", "b")],
            {"a": 5},
            {"a": ""},
            {"a": "x" * (ai.CONTEXT_VALUE_MAX + 1)},
            {"bad key!": "x"},
            {"a\n": "x"},
            {f"k{i}": "x" for i in range(ai.CONTEXT_MAX_ITEMS + 1)},
        ):
            with self.subTest(context=context):
                self.assertIn("context", self.refused(context))

    def test_merged_context_cannot_exceed_the_key_cap_across_calls(self) -> None:
        half = ai.CONTEXT_MAX_ITEMS // 2 + 1
        self.svc.add_sensor_context(COORDINATOR, "AC-001", {f"a{i}": "x" for i in range(half)})
        self.assertIn("context", self.refused({f"b{i}": "x" for i in range(half)}))
        self.svc.add_sensor_context(COORDINATOR, "AC-001", {"a0": "changed"})

    def test_valid_descriptive_context_is_kept_and_never_dismisses_or_touches_remedy(self) -> None:
        shown = self.svc.add_sensor_context(
            COORDINATOR, "AC-001", {"signal": "NO_EXERCISE_SIGNAL", "label": "Normal reading"}
        )
        self.assertEqual(shown["sensor_context"]["label"], "Normal reading")
        self.assertTrue(shown["unresolved"])
        self.assertFalse(shown["dismissed_by_sensor"])
        self.assertEqual(shown["remedy"]["status"], "not_assessed")

    def test_route_refusal_is_400_with_the_context_error(self) -> None:
        before = self.path.read_bytes()
        status, payload = self.svc.handle(
            "POST",
            "/api/aftercare/concerns/AC-001/sensor-context",
            COORDINATOR,
            {"context": {"note": "someone@example.com"}},
        )
        self.assertEqual(status, 400)
        self.assertIn("context", payload["errors"])
        self.assertNotIn("someone@example.com", json.dumps(payload))
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
