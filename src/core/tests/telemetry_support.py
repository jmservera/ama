"""Network-free real SDK fixture shared by core, agents and API tests."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from unittest.mock import patch

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

from zava_forward.core import telemetry


@dataclass
class CapturedTelemetry:
    spans: InMemorySpanExporter
    metrics: InMemoryMetricReader


@contextmanager
def capture_telemetry(ratio: float = 1.0) -> Iterator[CapturedTelemetry]:
    spans, reader = InMemorySpanExporter(), InMemoryMetricReader()
    resource = Resource({"service.name": "test", "service.version": "test"})
    traces = TracerProvider(
        resource=resource, sampler=ParentBased(TraceIdRatioBased(ratio)), shutdown_on_exit=False
    )
    traces.add_span_processor(SimpleSpanProcessor(spans))
    meters = MeterProvider(resource=resource, metric_readers=[reader], shutdown_on_exit=False)
    runtime = telemetry.Runtime(
        telemetry.Configuration("zava-forward-api", "http://localhost", {}, "test", ratio),
        traces,
        meters,
    )
    try:
        with patch.object(telemetry, "_runtime", runtime):
            yield CapturedTelemetry(spans, reader)
    finally:
        traces.shutdown()
        meters.shutdown()
