"""Live NFR-002 style load run against the synthetic demo API (issue #114, 2026-11-18).

Reads the Easy Auth session cookie from a Playwright storage-state file (path in argv[1]); never prints it.
Five concurrent sessions, two of them also writers, fixed request mix, warm-up excluded from the figures.
usage: live_load.py STATE.json OUT.json [seconds] [warmup_seconds]
"""

import http.client
import json
import random
import statistics
import sys
import threading
import time
from datetime import datetime, timezone

APP = "ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
LIMITS = {"list": 1.0, "detail": 1.0, "dashboard": 3.0, "write": 2.0}
state = json.load(open(sys.argv[1]))
COOKIE = "; ".join(
    f"{c['name']}={c['value']}"
    for c in state["cookies"]
    if c["domain"].endswith("azurecontainerapps.io")
)
OUT = sys.argv[2]
SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 1800
WARMUP = float(sys.argv[4]) if len(sys.argv) > 4 else 60
HEAD = {"Cookie": COOKIE, "X-ZF-CSRF": "1", "Accept": "application/json"}


def req(conn, method, path, body=None):
    h = dict(HEAD)
    data = None
    if body is not None:
        data = json.dumps(body)
        h["Content-Type"] = "application/json"
    t = time.perf_counter()
    conn.request(method, path, data, h)
    r = conn.getresponse()
    payload = r.read()
    return r.status, time.perf_counter() - t, payload


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, max(0, int(round(p / 100 * len(xs) + 0.5)) - 1))] if xs else None


def main():
    c0 = http.client.HTTPSConnection(APP, timeout=60)
    s, _, b = req(c0, "GET", "/api/cases?limit=50&view=all")
    assert s == 200, s
    ids = [i["id"] for i in json.loads(b)["items"]]
    start = time.time()
    t_warm = start + WARMUP
    end = start + SECONDS
    samples = {k: [] for k in LIMITS}
    errors = {k: [] for k in LIMITS}
    lock = threading.Lock()

    def record(kind, status, dt, measured):
        with lock:
            if measured:
                samples[kind].append(dt)
                if status != 200:
                    errors[kind].append(status)

    def session(n):
        rnd = random.Random(1000 + n)
        writer = n < 2
        conn = http.client.HTTPSConnection(APP, timeout=60)
        i = 0
        while time.time() < end:
            i += 1
            plan = [
                ("list", "/api/cases?limit=50&view=all"),
                ("detail", f"/api/cases/{rnd.choice(ids)}"),
            ]
            if i % 5 == 0:
                plan.append(("dashboard", "/api/progress"))
            for kind, path in plan:
                try:
                    st, dt, _ = req(conn, "GET", path)
                except Exception:
                    conn = http.client.HTTPSConnection(APP, timeout=60)
                    st, dt = 0, 60.0
                record(kind, st, dt, time.time() >= t_warm)
            if writer and i % 6 == 0:
                try:
                    st, dt, _ = req(
                        conn,
                        "POST",
                        f"/api/cases/{rnd.choice(ids)}/call",
                        {
                            "outcome": "No answer",
                            "note": "Synthetic load check issue 114",
                            "channel": "Phone",
                        },
                    )
                except Exception:
                    conn = http.client.HTTPSConnection(APP, timeout=60)
                    st, dt = 0, 60.0
                record("write", st, dt, time.time() >= t_warm)
            time.sleep(rnd.uniform(0.5, 1.5))

    threads = [threading.Thread(target=session, args=(n,)) for n in range(5)]
    started = datetime.now(timezone.utc).isoformat()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    finished = datetime.now(timezone.utc).isoformat()
    report = {}
    for k, xs in samples.items():
        p95 = pct(xs, 95)
        report[k] = dict(
            n=len(xs),
            errors=len(errors[k]),
            p50=round(statistics.median(xs), 4) if xs else None,
            p95=round(p95, 4) if p95 is not None else None,
            max=round(max(xs), 4) if xs else None,
            limit_p95=LIMITS[k],
            ok=bool(xs) and not errors[k] and p95 <= LIMITS[k],
        )
    out = dict(
        started_utc=started,
        finished_utc=finished,
        seconds=SECONDS,
        warmup_seconds=WARMUP,
        sessions=5,
        writers=2,
        classes=report,
        total_measured=sum(v["n"] for v in report.values()),
        all_ok=all(v["ok"] for v in report.values()),
    )
    json.dump(out, open(OUT, "w"), indent=2)
    print(json.dumps(out, indent=2))


main()
