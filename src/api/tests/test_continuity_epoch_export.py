"""Synthetic epoch lifetime and offline evidence checks; no live provider use."""

import copy
import json
import os
import threading
import unittest
import urllib.request
import uuid
from typing import Any
from unittest.mock import patch

import release_support  # type: ignore[import-not-found]
from zava_forward.core import ai_tasks, continuity
from zava_forward.core.ai import Ai
from zava_forward.core.assistants import canonical

import test_assistants as fixtures
from test_assistants import Base, proposal
from test_continuity import SUSPEND


def complete_release_fixtures(test: Any) -> None:
    """Replace bare releases only in an isolated positive-proof test store."""
    with test.service.transaction() as db:
        bodies = [
            json.loads(row[0])
            for row in db.execute("SELECT body FROM assistant_releases").fetchall()
        ]
        db.execute("DELETE FROM assistant_releases")
    test.service.approvers = {test.pm["email"]}
    for body in bodies:
        test.service.record_release(test.pm, dict(body, expires="2099-01-01T00:00:00Z"))


class EpochTests(Base):
    def cycle(self: Any, store: Any = None) -> None:
        store = store or self.store
        s = store.suspend(self.people["Quality Inspector"], dict(SUSPEND, synthetic=True))
        store.restart_propose(
            self.pm, dict(id=s["id"], corrective_evidence="Constructed offline check only.")
        )
        store.restart_decide(
            self.people["Programme Support Officer"],
            dict(
                id=s["id"],
                epoch=store.continuity_epoch(),
                decision="Restart",
                authority_ref="Constructed fixture, not genuine authority",
            ),
        )

    def test_ready_and_accepted_history_never_revives(self) -> None:
        ready = self.verify(self.run_ready("stock-prioritisation"))
        accepted = self.verify(self.run_ready("assessment-preparation"))
        accepted = self.service.review(
            self.pm, accepted["id"], "accept", accepted["revision"], "Synthetic disposition."
        )
        self.cycle()
        for p in (ready, accepted):
            detail = self.service.detail(self.pm, p["id"])
            self.assertEqual(detail["state"], p["state"])
            self.assertFalse(detail["actionable"])
            self.assertFalse(detail["epoch_current"])
            listed = next(
                x for x in self.service.listing(self.pm)["proposals"] if x["id"] == p["id"]
            )
            self.assertFalse(listed["actionable"])
            for action in ("verify", "accept", "edit-accept"):
                with self.assertRaises((ValueError, PermissionError)):
                    self.service.review(
                        self.pm,
                        p["id"],
                        action,
                        p["revision"],
                        "Must not revive.",
                        output=proposal(p["snapshot"]),
                        source_verified=True,
                    )
        exported = self.service.export()
        self.assertTrue(all(not x["relied_on"] for x in exported["proposals"]))
        fresh = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.assertNotEqual(fresh["id"], ready["id"])
        self.assertTrue(self.service.execute(fresh["id"]))
        rejected = self.service.review(
            self.pm, ready["id"], "reject", ready["revision"], "Retain rejected history."
        )
        self.assertEqual(rejected["state"], "rejected")

    def test_old_queued_leased_and_missing_epoch_cannot_be_claimed(self) -> None:
        queued = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        leased = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        claim = self.service.claim(leased["id"], "old-process")
        self.cycle()
        other = self.other()
        self.assertIsNone(other.claim(queued["id"], "new-process"))
        self.assertTrue(
            other.complete(
                claim,
                dict(outcome="returned", source="ai", usage=None, model="test-model"),
                proposal(claim["snapshot"]),
            )
        )
        self.assertEqual(other.detail(self.pm, leased["id"])["state"], "quarantined")
        with other.transaction() as db:
            attempt = db.execute(
                "SELECT actual,reserved FROM assistant_attempts WHERE task_id=?", (leased["id"],)
            ).fetchone()
            self.assertIsNone(attempt[0])
            self.assertGreater(attempt[1], 0)
        fresh = other.invoke(self.pm, "funding-evidence", "ZF-1")
        with other.transaction() as db:
            body = other._row(db, fresh["id"])
            body.pop("continuity_epoch", None)
            body.pop("claim_epoch", None)
            db.execute(
                "UPDATE assistant_tasks SET body=? WHERE id=?", (canonical(body), fresh["id"])
            )
        self.assertIsNone(other.claim(fresh["id"], "unbound"))

    def test_old_process_epoch_reads_persisted_restart(self) -> None:
        other = self.other()
        self.assertEqual(other.store.continuity_epoch(), 0)
        self.cycle()
        self.assertEqual(other.store.continuity_epoch(), 2)

    def test_missing_historical_epoch_and_export_collection_race_fail_closed(self) -> None:
        p = self.verify(self.run_ready("stock-prioritisation"))
        self.service.review(
            self.pm, p["id"], "accept", p["revision"], "Historical synthetic acceptance."
        )
        collected = self.service.export()
        self.assertTrue(collected["proposals"][0]["relied_on"])
        self.cycle()
        bundle = self.store.continuity_export(self.pm, collected)
        self.assertFalse(bundle["assistant_proposals"][0]["relied_on"])
        fresh = self.run_ready("assessment-preparation")
        with self.service.transaction() as db:
            body = self.service._row(db, fresh["id"])
            body.pop("continuity_epoch", None)
            body.pop("claim_epoch", None)
            db.execute(
                "UPDATE assistant_tasks SET body=? WHERE id=?", (canonical(body), fresh["id"])
            )
        self.assertFalse(self.service.detail(self.pm, fresh["id"])["actionable"])
        with self.assertRaises(PermissionError):
            self.verify(fresh)

    def test_restart_between_claim_and_dispatch_prevents_provider_call(self) -> None:
        original = self.service.claim

        def claim_then_cycle(*args: Any) -> Any:
            result = original(*args)
            self.cycle(self.other().store)
            return result

        pending = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        with patch.object(self.service, "claim", side_effect=claim_then_cycle):
            self.service.execute(pending["id"])
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(self.service.detail(self.pm, pending["id"])["state"], "quarantined")

    def test_proactive_scan_creates_epoch_distinct_work(self) -> None:
        before = set(self.service.scan()["enqueued"])
        self.assertTrue(before)
        self.cycle()
        after = set(self.service.scan()["enqueued"])
        self.assertTrue(after)
        self.assertFalse(before & after)

    def test_overlapping_review_suspend_restart_retains_noncurrent_disposition(self) -> None:
        p = self.verify(self.run_ready("stock-prioritisation"))
        other = self.other()
        entered, competing, release = threading.Event(), threading.Event(), threading.Event()
        results: list[Any] = []
        errors: list[Exception] = []
        original = self.service._view

        def held_view(*args: Any) -> Any:
            result = original(*args)
            entered.set()
            self.assertTrue(competing.wait(10))
            self.assertTrue(release.wait(10))
            return result

        def review() -> None:
            try:
                results.append(
                    self.service.review(
                        self.pm, p["id"], "accept", p["revision"], "Overlapping fixture review."
                    )
                )
            except Exception as error:
                errors.append(error)

        def suspend_restart() -> None:
            competing.set()
            try:
                self.cycle(other.store)
            except Exception as error:
                errors.append(error)

        with patch.object(self.service, "_view", side_effect=held_view):
            first = threading.Thread(target=review)
            first.start()
            self.assertTrue(entered.wait(10))
            second = threading.Thread(target=suspend_restart)
            second.start()
            self.assertTrue(competing.wait(10))
            release.set()
            first.join(20)
            second.join(20)
        self.assertFalse(first.is_alive() or second.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 1)
        final = other.detail(self.pm, p["id"])
        self.assertEqual(final["state"], "accepted")
        self.assertFalse(final["actionable"])
        self.assertFalse(other.export()["proposals"][0]["relied_on"])

    def test_inflight_completion_overlaps_suspend_restart_and_keeps_unknown_liability(self) -> None:
        entered, release = threading.Event(), threading.Event()
        errors = []
        other = self.other()

        def provider(*args: Any) -> dict[str, Any]:
            entered.set()
            self.assertTrue(release.wait(10))
            return dict(
                text=canonical(proposal({})),
                provider="local-test-double",
                deployment="test",
                model="test-model",
                source="ai",
                outcome="returned",
                usage=None,
            )

        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")

        def execute() -> None:
            try:
                self.service.execute(p["id"])
            except Exception as error:
                errors.append(error)

        with patch.object(self.service, "provider", side_effect=provider):
            thread = threading.Thread(target=execute)
            thread.start()
            self.assertTrue(entered.wait(10))
            self.cycle(other.store)
            release.set()
            thread.join(20)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        detail = other.detail(self.pm, p["id"])
        self.assertEqual(detail["state"], "quarantined")
        self.assertIsNone(detail["output"])
        with other.transaction() as db:
            row = db.execute(
                "SELECT actual,reserved,outcome FROM assistant_attempts WHERE task_id=?", (p["id"],)
            ).fetchone()
        self.assertIsNone(row[0])
        self.assertGreater(row[1], 0)
        self.assertEqual(row[2], "returned")


