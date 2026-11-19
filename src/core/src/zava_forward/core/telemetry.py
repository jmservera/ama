"""Explicit, content-free OTLP instrumentation; disabled unless configured."""

from __future__ import annotations

import json
import logging
import math
import os
import re
import threading
import time
from collections.abc import Iterator, Mapping
from contextlib import AbstractContextManager, contextmanager, nullcontext
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import TYPE_CHECKING, Literal
from urllib.parse import urlsplit

from .version import __version__

if TYPE_CHECKING:
    from opentelemetry import trace
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.trace import TracerProvider

LOG = logging.getLogger(__name__)
OperationName = Literal[
    "http.server",
    "http.client",
    "messaging.publish",
    "messaging.process",
    "db.transaction",
    "invoke_workflow",
    "chat",
]
CAPABILITIES = frozenset(
    {
        "stock-prioritisation",
        "assessment-preparation",
        "funding-evidence",
        "works-resident-coordination",
        "quality-evidence",
    }
)
_METHODS = frozenset({"GET", "HEAD", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"})
_TRACEPARENT = re.compile(r"00-([0-9a-f]{32})-([0-9a-f]{16})-[0-9a-f]{2}")
_LOCK = threading.Lock()
_runtime: Runtime | None = None


@dataclass(frozen=True)
class Configuration:
    service: str
    endpoint: str = field(repr=False)
    headers: Mapping[str, str] = field(repr=False)
    environment: str = "local"
    sample_ratio: float = 1.0


class Runtime:
    def __init__(
        self, config: Configuration, traces: TracerProvider, meters: MeterProvider
    ) -> None:
        from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

        self.config, self.traces, self.meters = config, traces, meters
        self.propagator = TraceContextTextMapPropagator()
        self.tracer = traces.get_tracer(__name__, __version__)
        meter = meters.get_meter(__name__, __version__)
        buckets = tuple(0.01 * 2**i for i in range(15))
        self.durations = {
            operation: meter.create_histogram(
                metric,
                unit="s",
                explicit_bucket_boundaries_advisory=buckets,
            )
            for operation, metric in (
                ("http.server", "http.server.request.duration"),
                ("invoke_workflow", "gen_ai.invoke_agent.duration"),
                ("chat", "gen_ai.client.inference.duration"),
            )
        }
        self.tokens = {
            direction: meter.create_counter(
                f"gen_ai.client.inference.usage.{direction}_tokens", unit="{token}"
            )
            for direction in ("input", "output")
        }


def _configuration(service: str, env: Mapping[str, str]) -> Configuration:
    if service not in {"zava-forward-api", "zava-forward-agents"}:
        raise ValueError("Invalid telemetry service.")
    endpoint = env.get("ZF_OTEL_ENDPOINT", "")
    try:
        parsed = urlsplit(endpoint)
        valid = (
            bool(parsed.hostname)
            and bool(parsed.port is None or parsed.port > 0)
            and (
                parsed.scheme == "https"
                or (
                    parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
                )
            )
            and not parsed.username
            and not parsed.password
            and not parsed.query
            and not parsed.fragment
        )
        ratio = float(env.get("ZF_OTEL_SAMPLE_RATIO", "1"))
        headers = json.loads(env.get("ZF_OTEL_HEADERS", "{}"))
    except (ValueError, TypeError):
        raise ValueError("Invalid telemetry configuration.") from None
    environment = env.get("ZF_OTEL_ENVIRONMENT", "local")
    if (
        not valid
        or len(endpoint) > 4096
        or any(ord(c) < 33 or ord(c) > 126 for c in endpoint)
        or not math.isfinite(ratio)
        or not 0 <= ratio <= 1
        or environment not in {"local", "test", "development", "staging", "production"}
        or not isinstance(headers, dict)
        or len(headers) > 16
        or any(
            not isinstance(k, str)
            or not re.fullmatch(r"[A-Za-z0-9-]{1,64}", k)
            or not isinstance(v, str)
            or len(v) > 4096
            or not v
            or v[:1].isspace()
            or any(ord(c) < 32 or ord(c) > 126 for c in v)
            for k, v in headers.items()
        )
    ):
        raise ValueError("Invalid telemetry configuration.")
    return Configuration(service, endpoint.rstrip("/"), headers, environment, ratio)


def initialize(service: str) -> None:
    """Create one owned pipeline; no global SDK auto-instrumentation or detectors."""
    global _runtime
    exporter = os.environ.get("ZF_OTEL_EXPORTER", "none")
    if exporter not in {"none", "otlp"}:
        raise ValueError("Invalid ZF_OTEL_EXPORTER.")
    with _LOCK:
        if exporter == "none":
            if _runtime is not None:
                raise ValueError("Conflicting telemetry initialization.")
            return
        config = _configuration(service, os.environ)
        if _runtime is not None:
            if _runtime.config != config:
                raise ValueError("Conflicting telemetry initialization.")
            return
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import SpanLimits, TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

        from .diagnostic_logging import install_diagnostic_redaction

        install_diagnostic_redaction()
        resource = Resource(
            {
                "service.name": config.service,
                "service.version": __version__,
                "deployment.environment": config.environment,
                "deployment.environment.name": config.environment,
                "telemetry.sdk.name": "opentelemetry",
                "telemetry.sdk.language": "python",
                "telemetry.sdk.version": version("opentelemetry-sdk"),
            }
        )
        meters = MeterProvider(
            resource=resource,
            shutdown_on_exit=False,
            metric_readers=[
                PeriodicExportingMetricReader(
                    OTLPMetricExporter(
                        endpoint=config.endpoint + "/v1/metrics",
                        headers=config.headers,
                        timeout=5,
                    ),
                    export_interval_millis=60000,
                    export_timeout_millis=5000,
                )
            ],
        )
        traces = TracerProvider(
            resource=resource,
            shutdown_on_exit=False,
            sampler=ParentBased(TraceIdRatioBased(config.sample_ratio)),
            span_limits=SpanLimits(max_attributes=16, max_events=0, max_links=0),
        )
        traces.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(
                    endpoint=config.endpoint + "/v1/traces",
                    headers=config.headers,
                    timeout=5,
                ),
                max_queue_size=512,
                max_export_batch_size=128,
                schedule_delay_millis=5000,
                export_timeout_millis=5000,
            )
        )
        _runtime = Runtime(config, traces, meters)
        install_diagnostic_redaction(structured=True)


