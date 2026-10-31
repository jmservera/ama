"""Dispatch half of the proposal-only assistants: the agents worker.

The worker turns a queued task message into a bounded provider call and a result
message. It has no database, blob or Key Vault access (ADR 0001) and cannot
change a case, approve or send anything. Leases, fences, allowance, release
admission, quarantine and human review stay with the API, which validates and
stores the result. Transport adapters (the `agent-tasks` queue and the API
post-back) belong to issue #144; this module defines the ports they implement.
"""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from zava_forward.core import assistants
from zava_forward.core.ai_consumption import CallContext, call_context, reference

MAX_MESSAGE_CHARS = 64000
TASK_KEYS = (
    "id",
    "capability",
    "case_id",
    "version",
    "source_signature",
    "fence",
    "owner",
    "snapshot",
)
FAILED_ENVELOPE = {"usage": None, "source": "unverified", "text": None}


Provider = Callable[[str, str, int, int], dict[str, Any]]
"""(system, prompt, max_tokens, timeout) -> raw provider envelope."""


def foundry_provider(ai: Any) -> Provider:
    """Adapt a core `Ai` client; its `evidence` method already returns a durable-safe envelope."""
    return lambda system, prompt, max_tokens, timeout: ai.evidence(
        system, prompt, max_tokens, timeout
    )


@dataclass(frozen=True)
class TaskMessage:
    """A claimed task as the API queues it; only the permitted inert snapshot."""

    task: dict[str, Any]
    max_tokens: int
    timeout: int

    @classmethod
    def from_task(cls, task: dict[str, Any], limits: Any) -> TaskMessage:
        return cls(
            task={k: task[k] for k in TASK_KEYS},
            max_tokens=limits.output_tokens,
            timeout=limits.timeout,
        )

    def to_json(self) -> str:
        return str(
            assistants.canonical(
                dict(task=self.task, max_tokens=self.max_tokens, timeout=self.timeout)
            )
        )

    @classmethod
    def from_json(cls, text: str) -> TaskMessage:
        if not isinstance(text, str) or len(text) > MAX_MESSAGE_CHARS:
            raise ValueError("Task message exceeds bounds.")
        raw = json.loads(text)
        task = raw["task"]
        if (
            not isinstance(task, dict)
            or set(task) != set(TASK_KEYS)
            or task["capability"] not in assistants.REGISTRY
        ):
            raise ValueError("Malformed task message.")
        max_tokens, timeout = raw["max_tokens"], raw["timeout"]
        if (
            type(max_tokens) is not int
            or type(timeout) is not int
            or not 1 <= timeout <= 40
            or not 1 <= max_tokens <= 2000
        ):
            raise ValueError("Task message bounds are invalid.")
        return cls(task=task, max_tokens=max_tokens, timeout=timeout)


@dataclass(frozen=True)
class ResultMessage:
    """The worker's result; the API re-validates, re-checks fence and release, and stores it."""

    task_id: str
    fence: int
    owner: str
    envelope: dict[str, Any]
    output: dict[str, Any] | None
    failure: str | None

    def to_json(self) -> str:
        body = dict(
            task_id=self.task_id,
            fence=self.fence,
            owner=self.owner,
            envelope=self.envelope,
            output=self.output,
            failure=self.failure,
        )
        return str(assistants.canonical(body))

    @classmethod
    def from_json(cls, text: str) -> ResultMessage:
        raw = json.loads(text)
        return cls(
            raw["task_id"],
            raw["fence"],
            raw["owner"],
            raw["envelope"],
            raw["output"],
            raw["failure"],
        )


class TaskQueue(Protocol):
    def receive(self) -> tuple[str, TaskMessage] | None: ...

    def ack(self, receipt: str) -> None: ...

    def release(self, receipt: str) -> None: ...


class ResultSink(Protocol):
    def post(self, result: ResultMessage) -> None: ...


