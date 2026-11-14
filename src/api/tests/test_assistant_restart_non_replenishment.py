"""Independent SQL workers and restarts cannot restore a revoked release or refill an allowance.

Issue #107, RAI criterion 8. Constructed fixtures only. A "worker" or "restart" is a fresh
`SqlStore` and `Assistants` over one file-backed SQLite database; the provider is a counting double.
"""

import threading
import unittest
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import release_support
from zava_forward.core import ai_registry, assistants
from zava_forward.core import assistant_release as rel
from zava_forward.core.assistants import Assistants

from test_assistant_release import CAP, assistants_proposal, body
from test_assistants import Base, config
from test_continuity import SUSPEND

LARGER = dict(call_allowance=1000, token_allowance=9000000, expires="2100-01-01T00:00:00Z")
ENVELOPE = dict(outcome="returned", source="ai", usage=None, model="test-model")


class Restart(Base):
    def setUp(self) -> None:
        super().setUp()
        self.qi = self.people["Quality Inspector"]

    def worker(self, **cfg: Any) -> Assistants:
        """A new store, connection and service: a separate worker or a restarted process."""
        return self.other(**cfg)

    def approver(self, **cfg: Any) -> Assistants:
        service = self.worker(**cfg)
        service.approvers = {self.pm["email"].lower()}
        return service

    def suspend(self, scope: str = "all") -> Any:
        store = self.open_store()
        self.addCleanup(store.db.close)
        return store.suspend(self.qi, dict(SUSPEND, scope=scope), self.service.affected(scope))

    def controlled(self) -> list[Any]:
        """Controlled domain records; the append-only audit of the suspension itself is excluded."""
        return [rows for i, rows in enumerate(self.domain()) if i != 3]

    def pool(self, service: Assistants) -> Any:
        with service.transaction() as db:
            return db.execute(
                "SELECT calls,tokens,used_calls,reserved_tokens FROM assistant_allowance"
            ).fetchone()

    def statuses(self, service: Assistants, cap: str = CAP) -> list[str]:
        with service.transaction() as db:
            return [r["status"] for r in rel.releases(db, cap)]


class RevocationAndSuspension(Restart):
    def test_suspension_on_one_connection_blocks_claim_dispatch_and_completion_on_others(
        self,
    ) -> None:
        queued = self.service.invoke(self.pm, CAP, "ZF-1")
        leased = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        task = self.service.claim(leased["id"], "worker-a")
        self.assertIsNotNone(task)
        calls, domain = self.provider.calls, self.controlled()
        self.suspend()

        for service in (self.worker(), self.worker(**LARGER)):
            self.assertIsNone(service.claim(queued["id"], "worker-b"))
            self.assertFalse(service.execute(queued["id"]))
            self.assertEqual(service.invoke(self.pm, CAP, "ZF-1")["state"], "disabled")
        self.assertEqual(self.provider.calls, calls)

        late = self.worker()
        self.assertTrue(late.complete(task, ENVELOPE, assistants_proposal(task)))
        view = self.worker(**LARGER).detail(self.pm, leased["id"])
        self.assertEqual((view["state"], view["output"]), ("quarantined", None))
        self.assertEqual(self.provider.calls, calls)
        self.assertEqual(self.controlled(), domain)

    def test_suspension_after_claim_stops_a_worker_paused_before_provider_dispatch(self) -> None:
        queued = self.service.invoke(self.pm, CAP, "ZF-1")
        worker = self.worker()
        original = worker._captured_sensors
        paused, proceed, results = threading.Event(), threading.Event(), []

        def pause(task: Any) -> Any:
            paused.set()
            proceed.wait(30)
            return original(task)

        worker._captured_sensors = pause
        thread = threading.Thread(target=lambda: results.append(worker.execute(queued["id"])))
        thread.start()
        try:
            self.assertTrue(paused.wait(30))
            self.suspend()
        finally:
            proceed.set()
            thread.join(30)
        self.assertEqual(results, [True])
        self.assertEqual(self.provider.calls, 0)
        view = self.worker(**LARGER).detail(self.pm, queued["id"])
        self.assertEqual((view["state"], view["output"]), ("quarantined", None))
        self.assertFalse(self.worker(**LARGER).execute(queued["id"]))
        self.assertEqual(self.provider.calls, 0)

    def test_revoked_or_suspended_release_stays_blocked_after_store_reopen(
        self,
    ) -> None:
        revoked = self.service.invoke(self.pm, CAP, "ZF-1")
        suspended = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        self.approver().change_release(self.pm, f"fx-{CAP}", "revoked", "withdrawn")
        self.approver().change_release(self.pm, "fx-assessment-preparation", "suspended", "paused")
        domain = self.domain()

        for generation in range(2):
            restarted = self.worker(**(LARGER if generation else {}))
            with self.subTest(generation=generation):
                self.assertEqual(self.statuses(restarted), ["revoked"])
                self.assertEqual(self.statuses(restarted, "assessment-preparation"), ["suspended"])
                for tid in (revoked["id"], suspended["id"]):
                    self.assertIsNone(restarted.claim(tid, "old-image"))
                    self.assertFalse(restarted.execute(tid))
                for cap in (CAP, "assessment-preparation"):
                    self.assertEqual(restarted.invoke(self.pm, cap, "ZF-1")["state"], "disabled")
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(self.domain(), domain)

    def test_old_image_cannot_reactivate_revoked_release_through_the_change_path(self) -> None:
        self.approver().change_release(self.pm, f"fx-{CAP}", "revoked", "withdrawn")
        old_image = self.approver(**LARGER)
        with self.assertRaises((ValueError, PermissionError)):
            old_image.change_release(self.pm, f"fx-{CAP}", "active", "stale registry default")
        self.assertEqual(self.statuses(self.worker()), ["revoked"])
        self.assertEqual(self.worker().invoke(self.pm, CAP, "ZF-1")["state"], "disabled")
        self.assertEqual(self.provider.calls, 0)

    def test_only_a_new_release_record_reenables_and_never_revives_the_old_task(self) -> None:
        old = self.service.invoke(self.pm, CAP, "ZF-1")
        self.approver().change_release(self.pm, f"fx-{CAP}", "revoked", "withdrawn")
        self.assertFalse(self.worker().execute(old["id"]))
        fresh = self.approver()
        fresh.record_release(self.pm, body(fresh, release_version="v2"))
        self.assertNotEqual(fresh.invoke(self.pm, CAP, "ZF-1")["state"], "disabled")
        self.assertFalse(self.worker().execute(old["id"]))
        self.assertEqual(self.statuses(self.worker()).count("revoked"), 1)


