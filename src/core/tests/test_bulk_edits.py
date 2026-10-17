"""Controlled administrative edits, using only temporary synthetic records."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA, change_metadata
from zava_forward.core import bulk_edits
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store

FORBIDDEN = (
    "technical",
    "consent",
    "decision",
    "safety",
    "hazards",
    "procurement",
    "budget",
    "invoices",
    "payments",
    "claims",
    "quality",
    "defects",
    "complaints",
    "contractor_instructions",
    "closed",
    "owner_code",
    "resident_update",
    "funding_ok",
    "documents",
    "handoff.state",
)


class JsonBulkEdits(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        self.path.write_text(json.dumps(copy.deepcopy(DATA)))
        self.store = self.open_store()
        self.sam, self.pam = copy.deepcopy(DATA["staff"])

    def open_store(self) -> Any:
        if self.sql:
            store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.path))

    def request(self, **overrides: Any) -> dict[str, Any]:
        return dict(
            dict(
                case_ids=["ZF-1", "ZF-2"],
                changes={"case_reason": "to review the supplied reference"},
                source="SYN-REGISTER",
                source_version="v3",
                reason="Synthetic correction",
            ),
            **overrides,
        )

    def preview(self, **overrides: Any) -> Any:
        return self.store.bulk_edit_preview(self.sam, self.request(**overrides))

    def apply(self, preview: Any, actor: Any = None) -> Any:
        return self.store.bulk_edit_apply(actor or self.sam, {"preview_id": preview["preview_id"]})

    def cases(self) -> Any:
        return copy.deepcopy(self.store.cases)

    def test_exact_preview_before_apply_and_provenance_reopens(self) -> None:
        before = self.cases()
        preview = self.preview()
        self.assertEqual(self.cases(), before)
        self.assertEqual(preview["status"], "pending")
        self.assertEqual([r["case_id"] for r in preview["records"]], ["ZF-1", "ZF-2"])
        row = preview["records"][0]
        self.assertEqual(row["outcome"], "would_apply")
        self.assertEqual(row["failures"], [])
        self.assertEqual(
            row["changes"],
            {
                "case_reason": {
                    "old": before["ZF-1"]["reason"],
                    "new": self.request()["changes"]["case_reason"],
                }
            },
        )
        result = self.apply(preview)
        self.assertEqual(result["status"], "applied")
        self.assertEqual([r["outcome"] for r in result["records"]], ["applied"] * 2)
        reopened = self.open_store()
        event = reopened.detail("ZF-1")["edit_history"][0]
        for key in ("source", "source_version", "reason"):
            self.assertEqual(event[key], self.request()[key])
        self.assertEqual(event["actor"]["email"], self.sam["email"])
        self.assertEqual(event["version"], 1)
        self.assertTrue(event["at"].endswith("+00:00"))
        self.assertEqual(event["changes"], row["changes"])
        entries = list(reopened.audit_entries())
        self.assertEqual(
            json.loads(next(e["detail"] for e in entries if e["action"] == "bulk_case_edited")),
            event,
        )
        self.assertTrue(reopened.verify_audit())
        with self.assertRaises(ConflictError):
            self.apply(preview)

    def test_mixed_missing_foreign_and_valid_has_all_outcomes_no_disclosure(self) -> None:
        before = self.cases()
        preview = self.preview(case_ids=["ZF-1", "ZF-5", "MISSING"])
        self.assertEqual(preview["status"], "blocked")
        self.assertEqual(
            [r["outcome"] for r in preview["records"]],
            ["batch_blocked", "blocked", "blocked"],
        )
        for row in preview["records"][1:]:
            self.assertEqual(row["changes"], {})
            self.assertTrue(row["failures"])
        with self.assertRaises(ConflictError):
            self.apply(preview)
        self.assertEqual(self.cases(), before)

    def test_closed_and_inactive_handoff_are_per_record_failures(self) -> None:
        with self.store.lock:
            self.store._case("ZF-1")["closed"] = True
            self.store.save()
        preview = self.preview(changes={"handoff_due_at": "2026-10-20T10:00:00Z"})
        self.assertEqual(preview["status"], "blocked")
        self.assertTrue(all(r["failures"] for r in preview["records"]))

    def test_handoff_edits_preserve_owner_decisions_and_resident_commitment(self) -> None:
        self.store.offer_handoff(
            self.sam,
            "ZF-1",
            self.pam["email"],
            metadata={
                **change_metadata(self.store, "ZF-1"),
                **{"due_at": "2026-10-19T10:00:00Z", "next_action": "Check reference"},
            },
        )
        before = self.cases()["ZF-1"]
        preview = self.preview(
            case_ids=["ZF-1"],
            changes={
                "handoff_due_at": "2026-10-20T11:00:00+01:00",
                "handoff_next_action": "Chase the administrative response",
            },
        )
        self.apply(preview)
        after = self.cases()["ZF-1"]
        for key in ("owner", "owner_code", "decision", "hazards", "resident_update"):
            self.assertEqual(after.get(key), before.get(key))
        self.assertEqual(after["handoff"]["state"], before["handoff"]["state"])
        self.assertEqual(after["handoff"]["due_at"], "2026-10-20T10:00+00:00")

    def test_noops_never_invent_history_or_edit_version(self) -> None:
        original = self.cases()
        preview = self.preview(changes={"case_reason": original["ZF-1"]["reason"]})
        self.assertTrue(all(r["outcome"] == "no_change" for r in preview["records"]))
        result = self.apply(preview)
        self.assertTrue(all(r["outcome"] == "no_change" for r in result["records"]))
        self.assertEqual(self.cases(), original)
        self.assertTrue(any(e["action"] == "bulk_edit_applied" for e in self.store.audit_entries()))

    def test_mixed_noop_and_changed_versions_are_exact(self) -> None:
        with self.store.lock:
            self.store._case("ZF-2")["reason"] = "Already correct"
            self.store.save()
        preview = self.preview(changes={"case_reason": "Already correct"})
        self.assertEqual([r["outcome"] for r in preview["records"]], ["would_apply", "no_change"])
        result = self.apply(preview)
        self.assertEqual([r["outcome"] for r in result["records"]], ["applied", "no_change"])
        self.assertEqual(self.store.cases["ZF-1"]["edit_history"][0]["version"], 1)
        self.assertNotIn("edit_history", self.store.cases["ZF-2"])
        second = self.preview(case_ids=["ZF-1"], changes={"case_reason": "Second correction"})
        self.apply(second)
        self.assertEqual([e["version"] for e in self.store.cases["ZF-1"]["edit_history"]], [1, 2])

    def test_every_controlled_field_and_unknown_input_refused_and_audited(self) -> None:
        before = self.cases()
        for field in FORBIDDEN + ("arbitrary",):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.preview(changes={"case_reason": "Allowed", field: "Approved"})
        invalid_requests: tuple[dict[str, Any], ...] = (
            {"case_ids": []},
            {"case_ids": ["ZF-1", "ZF-1"]},
            {"case_ids": [1]},
            {"case_ids": [f"ZF-{i}" for i in range(101)]},
            {"changes": {}},
            {"source": ""},
            {"source_version": 3},
            {"reason": "x" * 301},
            {"changes": {"handoff_due_at": "2026-10-20"}},
            {"changes": {"case_reason": {"nested": True}}},
            {"all": True},
        )
        for overrides in invalid_requests:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.preview(**overrides)
        self.assertEqual(self.cases(), before)
        self.assertTrue(
            any(e["action"] == "bulk_edit_rejected" for e in self.store.audit_entries())
        )
        self.assertNotIn("Approved", "".join(e["detail"] for e in self.store.audit_entries()))

    def test_actor_binding_and_payload_override(self) -> None:
        preview = self.preview()
        with self.assertRaises(PermissionError):
            self.apply(preview, self.pam)
        with self.assertRaises(ValueError):
            self.store.bulk_edit_apply(
                self.sam, {"preview_id": preview["preview_id"], "changes": {"technical": True}}
            )
        impostor = dict(self.sam, role="Retrofit Programme Manager")
        with self.assertRaises(PermissionError):
            self.store.bulk_edit_preview(impostor, self.request())

    def test_returned_or_cached_preview_cannot_change_instructions(self) -> None:
        preview = self.preview()
        preview["records"][0]["changes"]["case_reason"]["new"] = "Altered client value"
        self.apply(preview)
        self.assertEqual(
            self.store.cases["ZF-1"]["reason"], self.request()["changes"]["case_reason"]
        )
        other = self.preview(changes={"case_reason": "Second change"})
        self.store.data["bulk_edits"][other["preview_id"]]["issued"]["request"]["source"] = (
            "Altered"
        )
        with self.assertRaises(ConflictError):
            self.apply(other)

    def test_stale_target_and_owner_refused(self) -> None:
        preview = self.preview()
        with self.store.lock:
            self.store._case("ZF-1")["owner_code"] = "PM-01"
            self.store.save()
        with self.assertRaises(ConflictError):
            self.apply(preview)
        self.assertNotIn("edit_history", self.store.cases["ZF-2"])

    def test_edit_history_projection_hides_nested_free_text(self) -> None:
        self.apply(self.preview())
        viewer = dict(self.pam, role="Quality Inspector")
        detail = self.store.detail("ZF-1", viewer)
        self.assertNotIn("Synthetic correction", json.dumps(detail["edit_history"]))
        self.assertNotIn("SYN-REGISTER", json.dumps(detail["edit_history"]))
        self.assertNotIn("supplied reference", json.dumps(detail["edit_history"]))

    def test_issued_eligibility_requires_exact_records_snapshots_and_outcomes(self) -> None:
        preview = self.preview()
        original = copy.deepcopy(self.store.data["bulk_edits"][preview["preview_id"]]["issued"])
        invalid = []
        for failure in (["A retained rule failure"], None):
            issued = copy.deepcopy(original)
            issued["records"][0]["failures"] = failure
            invalid.append(issued)
        for outcome in ("blocked", "batch_blocked", "applied", "no_change"):
            issued = copy.deepcopy(original)
            issued["records"][0]["outcome"] = outcome
            invalid.append(issued)
        for records in (
            original["records"][:1],
            list(reversed(original["records"])),
            [original["records"][0]] * 2,
            original["records"] + [original["records"][0]],
        ):
            issued = copy.deepcopy(original)
            issued["records"] = records
            invalid.append(issued)
        for snapshots in (
            {},
            {"ZF-1": original["snapshots"]["ZF-1"]},
            dict(original["snapshots"], **{"FOREIGN": original["snapshots"]["ZF-1"]}),
        ):
            issued = copy.deepcopy(original)
            issued["snapshots"] = snapshots
            invalid.append(issued)
        for changes in (
            {},
            {"case_reason": {"old": "x", "new": "A different allowed change"}},
            {"case_reason": {"new": original["request"]["changes"]["case_reason"]}},
        ):
            issued = copy.deepcopy(original)
            issued["records"][0]["changes"] = changes
            invalid.append(issued)
        for index, issued in enumerate(invalid):
            with self.subTest(index=index), self.assertRaises(ConflictError):
                bulk_edits._applicable_request(issued)
        self.assertEqual(bulk_edits._applicable_request(original), original["request"])

    def test_all_active_handoff_states_and_noops_remain_permitted(self) -> None:
        for state in ("Offered", "Received", "Escalated", "Accepted"):
            with self.subTest(state=state):
                with self.store.lock:
                    case = self.store._case("ZF-1")
                    case["handoff"] = {"state": state, "next_action": "Existing chase"}
                    self.store.save()
                preview = self.preview(
                    case_ids=["ZF-1"], changes={"handoff_next_action": "An administrative chase"}
                )
                self.assertEqual(preview["status"], "pending")
                self.apply(preview)
                noop = self.preview(
                    case_ids=["ZF-1"], changes={"handoff_next_action": "An administrative chase"}
                )
                self.assertEqual(self.apply(noop)["records"][0]["outcome"], "no_change")
                self.assertEqual(self.store.cases["ZF-1"]["handoff"]["state"], state)


class SqlBulkEdits(JsonBulkEdits):
    sql = True

    def test_blocked_issuance_cannot_be_enabled_by_cached_or_persisted_status(self) -> None:
        for persisted in (False, True):
            for changes in (
                {"case_reason": "A blocked change"},
                {"case_reason": self.store.cases["ZF-1"]["reason"]},
            ):
                with self.subTest(persisted=persisted, changes=changes):
                    preview = self.preview(case_ids=["ZF-1", "ZF-5"], changes=changes)
                    self.assertEqual(preview["status"], "blocked")
                    before = self.cases()
                    successes = [
                        e
                        for e in self.store.audit_entries()
                        if e["action"] in ("bulk_case_edited", "bulk_edit_applied")
                    ]
                    if persisted:
                        rows = copy.deepcopy(self.store.data["bulk_edits"])
                        rows[preview["preview_id"]]["status"] = "pending"
                        self.store.db.execute(
                            "UPDATE meta SET value=? WHERE key='bulk_edits'", (json.dumps(rows),)
                        )
                        target = self.open_store()
                        with self.assertRaises(ConflictError):
                            target.bulk_edit_apply(self.sam, {"preview_id": preview["preview_id"]})
                    else:
                        with self.store.lock:
                            self.store.data["bulk_edits"][preview["preview_id"]]["status"] = (
                                "pending"
                            )
                            with self.assertRaises(ConflictError):
                                self.apply(preview)
                    reopened = self.open_store()
                    self.assertEqual(self.cases(), before)
                    self.assertEqual(reopened.cases, before)
                    self.assertEqual(
                        [
                            e
                            for e in reopened.audit_entries()
                            if e["action"] in ("bulk_case_edited", "bulk_edit_applied")
                        ],
                        successes,
                    )
                    self.assertEqual(
                        list(reopened.audit_entries())[-1]["action"], "bulk_edit_rejected"
                    )
                    self.assertTrue(reopened.verify_audit())
                    self.store = reopened

    def test_every_issued_target_including_noop_is_revalidated_inside_commit(self) -> None:
        with self.store.lock:
            self.store._case("ZF-2")["reason"] = "Already correct"
            self.store.save()
        preview = self.preview(changes={"case_reason": "Already correct"})
        eligibility_calls = []
        original = bulk_edits._eligible

        def observe(store: Any, user: Any, case: Any, changes: Any) -> None:
            eligibility_calls.append((case["id"], store.db.in_transaction))
            original(store, user, case, changes)

        with (
            patch.object(bulk_edits, "_eligible", side_effect=observe),
            patch.object(
                bulk_edits, "_applicable_request", wraps=bulk_edits._applicable_request
            ) as contract,
        ):
            result = self.apply(preview)
        self.assertEqual([r["outcome"] for r in result["records"]], ["applied", "no_change"])
        self.assertEqual(
            eligibility_calls,
            [("ZF-1", False), ("ZF-2", False), ("ZF-1", True), ("ZF-2", True)],
        )
        self.assertEqual(contract.call_count, 2)
        self.assertNotIn("edit_history", self.store.cases["ZF-2"])

    def test_commit_validator_independently_refuses_genuine_blocked_issuance(self) -> None:
        preview = self.preview(case_ids=["ZF-1", "ZF-5"])
        before = self.cases()
        issued = self.store.data["bulk_edits"][preview["preview_id"]]["issued"]
        with self.store.lock:
            self.store.data["bulk_edits"][preview["preview_id"]]["status"] = "pending"
            context = dict(
                user=self.sam,
                staff=issued["staff"],
                snapshots=issued["snapshots"],
                changes=issued["request"]["changes"],
                preview_id=preview["preview_id"],
                issued=issued,
            )
            with patch.object(
                bulk_edits, "_applicable_request", wraps=bulk_edits._applicable_request
            ) as contract:
                with self.assertRaises(ConflictError):
                    bulk_edits._save(self.store, context)
            self.assertEqual(contract.call_count, 1)
            self.assertIsNone(self.store.local.bulk_validation)
        reopened = self.open_store()
        self.assertEqual(reopened.cases, before)
        self.assertFalse(
            any(
                e["action"] in ("bulk_case_edited", "bulk_edit_applied")
                for e in reopened.audit_entries()
            )
        )
        self.assertTrue(reopened.verify_audit())

    def test_sql_preview_and_apply_recheck_revoked_deleted_and_oid_bound_actor(self) -> None:
        for mutation in ("role", "delete", "oid"):
            with self.subTest(mutation=mutation):
                preview = self.preview()
                original = json.dumps(self.sam)
                fresh = dict(
                    self.sam,
                    **({"role": "Contractor"} if mutation == "role" else {"oid": "new-oid"}),
                )
                if mutation == "delete":
                    self.store.db.execute("DELETE FROM staff WHERE email=?", (self.sam["email"],))
                else:
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(fresh), self.sam["email"]),
                    )
                with self.assertRaises(PermissionError):
                    self.preview()
                with self.assertRaises(PermissionError):
                    self.apply(preview)
                self.store.db.execute(
                    "INSERT OR REPLACE INTO staff(email,body) VALUES (?,?)",
                    (self.sam["email"], original),
                )

    def test_two_store_changed_away_and_back_is_stale(self) -> None:
        preview = self.preview()
        other = self.open_store()
        original = other.cases["ZF-1"]["reason"]
        for value in ("Changed away", original):
            with other.lock:
                other._case("ZF-1")["reason"] = value
                other.save()
        with self.assertRaises(ConflictError):
            self.apply(preview)

    def test_stored_preview_corruption_detected_on_reopen(self) -> None:
        preview = self.preview()
        rows = copy.deepcopy(self.store.data["bulk_edits"])
        rows[preview["preview_id"]]["issued"]["request"]["changes"]["case_reason"] = "Altered"
        self.store.db.execute("UPDATE meta SET value=? WHERE key='bulk_edits'", (json.dumps(rows),))
        other = self.open_store()
        with self.assertRaises(ConflictError):
            other.bulk_edit_apply(self.sam, {"preview_id": preview["preview_id"]})

    def test_consumed_noop_cannot_be_replayed_by_resetting_document_status(self) -> None:
        preview = self.preview(changes={"case_reason": self.store.cases["ZF-1"]["reason"]})
        self.apply(preview)
        rows = copy.deepcopy(self.store.data["bulk_edits"])
        rows[preview["preview_id"]]["status"] = "pending"
        self.store.db.execute("UPDATE meta SET value=? WHERE key='bulk_edits'", (json.dumps(rows),))
        other = self.open_store()
        with self.assertRaises(ConflictError):
            other.bulk_edit_apply(self.sam, {"preview_id": preview["preview_id"]})

    def test_failure_after_case_writes_or_document_or_audit_never_publishes_success(self) -> None:
        for hook in ("_proc_write", "_append_audit", "_refresh_queue_membership"):
            with self.subTest(hook=hook):
                preview = self.preview()
                before = self.cases()
                original = getattr(self.store, hook)

                def fail(*args: Any, original: Any = original, **kwargs: Any) -> Any:
                    original(*args, **kwargs)
                    raise RuntimeError("Synthetic write failure")

                with patch.object(self.store, hook, side_effect=fail):
                    with self.assertRaises(RuntimeError):
                        self.apply(preview)
                self.assertEqual(self.cases(), before)
                reopened = self.open_store()
                self.assertEqual(reopened.cases, before)
                self.assertEqual(
                    reopened.data["bulk_edits"][preview["preview_id"]]["status"], "pending"
                )
                self.assertFalse(
                    any(e["action"] == "bulk_case_edited" for e in reopened.audit_entries())
                )
                with self.store.lock:
                    self.store._case("ZF-5")["reason"] = "Unrelated save"
                    self.store.save()
                self.assertNotIn("edit_history", self.open_store().cases["ZF-1"])
                self.assertTrue(self.store.verify_audit())

    def test_first_preview_failure_restores_absence(self) -> None:
        with patch.object(self.store, "_proc_write", side_effect=RuntimeError("Synthetic failure")):
            with self.assertRaises(RuntimeError):
                self.preview()
        self.assertNotIn("bulk_edits", self.store.data)
        with self.store.lock:
            self.store._case("ZF-5")["reason"] = "Unrelated"
            self.store.save()
        self.assertNotIn("bulk_edits", self.open_store().data)

    def test_authority_revocation_between_prepare_and_commit_for_preview_and_apply(self) -> None:
        for applying in (False, True):
            with self.subTest(applying=applying):
                preview = self.preview()
                other = self.open_store()
                original_save = self.store.save
                before = self.cases()

                def revoke_then_save(
                    other: Any = other, original_save: Any = original_save
                ) -> None:
                    other.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(dict(self.sam, role="Contractor")), self.sam["email"]),
                    )
                    original_save()

                with patch.object(self.store, "save", side_effect=revoke_then_save):
                    with self.assertRaises(PermissionError):
                        self.apply(preview) if applying else self.preview()
                self.assertEqual(self.cases(), before)
                self.assertFalse(
                    any(e["action"] == "bulk_case_edited" for e in self.store.audit_entries())
                )
                other.db.execute(
                    "UPDATE staff SET body=? WHERE email=?",
                    (json.dumps(self.sam), self.sam["email"]),
                )
                self.assertTrue(self.store.verify_audit())

    def test_concurrent_guardrail_change_cannot_bypass_transaction_validation(self) -> None:
        preview = self.preview()
        other = self.open_store()
        original_save = self.store.save

        def pause_then_save() -> None:
            with other.lock:
                other.data.setdefault("governance", {}).setdefault("breaches", []).append(
                    dict(id="SYN-PAUSE", status="Paused", scope_kind="home", scope="ZF-1")
                )
                other.save()
            original_save()

        with patch.object(self.store, "save", side_effect=pause_then_save):
            with self.assertRaises(ConflictError):
                self.apply(preview)
        self.assertNotIn("edit_history", self.open_store().cases["ZF-1"])

    def test_two_store_apply_interleaving_commits_exactly_once_including_noops(self) -> None:
        for value in ("to agree a visit", "A new reason"):
            with self.subTest(value=value):
                preview = self.preview(changes={"case_reason": value})
                other = self.open_store()
                original_save = self.store.save

                def winner_then_save(
                    other: Any = other,
                    original_save: Any = original_save,
                    preview: Any = preview,
                ) -> None:
                    result = other.bulk_edit_apply(self.sam, {"preview_id": preview["preview_id"]})
                    self.assertEqual(result["status"], "applied")
                    original_save()

                with patch.object(self.store, "save", side_effect=winner_then_save):
                    with self.assertRaises(ConflictError):
                        self.apply(preview)
                events = [
                    json.loads(e["detail"])
                    for e in self.store.audit_entries()
                    if e["action"] == "bulk_edit_applied"
                ]
                self.assertEqual(sum(e["preview_id"] == preview["preview_id"] for e in events), 1)
                self.assertEqual(
                    self.open_store().data["bulk_edits"][preview["preview_id"]]["status"],
                    "applied",
                )

    def test_fault_after_first_row_and_before_commit_rolls_back_without_ghosts(self) -> None:
        for fail_at in ("first_row", "before_commit", "after_commit"):
            with self.subTest(fail_at=fail_at):
                preview = self.preview(changes={"case_reason": f"Synthetic {fail_at}"})
                before = self.cases()
                actual = self.store.db

                class FaultConnection:
                    fired = False

                    def __getattr__(self, name: str, connection: Any = actual) -> Any:
                        return getattr(connection, name)

                    def execute(
                        self,
                        sql: str,
                        parameters: tuple[Any, ...] = (),
                        mode: str = fail_at,
                        connection: Any = actual,
                    ) -> Any:
                        match = (
                            sql.startswith("UPDATE cases SET rowversion=")
                            if mode == "first_row"
                            else sql == "COMMIT"
                        )
                        if match and not self.fired:
                            self.fired = True
                            if mode != "before_commit":
                                connection.execute(sql, parameters)
                            raise RuntimeError("Synthetic transaction interruption")
                        return connection.execute(sql, parameters)

                with patch.object(self.store, "db", FaultConnection()):
                    with self.assertRaises((RuntimeError, self.store.dberror)):
                        self.apply(preview)
                reopened = self.open_store()
                persisted = reopened.data["bulk_edits"][preview["preview_id"]]
                if fail_at == "after_commit":
                    self.assertEqual(persisted["status"], "applied")
                    with self.assertRaises(ConflictError):
                        self.apply(preview)
                else:
                    self.assertEqual(persisted["status"], "pending")
                    self.assertEqual(reopened.cases, before)
                    self.assertEqual(self.cases(), before)
                with self.store.lock:
                    self.store._case("ZF-5")["reason"] = "Independent follow-on save"
                    self.store.save()
                self.assertTrue(self.open_store().verify_audit())
