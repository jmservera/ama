"""Issue 95: tiny synthetic authority, state separation and persistence probes."""

import copy
import json
import os
import tempfile
import unittest
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset
from test_finance_signoffs import STAFF, person
from zava_forward.core.grants import GRANT_STATES, require_authority
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store


def designate(user: dict[str, Any]) -> dict[str, Any]:
    """Explicit fixture authority only, never a production staff default."""
    result = copy.deepcopy(user)
    result["financial_authority"] = dict(
        kind="Synthetic exercise",
        status="Active",
        human=True,
        subject={key: user.get(key) for key in ("email", "code", "oid")},
        evidence_ref="SYN-95 delegation, not real authority",
        effective_from="2026-01-01T00:00:00+00:00",
        expires_at="2099-01-01T00:00:00+00:00",
        permissions=[
            dict(action=action, case_id="ZF-1", route="SYN-95")
            for action in (
                *("grant:" + state for state in GRANT_STATES),
                "application:approve",
                "application:submit",
                "application:confirm",
            )
        ],
    )
    return result


class GrantFixture:
    sql = False

    def setUp(self: Any) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.seed = Path(self.tmp.name) / "seed.json"
        data = copy.deepcopy(dataset.DATA)
        self.a = designate(person("PM-A", "Retrofit Programme Manager", oid="syn-a"))
        self.b = designate(person("PM-B", "Retrofit Programme Manager", oid="syn-b"))
        self.alias = designate(person("PM-ALIAS", "Retrofit Programme Manager", oid="syn-a"))
        self.same_code = designate(dict(self.b, email="same-code@example.test"))
        self.plain = person("PM-PLAIN", "Retrofit Programme Manager", oid="syn-plain")
        data["staff"] = [
            *copy.deepcopy(STAFF),
            self.a,
            self.b,
            self.alias,
            self.same_code,
            self.plain,
        ]
        self.seed.write_text(json.dumps(data))
        self.store = self.open()
        with self.store.lock:
            self.store._case("ZF-1")["funding"]["route"] = "SYN-95"
            self.store.save()

    def open(self: Any) -> Any:
        if self.sql:
            store = SqlStore(str(self.seed), str(self.seed.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.seed))

    def grant(self: Any, user: dict[str, Any], action: str, **body: Any) -> None:
        self.store.grant_action(user, "ZF-1", dict(action=action, **body))

    def opportunity(self: Any) -> None:
        self.grant(
            self.a,
            "grant_open",
            scheme="SYN-95",
            source="Unverified opportunity",
            amount=40_000_000,
        )
        self.grant(self.b, "grant_approve", id="GR-1")

    def record(self: Any, store: Any = None) -> dict[str, Any]:
        selected = store or self.store
        with selected.lock:
            return copy.deepcopy(selected.cases["ZF-1"])

    def staff(self: Any, user: dict[str, Any]) -> None:
        if self.sql:
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(user), user["email"])
            )
        else:
            self.store.staff[user["email"]] = copy.deepcopy(user)


