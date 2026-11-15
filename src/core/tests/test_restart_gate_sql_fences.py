"""Restart gate corrective-evidence, anti-replay, SQL gate trigger, and old-image fence tests."""

import copy
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from typing import Any

import dataset
import release_support
from zava_forward.core import assistants, continuity, mssqlstore
from zava_forward.core.restart_authority import (
    UNAPPOINTED_RESTART_AUTHORITY,
    validate_corrective_evidence,
)
from zava_forward.core.sqlstore import SqlStore

DATASET_MOD: Any = dataset
RELEASE_SUPPORT: Any = release_support
ASSISTANTS_MOD: Any = assistants
CONTINUITY_MOD: Any = continuity
MSSQLSTORE_MOD: Any = mssqlstore
SQL_STORE_CLS: Any = SqlStore

CAPABILITY = "stock-prioritisation"
OTHER_CAPABILITY = "assessment-preparation"
HUMAN_AUTHORITY = (
    "Building Safety Lead and Executive Sponsor (OD-35 synthetic fixture; not live authority)"
)


def _person(code: str, role: str, oid: str, **extra: Any) -> dict[str, Any]:
    return {
        "code": code,
        "name": f"{role} {code}",
        "email": f"{code.lower()}@example.test",
        "role": role,
        "oid": oid,
        **extra,
    }


STAFF: list[dict[str, Any]] = [
    _person("QI-1", "Quality Inspector", "00000000-0000-0000-0000-000000000201"),
    _person("PM-1", "Retrofit Programme Manager", "00000000-0000-0000-0000-000000000202"),
    _person("PM-2", "Retrofit Programme Manager", "00000000-0000-0000-0000-000000000203"),
    _person("RLO-1", "Resident Liaison Officer", "00000000-0000-0000-0000-000000000204"),
    _person(
        "PSO-1",
        "Programme Support Officer",
        "00000000-0000-0000-0000-000000000205",
        auth_provider="trusted-proxy",
        rule_roles=["ai_restart"],
    ),
    _person(
        "PSO-2",
        "Programme Support Officer",
        "00000000-0000-0000-0000-000000000206",
        auth_provider="trusted-proxy",
        rule_roles=["ai_restart"],
    ),
]
ACTORS: dict[str, dict[str, Any]] = {row["code"]: row for row in STAFF}


def _incident(scope: str = CAPABILITY, **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "scope": scope,
        "reason": "Synthetic guardrail breach containment",
        "incident_owner": "Quality Inspector QI-1",
        "containment": "Stop affected AI proposals while manual casework continues",
        "comms_owner": "Quality Inspector QI-1",
        "comms_audience": "Synthetic retrofit staff",
        "trigger": "guardrail breach",
        "evidence": "SYN-INCIDENT-122",
        "resident_impact": "Manual liaison continuity active; statutory safety unaffected",
        "remediation": "Correct prompt grounding and rerun negative controls",
        "restart_authority": HUMAN_AUTHORITY,
        "synthetic": True,
    }
    body.update(overrides)
    return body


def _proposal_body(
    suspension_id: str,
    *,
    test_id: str = "synthetic-negative-control-suite-122",
    corrective_evidence: str = "synthetic:corrective-pack-122",
    result: str = "Pass",
    evidence_class: str = "constructed-fixture",
) -> dict[str, Any]:
    return {
        "id": suspension_id,
        "test_id": test_id,
        "corrective_evidence": corrective_evidence,
        "result": result,
        "evidence_class": evidence_class,
    }


def _decision_body(
    suspension: dict[str, Any],
    *,
    decision: str = "Restart",
    authority_ref: str | None = None,
) -> dict[str, Any]:
    return {
        "id": suspension["id"],
        "epoch": suspension["proposal"]["epoch"],
        "proposal_digest": suspension["proposal"]["digest"],
        "decision": decision,
        "authority_ref": authority_ref or suspension["restart_authority"],
    }


_ASSIST_ENV: dict[str, str] = {
    "ZF_ASSIST_AUTHORITY": "local-nonbillable-test-authority",
    "ZF_ASSIST_EXPIRES": "2099-01-01T00:00:00Z",
    "ZF_ASSIST_CALL_ALLOWANCE": "100",
    "ZF_ASSIST_TOKEN_ALLOWANCE": "2000000",
    "ZF_ASSIST_PROACTIVE": "1",
}


