"""Exact issue 94 controls on tiny fictional local finance records."""

import copy
import json
import os
import tempfile
import threading
import unittest
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

import dataset
from test_finance_signoffs import STAFF, lines, person
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store

if TYPE_CHECKING:
    _TestCase = unittest.TestCase
else:
    _TestCase = object


class FinanceChecks(_TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.seed = Path(self.tmp.name) / "seed.json"
        data = copy.deepcopy(dataset.DATA)
        data["staff"] = copy.deepcopy(STAFF)
        self.a = person("PM-A", "Retrofit Programme Manager", oid="synthetic-a")
        self.b = person("PM-B", "Retrofit Programme Manager", oid="synthetic-b")
        self.alias = person("PM-ALIAS", "Retrofit Programme Manager", oid="synthetic-a")
        self.same_code = dict(self.b, email="alias-code@example.test")
        self.geo = person("GEO-1", "Grants and Evidence Officer")
        data["staff"].extend([self.a, self.b, self.alias, self.same_code])
        self.seed.write_text(json.dumps(data))
        self.store: Any = self.open()

    def open(self) -> Any:
        if self.sql:
            store = SqlStore(str(self.seed), str(self.seed.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.seed))

    def fin(self, user: dict[str, Any], action: str, **body: Any) -> None:
        self.store.finance_action(user, "ZF-1", dict(action=action, **body))

    def finance(self, store: Any = None) -> Any:
        return copy.deepcopy((store or self.store).detail("ZF-1").get("finance"))

    def funded(self, amount: int = 100) -> None:
        self.fin(self.a, "budget_propose", amount=amount)
        self.fin(self.b, "budget_approve")
        self.fin(
            self.a,
            "commit_raise",
            supplier="Fiction Ltd",
            contract="SYN-C",
            work_order="SYN-W",
            measure="Loft insulation",
            amount=amount,
            quantity=10,
        )
        self.fin(self.b, "commit_approve", id="COM-1")

    def invoice(self, ref: str = "SYN-I", amount: int = 60, milestone: str = "SYN-MS") -> str:
        self.fin(
            self.a,
            "invoice_receive",
            supplier="Fiction Ltd",
            work_order="SYN-W",
            ref=ref,
            lines=lines(qty=1, amount=amount, ms=milestone),
        )
        invoice_id: str = self.finance()["invoices"][-1]["id"]
        return invoice_id

    def accept(self, inv: str) -> None:
        self.fin(
            self.b, "disposition", id=inv, decision="Accept for payment", note="Synthetic review"
        )

    def test_same_role_different_humans_can_approve_but_oid_alias_cannot(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        before = self.finance()
        for user in (self.a, self.alias):
            with self.assertRaises(PermissionError):
                self.fin(user, "budget_approve")
            self.assertEqual(self.finance(), before)
        self.fin(self.b, "budget_approve")
        self.assertEqual(self.finance(self.open())["budget"]["status"], "Approved")

    def test_same_staff_code_with_different_email_and_oid_is_not_independent(self) -> None:
        self.fin(self.b, "budget_propose", amount=100)
        with self.assertRaises(PermissionError):
            self.fin(self.same_code, "budget_approve")

    def test_all_independent_finance_decisions_reject_same_oid_alias(self) -> None:
        self.funded()
        inv = self.invoice()
        self.fin(self.a, "invoice_match", id=inv)
        with self.assertRaises(PermissionError):
            self.fin(self.alias, "disposition", id=inv, decision="Accept for payment", note="x")
        self.fin(self.a, "hold_place", id=inv, reason="Synthetic query")
        with self.assertRaises(PermissionError):
            self.fin(self.alias, "hold_release", id=inv, note="x")
        self.fin(self.b, "hold_release", id=inv, note="Independent review")
        self.accept(inv)
        b_alias = dict(self.b, email="alias-code@example.test")
        with self.assertRaises(PermissionError):
            self.fin(b_alias, "payment_status", id=inv, status="Paid outside this system")

    def test_commitment_preparer_cannot_approve_through_oid_alias(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        self.fin(self.b, "budget_approve")
        self.fin(
            self.a,
            "commit_raise",
            supplier="Fiction Ltd",
            contract="SYN-C",
            work_order="SYN-W",
            measure="Loft insulation",
            amount=100,
            quantity=10,
        )
        with self.assertRaises(PermissionError):
            self.fin(self.alias, "commit_approve", id="COM-1")
        self.fin(self.b, "commit_approve", id="COM-1")

    def test_unknown_legacy_preparer_is_not_independent(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        with self.store.lock:
            case = self.store._case("ZF-1")
            case["finance"]["budget"].pop("proposed_identity", None)
            case["finance"]["budget"]["proposed_by"] = "unknown@example.test"
            self.store.save()
        with self.assertRaises(PermissionError):
            self.fin(self.b, "budget_approve")

    def test_every_exception_has_an_actual_line_including_aggregate_blockers(self) -> None:
        inv = self.invoice(milestone="")
        self.fin(self.a, "invoice_match", id=inv)
        errors = self.finance()["invoices"][0]["exceptions"]
        self.assertEqual(
            {e["code"] for e in errors}, {"no_budget", "no_commitment", "no_milestone"}
        )
        self.assertTrue(all(e["line"] == 0 for e in errors), errors)
        with self.assertRaises(ValueError):
            self.accept(inv)

    def test_ambiguous_commitment_never_selects_the_first(self) -> None:
        self.funded()
        with self.store.lock:
            case = self.store._case("ZF-1")
            second = dict(case["finance"]["commitments"][0], id="COM-2")
            case["finance"]["commitments"].append(second)
            self.store.save()
        inv = self.invoice()
        self.fin(self.a, "invoice_match", id=inv)
        invoice = self.finance()["invoices"][0]
        self.assertIsNone(invoice["commitment"])
        self.assertIn(
            ("ambiguous_commitment", 0), {(e["code"], e["line"]) for e in invoice["exceptions"]}
        )

    def test_acceptance_rechecks_totals_after_another_invoice_is_accepted(self) -> None:
        self.funded()
        first = self.invoice("SYN-1")
        second = self.invoice("SYN-2")
        for inv in (first, second):
            self.fin(self.a, "invoice_match", id=inv)
        self.accept(first)
        with self.assertRaises(ValueError):
            self.accept(second)
        self.assertIsNone(self.finance(self.open())["invoices"][1]["disposition"])

    def test_record_only_status_and_held_dispositions_preserve_other_ledgers(self) -> None:
        self.funded()
        with self.store.lock:
            case = self.store._case("ZF-1")
            case["grants"] = [{"id": "SYN-G", "state": "Cash received", "amount": 7}]
            self.store.save()
        inv = self.invoice()
        before = self.finance()
        grant = copy.deepcopy(self.store.cases["ZF-1"]["grants"])
        self.fin(self.a, "invoice_match", id=inv)
        self.fin(self.a, "hold_place", id=inv, reason="Synthetic hold")
        self.fin(self.b, "disposition", id=inv, decision="Keep on hold", note="Still unknown")
        held = self.finance()
        for action, body in (
            ("disposition", dict(decision="Accept for payment", note="x")),
            ("payment_status", dict(status="Paid outside this system")),
        ):
            with self.assertRaises(ValueError):
                self.fin(self.b, action, id=inv, **body)
            self.assertEqual(self.finance(self.open()), held)
        self.fin(self.b, "hold_release", id=inv, note="Resolved")
        self.accept(inv)
        for status in ("Awaiting payment run", "Paid outside this system"):
            self.fin(self.a, "payment_status", id=inv, status=status)
        after = self.finance(self.open())
        self.assertEqual(after["budget"], before["budget"])
        self.assertEqual(after["commitments"], before["commitments"])
        self.assertEqual(self.open().cases["ZF-1"]["grants"], grant)
        self.assertIn("never makes", after["invoices"][0]["payment_note"])
        self.assertTrue(self.store.verify_audit())


class JsonFinanceChecks(FinanceChecks, unittest.TestCase):
    def test_persistent_replace_failure_cannot_retain_a_success_audit(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        before = self.finance()
        entries = list(self.store.audit_entries())
        head = self.store.last_hash
        with patch(
            "zava_forward.core.store.os.replace",
            side_effect=PermissionError("Synthetic persistent replacement failure"),
        ):
            with self.assertRaises((OSError, RuntimeError)) as failed:
                self.fin(self.b, "budget_approve")
        if isinstance(failed.exception, RuntimeError):
            self.assertIn("outcome may be unknown", str(failed.exception))
        self.assertEqual(self.finance(), before)
        self.assertEqual(self.finance(self.open()), before)
        self.assertEqual(list(self.store.audit_entries()), entries)
        self.assertEqual(self.store.last_hash, head)
        self.fin(self.b, "budget_approve")
        self.assertTrue(self.open().verify_audit())

    def test_caught_save_and_audit_errors_restore_durable_state_and_chain(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        for method in ("save", "audit"):
            for after_write in (False, True):
                with self.subTest(method=method, after_write=after_write):
                    before = self.finance()
                    entries = list(self.store.audit_entries())
                    original = getattr(self.store, method)

                    def fail(
                        *args: Any,
                        after_write: bool = after_write,
                        original: Any = original,
                        **kwargs: Any,
                    ) -> None:
                        if after_write:
                            original(*args, **kwargs)
                        raise OSError("Synthetic failure")

                    with patch.object(self.store, method, side_effect=fail):
                        with self.assertRaises(OSError):
                            self.fin(self.b, "budget_approve")
                    self.assertEqual(self.finance(), before)
                    self.assertEqual(self.finance(self.open()), before)
                    self.assertEqual(list(self.store.audit_entries()), entries)
                    self.assertTrue(self.store.verify_audit())
        self.fin(self.b, "budget_approve")
        self.assertTrue(self.open().verify_audit())


class SqlFinanceChecks(FinanceChecks, unittest.TestCase):
    sql = True

    def test_fresh_permission_without_case_sequence_change_and_inside_save(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        before = self.finance()
        for during_save in (False, True):
            with self.subTest(during_save=during_save):
                original_save = self.store.save
                revoked = dict(self.b, role="Resident Liaison Officer")

                def revoke(revoked: dict[str, Any] = revoked) -> None:
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(revoked), self.b["email"]),
                    )

                def save(original_save: Any = original_save) -> None:
                    revoke()
                    original_save()

                try:
                    if during_save:
                        with patch.object(self.store, "save", side_effect=save):
                            with self.assertRaises(PermissionError):
                                self.fin(self.b, "budget_approve")
                    else:
                        revoke()
                        with self.assertRaises(PermissionError):
                            self.fin(self.b, "budget_approve")
                    self.assertEqual(self.finance(self.open()), before)
                    self.assertFalse(
                        any(
                            e["action"] == "finance_budget_approve"
                            for e in self.store.audit_entries()
                        )
                    )
                finally:
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(self.b), self.b["email"]),
                    )

    def test_sql_audit_failure_rolls_back_state_and_success_event(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        before = self.finance()
        original = self.store._append_audit

        def fail(entries: Any) -> None:
            original(entries)
            raise OSError("Synthetic audit failure")

        with patch.object(self.store, "_append_audit", side_effect=fail):
            with self.assertRaises(OSError):
                self.fin(self.b, "budget_approve")
        self.assertEqual(self.finance(self.open()), before)
        self.assertFalse(
            any(e["action"] == "finance_budget_approve" for e in self.store.audit_entries())
        )
        self.fin(self.b, "budget_approve")
        self.assertTrue(self.open().verify_audit())

    def test_competing_store_write_refuses_stale_approval_without_success_audit(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        other = self.open()
        original = self.store.save

        def race() -> None:
            other.finance_action(self.geo, "ZF-1", dict(action="budget_propose", amount=99))
            original()

        with patch.object(self.store, "save", side_effect=race):
            with self.assertRaises(ConflictError):
                self.fin(self.b, "budget_approve")
        self.assertEqual(self.finance(self.open())["budget"]["status"], "Proposed")
        self.assertEqual(self.finance()["budget"]["amount"], 99)
        self.assertFalse(
            any(e["action"] == "finance_budget_approve" for e in self.store.audit_entries())
        )

    def test_two_concurrent_acceptances_cannot_spend_the_same_budget(self) -> None:
        self.funded()
        first, second = self.invoice("SYN-1"), self.invoice("SYN-2")
        for inv in (first, second):
            self.fin(self.a, "invoice_match", id=inv)
        other = self.open()
        barrier = threading.Barrier(2)
        outcomes: list[str] = []

        def accept(store: Any, inv: str) -> None:
            original = store.save

            def save() -> None:
                barrier.wait(timeout=10)
                original()

            try:
                with patch.object(store, "save", side_effect=save):
                    store.finance_action(
                        self.b,
                        "ZF-1",
                        dict(action="disposition", id=inv, decision="Accept for payment", note="x"),
                    )
                outcomes.append("accepted")
            except ConflictError:
                outcomes.append("conflict")

        threads = [
            threading.Thread(target=accept, args=(self.store, first)),
            threading.Thread(target=accept, args=(other, second)),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=20)
            self.assertFalse(thread.is_alive())
        self.assertCountEqual(outcomes, ["accepted", "conflict"])
        invoices = self.finance(self.open())["invoices"]
        self.assertEqual(sum(i["disposition"] == "Accept for payment" for i in invoices), 1)
        self.assertTrue(self.open().verify_audit())

    def test_oid_revocation_without_case_sequence_change_refuses_write(self) -> None:
        self.fin(self.a, "budget_propose", amount=100)
        before = self.finance()
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?",
            (json.dumps(dict(self.b, oid="replacement-identity")), self.b["email"]),
        )
        with self.assertRaises(PermissionError):
            self.fin(self.b, "budget_approve")
        self.assertEqual(self.finance(self.open()), before)


@unittest.skipUnless(os.environ.get("ZF_FINANCE_MSSQL") == "1", "opt-in isolated local SQL Server")
class MssqlFinanceChecks(SqlFinanceChecks):
    def setUp(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        self.database = "zf_finance94_" + uuid.uuid4().hex
        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{self.database}]")

        def drop_owned_database() -> None:
            admin.execute(
                f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
            )
            admin.execute(f"DROP DATABASE [{self.database}]")

        self.addCleanup(drop_owned_database)
        os.environ["ZF_SQL_DATABASE"] = self.database
        super().setUp()

    def open(self) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        store = MssqlStore(str(self.seed), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store


if __name__ == "__main__":
    unittest.main()