class InMemoryQueue:
    """Local and test transport. Unacknowledged messages are redelivered."""

    def __init__(self, messages: list[TaskMessage] | None = None) -> None:
        self.pending: list[tuple[str, TaskMessage]] = [
            (str(i), m) for i, m in enumerate(messages or [])
        ]
        self.leased: dict[str, TaskMessage] = {}
        self.acked: list[str] = []

    def receive(self) -> tuple[str, TaskMessage] | None:
        if not self.pending:
            return None
        receipt, message = self.pending.pop(0)
        self.leased[receipt] = message
        return receipt, message

    def ack(self, receipt: str) -> None:
        self.leased.pop(receipt, None)
        self.acked.append(receipt)

    def release(self, receipt: str) -> None:
        message = self.leased.pop(receipt, None)
        if message is not None:
            self.pending.append((receipt, message))


class AgentWorker:
    def __init__(self, provider: Provider, active_calls: int = 2) -> None:
        self.provider = provider
        self.slots = threading.BoundedSemaphore(active_calls)
        self.stop_event = threading.Event()

    def provider_call(
        self, system: str, prompt: str, max_tokens: int, timeout: int
    ) -> dict[str, Any]:
        """One provider call; never raises and always returns an envelope with an outcome."""
        try:
            result = self.provider(system, prompt, max_tokens, timeout)
        except Exception:
            return dict(FAILED_ENVELOPE, outcome="provider-unavailable")
        if not isinstance(result, dict):
            return dict(FAILED_ENVELOPE, outcome="malformed-provider-envelope")
        return result

    def _bounded(
        self,
        system: str,
        prompt: str,
        max_tokens: int,
        timeout: int,
        task: dict[str, Any],
    ) -> dict[str, Any]:
        returned, values = threading.Event(), []

        def call() -> None:
            try:
                context = CallContext(
                    reference(task["id"]),
                    reference(f"{task['id']}:{task['fence']}"),
                    task["capability"],
                    "retrofit-case",
                    reference(task["version"]),
                    reference(
                        assistants.canonical(
                            [
                                system,
                                assistants.REGISTRY[task["capability"]]["purpose"],
                                task["version"],
                            ]
                        )
                    ),
                    retry=max(0, task["fence"] - 1),
                )
                with call_context(context):
                    values.append(self.provider_call(system, prompt, max_tokens, timeout))
            finally:
                # A timed-out physical call keeps its slot until it returns.
                self.slots.release()
                returned.set()

        started = time.perf_counter()
        threading.Thread(target=call, daemon=True, name="agents-provider").start()
        while not returned.wait(0.1):
            if self.stop_event.is_set() or time.perf_counter() - started >= timeout:
                break
        if returned.is_set() and time.perf_counter() - started <= timeout:
            return values[0]
        return dict(FAILED_ENVELOPE, outcome="timeout")

    def handle(self, message: TaskMessage, limits: Any) -> ResultMessage | None:
        """Run one task; None when no slot is free or the worker is stopping (redeliver)."""
        task = message.task
        if self.stop_event.is_set() or not self.slots.acquire(blocking=False):
            return None
        system, prompt = assistants.build_request(task)
        if len(system) + len(prompt) > limits.input_chars:
            self.slots.release()
            envelope, output, _ = assistants.shape_result(
                task, dict(FAILED_ENVELOPE, outcome="input-too-large"), limits
            )
            failure: str | None = "Input exceeds limit; manual review required."
        else:
            raw = self._bounded(system, prompt, message.max_tokens, message.timeout, task)
            envelope, output, failure = assistants.shape_result(task, raw, limits)
        return ResultMessage(task["id"], task["fence"], task["owner"], envelope, output, failure)


def run_once(queue: TaskQueue, worker: AgentWorker, sink: ResultSink, limits: Any) -> bool:
    """Receive, handle and post one task; acknowledge only after the post succeeds."""
    received = queue.receive()
    if received is None:
        return False
    receipt, message = received
    try:
        result = worker.handle(message, limits)
        if result is None:
            queue.release(receipt)
            return False
        sink.post(result)
    except Exception:
        queue.release(receipt)
        return False
    queue.ack(receipt)
    return True


__all__ = [
    "AgentWorker",
    "InMemoryQueue",
    "Provider",
    "ResultMessage",
    "ResultSink",
    "TaskMessage",
    "TaskQueue",
    "foundry_provider",
    "run_once",
]