class LegacyTests(Base):
    cycle = EpochTests.cycle

    def prepare_ai(self: Any, store: Any) -> None:
        store.ai = Ai()
        store.ai.endpoint = "http://offline-script.invalid"
        store.ai._chat = lambda *args, **kwargs: "- Fixture [[Stage: Contacting resident]]"
        release_support.install(store)

    def test_legacy_review_and_priority_reliance_do_not_revive(self) -> None:
        self.prepare_ai(self.store)
        output = self.store.ai_run(self.pm, "ZF-1", "summary")
        self.cycle()
        with self.assertRaises(PermissionError):
            self.store.review_ai(self.pm, output["record_id"], "accept")
        with self.assertRaises(PermissionError):
            self.store.review_ai(self.pm, output["record_id"], "edit", "Stale", "Not current")
        rejected = self.store.review_ai(self.pm, output["record_id"], "reject", "Stale epoch")
        self.assertEqual(rejected["status"], "Rejected")

    def test_legacy_text_document_priority_publication_race(self) -> None:
        for task in ("summary", "read_document", "priority"):
            with self.subTest(task=task):
                self.prepare_ai(self.store)
                other = self.other()
                # Give the manager one synthetic owned case for the legacy priority route.
                with self.store.lock:
                    self.store._case("ZF-1").update(
                        owner_code=self.pm["code"], owner=self.pm["name"]
                    )
                    self.store.save()
                start = self.store.continuity_epoch()
                entered, release = threading.Event(), threading.Event()
                results: list[Any] = []
                errors: list[Exception] = []
                original = self.store.save
                armed = [True]
                existing_ids = {r["id"] for r in self.store.data["recommendations"]}

                def blocked_save(
                    armed: list[bool] = armed,
                    entered: threading.Event = entered,
                    release: threading.Event = release,
                    original: Any = original,
                    existing_ids: set[str] = existing_ids,
                ) -> Any:
                    if armed[0] and any(
                        r["id"] not in existing_ids for r in self.store.data["recommendations"]
                    ):
                        armed[0] = False
                        entered.set()
                        self.assertTrue(release.wait(15))
                    return original()

                def publish(
                    task: str = task,
                    start: int = start,
                    results: list[Any] = results,
                    errors: list[Exception] = errors,
                ) -> None:
                    try:
                        if task == "priority":
                            self.store.ai._chat = lambda *a, **k: json.dumps(
                                [
                                    dict(
                                        case_id="ZF-1",
                                        reason="Fixture",
                                        cites=["Stage: Contacting resident"],
                                    )
                                ]
                            )
                            result = self.store.ai_priority(self.pm, 1)
                        else:
                            # Both retained text and document routes publish through finish.
                            result = ai_tasks.finish(
                                self.store,
                                self.pm,
                                task,
                                ["ZF-1"],
                                dict(
                                    text="Fixture [[Stage: Contacting resident]]",
                                    source="ai",
                                    model=self.store.ai.fast,
                                    latency_ms=1,
                                    validated=True,
                                    release=self.store.release_context(task),
                                ),
                                "Manual fixture",
                                {"ZF-1": ["Stage: Contacting resident"]},
                                record_cites=["Stage: Contacting resident"]
                                if task == "read_document"
                                else None,
                                epoch0=start,
                            )
                        results.append(result)
                    except Exception as error:
                        errors.append(error)

                with patch.object(self.store, "save", side_effect=blocked_save):
                    thread = threading.Thread(target=publish)
                    thread.start()
                    self.assertTrue(entered.wait(15))
                    self.cycle(other.store)
                    release.set()
                    thread.join(25)
                self.assertFalse(thread.is_alive())
                self.assertEqual(errors, [])
                self.assertEqual(len(results), 1)
                with other.store.lock:
                    records = [
                        r
                        for r in other.store.data["recommendations"]
                        if r["id"] not in existing_ids
                    ]
                self.assertEqual(len(records), 1)
                self.assertEqual(records[0]["status"], "Quarantined")
                self.assertEqual(records[0]["continuity_epoch"], start)
                self.assertIsNotNone(records[0]["ai_output"])
                if task != "priority":
                    self.assertEqual(results[0]["source"], "template")
                    self.assertEqual(results[0]["text"], "Manual fixture")
                else:
                    self.assertFalse(results[0]["actionable"])
                self.assertFalse(
                    self.store.continuity_export(self.pm, self.service.export())["ai_records"][-1][
                        "relied_on"
                    ]
                )

    def test_legacy_priority_ready_accepted_missing_epoch_and_cache(self) -> None:
        self.prepare_ai(self.store)
        with self.store.lock:
            self.store._case("ZF-1").update(owner_code=self.pm["code"], owner=self.pm["name"])
            self.store.save()
        calls = []

        def scripted(*args: Any, **kwargs: Any) -> str:
            calls.append(1)
            return json.dumps(
                [dict(case_id="ZF-1", reason="Fixture", cites=["Stage: Contacting resident"])]
            )

        self.store.ai._chat = scripted
        ready = self.store.ai_priority(self.pm, 1)
        self.assertEqual(ready["source"], "ai")
        accepted = self.store.resolve_priority(self.pm, ready["id"], "accept")
        self.assertEqual(accepted["status"], "Accepted")
        self.cycle()
        self.assertFalse(self.store.latest_priority(self.pm)["actionable"])
        self.assertEqual(self.store.latest_priority(self.pm)["status"], "Accepted")
        new = self.store.ai_priority(self.pm, 1)
        with self.store.lock:
            rec = next(r for r in self.store.data["recommendations"] if r["id"] == new["id"])
            rec.pop("continuity_epoch")
            self.store.save()
        with self.assertRaises(PermissionError):
            self.store.resolve_priority(self.pm, new["id"], "accept")
        # Same process/version cache cannot outlive epoch, including external writes.
        self.store.ai._chat = lambda *a, **k: "Fixture [[Stage: Contacting resident]]"
        briefing = self.store.briefing(self.pm)
        old = self.other()
        self.cycle(old.store)
        refreshed = self.store.briefing(self.pm)
        self.assertNotEqual(briefing["record_id"], refreshed["record_id"])


