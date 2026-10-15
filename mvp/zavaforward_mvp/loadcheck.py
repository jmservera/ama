"""Measured load check against the NFR-002 core workload (synthetic data only).

python -m zavaforward_mvp.loadcheck --data zavaforward.json --homes 60000 --seconds 30

Clones the synthetic programme cases up to --homes labelled synthetic homes, opens the configured store
(ZF_STORE=sqlite by default, mssql for Azure SQL), runs five concurrent sessions with two writers and prints
p50/p95/max per request class against the PRD limits. A local run proves the harness, not Azure sizing.
Cost is not computed here: it needs the Azure meter rates and measured vCore seconds from the Azure run.
"""
import argparse
import copy
import json
import os
import statistics
import tempfile
import threading
import time

LIMITS = {"list": 1.0, "detail": 1.0, "write": 2.0}


def grow(src, homes):
    cases = src["cases"]
    out = list(cases)
    i = 0
    while len(out) < homes:
        c = copy.deepcopy(cases[i % len(cases)])
        c["id"] = f"SYN-{len(out):06d}"
        c["resident"]["name"] = f"Synthetic Resident {len(out)}"
        out.append(c)
        i += 1
    return dict(src, cases=out[:homes] if homes < len(cases) else out)


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))] if xs else 0.0


def run(store, user, seconds, sessions=5, writers=2):
    ids = list(store.cases)
    lat = {k: [] for k in LIMITS}
    errors, lock, stop = [], threading.Lock(), time.time() + seconds

    def session(n):
        writer, i = n < writers, n
        while time.time() < stop:
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
                with lock:
                    lat[kind].append(time.perf_counter() - t)

    threads = [threading.Thread(target=session, args=(n,)) for n in range(sessions)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    rep = {k: dict(n=len(v), p50=round(statistics.median(v), 4) if v else None, p95=round(pct(v, .95), 4),
                   max=round(max(v), 4) if v else None, limit=LIMITS[k], within=pct(v, .95) <= LIMITS[k]) for k, v in lat.items()}
    return dict(classes=rep, errors=len(errors), error_kinds=sorted(set(errors)))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--homes", type=int, default=60000)
    ap.add_argument("--seconds", type=int, default=30)
    a = ap.parse_args(argv)
    with open(a.data, encoding="utf-8") as f:
        src = grow(json.load(f), a.homes)
    with tempfile.TemporaryDirectory() as tmp:
        data = os.path.join(tmp, "load.json")
        with open(data, "w", encoding="utf-8") as f:
            json.dump(src, f)
        from .factory import open_store
        env = dict(os.environ, ZF_DATA=data, ZF_STATE=tmp)
        env.setdefault("ZF_STORE", "sqlite")
        store = open_store(env)
        user = next(s for s in src["staff"] if s["role"] == "Retrofit Programme Manager")
        rep = run(store, user, a.seconds)
    rep.update(homes=a.homes, store=env["ZF_STORE"], seconds=a.seconds, synthetic=True)
    print(json.dumps(rep, indent=2))
    return 0 if rep["errors"] == 0 and all(c["within"] for c in rep["classes"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