class GrantChecks:
    def test_exact_effective_time_boundaries(self: Any) -> None:
        authority = self.b["financial_authority"]
        start = datetime.fromisoformat(authority["effective_from"])
        end = datetime.fromisoformat(authority["expires_at"])
        for now, allowed in (
            (start - timedelta(microseconds=1), False),
            (start, True),
            (end - timedelta(microseconds=1), True),
            (end, False),
        ):
            with (
                self.subTest(now=now),
                patch("zava_forward.core.grants.authority_now", return_value=now),
            ):
                if allowed:
                    self.assertEqual(
                        require_authority(
                            self.store, self.b, "grant:Opportunity", "ZF-1", "SYN-95"
                        ),
                        authority,
                    )
                else:
                    with self.assertRaises(PermissionError):
                        require_authority(self.store, self.b, "grant:Opportunity", "ZF-1", "SYN-95")

    def test_current_registered_actor_required_for_all_grant_writes(self: Any) -> None:
        self.opportunity()
        before = self.record()
        for user in (
            person("FAKE", "Retrofit Programme Manager"),
            dict(self.a, oid="forged"),
            dict(self.a, name="forged"),
        ):
            for action, body in (
                ("grant_open", dict(scheme="SYN-95", source="SYN")),
                ("grant_propose", dict(id="GR-1", to="Award", source="SYN")),
                ("grant_withdraw", dict(id="GR-1")),
            ):
                with self.subTest(action=action, user=user["email"]):
                    with self.assertRaises(PermissionError):
                        self.grant(user, action, **body)
        self.assertEqual(self.record(), before)

    def test_role_and_request_authority_are_not_designation(self: Any) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        with self.assertRaises(PermissionError):
            self.grant(
                self.plain,
                "grant_approve",
                id="GR-1",
                financial_authority=self.b["financial_authority"],
            )
        self.assertEqual(self.record()["grants"][0]["state"], "Not recorded")

    def test_exact_action_case_route_subject_and_validity(self: Any) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        for mutation in (
            dict(kind="Verified delegation"),
            dict(status="Proposed"),
            dict(human=False),
            dict(subject=dict(email="other", code="other", oid="other")),
            dict(effective_from="2099-01-01T00:00:00+00:00"),
            dict(expires_at="2020-01-01T00:00:00+00:00"),
            dict(expires_at="2099-01-01"),
            dict(evidence_ref=""),
            dict(permissions=[dict(action="grant:Cash received", case_id="ZF-1", route="SYN-95")]),
            dict(permissions=[dict(action="grant:Opportunity", case_id="ZF-2", route="SYN-95")]),
            dict(permissions=[dict(action="grant:Opportunity", case_id="ZF-1", route="OTHER")]),
        ):
            changed = copy.deepcopy(self.b)
            changed["financial_authority"].update(mutation)
            self.staff(changed)
            with self.subTest(mutation=mutation), self.assertRaises(PermissionError):
                self.grant(self.b, "grant_approve", id="GR-1")
        self.staff(self.b)
        with patch.dict(os.environ, ZF_ENV="production"), self.assertRaises(PermissionError):
            self.grant(self.b, "grant_approve", id="GR-1")
        self.grant(self.b, "grant_approve", id="GR-1")
        self.grant(self.a, "grant_propose", id="GR-1", to="Award", source="SYN award")
        changed = copy.deepcopy(self.b)
        changed["financial_authority"]["permissions"] = [
            dict(action="grant:Opportunity", case_id="ZF-1", route="SYN-95")
        ]
        self.staff(changed)
        with self.assertRaises(PermissionError):
            self.grant(self.b, "grant_approve", id="GR-1")

    def test_same_oid_or_code_is_not_independent(self: Any) -> None:
        for preparer, approver in ((self.a, self.alias), (self.b, self.same_code)):
            self.grant(preparer, "grant_open", scheme="SYN-95", source="SYN")
            gid = self.record()["grants"][-1]["id"]
            with self.assertRaises(PermissionError):
                self.grant(approver, "grant_approve", id=gid)

    def test_event_local_amount_currency_and_opportunity_projection(self: Any) -> None:
        self.opportunity()
        before = self.record()
        for currency in ("USD", "EUR", "", None, 42):
            with self.subTest(currency=currency), self.assertRaises(ValueError):
                self.grant(
                    self.a,
                    "grant_propose",
                    id="GR-1",
                    to="Award",
                    source="SYN award",
                    amount=1,
                    currency=currency,
                )
        self.assertEqual(self.record(), before)
        for target in ("Award", "Claimable", "Submitted", "Accepted", "Cash received"):
            self.grant(
                self.a,
                "grant_propose",
                id="GR-1",
                to=target,
                source="SYN " + target,
                amount=1 if target == "Cash received" else None,
            )
            self.grant(self.b, "grant_approve", id="GR-1")
        grant = self.record(self.open())["grants"][0]
        self.assertEqual(
            [h["amount"] for h in grant["history"]], [40_000_000, None, None, None, None, 1]
        )
        for event in grant["history"]:
            self.assertEqual(
                (event["case_id"], event["scheme"], event["currency"]), ("ZF-1", "SYN-95", "GBP")
            )
            self.assertEqual(event["proposed_identity"]["oid"], "syn-a")
            self.assertEqual(event["approved_identity"]["oid"], "syn-b")
            self.assertEqual(event["authority"]["kind"], "Synthetic exercise")
        self.assertNotIn("finance", self.record())
        self.assertEqual(self.record()["funding"], before["funding"])

    def test_legacy_pending_requires_reproposal_and_unknown_identity_refuses(self: Any) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        with self.store.lock:
            pending = self.store._case("ZF-1")["grants"][0]["pending"]
            pending.pop("identity", None)
            pending.pop("currency", None)
            self.store.save()
        with self.assertRaises(ValueError):
            self.grant(self.b, "grant_approve", id="GR-1")
        self.grant(self.a, "grant_withdraw", id="GR-1")
        self.grant(self.a, "grant_propose", id="GR-1", to="Opportunity", source="Re-attested SYN")
        with self.store.lock:
            pending = self.store._case("ZF-1")["grants"][0]["pending"]
            pending.pop("identity")
            pending["by"] = "missing@example.test"
            self.store.save()
        with self.assertRaises(PermissionError):
            self.grant(self.b, "grant_approve", id="GR-1")
        with self.store.lock:
            self.store._case("ZF-1")["grants"][0]["pending"]["by"] = self.a["email"]
            self.store.save()
        self.grant(self.b, "grant_approve", id="GR-1")
        self.assertEqual(len(self.record()["grants"][0]["history"]), 1)

    def test_grant_open_invalid_source_is_not_a_partial_write(self: Any) -> None:
        before = self.record()
        with self.assertRaises(ValueError):
            self.grant(self.a, "grant_open", scheme="SYN-95", source="")
        self.assertEqual(self.record(), before)
        self.assertEqual(self.record(self.open()), before)

    def test_grant_save_and_audit_failures_restore_state_and_ledger(self: Any) -> None:
        for action in ("grant_open", "grant_approve"):
            if action == "grant_approve":
                self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
            for method in ("audit", "save"):
                before, events = self.record(), list(self.store.audit_entries())
                error = RuntimeError("SYN injected failure")
                with patch.object(self.store, method, side_effect=error):
                    with self.assertRaises(RuntimeError) as raised:
                        self.grant(self.b, action, id="GR-1", scheme="SYN-95", source="SYN")
                self.assertIs(raised.exception, error)
                self.assertEqual(self.record(), before)
                self.assertEqual(self.record(self.open()), before)
                self.assertEqual(list(self.store.audit_entries()), events)
                self.assertTrue(self.store.verify_audit())

    def application_ready(self: Any) -> None:
        with self.store.lock:
            case = self.store._case("ZF-1")
            case["funding"].update(status="Draft ready", draft="SYN application")
            self.store.save()

    def test_application_authority_evidence_history_and_separation(self: Any) -> None:
        self.opportunity()
        self.application_ready()
        grants = self.record()["grants"]
        with patch.object(self.store, "checklist", return_value=[]):
            for action, user in (("approve", self.a), ("submit", self.b), ("confirm", self.a)):
                before = self.record()
                with self.assertRaises(PermissionError):
                    self.store.funding_step(self.plain, "ZF-1", action, "SYN")
                with self.assertRaises(ValueError):
                    self.store.funding_step(user, "ZF-1", action, "")
                self.assertEqual(self.record(), before)
                self.store.funding_step(user, "ZF-1", action, "SYN " + action)
                events = self.record(self.open())["funding"]["history"]
                self.assertEqual(events[-1]["action"], action)
                self.assertEqual(events[-1]["source"], "SYN " + action)
                self.assertEqual(events[-1]["actor"]["email"], user["email"])
                self.assertEqual(events[-1]["authority"], user["financial_authority"])
                self.assertEqual((events[-1]["case_id"], events[-1]["route"]), ("ZF-1", "SYN-95"))
        self.assertEqual(self.record()["grants"], grants)
        self.assertNotIn("finance", self.record())
        self.assertEqual(self.record()["grants"][0]["state"], "Opportunity")
        self.assertEqual(
            [e["action"] for e in self.record()["funding"]["history"]],
            ["approve", "submit", "confirm"],
        )
        row = next(r for r in self.store.funding_list(self.b) if r["id"] == "ZF-2")
        self.assertNotIn("40000000", json.dumps(row))
        self.assertNotIn("40000000", json.dumps(self.store.stats()))

    def test_each_application_transition_rolls_back_on_save_failure(self: Any) -> None:
        self.application_ready()
        with patch.object(self.store, "checklist", return_value=[]):
            for action in ("approve", "submit", "confirm"):
                before, audit = self.record(), list(self.store.audit_entries())
                with patch.object(self.store, "save", side_effect=RuntimeError("SYN failure")):
                    with self.assertRaises(RuntimeError):
                        self.store.funding_step(self.a, "ZF-1", action, "SYN " + action)
                self.assertEqual(self.record(), before)
                self.assertEqual(self.record(self.open()), before)
                self.assertEqual(list(self.store.audit_entries()), audit)
                self.store.funding_step(self.a, "ZF-1", action, "SYN " + action)

    def test_application_actions_cannot_borrow_other_scope_or_identity(self: Any) -> None:
        self.application_ready()
        for action in ("approve", "submit", "confirm"):
            for permission in (
                dict(action="application:save_draft", case_id="ZF-1", route="SYN-95"),
                dict(action="application:" + action, case_id="ZF-2", route="SYN-95"),
                dict(action="application:" + action, case_id="ZF-1", route="OTHER"),
            ):
                changed = copy.deepcopy(self.b)
                changed["financial_authority"]["permissions"] = [permission]
                self.staff(changed)
                before = self.record()
                with self.assertRaises(PermissionError):
                    self.store.funding_step(self.b, "ZF-1", action, "SYN")
                self.assertEqual(self.record(), before)
            self.staff(self.b)
            with self.assertRaises(PermissionError):
                self.store.funding_step(dict(self.b, oid="forged"), "ZF-1", action, "SYN")


