"""Composed local metering on constructed data and a fake HTTP provider."""

from __future__ import annotations

import json
import sqlite3
import threading
import unittest
import urllib.error
import urllib.request
from contextlib import nullcontext
from dataclasses import replace
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

import release_support

# The installed agents distribution lacks a py.typed marker.
from zava_forward.agents.chat import ChatModel  # type: ignore[import-untyped]
from zava_forward.agents.dispatch import (  # type: ignore[import-untyped]
    AgentWorker,
    ResultMessage,
    TaskMessage,
    foundry_provider,
)
from zava_forward.core import ai_prompts, ai_tasks
from zava_forward.core.ai import Ai
from zava_forward.core.ai_consumption import (
    CURRENT,
    CallContext,
    DispatchHeld,
    call_context,
    reference,
)
from zava_forward.core.assistants import REGISTRY, build_request, canonical, runtime_binding
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import FALLBACK, SYSTEM, TASK, ChatPanel
from zava_forward.core.store import ConflictError, Store

from test_assistants import Base, proposal
from zava_forward.api.server import App, make_handler

START = "2026-10-01T00:00:00Z"
END = "2099-01-01T00:00:00Z"


class ConsumptionApi(unittest.TestCase):
    def setUp(self) -> None:
        scratch = patch("tempfile.tempdir", str(Path.cwd()))
        scratch.start()
        self.addCleanup(scratch.stop)
        self.fixture = Base()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        self.store = self.fixture.store
        self.provider = self.fixture.provider
        self.pm: dict[str, Any] = self.fixture.pm
        self.inner = Ai()
        self.inner.model_version = "test-model"
        self.inner.model_version_strong = "test-model"
        self.inner.consumption = self.service.consumption
        self.requests: list[dict[str, Any]] = []
        self.response_text: str | None = None
        self.response_status = 200
        self.response_model: object = "test-model"
        test = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:
                pass

            def do_POST(self) -> None:
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                test.requests.append(payload)
                user = payload["messages"][1]["content"]
                snapshot = json.loads(user).get("evidence", {}) if user.startswith("{") else {}
                text = test.response_text or canonical(proposal(snapshot))
                body = json.dumps(
                    dict(
                        model=test.response_model,
                        usage=dict(
                            prompt_tokens=100,
                            completion_tokens=20,
                            total_tokens=120,
                            prompt_tokens_details=dict(cached_tokens=10),
                        ),
                        choices=[dict(message=dict(content=text))],
                    )
                ).encode()
                self.send_response(test.response_status)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.fake = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.fake.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.thread.join, 5)
        self.addCleanup(self.fake.server_close)
        self.addCleanup(self.fake.shutdown)
        self.inner.endpoint = f"http://127.0.0.1:{self.fake.server_address[1]}"
        token = patch.object(self.inner, "_token", return_value="constructed-not-a-credential")
        token.start()
        self.addCleanup(token.stop)
        evidence = patch.object(self.provider, "evidence", side_effect=self.inner.evidence)
        evidence.start()
        self.addCleanup(evidence.stop)

    def authority(
        self,
        capability: str,
        deployment: str = "standard",
        temperature: float = 0,
        output: int = 600,
        **extra: Any,
    ) -> None:
        meter = self.service.consumption
        price = meter.price(
            source="https://prices.azure.com/api/retail/prices",
            source_hash=reference("fictional-price-fixture"),
            retrieved=START,
            version="fictional-v1",
            model="test-model",
            currency="USD",
            start=START,
            end=END,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=True,
        )
        fields = dict(
            authority="nonbillable-local-" + capability,
            owner="fictional-owner",
            evidence="fixture-only-no-paid-authority",
            price=price,
            capability=capability,
            configuration=self.inner.configuration(deployment, temperature, output),
            start=START,
            end=END,
            max_calls=2,
            max_depth=1,
            budgets=[dict(id=reference("period"), calls=100, tokens=10000000, amount="100")],
        )
        fields.update(extra)
        meter.authorize(**fields)

    def records(self) -> list[dict[str, Any]]:
        with self.service.transaction() as db:
            return [dict(r) for r in self.service.consumption._read(db)]

    def fresh(self) -> ConsumptionApi:
        fixture = ConsumptionApi()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        return fixture

    def publication_store(self, backend: str) -> Any:
        store = self.store
        if backend == "json":
            store = Store(
                str(self.fixture.seed),
                str(self.fixture.root / "publication-live.json"),
                str(self.fixture.root / "publication-audit.jsonl"),
            )
        store.ai = self.inner
        self.inner.gate = lambda task, deployment=None: (
            store.continuity_block(task) or store.release_block(task, deployment)
        )
        release_support.install(store)
        with store.lock:
            store._case("ZF-1")["owner_code"] = self.pm["code"]
            store.save()
        return store

    def chat_panel(self, store: Any) -> ChatPanel:
        iso = ChatIsolation(
            store,
            env=dict(
                CHAT_DPIA_REF="SYNTH-DPIA",
                CHAT_LAWFUL_BASIS_REF="SYNTH-LAWFUL-BASIS",
                CHAT_NOTICE_REF="SYNTH-NOTICE",
            ),
        )
        return ChatPanel(
            iso, ChatModel(AgentWorker(foundry_provider(self.inner)), admission=lambda: None)
        )

    def fill_partition(self, target: int = 9999) -> None:
        with self.service.transaction() as db:
            rows = self.service.consumption._read(db)
            price = next(r for r in rows if r["kind"] == "price")
            for _ in range(target - len(rows)):
                self.service.event(db, "ai-consumption", **price)
            actual = db.execute(
                "SELECT COUNT(*) FROM assistant_events WHERE task_id='ai-consumption'"
            ).fetchone()[0]
        self.assertEqual(actual, target)

    def saved_recommendation(self, store: Any, backend: str, rid: str) -> dict[str, Any]:
        if backend == "sql":
            value = json.loads(
                store.db.execute("SELECT body FROM recommendations WHERE id=?", (rid,)).fetchone()[
                    0
                ]
            )
        else:
            value = next(
                r
                for r in json.loads(Path(store.live_path).read_text())["recommendations"]
                if r["id"] == rid
            )
        return dict(value)

    def provenance(
        self,
        envelope: dict[str, Any],
        root: str,
        attempt: str,
        configuration: str,
        prompt: str,
    ) -> None:
        records = self.records()
        reserved = next(
            r for r in records if r["kind"] == "reserved" and r["id"] == envelope["meter_id"]
        )
        self.assertEqual(envelope["meter_root"], root)
        self.assertEqual(
            [reserved[k] for k in ("root", "attempt", "configuration", "prompt")],
            [root, attempt, configuration, prompt],
        )
        if "configuration" in envelope:
            self.assertEqual(envelope["configuration"], configuration)
        if "prompt_hash" in envelope:
            self.assertEqual(envelope["prompt_hash"], prompt)
        self.assertEqual(len(envelope["meter_id"]), 64)
        completed = next(
            r for r in records if r["kind"] == "completed" and r["id"] == reserved["id"]
        )
        self.assertEqual(completed["tokens"]["cached_tokens"], 10)
        self.assertEqual(completed["tokens"], envelope["usage"])

    def test_assistant_thread_preserves_usage_metadata_and_review_join(self) -> None:
        self.authority("assessment-preparation")
        task = self.fixture.run_ready("assessment-preparation")
        envelope = task["envelope"]
        self.assertEqual(envelope["usage"]["cached_tokens"], 10)
        self.assertEqual(envelope["usage"]["total_tokens"], 120)
        self.assertEqual(len(envelope["meter_id"]), 64)
        self.provenance(
            envelope,
            reference(task["id"]),
            reference(f"{task['id']}:{task['fence']}"),
            self.inner.configuration("standard", 0, 600),
            reference(runtime_binding("assessment-preparation", self.provider)["prompt_version"]),
        )
        before = self.fixture.domain()
        verified = self.fixture.verify(task)
        accepted = self.service.review(
            self.pm,
            task["id"],
            "accept",
            verified["revision"],
            "Constructed human review, not live acceptance.",
        )
        report = self.service.consumption.report(start=START, end=END, as_of=END)
        self.assertEqual(report["accepted_proposals"], 1)
        self.assertEqual(report["token_cost"], "Unknown")
        self.assertTrue(accepted["relied_on"])
        with self.assertRaises(ValueError):
            self.service.review(
                self.pm, task["id"], "accept", accepted["revision"], "No second acceptance."
            )
        rejected = self.service.review(
            self.pm, task["id"], "reject", accepted["revision"], "Withdraw human acceptance."
        )
        self.assertEqual(rejected["state"], "rejected")
        self.assertFalse(rejected["relied_on"])
        self.assertEqual(before, self.fixture.domain())
        self.assertEqual(
            self.service.consumption.report(start=START, end=END, as_of=END)["accepted_proposals"],
            0,
        )
        rejected = self.service.review(
            self.pm, task["id"], "reject", rejected["revision"], "Retain rejected history."
        )
        self.assertEqual(len([r for r in self.records() if r["kind"] == "review"]), 2)
        self.assertEqual(rejected["envelope"]["meter_id"], envelope["meter_id"])
        self.assertEqual(rejected["envelope"]["usage"], envelope["usage"])
        self.assertTrue(
            next(
                r
                for r in self.records()
                if r["kind"] == "output" and r["output"] == reference(task["id"])
            )["eligible"]
        )
        self.fixture.case(lambda c: c["home"].update(address="Constructed changed home"))
        edited_task = self.fixture.run_ready("assessment-preparation")
        edited_task = self.fixture.verify(edited_task)
        edited_task = self.service.review(
            self.pm,
            edited_task["id"],
            "edit-accept",
            edited_task["revision"],
            "Human edit.",
            output=proposal(edited_task["snapshot"]),
        )
        self.assertEqual(edited_task["state"], "accepted")
        edited_task = self.service.review(
            self.pm,
            edited_task["id"],
            "reject",
            edited_task["revision"],
            "Withdraw edited proposal.",
        )
        self.assertEqual(edited_task["state"], "rejected")
        self.assertFalse(edited_task["relied_on"])
        self.assertEqual(
            self.service.consumption.report(start=START, end=END, as_of=END)["accepted_proposals"],
            0,
        )
        self.assertEqual(before[1:], self.fixture.domain()[1:])
        self.assertEqual(len(self.requests), 2)
        with self.service.transaction() as db:
            records = self.service.consumption._read(db)
        serialized = json.dumps(records)
        for canary in (
            "PRIVATE-VULNERABILITY-REASON",
            "PRIVATE-DOCUMENT-NAME",
            "PRIVATE-AI-SUMMARY",
            "PRIVATE-HANDOFF-NOTE",
        ):
            self.assertNotIn(canary, serialized)

    def test_unmetered_unknown_authority_and_image_stop_before_http(self) -> None:
        self.inner.consumption = None
        result = self.inner.evidence("system", "constructed-input")
        self.assertEqual(result["outcome"], "financial-held")
        self.inner.consumption = self.service.consumption
        result = self.inner.evidence("system", "constructed-input")
        self.assertEqual(result["outcome"], "financial-held")
        self.assertEqual(result["reason"], "authority-unknown")
        self.authority("read-document", deployment="capable", temperature=0.3, output=500)
        result = self.inner.look_at("fictional.png", b"not-an-image", "image/png")
        self.assertEqual(result["source"], "template")
        self.assertEqual(len(self.requests), 0)

    def test_shared_root_fanout_stops_real_transport_at_two(self) -> None:
        self.authority("assessment")
        for i in range(3):
            root = reference("one-root")
            context = CallContext(
                root,
                reference(str(i)),
                "assessment",
                "retrofit-case",
                reference("config"),
                reference("prompt"),
            )
            with call_context(context):
                result = self.inner.evidence("system", "constructed-input")
            self.assertEqual(result["outcome"], "returned" if i < 2 else "financial-held")
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(result["reason"], "request-call-limit")

    def test_money_limit_prevents_transport_and_ordinary_case_is_unchanged(self) -> None:
        before = self.fixture.domain()
        self.authority(
            "assessment-preparation",
            budgets=[dict(id=reference("period"), calls=100, tokens=10000000, amount="0")],
        )
        task = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        self.service.execute(task["id"])
        task = self.service.detail(self.pm, task["id"])
        self.assertEqual(task["state"], "failed")
        self.assertIn("ordinary case", task["manual"])
        self.assertEqual(self.fixture.domain(), before)
        self.assertEqual(len(self.requests), 0)

    def test_unknown_price_and_liability_never_claim_success(self) -> None:
        self.authority("assessment", price=reference("missing-price"))
        root = reference("root")
        with call_context(
            CallContext(
                root, root, "assessment", "retrofit-case", reference("config"), reference("prompt")
            )
        ):
            result = self.inner.evidence("system", "constructed-input")
        self.assertEqual(result["reason"], "price-unknown")
        self.assertEqual(len(self.requests), 0)
        with self.assertRaises(DispatchHeld):
            self.service.consumption.reserve(
                CallContext(
                    root,
                    root,
                    "assessment",
                    "retrofit-case",
                    self.inner.configuration("standard", 0, 600),
                    reference("prompt"),
                ),
                "test-model",
                None,
                600,
            )
        self.authority(
            "assessment-preparation",
            budgets=[dict(id=reference("token-period"), calls=100, tokens=10000000, amount="100")],
        )
        config = self.inner.configuration("standard", 0, 600)
        other = CallContext(
            reference("other-root"),
            reference("other-attempt"),
            "assessment-preparation",
            "retrofit-case",
            config,
            reference("other-prompt"),
        )

        def token_wait() -> str:
            rid = self.service.consumption.reserve(other, "test-model", 2000, 600)
            self.service.consumption.complete(
                rid,
                dict(prompt_tokens=100, completion_tokens=20, total_tokens=120),
                "test-model",
                "returned",
            )
            return "constructed-not-a-credential"

        with patch.object(self.inner, "_token", side_effect=token_wait) as token:
            with call_context(
                CallContext(
                    reference("waiting-root"),
                    reference("waiting-attempt"),
                    "assessment-preparation",
                    "retrofit-case",
                    config,
                    reference("waiting-prompt"),
                )
            ):
                waiting = self.inner.evidence("system", "constructed-input")
        token.assert_called_once()
        self.assertEqual(waiting["outcome"], "financial-held")
        self.assertEqual(waiting["reason"], "liability-unknown")
        self.assertEqual(len(self.requests), 0)
        held = self.service.consumption.report(start=START, end=END, as_of=END)
        self.assertTrue(
            any(
                a["owner"] == reference("fictional-owner")
                and a["reason"] == "liability-unknown"
                and a["route"] == "workflow-only"
                for a in held["owned_alerts"]
            )
        )

    def test_legacy_and_priority_reviews_recover_only_committed_matching_links(self) -> None:
        meter = self.service.consumption
        meter.billing(
            source="constructed-local-bill",
            allocation="constructed-allocation",
            budget=reference("period"),
            start=START,
            end=END,
            currency="USD",
            billed="0.000135",
            tolerance="1",
            complete=True,
            synthetic=True,
        )
        for backend in ("sql", "json"):
            store = self.store
            if backend == "json":
                store = Store(
                    str(self.fixture.seed),
                    str(self.fixture.root / "legacy-live.json"),
                    str(self.fixture.root / "legacy-audit.jsonl"),
                )
            store.ai = self.inner
            self.inner.gate = lambda task, deployment=None, store=store: (
                store.continuity_block(task) or store.release_block(task, deployment)
            )
            release_support.install(store)
            with store.lock:
                store._case("ZF-1")["owner_code"] = self.pm["code"]
                store.save()
            for path in ("legacy", "priority"):
                capability = "briefing" if path == "legacy" else "priority"
                deployment = "standard" if path == "legacy" else "capable"
                self.authority(capability, deployment=deployment, temperature=0.3, output=700)
                for action in ("accept", "edit", "reject"):
                    for fault in ("none", "review-link", "save-before", "output-link"):
                        with self.subTest(backend=backend, path=path, action=action, fault=fault):
                            with store.lock:
                                case = store._case("ZF-1")
                                label = next(
                                    s
                                    for s in ai_tasks.source_labels(case, True)
                                    if s.startswith("Stage:")
                                )
                            self.response_text = (
                                f"Check supplied facts [[ZF-1: {label}]]."
                                if path == "legacy"
                                else json.dumps(
                                    [
                                        dict(
                                            case_id="ZF-1",
                                            reason="Check supplied facts.",
                                            cites=[label],
                                        )
                                    ]
                                )
                            )

                            def produce(
                                path: str = path, store: Any = store, label: str = label
                            ) -> dict[str, Any]:
                                if path == "priority":
                                    return dict(store.ai_priority(self.pm, n=1))
                                return dict(
                                    ai_tasks.run_text_task(
                                        store,
                                        self.pm,
                                        "briefing",
                                        [store._case("ZF-1")],
                                        "Constructed legacy system",
                                        "Constructed legacy input",
                                        "Manual text",
                                        [f"ZF-1: {label}"],
                                    )
                                )

                            before = meter.report(start=START, end=END, as_of=END)
                            if fault == "output-link":
                                with patch.object(
                                    meter, "output", side_effect=RuntimeError("output-link")
                                ):
                                    with self.assertRaisesRegex(RuntimeError, "output-link"):
                                        produce()
                                rec = store.data["recommendations"][-1]
                                report = meter.report(start=START, end=END, as_of=END)
                                self.assertEqual(
                                    report["unjoined_outputs"], before["unjoined_outputs"] + 1
                                )
                                self.assertEqual(report["coverage"], "incomplete")

                                def missing_review(
                                    path: str = path,
                                    store: Any = store,
                                    rec: dict[str, Any] = rec,
                                    action: str = action,
                                ) -> dict[str, Any]:
                                    if path == "legacy":
                                        return dict(
                                            store.review_ai(
                                                self.pm, rec["id"], action, "Human review."
                                            )
                                        )
                                    return dict(
                                        store.resolve_priority(
                                            self.pm,
                                            rec["id"],
                                            action,
                                            "Human review.",
                                            items=[dict(case_id="ZF-1", reason="Human edit.")],
                                        )
                                    )

                                if action == "reject":
                                    rejected = missing_review()
                                    self.assertEqual(rejected["status"], "Rejected")
                                    if backend == "sql":
                                        saved = json.loads(
                                            store.db.execute(
                                                "SELECT body FROM recommendations WHERE id=?",
                                                (rec["id"],),
                                            ).fetchone()[0]
                                        )
                                    else:
                                        saved = next(
                                            r
                                            for r in json.loads(Path(store.live_path).read_text())[
                                                "recommendations"
                                            ]
                                            if r["id"] == rec["id"]
                                        )
                                    self.assertEqual(saved["status"], "Rejected")
                                    report = meter.report(start=START, end=END, as_of=END)
                                    self.assertEqual(
                                        report["unjoined_reviews"], before["unjoined_reviews"] + 1
                                    )
                                    self.assertEqual(report["coverage"], "incomplete")
                                    self.assertEqual(report["token_cost"], "Unknown")
                                    self.assertEqual(
                                        report["cost_per_accepted_proposal"], "Unknown"
                                    )
                                    envelope = rec["envelope"] if path == "legacy" else rec
                                    with (
                                        patch.object(
                                            store,
                                            "audit",
                                            side_effect=AssertionError("must not rereview"),
                                        ),
                                        patch.object(
                                            store,
                                            "save",
                                            side_effect=AssertionError("must not resave"),
                                        ),
                                    ):
                                        meter.output(
                                            envelope["meter_root"], rec["id"], eligible=True
                                        )
                                        with self.assertRaisesRegex(ValueError, "already"):
                                            missing_review()
                                    repaired = meter.report(start=START, end=END, as_of=END)
                                    self.assertEqual(
                                        repaired["unjoined_outputs"], before["unjoined_outputs"]
                                    )
                                    self.assertEqual(
                                        repaired["unjoined_reviews"], before["unjoined_reviews"]
                                    )
                                    self.assertEqual(
                                        repaired["accepted_proposals"],
                                        before["accepted_proposals"],
                                    )
                                    self.assertEqual(rec, saved)
                                    continue
                                with self.assertRaisesRegex(
                                    ValueError, "Output attribution is missing"
                                ):
                                    missing_review()
                                self.assertEqual(
                                    rec["status"],
                                    "Not reviewed" if path == "legacy" else "Proposed",
                                )
                                continue
                            result = produce()
                            rid = result["record_id"] if path == "legacy" else result["id"]
                            rec = next(r for r in store.data["recommendations"] if r["id"] == rid)
                            envelope = rec["envelope"] if path == "legacy" else rec
                            self.provenance(
                                envelope,
                                envelope["meter_root"],
                                envelope["meter_root"],
                                self.inner.configuration(deployment, 0.3, 700),
                                reference(ai_prompts.version(capability)),
                            )
                            output = next(
                                r
                                for r in self.records()
                                if r["kind"] == "output" and r["output"] == reference(rid)
                            )
                            self.assertTrue(output["eligible"])

                            def review(
                                requested: str = action,
                                reason: str = "Original human review.",
                                path: str = path,
                                store: Any = store,
                                rid: str = rid,
                            ) -> dict[str, Any]:
                                if path == "priority":
                                    return dict(
                                        store.resolve_priority(
                                            self.pm,
                                            rid,
                                            requested,
                                            reason,
                                            items=[dict(case_id="ZF-1", reason=reason)],
                                        )
                                    )
                                return dict(
                                    store.review_ai(self.pm, rid, requested, reason, text=reason)
                                )

                            disposition = "edit-accept" if action == "edit" else action
                            if fault == "save-before":
                                with patch.object(
                                    store, "save", side_effect=RuntimeError("save-before")
                                ):
                                    with self.assertRaises(RuntimeError):
                                        review()
                                self.assertIsNotNone(meter.pending_review(rid, disposition))
                                report = meter.report(start=START, end=END, as_of=END)
                                self.assertEqual(
                                    report["unjoined_reviews"], before["unjoined_reviews"] + 1
                                )
                                self.assertEqual(
                                    report["accepted_proposals"], before["accepted_proposals"]
                                )
                                self.assertEqual(report["cost_per_accepted_proposal"], "Unknown")
                                # An unsaved in-memory status is not authoritative.
                                if rec["status"] in ("Accepted", "Edited", "Rejected"):
                                    with self.assertRaisesRegex(ValueError, "already"):
                                        review()
                                    self.assertIsNotNone(meter.pending_review(rid, disposition))
                                if backend == "sql":
                                    persisted = json.loads(
                                        store.db.execute(
                                            "SELECT body FROM recommendations WHERE id=?", (rid,)
                                        ).fetchone()[0]
                                    )
                                else:
                                    persisted = next(
                                        r
                                        for r in json.loads(Path(store.live_path).read_text())[
                                            "recommendations"
                                        ]
                                        if r["id"] == rid
                                    )
                                self.assertEqual(
                                    persisted["status"],
                                    "Not reviewed" if path == "legacy" else "Proposed",
                                )
                                rec.clear()
                                rec.update(persisted)
                            if fault == "review-link":
                                with (
                                    patch.object(
                                        meter, "review", side_effect=RuntimeError("review-link")
                                    ),
                                    self.assertLogs(
                                        "zava_forward.core.resident_decisions", level="ERROR"
                                    )
                                    if path == "priority"
                                    else nullcontext(),
                                ):
                                    with self.assertRaises(RuntimeError):
                                        review()
                                saved = json.loads(canonical(rec))
                                pending = meter.pending_review(rid, disposition)
                                self.assertIsNotNone(pending)
                                report = meter.report(start=START, end=END, as_of=END)
                                self.assertEqual(
                                    report["unjoined_reviews"], before["unjoined_reviews"] + 1
                                )
                                self.assertEqual(
                                    report["accepted_proposals"], before["accepted_proposals"]
                                )
                                self.assertEqual(report["coverage"], "incomplete")
                                self.assertEqual(report["token_cost"], "Unknown")
                                with self.assertRaisesRegex(ValueError, "already"):
                                    review("reject" if action != "reject" else "accept")
                                with (
                                    patch.object(
                                        store, "save", side_effect=AssertionError("must not resave")
                                    ),
                                    patch.object(
                                        store,
                                        "audit",
                                        side_effect=AssertionError("must not rereview"),
                                    ),
                                ):
                                    review(reason="Different retry content must be ignored.")
                                self.assertEqual(rec, saved)
                                meter.review(rid, disposition, intent=pending)
                            else:
                                review()
                            self.assertIsNone(meter.pending_review(rid, disposition))
                            after = meter.report(start=START, end=END, as_of=END)
                            self.assertEqual(after["unjoined_reviews"], before["unjoined_reviews"])
                            self.assertEqual(
                                after["accepted_proposals"],
                                before["accepted_proposals"] + (action != "reject"),
                            )
                            if before["unjoined_outputs"] == 0:
                                self.assertEqual(after["coverage"], "recorded-ledger-only")
                                self.assertEqual(after["token_cost"], "0.000135")
                                self.assertNotEqual(after["cost_per_accepted_proposal"], "Unknown")
                            with self.assertRaisesRegex(ValueError, "already"):
                                review()

    def test_actual_chat_adapter_preserves_metering_without_proposal_eligibility(self) -> None:
        self.store.ai = self.inner
        self.authority(TASK)
        worker = AgentWorker(foundry_provider(self.inner))
        iso = ChatIsolation(
            self.store,
            env=dict(
                CHAT_DPIA_REF="SYNTH-DPIA",
                CHAT_LAWFUL_BASIS_REF="SYNTH-LAWFUL-BASIS",
                CHAT_NOTICE_REF="SYNTH-NOTICE",
            ),
        )
        before = self.fixture.domain()
        for mode in ("returned", "revoked", "provider-failure"):
            with self.subTest(mode=mode):
                admission = [None, "revoked"] if mode == "revoked" else [None, None]
                with patch.object(
                    self.inner, "_token", return_value="constructed-not-a-credential"
                ):
                    model = ChatModel(
                        worker, admission=lambda admission=admission: admission.pop(0)
                    )
                    panel = ChatPanel(iso, model)
                    thread = self.store.chat_create_thread(self.pm, "ZF-1")
                    self.response_text = json.dumps(
                        dict(answer="Check the case stage.", citations=["ZF-1/stage"])
                    )
                    self.response_status = 500 if mode == "provider-failure" else 200
                    calls = len(self.requests)
                    report_before = self.service.consumption.report(start=START, end=END, as_of=END)
                    answer = panel.ask(self.pm, thread["id"], "Tell me a story.")
                self.assertEqual(len(self.requests), calls + 1)
                receipt = answer["consumption"]
                latest = [r for r in self.records() if r["kind"] == "reserved"][-1]
                self.assertEqual(
                    latest["configuration"], self.inner.configuration("standard", 0, 600)
                )
                self.assertEqual(latest["prompt"], reference(SYSTEM))
                self.assertEqual(latest["attempt"], latest["root"])
                report = self.service.consumption.report(start=START, end=END, as_of=END)
                self.assertEqual(report["accepted_proposals"], 0)
                if mode == "returned":
                    self.assertEqual(answer["kind"], "answer")
                    self.assertEqual(receipt["tokens"]["cached_tokens"], 10)
                    self.assertEqual(receipt["meter_id"], latest["id"])
                    self.assertEqual(receipt["meter_root"], latest["root"])
                    self.provenance(
                        dict(
                            receipt,
                            usage=receipt["tokens"],
                            configuration=latest["configuration"],
                            prompt_hash=latest["prompt"],
                        ),
                        latest["root"],
                        latest["attempt"],
                        latest["configuration"],
                        latest["prompt"],
                    )
                    output = next(
                        r
                        for r in self.records()
                        if r["kind"] == "output" and r["root"] == latest["root"]
                    )
                    messages = self.store.chat_resume(self.pm, thread["id"])["messages"]
                    self.assertEqual(
                        output["output"], reference(f"chat:{thread['id']}:{messages[-1]['seq']}")
                    )
                    self.assertFalse(output["eligible"])
                else:
                    self.assertEqual(answer["kind"], "fallback")
                    self.assertEqual(
                        receipt["provider_outcome"],
                        "activation-revoked" if mode == "revoked" else "provider-unavailable",
                    )
                    self.assertEqual(
                        report["unjoined_outputs"], report_before["unjoined_outputs"] + 1
                    )
                    self.assertEqual(report["coverage"], "incomplete")
                    self.assertEqual(report["cost_per_accepted_proposal"], "Unknown")
                    if mode == "revoked":
                        self.assertEqual(receipt["tokens"]["cached_tokens"], 10)
                    else:
                        self.assertIsNone(receipt["tokens"])
                        self.assertEqual(report["unknown_liabilities"], 1)
        self.assertEqual(before[:3], self.fixture.domain()[:3])

    def test_actual_worker_thread_settlement_survives_failure_revocation_and_fence(self) -> None:
        self.authority("assessment-preparation")
        worker = AgentWorker(foundry_provider(self.inner))
        for mode in ("returned", "revoked", "stale-fence", "provider-failure"):
            with self.subTest(mode=mode):
                self.fixture.case(
                    lambda c, mode=mode: c["home"].update(address="Constructed " + mode)
                )
                task = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
                task = self.service.claim(task["id"], "constructed-worker")
                self.assertIsNotNone(task)
                message = TaskMessage.from_json(
                    TaskMessage.from_task(task, self.service.limits).to_json()
                )
                system, _ = build_request(task)
                self.response_status = 500 if mode == "provider-failure" else 200
                calls = len(self.requests)
                observed: list[tuple[str, Any]] = []

                def token(observed: list[tuple[str, Any]] = observed) -> str:
                    from zava_forward.core.ai_consumption import CURRENT

                    observed.append((threading.current_thread().name, CURRENT.get()))
                    return "constructed-not-a-credential"

                with patch.object(self.inner, "_token", side_effect=token):
                    result = worker.handle(message, self.service.limits)
                self.assertIsNotNone(result)
                assert result is not None
                result = ResultMessage.from_json(result.to_json())
                self.assertEqual(len(self.requests), calls + 1)
                self.assertEqual(observed[0][0], "agents-provider")
                self.assertEqual(observed[0][1].root, reference(task["id"]))
                self.assertEqual(observed[0][1].attempt, reference(f"{task['id']}:{task['fence']}"))
                latest = [r for r in self.records() if r["kind"] == "reserved"][-1]
                self.assertEqual(latest["root"], reference(task["id"]))
                self.assertEqual(latest["attempt"], reference(f"{task['id']}:{task['fence']}"))
                self.assertEqual(
                    latest["configuration"], self.inner.configuration("standard", 0, 600)
                )
                self.assertEqual(
                    latest["prompt"],
                    reference(
                        canonical(
                            [system, REGISTRY[task["capability"]]["purpose"], task["version"]]
                        )
                    ),
                )
                self.assertEqual(result.envelope["meter_id"], latest["id"])
                if mode != "provider-failure":
                    self.provenance(
                        result.envelope,
                        latest["root"],
                        latest["attempt"],
                        latest["configuration"],
                        latest["prompt"],
                    )
                    self.assertIsNotNone(result.output)
                else:
                    self.assertIsNone(result.output)
                    self.assertIsNone(result.envelope["usage"])
                    self.assertEqual(result.envelope["outcome"], "provider-unavailable")
                if mode == "revoked":
                    with self.service.transaction() as db:
                        db.execute(
                            "UPDATE assistant_releases SET status='suspended' "
                            "WHERE id='fx-assessment-preparation'"
                        )
                elif mode == "stale-fence":
                    with self.service.transaction() as db:
                        db.execute(
                            "UPDATE assistant_tasks SET fence=fence+1 WHERE id=?", (task["id"],)
                        )
                completed = self.service.complete(
                    task, result.envelope, result.output, result.failure
                )
                self.assertEqual(completed, mode != "stale-fence")
                detail = self.service.detail(self.pm, task["id"])
                report = self.service.consumption.report(start=START, end=END, as_of=END)
                if mode == "returned":
                    self.assertEqual(detail["state"], "ready")
                    output = next(
                        r
                        for r in self.records()
                        if r["kind"] == "output" and r["root"] == latest["root"]
                    )
                    self.assertTrue(output["eligible"])
                    self.assertEqual(output["output"], reference(task["id"]))
                elif mode == "revoked":
                    self.assertEqual(detail["state"], "quarantined")
                    self.assertIsNone(detail["output"])
                    output = next(
                        r
                        for r in self.records()
                        if r["kind"] == "output" and r["root"] == latest["root"]
                    )
                    self.assertFalse(output["eligible"])
                    with self.service.transaction() as db:
                        db.execute(
                            "UPDATE assistant_releases SET status='active' "
                            "WHERE id='fx-assessment-preparation'"
                        )
                else:
                    self.assertIsNone(detail["output"])
                    self.assertGreater(report["unjoined_outputs"], 0)
                    self.assertEqual(report["coverage"], "incomplete")
                    self.assertEqual(report["cost_per_accepted_proposal"], "Unknown")
                self.assertTrue(
                    any(
                        r["kind"] == "completed" and r["id"] == latest["id"] for r in self.records()
                    )
                )
                self.assertEqual(report["accepted_proposals"], 0)
                if mode == "provider-failure":
                    self.assertEqual(report["unknown_liabilities"], 1)

    def test_document_calls_preserve_shared_call_and_depth_limits(self) -> None:
        self.authority(
            "read-document", deployment="capable", temperature=0.3, output=500, max_calls=1
        )
        self.response_text = "Constructed document description."
        context = CallContext(
            reference("document-root"),
            reference("document-first"),
            "read-document",
            "document",
            self.inner.configuration("capable", 0.3, 500),
            reference("enclosing-request-prompt"),
            retry=1,
        )
        with call_context(context):
            first = self.inner.look_at("fixture.txt", b"Constructed evidence.", "text/plain")
            self.assertIs(CURRENT.get(), context)
            with call_context(replace(context, attempt=reference("document-second"))):
                second = self.inner.look_at("fixture.txt", b"Constructed evidence.", "text/plain")
            self.assertIs(CURRENT.get(), context)
        self.assertIsNone(CURRENT.get())
        self.assertEqual(first["source"], "ai")
        self.assertEqual(first["meter_root"], context.root)
        reserved = next(r for r in self.records() if r["kind"] == "reserved")
        self.assertEqual(reserved["attempt"], context.attempt)
        self.assertEqual(reserved["prompt"], context.prompt)
        self.assertEqual(reserved["retry"], 1)
        self.assertEqual(second["source"], "template")
        self.assertEqual(second["error"], "DispatchHeld")
        deep = replace(
            context, root=reference("deep-root"), attempt=reference("deep-attempt"), depth=2
        )
        with call_context(deep):
            held = self.inner.look_at("fixture.txt", b"Constructed evidence.", "text/plain")
            self.assertIs(CURRENT.get(), deep)
        self.assertEqual(held["source"], "template")
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(
            {r["reason"] for r in self.records() if r["kind"] == "alert"},
            {"request-call-limit", "request-depth-limit"},
        )
        standalone = self.inner.look_at("fixture.txt", b"Constructed evidence.", "text/plain")
        self.assertEqual(standalone["source"], "ai")
        self.assertNotEqual(standalone["meter_root"], context.root)
        self.assertIsNone(CURRENT.get())
        self.assertEqual(len(self.requests), 2)

    def test_model_mismatch_survives_worker_roundtrip_and_suspends_release(self) -> None:
        for returned in ("other-model", "m" * 121, "m" * 512, "m" * 513, {"private": "canary"}):
            with self.subTest(model=type(returned).__name__, length=len(returned)):
                fixture = self.fresh()
                fixture.authority("assessment-preparation")
                fixture.response_model = returned
                task = fixture.service.invoke(fixture.pm, "assessment-preparation", "ZF-1")
                task = fixture.service.claim(task["id"], "mismatch-worker")
                worker = AgentWorker(foundry_provider(fixture.inner))
                result = worker.handle(
                    TaskMessage.from_task(task, fixture.service.limits), fixture.service.limits
                )
                assert result is not None
                result = ResultMessage.from_json(result.to_json())
                expected = returned if isinstance(returned, str) and len(returned) <= 512 else None
                self.assertEqual(result.envelope["outcome"], "model-mismatch")
                self.assertEqual(result.envelope["model"], expected)
                self.assertEqual(result.envelope["usage"]["total_tokens"], 120)
                self.assertIsNone(result.output)
                self.assertNotIn("text", result.envelope)
                self.assertTrue(
                    fixture.service.complete(task, result.envelope, result.output, result.failure)
                )
                detail = fixture.service.detail(fixture.pm, task["id"])
                self.assertEqual(detail["state"], "quarantined")
                self.assertIsNone(detail["output"])
                self.assertEqual(
                    detail["serving_attestation"], dict(returned=expected, outcome="mismatch")
                )
                with fixture.service.transaction() as db:
                    release = db.execute(
                        "SELECT status FROM assistant_releases WHERE id='fx-assessment-preparation'"
                    ).fetchone()[0]
                    attempt = db.execute(
                        "SELECT actual,outcome FROM assistant_attempts WHERE id=?",
                        (f"{task['id']}:{task['fence']}",),
                    ).fetchone()
                    durable = json.dumps(db.execute("SELECT body FROM assistant_events").fetchall())
                self.assertEqual(release, "suspended")
                self.assertEqual(tuple(attempt), (120, "model-mismatch"))
                completed = next(r for r in fixture.records() if r["kind"] == "completed")
                self.assertEqual(completed["outcome"], "returned")
                self.assertEqual(completed["tokens"]["total_tokens"], 120)
                self.assertTrue(completed["held"])
                self.assertFalse(
                    next(r for r in fixture.records() if r["kind"] == "output")["eligible"]
                )
                if expected is None:
                    self.assertIsNone(completed["returned_model"])
                    self.assertNotIn("canary", durable)
                    self.assertNotIn("m" * 513, durable)
                self.assertFalse(fixture.service.execute(task["id"]))
                self.assertIsNone(fixture.service.claim(task["id"], "retry-worker"))
                self.assertEqual(len(fixture.requests), 1)

    def test_exact_capacity_publication_returns_persisted_manual_routes(self) -> None:
        for backend in ("sql", "json"):
            for path in ("legacy", "priority", "chat"):
                with self.subTest(backend=backend, path=path):
                    fixture = self.fresh()
                    store = fixture.publication_store(backend)
                    label = next(
                        s
                        for s in ai_tasks.source_labels(store._case("ZF-1"), True)
                        if s.startswith("Stage:")
                    )
                    panel = None
                    thread = None
                    if path == "chat":
                        fixture.authority(TASK)
                        fixture.response_text = json.dumps(
                            dict(answer="Check the case stage.", citations=["ZF-1/stage"])
                        )
                        panel = fixture.chat_panel(store)
                        thread = store.chat_create_thread(fixture.pm, "ZF-1")

                    elif path == "priority":
                        fixture.authority(
                            "priority", deployment="capable", temperature=0.3, output=700
                        )
                        fixture.response_text = json.dumps(
                            [dict(case_id="ZF-1", reason="Constructed AI priority.", cites=[label])]
                        )

                    else:
                        fixture.authority("briefing", temperature=0.3, output=700)
                        fixture.response_text = f"Constructed AI draft [[ZF-1: {label}]]."

                    def produce(
                        path: str = path,
                        panel: ChatPanel | None = panel,
                        fixture: ConsumptionApi = fixture,
                        thread: Any = thread,
                        store: Any = store,
                        label: str = label,
                    ) -> dict[str, Any]:
                        if path == "chat":
                            assert panel is not None and thread is not None
                            return dict(panel.ask(fixture.pm, thread["id"], "Tell me a story."))
                        if path == "priority":
                            return dict(store.ai_priority(fixture.pm, n=1))
                        return dict(
                            ai_tasks.run_text_task(
                                store,
                                fixture.pm,
                                "briefing",
                                [store._case("ZF-1")],
                                "Constructed system",
                                "Constructed input",
                                "Manual text",
                                [f"ZF-1: {label}"],
                            )
                        )

                    fixture.fill_partition()
                    with self.assertLogs("zava_forward.core.ai_consumption", level="WARNING"):
                        answer = produce()
                    expected = dict(
                        status="unresolved", reason="meter-capacity-reached", cost="Unknown"
                    )
                    if path == "chat":
                        assert thread is not None
                        self.assertEqual(answer["kind"], "fallback")
                        self.assertEqual(answer["reply"], FALLBACK)
                        self.assertTrue(answer["workflow_only"])
                        self.assertEqual(answer["model"], "workflow-only")
                        self.assertEqual(answer["citations"], [])
                        self.assertEqual(answer["consumption"]["financial_attribution"], expected)
                        saved = store.chat_resume(fixture.pm, thread["id"])["messages"][-1]
                        self.assertEqual(saved["content"], answer["reply"])
                        self.assertEqual(saved["evidence"], [])
                        self.assertEqual(saved["model"], "workflow-only")
                        if backend == "json":
                            disk = json.loads(Path(store.live_path).read_text())
                            self.assertEqual(
                                disk["chat_threads"][thread["id"]]["messages"][-1], saved
                            )
                    else:
                        rid = answer["record_id"] if path == "legacy" else answer["id"]
                        saved = fixture.saved_recommendation(store, backend, rid)
                        self.assertEqual(answer["source"], "template")
                        self.assertIsNone(answer["model"])
                        self.assertEqual(answer["mode"], "workflow-only")
                        self.assertEqual(answer["financial_attribution"], expected)
                        self.assertEqual(saved["financial_attribution"], expected)
                        self.assertEqual(saved["source"], "template")
                        self.assertEqual(saved["mode"], "workflow-only")
                        self.assertIsNone(saved["model"])
                        self.assertTrue(saved["ai_output"])
                        if path == "legacy":
                            self.assertEqual(answer["text"], "Manual text")
                            self.assertEqual(saved["shown_output"], answer["text"])
                            self.assertEqual(answer["citations"], [])
                            self.assertEqual(saved["citations"], [])
                            self.assertEqual(
                                saved["envelope"]["model"], answer["envelope"]["model"]
                            )
                            self.assertIsNone(saved["envelope"]["provider"])
                        else:
                            self.assertEqual(saved["items"], saved["workflow_items"])
                    with patch("zava_forward.core.ai_consumption.MAX_EVENTS", 20000):
                        rows = fixture.records()
                        self.assertEqual(len(rows), 10001)
                        self.assertEqual(sum(r["kind"] == "reserved" for r in rows), 1)
                        self.assertEqual(sum(r["kind"] == "completed" for r in rows), 1)
                        self.assertFalse(any(r["kind"] == "output" for r in rows))
                        report = fixture.service.consumption.report(start=START, end=END, as_of=END)
                        self.assertEqual(report["unjoined_outputs"], 1)
                        self.assertEqual(report["coverage"], "incomplete")
                        self.assertEqual(report["token_cost"], "Unknown")
                        self.assertEqual(report["cost_per_accepted_proposal"], "Unknown")
                    second = produce()
                    self.assertEqual(
                        second["kind"] if path == "chat" else second["source"],
                        "fallback" if path == "chat" else "template",
                    )
                    self.assertEqual(len(fixture.requests), 1)

    def test_assistant_completion_preserves_capacity_quarantine_and_terminal_release(self) -> None:
        for model in ("test-model", "other-model"):
            for capacity in (False, True):
                for revoked in (False, True):
                    with self.subTest(model=model, capacity=capacity, revoked=revoked):
                        fixture = self.fresh()
                        fixture.authority("assessment-preparation")
                        fixture.response_model = model
                        task = fixture.service.invoke(fixture.pm, "assessment-preparation", "ZF-1")
                        task = fixture.service.claim(task["id"], "capacity-worker")
                        if capacity:
                            fixture.fill_partition()
                        result = AgentWorker(foundry_provider(fixture.inner)).handle(
                            TaskMessage.from_task(task, fixture.service.limits),
                            fixture.service.limits,
                        )
                        assert result is not None
                        result = ResultMessage.from_json(result.to_json())
                        if revoked:
                            with fixture.service.transaction() as db:
                                db.execute(
                                    "UPDATE assistant_releases SET status='revoked' "
                                    "WHERE id='fx-assessment-preparation'"
                                )
                        with (
                            self.assertLogs("zava_forward.core.ai_consumption", level="WARNING")
                            if capacity
                            else nullcontext()
                        ):
                            self.assertTrue(
                                fixture.service.complete(
                                    task, result.envelope, result.output, result.failure
                                )
                            )
                        detail = fixture.service.detail(fixture.pm, task["id"])
                        mismatch = model != "test-model"
                        expected_state = (
                            "quarantined"
                            if mismatch or revoked
                            else "failed"
                            if capacity
                            else "ready"
                        )
                        self.assertEqual(detail["state"], expected_state)
                        self.assertEqual(detail["envelope"]["usage"]["total_tokens"], 120)
                        if expected_state != "ready":
                            self.assertIsNone(detail["output"])
                        if mismatch:
                            self.assertEqual(
                                detail["serving_attestation"],
                                dict(returned=model, outcome="mismatch"),
                            )
                        with fixture.service.transaction() as db:
                            status = db.execute(
                                "SELECT status FROM assistant_releases "
                                "WHERE id='fx-assessment-preparation'"
                            ).fetchone()[0]
                            event = json.loads(
                                db.execute(
                                    "SELECT body FROM assistant_events WHERE task_id=? "
                                    "AND json_extract(body,'$.kind')='completed'",
                                    (task["id"],),
                                ).fetchone()[0]
                            )
                            attempt = db.execute(
                                "SELECT actual,active_until FROM assistant_attempts WHERE id=?",
                                (f"{task['id']}:{task['fence']}",),
                            ).fetchone()
                        self.assertEqual(
                            status, "revoked" if revoked else "suspended" if mismatch else "active"
                        )
                        self.assertEqual(tuple(attempt), (120, 0))
                        self.assertEqual(event["state"], expected_state)
                        if capacity:
                            attribution = dict(
                                status="unresolved", reason="meter-capacity-reached", cost="Unknown"
                            )
                            self.assertEqual(detail["financial_attribution"], attribution)
                            self.assertEqual(event["financial_attribution"], attribution)
                            with patch("zava_forward.core.ai_consumption.MAX_EVENTS", 20000):
                                rows = fixture.records()
                                self.assertEqual(len(rows), 10002 if mismatch else 10001)
                                self.assertFalse(any(r["kind"] == "output" for r in rows))
                                report = fixture.service.consumption.report(
                                    start=START, end=END, as_of=END
                                )
                                self.assertEqual(report["unjoined_outputs"], 1)
                                self.assertEqual(report["token_cost"], "Unknown")
                        self.assertFalse(fixture.service.execute(task["id"]))
                        self.assertEqual(len(fixture.requests), 1)

    def test_chat_finalization_has_no_phantom_join_on_fault_or_other_writer(self) -> None:
        for backend in ("sql", "json"):
            for fault in ("output", "message-save", "other-writer"):
                if backend == "json" and fault == "other-writer":
                    continue
                with self.subTest(backend=backend, fault=fault):
                    fixture = self.fresh()
                    store = fixture.publication_store(backend)
                    fixture.authority(TASK)
                    fixture.response_text = json.dumps(
                        dict(answer="Check the case stage.", citations=["ZF-1/stage"])
                    )
                    panel = fixture.chat_panel(store)
                    thread = store.chat_create_thread(fixture.pm, "ZF-1")
                    original = store.chat_add_message
                    other = fixture.fixture.open_store() if fault == "other-writer" else None
                    if other is not None:
                        self.addCleanup(other.db.close)

                    def add_message(
                        *args: Any,
                        original: Any = original,
                        other: Any = other,
                        fixture: ConsumptionApi = fixture,
                        thread: Any = thread,
                        fault: str = fault,
                        store: Any = store,
                        backend: str = backend,
                        **kwargs: Any,
                    ) -> Any:
                        if args[2] != "assistant":
                            return original(*args, **kwargs)
                        if other is not None:
                            other.chat_add_message(
                                fixture.pm, thread["id"], "user", "Other writer."
                            )
                        if fault == "message-save":
                            with patch.object(
                                store.chat_repo,
                                "add_message" if backend == "sql" else "commit",
                                side_effect=RuntimeError("message-save"),
                            ):
                                return original(*args, **kwargs)
                        return original(*args, **kwargs)

                    with (
                        patch.object(store, "chat_add_message", side_effect=add_message),
                        patch.object(
                            fixture.service.consumption,
                            "output",
                            side_effect=RuntimeError("output"),
                        )
                        if fault == "output"
                        else nullcontext(),
                    ):
                        if fault == "other-writer":
                            answer = panel.ask(fixture.pm, thread["id"], "Tell me a story.")
                            self.assertEqual(answer["kind"], "answer")
                        else:
                            with self.assertRaisesRegex(RuntimeError, fault):
                                panel.ask(fixture.pm, thread["id"], "Tell me a story.")
                    messages = store.chat_resume(fixture.pm, thread["id"])["messages"]
                    outputs = [r for r in fixture.records() if r["kind"] == "output"]
                    if fault == "other-writer":
                        self.assertEqual([m["seq"] for m in messages], [1, 2, 3])
                        self.assertEqual(messages[-1]["role"], "assistant")
                        self.assertEqual(outputs[0]["output"], reference(f"chat:{thread['id']}:3"))
                        self.assertFalse(outputs[0]["eligible"])
                    else:
                        self.assertEqual(outputs, [])
                        if backend == "json" and fault == "message-save":
                            messages = json.loads(Path(store.live_path).read_text())[
                                "chat_threads"
                            ][thread["id"]]["messages"]
                        if backend == "sql" or fault == "message-save":
                            self.assertEqual([m["role"] for m in messages], ["user"])
                    self.assertEqual(len(fixture.requests), 1)

    def test_failed_metered_provider_pending_task_can_be_rejected_without_redispatch(self) -> None:
        self.authority("assessment-preparation")
        self.response_status = 500
        task = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        self.assertTrue(self.service.execute(task["id"]))
        task = self.service.detail(self.pm, task["id"])
        self.assertEqual(task["state"], "pending")
        self.assertIsNone(task["output"])
        self.assertEqual(task["envelope"]["outcome"], "provider-unavailable")
        self.assertFalse(any(r["kind"] == "output" for r in self.records()))
        before = self.fixture.domain()
        for action in ("verify", "accept", "edit-accept"):
            with self.assertRaisesRegex(ValueError, "Only current, valid AI proposals"):
                self.service.review(self.pm, task["id"], action, task["revision"], "Not ready.")
        rejected = self.service.review(
            self.pm, task["id"], "reject", task["revision"], "Withdraw failed draft."
        )
        self.assertEqual(rejected["state"], "rejected")
        self.assertEqual(rejected["review"]["action"], "reject")
        self.assertFalse(rejected["relied_on"])
        self.assertEqual(rejected["revision"], task["revision"] + 1)
        records = self.records()
        linked = next(r for r in records if r["kind"] == "output")
        self.assertEqual(linked["root"], task["envelope"]["meter_root"])
        self.assertEqual(linked["output"], reference(task["id"]))
        self.assertFalse(linked["eligible"])
        self.assertEqual(next(r for r in records if r["kind"] == "review")["action"], "reject")
        self.assertFalse(self.service.execute(task["id"]))
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(before, self.fixture.domain())
        report = self.service.consumption.report(start=START, end=END, as_of=END)
        self.assertEqual(report["unjoined_outputs"], 0)
        self.assertEqual(report["unknown_liabilities"], 1)
        self.assertEqual(report["accepted_proposals"], 0)
        self.assertEqual(report["token_cost"], "Unknown")

    def test_capacity_held_withdrawal_persists_unresolved_economics_after_recovery(self) -> None:
        self.authority("assessment-preparation")
        task = self.fixture.verify(self.fixture.run_ready("assessment-preparation"))
        accepted = self.service.review(
            self.pm, task["id"], "accept", task["revision"], "Constructed human acceptance."
        )
        with self.service.transaction() as db:
            before_withdrawal = self.service.now(db) + 1
        end = datetime.fromtimestamp(before_withdrawal, UTC).isoformat()
        as_of = datetime.fromtimestamp(before_withdrawal + 2, UTC).isoformat()
        self.service.consumption.billing(
            source="constructed-complete-bill",
            allocation="constructed-exact-allocation",
            budget=reference("period"),
            start=START,
            end=end,
            currency="USD",
            billed="0.000135",
            tolerance="0",
            complete=True,
            synthetic=True,
        )
        original = self.service.consumption.report(start=START, end=end, as_of=end)
        self.assertEqual(original["reconciliation"], "reconciled")
        self.assertEqual(original["accepted_proposals"], 1)
        before = self.fixture.domain()
        with (
            patch("zava_forward.core.ai_consumption.MAX_EVENTS", 0),
            patch.object(self.service, "now", return_value=before_withdrawal + 1),
        ):
            rejected = self.service.review(
                self.pm,
                task["id"],
                "reject",
                accepted["revision"],
                "Withdraw prior acceptance while metering is held.",
            )
            self.assertEqual(rejected["state"], "rejected")
            self.assertFalse(rejected["relied_on"])
            self.assertEqual(rejected["financial_attribution"]["status"], "unresolved")
            self.assertEqual(rejected["financial_attribution"]["reason"], "meter-capacity-reached")
            repeated = self.service.review(
                self.pm, task["id"], "reject", rejected["revision"], "Retain withdrawal."
            )
            self.assertEqual(repeated["financial_attribution"]["status"], "unresolved")
            with self.assertRaisesRegex(DispatchHeld, "meter-capacity-reached"):
                self.service.consumption.report(start=START, end=end, as_of=as_of)
        self.assertEqual(before, self.fixture.domain())
        restarted = self.fixture.other()
        saved = restarted.detail(self.pm, task["id"])
        self.assertEqual(saved["state"], "rejected")
        self.assertEqual(saved["review"]["action"], "reject")
        self.assertTrue(
            any(
                r["kind"] == "review" and r["financial_attribution"]["status"] == "unresolved"
                for r in saved["provenance"]
                if r.get("financial_attribution")
            )
        )
        historical = restarted.consumption.report(start=START, end=end, as_of=end)
        self.assertEqual(historical["accepted_proposals"], 1)
        current = restarted.consumption.report(start=START, end=end, as_of=as_of)
        self.assertEqual(current["accepted_proposals"], 0)
        self.assertEqual(current["unjoined_reviews"], 1)
        self.assertEqual(current["coverage"], "incomplete")
        self.assertEqual(current["reconciliation"], "unreconciled")
        for field in ("token_cost", "cost_per_accepted_proposal", "quality_qualified_cost"):
            self.assertEqual(current[field], "Unknown")

    def test_rejection_link_capacity_boundary_and_sql_failures_are_atomic(self) -> None:
        self.authority("assessment-preparation")
        self.response_status = 500
        task = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        self.assertTrue(self.service.execute(task["id"]))
        task = self.service.detail(self.pm, task["id"])
        before = self.records()
        event = self.service.event
        for kind in ("output", "review", "review-unresolved"):
            with self.subTest(failing_event=kind):

                def fail_insert(db: Any, tid: str, failed_kind: str = kind, **body: Any) -> None:
                    if body["kind"] == failed_kind:
                        raise sqlite3.OperationalError("constructed-insert-failure")
                    event(db, tid, **body)

                with (
                    patch.object(self.service, "event", side_effect=fail_insert),
                    patch("zava_forward.core.ai_consumption.MAX_EVENTS", 0)
                    if kind == "review-unresolved"
                    else nullcontext(),
                ):
                    with self.assertRaises(sqlite3.OperationalError):
                        self.service.review(
                            self.pm, task["id"], "reject", task["revision"], "Withdraw."
                        )
                saved = self.service.detail(self.pm, task["id"])
                self.assertEqual(saved["state"], "pending")
                self.assertEqual(saved["revision"], task["revision"])
                self.assertIsNone(saved["review"])
                self.assertEqual(self.records(), before)
        with patch("zava_forward.core.ai_consumption.MAX_EVENTS", 0):
            with self.assertRaises(ConflictError):
                self.service.review(
                    self.pm, task["id"], "reject", task["revision"] - 1, "Stale revision."
                )
            with self.assertRaises(PermissionError):
                self.service.review(
                    dict(self.pm, role="Contractor"),
                    task["id"],
                    "reject",
                    task["revision"],
                    "Wrong role.",
                )
        self.assertEqual(self.records(), before)
        # One snapshot stages both writes, even at the exact existing-record boundary.
        with patch("zava_forward.core.ai_consumption.MAX_EVENTS", len(before)):
            rejected = self.service.review(
                self.pm, task["id"], "reject", task["revision"], "Exact-capacity withdrawal."
            )
        self.assertEqual(rejected["state"], "rejected")
        records = self.records()
        self.assertEqual(len(records), len(before) + 2)
        self.assertEqual(sum(r["kind"] == "output" for r in records), 1)
        self.assertEqual(sum(r["kind"] == "review" for r in records), 1)
        self.assertFalse(any(r["kind"] == "review-unresolved" for r in records))

    def test_manager_report_local_http_and_bad_period(self) -> None:
        test = self
        self.authority("assessment-preparation")

        class Identity:
            name = "password"

            def authenticate(self, handler: Any) -> dict[str, Any]:
                return test.pm

        app = App(self.store, provider=Identity())
        self.addCleanup(app.assistants.stop)
        http = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(http.server_close)
        self.addCleanup(http.shutdown)
        base = f"http://127.0.0.1:{http.server_address[1]}/api/ai/report"
        with urllib.request.urlopen(base) as response:
            result = json.load(response)
        self.assertEqual(result["consumption"]["cost_per_accepted_proposal"], "Unknown")
        self.assertEqual(result["consumption"]["accepted_proposals"], 0)
        self.assertNotIn("PRIVATE-VULNERABILITY-REASON", json.dumps(result["consumption"]))
        for hold in ("meter-capacity-reached", "meter-evidence-invalid"):
            if hold == "meter-evidence-invalid":
                with app.assistants.transaction() as db:
                    app.assistants.event(db, "ai-consumption", schema="invalid", kind="invalid")
            with (
                self.subTest(hold=hold),
                patch("zava_forward.core.ai_consumption.MAX_EVENTS", 0)
                if hold == "meter-capacity-reached"
                else nullcontext(),
            ):
                with urllib.request.urlopen(base) as response:
                    held = json.load(response)
                    self.assertEqual(response.status, 200)
                self.assertEqual(set(held), {"evaluation", "live", "registry", "consumption"})
                self.assertEqual(set(held["evaluation"]), set(result["evaluation"]))
                self.assertEqual(held["evaluation"]["version"], result["evaluation"]["version"])
                self.assertEqual(held["registry"], result["registry"])
                self.assertEqual(
                    held["consumption"],
                    dict(
                        coverage="unavailable",
                        token_cost="Unknown",
                        cost_per_accepted_proposal="Unknown",
                        reason=hold,
                    ),
                )
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + "?start=invalid")
                self.assertEqual(error.exception.code, 400)
        invalid_periods = (
            "?start=invalid",
            "?start=2026-10-31T00:00:00",
            "?end=invalid",
            "?as_of=2026-10-31T12:00:00",
            "?start=2099-01-01T00:00:00Z&end=2026-10-31T00:00:00Z",
            "?start=2026-10-31T00:00:00Z&end=2026-11-01T00:00:00Z&as_of=2026-10-31T12:00:00Z",
            "?start=&end=invalid",
            "?start=invalid&start=invalid",
            "?unknown=1",
        )
        json_store = Store(
            str(self.fixture.seed),
            str(self.fixture.root / "report-live.json"),
            str(self.fixture.root / "report-audit.jsonl"),
        )
        json_app = App(json_store, provider=Identity())
        self.addCleanup(json_app.assistants.stop)
        sql_assistants = app.assistants
        for backend in ("sql", "json", "schema-unavailable"):
            assistants = json_app.assistants if backend == "json" else sql_assistants
            with (
                patch.object(app, "store", json_store if backend == "json" else self.store),
                patch.object(app, "assistants", assistants),
                patch.object(assistants, "sql", backend == "sql"),
                patch.object(
                    assistants,
                    "schema_error",
                    "Constructed unavailable schema" if backend == "schema-unavailable" else None,
                ),
            ):
                for query in invalid_periods:
                    with self.subTest(backend=backend, query=query):
                        with self.assertRaises(urllib.error.HTTPError) as error:
                            urllib.request.urlopen(base + query)
                        self.assertEqual(error.exception.code, 400)
                if backend != "sql":
                    with urllib.request.urlopen(base) as response:
                        unavailable = json.load(response)["consumption"]
                    self.assertEqual(unavailable["coverage"], "unavailable")
                    self.assertEqual(unavailable["token_cost"], "Unknown")


if __name__ == "__main__":
    unittest.main()
