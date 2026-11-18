"""Measured load check against the NFR-002 core workload (synthetic data only).

python -m zava_forward.core.synthetic.loadcheck --data zavaforward.json --homes 60000 --seconds 30

Clones the synthetic programme cases up to --homes labelled synthetic homes, opens the configured store
(ZF_STORE=sqlite by default, mssql for Azure SQL), runs five concurrent sessions with two writers and prints
p50/p95/max per request class against the PRD limits alongside a structured cost section. A local run proves
the harness, not Azure sizing. When Azure meter rate or measured vCore seconds are omitted, cost is reported
honestly as "Unknown" with missing_inputs and azure_live_run_human_gated=True.
"""
import argparse
import copy
from decimal import Context, Decimal, localcontext
import json
import math
import os
import statistics
import sys
import tempfile
import threading
import time
from typing import Any

LIMITS = {"list": 1.0, "detail": 1.0, "write": 2.0}


def _validate_cost_number(name: str, value: float | None, *, positive: bool = False) -> float | None:
    if value is None:
        return None
    qualifier = "positive" if positive else "non-negative"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite {qualifier} number")
    if not -sys.float_info.max <= value <= sys.float_info.max:
        raise ValueError(f"{name} must be a finite {qualifier} number")
    fval = float(value)
    if not math.isfinite(fval) or (fval <= 0.0 if positive else fval < 0.0):
        raise ValueError(f"{name} must be a finite {qualifier} number")
    return 0.0 if fval == 0.0 else fval


def evaluate_cost(
    vcore_seconds: float | None = None,
    meter_rate_per_vcore_second: float | None = None,
    target_cost: float | None = None,
) -> dict[str, Any]:
    vc = _validate_cost_number("vcore_seconds", vcore_seconds, positive=False)
    rate = _validate_cost_number("meter_rate_per_vcore_second", meter_rate_per_vcore_second, positive=True)
    target = _validate_cost_number("target_cost", target_cost, positive=False)
    missing_inputs: list[str] = []
    if vc is None:
        missing_inputs.append("vcore_seconds")
    if rate is None:
        missing_inputs.append("meter_rate_per_vcore_second")
    if target is None:
        missing_inputs.append("target_cost")
    if vc is None or rate is None:
        return dict(
            status="Unknown",
            vcore_seconds=vc,
            meter_rate_per_vcore_second=rate,
            measured_cost=None,
            target_cost=target,
            within_target=None,
            missing_inputs=missing_inputs,
            azure_live_run_human_gated=True,
        )
    with localcontext(Context(prec=60)):
        raw = Decimal(str(vc)) * Decimal(str(rate))
        measured_cost = 0.0 if raw == 0 else float(raw)
        if not math.isfinite(measured_cost) or (raw > 0 and measured_cost == 0.0):
            raise ValueError("measured_cost must be a representable finite number")
        within_target = bool(raw <= Decimal(str(target))) if target is not None else None
    return dict(
        status="measured",
        vcore_seconds=vc,
        meter_rate_per_vcore_second=rate,
        measured_cost=measured_cost,
        target_cost=target,
        within_target=within_target,
        missing_inputs=missing_inputs,
        azure_live_run_human_gated=True,
    )


def grow(src: dict[str, Any], homes: int) -> dict[str, Any]:
    if type(homes) is not int or homes <= 0:
        raise ValueError("homes must be a positive integer")
    cases = src["cases"]
    if not cases:
        raise ValueError("load check requires at least one case")
    out = list(cases)
    i = 0
    while len(out) < homes:
        c = copy.deepcopy(cases[i % len(cases)])
        c["id"] = f"SYN-{len(out):06d}"
        c["resident"]["name"] = f"Synthetic Resident {len(out)}"
        out.append(c)
        i += 1
    return dict(src, cases=out[:homes] if homes < len(cases) else out)


def pct(xs: list[float], p: float) -> float | None:
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))] if xs else None


