"""End-to-end non-retaliation, non-refusal and zero-hazard-delay tests for Issue #220 Criterion 5.

Verifies across ChallengeRegister, JSON Store, SQLite SqlStore (priority, ai_task and form_staging
targets, plus nomination and service dispute routes) and SQLite Assistants proposals that raising,
updating, reopening, escalating or resolving a challenge across resident digital, staff-recorded
non-digital and representative/nominee channels never lowers case priority or ranking score, never
sets or infers refusal/no-access/sanction/withdrawn/negative-engagement flags, never closes
unrelated work items, never pauses or delays statutory/emergency hazard or safeguarding clocks,
immediately routes independent hazard intake without waiting for challenge review, and emits the
machine-checkable non_retaliation_assurance / hazard_clock_preserved contract.
"""

from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset as _dataset
import release_support as _release_support
from zava_forward.core import ai_tasks as _ai_tasks
from zava_forward.core import ranking as _ranking_mod
from zava_forward.core import resident_decisions as _rd_mod
from zava_forward.core.assistants import (
    WITHHELD_NOTE,
)
from zava_forward.core.assistants import (
    Assistants as _Assistants,
)
from zava_forward.core.assistants import (
    canonical as _canonical,
)
from zava_forward.core.challenges import (
    FORBIDDEN_ADVERSE_FIELDS,
    NON_DIGITAL_CHANNELS,
    NOT_INFERRED,
    SAFEGUARDS,
    SUBMITTER_KINDS,
    ChallengeRegister,
    ChallengeSafeguardError,
    Node,
    assert_no_adverse_challenge_effects,
    build_non_retaliation_assurance,
    reject_adverse_mapping,
)
from zava_forward.core.sqlstore import SqlStore as _SqlStore
from zava_forward.core.store import ConflictError
from zava_forward.core.store import Store as _Store

DATA: dict[str, Any] = _dataset.DATA
STORE_CLS: Any = _Store
SQL_STORE_CLS: Any = _SqlStore
ASSISTANTS_CLS: Any = _Assistants
CANONICAL: Any = _canonical
RELEASE_SUPPORT: Any = _release_support
AI_TASKS: Any = _ai_tasks
RANKING: Any = _ranking_mod
RD: Any = _rd_mod


def _node(kind: str, item_id: str, version: str = "v1") -> Node:
    return (kind, item_id, version)


def _assert_assurance_contract(
    test: unittest.TestCase,
    assurance: dict[str, Any],
    *,
    flagged: bool,
    routed: bool,
) -> None:
    expected = build_non_retaliation_assurance(
        hazard_concern=flagged,
        independent_hazard_routed=routed,
    )
    test.assertEqual(assurance, expected)
    test.assertTrue(assurance["priority_preserved"])
    test.assertFalse(assurance["ranking_score_lowered"])
    test.assertFalse(assurance["refusal_inferred"])
    test.assertFalse(assurance["no_access_inferred"])
    test.assertFalse(assurance["sanction_applied"])
    test.assertFalse(assurance["withdrawn_inferred"])
    test.assertFalse(assurance["negative_engagement_inferred"])
    test.assertFalse(assurance["unrelated_work_items_closed"])
    test.assertTrue(assurance["hazard_clock_preserved"])
    test.assertTrue(assurance["awaabs_law_clocks_preserved"])
    test.assertTrue(assurance["safeguarding_clocks_preserved"])
    test.assertTrue(assurance["awaiting_hazard_action_preserved"])
    test.assertFalse(assurance["waits_for_challenge_review"])
    test.assertEqual(assurance["hazard_concern_flagged"], flagged)
    test.assertEqual(assurance["independent_hazard_intake_routed"], routed)