class JsonGrantChecks(GrantFixture, GrantChecks, unittest.TestCase):
    pass


class SqlGrantChecks(GrantFixture, GrantChecks, unittest.TestCase):
    sql = True

    def test_legacy_preparer_is_reloaded_inside_grant_and_finance_transaction(self: Any) -> None:
        for path in ("grant", "finance"):
            for identifier in ("code", "oid"):
                with self.subTest(path=path, identifier=identifier):
                    if path == "grant":
                        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN legacy")
                        gid = self.record()["grants"][-1]["id"]
                        with self.store.lock:
                            self.store._case("ZF-1")["grants"][-1]["pending"].pop("identity")
                            self.store.save()
                    else:
                        with self.store.lock:
                            self.store._case("ZF-1").setdefault(
                                "finance", dict(commitments=[], invoices=[])
                            )["budget"] = None
                            self.store.save()
                        self.store.finance_action(
                            self.a, "ZF-1", dict(action="budget_propose", amount=100)
                        )
                        with self.store.lock:
                            self.store._case("ZF-1")["finance"]["budget"].pop("proposed_identity")
                            self.store.save()
                    before = self.record()
                    events = list(self.store.audit_entries())
                    original = self.store.save

                    def save(identifier: str = identifier, original: Any = original) -> None:
                        changed = copy.deepcopy(self.a)
                        changed[identifier] = self.b[identifier]
                        self.staff(changed)
                        original()

                    try:
                        with patch.object(self.store, "save", side_effect=save):
                            with self.assertRaises(PermissionError):
                                if path == "grant":
                                    self.grant(self.b, "grant_approve", id=gid)
                                else:
                                    self.store.finance_action(
                                        self.b, "ZF-1", dict(action="budget_approve")
                                    )
                        self.assertEqual(self.record(self.open()), before)
                        self.assertEqual(list(self.store.audit_entries()), events)
                        self.assertIsNone(self.store.local.finance_validation)
                        self.assertTrue(self.store.verify_audit())
                    finally:
                        self.staff(self.a)

    def test_transaction_rechecks_designation_change_and_clock_expiry(self: Any) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        before = self.record()
        original = self.store.save
        for changed in ("scope", "expiry"):

            def save(changed: str = changed) -> None:
                if changed == "scope":
                    user = copy.deepcopy(self.b)
                    user["financial_authority"]["evidence_ref"] = "replaced"
                    self.staff(user)
                with patch(
                    "zava_forward.core.grants.authority_now",
                    return_value=datetime(2100, 1, 1, tzinfo=UTC)
                    if changed == "expiry"
                    else datetime.now(UTC),
                ):
                    original()

            with patch.object(self.store, "save", side_effect=save):
                with self.assertRaises(PermissionError):
                    self.grant(self.b, "grant_approve", id="GR-1")
            self.assertEqual(self.record(self.open()), before)
            self.assertFalse(
                any(e["action"] == "finance_grant_approve" for e in self.store.audit_entries())
            )
            self.staff(self.b)
        self.grant(self.b, "grant_approve", id="GR-1")

    def test_rowversion_conflict_cannot_approve_stale_grant(self: Any) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        other = self.open()
        original = self.store.save

        def save() -> None:
            other.grant_action(self.a, "ZF-1", dict(action="grant_withdraw", id="GR-1"))
            original()

        with patch.object(self.store, "save", side_effect=save):
            with self.assertRaises(ConflictError):
                self.grant(self.b, "grant_approve", id="GR-1")
        self.assertEqual(self.record(self.open())["grants"][0]["state"], "Not recorded")
        self.assertTrue(self.store.verify_audit())

    def test_grant_and_application_audit_insert_and_recovery_failure(self: Any) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        with self.store.lock:
            self.store._case("ZF-1")["funding"].update(status="Submitted", reference="SYN submit")
            self.store.save()
        for action in ("finance_grant_approve", "funding_confirm"):
            for persistent in (False, True):
                before = self.record()
                entries = list(self.store.audit_entries())
                connection = self.store.db
                failed = False
                reads: list[str] = []
                error = RuntimeError("SYN actual audit INSERT failure")

                class FailingConnection:
                    def execute(
                        inner,
                        statement: str,
                        args: Any = (),
                        *,
                        connection: Any = connection,
                        action: str = action,
                        error: Exception = error,
                        reads: list[str] = reads,
                        persistent: bool = persistent,
                    ) -> Any:
                        nonlocal failed
                        if statement.startswith("INSERT INTO audit "):
                            result = connection.execute(statement, args)
                            if args[2] == action and not failed:
                                failed = True
                                raise error
                            return result
                        if failed and statement.startswith("SELECT rowversion, body FROM cases"):
                            reads.append(statement)
                            self.assertNotIn(action, [e[1] for e in self.store.local.pending])
                            self.assertFalse(self.store.local.touched)
                            if persistent or len(reads) == 1:
                                raise RuntimeError("SYN recovery read failure")
                        return connection.execute(statement, args)

                    def __getattr__(inner, name: str, connection: Any = connection) -> Any:
                        return getattr(connection, name)

                with (
                    self.subTest(action=action, persistent=persistent),
                    self.assertLogs("zava_forward.core", level="ERROR"),
                    patch.object(self.store, "db", FailingConnection()),
                ):
                    with self.assertRaises(RuntimeError) as caught, self.store.lock:
                        self.store.audit("synthetic", "prior_legitimate_note", "ZF-1", "SYN")
                        if action == "finance_grant_approve":
                            self.grant(self.b, "grant_approve", id="GR-1")
                        else:
                            self.store.funding_step(self.b, "ZF-1", "confirm", "SYN confirm")
                self.assertIs(caught.exception, error)
                self.assertTrue(reads)
                self.assertEqual(self.record(self.open()), before)
                actual = list(self.store.audit_entries())
                self.assertEqual(
                    [e["action"] for e in actual],
                    [e["action"] for e in entries] + ["prior_legitimate_note"],
                )
                self.assertIsNone(self.store.local.finance_validation)
                self.assertTrue(self.store.verify_audit())
        self.grant(self.b, "grant_approve", id="GR-1")
        self.store.funding_step(self.b, "ZF-1", "confirm", "SYN healthy confirm")
        self.assertEqual(
            sum(e["action"] == "finance_grant_approve" for e in self.store.audit_entries()), 1
        )
        self.assertEqual(
            sum(e["action"] == "funding_confirm" for e in self.store.audit_entries()), 1
        )


@unittest.skipUnless(os.environ.get("ZF_GRANT_MSSQL") == "1", "opt-in local SQL Server")
class MssqlGrantChecks(SqlGrantChecks):
    def setUp(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        database = "zf_grant95_" + uuid.uuid4().hex
        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{database}]")

        def drop_owned_database() -> None:
            admin.execute(f"ALTER DATABASE [{database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
            admin.execute(f"DROP DATABASE [{database}]")

        self.addCleanup(drop_owned_database)
        os.environ["ZF_SQL_DATABASE"] = database
        super().setUp()

    def open(self: Any) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        store = MssqlStore(str(self.seed), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store


if __name__ == "__main__":
    unittest.main()
