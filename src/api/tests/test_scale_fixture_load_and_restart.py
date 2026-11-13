"""Separate-process API load and hard-restart run over the scale fixture (issue 144, C4 and C5).

The API server runs as its own OS process on loopback over a SQLite SQL store with fictional
homes only, so server RSS is measured without the load client. A concurrent closed-loop load
runs, the process is killed with SIGKILL (no graceful shutdown), restarted on the same store
file, and the audit chain must be intact with every acknowledged entry still present.
Single OS process only: this is not a hosted replica, Azure, autoscaling or production-scale
claim. Cost stays out of scope here (see scale_load.py for cost drivers).

Benchmark, from src/api with installed distributions:
    PYTHONPATH=../core/tests:../agents/tests python3 tests/test_scale_fixture_load_and_restart.py \
        --homes 60000 --out report.json
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import platform
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from typing import Any

from test_sqlreads import STAFF

import scale_load

PASSWORD = "zf-restart"
CALLS_BEFORE = 3
MIX = (("list", 6), ("detail", 3), ("dashboard", 1))


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def rss_mib(pid: int, key: str = "VmRSS") -> float:
    for line in Path(f"/proc/{pid}/status").read_text().splitlines():
        if line.startswith(key + ":"):
            return round(int(line.split()[1]) / 1024, 1)
    return 0.0


class ApiProcess:
    """One API server process on a fixed store file."""

    def __init__(self, seed: Path, sqlite: Path, port: int) -> None:
        self.base = f"http://127.0.0.1:{port}"
        env = {
            **os.environ,
            "ZF_STORE": "sqlite",
            "ZF_DATA": str(seed),
            "ZF_SQLITE": str(sqlite),
            "ZF_PASSWORD": PASSWORD,
            "PORT": str(port),
            "ZF_BIND": "127.0.0.1",
        }
        env.pop("ZF_AUTH", None)
        self.process = subprocess.Popen(
            [sys.executable, "-m", "zava_forward.api.server"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.cookie = ""

    def wait_ready(self, timeout: float = 120) -> float:
        started = time.perf_counter()
        while time.perf_counter() - started < timeout:
            if self.process.poll() is not None:
                raise RuntimeError("API process exited before becoming ready.")
            code, _, _ = scale_load.call(self.base, "/healthz") if self._up() else (0, {}, b"")
            if code == 200:
                return time.perf_counter() - started
            time.sleep(0.1)
        raise RuntimeError("API process did not become ready.")

    def _up(self) -> bool:
        try:
            with socket.create_connection(("127.0.0.1", int(self.base.rsplit(":", 1)[1])), 0.5):
                return True
        except OSError:
            return False

    def login(self) -> None:
        code, headers, _ = scale_load.call(
            self.base, "/api/login", body={"email": STAFF[1]["email"], "password": PASSWORD}
        )
        if code != 200:
            raise RuntimeError(f"Staff login failed with {code}.")
        self.cookie = headers["Set-Cookie"].split(";")[0]

    def get(self, path: str) -> tuple[int, Any]:
        code, _, payload = scale_load.call(self.base, path, self.cookie)
        return code, json.loads(payload) if payload.startswith((b"{", b"[")) else payload

    def post(self, path: str, body: dict[str, Any]) -> int:
        return scale_load.call(self.base, path, self.cookie, body)[0]

    def kill(self) -> None:
        self.process.send_signal(signal.SIGKILL)
        self.process.wait(timeout=30)

    def stop(self) -> None:
        if self.process.poll() is None:
            self.kill()


def audit_state(api: ApiProcess) -> dict[str, Any]:
    code, report = api.get("/api/audit-check")
    if code != 200:
        raise RuntimeError(f"Audit check failed with {code}.")
    return dict(report)


def acknowledged_calls(api: ApiProcess, count: int, label: str) -> int:
    done = 0
    for index in range(count):
        code = api.post(
            f"/api/cases/ZF-{index:05d}/call",
            {"outcome": "No answer", "note": f"{label} {index}", "channel": "Phone"},
        )
        done += code == 200
    return done


def closed_loop(api: ApiProcess, homes: int, concurrency: int, seconds: float) -> dict[str, Any]:
    names = [name for name, weight in MIX for _ in range(weight)]
    samples: dict[str, list[float]] = {name: [] for name, _ in MIX}
    errors = {name: 0 for name, _ in MIX}
    lock = threading.Lock()
    peak = [0.0]
    deadline = time.perf_counter() + seconds
    stop = threading.Event()

    def sample_rss() -> None:
        while not stop.is_set():
            peak[0] = max(peak[0], rss_mib(api.process.pid))
            time.sleep(0.25)

    def worker(index: int) -> None:
        import random

        rnd = random.Random(index)
        while time.perf_counter() < deadline:
            name = rnd.choice(names)
            if name == "list":
                offset = rnd.randrange(0, max(1, homes - 49), 50)
                path = f"/api/cases?view=all&limit=50&offset={offset}"
            elif name == "detail":
                path = f"/api/cases/ZF-{rnd.randrange(homes):05d}"
            else:
                path = "/api/progress"
            begin = time.perf_counter()
            try:
                code = scale_load.call(api.base, path, api.cookie)[0]
            except OSError:
                code = 0
            elapsed = (time.perf_counter() - begin) * 1000
            with lock:
                samples[name].append(elapsed)
                errors[name] += code != 200

    sampler = threading.Thread(target=sample_rss, daemon=True)
    sampler.start()
    started = time.perf_counter()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(concurrency)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    wall = time.perf_counter() - started
    stop.set()
    sampler.join()
    every = [value for values in samples.values() for value in values]
    total = len(every)
    failed = sum(errors.values())
    return {
        "concurrency": concurrency,
        "wall_seconds": round(wall, 1),
        "requests": total,
        "errors": failed,
        "error_rate": round(failed / total, 4) if total else 1.0,
        "requests_per_second": round(total / wall, 2),
        "p50_ms": scale_load.percentile(every, 0.5),
        "p95_ms": scale_load.percentile(every, 0.95),
        "routes": {
            name: {
                "requests": len(values),
                "errors": errors[name],
                "p50_ms": scale_load.percentile(values, 0.5),
                "p95_ms": scale_load.percentile(values, 0.95),
            }
            for name, values in samples.items()
        },
        "server_rss_peak_mib_sampled": peak[0],
    }


def run(homes: int, concurrency: int, seconds: float) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="zf-restart-") as tmp, contextlib.ExitStack() as stack:
        directory = Path(tmp)
        begun = time.perf_counter()
        store, events = scale_load.build_store(directory, homes)
        store.db.close()
        setup_seconds = time.perf_counter() - begun
        seed, sqlite = directory / "zavaforward.json", directory / "scale.sqlite"
        port = free_port()

        first = ApiProcess(seed, sqlite, port)
        stack.callback(first.stop)
        cold_start = first.wait_ready()
        first.login()
        acked = acknowledged_calls(first, CALLS_BEFORE, "before")
        before = audit_state(first)
        load = closed_loop(first, homes, concurrency, seconds)
        rss = {
            "after_load_mib": rss_mib(first.process.pid),
            "high_water_mib": rss_mib(first.process.pid, "VmHWM"),
        }
        before_kill = audit_state(first)
        first.kill()

        second = ApiProcess(seed, sqlite, port)
        stack.callback(second.stop)
        restart_ready = second.wait_ready()
        second.login()
        after = audit_state(second)
        acked_after = acknowledged_calls(second, 1, "after")
        final = audit_state(second)
        restart = {
            "kill": "SIGKILL, no graceful shutdown",
            "restart_ready_seconds": round(restart_ready, 2),
            "acknowledged_calls_before_kill": acked,
            "entries_before_kill": before_kill["entries"],
            "entries_after_restart": after["entries"],
            "chain_intact_after_restart": bool(after["intact"]),
            "acknowledged_call_after_restart": acked_after,
            "entries_after_new_write": final["entries"],
            "chain_intact_after_new_write": bool(final["intact"]),
            "entries_at_first_check": before["entries"],
        }
        second.stop()
    return {
        "scope": "Local loopback, one API OS process on a SQLite SQL store, fictional homes "
        "only, no inference. Not production scale, not Azure, not autoscaling or availability "
        "evidence. The load client runs on the same machine.",
        "environment": {
            "python": platform.python_version(),
            "machine": platform.machine(),
            "cpus": os.cpu_count(),
        },
        "declared_workload": scale_load.DECLARED,
        "executed_workload": {
            "homes": homes,
            "events_in_fixture": events,
            "fixture_seed": scale_load.SEED,
            "model": "closed loop (each client sends its next request when the last returns)",
            "request_mix": dict(MIX),
            "meets_declared_workload": False,
            "reason": "Declared 1,800 s open-loop run at 5 requests/s with 600,000 events was "
            "not executed.",
        },
        "fixture_setup_seconds": round(setup_seconds, 1),
        "cold_start_ready_seconds": round(cold_start, 2),
        "declared_limits": scale_load.API_LIMITS,
        "load": load,
        "server_rss": rss,
        "restart": restart,
    }


class SeparateProcessRestart(unittest.TestCase):
    report: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run(homes=150, concurrency=4, seconds=2)

    def test_load_is_recorded_without_overclaiming(self) -> None:
        load = self.report["load"]
        self.assertEqual(load["concurrency"], 4)
        self.assertGreater(load["requests"], 0)
        self.assertEqual(load["errors"], 0)
        self.assertLessEqual(load["p50_ms"], load["p95_ms"])
        self.assertFalse(self.report["executed_workload"]["meets_declared_workload"])
        self.assertIn("Not production scale", self.report["scope"])
        self.assertGreater(self.report["server_rss"]["high_water_mib"], 0)

    def test_declared_fixture_matches_the_scale_run(self) -> None:
        declared = self.report["declared_workload"]
        self.assertEqual((declared["homes"], declared["events"]), (60000, 600000))
        self.assertFalse(declared["inference_per_home"])

    def test_hard_restart_keeps_every_acknowledged_audit_entry(self) -> None:
        restart = self.report["restart"]
        self.assertEqual(restart["acknowledged_calls_before_kill"], CALLS_BEFORE)
        self.assertGreaterEqual(restart["entries_before_kill"], CALLS_BEFORE)
        self.assertEqual(restart["entries_after_restart"], restart["entries_before_kill"])
        self.assertTrue(restart["chain_intact_after_restart"])

    def test_chain_continues_after_restart(self) -> None:
        restart = self.report["restart"]
        self.assertEqual(restart["acknowledged_call_after_restart"], 1)
        self.assertGreater(restart["entries_after_new_write"], restart["entries_after_restart"])
        self.assertTrue(restart["chain_intact_after_new_write"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--homes", type=int, default=scale_load.DECLARED["homes"])
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run(args.homes, args.concurrency, args.seconds)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    restart = report["restart"]
    ok = (
        report["load"]["errors"] == 0
        and restart["chain_intact_after_new_write"]
        and restart["entries_after_restart"] == restart["entries_before_kill"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(main())
    unittest.main()