def _seed_case_clocks_and_open_work(case: dict[str, Any]) -> None:
    case["score"] = 94
    case["urgent"] = True
    case["awaiting_hazard_action"] = True
    case["hazards"] = [
        {
            "category": "Electrical",
            "priority": "Emergency",
            "noticed": "2026-01-14",
            "aware_at": "2026-01-14T08:00:00Z",
            "investigation_due_at": "2026-01-15T08:00:00Z",
            "make_safe_due_at": "2026-01-15T08:00:00Z",
            "source": "SYN baseline 24h emergency report",
            "recorded_at": "2026-01-14T08:05:00Z",
            "referred": None,
            "repaired": None,
            "released": False,
            "job": "",
            "owner": "Sam Officer",
            "note": "SYN Awaabs Law 24h emergency clock active",
            "hold": {
                "scope": "Home",
                "case_id": case["id"],
                "status": "Active",
                "accountable_role": "Building Safety Liaison",
                "decision": None,
            },
        },
        {
            "category": "Damp and mould",
            "priority": "Significant",
            "noticed": "2026-01-10",
            "aware_at": "2026-01-10T10:00:00Z",
            "investigation_due_at": "2026-01-24T10:00:00Z",
            "written_summary_due_at": "2026-01-27T10:00:00Z",
            "safety_works_due_at": "2026-02-01T10:00:00Z",
            "source": "SYN baseline 7d/14d significant damp report",
            "recorded_at": "2026-01-10T10:15:00Z",
            "referred": "2026-01-10",
            "repaired": None,
            "released": False,
            "job": "SYN-HAZ-14D",
            "owner": "Sam Officer",
            "note": "SYN Awaabs Law 14d investigation and 7d make-safe clock active",
            "hold": {
                "scope": "Home",
                "case_id": case["id"],
                "status": "Active",
                "accountable_role": "Building Safety Liaison",
                "decision": None,
            },
        },
    ]
    case["safeguarding"] = [
        {
            "id": "SG-1",
            "status": "Open",
            "raised_at": "2026-11-12T09:00:00Z",
            "due_by": "2026-11-16T09:00:00Z",
            "escalate_by": "2026-11-17T09:00:00Z",
            "paused": False,
        }
    ]
    case["tasks"] = [
        {"id": "TSK-1", "title": "SYN book independent survey", "done": False, "status": "Open"}
    ]
    case["returns"] = [{"id": "RET-1", "status": "Open"}]
    case["service_requests"] = [
        {
            "id": "SR-1",
            "kind": "Repair query",
            "status": "Open",
            "closed": False,
            "route": "Standard",
            "channel": "Phone",
            "summary": "SYN existing heating repair request",
            "source": "SYN-SR-1",
            "owner": {
                "email": "sam@example.test",
                "name": "Sam Officer",
                "role": "Resident Liaison Officer",
                "code": "RLO-1",
            },
            "next_update": "2026-11-20",
            "version": 1,
            "remedy": {
                "status": "Open",
                "owner": None,
                "at": None,
                "opened_at": "2026-11-12T10:00:00Z",
                "version": 1,
                "history": [],
            },
        }
    ]
    case["work_orders"] = [{"id": "WO-1", "status": "Issued", "closed": False}]
    case["packages"] = [{"id": "PKG-1", "status": "In progress", "closed": False}]
    case["handoff"] = {"state": "Offered", "to_code": "RLO-1", "note": "SYN active handoff"}
    case["resident_update"] = {
        "status": "Open",
        "version": 1,
        "purpose": "SYN scheduled resident update",
        "basis": "SYN consent",
        "safe_contact_ref": "SYN-SAFE-1",
        "owner_identity": None,
        "at": "2026-11-12T10:00:00Z",
        "opened_at": "2026-11-12T10:00:00Z",
    }
    case["representative_authorities"] = {
        "SYN-NOMINEE-FORM-1": [
            {
                "version": 1,
                "representative_ref": "SYN-NOMINEE-FORM-1",
                "status": "Confirmed",
            }
        ]
    }
    case["form_staging"] = [
        {
            "id": "BATCH-220-1",
            "case_id": case["id"],
            "schema_id": "pas2035-occupancy",
            "schema_version": "1.0",
            "schema_digest": "sha256:syn-schema-220",
            "source": {
                "id": "DOC-OCC-1",
                "kind": "Survey",
                "version": 1,
                "content_sha256": "synsha256doc1",
            },
            "processing": {
                "mode": "ai",
                "model": "syn-form-model-v1",
                "prompt_version": "form-extract-v1",
            },
            "verification": None,
            "candidates": [
                {
                    "id": "CAND-1",
                    "field_id": "occupants",
                    "raw_value": "2",
                    "locator": {"page": 1},
                }
            ],
        }
    ]
    case["form_reviews"] = [
        {
            "id": "DRAFT-220-1",
            "version": 1,
            "schema_digest": "sha256:syn-schema-220",
            "status": "Unapproved working notes",
            "fields": {
                "occupants": {
                    "value": "2",
                    "state": "Accepted",
                    "evidence": {
                        "batch_id": "BATCH-220-1",
                        "candidate_id": "CAND-1",
                    },
                }
            },
            "recorded_by": "pam@example.test",
            "recorded_at": "2026-10-01T11:30:00+00:00",
        }
    ]


class LocalAssistantProvider:
    configured = True
    sends_no_bytes = True
    provider = "local-test-double"
    endpoint = "local-test"
    fast = "test"

    def evidence(self, system: str, prompt: str, max_tokens: int, timeout: float) -> dict[str, Any]:
        del system, max_tokens, timeout
        payload = json.loads(prompt)["evidence"]
        citations = ["source:home"]
        sensors = ((payload.get("sources") or {}).get("sensors") or {}).get("citation_keys") or []
        if sensors:
            citations.append(sensors[0])
        out = {
            "summary": "SYN check supplied evidence with the responsible officer.",
            "findings": [
                {
                    "text": "SYN supplied home facts require human verification.",
                    "citations": citations,
                }
            ],
            "unknowns": [],
        }
        return {
            "text": str(CANONICAL(out)),
            "provider": "local-test-double",
            "deployment": "test",
            "model": "test-model",
            "source": "ai",
            "outcome": "returned",
            "usage": {"prompt_tokens": 80, "completion_tokens": 25, "total_tokens": 105},
        }


