"""Composed local metering on constructed data and a fake HTTP provider."""

from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from unittest.mock import patch

from zava_forward.core.ai import Ai
from zava_forward.core.ai_consumption import (
    CallContext,
    DispatchHeld,
    call_context,
    reference,
)
from zava_forward.core.assistants import canonical

from test_assistants import Base, proposal
from zava_forward.api.server import App, make_handler

START = "2026-10-01T00:00:00Z"
END = "2099-01-01T00:00:00Z"


class ConsumptionApi(unittest.TestCase):
    def setUp(self) -> None:
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
        test = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:
                pass

            def do_POST(self) -> None:
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                test.requests.append(payload)
                user = payload["messages"][1]["content"]
                snapshot = json.loads(user)["evidence"] if user.startswith("{") else {}
                text = canonical(proposal(snapshot))
                body = json.dumps(
                    dict(
                        model="test-model",
                        usage=dict(
                            prompt_tokens=100,
                            completion_tokens=20,
                            total_tokens=120,
                            prompt_tokens_details=dict(cached_tokens=10),
                        ),
                        choices=[dict(message=dict(content=text))],
                    )
                ).encode()
                self.send_response(200)
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

    def test_assistant_thread_preserves_usage_metadata_and_review_join(self) -> None:
        self.authority("assessment-preparation")
        task = self.fixture.run_ready("assessment-preparation")
        envelope = task["envelope"]
        self.assertEqual(envelope["usage"]["cached_tokens"], 10)
        self.assertEqual(envelope["usage"]["total_tokens"], 120)
        self.assertEqual(len(envelope["meter_id"]), 64)
        verified = self.fixture.verify(task)
        self.service.review(
            self.pm,
            task["id"],
            "accept",
            verified["revision"],
            "Constructed human review, not live acceptance.",
        )
        report = self.service.consumption.report(start=START, end=END, as_of=END)
        self.assertEqual(report["accepted_proposals"], 1)
        self.assertEqual(report["token_cost"], "Unknown")
        self.assertEqual(len(self.requests), 1)
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

    def test_manager_report_local_http_and_bad_period(self) -> None:
        test = self

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
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(base + "?start=invalid")
        self.assertEqual(error.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
