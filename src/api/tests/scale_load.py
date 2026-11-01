"""Scale load run for the staff API over the declared fictional stock (issue 144, NFR-002).

One in-process API replica over the SQL store, fictional homes only, no inference and no
Azure access. The report records what was actually run beside the declared workload and
the usage and cost drivers per unit of load. It is not a production-scale or
autoscaling claim, and cost stays Unknown because no price source is set.

From src/api with installed distributions:
    PYTHONPATH=../core/tests:../agents/tests python3 tests/scale_load.py --out report.json
"""

from __future__ import annotations

import argparse
import contextlib
import itertools
import json
import platform
import random
import resource
import tempfile
import threading
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from test_sqlreads import STAFF, dataset, make_cases
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler

DECLARED = {
    "homes": 60000,
    "events": 600000,
    "sessions": 20,
    "requests_per_second": 5.0,
    "duration_seconds": 1800,
    "inference_per_home": False,
}
THRESHOLDS_MS = {"list": 1000, "detail": 1000, "dashboard": 3000}
# Container limits declared in infra/modules/containerapps.bicep for the API app.
API_LIMITS = {"vcpu": 0.5, "memory_gib": 1.0, "max_replicas": 4}
SEED = 11
THROUGHPUT_TOLERANCE = 0.05
PASSWORD = "zf-scale"
MIX = (("list", 6), ("detail", 3), ("dashboard", 1))


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return round(ordered[min(len(ordered) - 1, int(fraction * len(ordered)))], 1) if ordered else 0


def build_store(directory: Path, homes: int) -> tuple[SqlStore, int]:
    cases = make_cases(homes, seed=SEED)
    for index, case in enumerate(cases):
        # Explicit synthetic marker and a deterministic lifecycle so the dashboard does real work.
        opened = f"2026-0{index % 9 + 1}-1{index % 9}T09:00:00Z"
        case["is_synthetic"] = True
        case["history"] = [dict(action="Identified", at=opened, is_synthetic=True)]
        if case["closed"]:
            case["history"].append(
                dict(
                    action="Withdrawn",
                    at=f"2026-1{index % 3}-2{index % 8}T09:00:00Z",
                    is_synthetic=True,
                )
            )
    events = sum(len(c.get("contacts", [])) + len(c.get("appointments", [])) for c in cases)
    seed = directory / "zavaforward.json"
    seed.write_text(json.dumps(dataset(cases)))
    return SqlStore(str(seed), str(directory / "scale.sqlite")), events


