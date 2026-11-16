"""Privacy, propagation and configuration contracts on real OTel SDK output."""

import contextvars
import json
import os
import threading
import unittest
from unittest.mock import patch

from opentelemetry import trace
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export import SpanExportResult
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from telemetry_support import capture_telemetry
from zava_forward.core import telemetry

CANARY = "resident=private@example.invalid prompt=PRIVATE_PAYLOAD"


class TelemetryTests(unittest.TestCase):
    def test_default_off_has_no_spans_or_context(self) -> None:
        with patch.dict(os.environ, {}, clear=True), patch.object(telemetry, "_runtime", None):
            telemetry.initialize("zava-forward-api")
            with telemetry.operation("chat"):
                self.assertIsNone(telemetry.carrier())
                self.assertEqual(telemetry.correlation(), {})
            self.assertIsNone(telemetry._runtime)

    def test_configuration_rejects_bad_values_without_echoing_them(self) -> None:
        base = {"ZF_OTEL_ENDPOINT": "http://localhost:4318"}
        cases = [
            {"ZF_OTEL_ENDPOINT": ""},
            {"ZF_OTEL_ENDPOINT": "http://external.example.invalid"},
            {"ZF_OTEL_ENDPOINT": "https://private:secret@example.invalid"},
            {"ZF_OTEL_ENDPOINT": "https://example.invalid/?password=secret"},
            {"ZF_OTEL_SAMPLE_RATIO": "nan"},
            {"ZF_OTEL_SAMPLE_RATIO": "2"},
            {"ZF_OTEL_HEADERS": CANARY},
            {"ZF_OTEL_HEADERS": '{"Authorization": "secret\\r\\nheader"}'},
            {"ZF_OTEL_HEADERS": '{"Authorization": "\\u0000"}'},
            {"ZF_OTEL_HEADERS": '{"Authorization": " secret"}'},
            {"ZF_OTEL_ENVIRONMENT": CANARY},
        ]
        for case in cases:
            with self.subTest(case=next(iter(case))), self.assertRaises(ValueError) as error:
                telemetry._configuration("zava-forward-api", base | case)
            self.assertEqual(str(error.exception), "Invalid telemetry configuration.")

    def test_initialize_is_idempotent_minimal_and_rejects_conflict(self) -> None:
        spans, reader = InMemorySpanExporter(), InMemoryMetricReader()
        env = {
            "ZF_OTEL_EXPORTER": "otlp",
            "ZF_OTEL_ENDPOINT": "http://localhost:4318",
            "OTEL_RESOURCE_ATTRIBUTES": "user.email=private@example.invalid",
            "OTEL_SERVICE_NAME": CANARY,
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(telemetry, "_runtime", None),
            patch(
                "opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter",
                return_value=spans,
            ) as factory,
            patch(
                "opentelemetry.sdk.metrics.export.PeriodicExportingMetricReader",
                return_value=reader,
            ),
        ):
            try:
                telemetry.initialize("zava-forward-api")
                telemetry.initialize("zava-forward-api")
                with telemetry.operation("chat"):
                    pass
                runtime = telemetry._runtime
                assert runtime is not None
                runtime.traces.force_flush()
                attrs = spans.get_finished_spans()[0].resource.attributes
                self.assertEqual(attrs["service.name"], "zava-forward-api")
                self.assertFalse(any(k.startswith(("host.", "process.", "user.")) for k in attrs))
                self.assertNotIn("private", json.dumps(dict(attrs)))
                factory.assert_called_once()
                with self.assertRaisesRegex(ValueError, "Conflicting"):
                    telemetry.initialize("zava-forward-agents")
            finally:
                telemetry.shutdown()

    def test_unsupported_exporter_and_disabling_running_pipeline_are_explicit_errors(self) -> None:
        for exporter in ("azure-monitor", "PRIVATE_PAYLOAD", ""):
            with (
                patch.dict(os.environ, {"ZF_OTEL_EXPORTER": exporter}),
                self.assertRaises(ValueError) as error,
            ):
                telemetry.initialize("zava-forward-api")
            self.assertEqual(str(error.exception), "Invalid ZF_OTEL_EXPORTER.")
        with capture_telemetry(), patch.dict(os.environ, {"ZF_OTEL_EXPORTER": "none"}):
            with self.assertRaisesRegex(ValueError, "Conflicting telemetry"):
                telemetry.initialize("zava-forward-api")

    def test_blocked_export_does_not_block_controlled_work(self) -> None:
        entered, release, completed = threading.Event(), threading.Event(), threading.Event()
        exporter, reader = InMemorySpanExporter(), InMemoryMetricReader()

        def blocked_export(_spans: object) -> SpanExportResult:
            entered.set()
            release.wait(30)
            return SpanExportResult.SUCCESS

        def controlled_work() -> None:
            with telemetry.operation("invoke_workflow"):
                pass
            completed.set()

        env = {"ZF_OTEL_EXPORTER": "otlp", "ZF_OTEL_ENDPOINT": "http://localhost:4318"}
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(telemetry, "_runtime", None),
            patch.object(exporter, "export", side_effect=blocked_export),
            patch(
                "opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter",
                return_value=exporter,
            ),
            patch(
                "opentelemetry.sdk.metrics.export.PeriodicExportingMetricReader",
                return_value=reader,
            ),
        ):
            try:
                telemetry.initialize("zava-forward-api")
                for _ in range(128):
                    with telemetry.operation("chat"):
                        pass
                self.assertTrue(entered.wait(2))
                thread = threading.Thread(target=controlled_work, daemon=True)
                thread.start()
                try:
                    self.assertTrue(completed.wait(2), "Work waited for the blocked exporter")
                    self.assertFalse(release.is_set())
                finally:
                    release.set()
                    thread.join(2)
            finally:
                release.set()
                telemetry.shutdown()

    def test_parent_context_crosses_threads_without_baggage(self) -> None:
        with capture_telemetry() as captured:
            with telemetry.operation("invoke_workflow", capability="funding-evidence"):
                parent = telemetry.carrier()
                context = contextvars.copy_context()
                thread = threading.Thread(target=context.run, args=(self._child,))
                thread.start()
                thread.join(2)
                self.assertFalse(thread.is_alive())
            with telemetry.operation("messaging.process", parent=parent):
                propagated = telemetry.correlation()
            spans = captured.spans.get_finished_spans()
            child, root, consumer = spans
            assert child.parent is not None and consumer.parent is not None
            self.assertEqual(child.parent.span_id, root.context.span_id)
            self.assertEqual(consumer.parent.span_id, root.context.span_id)
            self.assertEqual(propagated["trace_id"], f"{root.context.trace_id:032x}")
            self.assertEqual(telemetry.correlation(), {})

    @staticmethod
    def _child() -> None:
        with telemetry.operation("chat"):
            pass

    def test_errors_metrics_and_usage_are_content_free_and_bounded(self) -> None:
        with capture_telemetry() as captured:
            with self.assertRaises(TimeoutError), telemetry.operation("chat") as observation:
                observation.usage(7, 3)
                raise TimeoutError(CANARY)
            with telemetry.operation("invoke_workflow", capability=CANARY):
                pass
            spans = captured.spans.get_finished_spans()
            self.assertEqual(spans[0].status.status_code, trace.StatusCode.ERROR)
            self.assertEqual(spans[0].events, ())
            self.assertEqual((spans[0].attributes or {})["gen_ai.usage.input_tokens"], 7)
            self.assertNotIn("gen_ai.agent.name", spans[1].attributes or {})
            metrics = captured.metrics.get_metrics_data()
            assert metrics is not None
            serialized = metrics.to_json()
            self.assertNotIn("PRIVATE_PAYLOAD", serialized)
            self.assertNotIn("private@example.invalid", serialized)
            self.assertNotIn("task_id", serialized)
            self.assertIn("gen_ai.client.inference.duration", serialized)
            self.assertIn("gen_ai.client.inference.usage.output_tokens", serialized)
            for resource in metrics.resource_metrics:
                for scope in resource.scope_metrics:
                    for metric in scope.metrics:
                        for point in metric.data.data_points:
                            attributes = point.attributes or {}
                            self.assertLessEqual(len(attributes), 3)
                            self.assertNotIn("trace_id", attributes)
                            self.assertNotIn("span_id", attributes)

    def test_sampling_inherits_remote_decision_and_still_records_metrics(self) -> None:
        sampled = "00-11111111111111111111111111111111-2222222222222222-01"
        with capture_telemetry(ratio=0) as captured:
            with telemetry.operation("chat"):
                pass
            with telemetry.operation("chat", parent=sampled):
                pass
            self.assertEqual(len(captured.spans.get_finished_spans()), 1)
            self.assertIsNotNone(captured.metrics.get_metrics_data())

    def test_invalid_carriers_are_ignored_and_do_not_leak_context(self) -> None:
        for value in (CANARY, "", "00-" + "0" * 32 + "-" + "1" * 16 + "-01", {"baggage": CANARY}):
            with self.subTest(value=type(value).__name__):
                self.assertIsNone(telemetry.valid_traceparent(value))
        with capture_telemetry() as captured:
            with telemetry.operation("http.server", root=True, method=CANARY) as request:
                request.http_status(503)
            with telemetry.operation("http.server", root=True, method="GET"):
                pass
            first, second = captured.spans.get_finished_spans()
            self.assertIsNone(first.parent)
            self.assertIsNone(second.parent)
            self.assertNotEqual(first.context.trace_id, second.context.trace_id)
            self.assertEqual(first.name, "_OTHER")


if __name__ == "__main__":
    unittest.main()