class OfflineTests(Base):
    cycle = EpochTests.cycle

    def setUp(self) -> None:
        super().setUp()
        complete_release_fixtures(self)

    def bundle(self) -> tuple[dict[str, Any], str]:
        cap = "stock-prioritisation"
        self.service.approvers = {self.pm["email"]}
        from zava_forward.core.assistants import runtime_binding

        body = release_support.fixture(cap, runtime_binding(cap, self.store.ai))
        body["expires"] = "2099-01-01T00:00:00Z"
        released = self.service.record_release(self.pm, body)
        p = self.verify(self.run_ready(cap))
        self.service.review(self.pm, p["id"], "accept", p["revision"], "Synthetic only.")
        self.service.change_release(self.pm, released["id"], "revoked", "Synthetic end.")
        result = json.loads(
            json.dumps(self.store.continuity_export(self.pm, self.service.export()))
        )
        self.assertTrue(continuity.verify_export(result)["valid"], result["incomplete_reasons"])
        return result, released["id"]

    def redigest(self, bundle: dict[str, Any]) -> dict[str, Any]:
        bundle["complete"] = True
        bundle["incomplete_reasons"] = []
        bundle["digest"] = continuity.sha({k: v for k, v in bundle.items() if k != "digest"})
        return dict(continuity.verify_export(bundle))

    def test_release_snapshot_and_lifecycle_verify_offline_after_revocation(self) -> None:
        bundle, rid = self.bundle()
        record = next(r for r in bundle["task_releases"]["records"] if r["id"] == rid)
        self.assertEqual(record["snapshot"]["status"], "active")
        self.assertEqual(record["current_status"], "revoked")
        self.assertEqual(record["revision"], 2)
        self.assertEqual(len(record["events"]), 2)
        self.assertTrue(
            all(e["id"] and e["at"] and e["release_id"] == rid for e in record["events"])
        )
        self.assertFalse(bundle["assistant_proposals"][0]["relied_on"])
        with patch.object(
            self.store, "assistant_connection", side_effect=AssertionError("offline")
        ):
            self.assertTrue(continuity.verify_export(bundle, bundle["ledger"]["head"])["valid"])
        text = json.dumps(bundle)
        for private in (
            "PRIVATE-VULNERABILITY-REASON",
            "PRIVATE-HANDOFF-NOTE",
            "PRIVATE-DOCUMENT-NAME",
        ):
            self.assertNotIn(private, text)

    def test_recomputed_digest_cannot_mask_missing_mismatched_or_truncated_releases(self) -> None:
        original, rid = self.bundle()
        for defect in (
            "missing",
            "snapshot",
            "version",
            "event",
            "truncated",
            "association",
            "status",
            "envelope",
        ):
            with self.subTest(defect=defect):
                bundle = copy.deepcopy(original)
                record = next(r for r in bundle["task_releases"]["records"] if r["id"] == rid)
                if defect == "missing":
                    bundle["task_releases"]["records"].remove(record)
                elif defect == "snapshot":
                    record["snapshot"]["impact_assessment"] = "Forged"
                elif defect == "version":
                    bundle["assistant_proposals"][0]["release"]["version"] = "forged"
                elif defect == "event":
                    record["events"].pop()
                elif defect == "truncated":
                    record["truncated"] = True
                elif defect == "association":
                    record["events"][0]["release_id"] = "wrong"
                elif defect == "envelope":
                    bundle["assistant_proposals"][0]["envelope"]["release"]["digest"] = "wrong"
                else:
                    record["current_status"] = "suspended"
                self.assertFalse(self.redigest(bundle)["valid"])

    def test_producer_marks_missing_and_bounded_release_evidence_incomplete(self) -> None:
        _, rid = self.bundle()
        for mode in ("missing", "events", "releases", "unavailable"):
            with self.subTest(mode=mode):
                part = self.service.export()
                if mode == "missing":
                    part["task_releases"]["records"] = [
                        r for r in part["task_releases"]["records"] if r["id"] != rid
                    ]
                elif mode == "events":
                    part = self.service.export(event_limit=1)
                elif mode == "releases":
                    part = self.service.export(release_limit=0)
                else:
                    part.pop("task_releases")
                bundle = self.store.continuity_export(self.pm, part)
                self.assertFalse(bundle["complete"])
                self.assertFalse(continuity.verify_export(bundle)["valid"])

    def test_legacy_top_level_release_and_collection_restart_are_retained(self) -> None:
        LegacyTests.prepare_ai(self, self.store)
        result = self.store.ai_run(self.pm, "ZF-1", "summary")
        part = self.service.export()
        self.cycle()
        bundle = self.store.continuity_export(self.pm, part)
        record = next(r for r in bundle["ai_records"] if r["id"] == result["record_id"])
        self.assertEqual(record["release"], result["release"])
        self.assertFalse(record["relied_on"])
        self.assertFalse(record["actionable"])

    def test_original_review_missing_and_truncated_proposals_with_unchanged_head(self) -> None:
        original, _ = self.bundle()
        head = copy.deepcopy(original["ledger"]["head"])
        missing = copy.deepcopy(original)
        del missing["assistant_proposals"]
        truncated = json.loads(
            json.dumps(self.store.continuity_export(self.pm, self.service.export(limit=0)))
        )
        # Use each bundle's separately retained head; neither negative rewrites its ledger.
        for bundle in (missing, truncated):
            with self.subTest(truncated="assistant_proposals" in bundle):
                expected = head if bundle is missing else copy.deepcopy(bundle["ledger"]["head"])
                self.redigest(bundle)
                check = continuity.verify_export(bundle, expected)
                self.assertFalse(check["valid"], check)
                self.assertFalse(
                    any("digest" in p or "externally held head" in p for p in check["problems"])
                )

    def test_proposal_metadata_shapes_counts_and_source_status_fail_closed(self) -> None:
        original, _ = self.bundle()
        changes: list[tuple[str, Any]] = [
            ("supported", None),
            ("supported", 1),
            ("supported", "true"),
            ("total", None),
            ("total", True),
            ("total", -1),
            ("total", 1.0),
            ("total", "1"),
            ("exported", False),
            ("exported", -1),
            ("exported", 0),
            ("total", 2),
            ("truncated", 0),
            ("truncated", "false"),
            ("truncated", True),
            ("source_status", "unavailable"),
            ("source_status", "unsupported"),
            ("source_status", None),
        ]
        for key, value in changes:
            with self.subTest(key=key, value=value):
                bundle = copy.deepcopy(original)
                bundle["assistants"][key] = value
                self.redigest(bundle)
                self.assertFalse(
                    continuity.verify_export(bundle, original["ledger"]["head"])["valid"]
                )
        for field, value in (
            ("assistant_proposals", None),
            ("assistant_proposals", {}),
            ("assistant_proposals", [None]),
            ("assistants", None),
            ("assistants", []),
        ):
            with self.subTest(field=field, value=value):
                bundle = copy.deepcopy(original)
                bundle[field] = value
                self.redigest(bundle)
                self.assertFalse(
                    continuity.verify_export(bundle, original["ledger"]["head"])["valid"]
                )
        for field in ("assistants", "assistant_proposals"):
            bundle = copy.deepcopy(original)
            del bundle[field]
            self.assertFalse(self.redigest(bundle)["valid"])
        for field in ("supported", "total", "exported", "truncated", "source_status"):
            bundle = copy.deepcopy(original)
            del bundle["assistants"][field]
            self.assertFalse(self.redigest(bundle)["valid"])

    def test_empty_legacy_and_explicit_unsupported_sources_are_distinct(self) -> None:
        empty = self.store.continuity_export(self.pm, self.service.export())
        self.assertTrue(continuity.verify_export(empty, empty["ledger"]["head"])["valid"])
        LegacyTests.prepare_ai(self, self.store)
        complete_release_fixtures(self)
        self.store.ai_run(self.pm, "ZF-1", "summary")
        legacy = self.store.continuity_export(self.pm, self.service.export())
        self.assertEqual(legacy["assistant_proposals"], [])
        self.assertTrue(continuity.verify_export(legacy, legacy["ledger"]["head"])["valid"])
        unavailable = self.store.continuity_export(self.pm)
        self.assertFalse(unavailable["complete"])
        self.assertFalse(self.redigest(unavailable)["valid"])
        unsupported = copy.deepcopy(empty)
        unsupported["assistants"] = dict(
            supported=False,
            total=0,
            exported=0,
            truncated=False,
            source_status="unsupported",
            note="JSON store does not hold durable proposals.",
        )
        self.assertTrue(self.redigest(unsupported)["valid"])
        unsupported["assistants"]["total"] = 1
        self.assertFalse(self.redigest(unsupported)["valid"])

    def test_unreferenced_retained_release_lifecycle_is_required(self) -> None:
        part = self.service.export()
        self.assertEqual(part["proposals"], [])
        original = self.store.continuity_export(self.pm, part)
        head = copy.deepcopy(original["ledger"]["head"])
        self.assertTrue(continuity.verify_export(original, head)["valid"])
        for defect in ("truncated", "events", "count", "revision", "association", "task", "status"):
            with self.subTest(defect=defect):
                source = copy.deepcopy(part)
                record = source["task_releases"]["records"][0]
                if defect == "truncated":
                    record.update(events=[], truncated=True)
                elif defect == "events":
                    record["events"] = []
                elif defect == "count":
                    record["event_total"] = True
                elif defect == "revision":
                    record["revision"] = True
                elif defect == "association":
                    record["events"][0]["release_id"] = "other"
                elif defect == "task":
                    record["events"][0]["body"]["task"] = "other"
                else:
                    record["current_status"] = "revoked"
                bundle = self.store.continuity_export(self.pm, source)
                self.assertFalse(bundle["complete"], defect)
                expected = copy.deepcopy(bundle["ledger"]["head"])
                self.redigest(bundle)
                check = continuity.verify_export(bundle, expected)
                self.assertFalse(check["valid"], check)
                self.assertFalse(check["complete"], check)
                self.assertFalse(
                    any("digest" in p or "externally held" in p for p in check["problems"])
                )
        limited_events = self.store.continuity_export(self.pm, self.service.export(event_limit=0))
        self.assertFalse(limited_events["complete"])
        self.assertFalse(continuity.verify_export(limited_events)["valid"])

    def test_unreferenced_lifecycle_transitions_and_timestamp_ties(self) -> None:
        from zava_forward.core.assistants import runtime_binding

        cap = "stock-prioritisation"
        body = release_support.fixture(
            cap, runtime_binding(cap, self.store.ai), expires="2099-01-01T00:00:00Z"
        )
        with patch.object(self.service, "now", return_value=2_000_000_000):
            released = self.service.record_release(self.pm, body)
            for state in ("active", "suspended", "suspended", "revoked"):
                if state != "active":
                    self.service.change_release(self.pm, released["id"], state, "Synthetic.")
                bundle = self.store.continuity_export(self.pm, self.service.export())
                record = next(
                    r for r in bundle["task_releases"]["records"] if r["id"] == released["id"]
                )
                record["events"].reverse()
                head = copy.deepcopy(bundle["ledger"]["head"])
                self.redigest(bundle)
                self.assertTrue(continuity.verify_export(bundle, head)["valid"])
        for defect in (
            "initial-late",
            "after-revoke",
            "duplicate-initial",
            "duplicate-revoke",
            "missing-initial",
            "final",
        ):
            with self.subTest(defect=defect):
                bad = copy.deepcopy(bundle)
                record = next(
                    r for r in bad["task_releases"]["records"] if r["id"] == released["id"]
                )
                recorded = next(
                    e for e in record["events"] if e["body"]["kind"] == "release-recorded"
                )
                revoked = next(
                    e for e in record["events"] if e["body"]["kind"] == "release-revoked"
                )
                if defect == "initial-late":
                    recorded["at"] += 1
                elif defect == "after-revoke":
                    next(e for e in record["events"] if e["body"]["kind"] == "release-suspended")[
                        "at"
                    ] += 1
                elif defect in ("duplicate-initial", "duplicate-revoke"):
                    extra = copy.deepcopy(recorded if defect == "duplicate-initial" else revoked)
                    extra["id"] = uuid.uuid4().hex
                    record["events"].append(extra)
                    record["revision"] += 1
                    record["event_total"] += 1
                elif defect == "missing-initial":
                    record["events"].remove(recorded)
                    record["revision"] -= 1
                    record["event_total"] -= 1
                else:
                    record["current_status"] = "active"
                self.redigest(bad)
                self.assertFalse(continuity.verify_export(bad, head)["valid"])

    def test_malformed_release_sources_fail_producer_and_verifier_without_exceptions(self) -> None:
        part = self.service.export()
        original = self.store.continuity_export(self.pm, part)
        malformed_sources: tuple[Any, ...] = (None, False, [], 3, "unknown", {})
        invalid: list[tuple[str, Any]] = [("task_releases", value) for value in malformed_sources]
        for field, value in (
            ("records", None),
            ("records", [None]),
            ("records", [{}]),
            ("total", True),
            ("exported", 1.0),
            ("truncated", 0),
            ("supported", "yes"),
        ):
            evidence = copy.deepcopy(part["task_releases"])
            evidence[field] = value
            invalid.append(("task_releases", evidence))
        for field, value in (
            ("id", []),
            ("id", None),
            ("snapshot", None),
            ("snapshot", []),
            ("events", None),
            ("events", [None]),
            ("event_total", -1),
            ("revision", 1.0),
            ("truncated", None),
        ):
            evidence = copy.deepcopy(part["task_releases"])
            evidence["records"][0][field] = value
            invalid.append(("task_releases", evidence))
        for field, value in (
            ("at", True),
            ("at", float("nan")),
            ("at", float("inf")),
            ("body", None),
            ("body", []),
            ("id", []),
            ("release_id", []),
        ):
            evidence = copy.deepcopy(part["task_releases"])
            evidence["records"][0]["events"][0][field] = value
            invalid.append(("task_releases", evidence))
        for field, value in invalid:
            with self.subTest(field=field, value=value):
                source = copy.deepcopy(part)
                source[field] = value
                produced = self.store.continuity_export(self.pm, source)
                self.assertFalse(produced["complete"])
                self.assertTrue(produced["incomplete_reasons"])
                bad = copy.deepcopy(original)
                bad[field] = value
                self.redigest(bad)
                check = continuity.verify_export(bad, original["ledger"]["head"])
                self.assertFalse(check["valid"])
                self.assertFalse(check["complete"])
                self.assertTrue(check["problems"])
        for source in (
            None,
            False,
            [],
            3,
            {},
            dict(part, proposals=None),
            dict(part, proposals=[None]),
        ):
            with self.subTest(source=source):
                produced = self.store.continuity_export(self.pm, source)
                self.assertFalse(produced["complete"])
        for envelope, provenance in (([], []), ({}, [None]), ({}, {}), (1, [])):
            source = copy.deepcopy(part)
            source["proposals"] = [
                dict(capability="stock-prioritisation", envelope=envelope, provenance=provenance)
            ]
            source["total"] = 1
            produced = self.store.continuity_export(self.pm, source)
            self.assertFalse(produced["complete"])
            self.assertFalse(self.redigest(produced)["valid"])

    def test_json_numeric_timestamps_fail_closed_without_conversion_errors(self) -> None:
        part = self.service.export()
        original = self.store.continuity_export(self.pm, part)
        head = copy.deepcopy(original["ledger"]["head"])
        self.assertTrue(continuity.verify_export(original, head)["valid"])
        cases = (
            (0, True),
            (-1, True),
            (1.25, True),
            (-1.25, True),
            (10**308, True),
            (-(10**308), True),
            (1.7976931348623157e308, True),
            (-1.7976931348623157e308, True),
            (10**400, False),
            (-(10**400), False),
            (True, False),
            (False, False),
            (None, False),
            ("2000000000", False),
            (float("nan"), False),
            (float("inf"), False),
            (-float("inf"), False),
        )
        problem = "invalid task-release event envelope"
        for boundary in ("producer", "verifier"):
            for at, valid in cases:
                with self.subTest(boundary=boundary, at=at):
                    source = copy.deepcopy(part if boundary == "producer" else original)
                    source["task_releases"]["records"][0]["events"][0]["at"] = at
                    source = json.loads(json.dumps(source))
                    if boundary == "producer":
                        bundle = self.store.continuity_export(self.pm, source)
                        expected_head = copy.deepcopy(bundle["ledger"]["head"])
                        self.assertEqual(bundle["complete"], valid, bundle["incomplete_reasons"])
                        if not valid:
                            self.assertIn(problem, bundle["incomplete_reasons"])
                    else:
                        bundle = source
                        expected_head = head
                        bundle["complete"] = True
                        bundle["incomplete_reasons"] = []
                        bundle["digest"] = continuity.sha(
                            {k: v for k, v in bundle.items() if k != "digest"}
                        )
                    bundle = json.loads(json.dumps(bundle))
                    check = continuity.verify_export(bundle, expected_head)
                    self.assertEqual(check["valid"], valid, check)
                    self.assertEqual(check["complete"], valid, check)
                    if boundary == "verifier":
                        self.assertEqual(bundle["ledger"], original["ledger"])
                    self.assertEqual(bundle["ledger"]["head"], expected_head)
                    self.assertFalse(
                        any(
                            "digest mismatch" in p or "externally held" in p
                            for p in check["problems"]
                        ),
                        check,
                    )
                    if not valid:
                        self.assertIn(problem, check["problems"])

    def test_release_source_absence_and_unsupported_are_not_full_evidence(self) -> None:
        part = self.service.export()
        missing = copy.deepcopy(part)
        del missing["task_releases"]
        bundle = self.store.continuity_export(self.pm, missing)
        self.assertFalse(bundle["complete"])
        self.assertFalse(self.redigest(bundle)["valid"])
        for field, value in (("supported", False), ("total", 0), ("exported", 0)):
            bad = copy.deepcopy(part)
            bad["task_releases"][field] = value
            produced = self.store.continuity_export(self.pm, bad)
            self.assertFalse(produced["complete"])
            self.assertFalse(self.redigest(produced)["valid"])
        # Real absence is retained as negative evidence, not repaired by an exporter.
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_releases")
        empty = self.store.continuity_export(self.pm, self.service.export())
        self.assertEqual(empty["task_releases"]["records"], [])
        self.assertTrue(continuity.verify_export(empty, empty["ledger"]["head"])["valid"])
        release_support.install(self.store)
        bare = self.store.continuity_export(self.pm, self.service.export())
        self.assertFalse(bare["complete"])
        self.assertFalse(self.redigest(bare)["valid"])