def call(
    base: str, path: str, cookie: str | None = None, body: Any = None
) -> tuple[int, dict[str, str], bytes]:
    request = urllib.request.Request(
        base + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Cookie": cookie} if cookie else {},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read()
            return response.status, dict(response.headers), payload
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()


def run(homes: int, sessions: int, rate: float, duration: float) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="zf-scale-") as tmp, contextlib.ExitStack() as stack:
        started = time.perf_counter()
        store, events = build_store(Path(tmp), homes)
        stack.callback(store.db.close)
        setup_seconds = time.perf_counter() - started
        statements = itertools.count()
        store.db.set_trace_callback(lambda _: next(statements))
        app = App(store, PASSWORD)
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        stack.callback(httpd.server_close)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        stack.callback(httpd.shutdown)
        base = f"http://127.0.0.1:{httpd.server_address[1]}"
        status, headers, _ = call(
            base, "/api/login", body={"email": STAFF[1]["email"], "password": PASSWORD}
        )
        if status != 200:
            raise RuntimeError(f"Staff login failed with {status}.")
        cookie = headers["Set-Cookie"].split(";")[0]
        warmup_ms = {}
        for name, path in (
            ("list", "/api/cases?view=all&limit=50"),
            ("detail", "/api/cases/ZF-00000"),
            ("dashboard", "/api/progress"),
        ):
            begin = time.perf_counter()
            status, _, payload = call(base, path, cookie)
            if status != 200:
                raise RuntimeError(f"Warm-up {name} failed with {status}.")
            if name == "dashboard":
                coverage = json.loads(payload)["coverage"]
                if coverage["synthetic_cases"] != homes or coverage["known_lifecycle"] != homes:
                    raise RuntimeError(f"Dashboard did not cover the requested homes: {coverage}.")
            warmup_ms[name] = round((time.perf_counter() - begin) * 1000, 1)
        statements_before = next(statements)
        cpu_before = resource.getrusage(resource.RUSAGE_SELF)
        samples: dict[str, list[float]] = {name: [] for name, _ in MIX}
        errors: dict[str, int] = {name: 0 for name, _ in MIX}
        lock = threading.Lock()
        failures: list[BaseException] = []
        interval = sessions / rate
        run_started = time.perf_counter()
        deadline = run_started + duration
        in_window = [0]

        def session(index: int) -> None:
            try:
                session_body(index)
            except BaseException as error:
                with lock:
                    failures.append(error)

        def session_body(index: int) -> None:
            rnd = random.Random(index)
            names = [name for name, weight in MIX for _ in range(weight)]
            next_at = run_started + rnd.random() * interval
            while next_at < deadline:
                time.sleep(max(0.0, next_at - time.perf_counter()))
                if time.perf_counter() >= deadline:
                    break
                name = rnd.choice(names)
                if name == "list":
                    offset = rnd.randrange(0, max(1, homes - 49), 50)
                    path = f"/api/cases?view=all&limit=50&offset={offset}"
                elif name == "detail":
                    path = f"/api/cases/ZF-{rnd.randrange(homes):05d}"
                else:
                    path = "/api/progress"
                try:
                    code, _, _ = call(base, path, cookie)
                except OSError:
                    code = 0
                finished = time.perf_counter()
                elapsed = (finished - next_at) * 1000
                with lock:
                    in_window[0] += finished <= deadline
                    samples[name].append(elapsed)
                    errors[name] += code != 200
                next_at += interval

        threads = [threading.Thread(target=session, args=(i,)) for i in range(sessions)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        elapsed = time.perf_counter() - run_started
        drain_seconds = max(0.0, elapsed - duration)
        if failures:
            raise RuntimeError(f"{len(failures)} load session(s) failed.") from failures[0]
        cpu_after = resource.getrusage(resource.RUSAGE_SELF)
        rss_after_mib = round(
            int(Path("/proc/self/statm").read_text().split()[1]) * 4096 / 2**20, 1
        )
        sql_statements = next(statements) - statements_before - 1
    total = sum(len(v) for v in samples.values())
    cpu_seconds = (cpu_after.ru_utime + cpu_after.ru_stime) - (
        cpu_before.ru_utime + cpu_before.ru_stime
    )
    routes = {
        name: {
            "requests": len(values),
            "errors": errors[name],
            "p50_ms": percentile(values, 0.5),
            "p95_ms": percentile(values, 0.95),
            "p99_ms": percentile(values, 0.99),
            "nfr_002_threshold_ms": THRESHOLDS_MS[name],
            "p95_within_threshold": bool(values)
            and percentile(values, 0.95) <= THRESHOLDS_MS[name],
        }
        for name, values in samples.items()
    }
    return {
        "scope": "Local single-process run over fictional data. Not production scale, not "
        "autoscaling or availability evidence, not an Azure measurement.",
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "declared_workload": DECLARED,
        "executed_workload": {
            "homes": homes,
            "events_in_fixture": events,
            "sessions": sessions,
            "target_requests_per_second": rate,
            "duration_seconds": round(duration, 1),
            "observation_window_seconds": round(duration, 1),
            "drain_seconds": round(drain_seconds, 2),
            "in_window_requests": in_window[0],
            "in_window_requests_per_second": round(in_window[0] / duration, 2),
            "throughput_tolerance": THROUGHPUT_TOLERANCE,
            "request_mix": dict(MIX),
            "fixture_seed": SEED,
            "inference_per_home": False,
            "meets_declared_workload": homes >= DECLARED["homes"]
            and events >= DECLARED["events"]
            and sessions >= DECLARED["sessions"]
            and rate >= DECLARED["requests_per_second"]
            and duration >= DECLARED["duration_seconds"]
            and in_window[0] / duration
            >= DECLARED["requests_per_second"] * (1 - THROUGHPUT_TOLERANCE),
        },
        "fixture_setup_seconds": round(setup_seconds, 1),
        "cold_first_request_ms": warmup_ms,
        "routes": routes,
        "cost_drivers": {
            "requests": total,
            "achieved_requests_per_second": round(in_window[0] / duration, 2),
            "assistant_calls": 0,
            "sql_statements": sql_statements,
            "sql_statements_per_request": round(sql_statements / total, 2) if total else 0,
            "replicas": 1,
            "process_cpu_seconds": round(cpu_seconds, 2),
            "rss_after_run_mib": rss_after_mib,
            "peak_rss_mib_including_fixture_build": round(
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1
            ),
            "declared_limits": API_LIMITS,
            "billed_vcpu_seconds_at_limit": round(API_LIMITS["vcpu"] * elapsed, 1),
            "billed_gib_seconds_at_limit": round(API_LIMITS["memory_gib"] * elapsed, 1),
            "cost": "Unknown",
            "cost_note": "No price source or budget is set (BRD OD-51); model cost from these "
            "drivers once a price source exists.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--homes", type=int, default=DECLARED["homes"])
    parser.add_argument("--sessions", type=int, default=DECLARED["sessions"])
    parser.add_argument("--rate", type=float, default=DECLARED["requests_per_second"])
    parser.add_argument("--duration", type=float, default=60)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run(args.homes, args.sessions, args.rate, args.duration)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if any(route["errors"] for route in report["routes"].values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