class ChallengeRegisterNoRetaliationTests(unittest.TestCase):
    def test_adverse_keys_are_rejected_despite_case_spacing_and_hyphen_variants(self) -> None:
        for variant in (
            "Retaliation_Flag",
            " refusal",
            "hazard-pause",
            "HAZARD_PAUSE",
            "priority penalty",
        ):
            with self.subTest(variant=variant):
                with self.assertRaises(ChallengeSafeguardError):
                    reject_adverse_mapping({variant: True})
        base: dict[str, Any] = {"id": "ZF-220-KEY", "score": 50}
        after = {**base, "Hazard-Delay": True}
        with self.assertRaises(ChallengeSafeguardError):
            assert_no_adverse_challenge_effects(base, after)
        reject_adverse_mapping({"summary": "ok", "route": "phone"})

    def test_every_forbidden_adverse_key_is_refused_at_every_depth(self) -> None:
        src = _node("source", "SRC-220", "v1")
        prop = _node("proposal", "PROP-220", "v1")
        dec = _node("human_decision", "DEC-220", "d1")
        for key in sorted(FORBIDDEN_ADVERSE_FIELDS):
            with self.subTest(key=key):
                with self.assertRaisesRegex(ChallengeSafeguardError, key):
                    reject_adverse_mapping({key: True})
                reg = ChallengeRegister({prop: [src], dec: [prop]})
                with self.assertRaisesRegex(ChallengeSafeguardError, key):
                    reg.record_digital(
                        {"kind": "source", "id": "SRC-220", "version": "v1"},
                        "DEC-220#d1",
                        "SYN challenge statement.",
                        "Sam Officer",
                        "2026-11-20",
                        explanations=[{"kind": "policy", "text": "SYN policy reason.", key: True}],
                    )
                self.assertEqual(reg.challenges, {})
                base: dict[str, Any] = {"id": "ZF-220-KEY", "score": 50}
                with self.assertRaises(ChallengeSafeguardError):
                    assert_no_adverse_challenge_effects(base, {**base, key: True})

    def test_register_reopen_representative_channels_and_assurance_contract(self) -> None:
        self.assertIn("trusted_intermediary", NON_DIGITAL_CHANNELS)
        self.assertEqual(SUBMITTER_KINDS, ("resident", "representative", "nominee", "third_party"))
        self.assertIn("withdrawn", NOT_INFERRED)
        self.assertIn("negative_engagement", FORBIDDEN_ADVERSE_FIELDS)

        src = _node("source", "SRC-220", "v1")
        prop = _node("proposal", "PROP-220", "v1")
        dec = _node("human_decision", "DEC-220", "d1")
        reg = ChallengeRegister({prop: [src], dec: [prop]})

        rec = reg.record_representative(
            "SYN-NOMINEE-FORM-1",
            {"kind": "source", "id": "SRC-220", "version": "v1"},
            "DEC-220#d1",
            "SYN nominee reports household size is 4, not 2, with damp smell.",
            "Sam Officer",
            "2026-11-20",
            submitted_by="nominee",
            route="staff_recorded",
            recorded_by="Sam Officer",
            channel="trusted_intermediary",
            hazard_concern=True,
            received_on="2026-11-15",
        )
        self.assertEqual(rec["submitted_by"], "nominee")
        self.assertEqual(rec["representative_ref"], "SYN-NOMINEE-FORM-1")
        self.assertEqual(rec["channel"], "trusted_intermediary")
        self.assertTrue(rec["hazard_clock_preserved"])
        self.assertEqual(
            rec["hazard_referral"],
            {
                "to": "Sam Officer",
                "status": "referred_on_receipt",
                "received_on": "2026-11-15",
                "independent_intake": True,
                "waits_for_challenge_review": False,
                "hazard_clock_preserved": True,
            },
        )
        _assert_assurance_contract(
            self, rec["non_retaliation_assurance"], flagged=True, routed=True
        )

        # Resolve as corrected -> marks transitive dependents PROP-220 and DEC-220 stale.
        resolved = reg.resolve(
            rec["id"],
            "Sam Officer",
            "corrected",
            "SYN verified household occupancy is 4.",
        )
        self.assertEqual(resolved["status"], "corrected")
        self.assertIn(prop, reg.stale)
        self.assertIn(dec, reg.stale)

        # Reopen with supplementary representative evidence on a later date:
        # prior correction staleness and original hazard_referral received_on stay intact.
        reopened = reg.reopen(
            rec["id"],
            "SYN representative supplied updated tenancy schedule.",
            "Rae Reviewer",
            "2026-11-22",
            route="staff_recorded",
            recorded_by="Rae Reviewer",
            channel="assisted_visit",
            submitted_by="representative",
            representative_ref="SYN-SOLICITOR-REF-9",
            hazard_concern=True,
            received_on="2026-11-18",
        )
        self.assertEqual(reopened["status"], "reopened")
        self.assertIsNone(reopened["resolution"])
        self.assertTrue(reopened["prior_correction_preserved"])
        self.assertEqual(len(reopened["previous_resolutions"]), 1)
        self.assertEqual(reopened["previous_resolutions"][0]["outcome"], "corrected")
        self.assertEqual(reopened["hazard_referral"]["received_on"], "2026-11-15")
        self.assertEqual(reopened["hazard_referral"]["to"], "Rae Reviewer")
        self.assertIn(prop, reg.stale)
        self.assertIn(dec, reg.stale)
        self.assertEqual(reopened["reopens"][0]["submitted_by"], "representative")
        self.assertEqual(reopened["reopens"][0]["representative_ref"], "SYN-SOLICITOR-REF-9")
        view = reg.view(rec["id"])
        self.assertTrue(view["hazard_clock_preserved"])
        _assert_assurance_contract(
            self, view["non_retaliation_assurance"], flagged=True, routed=True
        )

    def test_safeguard_verifier_fails_closed_on_every_adverse_mutation_class(self) -> None:
        base: dict[str, Any] = {"id": "ZF-220", "closed": False, "resident": {"support": "Yes"}}
        _seed_case_clocks_and_open_work(base)
        base["decision"] = {"status": "Asked", "by": None, "at": None}
        base["measure_decisions"] = {"Loft insulation": {"status": "Agreed"}}
        base["funding"] = {"route": "SHDF", "ok": True}

        clean_after = copy.deepcopy(base)
        clean_after["affected_challenges"] = [
            {
                "id": "CH-1",
                "safeguards": dict(SAFEGUARDS),
                "hazard_clock_preserved": True,
                "non_retaliation_assurance": build_non_retaliation_assurance(),
            }
        ]
        assert_no_adverse_challenge_effects(base, clean_after)

        mutations: list[tuple[str, Any]] = [
            ("lowered_score", lambda c: c.__setitem__("score", 90)),
            ("cleared_urgent", lambda c: c.__setitem__("urgent", False)),
            ("case_closed", lambda c: c.__setitem__("closed", True)),
            ("awaiting_hazard_cleared", lambda c: c.__setitem__("awaiting_hazard_action", False)),
            ("refusal_key", lambda c: c.__setitem__("refusal", True)),
            ("no_access_nested", lambda c: c["resident"].__setitem__("no_access_count", 1)),
            ("sanction_nested", lambda c: c.__setitem__("sanction_flag", "warned")),
            ("withdrawn_flag", lambda c: c.__setitem__("withdrawn_flag", True)),
            ("negative_engagement", lambda c: c.__setitem__("negative_engagement", True)),
            ("decision_changed", lambda c: c["decision"].__setitem__("status", "Declined")),
            (
                "measure_decision_changed",
                lambda c: c["measure_decisions"]["Loft insulation"].__setitem__(
                    "status", "Declined"
                ),
            ),
            ("task_closed", lambda c: c["tasks"][0].__setitem__("done", True)),
            ("task_deleted", lambda c: c["tasks"].clear()),
            ("return_closed", lambda c: c["returns"][0].__setitem__("status", "Closed")),
            (
                "service_request_closed",
                lambda c: c["service_requests"][0].__setitem__("status", "Closed"),
            ),
            (
                "work_order_cancelled",
                lambda c: c["work_orders"][0].__setitem__("status", "Cancelled"),
            ),
            ("package_closed", lambda c: c["packages"][0].__setitem__("closed", True)),
            ("handoff_closed", lambda c: c["handoff"].__setitem__("state", "Closed")),
            (
                "resident_update_closed",
                lambda c: c["resident_update"].__setitem__("status", "Closed"),
            ),
            (
                "emergency_24h_clock_delayed",
                lambda c: c["hazards"][0].__setitem__("make_safe_due_at", "2026-11-16T08:00:00Z"),
            ),
            (
                "significant_14d_clock_reset",
                lambda c: c["hazards"][1].__setitem__("aware_at", "2026-11-15T10:00:00Z"),
            ),
            (
                "hazard_hold_weakened",
                lambda c: c["hazards"][0]["hold"].__setitem__("status", "Released"),
            ),
            (
                "safeguarding_due_delayed",
                lambda c: c["safeguarding"][0].__setitem__("due_by", "2026-11-25T09:00:00Z"),
            ),
            (
                "safeguarding_paused",
                lambda c: c["safeguarding"][0].__setitem__("paused", True),
            ),
        ]
        for label, mutate in mutations:
            with self.subTest(mutation=label):
                tampered = copy.deepcopy(clean_after)
                mutate(tampered)
                with self.assertRaises(ChallengeSafeguardError):
                    assert_no_adverse_challenge_effects(base, tampered)


