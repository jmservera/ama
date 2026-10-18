"""Offline evidence-contract regressions; no configured stores or private inputs."""

import contextlib
import io
import itertools
import json
import os
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from pathlib import Path
from types import TracebackType
from typing import Any
from unittest.mock import MagicMock, Mock, patch

from zava_forward.core.synthetic import loadcheck

PRIVATE_ERROR = "private sentinel must not appear in reports"


class InlineThread:
    def __init__(self, target: Callable[[int], None], args: tuple[int]) -> None:
        self.target, self.args = target, args
        self.started = False

    def start(self) -> None:
        self.started = True
        self.target(*self.args)

    def join(self) -> None:
        if not self.started:
            raise AssertionError("must not join an unstarted worker")


class FailedStartThread(InlineThread):
    def start(self) -> None:
        if self.args[0] == 0:
            raise RuntimeError(PRIVATE_ERROR)
        super().start()


def store_fixture() -> Mock:
    return Mock(cases={"SYN-1": {}, "SYN-2": {}})


def broken_ids() -> MagicMock:
    ids = MagicMock(spec=list)
    ids.__len__.return_value = 2

    def select(index: int) -> str:
        if index == 0:
            raise IndexError(PRIVATE_ERROR)
        return "SYN-2"

    ids.__getitem__.side_effect = select
    return ids


