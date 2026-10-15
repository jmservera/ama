import json
import threading
import time
import unittest
from typing import Any

from zava_forward.core import assistants

from zava_forward.agents.dispatch import (
    AgentWorker,
    InMemoryQueue,
    ResultMessage,
    TaskMessage,
    run_once,
)

SNAPSHOT: dict[str, Any] = {"citations": ["home.epc", "survey.epc"], "unknowns": ["survey.built"]}


def make_task() -> dict[str, Any]:
    return dict(
        id="t1",
        capability="stock-prioritisation",
        case_id="ZF-1",
        version=assistants.VERSION,
        source_signature="sig",
        fence=3,
        owner="own",
        snapshot=dict(SNAPSHOT),
    )


def good_text() -> str:
    return json.dumps(
        dict(
            summary="EPC differs from the survey.",
            findings=[dict(text="Recorded EPC is D; survey says C.", citations=["home.epc"])],
            unknowns=[],
        )
    )


def returned(text: str | None) -> dict[str, Any]:
    return dict(
        provider="azure-openai",
        deployment="d",
        model="m1",
        outcome="returned",
        source="ai",
        usage=dict(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        text=text,
    )


def limits() -> assistants.Limits:
    return assistants.Limits(
        dict(
            ZF_ASSIST_AUTHORITY="op",
            ZF_ASSIST_CALL_ALLOWANCE="10",
            ZF_ASSIST_TOKEN_ALLOWANCE="1000000",
            ZF_ASSIST_EXPIRES="2999-01-01T00:00:00Z",
        )
    )


class Sink:
    def __init__(self, fail: bool = False) -> None:
        self.results: list[ResultMessage] = []
        self.fail = fail

    def post(self, result: ResultMessage) -> None:
        if self.fail:
            raise OSError("api unavailable")
        self.results.append(result)


def message(task: dict[str, Any] | None = None) -> TaskMessage:
    return TaskMessage.from_task(task or make_task(), limits())


class WorkerTests(unittest.TestCase):
    def handle(self, provider: Any, task: dict[str, Any] | None = None) -> ResultMessage:
        result = AgentWorker(provider).handle(message(task), limits())
        assert result is not None
        return result

    def test_valid_output_is_shaped_and_unapproved(self) -> None:
        r = self.handle(lambda *a: returned(good_text()))
        self.assertIsNone(r.failure)
        assert r.output is not None
        self.assertEqual(r.output["unknowns"], ["survey.built"])
        self.assertIs(r.envelope["approved"], False)
        self.assertEqual((r.task_id, r.fence, r.owner), ("t1", 3, "own"))

    def test_request_matches_the_api_request(self) -> None:
        seen: list[tuple[str, str]] = []

        def provider(system: str, prompt: str, tokens: int, timeout: int) -> dict[str, Any]:
            seen.append((system, prompt))
            return returned(good_text())

        self.handle(provider)
        self.assertEqual(seen[0], assistants.build_request(make_task()))

    def test_failures_keep_no_text_or_exception_detail(self) -> None:
        def boom(*a: Any) -> dict[str, Any]:
            raise RuntimeError("secret-token-123")

        for provider in (
            boom,
            lambda *a: "not a dict",
            lambda *a: returned("{not json"),
            lambda *a: returned("x" * 9000),
        ):
            r = self.handle(provider)
            self.assertIsNone(r.output)
            self.assertTrue(r.failure)
            self.assertNotIn("secret-token-123", r.to_json())
            self.assertNotIn("not json", r.to_json())
            self.assertEqual(r.envelope["source"], "unverified")

    def test_uncited_forbidden_and_unreturned_output_is_rejected(self) -> None:
        uncited = json.dumps(
            dict(summary="s", findings=[dict(text="t", citations=["other"])], unknowns=[])
        )
        forbidden = json.dumps(
            dict(
                summary="I have sent the email",
                findings=[dict(text="t", citations=["home.epc"])],
                unknowns=[],
            )
        )
        self.assertIsNone(self.handle(lambda *a: returned(uncited)).output)
        self.assertIsNone(self.handle(lambda *a: returned(forbidden)).output)
        template = dict(returned(good_text()), source="template")
        self.assertIsNotNone(self.handle(lambda *a: template).failure)

    def test_timeout_outcome(self) -> None:
        release = threading.Event()

        def slow(system: str, prompt: str, tokens: int, timeout: int) -> dict[str, Any]:
            release.wait(5)
            return returned(good_text())

        task = make_task()
        msg = TaskMessage(task=task, max_tokens=100, timeout=1)
        started = time.perf_counter()
        result = AgentWorker(slow).handle(msg, limits())
        release.set()
        assert result is not None
        self.assertEqual(result.envelope["outcome"], "timeout")
        self.assertLess(time.perf_counter() - started, 3)

    def test_busy_or_stopped_worker_returns_none(self) -> None:
        worker = AgentWorker(lambda *a: returned(good_text()), active_calls=1)
        self.assertTrue(worker.slots.acquire(blocking=False))
        self.assertIsNone(worker.handle(message(), limits()))
        worker.slots.release()
        worker.stop_event.set()
        self.assertIsNone(worker.handle(message(), limits()))

    def test_oversize_input_never_calls_the_provider(self) -> None:
        calls: list[int] = []
        task = make_task()
        task["snapshot"] = dict(SNAPSHOT, big="x" * 13000)

        def provider(system: str, prompt: str, tokens: int, timeout: int) -> dict[str, Any]:
            calls.append(1)
            return returned(good_text())

        r = self.handle(provider, task)
        self.assertEqual(calls, [])
        self.assertEqual(r.envelope["outcome"], "input-too-large")
        self.assertIsNone(r.output)

    def test_slot_is_released_after_each_call(self) -> None:
        worker = AgentWorker(lambda *a: returned(good_text()), active_calls=1)
        for _ in range(3):
            self.assertIsNotNone(worker.handle(message(), limits()))


class MessageTests(unittest.TestCase):
    def test_task_round_trip_and_bounds(self) -> None:
        m = message()
        self.assertEqual(TaskMessage.from_json(m.to_json()), m)
        for bad in ("x" * 70000, json.dumps(dict(task={}, max_tokens=1, timeout=1))):
            with self.assertRaises(ValueError):
                TaskMessage.from_json(bad)
        raw = json.loads(m.to_json())
        raw["task"]["capability"] = "unknown"
        with self.assertRaises(ValueError):
            TaskMessage.from_json(json.dumps(raw))
        raw = json.loads(m.to_json())
        raw["timeout"] = 999
        with self.assertRaises(ValueError):
            TaskMessage.from_json(json.dumps(raw))

    def test_task_message_has_only_the_allowed_keys(self) -> None:
        task = dict(make_task(), email="a@b.c", resident="private")
        self.assertEqual(set(message(task).task), set(make_task()))

    def test_result_round_trip(self) -> None:
        r = ResultMessage("t", 1, "o", dict(approved=False), None, "failed")
        self.assertEqual(ResultMessage.from_json(r.to_json()), r)


class QueueTests(unittest.TestCase):
    def test_ack_after_successful_post(self) -> None:
        queue, sink = InMemoryQueue([message()]), Sink()
        worker = AgentWorker(lambda *a: returned(good_text()))
        self.assertTrue(run_once(queue, worker, sink, limits()))
        self.assertEqual(len(sink.results), 1)
        self.assertEqual(queue.acked, ["0"])
        self.assertFalse(run_once(queue, worker, sink, limits()))

    def test_failed_post_is_redelivered_not_acknowledged(self) -> None:
        queue = InMemoryQueue([message()])
        worker = AgentWorker(lambda *a: returned(good_text()))
        self.assertFalse(run_once(queue, worker, Sink(fail=True), limits()))
        self.assertEqual(queue.acked, [])
        self.assertEqual(len(queue.pending), 1)
        self.assertTrue(run_once(queue, worker, Sink(), limits()))

    def test_busy_worker_leaves_message_for_redelivery(self) -> None:
        queue = InMemoryQueue([message()])
        worker = AgentWorker(lambda *a: returned(good_text()), active_calls=1)
        worker.slots.acquire()
        self.assertFalse(run_once(queue, worker, Sink(), limits()))
        self.assertEqual(len(queue.pending), 1)


if __name__ == "__main__":
    unittest.main()