class StoreAndSqlStoreNoRetaliationLifecycleTests(unittest.TestCase):
    def _build_fixture(self, sql: bool) -> tuple[Any, tempfile.TemporaryDirectory[str]]:
        tmp = tempfile.TemporaryDirectory()
        seed_path = Path(tmp.name) / "seed.json"
        data = copy.deepcopy(DATA)
        data["staff"].append(
            {
                "code": "RLO-2",
                "name": "Rae Reviewer",
                "email": "rae@example.test",
                "role": "Resident Liaison Officer",
            }
        )
        for c in data["cases"]:
            if c["id"] == "ZF-1":
                _seed_case_clocks_and_open_work(c)
        seed_path.write_text(json.dumps(data))
        if sql:
            store = SQL_STORE_CLS(str(seed_path), str(seed_path.with_suffix(".sqlite")))
        else:
            store = STORE_CLS(str(seed_path))
        RELEASE_SUPPORT.install(store)
        return store, tmp

    def _verify_store_backend(self, sql: bool) -> None:
        store, tmp = self._build_fixture(sql=sql)
        try:
            if sql:
                self.addCleanup(store.db.close)
            sam = store.staff["sam@example.test"]
            rae = store.staff["rae@example.test"]
            pam = store.staff["pam@example.test"]

            # Generate priority + ai_task message suggestions; form_staging is already on ZF-1.
            prio_rec = store.ai_priority(sam, n=5, mode="workflow-only")
            msg_rec = store.ai_run(sam, "ZF-1", "message", mode="workflow-only")
            msg_id = str(msg_rec["record_id"])

            detail0 = store.detail("ZF-1", sam)
            targets_by_id = {t["proposal_id"]: t for t in detail0["challenge_targets"]}
            self.assertIn(prio_rec["id"], targets_by_id)
            self.assertIn(msg_id, targets_by_id)
            self.assertIn("form:BATCH-220-1", targets_by_id)
            for t in targets_by_id.values():
                self.assertTrue(t["hazard_clock_preserved"])
                _assert_assurance_contract(
                    self, t["non_retaliation_assurance"], flagged=False, routed=False
                )

            store._ranks = None
            baseline_ranking = copy.deepcopy(store._ranking())
            baseline_case = copy.deepcopy(store._case("ZF-1"))

            # 1. Exercise all 6 channels + 3 submitter roles across priority, ai_task & form!
            matrix = [
                ("Digital", "The resident", None, prio_rec["id"], "proposal"),
                ("Phone", "Their representative", "SYN-SOLICITOR-1", prio_rec["id"], "source"),
                ("Letter", "Nominee", "SYN-NOMINEE-FORM-1", msg_id, "proposal"),
                ("In person", "The resident", None, "form:BATCH-220-1", "source"),
                ("Assisted visit", "Their representative", "REP-AUTH-1", msg_id, "source"),
                ("Trusted intermediary", "Nominee", "SYN-ADVOCATE-7", "form:BATCH-220-1", "policy"),
            ]
            opened_ids: list[str] = []
            for idx, (channel, sub_by, rep_ref, prop_id, t_kind) in enumerate(matrix, 1):
                target = targets_by_id[prop_id]
                payload: dict[str, Any] = {
                    "action": "challenge_open",
                    "proposal_id": prop_id,
                    "proposal_version": target["proposal_version"],
                    "decision_version": target["decision_version"],
                    "target_kind": t_kind,
                    "channel": channel,
                    "submitted_by": sub_by,
                    "source": f"SYN-SRC-{idx}",
                    "request": f"SYN request {idx} via {channel}",
                    "explanation": f"SYN explanation {idx}",
                    "owner": "sam@example.test",
                    "non_digital_route": "SYN Phone Sam or visit the housing office.",
                    "next_update": "2099-01-10",
                }
                if rep_ref is not None:
                    payload["representative_ref"] = rep_ref
                store.resident_action(sam, "ZF-1", payload)
                opened_ids.append(f"CH-{idx}")

            # Verify verified vs unverified representative status without consent inference.
            stored_challenges = store._case("ZF-1")["affected_challenges"]
            self.assertEqual(len(stored_challenges), 6)
            self.assertIn(
                "Verified representative authority",
                stored_challenges[2]["representative_authority_status"],
            )
            self.assertIn(
                "Unverified representative",
                stored_challenges[1]["representative_authority_status"],
            )

            # 2. Update CH-3 (ai_task), escalate to pam, resolve as Correction recorded,
            # confirm ai_tasks.review blocks accept/edit (PC-003), then REOPEN CH-3 and confirm
            # correction staleness and SQLite priority_correction indexing stay active (PC-002)!
            store.resident_action(
                sam,
                "ZF-1",
                {
                    "action": "challenge_update",
                    "id": "CH-3",
                    "expected_version": 1,
                    "channel": "Assisted visit",
                    "submitted_by": "Nominee",
                    "representative_ref": "SYN-NOMINEE-FORM-1",
                    "source": "SYN-UPD-3",
                    "request": "SYN nominee added meter photo evidence.",
                    "explanation": "SYN logged supplementary evidence.",
                    "next_update": "2099-01-12",
                },
            )
            store.resident_action(
                sam,
                "ZF-1",
                {
                    "action": "challenge_escalate",
                    "id": "CH-3",
                    "expected_version": 2,
                    "owner": "pam@example.test",
                    "reason": "SYN programme manager review requested by nominee.",
                    "next_update": "2099-01-14",
                },
            )
            store.resident_action(
                pam,
                "ZF-1",
                {
                    "action": "challenge_resolve",
                    "id": "CH-3",
                    "expected_version": 3,
                    "resolution": "Correction recorded",
                    "resolution_ref": "SYN-CORR-3",
                    "explanation": "SYN message draft used outdated household record.",
                    "next_update": "2099-01-15",
                },
            )
            with self.assertRaises(PermissionError):
                AI_TASKS.review(store, sam, msg_id, "accept")

            # Reopen CH-3 -> prior correction must remain preserved across memory and SQLite index!
            store.resident_action(
                pam,
                "ZF-1",
                {
                    "action": "challenge_reopen",
                    "id": "CH-3",
                    "expected_version": 4,
                    "channel": "Trusted intermediary",
                    "submitted_by": "Nominee",
                    "representative_ref": "SYN-NOMINEE-FORM-1",
                    "source": "SYN-REOPEN-3",
                    "request": "SYN nominee requested additional wording check.",
                    "explanation": "SYN reopened while keeping prior correction active.",
                    "owner": "rae@example.test",
                    "next_update": "2099-01-18",
                },
            )
            ch3 = next(r for r in store._case("ZF-1")["affected_challenges"] if r["id"] == "CH-3")
            self.assertEqual(ch3["status"], "Reopened")
            self.assertTrue(ch3["prior_correction_preserved"])
            self.assertEqual(len(ch3["previous_resolutions"]), 1)
            with self.assertRaises(PermissionError):
                AI_TASKS.review(store, sam, msg_id, "accept")
            # Rejecting the stale AI task remains permitted!
            rejected = AI_TASKS.review(
                store, sam, msg_id, "reject", reason="SYN rejected after correction"
            )
            self.assertEqual(rejected["status"], "Rejected")

            # Resolve CH-4 (form:BATCH-220-1) as Correction recorded and check target staleness.
            store.resident_action(
                sam,
                "ZF-1",
                {
                    "action": "challenge_resolve",
                    "id": "CH-4",
                    "expected_version": 1,
                    "resolution": "Correction recorded",
                    "resolution_ref": "SYN-FORM-CORR-4",
                    "explanation": "SYN occupancy extraction was stale.",
                    "next_update": "2099-01-16",
                },
            )
            detail_mid = store.detail("ZF-1", sam)
            mid_targets = {t["proposal_id"]: t for t in detail_mid["challenge_targets"]}
            self.assertTrue(mid_targets[msg_id]["stale"])
            self.assertTrue(mid_targets["form:BATCH-220-1"]["stale"])

            # Verify zero drift on non-challenge case fields & portfolio ranking so far!
            after_non_hazard = copy.deepcopy(store._case("ZF-1"))
            after_non_hazard.pop("affected_challenges", None)
            baseline_without_challenges = copy.deepcopy(baseline_case)
            baseline_without_challenges.pop("affected_challenges", None)
            self.assertEqual(after_non_hazard, baseline_without_challenges)
            store._ranks = None
            self.assertEqual(store._ranking(), baseline_ranking)

            # 3. Also exercise nomination_record -> nomination_correct -> nomination_review
            # and verify that existing clocks/tasks/priority stay 100% preserved!
            store.resident_action(
                sam,
                "ZF-1",
                {
                    "action": "nomination_record",
                    "case_id": "ZF-1",
                    "kind": "Self-referral",
                    "reported_subject_ref": "SYN-NOM-SUBJ-1",
                    "account": "SYN household asked for retrofit consideration.",
                    "source": "SYN-NOM-SRC-1",
                    "channel": "Phone",
                    "owner": "sam@example.test",
                    "acknowledgement_ref": "SYN-NOM-ACK-1",
                    "next_update": "2099-01-20",
                    "non_digital_route": "SYN Phone Sam.",
                    "hazard_concern": False,
                },
            )
            nom_id = str(store._case("ZF-1")["nomination_records"][-1]["id"])
            store.resident_action(
                sam,
                "ZF-1",
                {
                    "action": "nomination_correct",
                    "case_id": "ZF-1",
                    "id": nom_id,
                    "expected_version": 1,
                    "reported_subject_ref": "SYN-NOM-SUBJ-1",
                    "account": "SYN corrected floor level detail.",
                    "source": "SYN-NOM-SRC-2",
                    "channel": "In person",
                    "next_update": "2099-01-22",
                    "challenge_id": "CH-1",
                },
            )
            store.resident_action(
                rae,
                "ZF-1",
                {
                    "action": "nomination_review",
                    "case_id": "ZF-1",
                    "id": nom_id,
                    "expected_version": 2,
                    "outcome": "More evidence needed",
                    "rationale": "SYN awaits next programme check; challenge route preserved.",
                    "evidence_ref": "SYN-NOM-REV-1",
                    "next_update": "2099-01-25",
                },
            )

            # 4. Challenge mentioning a hazard concern with immediate independent hazard_intake!
            safety_audit_before = [
                e
                for e in store.audit_entries()
                if e.get("action") in ("safety_raised", "safety_emergency")
            ]
            prio_target = mid_targets[prio_rec["id"]]
            store.resident_action(
                sam,
                "ZF-1",
                {
                    "action": "challenge_open",
                    "proposal_id": prio_rec["id"],
                    "proposal_version": prio_target["proposal_version"],
                    "decision_version": prio_target["decision_version"],
                    "target_kind": "proposal",
                    "channel": "Phone",
                    "submitted_by": "Their representative",
                    "representative_ref": "SYN-REP-HAZARD-1",
                    "source": "SYN-HAZ-CHAL-SRC",
                    "request": (
                        "SYN challenging score AND reporting active ceiling water near electrics."
                    ),
                    "explanation": (
                        "SYN safety issue routed immediately without waiting for challenge review."
                    ),
                    "owner": "sam@example.test",
                    "non_digital_route": "SYN 24h emergency repair line and named RLO.",
                    "hazard_concern": True,
                    "hazard_intake": {
                        "category": "Electrical",
                        "priority": "Emergency",
                        "source": "SYN representative challenge call",
                        "aware_at": "2026-01-15T11:00:00Z",
                        "note": "SYN immediate make-safe dispatched independently",
                    },
                    "next_update": "2099-01-19",
                },
            )
            final_case = store._case("ZF-1")
            # Original 2 hazards (24h Emergency & 14d Significant) stay byte-for-byte untouched!
            self.assertEqual(len(final_case["hazards"]), 3)
            self.assertEqual(final_case["hazards"][:2], baseline_case["hazards"])
            self.assertEqual(final_case["safeguarding"], baseline_case["safeguarding"])
            self.assertTrue(final_case["awaiting_hazard_action"])
            self.assertEqual(final_case["score"], baseline_case["score"])
            self.assertEqual(final_case["urgent"], baseline_case["urgent"])
            self.assertEqual(final_case["tasks"], baseline_case["tasks"])
            self.assertEqual(final_case["service_requests"], baseline_case["service_requests"])
            self.assertEqual(final_case["work_orders"], baseline_case["work_orders"])
            self.assertEqual(final_case["packages"], baseline_case["packages"])
            self.assertEqual(final_case["handoff"], baseline_case["handoff"])
            self.assertEqual(final_case["resident_update"], baseline_case["resident_update"])

            new_haz = final_case["hazards"][2]
            self.assertEqual(new_haz["priority"], "Emergency")
            self.assertFalse(new_haz["released"])
            self.assertEqual(new_haz["hold"]["status"], "Active")

            ch7 = final_case["affected_challenges"][-1]
            self.assertEqual(ch7["id"], "CH-7")
            self.assertEqual(ch7["hazard_referral"]["status"], "referred_on_receipt")
            self.assertTrue(ch7["hazard_referral"]["independent_intake"])
            self.assertFalse(ch7["hazard_referral"]["waits_for_challenge_review"])
            self.assertEqual(ch7["hazard_referral"]["routed_hazard_index"], 2)
            self.assertTrue(ch7["hazard_clock_preserved"])
            _assert_assurance_contract(
                self, ch7["non_retaliation_assurance"], flagged=True, routed=True
            )

            # Confirm PC-001: 1 safety_raised + 1 safety_emergency added (no SQL replay duplicate).
            safety_audit_after = [
                e
                for e in store.audit_entries()
                if e.get("action") in ("safety_raised", "safety_emergency")
            ]
            added_actions = [e["action"] for e in safety_audit_after[len(safety_audit_before) :]]
            self.assertEqual(added_actions, ["safety_emergency", "safety_raised"])

            challenge_audits = [
                e
                for e in store.audit_entries()
                if str(e.get("action", "")).startswith("resident_challenge_")
            ]
            self.assertGreaterEqual(len(challenge_audits), 11)
            for entry in challenge_audits:
                self.assertIn("non_retaliation_assurance=verified", entry["detail"])
                self.assertIn("hazard_clock_preserved=true", entry["detail"])
            self.assertTrue(store.verify_audit())
        finally:
            tmp.cleanup()


class AssistantsProposalChallengeNoRetaliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="assist-220-test-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.seed = self.root / "seed.json"
        self.dbpath = self.root / "cases.sqlite"
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                {
                    "code": "QI-1",
                    "name": "Quinn Inspector",
                    "email": "quinn@example.test",
                    "role": "Quality Inspector",
                },
                {
                    "code": "RC-1",
                    "name": "Rex Coordinator",
                    "email": "rex@example.test",
                    "role": "Retrofit Coordinator",
                },
            ]
        )
        for c in data["cases"]:
            if c["id"] == "ZF-1":
                _seed_case_clocks_and_open_work(c)
        self.seed.write_text(json.dumps(data))
        self.store = SQL_STORE_CLS(str(self.seed), str(self.dbpath))
        self.addCleanup(self.store.db.close)
        self.store.ai = LocalAssistantProvider()
        cfg = {
            "ZF_ASSIST_AUTHORITY": "local-nonbillable-test-authority",
            "ZF_ASSIST_EXPIRES": "2099-01-01T00:00:00Z",
            "ZF_ASSIST_CALL_ALLOWANCE": "100",
            "ZF_ASSIST_TOKEN_ALLOWANCE": "2000000",
            "ZF_ASSIST_PROACTIVE": "1",
        }
        self.assistants = ASSISTANTS_CLS(self.store, cfg)
        self.addCleanup(self.assistants.stop)
        RELEASE_SUPPORT.install(self.store)
        self.pam = self.store.staff["pam@example.test"]
        self.sam = self.store.staff["sam@example.test"]
        self.rex = self.store.staff["rex@example.test"]

    def test_assistant_proposal_challenge_reopen_staleness_hazard_intake_and_redaction(
        self,
    ) -> None:
        invoked = self.assistants.invoke(self.sam, "works-resident-coordination", "ZF-1")
        tid = invoked["id"]
        self.assertTrue(self.assistants.execute(tid))
        ready = self.assistants.detail(self.sam, tid)
        self.assertEqual(ready["state"], "ready")
        self.assertTrue(ready["actionable"])

        baseline_case = copy.deepcopy(self.store._case("ZF-1"))

        # 1. Open representative challenge mentioning an emergency safety hazard + hazard_intake!
        opened = self.assistants.challenge(
            self.sam,
            tid,
            {
                "action": "open",
                "revision": ready["revision"],
                "target_kind": "proposal",
                "channel": "Trusted intermediary",
                "submitted_by": "Nominee",
                "representative_ref": "SYN-NOMINEE-FORM-1",
                "source": "SYN-ASSIST-CHAL-1",
                "request": (
                    "SYN nominee challenges visit draft and reports live spark at consumer unit."
                ),
                "explanation": (
                    "SYN visit draft held for human review; emergency electrical hazard raised now."
                ),
                "owner": "sam@example.test",
                "non_digital_route": "SYN Phone Sam or the emergency desk.",
                "hazard_concern": True,
                "hazard_intake": {
                    "category": "Electrical",
                    "priority": "Emergency",
                    "source": "SYN nominee intermediary call",
                    "aware_at": "2026-01-15T12:00:00Z",
                    "note": "SYN immediate emergency electrical dispatch",
                },
                "next_update": "2099-02-01",
            },
        )
        self.assertTrue(opened["hazard_clock_preserved"])
        _assert_assurance_contract(
            self, opened["non_retaliation_assurance"], flagged=True, routed=True
        )
        self.assertEqual(len(opened["challenges"]), 1)
        ach = opened["challenges"][0]
        self.assertEqual(ach["id"], "ACH-1")
        self.assertEqual(ach["hazard_referral"]["routed_hazard_index"], 2)

        # Pre-existing 24h & 14d hazard clocks, safeguarding clocks, score, tasks all untouched!
        case_after_open = self.store._case("ZF-1")
        self.assertEqual(len(case_after_open["hazards"]), 3)
        self.assertEqual(case_after_open["hazards"][:2], baseline_case["hazards"])
        self.assertEqual(case_after_open["safeguarding"], baseline_case["safeguarding"])
        self.assertEqual(case_after_open["score"], baseline_case["score"])
        self.assertEqual(case_after_open["tasks"], baseline_case["tasks"])

        # Role without recorded-reason rights (Retrofit Coordinator rex) sees assurance booleans
        # and proposal state, but NEVER sees resident challenge free-text!
        rex_view = self.assistants.detail(self.rex, tid)
        self.assertNotIn("challenges", rex_view)
        self.assertNotIn("live spark at consumer unit", json.dumps(rex_view))
        self.assertTrue(rex_view["hazard_clock_preserved"])

        # 2. Update -> Escalate -> Resolve as Correction recorded -> stale & non-actionable!
        updated = self.assistants.challenge(
            self.sam,
            tid,
            {
                "action": "update",
                "revision": opened["revision"],
                "id": "ACH-1",
                "expected_version": 1,
                "channel": "Phone",
                "detail": "SYN nominee confirmed preferred morning access.",
                "source": "SYN-ASSIST-UPD-1",
                "next_update": "2099-02-02",
            },
        )
        escalated = self.assistants.challenge(
            self.sam,
            tid,
            {
                "action": "escalate",
                "revision": updated["revision"],
                "id": "ACH-1",
                "expected_version": 2,
                "reason": "SYN escalate to programme manager.",
                "escalated_to": "pam@example.test",
                "next_update": "2099-02-03",
            },
        )
        resolved = self.assistants.challenge(
            self.pam,
            tid,
            {
                "action": "resolve",
                "revision": escalated["revision"],
                "id": "ACH-1",
                "expected_version": 3,
                "resolution": "Correction recorded",
                "resolution_ref": "SYN-ASSIST-CORR-1",
                "explanation": "SYN appointment draft relied on superseded slot.",
                "next_update": "2099-02-04",
            },
        )
        self.assertTrue(resolved["stale"])
        self.assertEqual(resolved["display_state"], "stale")
        self.assertFalse(resolved["actionable"])

        # Verify/accept on corrected proposal MUST fail closed, while reject remains allowed!
        with self.assertRaises(ValueError):
            self.assistants.review(
                self.pam,
                tid,
                "verify",
                resolved["revision"],
                note="SYN try verify stale",
                source_verified=True,
            )

        # 3. Reopen ACH-1 -> staleness remains preserved until fresh proposal work!
        reopened = self.assistants.challenge(
            self.pam,
            tid,
            {
                "action": "reopen",
                "revision": resolved["revision"],
                "id": "ACH-1",
                "expected_version": 4,
                "channel": "Assisted visit",
                "reason": "SYN household supplied additional appointment constraint.",
                "source": "SYN-ASSIST-REOPEN-1",
                "next_update": "2099-02-06",
            },
        )
        self.assertTrue(reopened["stale"])
        self.assertFalse(reopened["actionable"])
        self.assertEqual(reopened["challenges"][0]["status"], "Open")
        self.assertTrue(reopened["challenges"][0]["prior_correction_preserved"])

        # Stale revision fence raises ConflictError, and forged keys raise ValueError.
        with self.assertRaises(ConflictError):
            self.assistants.challenge(
                self.pam,
                tid,
                {
                    "action": "update",
                    "revision": resolved["revision"],
                    "id": "ACH-1",
                    "expected_version": 5,
                    "detail": "SYN stale task revision",
                    "source": "SYN",
                    "next_update": "2099-02-07",
                },
            )
        with self.assertRaises(ChallengeSafeguardError):
            self.assistants.challenge(
                self.pam,
                tid,
                {
                    "action": "update",
                    "revision": reopened["revision"],
                    "id": "ACH-1",
                    "expected_version": 5,
                    "detail": "SYN adverse field attempt",
                    "source": "SYN",
                    "next_update": "2099-02-07",
                    "refusal": True,
                },
            )

        # PC-004 check: transient keys are stripped from stored SQLite JSON, and sensor-consent
        # withholding scrubs challenge free-text notes to WITHHELD_NOTE!
        with self.assistants.transaction() as db:
            raw_stored = json.loads(
                db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()[0]
            )
            self.assertNotIn("non_retaliation_assurance", raw_stored)
            self.assertNotIn("review_flag", raw_stored)
            # Simulate sensor-consent withholding on a projected body copy.
            body_copy = copy.deepcopy(reopened)
            self.assistants._sensors_granted = lambda _db, _b: False
            self.assertTrue(self.assistants._withhold_sensors(db, body_copy))
            self.assertEqual(body_copy["challenges"][0]["request"], WITHHELD_NOTE)
            self.assertEqual(body_copy["challenges"][0]["explanation"], WITHHELD_NOTE)
            self.assertEqual(
                body_copy["challenges"][0]["previous_resolutions"][0]["explanation"],
                WITHHELD_NOTE,
            )
        self.assertTrue(self.store.verify_audit())


if __name__ == "__main__":
    unittest.main()