class LoadcheckEvidenceTests(unittest.TestCase):
    def run_once(
        self,
        store: Mock | None = None,
        sessions: int = 1,
        writers: int = 1,
        ticks: list[float] | None = None,
        durations: list[float] | None = None,
        seconds: float = 1,
    ) -> dict[str, Any]:
        with (
            patch.object(threading, "Thread", InlineThread),
            patch.object(
                time,
                "monotonic",
                side_effect=ticks if ticks is not None else [0] + [0, 2] * sessions,
            ),
            patch.object(time, "time", side_effect=AssertionError("wall clock used")),
            patch.object(
                time,
                "perf_counter",
                side_effect=durations if durations is not None else itertools.count(0, 0.125),
            ),
        ):
            return loadcheck.run(
                store if store is not None else store_fixture(), {}, seconds, sessions, writers
            )

    def assert_missing(self, report: dict[str, Any], kind: str) -> None:
        self.assertEqual(
            report["classes"][kind],
            dict(n=0, p50=None, p95=None, max=None, limit=loadcheck.LIMITS[kind], within=False),
        )

    def test_percentile_absence_and_existing_order_statistic(self) -> None:
        self.assertIsNone(loadcheck.pct([], 0.95))
        self.assertEqual(loadcheck.pct([3.0, 1.0, 2.0], 0.5), 2.0)
        self.assertEqual(loadcheck.pct([3.0, 1.0, 2.0], 0.95), 3.0)

    def test_grow_rejects_invalid_size_and_empty_seed(self) -> None:
        for homes in (0, -1, True, 1.5):
            with self.subTest(homes=homes), self.assertRaises(ValueError):
                loadcheck.grow({"cases": [{}]}, homes)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "at least one case"):
            loadcheck.grow({"cases": []}, 1)

    def test_run_rejects_invalid_parameters_before_reading_store(self) -> None:
        store = Mock(spec=[])
        for seconds, sessions, writers in (
            (0, 1, 1),
            (-1, 1, 1),
            (float("nan"), 1, 1),
            (float("inf"), 1, 1),
            (10**400, 1, 1),
            (-(10**400), 1, 1),
            (True, 1, 1),
            (1, 0, 0),
            (1, -1, 1),
            (1, True, 1),
            (1, 1.5, 1),
            (1, 1, 0),
            (1, 1, -1),
            (1, 1, 2),
            (1, 1, True),
            (1, 2, 1.5),
        ):
            with (
                self.subTest(seconds=seconds, sessions=sessions, writers=writers),
                self.assertRaises(ValueError),
            ):
                loadcheck.run(store, {}, seconds, sessions, writers)  # type: ignore[arg-type]
        self.assertEqual(store.mock_calls, [])

    def test_empty_workload_rejected_before_workers(self) -> None:
        with patch.object(threading, "Thread") as worker:
            with self.assertRaisesRegex(ValueError, "at least one case"):
                loadcheck.run(Mock(cases={}), {}, 1)
            worker.assert_not_called()

    def test_no_observations_are_insufficient(self) -> None:
        for seconds in (1, sys.float_info.max, int(sys.float_info.max)):
            with self.subTest(seconds=seconds):
                report = self.run_once(ticks=[0, float("inf")], seconds=seconds)
                self.assertEqual(report["errors"], 0)
                for kind in loadcheck.LIMITS:
                    self.assert_missing(report, kind)

    def test_missing_required_writer_measurements_cannot_pass(self) -> None:
        store = store_fixture()
        store.log_call.side_effect = RuntimeError(PRIVATE_ERROR)
        report = self.run_once(store)
        self.assert_missing(report, "write")
        self.assertTrue(report["classes"]["list"]["within"])
        self.assertTrue(report["classes"]["detail"]["within"])
        self.assertEqual(report["errors"], 1)

    def test_request_exceptions_are_counted_by_kind_without_private_text(self) -> None:
        for kind, method in (("list", "page_cases"), ("detail", "detail"), ("write", "log_call")):
            store = store_fixture()
            getattr(store, method).side_effect = RuntimeError(PRIVATE_ERROR)
            with self.subTest(kind=kind):
                report = self.run_once(store)
                self.assertEqual(report["errors"], 1)
                self.assertEqual(report["error_kinds"], [f"{kind}: RuntimeError"])
                self.assert_missing(report, kind)
                self.assertNotIn(PRIVATE_ERROR, json.dumps(report))

    def test_raw_latency_limits_are_inclusive_and_not_rounded_for_acceptance(self) -> None:
        for excess in (0.0, 0.00001):
            with self.subTest(excess=excess):
                report = self.run_once(durations=[0, 1 + excess, 0, 1 + excess, 0, 2 + excess])
                for kind, limit in loadcheck.LIMITS.items():
                    self.assertEqual(report["classes"][kind]["within"], excess == 0)
                    self.assertEqual(report["classes"][kind]["p95"], limit)

    def test_success_preserves_default_session_writer_mix(self) -> None:
        store = store_fixture()
        report = self.run_once(store, sessions=5, writers=2)
        self.assertEqual(report["errors"], 0)
        self.assertEqual(report["error_kinds"], [])
        for kind, count in (("list", 5), ("detail", 5), ("write", 2)):
            self.assertEqual(report["classes"][kind]["n"], count)
            self.assertTrue(report["classes"][kind]["within"])
        self.assertEqual(store.page_cases.call_count, 5)
        self.assertEqual(store.detail.call_count, 5)
        self.assertEqual(store.log_call.call_count, 2)

    def test_worker_start_failure_retains_healthy_observations(self) -> None:
        with (
            patch.object(threading, "Thread", FailedStartThread),
            patch.object(time, "monotonic", side_effect=[0, 0, 2]),
            patch.object(time, "perf_counter", return_value=0),
        ):
            report = loadcheck.run(store_fixture(), {}, 1, sessions=2, writers=2)
        self.assertEqual(report["errors"], 1)
        self.assertEqual(report["error_kinds"], ["startup: RuntimeError"])
        self.assertTrue(all(c["within"] and c["n"] == 1 for c in report["classes"].values()))
        self.assertNotIn(PRIVATE_ERROR, json.dumps(report))

    def test_worker_selection_failure_retains_healthy_observations(self) -> None:
        with patch.object(loadcheck, "list", return_value=broken_ids(), create=True):
            report = self.run_once(sessions=2, writers=2, ticks=[0, 0, 0, 2])
        self.assertEqual(report["errors"], 1)
        self.assertEqual(report["error_kinds"], ["session: IndexError"])
        self.assertTrue(all(c["within"] and c["n"] == 1 for c in report["classes"].values()))
        self.assertNotIn(PRIVATE_ERROR, json.dumps(report))

    def test_shared_monotonic_cutoff_and_entered_cycle_completion(self) -> None:
        store = store_fixture()
        with (
            patch.object(threading, "Thread", InlineThread),
            patch.object(time, "time", side_effect=AssertionError("wall clock used")),
            patch.object(time, "monotonic", side_effect=[10, 10.5, 11, 11]) as clock,
            patch.object(time, "perf_counter", side_effect=[0, 2, 2, 4, 4, 6]),
        ):
            report = loadcheck.run(store, {}, 1, sessions=2, writers=2)
        self.assertEqual(clock.call_count, 4)
        self.assertTrue(all(c["n"] == 1 for c in report["classes"].values()))
        self.assertEqual(store.log_call.call_count, 1)
        self.assertEqual(report["errors"], 0)

    def test_aggregation_wait_is_not_request_latency(self) -> None:
        now = 0.0

        class WaitingLock:
            def __enter__(self) -> None:
                nonlocal now
                now += 10

            def __exit__(
                self,
                exc_type: type[BaseException] | None,
                exc: BaseException | None,
                tb: TracebackType | None,
            ) -> None:
                pass

        def request(*args: Any, **kwargs: Any) -> None:
            nonlocal now
            now += 0.25

        store = store_fixture()
        for method in ("page_cases", "detail", "log_call"):
            getattr(store, method).side_effect = request
        with (
            patch.object(threading, "Thread", InlineThread),
            patch.object(threading, "Lock", WaitingLock),
            patch.object(time, "monotonic", side_effect=[0, 0, 2]),
            patch.object(time, "perf_counter", side_effect=lambda: now),
        ):
            report = loadcheck.run(store, {}, 1, sessions=1, writers=1)
        self.assertTrue(all(c["p95"] == 0.25 and c["within"] for c in report["classes"].values()))

    def test_real_workers_aggregate_all_required_successes(self) -> None:
        calls = threading.local()

        def clock() -> float:
            if threading.current_thread() is threading.main_thread():
                return 0
            count = getattr(calls, "count", 0)
            calls.count = count + 1
            return 0 if count == 0 else 2

        with (
            patch.object(time, "monotonic", side_effect=clock),
            patch.object(time, "time", side_effect=AssertionError("wall clock used")),
            patch.object(time, "perf_counter", return_value=0),
        ):
            report = loadcheck.run(store_fixture(), {}, 1)
        self.assertEqual(report["errors"], 0)
        for kind, count in (("list", 5), ("detail", 5), ("write", 2)):
            self.assertEqual(report["classes"][kind]["n"], count)
            self.assertTrue(report["classes"][kind]["within"])

    def test_cli_invalid_inputs_reject_before_store_initialization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "synthetic.json"
            case = {"id": "SYN-1", "resident": {"name": "Synthetic Resident"}}
            inputs: list[tuple[list[str], list[dict[str, Any]]]] = [
                (["--seconds", "0"], [case]),
                (["--seconds", "-1"], [case]),
                (["--seconds", str(10**400)], [case]),
                (["--seconds", str(-(10**400))], [case]),
                (["--homes", "0"], [case]),
                (["--homes", "-1"], [case]),
                ([], []),
            ]
            for extra, cases in inputs:
                seed.write_text(
                    json.dumps(
                        {
                            "cases": cases,
                            "staff": [{"role": "Retrofit Programme Manager"}],
                        }
                    ),
                    encoding="utf-8",
                )
                with self.subTest(extra=extra, cases=cases):
                    with (
                        patch.dict(os.environ, {}, clear=True),
                        patch.object(tempfile, "tempdir", tmp),
                        patch("zava_forward.core.factory.open_store") as factory,
                        contextlib.redirect_stderr(io.StringIO()),
                        self.assertRaises(SystemExit) as exit_status,
                    ):
                        loadcheck.main(["--data", str(seed), "--homes", "1", *extra])
                    self.assertEqual(exit_status.exception.code, 2)
                    factory.assert_not_called()

    def test_cli_exit_status_tracks_real_run_evidence(self) -> None:
        for mode in ("good", "missing", "request", "latency", "startup", "selection"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                seed = Path(tmp) / "synthetic.json"
                seed.write_text(
                    json.dumps(
                        {
                            "cases": [{"id": "SYN-1"}],
                            "staff": [{"role": "Retrofit Programme Manager"}],
                        }
                    ),
                    encoding="utf-8",
                )
                store = store_fixture()
                if mode == "request":
                    store.detail.side_effect = RuntimeError(PRIVATE_ERROR)
                ticks = [0] + ([2] * 5 if mode == "missing" else [0, 2] * 5)
                if mode == "startup":
                    ticks = [0] + [0, 2] * 4
                if mode == "selection":
                    ticks = [0, 0, 0, 2, 0, 0, 2, 0]
                out = io.StringIO()
                with contextlib.ExitStack() as stack:
                    stack.enter_context(patch.dict(os.environ, {}, clear=True))
                    stack.enter_context(patch.object(tempfile, "tempdir", tmp))
                    factory = stack.enter_context(
                        patch("zava_forward.core.factory.open_store", return_value=store)
                    )
                    stack.enter_context(
                        patch.object(
                            threading,
                            "Thread",
                            FailedStartThread if mode == "startup" else InlineThread,
                        )
                    )
                    stack.enter_context(patch.object(time, "monotonic", side_effect=ticks))
                    stack.enter_context(
                        patch.object(
                            time,
                            "time",
                            side_effect=AssertionError("wall clock used"),
                        )
                    )
                    stack.enter_context(
                        patch.object(
                            time,
                            "perf_counter",
                            side_effect=itertools.count(0, 3 if mode == "latency" else 0.125),
                        )
                    )
                    if mode == "selection":
                        stack.enter_context(
                            patch.object(loadcheck, "list", return_value=broken_ids(), create=True)
                        )
                    stack.enter_context(contextlib.redirect_stdout(out))
                    status = loadcheck.main(["--data", str(seed), "--homes", "1", "--seconds", "1"])
                report = json.loads(out.getvalue())
                self.assertEqual(status, 0 if mode == "good" else 1)
                self.assertEqual(report["homes"], 1)
                self.assertEqual(report["seconds"], 1)
                self.assertEqual(report["store"], "sqlite")
                self.assertIs(report["synthetic"], True)
                self.assertNotIn(PRIVATE_ERROR, out.getvalue())
                env = factory.call_args.args[0]
                self.assertEqual(set(env), {"ZF_DATA", "ZF_STATE", "ZF_STORE"})
                self.assertTrue(Path(env["ZF_STATE"]).is_relative_to(tmp))
                self.assertTrue(Path(env["ZF_DATA"]).is_relative_to(env["ZF_STATE"]))
                self.assertFalse(Path(env["ZF_STATE"]).exists())


if __name__ == "__main__":
    unittest.main()