class HttpTests(fixtures.ApiTests):
    cycle = EpochTests.cycle

    def setUp(self) -> None:
        super().setUp()
        complete_release_fixtures(self)

    def test_register_recorded_need_canaries_and_canonical_nonmutation(self) -> None:
        canary = "SYNTHETIC-REGISTER-PRIVATE-122"
        suspended = self.store.suspend(
            self.pm,
            dict(
                SUSPEND,
                reason=canary,
                incident_owner=canary,
                containment=canary,
                comms_owner=canary,
                comms_audience=canary,
            ),
        )
        changed = self.store.change_record(
            self.pm,
            dict(
                kind="model",
                subject=canary,
                from_version=canary + "-v1",
                to_version=canary + "-v2",
                reason=canary,
                evaluation="pass",
                evaluation_ref=canary,
            ),
        )
        with self.store.lock:
            self.store._cont()["suspensions"][0]["unknown_nested"] = {"reason": canary}
            self.store._cont()["changes"][0]["unknown_nested"] = [canary]
            self.store.save()
            canonical_before = copy.deepcopy(self.store._cont())
        for need in (None, "", "Programme Support Officer,Quality Inspector"):
            context = (
                patch.dict(os.environ, {"ZF_REASON_ROLES": need})
                if need is not None
                else patch.dict(os.environ, {}, clear=False)
            )
            with context:
                from zava_forward.core import projection

                for role in (
                    "Programme Support Officer",
                    "Quality Inspector",
                    "Retrofit Programme Manager",
                    "Building Safety Liaison",
                ):
                    with self.subTest(need=need, role=role):
                        self.user = self.people[role]
                        status, body = self.request("/api/continuity")
                        self.assertEqual(status, 200, body)
                        self.assertEqual(
                            canary in json.dumps(body), projection.can_see_reason(self.user)
                        )
                        self.assertEqual(body["epoch"], suspended["epoch"])
                        self.assertEqual(body["suspensions"][0]["id"], suspended["id"])
                        self.assertEqual(body["changes"][0]["id"], changed["id"])
                        self.assertFalse(body["suspensions"][0]["communication"]["sent"])
                        if projection.can_see_reason(self.user):
                            self.assertEqual(body["suspensions"], canonical_before["suspensions"])
                            self.assertEqual(body["changes"], canonical_before["changes"])
        with self.store.lock:
            self.assertEqual(self.store._cont(), canonical_before)

    def test_limited_mutation_responses_preserve_human_controls_without_text(self) -> None:
        canary = "SYNTHETIC-MUTATION-PRIVATE-122"
        with patch.dict(os.environ, {"ZF_REASON_ROLES": "Building Safety Liaison"}):
            self.user = self.people["Quality Inspector"]
            status, suspended = self.request(
                "/api/continuity/suspend", dict(SUSPEND, reason=canary)
            )
            self.assertEqual(status, 200, suspended)
            sid = suspended["id"]
            self.assertEqual(suspended["status"], "Suspended")
            self.assertNotIn(canary, json.dumps(suspended))
            self.assertFalse(suspended["communication"]["sent"])
            for decision in ("Keep suspended", "Restart"):
                self.user = self.pm
                status, proposed = self.request(
                    "/api/continuity/restart-propose", dict(id=sid, corrective_evidence=canary)
                )
                self.assertEqual(status, 200, proposed)
                self.assertTrue(proposed["proposal"])
                self.assertNotIn(canary, json.dumps(proposed))
                self.user = self.people["Programme Support Officer"]
                status, decided = self.request(
                    "/api/continuity/restart-decide",
                    dict(
                        id=sid,
                        epoch=proposed["proposal"]["epoch"],
                        decision=decision,
                        authority_ref=canary,
                    ),
                )
                self.assertEqual(status, 200, decided)
                self.assertNotIn(canary, json.dumps(decided))
                self.assertEqual(
                    decided["status"], "Restarted" if decision == "Restart" else "Suspended"
                )
            status, changed = self.request(
                "/api/continuity/change",
                dict(
                    kind="rule",
                    subject=canary,
                    from_version="v1",
                    to_version="v2",
                    reason=canary,
                    evaluation="pass",
                    evaluation_ref=canary,
                ),
            )
            self.assertEqual(status, 200, changed)
            self.assertEqual(changed["status"], "Applied")
            self.assertNotIn(canary, json.dumps(changed))
            status, reverse = self.request(
                "/api/continuity/change-reverse", dict(id=changed["id"], reason=canary)
            )
            self.assertEqual(status, 200, reverse)
            self.assertEqual(reverse["reverses"], changed["id"])
            self.assertNotIn(canary, json.dumps(reverse))
        self.user = self.pm
        _, full = self.request("/api/continuity")
        self.assertIn(canary, json.dumps(full))
        self.assertEqual(full["changes"][0]["status"], "Reversed")

    def test_export_preserves_programme_support_reason_redaction(self) -> None:
        canary = "SYNTHETIC-RESTRICTED-REASON-122"
        self.store.audit(self.pm["email"], "log_contact", "ZF-1", canary)
        self.store.save()
        head = self.store.ledger_head()
        self.user = self.people["Programme Support Officer"]
        status, bundle = self.request("/api/continuity/export")
        self.assertEqual(status, 200, bundle)
        self.assertNotIn(canary, json.dumps(bundle))
        self.assertEqual(bundle["audience"]["scope"], "limited")
        self.assertFalse(bundle["complete"])
        self.assertFalse(bundle["ledger"]["report"]["intact"])
        self.assertFalse(continuity.verify_export(bundle)["valid"])
        self.assertEqual(bundle["ledger"]["head"], dict(count=head[0], hash=head[1]))
        self.assertTrue(any(canary in json.dumps(row) for row in self.store.audit_entries()))

    def test_nested_evidence_projection_and_full_manager_proof(self) -> None:
        canary = "SYNTHETIC-NESTED-PROTECTED-TEXT-122"
        from zava_forward.core.assistants import runtime_binding

        self.service.approvers = {self.pm["email"]}
        cap = "stock-prioritisation"
        released = self.service.record_release(
            self.pm,
            release_support.fixture(
                cap,
                runtime_binding(cap, self.store.ai),
                expires="2099-01-01T00:00:00Z",
                impact_assessment=canary,
                residual_risk_note=canary,
            ),
        )
        p = self.verify(self.run_ready(cap))
        self.service.review(self.pm, p["id"], "accept", p["revision"], canary)
        with self.service.transaction() as db:
            self.service.event(db, p["id"], kind="synthetic-test", nested={"free_text": canary})
        self.service.change_release(self.pm, released["id"], "revoked", canary)
        with self.store.lock:
            self.store.data["recommendations"].append(
                dict(
                    id="synthetic-legacy122",
                    user=self.pm["email"],
                    kind="ai_task",
                    task="summary",
                    source="template",
                    status="Not reviewed",
                    shown_output=canary,
                    reviewer_reason=canary,
                    envelope=dict(nested={"arbitrary": canary}),
                    provenance=[dict(text=canary)],
                )
            )
            self.store._gov()["breaches"].append(dict(note=canary, nested={"reason": canary}))
            self.store.save()
        self.store.suspend(
            self.people["Quality Inspector"],
            dict(SUSPEND, reason=canary, containment=canary, synthetic=True),
        )
        self.store.audit(self.pm["email"], "synthetic-nested", "ZF-1", canary)
        self.store.save()
        self.user = self.pm
        head = self.store.ledger_head()
        status, full = self.request("/api/continuity/export")
        self.assertEqual(status, 200, full)
        expected = dict(count=head[0], hash=head[1])
        self.assertEqual(full["ledger"]["head"], expected)
        self.assertTrue(
            continuity.verify_export(full, expected)["valid"], full["incomplete_reasons"]
        )
        for section in (
            "ledger",
            "ai_records",
            "assistant_proposals",
            "task_releases",
            "approvals",
            "continuity",
        ):
            self.assertIn(canary, json.dumps(full[section]), section)
        self.assertFalse(any(row["relied_on"] for row in full["assistant_proposals"]))
        before = copy.deepcopy(full)
        for role in ("Programme Support Officer", "Retrofit Programme Manager"):
            with self.subTest(role=role):
                self.user = self.people[role]
                # Existing recorded-need override, not a policy change or authorization bypass.
                with patch.dict(os.environ, {"ZF_REASON_ROLES": "Building Safety Liaison"}):
                    status, limited = self.request("/api/continuity/export")
                self.assertEqual(status, 200, limited)
                self.assertNotIn(canary, json.dumps(limited))
                self.assertFalse(limited["complete"])
                self.assertFalse(limited["audience"]["full_ledger_proof"])
                self.assertEqual(limited["assistant_proposals"][0]["state"], "accepted")
                self.assertFalse(limited["assistant_proposals"][0]["relied_on"])
                self.assertFalse(continuity.verify_export(limited, expected)["valid"])
                limited["complete"] = True
                limited["incomplete_reasons"] = []
                limited["digest"] = continuity.sha(
                    {key: value for key, value in limited.items() if key != "digest"}
                )
                verified = continuity.verify_export(limited)
                self.assertFalse(verified["valid"])
                self.assertFalse(verified["complete"])
        self.assertEqual(full, before)
        self.assertTrue(continuity.verify_export(full, expected)["valid"])

    def test_continuity_http_audiences_and_offline_export(self) -> None:
        managers = ("Retrofit Programme Manager", "Programme Support Officer")
        viewers = (*managers, "Quality Inspector", "Building Safety Liaison")
        for role, person in self.people.items():
            with self.subTest(role=role):
                self.user = person
                status, body = self.request("/api/continuity")
                self.assertEqual(status, 200 if role in viewers else 403, body)
                status, body = self.request("/api/continuity/export")
                self.assertEqual(status, 200 if role in managers else 403, body)
                if role in managers:
                    bundle = json.loads(json.dumps(body))
                    valid = continuity.verify_export(bundle, bundle["ledger"]["head"])["valid"]
                    self.assertEqual(valid, role == "Retrofit Programme Manager")
                    self.assertEqual(
                        bundle["audience"]["scope"],
                        "full" if role == "Retrofit Programme Manager" else "limited",
                    )

    def test_http_epoch_read_review_export_and_manual_actions(self) -> None:
        with urllib.request.urlopen(self.url + "/healthz") as response:
            self.assertEqual(response.status, 200)
        p = self.verify(self.run_ready("stock-prioritisation"))
        s = self.store.suspend(self.people["Quality Inspector"], dict(SUSPEND, synthetic=True))
        # Actual case transaction, not just a continuity availability note.
        self.assertEqual(
            self.request(
                "/api/cases/ZF-1/call",
                dict(outcome="Spoke to resident", note="Synthetic manual call"),
            )[0],
            200,
        )
        liaison = self.people["Resident Liaison Officer"]
        self.user = liaison
        status, detail = self.request(
            "/api/cases/ZF-1/resident",
            dict(
                action="service_open",
                route="Complaint",
                summary="Synthetic challenge",
                desired_outcome="Independent explanation",
                service_owner=liaison["email"],
                redress_owner=self.pm["email"],
                next_update="2099-01-01",
            ),
        )
        self.assertEqual(status, 200, detail)
        self.user = self.pm
        with self.store.lock:
            self.store._case("ZF-1")["stage"] = "Final checks before ordering"
            self.store.save()
        code, detail = self.request(
            "/api/cases/ZF-1/hazard-raise",
            dict(
                category="Damp and mould",
                priority="Emergency",
                note="Synthetic hazard",
                source="Synthetic phone report",
                aware_at="2026-01-01T10:00:00Z",
            ),
        )
        self.assertEqual(code, 200, detail)
        safety = self.people["Building Safety Liaison"]
        self.assertEqual(
            self.request(
                "/api/cases/ZF-1/hazard-refer",
                dict(
                    index=0, to=safety["email"], job="Synthetic job", evidence="Synthetic referral"
                ),
            )[0],
            200,
        )
        self.user = safety
        for action in ("hazard-receive", "hazard-accept", "hazard-repaired"):
            code, detail = self.request(
                "/api/cases/ZF-1/" + action,
                dict(index=0, evidence="Synthetic " + action),
            )
            self.assertEqual(code, 200, detail)
        self.assertEqual(
            self.request(
                "/api/cases/ZF-1/hazard-release",
                dict(index=0, evidence="No repair", note="Must refuse"),
            )[0],
            403,
        )
        self.user = self.pm
        self.assertEqual(self.request("/api/cases/ZF-1/advance", {})[0], 409)
        self.assertEqual(
            self.request("/api/assistants/proposals/" + p["id"])[1]["actionable"], False
        )
        self.store.restart_propose(self.pm, dict(id=s["id"], corrective_evidence="Synthetic only"))
        self.store.restart_decide(
            self.people["Programme Support Officer"],
            dict(
                id=s["id"],
                epoch=self.store.continuity_epoch(),
                decision="Restart",
                authority_ref="Fixture only",
            ),
        )
        for action in ("verify", "accept", "edit-accept"):
            status, body = self.request(
                f"/api/assistants/proposals/{p['id']}/review",
                dict(
                    action=action,
                    revision=p["revision"],
                    note="Stale",
                    source_verified=True,
                    output=proposal(p["snapshot"]),
                ),
            )
            self.assertEqual(status, 403, body)
        listing = self.request("/api/assistants/proposals")[1]["proposals"]
        self.assertFalse(next(x for x in listing if x["id"] == p["id"])["actionable"])
        status, bundle = self.request("/api/continuity/export")
        self.assertEqual(status, 200)
        self.assertTrue(all(not x["relied_on"] for x in bundle["assistant_proposals"]))
        self.user = self.people["Contractor"]
        self.assertEqual(self.request("/api/continuity/export")[0], 403)