class Allowance(Restart):
    def spend(self, service: Assistants, cap: str, case: str = "ZF-1") -> dict[str, Any]:
        p = service.invoke(self.pm, cap, case)
        self.assertTrue(service.execute(p["id"]))
        return dict(p)

    def test_restart_cannot_replenish_consumed_calls_or_raise_the_stored_ceiling(self) -> None:
        caps = list(assistants.REGISTRY)[:3]
        first = self.worker(call_allowance=2)
        self.spend(first, caps[0])
        before = self.pool(first)
        self.assertEqual((before[0], before[2]), (2, 1))

        second = self.worker(**LARGER)
        self.spend(second, caps[1])
        stored = self.pool(second)
        self.assertEqual((stored[0], stored[1], stored[2]), (2, 2000000, 2))

        third_task = second.invoke(self.pm, caps[2], "ZF-1")
        for service in (second, self.worker(**LARGER), self.worker(call_allowance=1000)):
            self.assertFalse(service.execute(third_task["id"]))
        self.assertEqual(self.provider.calls, 2)
        self.assertEqual(self.pool(self.worker(**LARGER))[:3], (2, 2000000, 2))
        self.assertEqual(self.service.detail(self.pm, third_task["id"])["state"], "disabled")

    def test_restart_cannot_replenish_token_allowance(self) -> None:
        reservation = assistants.Limits(config()).reservation
        first = self.worker(token_allowance=reservation + 10)
        self.spend(first, CAP)
        stored = self.pool(first)
        self.assertLessEqual(stored[3] + reservation, stored[1] + stored[3])
        second = self.worker(**LARGER)
        blocked = second.invoke(self.pm, "assessment-preparation", "ZF-1")
        self.assertFalse(second.execute(blocked["id"]))
        self.assertEqual(self.provider.calls, 1)
        after = self.pool(second)
        self.assertEqual((after[1], after[2]), (stored[1], stored[2]))
        self.assertGreaterEqual(after[3], stored[3])

    def test_concurrent_connections_never_exceed_the_last_stored_call(self) -> None:
        seed = self.worker(call_allowance=1)
        tasks = [seed.invoke(self.pm, cap, "ZF-1")["id"] for cap in list(assistants.REGISTRY)[:3]]
        results, barrier = [], threading.Barrier(len(tasks))

        def run(tid: str) -> None:
            service = self.worker(call_allowance=1)
            barrier.wait(10)
            results.append(service.execute(tid))

        threads = [threading.Thread(target=run, args=(tid,)) for tid in tasks]
        for t in threads:
            t.start()
        for t in threads:
            t.join(60)
        self.assertEqual(sorted(results), [False, False, True])
        self.assertEqual(self.provider.calls, 1)
        row = self.pool(self.worker(**LARGER))
        self.assertEqual((row[0], row[2]), (1, 1))

    def test_revoked_release_keeps_its_consumed_allowance_and_a_new_record_does_not_refund_it(
        self,
    ) -> None:
        self.spend(self.worker(call_allowance=2), CAP)
        used = self.pool(self.service)
        self.approver().change_release(self.pm, f"fx-{CAP}", "revoked", "withdrawn")
        restarted = self.approver(**LARGER)
        restarted.record_release(self.pm, body(restarted, release_version="v2"))
        self.spend(restarted, CAP)
        after = self.pool(restarted)
        self.assertEqual((after[0], after[2]), (used[0], used[2] + 1))
        blocked = restarted.invoke(self.pm, "assessment-preparation", "ZF-1")
        self.assertFalse(restarted.execute(blocked["id"]))
        self.assertEqual(self.provider.calls, 2)
        self.assertEqual(self.pool(self.worker(**LARGER))[:3], (2, 2000000, 2))