def run(
    store: Any,
    user: dict[str, Any],
    seconds: float,
    sessions: int = 5,
    writers: int = 2,
    *,
    vcore_seconds: float | None = None,
    meter_rate_per_vcore_second: float | None = None,
    target_cost: float | None = None,
) -> dict[str, Any]:
    if isinstance(seconds, bool) or not 0 < seconds <= sys.float_info.max:
        raise ValueError("seconds must be finite and positive")
    if type(sessions) is not int or sessions <= 0:
        raise ValueError("sessions must be a positive integer")
    if type(writers) is not int or not 1 <= writers <= sessions:
        raise ValueError("writers must be an integer between 1 and sessions")
    cost = evaluate_cost(
        vcore_seconds=vcore_seconds,
        meter_rate_per_vcore_second=meter_rate_per_vcore_second,
        target_cost=target_cost,
    )
    ids = list(store.cases)
    if not ids:
        raise ValueError("load check requires at least one case")
    lat = {k: [] for k in LIMITS}
    errors, lock, stop = [], threading.Lock(), time.monotonic() + seconds

    def session(n):
        try:
            writer, i = n < writers, n
            while time.monotonic() < stop:
                cid = ids[(i * 7919) % len(ids)]
                i += sessions
                for kind, fn in (("list", lambda: store.page_cases(user, "mine", limit=50)),
                                 ("detail", lambda: store.detail(cid, user)),
                                 ("write", lambda: store.log_call(user, cid, "Load check call", ""))):
                    if kind == "write" and not writer:
                        continue
                    t = time.perf_counter()
                    try:
                        fn()
                    except Exception as e:
                        with lock:
                            errors.append(f"{kind}: {type(e).__name__}")
                        continue
                    elapsed = time.perf_counter() - t
                    with lock:
                        lat[kind].append(elapsed)
        except Exception as e:
            # Thread exceptions do not propagate through join().
            with lock:
                errors.append(f"session: {type(e).__name__}")

    threads = []
    for n in range(sessions):
        t = threading.Thread(target=session, args=(n,))
        try:
            t.start()
        except RuntimeError as e:
            with lock:
                errors.append(f"startup: {type(e).__name__}")
        else:
            threads.append(t)
    [t.join() for t in threads]
    rep = {}
    for k, v in lat.items():
        p95 = pct(v, .95)
        rep[k] = dict(n=len(v), p50=round(statistics.median(v), 4) if v else None,
                      p95=round(p95, 4) if p95 is not None else None,
                      max=round(max(v), 4) if v else None, limit=LIMITS[k],
                      within=p95 is not None and p95 <= LIMITS[k])
    total_requests = sum(c["n"] for c in rep.values())
    load = dict(
        sessions=sessions,
        writers=writers,
        seconds=seconds,
        total_requests=total_requests,
        achieved_rps=round(total_requests / float(seconds), 4),
    )
    return dict(
        classes=rep,
        load=load,
        cost=cost,
        errors=len(errors),
        error_kinds=sorted(set(errors)),
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--homes", type=int, default=60000)
    ap.add_argument("--seconds", type=int, default=30)
    ap.add_argument("--vcore-seconds", type=float, default=None)
    ap.add_argument("--meter-rate", type=float, default=None)
    ap.add_argument("--cost-target", type=float, default=None)
    a = ap.parse_args(argv)
    if not 0 < a.seconds <= sys.float_info.max:
        ap.error("seconds must be finite and positive")
    if a.homes <= 0:
        ap.error("homes must be a positive integer")
    try:
        evaluate_cost(
            vcore_seconds=a.vcore_seconds,
            meter_rate_per_vcore_second=a.meter_rate,
            target_cost=a.cost_target,
        )
    except ValueError as e:
        ap.error(str(e))
    with open(a.data, encoding="utf-8") as f:
        src = json.load(f)
    try:
        src = grow(src, a.homes)
    except ValueError as e:
        ap.error(str(e))
    with tempfile.TemporaryDirectory() as tmp:
        data = os.path.join(tmp, "load.json")
        with open(data, "w", encoding="utf-8") as f:
            json.dump(src, f)
        from zava_forward.core.factory import open_store
        env = dict(os.environ, ZF_DATA=data, ZF_STATE=tmp)
        env.setdefault("ZF_STORE", "sqlite")
        store = open_store(env)
        user = next(s for s in src["staff"] if s["role"] == "Retrofit Programme Manager")
        rep = run(
            store,
            user,
            a.seconds,
            vcore_seconds=a.vcore_seconds,
            meter_rate_per_vcore_second=a.meter_rate,
            target_cost=a.cost_target,
        )
    rep.update(homes=a.homes, store=env["ZF_STORE"], seconds=a.seconds, synthetic=True)
    print(json.dumps(rep, indent=2))
    cost_ok = rep["cost"]["within_target"] is not False
    return 0 if rep["errors"] == 0 and all(c["within"] for c in rep["classes"].values()) and cost_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