class OwnedMssql(Base):
    """UUID database on an explicitly owned loopback container, never Azure."""

    def setUp(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        if os.environ.get("ZF_SQL_SERVER") != "127.0.0.1" or not os.environ.get(
            "ZF_ISSUE122_OWNED_SQL"
        ):
            raise ValueError("Requires an explicitly issue-owned loopback SQL container")
        name = "zf_continuity122_" + uuid.uuid4().hex
        self.sql_env = dict(os.environ, ZF_SQL_DATABASE=name)
        master = _Conn(connection_string(dict(self.sql_env, ZF_SQL_DATABASE="master")))
        try:
            master.execute("CREATE DATABASE " + name)
        finally:
            master.close()
        self.addCleanup(self.drop_database, name)
        super().setUp()

    def drop_database(self, name: str) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        master = _Conn(connection_string(dict(self.sql_env, ZF_SQL_DATABASE="master")))
        try:
            master.execute(f"ALTER DATABASE {name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
            master.execute("DROP DATABASE " + name)
        finally:
            master.close()

    def open_store(self) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        return MssqlStore(str(self.seed), env=self.sql_env, state_dir=str(self.root))


@unittest.skipUnless(os.environ.get("ZF_CONTINUITY_MSSQL") == "1", "owned local MSSQL opt-in")
class MssqlEpochTests(OwnedMssql, EpochTests):
    pass


@unittest.skipUnless(os.environ.get("ZF_CONTINUITY_MSSQL") == "1", "owned local MSSQL opt-in")
class MssqlLegacyTests(OwnedMssql, LegacyTests):
    pass


@unittest.skipUnless(os.environ.get("ZF_CONTINUITY_MSSQL") == "1", "owned local MSSQL opt-in")
class MssqlOfflineTests(OwnedMssql, OfflineTests):
    pass


@unittest.skipUnless(os.environ.get("ZF_CONTINUITY_MSSQL") == "1", "owned local MSSQL opt-in")
class MssqlHttpTests(OwnedMssql, HttpTests):
    pass


if __name__ == "__main__":
    unittest.main()