class _FakeAiProvider:
    configured = True
    sends_no_bytes = True
    provider = "local-test-double"
    endpoint = "local-test"
    fast = "test"
    strong = "test"
    model_version = "test-model"
    model_version_strong = "test-model"
    release: Any = None

    def is_live(self, capability: str | None = None) -> bool:
        return True


class RestartGateSqlFencesTest(unittest.TestCase):
    tmp: tempfile.TemporaryDirectory[str]
    seed_path: str
    db_path: str
    store: Any
    service: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        seed: dict[str, Any] = copy.deepcopy(DATASET_MOD.DATA)
        seed["staff"] = copy.deepcopy(STAFF)
        self.seed_path = str(Path(self.tmp.name) / "zavaforward.json")
        Path(self.seed_path).write_text(json.dumps(seed))
        self.db_path = os.path.join(self.tmp.name, "zf-122.sqlite")
        self.store = SQL_STORE_CLS(self.seed_path, self.db_path)
        self.store.ai = _FakeAiProvider()
        self.service = ASSISTANTS_MOD.Assistants(self.store, _ASSIST_ENV)
        RELEASE_SUPPORT.install(self.store)

    def tearDown(self) -> None:
        self.service.stop()
        self.tmp.cleanup()

    def _open_peer(self) -> tuple[Any, Any]:
        peer_store = SQL_STORE_CLS(self.seed_path, self.db_path)
        peer_store.ai = _FakeAiProvider()
        peer_service = ASSISTANTS_MOD.Assistants(peer_store, _ASSIST_ENV)
        self.addCleanup(peer_service.stop)
        return peer_store, peer_service

    def test_placeholder_missing_and_non_pass_corrective_evidence_refused(self) -> None:
        self.assertEqual(
            validate_corrective_evidence("synthetic:corrective-pack-122"),
            "synthetic:corrective-pack-122",
        )
        self.assertEqual(
            validate_corrective_evidence(
                "Verified pending-queue handling with negative controls",
                label="corrective evidence",
            ),
            "Verified pending-queue handling with negative controls",
        )
        canary = "PRIVATE-CANARY-122"
        placeholders = (
            "",
            "   ",
            "ab",
            "TBD",
            f"TBD: {canary}",
            "TODO: run negative control pack",
            "Pending verification",
            "none",
            "N/A",
            "unknown",
            "placeholder",
            "Unavailable: awaiting test runner",
            "CM-0123456789abcdef",
            "self-approved",
            "auto-restart",
        )
        for bad in placeholders:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError) as err_ctx:
                    validate_corrective_evidence(bad)
                self.assertNotIn(canary, str(err_ctx.exception))

        s = self.store.suspend(ACTORS["QI-1"], _incident())
        for bad_ev in ("TBD", "TODO: rerun later", "Unavailable: skipped", "none", "N/A"):
            with self.assertRaises(ValueError):
                self.store.restart_propose(
                    ACTORS["PM-1"],
                    _proposal_body(s["id"], corrective_evidence=bad_ev),
                )
        for bad_tid in ("TBD", "placeholder", "CM-abcdef012345"):
            with self.assertRaises(ValueError):
                self.store.restart_propose(
                    ACTORS["PM-1"],
                    _proposal_body(s["id"], test_id=bad_tid),
                )
        with self.assertRaises(PermissionError):
            self.store.restart_propose(
                ACTORS["PM-1"],
                _proposal_body(s["id"], result="Fail"),
            )

    def test_view_only_and_unauthorized_proposer_and_approver_refused(self) -> None:
        with self.assertRaises(PermissionError):
            self.store.suspend(dict(ACTORS["QI-1"], view_only=True), _incident())

        s = self.store.suspend(ACTORS["QI-1"], _incident())
        with self.assertRaises(PermissionError):
            self.store.restart_propose(
                dict(ACTORS["PM-1"], view_only=True),
                _proposal_body(s["id"]),
            )
        with self.assertRaises(PermissionError):
            self.store.restart_propose(ACTORS["RLO-1"], _proposal_body(s["id"]))

        proposed = self.store.restart_propose(ACTORS["PM-1"], _proposal_body(s["id"]))
        decide = _decision_body(proposed)
        for unauthorized in (
            dict(ACTORS["PSO-1"], view_only=True),
            dict(ACTORS["PSO-1"], rule_roles=[]),
            dict(ACTORS["PSO-1"], auth_provider="password"),
            dict(ACTORS["PSO-1"], oid="00000000-0000-0000-0000-999999999999"),
            ACTORS["RLO-1"],
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(unauthorized, decide)

        with self.assertRaises(PermissionError):
            self.store.restart_decide(
                ACTORS["PSO-1"],
                _decision_body(proposed, authority_ref=UNAPPOINTED_RESTART_AUTHORITY),
            )
        with self.assertRaises(PermissionError):
            self.store.restart_decide(
                ACTORS["PSO-1"],
                {**decide, "automatic": True},
            )
        actions = [row["action"] for row in self.store.audit_entries()]
        self.assertIn("ai_restart_propose_denied", actions)
        self.assertIn("ai_restart_decide_denied", actions)

    def test_self_approval_across_email_code_oid_and_name_aliases_refused(self) -> None:
        s = self.store.suspend(ACTORS["QI-1"], _incident())
        with self.assertRaises(PermissionError):
            self.store.restart_propose(ACTORS["QI-1"], _proposal_body(s["id"]))
        with self.assertRaises(PermissionError):
            self.store.restart_propose(
                {
                    "email": "alias-qi@example.test",
                    "name": "Different Name",
                    "code": "QI-ALIAS",
                    "role": "Retrofit Programme Manager",
                    "oid": ACTORS["QI-1"]["oid"],
                },
                _proposal_body(s["id"]),
            )

        proposed = self.store.restart_propose(ACTORS["PM-1"], _proposal_body(s["id"]))
        decide = _decision_body(proposed)
        for colliding_approver in (
            dict(ACTORS["PM-1"], auth_provider="trusted-proxy", rule_roles=["ai_restart"]),
            dict(ACTORS["QI-1"], auth_provider="trusted-proxy", rule_roles=["ai_restart"]),
            {
                **ACTORS["PSO-1"],
                "email": ACTORS["PM-1"]["email"].upper(),
            },
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(colliding_approver, decide)

        self.store.restart_decide(ACTORS["PSO-1"], decide)
        decided = self.store.continuity_view(ACTORS["PM-1"])["suspensions"][-1]["restart"]
        self.assertEqual(decided["actor"]["oid"], ACTORS["PSO-1"]["oid"])
        self.assertEqual(decided["actor"]["code"], "PSO-1")

    def test_replayed_and_stale_restart_proposals_and_digests_fail_closed(self) -> None:
        s = self.store.suspend(ACTORS["QI-1"], _incident())
        p1 = self.store.restart_propose(
            ACTORS["PM-1"],
            _proposal_body(
                s["id"],
                test_id="suite-alpha-122",
                corrective_evidence="synthetic:evidence-alpha-122",
            ),
        )
        d1 = _decision_body(p1)
        kept = self.store.restart_decide(
            ACTORS["PSO-1"],
            _decision_body(p1, decision="Keep suspended"),
        )
        self.assertEqual(kept["status"], "Suspended")

        # Rejected digest cannot be replayed directly for Restart.
        with self.assertRaises(PermissionError):
            self.store.restart_decide(ACTORS["PSO-1"], d1)
        # Rejected (test_id, corrective_evidence) or EITHER normalized identifier alone cannot
        # be re-proposed on the same suspension.
        for replay_tid, replay_ev in (
            ("suite-alpha-122", "synthetic:evidence-alpha-122"),
            ("  SUITE-ALPHA-122  ", "synthetic:fresh-evidence-after-reject-122"),
            ("suite-fresh-after-reject-122", "  SYNTHETIC:EVIDENCE-ALPHA-122  "),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_propose(
                    ACTORS["PM-1"],
                    _proposal_body(
                        s["id"],
                        test_id=replay_tid,
                        corrective_evidence=replay_ev,
                    ),
                )

        # Superseding proposal invalidates older digest via proposal_seq even at same epoch.
        p2 = self.store.restart_propose(
            ACTORS["PM-1"],
            _proposal_body(
                s["id"],
                test_id="suite-beta-122",
                corrective_evidence="synthetic:evidence-beta-122",
            ),
        )
        d2 = _decision_body(p2)
        p3 = self.store.restart_propose(
            ACTORS["PM-1"],
            _proposal_body(
                s["id"],
                test_id="suite-gamma-122",
                corrective_evidence="synthetic:evidence-gamma-122",
            ),
        )
        self.assertNotEqual(d2["proposal_digest"], p3["proposal"]["digest"])
        with self.assertRaises(PermissionError):
            self.store.restart_decide(ACTORS["PSO-1"], d2)

        # Epoch bump from another incident makes p3 stale until re-proposed at the new epoch.
        other_s = self.store.suspend(ACTORS["QI-1"], _incident(scope="quality-evidence"))
        other_p = self.store.restart_propose(
            ACTORS["PM-2"],
            _proposal_body(
                other_s["id"],
                test_id="suite-quality-122",
                corrective_evidence="synthetic:evidence-quality-122",
            ),
        )
        self.store.restart_decide(ACTORS["PSO-2"], _decision_body(other_p))
        with self.assertRaises(PermissionError):
            self.store.restart_decide(ACTORS["PSO-1"], _decision_body(p3))

        p4 = self.store.restart_propose(
            ACTORS["PM-1"],
            _proposal_body(
                s["id"],
                test_id="suite-gamma-122",
                corrective_evidence="synthetic:evidence-gamma-122",
            ),
        )
        d4 = _decision_body(p4)
        self.store.restart_decide(ACTORS["PSO-1"], d4)

        # Closed suspension refuses replay; consumed or previously rejected test_id or
        # corrective_evidence cannot reuse on a new incident, even when paired with a new peer
        # value or whitespace/case differences.
        with self.assertRaises(ValueError):
            self.store.restart_decide(ACTORS["PSO-1"], d4)
        s2 = self.store.suspend(ACTORS["QI-1"], _incident())
        with self.assertRaises(PermissionError):
            self.store.restart_decide(
                ACTORS["PSO-1"],
                {**d4, "id": s2["id"], "epoch": s2["epoch"]},
            )
        for bad_tid, bad_ev in (
            ("suite-gamma-122", "synthetic:evidence-gamma-122"),
            ("  SUITE-GAMMA-122  ", "synthetic:distinct-new-evidence-122"),
            ("suite-distinct-new-122", "  SYNTHETIC:EVIDENCE-GAMMA-122  "),
            ("  SUITE-ALPHA-122  ", "synthetic:cross-suspension-fresh-122"),
            ("suite-cross-suspension-fresh-122", "  SYNTHETIC:EVIDENCE-ALPHA-122  "),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_propose(
                    ACTORS["PM-1"],
                    _proposal_body(s2["id"], test_id=bad_tid, corrective_evidence=bad_ev),
                )

        # Open pending proposal on s2 also blocks reusing its test_id or corrective_evidence on
        # a concurrent open suspension s3, while distinct fresh identifiers succeed.
        s2_pending = self.store.restart_propose(
            ACTORS["PM-1"],
            _proposal_body(
                s2["id"],
                test_id="suite-open-pending-122",
                corrective_evidence="synthetic:open-pending-122",
            ),
        )
        self.assertEqual(s2_pending["proposal"]["test_id"], "suite-open-pending-122")
        s3 = self.store.suspend(ACTORS["QI-1"], _incident(scope=OTHER_CAPABILITY))
        for open_tid, open_ev in (
            ("  SUITE-OPEN-PENDING-122  ", "synthetic:completely-fresh-s3-122"),
            ("suite-completely-fresh-s3-122", "  SYNTHETIC:OPEN-PENDING-122  "),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_propose(
                    ACTORS["PM-2"],
                    _proposal_body(s3["id"], test_id=open_tid, corrective_evidence=open_ev),
                )
        s3_ok = self.store.restart_propose(
            ACTORS["PM-2"],
            _proposal_body(
                s3["id"],
                test_id="suite-s3-distinct-122",
                corrective_evidence="synthetic:s3-distinct-122",
            ),
        )
        self.assertEqual(s3_ok["proposal"]["test_id"], "suite-s3-distinct-122")

    def test_sql_gate_state_monotonic_no_delete_and_open_holds_sync(self) -> None:
        peer_store, peer_service = self._open_peer()
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        self.addCleanup(conn.close)

        row = conn.execute("SELECT id, gate_version, epoch FROM continuity_gate_state").fetchone()
        self.assertEqual(row, (1, CONTINUITY_MOD.GATE_VERSION, 0))
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM continuity_open_holds").fetchone()[0], 0
        )

        s = self.store.suspend(ACTORS["QI-1"], _incident())
        self.assertIsNotNone(peer_store.continuity_block(CAPABILITY))
        self.assertIsNone(peer_store.continuity_block(OTHER_CAPABILITY))
        with peer_service.transaction() as peer_db:
            self.assertIsNotNone(peer_service.suspended(peer_db, CAPABILITY))
            self.assertIsNone(peer_service.suspended(peer_db, OTHER_CAPABILITY))
        holds = conn.execute(
            "SELECT scope, incident_id, epoch FROM continuity_open_holds"
        ).fetchall()
        self.assertEqual(holds, [(CAPABILITY, s["id"], 1)])

        proposed = self.store.restart_propose(ACTORS["PM-1"], _proposal_body(s["id"]))
        self.store.restart_decide(ACTORS["PSO-1"], _decision_body(proposed))
        # Constructed restart keeps actual_hold=True on continuity_block while clearing open holds.
        self.assertIsNotNone(peer_store.continuity_block(CAPABILITY))
        self.assertIsNone(CONTINUITY_MOD.active(peer_store._cont(), CAPABILITY, constructed=True))
        with peer_service.transaction() as peer_db:
            self.assertIsNone(peer_service.suspended(peer_db, CAPABILITY))
        self.assertEqual(
            conn.execute("SELECT epoch FROM continuity_gate_state WHERE id=1").fetchone()[0],
            2,
        )
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM continuity_open_holds").fetchone()[0], 0
        )

        with self.assertRaisesRegex(sqlite3.IntegrityError, "monotonic"):
            conn.execute("UPDATE continuity_gate_state SET epoch = 0 WHERE id = 1")
        with self.assertRaisesRegex(sqlite3.IntegrityError, "cannot be deleted"):
            conn.execute("DELETE FROM continuity_gate_state WHERE id = 1")

    def test_sql_triggers_reject_old_image_and_suspended_scope_attempts(self) -> None:
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        self.addCleanup(conn.close)

        # Pre-gate 8-column INSERT (gate_version='', capability='') fails closed in SQLite trigger.
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute(
                "INSERT INTO assistant_attempts "
                "(id, task_id, fence, pool, reserved, actual, outcome, active_until) "
                "VALUES ('old-1', 'T-OLD', 1, 'demo', 100, NULL, 'reserved', 9999999999.0)"
            )
        # Wrong gate_version fails closed.
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute(
                "INSERT INTO assistant_attempts "
                "(id, task_id, fence, pool, reserved, actual, outcome, active_until, "
                "capability, gate_version, send_gate_version) "
                "VALUES ('old-2', 'T-OLD', 1, 'demo', 100, NULL, 'reserved', 9999999999.0, "
                "?, 'continuity-gate-v0', '')",
                (CAPABILITY,),
            )

        # Valid current-gate reservation succeeds, but sending without send_gate_version fails.
        conn.execute(
            "INSERT INTO assistant_attempts "
            "(id, task_id, fence, pool, reserved, actual, outcome, active_until, "
            "capability, gate_version, send_gate_version) "
            "VALUES ('cur-1', 'T-CUR', 1, 'demo', 100, NULL, 'reserved', 9999999999.0, ?, ?, '')",
            (CAPABILITY, CONTINUITY_MOD.GATE_VERSION),
        )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute("UPDATE assistant_attempts SET outcome='sending' WHERE id='cur-1'")

        conn.execute(
            "INSERT INTO assistant_attempts "
            "(id, task_id, fence, pool, reserved, actual, outcome, active_until, "
            "capability, gate_version, send_gate_version) "
            "VALUES ('cur-send', 'T-SEND', 1, 'demo', 100, NULL, 'sending', 9999999999.0, ?, ?, ?)",
            (CAPABILITY, CONTINUITY_MOD.GATE_VERSION, CONTINUITY_MOD.GATE_VERSION),
        )
        for ready_tid in ("T-READY-1", "T-READY-2"):
            conn.execute(
                "INSERT INTO assistant_tasks "
                "(id, capability, case_id, signature, body, state, fence, owner, lease_until, "
                "attempts, not_before, revision) "
                "VALUES (?, ?, 'ZF-1', 'sig', '{}', 'ready', 1, '', 0, 1, 0, 1)",
                (ready_tid, CAPABILITY),
            )

        # Pre-gate assistant_tasks verify/accept UPDATE or accepted INSERT (missing
        # review_gate_version / reviewed_revision) fails closed in SQLite triggers.
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute(
                "UPDATE assistant_tasks SET state='accepted', revision=revision+1 "
                "WHERE id='T-READY-1'"
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute(
                "UPDATE assistant_tasks SET body='{\"verified\":1}', revision=revision+1 "
                "WHERE id='T-READY-1'"
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute(
                "UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id='T-READY-1'"
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            conn.execute(
                "INSERT INTO assistant_tasks "
                "(id, capability, case_id, signature, body, state, fence, owner, lease_until, "
                "attempts, not_before, revision) "
                "VALUES ('T-OLD-ACC', ?, 'ZF-1', 'sig', '{}', 'accepted', 1, '', 0, 1, 0, 1)",
                (CAPABILITY,),
            )

        # Suspending CAPABILITY blocks cur-1 from transitioning to 'sending', blocks same-outcome
        # lease extensions and sending->reserved re-reservations, blocks assistant_tasks verify
        # and accept updates, and blocks new inserts on CAPABILITY, while OTHER_CAPABILITY and
        # reject/settlement remain open.
        s = self.store.suspend(ACTORS["QI-1"], _incident(CAPABILITY))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_attempts SET outcome='sending', send_gate_version=? "
                "WHERE id='cur-1'",
                (CONTINUITY_MOD.GATE_VERSION,),
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_attempts SET active_until = active_until + 60 WHERE id='cur-1'"
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_attempts SET active_until = active_until + 60 WHERE id='cur-send'"
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_attempts SET outcome='reserved', active_until=9999999999.0 "
                "WHERE id='cur-send'"
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_tasks SET state='accepted', review_gate_version=?, "
                "reviewed_revision=revision+1, revision=revision+1 WHERE id='T-READY-1'",
                (CONTINUITY_MOD.GATE_VERSION,),
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_tasks SET body='{\"verified\":1}', review_gate_version=?, "
                "reviewed_revision=revision+1, revision=revision+1 WHERE id='T-READY-1'",
                (CONTINUITY_MOD.GATE_VERSION,),
            )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "INSERT INTO assistant_attempts "
                "(id, task_id, fence, pool, reserved, actual, outcome, active_until, "
                "capability, gate_version, send_gate_version) "
                "VALUES ('cur-2', 'T-CUR-2', 1, 'demo', 100, NULL, 'reserved', "
                "9999999999.0, ?, ?, '')",
                (CAPABILITY, CONTINUITY_MOD.GATE_VERSION),
            )
        conn.execute(
            "INSERT INTO assistant_attempts "
            "(id, task_id, fence, pool, reserved, actual, outcome, active_until, "
            "capability, gate_version, send_gate_version) "
            "VALUES ('other-1', 'T-OTHER', 1, 'demo', 100, NULL, 'reserved', "
            "9999999999.0, ?, ?, '')",
            (OTHER_CAPABILITY, CONTINUITY_MOD.GATE_VERSION),
        )
        conn.execute(
            "UPDATE assistant_tasks SET state='rejected', revision=revision+1 WHERE id='T-READY-2'"
        )
        # Settlement / cleanup to non-active outcome remains allowed during suspension.
        conn.execute(
            "UPDATE assistant_attempts SET outcome='suspended', active_until=0 "
            "WHERE id IN ('cur-1', 'cur-send')"
        )
        self.assertEqual(s["status"], "Suspended")

        # Triggers never reference dispatched: dispatched-only/revision retry updates on 'ready'
        # rows succeed, body=body pre-gate verify updates still fail closed, and C5->C7 schema
        # downgrade (DROP COLUMN dispatched) + migrate() recovery succeed with active triggers.
        for trig in (
            *ASSISTANTS_MOD.SQLITE_ATTEMPT_TRIGGERS,
            *ASSISTANTS_MOD.MSSQL_ATTEMPT_TRIGGERS,
        ):
            self.assertNotIn("dispatched", trig)
        conn.execute(
            "UPDATE assistant_tasks SET dispatched=99.0, revision=revision+1 WHERE id='T-READY-1'"
        )
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity scope is suspended"):
            conn.execute(
                "UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id='T-READY-1'"
            )
        conn.execute("DROP INDEX IF EXISTS ix_assistant_dispatched")
        conn.execute("ALTER TABLE assistant_tasks DROP COLUMN dispatched")
        self.service.migrate()
        cols = {row[1] for row in conn.execute("PRAGMA table_info(assistant_tasks)")}
        self.assertIn("dispatched", cols)

    def test_null_gate_version_and_missing_gate_row_fail_closed_in_sql_and_python(self) -> None:
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        self.addCleanup(conn.close)

        # Bump gate_version to simulate newer schema running ahead of this image.
        conn.execute(
            "UPDATE continuity_gate_state SET gate_version='continuity-gate-v99' WHERE id=1"
        )
        hold = self.store.continuity_suspension(CAPABILITY)
        self.assertIsNotNone(hold)
        self.assertEqual(hold["id"], "gate-mismatch")
        queued = self.service.invoke(ACTORS["PM-1"], CAPABILITY, "ZF-1")
        self.assertIsNone(self.service.claim(queued["id"], "mismatched-worker"))
        # Manual casework remains available while SQL gate version mismatches.
        self.store.log_call(ACTORS["RLO-1"], "ZF-1", "Spoke", "SYN manual note under gate hold")
        self.assertEqual(
            self.store.cases["ZF-1"]["contacts"][-1]["note"],
            "SYN manual note under gate hold",
        )

        # Verify NULL-safe NOT EXISTS behavior if gate row were absent in an uninitialized DB.
        raw = sqlite3.connect(":memory:", isolation_level=None)
        self.addCleanup(raw.close)
        for ddl in ASSISTANTS_MOD.SQLITE_DDL[:6]:
            raw.execute(ddl)
        for trig in ASSISTANTS_MOD.SQLITE_ATTEMPT_TRIGGERS:
            raw.execute(trig)
        self.assertIsNotNone(CONTINUITY_MOD.gate_hold(raw))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "continuity SQL gate mismatch"):
            raw.execute(
                "INSERT INTO assistant_attempts "
                "(id, task_id, fence, pool, reserved, actual, outcome, active_until, "
                "capability, gate_version, send_gate_version) "
                "VALUES ('missing-row', 'T-1', 1, 'demo', 100, NULL, 'reserved', 100.0, ?, ?, '')",
                (CAPABILITY, CONTINUITY_MOD.GATE_VERSION),
            )

        # Verify T-SQL parity constants retain BIN2 collation and set-based inserted/deleted joins.
        self.assertIn(
            "COLLATE Latin1_General_100_BIN2",
            MSSQLSTORE_MOD.TABLES["continuity_gate_state"],
        )
        self.assertTrue(
            all("NOT EXISTS" in trig for trig in ASSISTANTS_MOD.MSSQL_ATTEMPT_TRIGGERS[2:])
        )

    def test_corrupt_continuity_meta_and_sql_envelope_fail_closed_and_recover(self) -> None:
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        self.addCleanup(conn.close)

        # Persisted SQL meta('continuity') uses the versioned fail-closed outer envelope.
        raw_meta = conn.execute("SELECT value FROM meta WHERE key='continuity'").fetchone()[0]
        outer = json.loads(raw_meta)
        self.assertEqual(outer["gate_version"], CONTINUITY_MOD.GATE_VERSION)
        self.assertEqual(outer["epoch"], -1)
        self.assertEqual(CONTINUITY_MOD.unwrap_sql(outer)["epoch"], 0)
        self.assertEqual(CONTINUITY_MOD.load(None), CONTINUITY_MOD.blank())

        queued = self.service.invoke(ACTORS["PM-1"], CAPABILITY, "ZF-1")

        # Corrupting meta('continuity') fails closed across SqlStore and Assistants without
        # crashing _proc_sync or _discard, while manual casework continues uninterrupted.
        seq_now = int(conn.execute("SELECT value FROM meta WHERE key='seq'").fetchone()[0])
        conn.execute("UPDATE meta SET value='{corrupt-json' WHERE key='continuity'")
        conn.execute("UPDATE meta SET value=? WHERE key='seq'", (str(seq_now + 1),))

        self.assertEqual(self.store.continuity_epoch(), -1)
        hold = self.store.continuity_suspension(CAPABILITY)
        self.assertIsNotNone(hold)
        self.assertTrue(hold["invalid_history"])
        self.assertIsNone(self.service.claim(queued["id"], "corrupt-meta-worker"))
        with self.assertRaises(PermissionError):
            self.store.suspend(ACTORS["QI-1"], _incident(CAPABILITY))

        self.store.log_call(ACTORS["RLO-1"], "ZF-1", "Spoke", "SYN manual call during corrupt meta")
        self.assertEqual(
            self.store.cases["ZF-1"]["contacts"][-1]["note"],
            "SYN manual call during corrupt meta",
        )
        # _discard() also reloads corrupt meta('continuity') without raising JSONDecodeError.
        with self.store.lock:
            self.store._discard()
        self.assertEqual(self.store.continuity_epoch(), -1)

        # Restoring a valid wrapped continuity document recovers cleanly on next sync, and
        # sequential fast-path saves keep _proc_loaded aligned across non-continuity writes.
        seq_after = int(conn.execute("SELECT value FROM meta WHERE key='seq'").fetchone()[0])
        conn.execute("UPDATE meta SET value=? WHERE key='continuity'", (raw_meta,))
        conn.execute("UPDATE meta SET value=? WHERE key='seq'", (str(seq_after + 1),))
        self.assertEqual(self.store.continuity_epoch(), 0)
        self.assertIsNone(self.store.continuity_suspension(CAPABILITY))
        s_rec = self.store.suspend(ACTORS["QI-1"], _incident(CAPABILITY))
        self.assertEqual(s_rec["epoch"], 1)
        self.store.log_call(ACTORS["RLO-1"], "ZF-1", "Spoke", "SYN sequential fast-path save")
        self.assertEqual(self.store.continuity_epoch(), 1)

    def test_multiprocess_old_image_subprocess_cannot_claim_send_or_bypass_hold(self) -> None:
        queued = self.service.invoke(ACTORS["PM-1"], CAPABILITY, "ZF-1")
        leased_task = self.service.invoke(ACTORS["PM-1"], OTHER_CAPABILITY, "ZF-1")
        leased_claim = self.service.claim(leased_task["id"], "pre-upgrade-worker")
        self.assertIsNotNone(leased_claim)

        child_code = textwrap.dedent(
            """
            import json, sqlite3, sys
            from zava_forward.core import assistants, continuity
            from zava_forward.core.sqlstore import SqlStore

            seed_path, db_path, queued_id, leased_id, leased_fence = sys.argv[1:6]
            continuity.GATE_VERSION = "continuity-gate-v0-old-image"
            env = {
                "ZF_ASSIST_AUTHORITY": "local-nonbillable-test-authority",
                "ZF_ASSIST_EXPIRES": "2099-01-01T00:00:00Z",
                "ZF_ASSIST_CALL_ALLOWANCE": "100",
                "ZF_ASSIST_TOKEN_ALLOWANCE": "2000000",
                "ZF_ASSIST_PROACTIVE": "1",
            }
            class _FakeAi:
                configured = True
                sends_no_bytes = True
                provider = "local-test-double"
                endpoint = "local-test"
                fast = "test"
                strong = "test"
                model_version = "test-model"
                model_version_strong = "test-model"
                release = None
                def is_live(self, capability=None):
                    return True
            store = SqlStore(seed_path, db_path)
            store.ai = _FakeAi()
            svc = assistants.Assistants(store, env)
            try:
                results = {}
                try:
                    c = svc.claim(queued_id, "old-image-proc")
                    results["claim"] = "none" if c is None else "claimed"
                except Exception as exc:
                    results["claim"] = f"error:{type(exc).__name__}"
                with svc.transaction() as db:
                    try:
                        err = svc._fence_in(
                            db,
                            f"{leased_id}:{leased_fence}",
                            "assessment-preparation",
                        )
                        results["fence_in"] = f"returned:{err}"
                    except Exception as exc:
                        results["fence_in"] = f"error:{type(exc).__name__}"
                raw = sqlite3.connect(db_path, isolation_level=None)
                try:
                    raw.execute(
                        "INSERT INTO assistant_attempts "
                        "(id, task_id, fence, pool, reserved, actual, outcome, active_until) "
                        "VALUES ('legacy-8col', ?, 99, 'demo', 100, NULL, 'reserved', 9999999.0)",
                        (queued_id,),
                    )
                    results["raw_8col"] = "inserted"
                except sqlite3.IntegrityError:
                    results["raw_8col"] = "blocked"
                finally:
                    raw.close()
                print(json.dumps(results))
            finally:
                svc.stop()
            """
        )
        repo_src = Path(__file__).resolve().parents[2]
        py_paths = [
            str(repo_src / "core" / "src"),
            str(repo_src / "agents" / "src"),
            str(repo_src / "api" / "src"),
        ]
        if os.environ.get("PYTHONPATH"):
            py_paths.append(os.environ["PYTHONPATH"])
        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                child_code,
                self.seed_path,
                self.db_path,
                queued["id"],
                leased_task["id"],
                str(leased_claim["fence"]),
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": os.pathsep.join(py_paths)},
            check=True,
            timeout=30,
        )
        payload = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(payload["claim"], "none")
        self.assertTrue(
            payload["fence_in"].startswith("error:")
            or "gate version mismatch" in payload["fence_in"],
            payload,
        )
        self.assertEqual(payload["raw_8col"], "blocked")
        self.assertEqual(self.service.detail(ACTORS["PM-1"], queued["id"])["state"], "disabled")
