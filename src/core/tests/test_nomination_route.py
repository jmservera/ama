"""Nomination, self-referral, acknowledgement, challenge, re-review and hazard routing (#130)."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from functools import partial
from pathlib import Path
from typing import Any, cast

_CORE_DIR = Path(__file__).resolve().parents[1]
_SRC_ROOT = _CORE_DIR.parent


def _module_outside_worktree(mod: object) -> bool:
    mod_file = getattr(mod, "__file__", None)
    if isinstance(mod_file, str):
        return not Path(mod_file).resolve().is_relative_to(_SRC_ROOT)
    mod_paths = getattr(mod, "__path__", None)
    if mod_paths is not None:
        for entry in mod_paths:
            if isinstance(entry, str) and not Path(entry).resolve().is_relative_to(_SRC_ROOT):
                return True
    return False


def _bootstrap_worktree_paths() -> None:
    """Keep bare unittest discover isolated to this worktree without breaking suite imports."""
    for target in (_SRC_ROOT / "agents" / "src", _CORE_DIR / "tests", _CORE_DIR / "src"):
        path_str = str(target)
        if path_str in sys.path:
            sys.path.remove(path_str)
        sys.path.insert(0, path_str)
    if any(
        (name == "zava_forward" or name.startswith("zava_forward."))
        and _module_outside_worktree(mod)
        for name, mod in list(sys.modules.items())
    ):
        for name in [
            key
            for key in list(sys.modules)
            if key == "zava_forward" or key.startswith("zava_forward.")
        ]:
            sys.modules.pop(name, None)


_bootstrap_worktree_paths()

from dataset import DATA  # noqa: E402
from zava_forward.core import nomination_route as nr  # noqa: E402
from zava_forward.core import resident_decisions, taskqueues  # noqa: E402
from zava_forward.core.sqlstore import SqlStore  # noqa: E402
from zava_forward.core.store import ConflictError, GateError, Store  # noqa: E402

MEASURES = ("Loft insulation", "Cavity wall")

REC: dict[str, Any] = {
    "owner": {"name": "Sam Owner", "role": "Resident Liaison Officer"},
    "acknowledgement": {"reference": "SYN-ACK"},
    "non_digital_route": "Phone the staffed office",
    "original": {
        "reported_subject_ref": "SYN-SUBJ-1",
        "account": "SYN-ORIGINAL",
        "source": "SYN-ORIG-SRC",
        "channel": "Phone",
    },
    "corrections": [
        {
            "version": 2,
            "reported_subject_ref": "SYN-SUBJ-2",
            "account": "SYN-CORRECTED",
            "source": "SYN-SRC",
            "channel": "Letter",
            "raised_by": "Representative",
            "representative_ref": "SYN-REP-A",
            "challenge": {"id": "CH-001", "status": "Open", "resolution": None},
            "challenged_review": {
                "record_version": 1,
                "reviewer": {"name": "Rae"},
                "outcome": "More evidence needed",
            },
        }
    ],
    "reviews": [
        {
            "record_version": 1,
            "reviewer": {"name": "Rae", "code": "RLO-2"},
            "outcome": "More evidence needed",
            "rationale": "SYN initial review",
            "evidence_ref": "SYN-EV-1",
            "competing_evidence_versions": [],
            "stale_from_version": 2,
        }
    ],
}


def _open_store_instance(path: Path, *, sql: bool) -> Any:
    if sql:
        return cast(Any, SqlStore)(str(path), str(path.with_suffix(".sqlite")))
    return cast(Any, Store)(str(path))


class NominationRoute(unittest.TestCase):
    def test_review_needs_owner_acknowledgement_and_route(self) -> None:
        self.assertEqual(nr.missing_before_review(REC), [])
        nr.require_ready_for_review(REC)
        legacy = {**REC, "owner": None, "acknowledgement": {}, "non_digital_route": "   "}
        self.assertEqual(
            nr.missing_before_review(legacy),
            ["named owner", "staff-recorded acknowledgement", "staffed non-digital route"],
        )
        role_only = {
            **REC,
            "owner": {"name": "Resident Liaison Officer", "role": "Resident Liaison Officer"},
            "acknowledgement": {"reference": "  "},
        }
        self.assertEqual(
            nr.missing_before_review(role_only),
            ["named owner", "staff-recorded acknowledgement"],
        )
        with self.assertRaisesRegex(ValueError, "named owner"):
            nr.require_ready_for_review(legacy)

    def test_hazard_concern_routes_to_intake_unless_explicitly_false(self) -> None:
        self.assertIsNone(nr.hazard_routing(False))
        for flag in (True, None, "no", 0, ""):
            route = nr.hazard_routing(flag, case_id="ZF-1")
            assert route is not None
            self.assertEqual(route["issue"], "#85")
            self.assertEqual(route["route"], "independent_hazard_intake")
            self.assertEqual(route["action"], "/api/cases/ZF-1/hazard-raise")
            self.assertIs(route["queue_item_created"], False)
            self.assertIs(route["immediate"], True)
        err = nr.HazardRouted(case_id="ZF-1")
        self.assertEqual(err.route["issue"], "#85")
        self.assertEqual(err.route["action"], "/api/cases/ZF-1/hazard-raise")
        self.assertIs(err.route["queue_item_created"], False)

    def test_trail_keeps_competing_evidence_reviewer_and_live_outcome(self) -> None:
        trail = nr.challenge_trail(REC)
        self.assertEqual(trail["original_account"], "SYN-ORIGINAL")
        self.assertEqual(trail["competing_evidence"][0]["challenge_id"], "CH-001")
        self.assertEqual(trail["competing_evidence"][0]["challenge_status"], "Open")
        self.assertEqual(trail["competing_evidence"][0]["challenged_review"]["reviewer"], "Rae")
        self.assertEqual(trail["reviews"][0]["reviewer"], "Rae")
        self.assertEqual(trail["reviews"][0]["outcome"], "More evidence needed")
        self.assertIn("sanction", trail["not_decided"])

        live_challenges = [
            {
                "id": "CH-001",
                "status": "Resolved",
                "resolution": {
                    "outcome": "Correction recorded",
                    "recorded_by": {"name": "Sam Owner"},
                    "reference": "SYN-RES-1",
                },
            }
        ]
        resolved_trail = nr.challenge_trail(REC, live_challenges)
        competing = resolved_trail["competing_evidence"][0]
        self.assertEqual(competing["challenge_status"], "Resolved")
        self.assertEqual(
            competing["challenge_resolution"],
            {
                "outcome": "Correction recorded",
                "reviewer": "Sam Owner",
                "reference": "SYN-RES-1",
            },
        )

    def test_correction_sends_only_dependents_back_without_acceptance(self) -> None:
        nom_v1 = ("nomination", "NOM-1", "v1")
        nom_v3 = ("nomination", "NOM-1", "v3")
        graph = {
            ("proposal", "P-1", "v1"): [nom_v1],
            ("review", "R-1", "v1"): [("proposal", "P-1", "v1")],
            ("proposal", "P-2", "v1"): [("source", "S-2", "v1")],
        }
        multi_reviews = {
            **REC,
            "reviews": [
                {
                    "record_version": 1,
                    "reviewer": {"name": "Rae"},
                    "outcome": "More evidence needed",
                },
                {
                    "record_version": 3,
                    "reviewer": {"name": "Rae"},
                    "outcome": "Accepted for human eligibility review",
                },
            ],
        }
        out_v1 = nr.re_review_set(nom_v1, graph, multi_reviews)
        self.assertEqual(out_v1["dependents"], [("proposal", "P-1", "v1"), ("review", "R-1", "v1")])
        self.assertEqual(out_v1["review_versions"], [1])
        self.assertEqual(out_v1["dependent_review_versions"], [1])
        self.assertIs(out_v1["automatic_acceptance"], False)
        self.assertIs(out_v1["automatic_sanction"], False)

        out_v3 = nr.re_review_set(nom_v3, graph, multi_reviews)
        self.assertEqual(out_v3["review_versions"], [1, 3])
        with self.assertRaises(ValueError):
            nr.parse_dependencies([{"decision": ["bad"], "depends_on": []}])


class JsonNominationChallengeRoute(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["cases"][0]["measures"] = list(MEASURES)
        data["staff"].extend(
            [
                {
                    "code": "RLO-2",
                    "name": "Rae Reviewer",
                    "email": "rae@example.test",
                    "role": "Resident Liaison Officer",
                },
                {
                    "code": "CON-1",
                    "name": "Kim Contractor",
                    "email": "kim@example.test",
                    "role": "Contractor",
                    "contractor": "Test Ltd",
                },
            ]
        )
        self.sam, self.pam, self.rae, self.kim = data["staff"]
        self.seed_data = data
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()
        self.store.technical_action(self.pam, "ZF-1", {"action": "design_submit", "note": "SYN"})

    def open_store(self) -> Any:
        store = _open_store_instance(self.path, sql=self.sql)
        if self.sql:
            self.addCleanup(store.db.close)
        return store

    def reseed(self, data: dict[str, Any], name: str) -> None:
        self.path = Path(self.tmp.name) / name / "synthetic.json"
        self.path.parent.mkdir()
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()

    def nomination_body(self, **changes: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "action": "nomination_record",
            "case_id": "ZF-1",
            "kind": "Self-referral",
            "reported_subject_ref": "SYN-SUBJ-ORIG",
            "account": "SYN original referral account",
            "source": "SYN phone intake",
            "channel": "Phone",
            "owner": self.sam["email"],
            "acknowledgement_ref": "SYN-ACK-1",
            "next_update": "2099-01-10",
            "non_digital_route": "Phone Sam or write to staffed office",
            "hazard_concern": False,
        }
        base.update(changes)
        return base

    def acknowledge_body(self, record_id: str, version: int, **changes: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "action": "nomination_acknowledge",
            "case_id": "ZF-1",
            "id": record_id,
            "expected_version": version,
            "owner": self.sam["email"],
            "acknowledgement_ref": "SYN-ACK-RESTORED",
            "non_digital_route": "Phone staffed office or visit hub",
            "next_update": "2099-01-15",
        }
        base.update(changes)
        return base

    def review_body(self, record_id: str, version: int, **changes: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "action": "nomination_review",
            "case_id": "ZF-1",
            "id": record_id,
            "expected_version": version,
            "outcome": "More evidence needed",
            "rationale": "SYN plain-language review rationale",
            "evidence_ref": "SYN-REV-EV-1",
            "next_update": "2099-02-01",
        }
        base.update(changes)
        return base

    def correction_body(self, record_id: str, version: int, **changes: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "action": "nomination_correct",
            "case_id": "ZF-1",
            "id": record_id,
            "expected_version": version,
            "reported_subject_ref": "SYN-SUBJ-CORRECTED",
            "account": "SYN competing resident correction",
            "source": "SYN letter correction",
            "channel": "Letter",
            "next_update": "2099-01-20",
            "challenge_id": None,
        }
        base.update(changes)
        return base

    def challenge_body(self, proposal: dict[str, Any], **changes: Any) -> dict[str, Any]:
        target = next(
            item
            for item in self.store.detail("ZF-1", self.sam)["challenge_targets"]
            if item["proposal_id"] == proposal["id"]
        )
        base: dict[str, Any] = {
            "action": "challenge_open",
            "proposal_id": proposal["id"],
            "proposal_version": target["proposal_version"],
            "decision_version": target["decision_version"],
            "target_kind": "proposal",
            "channel": "Letter",
            "source": "SYN challenge source",
            "request": "SYN review source inputs",
            "explanation": "SYN plain-language explanation",
            "owner": self.sam["email"],
            "non_digital_route": "SYN phone or letter to Sam",
            "next_update": "2099-01-25",
        }
        base.update(changes)
        return base

    def assert_unchanged_failure(self, call: Any) -> None:
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        with self.assertRaises((ValueError, PermissionError, GateError, ConflictError)):
            call()
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_ac1_referral_has_acknowledged_route_and_named_owner_before_review(self) -> None:
        seeded = copy.deepcopy(self.seed_data)
        seeded["cases"][0]["nomination_records"] = [
            {
                "id": "NOM-LEGACY-1",
                "version": 1,
                "case_id": "ZF-1",
                "kind": "Officer nomination",
                "original": {
                    "reported_subject_ref": "SYN-LEGACY-SUBJ",
                    "account": "SYN legacy unacknowledged referral",
                    "source": "SYN legacy import",
                    "channel": "Letter",
                    "recorded_by": {
                        "email": self.sam["email"],
                        "code": self.sam["code"],
                        "name": self.sam["name"],
                        "role": self.sam["role"],
                        "oid": None,
                    },
                    "at": "2026-01-01T10:00:00+00:00",
                },
                "identity_status": "Unknown",
                "support_needs": "Unknown",
                "risk_flags": "Unknown",
                "owner": None,
                "acknowledgement": None,
                "next_update": "2099-01-05",
                "non_digital_route": "",
                "review_status": "Human identity and eligibility review required",
                "corrections": [],
            }
        ]
        self.reseed(seeded, "legacy-unready")
        unready_view = self.open_store().detail("ZF-1", self.sam)["nomination_records"][0]
        self.assertFalse(unready_view["follow_up"]["route_ready"])
        self.assertEqual(
            unready_view["follow_up"]["missing"],
            ["named owner", "staff-recorded acknowledgement", "staffed non-digital route"],
        )
        self.assert_unchanged_failure(
            partial(
                self.store.resident_action,
                self.rae,
                "ZF-1",
                self.review_body("NOM-LEGACY-1", 1),
            )
        )
        self.assert_unchanged_failure(
            partial(
                self.store.resident_action,
                self.sam,
                "ZF-1",
                self.acknowledge_body("NOM-LEGACY-1", 1, owner=self.kim["email"]),
            )
        )
        self.store.resident_action(self.sam, "ZF-1", self.acknowledge_body("NOM-LEGACY-1", 1))
        ready = self.open_store().detail("ZF-1", self.sam)["nomination_records"][0]
        self.assertEqual(ready["version"], 2)
        self.assertTrue(ready["follow_up"]["route_ready"])
        self.assertEqual(ready["owner"]["code"], self.sam["code"])
        self.assertEqual(ready["original"]["account"], "SYN legacy unacknowledged referral")
        self.assert_unchanged_failure(
            partial(
                self.store.resident_action,
                self.sam,
                "ZF-1",
                self.review_body("NOM-LEGACY-1", 2),
            )
        )
        self.store.resident_action(
            self.rae,
            "ZF-1",
            self.review_body("NOM-LEGACY-1", 2, outcome="Accepted for human eligibility review"),
        )
        reviewed = self.open_store().detail("ZF-1", self.sam)["nomination_records"][0]
        self.assertTrue(reviewed["follow_up"]["review_current"])
        self.assertEqual(reviewed["reviews"][0]["reviewer"]["code"], self.rae["code"])
        self.assertTrue(self.open_store().verify_audit())

    def test_ac2_resident_and_representative_challenge_retain_competing_evidence(self) -> None:
        self.store.resident_action(self.sam, "ZF-1", self.nomination_body())
        nom_id = str(self.store.cases["ZF-1"]["nomination_records"][0]["id"])
        self.store.resident_action(
            self.rae,
            "ZF-1",
            self.review_body(nom_id, 1, outcome="Not progressed; resident may challenge"),
        )
        proposal = dict(self.store.ai_priority(self.sam, mode="workflow-only"))
        self.store.resident_action(
            self.sam,
            "ZF-1",
            self.challenge_body(proposal, raised_by="Resident"),
        )
        self.assert_unchanged_failure(
            partial(
                self.store.resident_action,
                self.sam,
                "ZF-1",
                self.challenge_body(
                    proposal, raised_by="Representative", representative_ref="SYN-REP-A"
                ),
            )
        )
        for measure in MEASURES:
            self.store.resident_action(
                self.sam,
                "ZF-1",
                {
                    "action": "scope_record",
                    "measure": measure,
                    "design_version": 1,
                    "scope": "SYN-SCOPE",
                    "source": "SYN",
                },
            )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            {
                "action": "safe_contact_record",
                "safe_contact_ref": "SYN-SAFE-1",
                "source": "SYN",
            },
        )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            {
                "action": "representative_record",
                "measure": MEASURES[0],
                "context_revision": 1,
                "representative_ref": "SYN-REP-A",
                "status": "Confirmed",
                "tasks": ["Communicate"],
                "source": "SYN-AUTH-1",
                "authority_date": "2026-01-01",
                "review_date": "2099-01-01",
                "resident_wishes": "SYN wishes",
                "safe_contact_ref": "SYN-SAFE-1",
            },
        )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            {
                "action": "representative_record",
                "measure": MEASURES[1],
                "context_revision": 1,
                "representative_ref": "SYN-REP-A",
                "status": "Confirmed",
                "tasks": ["Works decision"],
                "source": "SYN-AUTH-2",
                "authority_date": "2026-01-01",
                "review_date": "2099-01-01",
                "resident_wishes": "SYN wishes",
                "safe_contact_ref": "SYN-SAFE-1",
            },
        )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            self.challenge_body(
                proposal, raised_by="Representative", representative_ref="  SYN-REP-A  "
            ),
        )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            self.correction_body(
                nom_id,
                1,
                challenge_id="CH-2",
                raised_by="Representative",
                representative_ref="  SYN-REP-A  ",
            ),
        )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            {
                "action": "challenge_resolve",
                "id": "CH-2",
                "expected_version": 1,
                "resolution": "Correction recorded",
                "resolution_ref": "SYN-CH-RES-2",
                "explanation": "SYN correction linked and reviewed",
                "next_update": "2099-02-05",
            },
        )
        self.store.resident_action(
            self.rae,
            "ZF-1",
            self.review_body(nom_id, 2, outcome="Accepted for human eligibility review"),
        )
        detail = self.open_store().detail("ZF-1", self.sam)
        self.assertEqual(detail["affected_challenges"][0]["raised_by"], "Resident")
        self.assertEqual(detail["affected_challenges"][1]["raised_by"], "Representative")
        self.assertEqual(detail["affected_challenges"][1]["representative_ref"], "SYN-REP-A")
        record = detail["nomination_records"][0]
        trail = record["challenge_trail"]
        self.assertEqual(trail["original_account"], "SYN original referral account")
        self.assertEqual(len(trail["competing_evidence"]), 1)
        comp = trail["competing_evidence"][0]
        self.assertEqual(comp["raised_by"], "Representative")
        self.assertEqual(comp["representative_ref"], "SYN-REP-A")
        self.assertEqual(comp["challenge_id"], "CH-2")
        self.assertEqual(comp["challenge_status"], "Resolved")
        self.assertEqual(comp["challenge_resolution"]["outcome"], "Correction recorded")
        self.assertEqual(
            comp["challenged_review"]["outcome"], "Not progressed; resident may challenge"
        )
        self.assertEqual(
            [item["outcome"] for item in trail["reviews"]],
            [
                "Not progressed; resident may challenge",
                "Accepted for human eligibility review",
            ],
        )
        self.assertEqual(trail["reviews"][1]["competing_evidence_versions"], [2])

    def test_ac3_correction_triggers_dependent_re_review_without_acceptance_or_sanction(
        self,
    ) -> None:
        self.store.resident_action(
            self.sam,
            "ZF-1",
            {
                "action": "scope_record",
                "measure": MEASURES[0],
                "design_version": 1,
                "scope": "SYN-SCOPE",
                "source": "SYN",
            },
        )
        self.store.resident_action(
            self.sam,
            "ZF-1",
            {
                "action": "decision_record",
                "measure": MEASURES[0],
                "context_revision": 1,
                "status": "Accepted",
                "answered_by": "The resident",
                "source": "SYN-CONSENT",
                "note": "SYN explicit consent",
            },
        )
        self.store.resident_action(self.sam, "ZF-1", self.nomination_body())
        nom_id = str(self.store.cases["ZF-1"]["nomination_records"][0]["id"])
        self.store.resident_action(self.rae, "ZF-1", self.review_body(nom_id, 1))
        ranking_before = self.store._ranking()
        decisions_before = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"])
        hazards_before = copy.deepcopy(self.store.cases["ZF-1"]["hazards"])
        self.assert_unchanged_failure(
            partial(
                self.store.resident_action,
                self.sam,
                "ZF-1",
                self.correction_body(nom_id, 1, dependencies="invalid"),
            )
        )
        deps = [
            {
                "decision": ["proposal", "PRIO-1", "v1"],
                "depends_on": [["nomination", nom_id, "v1"]],
            },
            {
                "decision": ["review", "ELIG-1", "v1"],
                "depends_on": [["proposal", "PRIO-1", "v1"]],
            },
            {
                "decision": ["proposal", "UNRELATED-9", "v1"],
                "depends_on": [["source", "OTHER-SRC", "v1"]],
            },
        ]
        self.store.resident_action(
            self.sam,
            "ZF-1",
            self.correction_body(nom_id, 1, raised_by="Resident", dependencies=deps),
        )
        record = self.open_store().detail("ZF-1", self.sam)["nomination_records"][0]
        re_review = record["corrections"][0]["re_review"]
        self.assertEqual(
            re_review,
            {
                "required": True,
                "automatic_acceptance": False,
                "automatic_sanction": False,
                "dependent_review_versions": [1],
                "dependents": [
                    {"kind": "proposal", "id": "PRIO-1", "version": "v1"},
                    {"kind": "review", "id": "ELIG-1", "version": "v1"},
                ],
            },
        )
        self.assertTrue(record["follow_up"]["re_review_pending"])
        self.assertFalse(record["follow_up"]["review_current"])
        self.assertIs(record["follow_up"]["automatic_acceptance"], False)
        self.assertIs(record["follow_up"]["automatic_sanction"], False)
        self.assertEqual(self.store._ranking(), ranking_before)
        self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], decisions_before)
        self.assertEqual(self.store.cases["ZF-1"]["hazards"], hazards_before)

    def test_ac4_emergency_or_hazard_routes_immediately_to_independent_hazard_intake(
        self,
    ) -> None:
        self.store.resident_action(self.sam, "ZF-1", self.nomination_body())
        nom_id = str(self.store.cases["ZF-1"]["nomination_records"][0]["id"])
        proposal = dict(self.store.ai_priority(self.sam, mode="workflow-only"))
        queue_before = taskqueues.overdue_tasks(
            cast(dict[str, Any], self.store.cases["ZF-1"]),
            as_of="2100-01-01T00:00:00Z",
            handoff=None,
        )
        for body in (
            self.nomination_body(hazard_concern=True),
            self.nomination_body(hazard_concern=None),
            self.acknowledge_body(nom_id, 1, hazard_concern=True),
            self.acknowledge_body(nom_id, 1, hazard_concern=None),
            self.review_body(nom_id, 1, hazard_concern=True),
            self.review_body(nom_id, 1, hazard_concern=None),
            self.correction_body(nom_id, 1, hazard_concern=True),
            self.correction_body(nom_id, 1, hazard_concern=None),
            self.challenge_body(proposal, hazard_concern=True),
            self.challenge_body(proposal, hazard_concern=None),
        ):
            with self.subTest(action=body["action"], flag=body["hazard_concern"]):
                before_case = copy.deepcopy(self.store.cases["ZF-1"])
                before_audit = list(self.store.audit_entries())
                with self.assertRaises(nr.HazardRouted) as caught:
                    self.store.resident_action(self.sam, "ZF-1", body)
                self.assertIsInstance(caught.exception, resident_decisions.HazardRouted)
                self.assertEqual(caught.exception.route["issue"], "#85")
                self.assertEqual(caught.exception.route["route"], "independent_hazard_intake")
                self.assertEqual(caught.exception.route["action"], "/api/cases/ZF-1/hazard-raise")
                self.assertIs(caught.exception.route["queue_item_created"], False)
                self.assertEqual(self.store.cases["ZF-1"], before_case)
                self.assertEqual(list(self.store.audit_entries()), before_audit)
                self.assertEqual(
                    taskqueues.overdue_tasks(
                        cast(dict[str, Any], self.store.cases["ZF-1"]),
                        as_of="2100-01-01T00:00:00Z",
                        handoff=None,
                    ),
                    queue_before,
                )
        nom_count = len(self.store.cases["ZF-1"]["nomination_records"])
        idx = self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            "SYN immediate emergency hazard",
            {"source": "SYN hazard intake #85", "aware_at": "2026-01-01T10:00:00Z"},
        )
        reloaded = self.open_store().cases["ZF-1"]
        self.assertEqual(len(reloaded["nomination_records"]), nom_count)
        self.assertEqual(reloaded["hazards"][idx]["hold"]["status"], "Active")


class SqlNominationChallengeRoute(JsonNominationChallengeRoute):
    sql = True


if __name__ == "__main__":
    unittest.main()
