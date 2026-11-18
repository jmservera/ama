"""Exercise-scenario safety and resident consent gate verification tests (Refs #81).

Proves the two exercise-scenario acceptance criteria of #81 across JSON Store,
SQLite SqlStore, tests/dataset.DATA, and every synthetic exercise suite:
1. No controlled progression with unresolved safety evidence in the exercise scenarios.
2. No work started without valid resident agreement or authorised exception in the
   exercise scenarios.
"""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from zava_forward.core import gates, taskqueues
from zava_forward.core.resident_decisions import (
    RESIDENT_FIELDS,
    resident_gate,
    validate_authorised_works_exception,
)
from zava_forward.core.safety_consent_exercise_gate import (
    CONSENT_GATE_RULE_ID,
    EXERCISE_QUALIFICATION,
    SAFETY_GATE_RULE_ID,
    verify_exercise_safety_and_consent_gates,
    verify_store_safety_and_consent_invariants,
)
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import GateError, Store

_STORE_CLS: Any = Store
_SQL_STORE_CLS: Any = SqlStore
_RESIDENT_GATE_FN: Any = resident_gate


class SafetyConsentExerciseScenarioTests(unittest.TestCase):
    def _make_dataset_store(
        self, *, use_sql: bool = False
    ) -> tuple[tempfile.TemporaryDirectory[str], Any]:
        tmp = tempfile.TemporaryDirectory(prefix="zf-test-81-")
        root = Path(tmp.name)
        data = copy.deepcopy(dataset.DATA)
        dataset.supplied_resident_fixture(data["cases"][2])  # ZF-3 valid scoped acceptance
        seed = root / "seed.json"
        seed.write_text(json.dumps(data), encoding="utf-8")
        if use_sql:
            store = _SQL_STORE_CLS(
                str(seed),
                str(root / "zf.sqlite3"),
                docs_dir=str(root / "docs"),
                digest_dir=str(root / "digests"),
            )
        else:
            store = _STORE_CLS(str(seed), str(root / "live.json"), str(root / "audit.jsonl"))
        return tmp, store

    def test_json_exercise_suites_prove_zero_safety_and_consent_breaches(self) -> None:
        first = verify_exercise_safety_and_consent_gates(as_of="2026-11-15", use_sql=False)
        second = verify_exercise_safety_and_consent_gates(as_of="2026-11-15", use_sql=False)
        self.assertEqual(first, second)
        self.assertTrue(first["passed"], first["violations"])
        self.assertEqual(first["backend"], "json")
        self.assertEqual(first["qualification"], EXERCISE_QUALIFICATION)
        self.assertEqual(
            first["suite_names"],
            [
                "constructed_workbench",
                "resident_preview",
                "sensor_retrofit",
                "scale_matrix",
                "authorised_exception_controls",
                "learning_bundles",
            ],
        )
        self.assertEqual(first["controlled_progressions_with_unresolved_safety"], 0)
        self.assertEqual(first["work_started_without_agreement_or_exception"], 0)
        self.assertGreaterEqual(first["safety_progression_attempts"], 100)
        self.assertEqual(
            first["safety_progression_blocked"],
            first["safety_progression_attempts"],
        )
        self.assertGreaterEqual(first["consent_work_start_attempts"], 85)
        self.assertEqual(
            first["consent_work_start_blocked"],
            first["consent_work_start_attempts"],
        )

    def test_sqlite_exercise_suites_match_json_zero_breach_invariants(self) -> None:
        sql_res = verify_exercise_safety_and_consent_gates(as_of="2026-11-15", use_sql=True)
        self.assertTrue(sql_res["passed"], sql_res["violations"])
        self.assertEqual(sql_res["backend"], "sqlite")
        self.assertEqual(sql_res["controlled_progressions_with_unresolved_safety"], 0)
        self.assertEqual(sql_res["work_started_without_agreement_or_exception"], 0)
        self.assertEqual(
            sql_res["safety_progression_blocked"],
            sql_res["safety_progression_attempts"],
        )
        self.assertEqual(
            sql_res["consent_work_start_blocked"],
            sql_res["consent_work_start_attempts"],
        )

    def test_shared_workbench_dataset_fixture_passes_via_extra_stores(self) -> None:
        tmp, store = self._make_dataset_store(use_sql=False)
        try:
            report = verify_exercise_safety_and_consent_gates(
                as_of="2026-11-15",
                extra_stores=[("tests_dataset_seed", store)],
            )
            self.assertTrue(report["passed"], report["violations"])
            self.assertIn("tests_dataset_seed", report["suite_names"])
        finally:
            tmp.cleanup()

    def test_standalone_safeguarding_and_non_boolean_released_fail_closed(self) -> None:
        # Minimal hazard-only and note-only canary shapes stay compatible.
        minimal_clear = {"funding_ok": True, "hazards": [{"released": True}], "owner": "Sam"}
        canary_note = {
            "funding_ok": True,
            "hazards": [],
            "safeguarding": {"note": "canary"},
            "owner": "Sam",
        }
        for clear_case in (minimal_clear, canary_note):
            verdicts = {g.gate: g for g in gates.booking_gates(clear_case, [], on="2026-11-15")}
            self.assertTrue(verdicts["safety"].passed)
            self.assertEqual(_STORE_CLS._open_safety_items(clear_case), [])
            self.assertFalse(taskqueues.has_open_safety(clear_case))

        bad_shapes = (
            {
                "funding_ok": True,
                "hazards": [{"category": "Damp", "released": "false"}],
                "owner": "Sam",
            },
            {"funding_ok": True, "hazards": [{"category": "Damp", "released": 1}], "owner": "Sam"},
            {
                "funding_ok": True,
                "hazards": [],
                "safeguarding_items": [
                    {"id": "SG-1", "category": "Safeguarding", "released": False}
                ],
                "owner": "Sam",
            },
            {
                "funding_ok": True,
                "hazards": [],
                "safeguarding": {"id": "SG-LEG", "status": "Open"},
                "owner": "Sam",
            },
            {"funding_ok": True, "hazards": [], "safeguarding_items": "corrupt", "owner": "Sam"},
            {"funding_ok": True, "hazards": None, "owner": "Sam"},
        )
        for unsafe_case in bad_shapes:
            verdicts = {g.gate: g for g in gates.booking_gates(unsafe_case, [], on="2026-11-15")}
            self.assertFalse(verdicts["safety"].passed, unsafe_case)
            self.assertTrue(bool(_STORE_CLS._open_safety_items(unsafe_case)), unsafe_case)
            self.assertTrue(taskqueues.has_open_safety(unsafe_case), unsafe_case)

    def test_standalone_safeguarding_blocks_runtime_advance_on_json_and_sqlite(self) -> None:
        for use_sql in (False, True):
            tmp, store = self._make_dataset_store(use_sql=use_sql)
            try:
                pam = (
                    store.staff["pam@example.test"]
                    if "pam@example.test" in store.staff
                    else dict(
                        code="PM-01",
                        name="Pam Lead",
                        email="pam@example.test",
                        role="Retrofit Programme Manager",
                    )
                )
                with store.lock:
                    store.staff["pam@example.test"] = pam
                    if hasattr(store, "db"):
                        store.db.execute(
                            "INSERT OR REPLACE INTO staff (email, body) VALUES (?, ?)",
                            (pam["email"], json.dumps(pam)),
                        )
                    zf3 = store._case("ZF-3")
                    zf3["safeguarding_items"] = [
                        dict(
                            id="SG-81-TEST",
                            category="Safeguarding",
                            priority="Urgent",
                            aware_at="2026-11-10T09:00:00Z",
                            released=False,
                            status="Open",
                            owner="Bea Safe",
                        )
                    ]
                    store.save()
                with self.assertRaisesRegex(GateError, "stopped for safety review"):
                    store.advance(pam, "ZF-3")
                self.assertEqual(store.detail("ZF-3")["stage"], "Final checks before ordering")
            finally:
                db = getattr(store, "db", None)
                if db is not None:
                    db.close()
                tmp.cleanup()

    def test_authorised_works_exception_enforces_human_role_notification_and_retention(
        self,
    ) -> None:
        case = copy.deepcopy(dataset.DATA["cases"][1])  # ZF-2 Waiting
        dataset.supplied_resident_fixture(case)
        case["measure_decisions"] = {}
        case["decision"] = {"status": "Waiting", "by": None, "at": None}
        ctx = case["resident_scopes"]["Loft insulation"][-1]
        base_exc = dict(
            reference="EXC-TEST-81",
            status="Authorised",
            measure="Loft insulation",
            context_revision=ctx["revision"],
            design_version=ctx["design_version"],
            rule_source="Tenancy urgent fabric clause 14.2 (synthetic test)",
            reason="Urgent winter weather-tightness protection",
            approved_by="Bea Safe",
            approved_by_role="Building Safety Liaison",
            effective_date="2026-01-01",
            review_date="2027-01-01",
            expires_at="2027-01-01T00:00:00+00:00",
            resident_notified=True,
            notification_ref="NOTIF-81",
        )
        case["authorised_works_exceptions"] = {"Loft insulation": [dict(base_exc)]}
        verdict = validate_authorised_works_exception(
            case,
            "Loft insulation",
            ctx,
            now="2026-11-15T12:00:00+00:00",
        )
        self.assertTrue(verdict["permitted"], verdict["reason"])
        self.assertEqual(_RESIDENT_GATE_FN(case, now="2026-11-15T12:00:00+00:00"), [])

        # Automated approver, unnotified resident, memory citation, and review hold fail closed.
        for bad_override in (
            dict(approved_by="Copilot Agent"),
            dict(approved_by_role="Contractor"),
            dict(resident_notified=False),
            dict(rule_source="CM-abcdef012345"),
            dict(expires_at="2026-11-14T00:00:00+00:00"),
        ):
            bad_case = copy.deepcopy(case)
            bad_case["authorised_works_exceptions"]["Loft insulation"] = [
                dict(base_exc, **bad_override)
            ]
            self.assertNotEqual(
                _RESIDENT_GATE_FN(bad_case, now="2026-11-15T12:00:00+00:00"),
                [],
                bad_override,
            )

        review_hold_case = copy.deepcopy(case)
        review_hold_case["resident_reviews"] = {
            "Loft insulation": dict(status="Needs human review")
        }
        self.assertNotEqual(
            _RESIDENT_GATE_FN(review_hold_case, now="2026-11-15T12:00:00+00:00"),
            [],
        )

        # Retention purge clears authorised_works_exceptions alongside other RESIDENT_FIELDS.
        self.assertIn("authorised_works_exceptions", RESIDENT_FIELDS)
        tmp, store = self._make_dataset_store(use_sql=False)
        try:
            pam = dict(
                code="PM-01",
                name="Pam Lead",
                email="pam@example.test",
                role="Retrofit Programme Manager",
            )
            with store.lock:
                store.staff["pam@example.test"] = pam
                zf2 = store._case("ZF-2")
                zf2["resident"]["first_contact_at"] = "2018-01-01"
                zf2["authorised_works_exceptions"] = {"Loft insulation": [dict(base_exc)]}
                store.save()
            store.delete_resident_records(pam, "ZF-2", today="2026-11-15")
            self.assertNotIn("authorised_works_exceptions", store._case("ZF-2"))
        finally:
            tmp.cleanup()

    def test_store_invariant_verifier_detects_tampered_unsafe_or_unconsented_work_orders(
        self,
    ) -> None:
        tmp, store = self._make_dataset_store(use_sql=False)
        try:
            with store.lock:
                # Inject forged work orders on ZF-4 (open hazard) and ZF-2 (Waiting consent).
                store.data["procurement"] = dict(
                    packages=[],
                    work_orders=[
                        dict(
                            id="WO-TAMPER-SAFETY",
                            package="PKG-1",
                            case_id="ZF-4",
                            contractor="Test Ltd",
                            state="Appointed",
                            versions=[
                                dict(
                                    version=1,
                                    scope="SYN",
                                    scope_version=1,
                                    resident_bindings=[
                                        dict(measure="Loft insulation", context_revision=1)
                                    ],
                                )
                            ],
                        ),
                        dict(
                            id="WO-TAMPER-CONSENT",
                            package="PKG-1",
                            case_id="ZF-2",
                            contractor="Test Ltd",
                            state="Issued",
                            versions=[dict(version=1, scope="SYN", scope_version=1)],
                        ),
                    ],
                )
            res = verify_store_safety_and_consent_invariants(
                store,
                suite_name="tampered_probe",
                as_of="2026-11-15",
            )
            self.assertFalse(res["passed"])
            self.assertGreaterEqual(res["controlled_progressions_with_unresolved_safety"], 1)
            self.assertGreaterEqual(res["work_started_without_agreement_or_exception"], 1)
            rules_flagged = {v["rule_id"] for v in res["violations"]}
            self.assertIn(SAFETY_GATE_RULE_ID, rules_flagged)
            self.assertIn(CONSENT_GATE_RULE_ID, rules_flagged)
        finally:
            tmp.cleanup()

    def test_invalid_as_of_fails_closed(self) -> None:
        for bad_as_of in ("", "2026/11/15", "not-a-date"):
            with self.assertRaises(ValueError):
                verify_exercise_safety_and_consent_gates(as_of=bad_as_of)


if __name__ == "__main__":
    unittest.main()