def shutdown() -> None:
    """Drain outside controlled work with a finite caller wait, then detach."""
    global _runtime
    with _LOCK:
        runtime, _runtime = _runtime, None
    if runtime is None:
        return

    def drain() -> None:
        try:
            runtime.traces.force_flush(timeout_millis=2000)
            runtime.traces.shutdown()
            runtime.meters.shutdown(timeout_millis=5000)
        except Exception:
            LOG.error("Telemetry shutdown failed; pending diagnostics may be lost.")

    thread = threading.Thread(target=drain, daemon=True, name="telemetry-shutdown")
    thread.start()
    thread.join(timeout=5)
    if thread.is_alive():
        LOG.warning("Telemetry shutdown deadline exceeded; pending diagnostics may be lost.")


def valid_traceparent(value: object) -> str | None:
    """Accept bounded W3C version-00 traceparent only, never baggage/tracestate."""
    if value is None:
        return None
    if isinstance(value, str):
        match = _TRACEPARENT.fullmatch(value)
        if match and int(match[1], 16) and int(match[2], 16):
            return value
    LOG.warning("Invalid trace context ignored.")
    return None


def carrier() -> str | None:
    runtime = _runtime
    if runtime is None:
        return None
    values: dict[str, str] = {}
    runtime.propagator.inject(values)
    return valid_traceparent(values.get("traceparent"))


def correlation() -> dict[str, str]:
    if _runtime is None:
        return {}
    from opentelemetry import trace

    current = trace.get_current_span().get_span_context()
    if not current.is_valid:
        return {}
    return {"trace_id": f"{current.trace_id:032x}", "span_id": f"{current.span_id:016x}"}


def resource_attributes() -> dict[str, str]:
    runtime = _runtime
    if runtime is None:
        return {}
    keys = (
        "service.name",
        "service.version",
        "deployment.environment",
        "deployment.environment.name",
        "telemetry.sdk.name",
        "telemetry.sdk.language",
        "telemetry.sdk.version",
    )
    return {
        key: value
        for key in keys
        if isinstance(value := runtime.traces.resource.attributes.get(key), str)
    }


