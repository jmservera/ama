"""Focused offline tests for tools/ama-worker-watch.py (Refs #1204)."""

import importlib.util
import unittest
from pathlib import Path
from unittest import mock

TOOL = Path(__file__).with_name("ama-worker-watch.py")
spec = importlib.util.spec_from_file_location("ama_worker_watch", TOOL)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def run(snapshots, timeout=10.0):
    states = iter(snapshots)
    ticks = iter(range(0, 1000, 3))
    return mod.watch(
        ["rpi-1", "rpi-2", "rpi-3"],
        timeout=timeout,
        poll=1,
        query=lambda: set(next(states)),
        pause=lambda _s: None,
        clock=lambda: next(ticks),
        stamp=lambda: "T",
    )


class WatchTests(unittest.TestCase):
    def test_absent_before_start_is_error_not_completion(self):
        with self.assertRaises(mod.WatchError) as ctx:
            run([["rpi-1", "rpi-3"]])
        self.assertEqual(ctx.exception.code, mod.EXIT_START_MISSING)
        self.assertEqual(ctx.exception.missing, ["rpi-2"])

    def test_first_completion_reports_finished_and_remaining(self):
        event, code = run([["rpi-1", "rpi-2", "rpi-3"], ["rpi-1", "rpi-3", "other"]])
        self.assertEqual(code, mod.EXIT_FINISHED)
        self.assertEqual(event["finished"], [{"session": "rpi-2", "observed_at": "T"}])
        self.assertEqual(event["remaining"], ["rpi-1", "rpi-3"])

    def test_timeout_is_distinct(self):
        full = ["rpi-1", "rpi-2", "rpi-3"]
        event, code = run([full] * 20, timeout=5.0)
        self.assertEqual(code, mod.EXIT_TIMEOUT)
        self.assertEqual(event["event"], "watch_timeout")
        self.assertEqual(event["finished"], [])
        self.assertEqual(event["remaining"], full)

    def test_tmux_failure_and_missing_binary_raise(self):
        failed = mock.Mock(returncode=1, stderr="boom", stdout="")
        with mock.patch.object(mod.subprocess, "run", return_value=failed):
            with self.assertRaises(mod.WatchError):
                mod.list_sessions()
        with mock.patch.object(mod.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaises(mod.WatchError):
                mod.list_sessions()

    def test_no_server_means_no_sessions(self):
        none = mock.Mock(returncode=1, stderr="no server running on /tmp/x", stdout="")
        with mock.patch.object(mod.subprocess, "run", return_value=none):
            self.assertEqual(mod.list_sessions(), set())

    def test_main_exit_code_on_missing_start(self):
        with (
            mock.patch.object(mod, "list_sessions", return_value=set()),
            mock.patch("builtins.print"),
        ):
            self.assertEqual(mod.main(["rpi-9"]), mod.EXIT_START_MISSING)


if __name__ == "__main__":
    unittest.main()