class MaterialMismatch(Restart):
    def invoke_state(self, service: Assistants) -> str:
        try:
            return str(service.invoke(self.pm, CAP, "ZF-1")["state"])
        except PermissionError:
            return "disabled"

    @staticmethod
    def rescoped() -> Any:
        original = ai_registry.tasks

        def tasks() -> dict[str, Any]:
            out = original()
            out[CAP] = dict(out[CAP], scope="constructed different scope")
            return dict(out)

        return patch.object(ai_registry, "tasks", tasks)

    def variations(self) -> dict[str, Callable[[], Any]]:
        return {
            "prompt": lambda: patch.dict(
                assistants.REGISTRY[CAP],
                {"purpose": assistants.REGISTRY[CAP]["purpose"] + " (changed)"},
            ),
            "policy": lambda: patch.dict(
                assistants.RULES, {CAP: assistants.RULES[CAP] + " (changed)"}
            ),
            "permissions": lambda: patch.dict(
                assistants.REGISTRY[CAP], {"roles": (assistants.RC,)}
            ),
            "scope": self.rescoped,
            "version": lambda: patch.object(
                self.provider, "model_version", "different-model-version"
            ),
        }

    def test_mismatch_on_a_separate_worker_denies_dispatch_and_stays_denied_after_restart(
        self,
    ) -> None:
        for name, variation in self.variations().items():
            with self.subTest(variation=name):
                release_support.install(self.store)
                queued = self.service.invoke(self.pm, CAP, "ZF-1")
                domain, calls = self.domain(), self.provider.calls
                with variation():
                    changed = self.worker()
                    self.assertFalse(changed.execute(queued["id"]))
                    self.assertEqual(self.invoke_state(changed), "disabled")
                self.assertEqual(self.provider.calls, calls)
                self.assertEqual(self.statuses(self.worker()), ["revoked"])
                restarted = self.worker(**LARGER)
                self.assertFalse(restarted.execute(queued["id"]))
                self.assertEqual(self.invoke_state(restarted), "disabled")
                self.assertEqual(self.provider.calls, calls)
                self.assertEqual(self.domain(), domain)

    def test_mismatch_after_claim_quarantines_the_late_completion_without_domain_writes(
        self,
    ) -> None:
        for name, variation in self.variations().items():
            with self.subTest(variation=name):
                release_support.install(self.store)
                p = self.service.invoke(self.pm, CAP, "ZF-1")
                task = self.service.claim(p["id"], "worker-a")
                self.assertIsNotNone(task)
                domain = self.domain()
                with variation():
                    changed = self.worker()
                    self.assertTrue(changed.complete(task, ENVELOPE, assistants_proposal(task)))
                view = self.worker(**LARGER).detail(self.pm, p["id"])
                self.assertEqual((view["state"], view["output"]), ("quarantined", None))
                self.assertFalse(view["actionable"])
                self.assertEqual(self.domain(), domain)
                exported = {x["id"]: x for x in self.worker().export()["proposals"]}
                self.assertFalse(exported[p["id"]]["relied_on"])
        self.assertEqual(self.provider.calls, 0)


if __name__ == "__main__":
    unittest.main()