@dataclass
class Observation:
    span: trace.Span | None
    attributes: dict[str, str | int]
    runtime: Runtime | None = field(repr=False)

    def fail(self, reason: str = "error") -> None:
        error = reason if reason in {"error", "timeout", "cancelled", "rejected"} else "error"
        self.attributes["error.type"] = error
        if self.span is not None:
            from opentelemetry.trace import StatusCode

            self.span.set_attribute("error.type", error)
            self.span.set_status(StatusCode.ERROR)

    def http_status(self, status: int) -> None:
        code = status if 100 <= status <= 599 else 500
        self.attributes["http.response.status_code"] = code
        if self.span is not None:
            self.span.set_attribute("http.response.status_code", code)
        if code >= 500:
            self.fail()

    def usage(self, input_tokens: int, output_tokens: int) -> None:
        """Only call after existing consumption validation/settlement succeeds."""
        for direction, value in (("input", input_tokens), ("output", output_tokens)):
            if type(value) is not int or not 0 <= value <= 10**12:
                raise ValueError("Invalid settled telemetry usage.")
            if self.span is not None:
                self.span.set_attribute(f"gen_ai.usage.{direction}_tokens", value)
            if self.runtime is not None:
                self.runtime.tokens[direction].add(
                    value,
                    {
                        "gen_ai.operation.name": "chat",
                        "gen_ai.provider.name": "azure.ai.openai",
                    },
                )


@contextmanager
def operation(
    name: OperationName,
    *,
    parent: str | None = None,
    root: bool = False,
    capability: str | None = None,
    method: str | None = None,
    backend: Literal["servicebus", "other_sql"] = "servicebus",
) -> Iterator[Observation]:
    """Emit only closed operation/attribute vocabularies, with no exception events."""
    kinds = {
        "http.server": "SERVER",
        "http.client": "CLIENT",
        "messaging.publish": "PRODUCER",
        "messaging.process": "CONSUMER",
        "db.transaction": "CLIENT",
        "invoke_workflow": "INTERNAL",
        "chat": "CLIENT",
    }
    if name not in kinds:
        raise ValueError("Invalid telemetry operation.")
    attributes: dict[str, str | int] = {}
    span_name: str = name
    if name.startswith("http."):
        verb = method if method in _METHODS else "_OTHER"
        attributes["http.request.method"] = verb
        span_name = str(verb)
    elif name.startswith("messaging."):
        verb = "publish" if name.endswith("publish") else "process"
        attributes.update(
            {
                "messaging.system": backend,
                "messaging.destination.name": "agent-tasks",
                "messaging.operation.type": "send" if verb == "publish" else "process",
            }
        )
        span_name = f"{verb} agent-tasks"
    elif name in {"invoke_workflow", "chat"}:
        attributes["gen_ai.operation.name"] = name
        if name == "chat":
            attributes["gen_ai.provider.name"] = "azure.ai.openai"
        elif capability in CAPABILITIES:
            attributes["gen_ai.agent.name"] = capability
            span_name = f"invoke_workflow {capability}"
    remote = valid_traceparent(parent)
    runtime = _runtime
    span_context: AbstractContextManager[trace.Span | None] = nullcontext(None)
    started = 0.0
    if runtime is not None:
        from opentelemetry import context, trace

        parent_context = context.Context() if root else None
        if remote:
            parent_context = runtime.propagator.extract(
                {"traceparent": remote}, context=context.Context()
            )
        span_context = runtime.tracer.start_as_current_span(
            span_name,
            context=parent_context,
            kind=trace.SpanKind[kinds[name]],
            attributes=attributes,
            record_exception=False,
            set_status_on_exception=False,
        )
        started = time.perf_counter()
    with span_context as span:
        observation = Observation(span, attributes, runtime)
        try:
            yield observation
        except BaseException as exc:
            observation.fail("timeout" if isinstance(exc, TimeoutError) else "error")
            raise
        finally:
            if runtime and name in runtime.durations:
                runtime.durations[name].record(time.perf_counter() - started, attributes)
